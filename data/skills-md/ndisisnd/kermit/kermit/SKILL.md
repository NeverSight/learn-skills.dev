---
name: kermit
description: Format and run git commits using Conventional Commits style with emoji prefix, point-form file bodies, and BREAKING CHANGE footer. Manages CHANGELOG.md (hook-accelerated on Claude Code). Use --init to initialize changelog.
model: sonnet
allowed_tools:
  - Bash
  - AskUserQuestion
refs:
  - refs/protocol-init.md
  - refs/protocol-commit.md
  - refs/protocol-pr.md
  - refs/protocol-release.md
  - refs/protocol-changelog-sync.md
  - refs/protocol-subagent.md
  - refs/template-release.md
  - refs/changelog-protocol.md
  - refs/changelog-reset.md
---

## Usage

**Invoke**: `/kermit [--pr] [--init] [--changelog-reset] [--changelog-sync] [--release]` — "commit this", "make a commit", "commit my changes"

**Natural-language routing** (no flag needed): PR intent ("make/open/raise a PR", "open a pull request to `<base>`", "PR this branch") → `--pr`; if the user names a base ("…to `develop`"), use it as the PR base. Release intent ("write release notes", "cut a release", "do a release") → `--release`. Changelog-backfill intent ("check my changelog", "log missing commits", "sync the changelog", "backfill the changelog") → `--changelog-sync`. Otherwise commit intent → the default commit flow.

- `--pr`: run the **PR protocol** (`refs/protocol-pr.md`) — open/update a GitHub pull request for the current branch via `gh`. Operates on commits already on the branch; does **not** create a commit.
- `--init`: re-run the full init block regardless of prior initialization, then exit.
- `--changelog-reset [--apply]`: rewrite the existing changelog to current conventions (entries grouped under `## <date>` sections, numbered `### [N]`, normalised bullets); shows a diff and confirms before writing (`--apply` skips the confirm), then exits.
- `--changelog-sync`: run the **changelog-sync protocol** (`refs/protocol-changelog-sync.md`) — find commits that landed without a changelog entry, report them, and backfill the missing entries. Writes only the changelog; makes no commit.
- `--release`: run the **release protocol** (`refs/protocol-release.md`) — write user-facing release notes to `RELEASES.md` for the changes since the last release, organised by type with a highlight summary, then commit them (bumping `package.json`'s version) and publish a GitHub release via `gh`. Operates on committed history; the only commit it makes is the release commit itself.

When kermit is driven by an orchestrator as a subagent worker, read `refs/protocol-subagent.md` for the worker contract.

## Inputs

| Name | Format | Source |
|------|--------|--------|
| staged diff | text | `git diff --staged` (rtk-prefixed if available) |
| changelog exists | bool | `test -f` on the resolved changelog path (hook cache used if present) |
| branch state (PR mode) | text | `git rev-parse` / `git log $BASE..HEAD` / `gh pr view` |

## Outputs

| Name | Format | Destination |
|------|--------|-------------|
| commit message | text | shown inline for approval |
| CHANGELOG.md entry | prose | appended on confirmed commit |
| backfilled entries (changelog-sync mode) | prose | written to the changelog; no commit made |
| git commit / push | shell | run on user confirmation |
| pull request (PR mode) | shell | created/updated via `gh pr create`/`gh pr edit`, URL shown |
| RELEASES.md notes (release mode) | prose | prepended, then committed with a `package.json` version bump |
| GitHub release (release mode) | shell | published via `gh release create v<x.y.z>`, URL shown |
| kermit-result block | fenced text | emitted at the end of every run |

## Protocol

Four protocol modes, each in its own ref:

- **Commit** (default) — `refs/protocol-commit.md`: format a message, gate it, commit, and optionally push.
- **PR** — `refs/protocol-pr.md`: open/update a pull request for the current branch.
- **Release** — `refs/protocol-release.md`: write release notes, commit them, publish a GitHub release.
- **Changelog-sync** — `refs/protocol-changelog-sync.md`: backfill changelog entries for commits that landed without one.

kermit keeps two files under the resolved `KERMIT_DIR` (see **Harness resolution**): **`pref.json`** holds stable config
(`initialized`, `init_commit`, `changelog.*`, `gate_mode`) and is safe to
commit; **`state.json`** holds volatile runtime state (`last_logged_commit`, `last_number`,
`last_released_number`, `backfill`) that is rewritten on every commit and must stay git-ignored. Both are read
**once** at the mode-check step below — cache their values for the rest of the run rather
than re-reading either file in later steps.

### Harness resolution (runs first, once per run)

kermit runs on more than one agent harness. Resolve these three values **once**, in a single
batched Bash call, and cache them for the whole run — never re-detect them in a later step.

- **`HARNESS`** — `claude` or `codex`: which harness loaded this skill. Decide from the
  environment: `$CODEX_HOME`/`CODEX_*` variables set, or the skill was loaded from a Codex
  skill directory (`.agents/skills/kermit`, `~/.codex/…`) → `codex`. Otherwise → `claude`.
- **`KERMIT_DIR`** — where `pref.json` and `state.json` live. Precedence, first hit wins:
  1. `$KERMIT_DIR` if the environment variable is set;
  2. `.claude/kermit/` if that directory already exists;
  3. `.codex/kermit/` if that directory already exists;
  4. otherwise create it under the current harness's dir — `.claude/kermit/` when
     `HARNESS=claude`, `.codex/kermit/` when `HARNESS=codex`.
  A repo initialized under one harness is therefore reused, not duplicated, by the other.
- **`INTERACTIVE`** — `true` only when a human can answer a question **right now**. It is
  `false` when running under `codex exec`, when running as a spawned subagent (no approval
  channel), or under headless Claude (`claude -p`). When in doubt with no interactive
  signal, resolve `false` — stalling a non-interactive run is worse than auto-deciding.

One batched call, e.g.:

```
[ -n "$CODEX_HOME" ] && HARNESS=codex || HARNESS=claude
if [ -n "$KERMIT_DIR" ]; then :;
elif [ -d .claude/kermit ]; then KERMIT_DIR=.claude/kermit;
elif [ -d .codex/kermit ]; then KERMIT_DIR=.codex/kermit;
elif [ "$HARNESS" = codex ]; then KERMIT_DIR=.codex/kermit;
else KERMIT_DIR=.claude/kermit; fi
mkdir -p "$KERMIT_DIR"; echo "harness=$HARNESS dir=$KERMIT_DIR"
```

Everywhere a protocol writes `$KERMIT_DIR/pref.json` or `$KERMIT_DIR/state.json`, it means
the path resolved here. The git-ignore line for state must use the same resolved path.

### GATE contract

Protocols never name a question tool directly. They write `GATE(question, options, default)`
and this contract resolves it:

- **`INTERACTIVE=true` and `HARNESS=claude`** → make a real **`AskUserQuestion` tool call**
  with that question and those options. Not a plain-text question, not the default — an
  actual tool call, every time. This is the single most important rule on this page.
- **`INTERACTIVE=true` and `HARNESS=codex`** → ask the same question in plain chat text with
  the options as a numbered list, and wait for the reply.
- **`INTERACTIVE=false`** (either harness) → take the stated `default` silently. Emit no
  question, produce no pause. Free-text gates take their stated default string.

**Non-interactive forces effective-auto gates.** When `INTERACTIVE=false`, the resolved
`auto_approve` / `auto_commit` / `auto_merge` / `auto_create` / `auto_publish` are all treated
as `true` regardless of `gate_mode`, and the run's `kermit-result` records
`gates: auto (non-interactive)`. `gate_mode` still governs interactive runs unchanged.

### kermit-result block

**Every** run — every mode, every exit path, success or handled failure — ends by emitting
this fenced block, and nothing after it:

```kermit-result
mode: commit | pr | release | changelog-sync | init | changelog-reset
head: <sha or null>
changelog_entry: <N or null>
pushed: yes | no | failed
published: yes | no | n/a
gates: full | auto | auto (non-interactive)
```

`pushed: failed` and `published: no` are normal, successful terminations when the sandbox has
no network — add a one-line remediation after the block, do not error out.

### Mode check (runs after harness resolution, before everything else)

- **`--changelog-reset`** → read `refs/changelog-reset.md`, follow it end-to-end, then **exit** — do not run the commit flow.
- **Otherwise** → read `$KERMIT_DIR/pref.json` and `$KERMIT_DIR/state.json`. If pref is absent, create it with `{"initialized":false}`. If `initialized` is `false` **or** `--init` was passed: read `refs/protocol-init.md` and follow it end-to-end. An un-initialized repo runs setup first and then **continues into the requested mode** via the protocol dispatch below — only an explicit `--init` exits after setup. Otherwise fall through to the protocol dispatch below.
  - **Legacy migration.** Older prefs kept the state fields inside `pref.json`. If `state.json` is absent, create it now — seed `last_logged_commit` from `pref.last_logged_commit`, `last_number` from `pref.changelog.last_number`, `last_released_number` to `0`, and `backfill` from `pref.backfill` (each defaulting to `null`/`0` when the legacy key is missing), then rewrite `pref.json` without those three keys and ensure `$KERMIT_DIR/state.json` is in `.gitignore` (`grep -qxF "$KERMIT_DIR/state.json" .gitignore 2>/dev/null || printf '%s\n' "$KERMIT_DIR/state.json" >> .gitignore`). Cache the migrated state for the run.

### Protocol dispatch

Select the protocol mode and read its ref, then follow it end-to-end:

- `--release` was passed → read **`refs/protocol-release.md`** and follow it.
- `--pr` was passed → read **`refs/protocol-pr.md`** and follow it.
- `--changelog-sync` was passed → read **`refs/protocol-changelog-sync.md`** and follow it.
- Otherwise (default commit flow) → read **`refs/protocol-commit.md`** and follow it.

---

Dedicated to JC 💕
