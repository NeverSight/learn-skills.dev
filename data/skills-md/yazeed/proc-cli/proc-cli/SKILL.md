---
name: proc-cli
description: |
  Find, inspect and control processes and ports with the proc CLI (macOS, Linux, Windows), with JSON output for agents. Use it instead of lsof, ps, pgrep, pkill, kill, netstat, pstree or top whenever you need to: see what is on a port or free it (EADDRINUSE, "address already in use", a dev server that won't start); find processes by name, PID, file or project directory; inspect a process (command, cwd, parent, uptime, CPU, memory); stop, kill, pause, resume or wait for processes; trace why a port is busy; find orphaned, stuck or leftover processes, such as dev servers, watchers and headless browsers that you or another agent started; or clean up background work before finishing a task. Also use when the user mentions proc, ports, PIDs, signals (SIGTERM, SIGKILL, SIGSTOP) or a slow machine.
---

# proc CLI — Process Management Tool

proc is a semantic CLI for processes and ports on macOS, Linux, and Windows. You target processes by port (`:3000`), PID, name, file or directory, and every command can return a single JSON document.

## Before You Start

- Check it's installed: `proc --version`. This skill describes proc 1.14.5 (`proc inspect` and `uptime_secs` need 1.14 or later).
- If it's missing, ask the user before installing. Options: `brew install yazeed/proc/proc` (macOS), `cargo install proc-cli`, `npm install -g proc-cli`, `scoop bucket add proc https://github.com/yazeed/scoop-bucket-proc && scoop install proc` (Windows), or `nix profile install github:yazeed/proc`.

## Critical Rules

1. **Always pass `--json`** on every command for structured output
2. **Always pass `--yes`** on destructive commands to skip interactive prompts
3. **Use `--dry-run`** before destructive actions to preview what would happen
4. **Check the exit code**: 0=success, 1=general error (including partial failures and `wait` timeouts), 2=not found, 3=permission denied, 4=invalid input. `"success": false` always comes with a non-zero exit code
5. **Errors with `--json`** produce `{"action":"<cmd>", "success":false, "error":"...", "exit_code":N}` on stdout — including invalid flags or arguments
6. **Every JSON response** is a single document (except the `watch` stream) with `action` (the command name, aliases resolved) and `success` fields
7. **Only touch processes you started or the user named.** Prefer port and PID targets; scope name targets with `--in <dir>` or `--by <name>`
8. **Exit 3 means you need elevated rights.** Ask the user before retrying with `sudo`

## Use proc Instead Of

| Instead of | Use |
|------------|-----|
| `lsof -i :3000`, `netstat -tlnp`, `ss -tlnp` | `proc on :3000 --json`, `proc ports --json` |
| `lsof -ti :3000 \| xargs kill -9` | `proc free :3000 --yes --json` (kills, then verifies the port is free) |
| `ps aux \| grep node`, `pgrep -f node` | `proc by node --json`, or several patterns: `proc list 'node,vite' --json` |
| `pkill -f pattern` | `proc kill pattern --in . --dry-run --json`, then the same with `--yes` |
| `kill PID`, `kill -9 PID` | `proc stop PID --yes --json`, `proc kill PID --yes --json` |
| `kill -STOP` / `kill -CONT` | `proc freeze` / `proc thaw` |
| `while kill -0 $PID; do sleep 1; done` | `proc wait PID --timeout 60 --json` |
| `lsof /path/to/file` | `proc for /path/to/file --json` |
| `pstree`, `ps -o ppid=` | `proc tree PID --json`, `proc why PID --json` |
| `top`, `ps aux --sort=-%cpu` | `proc list --sort cpu --limit 10 --json` |

## Target Syntax

Most commands accept the same target format:

- `:3000` — process listening on port 3000
- `1234` — process with PID 1234
- `node` — processes matching name "node" (substring match on name and command line)
- `:3000,:8080,node` — comma-separated multiple targets, deduplicated by PID

Exceptions: `proc free` takes ports only, `proc for` takes a file path, `proc in` takes a directory.

Aliases you may see users type: `:` (on), `f` (for), `b` (by), `l`/`ps` (list), `i`/`inspect` (info), `p` (ports), `k` (kill), `s` (stop), `t` (tree), `w`/`top` (watch), `x` (stuck), `u` (unstick), `o` (orphans). JSON `action` always uses the full name.

## Commands

### Discovery (read-only, no --yes needed)

```bash
proc on :3000 --json              # what process is on port 3000?
proc on 1234 --json               # what ports does PID 1234 use?
proc on node --json               # what ports are node processes using?
proc for ./server.py --json       # what's running (or holding open) this file?
proc by node --json               # find processes by name
proc by node --in . --json        # ...started from the current directory
proc in . --json                  # all processes whose cwd is under this directory
proc in ~/project --by node --json
proc list --json                  # all processes
proc list --min-cpu 10 --json     # processes using >10% CPU
proc list --status stopped --json # frozen/stopped processes
proc list --path /usr/local/bin --json  # filter by executable path
proc info :3000,1234 --json       # inspect one or more targets: full details
proc ports --json                 # all listening ports
proc ports --exposed --json       # only ports bound to 0.0.0.0 / ::
proc ports --local --json         # only ports bound to 127.0.0.1 / ::1
proc ports --range 3000-3999 --json
proc why :3000 --json             # trace ancestry — why is this port busy?
proc tree node --json             # descendants of node processes
proc tree 1234 --ancestors --json # path from the top ancestor down to PID 1234
proc orphans --in . --json        # processes whose parent died (reparented to PID 1)
proc stuck --json                 # processes >50% CPU running longer than --timeout (default 300s)
```

To inspect a process, use `proc info` (aliases: `inspect`, `i`; JSON `action` is always `"info"`). For each target it reports the name, PID, command line, executable path, working directory, user, parent PID, status, CPU, memory, start time and uptime. `list`, `by` and `in` return the same process fields for many processes at once.

### Lifecycle (destructive — always use --yes --json)

```bash
proc kill :3000 --yes --json               # force kill (SIGKILL)
proc kill node --in . --graceful --yes --json  # SIGTERM instead of SIGKILL
proc stop node --yes --json                # SIGTERM, then SIGKILL after --timeout (default 10s)
proc stop nginx --signal HUP --yes --json  # send a different initial signal
proc freeze node --yes --json              # pause (SIGSTOP)
proc thaw node --yes --json                # resume (SIGCONT)
proc free :3000 --yes --json               # kill + verify port is free (--wait, default 10s)
proc free :3000,:8080 --yes --json         # free multiple ports
proc unstick 1234 --yes --json             # SIGCONT then SIGINT; no kill
proc unstick 1234 --force --yes --json     # ...then SIGTERM, SIGKILL if still stuck
proc orphans --in . --kill --yes --json    # kill orphans whose cwd is under this directory
```

### Monitoring

```bash
proc wait node --timeout 60 --json       # block until all node processes exit (max 60s)
proc wait :3000 -n 1 -q --timeout 30 --json  # poll every 1s, quiet
timeout 10 proc watch node --json        # NDJSON stream, one object per refresh (-n seconds)
```

## Playbooks

### A port is busy (EADDRINUSE, "address already in use")

```bash
proc on :3000 --json        # who holds it? check name, cwd and command
proc why :3000 --json       # what started it (ancestry)
proc free :3000 --yes --json  # only if it's yours or the user agreed
```

If the holder is the user's own app, another project, or another agent's server, ask before freeing it, or start yours on a different port.

### Run a server or job in the background, then clean it up

- Note its port or PID when you start it. Stop it by that target: `proc stop :4789 --yes --json` or `proc kill 12345 --yes --json`.
- Don't stop it with a name pattern copied from the command you typed. The real command line often differs (`bunx serve` runs as `node …/serve`), so the pattern can silently match nothing.
- `kill` and `stop` signal only the processes you target, not their children. Killing `npm run dev` can leave its `node` or `ts-node` child running. Check `proc tree PID --json` and target the children too, or stop by port.
- Confirm it's gone: `proc on :4789 --json` exits 2 when nothing is listening.

### Before finishing a task, check for leftovers

```bash
proc ports --in <project-dir> --json      # servers you left listening
proc orphans --in <project-dir> --json    # processes whose parent already exited
proc list 'headless,ms-playwright,puppeteer' --json   # headless browsers
```

`--in` matches the process's working directory, so pass the directory the process ran in (where you `cd`'d), which may not be your own cwd. Before stopping a leftover, check `proc why PID --json`. If its ancestry leads to another agent session, an editor or the user's terminal, it isn't yours: report it instead of killing it.

### The machine is slow

```bash
proc list --sort cpu --limit 10 --json
proc list --min-mem 1000 --sort mem --json   # over 1 GB
proc stuck --json                             # >50% CPU now, running > 5 min
```

Report what you find with each process's `cwd`, `uptime_secs` and `parent_pid`, and let the user decide what to stop.

### Restart something cleanly

```bash
proc stop :3000 --yes --json   # SIGTERM, SIGKILL after 10s
proc on :3000 --json           # exit 2 = nothing listening; safe to start again
```

`proc free :3000 --yes --json` does both in one step: SIGTERM, SIGKILL after at most 5 seconds, then it checks the port was released. Use `proc wait` for processes you expect to exit on their own: with no matching process it exits 2 straight away.

## Safety

- Name targets match every process proc can see whose name or command line contains the pattern: other projects, editors, the user's terminals, and other agents' MCP servers and browsers. Always `--dry-run` a name target first, and scope it with `--in`.
- proc never matches its own process or its parent chain (up to 10 levels) by name, so `proc by claude` run from inside an agent leaves out that agent. PID and port targets are not protected.
- Don't use `kill` (SIGKILL) as a first resort. Prefer `stop`, which gives the process time to clean up.

## Filters

Not every command takes every filter — check `proc <cmd> --help`.

| Filter | Commands |
|--------|----------|
| `--in [dir]` (`-i`, defaults to `.`) | all except `why`, `free`, `in` |
| `--by <name>` (`-b`) | all except `why`, `free`, `by` and `list` (those two take the name as an argument) |
| `--min-cpu <pct>`, `--min-mem <MB>` | `list`, `by`, `in`, `for`, `tree`, `watch` |
| `--status <s>` (running, sleeping, stopped, zombie) | `list`, `by`, `in`, `for`, `tree` |
| `--min-uptime <secs>` | `list`, `by`, `in`, `for`, `tree` |
| `--parent <pid>` | `list`, `by`, `in` |
| `--path <path>` (`-p`, executable path) | `list` |
| `--sort <key>` (cpu, mem, pid, name) | `list`, `by`, `in`, `for`, `watch` |
| `--sort <key>` (port, pid, name) | `ports` |
| `--limit <n>` (`-n`; `-l` on `watch`) | `list`, `by`, `in`, `for`, `ports`, `watch` |
| `--depth <n>` (`-d`, default 10), `--compact` (`-C`, PIDs only) | `tree` |

## Output Schemas

For complete JSON output schemas and field definitions, see [reference.md](reference.md). The fields you'll use most on a process: `pid`, `name`, `command`, `cwd`, `parent_pid`, `user`, `status`, `cpu_percent`, `memory_mb`, `start_time`, `uptime_secs`.

## Agent/Pipe Readiness

- **One-shot queries**: `on`, `for`, `by`, `in`, `list`, `info`, `ports`, `why`, `tree`, `orphans`, `stuck` — return immediately
- **Blocking**: `proc wait` — always pass `--timeout`
- **Streaming**: `proc watch --json` — NDJSON forever; bound it with `timeout N` or `| head -n N`. Without `--json` and without a TTY it prints one snapshot. Prefer `proc list` for a single snapshot
- **Destructive**: `kill`, `stop`, `freeze`, `thaw`, `free`, `unstick`, and `orphans`/`stuck` with `--kill` — always pass `--yes --json`
- **Showing results to the user**: run without `--json` for a readable table (an `UPTIME` column appears on terminals 100+ columns wide)

## Gotchas

- Port targets must start with `:` — `proc on 3000` looks up PID 3000, not port 3000.
- `proc free` only accepts port targets (`:3000`). Use `proc kill` for name/PID targets.
- Name matching is substring-based: `proc by node` matches "node", "nodejs", "nodemon". Narrow with `--in` or use PIDs.
- `proc by` takes one pattern; `proc list` takes several, comma-separated: `proc list 'git commit,pre-commit' --json`. Patterns are plain case-insensitive substrings matched against the name and the full command line, not regular expressions.
- Uptime is `uptime_secs` in the JSON (seconds), on every process in every command (since 1.14.5 also in `tree`, `why` and `unstick`). `start_time` is a Unix timestamp, not a duration. In human output, process tables show an UPTIME column on terminals 100+ columns wide, and `tree` and `why` show `up 3m 12s` on each line.
- Processes can keep running in a directory that was deleted (a removed worktree, say), and they're often the leftovers you're looking for. From proc 1.14.1, `proc in <dir>` lists them and `cwd` shows the plain path. In 1.14.0 and earlier, `proc in <dir>` rejects a deleted directory with exit 4, so use `proc list --in <dir>` or `proc orphans --in <dir>` there (on macOS; on Linux those versions miss them, because the kernel reports their cwd as `<dir> (deleted)`).
- `--dry-run --json` prints `"dry_run": true` plus the `processes` that would be affected; nothing is changed.
- `proc orphans --kill` and `proc stuck --kill` report like `proc kill` (`succeeded`/`failed`), with `action` `"orphans"`/`"stuck"`.
- If any process fails in `kill`/`stop`/`freeze`/`thaw`/`orphans --kill`/`stuck --kill`, the exit code is 1 and `failed` lists why; the ones in `succeeded` were still acted on.
- `proc wait` on timeout prints its result with `timed_out: true` and exits 1.
- `--signal` is only on `proc stop`. Valid signals: HUP, INT, QUIT, ABRT, KILL, TERM, STOP, CONT, USR1, USR2 (with or without `SIG`, any case). Windows has no signals, so there `--signal` exits 4.
- `--graceful` is only on `proc kill`.
- Unknown flags exit 4; with `--json` the error is a JSON object on stdout, otherwise plain text on stderr.
- `freeze` and `thaw` are Unix only — on Windows they fail with exit 1.
- `proc stuck` is a heuristic (sustained high CPU), not a hang detector.
- An orphan (parent PID 1) isn't necessarily abandoned: daemons and `tmux`/`nohup` jobs are orphaned on purpose. Check `cwd`, `command` and uptime before treating one as a leftover.
