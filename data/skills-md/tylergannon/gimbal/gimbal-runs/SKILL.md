---
name: gimbal-runs
description: >
  Use existing Gimbal workflows in a project: choose and invoke a command,
  understand goals and proof, observe runs, steer sessions or loop planners,
  and assess results. Includes promise, chapter, and sprint terminology.
---

# Use Gimbal

Use the installed command to run a workflow against a project. You do not need
to write Go or build Svelte to call an installed workflow. For a new workflow
use [Author workflows](../gimbal-workflows/SKILL.md); for building the application
use [Build and release](../gimbal-release/SKILL.md).

## Choose a workflow and understand its contract

```sh
gimbal --help
gimbal run --help
gimbal run review --help
```

Workflow help comes from the selected running central catalog. Use
`--instance-dir /abs/instance` when it is outside the current directory.
It tells you which registered workflows, inputs and model defaults are available. The presence of a `df-*` skill does not make it a Gimbal command.

By default, the macOS app starts its bundled central with
`~/.gimbal/desktop` as its instance directory. To submit CLI runs to that
catalog, pass `--instance-dir ~/.gimbal/desktop` or set `GIMBAL_INSTANCE_DIR`
for the CLI.
The app uses `GIMBAL_SERVER_URL` only when explicitly configured to proxy an
external server.

Establish the goal, target project, permitted changes, and what would
demonstrate a useful result. A supplied chapter or sprint can provide context;
use it when relevant rather than manufacturing planning artifacts for every
invocation. See the [glossary and proof guidance](references/glossary-and-proof.md)
for the distinctions among promises, chapters, sprints, tasks, and runs.

Workflow help should explain purpose, inputs, outputs or changes, completion
expectations, and limits. If a material part is missing, resolve it from the
workflow's source or the user rather than guessing at its authority.

For a research document, inspect `gimbal run research-document --help`. Supply
the goal, a local research directory, an output path, and a document token
budget. `--source-dir` uses fixed local originals; omit it for web collection.
The workflow writes a semantic `INDEX.md`, records every extracted claim and
Jev source/pair finding under `<research-dir>/.semantic-index/`, and repairs or
qualifies findings before document acceptance. The separate
`gimbal run research-eval --help` command compares researcher and index-curator
model assignments on fixed sources. Its winner is provisional for that suite;
the report distinguishes factual correctness, retrieval, repair, and cost.

For sprint planning, inspect `gimbal run sprint-plan --help`. Supply a local
intent file and a new sprint directory under `ephemeral/sprints/`. The intent
names the stakeholder outcome, boundaries, acceptance evidence, and useful
reference paths. The workflow gathers project information and prior art into
an indexed working set, then produces three drafts, cross-critiques, and a
proposed `plan.md` with references for implementation. Review unresolved
stakeholder decisions before execution; planning completion does not establish
that the outcome has been delivered.

## Start a run

Gimbal requires `TYPESAFE_API_KEY` only when a workflow uses
`WithSupervisor` for Jev supervision. `run-prompt`, workflows without Jev, and
instance startup work without that key. A supervised workflow reports a clear
error when it reaches Jev supervision without the key. Help and commands that
only contact an already running instance do not need a local TypeSafe key.

```sh
gimbal --instance-dir /abs/instance --port 8080
# In another shell:
gimbal run review --instance-dir /abs/instance --project /abs/project --input '{"goal":"Review the parser changes for correctness; report concrete findings with evidence."}'
```

Central and workflow daemons discover native plugins at startup through repeated
`--plugin-dir DIR`. Deploy matching plugin builds to each environment and restart
after rebuilding the project plugin. The CLI and frontend need no rebuild to
accept its changed input contract. Control commands and generation do not load
local plugin files.

Supply `--input` as a JSON object or `@/abs/input.json`, or use the catalog's
parameter flags. The shared browser Run form presents those same fields; check
Include to submit an optional empty, zero or false value. Input errors name the
visible field before a run is admitted.

By default central launches a local independent runner. For remote placement,
select `--workflow-endpoint URL --workflow-project /abs/project-at-A` and
`--work-dir /abs/workdir-at-A`, independently of central's `--project` directory.
Select `--task-endpoint URL` for tasks at B. `--workflow-route` and `--task-route`
accept JSON or `@file` with backend `name`, `configuration` and `environment`
for registered backend implementations. Provision the repository and workspace
at each environment; plugin paths are configured locally at each daemon.
Central retains run routes so restarting central can reopen active runs without
resubmitting them. A disconnected observation channel is a gap, not proof that
the work stopped or failed.

Use an absolute project path. Do not pass role-model flags by default: the
workflow's displayed defaults are its intended role configuration, and a
supplied flag replaces one. Override a role when the user requests a particular
model or effort, when its default cannot run and the user approves the
replacement, or when the workflow's own help identifies the present work as a
clearly bounded case for a cheaper model. In that last case, prefer the
documented Sol or Opus selection for routine work, but retain the configured
frontier default when the help's ambiguity, risk, or difficulty criteria apply.
Do not turn general cost pressure into blanket overrides across unrelated
roles. Before an override, read every role line in `--help` and state the
resulting mapping. Record the models actually used in the result report.

OpenCode models are explicit: `opencode/<model-id>` selects OpenCode's
`opencode` provider, while `opencode/<provider>/<model-id>` selects another
provider configured in OpenCode. Both forms work on workflow role flags and on
`gimbal run-prompt --model`. The shared server starts on first use and survives
session close. Its state defaults to `~/.gimbal/opencode`, or
`GIMBAL_OPENCODE_DIR`; `gimbal opencode start|stop [--state-dir DIR]` manages
it directly, and stop interrupts active work. Raw request/result/SSE captures
are written to `<state-dir>/captures/`.

For Pi with Diffusion Router, discover the model IDs available to the current
key that support chat and tools:

```sh
curl -fsS https://router.diffusion.io/v1/models \
  -H "Authorization: Bearer ${DIFFUSION_API_KEY}" |
  jq -r '.data[] | select(.capabilities.openai_chat == true and .capabilities.tools == true) | .id'
```

Prefix a chosen open-weight ID with `pi/diffusion/` on a workflow role flag or
`gimbal run-prompt --model`, for example `pi/diffusion/deepseek-4.1-flash-background`.
Gimbal does not require models.dev to route these models. Set
`DIFFUSION_API_KEY` in the server environment. The Pi harness runs natively
in the Gimbal process; it does not require a separate Pi, Bun, or Node
installation. Shell tools still launch child commands.

Another useful profile spends frontier capability on planning, then assigns
low-risk, reversible, independently checkable background work to Terra or
Sonnet. Prefer it when wall-clock time is cheap and the workflow has bounded
validation feedback that can reject a weak completed attempt and try a better
assignment. The plan is not proof, so keep independent validation appropriate
to the risk. Do not assume the workflow retries provider, harness, or execution
errors; only an explicit retry path does that.

The command returns the run ID after the independent run process starts. Use
`--follow` to wait for its outcome. If central disconnects, follow rediscovers
the selected instance for up to 30 seconds and resumes the same run without
resubmitting it; an unrecovered disconnect returns an explicit error. The run continues when the command exits or
the daemon stops. Restart the daemon with the same instance directory to resume
observation and control of its admitted projects. The daemon's `--port 0`
selects an available browser port; `--uds` serves through a Unix socket.

Use `--task-endpoint` to execute agents, commands, and scope-owned services in a
selected standalone daemon. See [task daemons](references/task-environments.md)
for workspace configuration, transferred artifacts, and scoped secrets.

### Messaging task routes

The `filesystem`, `river`, and `http-sse` native plugins carry requests and retained
events while the workflow remains ordinary Go. Build the CLI and each plugin
from the same checkout and Go toolchain; `go build -buildmode=plugin -o /abs/plugins/filesystem.so ./plugins/messaging-filesystem` builds the filesystem
plugin. The River and HTTP packages are `./plugins/messaging-river` and
`./plugins/messaging-http`. Start central with `--plugin-dir /abs/plugins`.
For a published CLI, add `-trimpath` and follow the exact source/toolchain and
workspace requirements in [distribution](../gimbal-release/references/distribution.md#plugin-builds).

A route file contains `Name` and `Configuration`. Choose one configuration:

| Name | Configuration |
| --- | --- |
| `filesystem` | `{"Directory":"/abs/private-messages"}` |
| `river` | `{"DSNFile":"/abs/private-postgres-dsn","Queue":"gimbal"}` |
| `http-sse` | `{"URL":"http://127.0.0.1:18091"}` |

For filesystem or River, start one worker with the same route as the caller:

```sh
gimbal message-worker --plugin-dir /abs/plugins --task-route @/abs/route.json
gimbal run service-check --instance-dir /abs/instance --project /abs/project --work-dir /abs/project/work --task-route @/abs/route.json --task 'Write the required file.' --follow
gimbal message-watch --plugin-dir /abs/plugins --task-route @/abs/route.json --run RUN_ID
```

Workers without configured backend dependencies keep scoped secrets in private
process memory. Named environments use the shared secrets directory supplied by
orchestration.

Run those commands in separate shells. River requires reachable PostgreSQL and
a private file containing its connection string; the worker initializes its
schema. Its action queue defaults to `gimbal`, its separate control queue to
`gimbal_control`, and action workers to four. Use distinct queues to isolate
independent deployments.

HTTP uses one URL per environment. The worker route additionally specifies
`Listen` (`127.0.0.1:18091`) and an absolute `EventsDir`. Agent sessions,
commands, and services use the daemon selected by orchestration.

For automatic named-environment startup, the caller route adds `Environment`
and `Backends`. For example, with the filesystem plugin:

```json
{
  "Name": "filesystem",
  "Configuration": {"Directory": "/abs/control"},
  "Environment": "development",
  "Backends": {
    "Orchestrator": {
      "Name": "local",
      "Configuration": {
        "Directory": "/abs/private-backends",
        "Environments": {
          "development": {
            "Command": ["/abs/gimbal", "message-worker", "--plugin-dir", "/abs/plugins", "--task-route", "@/abs/worker.json"],
            "Route": {"Name": "filesystem", "Configuration": {"Directory": "/abs/development-messages"}}
          }
        }
      }
    },
    "Secrets": {"Name": "file", "Configuration": {"Directory": "/abs/private-backends/secrets"}}
  }
}
```

`worker.json` contains the same Name and Configuration as that environment's
Route. Orchestration supplies worker readiness and passes the selected secrets
configuration through private standard input. Named orchestrator and secrets
registrations are independent of the messaging plugin. The local subprocess
orchestrator requires shared secrets; the `file` backend shares its private
directory across callers and workers. The `memory` backend is for callers and
workers in the same process and is rejected for local subprocess orchestration. It
starts the daemon before dispatch, preserves unrelated scoped use, and stops
it after its last native scope is cleaned up. Do not start this worker manually.
Named environments require messaging; direct task endpoints cannot bypass placement.

The `service-check` workflow needs Docker, psql, Python 3, and an agent harness
in the daemon environment. It owns Postgres and a web service, publishes scoped
connection values, queries the database through parallel consumers, and has an
agent fetch the web response using a Gimbal secrets callback. Use a fresh work
directory and an explicit inexpensive model such as `gpt-5.6-luna`.

Workers and callers share local paths in this implementation. Restarting a
worker does not restore native actions or sessions. Steering and fork remain
unsupported on messaging routes. Delivery uncertainty never establishes native
failure or cessation. `message-watch` reads retained history independently;
stopping it never cancels work. Its JSONL can contain private agent content.
Event files or PostgreSQL rows remain until explicitly removed.

## Find the run and observe its work

```sh
gimbal runs --work-dir /abs/project
gimbal watch RUN_ID --work-dir /abs/project
```

Use the same project directory. `runs` returns JSON with active runs from
responding local runtimes. `watch` emits an initial snapshot followed by
newline-delimited JSON changes. Read run status, scopes, sessions, and turns
to understand what is happening.

A turn without an end time identifies an active session. Copy that session's
exact ID. Role names, session IDs, turn IDs, and loop scope IDs identify
different things. An empty discovery result may mean the runtime is absent
or unreachable; it says nothing conclusive about saved history.

## Steer a session or the next planning decision

```sh
gimbal steer RUN_ID --work-dir /abs/project --session SESSION_ID "Investigate the failing parser test before expanding the review."
gimbal steer RUN_ID --work-dir /abs/project --loop LOOP_SCOPE_ID "Prioritize the CLI work in the next assignment."
```

Choose exactly one target. A session steer goes to that session's active turn;
`landed: false` means it was dropped, not saved for a later turn. Loop steering
queues a message for the next planning decision of that dispatching loop.

Give an actionable correction and relevant evidence, then observe what the
agent does. `landed: true` establishes delivery; `queued: true` establishes
queueing. Neither establishes that the instruction was followed.

## Assess the result and its proof

Inspect the work or behavior relevant to the goal. A review finding should
point to a concrete defect; an implementation claim needs observation of the
changed behavior. Tests and command results are evidence for what they
actually exercise. Recorded failure cannot be overruled by prose saying it
passed.

A run can finish, and a planner can stop dispatching, while the requested
outcome remains unmet. For a promise, identify the claim, scope, evidence,
verifier, and inspected state. Use independent validation when the workflow
or acceptance contract calls for it; the validator inspects the result rather
than accepting the worker's account as proof.

Saved records remain in `/abs/project/.gimbal/runs/RUN_ID/`. To inspect history
in the browser, run `gimbal --port 0` from the project directory. Live `watch`
needs a running owner; viewing saved history does not revive its sessions.
Codex actively reconciles a lost connection with up to three attempts within
one minute. A surviving native turn is reattached; a completed result is read
from history. If the daemon remains unavailable or safe continuation is unclear,
the same call, run and task stay paused while the owning instance is alive.
The transcript's connection notice explains the cause. After inspecting existing
work and confirming that prior operations have ceased, request another bounded
reconciliation batch with:

```sh
gimbal steer RUN_ID --work-dir /abs/project --session SESSION_ID resume
```

This is an adapter recovery control when that Codex session is paused; it does
not establish native delivery or task completion. The adapter checks history
again before reattaching or starting a same-thread continuation. It never replays
accepted outcomes. Cancel instead with `gimbal cancel RUN_ID --work-dir /abs/project`.
That command also retries pending remote cleanup of a terminal run. Failed cleanup
retains stop control in the owning instance; it does not prove the worker stopped.
An instance restart reconnects controls to surviving independent workflow
processes. It cannot restore a workflow process that died. For `--task-endpoint`
runs, central uses the retained owner route to clean up that process's remote
scope; failed cleanup remains retryable.

Gimbal has no generic resume command. Repository promise helpers may define
their own resumable state, schedules, and badges; those are separate
capabilities.

For direct inspection, start with stored run and turn results, then the
relevant session transcript or recorded command output. Follow the consumer
project's policy for retaining or sharing evidence.

## Run practical user testing

`gimbal run validate-product --suite-file /abs/suite.yaml --instance-dir /abs/instance --project /abs/project --follow`
runs one to three caller-assigned workloads with Opus 5.5, reviews their
screenshots with Gemini Flash, and synthesizes findings. The suite requires
`issue_repo` for the tested product. The final agent checks for duplicates,
uploads supporting screenshots
with `gimbal upload-artifact`, and publishes supported findings there. After each
workload, the same tester session
answers one follow-up: its three favorite and three least favorite aspects of UX
and UI separately, with concrete examples. The debrief is appended to the task
report; elapsed workload time excludes it. Supply the product, local assignment
files, isolated workspaces, startup/readiness commands or existing URLs, and an
output directory. Start the selected instance; the workflow command admits
`/abs/project` on its first start when it was not admitted at startup.
`--follow` waits for triage and issue publication. The command's help describes the
JSON/YAML input and model overrides. Publishing requires authenticated `gh`
and a configured public artifact destination.

Assign useful tasks rather than exhaustive feature checklists. Testers must never
inspect the tested product's source. They capture captioned screenshots and report
task success separately from usability; video is for optional human review.
Install FFmpeg with libx264 before running it. `reports.json` points to each
2.5× H.264 `video.mp4`, capped at 1280×720 and ready for `gimbal upload-artifact`;
the raw `video.webm` remains beside it.
When testing Gimbal by having it build another project, use the delegated run's
own web listener for live UI/API monitoring. A standalone history viewer can
retain stale snapshots of runs owned by another process.

## Work from a conversation

Run `gimbal --port 0` from a Git checkout and open **Conversations**. Choose
Codex, Claude, or agy/Gemini when creating a conversation; Gimbal creates its
worktree and branch. Ask the agent to start a review or implementation, then
open the linked run to monitor it in the same server. Implementation needs a
local definition-of-done file in the conversation's worktree. Keep the server
running while a conversation turn is active. Launched workflows run independently. After a restart, saved Codex
conversations resume their native thread on the next message. Saved Claude and
agy/Gemini conversations remain readable history and cannot continue yet.

## Report what happened

Give the workflow, project, model, run ID, useful result, and observed evidence.
When steering, include the target, delivery result, and subsequent behavior.
State failed or unproved requirements separately from completed work. Keep
the report proportionate to the task.
