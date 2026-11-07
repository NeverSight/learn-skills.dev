---
name: sota-python
description: >-
  State-of-the-art Python engineering for both writing new Python and
  auditing existing Python code. Covers uv-based tooling and project setup, strict typing,
  idioms and pitfalls, asyncio structured concurrency, security (injection, deserialization,
  supply chain), performance, and FastAPI/Django/pytest practice. Use whenever the task
  involves Python source, pyproject.toml, requirements files, or Python tooling — building
  features, scaffolding projects, reviewing PRs, or hunting bugs/vulnerabilities.
  Trigger keywords: Python, pip, uv, pyproject, asyncio, Django, FastAPI, pytest, type hints,
  mypy, ruff, pydantic, SQLAlchemy, venv.
---

# SOTA Python (2026)

## Purpose

This skill encodes the 2026 state of the art for Python: modern toolchain (uv + ruff + one
strict type checker), Python ≥3.12 idioms, structured async, security-by-default, and
measured performance work. It serves two modes:

- **BUILD** — writing new code or modifying existing code to this standard.
- **AUDIT** — reviewing existing code against this standard and reporting findings.

The detailed rules live in `rules/*.md`. Read SKILL.md fully; load rules files on demand per
the index table below. When in doubt between two rules files, the index's "read when" column
decides.

## BUILD mode

When creating or modifying Python code:

1. **Establish context first.** Check `pyproject.toml`, `uv.lock`, `.python-version`, ruff
   config, and the type checker in use. Match the project's floor (e.g., no `type` aliases
   on a 3.10 project). For a *new* project, scaffold per [rules/01](rules/01-tooling-project-setup.md): `uv init`, src/ layout,
   ruff with the standard select, strict checker, pre-commit.
2. **Default stack:** uv for env/deps (commit the lockfile), `ruff check --fix` + `ruff
   format` before presenting code, full annotations on everything public, pydantic v2 at
   trust boundaries, frozen+slots dataclasses inside, `pathlib`, `logging` with lazy `%`
   formatting.
3. **Async code** follows [rules/04](rules/04-async.md) unconditionally: TaskGroup scopes, no blocking calls in
   coroutines, timeouts on external awaits, no unreferenced `create_task`.
4. **Security posture is non-optional** even when unrequested: parameterized SQL, argv-list
   subprocess, `secrets` for tokens, safe extraction, no pickle/eval on external data.
5. **Tests accompany code:** pytest, fixtures + parametrize, independent tests; property
   tests (hypothesis) for invariant-bearing code ([rules/07](rules/07-frameworks-testing.md) §3).
6. **Performance:** correct data structures by default (set membership, join, generators);
   anything beyond that requires a profile first ([rules/06](rules/06-performance.md) §1). Don't micro-optimize cold code.
7. **Verify before declaring done:** run `ruff check`, the project's type checker, and the
   test suite via `uv run`. Code that doesn't pass these is not done.

## AUDIT mode

**Coverage:** every `rules/` file's Audit checklist applies in AUDIT mode. Mark one *not applicable* only with its reason in the report — never skip a file because the thing it checks for is absent, since that absence may be the finding.

When reviewing existing Python code:

1. **Sweep mechanically first.** Run the "Audit checklist" block at the end of every relevant
   rules file — they are ordered grep/ruff/bandit commands. Start with
   `uvx ruff check --select F,B,S,ASYNC,DTZ,E722,BLE --statistics .` for a heat map, then
   `uvx bandit -r src/ -ll` and a pip-audit of the *project's* lock for security baselines —
   `uv export --format requirements-txt --no-emit-project | uvx pip-audit --disable-pip -r /dev/stdin`
   (bare `uvx pip-audit` audits its own tool venv and exits 0 on any project; a project with
   no third-party dependencies makes this pipe exit 1 — [rules/08](rules/08-supply-chain.md) §1 has the counted form).
2. **Then read for design:** trust-boundary placement (validation at edges?), exception
   strategy, async ownership of tasks, N+1 patterns, cache invalidation, test independence.
   Greps find syntax; you find architecture.
3. **Verify every finding** — open the file, confirm the context (a `pickle.loads` of a file
   the same process wrote with HMAC verification is not a CRITICAL). No finding ships on grep
   output alone. Note mitigations that are already present.
4. **Don't report style noise** a formatter/linter would auto-fix; mention once collectively
   ("run ruff format; 40 files drift") and move on.

### Severity conventions

| Severity | Meaning | Examples |
|---|---|---|
| CRITICAL | Exploitable now, or data loss/corruption | SQL injection, `pickle.loads`/`eval` on untrusted input, `shell=True` with user data, auth bypass |
| HIGH | Exploitable with preconditions, or production-breaking bug | path traversal, unsafe `extractall`, `random` for tokens, swallowed `CancelledError`, blocking call in async hot path, bare `except: pass` around critical logic, `verify=False` |
| MEDIUM | Correctness/maintenance risk, degraded ops | mutable default args, fire-and-forget tasks, unbounded `@cache` on user input, N+1 queries, missing lockfile in an app, no type checker in CI, edited applied migrations |
| LOW | Deviation from SOTA, friction, future risk | legacy typing forms, os.path usage, f-strings in log calls, flat layout in a library, bare `# type: ignore` |
| INFO | Worth knowing, no action forced | tooling consolidation opportunities, 3.13/3.14 features available after floor bump |

Confidence accompanies severity: **confirmed** (you traced the data flow) vs **suspected**
(pattern present, flow not fully traced — say what would confirm it).

### Finding format

Expands the router's canonical row (`file:line | rule | severity | effort | fix`, which wins on a
cross-domain roll-up); evidence block and report order: [`sota` rules/03](../sota/rules/03-audit-findings.md) §2 and §5.

```
[SEVERITY/confidence] short title
  File: src/pkg/module.py:42 (absolute path in final report)
  Issue: what is wrong, in one or two sentences, with the data-flow if security-relevant
  Evidence: the offending line(s), quoted
  Fix: concrete change — code snippet or exact rule reference (rules/05 §2)
  Effort: trivial | small | medium | large
```

Group findings by severity, CRITICAL first. End with: counts per severity, the mechanical
sweep commands you ran, and explicit "checked and clean" areas (so absence of findings is
information, not omission).

## Rules index

| File | Read this when... |
|---|---|
| [`rules/01-tooling-project-setup.md`](rules/01-tooling-project-setup.md) | starting/scaffolding a project; reviewing pyproject/uv/ruff/CI setup; choosing type checker; questions about uv lockfiles, **`pylock.toml` (PEP 751) exports for non-uv tools**, PEP 723 scripts, src/ layout, 3.12–3.14 features, free-threading; **what 3.12/3.13 REMOVED (PEP 594, `distutils`, `imp`, `lib2to3`)** before a floor bump; **suppressions that expire** (`noqa`/`type: ignore` with a rule and a reason), test-path lint exemptions, `uv sync --frozen` vs `--locked` |
| [`rules/02-typing-correctness.md`](rules/02-typing-correctness.md) | annotating APIs; choosing TypedDict vs dataclass vs pydantic; Protocol vs ABC; generics/`Self`/`ParamSpec`; Any leaks; **in-band sentinels (`-1` for absent) — the defect `int \| None` exists to prevent, invisible to the type checker**; `assert_never` exhaustiveness; where runtime validation belongs |
| [`rules/03-idioms-pitfalls.md`](rules/03-idioms-pitfalls.md) | any general Python code; mutable defaults, closures, comprehensions, context managers, pathlib, EAFP, dataclass/enum patterns, itertools/functools; designing exceptions; **what no `except` catches (C-extension crash, SIGKILL) and `json.loads` depth**; logging setup; **the public API surface** (`__all__`, keyword-only parameters, `__slots__`, deprecation) |
| [`rules/04-async.md`](rules/04-async.md) | any `async def` in sight: TaskGroup vs gather, blocking-the-loop, fire-and-forget, timeouts/cancellation, async generators, anyio, sync-ORM-in-async bugs; **per-request `ContextVar`/thread-local state reset in `finally`** |
| [`rules/05-security.md`](rules/05-security.md) | auditing for vulnerabilities; handling untrusted input; subprocess/SQL/paths/archives/secrets; pickle/eval/yaml and reflection by name (`import_module`, `getattr`); SSRF/XML (dependency auditing, supply chain, adopting a new dependency and the insecure defaults of the libraries you call moved to [rules/08](rules/08-supply-chain.md)); temp-file and permission hygiene; where crypto is owned; remote-host trust; debug consoles, debug switches and dev servers (`runserver`, `flask run`, `--reload`) in production; **3.14 t-string (`Template`) consumers that render values raw; remote debugger attach (PEP 768) and its switches**; **escape hatches into raw memory**: `ctypes`/`cffi` and C extensions |
| [`rules/06-performance.md`](rules/06-performance.md) | anything slow: profiling tool choice, hot-loop suspects, numpy/polars vectorization, functools caching caveats, threads vs processes vs asyncio, lazy imports/startup |
| [`rules/07-frameworks-testing.md`](rules/07-frameworks-testing.md) | FastAPI (DI, boundary models, sync-in-async), Django (N+1, select_related, migrations), **cookies the app sets (`set_cookie` defaults: Secure/HttpOnly off)**, pytest (fixtures, parametrize, independence, hypothesis, CrossHair), **`-X dev` in CI for `ctypes`/`cffi`/C-extension code**. **Test *strategy* — suite shape, TDD, doubles, test data, flake policy — lives in [`sota-testing`](../sota-testing/SKILL.md); load it for any build that writes logic. This file owns Python runner mechanics only.** |
| [`rules/08-supply-chain.md`](rules/08-supply-chain.md) | Adding or auditing dependencies: lockfiles and hashes (**pip-audit on a project with no dependencies exits 1 — the counted form**), typosquats and adoption checks, code that runs at install time, publishing credentials and provenance, static-analysis gates (formerly [rules/05](rules/05-security.md) sections 9–10, now §1–§2) |

## Top-10 non-negotiables

1. **uv + committed lockfile; CI installs `--locked`.** No unlocked `pip install` in
   pipelines or images. ([rules/01](rules/01-tooling-project-setup.md))
2. **One strict type checker gating CI; public APIs fully annotated; no `Any` leaking
   across module boundaries.** ([rules/02](rules/02-typing-correctness.md))
3. **Validate at the boundary, trust inside:** pydantic v2 (`extra="forbid"`) where data
   enters; typed dataclasses within. Never pass raw parsed JSON deep into the core. ([rules/02](rules/02-typing-correctness.md))
4. **Never `eval`/`exec`/`pickle.loads`/`yaml.load` on data you don't fully control.**
   ([rules/05](rules/05-security.md))
5. **SQL via bound parameters only; subprocess via argv lists with `shell=False`, `--`
   before user args.** ([rules/05](rules/05-security.md))
6. **No bare `except:`; no `except Exception: pass`; chain with `raise ... from e`;
   `except Exception` only at top-level boundaries with `logger.exception`.** ([rules/03](rules/03-idioms-pitfalls.md))
7. **Async: TaskGroup-owned tasks only; zero blocking calls in coroutines
   (`to_thread`/process pool instead); `asyncio.timeout` on every external await;
   re-raise `CancelledError`.** ([rules/04](rules/04-async.md))
8. **No mutable default arguments; context managers for every resource; `pathlib` +
   explicit `encoding="utf-8"`.** ([rules/03](rules/03-idioms-pitfalls.md))
9. **`secrets` (never `random`) for anything security-relevant; `compare_digest` for
   secret comparison; no hardcoded credentials; no `verify=False`.** ([rules/05](rules/05-security.md))
10. **Tests are independent (random order + parallel safe), fixture-based, parametrized;
    performance claims require a profile.** ([rules/06](rules/06-performance.md), [rules/07](rules/07-frameworks-testing.md))
