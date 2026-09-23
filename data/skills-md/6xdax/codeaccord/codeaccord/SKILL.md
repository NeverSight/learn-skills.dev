---
name: codeaccord
description: Investigate, implement, and verify software changes. Work directly on clear requests; discuss genuine decisions and present a concise, flexible agreement only when needed. Use for product requirements, bug fixes, refactors, configuration changes, and other codebase work.
license: MIT
metadata:
  author: CodeAccord contributors
  version: "0.6.0"
---

# CodeAccord

CodeAccord is a lightweight, conversation-first form of specification-driven development: establish the intended behavior before editing, then verify the implementation against it. The specification may be the user's clear request or a confirmed Accord; it does not require a separate plan or approval for every task.

The user's desired outcome and explicit constraints are authoritative. Their diagnosis, proposed files, and preferred implementation are hypotheses to evaluate. Agree when the evidence supports them. Disagree plainly when they are incomplete, incorrect, risky, or less effective than an available alternative.

Use the user's language unless project instructions require another language.

## Lifecycle

Use one continuous lifecycle, with an agreement only when the task needs a user decision:

```text
Explore [Inspect <-> Challenge] -> [Accord if needed] -> Build -> Verify
```

- **Explore:** Inspect the relevant project and challenge assumptions. For a clear request, this may be brief and lead straight to Build. When the user is discussing options or a material decision remains, keep exploring without editing product files.
- **Accord, when needed:** Make the recommended decision easy to review and confirm once before Build.
- **Build:** Complete the authorized implementation, tests, and necessary documentation.
- **Verify:** Check the delivered behavior against the request or accord and report evidence.

Do not split this lifecycle across separate planning and implementation skills. Infer the current stage from the conversation. The need for a decision, not task size or file count, determines whether to present an Accord. See **Choose the response path**.

## Explore loop

Explore is a loop, not two one-time steps. Move between **Inspect** and **Challenge** whenever new evidence changes the diagnosis, exposes a missing case, or invalidates a proposed solution.

During Explore:

- read code, configuration, logs, tests, history, documentation, schemas, and runtime evidence;
- run non-destructive diagnostics or reproductions that do not intentionally change tracked files or business data;
- discuss alternatives, answer the user's questions, and record decisions as they become clear;
- distinguish confirmed facts, supported inferences, user decisions, and unresolved questions;
- do not edit implementation files, tests, configuration, or product documentation.

An interim Explore response may answer a question, report findings, reject a premise, or explain what evidence is still missing. Keep it brief and proportional. Compare alternatives when they have a real tradeoff; do not invent options to fill a template. Do not mix a long investigation log into the recommended decision.

For a clear implementation request, proceed once the minimal specification below is clear and inspection supplies enough evidence to act. Do not wait for a separate signal to end Explore. If the user asked to discuss or a material choice remains, continue the read-only discussion. Once the decision is clear, present the concise Accord described below, unless the user has already authorized direct implementation.

## Minimal specification

Before Build, identify the observable expected behavior and how to check it, using the user's request and established project contracts as the source of truth. For a bug, distinguish current behavior from the expected behavior; for a new requirement, identify the requested result. Include any material boundary that must be preserved. This is the minimum specification for a direct-path task, even if no plan or Accord is output.

If a material part of the expected behavior cannot be derived, ask only for that missing decision. Do not invent a requirement or create a confirmation gate merely to restate a clear request. A direct-path task needs no separate specification file; when a recovery checkpoint is needed, record the authorized outcome there. Keep the intended behavior current if the user changes it, and verify the result against it.

## Classify the change

Choose the mode from evidence rather than keywords:

- **Product change:** The user wants new behavior or a deliberate change to existing behavior.
- **Bug fix:** Existing behavior violates an established contract, documented behavior, or reproducible expectation.
- **Mixed change:** Resolving the defect also requires a product decision or new contract.

When classification is uncertain, investigate first. Ask the user only when the distinction changes the desired outcome or compatibility contract.

## Choose the response path

Choose the path from the request and evidence, not keywords, file count, or a requirement to fill a plan.

**Direct path:** When the minimal specification is clear, no material user decision remains, and the user asked for the change, inspect enough to act, then implement and verify. Do not output a proposal or ask for an extra confirmation. This can include several files or callers. Give useful progress updates and a concise final report, without turning them into a mandatory pre-edit plan. A bug may need investigation before the root cause is known; uncertainty in diagnosis alone does not create a confirmation gate.

**Decision path:** When the user asks to explore first, the intended behavior is ambiguous, or a material product, compatibility, data, deployment, or other consequential choice remains, investigate and discuss the actual alternatives. Recommend a direction. Once the user has chosen a direction or asks to finalize it, present a scannable Accord if confirmation is still needed. If the user explicitly authorizes implementation of the concrete direction, continue without another gate. Size or verification difficulty alone does not require an Accord.

## Authorization boundary

A request to add, change, or fix behavior authorizes routine, reversible implementation of the clear requested outcome. A question or a request to discuss options does not. Do not invent a second approval gate when no material user decision remains.

Inspect before editing. On the direct path, proceed once evidence is sufficient to act safely. On the decision path, keep product files read-only while the direction or boundary is unresolved. Once the user confirms the concrete direction, implement it without asking again for routine engineering choices. If the user explicitly says to proceed immediately with that direction, no separate Accord output or confirmation is needed.

If new evidence reveals a material change to product behavior, public contracts, data, deployment, or another boundary the user did not authorize, explain the decision and ask only about that change. Do not silently treat answers to discovery questions as authorization to change unrelated behavior.

Committing, pushing, deploying, publishing, deleting durable data, and messaging external parties require their own authorization unless the user already requested them.

## Inspect

Before implementing or recommending a solution:

1. Read the nearest project instructions and inspect repository status without disturbing existing work.
2. Trace the real entrypoint, data flow, contracts, persistence, runtime processes, and tests relevant to the request.
3. For a bug, reproduce it or establish equivalent evidence from logs, tests, and code paths.
4. Separate observed facts, supported inferences, user decisions, and unresolved questions.
5. Ask only questions whose answers cannot be derived from available evidence and materially change the result.

Do not let the user's suggested file or diagnosis artificially narrow the investigation.

## Challenge

Evaluate the requested approach before adopting it:

- Identify false premises, missing cases, duplicated mechanisms, and avoidable compatibility costs.
- Prefer existing project patterns and the smallest complete change over parallel abstractions.
- Offer alternatives only when they represent a real tradeoff.
- Recommend a direction when evidence supports one; do not offload ordinary engineering decisions to the user.
- State uncertainty directly. Continue investigating instead of presenting a guess as a root cause.

For bugs, locate the earliest point where the state becomes incorrect. Fix that source rather than masking downstream symptoms with defaults, broad exception handling, or speculative compatibility branches.

## Form the accord

Use an Accord only on the decision path when a consequential direction or scope needs review. It is a clear decision summary in the conversation, not a form with mandatory headings. Do not emit it for a direct-path task merely because the change is large or touches multiple files.

**Lead with one complete sentence** that states the relevant cause or goal, the recommended action, the main affected area, and the expected result. A reader should understand the proposal from this sentence alone. Then expand only what helps the user judge it:

- For a bug: established cause and evidence, repair at the source, affected code or contract, and how the failure will be checked.
- For a new requirement: real alternatives and tradeoffs when they matter, recommended implementation, affected components and contracts, and observable acceptance.
- For a mixed change: combine the relevant parts without duplicating them.
- State material compatibility effects, risks, and remaining decisions. Label inferences rather than presenting them as confirmed facts.

Use the user's language for prose and any headings; the word Accord is not a required output title. Choose the order and headings that make this task easiest to scan; omit empty sections and investigation history. A concise paragraph or a few bullets may be sufficient. If a user-owned decision remains unresolved, keep discussing it instead of presenting an incomplete scope for approval.

If the user has already authorized the concrete direction, go straight to Build. Otherwise, ask for one confirmation of the concise Accord. After confirmation, implement without generating another plan.

## Update an accord

After an Accord is confirmed, explain a proposed material change in one complete sentence: what decision changes, why, and what result it affects. Add only the changed scope, risks, or acceptance checks needed for review. Do not repeat the whole Accord or require a fixed delta template. Ask for confirmation only when the change crosses an unapproved material boundary. If the user has already authorized that boundary, continue.

Keep unapproved proposed changes under checkpoint **Unresolved** when a checkpoint exists; they are not part of **Confirmed scope**. Once authorized, merge the change into the checkpoint, increment accord_revision for a decision-path Accord, and verify that update before Build resumes. Routine implementation details within the authorized outcome do not require an Accord delta.

## Recovery checkpoint

The conversation is the primary working surface. Use one short checkpoint to preserve a confirmed decision or recover the active change after context compaction, session resumption, or an interrupted implementation. It is a recovery cache, not a second specification system or a history archive.

Use exactly `.codeaccord/checkpoint.md` at the project root. Never create per-change files or accumulate completed records. Use it as follows:

- On the direct path, skip it when the task can be completed and verified in the current context without meaningful recovery risk.
- On the direct path, create it when investigation or implementation is likely to cross compaction, a session boundary, or a long-running operation. Record the user's authorized outcome; no Accord text or confirmation is required.
- On the decision path, persist the confirmed Accord scope and verify the write before editing product files. A checkpoint does not turn a direct request into an approval gate.

Keep the checkpoint semantically current. Refresh it:

1. after a decision-path Accord or material scope change is confirmed;
2. after an important implementation or verification milestone;
3. before a long-running command, test suite, delegation, or other operation that may interrupt the turn;
4. before compaction when the platform signals it or the remaining context indicates it is approaching.

Treat each refresh as an actual persistence operation: write the file, read or validate the result, then continue. Because automatic compaction may arrive without warning, also refresh after each completed implementation batch whose conclusions are needed to resume safely; do not leave `Current state` saying that no code has changed after product files have already been edited.

When a checkpoint already exists for this workspace and session, direct work also changes the worktree and invalidates its stored fingerprint. Update **Current state** and refresh `git_head` and `worktree_fingerprint` before finishing. Do not take over a checkpoint owned by another session for an unrelated task.

Do not rely on a mechanical hook or a generated compaction summary to record decisions. A command cannot infer unrecorded decisions reliably; the active agent owns the semantic update and refreshes the file before compaction or interruption.

Treat **Confirmed scope** as the currently authorized outcome: the user's request on the direct path, or the merged confirmed Accord on the decision path. Keep unapproved proposed changes under **Unresolved** until the user authorizes them. A compaction or resume must never promote an unresolved proposal into confirmed scope.

Keep phase fields self-consistent:

- `exploring` may contain candidate changes under Unresolved but does not authorize Build for an undecided direction;
- `approved` means a decision-path Accord is confirmed and persisted but implementation has not started;
- `implementing` and `verifying` require an authorized scope and no unresolved decision that materially changes it; direct work may have `accord_revision: 0`;
- when a user-owned decision blocks progress, keep the authorized scope unchanged and record the proposal under Unresolved.

One checkpoint belongs to one workspace and one session. Record both ownership fields and keep them when you refresh the file:

- `workspace`: the absolute project root;
- `session`: the session identifier available in your environment; record `unknown` when none is available.

These fields are how a later session decides whether the checkpoint is its own. Because there is only one checkpoint per workspace, do not run two CodeAccord tasks in the same workspace at the same time; park one task or use a separate worktree.

When the checkpoint records a session or workspace that does not match the current one, do not adopt its scope and do not overwrite it until the user confirms. After the user confirms they are continuing that task, take ownership by updating `workspace` and `session` to the current values. When no owner is recorded, or the recorded workspace does not match the checkpoint's location, treat the checkpoint as moved or copied and verify with the user before continuing. The snapshot helper never writes the file, so ownership is always yours to maintain.

After compaction or session resumption, cross a recovery barrier before continuing:

1. read the checkpoint from disk;
2. inspect Git HEAD, status, and relevant current source;
3. reconcile any difference between the checkpoint and the workspace;
4. state the recovered goal, phase, and next action in the recorded user language;
5. refresh the checkpoint when it is legacy, stale, or materially incomplete.

Do not edit implementation files, tests, configuration, or product documentation until this barrier is complete. Source and tests remain authoritative for implementation state, while Confirmed scope remains the product boundary. Do not silently expand scope from a generated compaction summary.

Keep it concise, normally no more than 500–800 tokens. Store decisions and state, not raw transcripts, long evidence, source code, logs, or secrets. `Current state` contains only conclusions needed to resume the task; do not turn it into a chronological investigation or implementation log. Use this shape and omit empty bullets rather than adding more sections:

```markdown
---
status: exploring | approved | implementing | verifying
updated: YYYY-MM-DDTHH:MM:SSZ
workspace: /absolute/project/root
session: <session id>
checkpoint_version: 1
language: <BCP-47 language tag>
accord_revision: <0 for direct work; positive integer after a decision-path Accord is confirmed>
git_head: <current Git commit>
worktree_fingerprint: <hash from checkpoint_snapshot.py>
checkpoint_reason: direct_start | accord_confirmed | delta_confirmed | milestone | precompact
---

# Goal

## Confirmed scope

## Non-goals

## Current state

## Next action

## Acceptance checks

## Unresolved
```

For a Git workspace, obtain `git_head` and `worktree_fingerprint` from the bundled read-only helper and copy both values into the frontmatter after the semantic content is current:

```bash
python3 .agents/skills/codeaccord/scripts/checkpoint_snapshot.py "$(git rev-parse --show-toplevel)"
```

The fingerprint covers HEAD, staged changes, unstaged tracked changes, and untracked file contents while excluding `.codeaccord/`; only the hash is stored. If Git freshness is unavailable, record `unavailable` and reconcile the workspace manually after recovery. The helper never writes these fields.

When verification is complete and the final result has been reported, remove the checkpoint. If work remains incomplete or verification is blocked, keep it updated for recovery. Do not archive it automatically.

## Build

After the direct request or decision-path confirmation:

1. For a confirmed decision-path Accord, persist its scope before the first product edit. Direct work needs no separate approval or mandatory checkpoint.
2. Implement the authorized behavior in the minimal specification or confirmed Accord, and preserve unrelated user changes.
3. Update affected contracts, callers, configuration, migrations, tests, and documentation together.
4. Follow project-local instructions and established patterns.
5. Keep working through ordinary implementation failures without reopening the decision.
6. Remove dead code introduced or made obsolete by this change when it is safely within scope.

Do not create an OpenSpec change or another planning system unless the user explicitly requests it.

## Verify

Run focused checks first, then expand according to the actual impact. Verify against the expected behavior and checks identified before Build, or against the confirmed Accord; tests must exercise behavior rather than merely mirror implementation details.

Before declaring completion:

- compare the result with the requested outcome and any agreed acceptance criteria;
- verify the original bug reproduction no longer fails when applicable;
- check affected contracts and callers;
- report commands actually run and their results;
- disclose remaining limitations, skipped checks, or unresolved risks;
- compare the authorized scope and acceptance checks with the changed-file list, and explain any file outside the obvious scope;
- if this session owns a checkpoint, update it after major verification results and remove it only after the work is complete.

Lead the final response with the outcome. Explain what changed, why it changed, how it was verified, and any material limitations.
