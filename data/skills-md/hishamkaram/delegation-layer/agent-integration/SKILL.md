---
name: agent-integration
description: Use the installed Delegation Layer CLI to select a ready provider, run one bounded agent turn, collect durable JSON evidence, and continue a timed out session safely.
---

# Delegation Layer

Use this skill when a task should be performed by another coding agent through
the local `delegate` CLI. The CLI is the only integration surface. Do not call,
inspect, authenticate, or install a provider CLI directly.

## Rules

1. Check whether `delegate` is already installed. If it is missing, report the
   missing prerequisite and stop. This skill never installs or repairs the CLI.
2. Use `dispatch --auto` unless the user explicitly selected a provider ID.
   Provider selection, executable checks, compatibility checks, authentication
   gates, and supervisor admission belong inside Delegation Layer.
3. Give every turn an absolute workspace, a separate state root, an explicit
   permission mode, and a finite budget.
4. Use `--json` and save the returned `task_id`. Read `admission`, `liveness`,
   `publication`, `status`, `outcome`, `continuation`, `task_record`, `failure`,
   and `error` as separate fields.
   Delegate owns the supervisor lifecycle. Never install, configure, start,
   inspect, or repair Pueue, and never poll a task unless the response says its
   `task_record` is `created`.
5. Observe with `status` and collect with `collect`. Collection may recover the
   saved supervisor only to observe an already-requested budget stop; it never
   launches a provider or retries a task.
6. If a task is timed out and its JSON says `continuation.resumable: true`, use
   `continue --task TASK_ID`, optionally with a new `--brief`. Do not create a
   fresh unrelated dispatch to replace a resumable task.
7. Treat `blocked` authentication as unresolved. Do not call it compatible,
   successful, or failed provider behavior, and do not invent login commands.
8. Never put credentials, tokens, or unrestricted provider output in a brief,
   option, receipt, or agent message.
9. Permission modes select provider-native behavior, not an independent sandbox.
   Providers load their own configuration and extensions. If a task is rejected,
   report delegate's evidence; do not assume the user's configuration is faulty
   or remove MCP servers, plugins, settings, or credentials to make it pass.
10. The model chooses ordinary-task fan-out by issuing independent `dispatch`
    commands concurrently. The private supervisor does not impose a task-count
    or CPU-based limit. Use this for independent investigation, debate, review,
    or provider comparison. Concurrent write tasks must use separate workspaces
    or explicit coordination to avoid file conflicts.

## Operating procedure

### 1. Verify the control CLI

Run a quick local check:

```sh
command -v delegate && delegate --version
```

If discovery fails, report that Delegation Layer is missing. If the version
command fails, report that the installed CLI is unusable. Stop in either case.
Do not substitute a provider command.

### 2. Discover only when useful

For the normal path, use automatic selection directly. If you need to explain
what the installed build knows, run:

```sh
delegate providers --json
```

This is a catalog, not proof that a provider is installed, authenticated, or
ready. If the caller named one provider ID and wants a side-effect-free check,
run:

```sh
delegate preflight --provider PROVIDER_ID --cwd ABSOLUTE_WORKSPACE \
  --permission REQUESTED_MODE --json
```

Replace `REQUESTED_MODE` with `read-only` for investigation or
`workspace-write` for authorized edits. Preflight reports static admission only.
It does not create a task, start the supervisor, or launch a provider. Do not keep
retrying preflight when it says
`blocked` or `unsupported`; report the bounded reason.

The catalog and `capabilities` response expose supported permission modes,
request options, continuation, and the read-only mechanism. A read-only
capability with `containment: "provider-owned"` selects the provider's native
behavior but is not an independent delegate-owned sandbox. Static discovery
does not prove authentication or live acceptance; use the dispatch or live
acceptance result for that evidence.

If the caller needs an explicit model or effort, use the implemented native
discovery command for that provider:

```sh
delegate models --provider PROVIDER_ID --cwd ABSOLUTE_WORKSPACE --json
```

Omit `--cwd` to use the current directory. Run discovery only when the caller
needs a non-default choice; provider defaults are valid. The command uses the
state-rooted supervisor and a bounded `model-discovery-v1` five-minute native
inspection to allow first-run provider model/cache initialization. It creates
inspection evidence without admitting a provider task, and may contact the
provider CLI. It is advisory and never an admission allowlist. Do not reject a
requested value merely because discovery did not list it, and do not infer
per-model effort support from the harness-wide list. If a selected model has
`efforts: null` or `efforts: []`, omit `--effort` unless the caller explicitly
requested it; do not invent model aliases or combine options by guessing.

The response includes `schema_version`, `command: "models"`, `provider`,
`observed_at`, `status`, `reason_code`, `complete`, `source`, nullable
`efforts`, and model rows with exact `id` values plus optional `name`, nullable
`efforts`, and optional `default_effort`. `complete` describes model
enumeration, not effort metadata. `null` means effort metadata is unknown;
`[]` means the provider explicitly reported no choices. Discovery exits `0`
for `available` or `partial`, `2` for `blocked` or `unavailable`, and `1` for
`failed`. Preserve a blocked or unavailable discovery result as unresolved;
defaults remain allowed.

### 3. Prepare separate paths and a finite brief

Use an existing task brief when one is supplied. Otherwise create a bounded
brief file that contains the requested work and its acceptance criteria. Keep
the state root outside the workspace:

```sh
STATE_ROOT="${DELEGATE_ROOT:-$HOME/delegation-state}"
WORKSPACE="$PWD"
BRIEF="$(mktemp)"
cat >"$BRIEF" <<'EOF'
Describe the delegated task, the files or behavior to change, and the checks
that must pass. Keep the response concise and report validation evidence.
EOF
```

Replace the example brief with the actual user request. Do not place the state
root inside the workspace or place secrets in either path’s task data. Keep it
outside provider configuration and runtime directories as well. If delegate
rejects placement before admission, choose a separate state directory; do not
change provider settings. Once admitted, retain that state root for every
observation and continuation.

### 4. Dispatch one bounded turn

Use automatic selection unless the user explicitly supplied `PROVIDER_ID`.
For a named provider, replace `--auto` with `--provider PROVIDER_ID`; never
combine the two:

```sh
delegate --root "$STATE_ROOT" dispatch --auto \
  --brief "$BRIEF" \
  --cwd "$WORKSPACE" \
  --permission read-only \
  --budget 30m \
  --json
```

For an authorized code change, use `--permission workspace-write`; this requests
unattended native tool execution, including shell commands and file edits.
The provider may allow access beyond the selected workspace. Delegate supplies
the native approval options; do not add provider flags or call its CLI yourself.
Keep the budget finite. A successful dispatch means the request was durably admitted;
it does not mean the delegated work finished.

For independent work, the model may run several complete `dispatch` commands
concurrently. Keep each task's brief, workspace, permission, and task ID
independent. Do not configure Pueue or wait for one task before dispatching the
next solely to serialize ordinary work. Inspect each returned task separately
with `status` and `collect`.

When an explicit selection is supplied, pass it through the public fields:
`--model MODEL` and `--effort VALUE`. Codex encodes effort as its native TOML
`model_reasoning_effort` setting; Claude and AGY use their native effort flags;
Pi maps effort to `--thinking`; and OpenCode maps effort to `--variant`. An
omitted or `default` effort is omitted from native argv. For AGY read-only,
`--permission read-only` selects the exact native `--sandbox --mode plan` path
without a bypass. Authorized AGY workspace-write retains its existing native
bypass. Do not add these native flags yourself.

Save the exact `task_id` from the JSON response. The recovery steps below apply
to parsed dispatch responses. If the CLI rejects the command syntax before
dispatch (nonzero exit with a usage error and no JSON response), correct the
reported syntax and invoke it again; argument parsing fails before admission and
does not create a task record. For a parsed dispatch error, read its `failure`
and `task_record` fields. If `task_record` is
`not_created`, do not run `status`, `collect`, or `continue`; correct the request
only when `failure.next_action` is `correct_request`, otherwise report the
delegate failure and stop. If it is `created`, use `status` before taking any
other action. If it is `unknown`, stop and report the failure: with an
explicit task ID, absence can race another dispatch that is creating the same
ID. Never retry that ID, run Pueue commands, or silently try another provider
after a task may have been admitted.

### 5. Observe and collect

Use the same state root and task ID:

```sh
delegate --root "$STATE_ROOT" status TASK_ID --json
delegate --root "$STATE_ROOT" collect TASK_ID --watch 5s --json
```

Check `status` first: if it is `timed_out`, follow step 6 even when publication
is pending and no outcome is present. Otherwise, if `collect` exits with code
`3` because publication is still pending, wait a short interval and run
`collect` again. Do not dispatch again. Continue until
the response has a terminal `outcome` or a bounded operational error that
requires the caller’s attention.

Accept a result only when the terminal outcome is present and its publication
is committed. A rejected outcome is terminal evidence and must be reported as
rejected. Payload and raw output are returned as validated descriptors; do not
copy unrestricted provider output into the control response.

### 6. Continue a timed out turn

When `status` or `collect` returns `status: "timed_out"`, inspect the nested
continuation object:

```json
{
  "status": "timed_out",
  "continuation": {
    "resumable": true,
    "mode": "native",
    "predecessor_task_id": "TASK_ID",
    "continue_command": "delegate continue --task TASK_ID --json"
  }
}
```

If `resumable` is true, create the linked successor through the public
continuation command. Supply a new follow-up brief when the next turn needs a
new instruction:

```sh
delegate --root "$STATE_ROOT" continue \
  --task TASK_ID \
  --brief "$FOLLOW_UP_BRIEF" \
  --budget 30m \
  --json
```

The command preserves the exact provider session and permission mode and
creates a new task ID. Do not add `--permission` to `continue`. Always include
the original `--root`, even if a returned command hint omits it. Observe and
collect the successor by repeating step 5. If `resumable` is
false, report the reason and stop; a fresh dispatch would lose the original
conversation and is not an equivalent recovery.

If `continue` returns an error, use its `failure` and `task_record` fields just
as for dispatch: when the record is `created`, check the returned successor
`task_id` with `status`; when it is `not_created`, correct the request only if
`failure.next_action` is `correct_request`; and when it is `unknown`, stop and
report the failure. Do not repeat `continue` while successor creation is
unknown.

## JSON decisions

The capability projection uses the stable `runtime-capability-v1` contract.
Catalog responses have `verification: "catalog"` and `status: "unknown"`.
Preflight responses have `verification: "preflight"` and describe static
readiness. A dispatch response can report `verification: "runtime"` only after
the supervised runtime probe has observed the required behavior and executable
identity.

Versions and help text are observations. Accept any valid nonempty version
reported by the CLI; never apply a semantic-version allowlist or web lookup.
The adapter’s required flags and runtime behavior decide compatibility.

Authentication is a separate live gate. `live_acceptance.status` values are
`not_run`, `passed`, or `blocked`; a blocked authentication prerequisite is
neutral evidence and must not be relabeled. Report the missing authentication
prerequisite and stop that attempt; do not retry or authenticate the provider.

The task response separates:

- `admission`: whether the request was accepted by the durable boundary;
- `liveness`: the observed supervisor state;
- `publication`: whether validated evidence was committed or rejected;
- `outcome`: the terminal authority, when available;
- `continuation`: whether the exact session can make a linked successor; and
- `error`: bounded operational diagnostics.

See [references/command-reference.md](references/command-reference.md) for
the command matrix, [references/result-handling.md](references/result-handling.md)
for decision rules, and [references/continuation.md](references/continuation.md)
for timeout recovery. The examples and machine-readable checks in `examples/`
and `evals/` are part of this skill package.

## Completion report

Report the original task ID, selected provider ID when the CLI returns one,
the final admission/liveness/publication fields, the terminal outcome and
evidence descriptors, and any continuation or blocked-authentication state.
