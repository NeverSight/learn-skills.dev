---
name: work-report
description: >
  Writes or overwrites WORK-REPORT.md at the working tree root - session self-report (goal,
  problem/solution, follow-ups, suggested skills, abandoned) a reviewer or later session reads
  instead of re-deriving intent from the diff. Use for "work report", "checkpoint this",
  "hand off", "write up what we did". Offer proactively - asking first - when work is finished:
  "done", "ready to commit", "wrapping up", handoff to another agent.
allowed-tools: Bash(git rev-parse:*), Bash(git branch:*), Bash(printenv CLAUDE_CODE_SESSION_ID), Bash(grep:*), Read, Write, Edit
---

Write the **work report**, `WORK-REPORT.md` at the working tree root: what the diff cannot show, for a reviewer or
fresh session. One per tree, overwritten each run, so it reads as current state. Any directory (git or not, worktree or
not), any shape of work (commits, loose edits, cross-repo changes, editor settings).

Follow the steps in order. Stop only on an unwritable path; missing `git`, no repo, or a quiet session still get a
valid report.

## Never write without being asked

Self-activated (user signalled work finished without naming the report): offer in one sentence, wait for a go-ahead.
You may read the existing report first so the offer carries the Step 2 question. An explicit invocation
(`/work-report`, "write the work report") is the go-ahead.

## Scope of "the work" = this chat session

Report what you did this session. Never infer it from `git diff` or `git log`: git already records that, and
reconstruction loses the intent. A free-text note passed with the invocation sets emphasis (that topic leads each
section), never narrows scope.

## Altitude - keep every entry the same size

Goal and nested bullets: 1-2 sentences. List items: one sentence plus optional parenthetical. No paragraphs; the reader
scans.

## Step 1 - Locate the report

`<root>/WORK-REPORT.md`, root from `git rev-parse --show-toplevel`; outside git, the current directory.

## Step 2 - Read the existing report and build on it

An existing report (maybe another agent's) may belong to other work. Ask the user when its *Goal* is clearly unrelated
to this session, or when both its session id and branch differ from the current ones. A matching session id waives the
branch test: one session may build variants on several branches. A foreign report is often a deliberate handoff, so
name what a fresh start drops: "WORK-REPORT.md may belong to other work (*Add retry to CSV export*, branch
`feat/export-retry`). Extend it, or start a new report and drop its 2 open follow-ups and 1 `[ignored]` entry?"
Self-activated: fold this into the one-sentence offer. On "start new", write from this session alone; skip the rest of
this step.

Otherwise extend, never regenerate: carry *Problem → Solution* and *Abandoned* entries with tags unchanged, widen the
*Goal* if this session did, and disposition every carried follow-up (dropping keeps the report bounded across resumed
sessions):

| Carried follow-up | Where it goes |
| ----------------- | ------------- |
| Done, after a changed course, a fork taken, or a check the diff cannot show (pipeline run inspected, email sent, console flag toggled) | *Problem → Solution* |
| Done, what it took recoverable from the diff | dropped, no trace |
| Rejected after evaluation | *Abandoned*, tagged `[considered]` |
| Dismissed by the user, or by a rule the user set (Step 4, *Abandoned*) | *Abandoned*, tagged `[ignored]` |
| Still open | kept verbatim |
| Obsolete, goal moved | dropped, no trace |

## Step 3 - Offer the gitignore entry (first run in a repo only)

Skip outside git, or when Step 2 found a report (the first-run test; stops re-asking after a decline). Otherwise run
`grep -qxF '/WORK-REPORT.md' <root>/.gitignore` with the Step 1 root. Present: say nothing. Absent: say the report is a
local artifact normally kept out of the branch diff, ask to add it, continue to Step 4 either way. On yes, append to
`<root>/.gitignore` (trailing newline first if missing):

```text
# Work report (work-report skill) - git add -f to commit it
/WORK-REPORT.md
```

Keep the leading slash: it anchors to the tree root, so a same-named file deeper down is not ignored, and still covers
every worktree.

## Step 4 - Compose the report

Only what the diff cannot show: intent, reasoning, verification, next steps. Never restate commits or changed files.
Reference artifacts (PR/issue URLs, file paths, ADRs), never paste them. Never reproduce the value of an API key,
password, token, credential, or PII; note only that it exists and where (other agents read the report; it may be
committed).

**Header** - exactly `# Work report`, then two identifier lines, one fact each, never merged. *branch* = where the work
started: current branch on a new report, carried unchanged when extending. *session id* = last writer. Readers grep
these lines and their fallback values:

```text
# Work report

- **branch:** <on a new report git branch --show-current, `(detached)` on a detached head, `(no git)` outside a repo or with git unavailable>
- **session id:** <printenv CLAUDE_CODE_SESSION_ID, or `unknown` if unset>
```

Then five `##` headings, in order, each always present, `- none` under an empty one:

- **Goal** - what this work set out to do.
- **Problem → Solution** - numbered list. Entry when: a first attempt failed and you changed course; you took a real
  fork (≥2 viable options); or a follow-up the report already listed was finished (by anyone, this session included)
  and closing it is not recoverable from the diff or was itself a fork. Record problem and working approach, or fork
  and why. A finished follow-up failing this test just leaves *Follow-ups*. Fold verification the diff, PR and CI
  cannot show (retry path clicked through with the proxy down, a pipeline run inspected) into the **Solution** it
  verifies; when the verified work has no entry, the check is its own entry (**Problem** = what needed proving,
  **Solution** = the check and its result). A green test run is not an entry. Each changed course is its own entry,
  even inside a larger fix, and the failed attempt also goes to *Abandoned* as `[tried]`. Entry shape:

  ```text
  1.
      - **Problem:** description
      - **Solution:** description
  ```

- **Follow-ups** - flat list of what the next session or reviewer picks up, each tagged:
  - `[question]` - unresolved decision or unknown, phrased as a question.
  - `[action]` - concrete work, imperative. Believed working but never exercised = `[action]` naming the settling
    check. Valid with no owner.

  Never here:

  - Gap already decided against (accepted risk, platform out of scope): *Abandoned* `[considered]`, or `[ignored]` if
    the user, or a rule the user set, dismissed it.
  - Shipping (commit, push, PR, merge, tag, release): the user's move, even if the session ends uncommitted.
  - Invoking a skill or slash-command: state the outcome (`[action] Add regression tests for the retry path`), never
    the tool (`[action] Run /test-writer`).
- **Suggested skills** - means for an outcome-only follow-up. List a skill only if it advances an `[action]` item, as
  `/skill - which follow-up it advances`.
- **Abandoned** - what the next agent should not re-walk: dropped approaches, and carried follow-ups later rejected.
  Numbered, one sentence plus reason:

  ```text
  1. [tried] implemented or attempted, then reverted - why it was backed out
  2. [considered] evaluated and rejected without building it - why it was rejected
  3. [ignored] dismissed by the user or a rule the user set - the user's reason, "user's call", or the rule and its source
  ```

  `[ignored]` = user veto: later runs never re-raise, re-tag or re-offer it, except as the reopen check below. It needs
  the user's authority, given one of three ways:

  - Directly: an explicit dismissal this session ("ignore that", "skip the Safari case", "don't bother").
  - Through a rule the user stated or confirmed this session (a review bar such as "fix blockers only"), or one written
    in the repo's instruction files (AGENTS.md, CONTRIBUTING.md), applied to the item. Cite the rule and its source:
    `- non-blocker under user's bar "blockers only" (this session)`, or the file path. One entry per item.
  - Carried from the existing report.

  A rule you cannot cite, a skill's default the user never confirmed, or your own rejection is `[considered]` with your
  reason. Silence, an unanswered `[question]`, or a deferral ("not now", "later") keeps it in *Follow-ups*; a deferral a
  ticket or doc already records gets no entry. Never invent the user's reason or rule.

  The user lifts `[ignored]` by asking for that work again, or by changing or withdrawing the rule, which lifts every
  entry citing it. Reopen check: when a defect or failure this session shares a root cause or failing scenario with an
  `[ignored]` entry, keep the entry and add `[question] Does <defect> reopen [ignored] <item>?`. The user decides.

Example:

```markdown
# Work report

- **branch:** feat/export-retry
- **session id:** 3f1c9a2e-7b44-4d0e-9c1a-5e8f2b6d7a10

## Goal

Make the CSV export survive a dropped connection by retrying failed chunk uploads.

## Problem → Solution

1.
    - **Problem:** Retrying the whole export duplicated rows already written.
    - **Solution:** Retry per chunk with an idempotency key; verified by killing the proxy mid-export and diffing the output.

## Follow-ups

- [question] Should the retry limit be configurable per tenant?
- [action] Add regression tests for the chunk retry path.

## Suggested skills

- /test-writer - Add regression tests for the chunk retry path.

## Abandoned

1. [tried] Exponential backoff in the HTTP client - it retried non-idempotent POSTs elsewhere in the app.
2. [considered] Streaming the export over websockets - too large a change for the bug.
3. [ignored] Safari download filename encoding - user's call.
```

## Step 5 - Write the file and report back

Write `<root>/WORK-REPORT.md`, reply with the path and a one-line summary, naming any reopen `[question]`. If gitignored
(Step 3), note a reviewer on the PR needs a deliberate `git add -f WORK-REPORT.md`.
