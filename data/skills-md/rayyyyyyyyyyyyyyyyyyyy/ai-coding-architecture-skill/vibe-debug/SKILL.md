---
name: vibe-debug
description: Diagnose failures or regressions with a red-capable feedback loop; fix only when requested. Not for feature work or speculative cleanup.
---

# Vibe Debug

Load named skills through the host mechanism; call the Skill tool when exposed.
Do not reload an active skill.

## Authority

- **Diagnosis only:** inspect evidence and report the supported cause; source or
  runtime changes require authorization.
- **Diagnose and fix:** isolate the cause, then apply the smallest in-scope fix.

Ambiguous wording permits read-only diagnosis. It does not authorize source or
runtime edits, deployment, provider/production changes, or instrumentation.
Read [references/instrumentation.md](references/instrumentation.md) before adding
instrumentation or observing production.

## Red-capable loop

- Identify the symptom's source: user report, existing test, or actual observation.
  Separate symptom from proposed cause; capture expected/actual behavior, path,
  environment, and smallest trigger.
- Ground expectations in accepted requirements or established contracts. Imagined
  edge cases are hypotheses; newly written tests need an independent expectation
  basis and do not create requirements or fix authority.
- Reproduce through the smallest relevant test, command, request, interaction,
  replay, trace, or authorized instrumentation. The loop must exercise the reported
  path, fail for the symptom, and rerun after one change. Use controlled timing,
  bounded trials, or the same before/after measure for intermittent/performance
  failures.
- Unrelated failures, historical logs alone, compilation, and source inspection
  do not establish the loop. Without reproduction or an equivalent signal, report
  the missing evidence; do not patch a plausible hypothesis.

## Isolate and reframe

Reduce the path while preserving the symptom. Test one evidence-backed hypothesis
at a time with a predicted discriminating observation. Instrument only the owning
boundary and remove temporary instrumentation per the reference. Obtain new
evidence after rejecting a hypothesis before proposing another fix.

After three consecutive unsuccessful attempts with the same causal model, owning
boundary, and evidence source, stop refining that approach. Parameter, timing,
wording, or implementation variations do not reset the count. Restate the user's
outcome and success evidence, separate facts from assumptions, and reconsider
ownership and cause versus symptom. Choose a materially different hypothesis,
evidence source, boundary, simplification, or safe workaround for what it can
prove. New evidence or external state must change a retry's evidentiary value.
With no different in-scope path, report the blocked outcome, failed approach,
and smallest missing decision, evidence, or access.

## Fix and report

Only in diagnose-and-fix mode, change the owning boundary, preserve contracts,
and exclude cleanup, dependency churn, or architecture migration. Rerun the
original loop and proportionate regression checks; retain bounded observability
only with explicit authorization. After a fix, invoke `vibe-verify`.

Report cause, decisive evidence, any authorized fix, and uncertainty. On actual
agent transfer invoke `vibe-handoff`.
