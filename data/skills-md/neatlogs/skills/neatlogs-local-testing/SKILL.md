---
name: neatlogs-local-testing
description: Test and improve a user's real agent with the Neatlogs CLI and SDK. Create or resume local experiments, capture or select dataset cases, run current and candidate versions with quality checks, and compare recorded evidence in Neatlogs.
---

# Neatlogs local testing

Work in the user's agent project. The coding assistant runs the workflow; Neatlogs displays command activity and saved results. Keep setup in this chat, without sending the user back to Neatlogs for routine configuration. Do not display internal phase numbers.

## Establish intent and connection

- Use the user's goal, host and project. Ask one short question if the goal is missing. Never hardcode a cost, speed or quality target. Clarify an ambiguous measurement before claiming it was achieved.
- Inspect installed CLI and SDK versions and `--help` before choosing commands. The API package is `neatlogs-cli`; the SDK's doctor executable is not a substitute. Verify the resolved executable, host, account and project. The API host is the dashboard origin, not the telemetry ingest endpoint.
- Read `neatlogs --help`, `neatlogs local --help`, `neatlogs experiments --help`, `neatlogs datasets --help`, `neatlogs evals --help`, `neatlogs evaluators --help` and `neatlogs detections --help` as needed. Use installed command schemas for request bodies. If a required command is missing, identify the installed version and required capability; do not invent syntax.
- Use existing authorized credentials without printing or committing them. Request browser approval when device sign-in requires it. Do not broaden scopes silently.
- Start `neatlogs local connect` in a separate terminal and keep it alive during testing. A heartbeat confirms CLI availability, not agent execution. Only an actual saved agent trace confirms capture.

## Create or resume the experiment

Create the experiment name and goal yourself from the user's intent:

```sh
neatlogs --json experiments create --name "<name>" --goal "<goal>" --idempotency-key "<uuid>"
```

Use real values, not these placeholders. Save each request key before calling and reuse it if that request must be retried. Read returned IDs; set `NEATLOGS_LOCAL_EXPERIMENT_ID` in every command shell and child task environment. Set `NEATLOGS_LOCAL_ROUND_ID` after creating the prepared round below. This links relevant CLI activity, failures and retries to the correct experiment in Neatlogs. A new hypothesis gets a new round ID.

Resume only when the user asks to resume a specific experiment or the current task was interrupted. Verify saved host/project/experiment IDs before restoring private state. A new prompt is not permission to resume a previous experiment automatically. Keep assistant-owned metadata such as run IDs, pins, request keys and progress credential-free in ignored, permission-restricted local state.

SDK resume files can also contain task outputs and exception text, including credentials embedded in an HTTP error or URL. File permissions do not sanitize that content. Before using resumable state, use sanitized test credentials/fixtures and a safe task/error boundary that preserves the behavior being tested. If faithful evidence cannot be captured safely, report the limitation instead of claiming the state is credential-free. Never print, commit or share raw resume files.

## Choose cases deliberately

Honor the user's choice:

| Intent | Action |
| --- | --- |
| Fresh cases or new dataset | Run new representative conversations and create a new dataset from their verified traces. Do not reuse previous cases. |
| Existing dataset/cases | List datasets and versions, inspect the chosen cases and use the requested selection. |
| Add cases | Capture the additional cases and create a new dataset version; preserve earlier versions. |
| Resume a run | Reuse its exact pinned version, cases, trials, settings and checks. Retry only unfinished work. |
| No preference on a new experiment | Ask once: “Use an existing dataset, or create fresh cases for this goal?” Do not silently select an old pinned dataset. |

Choose realistic cases relevant to the goal, including follow-ups, ambiguous requests, tool failures and unsupported requests when applicable. Do not narrow the sample to easy cases to obtain a winner. Summarize the selected scope in chat; do not add a separate approval step when the user has already authorized it.

Inspect the actual agent entry point and instrument its real model calls and tool executions with the language-appropriate SDK. Use provider wrappers or supported explicit spans; preserve request messages, instructions, model/settings, tool declarations, call IDs, tool arguments/results, errors, timestamps and available usage. Keep conversation history and link tool execution to its requesting call. Do not substitute saved answers or fabricated telemetry for agent execution.

Finish spans and flush using the installed SDK's supported lifecycle. Wait for ingestion/finalization with bounded polling. Trace metadata alone is insufficient: inspect recorded spans, including pagination, and confirm complete requests and tool outcomes. Use the CLI's dataset/case validation before launching a run. Distinguish:

- **Saved recording:** replay requires complete captured model requests and compatible tool evidence.
- **Input-only case:** usable by a real agent task that accepts the input; not necessarily replayable.

Repair capture at its source and recapture when needed. Preserve failed cases and exact reasons; do not silently omit them. If repair cannot proceed, explain what is missing and offer a real agent task or recapture path. Avoid repeated polling for evidence that was never emitted.

Inspect `neatlogs datasets from-traces --help` before creating a dataset. Pin its returned version and exact case IDs for both runs. Do not mutate pins midway through a comparison.

## Prepare quality checks

Inspect existing evaluations, evaluators and detections. Reuse checks only when they fit the goal and cases; otherwise create them through supported CLI commands. Pin the same evaluation version and evaluator IDs for both runs. Verify question assignments, evaluator model access, supported evidence and available allowance before generation. Use preview/readiness capabilities when available.

Check accuracy, grounding and goal-specific behavior. Score against a declared source of truth; do not assume the original answer is correct. A failed grader is an execution failure, not a failed quality score. A successful tool execution does not prove its output is correct. Report detection configuration, execution and findings separately: missing findings do not establish that detection ran or passed.

Do not modify billing/credit records, weaken checks or change pass criteria to make a run succeed. Report unsupported checks and missing permissions precisely.

## Save the setup and prepare a round

Inspect `neatlogs experiments record --help` and `neatlogs experiments round --help`. Use only supported capabilities; older CLI/SDK builds must be updated before claiming round tracking. Save checkpoints with `neatlogs experiments record --experiment <id> --body-stdin --idempotency-key <uuid>`:

- `kind: "setup"`: send `setup` with `datasetVersionId`, selected `caseIds`, `trials`, `formVersionId`, `evaluatorIds`, `detectionIds`, and `resources`. Each resource records its `kind`, `id`, `revision`, `disposition` (`created` or `reused`) and a short user-facing `reason`. Include no credentials, raw terminal output or private reasoning. The backend validates selection and freezes the grading/detection configuration.
- Create the round using the existing `experiments round` command with its name, hypothesis and `--variants` JSON containing `A` and `B`, each with `name` and exact `changes`. The round snapshots the shared setup. Set its returned `NEATLOGS_LOCAL_ROUND_ID`.
- `kind: "preparation"`: send `roundId`, `variant` (`A` or `B`) and `preparation` containing `state` (`preparing`, `ready` or `failed`), a brief `message` and the real `git` branch/sha when available. Mark ready only after preparing the actual agent code and settings. Each round has stable identities `(roundId, A)` and `(roundId, B)`.

A changed dataset, check configuration or hypothesis requires a new setup/round; never mutate the setup frozen into earlier rounds. This tracking adds no human approval step in the Neatlogs UI.

## Run and improve

Create an SDK evaluation task that invokes the actual agent with the chosen settings, retains conversation history and executes its own tools. Inspect `neatlogs evals run --help`; use supported dataset/version/case/trial/form/evaluator options. With an initialized TypeScript SDK, use `--trace-evidence` when supported. Explain other language/provider limitations rather than inventing evidence support.

Run current and candidate on the same pinned cases, trials and checks. Include `--experiment <id> --round <id> --variant A|B --attempt 1` on each `evals run`; use the matching git options when the preparation pinned a revision. Keep separate private retry state for each run, subject to the task-data boundary above. Record actual model/prompt/tool/config changes. Hosted simulation reuses saved tool results; it cannot demonstrate new execution of the user's tools. Use real agent tasks for runtime comparisons. Respect the user's budget and tool permissions.

Wait for generation and grading separately. On failure, inspect the exact error and repair its cause. Retry transient failures with backoff, at most two automatic retries per unchanged failure; preserve successful answers and prevent duplicate mutations/charges. Use a supported grading retry path for saved answers instead of regenerating the whole run. Stop repeated retries for auth, quota, unsupported evidence or missing configuration and report the needed action.

If B alone fails, keep successful A. Resume B with the same attempt and private state if execution is safe to resume. If a repaired task requires a new run, use the next B attempt number and a new private state file; retain the failed attempt. Do not rerun A to make the screen symmetric. An uncertain execution requires inspection before another dispatch.

After each run completes, if detections were configured, record `kind: "checks"` with `roundId`, `runId` and a stable UUID `requestKey`. This queues the existing run-level detection worker against the frozen selection. Inspect `experiments get <id>` for `runAttempts[].detectionChecks`; wait for complete coverage and report failed, skipped or uncertain checks explicitly. Do not replace missing results with a pass. Retry a failed check batch with a new saved request key only after inspecting its cause; never regenerate successful agent answers for a grading or detection retry.

For each iteration, keep the baseline and checks stable where comparable, state the hypothesis, and save a new round. Do not overwrite unfavorable results. If pins/checks change, mark the comparison as changed and rerun both versions as needed. Never iterate indefinitely without a user-approved time or spend budget.

## Compare and report

Use `neatlogs evals compare <current-run> <candidate-run>` after inspecting both runs' completion and grading. Do not assume its response contains a URL. If one is returned, verify its host before opening it. Otherwise open the saved experiment from Local testing on the verified dashboard and select its run comparison. When that host supports it, the experiment route is `/experiments/local/workspace/<experiment-id>?orgId=<verified-org-id>&projectId=<verified-project-id>`; use actual returned IDs and verify the destination. If no supported browser destination is available, report the experiment/run IDs and CLI results with that navigation limitation. Keep the two environment IDs set for related CLI commands so the UI can show execution status. The activity feed represents reported Neatlogs commands, not the coding assistant's private reasoning or unrelated terminal activity.

Give a report card for each round: hypothesis, model/settings, selected and completed cases, grades, detections, tool names/outcomes, tokens, latency, cost, failures and unavailable measurements. Distinguish model time from whole-agent time and generation cost from grading/tool cost. Missing measurements are not zero.

Save the round using the same `experiments record` command with `kind: "result"`, `roundId` and `result` containing `runA`, `runB`, `outcome` (`goal_met`, `goal_not_met`, `tradeoff`, `incomplete`), `decision` (`continue` or `finish`) and a brief evidence-based `reason`. If using saved rechecks, include their exact `gradingBatchA`/`gradingBatchB` IDs. A blocked result may include `blocker` with stage, safe error code/message, request ID and retry timing. Retry incomplete checks and replace that incomplete assessment after recovery; completed decisions remain immutable. Results are the coding agent's assessment, not a backend guarantee of a production winner. Persist it before starting another round or finishing.

Compare against the user's goal and quality constraints. Name the version and model when recommending a winner, with the supporting evidence and sample limitations. If results are incomplete or inconclusive, say so; never promise the goal will be achieved. Keep results discoverable under the experiment. Rollout, deployment, publishing and sending results to other people require separate user authorization.
