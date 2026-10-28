---
name: python-typing
description: Sets up static type checking for a Python package — choosing mypy, pyright, basedpyright or ty, strict configuration, per-module overrides, shipping py.typed — and fixes type-check errors. Use when the user says 'add type checking', 'set up mypy', 'pyright errors', 'make this package typed'. Not for lint or format failures, failing tests, runtime bugs, or the CI workflow that runs the checker.
license: MIT
---

# Python Typing

Stand up static type checking in the user's Python package with a strictness
strategy the team can defend — one checker, pinned, configured in
`pyproject.toml`, per-module escape hatches tracked as debt, a ratchet toward
strict, and (for libraries) a `py.typed` marker that verifiably survives into
the built wheel. Also covers fixing the errors the checker then reports.

## When NOT to use

- Ruff lint or format failures — including the ANN annotation-style rules,
  which are lint, not type checking (the python-lint skill, if installed).
- A failing test suite or pytest setup (python-testing).
- Runtime exceptions — a `TypeError` raised at runtime is a bug to debug
  directly, not a checker-configuration task.
- The CI workflow YAML that runs the checker (python-ci) or pre-commit wiring
  (python-precommit) — this skill hands the working command off to those.
- Packaging metadata, build backends, or wheel building beyond the `py.typed`
  marker itself (python-packaging).

## Workflow

### 1. Survey before choosing anything

- Layout: `src/` vs flat; the import-package name; library (published, has
  consumers) vs application.
- Lowest supported Python from `requires-python` — the checker must target it,
  not the interpreter you happen to run.
- Framework deps that need checker *plugins*: `grep -E "django|sqlalchemy|pydantic" pyproject.toml`.
  Plugins exist for mypy only; this can decide the whole checker choice.
- Existing config (`[tool.mypy]`, `[tool.pyright]`, `mypy.ini`,
  `pyrightconfig.json`) — extend it, don't silently replace it.
- New project vs legacy codebase (rough annotation coverage) — decides
  strict-from-day-one vs ratchet in step 4.

### 2. Pick ONE checker — the race is unsettled

The type-checker field is a live, unsettled race (mypy, pyright/basedpyright,
ty, Pyrefly, zuban). Do not present any of them as the obvious winner, and do
not quote speed multipliers or conformance percentages — the circulating
numbers are single-source and partly refuted. Decision rules that hold up:

| Situation | Pick |
| --- | --- |
| Django (django-stubs) or Pydantic plugin-dependent stack | mypy + the framework's plugin (SQLAlchemy 2.x is natively typed — its mypy plugin is deprecated and stopped at mypy 1.10) |
| New project, no plugin needs, VS Code team | pyright (`standard`, then `strict`) |
| Non-VS-Code editors (Neovim, Helix, Cursor) or stricter defaults wanted | basedpyright |
| uv/Ruff shop that tolerates beta churn | pilot ty locally; keep mypy or pyright as the CI gate |
| Multi-million-LOC monorepo | evaluate Pyrefly |

Commit to **one primary checker as the CI gate**. Using pyright in the editor
(Pylance) with a different CI checker is normal; running two checkers *as
gates* means maintaining parallel suppression comments (gotcha 5). Details and
trade-offs: [references/checker-selection.md](references/checker-selection.md).

### 3. Install pinned, run via uv

Pin the exact version — checker releases routinely add new diagnostics, so an
unpinned checker breaks CI on unrelated PRs. Substitute the current release
from PyPI for the pins shown:

```bash
uv add --dev "mypy==2.3.1"         # or: "pyright==1.1.413" (PyPI wrapper, bundles node)
uv run mypy src tests               # or: uv run pyright
```

Without uv (once, for reference): `python -m pip install "mypy==2.3.1"` then
`python -m mypy src tests`. For a ty pilot without touching deps:
`uvx --from "ty==0.0.80" ty check src` (again, substitute the current pin; ty is still pre-1.0).

### 4. Configure in pyproject.toml

mypy and pyright read different tables, so both can coexist while migrating.
mypy — and note `strict = true` is what makes mypy check unannotated code at
all (gotcha 1):

```toml
[tool.mypy]
python_version = "3.10"          # lowest supported, from requires-python
strict = true
warn_unused_ignores = true
# plugins = ["pydantic.mypy"]    # only if pydantic is a dependency

[[tool.mypy.overrides]]
module = ["some_untyped_lib.*"]  # third-party deps that ship no types
ignore_missing_imports = true
```

pyright / basedpyright (use `[tool.basedpyright]` for the fork):

```toml
[tool.pyright]
include = ["src", "tests"]
exclude = ["**/legacy"]                # added on top of pyright's defaults (node_modules, __pycache__, .*)
typeCheckingMode = "standard"          # "strict" for new projects
pythonVersion = "3.10"
```

ty reads `[tool.ty]` in `pyproject.toml` (or `ty.toml`); config surface is
small and beta — check `uv run ty --help` rather than trusting stale examples.

### 5. Set strictness — day one or ratchet, never big-bang retrofit

- **New project**: `strict = true` / `typeCheckingMode = "strict"` from the
  first commit. Retrofitting strictness later is what generates contributor
  friction and hundred-error floods.
- **Legacy codebase**: ratchet. Global strict with per-module exemptions that
  only ever shrink:

```toml
[tool.mypy]
strict = true

[[tool.mypy.overrides]]
module = ["myapp.legacy.*"]      # exempt, migrate module-by-module
ignore_errors = true
```

  pyright's equivalent is a `strict = ["src/myapp/core"]` array of strict
  islands over a `standard` base. Full staged rollout, both checkers:
  [references/strictness-ratchet.md](references/strictness-ratchet.md).
- Record the strategy where the team will see it (CONTRIBUTING or README): the
  chosen checker, the run command, and the rule that exemptions only shrink.

### 6. Ship py.typed and verify the wheel (libraries)

Without a `py.typed` marker, PEP 561 says checkers treat every import from
your library as `Any` — annotations exist in source but are invisible to
consumers, silently.

```bash
touch src/<pkg>/py.typed
```

Build backends differ on whether non-`.py` files get packaged (setuptools
needs `[tool.setuptools.package-data]`; hatchling usually includes it), so
never trust the source tree — verify the artifact:

```bash
uv build
python3 "${CLAUDE_SKILL_DIR}/scripts/check_py_typed.py" --package <pkg>
```

The script exits non-zero if `py.typed` is missing from the source package,
the newest wheel, or the newest sdist. Backend-by-backend config and stub
distribution options: [references/py-typed-distribution.md](references/py-typed-distribution.md).

### 7. Fix the reported errors

Triage in this order:

1. **Real bugs first** — `Optional` misuse, wrong return types, unreachable
   branches. These are the payoff; don't suppress them.
2. **Untyped third-party imports** — install the `types-*` stub package if one
   exists and pin it (stubs version independently of their library). Only
   fall back to a per-module `ignore_missing_imports` override — never the
   global flag.
3. **Genuine false positives** — suppress with an error-code-scoped comment,
   `# type: ignore[arg-type]` (mypy) or `# pyright: ignore[reportArgumentType]`,
   and keep `warn_unused_ignores` (mypy) / `reportUnnecessaryTypeIgnoreComment`
   (pyright) on so stale ignores fail the build.
4. Never fix an error by weakening global config.

### 8. Hand off

The type-check command is now the contract: the python-ci skill (if installed)
turns it into a CI job; python-precommit wires it into hooks. Not this skill's
job — stop at a locally passing command.

## Output spec

Done means all of these hold:

- Exactly one primary checker, pinned in dev dependencies, configured in
  `pyproject.toml`.
- `uv run <checker> ...` exits 0 over `src` (and `tests`, unless deliberately
  excluded with a written reason).
- Strictness decision recorded: strict, or the current ratchet stage plus the
  exemption list tracked as debt.
- For a library: `py.typed` present in the package **and**
  `scripts/check_py_typed.py` passes against a freshly built wheel.
- Every suppression comment is error-code-scoped; unused-ignore detection is
  enabled.
- The run command is documented where the team will find it.

## Failure modes & gotchas

1. **mypy green ≠ checked.** By default mypy skips unannotated function
   bodies; a "no errors" run can be ignoring most of the codebase. Set
   `check_untyped_defs = true` (or `strict`) before trusting any green run.
2. **Global strict + per-module downgrades don't compose.** Long-standing
   issues in both tools (mypy #11401, pyright #601): you cannot cleanly
   downgrade individual strict rules per module. What works: global strict
   with per-module `ignore_errors` (mypy) or a `strict` directory array over a
   `standard` base (pyright).
3. **pyright floods legacy code harder than mypy.** It was already checking
   unannotated code, so jumping straight to `strict` surfaces far more errors
   at once — start at `standard` on existing codebases.
4. **py.typed missing from the wheel** is the classic invisible failure: the
   marker sits in git, the backend drops it from the artifact, and every
   downstream user silently gets `Any`. Always verify the built wheel, not the
   source tree (step 6).
5. **Two checkers, double suppressions.** The engines disagree (kwargs typing,
   `__new__` inference, union widening), so the same line can need both
   `# type: ignore[...]` and `# pyright: ignore[...]`. Accept that cost
   knowingly or stay with one gate.
6. **Strict is not portable.** mypy strict, pyright strict, basedpyright's
   "recommended" preset, and ty/Pyrefly rules are all different contracts —
   zero errors on one implies nothing about the others.
7. **Pydantic friction.** Checkers can't see through `before`/`wrap`
   validators, so constructors called with pre-validation input types raise
   false positives. Options with trade-offs: mypy + `pydantic.mypy` plugin,
   rule-scoped ignores on model modules, or (bleeding-edge) Pyrefly's
   experimental Pydantic integration. Separately — a statically clean model is
   not runtime-safe: Pydantic coerces by default (`"30"` becomes `30`) unless
   its own strict mode is enabled.
8. **ty/Pyrefly maturity.** No plugin system (Django/SQLAlchemy/Pydantic
   plugin stacks can't migrate), beta-grade churn, and migrating off pyright
   can *lose* diagnostics it used to catch. ty's "gradual guarantee" (removing
   or loosening an annotation never introduces new errors — adding precision
   may surface real ones) makes it a pleasant incremental pilot — as an editor/local tool, not yet an OSS package's CI
   gate.
9. **pyright `exclude` is additive.** Custom entries are added on top of the
   defaults (`**/node_modules`, `**/__pycache__`, `**/.*`), and the defaults take
   precedence — so you cannot un-exclude a dot-directory by listing it in
   `include`; move the code instead.
10. **Ruff is not a type checker.** Its ANN rules police annotation *style*;
    they catch zero type errors. A passing lint run says nothing here.
11. **Checker upgrades flip defaults.** mypy 2.0 (2026-05) turned
    `--local-partial-types` and `--strict-bytes` on by default, changed
    `--allow-redefinition` semantics, dropped `--python-version 3.9`, and
    added experimental parallel checking (`--num-workers N`) — a routine bump
    can newly break CI, which is why step 3 pins exact versions and upgrades
    deliberately.

## Bundled resources

- [references/checker-selection.md](references/checker-selection.md) — the
  contender field, comparison table, decision guide, hybrid editor/CI pattern.
- [references/strictness-ratchet.md](references/strictness-ratchet.md) —
  staged strict-mode rollout with full configs for mypy and pyright.
- [references/py-typed-distribution.md](references/py-typed-distribution.md) —
  PEP 561 distribution options, per-backend packaging config, verification.
- `scripts/check_py_typed.py` — verifies `py.typed` in the source package and
  inside built wheel/sdist artifacts; read-only, non-zero exit on failure.
