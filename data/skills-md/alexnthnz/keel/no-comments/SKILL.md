---
name: no-comments
description: "Spawn critic with the comments lens, carry out accepted kills, fix accepted findings, and offer encodings for claimed constraints."
disable-model-invocation: true
---

# No comments

Other keel skills named here sit beside this one at `${CLAUDE_SKILL_DIR}/../<name>/SKILL.md`, and a principle at `principle-<name>`. The Skill tool refuses them, so read the file and follow it.

Spawn critic with the comments lens. Act on accepted findings.

Defer to critic's fresh perspective. critic is read-only, so it sentences comments and you carry out the kills.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch, default `main`, including the working tree.

## Steps

1. Spawn an Agent call with `subagent_type: "keel:critic"` and the comments lens. Pass the scope and the keel skills directory (`${CLAUDE_SKILL_DIR}/..`). Pick each subagent's effort for the job, per the Subagents section of the **lead** skill. Do not restate its rules.
2. Inspect its report. Reject scope escapes, exception-protected kills, misstated `MUST KILL` reasons, and flags that treat kept intentional code as guilty. Reshape flags on our-code surprises stay actionable. Delete those comments. A keep survives only with proof it is about something we cannot change. Audit missed scoped lint and TypeScript suppressions. Correctness or safety suppressions stay actionable `MUST KILL`s. Spare a sentenced comment only with exact exceptions and scoped proof. Before accepting thin `IMPORTANT` or `do not remove` kills or keeps, trace their symbol or run `/keel:why` on it. If a kill is ambiguous, delete it. If a keep is refuted or still ambiguous, delete it. Then delete every accepted kill yourself. Rerun one rejected report with the failure named. Reject a second, report it open, and fail `/keel:no-comments`.
3. Fix trivial accepted flags directly by deleting a dead path, dropping a parameter, or using the real API. If any fix needs a shape, run `/keel:architect` once for the accepted set and surrounding code. Stop at the sketch. Architect shapes. Step 4 implements.
4. Implement the smallest root-cause fix in scope. Remove every named workaround. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. The **principle-fix-root-causes** and **principle-redesign-from-first-principles** skills guide intent only. Neither authorizes widening the fence nor fixing instances outside it. Never bolt on symptom guards.
5. Constraint comments say `do not remove`, `do not change wording`, or `talk to X before changing`. Leave keeps about things we cannot change. Offer the cheapest in-scope type, runtime, test, or CI lint. Wait for interactive approval. Unattended and eval require caller pre-approval. If approved, encode then delete. Otherwise delete, report the constraint open, and sketch out-of-scope work.
6. Report the deletion count, spared comments, reruns, architect sketch, fixes, encoding offers, encodings, unenforced constraints, and other open work.
