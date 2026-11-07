---
name: python-testing
description: Builds pytest infrastructure for a Python package — layout and config, coverage gates with fail_under, Hypothesis property-based tests, mutation testing to catch weak or agent-gamed tests, multi-version runs via tox, nox, or uv. Use for 'set up pytest', 'add coverage', 'test on multiple Python versions'. Not for writing tests for one file, fixing a single failing test, or CI workflow YAML.
license: MIT
---

# python-testing

Build test infrastructure for a Python package that stays trustworthy under
pressure: pytest configuration the installed pytest actually reads, branch
coverage with a gate proven to fail, Hypothesis and mutation testing as
backstops against tests that execute code without checking it, and multi-version
runs. The failure this skill prevents is green-but-meaningless — gates that
silently pass, config tables that are silently ignored, and suites edited (by
humans or agents) until they stop proving anything.

## When NOT to use

- Writing tests for a single file or function, or improving one module's tests —
  do that directly; no infrastructure needed.
- Diagnosing or fixing one failing test — read the test and the code under test.
- CI workflow YAML — GitHub Actions jobs, version-matrix wiring, coverage
  upload/combine across CI legs. The python-ci skill, if installed, owns that.
  This skill decides *what* runs; CI decides *where*.
- Packaging work — pyproject metadata, build backend, converting a repo to src
  layout as a packaging exercise. The python-packaging skill, if installed.
- Git hook wiring — the python-precommit skill; full test suites do not belong
  in pre-commit hooks anyway.

## Workflow

### 1. Survey the repo

Run the read-only audit first — it catches shadowed and split config sources:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/check_test_config.py" --root .
```

Then establish the facts later steps depend on:

```bash
uv run pytest --version            # major version decides the config table (step 2)
grep -n "requires-python" pyproject.toml
ls pytest.ini setup.cfg tox.ini .coveragerc noxfile.py 2>/dev/null
```

Note the layout: `src/<pkg>/` + sibling `tests/` (src layout) or package at the
repo root (flat). Convention throughout: invoke tools through uv (`uv run`,
`uvx`). If uv is unavailable, the plain fallback is
`python -m pip install -e ".[dev]"` then `python -m pytest` — same flags
everywhere; stated once here.

### 2. pytest config — one table, in pyproject.toml

Two tables exist, and the installed major decides: pytest >= 9.0 (Nov 2025) reads
a native `[tool.pytest]` table (real TOML arrays/booleans); every supported
pytest reads `[tool.pytest.ini_options]` (INI-style strings). Never write both.
On pytest below 9, `[tool.pytest]` is ignored **silently**: no error, tests still
run, strictness flags never apply — so check `uv run pytest --version` first
(https://docs.pytest.org/en/stable/reference/customize.html). The block below
uses `ini_options` because it works everywhere; on a >= 9 repo prefer the native
table with the same keys.

```toml
[tool.pytest.ini_options]
minversion = "8.0"          # raise to "9.1" if you rely on the strict flags below via addopts (see gotchas)
testpaths = ["tests"]
addopts = "-ra --strict-markers --strict-config"
filterwarnings = ["error"]
```

- `--strict-markers` — typo'd or undeclared `@pytest.mark.*` markers fail
  instead of silently never running.
- `--strict-config` — typo'd config keys become errors.
- `filterwarnings = ["error"]` — deprecations fail now, not at upgrade time. On
  a legacy dependency tree this is noisy; add targeted
  `"ignore:<msg>:<category>"` entries rather than deleting the gate.
- Async project? Add `asyncio_mode = "auto"` (with pytest-asyncio as a dev dep)
  to drop the per-test marker.
- Keep `--cov` OUT of `addopts`. Coupling every run to coverage slows
  single-test loops and can confuse debugger breakpoints; pass coverage flags
  in the explicit commands below and in CI. Trade-off: some teams keep it in
  `addopts` so coverage is never forgotten — if the user prefers that, keep it
  and note `--no-cov` disables it for one run.
- **One config source.** pytest uses the first of `pytest.toml`/`.pytest.toml`,
  `pytest.ini`/`.pytest.ini` (both win even when empty), `pyproject.toml`
  (with either table), `tox.ini`, `setup.cfg` and ignores the rest — a stray
  `pytest.ini` silently shadows everything in pyproject. Merge, then delete.

### 3. Layout and discovery

src layout (`src/<pkg>/` with tests in a sibling `tests/`, not inside the
package) is the reliable shape: with `uv run`, pytest imports the *installed*
package, so import and packaging bugs surface in tests instead of in users'
environments (https://docs.pytest.org/en/stable/explanation/goodpractices.html).
`testpaths = ["tests"]` and coverage `source = ["src"]` then line up.

- "pytest can't find/import my package" right after moving to src layout
  usually means the package is not installed in the environment — `uv sync`
  (or `pip install -e .`) and re-run.
- Do not migrate a flat-layout repo to src layout just for tests; that is a
  packaging change (python-packaging territory). Testing works in flat layout —
  you only lose the installed-package guarantee.
- Shared fixtures live in `tests/conftest.py`.

### 4. Coverage — branch on, gate proven

```toml
[tool.coverage.run]
source = ["src"]
branch = true
parallel = true
relative_files = true

[tool.coverage.report]
fail_under = 85
show_missing = true
skip_covered = true
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

- `branch = true` is the point — line coverage says a line ran; branch coverage
  says both sides of each `if` did. Line-only numbers overstate.
- `fail_under` of 80–90 is the defensible band. 100% is anti-recommended: it
  breeds assert-free tests and `pragma` sprawl. Exclude genuinely unreachable
  lines instead.
- If a `.coveragerc` exists it silently wins over `[tool.coverage.*]` in
  pyproject — keep exactly one source.
- Run with `uv run pytest --cov --cov-report=term-missing`.

**Prove the gate.** pytest-cov below 7.1 could return exit code 0 on a missed
aggregate threshold depending on report options (fixed in 7.1.0, 2026-03), and
rounding once passed 66.6% against a 67 bar. Never assume — demonstrate:

```bash
uv run pytest --cov --cov-fail-under=100 -q; echo "exit=$?"
```

Expect a non-zero exit (unless coverage is genuinely 100%). If it exits 0, gate
in two steps instead — `uv run pytest --cov` then
`uv run coverage report --fail-under=85` — the standalone coverage command's
exit code is reliable.

- Parallel runs (`pytest -n auto` via pytest-xdist) require `parallel = true`
  and `relative_files = true`. Subprocesses spawned by tests need
  `[tool.coverage.run] patch = ["subprocess"]` (coverage >= 7.10) — pytest-cov 7
  dropped its own subprocess measurement — otherwise coverage comes back empty
  or 0%.
- A threshold is a floor, not a quality signal — it is trivially satisfied by
  tests without assertions. Steps 5–6 are the countermeasures. Patch/delta
  coverage on PRs is CI wiring (python-ci skill, if installed).

Flag-by-flag detail, precedence rules, and combine mechanics:
[references/configuration.md](references/configuration.md).

### 5. Property-based tests where they pay

Add Hypothesis for parsers, serializers, codecs, and algorithmic code — anywhere
a property (round-trip, idempotence, invariant) exists. A 426-project corpus
study found each property-based test kills roughly 50x the mutations of an
average unit test (https://dl.acm.org/doi/10.1145/3764068).

```bash
uv add --dev hypothesis    # exact version pinned by uv.lock
```

```python
from hypothesis import given, strategies as st

@given(st.text())
def test_roundtrip(s):
    assert decode(encode(s)) == s
```

- Prefer bounded strategies (`st.integers(min_value=1)`) over `assume()`
  filtering — rejecting most examples raises `HealthCheck.filter_too_much`.
- Register settings profiles in `tests/conftest.py`; CI runs the heavy one via
  `pytest --hypothesis-profile=ci`:

```python
from hypothesis import settings
settings.register_profile("ci", max_examples=1000)
settings.register_profile("dev", max_examples=25)
```

- Persist the `.hypothesis/` example database (commit it, or cache it in CI) —
  otherwise every run rediscovers known counterexamples from scratch.
- `DeadlineExceeded` only on CI machines means slow shared runners — raise or
  disable `deadline` in the ci profile deliberately; don't delete the test.

Property patterns, strategy design, and stateful testing:
[references/beyond-coverage.md](references/beyond-coverage.md).

### 6. Mutation testing — do the tests notice bugs?

Coverage proves a line executed; mutation testing proves a test *fails* when
that line is wrong. It is the direct check on assertion quality, which matters
most when agents write or edit tests: a suite that was edited until green
proves nothing by itself. Options — no settled winner, choose per constraints:

| Tool | Character | Watch out |
| --- | --- | --- |
| mutmut | Mature, simplest CLI, pytest-first | Full-repo runs are slow — scope `paths_to_mutate` |
| cosmic-ray | Session-based, resumable, distributed | Heaviest setup; overkill for small packages |
| pytest-gremlins | Runs as a pytest plugin | Newer; adoption evidence is thin — vet maintenance first |

Install as a dev dependency so it runs inside the project environment and gets
pinned by `uv.lock` (an unpinned `uvx` one-off executes whatever was published
last — a reproducibility and supply-chain hole):

```bash
uv add --dev mutmut
uv run mutmut run
```

- Scope the first run to one core module (`[tool.mutmut]` `source_paths`; `do_not_mutate` for generated code),
  then triage survivors: a surviving mutant means a missing or weak assertion —
  or a genuinely equivalent mutant, which you mark and move on.
- Do not gate CI on mutation score on day one; run it scoped or nightly and
  treat the score as a diagnostic — mutmut 3.7.0's own unreleased notes still list
  coverage-excluded lines being mutated, false survivors and timeouts counted as
  kills. Practitioners report 85–95% mutation scores
  as far more meaningful than the same number in line coverage.

Triage workflow and the agent-era rationale:
[references/beyond-coverage.md](references/beyond-coverage.md).

### 7. Multi-version runs

Match the tool to the project — this debate is genuinely unsettled:

| Situation | Use |
| --- | --- |
| Simple deps, few version-specific branches | plain uv loop (below) |
| Complex matrix (extras, backends, C extensions) | tox or nox, uv-accelerated |
| Want Python (not INI) config, dynamic sessions | nox |
| Already on tox | keep it; add tox-uv — speed-up, no config rewrite |

```bash
for v in 3.11 3.12 3.13 3.14; do   # the versions requires-python promises; 3.10 is EOL 2026-10
  uv run -p "$v" --with pytest --with pytest-cov pytest || exit 1
done
```

For tox or nox, swap the environment backend to uv (`tox-uv`, nox's uv backend):
environment setup gets dramatically faster with no config-model change.

- nox footgun: a repo-root `.python-version` file can silently pin every
  session to the local dev version (https://github.com/wntrblm/nox/issues/1038).
- Never enforce `fail_under` inside each version leg — a 3.13-only branch drops
  coverage on the 3.10 leg. Locally: run the loop with `parallel = true`, then
  `uv run coverage combine && uv run coverage report --fail-under=85` once. The
  CI version of that split (artifacts, combine job) belongs to python-ci.

Configs and trade-offs in depth:
[references/multi-version.md](references/multi-version.md).

### 8. Verify

1. `uv run pytest` — green.
2. The gate-trip demonstration from step 4 exits non-zero.
3. `python3 "${CLAUDE_SKILL_DIR}/scripts/check_test_config.py" --root .` exits 0.
4. Report to the user: config location and table chosen (and why), thresholds,
   and which backstops (Hypothesis, mutation, multi-version) are wired vs
   deferred.

## Output spec

Done means:

- Exactly one pytest config source and one coverage config source; the pytest
  table matches the installed major version.
- Branch coverage on; `fail_under` in the 80–90 band; the gate demonstrated to
  exit non-zero when missed.
- Suite runs green via `uv run pytest` from a clean checkout.
- Where requested: Hypothesis dev dep with profiles; mutation tool pinned with
  a first scoped run triaged; multi-version runner chosen with stated rationale.
- No CI YAML written or modified.

## Failure modes & gotchas

| Symptom | Cause / fix |
| --- | --- |
| Coverage gate "passes" while below threshold | pytest-cov < 7.1 aggregate exit-code bug or rounding; prove the gate (step 4) or gate via standalone `coverage report --fail-under` |
| Strictness flags mysteriously not applied | `[tool.pytest]` on pytest <9 (silently ignored), a shadowing `pytest.toml`/`pytest.ini`, or pytest 9.0.x — a regression silently ignored `--strict-markers`/`--strict-config` inside `addopts` (fixed 9.1.0, 2026-06); on >= 9 prefer the `strict_markers`/`strict_config` ini keys |
| Coverage 0% or empty under `pytest -n auto` | missing `parallel`/`relative_files`; test-spawned subprocesses need coverage's `patch = ["subprocess"]` (pytest-cov 7 no longer measures them) |
| Coverage config edits change nothing | a `.coveragerc` wins over pyproject — delete one |
| Gate script keys on a specific exit code | the tools disagree: coverage.py `fail_under` exits 2, pytest-cov exits 1, pytest exits 5 when no tests were collected — gate on non-zero |
| `fail_under = 90` with `branch = true` "passes" at 85% branch coverage | the total combines statement and branch opportunities; it is not a branch-only minimum — read the branch column, or gate branches separately |
| Matrix legs fail on version-specific code | `fail_under` enforced per leg; combine first, gate once |
| Suite green right after an agent edited the tests | proves nothing — review test diffs before source diffs, run mutation testing; researchers have shown agents faking green via an injected `conftest.py`, so verify in an environment the agent cannot write to |
| Generated tests pass but catch no regressions | mock-heavy tests, a documented agent bias (https://arxiv.org/abs/2602.00409) — require behavioral assertions on the public API, not mock call counts |
| Hypothesis rejects most examples (`filter_too_much`) | replace `assume()` with bounded strategies |
| Hypothesis finds a bug, next run forgets it | `.hypothesis/` database not persisted across runs |
| Flaky `DeadlineExceeded` on CI only | slow shared runners — adjust `deadline` in the ci profile |

## Files

- `scripts/check_test_config.py` — read-only audit of pytest/coverage config
  (shadowed sources, wrong config table, missing branch coverage or gate).
  Exits non-zero when it finds errors; never modifies the repo.
- `references/configuration.md` — pytest and coverage config in depth:
  precedence, the pytest-9 table question, the exit-code bug, xdist/combine
  mechanics.
- `references/beyond-coverage.md` — Hypothesis patterns and settings; mutation
  tool comparison and survivor triage; why agent-edited green suites need
  backstops.
- `references/multi-version.md` — uv loop vs tox vs nox, uv-backed runners,
  coverage across versions.
