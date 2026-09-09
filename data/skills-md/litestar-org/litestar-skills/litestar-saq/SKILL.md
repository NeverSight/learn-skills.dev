---
name: litestar-saq
description: "Auto-activate for litestar_saq, SAQPlugin, SAQConfig, QueueConfig, TaskQueues, CronJob, litestar workers run, background jobs, schedules, or SAQ web UI. Not for Celery, RQ, or Dramatiq — use their respective integrations or litestar-queues."
---

# litestar-saq

`litestar-saq` is the first-party plugin that integrates [SAQ (Simple Async Queue)](https://github.com/tobymao/saq) with Litestar. It provides:

- `SAQPlugin` — registers queues, workers, lifespan management, and DI for `TaskQueues`
- `SAQConfig` / `QueueConfig` — declarative plugin, queue, worker, broker, shutdown, polling, and OpenTelemetry configuration
- `litestar workers run` — CLI to start worker processes, optionally filtered by queue
- Optional web UI mounted under the Litestar app
- DI injection of `TaskQueues` into route handlers for ergonomic enqueueing

## Code Style Rules

- Use PEP 604 unions: `T | None`, never `Optional[T]`
- Async all I/O — task bodies and enqueue calls are `async def`.
- First positional arg of every task is `ctx: dict` (the SAQ context dict).
- Pass job payload as keyword arguments so task signatures and enqueue calls stay explicit.
- Use `NamedDependency[TaskQueues]` for handler injection. `TaskQueues` is registered under the `task_queues` dependency key, and Litestar 2.24 deprecates implicit DI.

## Quick Reference

### Plugin Setup (canonical pattern)

The canonical pattern from [litestar-fullstack](https://github.com/litestar-org/litestar-fullstack) (`src/py/app/server/plugins.py`) uses lazy initialization and `use_server_lifespan=True` so worker child processes start and stop with the Litestar server lifespan.

**Redis broker:** Use this when Redis is already in the stack or is the chosen SAQ backend:

```python
from litestar_saq import CronJob, QueueConfig, SAQConfig, SAQPlugin

from app.lib.settings import get_settings


def create_saq_plugin() -> SAQPlugin:
    settings = get_settings()
    return SAQPlugin(
        config=SAQConfig(
            use_server_lifespan=True,
            web_enabled=settings.saq.web_enabled,
            enable_otel=None,
            queue_configs=[
                QueueConfig(
                    name="default",
                    dsn=settings.redis.url,
                    tasks=["app.domain.system.tasks.send_email"],
                    scheduled_tasks=[
                        CronJob(
                            function="app.domain.system.tasks.cleanup_sessions",
                            cron="*/15 * * * *",
                            timeout=120,
                        ),
                    ],
                ),
            ],
        ),
    )


saq_plugin = create_saq_plugin()
```

**PostgreSQL broker:** Install `litestar-saq[psycopg]` when PostgreSQL is the chosen backend:

```python
from litestar_saq import QueueConfig, SAQConfig, SAQPlugin

from app.lib.settings import get_settings


def create_saq_plugin_pg() -> SAQPlugin:
    settings = get_settings()
    return SAQPlugin(
        config=SAQConfig(
            use_server_lifespan=True,
            web_enabled=settings.saq.web_enabled,
            queue_configs=[
                QueueConfig(
                    name="default",
                    dsn=settings.database.url,
                    tasks=["app.domain.system.tasks.send_email"],
                ),
            ],
        ),
    )
```

Choose the broker already supported by the deployment. PostgreSQL job writes use
SAQ's own pool and transaction; they are not automatically atomic with writes
made through an application ORM or SQL session.

Each `QueueConfig` accepts exactly one connection source: a supported `redis://`,
`postgresql://`, or `http://` `dsn`, or a supported `broker_instance`. Supplying
both or neither raises `ImproperlyConfiguredException`. PostgreSQL requires
`litestar-saq[psycopg]`; configure queue behavior with `broker_options` and
connection/client construction with `broker_instance_options`.

### Wire into Litestar

```python
from litestar import Litestar
from app.server.plugins import saq_plugin

app = Litestar(
    route_handlers=[...],
    plugins=[saq_plugin],
)
```

### Define a Task

Task functions live in `app/domain/<domain>/tasks.py`:

```python
async def send_email(ctx: dict, *, recipient: str, subject: str, body: str) -> None:
    """Send an email as a background job.

    Args:
        ctx: SAQ context dict populated by worker hooks.
        recipient: To address.
        subject: Email subject.
        body: Email body.
    """
    email_service = ctx["email_service"]
    await email_service.send(recipient, subject, body)
```

For long-running work, set the job's `heartbeat` stale threshold and decorate the task with `monitored_job()` so the plugin signals its batched `HeartbeatManager` while the task runs. `heartbeat` is not an update interval: SAQ marks an active job stuck when its last touch is older than that threshold.

```python
from litestar_saq import monitored_job


@monitored_job()
async def rebuild_index(ctx: dict, *, index_name: str) -> dict[str, str]:
    await run_rebuild(index_name)
    return {"status": "complete"}
```

### Enqueue from a Handler (DI of TaskQueues)

```python
from litestar import Controller, post
from litestar.di import NamedDependency
from litestar_saq import TaskQueues


class NotificationController(Controller):
    path = "/api/notifications"

    @post("/")
    async def queue_notification(
        self,
        data: NotificationCreate,
        task_queues: NamedDependency[TaskQueues],
    ) -> dict[str, str]:
        queue = task_queues.get("default")
        job = await queue.enqueue(
            "send_email",
            recipient=data.email,
            subject=data.subject,
            body=data.body,
            timeout=30,
            retries=2,
            key=f"notify-{data.email}",
        )
        return {"status": "queued" if job is not None else "duplicate"}
```

### CLI

```bash
# Run workers (uses the same Litestar app)
litestar --app app:app workers run

# Run multiple worker processes
litestar --app app:app workers run --workers 4

# Run only selected queues in this worker service
litestar --app app:app workers run --queues emails --queues reports

# Inspect queues
litestar --app app:app workers status
```

### Web UI

When `web_enabled=True`, the SAQ web UI is mounted under the Litestar app for queue introspection and job retry.

### Job Options

| Option | Default | Use |
| --- | --- | --- |
| `timeout` | `10` | **Always set explicitly** — SAQ's default is usually too low or too high for real jobs |
| `retries` | `1` | Retry count on exception |
| `retry_delay` | `0.0` | Seconds to wait before retrying |
| `retry_backoff` | `False` | `True` for exponential backoff with jitter, or a numeric maximum delay |
| `ttl` | `600` | Seconds to retain result after completion |
| `key` | generated | Stable uniqueness key; enqueue returns `None` while that key already exists |
| `heartbeat` | `0` | Maximum seconds an active job may go without a touch; `0` disables stale detection |
| `scheduled` | `0` | Unix timestamp to delay start |

<workflow>

## Workflow

### Step 1: Install

```bash
pip install litestar-saq
pip install "litestar-saq[psycopg]"  # PostgreSQL broker
pip install "litestar-saq[otel]"     # OpenTelemetry spans
```

### Step 2: Define Queues

Build `QueueConfig` instances for each logical queue (`"default"`, `"emails"`, `"reports"`). Put exactly one of `dsn` or `broker_instance` on each `QueueConfig`. Reference task functions by dotted path or callable; the plugin imports dotted paths at startup.

### Step 3: Configure Plugin

Wrap `QueueConfig`s in `SAQConfig`. Pick a supported broker DSN
(`redis://...`, `postgresql://...`, or `http://...`) that matches the
deployment. Set `use_server_lifespan=True` when the web process should own
worker child processes. Toggle `web_enabled` / `web_guards` for the
introspection UI and `enable_otel` for tracing.

### Step 4: Define Tasks

Place task functions in `app/domain/<domain>/tasks.py`. Use `ctx: dict` as the
first argument and pass job data as keywords. Add shared resources (DB, HTTP
client, email service) in `QueueConfig.startup` / `before_process` hooks and
read them from `ctx`.

### Step 5: Schedule Cron Work

Add `CronJob` entries to `QueueConfig.scheduled_tasks` for recurring work. Always set `timeout`. Do not use external cron tools for work that belongs in the queue.

### Step 6: Enqueue from Handlers

Inject `TaskQueues` into route handlers. Use `task_queues.get("name")` then `await queue.enqueue("task_name", ...)`. The result is the new `Job`, or `None` when its unique `key` already exists; handle both outcomes. Use `key=` for deduplication.

### Step 7: Publish to Channels (optional)

For real-time updates after a job completes, publish to Litestar Channels from inside the task. See `../litestar-realtime/references/websockets.md`.

### Step 8: Run

For dev: `litestar run` can start worker child processes when `use_server_lifespan=True`.
For production: run `litestar workers run --workers N` as a separate service/process from `litestar run`. There is no `--process` flag in litestar-saq 0.8.0.
For portable multi-process workers, configure each queue with `dsn`. Under `spawn` and `forkserver`, litestar-saq removes cached live broker objects from the child configuration and rebuilds them from that DSN.

</workflow>

<guardrails>

## Guardrails

- **Use `litestar-saq`, not raw SAQ, in Litestar apps** — the plugin handles DI, lifespan, CLI, and the web UI. Raw SAQ misses all of that.
- **Always set `timeout`** on tasks and CronJobs — SAQ defaults to 10s, which is rarely the correct production value.
- **Pair `heartbeat` with `monitored_job()` for long-running jobs** — `heartbeat` defines when a job is stale; it does not emit updates. Keep the stale threshold longer than the decorator signal interval and the heartbeat manager's flush cadence.
- **Inject `TaskQueues` via DI** — don't import a global queue inside handlers. The plugin owns the queue lifecycle.
- **Use `CronJob` for scheduled work** — not external cron. CronJobs participate in retries, timeouts, and observability.
- **Handle `queue.enqueue()` returning `None`** — an existing unique key prevents insertion, so do not report every enqueue attempt as newly queued.
- **Use `key=` for deduplication** — same logical job (per-user sync, per-resource refresh) should not stack. The key remains occupied until the stored job expires or is removed, including after terminal completion.
- **`use_server_lifespan=True`** for dev and small-to-mid apps that should start worker child processes with the web server. For high-throughput production, run `litestar workers run --workers N` as a separate service.
- **Use `dsn` for portable multi-process workers** — forkserver/spawn workers rebuild brokers from `QueueConfig.dsn`. A `broker_instance`-only queue works in the parent and under `fork`, but spawn preparation rejects it.
- **Set graceful shutdown controls for long jobs** — use `shutdown_grace_period_s` and, when needed, `cancellation_hard_deadline_s` on `QueueConfig`.
- **Publish to Litestar Channels from tasks** when the job result must update connected websocket clients. See `../litestar-realtime/references/websockets.md`.
- **Pull shared resources from `ctx` populated by `QueueConfig` hooks**, not module-level globals — keeps tests deterministic and supports per-worker init.

</guardrails>

<validation>

### Validation Checkpoint

Before delivering Litestar + SAQ code, verify:

- [ ] `SAQPlugin` is in `app.plugins`
- [ ] `SAQConfig.use_server_lifespan` is set explicitly
- [ ] `SAQConfig.worker_processes` or CLI `--workers` is set intentionally
- [ ] Each `QueueConfig` has exactly one of `dsn` or `broker_instance`
- [ ] Multi-process worker configs use `dsn`, not `broker_instance` only
- [ ] Each `QueueConfig` lists tasks by dotted path; the imports resolve
- [ ] All tasks have `ctx: dict` as the first positional arg and receive job data as keywords
- [ ] Every task has `timeout` set
- [ ] Long-running jobs have a `heartbeat` stale threshold longer than their update cadence
- [ ] Long-running task functions use `monitored_job()` when they need automatic heartbeats
- [ ] CronJobs have `timeout` and a sensible `cron` expression
- [ ] Handlers enqueue via injected `TaskQueues`, not module globals
- [ ] Handlers account for `queue.enqueue()` returning `None` for an existing unique key
- [ ] Job dedup uses `key=` where applicable
- [ ] Production deploys run workers as a separate service (`litestar workers run --workers N`)

</validation>

<example>

## Example

**Task:** A Litestar app with a default queue, an email task, a cleanup CronJob, and a handler that enqueues notifications. This example uses Redis as the SAQ broker; swap `dsn=settings.redis.url` for `dsn=settings.database.url` if the project is PG-only — see Quick Reference above for both patterns.

Plugin creation in `app/server/plugins.py`:

```python
from litestar_saq import CronJob, QueueConfig, SAQConfig, SAQPlugin

from app.lib.settings import get_settings


def create_saq_plugin() -> SAQPlugin:
    settings = get_settings()
    return SAQPlugin(
        config=SAQConfig(
            use_server_lifespan=True,
            web_enabled=settings.saq.web_enabled,
            queue_configs=[
                QueueConfig(
                    name="default",
                    dsn=settings.redis.url,
                    startup="app.domain.system.tasks.worker_startup",
                    shutdown="app.domain.system.tasks.worker_shutdown",
                    tasks=[
                        "app.domain.system.tasks.send_email",
                        "app.domain.system.tasks.cleanup_sessions",
                    ],
                    scheduled_tasks=[
                        CronJob(
                            function="app.domain.system.tasks.cleanup_sessions",
                            cron="*/15 * * * *",
                            timeout=120,
                        ),
                    ],
                ),
            ],
        ),
    )


saq_plugin = create_saq_plugin()
```

Task definitions in `app/domain/system/tasks.py`:

```python
async def worker_startup(ctx: dict) -> None:
    """Initialize shared resources for this worker."""
    ctx["email_service"] = create_email_service()
    ctx["db"] = create_database_client()


async def worker_shutdown(ctx: dict) -> None:
    """Dispose shared worker resources."""
    await ctx["db"].close()


async def send_email(ctx: dict, *, recipient: str, subject: str, body: str) -> None:
    """Send an email as a background job."""
    email = ctx["email_service"]
    await email.send(recipient, subject, body)


async def cleanup_sessions(ctx: dict) -> None:
    """Purge expired sessions every 15 minutes."""
    db = ctx["db"]
    await db.execute("DELETE FROM session WHERE expires_at < now()")
```

Controller enqueueing in `app/domain/notifications/controllers.py`:

```python
from litestar import Controller, post
from litestar.di import NamedDependency
from litestar_saq import TaskQueues

from app.domain.notifications.schemas import NotificationCreate


class NotificationController(Controller):
    path = "/api/notifications"
    tags = ["Notifications"]

    @post("/")
    async def queue_notification(
        self,
        data: NotificationCreate,
        task_queues: NamedDependency[TaskQueues],
    ) -> dict[str, str]:
        queue = task_queues.get("default")
        job = await queue.enqueue(
            "send_email",
            recipient=data.email,
            subject=data.subject,
            body=data.body,
            timeout=30,
            retries=2,
            key=f"notify-{data.email}",
        )
        return {"status": "queued" if job is not None else "duplicate"}
```

Application entrypoint in `app.py`:

```python
from litestar import Litestar

from app.domain.notifications.controllers import NotificationController
from app.server.plugins import saq_plugin


app = Litestar(
    route_handlers=[NotificationController],
    plugins=[saq_plugin],
)
```

Running in development (workers start with server lifespan) and production:

```bash
litestar --app app:app run
litestar --app app:app workers run --workers 4
```

</example>

---

## References Index

- **[Advanced Patterns](references/patterns.md)** — Heartbeat tuning, dead-letter handling, job chaining, queue priorities, worker lifecycle hooks, Postgres backend.
- **[Sidecar Worker Pattern](references/postgres-native-sidecar-worker.md)** — optional application-owned worker architecture; it is not part of `litestar-saq` or SAQ.

## Cross-References

- **[litestar](../litestar/SKILL.md)** — Litestar app initialization, plugins, and lifespan.
- **[litestar websockets reference](../litestar-realtime/references/websockets.md)** — Publish from a SAQ task to Litestar Channels for real-time UI updates.

## Official References

- <https://github.com/litestar-org/litestar-saq/tree/v0.8.0>
- <https://pypi.org/project/litestar-saq/0.8.0/>
- <https://github.com/tobymao/saq/tree/v0.26.4>

## Shared Styleguide Baseline

- Use shared styleguides for generic language/framework rules to reduce duplication in this skill.
- [General Principles](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
- Keep this skill focused on tool-specific workflows, edge cases, and integration details.
