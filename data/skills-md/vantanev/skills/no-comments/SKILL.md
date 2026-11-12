---
name: no-comments
description: "Spawn Comment Sicko on the scoped diff, act on accepted findings, and offer encodings for claimed constraints."
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

# No comments

Spawn Comment Sicko. Act on accepted findings.

Authoring agents defend comments. Defer to Comment Sicko's fresh perspective.

## Scope

Use the caller's files or diff. Otherwise pin the fixed point the caller named (a commit SHA, branch name, tag, `HEAD~5`, etc.); without one, ask in chat.

Capture the diff once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty before spawning; a bad ref or empty diff fails here, not inside the Sicko.

## Steps

1. Read `references/comment-sicko.md`. Spawn `Agent` with `subagent_type: "general-purpose"` and that file verbatim as the prompt, followed by the scope. Start it with a fresh context window. Set the subagent's effort one step below your own. If you do not know your effort, do not set it.
2. Inspect its report and diff. Reject application-code edits, scope escapes, exception-protected deletions, misstated `MUST KILL` reasons, and flags that treat kept intentional code as guilty. Reshape flags on our-code surprises stay actionable. Do not restore those comments. A keep survives only with proof it is about something we cannot change. Audit missed scoped lint and TypeScript suppressions. Correctness or safety suppressions stay actionable `MUST KILL`s. Restore deletions only with exact exceptions and scoped proof. Before accepting thin `IMPORTANT` or `do not remove` kills or keeps, run the Sicko's Trace on their symbol. If a kill is ambiguous, do not restore. If a keep is refuted or still ambiguous, delete it. Revert and rerun one rejected report with the failure named. Reject a second, report it open, and fail `/no-comments`.
3. Fix trivial accepted flags directly by deleting a dead path, dropping a parameter, or using the real API. If any fix needs a shape, sketch once for the accepted set and surrounding code: write the caller's usage first, then types and signatures with `not implemented` bodies. Sketch two structurally distinct shapes and keep the one that hides more behind a smaller public surface. Stop at the sketch. Step 4 implements.
4. Implement the smallest root-cause fix in scope against the sketch. Remove every named workaround. Fix the cause where it lives: a guard that silences a symptom is not a fix. Redesign as if the requirement had existed from day one. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. Neither rule authorizes widening the fence nor fixing instances outside it.
5. Constraint comments say `do not remove`, `do not change wording`, or `talk to X before changing`. Leave keeps about things we cannot change. Offer the cheapest in-scope type, runtime, test, or CI lint. Ask in chat and wait for approval. Unattended runs require caller pre-approval. If approved, encode then delete. Otherwise delete, report the constraint open, and sketch out-of-scope work.
6. Report the deletion count, restored comments, reruns, sketch, fixes, encoding offers, encodings, unenforced constraints, and other open work.
