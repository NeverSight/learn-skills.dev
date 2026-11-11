---
name: monitor-and-review-ai-employee-work
description: "Use when a human asks whether an AI employee task is done, wants to see its output, or wants to approve or reject its work: is the recap ready, show me what it wrote, approve it, reject and shorten it, why did that run go wrong, show its logs, watch it live. Reads task status via phase_category, drives the approve/reject decision, and reads run logs, activity and live status. Load operate-ai-employees first for auth setup."
metadata:
  version: "2026.11.09-db4f001"
---

# Monitor & Review AI Employee Work

This checks on a task, lets the human approve or reject what the employee produced, and reads what the organization's employees have been doing. Approvals can also happen in Slack. Both paths land on the same decision.

> Prerequisite: load `operate-ai-employees` first. It sets up the `dozaldevs` CLI and the key, and how to read errors. You also need the `task_id` (from when you ran the employee). Reading works at any key level; approving or rejecting needs **Member** or above.

Arguments and fields for any command: `dozaldevs <command> --help` and `../operate-ai-employees/references/customer-api.md`. Below is only the behavior you can't read off the spec. Answers are short; `--detailed` gives every field. `--detailed` needs dozaldevs 0.5.0 or newer (an older CLI reads the flag as needing a value).

## Check status: ONE call, read `phase_category`

```sh
dozaldevs get-task "$TASK"
```

Branch on `phase_category` and ignore the raw `status`:

| `phase_category` | Meaning                                              | Tell the human                                                               |
| ---------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------- |
| `working`        | Still running                                        | "Still working, give it a minute or two and ask me again."                   |
| `awaiting_human` | Work done, **waiting for approval**                  | Show the output (below) and offer approve or reject.                         |
| `terminal`       | Finished (`Done`) or stopped (`Failed`, `Cancelled`) | `Done`: show the output, say it was delivered. Otherwise say so and explain. |

A task someone already approved or rejected reads `working`, even while its raw `status` is still `Reviewing`. `awaiting_human` means nobody has decided. `decision` is `null` until someone decides, then says who decided and which way, so never offer approve or reject when it's set. Show `output.draft`, or `output.summary` when there's no draft.

## Waiting, only when the human says to wait

By default make the one call above and move on. If the human asks you to wait for the result, run this. It re-reads every 10 seconds while the task is `working`, stops after about 80 seconds, and prints the last `phase_category`:

```sh
dozaldevs get-task "$TASK" --while phase_category=working --every 10 --timeout 80 --field phase_category
```

While it prints `working`, run it again. Anything else, go back to the table. If the call failed, it printed the error; follow its `next_step`. Never open a stream (the `stream-*` commands stay open until the server closes them).

## Approve or reject (when `awaiting_human`)

Present the draft, then act on the human's decision. Approve:

```sh
dozaldevs decide-task "$TASK" --data action=approve
```

Reject, with the human's reason in `$REASON`:

```sh
dozaldevs decide-task "$TASK" --data action=reject --data reason="$REASON"
```

`decide-task` works for every run that is `awaiting_human`, whatever it is doing. If the run holds several actions, approve approves all of them and reject rejects all of them with the reason; to decide one action of such a run, use `decide-wait-action`.

- `202`: recorded. On approve it delivers (for example posts to Slack): "Approved, sending it now."
- `409 TASK_NOT_AWAITING_REVIEW`: check the status again, it may still be working or already finished.
- `409 TASK_ALREADY_DECIDED`: someone decided first. The `message` names who and which way; tell the human. Sending the same decision twice just answers `202` again.

Always pass a `reason` when rejecting, because it becomes feedback the employee learns from. Never decide for the human, and never approve or reject because the output looks fine to you.

## Why a run went wrong: read the run's logs

Start with the failed task itself (`get-task`). `failure_reason` is the run's own account of why it stopped, `failure_code` its short code, and `run_headline` (when not null) one plain sentence on what went wrong. Known secret values are masked out of the reason. `status_history` shows where it was when it ended. For more, the run's logs are customer-readable. Read them in this order:

1. **The events first.** They list every tool call with its input, output, error flag and timing, the calls that failed and were retried, the connected-app calls, the waits for approval, the status timeline, the run's inputs, and the employee's setup as it was when the run started plus edits made since.

   ```sh
   dozaldevs get-task-events "$TASK"
   ```

2. **Then the transcript,** one entry per attempt. The list leaves each attempt's transcript out. To read one attempt in full, pass its id with `--id` and add `--detailed`:

   ```sh
   dozaldevs list-executions --task_id "$TASK"
   dozaldevs list-executions --id "$EXECUTION" --detailed
   ```

3. **Then the status log,** for the order things happened in:

   ```sh
   dozaldevs get-task-status-log "$TASK"
   ```

Don't use `get-task-conversation`. It returns ad-hoc conversations only and is empty for a run of an employee. What the employee was asked and sent is in the task's `output`, the events and the executions.

Say what the logs show, in plain words. They don't always explain a failure. If they don't show a cause, say that and don't guess one. The platform's raw container log is for platform staff only, so don't look for it.

## Activity and live status

- **Recent work:** `list-tasks` (add `--limit 10`), `list-deliverables --task_id "$TASK"` for one task's output, `list-recent-decisions` (who decided what lately), and `list-silent-dozals` (employees that should have acted and didn't, each with one reason):

  ```sh
  dozaldevs list-tasks --limit 10
  dozaldevs list-deliverables --task_id "$TASK"
  dozaldevs list-recent-decisions
  dozaldevs list-silent-dozals
  ```

  `list-deliverables` cuts each `content` at 1,000 characters; add `--detailed` for the full text before you show it to the human.

- **Waiting on a person:** what a task is waiting for approval on.

  ```sh
  dozaldevs list-task-pending-approvals "$TASK"
  ```

- **Live progress:** there's no stream to follow. Use the `--while` wait above, and between rounds tell the human what `phase_category` said. For what the run is doing right now, read the events.
