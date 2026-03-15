---
name: python-services
description: >-
  Python patterns for CLI tools, async concurrency, and backend services. Use
  when working with Python code, building CLI apps, FastAPI services,
  async with asyncio, background jobs, or configuring uv, ruff, ty, pytest, or
  pyproject.toml.
---

# Python Services & CLI

## Modern Tooling

| Tool | Replaces | Purpose |
|------|----------|---------|
| **uv** | pip, virtualenv, pyenv, pipx | Package/dependency management |
| **ruff** | flake8, black, isort | Linting + formatting |
| **ty** | mypy, pyright | Type checking (Astral, faster) |

- `uv init --package myproject` for distributable packages, `uv init` for apps
- `uv add <pkg>`, `uv add --group dev <pkg>`, never edit pyproject.toml deps manually
- `uv run <cmd>` instead of activating venvs
- `uv.lock` goes in version control
- Use `[dependency-groups]` (PEP 735) for dev/test/docs, not `[project.optional-dependencies]`
- PEP 723 inline metadata for standalone scripts with deps
- `ruff check --fix . && ruff format .` for lint+format in one pass

See [cli-tools.md](./references/cli-tools.md) for Click patterns, argparse, and CLI project layout.

## Parallelism

| Workload | Approach |
|----------|----------|
| Many concurrent I/O calls | `asyncio` (gather, create_task) |
| CPU-bound computation | `multiprocessing.Pool` or `concurrent.futures.ProcessPoolExecutor` |
| Mixed I/O + CPU | `asyncio.to_thread()` to offload blocking work |
| Simple scripts, few connections | Stay synchronous |

**Key rule:** Stay fully sync or fully async within a call path.

**asyncio patterns:**
- `asyncio.gather(*tasks)` for concurrent I/O — use `return_exceptions=True` for partial failure tolerance
- `asyncio.TaskGroup` (3.11+) for structured concurrency — automatic cancellation of sibling tasks on failure; prefer over `gather` when all tasks must succeed
- `asyncio.Semaphore(n)` to limit concurrency (rate limiting external APIs)
- `asyncio.wait_for(coro, timeout=N)` for timeouts
- `asyncio.Queue` for producer-consumer
- `asyncio.Lock` when coroutines share mutable state
- Never block the event loop: `asyncio.to_thread(sync_fn)` for sync libs, `aiohttp`/`httpx.AsyncClient` for HTTP
- Handle `CancelledError` — always re-raise after cleanup
- Async generators (`async for`) for streaming/pagination

**multiprocessing** for CPU-bound:
```python
from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(cpu_task, items))
```

See [fastapi.md](./references/fastapi.md) for project structure, lifespan, config, DI, async DB, and repository pattern.

## Background Jobs

- Return job ID immediately, process async. Client polls `/jobs/{id}` for status
- **Celery**: `@app.task(bind=True, max_retries=3, autoretry_for=(ConnectionError,))` — exponential backoff: `raise self.retry(countdown=2**self.request.retries * 60)`
- **Alternatives**: Dramatiq (modern Celery), RQ (simple Redis), cloud-native (SQS+Lambda, Cloud Tasks)
- **Idempotency is mandatory** — tasks may retry. Use idempotency keys for external calls, check-before-write, upsert patterns
- Dead letter queue for permanently failed tasks after max retries
- Task workflows: `chain(a.s(), b.s())` for sequential, `group(...)` for parallel, `chord(group, callback)` for fan-out/fan-in

## Resilience

**Retries with tenacity:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, retry_if_exception_type

@retry(
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
    stop=stop_after_attempt(5) | stop_after_delay(60),
    wait=wait_exponential_jitter(initial=1, max=30),
    before_sleep=log_retry_attempt,
)
def call_api(url: str) -> dict: ...
```

- Retry only transient errors: network, 429/502/503/504. Never retry 4xx (except 429), auth errors, validation errors
- Every network call needs a timeout
- `@fail_safe(default=[])` decorator for non-critical paths — return cached/default on failure
- `functools.lru_cache(maxsize=N)` for pure-function memoization; `functools.cache` (unbounded) for small domains
- Stack decorators: `@traced @with_timeout(30) @retry(...)` — separate infra from business logic

**Connection pooling** is mandatory for production: reuse `httpx.AsyncClient()` across requests, configure SQLAlchemy `pool_size`/`max_overflow`, use `aiohttp.TCPConnector(limit=N)`.

## Observability

- **structlog** for JSON structured logging. Configure once at startup with `JSONRenderer`, `TimeStamper`, `merge_contextvars`
- **Correlation IDs** — generate at ingress (`X-Correlation-ID` header), bind to `contextvars`, propagate to downstream calls
- **Log levels**: DEBUG=diagnostics, INFO=operations, WARNING=anomalies handled, ERROR=failures needing attention. Never log expected behavior at ERROR
- **Prometheus metrics** — track latency (Histogram), traffic (Counter), errors (Counter), saturation (Gauge). Keep label cardinality bounded (no user IDs)
- **OpenTelemetry** for distributed tracing across services

## Discipline

- For non-trivial changes, pause and ask: "is there a more elegant way?" Skip for obvious fixes.
- Simplicity first — every change as simple as possible, impact minimal code
- Only touch what's necessary — avoid introducing unrelated changes
- No hacky workarounds — if a fix feels wrong, step back and implement the clean solution
- Verify: `uv run pytest && uv run ruff check .` pass with zero warnings before declaring done

## Error Handling

- Validate inputs at boundaries before expensive ops. Report all errors at once when possible
- Use specific exceptions: `ValueError`, `TypeError`, `KeyError`, not bare `Exception`
- `raise ServiceError("upload failed") from e` — always chain to preserve debug trail
- Convert external data to domain types (enums, Pydantic models) at system boundaries
- Batch processing: `BatchResult(succeeded={}, failed={})` — don't let one item abort the batch
- Pydantic `BaseModel` with `field_validator` for complex input validation
