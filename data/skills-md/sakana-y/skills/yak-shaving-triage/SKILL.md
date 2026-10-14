---
name: yak-shaving-triage
description: Guard engineering tasks against yak shaving. Capture independent observations in configured working records, assess related findings, and reconcile formal tracker work without diverting the active task.
---

# Yak Shaving Triage

Notice broadly. Solve the current problem. Preserve the rest.

Start with the engineering task, whether selected by the model or the user. A later invocation joins the current task. Stay active until the User Problem is complete or the user stops this skill. The User Problem is the currently authorized outcome and boundaries; its workflow owns necessary investigation, implementation and verification. Ordinary work needs silent checks, not recurring scope reports.

Use [Assess Findings](../assess-findings/SKILL.md), installed with `investigate-with-evidence`, for qualification, relationships and recommendations. Reuse existing assessments from Just or Explore. A missing dependency leaves the judgment pending while feasible main work continues.

## 1. Establish capture and guard the next branch

Read the [working-record contract](../assess-findings/references/working-records.md) to resolve the user-selected repository, project identity, save/commit authority and existing record layout. Reuse configuration; if the destination is missing, ask once while continuing the main task. Preserve unsaved observations with that blocker until it is resolved. Read prior findings only when the active task's history gates permit it. Setup is optional and is not invoked automatically.

Compare each concrete clue or contemplated task switch with the User Problem. With Just, use its declared batch: retain necessary investigation in that batch and save independent new outcomes for future work. Remaining side findings do not extend the batch or prevent its closure. Necessary investigation or repair remains with the main workflow at whatever depth it needs. Independent observations can be captured before final assessment; a suspicion without concrete evidence remains a note, not a confirmed finding. Use [discovery lenses](references/discovery-lenses.md) for a bounded check of an unresolved clue, or exploration explicitly requested by the user. Reuse already sufficient evidence.

At a coherent checkpoint, save independent observations and their evidence in the configured record, or return an update to its coordinator. Keep separate facts, hypotheses, current assessment and implementation progress. Persist essential evidence before disposable cleanup. A working record is not a formal issue: [issue capture](references/issue-capture.md) governs issue readiness, canonical reconciliation and tracker publication.

**Complete when:** each branch belongs to the main task, has a saved or explicitly pending observation, or is excluded for a stated evidence-based reason. Continue the main task.

## 2. Assess and reconcile without duplicate work

Use the shared [coordination method](../assess-findings/references/coordination.md). The coordinator chooses direct work or a bounded worker by task fit, rather than requiring a separate agent for each role. A discovery worker checks one concrete clue; an Assess owner judges the finding and its relationships; a reconciliation worker searches existing records and implementation coverage. These assignments have distinct questions and reuse existing results. None independently repairs the side problem or publishes it.

Before canonical tracker research, check [search eligibility](references/issue-capture.md#wait-for-search-eligibility). When eligible and independent search can proceed while the main task continues, use [background reconciliation](references/background-reconciliation.md). Otherwise perform a bounded search at a suitable checkpoint or retain it with a reason and next action. Closed gates apply to workers too. Revisit pending work on gate changes, resumption and completion.

Assess owns action value and suggested priority; Yak owns record identity, reconciliation disposition, report ordering and approved tracker publication. Return material search results and delivery coverage to the same assessor; revise affected judgments instead of rerunning the whole assessment. For confirmed findings request suggested priority through Assess, preserving its scale and limits. Related problems can share a cause while keeping separate acceptance boundaries.

Reconcile PR links under the working-record contract when history access is open. Known remote state is a dated observation, not a permanent truth. Missing Tracker Guidance blocks formal reconciliation, not authorized working-record capture; retain the draft and defer the canonical-destination question to completion.

**Complete when:** each eligible finding has an owner and result or a pending reason and next action, shared records reflect returned evidence, and ordinary side work has not displaced the User Problem.

## 3. Close and hand back

Report the main task's actual status, collect dispatched work and revisit pending findings. End unproductive canonical searches as Reconciliation Blocked with their limits. Present findings under the [outcome reporting contract](references/issue-capture.md#report-the-outcome), preserving confirmed defects, opportunities and unresolved observations separately. Show recorded paths and save/commit failures as well as canonical matches.

For formal tracker mutations, present exact drafts and obtain Tracker Write Approval under issue capture. Reused records need no mutation. Without canonical guidance, collect one destination question, then reconcile before proposing a write. An authorized working record can retain evidence and a pending tracker draft without implying publication.

On pause or stop, stop dispatch and affected workers promptly, preserve checkpoints, and transfer or clean owned resources. Stopping Yak alone leaves the main workflow under its existing authority. Resume from recorded state and inherited evidence gates rather than repeating completed searches. Apply the working-record lifecycle when later evidence supports archive or reopening; PR merge alone does not settle acceptance.

**Complete when:** task status, every observation's assessment and persistence state, eligible reconciliation results or blockers, and every approved tracker mutation's actual result are clear and recoverable.

## Urgent findings

For credible security, data-loss or destructive risk, notify the user immediately, stop actions that would realize the risk and preserve sanitized evidence. Maintain independence gates and tracker publication requirements. Repair changes scope only when the user authorizes it.
