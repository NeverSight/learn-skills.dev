---
name: python-packaging
description: Configures packaging for a Python library — pyproject.toml metadata, build backend, src layout, CLI entry points, uv lockfiles, where dev dependencies go (dependency-groups vs optional-dependencies), wheels and sdists. Use to make a project installable, set up pyproject.toml, build a wheel, move off requirements.txt, or switch to uv. Not for publishing to PyPI or release automation.
license: MIT
---

# python-packaging

Make a Python library installable and buildable with verified artifacts: one
`pyproject.toml` as the single source of truth, a deliberately chosen PEP 517
build backend, `src/` layout, uv-managed dependencies with a committed lockfile,
and an sdist + wheel whose contents are checked rather than assumed. The failures
this skill prevents: declared files (`py.typed`, data files) silently missing from
the wheel, backends that cannot handle the project's layout or extensions, Poetry
migrations that switch the backend before resolution is verified, and `pip` calls
that desync a uv-managed environment.

## When NOT to use

- Publishing to PyPI, version bumps, changelogs, git tags, trusted publishing —
  the python-release skill, if installed. Stop after artifacts are verified.
- Type-checker choice or configuration, and whether/how to ship `py.typed` — the
  python-typing skill. This skill only verifies that an existing `py.typed`
  actually lands in the built wheel.
- `[tool.ruff]` config — python-lint. pytest/coverage config — python-testing.
  GitHub Actions — python-ci. Dependency vulnerability audits — python-supply-chain.
- Single-file scripts that just need dependencies — PEP 723 inline script metadata
  plus `uv run script.py` covers that with no packaging at all.

## Workflow

### 1. Assess what exists

```bash
ls setup.py setup.cfg MANIFEST.in requirements*.txt poetry.lock Pipfile uv.lock 2>/dev/null
grep -n "build-backend\|tool.poetry\|dependency-groups\|optional-dependencies" pyproject.toml 2>/dev/null
find . -name "*.pyx" -o -name "*.c" -o -name "Cargo.toml" | grep -v .venv | head
```

Record three facts before changing anything: (a) native extensions or pure
Python — this decides the backend; (b) flat or `src/` layout; (c) which
dev-dependency convention the repo already uses (`[dependency-groups]`,
a `dev` extra under `[project.optional-dependencies]`, or legacy
`[tool.uv] dev-dependencies`) — match it or migrate it wholesale, never mix.

### 2. Choose the build backend

| Backend | Pick when | Avoid when |
| --- | --- | --- |
| `uv_build` | pure-Python library; zero-config `src/` discovery, strict metadata validation | any C/Cython/Rust extension modules (unsupported); VCS-tag dynamic versioning needed |
| `hatchling` | dynamic versioning from git tags via `hatch-vcs` matters; widely treated as the general-guidance default; plugin ecosystem | you want uv_build's stricter validation and zero config |
| `setuptools` | extension modules (`ext_modules`), deep legacy config | greenfield pure-Python — looser validation, auto-discovery surprises |

Do not adopt `poetry-core` for new projects; the ecosystem consolidated on
PEP 621 `[project]` metadata. Note that `uv build` is a backend-agnostic PEP 517
frontend — it drives hatchling or setuptools just as well, so adopting uv as the
project manager does not force a backend migration; treat that as a separate,
verified step.

```toml
[build-system]
requires = ["uv_build>=0.12,<0.13"]
build-backend = "uv_build"
```

Keep the upper bound on `uv_build`: it follows uv's versioning policy, where
breaking changes may land in minor releases, so an unbounded requirement can
break your build the day a new version ships. Hatchling and setuptools have more
conservative compatibility norms; a floor (e.g. `hatchling>=1.27`) is customary.
Risk framing: uv as a whole is pre-1.0, but the `uv_build` backend specifically
is marked Production/Stable on PyPI and has been the `uv init` default since
mid-2025 — do not conflate the two in either direction.

Full trade-offs, `[tool.uv.build-backend]` keys, and per-backend file-inclusion
config: [references/build-backends.md](references/build-backends.md).

### 3. Lay out the package (src/)

```
my-package/
├── pyproject.toml
├── README.md
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── py.typed        # only if the project already ships one
└── tests/
```

Use `src/` for libraries: tests and tools then import the *installed* package.
With a flat layout, `import my_package` resolves to the working-directory copy
even when the built wheel is broken or missing files — packaging bugs stay
invisible until release. For a new project, `uv init --lib my-package` scaffolds
`src/`, `py.typed`, and the uv_build backend in one step.

uv_build expects `src/<module>/__init__.py` with the module named after the
normalized project name. If the import name differs, declare it:

```toml
[tool.uv.build-backend]
module-name = "actual_import_name"
```

### 4. Write [project] metadata

Minimal publishable set — `validate-pyproject` (step 6) will hold you to it:

```toml
[project]
name = "my-package"
version = "0.1.0"
description = "One line, benefit first."
readme = "README.md"
license = "MIT"                      # SPDX expression (PEP 639; needs a current backend)
requires-python = ">=3.10"
authors = [{ name = "Your Name", email = "you@example.com" }]
dependencies = ["httpx>=0.27"]
classifiers = ["Programming Language :: Python :: 3"]

[project.scripts]
my-cli = "my_package.cli:main"       # callable must take no required args; parse sys.argv inside

[dependency-groups]
dev = ["pytest>=8"]
```

Dev tooling goes in PEP 735 `[dependency-groups]` (written by `uv add --dev`),
not in a published extra: extras under `[project.optional-dependencies]` are
installable by consumers from PyPI, dependency groups are not. A `dev` extra
leaks your toolchain into downstream resolvers. Optional *runtime* features
(e.g. `my-package[cli]`) are what extras are for.

### 5. Manage the project with uv

```bash
uv init --lib my-package            # new projects only (uv >= 0.12 also declares a build system for plain `uv init`; `--no-package` opts out)
uv add httpx                        # runtime dep -> [project.dependencies] + uv.lock
uv add --dev pytest                 # dev dep -> [dependency-groups].dev
uv sync                             # build .venv from uv.lock (--no-dev in production)
uv lock --upgrade-package httpx     # targeted upgrade; rest of the lockfile intact
uv run pytest                       # run tools in the env, no activation
```

Commit `uv.lock`; never hand-edit it. uv verifies lockfile freshness against
`pyproject.toml` and environment freshness against the lockfile before every
`uv run`, which is what makes results reproducible. Never call `pip` inside a
uv project — it mutates `.venv` behind the lockfile's back.

Migrations:

- **From setup.py/setup.cfg** — inventory every section first: `[options]`
  metadata goes to `[project]`, `package_data`/`MANIFEST.in` directives become
  the backend's file-inclusion config, and tool sections (`[tool:pytest]`,
  `[flake8]`, `[mypy]`) move to `pyproject.toml` or their owning skill. Build
  once with the old config, once with the new, diff the wheel/sdist listings,
  and only then delete `setup.py`, `setup.cfg`, and `MANIFEST.in` (steps 6–8
  verify the result). Exception: setuptools with C extensions still needs a
  `setup.py` for `ext_modules` — keep only that part.
- **From Poetry** — run `uvx 'migrate-to-uv==0.12.0'` (pin the version: unpinned
  `uvx` executes whatever was published to PyPI most recently, which is both
  irreproducible and a supply-chain hole; bump pins deliberately). It maps
  `[tool.poetry.*]` to PEP 621 and `poetry.lock` to `uv.lock`. Switch
  `[build-system]` away from `poetry-core` **last**, after `uv lock && uv sync`
  resolve cleanly — flipping the backend first is the classic way to debug two
  migrations at once.
- **From requirements.txt** — `uv add -r requirements.txt` (plus
  `-c constraints.txt` if present), then delete the file. If downstream tooling
  still needs one, generate it with `uv export`.

### 6. Validate the metadata

```bash
uvx --from 'validate-pyproject[all]==0.26' validate-pyproject pyproject.toml
```

A `pyproject.toml` that parses as valid TOML can still violate the packaging
PEP schemas (bad license shape, misplaced key, malformed entry point) — this
catches what formatters and TOML parsers do not. Run it after every metadata
edit; it is cheap.

### 7. Build

```bash
uv build        # sdist (.tar.gz) + wheel (.whl) into dist/
```

To debug `uv_build` under any frontend, set `RUST_LOG=uv=debug`. No-uv fallback
(once, for environments where uv is unavailable): `python -m pip install
build==1.6.0 && python -m build` produces the same artifacts, and
`pip install -e . --group dev` (pip >= 25.1; groups are not extras) replaces `uv sync` for dev installs — at the cost of
lockfile reproducibility.

### 8. Verify the artifacts — never skip

Run the bundled checker (path relative to this skill's folder):

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/check_wheel.py" --project-root /path/to/project /path/to/project/dist
```

It is read-only and exits non-zero with `ERROR` lines if: the wheel lacks
`METADATA`/`WHEEL`/`RECORD`; any `py.typed` present in the source tree is
missing from the wheel; `tests/`, `docs/`, or similar directories leaked into
the wheel; or the sdist lacks `pyproject.toml`. Manual equivalents:
`unzip -l dist/*.whl` and `tar -tzf dist/*.tar.gz`.

Then smoke-test the wheel itself (not the source tree):

```bash
uv run --isolated --no-project --with dist/my_package-0.1.0-py3-none-any.whl \
  python -c "import my_package; print(my_package.__name__)"
```

## Output spec — what done looks like

- `pyproject.toml` is the only packaging config; `setup.py`/`setup.cfg`/
  `MANIFEST.in`/`requirements.txt` are gone (except `setup.py` kept solely for
  `ext_modules`).
- `validate-pyproject` exits 0.
- `uv build` produces both `dist/*.tar.gz` and `dist/*.whl`.
- `scripts/check_wheel.py` exits 0 — expected files (including `py.typed` when
  the source ships one) verified inside the wheel; no test/doc leakage.
- The built wheel imports in an isolated environment.
- `uv.lock` exists and is committed.

## Failure modes & gotchas

- **`py.typed` in the repo, missing from the wheel.** No backend can be assumed
  to ship arbitrary non-`.py` files: setuptools needs
  `[tool.setuptools.package-data]`, hatchling ships files inside the package dir
  only if the wheel target points at it, uv_build includes files under the
  module root. Consumers of a wheel without the marker silently get `Any` for
  your whole API — verify the artifact, not the source tree. Per-backend
  snippets in [references/build-backends.md](references/build-backends.md).
- **uv_build "module not found" / metadata validation failure.** By default it
  expects one module named after the normalized project name at `src/<module>/`
  or `./<module>/`. Declare a different name, several modules, or a namespace
  package with `[tool.uv.build-backend]` `module-name = [...]` / `module-root` /
  `namespace` (an explicit list is recommended over `namespace = true`, which
  disables the safety checks).
- **Build breaks after a uv release.** Unbounded `requires = ["uv_build"]` —
  restore the `>=X,<X+1` bound (step 2).
- **Half-finished Poetry migration.** `[build-system]` flipped while the real
  dependency list still sits in `[tool.poetry.dependencies]` — artifacts build
  with wrong or missing metadata. Metadata first, resolution verified, backend
  last.
- **Heisenbug environments.** Someone ran `pip install` in the uv project; the
  next `uv run` silently reverts it. Both directions look like flakiness. Only
  `uv add`/`uv sync` mutate the env.
- **Tests pass, installed package broken.** Flat layout imported the
  working-directory copy, masking files missing from the wheel. `src/` layout
  plus the step 8 wheel smoke test catches it.
- **`tests/` ships inside the wheel.** setuptools auto-discovery picks up any
  importable top-level directory. Constrain it
  (`[tool.setuptools.packages.find] where = ["src"]`) or move to `src/` layout;
  `check_wheel.py` flags the leak.
- **Dev extra published to PyPI.** Dev tooling declared as
  `[project.optional-dependencies] dev` becomes an installable extra for every
  consumer. Use `[dependency-groups]` for tooling; extras for optional runtime
  features only.
- **Valid TOML, invalid metadata.** Formatters and TOML parsers accept files
  that violate packaging schemas — that is what step 6 exists for.
- **Performance folklore.** Large build-speed multipliers claimed for uv_build
  trace to practitioner blog posts, not controlled benchmarks. Treat as
  directional; do not repeat specific numbers as fact.

## Bundled files

- [references/build-backends.md](references/build-backends.md) — backend
  trade-offs in depth, `[tool.uv.build-backend]` reference, per-backend file
  inclusion (`py.typed`, data files), migration paths, legacy-tool→uv command map.
- `scripts/check_wheel.py` — read-only sdist/wheel verification; run after every
  build; non-zero exit with machine-readable `ERROR` lines on failure.
