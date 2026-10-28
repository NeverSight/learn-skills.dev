---
name: pytest
description: |
  Pytest testing standards emphasizing the AAA pattern, fixtures, and parametrize.
  Use when writing or reviewing Python tests with pytest, including Django tests.
  Covers fixture organization, database access patterns, API testing, and mock clients.
  Do NOT use for: JavaScript/TypeScript tests, unittest-style tests, or non-pytest
  frameworks.
metadata:
  imankulov.skills-sh-group: Python
  imankulov.skills-sh-order: "40"
  imankulov.claude-display-name: Pytest
  imankulov.claude-category: development
  imankulov.claude-keywords: "pytest,agent-skills"
---

# Pytest Standards

Opinionated testing conventions for pytest, with Django-specific patterns included.

## AAA Pattern (Arrange-Act-Assert)

Structure every test with `# Arrange`, `# Act`, `# Assert` comments separating setup,
execution, and verification. Arrange primarily through fixtures. Omit any section you
don't need rather than leaving it empty. Multiple assertions are fine when logically
connected.

```python
def test_user_service_create(sample_user, db_session):
    # Arrange
    service = UserService(db_session)

    # Act
    created_user = service.create(sample_user)

    # Assert
    assert created_user.id is not None
    assert created_user.name == sample_user.name
```

## Test Organization

- Store tests in a `tests/` subdirectory within each module.
- Name test files to match tested modules: `services.py` -> `tests/test_services.py`.
- Write flat pytest functions, never test classes.

## Fixtures

Before creating a fixture, look for an existing one in this order: root `conftest.py`,
the module's `tests/conftest.py`, then the current test file. Create a new one only if
none fits.

Place fixtures shared across a module's test files in `tests/conftest.py`, not in
individual test files. Order fixtures by scope: session -> module -> function.

## Parametrize

Use `@pytest.mark.parametrize` for testing multiple input/output combinations rather
than repeating near-identical test bodies.

## Running Tests

```bash
# All tests (excluding e2e)
uv run pytest -m "not e2e" -q --tb=short

# Stop at the first failure, then iterate on only what failed
uv run pytest -m "not e2e" -q --tb=short -x
uv run pytest --lf -q --tb=short

# Full assertion diff for one test, once you know which one failed
uv run pytest path/to/test_file.py::test_function_name -vv
```

Run with `-q --tb=short`. `-q` collapses passing tests into progress dots while keeping
the `FAILED path::test_name - reason` summary, so output stays flat as the suite grows;
`-v`/`-vv` print a line per passing test, which costs roughly 10k tokens of context on a
green 500-test suite against ~150 for `-q`.

Leave `-s` off. Pytest already replays a failing test's `Captured stdout call`,
`Captured stderr call`, and `Captured log call` sections; `-s` adds only the output of
tests that passed.

Escalate to `-vv` on a single node ID, never the whole suite. At default verbosity pytest
trims long assertion diffs to the differing items and prints `use -vv to show` — re-run
that one test when the trimmed diff isn't enough.

Exclude e2e tests by default — they call external services and are slow/flaky. Only run
e2e when changes directly affect e2e-tested code.

Make the defaults stick in `pyproject.toml` so every invocation inherits them:

```toml
[tool.pytest.ini_options]
addopts = "-q --tb=short"
```

## Django Test Database

On Django projects, extend `addopts` with `--reuse-db` so the test database survives
between runs instead of being dropped and rebuilt from migrations every time:

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "myproject.settings"
addopts = "-q --tb=short --reuse-db"
```

Adding a migration needs no extra flag — `--reuse-db` only skips dropping and recreating
the database, not the `migrate` that follows, so new migrations apply on the next run.
Pairing it with `--no-migrations` breaks that: the schema is then built by `run_syncdb`,
which creates missing tables but never alters existing ones, so every schema change from
then on needs `--create-db`.

Reach for `--create-db` when the reused database is genuinely broken, which shows up as a
schema error contradicting the current models:

- `OperationalError: table myapp_thing has no column named shade` — an existing migration
  was edited in place, so the database has it recorded as applied and never re-runs it
- `IntegrityError: NOT NULL constraint failed: ...` or `InconsistentMigrationHistory` —
  the database still carries a migration the current branch no longer has

```bash
uv run pytest --create-db
```

`--create-db` overrides `--reuse-db` for that run and leaves the rebuilt database in place
for the next one, so pass it once rather than adding it to `addopts`.

## Django Database Access

A test gets database access automatically if any of its fixtures depends on `db`
(directly or transitively). Only when no fixture brings that dependency does the test
need `@pytest.mark.django_db`.

```python
# No decorator — client_with_user brings db via the user fixture
def test_create_report_success(client_with_user):
    response = client_with_user.post("/api/v1/reports", ...)
    assert response.status_code == 200

# Decorator needed — client alone doesn't bring db
@pytest.mark.django_db
def test_create_report_requires_auth(client):
    response = client.post("/api/v1/reports", ...)
    assert response.status_code == 401
```

## Django API Testing

Test API endpoints with the Django test client: the `client` fixture for
unauthenticated requests and `client_with_user` for authenticated ones. Use these
rather than `ninja.testing.TestClient`. Post JSON with
`content_type="application/json"`. For database mutation tests, add ORM assertions on
the resulting state:

```python
assert User.objects.get(id=user.id).settings.theme == "dark"
```

## Mock Client Testing

The test environment configures clients through `.env.test` with a real mock provider,
so use the mock client directly and assert on the data it captures. Reference class
constants from mock clients directly, and keep global state untouched (no `make_empty()`
or similar). Leave the `get_*_client()` factory functions unmocked — mocking them breaks
the dependency chain.

```python
def test_event_is_captured(posthog_client):
    some_function_that_captures_event()

    assert len(posthog_client.events) == 1
    assert posthog_client.events[0]["event"] == "oauth_completed"
```

## Assertions for HTTP Responses

Assert the full body for short responses (`assert response.json() == {...}`). For long
responses, assert on the key fields that matter rather than the whole payload.

## Regression Tests

Reproduce a reported bug at the closest stable public boundary. A regression test
should use the request shape, input normalization, and output that failed, rather than
only testing a newly added helper or asserting that one argument was forwarded.

For integrations, avoid a live third-party call when the generated provider request is
the behavior under test. Capture the request at the configured mock/client boundary,
then assert the exact filters, normalized identifiers, or cache inputs that caused the
bug. Keep a focused unit test for complicated helpers, but do not use it as a substitute
for the boundary regression.

## Cache Identity Tests

When behavior is cached, list every input that can change the result. Each input must
either appear in the cache key or resolve to an identity that does, such as a selected
property ID. Add a test proving that two semantically different requests do not share a
cache entry, especially for tenant, locale, scope, filter, permission, and date inputs.

Do not add redundant key parts when a stronger resolved identity already separates the
results. Document that identity in the test so a later change to resolution does not
silently invalidate the assumption.

## E2E Tests

Apply the `@pytest.mark.e2e` marker when a test is something a local `pytest` run should
skip by default because it:

- Hits external/third-party services (real LLM provider, Stripe, GitHub API, etc.)
- Requires paid resources or burns API quota
- Needs extra setup or credentials beyond the standard dev environment (live database,
  browser drivers, secrets, network access to internal hosts)
- Drives a real browser (Playwright, Selenium)
- Is noticeably slow (multi-second) or flaky by nature

A test that spins up an in-process server, mock target, or local subprocess and runs
self-contained is an integration test, not e2e — including one that boots a real uvicorn
on a random port and makes localhost requests.

The marker alone is sufficient; no `os.environ` checks needed. CI skips them with
`pytest -m "not e2e"`. To mark every test in a file, set `pytestmark = pytest.mark.e2e`
at module level.
