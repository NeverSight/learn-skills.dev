---
name: pr-apply-changes
description: Apply changes from the current conversation, an implementation plan, review feedback, issue reports, or PR follow-up work, then integrate them into the right commits. Use when the user asks to apply requested changes, implement an agreed plan, fix issues found in review, address issue feedback, or fold follow-up fixes into a branch or PR.
---

# PR Apply Changes

## Hard Rules

- Ask at most once. Combine necessary questions, assumptions, risk notes, and
  confirmation into a single prompt.
- Preserve unrelated user changes. If the worktree is dirty, separate existing
  changes from your edits before committing or rewriting.
- Keep fixes scoped to the requested change unless the smallest correct fix
  requires a wider adjustment.

## Identify The Change

Resolve what needs to change in this order:

1. Specific edits the user requested in the current message.
2. The latest agreed plan or checklist in the conversation.
3. Issues, bugs, review comments, CI failures, or acceptance gaps the user wants
   fixed.
4. If still unclear, inspect the relevant code, diff, issue context, and project
   guidance, then state the inferred change.

If the change source is ambiguous enough that different choices would produce
different code, ask one consolidated question. Otherwise proceed with a clear
assumption and mention it briefly.

## Fix Strategy

For issue fixes, compare:

- `best fix`: the solution the code should have if reviewed as final.
- `quick fix`: the smallest localized change that removes the symptom.

If they are the same, proceed. If they conflict, ask once with the tradeoff. For
features introduced in the current branch or PR, present the best fix as the
preferred option.

Then classify implementation risk:

- `trivial`: localized, mechanically clear, and low-risk. Apply it immediately.
- `standard`: requires normal code understanding but stays within existing
  architecture. Apply the selected coherent fix.
- `architectural`: changes module boundaries, data flow, storage shape, public
  contracts, migration behavior, or broad test strategy. Explain the best fix,
  tradeoffs, and files likely affected before editing.
  When issues are mixed, apply trivial and standard fixes but stop before
  architectural changes unless the user already approved that direction.

## Implementation

1. Read local project guidance and the files touched by the requested work.
2. Implement the minimal complete change using existing patterns.
3. Update tests, fixtures, docs, generated files, or snapshots only when they are
   part of the behavior or review expectation.
4. Run the smallest meaningful validation for the changed surface.
5. If validation cannot run, say exactly what blocked it and what risk remains.

## Commit Integration

After validation, integrate the changes into the branch history unless the user
explicitly asked to leave them uncommitted.

Choose the destination for each change in this order:

1. If a current-branch commit introduced the issue, regression, or directly
   related scope, fold the change into that commit.
2. If the change improves or fixes a feature introduced in the current branch or
   PR, fold it into the commit that introduced that feature.
3. If no logical current-branch commit owns the change, make a new commit.

Resolve the base from PR metadata, branch configuration, or repo context; if you
infer it, say what you inferred. Branch commits are commits reachable from `HEAD`
and not from that base. Never rewrite commits reachable from the base.

Safe rewrite: all branch commits and affected rewrite-range commits are
user-authored. Execute safe rewrites without confirmation, even if pushed. If any
are not user-authored, warn and get one confirmation before rewriting.

Before rewriting history, state one concise fold plan:

- base branch or base commit
- commits that will be rewritten
- where each new change will land
- whether the rewrite is safe, including author and base-branch checks
- whether a backup branch or equivalent recovery point will be created

Stop only if base or scope ambiguity risks rewriting base history.

## Response Shape

When finished, report what changed, how it was integrated into commits or the
pending fold plan, validation run and result, and any skipped architectural work,
rewrite risk, or remaining follow-up.
