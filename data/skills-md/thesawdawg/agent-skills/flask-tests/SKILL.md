---
name: flask-tests
description: Write and run tests for this Flask app using the established two-tier pytest framework (fast SQLite unit tests + MySQL integration tests). Use when adding tests for a controller/model/worker/route, scaffolding tests for a new module, or asked how to test something here. Assumes Flask; confirm framework decisions with the user before scaffolding anything new.
---

# Flask App Testing

This project has an established pytest framework. Match it; do not invent a parallel one.

## Step 0 — Confirm framework decisions (ALWAYS, when this skill is invoked)

The stack is **Flask** (assume this). Before scaffolding new test infrastructure,
ask the user to confirm — they may differ per task. Skip a question only if the
answer is already obvious from the directive.

1. **Tier(s) needed** — unit only, or also an integration (real-DB) test?
2. **Database for integration** — MySQL test schema via `TEST_DATABASE_URI` is the
   default here. Confirm if a test genuinely needs a real DB (e.g. `FOR UPDATE`,
   `GET_LOCK`, raw SQL) vs. logic that runs fine on SQLite.
3. **Seams to fake** — confirm which externals to stub: AWS/SOAP via
   `test_mode=True` controllers, HTTP via `responses`, Celery via direct method
   calls. Do not hit real services.
4. **New dependency or config change** — if a test needs a new lib, marker, or
   `addopts` change, confirm before editing `pyproject.toml`.

If only *adding* tests to the existing structure (no new infra), a one-line
confirmation of tier + DB is enough.

## Layout

```
tests/
  conftest.py            # root: sqlite UUID adapter, path-based tier auto-marking
  unit/
    conftest.py          # minimal Flask app on in-memory SQLite (StaticPool), NullCache, fixtures
    <pkg path>/test_*.py # mirrors source tree, e.g. unit/lus/pac/test_soap_classification.py
  integration/
    conftest.py          # MySQL app from TEST_DATABASE_URI; auto-skips if unset
    <pkg path>/test_*.py
```

- Import mode is `importlib` (set in `pyproject.toml`). **Do not add `__init__.py`
  under `tests/`.**
- Test files mirror the source path of what they cover.
- Markers `unit` / `integration` are applied automatically by the root conftest
  based on directory — do not hand-mark tests.

## Choosing a tier

1. Pure logic, no I/O → **unit** (fake inputs, assert output/branch).
2. Needs a real query/commit or several layers wired together → **integration**.
3. Correctness only visible under DB-engine semantics (advisory locks, row locks,
   raw SQL) → **integration on MySQL**; SQLite silently no-ops these and would
   pass falsely.

Same method can warrant tests in both tiers: fast logic on SQLite, the
concurrency/lock guarantee on MySQL.

## Writing a unit test

Use the `app` fixture (in-memory SQLite + app context) when you need a DB or
config; omit it for pure-logic tests. Construct controllers with `test_mode=True`
to fake AWS/SOAP. Available fixtures: `app`, `pool`, `account`, `second_account`,
`past`, `future`, and autouse `_reset_toolsboto` (clears the in-memory SSM store).

```python
# tests/unit/lus/pac/test_example.py
from tools.lus.pac.provision import ProvisionController
from tools.lus.pac.controllers.ssm import ToolsBoto


def test_pure_logic():            # no app fixture -> no DB, fastest
    from tools.lus.pac.controllers.soap import SetPasswordResult
    assert SetPasswordResult(status="ok").ok is True


def test_with_db(app, account, past):
    account.next_password_change = past
    account.save()
    pc = ProvisionController(test_mode=True)
    before = ToolsBoto._test_version_counter
    assert pc.provision_expire(account) is True
    assert ToolsBoto._test_version_counter > before   # rotation occurred
```

The in-memory SSM `ToolsBoto._test_version_counter` is the observable signal for
"did a rotation/SSM write actually happen" without real AWS.

## Writing an integration test

Same fixture names (`app`, `pool`, `account`) but backed by MySQL. The test runs
only when `TEST_DATABASE_URI` is set; otherwise it skips. Put it here only when
SQLite can't prove the behavior.

```python
# tests/integration/lus/pac/test_task_claim.py
from tools.lus.pac.controllers.account import AccountController
def test_claim_single_winner(app, account):
    ...  # needs real SELECT ... FOR UPDATE
```

## Running

```bash
.venv/bin/python -m pytest -m unit          # fast loop (default working set)
.venv/bin/python -m pytest                  # all; integration auto-skips without a DB
TEST_DATABASE_URI="mysql+pymysql://tools:tools-password@127.0.0.1:4306/tools_test" \
  .venv/bin/python -m pytest -m integration
.venv/bin/python -m pytest --cov            # coverage (needs `poetry install` for pytest-cov)
```

Rich output for debugging: `-vv -rA --durations=10 --showlocals --log-cli-level=INFO`.

## Gotchas specific to this repo

- **Import-time app context**: report modules must not read `app.config` at module
  import (it breaks collection). Build clients lazily inside functions
  (see `tools/lus/reports/alma_fulfillment.py`). If a new import-time config read
  appears, fix it lazily rather than hacking conftest.
- **In-memory SQLite** needs `StaticPool` + `check_same_thread=False` (already in
  `tests/unit/conftest.py`) so every connection sees the same DB.
- **UUID PKs**: `sqlite3.register_adapter(uuid.UUID, str)` in the root conftest;
  keep it for SQLite tiers.
- **Coverage has no gate** (report only) by design — don't add `fail_under`
  without asking.
- Reference doc: `tests/README.md`.
