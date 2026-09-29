---
name: regression-notes
description: >
  Record bug-fix decisions as Agent Notes bound to regression tests so AI-driven
  code changes cannot silently regress. Use when fixing a bug, reviewing a fix,
  verifying a notes tree, or asking when to write a postmortem. Do not use for
  general feature docs or changelogs.
license: Apache-2.0
metadata:
  author: meimingqi222
  derived-from: >
    DeepSeek Harness `.agents/notes` Agent Note system (bug-fix class, format
    gate, regression binding, postmortem bar); lightweight, dependency-free port.
  tools: any
  # Claude Code v2.1.129+ expands ${CLAUDE_SKILL_DIR} here so the verifier runs
  # without a permission prompt; other harnesses ignore this field.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/verify-notes.py *), Bash(${CLAUDE_SKILL_DIR}/scripts/new-note.py *)
---

# Regression notes

Version 0.4.0

Use `python` or `py -3` when `python3` is unavailable (stock Windows).

A lightweight port of the DeepSeek Harness Agent Note loop: every non-trivial bug fix ships **one note (the why) + one regression test (the lock)** in the same change. The note records the decision; the test pins the behavior.

A fix is non-trivial when it changes behavior, a contract shared across files, an on-disk/wire/config format, or a decision a maintainer may revisit. Purely mechanical or local edits with no behavior change are exempt.

## Installing into a repository

The skill only works if it is required, not merely available. Add this standing rule to the repo's `AGENTS.md` or `CLAUDE.md` so every agent session enforces it:

```markdown
## Regression notes

Every non-trivial bug fix ships one regression note and one regression test in the same change. The note records the problem, the decision, the alternatives considered, and the consequences; the test pins the behavior. A `## Verification` section names the test path and records the red-run proof.

Trivial mechanical edits with no behavior change are exempt.

`python3 regression-notes/scripts/verify-notes.py --notes-dir .agents/notes` must pass before any related change is merged.
```

Then give the gate something that actually runs it. A rule in a prose file is a request; a command that runs without an agent choosing to is a gate. Use whichever the repository already has:

```yaml
# 1. CI, when the repository has it
- name: Verify regression notes
  run: python3 regression-notes/scripts/verify-notes.py --notes-dir .agents/notes
```

```sh
# 2. A pre-commit hook -- the common case, since most repositories have no CI
#!/bin/sh
# .git/hooks/pre-commit   (chmod +x it; on Windows run hooks under Git Bash,
# where `python3` may be missing and the `py` launcher stands in)
if command -v python3 >/dev/null 2>&1; then
  python3 regression-notes/scripts/verify-notes.py --notes-dir .agents/notes || exit 1
else
  py -3 regression-notes/scripts/verify-notes.py --notes-dir .agents/notes || exit 1
fi
```

```sh
# 3. Inside an existing packaging/release script, where the tree may be absent
python3 regression-notes/scripts/verify-notes.py --notes-dir .agents/notes --allow-missing
```

Then prove the wiring (read-only; a packaging-script wiring cannot be auto-detected, so the gate counts a hook or a CI config):

```bash
python3 regression-notes/scripts/verify-notes.py --notes-dir .agents/notes --check-install
```

**You have not installed this skill until you can name the command that runs the verifier without an agent deciding to.** If the answer is "the agent runs it when it remembers", the gate does not exist — that is the failure this skill was built to prevent.

You can either vendor this skill under `regression-notes/` in the target repository, or install it in CI and point `--notes-dir` at the repo's note tree. Git does not track empty directories: commit a one-line `.agents/notes/README.md` (the verifier skips it) so the gate has a tree to verify on a fresh clone before the first note exists.

## Locate the scripts

The scripts live next to this file. Never glob for them first — resolve once, cheapest source first:

1. **Claude Code v2.1.64+** — the harness already expanded `${CLAUDE_SKILL_DIR}` to this skill's directory when it loaded this file. Use it directly and skip the rest:

   ```bash
   SCRIPTS="${CLAUDE_SKILL_DIR}/scripts"
   ```

2. **Other harnesses** — `~/.agents/skills` is the Agent Skills open-standard location that `npx skills` installs to for most agents; a few agents use their own directories instead. Test the standard locations in one command (sh/bash; on Windows use Git Bash, or the PowerShell equivalent below); it exits at the first hit, and globs only as a last resort:

   ```bash
   for d in "${CLAUDE_SKILL_DIR:-}" "$HOME/.agents/skills" \
            "$HOME/.claude/skills" "$HOME/.config/opencode/skills" \
            "$HOME/.codex/skills" "$HOME/.cursor/skills" \
            ".agents/skills" ".claude/skills"; do
     [ -f "$d/regression-notes/scripts/verify-notes.py" ] \
       && SCRIPTS="$d/regression-notes/scripts" && break
   done
   if [ -z "${SCRIPTS:-}" ]; then
     path=$(find "$HOME" . -maxdepth 6 -path '*/regression-notes/scripts/verify-notes.py' -print -quit 2>/dev/null)
     [ -n "$path" ] && SCRIPTS=$(dirname "$path")
   fi
   ```

   PowerShell equivalent:

   ```powershell
   $roots = @(
       $env:CLAUDE_SKILL_DIR,
       (Join-Path $env:USERPROFILE ".agents\skills"),
       (Join-Path $env:USERPROFILE ".claude\skills"),
       (Join-Path $env:USERPROFILE ".config\opencode\skills"),
       (Join-Path $env:USERPROFILE ".codex\skills"),
       (Join-Path (Get-Location) ".agents\skills")
   ) | Where-Object { -not [string]::IsNullOrEmpty($_) }
   $hit = $roots | ForEach-Object { Join-Path $_ "regression-notes\scripts\verify-notes.py" } |
       Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
   if (-not $hit) { throw "Could not locate regression-notes/scripts/verify-notes.py" }
   $SCRIPTS = Split-Path -Parent $hit
   ```

The notes root defaults to `.agents/notes/` and is overridable per call with `--notes-dir` or globally with the `NOTES_DIR` environment variable.

## Start here

When fixing a bug, scaffold a note and bind it to a regression test:

```bash
python3 "$SCRIPTS/new-note.py" --status implemented --test tests/test_login.py login-retry-race
```

`--test` is repeatable and pre-fills `## Verification` with real test paths. Write `--test 'tests/test_login.py::test_retry_after_lockout'` to bind one exact test (see [Regression binding](#regression-binding)). Strict verification still fails until the test file exists and the `Proved:` line records the real red run in place of the template placeholder.

`--class` accepts any class in the closed set below; non-`bug-fix` classes use `templates/generic.md` and carry no `## Verification` requirement.

A rejected proposal:

```bash
python3 "$SCRIPTS/new-note.py" --status rejected --reason "duplicates the retry policy" login-retry-race
```

Find the note that already owns a decision before writing a new one:

```bash
python3 "$SCRIPTS/verify-notes.py" --notes-dir <notes-dir> --find "retry policy"
```

`--find` matches a regex against note filenames and bodies, and prints each hit's path, title, decision, and cited tests. There is no index file to maintain — the tree is the index, and this is how you search it.

Verify the tree:

```bash
python3 "$SCRIPTS/verify-notes.py" --notes-dir <notes-dir>
```

Exit non-zero means red. The gate needs exactly one line:

```bash
python3 regression-notes/scripts/verify-notes.py --notes-dir .agents/notes
```

If the notes directory may legitimately be absent during a dry run, use `--allow-missing`; do not use that flag in the commit gate.

## Layout and format

Notes are path-encoded as `{proposed,implemented,rejected,archived}/{class}/yyyy-mm-dd-topic.md`:

- **Lifecycle** is the status:
  - `proposed/` (`Status: proposed`) → `implemented/` (`Status: implemented`) → `archived/` (`Status: implemented` + `Archived: YYYY-MM-DD`). Moving `proposed/` → `implemented/` means rewriting `## Proposal` into a present-tense `## Decision` and folding `## Acceptance criteria` / `## Risks` into `## Consequences`.
  - `rejected/` (`Status: rejected — <why>`) keeps proposal-time sections (`## Problem`, `## Proposal`, `## Alternatives considered`, optionally `## Acceptance criteria` / `## Risks`) and is kept only while the losing proposal remains a tempting mistake.
  - `archived/` notes are frozen: once they carry `Archived: YYYY-MM-DD` they must not be edited again, and every archived note must be sealed (see below).
- **Class** is closed: `bug-fix, feature, architecture, process, testing, simplification`. Adding a class requires updating this file and the `CLASSES` constant in `verify-notes.py` together; `new-note.py` reads the set from the verifier, so it cannot drift.

Every note follows one skeleton. `bug-fix` uses `templates/bug-fix.md`; the other classes use `templates/generic.md`, which is the same skeleton minus `## Verification` (only `bug-fix` binds a test):

```markdown
# Agent Note: <title>

Status: implemented

## Problem
## Decision
## Alternatives considered
## Consequences
## Verification        # bug-fix only
```

### Header block

The header is a closed, minimal block — resist extending it into front-matter:

```markdown
# Agent Note: <title>

Status: implemented
Archived: YYYY-MM-DD                            # archived/ only
Superseded-by: <note.md>                        # archived/ only, optional
Partly-superseded-by: <note.md>                 # optional
                                                # <- blank line ends the block
```

`Superseded-by` and `Partly-superseded-by` name another note in the same tree. The verifier checks that each pointer resolves, that neither points at its own note, and that the chain has no cycles.

- **`Superseded-by`** means the successor fully replaces this note. It is valid only under `archived/`, and the successor should carry the consolidated rationale.
- **`Partly-superseded-by`** means the successor replaces part of the decision while the rest still holds. It requires a `## Superseded` section stating what still holds and what no longer does, because a partially replaced note is otherwise indistinguishable from current authority.

Rules the verifier enforces:

- Header block exact (`L1/L3`, blank `L2`; `Archived:` immediately below `Status: implemented` for archived notes; supersede lines after that; a blank line ends the block).
- Exactly one `Status:` line and it agrees with the folder.
- Body opens with `## Problem`.
- `## Alternatives considered` mandatory.
- `proposed/` and `rejected/` may use `## Proposal` / `## Acceptance criteria` / `## Plan`; `implemented/` and `archived/` ban them.
- `bug-fix` in `implemented/` or `archived/` requires `## Verification` with:
  - at least one backticked test path that exists (`--no-strict` degrades a missing target to a warning), and
  - a `Proved:` line recording that the regression test was seen to fail before the fix and to pass after; the line must not still carry the template placeholder.
- Supersede pointers resolve, are not self-references, and form no cycle (see above).
- Note basenames must be unique across the whole tree: `Superseded-by` and note references address notes by basename, so `bug-fix/2026-01-01-x.md` and `feature/2026-01-01-x.md` side by side are an error.
- Filenames must encode a valid calendar date and not be in the future.
- Only `.md` files live in the notes tree. A `*.zh.md` sibling is allowed as the translation of its canonical note and is skipped by the gate (no format checks); keep it next to the note it translates so the pair stays in sync.
- Every archived note must be sealed in `archived/manifest.json`; a sealed note that is later modified or deleted fails verification.

Warnings (never errors — each is a heuristic, so it is advisory):

- A cited `snake_case`/`Pascal_Case` identifier that appears in no test file the note cites — likely a renamed test. Disable with `--no-name-heuristic`.
- A backticked bare source filename (`OldTests.cs`) that resolves nowhere under the repo. Disable with `--no-bare-resolution`. Date-prefixed note filenames are excluded here so one token never yields two warnings.
- A backticked note filename that is not in the tree — a renamed or deleted note.
- A `path::anchor` whose anchor is missing from that file. Promote to an error with `--strict-anchors` once a repository's bindings are clean. A per-note `anchor` disable only silences the warning form, never the `--strict-anchors` error.

Keep the gate quiet without weakening it (all generic, all optional; errors always cover the whole tree):

```bash
# Per-note opt-out for one noisy legacy note (does not affect other notes;
# parsed from fence-stripped prose with inline code spans removed, so a fenced
# or backticked usage example cannot disable its own note's checks):
# <!-- verify-disable: name-heuristic, bare-resolution, note-ref, anchor -->
# <!-- verify-disable: all -->

# Adopt incrementally: record today's warnings, keep the file in version control
# (--update-baseline cannot be combined with --changed-only: a partial-tree
# baseline would be incomplete)
python3 "$SCRIPTS/verify-notes.py" --notes-dir <notes-dir> --baseline .agents/notes-baseline.json --update-baseline
python3 "$SCRIPTS/verify-notes.py" --notes-dir <notes-dir> --baseline .agents/notes-baseline.json

# pre-commit: warnings only for notes changed versus HEAD (untracked included)
python3 "$SCRIPTS/verify-notes.py" --notes-dir <notes-dir> --changed-only
# nightly/CI: full warnings, optionally with --strict-anchors
python3 "$SCRIPTS/verify-notes.py" --notes-dir <notes-dir> --strict-anchors
```

`--changed-only [--base HEAD]` falls back to the full tree outside a git work tree. Paths are resolved relative to `--repo-root`, so a subdir repo-root sees its own subtree; git-ignored notes stay warning-enabled (conservative). Bare-filename resolution prefers `git ls-files` (respects `.gitignore`, much faster on monorepos) and falls back to a pruned walk.

## Sealing the archive

The archive freeze is machine-checked, not a convention. Archive in one step — move, header, and seal together:

```bash
python3 "$SCRIPTS/new-note.py" --archive 2026-09-01-old-decision.md --successor 2026-09-09-new-decision.md --notes-dir <notes-dir>
```

`--archive` moves the implemented note to `archived/`, inserts `Archived:` plus `Superseded-by:`, then verifies and seals. `--by` is an alias of `--successor`. The manual equivalent is: move the file, add the two header lines, then run `verify-notes.py --seal` in the same change.

`--seal` verifies the tree, then records each archived note's SHA-256 in `archived/manifest.json`. The manifest is append-only: `--seal` adds missing entries and refuses to rewrite a recorded hash, so a note that was modified after sealing stays red — fix forward with a new note instead of editing history. Plain verification, including the gate one-liner, fails on any archived note that is unsealed, modified, or deleted.

Archive a note only when it is fully superseded and its successor carries the consolidated rationale. Once sealed the note is frozen, so a `Superseded-by` pointer added afterwards can never be corrected — get the pointer right before sealing (the `--archive` command above gets this order right by construction).

## Keep the corpus current

A note that contradicts the code is worse than no note: an agent following stale authority will regress the fix.

Before creating a note, search the tree for an existing note that owns the same decision or mechanism (`--find` above). Update that note in the same change instead of duplicating it.

When a later decision replaces an earlier one, record the link in the header so the old note cannot be read as current authority:

- **Fully superseded** — consolidate the unique rationale, alternatives, consequences, and verification into the new owner, then run `new-note.py --archive <old>.md --successor <new>.md` (moves to `archived/`, adds `Superseded-by:`, seals). The old note keeps its history; the pointer says who owns the decision now.
- **Partly superseded** — the successor covers one branch, and the rest still holds. Add `Partly-superseded-by: <successor>.md` and a `## Superseded` section saying which part is dead. Leave the note in `implemented/`: it is still live authority for the rest.

Do not leave a partly replaced decision recorded only as an inline remark in the body — that is how a superseded `## Consequences` section keeps asserting behavior the code no longer has. The header pointer and the `## Superseded` section are what make the stale part legible.

When code moves, renames, or deletes files referenced in an implemented note, update the note's paths and symbols in the same change. The verifier warns on missing test paths, unresolvable bare filenames, and dangling note references; you must catch stale module names, defaults, and prose claims it cannot see.

## Regression binding

The note-to-test link is one-directional and reviewable: the note's `## Verification` section names the test path(s); the spec itself stays plain test code. Ship both in the same change — a note without a test is a wish, a test without a note is a mystery. `archived/` notes are frozen and never cited as authority for current behavior.

To bind one exact test, write the path and an anchor separated by `::`:

```markdown
- `tests/test_login.py::test_retry_after_lockout`
```

The anchor is checked as a plain substring of that file. That is the whole grammar: the verifier never parses the test language, so it works the same for `test_foo` (pytest), `TestFoo` (Go), `should foo` (JS), or a snapshot directory name. A token containing `::` is treated as a binding only when the part before the first `::` is an existing file, so C++ scope resolution (`std::filesystem`, `Class::Method`) is never mistaken for one — no language list required.

Prefer the anchored form: a bare `tests/test_login.py` proves the file exists, not that the test does. If you cite a test by name anywhere in `## Verification` without an anchor, the verifier warns, because it cannot tell a renamed test from prose.

A guard only guards if the regression fails it. Before submitting, prove it: temporarily reintroduce the bug (or stub the fix), watch the bound test go red, then revert. Record the red run in the `Proved:` line under `## Verification` (e.g. `Proved: disabled the latch → tests/test_login.py::test_retry_after_lockout failed as expected, then reverted`). A test you have never seen fail is a self-report, not a lock — assert against the world (re-run the command, re-read the file from outside), never against the agent's own output.

## When to write a postmortem

Reserve a deeper postmortem for failures that are all three of subtle (hard for a veteran to derive), systemic (a gap in tests, tooling, or convention — not a typo), and costly to rediscover. Ordinary bugs get a note, not a postmortem.

## Safety

The verifier opens notes read-only, never executes project code, and treats note content as untrusted text. Verify its test-path claims against the live repo before acting — a path string is not proof the behavior holds. The `Proved:` line records the ritual, but a lying author can still write a fake one; review is the backstop.

The binding and staleness checks are existence checks, not proofs. An anchor that appears in a file does not mean the test passes, and a `Proved:` line cannot be verified without running the suite, which this skill deliberately does not do. Treat a green run as "the tree is internally consistent", not "the fixes work".

## Changing the verifier

Run the suite after any change to `scripts/`:

```bash
python regression-notes/tests/test_verify_notes.py
```

New checks must be **warnings** unless they are provably free of false positives across languages and layouts. Errors are reserved for structural facts the grammar fully determines (a missing file, a malformed header, an unresolvable pointer). Anything shaped like a language convention — test naming, symbol resolution, module layout — is a warning with an opt-out flag, because a check that misfires on a correct tree teaches people to ignore the gate. Keep optimizations generic: no language list, no required tooling beyond stock Python (git is an optional fast path with a walk fallback), no per-project config.
