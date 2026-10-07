---
name: verify-10x-cli
description: Drive the real `10x` CLI (@przeprogramowani/10x-cli) end to end the way a learner does — login, list, get, sync, changelog, doctor — against a local fake delivery API with isolated config and project dirs, and capture stdout/stderr/exit codes, PTY screens and file-tree hashes as proof. Use after changing a command, the writer, conflict handling, auth or the API client, when unit tests pass but you need to see the shipped behaviour, or when asked to "verify", "run the CLI", "prove it works".
---

# Verify 10x-cli

The surface is a short-lived CLI (`10x <command>`), not a server. Every run gets its own
fake delivery API on an OS-assigned free port, its own `XDG_CONFIG_HOME`, and its own
throwaway project dir — so several agents can verify in parallel on one machine and nothing
touches production, real email, your `~/.config/10x-cli` or this checkout's `.claude/`.

Everything goes through one helper (run from the repo root):

```bash
V=.claude/skills/verify-10x-cli/scripts/verify.sh
$V help
```

## Launch

```bash
bun install --frozen-lockfile        # once per checkout
$V up                                # prints run=<id> api=http://127.0.0.1:<port> pid=<pid> project=<dir> evidence=<dir>
$V seed-auth                         # optional: logged-in state without driving the login flow
```

`up` is ready when it prints `run=…`: `scripts/fake-api.ts` only writes `api.json` after it
is listening. It generates a fresh Ed25519 key; the CLI accepts it through
`BUNDLE_PUBLIC_KEYSET`, which `src/lib/signing.ts` honours only when `API_BASE_URL` is
`localhost`/`127.0.0.1`. The CLI runs from source (`bun run src/index.ts`); to prove the
shipped Node bundle instead, `bun run build` and prefix commands with `VERIFY_ENTRY=dist`.

Fixture served by the fake API (course `10xdevs3`, id `10xdevs-3`):

| Lesson | Module state | Content |
| --- | --- | --- |
| `m1l1` | unlocked | skill `verify-fixture-skill`, prompt `verify-fixture-prompt`, rule, config `verify-fixture.json` |
| `m1l2` | unlocked | skill `verify-m1l2-skill` |
| `m2l1` | locked (403) | — |

`$V bump <lessonId>` publishes a new upstream version (`v1` → `v2` in every file and a new
catalog `contentHash`) — use it to prove `sync` and conflict handling.

## Doctor

```bash
$V doctor        # exit 0 = worth driving
```

Read-only. Checks: the fake API pid is alive **and** was started by this run, `/health`
answers, the URL is loopback, config/project dirs are this run's, the checkout revision has
not changed since `up` (rebuild/re-`up` if it did), and the CLI starts (`--version`). Run it
first, and again whenever output looks wrong. Not the same as `10x doctor` (a feature, see
the map).

## Drive

Non-TTY (JSON envelope mode — the CLI implies `--json` when stdout is not a TTY):

```bash
$V cli <label> -- <10x args>         # e.g. $V cli get -- get m1l1 --tool claude-code
```

Runs in the run's project dir; saves `NN-<label>.cmd|stdout|stderr|exit`; prints them. The
helper always exits 0 — the CLI's exit code is data (`0` ok, `1` error, `2` usage, `3` auth,
`4` forbidden, `5` not found). Always pass `--tool claude-code` to `get`/`sync` in a fresh
project, or tool detection prompts / fails.

TTY (human output, `@clack/prompts` menus) in a private tmux server (`-L 10x-verify-<run>`,
never your default tmux):

```bash
$V tty <label> -- <10x args>         # start
$V wait-screen '<regex>' [seconds]   # wait for a prompt string, never a fixed sleep
$V keys Down Enter                   # tmux key names, or literal text
$V screen <label>                    # save the screen as evidence
$V wait-screen '10x exited'          # the PTY prints "[10x exited <code>]" when done
```

Fake-world actions: `$V click` (the learner clicks the newest magic link), `$V bump <lesson>`,
`$V changelog release|off|on` (publish a newer toolkit release; remove / restore the
changelog route).
State proof: `$V snapshot <label>` (sha256 of every file in project + config dirs).
Narrative: `$V note "<text>"` appends to the run's `notes.md`.

The feature map in [`features/`](features/README.md) has the exact recipe per feature.
Read its README first; a proof that drives one convenient entry point is incomplete when
the map lists others.

## Evidence

All proof lands in `.quality-local/verify-10x-cli/<run>/` (gitignored, survives `down`):
numbered `.cmd/.stdout/.stderr/.exit`, `.screen.txt`, `.tree.txt`, `notes.md`,
`fake-api.log`, and `requests.log` (every HTTP request the CLI made, copied at `down`).

Proof standards:

- Drive the real user path (`10x …` in a project dir). No importing `src/` functions, no
  writing the manifest by hand. `seed-auth` is the one allowed shortcut, and only for
  features other than auth.
- Capture the action and the resulting state: the command output **and** a `snapshot` (or
  file contents) showing what was written, kept or removed.
- Verify side effects, not just the envelope: files on disk, `.claude/.10x-cli-manifest.json`,
  `.10x-cli.json`, `CLAUDE.md` rule block, `auth.json`, and `requests.log` for which endpoints
  were hit.
- `--dry-run` was observed to write nothing (compare `snapshot` before/after) but still fetch
  over the network (see `requests.log`). Re-check that when you change it; do not trust the
  flag name.
- `10x doctor` calls the real npm registry (`registry.npmjs.org`, read-only GET) for its
  version check. Everything else stays on the fake API.
- Report skipped entry points as skipped, with the unmet precondition.

## Cleanup

```bash
$V down
```

Kills only the fake API pid recorded by `up` (after checking its command line contains this
run's scratch dir) and this run's private tmux server, deletes the scratch dir
(`$TMPDIR/10x-verify-<run>.*`), and keeps the evidence dir. Never `pkill bun`/`pkill tmux`:
other sessions run on this machine. After a failed attempt, still run `down`. To target an
older run: `VERIFY_RUN=<id> $V down`.

## Helpers

| Script | Invocation |
| --- | --- |
| `scripts/verify.sh` | `$V <command>` — all of the above; `$V help` lists commands |
| `scripts/fake-api.ts` | started by `$V up`; standalone: `bun .claude/skills/verify-10x-cli/scripts/fake-api.ts <dir> [port]` |

Both are verification scaffolding, not product code. When the API contract changes
(`bun run generate-types` updates `src/generated/api-types.ts`), update `fake-api.ts` to
match or verification will lie.
