---
name: swe-devops-standards
description: >-
  Always invoke to review, repair, or deliver geospatial or GeoAI code,
  including contract compliance, security, error handling, transactions,
  tests, scripts, functions, notebooks, packages, CI/CD, and repository
  changes, even when deployment is not requested. Pair with the domain skill
  for ETL and other production code. Covers CRS/data invariants, dependencies,
  cross-platform reproducibility, automation, and shipping. Do not trigger for
  unrelated software or analysis requesting no code or repository artifact.
license: MIT
metadata:
  author: Muhammed Enes Duran
---

# Geospatial SWE & DevOps Standards

Purpose: code produced as part of geospatial work should run in the user's
real environment and meet peer-level engineering quality. Apply these rules
only when code or repository artifacts are in scope.

## 1. Environment realities (the top error source)

- **Script-first by default**: no `%matplotlib inline`, `!pip install`, or
  `display()` unless the user is explicitly in a notebook. Every file runs
  from a terminal via `python script.py` behind an
  `if __name__ == "__main__":` block. (Cell markers like `# %%` are fine
  as an addition — the script must also work without them.)
- **Cross-platform paths**: always `pathlib.Path`; never string-concatenate
  or hardcode `/` or `\\`. Ask or detect the user's OS before giving shell
  commands; give CMD/PowerShell syntax on Windows, POSIX elsewhere —
  don't mix (`export` vs `set`, `venv/bin/activate` vs
  `venv\Scripts\activate`).
- **Encodings**: explicit `encoding="utf-8"` on every text file open —
  Windows still defaults to legacy code pages, and non-ASCII content
  corrupts silently.
- **Modern Python (3.11+)**: `X | None` unions, `type` aliases, structural
  pattern matching where they clarify; state the minimum version if a
  feature requires it.

## 2. Code quality defaults

Applied to every generated function/module, even when not asked:

```python
def compute_share(values: list[float], total: float) -> list[float]:
    """Return each value's share of the total.

    Args:
        values: Values to compute shares for.
        total: Denominator; must be non-zero.

    Returns:
        Shares in the same order as values.

    Raises:
        ValueError: If total is zero.
    """
    if total == 0:
        raise ValueError("total must be non-zero — share is undefined.")
    return [v / total for v in values]
```

- Type hints on every signature; `dataclass`/`TypeAlias` for complex types.
- Google-style docstrings; one-liners suffice for trivial functions.
- **Never bare `except:`**; catch specific exceptions, handle or re-raise
  with `raise ... from e`. A silent `pass` costs a week of debugging.
- `logging` over `print` (leveled, formatted), except user-facing CLI
  output.
- Note algorithmic complexity where it matters ("this is O(n log n), safe
  at n>10⁶") — especially around nested loops and pandas `apply`.
- Magic numbers → named module-level constants.

## 3. Testing and verification

- Offer at least a skeleton pytest for every function carrying real logic:

```python
# test_compute.py — run: python -m pytest -q
import pytest
from compute import compute_share

def test_basic() -> None:
    assert compute_share([1, 1], 2) == [0.5, 0.5]

def test_zero_total_raises() -> None:
    with pytest.raises(ValueError):
        compute_share([1.0], 0)
```

- Numerical code: test edge cases — empty input, NaN, negatives, single
  element.
- Run generated code yourself when an execution environment exists;
  otherwise mark it explicitly "not executed" — no silent assumptions.

## 4. Dependencies and reproducibility

- New project → virtual environment + pinned `requirements.txt`
  (`package==version`); never "install the latest".
- Seed randomness and put the seed in config (details in
  `ml-experiment-standards`).
- Note environment-difference risks where relevant (BLAS, CUDA, locale).

## 5. Git practices

- Conventional Commits: `feat(scope): ...`, `fix: ...`, `refactor: ...`;
  the body explains *why* — the diff already shows *what*.
- Commit in meaningful units; warn against 500-line single commits.
- Default `.gitignore`: `venv/`, `__pycache__/`, `*.pyc`, large data files
  (suggest DVC/LFS), IDE folders.

## 6. Automation / DevOps

- **CI**: minimal GitHub Actions for test + lint (ruff); note OS-runner
  differences if jobs must run on Windows too.
- **Docker**: start from `python:3.12-slim`, simple single-stage until
  size/caching demands more; note image size and build-cache implications.
- **Monitoring**: any long-lived service/pipeline ships three signals
  minimum: structured logs, failure alerting, basic metrics (duration,
  volume). ML services add drift checks (see `ml-experiment-standards`).
- **Scheduled jobs**: match the user's platform — cron on POSIX,
  Task Scheduler (`schtasks`) on Windows.

## 7. Code review mode

Review in this order and report findings by severity: correctness (edge
cases, silent failures) → security (injection, secrets, path traversal) →
performance (N+1, needless copies, O(n²)) → readability. Every finding
ships with the suggested fix as code — never "this is bad" and nothing
else.

## Execution contract

- **Workflow:** clarify the geospatial code's contract; reproduce the environment; inspect correctness and data invariants; implement the smallest safe change; test; package; document operations and rollback.
- **Decision rules:** apply this skill to geospatial software and pipeline delivery, not generic non-spatial coding; scale CI, containers, and observability to the actual deployment risk.
- **Verification protocol:** run focused and regression tests, lint and type checks where configured, exercise CRS/nodata/geometry edge cases, verify clean installation, and review CI artifacts.
- **Failure modes:** block release for silent data loss, nondeterminism, mutable hidden state, unpinned critical dependencies, secrets, platform assumptions, missing rollback, or unhandled spatial edge cases.
- **Deliverables:** reviewed code, tests, reproducible environment and lock data, CI configuration, operational notes, risk-ranked findings, observability plan, and rollback instructions.
- **Source freshness:** consult [the authoritative source registry](references/authoritative-sources.md) before applying packaging, CI, testing, or supply-chain guidance.
