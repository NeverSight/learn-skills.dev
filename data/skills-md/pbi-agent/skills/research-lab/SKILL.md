---
name: research-lab
description: Use when a task needs a staged, evidence-based research workflow across any domain, including framing, baseline measurement, alternative exploration, comparison, decision, implementation or final artifact creation, regression review, and optional phase delegation to subagents.
---

# Research Lab

Use this for research-level work where the answer should be selected from
evidence, not intuition. The workflow adapts to software, data analysis,
academic synthesis, product strategy, policy, writing, or other domains.

## Scope

- Work on one research item at a time.
- Keep research artifacts under `research/<slug>/` unless the user or repo has
  an existing equivalent location.
- Use the local project, user-provided sources, web sources, datasets,
  benchmarks, interviews, or examples as evidence depending on the domain.
- Ask questions only when the research item, constraints, or acceptable output
  cannot be inferred.

## Load References

- Load `references/artifacts.md` before creating or resuming a research folder.
- Load `references/phases.md` for the detailed phase-by-phase workflow.
- Load `references/domain-adaptation.md` when the theme is not software or the
  evidence and metrics need domain-specific translation.
- Load `references/subagent-orchestration.md` when the user asks to use
  subagents to run framework phases.

## Startup

1. Identify the target research item, theme/domain, expected final output, user
   constraints, and any existing tracker or checklist item.
2. Create a stable slug from the research item.
3. Create or resume `research/<slug>/`; read `state.md`, `decision.md`, and
   prior `runs/*/results.md` if present.
4. If the user asks for one phase, complete only that phase and write the
   handoff. Otherwise, run phases in order while feasible and stop at blockers,
   missing evidence, or an explicit decision gate.
5. If subagent phase delegation is requested, keep the main agent as owner:
   delegate one phase at a time, review the result, then continue or fix.

## Phase Flow

1. Prepare: create the workspace, capture scope, list hypotheses, and record
   open questions.
2. Specify: define inputs, outputs, success criteria, evidence sets, metrics,
   edge cases, and validation requirements.
3. Baseline: build or document the simplest credible baseline and measure it.
4. Explore: test one new or refined alternative per loop without repeating old
   approaches.
5. Compare: evaluate viable approaches under a shared matrix of criteria,
   workloads, sources, or cases.
6. Decide: select the approach or conclusion only when evidence gates pass;
   otherwise send the task back to Explore or Compare.
7. Apply: create the final implementation, recommendation, report, policy,
   design, or other artifact exactly from the decision scope.
8. Review: rerun targeted validation, compare against the saved decision, and
   reopen the loop if the result regresses or evidence no longer holds.

## Non-Negotiable Rules

- Do not skip the spec, baseline, and decision phases unless the exception is
  documented in `decision.md` or `state.md` with a reason.
- Do not create final target-artifact changes or final user-facing conclusions
  before `decision.md` exists, unless the user explicitly asks for a lightweight
  answer.
- Ground claims in observed evidence and record enough provenance to reproduce
  or audit the conclusion.
- Use comparable methods across runs; record environment, sources, assumptions,
  and limits.
- Update `state.md` after every completed phase with status, evidence summary,
  open questions, and next phase.
- Preserve prior research artifacts on resume; append new runs instead of
  rewriting history.
- Do not mark a delegated phase complete until the main agent has reviewed the
  subagent output and required validation passes.

## Deliverables

- `research/<slug>/README.md`
- `research/<slug>/state.md`
- `research/<slug>/hypotheses.md`
- `research/<slug>/runs/<timestamp>-<phase>/plan.md`
- `research/<slug>/runs/<timestamp>-<phase>/results.md`
- `research/<slug>/runs/<timestamp>-<phase>/metadata.json` when measurements,
  sources, or reproducibility details need structured capture
- `research/<slug>/decision.md` before final application

## Handoff

When stopping, report the research path, completed phase, current best strategy
or conclusion, missing evidence, and exact next phase.

## References

- `references/artifacts.md`
- `references/phases.md`
- `references/domain-adaptation.md`
- `references/subagent-orchestration.md`
