---
name: tmux-ssh-workflow
description: Reuse authenticated SSH or container shells in existing local tmux sessions to run remote commands, transfer files with chunked downloads and whole-file SHA256 verification, manage long-running jobs, and coordinate container restarts across sessions. Use when the user provides a tmux socket and session names for remote work or artifact collection. Does not create SSH connections or work without a local tmux channel. Runs natively on macOS/Linux and through WSL on Windows.
---

# tmux SSH Workflow

Use existing local tmux sessions as remote control channels when they already contain authenticated SSH or container shells.

## Core model

```text
Local tmux socket → tmux sessions (one or more) → authenticated remote shell → remote jobs
```

Only two inputs are needed: `--socket` and session names. Do not require or accept host, user, port, jump-host, or pane-mapping configuration.

Four rules must always hold:

1. **Rediscover the active pane on every operation.** A pane is a tmux terminal area; container restarts or SSH reconnects can invalidate a previously discovered pane.
2. **A timeout does not mean failure.** It only means the receipt has not appeared yet. The operation may still be running; inspect its state before considering a retry. Never resend automatically.
3. **Job state lives in remote files, not tmux scrollback.** Another local process can take over after the original driver exits.
4. **Stop only the remote job.** Never run `tmux kill-session`, `kill-window`, or `kill-pane`. Preserve sessions for investigation.

## macOS / Linux

The local machine needs Python 3.10+, tmux, and access to the socket; scripts run natively. The remote environment needs Python 3.8+, bash, base64, and stty; long-running job management also requires `ps`. Quote complete arguments when local paths on macOS or remote job paths contain spaces.

## Windows

Run only inside WSL (Windows Subsystem for Linux). The tmux socket and its SSH/container sessions must also live in WSL. Native Windows Python cannot access a WSL socket; scripts exit immediately with a suggested `wsl` command.

- **Agent running on Windows:** Prefer PowerShell with `wsl -d <distribution> -e python3 "/mnt/c/<skill-path>/scripts/X.py" ...`. Use the distribution and user that created tmux; add `-u <user>` if needed. With Git Bash, prefix the command with `MSYS_NO_PATHCONV=1` to prevent arguments such as `/tmp/x` from becoming `C:/...`. Scripts reject rewritten socket and remote paths.
- **Claude Code running inside WSL:** Use the Linux commands below directly, without `wsl -e`.
- **Paths:** Local file arguments (`--source`, `--dest`, `--python-file`, `--plan`) accept `C:\...` and automatically convert it to `/mnt/c/...`. Remote paths must use POSIX syntax.
- **Timeouts:** Allow enough time for large transfers within the current agent tool's actual timeout limits. If a call is interrupted, inspect the pane read-only first. If it is stuck in a transfer read loop, confirm that interruption is appropriate, use Ctrl-C to exit it, and then recover the session as described below.

## Standard workflow

Follow this sequence unless there is a clear reason to skip a step.

1. Use `session_preflight.py` to confirm the session is available, the remote shell is in the expected environment, and required commands exist.
   Add `--expect-in-container` when the session should already be inside a container, such as a persistent `docker exec -it <ctr> bash`. This rejects a pane that has fallen back to the host shell after a container restart.
2. Upload code or input data with `transfer.py put`.
3. Use `tmux_exec.py` for preparation such as unpacking files and checking dependencies.
4. Launch a long-running job with `remote_job.py launch` and record its `pid` and `pgid` (process and process-group IDs).
5. Poll with `remote_job.py status` until the state becomes `SUCCEEDED` or `FAILED`.
6. Package results remotely with `remote_job.py collect`, then retrieve and verify them with `transfer.py get`.
7. Use `remote_job.py stop` when the job must be stopped.

Use `batch_sessions.py` when multiple machines need the same sequence of dependent actions.

## Script usage

All scripts output JSON and return exit code 0 on success. `--sessions` accepts comma-separated session names. Different sessions run in parallel; operations within a session run sequentially.

**Preflight**

```bash
python3 scripts/session_preflight.py --socket /path/to/sock --sessions n1,n2 \
  --expect-cwd-prefix /workspace --require-command python3
```

**Execute commands**

```bash
python3 scripts/tmux_exec.py --socket S --sessions n1,n2 --command 'nvidia-smi -L' --show-output
python3 scripts/tmux_exec.py --socket S --sessions n1 --python-file body.py
```

`--python-file` contains a function body that must end with `return`; its result must be JSON-serializable. Use this for structured checks rather than parsing human-readable output.

**Transfer files**

```bash
python3 scripts/transfer.py put --socket S --sessions n1,n2 \
  --source ./bundle.zip --remote-path /remote/dir/bundle.zip --compress
python3 scripts/transfer.py get --socket S --session n1 \
  --remote-path /remote/dir/result.tar.gz --dest ./returns/result.tar.gz
```

Package directories locally into a single archive first. Add `--compress` for text and highly compressible content. Downloads from multiple sessions automatically prefix local filenames with the session name to avoid collisions. Overwriting an existing file requires explicit `--overwrite`.

**Remote jobs**

```bash
python3 scripts/remote_job.py launch --socket S --sessions n1 --job-id run-001 \
  --job-root /remote/state/jobs --command './train.sh' --cwd /remote/project
python3 scripts/remote_job.py status  --socket S --sessions n1 --job-id run-001 --job-root /remote/state/jobs
python3 scripts/remote_job.py stop    --socket S --sessions n1 --job-id run-001 --job-root /remote/state/jobs
python3 scripts/remote_job.py collect --socket S --sessions n1 --job-id run-001 --job-root /remote/state/jobs
```

States are `RUNNING`, `SUCCEEDED`, `FAILED`, `LOST`, and `MISSING`. `LOST` means the process is gone but no exit code is available, usually because it was killed externally or the machine restarted. Inspect logs before rerunning.

**When the pane is already inside a container**, such as a persistent `docker exec -it <ctr> bash`, call `remote_job.py` directly **without** `--container`. Keep the shell inside the container. The job runs as an ordinary shell job there, with the usual `status` and `stop` commands. The container needs bash, Python 3.8+, and procps `ps` (BusyBox `ps` is unsupported). If the container may be recreated, place `--job-root` on a persistent mounted directory.

Use `--container` only when the pane is on the host and jobs need to start or stop inside a container. Invoke `launch --container NAME` from the **host shell**: the script starts the command through the container runtime's `exec`. `--cwd` is a container directory; `--job-root` is a host state directory. Invoke subsequent `status`, `stop`, and `collect` from the host as well. `stop` stops the container using the ID and runtime recorded at launch, then confirms the host process group has exited. Older jobs that record only a container name cannot be stopped automatically; inspect them from the host before taking action.

**Multi-session orchestration**

```bash
python3 scripts/batch_sessions.py --socket S --plan plan.json --dry-run
python3 scripts/batch_sessions.py --socket S --plan plan.json
```

Each plan step declares its expected outcome:

- `marker`: An ordinary command whose `rc` must be in `allow_rc` (default `[0]`).
- `disconnect`: The shell is expected to disappear, such as when exiting a container or restarting. Never resend commands to a dead shell.
- `ready`: Run `ready_command` repeatedly until it succeeds to confirm availability after reentry.
- `json`: Run a Python function body and retain structured results.

See [references/plan-examples.md](references/plan-examples.md) for a standard container restart plan.

## Decisions and tradeoffs

**Chunk size.** The default is 3 MiB. Smaller chunks expose problems sooner on slow links or low-throughput PTYs (pseudoterminals, the terminal channels used by tmux). Larger chunks reduce round trips for large files. Adjust using the reported `throughput_mib_s` rather than intuition.

**Compression.** Use `--compress` for source code, logs, and JSON. Skip it for already compressed archives, images, and model weights; recompression wastes CPU.

**After a failure.** A timeout or terminated driver leaves an unfinished-operation marker, and later scripts refuse further writes. Inspect the pane read-only with `tmux -S SOCK capture-pane -p -t SESSION` and confirm the shell is idle. If necessary, exit the specific read loop or interactive program. Then explicitly recover and check the session:

```bash
python3 scripts/tmux_exec.py --socket SOCK --sessions SESSION \
  --recover-session --command 'stty echo; pwd' --show-output
```

`--recover-session` confirms that the pane has been inspected and the shell is idle. It does not automatically stop jobs or resend old commands. After recovery, inspect processes, files, and logs before deciding whether to retry. Uploads are verified in staging files before an atomic rename.

**Downloads and terminal logging.** Downloads need exclusive access to the pane's output pipe. If a `pipe-pane` logging pipe already exists, the download is refused and that pipe is preserved. Use a pane without an output pipe, or change the existing logging setup only with explicit authorization.

**Concurrency boundary.** Two drivers using one session can interleave and corrupt receipts. A separate file lock protects each `socket + session` pair. On a lock timeout, investigate the owner rather than bypassing the lock.

Read additional details as needed:

- Transfer protocol and failure handling: [references/transfer-protocol.md](references/transfer-protocol.md)
- Orchestration plan examples: [references/plan-examples.md](references/plan-examples.md)
- Common failures and troubleshooting: [references/troubleshooting.md](references/troubleshooting.md)
