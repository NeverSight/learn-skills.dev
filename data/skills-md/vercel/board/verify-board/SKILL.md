---
name: verify-board
description: Prove board behavior from a fresh environment. Spins up a Vercel Sandbox (vercel-labs scope), installs this checkout (or a published board version from npm), runs a local board with `vb serve`, and drives the `vb` CLI against it, capturing a transcript and the board's files as evidence. Use to verify a CLI or board change end to end, reproduce a bug on a clean machine, or check what users get from npm.
---

# verify-board

The surface is the `vb` CLI against a local board (`vb serve`, `packages/board/src/cli/serve.ts`):
SQLite log and attachments under the project's `.board/`, a scheduler in its process, a local
issuer, `127.0.0.1:4100`, no sync.
Everything runs in a fresh Vercel Sandbox, so nothing on this machine (your `~/.config/board`,
your `BOARD_URL`, a global `vb`) leaks into the result. The inspector (`vb inspect --no-open`)
is a secondary surface; see [features/README.md](features/README.md).

All scripts live in `.claude/skills/verify-board/scripts/` and run from anywhere in the repo.
Set `V=.claude/skills/verify-board/scripts` below.

## Launch

```bash
V=.claude/skills/verify-board/scripts
S=$($V/up.sh)                     # this checkout, working tree included (uncommitted changes too)
S=$($V/up.sh --published 0.9.0)   # or: board from npm, exactly what users install
```

`up.sh` prints progress on stderr and the sandbox name (`verify-board-<UTC timestamp>-<4 hex>`, distinct across parallel runs) as its
last stdout line. It:

1. creates the sandbox: `npx --yes sandbox@4.8.1 create --scope vercel-labs --name <name> --timeout 45m --vcpus 4`
   (`VERIFY_TIMEOUT`, `VERIFY_VCPUS` override; the image is Node 24, user `ubuntu`, home `/vercel`);
2. source mode: tars the working tree (`git ls-files --cached --others --exclude-standard`), copies
   it in with `sandbox cp`, extracts to `/vercel/board`, then
   `corepack pnpm install --frozen-lockfile --filter '@vercel/board...' && corepack pnpm --filter @vercel/board build`;
   published mode: `npm install @vercel/board@<version>` in `/vercel/cli`;
3. links `/vercel/bin/vb` to the CLI under test (a symlink, as npm would);
4. in a fresh `git init` project at `/vercel/proj`, starts
   `setsid nohup vb serve --no-inspect --no-open > /vercel/serve.log &`;
5. readiness: polls `vb whoami` (with `BOARD_URL` set to it, as every call is) every 0.5s for 30s; on success prints the serve log
   (`serving a local board at http://127.0.0.1:4100/api/board as local:user:ubuntu, ...`).

If any step fails, `up.sh` runs `down.sh` itself so nothing is stranded (`VERIFY_KEEP=1` keeps the
sandbox for debugging; then remove it yourself). The setup log is `.verify/board/<timestamp>/up.log`.
The repo is private, so the sandbox can't `git clone` it: the tarball is the way in.

Teardown is `$V/down.sh "$S"` (see Cleanup).

## Doctor

Read-only; changes nothing. Run it after `up.sh` and whenever a drive misbehaves.

```bash
$V/doctor.sh "$S"
```

```
sandbox   verify-board-20261014-205253-3f2a running
vb        0.9.0
board     http://127.0.0.1:4100/api/board as ubuntu (local:user:ubuntu)
```

It checks that `sandbox ls --all` shows the sandbox `running`, that the sandbox's `vb --version` equals
the version under test (`packages/board/package.json` of this checkout, or the `--published`
version), and that the board answers `vb whoami`. Exit 1 on any miss. A `stopped` sandbox hit its
timeout: tear it down and launch again.

## Drive

Two wrappers. Both run in `/vercel/proj` (the served project) with `BOARD_URL` set to the board, pass
stdout, stderr, and the exit code through, and append each call to the transcript.

```bash
$V/vb.sh "$S" post dev "hello from a sandbox" --label kind=bug   # argv, no shell; prints the id
$V/vb.sh "$S" read dev --json
$V/sh.sh "$S" 'echo "from stdin" | vb reply 2 -'                  # a bash line, vb on PATH
$V/sh.sh "$S" '(sleep 3; vb post dev late) & vb wait dev --timeout 30s'
```

A worked drive, posting and threads end to end with checks that fail loudly:

```bash
$V/drive-posting.sh "$S"     # posting and threads: ok (thread #2)
```

Real commands to reach for (see `vb help` and `features/` for the rest):

| What | Command |
| --- | --- |
| post, reply, edit, delete | `vb post dev "text" --label k=v`, `vb reply <id> "text"`, `vb edit <id> "text"`, `vb delete <id>` |
| idempotent post | `vb post dev "text" --idempotency-key <key>` (same id twice) |
| attach | `sh.sh 'printf x > f.txt && vb reply <id> "file" --attach f.txt'`, then `vb download <attachment> -` |
| read | `vb read dev`, `vb read <id>`, filters `--label k[=v]`, `--by`, `--text`, `--re`, `--mentions`, `--json` |
| react, label | `vb react <id> eyes [--remove]`, `vb label <id> k=v --unset k` |
| live | `vb wait dev --timeout 30s` (exit 1, `reason: "timeout"`, on timeout), `timeout 6 vb tail dev` |
| who, where | `vb whoami --json`, `vb channels`, `vb actors` |

Any other command in the sandbox: `$V/sb.sh exec "$S" -- <cmd...>` (not logged). Copy a file out:
`$V/sb.sh cp "$S:/vercel/proj/<path>" <local path>`.

Never point the sandbox's `vb` at a remote board. Its board is the local one; the production
factory board syncs to Slack and GitHub.

## Evidence

Everything lands in `.verify/board/<timestamp>/` in the repo (gitignored), which survives
teardown:

| File | What |
| --- | --- |
| `meta` | sandbox name, mode (source/published), version, commit, count of dirty files |
| `up.log` | setup output: create, install, build, serve |
| `doctor.txt` | each doctor run |
| `transcript.txt` | every `vb.sh`/`sh.sh` call: `$ command`, output, `[exit N]` when nonzero |
| `files/` | from `collect.sh` (run by `down.sh`): `.board/` (`local.db` + WAL and `local/` for its files, or `board.db` and `attachments/` on an older board), `serve.log`, `read.json` (`vb read <id> --json` of every thread), `files.txt` |
| `down.txt` | the removal |

Proof standards:

- **The real user path.** Drive `vb` as a person or agent would, against the served board. No
  calls into source, no test harness, no hand-written HTTP.
- **Action, then resulting state.** Every write is followed by a read that shows it
  (`vb post` then `vb read <id>`; `vb label` then `vb read dev --label k=v`). An exit code alone
  proves little; `vb edit` and `vb delete` print nothing on success.
- **Side effects.** Show the files the action leaves: the attachment under
  `.board/local/` (an older board's `.board/attachments/`), the WAL growing, `~/.claude/settings.json` in a throwaway `HOME`.
- **Errors too.** A misuse exits 2 (`error: Unknown command …`, `error: Missing …`); a missing
  thread exits 1 with `error: Couldn't find message #N.` With `--json`, stderr is one JSON document
  with its `reason`. Capture both when behavior at the edges is the claim.
- Quote the transcript lines that prove the claim, and give the evidence path.

## Cleanup

```bash
$V/down.sh "$S"              # collect evidence, rm the sandbox, confirm `sandbox ls --all` no longer lists it
$V/down.sh "$S" --no-collect # when the sandbox is already broken
```

Remove only the sandbox you created, by its exact name. `down.sh` refuses anything that isn't
`verify-board-<YYYYMMDD-HHMMSS>-<hex>`, and never removes by pattern: other agents may be running their
own sandboxes in the same scope. After a failed attempt, run `down.sh` before trying again, then
check `$V/sb.sh ls --all --name-prefix "$S"` for your name. Never commit `.verify/`.

## Helpers

| Script | Use |
| --- | --- |
| `sb.sh <cmd> [args]` | `npx --yes sandbox@4.8.1 <cmd> --scope vercel-labs` (`SANDBOX_SCOPE` overrides) |
| `up.sh [--published <v>]` | create, upload or install, serve; prints the name |
| `doctor.sh <name>` | read-only health check |
| `vb.sh <name> <args…>` | `vb` in the sandbox, logged |
| `sh.sh <name> '<line>'` | a bash line in the sandbox, `vb` on PATH, logged |
| `drive-posting.sh <name>` | the worked posting-and-threads drive |
| `collect.sh <name>` | copy `.board/`, the serve log, and `read.json` out |
| `down.sh <name> [--no-collect]` | collect, remove, confirm |
| `common.sh` | sourced: paths, name check, `sbx`, `sbx_script`, `run_logged` |

Each sandbox command costs a few seconds of round trip; batch related steps into one `sh.sh` line
when timing doesn't matter. Pass multi-line text through stdin (`sh.sh 'printf "a\nb" | vb post dev -'`),
not as a `vb.sh` argument.
