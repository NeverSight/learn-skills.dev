---
name: ensemble
description: Improve real work through independent, materially different or intentionally redundant agent contributions checked against ground truth.
disable-model-invocation: true
---

# Ensemble

An **ensemble** uses independent attempts to expose alternatives and misses, then changes one deliverable according to observed evidence. The coordinator owns the outcome and may investigate, implement, integrate, or validate directly; members own their assigned contributions.

Use harness-native agents, model selection, isolation, tools, artifacts, and notifications. Discover available capabilities instead of asking the user to restate them. When an adapter provides stronger guarantees, use them directly rather than reproducing them through prompts or process.

Before first dispatch, create `.ensemble/<NNN>-<invocation-slug>/STATE.md` from [`STATE-TEMPLATE.md`](STATE-TEMPLATE.md). Use `ensemble_state` when available. Keep technical truth in source, tests, maintained docs, and harness artifacts; `STATE.md` holds only compact coordination facts and pointers.

## 1. Frame the outcome

State the requested deliverable, subject, boundaries, and observable completion evidence. Decompose the outcome into the concrete coverage it requires. For feedback or a problem statement, identify each item's scope, root cause, and core need. The smallest ensemble may use few attempts; it may not shrink the outcome without explicit user approval.

**Complete when:** required coverage and consequential unresolved interpretations are explicit.

## 2. Compose result-changing attempts

Inspect the harness's available roles, models, tools, and isolation. Assign every contribution a coverage slice, expected artifact or observation, and a material difference: model, role, approach, evidence source, failure lens, or named redundancy against a costly stochastic miss. Use at least two independent attempts. Give competing writers isolated baselines; integrate accepted work into one candidate.

**Complete when:** every required constituent is owned or recorded as a gap, each attempt can change the result or confidence in a consequential judgment, and writers cannot interfere.

## 3. Produce independently

Dispatch the shared subject, ground truth, constraints, and assigned coverage without exposing sibling conclusions before each first attempt. Let agents return normal task results and artifact pointers; do not require ceremonial status summaries. After dispatch, wait for harness notification instead of polling. Steer, cancel, retry, replace, or recompose only when that can recover a result-changing contribution.

**Complete when:** each retained attempt produced a usable artifact or observation, or its missing coverage is explicit.

## 4. Decide by observation

Assess each contribution against its assigned coverage and ground truth. Separate observation, inference, and decision. Compare consequential differences; turn disputed or suspicious claims into checks rather than votes. Agreement is not evidence of sufficiency when attempts share a blind spot. Judge full-outcome coverage on the accepted set, not on any specialist contribution.

**Complete when:** consequential differences and under-supported coverage are observed, dispositioned, or returned for targeted follow-up.

## 5. Evolve the deliverable

Select, combine, implement, repair, document, and validate accepted results. The coordinator may do this directly or assign it to suitable native agents. Preserve useful findings, refresh observations invalidated by revision, and run checks against the candidate that may be delivered.

**Complete when:** the candidate reflects accepted results, affected checks are current, and failed or unavailable critical checks block delivery.

## 6. Close and deliver

Continue only when another attempt, repair, or check can plausibly change the deliverable or an important decision. Before delivery, confirm the accepted set satisfies full outcome coverage, surface unresolved user choices and consequential risks, and record the candidate and observed verification in `STATE.md`. Version coordination state through repository VCS when available; submit code under repository conventions and keep the two submissions separate.

**Complete when:** the requested deliverable is handed off with observed verification, no critical check blocks it, and `STATE.md` can recover the outcome, accepted decisions, candidate, verification, and next state.

References: [`README.md`](README.md) explains rationale and portability; [`PATTERNS.md`](PATTERNS.md) contains optional composition patterns; [`GLOSSARY.md`](GLOSSARY.md) defines terms.
