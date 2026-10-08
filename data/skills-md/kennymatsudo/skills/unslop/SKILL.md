---
name: unslop
description: >-
  Clean AI slop out of writing or code so a person wants to read it. Prose
  (docs, READMEs, plans, PR and commit text): put the point first, cut meta
  commentary, change history, and restatement, break up walls of text, rewrite
  generic headings, and fix AI sentence tells without losing a fact. Code (the
  branch diff): cut hollow tests, speculative abstractions, shims, defensive
  bloat, and dead code without changing behavior. Use for "unslop", "deslop",
  "unslop this doc", "make this readable", "clean up the AI slop", or before
  saving a doc or PR text an agent wrote. Skip chat replies. Use trim to only
  cut redundancy, and clean-up-comments for code comments.
---

# Unslop

You own a version of the target that a person would choose to read: the same facts for prose, the same behavior for code.

Slop is a set of moves, not a list of words. Each model generation swaps old tells for new ones, so the examples in the references show a move; fix every instance of the move, worded any way.

## 1. Scope and route

The target is what the user named: a file, a directory, pasted text, or the last document written in this session. With no target, use the branch diff. Find the default branch with `git symbolic-ref --short refs/remotes/origin/HEAD`, else `origin/main`, else `origin/master`. Take `git diff $(git merge-base HEAD <default>)` plus untracked files from `git status --porcelain`. The user can narrow it to uncommitted work (`git diff HEAD` plus untracked files) or staged changes (`git diff --staged`), or name a focus, such as the guards or the tests, which limits the pass to the matching checklist items. Tell the user the scope in one line before going further, such as "Scope: branch `foo` vs `origin/main`, 12 files".

Route each file:

- **Prose** (markdown, text, PR or commit text, pasted writing): read `references/prose.md`.
- **Code**: read `references/code.md`.

A diff with both gets both passes. When the target spans more than five documents, list them and ask the user which to rewrite first.

Done when every file in the target is routed and, for prose, the original is copied to a scratch file for the check in step 3.

## 2. Rewrite

Follow the loaded reference. Edit in place; for pasted text, write the new version in the reply.
Guardrails for both modes:

- Never invent a fact, number, reason, or example. Where the original is vague and you lack the specific, cut the vague sentence or flag it.
- Never change a claim because another file disagrees with it. Leave the claim as written and flag the conflict.
- Never change what code does. Report a bug you find instead of fixing it.
- Touch only the target. In a branch diff, touch only lines the branch added or changed.

Done when every checklist item in focus has been applied or ruled out.

## 3. Check

- **Prose.** Spawn one subagent on a mid-tier model with the prompt in `references/verifier-prompt.md`, the original, and the rewrite. Skip it when every edit was word-level, with no sentence cut, moved, or merged. For each claim it reports, restore it only if it is about the subject. A claim about the document itself (its status, freshness, upkeep, or history) stays cut.
- **Code.** Run the checks the repo already has for the touched files: typecheck, lint in check-only mode, and the affected tests. Revert any edit that breaks a check rather than patching around it.

Done when every verifier finding is restored or matches a planned cut, and every check passes or fails only where it failed before your edits.

**Reply for prose:** the line count before and after, then one line each for the biggest structural changes (sections moved, cut, merged, or split), any facts flagged as vague or contradicted elsewhere, and whether the doc should be split.

**Reply for code:** at most three sentences on what you removed, then each reported bug with `path:line`, then the check results.
