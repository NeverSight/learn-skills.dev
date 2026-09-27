---
name: ac-python
description: Generic Python coding guidelines covering style, typing, OOP design, testing, and tooling. Use when writing Python code outside of a Django context — scripts, CLIs, microservices, data pipelines, tooling. Do NOT use for Django-specific patterns (use ac-django instead).
compatibility: python3. Knowledge-only skill with no external tool requirements beyond a Python codebase.
metadata:
  version: 0.1.0
  subagent_safe: true
---

# Python Bible (Python 3.14)

**Targets:** Python **3.14** · **Previous line:** Python **3.13** (trailing section) · **Tooling:** uv · ruff · mypy/ty · prek · pytest

## Version Policy

This skill documents **one** Python line: the current one. Keep it that way when
you update it.

- **Main path = the current feature release.** Today that is Python **3.14**. When
  3.15 ships, the main path moves to it in the same edit.
- **Unmarked prose means the current line, and there is no marker form.** Python
  ships features only in a feature release, and the main path always *is* the
  current feature release — so nothing in it can post-date the line, and a version
  suffix would have nothing to qualify. (This is where the sibling `ac-django`
  policy differs: Django adds features *within* a line, so it needs version
  markers; Python does not.) Do not write "On Python 3.X+, ..." or "if you are on
  3.13" in the main path — a conditional in the main path is the defect this rule
  exists to stop.
- **Older lines get one trailing section each, at the end of `SKILL.md`**, and
  nothing anywhere else — the reference files carry the current line only and get
  no trailing section of their own. Today that is `## Previous line: Python 3.13`.
  It carries the diff a reader on that version needs: what is missing, what to
  use instead, and what to change on upgrade.
- **Research order when refreshing.** `https://docs.python.org/3/whatsnew/` and
  the library reference first. Then the sources already cited under Canonical
  Sources. Blogs and newsletters last, briefly, for what the docs do not cover.
- **Rotation.** Each October a new line ships: re-base unmarked prose on it,
  replace the trailing section with the line being retired, drop stale markers.

## Canonical Sources

- Python docs: <https://docs.python.org/3/>
- Ruff docs: <https://docs.astral.sh/ruff/>
- uv docs: <https://docs.astral.sh/uv/>
- mypy docs: <https://mypy.readthedocs.io/>
- pytest docs: <https://docs.pytest.org/>
- Typer (CLI): <https://typer.tiangolo.com/>

## Reference Files (load as needed)

| File | Covers | When to load |
| --- | --- | --- |
| [`references/style-and-typing.md`](references/style-and-typing.md) | Style, Pythonic idioms, type annotations, readability rules | Writing or reviewing any Python code |
| [`references/oop-and-design.md`](references/oop-and-design.md) | OOP patterns, data models, factories, properties, design principles | Designing classes, data models, module structure |
| [`references/testing-and-tooling.md`](references/testing-and-tooling.md) | Testing patterns, pytest setup, tooling (uv/ruff/mypy/prek), quality gates | Writing tests, setting up a project, CI |

## Dependencies

Standalone. No dependencies on other skills.

When used alongside ac-django, provides generic Python guidelines that complement Django-specific patterns.

## Trigger QA (Release Gate)

Before shipping skill changes, validate activation behavior with sample prompts:

- Should trigger:
  - "Write a CLI script that processes CSV files."
  - "Review this Python class for design issues."
  - "Set up testing for this Python microservice."
- Should NOT trigger:
  - "Add a Django model field and migration."
  - "Set up git worktrees for a ticket."
  - "Implement project delivery workflow."

If behavior under-triggers or over-triggers, tighten `description` cues before release.

## Example: Adding a new data model

User says: "Add a `LoanApplication` data model with validation"

1. Load [`references/oop-and-design.md`](references/oop-and-design.md) for data model patterns
2. Load [`references/style-and-typing.md`](references/style-and-typing.md) for typing conventions
3. Use a dataclass or attrs/pydantic if the project already uses them
4. Add full type annotations, use `@cached_property` for derived attributes
5. Name the factory `build_loan_application(...)` if needed in tests
6. Mirror the module path in `tests/` for the test file

## Prime Directives

### Pythonic first

- Prefer the idiomatic Python solution over a generic one.
- Use list comprehensions, walrus operator (`:=`), `itertools`, `operator` where they clarify intent.
- Avoid intermediate variables that are only used once.
- Prefer t-strings (`t"..."`, PEP 750) over f-strings when building SQL, HTML, shell commands, or templates from interpolated values. A t-string evaluates to a `string.templatelib.Template`, not a `str`: the static text and each `Interpolation` stay separable, so a processing function can escape every interpolated value for its target grammar. The safety is in that function — the stdlib ships none, so use a library's or write one. A `Template` passed where a `str` is expected is an error, not an escape.
- Use the stdlib `compression.zstd` for zstd rather than the third-party `zstandard` package. `compression.lzma`, `compression.bz2`, `compression.gzip` and `compression.zlib` are the preferred import names for those modules too; the originals still work and are not deprecated. `tarfile`, `zipfile` and `shutil` read and write zstd archives.
- Omit the brackets in a multi-type `except` when there is no `as` clause (PEP 758): `except TimeoutError, ConnectionRefusedError:`. With `as`, the brackets are still required.
- Never `return`, `break`, or `continue` out of a `finally` block — it swallows the in-flight exception, and the compiler emits a `SyntaxWarning` for it (PEP 765).

### Types are documentation

- Full, modern annotations everywhere: `list[str]`, `str | None`, `dict[str, int]`.
- Use the `type` statement for recurring complex types.
- No duck-typing: if you are checking for attribute existence before acting, the type hint is too broad — narrow it.

### No docstrings — names are the docs

- Use short, expressive function and variable names.
- Comment ONLY the non-obvious WHY. Never restate the code; never write a signature-echo docstring.
- A long comment is a code smell — refactor or rename instead of explaining. Multi-line comments are legit only for a genuine non-obvious why, never to narrate the code.
- Use vertical whitespace to group related lines.

### Clean imports

- All `import` statements at the top of the file.
- No function-level imports, no `try...except ImportError` guards. (Repo-specific conventions may relax this for established circular-import patterns.)
- Assume all dependencies are installed.

### No dirty hacks

- Pick the straightforward solution. If it doesn't exist, reconsider the design.
- Do not fight third-party frameworks — follow their intended patterns.

## Review Checklist

### Style

- [ ] no single-use intermediate variables
- [ ] list comprehensions / stdlib idioms used where appropriate
- [ ] vertical whitespace groups related logic

### Typing

- [ ] full modern annotations on all public functions and methods
- [ ] `type` statement used for complex/recurring types
- [ ] no duck-typing (no `hasattr` guards in place of proper types)

### Imports

- [ ] all imports at top of file
- [ ] no `try...except ImportError` blocks
- [ ] no function-level imports

### OOP / Design

- [ ] data models are first-class (not plain dicts passed around)
- [ ] factories named `build_...`
- [ ] application logic in methods, not module-scope functions
- [ ] `@property` / `@cached_property` for derived attributes

### Best Practices

- [ ] UTC timezone-aware datetimes throughout
- [ ] boolean params preceded by `, *,`
- [ ] `try` blocks and context managers are minimal (ideally one line each)

### Architectural Health (Module-Level)

Apply to **full files** touched by the diff, not just changed lines:

- [ ] no module with >500 LOC (split by concern)
- [ ] no module with >10 module-level functions (use classes)
- [ ] module-level functions are justified — default is methods on a class
- [ ] no god-module (single file mixing unrelated concerns — CLI wiring + business logic + subprocess management = split)
- [ ] no complexity rule suppressions (`C901`, `PLR09xx`) in `pyproject.toml` beyond the `python-boilerplate` baseline
- [ ] tests assert behavior through public interfaces, not by patching private functions or asserting subprocess command lists

### Testing

#### Integration-First Testing (Non-Negotiable)

Write **integration tests for happy paths, unit tests for edge cases.** This maximizes confidence per line of test code.

- **Integration tests** exercise multiple modules together with real (or near-real) I/O. They catch the bugs that matter most: broken contracts between modules, wrong assumptions about state, ordering issues. Mock only what you cannot control (network, external processes, databases).
- **Unit tests** target specific functions in isolation — but only when the function has edge cases worth covering (error handling, boundary values, complex branching). Don't unit-test trivial glue code.
- **Don't duplicate coverage.** If a happy path is already covered by an integration test, don't write a unit test for the same path. Unit tests should cover what integration tests cannot reach efficiently (rare error branches, corner cases).
- **E2E tests** (browser, full-stack) are separate — they belong in frontend/application test suites, not in library or infrastructure code. Write them when testing user-visible behavior end-to-end.

#### Test Conciseness (Non-Negotiable)

Tests must be easy to read and maintain. Verbose tests get skimmed, misunderstood, and copy-pasted without thought.

- **One assertion per concept.** A test method should test one behavior. Multiple assertions are fine when they verify different facets of the same behavior.
- **Use fixtures for setup, not copy-paste.** Repeated setup code across test methods means a missing fixture or parametrize.
- **Parametrize over copy-paste.** When multiple tests differ only in input/output values, use `@pytest.mark.parametrize`. Five test methods that differ by one string are one parametrized test.
- **Name tests after the behavior, not the method.** `test_returns_error_when_db_missing` beats `test_db_import_3`.
- **No unnecessary mocks.** Only mock what you cannot control (network, clock, external processes). Over-mocking makes tests tautological — they test the mocks, not the code.
- **Flat over nested.** Prefer module-level test functions or flat test classes. Deeply nested class hierarchies in tests add complexity without value.
- **Prefer context managers (`with patch(...)`) over `monkeypatch`.** Context managers clearly isolate the scope that needs the mock. Use `monkeypatch` only when it genuinely simplifies the test (e.g., env vars, `chdir`, patching attributes on fixtures that outlive the test body).

#### Checklist

- [ ] test file mirrors `src` module path
- [ ] test class and method names describe the behavior under test
- [ ] happy path covered by integration test; unit tests cover edge cases
- [ ] no duplicated coverage between integration and unit tests
- [ ] `@pytest.mark.parametrize` used where 3+ tests differ only by input/output
- [ ] fixtures used for repeated setup — no copy-pasted boilerplate
- [ ] mocks only for external boundaries (subprocess, network, clock)

## Previous line: Python 3.13

Everything above targets Python 3.14. On 3.13:

- **No t-strings.** Build SQL/HTML with the target library's own parameterisation
  or escaping (`cursor.execute(sql, params)`, `markupsafe`), never f-string
  interpolation.
- **No `compression.zstd`.** The third-party `zstandard` package is the option;
  `tarfile`/`zipfile`/`shutil` do not read or write zstd.
- **Annotations are evaluated eagerly.** `from __future__ import annotations` is
  still needed for forward references, and there is no `annotationlib` — use
  `typing.get_type_hints()`. The main path's ruff config bans that import
  (`lint.flake8-tidy-imports.banned-api."__future__.annotations"` in
  [`references/testing-and-tooling.md`](references/testing-and-tooling.md)); drop
  that one entry while the project targets 3.13, and restore it on 3.14.
- **`except` needs brackets** for multiple types:
  `except (TimeoutError, ConnectionRefusedError):`.
- **Free-threading is experimental**, not officially supported, and carries a much
  larger single-threaded penalty than 3.14's ~5–10%.
- Pin `python_version` / `python-version` to `"3.13"` in the mypy/ty config while
  the project targets it.
