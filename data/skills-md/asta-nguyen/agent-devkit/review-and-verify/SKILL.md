---
name: review-and-verify
description: Use when a user asks to review the diff, check the work, run or verify tests or builds, confirm a bug or feature is complete, or before declaring implementation or documentation done.
---

# review-and-verify

This skill reports findings; it does not fix them. A `Status: fail` returns to
`implement-task`'s `## After implementation` fix loop (or to
`systematic-debugging` for a bug). The only edits made here are the archive move
and link rewrites in `## Archive a change` and `Execution: complete` on a
legacy plan; never edit code, wiki, or `Progress`.

## Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you have not performed a fresh verification check in this message, you
cannot claim it passes. Previous runs are not evidence.

## Verification gate

Before claiming any status: **identify** the command or repeatable procedure that
proves the claim; **run** it fresh and complete; **read** the full output,
including failures; **verify** it confirms the claim, stating the actual status
with evidence either way; only then make the claim.

Before final completion, run every repository-mandated full verification command
in `AGENTS.md`, manifests, or CI configuration; targeted checks do not replace
it. If none is established, report that limitation.

Before reviewing requirements, read the active design and plan, the change's
`decisions.md`, and the other sources in `implement-task`'s
`## Decision sources`. A persisted decision is requirement evidence but does not
override a pending approval gate; conversation recall is not review evidence.
Mark completion only when this is the final review, every task is implemented
(`Progress: done` with a `Result:` this review confirms with fresh evidence), and
every required verification passes. A task with no `Progress` line is not
complete: report a blocker so `implement-task` backfills it
(`../using-devkit/references/legacy.md`). Approval status alone is not
completion evidence.

A passing final review marks a legacy plan complete as
`../using-devkit/references/legacy.md` describes, and runs
`## Archive a change` for a change folder.

Verify the edit or the archive before reporting `Status: pass`. If work or
required verification remains, leave the plan or change open and report the gap
under `Spec gaps`.

## Archive a change

Run this in the change's branch, after the code checks pass and before any
commit. Archive never merges or edits wiki requirements. With a delta, confirm
every block is in the after-merge state `document-wiki`'s `## Merge a task delta`
defines, including Sources, retired IDs, and the merge marker. If
documentation is unfinished, report a blocker (`Status: fail`, `Next:
implement-task`, which calls `document-wiki`'s `## Task updates`); do not move
the folder yet.

**Move and relink.** Before moving, compute every link that will change: relative
links in the folder's files that point outside it, and links anywhere in the
repository that point into it (search all files, including ignored `docs/`
paths). Rewrite links in `docs/agent-devkit/` (the index entry moves from
`## Changes` to `## Archived changes`) and in files this change already
modifies. A link from `docs/llm/` into a change folder breaks the wiki boundary
and fails the review. For any other file, stop before moving and report the file
and link for the user to decide. Confirm every new target will exist, move the
folder to `changes/archive/<same name>/`, rewrite the links, and verify they
resolve. If any check fails, move the folder back, undo only this archive's link
edits, keep `Status: fail`, and report the broken links. The change is complete
only when the moved folder, index, and every rewritten link are verified.

After a rebase that touches `docs/llm/` or the change folder, review again; an
earlier pass does not count.

## Git safety invariants

- Treat existing working-tree changes as user-owned: inspect `git status --short`
  and the diff before changing or discarding anything.
- Never run `git reset --hard`, `git clean -fd`/`-xdf`, `git checkout -- <path>`,
  `git restore` that overwrites work, or broad delete commands to remove user
  changes unless the user explicitly authorizes the exact target and command.
- Never force-push or rewrite remote history without an explicit request naming
  the remote, branch, and intended rewrite. A request to finish, clean up, or
  fix the branch is not authorization.
- Prefer recoverable actions; leave commits, pushes, and other remote operations
  to the user unless explicitly requested.

## Claims vs evidence

| Claim | Requires | Not sufficient |
|---|---|---|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Repeat original symptom check: passes | Code changed, assumed fixed |
| Requirements met | Line-by-line checklist vs spec, plan, and persisted decisions | Tests passing alone |
| Wiki updated | Validator passes, claims match source | "Page edited" |

## Diff review

### Trace changed callers

With OpenEZ, call `diff_context` (`staged: true`, a `ref`, or neither for the
working tree) and record changed symbols and callers. It may omit untracked
files, so always run `git status --short` and search changed symbols plus string,
route, config-key, and case variants with FFF multi-pattern grep or `rg`,
including untracked paths. Without OpenEZ, derive tracked symbols from
`git diff HEAD` (no commit: `git diff --cached` plus `git diff`). A branch review
adds `git diff <target-branch>...HEAD` (the PR's target, or the merge branch; ask
if unknown). Read untracked files and every listed caller. For a large diff, run
OpenEZ `index_workspace` (`mode: "incremental"`) on the registered workspace
first.

Review the diff for:

- **Correctness** — logic matches the approved design and persisted decisions
- **Stale documentation** — wiki pages or comments contradicting new behavior
- **Accidental scope** — changes outside the approved plan
- **Missing error handling** — edge cases, error paths, cleanup
- **Protected boundaries** — trust-boundary validation, security, accessibility,
  and data-loss prevention stay intact
- **Conventions** — changed code follows the rules in `AGENTS.md` or
  `CONVENTIONS.md` whose scope matches the changed files (most specific wins);
  cite `path:line`. With none recorded, report `not-applicable`; do not fail.

Compare the implementation and fresh evidence with every approved edge case.
Report every blocker, non-blocker, spec gap, and complexity finding with
`path:line`, the problem, and why it matters (a bare filename is not
actionable). Required behavior that diff, source, tests, or fresh output cannot
establish goes under `Spec gaps`:

```text
cannot verify <requirement> — needs <specific evidence or command>
```

An unverifiable required behavior keeps the status at `fail`.

For a task that changes `docs/llm/`, run the validator from the installed
`document-wiki` skill:
`node "<document-wiki-skill-directory>/scripts/validate-llm-wiki.mjs" "<target-repository-root>"`
with absolute paths. If it is missing, cannot run, or reports errors, keep
`Status: fail`; never run it against the devkit source repository instead. It
covers paths, links, legacy `[[...]]` links, and requirement syntax; also check
yourself for duplicate behavior within one prefix, placeholder text, and whether
each `Evidence:` supports its statement.

Before the final result, classify wiki impact, even for a bug fix: `yes` when the
change alters documented behavior or leaves a relevant page incomplete (list the
pages), `no` only after inspecting the page and source, `not-applicable` when the
repository has no `docs/llm/` (never create one), `unknown` when it cannot be
established. A page that contradicts the change, or missing coverage for affected
behavior when `docs/llm/` exists, is a blocker: report it, and `implement-task`
calls `document-wiki`'s `## Task updates` before the next review. Unrelated gaps
are optional findings. In the result block's `Evidence`, name the check for every
listed caller, or state `Verification limit: <caller> — <reason>`.

### Independent reviewer

Dispatch when spawn and exact diff target exist; else review directly.
Brief: design/plan/decisions; exact target (`git diff HEAD` + untracked paths, or
branch range); omit conversation; explicitly include "Do not edit files or delegate further."
OpenCode: `task` with `subagent_type: "explore"`. Disable inherited history
when supported (Codex: `fork_turns: "none"`); tools may edit. Require
path:line, problem, impact; no Status. Verify blockers, run checks, write result.

## Complexity pass

Report each behavior-preserving simplification with a file reference and one
label: `delete:` (dead code or flexibility with no approved requirement),
`reuse:` (duplicates existing repository behavior), `stdlib:` or `native:` (a
named standard-library or platform feature replaces custom code or a
dependency), `yagni:` (abstraction with no current use), or `shrink:` (a smaller
clear implementation, same behavior and checks). An in-scope finding is a
blocker: `Status: fail` until `implement-task` fixes it; report an out-of-scope
one as a non-blocker. If none exist, say the pass found none. Give no line-count
score.

## Review result

Start the final response with these three lines, in the user's language and the
format from `using-devkit`:

```text
Next: <skill or action, or none>
Waiting on: agent | user — <exact approval, answer, or action needed>
Done when: <observable result that completes the next step>
```

On `fail`, `Next` is `implement-task` (or `systematic-debugging` for a bug) to
fix the blockers; on `pass`, it is the user's step (review, then commit or PR).
Run the available setup and checks first; if only the user can run a
required check, give app-level steps and the expected result. Add one or two
sentences on what changed and was checked, then end with this result block,
repeating no finding in prose:

```md
Status: pass | fail
Evidence: <`check → result` items joined by " · ">
Blockers: <path:line — problem>
Non-blockers: <findings or limitations, one line each>
Spec gaps: <missing spec, plan, or decision requirements>
Wiki impact: yes | no | not-applicable | unknown — <pages or reason>
```

Omit empty `Blockers`, `Non-blockers`, `Spec gaps`. For `yes`, add `action:
<updated / required update>`.

Use `fail` when any blocker or spec gap remains; a passing check does not
override a failed requirements or diff review. A task is complete only when the
result says `Status: pass` and code, documentation, and verification output
agree. Never turn a failed blocker into a
non-blocker. Leave the verified tree to the user; commit only as `using-devkit`
allows, never failing or unverified work. For external review feedback, read
`references/receiving-code-review.md` first.

## Red flags

| Thought | Reality |
|---|---|
| "Review can fix it while it is here" | Report it; the fix goes through `implement-task`'s loop and a new review. |
| "One more fix attempt before reporting" | Three failed attempts on one blocker end the loop. |
| "It should pass" / "it looks correct" | Neither is evidence; run it. |
| "Approval is in the chat history" | Only this conversation, an `Approved:` line, a handoff's `Approval:` line, or `tasks.md`'s `Status: approved` counts. |
