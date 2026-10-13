---
name: dicos-cli
description: "Operator guide for the installed dicos CLI: run Slurm CPU/GPU jobs on ASGC DiCOS (slurm-ui.twgrid.org) from a laptop through one 2FA SSH master. Covers install/update, first-run setup (dicos init, doctor), config.yaml, the status/run/sweep/list/show/logs/wait/stop/clean/ssh/exec/code/logout commands, git vs --sync code shipping, job states, login-ban safety, and troubleshooting. Use when submitting, monitoring, stopping or cleaning DiCOS jobs, choosing a partition or GPU count, or diagnosing failed logins, stuck queued jobs, failed submissions or lost jobs — not when developing the dicos repo itself."
---

# dicos CLI Operator Guide

`dicos` submits jobs to the ASGC DiCOS Slurm cluster from a laptop. One SSH ControlMaster (`~/.dicos/cm.sock`, 8 h) performs the password + TOTP login; every other command reuses it. Code is shipped either as a pushed git commit (default) or by rsyncing the working tree (`--sync`). Jobs are tracked in a local SQLite database (`~/.dicos/dicos.db`).

## 1. Safety rules (read first)

**Agents: read [references/authentication.md](references/authentication.md) before the first remote command.** It defines what the user must do themselves, what needs their go-ahead, and what to tell them.

1. **Never retry logins in a loop.** More than 5 failed logins ban the source IP, which is the shared lab jump host. dicos itself never retries.
2. **Secrets stay with the user.** Never ask for, accept, or type the password, TOTP secret, or QR export, and never read `~/.dicos/credentials.json`. `dicos init` is run by the user in their own terminal.
3. **Any remote command may log in.** When the SSH master has expired, `status`, `run`, `list`, `doctor`, etc. perform one automated login. Check first without logging in: `ssh -o ControlPath=~/.dicos/cm.sock -O check x`.
4. **A failed login is latched** in `~/.dicos/login.failed`; every remote command then refuses to log in. Report the reason to the user and let them fix the cause. Run `dicos logout` (one new attempt) or ask them to run `dicos init --force` only after they agree.
5. `dicos run` exiting 0 means **submitted (queued)**, not finished. Use `dicos wait`.
6. GPUs are released by Slurm when the job ends. Keep `-t` tight; use `dicos stop ID` to end a job early. `dicos clean` only deletes files.

## 2. Setup

```bash
uv tool install git+https://github.com/novis10813/dicos   # install
dicos update                                               # upgrade later
dicos init                                                 # interactive wizard, run by the user
dicos doctor                                               # verify; exit 1 if any row fails
dicos status                                               # partitions your account may use
```

`init` asks for username, TOTP (base32 secret, `otpauth://` URI, Google Authenticator export URI, or a QR image path), and password; probes each `~/.ssh/config` Host alias as a jump host; prints the current TOTP for comparison; logs in; detects the remote workdir. Details: [references/setup.md](references/setup.md).

## 3. Procedures

### A. Single job (`dicos run`)

```bash
# Git mode (default): HEAD must be clean and pushed. The login node clones it.
dicos run -p a100-al9 --gpus 1 -t 6h -- uv run python train.py --lr 1e-4
dicos run -p a100-al9 --gpus 1 --branch exp -- uv run python train.py   # dirty tree allowed
dicos run -p a100-al9 --gpus 1 --tag v1.0 -- uv run python train.py
dicos run -p a100-al9 --gpus 1 --commit a1b2c3d -- uv run python train.py

# Sync mode: rsync the working tree (no commit or push needed, works outside git).
dicos run --sync -p edr1-al9_short_serial -t 10m -- python3 check.py

# Quick GPU check (a100_devel-al9 has a 20 min limit).
dicos run --sync -p a100_devel-al9 --gpus 1 -t 5m -- nvidia-smi

# Shell syntax: pass ONE quoted string.
dicos run --sync -p edr1-al9_short_serial -- 'python prep.py && python train.py --name "exp 1"'
```

Output: `<id> (slurm <n>) queued on <partition>`. Before the command, the job runs `uv sync` when `pyproject.toml` exists (uv is installed to `~/.local/bin` if missing). Details: [references/submission.md](references/submission.md).

### B. Parameter sweep (`dicos sweep`)

```yaml
# sweep.yaml (keep it outside the repo or commit it: an untracked file makes git mode "dirty")
command: uv run python train.py --lr {lr} --seed {seed}
grid:
  lr: ["1e-4", "5e-5"]
  seed: [1, 2, 3]
partition: a100-al9   # optional: partition, gpus, cpus, mem, time; CLI flags override
gpus: 1
time: 6h
```

```bash
dicos sweep sweep.yaml            # one Slurm array job, one local job ID per grid point
dicos sweep sweep.yaml --sync -t 30m
```

### C. Monitor

```bash
dicos list                 # latest 20 (refreshes queued/running jobs first); --all, -s failed
dicos show ID              # every field; adds Slurm Reason while queued
dicos logs ID              # last 200 lines; -n 50; -f to follow (Ctrl-C stops following only)
dicos wait ID --timeout 3600 --interval 30
dicos fetch ID out/ metrics.json   # copy outputs to ./ID/ (paths relative to the job's src/, or absolute); -o DIR
```

`wait` exit codes: `0` succeeded, `1` failed, `2` cancelled, `3` lost, `124` timeout. Remote/login errors also exit `1` with a message on stderr.

### D. Stop and clean

```bash
dicos stop ID              # scancel; marked cancelled immediately
dicos clean ID -y          # finished jobs only: delete the remote job directory
```

### E. Login node access

```bash
dicos ssh                              # interactive shell on the login node
dicos exec -- 'squeue -u $USER'        # one command, exit status passed through
dicos code                             # print the current TOTP
dicos logout                           # close the master (also clears a login latch)
```

## 4. Command reference

| Command | Purpose | Key flags |
|---|---|---|
| `init` | Create config, credentials, first login | `--user` `--jump ALIAS` \| `--no-jump` `--qr PATH` `--totp-secret-stdin` `--password-stdin` `--force` `--default-partition P` `--default-time T` |
| `doctor` | Check files/modes, jump, login, sinfo, account, workdir, GitHub | — |
| `status` | Partitions allowed for your account: GRES, idle/total nodes, time limit | `--all` (adds ALLOWED column) |
| `run` | Submit one job | `-p` `--gpus N` `--cpus N` `--mem 32G` `-t 6h` `--sync` `--branch`\|`--tag`\|`--commit` `-- CMD` |
| `sweep` | Submit one array job from a YAML grid | same as `run`, plus `FILE` |
| `list` | Refresh and list jobs | `-s STATUS` `--all` |
| `show` | Refresh and show one job | `ID` |
| `logs` | Tail the job log | `-n N` `-f` |
| `fetch` | Copy outputs to a local directory | `ID PATH...` `-o DEST` (default `./ID`) |
| `wait` | Block until terminal | `--timeout S` `--interval S` (default 15) |
| `stop` | Cancel a queued/running job | `ID` |
| `clean` | Remove a finished job's remote directory | `-y` |
| `ssh` / `exec` | Shell / command on the login node | `exec -- CMD` |
| `code` / `logout` | Print TOTP / close master | — |
| `update` | Reinstall from the git source | `--check` |
| `feedback` | Open a GitHub issue in novis10813/dicos via `gh` | `[TITLE]` `--body TEXT` |

## 5. Things that surprise people

1. **Partition names are not uniform**: `a100-al9`, `a100_short-al9`, `a100_long-al9`, `a100_devel-al9`, `v100-al9_short`, `b6000-al9_short`, `edr1-al9_short_serial` (CPU). Always confirm with `dicos status`; some partitions exclude your account.
2. **A partition is required** for every job: `-p`, a sweep `partition:` key, or `defaults.partition` in `~/.dicos/config.yaml` (asked by `dicos init`).
3. **Defaults** when nothing is set: `--gpus 0`, `--cpus 1`, `-t 1h`, no `--mem`. `--gpus N` becomes `--gres=gpu:N` (max 8 per node).
4. **Git mode ships the pushed commit**, never local edits. Untracked files count as dirty. Use `--sync` to test uncommitted work.
5. **Private GitHub repos** are cloned on the login node with your forwarded local ssh-agent: run `ssh-add` locally first.
6. **Remote `$HOME` is temporary NFS.** Write results under the workdir (`/ceph/work/<group>/<user>/dicos/...`) or another `/ceph/work` path. The job's cwd is `<workdir>/jobs/<id>/src`.
7. Inside jobs: `DICOS_JOB_ID`, `PYTHONUNBUFFERED=1`, `set -eo pipefail` (the first failing command ends the job as `failed`).

## 6. Troubleshooting (short)

| Symptom | Fix |
|---|---|
| `The previous login failed: ...` | Report the reason to the user. They fix credentials (`dicos init --force`) or the network; `dicos logout` once only after they agree. Never loop. |
| `Unknown host key. Run ... once manually` | Ask the user to run the printed `ssh -J ... user@slurm-ui.twgrid.org` command, verify the key, and Ctrl-C at the menu. |
| `working tree is dirty; commit first or use --sync` | Commit/stash, or `--sync`, or an explicit `--branch/--tag/--commit`. |
| `HEAD is not on any remote branch; push first` | `git push`. |
| `git checkout on the login node failed: ... Permission denied (publickey)` | `ssh-add` locally; check the key has repo access. |
| sbatch `Invalid account or account/partition combination` | Pick a partition from `dicos status`. |
| Job stays `queued` | `dicos show ID` → Reason (`Resources`, `Priority`, `QOS...`). Try another partition or fewer GPUs. |
| Job `lost` | Not in squeue or sacct anymore. Check `dicos logs ID`. |

Full guide: [references/troubleshooting.md](references/troubleshooting.md).

## 7. References

- [Authentication handoff](references/authentication.md) — agent/user split for login, latch handling, message templates.
- [Setup & utilities](references/setup.md) — install, init, doctor, update, login latch, ssh/exec/code/logout.
- [Submission](references/submission.md) — run and sweep, git vs sync, resources, time format, job script.
- [Monitoring & control](references/monitoring.md) — status, list, show, logs, wait, stop, clean, job states.
- [Configuration](references/configuration.md) — `~/.dicos` files, `config.yaml`, projects, remote layout, `sweep.yaml`.
- [Troubleshooting](references/troubleshooting.md) — error messages and recovery recipes.
