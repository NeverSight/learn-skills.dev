---
name: think-complexity-domain-sort
description: Runs a Complexity Domain Sort, sorting a situation into Clear, Complicated, Complex, Chaotic, or Confusion and choosing the response posture that fits, caveat-first. It leads with the weak evidence (the 2021 PMC internal-medicine review found scientific proof of its validity has yet to be provided), then forces the discipline the bare label lacks, namely an explicit response posture and a concrete next action rather than just a name. Use only when this complexity sort (also known as Cynefin) is asked for by name; for cause decomposition prefer think-issue-tree.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.complexity-domain-sort
  family: decision-and-option-evaluation
  evidence-tier: "C"
  version: 0.1.0
  standard: "0.8"
  caveat-first: true
  posture: run_caveat_first
  recommendation-policy: explicit_request_only
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Complexity Domain Sort

The Complexity Domain Sort triages a situation by how knowable its causal structure is, then picks the response posture that fits: sense-categorize-respond for the clear, probe-sense-respond for the complex, and so on. It is descriptively named here; the framework it derives from is Cynefin, and its evidence is conceptual only. This skill runs the sort honestly. It leads with that caveat, then forces the one thing the bare label omits and that makes the sort worth running at all: a concrete next action tied to the domain, because saying "this is complex" is not a decision.

## Before you run this: the evidence caveat

This sort is descriptively named; the framework it derives from is Cynefin, a trademark of The Cynefin Co. (Dave Snowden, 1999). Its evidence is tier **C** (conceptual): it is a coherent, widely taught sense-making heuristic, but no controlled study shows that classifying a problem this way improves decisions versus not classifying it. The 2021 PMC review applying it to internal-medicine diagnostic reasoning states the point plainly: the framework "is now widely used for teaching and as a simple heuristic; however, scientific proof of its validity has yet to be provided." The dominant failure mode is the cargo cult: stopping at the label ("ah, this is complex, we should probe") is satisfying to say and changes nothing. So the placement is a contested framing, not a found fact, and the deliverable is the next action it implies, not the bucket name.

## When to Use

- The user asks for this complexity sort (or Cynefin) by name and you should run it honestly rather than refuse.
- A team is applying the wrong management style to the problem type (running an emergent initiative on a rigid best-practice plan, or smothering a routine task in deliberation) and naming that mismatch out loud would help.
- As a front end to picking how to act, where the value is legitimizing safe-to-fail experiments in the complex domain and flagging the confusion trap, not the five-box picture.

## When NOT to Use

- As a substitute for a decision: a confident label ("this is complex") is not an answer, and stopping there is the documented cargo-cult failure.
- When the job is to enumerate the causes of one effect: use `think-issue-tree`.
- When the job is to hold several uncertain external futures in parallel: use `think-scenario-planning`.
- When the job is to choose among options under stated criteria: use `think-decision-option-review`.

## Instructions

When asked to run a Complexity Domain Sort, follow these steps:

1. **Lead with the caveat.** State up front that the evidence is conceptual (tier C, "scientific proof of its validity has yet to be provided," 2021), that Cynefin is a trademark of The Cynefin Co., and that the value is the response posture and next action, not the label.
2. **Sort the situation (or its parts) into the five domains.** Place the whole situation, and where parts differ, place them separately - real situations span domains.
   - **Clear:** cause and effect are evident; best practice applies. Posture: **sense - categorize - respond**.
   - **Complicated:** cause and effect exist but need expertise to see. Posture: **sense - analyze - respond** (good practice, expert diagnosis).
   - **Complex:** cause and effect are coherent only in hindsight. Posture: **probe - sense - respond** (safe-to-fail experiments; practice emerges).
   - **Chaotic:** no perceivable cause and effect. Posture: **act - sense - respond** (act first to establish stability).
   - **Confusion:** you do not yet know which of the four you are in. The danger is defaulting to the domain you are most comfortable with; the move is to break the situation into parts you can place.
3. **Justify the placement as a judgment, not a measurement.** Say why, and note that a different reader might place it differently. Flag anything you are unsure about as Confusion rather than forcing a box.
4. **Say what to DO, not just the label.** For each domain you used, name the concrete next action its posture implies (the experiment to run, the expert to consult, the standard to apply, the stabilizing act to take). This step is the deliverable.
5. **Emit the sort plus the actions** per `references/TEMPLATE.md`, caveat leading.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the domain placement (with its posture) plus the concrete next action each placement implies, with the caveat leading - not a bare label.

## Quality Checklist

Before finalizing, verify:

- [ ] Leads with the evidence caveat (tier C, "scientific proof of its validity has yet to be provided," 2021) before the artifact; does not overclaim the method's value.
- [ ] The trademark attribution (Cynefin, The Cynefin Co.) rides the leading caveat.
- [ ] Each domain used carries its response posture (sense-categorize-respond, sense-analyze-respond, probe-sense-respond, act-sense-respond).
- [ ] The placement is framed as a judgment, not a found fact; uncertainty is parked in Confusion rather than forced into a box.
- [ ] Every domain used ends in a concrete next action, not just the label (the cargo-cult guard).
- [ ] No invented statistic about the method's effectiveness appears (none is supported).

## Evidence

Tier **C** (conceptual; coherent and widely taught, but no controlled evidence it improves decisions). It ships as a contested lens, caveat-first and explicit-request-only, because users ask for this sort (or Cynefin) by name and an honest run that leads with the deficiency and forces a concrete next action beats a flat refusal. The governing source is the 2021 PMC internal-medicine review: "scientific proof of its validity has yet to be provided." Evidence is transferred from human managers, clinicians, and facilitators, not AI-validated. "Cynefin" and its branded facilitation methods are held by The Cynefin Co.; the method is named descriptively here and no branded method is reproduced. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed sort with response postures and concrete next actions.
