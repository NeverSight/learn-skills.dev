---
name: python-style
description: Enforce consistent Python typing (type hints + return types), concise Google-style docstrings, PEP 8/Black formatting, and unit tests when creating or editing Python code. Use when working on .py files, Python APIs, refactors, or bug fixes where maintainability and correctness matter.
compatibility: Cursor Agent Skills (nightly). Assumes Python 3.10+; prefers black/ruff/mypy/pytest if already configured in-repo.
metadata:
  author: janjaszczak
  version: "1.0"
---

# Python Style & Quality Gate (Typing • Docstrings • PEP 8/Black • Tests)

## Purpose
When writing or modifying Python, apply a “quality gate” aligned to this rule-set:
- Use type hints consistently (including return types), prefer `from __future__ import annotations`.
- Write concise docstrings for public modules/classes/functions (one-line summary + key params/returns/raises) in Google style.
- Follow PEP 8; Black formatting; keep functions small and cohesive.
- Provide unit tests that exercise the documented behavior and typed signatures.

## When to activate
Activate this skill when:
- Editing/creating `**/*.py`, or
- The user requests: typing, annotations, docstrings, PEP 8, Black, refactor-for-clarity, unit tests, pytest.

## Guardrails
- Minimize blast radius: do NOT reformat or refactor unrelated files unless the user asks.
- Preserve runtime behavior unless explicitly asked to change it.
- Prefer repo conventions over personal preference:
  - If the repo already uses ruff/mypy/pytest/unittest/isort/black settings, follow those.
  - If no tooling is present, default to Black-compatible formatting and pytest-style tests.

## Workflow (agent-operational)
1) **Clarify (0–3 questions max)** only if needed:
   - Target Python version? (or infer from `pyproject.toml`, `tox.ini`, CI)
   - Test framework in use (pytest vs unittest)?
   - Any strict typing expectations (mypy strict, pyright, etc.)?

2) **Dynamic context discovery**
   - Locate and follow existing style/tooling:
     - `pyproject.toml`, `setup.cfg`, `tox.ini`, `.ruff.toml`, `mypy.ini`, CI config.
   - Find canonical patterns in-code (similar modules, existing docstring style, existing test structure).

3) **Plan before large edits**
   - For multi-file refactors or public API changes, write a short plan with:
     - Files to touch
     - Small incremental steps
     - Verification steps (commands to run)

4) **Implement (incremental)**
   - Add/fix annotations for all params and return types.
     - Avoid `Any` unless truly unavoidable; if used, explain why and consider narrower types.
     - Prefer precise unions, protocols, generics, and typed collections.
   - Add `from __future__ import annotations` in new modules; in existing modules, follow repo pattern.
   - Ensure functions are small and cohesive; if a function is multi-purpose, propose (or perform) a small refactor into smaller units.

5) **Docstrings (public surfaces)**
   - Public module/class/function docstrings should be concise:
     - One-line summary (imperative mood)
     - Google style sections as needed:
       - Args / Returns / Raises
   - Keep docstrings aligned with real behavior and current signature.

6) **Tests**
   - Add or update unit tests to cover:
     - Core behavior
     - Edge cases implied by types/docs
     - Error paths (especially documented `Raises`)
   - Prefer targeted tests (fast, deterministic). Mirror existing repo testing patterns.

7) **Verification**
   - Run the most relevant checks available in the repo (in this order if present):
     - Formatter/linter (black/ruff)
     - Type checker (mypy/pyright)
     - Unit tests (pytest/unittest)
   - If tools are missing, state what you *would* run and why.

## Output expectations (what “done” looks like)
- All touched Python functions have explicit param + return annotations.
- Public API surfaces have up-to-date concise Google-style docstrings.
- Formatting is Black/PEP8-consistent (or consistent with repo tooling).
- Tests exist/updated and meaningfully cover the changed behavior.

## Common edge cases
- Legacy codebases without typing:
  - Add types incrementally; prioritize touched surfaces and high-value boundaries.
- Dynamic/duck-typed areas:
  - Prefer `Protocol`, `TypedDict`, `Mapping[str, Any]` (as last resort), or narrow `Any` usage with justification.
- Performance-sensitive paths:
  - Avoid heavy runtime validation; keep typing mostly static.

## Examples

### Example: function update
**Input request:** “Add a helper to parse an ISO date string and update callers.”

**Expected actions:**
- Create `parse_iso_date(value: str) -> datetime.date`
- Add docstring documenting accepted formats and raises
- Add tests for valid date, invalid date, boundary cases
- Update callers with correct types

### Example: refactor prompt
If a function violates cohesion (multiple responsibilities), propose:
- Extract 1–3 smaller helpers with tight types
- Keep behavior identical
- Add tests around the original public entrypoint
