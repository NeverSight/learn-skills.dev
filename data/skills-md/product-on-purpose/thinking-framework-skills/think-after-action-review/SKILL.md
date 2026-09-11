---
name: think-after-action-review
description: Produces a structured after-action review by comparing what was expected against what actually happened, diagnosing why the gaps occurred, and converting them into specific owned sustain-and-change actions. Use when a project, launch, sprint, or incident has finished and you want to turn the outcome into learning, not a status update.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.after-action-review
  family: meta-thinking-and-reflection
  evidence-tier: "S"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# After Action Review

Most retrospectives are an unstructured "how did it go?" that produces venting and vague lessons. The After Action Review imposes the structure that actually carries the benefit: compare what was expected to what actually happened, diagnose why the gaps occurred (in both directions), and convert that into what to sustain and what to change, specifically and with owners. The expected-vs-actual comparison is load-bearing; without a recorded expectation there is nothing to learn against, only hindsight narrative. The output is an **after-action review**, and it must be blameless to work.

## When to Use

- A project, launch, sprint, experiment, or incident has finished.
- There was a real expectation to compare the outcome against (or you can reconstruct it honestly).
- The team wants to learn, not assign fault.

## When NOT to Use

- Before the event (that is a premortem).
- As a status update or a summary of what shipped.
- When it will become blame (it stops working the moment people fear fault).
- When there is genuinely no expectation and none can be honestly reconstructed.

## Instructions

When asked to run an after-action review, follow these steps:

1. **State what was expected.** The goal, the plan, and the predicted outcome going in. If it was not recorded, reconstruct it honestly and say you are doing so - do not back-fit it to the result.
2. **State what actually happened.** The real outcome, concretely, including what went better than expected, not only what went worse.
3. **Diagnose the gaps.** For each meaningful difference (both directions), ask why - the actual cause, not the convenient one. Keep it blameless.
4. **Capture what to sustain.** The things that worked and should be repeated. Do not skip this for the failures.
5. **Specify what to change.** Concrete, owned changes for next time - not vague "communicate better."
6. **Emit the after-action review** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the expected-vs-actual review with sustain/change actions, not prose and not a status report.

## Quality Checklist

Before finalizing, verify:

- [ ] What was expected is stated (recorded or honestly reconstructed), separate from the outcome.
- [ ] What actually happened includes the better-than-expected, not only failures.
- [ ] Each gap has a real "why," kept blameless.
- [ ] What to sustain is captured, not just what to change.
- [ ] Changes are specific and owned, not vague.
- [ ] The output is the AAR artifact, not a status update.

## Evidence

Tier **S**. A meta-analysis of team and individual debriefs (Tannenbaum & Cerasoli, 2013) found structured debriefs improve performance substantially (effect size ~0.79), and the effect depends on the structure - intent, comparison to expectations, specific takeaways - not on merely holding a meeting (origin: US Army TC 25-20). Unstructured retros do not carry this. Evidence is for human teams, transferred to AI use, not AI-validated. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed after-action review.
