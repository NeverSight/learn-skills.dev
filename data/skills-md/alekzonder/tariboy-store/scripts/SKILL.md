---
name: scripts
description: Use when a local command must continue beyond the current Tariboy iteration or run repeatedly on a durable schedule.
---

# Durable Scripts

This skill's `scripts/scripts.sh` launcher lives inside this skill directory
and calls the identity-bound daemon through `TARIBOY_TOOLS_SOCKET`.
Execute the launcher when command execution is available. If it is unavailable,
return the exact command instead; never claim a script was queued, scheduled,
rerun, cancelled, or removed unless the command succeeded.

Run once with `scripts/scripts.sh run <name> -- <command>`. Queue it exactly once,
finish the iteration, and consume the later `script.result` message instead of
waiting in the current iteration.

Run repeatedly with `scripts/scripts.sh schedule <name> --every <seconds> -- <command>`.
Runs never overlap. `--quiet-exit CODE` records that exit without waking the
agent and is the only outcome that keeps the schedule running.

Inspect with `scripts/scripts.sh ls`, `scripts/scripts.sh runs`, and
`scripts/scripts.sh logs`; use `scripts/scripts.sh rerun`,
`scripts/scripts.sh cancel`, or `scripts/scripts.sh rm` for lifecycle control.

## Address every definition by its script ID

**REQUIRED:** `rerun`, `cancel`, and `rm` accept only the `scr-...` script ID
or a `srun-...` run ID. Names are not unique and are not resolved: passing one
fails with `not found`, and `run <name> -- <command>` creates a second
definition instead of resuming the stopped one.

Take the ID from the `script_id` field of the `script.result` message that woke
you, from the creation output, or from `scripts/scripts.sh ls`. Record the
script ID, not only the name, wherever a durable monitor is recorded.

## A published result stops the schedule

A recurring definition keeps its schedule only while every run stays quiet.
The moment a run publishes a `script.result` message, the daemon sets the
definition to `completed` and clears its next run: the agent is notified once
instead of repeatedly, and **no further runs happen until it is resumed**.

This covers every published outcome:

| Event | Effect on the recurring definition |
| --- | --- |
| Run exits with the `--quiet-exit CODE` value | No message; schedule keeps running |
| Run exits with any other code, success or failure | Result published; definition stopped |
| A schedule created without `--quiet-exit` | Every run publishes, so it stops after the first run |
| `cancel <run-id>` for one active run | That run still publishes a result, so the definition stops too |
| A run interrupted by a daemon restart | Recovery publishes the interrupted result, so the definition stops |
| `cancel <script-id>` | Definition cancelled; it can never run again |

## Handling a `script.result` for a recurring definition

**REQUIRED:** Process the result, then close it with exactly one of these two
decisions before the iteration ends. Doing neither silently ends the
observation.

1. **Still needed** — resume the same definition:

   ```bash
   scripts/scripts.sh rerun <script-id>
   ```

   `rerun` runs it now and returns the definition to `active`, so its fixed
   delay continues afterwards. Never create a replacement schedule for work
   the stopped definition already describes.

2. **No longer needed** — remove it:

   ```bash
   scripts/scripts.sh rm <script-id>
   ```

   The published result already stopped it, so no `cancel` is needed. Run
   `scripts/scripts.sh cancel <script-id>` first only when `ls` still reports
   `state: active`.

A stopped definition is not a wait object. Never end an iteration describing a
definition that published its result as an active monitor: either it was
resumed with `rerun` in this iteration, or the iteration's wait object is
something else.

## External prerequisite failures

**REQUIRED:** A recurring schedule whose command cannot succeed until an
external prerequisite changes, such as a missing credential, binary, or
dependency, is no longer a valid wait object. Its failing result already
stopped it, so take branch 2 above and never `rerun` it:

```bash
scripts/scripts.sh rm <script-id>
```

Run `scripts/scripts.sh cancel <script-id>` before it only when `ls` still
reports `state: active`. Then, for a Native Task:

1. Mention the customer and ask one blocking question. Reuse a matching
   unanswered question instead of creating or repeating it.
2. Set the task to `wait_customer` if it is not already there and record the
   question as the only resume event.
3. As the final action, finish the iteration through the `loop` skill with
   `scripts/loop.sh done`.

The failure is handled only after the definition is removed, the task has one
customer-answer wait, and the iteration is finished. An action trace that omits
any of these is incomplete.

Pausing or disabling leaves the useless definition behind; it does not complete
this sequence. Do not rerun the command, create a replacement schedule, or
repeat the failure comment while the question remains unanswered.

## Red flags

| Thought | Reality |
| --- | --- |
| "The schedule keeps running, so I can just finish." | Any published result stopped it. Resume with `rerun <script-id>` or remove it. |
| "Cancelling one run leaves the schedule intact." | That run still publishes a result, which stops the definition. |
| "I will schedule it again to resume monitoring." | A second definition duplicates the work. `rerun <script-id>` resumes the recorded one. |
| "`rerun <name>` is clearer than the ID." | Names are not resolved; only `scr-...` IDs work. |
| "It succeeded, so nothing stopped." | Success is not quiet. Only the `--quiet-exit` code is quiet. |
