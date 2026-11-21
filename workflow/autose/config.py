"""Every fixed number and name the workflow uses, in one place.

Values come from the ADRs. If a run shows a value is wrong, the ADR is superseded
and the value is changed here, so the git history shows both.
"""

REPO = "sulphatet/autose-a3-markdown"
LABEL = "autose"
STATE_BRANCH = "autose-state"
BRANCH_PREFIX = "autose/issue-"

# ADR-006: models
BUILDER_MODEL = "gemini-3.5-flash-lite"
REVIEWER_MODEL = "gemini-3.1-flash-lite"
TEMPERATURE = 0.2

# ADR-002: loop budgets
MAX_IMPL_ATTEMPTS = 3        # per design
MAX_REDESIGNS = 1            # after test failures
MAX_TEST_WRITES = 2          # ADR-011: test-file problems go back to the tester
MAX_REVIEW_ROUNDS = 2
FORMAT_RETRIES = 1           # ADR-007: a format-only failure goes back once

# ADR-009: budgets
MAX_TURNS = 40
MAX_REPEATS = 3
RUN_TOKEN_BUDGET = 2_000_000
COMMAND_TIMEOUT = 300
CI_TIMEOUT = 30 * 60
TOOL_OUTPUT_LIMIT = 12_000
RETRY_DELAYS = [5, 10, 20, 40, 80]

# ADR-003: removed from the working copy before any agent runs
ASSIGNMENT_PATHS = ["architecture", "experiment", "workflow", "results",
                    "report.pdf", "demo.mp4", "README.md"]

# ADR-005: where each role may write
WRITE_PATHS = {
    "implementer": ["markdown/", "docs/changelog.md"],
    "tester": ["tests/test_autose_"],
}

# ADR-009: the diff may never touch these
FORBIDDEN_DIFF_PATHS = [".github/", "pyproject.toml"] + [p if "." in p else p + "/" for p in ASSIGNMENT_PATHS]

PROMPT_VERSION = "2"
