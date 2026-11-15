---
name: stario-jobs
description: Slow work in a Stario app - a report, a model call, a download, an import - as a job that a command queues and a task runs while the page shows queued, running, and done. Use when a button starts work that takes seconds, when several jobs may run at once, when the page must update by itself while the work runs, when a job must stop cleanly on shutdown or survive a restart, or when a loop runs on a timer.
---

# Slow work as a job

`AGENTS.md` holds the rules. Look up a name in `stario-api` only when this skill and the code do not show it. The page is a live page on a `Relay` (skill `stario-relay`): the command queues a job and replies at once. A task does the work inside its own span and publishes each status change. The `queued` row is the click feedback.

```python
# data.py
from dataclasses import dataclass, field
from itertools import count


@dataclass(slots=True)
class Job:
    id: int
    status: str = "queued"  # queued | running | done | failed
    result: str = ""


@dataclass(slots=True)
class Jobs:
    rows: dict[int, Job] = field(default_factory=dict)
    ids: count[int] = field(default_factory=lambda: count(1))


def add_job(jobs: Jobs) -> Job:
    job = Job(next(jobs.ids))
    jobs.rows[job.id] = job
    return job


def list_jobs(jobs: Jobs) -> list[Job]:
    return sorted(jobs.rows.values(), key=lambda j: j.id, reverse=True)
```

```python
# urls.py
REPORTS = Route("GET /reports")
REPORTS_LIVE = Route("GET /reports/live")
START_REPORT = Route("POST /reports")
```

```python
# views.py
def render(jobs: list[Job]) -> HtmlElement:
    return page(
        "Reports",
        h.Main(
            {"id": "reports"},
            data.init(at.get(REPORTS_LIVE.href(), retry="always")),
            h.Button(
                {"type": "button"},
                data.on("click", at.post(START_REPORT.href())),
                data.indicator("_starting"),
                data.attr("disabled", "$_starting"),
                "Generate report",
            ),
            h.Ul(*[h.Li({"id": f"job-{j.id}"}, f"#{j.id} {j.status} {j.result}") for j in jobs]),
        ),
    )
```

The button carries `data.indicator` because its own `data.on` sends the request.

```python
# handlers.py
import asyncio
from dataclasses import dataclass
from datetime import UTC, datetime

from stario import App, Context, Relay, Span, Writer
from stario.datastar import SSE

CHANGED = "reports.changed"


@dataclass(frozen=True, slots=True)
class ReportsPage:
    jobs: Jobs
    relay: Relay[dict]
    delay: float

    def register(self, app: App) -> None:
        app.add(REPORTS, self.show)
        app.add(REPORTS_LIVE, self.live)
        app.add(START_REPORT, self.start)

    async def show(self, c: Context, w: Writer) -> None:
        w.html(render(list_jobs(self.jobs)))

    async def live(self, c: Context, w: Writer) -> None:
        async with self.relay.subscribe(CHANGED, latest=True) as events:
            sse = SSE(w)
            sse.patch_elements(render(list_jobs(self.jobs)))
            async for _ in c.alive(events):
                sse.patch_elements(render(list_jobs(self.jobs)))

    async def start(self, c: Context, w: Writer) -> None:
        job = add_job(self.jobs)
        w.empty()
        self.relay.publish(CHANGED, {})
        c.app.create_task(self.run(job, c.span.step("report.run")))

    async def run(self, job: Job, span: Span) -> None:
        with span:
            span.attrs({"job.id": job.id})
            job.status = "running"
            self.relay.publish(CHANGED, {})
            try:
                await asyncio.sleep(self.delay)
                job.result, job.status = f"Report at {datetime.now(UTC):%H:%M:%S}", "done"
            except asyncio.CancelledError:
                job.result, job.status = "stopped: the server shut down", "failed"
                raise
            except Exception as exc:
                job.result, job.status = str(exc), "failed"
                span.fail(str(exc))
            finally:
                self.relay.publish(CHANGED, {})
```

```python
# app/main.py, inside bootstrap before yield
ReportsPage(Jobs(), relay, config.report_delay).register(app)
```

`report_delay` is a `Config` field: `float(os.environ.get("REPORT_DELAY", "5"))`. A test sets it to `0`.

- `c.span.step("report.run")` is a child of the request span. The task enters it with `with span:`, so the job has its own duration, events, and error in the trace.
- `c.app.create_task`, never bare `asyncio.create_task`. Stario tracks the task and waits for it on shutdown.
- An error goes to the job row and to the span. Nothing is lost when the request has already ended.
- On shutdown, Stario waits `STARIO_GRACEFUL_SHUTDOWN_TIMEOUT` (5 s), then cancels the task. `CancelledError` marks the job failed and is raised again.
- A job with several steps passes `c.app` to `run`, checks `app.shutting_down` between the steps, and stops early.
- Several jobs run at once: each click is its own task.
- A message to the tab that started the job (a toast when it fails): skill `stario-relay`, A message after the work.

## A loop on a timer

Work that runs every few seconds or minutes with no click: a sweep, a poll, a cleanup. `bootstrap` starts the loop. Each pass ends with a wait on `app.shutdown`.

```python
# app/cleanup.py
import asyncio

from stario import App

from .data import Jobs


async def drop_finished_forever(app: App, jobs: Jobs, interval: float) -> None:
    shutdown = app.shutdown
    while not app.shutting_down:
        for job in list(jobs.rows.values()):
            if job.status in ("done", "failed"):
                del jobs.rows[job.id]
        await asyncio.wait({shutdown}, timeout=interval)
```

```python
# app/main.py, inside bootstrap before yield
app.create_task(drop_finished_forever(app, jobs, 600), name="jobs.drop_finished")
```

- `asyncio.wait` returns after `interval`, or at once when shutdown starts. It does not cancel `app.shutdown`.
- Read `app.shutdown` once, before the loop. Each read makes a new shield, and each pending shield keeps a callback on the app's future until shutdown.
- Never end a pass with `asyncio.sleep(interval)`. The drain then waits up to one interval, and after 5 s it cancels the loop.
- The loop finishes its current pass, then stops at the `while` check.
- A loop that waits on a queue or an event waits on `shutdown` too: `asyncio.wait({event_wait, shutdown}, timeout=...)`. Clear the event after the wait, so a set that comes during a pass is not lost.
- In a handler, use `c.alive()` instead.
- The `server.shutdown` span gets one `server.shutdown.task_cancelled` event, with `task.name`, for each task that the drain cancels (stario 5.3.2). Give the loop a `name`. A test checks that the loop stops in time:

```python
async def test_loops_stop_on_shutdown():
    async with TestClient(bootstrap) as client:
        pass
    shutdown = client.tracer.find_span("server.shutdown")
    assert not client.tracer.get_events(shutdown.id, name="server.shutdown.task_cancelled")
```

## Tests

```python
# tests/conftest.py: monkeypatch.setenv("REPORT_DELAY", "0") in the client fixture


async def test_a_job_runs_to_done(client):
    async with client.stream("GET", REPORTS_LIVE.href(), timeout=2) as live:
        events = live.iter_events()
        await anext(events)
        assert (await client.post(START_REPORT.href())).status_code == 204
        async for event in events:
            if "done" in event["data"]:
                break
    await client.drain_tasks()
    assert client.tracer.find_span("report.run").ok
```

The test reads events until one contains `done`. `timeout=2` covers the whole stream, so it must be longer than the delay of the job.

## Jobs in SQLite

A job row in SQLite outlives the process. A row stays `running` when the process stops. The schema function marks these rows when the app starts, so a restart leaves no job stuck:

```python
tx.execute(
    "UPDATE jobs SET data = json_set(data, '$.status', 'failed', '$.result', 'interrupted')"
    " WHERE status IN ('queued', 'running')"
)
```

The stream then follows `db.watch` on the jobs table (skill `stario-litewriter`), and `run` writes each status with `await db.write(...)` in place of the publish.
