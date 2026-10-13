---
name: gimbal-workflows
description: >
  Design and author Gimbal workflows as ordinary Go. Covers workflow
  structure, agent roles, context and handoffs, adaptive planning, supervision,
  independent validation, completion, and CLI documentation. Use Godoc for API details.
---

# Author Gimbal workflows

Write a program whose purpose, decisions, and evidence are visible in its
source. Aim for the clarity of a page of pseudocode. Research, bake-offs,
critique, retries, worktrees, and delivery are tactics written inline with
ordinary Go and Gimbal's primitives.

Adapters own transport maintenance and native-state reconciliation, with
bounded, observable, responsible best-effort completion of each requested turn.
Do not add workflow retries around connection loss: a lost reply does not prove
an operation never happened. Workflows own task policy and independent validation;
adapter recovery must retain session identity, avoid duplicate work, preserve
cancellation, and keep unverified remote cleanup retryable.

Use Godoc for the current API. For an existing command, use
[Use Gimbal](../gimbal-runs/SKILL.md); for building and installing the application,
use [Build and release](../gimbal-release/SKILL.md).

## Define the outcome and its proof

Review built-in workflow source with the human at `/workflows/<name>` in the
Gimbal application. In a checkout, `just dev` starts the live application:
workflow edits refresh its diagram, prompt and nested context inspection, guide
and parameter descriptions. The human can share a URL with selected and expanded
objects while the agent edits their Go source. Invalid edits retain the last
successful view; changed or removed identifiers reset without guessing.
The installed application shows its shipped snapshot. Reading a page does not
run it; invoke the workflow with `gimbal run <name>`.

Use an immediately preceding doc comment to give an operation, scope or
condition a human-readable title on its first line and a description on later
lines. `When true: Command provided` labels the positive condition edge;
case comments label switch edges. Preserve static source truth: do not invent
runtime values or interpret unlabeled operations as agent intentions.

State what the workflow should accomplish, its scope, and what someone must
observe to know it worked. Give agents outcomes and useful verified facts;
leave their approach open unless a particular method is a requirement. A plan
can change as facts emerge. The original goal remains authoritative.

Separate three things in the design:

- **Program:** roles, branches, concurrency, feedback, and stopping decisions.
- **Inputs:** the goal, project, issue, plan, or candidates for this invocation.
- **Knowledge:** material agents can retrieve while working.

The program should remain understandable as its inputs and knowledge change.
Put task data in parameters, scoped context, and local files rather than
encoding each new assignment into the orchestration.

## Choose the smallest useful shape

Use a single agent or a sequence when that is enough. Add a role or stage for
useful context, independent judgment, or a handoff the work actually needs.

| Need | Shape |
| --- | --- |
| One well-scoped task | One agent turn. |
| Dependent stages | A sequence with explicit results passed onward. |
| Independent investigations or candidates | Concurrent branches followed by a join. |
| Several agents need the same initial research | Research once, then fork conversations. |
| Competing implementations | Separate worktrees, followed by a judge inspecting actual candidates. |
| Criticism and revision | Explicit critique/revise rounds with a stopping condition. |
| A known finite collection | Iterate over the supplied items. |
| The next useful assignment depends on new evidence | A planner-driven loop with worker and validation feedback. |

Keep each tactic visible in the workflow. A helper that hides the orchestration
can make a shorter file harder to understand. In the Gimbal repository, new
exported API names require Tyler's explicit request.

Read [workflow patterns](references/patterns.md) when choosing how research,
parallel attempts, critique, or adaptive implementation should fit together.

## Give roles clear responsibilities

Use the established role constants in `roles.go`. Branch names identify
participants; roles identify reusable kinds of work; run bindings choose models.
Do not add workflow- or provider-specific roles to `internal/builtin/defaults.json`
to obtain another model assignment. Catalog changes require an explicit product
decision so model assignments remain reusable across workflows.

A researcher establishes facts and useful source locations. A planner chooses
the next assignment. A worker performs it. A validator inspects the result and
whether the evidence establishes acceptance. A supervisor coaches an active
agent. Use the roles the task warrants; naming every possible role does not
make a better workflow.

Preserve independence where it matters. Shared research can save repeated
reading, but a judge must inspect original evidence and actual candidates.
The implementer's summary can orient validation; it cannot establish that the
implementation works. Forking a worker's conversation into a judge carries
its assumptions along with the useful context.

## Make ownership and handoffs visible

Place sessions according to the lifetime of their work. A planner may need
continuity across assignments; a task worker may need isolation from previous
attempts. Reusing a session also reuses its conversation history. Ending a
scope does not erase what that agent already saw.

Every concurrent branch needs an owner and a join before its enclosing work
ends. Cancellation and cleanup are separate concerns. Give parallel editing
agents separate worktrees when they could interfere, and verify where they
actually wrote their changes.

Land crucial information locally before dispatch. Prompts name absolute paths
to the issue, plan, source, or research needed. For a large corpus, retrieve
through a compact index and pass selected evidence or its location. Keep
context relevant rather than copying the whole corpus into each turn.

A handoff gives the next role the exact assignment, relevant files, observed
results, unresolved findings, and decisions. Make feedback explicit; do not
rely on a child scope or provider conversation to become shared project state.
Use local artifacts for knowledge another role must inspect independently.

## Write prompts that leave room for judgment

Use plain English: what to read, what outcome to produce, meaningful
constraints, and the expected answer. Keep prompts inspectable in the source;
task-specific data belongs in context. Read the rendered prompt when diagnosing
bad behavior, since harness instructions and prior conversation also matter.

Use structured answers when the workflow needs to make decisions from fields.
Those field descriptions are instructions to the agent. Otherwise, prose or a
local artifact may be sufficient. Avoid elaborate output contracts that merely
restate what the model already understands.

## Adapt plans without moving the goal

An adaptive loop should choose work from the goal, current backlog, and
observed results. Assign a coherent outcome with a definition of done. An
investigation is valid work when uncertainty blocks a sound implementation.

Feed actual worker results and validation back to planning. Retain unresolved
findings and explain deferred work so replanning does not silently lose it.
A review finding is a claim to investigate against the goal, not an automatic
addition to the goal.

Keep retries, limits, and escalation visible and proportionate to the task.
A supplied plan can seed the backlog without dictating every later assignment.
Ending dispatch and fulfilling the goal are separate decisions.

Spend capability where uncertainty lives. A frontier planner can be worth one
expensive turn when it leaves a strong, bounded plan whose assignments are
reversible and independently checkable. Low-risk background work can then use
cheaper Terra or Sonnet workers when elapsed time matters less than token cost
and the workflow can tolerate a few completed attempts being rejected by
validation before one succeeds. Keep the validator strong enough for the risk,
feed each rejection back to planning, and cap the attempts.

This is a workflow property, not a model-selection slogan. Do not use the
pattern where work is irreversible, validation is weak, or a bad attempt can
corrupt shared state. A provider, harness, or execution error is not a rejected
implementation attempt and does not retry unless the workflow explicitly
handles it.

## Coach against scope drift

For implementation workflows, give the planner, workers, and validators scope
coaches. Their instruction should oppose over-engineering, unrequested
features, gold-plating, and hypothetical edge-case fixes without a reasonable
actual failing unit test.

Coaching is advisory and never gates completion. Put essential constraints in
the initial assignment too: a short turn can finish before its coach looks.
Set `TYPESAFE_API_KEY` before starting a standalone run or hosted instance.
Jev screens completed exposed thinking for attached supervisors; there is no
timed cadence or fallback. Providers without those events do not trigger
automatic reviews. Observe whether an objection changed behavior instead of
treating attachment or message delivery as proof of useful supervision.

## Validate behavior and assess completion

Choose meaningful acceptance evidence before implementation when practical.
Do not let a worker weaken that condition to obtain a pass. Record the actual
check result; an agent saying it passed cannot override a failed command.

Use `Check` when an agent should interpret a command result: it records the
command, working directory, exit code, both output streams, and any execution
error in the current scope for the next turn. Its key follows the same rules as
`Set`: it is a compile-time constant written once in that scope. Name repeated
observations explicitly at their call sites, such as `tests.1` and `tests.2`.
A nonzero exit is evidence rather than a `Check` error; failure to execute,
capture, or record is an error. Use `RunCommand` when ordinary Go needs the
returned values itself. `Check` gathers evidence and never certifies success.

Use `Service(ctx, name, workdir, command)` for a foreground dependency that
must live for one scope, such as a development server. Gimbal starts the
string through `zsh -c` and continues immediately; successful start is not a
readiness check. Keep readiness in ordinary workflow code with `Check` or the
protocol the service exposes. Any exit before scope shutdown, including exit
zero, fails and cancels the owning scope.

The declaring scope is the lifetime boundary. A service outside an `Iterate`
stays alive across its item scopes; one declared inside an item ends before
the next item. Normal close and cancellation send SIGTERM to the service's
process group, followed by bounded SIGKILL escalation. The command must remain
in the foreground and its descendants must remain in that process group.
Gimbal records output and status but does not add restarts, health checks, or
management of resources owned externally by Docker, Overmind, or similar
tools.

A validator examines the work and the legitimacy of its validation. A green
build or test gate establishes only what it exercised. Claims about live
workflows, external steering, or browser interactions require observing those
behaviors. Preserve the distinction between a task result, an execution error,
ended dispatch, and a fulfilled goal.

Return an honest outcome when proof is missing or a real blocker remains.
Style preferences and unrelated improvements do not become acceptance gates.

## Make the workflow callable and understandable

Author an ordinary Go entry taking `context.Context`, `gimbal.Env`, and optionally
one package-local Params struct. Supported invocation fields are strings, ints,
bools and `polytype.Optional` of those types. Field comments supply visible
help; JSON tags supply submitted names. Required strings must be nonblank and
required integers positive. Optional fields preserve omission versus explicit
empty, false and zero; `Optional` does not accept null.

Generate an external module with the installed host:

```sh
gimbal generate --dir . --entry Review --name review \
  --role-default code-review=gpt-5.6-luna
```

Declare `github.com/tylergannon/polytype/polytype` as a Go tool in the project's
`go.mod`, pinned to the host's Polytype version. Pin Gimbal and all shared
packages to the deployed host revisions, and use the same Go toolchain,
platform and build flags. Generation calls `go tool polytype --validate` for
concrete local `Generate[T]` outputs and writes the input adapter, schema,
ordered fields, graph and source guide in the workflow package. Keep the Go
source and field comments authoritative; regenerate after changing inputs,
outputs or workflow shape. No project frontend generation is needed.

A plugin's main package exports `Register(*gimbal.Registry) error`. Register the
generated `ReviewDefinition()` with `RegisterWorkflow`, plus any backend
configuration/factory with `RegisterBackend`. Build with `go build -buildmode=plugin`
using the local host's matching build flags. For a published CLI, use `-trimpath`
and the exact released Gimbal source in a Go workspace as described in
[distribution](../gimbal-release/references/distribution.md#plugin-builds).
Install the `.so` in a configured `--plugin-dir`. Central and workflow daemons
load their own sorted configured directories before accepting work. Deploy the
matching plugin to central and to the workflow environment; restart to expose a
new catalog. An incompatible or duplicate definition fails startup. Generated
graphs have no init registration authority.

Built-ins follow the same definitions and registry path. Their inventory remains
in `internal/builtin/workflows.go`; `go generate ./...` regenerates that selection.
The CLI fetches descriptions from the selected central, builds useful parameter
and role flags, then submits pure invocation data. The shared Run form consumes
the same runtime metadata, including optional Include controls. Central validates
before admission and the workflow daemon prepares again before spawning the
independent runner. Use `--input` with JSON or `@file`, or parameter flags, and
`--follow` to wait for terminal completion.

Workflow and task routes are independent. `--workflow-endpoint` selects the
HTTP workflow daemon; `--workflow-project` identifies its local project and
`--work-dir` its execution directory. `--task-endpoint` selects the task daemon.
For a registered backend use `--workflow-route` or `--task-route` with a JSON
route containing `name`, `configuration` and `environment`. Each environment
provides its own workspace root and provisioned repository. A central project
path is not the remote execution directory. Transfer explicitly named context
and task files; arbitrary absolute paths in prose are not transparently rewritten.
Plain local invocation remains an independent child with directly local tasks.

For a remote turn, `gimbal.WithTaskFiles(ctx, backend.TaskFile{Name: "input.txt",
Bytes: data})` supplies explicit named bytes alongside runtime-owned context. The
task environment writes them and supplies their native paths to the agent.
Use `gimbal.WithYields(ctx, "store", "DATABASE_URL")` inline as the context
argument of `RunCommand`, `Check`, or foreground `Service` to declare outputs.
Do not assign the returned context: outputs belong to that one producer, and
the workflow linter rejects declarations elsewhere. The program writes `NAME=value`
strings to `ENV_FILE`; services atomically rename a completed file into place
only after resource readiness. Even a service with no outputs must publish an
empty file. Finite producers publish only after exit zero.

`gimbal.WithRequirements(ctx, "store", "DATABASE_URL")` declares
consuming-operation requirements. Repeated calls accumulate access to multiple
stores. Use `gimbal.DefaultStore` for the unnamed store in either declaration.
Gimbal checks the named values and grants the whole visible store. Programs
receive string environment variables; agents call the operation-scoped Gimbal
callback supplied by their native executor. Values are not automatically
inserted into prompts. Child definitions shadow ancestors across stores.

Named environments use `OrchestratorBackend` to establish a listening daemon;
messaging delivers the work and `SecretsBackend` supplies scoped values. The
route's `Backends` construction data configures these dependencies explicitly.
The supplied local implementation starts configured daemon commands and uses a
private shared file store. Scope cleanup stops dependent native work, releases
values, then releases environment use. Services receive SIGINT and have ten
seconds to clean up; uncertain cleanup stays owned. No automatic replay,
restart, secret rotation, or per-key permission system is provided.

Standalone `gimbal.Run(gimbal.Project(ctx, dir), ...)` runs in its caller's
process, writes under `dir/runs`, and does not attach to a running instance.
`gimbal run-prompt` creates its own headless runtime, using a temporary log
directory unless `--logs` names a fresh, empty directory. Neither path joins
the hosted instance's live controls or inherits its startup environment. Keep
their durable state separate from projects admitted to a running instance;
concurrent shared-state use has no supported contract.

CLI documentation is part of authoring. A caller should understand purpose,
required inputs, meaningful defaults, outputs or changes, completion and proof
expectations, limits, and a useful invocation without reading implementation.
Use enough detail for that workflow, not a fixed word count or boilerplate.

The current generator takes the entry function's doc synopsis for short help,
package documentation for long help, and parameter field comments for flag
help. Put the detailed explanation and examples in package documentation;
extra paragraphs only in the function comment do not become long help.

A run saves its registered graph with its durable state when it starts. The run
UI reads that saved graph, so a daemon restart or later workflow build does not
change the graph of an existing run. Keep the workflow's `go:generate`
directive and regenerate after changing its shape.

Inspect the generated workflow list and detailed help after changing the
comments. A graph or output schema does not replace caller documentation.
If the desired help requires a generator change, identify that concrete gap.

## Finish with observation

Run the relevant checks and exercise the real workflow with cheap models such
as Luna or Haiku. Inspect actual prompts, handoffs, decisions, validation, and
results. Check that a caller can discover and understand it through CLI help.
Report what you observed, which model ran, and anything still unproved.
