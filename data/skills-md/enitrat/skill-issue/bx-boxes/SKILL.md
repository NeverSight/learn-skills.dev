---
name: bx-boxes
description: Run work on short-lived Boat sandboxes with the `bx` CLI and steer it with herdr. Use when a task needs a clean Linux machine, more parallelism than this Mac allows, or isolation between runs (evals, test shards, agent trials that share /tmp, ports or a browser), or when the user says box, Boat, sandbox, spawn a machine or run it remotely.
---

# Boxes with bx

`bx` starts Boat sandboxes ("boxes") from saved snapshots and saves each one as a herdr machine
labelled with the box name. `bx --help` and `herdr --skill` are the references. This skill is
the procedure. To move the current Claude Code session itself to a box, use `bx-teleport`.

## 1. Pick the snapshot

Run `bx list`. It prints each snapshot and the repos baked into it.

```
Is the repo you need in a snapshot's REPOS column?
├── Yes → that snapshot. The repo is at ~/<snapshot>/<repo>, deps installed, at the bake's commit.
└── No  → dev, then clone the repo on the box with `gh repo clone`.
```

A snapshot saves the clone and `pnpm install` (about a minute per box). Never bake a new
snapshot for a one-off task: a bake takes 15 minutes.

## 2. Get your code onto the box

The baked repo is at the bake's `main`, not your branch.

```
Is your branch pushed?
├── No  → boat push <id> <local-repo> --to /home/user/work/<repo>
└── Yes → on the box: git -C ~/<snapshot>/<repo> fetch origin <branch> && git checkout FETCH_HEAD
          Uncommitted local changes on top of it?
          └── Yes → ship them as a patch (below), applied after the checkout
```

```bash
# On the Mac: the whole working tree against HEAD, untracked files included, index untouched.
cp .git/index /tmp/idx && GIT_INDEX_FILE=/tmp/idx git add -A \
  && GIT_INDEX_FILE=/tmp/idx git diff --cached --binary HEAD > work.patch; rm /tmp/idx
boat scp work.patch <id>:/home/user/work.patch
# On the box, after the checkout:
git apply --binary ~/work.patch
```

The patch never commits or pushes the user's work, and a deletion in the working tree is a
deletion on the box. Do not commit or push just to reach a box unless the user asked.

Then run `pnpm install --frozen-lockfile --prefer-offline` in that directory. It takes
seconds because the snapshot's pnpm store holds the packages. Never `--offline` for this first
install: pnpm fetches the version a repo pins into `~/.cache`, which Boat does not keep.

Prefer the git branch: `boat push` copies files but never deletes one, so pushing over the
baked checkout leaves files your branch removed. That is why it goes to a fresh directory.

## 3. Split the work across boxes

One box per shard, never one per trial. A box takes 70 to 100 s to be ready (it waits for its
disk to restore, then checks nix, gh, git and pnpm), so short trials on their own boxes spend
most of their time starting.

- Shards = the number of independent pieces you can run in parallel. Each shard runs its
  pieces one after another, inside its box.
- At most 30 new boxes per minute (the account's start limit). Up to 300 can run at once.
- Names: lowercase letters, digits and `-` only, unique, `<task>-<n>`. The name is the herdr
  machine label you steer the box by, so a space or a stray suffix makes every later command
  awkward. Write each name out; never build it by splitting a string, because zsh does not
  word-split `$var` and `set -- $spec` puts the whole string in `$1`.
- Size: `bx new` starts `large` boxes (8 vCPU, 16 GB): a stack plus a browser plus an agent
  saturates `default` (4 vCPU, 8 GB, half the rate). Pass `--type default` only for light
  work such as a test shard with no browser.

```bash
for name in eval-1 eval-2 eval-3 eval-4; do bx new --snapshot zama --name "$name" > "/tmp/$name.id" & done; wait
```

`bx new` prints the box id last. It exits non-zero when a check failed. Delete that box
and create it again.

## 4. Run and steer through herdr

The box's shell has every tool, Claude Code logged in, `gh` logged in, and your git identity.
Each box runs its own herdr server with one shell pane, `w1:p1`. Address it from the Mac with
`herdr --machine <box-name> …`. Read pane IDs from `herdr --machine <box-name> pane list`
instead of assuming them.

```
What runs on the box?
├── A check under a minute (git, ls, a dry run)       → ssh <id> '<cmd>'
├── A long command (eval runner, test shard, build)   → a herdr pane
└── An agent you will prompt, watch or answer         → a herdr agent
```

Long work goes in herdr, not `ssh … nohup`: the user sees it in the herdr TUI, you read its
output and wait on it with one command, and a dropped SSH connection does not kill it.

**A long command:**

```bash
herdr --machine <box> pane run w1:p1 "cd ~/<snapshot>/<repo> && <cmd>; echo EXIT=\$?"
herdr --machine <box> pane wait-output w1:p1 --regex 'EXIT=\d+' --timeout 3600000
herdr --machine <box> pane read w1:p1 --source recent-unwrapped --lines 200
```

Always `cd` to an absolute path first: a restored box's pane starts in a stale directory.

Check herdr on every box before relying on it: `herdr --machine <box> pane list`. Right after
`bx new` the first call can be refused for a few seconds; retry. A herdr server started while
Boat restores the disk (after `boat resume`, the Mac's herdr may reconnect and start one)
listens on a socket the restore then removes, and `--machine` fails with `ConnectionRefused`
for good. Forwarding never starts or repairs a server. Nothing survives a resume, so a fresh
server loses nothing: once `boat info <id>` says `"hydrated": true`, stop the old one and
re-add the machine, which starts a new one:

```bash
ssh <id> 'pkill -x herdr'   # -x matches the process name, not this shell's command line
herdr machine remove "$(herdr machine list --json | jq -r '.[] | select(.label == "<box>") | .id')"
herdr machine add <id> --label <box>
```

If herdr still does not answer, detach over SSH instead, so a dropped connection does not kill
the run, and poll for the exit file:

```bash
ssh <id> 'cd <dir> && nohup sh -c "<cmd> > ~/run.log 2>&1; echo \$? > ~/run.exit" >/dev/null 2>&1 &'
ssh <id> cat ~/run.exit   # repeat until it exists; ~/run.log has the output
```

**An agent:**

```bash
herdr --machine <box> pane run w1:p1 "cd ~/<snapshot>/<repo>"
herdr --machine <box> agent start <agent-name> --kind claude --pane w1:p1
herdr --machine <box> agent prompt <agent-name> "<task>" --wait --timeout 1800000
herdr --machine <box> agent read <agent-name> --source recent-unwrapped --lines 200
```

- The first Claude start in a repo on a fresh box stops at the folder-trust dialog:
  `agent start` returns `agent_not_ready` and `agent prompt` returns `agent_blocked`. Read it
  with `agent read`, then ask the user before answering it. Any dialog that blocks an agent is
  the user's decision, never yours.
- Read the agent's reply before it exits. Claude draws in the terminal's alternate screen, so
  after `/exit` its output is gone from the pane's scrollback.
- One agent per pane. A second agent or command on the same box gets its own pane:
  `herdr --machine <box> pane split w1:p1 --direction right --no-focus`.

On every box, give each agent or trial its own `LAB_PORT` (or equivalent), `TMPDIR`,
agent-browser `--session` and `pnpm cli` `--as` lease. One box isolates shards from each other,
not processes inside a box from each other.

On the first box only, check the assumptions your run makes before starting every shard: a
5-second command that exercises the same tools (a dry run, a check mode, one tiny trial).
Fixing a wrong assumption costs one box, not twenty.

A box under load answers SSH and herdr slowly. Next, Chrome and an agent together fill 8 GB,
and Boat's own background snapshot (`ascii-capture` in `ps`) adds a load spike. A
`boat-resolve … Request timeout` while `boat info <id>` says `"health":"ok"` means busy, not
dead: retry before deleting anything.

## 5. Bring results back, then delete

Pack results on the box, leaving checkouts and `node_modules` behind, then copy the archive:

```bash
ssh <id> 'tar czf ~/results.tgz -C ~ --exclude="*/node_modules" --exclude="*/work" <results-dir>'
boat scp <id>:/home/user/results.tgz ./results/<task>-<n>.tgz
bx rm <task>-<n>
```

Always `bx rm`, failed runs included: wrap the run in `trap 'bx rm <name>' EXIT`. It deletes
the box and its herdr machine. A box left alone runs, and bills, until its 4-hour auto-stop.
`bx gc` offers to delete boxes stopped for more than 3 days.

Never `boat snapshot` a task box. It holds your gh and Claude logins, and a saved snapshot
keeps them forever.

## Example: the ds eval in super-app

`tools/ds-eval/eval.ts` runs agent trials, each with its own checkout, Lab port, `TMPDIR` and
browser session. A run evaluates the working tree as it is; `merge` joins runs from several
boxes and `compare` sets two runs side by side.

1. Snapshot `zama`. Code: the branch fetched, plus a patch of local changes (section 2).
2. Shards: one box per task and condition (for example full guidance vs guidance removed),
   `--concurrency 1`, on `large` boxes (the `bx new` default). One trial runs Next, Chrome and an agent at
   once; on the default 4 vCPU, 8 GB box that pushed load past 50, stalled SSH for minutes and
   made trials slower than the shards on lighter tasks.
3. On box 1 first: `bun tools/ds-eval/eval.ts check`, a dry `run`, and one throwaway checkout.
   The first per-trial `pnpm install --offline` on a fresh box can fail once; a throwaway
   checkout before the run warms it.
4. Each box, in its herdr pane: `run --tasks <task> --k <k> --model <m> --yes --out ~/ds-eval-out/<condition>`,
   then `verify` and `capture` there, because the verifier needs the run's snapshot and the
   trials' checkouts. Say the cost from the dry run before passing `--yes`.
5. Pack each run without `work/`, `verify/`, `snapshot/` and `verification-baseline/`, copy it
   back, `merge` the boxes of one condition into one run, then `compare` the conditions.
