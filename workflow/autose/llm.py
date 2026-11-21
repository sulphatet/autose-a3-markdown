"""Minimal Gemini REST client: retries, token counting. No SDK (ADR-006, ADR-009)."""

import json
import os
import random
import time
import urllib.error
import urllib.request

from . import config

API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
RETRY_STATUS = {429, 500, 502, 503, 504}

# Read once and removed from the environment, so commands that agents run
# cannot inherit it (ADR-005).
_KEY = os.environ.pop("GEMINI_API_KEY", None)


class ModelUnavailable(Exception):
    pass


class TokenBudgetExceeded(Exception):
    pass


class Usage:
    """Counts tokens per model for the whole run (reported per the rules)."""

    def __init__(self, budget=config.RUN_TOKEN_BUDGET):
        self.budget = budget
        self.by_model = {}
        self.calls = 0

    def add(self, model, meta):
        m = self.by_model.setdefault(model, {"prompt": 0, "output": 0, "total": 0})
        m["prompt"] += meta.get("promptTokenCount", 0)
        m["output"] += meta.get("candidatesTokenCount", 0) + meta.get("thoughtsTokenCount", 0)
        m["total"] += meta.get("totalTokenCount", 0)
        self.calls += 1

    @property
    def total(self):
        return sum(m["total"] for m in self.by_model.values())

    def check(self):
        if self.total > self.budget:
            raise TokenBudgetExceeded(f"run used {self.total} tokens, budget {self.budget}")

    def to_dict(self):
        return {"calls": self.calls, "total": self.total, "by_model": self.by_model}


def generate(model, system, contents, tools, usage, force_tool=True):
    """One generateContent call. Returns (content, finish_reason, model_version)."""
    if not _KEY:
        raise ModelUnavailable("GEMINI_API_KEY is not set")
    usage.check()
    body = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": contents,
        "generationConfig": {"temperature": config.TEMPERATURE},
    }
    if tools:
        body["tools"] = [{"functionDeclarations": tools}]
        if force_tool:
            body["toolConfig"] = {"functionCallingConfig": {"mode": "ANY"}}
    data = json.dumps(body).encode()
    last = None
    for attempt, delay in enumerate([0] + config.RETRY_DELAYS):
        if delay:
            time.sleep(delay + random.uniform(0, delay / 2))
        req = urllib.request.Request(
            API.format(model=model), data=data, method="POST",
            headers={"Content-Type": "application/json", "x-goog-api-key": _KEY})
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                out = json.load(resp)
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read()[:300].decode(errors='replace')}"
            if e.code in RETRY_STATUS:
                continue
            raise ModelUnavailable(last)
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last = f"network: {e}"
            continue
        usage.add(model, out.get("usageMetadata", {}))
        cands = out.get("candidates") or []
        if not cands:
            last = f"no candidates: {json.dumps(out.get('promptFeedback', {}))[:300]}"
            continue
        cand = cands[0]
        content = cand.get("content") or {"role": "model", "parts": []}
        content.setdefault("role", "model")
        content.setdefault("parts", [])
        return content, cand.get("finishReason", ""), out.get("modelVersion", model)
    raise ModelUnavailable(f"{model} failed after {len(config.RETRY_DELAYS) + 1} attempts; last error {last}")
