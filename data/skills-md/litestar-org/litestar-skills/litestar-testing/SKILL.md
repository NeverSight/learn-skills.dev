---
name: litestar-testing
description: "Auto-activate for test_*.py, conftest.py, litestar.testing, TestClient, AsyncTestClient, create_test_client, create_async_test_client, anyio, Guard mocks, DI overrides, or handler tests. Not for generic pytest."
---

# litestar-testing

Litestar-specific testing patterns built on pytest + anyio. Covers:

- `TestClient` vs `AsyncTestClient` — when to use each
- `@pytest.mark.anyio` setup
- App + lifespan in tests
- Fixture patterns from canonical [litestar-fullstack](https://github.com/litestar-org/litestar-fullstack) tests
- Mocking Guards and DI dependencies
- Integration with `pytest-databases` (see `../pytest-databases/SKILL.md`)
- Autowire discovery and cache isolation (see `../litestar-autowire/references/testing.md`)
- Request body / form / multipart / header / cookie testing
- Litestar-specific assertion patterns (Response, headers, cookies)

For JS-side testing (Vitest, Testing Library, Playwright), use the upstream Vitest docs and Litestar's own JS examples. Out of scope here.

## Code Style Rules

- PEP 604 unions: `T | None`, never `Optional[T]`
- Test modules MAY use `from __future__ import annotations` — they are pure consumer code.
- Function-based tests (not class-based)
- One assertion concern per test
- Async Litestar tests use `@pytest.mark.anyio` by default; do not mix AnyIO and pytest-asyncio auto modes.
- Prefer `AsyncTestClient` for new code; `TestClient` only for legacy / sync-only flows

## Quick Reference

### TestClient vs AsyncTestClient

| Client | When to Use | Lifespan | Internals |
| --- | --- | --- | --- |
| `TestClient` | Sync test bodies, simple smoke tests | Triggered via context manager | Runs ASGI in a thread pool |
| `AsyncTestClient` | **Default for new tests** — async test bodies, lifespan-aware fixtures | Native async lifespan | Runs ASGI in the test event loop |

```python
# AsyncTestClient — preferred
from litestar.testing import AsyncTestClient


async def test_index(async_client: AsyncTestClient):
    resp = await async_client.get("/")
    assert resp.status_code == 200
```

```python
# TestClient — legacy / sync
from litestar.testing import TestClient


def test_index(client: TestClient):
    resp = client.get("/")
    assert resp.status_code == 200
```

### anyio Setup

```python
# conftest.py
import pytest


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
```

```python
# tests/test_x.py
import pytest


@pytest.mark.anyio
async def test_something(): ...
```

Litestar's runtime is anyio-based; do not use `pytest-asyncio` — it conflicts.

### App + Lifespan Fixture

```python
# conftest.py
from collections.abc import AsyncGenerator
import pytest
from litestar import Litestar
from litestar.testing import AsyncTestClient

from app import create_app


@pytest.fixture
async def app() -> Litestar:
    return create_app()


@pytest.fixture
async def async_client(app: Litestar) -> AsyncGenerator[AsyncTestClient, None]:
    async with AsyncTestClient(app=app) as client:
        yield client
```

`async with AsyncTestClient(...)` runs `on_startup` / `on_shutdown` hooks and plugin lifespans (Vite, SAQ, SQLAlchemy session pool, etc.). Without the context manager, lifespan does not fire.

### Mocking Guards

Guards are functions of `(connection, route_handler) -> None`. Test the real
guard with fake identity or authorization providers. Build a fresh app with
replacement providers; Litestar has no mutable `app.dependency_overrides`
registry.

```python
from litestar.di import Provide


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncTestClient, None]:
    fake_users_service = FakeUserService()

    async def provide_fake_users_service() -> UserService:
        return fake_users_service

    test_app = create_app(
        dependencies={
            "users_service": Provide(provide_fake_users_service),
        },
    )
    async with AsyncTestClient(app=test_app) as client:
        yield client
```

### Mocking DI Dependencies

```python
from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
from litestar.di import Provide
from litestar.testing import AsyncTestClient


@pytest.fixture
async def async_client() -> AsyncGenerator[tuple[AsyncTestClient, AsyncMock], None]:
    fake_email = AsyncMock()

    async def provide_fake_email() -> AsyncMock:
        return fake_email

    app = create_app(
        dependencies={
            "email_service": Provide(provide_fake_email),
        },
    )
    async with AsyncTestClient(app=app) as client:
        yield client, fake_email
```

For isolated handler tests, pass replacements directly to
`create_async_test_client(..., dependencies={...})`. Do not mutate a
constructed app; rebuilding preserves dependency resolution and prevents
parallel tests from sharing overrides.

### Integration with pytest-databases

Combine `pytest-databases` fixtures with the app fixture. See `../pytest-databases/SKILL.md`.

```python
# conftest.py
pytest_plugins = ["pytest_databases.docker.postgres"]


@pytest.fixture
async def app(postgres_service) -> Litestar:
    from app import create_app
    from app.config import Settings

    settings = Settings(
        database_url=f"postgresql+asyncpg://{postgres_service.user}:{postgres_service.password}@{postgres_service.host}:{postgres_service.port}/{postgres_service.database}"
    )
    return create_app(settings=settings)
```

The `postgres_service` fixture starts a Postgres container. Inject its connection details into the app config.

### Request Bodies

| Body Type | Pass via |
| --- | --- |
| JSON | `client.post("/", json={...})` |
| Form | `client.post("/", data={...})` |
| Multipart (file upload) | `client.post("/", files={"file": ("name.txt", b"content", "text/plain")})` |
| Raw bytes | `client.post("/", content=b"...")` |
| Custom content-type | `client.post("/", content=b"...", headers={"Content-Type": "..."})` |

```python
async def test_create_user(async_client):
    resp = await async_client.post(
        "/api/users",
        json={"name": "Alice", "email": "alice@example.com"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "Alice"
```

### Headers, Cookies, Auth

```python
# Header
resp = await async_client.get("/", headers={"Authorization": "Bearer token"})

# Cookie
async_client.cookies.set("session", "abc123")
resp = await async_client.get("/")

# Per-request cookies
resp = await async_client.get("/", cookies={"session": "abc123"})
```

### HTMX Requests

```python
async def test_htmx_partial(async_client):
    resp = await async_client.get(
        "/items/list",
        headers={"HX-Request": "true", "HX-Target": "#item-list"},
    )
    assert resp.status_code == 200
    assert "<ul" in resp.text
```

### Response Assertions

```python
# Status
assert resp.status_code == 200

# Body
assert resp.json() == {"id": 1, "name": "Alice"}

# Headers
assert resp.headers["content-type"].startswith("application/json")
assert "HX-Trigger" in resp.headers

# Cookies (set by server)
assert "session" in resp.cookies
```

### Parametrize

```python
import pytest


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"name": "valid", "email": "a@b.co"}, 201),
        ({"name": "", "email": "a@b.co"}, 400),
        ({"name": "valid", "email": "not-email"}, 400),
    ],
)
@pytest.mark.anyio
async def test_create_user_validation(async_client, payload, expected_status):
    resp = await async_client.post("/api/users", json=payload)
    assert resp.status_code == expected_status
```

### Coverage

```bash
pytest --cov=src --cov-report=html
pytest --cov=src --cov-fail-under=90
```

<workflow>

## Workflow

### Step 1: Set Up anyio Backend

Add `anyio_backend` fixture to `conftest.py` returning `"asyncio"`. Mark async tests with `@pytest.mark.anyio`.

### Step 2: App + Client Fixtures

Build an `app` fixture that returns a fresh `Litestar` instance per test (or per session if no shared state). Build an `async_client` fixture that wraps the app in `AsyncTestClient` via `async with`.

### Step 3: Add Database Fixtures

If the app talks to a DB, layer in `pytest-databases` (`postgres_service`, `mysql_service`, etc.) and pass connection details into the app config. See `../pytest-databases/SKILL.md`.

### Step 4: Override DI for Externals

Mock `EmailService`, HTTP clients, and other side-effect-laden dependencies by
constructing a fresh app or test client with replacement `Provide` instances.
Avoid real network calls in tests.

### Step 5: Mock Guards When Needed

Build a fresh app with fake identity or authorization providers. Register a
no-op guard only when the test intentionally excludes authentication behavior;
never patch route internals on a shared app.

### Step 6: Write Tests

- One assertion concern per test.
- Use `@pytest.mark.parametrize` for input variations.
- Use `AsyncTestClient` for new code.
- Include HTMX / Inertia headers when testing those paths.

### Step 7: Verify Coverage

`pytest --cov=src --cov-fail-under=90`. Cover handlers, services, Guards, and at least one happy-path + one error-path per route.

</workflow>

<guardrails>

## Guardrails

- **Use `@pytest.mark.anyio` for new Litestar async tests** — keep pytest-asyncio only when a project already uses it explicitly, and never mix auto modes.
- **Always `async with AsyncTestClient(app=app)`** — without the context manager, plugin lifespans (Vite, SAQ, SQLAlchemy) never run, and tests see a half-initialized app.
- **Prefer `AsyncTestClient` over `TestClient`** for new tests — the async client matches Litestar's runtime model.
- **Mock side effects via DI override**, not patching — keeps tests isolated from import order and global state.
- **Build a fresh app for dependency replacements** — Litestar has no mutable
  dependency-override registry, and shared app mutation races under parallel
  tests.
- **Use `pytest-databases` for real DB testing** — never mock SQLAlchemy / sqlspec internals; assertions on mocked queries don't catch real bugs.
- **Function-based tests** — no class-based test containers unless absolutely needed for shared setup.
- **One assertion concern per test** — failures should pinpoint a single behavior.
- **Don't share state between tests** — fresh app + fresh DB per test (or per module with explicit cleanup).
- **Test the HTMX path with `HX-Request: true`** — handlers that branch on `request.htmx` need both branches covered.
- **Mock email via `backend="memory"` / `InMemoryBackend`** — see `../litestar-email/SKILL.md`.

</guardrails>

<validation>

### Validation Checkpoint

Before delivering Litestar tests, verify:

- [ ] `anyio_backend` fixture returns `"asyncio"`
- [ ] Async tests use `@pytest.mark.anyio`
- [ ] `AsyncTestClient` is wrapped in `async with` (lifespan fires)
- [ ] DI dependencies (email, HTTP clients) are overridden, not patched
- [ ] DB-dependent tests use `pytest-databases` fixtures
- [ ] Guards either pass real auth or use a fresh app with fake identity providers
- [ ] One assertion concern per test; parametrize for input variations
- [ ] HTMX-targeted handlers have tests with `HX-Request: true`
- [ ] Coverage gate (`--cov-fail-under`) is set in CI

</validation>

<example>

## Example

**Task:** Test an account creation endpoint that hits Postgres, sends a welcome email via SAQ, and is guarded by an auth check.

```python
# conftest.py
from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, Mock

import pytest
from litestar import Litestar
from litestar.di import Provide
from litestar.testing import AsyncTestClient

pytest_plugins = ["pytest_databases.docker.postgres"]


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def app(postgres_service) -> tuple[Litestar, AsyncMock]:
    from app import create_app
    from app.config import Settings

    fake_queue = AsyncMock()
    fake_task_queues = Mock()
    fake_task_queues.get.return_value = fake_queue

    async def provide_fake_task_queues() -> Mock:
        return fake_task_queues

    settings = Settings(
        database_url=(
            f"postgresql+asyncpg://{postgres_service.user}:{postgres_service.password}"
            f"@{postgres_service.host}:{postgres_service.port}/{postgres_service.database}"
        ),
    )
    return (
        create_app(
            settings=settings,
            dependencies={
                "task_queues": Provide(provide_fake_task_queues),
            },
        ),
        fake_queue,
    )


@pytest.fixture
async def async_client(
    app: tuple[Litestar, AsyncMock],
) -> AsyncGenerator[tuple[AsyncTestClient, AsyncMock], None]:
    test_app, fake_queue = app
    async with AsyncTestClient(app=test_app) as client:
        yield client, fake_queue
```

```python
# tests/test_accounts.py
import pytest


@pytest.mark.anyio
async def test_create_account_persists_and_queues_email(async_client):
    client, fake_queue = async_client

    resp = await client.post(
        "/api/accounts",
        json={"email": "alice@example.com", "name": "Alice"},
    )

    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "alice@example.com"
    fake_queue.enqueue.assert_awaited_once()
    args, kwargs = fake_queue.enqueue.await_args
    assert args[0] == "send_welcome_email"
    assert kwargs["email"] == "alice@example.com"


@pytest.mark.anyio
@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"email": "valid@example.com", "name": "Valid"}, 201),
        ({"email": "", "name": "Valid"}, 400),
        ({"email": "valid@example.com", "name": ""}, 400),
    ],
)
async def test_create_account_validation(async_client, payload, expected_status):
    client, _ = async_client
    resp = await client.post("/api/accounts", json=payload)
    assert resp.status_code == expected_status
```

</example>

---

## References Index

- **[Async Testing](references/async_testing.md)** — anyio setup, async fixtures, context manager testing, and common pitfalls.

## Cross-References

- **[litestar](../litestar/SKILL.md)** — Litestar fundamentals.
- **[pytest-databases](../pytest-databases/SKILL.md)** — Container-based DB fixtures.
- **[litestar-email](../litestar-email/SKILL.md)** — `backend="memory"` and `InMemoryBackend` for email tests.
- **[litestar-saq](../litestar-saq/SKILL.md)** — Mocking task queues.

## JS-side Testing

For Vitest, Testing Library (React/Vue), and component testing, refer to upstream Vitest docs (<https://vitest.dev/>). This skill covers the Python/Litestar side only.

## Official References

- <https://docs.litestar.dev/2/usage/testing.html>
- <https://github.com/litestar-org/litestar/tree/v2.24.0>
- <https://docs.pytest.org/en/stable/>
- <https://anyio.readthedocs.io/en/stable/testing.html>

## Shared Styleguide Baseline

- [General Principles](../litestar-styleguide/references/general.md)
- [Testing](../litestar-styleguide/references/testing.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
