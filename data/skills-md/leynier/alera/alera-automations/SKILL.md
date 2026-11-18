---
name: alera-automations
description: Create, edit, inspect, pause, and run scheduled Alera agent automations through the CLI, and report the lifecycle of an automation run. Use for recurring or one-time agent work in an Alera runtime.
metadata:
  version: 5
---

# Alera Automations

Use `alera automation` for scheduled agent work. Automations are definitions; runs are individual executions. Orchestration tasks are separate and use `alera-orchestration`.

## Authoring

Choose the execution target explicitly. Never infer a target type. Once chosen, `--workspace-id`, `--profile-id`, and origin can come from the current Alera terminal environment. A profile, prompt, schedule, and valid target are enough. Creation is Active unless `--draft` is supplied. Editing an Active automation keeps it Active and affects future runs.

```bash
alera automation --json create --name 'Daily Review' --prompt 'Review changed files and report findings' --cron '0 9 * * 1-5' --timezone America/Mexico_City --target fresh-tab --request-key daily-review
alera automation --json create --file automation.json --dry-run
alera automation --json edit --id <id> --prompt-file prompt.txt --expected-revision <revision>
alera automation --json list --workspace-id <workspace-id>
alera automation --json show --id <id>
alera automation run-now --id <id>
alera automation pause --id <id> --active-runs continue-active
alera automation resume --id <id>
alera automation --json clone --id <id> --name 'Weekly Review' --draft
alera automation --json edit --id <id> --reuse conversation
alera automation --json unbind --id <id> --reason 'Start over'
```

Use a stable `--request-key` when retrying creation after an ambiguous response. `--dry-run` checks readiness without saving. `preview-schedule --cron '0 9 * * *' --timezone UTC` previews dates. `clone` copies a definition's settings and target into a new automation. `--reuse workspace|conversation` makes later runs return to what the first run created; `show` prints where the automation is bound and `unbind` forgets it. Read [targets and JSON](references/authoring.md) for other targets, reuse, and advanced settings. Use `alera automation <command> --help` for optional flags.

## Execution

A runtime must be running for schedules to fire. Creating an automation does not enable login autostart or change keep-runtime settings. The default skips occurrences missed while offline. Already admitted runs recover separately: reconcile their owner, resume the native conversation when possible, then retry with context in the preserved workspace. Recovery has three total launches, 60/120 second backoff, and the original 24-hour deadline. A run on an unreachable remote host stays reserved until its closure can be verified; do not launch a replacement manually into the same target while ownership is unknown.

Watching a terminal is read-only. Take Over stops automatic recovery and preserves the workspace. Use it only when the user intends to operate that agent.

## When You Are Running An Automation

`ALERA_AUTOMATION_RUN_ID` and `ALERA_AUTOMATION_ATTEMPT_ID` bind lifecycle calls to the current attempt. The CLI supplies the target identity from the terminal environment. Keep those variables intact. An automation that reuses its conversation pastes later runs into the same agent, whose environment still names the first run: use the `--run` and `--attempt-id` values the latest prompt gives, which win over the environment.

```bash
alera automation --json context --run "$ALERA_AUTOMATION_RUN_ID"
alera automation heartbeat --run "$ALERA_AUTOMATION_RUN_ID"
alera automation complete --run "$ALERA_AUTOMATION_RUN_ID" --status success --summary 'Describe the result and verification'
```

Report progress during long work. Complete once with a useful summary and `success`, `failure`, or `blocked`. A superseded attempt must stop lifecycle writes. Before retrying external effects, inspect existing results to avoid repeating them.
