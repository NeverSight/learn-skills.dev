---
name: events-bus
description: Provide a reusable event protocol and bus integration for orchestrators, sub-agents, and background jobs so users can see live progress instead of waiting on a black box. Strongly recommended as a bootstrap skill for any agent system that delegates work. When installing it, strongly prefer adding a mandatory rule to the global AGENTS.md (or the platform-equivalent global system/custom instructions) that points to this skill's references/protocol.md; if no global instruction file exists, add the rule to the project AGENTS.md or equivalent bootstrap instructions.
---

# events-bus

## What this skill enables

Use one correlated event stream for a whole orchestrated job so sub-agents can report status and the owning orchestrator can proactively show meaningful progress to the user.

Real goal: **eliminate black-box waiting during delegated work.**

Capability tree:

1. create and propagate one `job_id` across the orchestration tree;
2. publish truthful lifecycle/progress events from every sub-agent;
3. establish a non-blocking job watch before delegation starts;
4. convert user-visible events into concise live status updates;
5. preserve nested task correlation and terminal outcomes;
6. fall back safely when the event transport is unavailable.

The canonical protocol is `references/protocol.md` inside this skill. Read it before implementing or changing event behavior.

## Event ownership guideline

`events-bus` provides transport and the current Neo compatibility envelope. Producer and Consumer own source-identity encoding and payload semantics; the bus does not interpret Job/Task/Execution identities, worker kinds, or domain lifecycle meaning. The current object-shaped envelope carries the opaque producer identity as `source.id`. It does **not** centrally enumerate every domain-specific event type. The skill or component that owns a semantic action owns the event names and payloads for that action, and SHOULD document its supported events in an `Events` section in its own `SKILL.md` or a referenced event contract. Those events MUST still conform to the events-bus envelope and protocol.

As a general transparency rule, whenever an agent/worker is selected or started, the component that owns that selection or launch MUST publish a user-visible event identifying the model and reasoning/thinking level when those values are known. The exact semantic event name and `data` shape belong to that component/skill, not to events-bus. Never invent a model or thinking level that was not actually selected.


## Runtime architecture and ownership

`events-bus` is the single owner of the event capability layer: transport setup, runtime connection discovery, persistence/replay, cursor semantics, and the reusable operations behind every adapter.

```text
                    events-bus core
                 /        |        \
              CLI        MCP       HTTP API
               |          |           |
               +----------+-----------+
                          |
                 NATS + history store
```

The adapters MUST remain thin. CLI, MCP, and HTTP call the same core methods for `publish`, `watch`, `wait`, `history`, `status`, and `health`; they must not implement separate event stores or cursor behavior. A standalone `api/server.mjs` process owns the continuous `neo.events.job.>` subscription and persists history even when no MCP client is connected.

Runtime connection discovery is also owned here. `core/config.mjs` resolves and persists one machine-readable runtime configuration containing `natsUrl`, `apiUrl`, `dataDir`, and `subjectPrefix`. Consumers such as Agents Relay use that contract for both native realtime NATS and the history API rather than defining independent endpoints. `node cli/events-bus.mjs config` prints the resolved configuration; `node cli/events-bus.mjs setup` installs/supervises the NATS and history/API processes through PM2.

Agents Relay uses native NATS publish/subscribe for lifecycle-critical realtime events and reads replay/history through the events-bus HTTP API. Hosted ChatGPT and sandboxed workers use the MCP adapter. Direct local workers may use the CLI or `NEO_EVENTS_EMIT`. The JSONL history file is an events-bus implementation detail and must not be read directly by Relay or dashboards.

## Orchestrator workflow

1. Generate one unique `job_id` before starting any child work.
2. For request/response MCP hosts, establish a pre-launch watch capability **before** publishing `job.started` or launching the child. Prefer `events__watch(job_id)` and remember its `after_cursor`. If that tool name is unavailable, only for a newly-created unique job with no prior events, use `events__history(job_id, after_cursor=0, limit=1)`; an empty result establishes cursor `0`. Never use that fallback for an existing/resumed job with an unknown cursor. Native subscribers may establish the equivalent non-blocking cursor directly.
3. Emit `job.started` for the orchestration itself.
4. Pass the Producer/Consumer-defined source identity as `NEO_EVENT_SOURCE`, plus the current Neo compatibility fields `NEO_JOB_ID`, `NEO_ORCHESTRATOR_ID`, and task-specific `NEO_TASK_ID`, to the child. For nested work also pass `NEO_PARENT_TASK_ID`. Put the exact literal `job_id` and `task_id` values in the delegation prompt as well as the environment; never say only `inherited` or use a placeholder. For direct local workers that can reach NATS, also pass `NEO_EVENTS_BUS_DIR` and `NEO_EVENTS_EMIT=<absolute-skill-dir>/scripts/emit.mjs`.
5. Keep consuming events while the job runs.
6. Proactively surface `visibility=user` events in the current user experience. Do not wait for the user to ask "what is the status?".
7. Emit exactly one terminal `job.completed|failed|blocked|cancelled` event and stop only after it has been reconciled with the actual work result.

For noisy numeric progress, coalesce updates; never suppress milestones, warnings, `phone.released`, blocked/failed states, or completion.

## Sub-agent workflow

A sub-agent uses the caller-provided source identity and compatibility correlation; it does not mint or reinterpret its own identity. A Codex worker running in the normal sandbox MUST use MCP `events__publish`, because the sandbox can deny direct TCP access to the local NATS port. The orchestrator must include the exact literal `job_id` and `task_id` in the worker prompt, and the worker must copy those exact values into every publish call. Do not pass strings such as `inherited`, `current`, or `<job-id>` as event IDs. Direct non-sandbox local workers may use `NEO_EVENTS_EMIT`.

At minimum emit:

- `task.started`
- meaningful milestones/progress
- one of `task.completed`, `task.failed`, `task.blocked`, `task.cancelled`

Carrier/process lifecycle is distinct from task lifecycle. The component that
owns the carrier MAY emit `task.process.launched` after a process/thread/browser
submission has actually launched, `task.process.exited` when a synchronous
carrier exits, or `task.process.async_exited` when an asynchronous submit
runtime exits while the remote task may still be running. These process events
are never substitutes for worker-owned `task.started` or a terminal task event.

### Task visibility policy

- `task.started` and meaningful milestones MAY be `visibility: user` when useful.
- `task.process.launched`, `task.process.exited`, and
  `task.process.async_exited` are lifecycle diagnostics and are non-terminal;
  show them only when they are useful to the user or to active debugging.
- `task.failed`, `task.blocked`, and `task.cancelled` MUST be `visibility: user` and surfaced immediately.
- Routine successful child `task.completed` SHOULD use `visibility: orchestrator` while the parent still reconciles or consumes results and will shortly emit a user-visible top-level `job.completed`.
- Child `task.completed` MAY be `visibility: user` only when its completion is a meaningful standalone user milestone; the render-before-next-tool-call barrier still applies.
- Top-level `job.completed`, `job.failed`, `job.blocked`, and `job.cancelled` remain user-visible terminal results.

If the task temporarily monopolizes NeoX, emit `phone.transaction.started` when phone-dependent work begins and `phone.released` immediately after the last phone-dependent operation completes. Work after `phone.released` must not require NeoX to remain foreground unless a new transaction begins.

Messages should be short and user-comprehensible, for example:

```text
正在从 NeoX 拉取 3 个素材
手机端素材传输完成，可以正常使用手机了
小红书视频上传中 66%
视频已提交，正在审核
```

Never include secrets or raw cookies/tokens in events.

### Direct local emit helper

For non-sandbox local workers that can reach NATS directly, the skill ships `scripts/emit.mjs` so sub-agents do not have to hand-build envelopes. The owning orchestrator should pass its absolute path as `NEO_EVENTS_EMIT`. Set correlation variables once, then emit milestones:

```bash
export NEO_JOB_ID='<job-id>'
export NEO_TASK_ID='publish-xhs'
export NEO_ORCHESTRATOR_ID='chatgpt:<session-or-run-id>'
export NEO_EVENT_SOURCE='job/<job-id>/task/publish-xhs/execution/<execution-id>'
export NEO_AGENT='codex' # optional diagnostic metadata
export NEO_EVENTS_BUS_DIR='<absolute-path-to-events-bus-skill>'
export NEO_EVENTS_EMIT="$NEO_EVENTS_BUS_DIR/scripts/emit.mjs"

node "$NEO_EVENTS_EMIT" task.started running user '开始发布到小红书'
node "$NEO_EVENTS_EMIT" publish.upload.progress running user '小红书视频上传中 66%' '{"current":66,"total":100,"unit":"percent"}'
node "$NEO_EVENTS_EMIT" task.completed succeeded user '小红书发布完成'
```

The helper publishes through the bundled NATS transport implementation; if transport delivery fails it writes the same structured event to stderr as the protocol fallback.

## Orchestrator event loop — mandatory

The owning orchestrator must treat event consumption as a loop, not as a one-shot status check. The required control flow is:

1. establish event consumption before child work starts;
2. establish the pre-launch watch capability before `job.started`: prefer `events__watch(job_id)`, or use the fresh-job-only `events__history(job_id, after_cursor=0, limit=1)` fallback when the preferred tool is unavailable; retain the resulting cursor;
3. launch the child only after the watch and any required pre-launch routing event/render are complete; request routine successful child completion as `visibility: orchestrator` unless it is a meaningful standalone user milestone;
4. call `wait(job_id, after_cursor, timeout_ms)` (or the transport-equivalent);
5. for each returned event, advance the cursor and immediately render any `visibility=user` event as a normal assistant-visible progress message;
6. **render barrier:** after `wait` returns one or more `visibility=user` events, emit the corresponding assistant progress message **before making any subsequent tool call**, including the next `events__wait`; tool traces such as “Called `events__wait`” never satisfy this barrier;
7. do not expose raw event JSON unless the user explicitly asks for diagnostics;
8. continue waiting after non-terminal task events and after wait timeouts;
9. stop when either a top-level terminal job event is observed, or the registered worker process is no longer alive. If the process ended without a terminal event, treat the outcome as abnormal/uncertain rather than continuing to wait.

A single `wait` timeout is **not** job completion. It only means no matching event arrived during that long-poll window. Continue the loop while the job is still active.

Each MCP `wait` call also checks the registered local worker process while it is waiting. A job should publish `data.worker = { kind: "process", pid, host }` (the bundled emit helper does this when `NEO_WORKER_PID` is set). If the process disappears, `wait` returns immediately and the orchestrator MUST stop the wait loop. If a top-level terminal job event was already observed, finish normally; otherwise report an abnormal/uncertain termination (`process_exited_without_terminal: true`) instead of continuing blind long-polls.

Top-level terminal job events are:

- `job.completed`
- `job.failed`
- `job.blocked`
- `job.cancelled`

`task.completed` is not sufficient to stop the orchestrator when the job may contain additional sibling or nested tasks.

If the worker exits or becomes unreachable without a terminal job event, reconcile that mismatch explicitly, surface it to the user, and terminate the job as failed/blocked rather than silently ending the wait loop.

For MCP clients such as web ChatGPT, Grok, or Claude, the intended pattern is:

```text
watch = events__watch(job_id)  # preferred; otherwise fresh unique job: history(job_id, 0, 1)
cursor = watch.after_cursor
publish/render required pre-launch model.selected
launch worker
while job not terminal:
    result = events__wait(job_id, cursor, 25000)
    if result.timed_out:
        continue
    for row in result.events:
        cursor = row.cursor
        if row.event.visibility == "user":
            render row.event.message as an assistant-visible progress update
        if row.event.type is a top-level terminal job event:
            reconcile and stop
```

The visible assistant message is part of the contract. A tool trace such as “Called `events__wait`” is implementation detail and does **not** count as showing the event to the user.

## Display contract — mandatory

When acting as the owning orchestrator, **important user-visible events MUST be actively shown to the user as they arrive**. Logging an event without surfacing it does not satisfy this skill.

If the current orchestrator itself publishes an event with `visibility=user`, it MUST immediately render that event's human-readable `message` in the conversation before making any subsequent tool call. Do not wait for the same event to come back through `events__wait` or another subscriber before showing it. This self-publish rule applies equally to events defined by any skill.

The orchestrator should render a human sentence, not raw event JSON. A good default is one short line per milestone. If many numeric updates arrive, show the first, meaningful deltas, and completion.

If the current harness cannot push messages after a turn has ended, keep the orchestration turn/session open while work is active when possible, or use the harness's supported notification mechanism. Do not pretend asynchronous chat delivery exists when it does not.

## MCP federation

`mcp/server.mjs` exposes the event bus through a platform-neutral MCP interface. The intended federated tool surface is:

- `events__health` — relay/broker health
- `events__watch` — non-blocking cursor establishment before delegation
- `events__wait` — cursor-based long-poll for one job
- `events__history` — replay stored events for one job
- `events__status` — latest/terminal job state
- `events__publish` — publish an event when the caller has MCP but no native event-bus client
- `events__progress` — return a compact structured job snapshot and, on MCP Apps-capable hosts, render the bundled Job Progress Card

For hosted ChatGPT, sandboxed Codex workers, and other MCP clients, use these MCP tools rather than requiring the client to connect to NATS directly. Establish the pre-launch watch capability before `job.started` or delegation: prefer non-blocking `events__watch(job_id)`; if unavailable, only for a newly-created unique job with no prior events, use `events__history(job_id, after_cursor=0, limit=1)` and start at cursor `0` when empty. Do not use that fallback for an existing/resumed job with an unknown cursor. Then route/render, launch, and use `events__wait(job_id, after_cursor, timeout_ms)`. A blocking wait before launch is invalid. `events__publish` requires the semantic fields `job_id`, `task_id`, `type`, `status`, `visibility`, and `message`; the relay validates their enums/shape and fills `version`, `event_id`, `timestamp`, `level`, `source`, and `data` when omitted.

### Rich progress card

The MCP server also exposes `events__progress(job_id)` with a bundled `text/html;profile=mcp-app` UI resource. Use it when a compact visual snapshot materially helps the user understand a longer job. It is supplemental presentation only: the owning orchestrator MUST still satisfy the render barrier and emit normal assistant-visible messages for `visibility=user` events. A card, tool invocation label, or hidden structured result never replaces those messages.

When `events-bus` is federated through MacDevBridge, the bridge must proxy `resources/list`, `resources/read`, and UI resource URIs together with the tool metadata.

## Transport

NATS is an internal transport implementation of `events-bus`, not a separate agent skill. Agents should reason in terms of Neo events and the MCP/event tools, not NATS mechanics.

The bundled transport helper is `transport/nats.mjs` and uses `NEO_NATS_URL` (default `nats://127.0.0.1:4222`). It supports `ping`, `pub`, and `sub` for implementation/testing. The local broker is supervised as the `events-bus` PM2 service in the `neo` namespace.

Common subjects:

```text
neo.events.job.<job_id>.task.started
neo.events.job.<job_id>.progress
neo.events.job.<job_id>.phone.released
neo.events.job.<job_id>.task.completed
```

See `references/examples.md` for event examples.

## Installation contract — strongly recommended

Do not rely on skill discovery alone. A system that adopts `events-bus` should make the protocol part of its always-on agent instructions so an orchestrator cannot delegate work without knowing the reporting contract.

**Strongly prefer the global instruction layer.** Add a mandatory rule to the user's/global `AGENTS.md` (or the platform-equivalent global system prompt, custom instructions, bootstrap policy, etc.) that points directly to this skill and `references/protocol.md`. This is preferred because it applies across repositories and prevents the event contract from disappearing when an agent starts work outside a particular project.

If there is no global instruction mechanism, add the same rule to the project's `AGENTS.md` or equivalent bootstrap instructions.

Recommended wording:

```text
For delegated or background work, follow the events-bus skill and its
references/protocol.md contract. The owning orchestrator must create and
propagate one job_id, establish event consumption before starting sub-agents,
and proactively surface user-visible milestones, blocked/failure states,
resource-release events, and completion. Progress that exists only in a child
process log is not sufficient.
```

For Web/hosted agent platforms that do not read `AGENTS.md`, put the equivalent requirement in their global custom instructions/bootstrap configuration and load `events-bus` as a bootstrap skill.
