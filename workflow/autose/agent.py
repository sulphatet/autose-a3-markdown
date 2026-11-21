"""The agent loop shared by every role (ReAct-style: think, call a tool, observe).

The loop ends when the agent calls `submit`. Budgets are enforced here
(ADR-009): turn limit, repeated identical calls, run token budget.
"""

import json
import time
from pathlib import Path

from . import config, llm


class AgentStopped(Exception):
    """The agent could not finish within its budget. The message is the reason."""


def submit_decl(description, props, required):
    return {"name": "submit", "description": description,
            "parameters": {"type": "object", "properties": props, "required": required}}


def run_agent(role, model, system, user, toolset, usage, log_path, max_turns=config.MAX_TURNS,
              validate=None):
    """Run one agent to completion. Returns the arguments it passed to `submit`.

    `validate(args)` may return an error string; the agent then gets one chance
    per call to fix its submission (format retries, ADR-007).
    """
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log = log_path.open("a")

    def record(kind, data):
        log.write(json.dumps({"t": round(time.time(), 1), "role": role, "kind": kind, "data": data}) + "\n")
        log.flush()

    contents = [{"role": "user", "parts": [{"text": user}]}]
    record("input", {"model": model, "system_chars": len(system), "user": user[:20000]})
    last_sig, repeats, format_failures = None, 0, 0
    try:
        for turn in range(1, max_turns + 1):
            try:
                content, finish, version = llm.generate(model, system, contents, toolset.decls, usage)
            except llm.TokenBudgetExceeded as e:
                raise AgentStopped(str(e))
            except llm.ModelUnavailable as e:
                raise AgentStopped(f"model unavailable: {e}")
            parts = content.get("parts", [])
            record("model", {"turn": turn, "finish": finish, "version": version,
                             "parts": [p for p in parts if "thoughtSignature" not in p or len(p) > 1]})
            calls = [p["functionCall"] for p in parts if "functionCall" in p]
            if not calls:
                # MALFORMED_FUNCTION_CALL or plain text: ask again, do not keep the empty turn
                contents.append(content if parts else {"role": "model", "parts": [{"text": "(no output)"}]})
                contents.append({"role": "user", "parts": [{"text":
                                 "You must respond by calling one of the tools. Call `submit` when you are done."}]})
                continue
            contents.append(content)
            responses = []
            for c in calls:
                name, args = c.get("name"), c.get("args") or {}
                if name == "submit":
                    err = validate(args) if validate else None
                    if not err:
                        record("submit", args)
                        return args
                    format_failures += 1
                    record("submit_rejected", {"error": err})
                    if format_failures > config.FORMAT_RETRIES + 1:
                        raise AgentStopped(f"submission still invalid after retries: {err}")
                    result = f"SUBMISSION REJECTED: {err}\nFix the problem and call submit again."
                else:
                    sig = json.dumps([name, args], sort_keys=True)
                    repeats = repeats + 1 if sig == last_sig else 1
                    last_sig = sig
                    if repeats >= config.MAX_REPEATS:
                        raise AgentStopped(f"stuck: called {name} with the same arguments {repeats} times in a row")
                    result = toolset.call(name, args)
                record("tool", {"name": name, "args": _short(args), "result": result[:4000]})
                fr = {"name": name, "response": {"result": result}}
                if c.get("id"):
                    fr["id"] = c["id"]
                responses.append({"functionResponse": fr})
            contents.append({"role": "user", "parts": responses})
        raise AgentStopped(f"turn budget used up ({max_turns} turns) without submitting")
    except AgentStopped as e:
        record("stopped", {"reason": str(e)})
        raise
    finally:
        log.close()


def _short(args):
    return {k: (v[:1500] + "..." if isinstance(v, str) and len(v) > 1500 else v) for k, v in args.items()}
