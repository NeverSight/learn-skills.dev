---
name: t3code
description: >-
  Delegate coding work to T3 Code, or follow up on, check, or stop an existing
  T3 Code thread.
disable-model-invocation: true
---
# T3 Code

## Where it runs
T3 Code runs on the same machine as your shell — the user's local machine. Drive it only through the bundled `scripts/t3-run.mjs`; the T3 Code window is the user's, so leave it to them.

Resolve script paths from this skill's directory (the folder that contains this `SKILL.md`). Below, `t3-run` means `node <skill-dir>/scripts/t3-run.mjs`.

## Setup
"Node 22+ required" or `node: command not found`: tell the user and stop. "T3 Code server isn't running" or "Could not connect": ask the user to open the app, then retry. These errors apply to any `t3-run` command.

## Launch a task
1. **Project.** Run `t3-run --workspace <dir> --preflight`, where `<dir>` is the directory the user named, otherwise the current working directory. The script maps a subdirectory or git worktree to the project of the repository's main checkout and creates the project when T3 doesn't have one (`created` line). A `worktree` line means the thread will run in that worktree. Follow-ups use `--thread` and need no workspace.
2. **Mode.** Leave the default `--mode auto`. Switch to `--mode full-access` only with the user's approval, or to `--mode auto-accept-edits` or `approval-required` when the user wants tighter control.
3. **Run.** The script's defaults fix Claude Code, Opus 5.5 at high effort, so launch with exactly the options below. Write the task itself; the script prepends `/fusion `. Pass the prompt through a heredoc (or an equivalent stdin redirect on the user's shell), so quotes and newlines survive. Name absolute paths in the prompt; when the task should produce a file, add `--expect-file <absolute path>`.

```
node <skill-dir>/scripts/t3-run.mjs --workspace <dir> \
  --timeout 300 [--expect-file <absolute path>] --prompt-file - <<'PROMPT'
<task>
PROMPT
```

4. **Read the outcome.** The last line, `result {"threadId":…,"status":…,"exitCode":…}`, is the outcome. Act on `exitCode`:

   | exitCode | Meaning | Next |
   |---|---|---|
   | `0` | Run completed. T3's answer follows `--- assistant ---`; with `--expect-file`, the file's contents follow it. | Read the files the task touched, then report. |
   | `1` | Run failed, was interrupted, or the script hit a connection/RPC error. | Report the `error [...]` lines and the thread id. |
   | `2` | Usage error, or Opus 5.5 at high effort isn't available. | A usage error: fix the command from the printed message. A model or effort message: report it and stop. |
   | `3` | Waiting for the user: a permission request in the T3 Code app, or a held queue. | Tell the user what is waiting. Held queue: `--resume-queue`. Request: the user answers it in the app (or approves a relaunch with `--mode full-access`), then watch. |
   | `4` | Still running past `--timeout`; fusion runs are long, so expect several rounds. | Watch: `t3-run --thread <threadId> --timeout 300`, until the exit code is not `4`. |
   | `5` | Run completed, but the `--expect-file` is missing. | Report it with T3's answer. |
   | `6` | The fusion skill isn't installed; nothing launched. | Stop, and ask the user to install it. |

5. **Report.** Done when the user has the thread id, the final status, T3's answer, and the files produced or changed. Keep the thread id so a later turn can follow up.

## Follow up on a thread
All take `--thread <threadId>` and end on the same `result` line and exit codes.

- **Send a follow-up:** `--prompt-file -` with a heredoc, holding just the message; the thread already runs under fusion. It queues behind an active run, or starts at once when the thread is idle.
- **Redirect the active run:** add `--steer`. A provider that can't steer exits `1`; send it again without `--steer` to queue it.
- **Stop:** `--interrupt`, only when the user asks. It stops the active run and holds the queue; `0` means the run ended, or nothing was running.
- **Release a held queue:** `--resume-queue`.
- **Check on it:** `--thread <threadId>` alone watches the latest run; `0` also covers a thread with no runs.

## Approval boundaries
Confirm with the user before sending T3 a task that deletes, force-pushes, deploys, publishes, or touches production systems.

## Beyond the script
When the script can't do what's needed, read [`references/protocol.md`](references/protocol.md) for the WebSocket API. Set `DEBUG=1` on the script to print raw frames.
