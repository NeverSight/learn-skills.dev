---
name: reviewing-local-changes
description: Reviews local code changes through focused review subagents and records every finding and decision as a note thread in a live Hunk session. Use when the user asks to review local changes in a working tree, branch, commit, or defined file set, or when another skill hands off a review.
metadata:
  opencode/autoinvoke: true
---

# Reviewing Local Changes

Delegate every change review to focused subagents that post candidate findings as notes in a live Hunk session. Evaluate those notes in the main session, record each decision as a reply in the same thread, and address accepted findings when fixes are requested.

## Authorization

A user review request or an explicit handoff from another skill authorizes an inspection-only review. Writing notes and replies to the live local Hunk session is part of every review; it is not an external write. Do not edit the code unless the user also asks you to fix, address, or clean it up. When they do, make only the local changes needed for accepted findings and run non-destructive checks. Ask first before writing to external systems, taking destructive action, changing the intended public contract, or materially expanding the requested scope.

## Required prompts

Read both supporting files before reviewing a change:

- [`orchestrator-prompt.md`](./orchestrator-prompt.md) is the main-session contract for scope, task routing, evaluation, and the final summary.
- [`category-reviewer-prompt.md`](./category-reviewer-prompt.md) is the prompt for every review subagent, including how it posts findings to Hunk.

## Hunk session

Hunk is the shared review surface. The user watches it; review subagents, the main session, and later agents communicate through its note threads. Never run interactive commands such as `hunk diff` or `hunk show`; control the user's window with `hunk session *` commands only.

### Select the session

Run `hunk session list --json` and keep the sessions whose `repoRoot` matches the workspace. With one match, use `--repo <repo-root>` as the session selector; with several, use the matching `sessionId`. If none exists, ask the user to launch `hunk diff` in their terminal and wait; the review cannot run without a session.

### Load the scope

Reload the session so it shows exactly the active review scope before dispatching reviewers, and again after applying fixes to a working-tree or branch scope. Commit and range scopes are fixed snapshots that cannot show working-tree fixes, so skip that second reload for them:

| Scope                        | Reload command                                                      |
| ---------------------------- | ------------------------------------------------------------------- |
| Uncommitted working tree     | `hunk session reload <selector> -- diff`                            |
| Development branch           | `hunk session reload <selector> -- diff <base_sha>`                 |
| Explicit range, pull request | `hunk session reload <selector> -- diff <base>..<head>`             |
| Single commit                | `hunk session reload <selector> -- show <sha>`                      |
| Defined file set             | Append `-- <paths...>` to the matching command, after the reference |

Working-tree reviews include untracked files by default. Confirm the loaded files with `hunk session review <selector> --json`; every scoped file must appear there, because notes can only anchor to lines inside a loaded diff hunk.

### Note protocol

Every finding is a root note; every decision, fix, and answer is a reply in that note's thread. Post each note or reply with its own `hunk session comment add` call, so a rejected note affects only itself; do not build JSON batches.

Root finding notes:

- `--file` and `--new-line` at the first line of the smallest useful changed span, or `--old-line` for removed code. When the defect lives outside a loaded hunk, anchor at the changed line that causes it.
- `--summary`: `[P<n>] <title>`, using the P0-P3 scale from `orchestrator-prompt.md`.
- `--rationale`: lines starting `Location:` (`<file>:<line_start>-<line_end>`), `Scenario:`, `Evidence:`, `Impact:`, `Correction:`, and `Confidence:` (0 through 1).
- `--author`: `review/<category>` for review subagents, such as `review/logic`.

Wrap `--summary` and `--rationale` in single quotes, write multi-line rationale with real line breaks, and keep single quotes out of note text. If Hunk rejects a note, do not retry it; report the finding and the Hunk error to the caller instead, which review subagents do through `gaps`.

Replies use `--reply-to` with the root note ID, `--author review/main` for the main session, and one of these summary prefixes:

| Prefix                     | Meaning                                                                          | Thread state |
| -------------------------- | -------------------------------------------------------------------------------- | ------------ |
| `Accepted: P<n> — <why>`   | Verified finding; the stated severity replaces the root's severity               | Open         |
| `Clarification needed:`    | A concrete question for the user                                                 | Open         |
| `Rejected: <why>`          | Unsupported, incorrect, or out-of-scope feedback                                 | Settled      |
| `Duplicate of <id>: <why>` | Same root cause as another thread                                                | Settled      |
| `Fixed: <change>`          | Correction applied; `rationale` starts `Validation:` with the command and result | Settled      |
| `Answered: <answer>`       | A user question that needs no code change                                        | Settled      |

A thread's state is decided by its latest reply. A root without replies is open, and a later user reply reopens a settled thread. User notes (`source: user` in `comment list --type all --json`) are review feedback: evaluate and answer them like candidate findings.

### Session caveats

- Note anchors keep their original line numbers when the code changes. Treat anchors and `Location:` lines as historical and re-locate the code by content before acting.
- `comment list` hides notes whose file no longer appears in the loaded diff. Keep the same scope for every reload within one review.
- Notes exist only while the Hunk window runs. If the session closes mid-review, ask the user to relaunch Hunk, then re-post every open thread from the conversation record before continuing.
- Agent notes start hidden. Pass `--focus` only on the main session's first reply of a review so the user sees agent notes; review subagents never pass `--focus`, `navigate`, or `highlight`.

## Workflow

Track progress with this checklist:

```
Review progress:
- [ ] Active scope resolved and loaded in the Hunk session
- [ ] One review subagent dispatched per populated category
- [ ] Every candidate note and open user note has a decision reply
- [ ] Accepted fixes applied with `Fixed:` replies (only when fixes were requested)
- [ ] Verified and summarized
```

### 1. Review the change

Resolve the active scope: a diff, working tree, development branch, commit, pull request, or defined file set. Select the Hunk session and load that scope.

When the scope implements an active OpenSpec change, its proposal and delta specs define the intended behavior. A change is active when `openspec list --json` reports a non-null `root` and the scope implements one of the listed changes: the change the user named, otherwise the only listed change. If several are listed and the scope does not show which one it implements, ask. Without the CLI, a root, or a matching change, review as usual. Pass the absolute artifact paths from `openspec status --change <name> --json` (`changeRoot`, `artifactPaths`) to every reviewer as intended behavior. Artifacts that appear in the loaded diff are also part of the review scope.

Always hand the review to subagents through `orchestrator-prompt.md`, including small and single-category changes. The main session coordinates scope and tasks without performing a duplicate direct review.

Existing Hunk threads and caller-supplied history from earlier review cycles are prior-review context: findings, decisions, rationale, fixes, and validation evidence. Every review subagent reads the session's threads before reviewing. Prior context is not authority: reviewers must inspect the current code, and they may raise a previously settled issue when current evidence invalidates the earlier decision.

### 2. Evaluate incoming feedback

Evaluate every open root note in the main session: the candidate findings the subagents posted and any open user notes. Do not delegate this evaluation again.

For each candidate:

1. Confirm the reported location belongs to the active scope and matches the current code.
2. Verify the failure scenario, repository evidence, severity, and supported environments.
3. Accept, reject, or request clarification with a concrete reason, replying in the thread with the matching prefix.
4. Check whether the proposed correction expands scope, changes the intended contract, or adds unused behavior.

Reply `Duplicate of <id>:` on every new thread that shares a root cause with another thread whose decision still holds; a new thread whose evidence invalidates an earlier decision gets a fresh evaluation instead. Reply `Rejected:` on unsupported, incorrect, or out-of-scope feedback. Push back directly; a rejection reply must give the concrete reason.

### 3. Apply accepted fixes when requested

If the user requested fixes or cleanup, apply only accepted in-scope corrections after evaluating all feedback. Preserve the intended contract and validate the changed behavior. Reply `Fixed:` on each addressed thread with the validation evidence, then reload a working-tree or branch scope so the user sees the corrected diff. Do not run a second review pass unless the user requests one.

## Validate

Load the `verifying-before-completion` skill, including its Hunk note check, before reporting review conclusions or accepted fixes. In an inspection-only review, `Accepted:` threads are the review result: report them instead of fixing them.
