---
name: think-premortem
description: Generates a ranked risk register that stress-tests a planned decision by imagining it has already failed, surfacing the likely causes and pairing each with a mitigation, tripwire, and kill criterion. Use when about to commit to a launch, hire, investment, migration, or any risky, hard-to-reverse decision, or when you need risks surfaced before committing.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.premortem
  family: risk-and-resilience
  evidence-tier: "S/M"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Premortem

A premortem stress-tests a plan by assuming it has *already failed* and reasoning backward to explain why, then converting each cause into a mitigation, a tripwire, and a kill criterion. The shift from "what might go wrong?" to "it went wrong, why?" is what does the work: it licenses dissent, surfaces more and more specific causes than ordinary risk review, and turns vague worry into pre-committed action while you can still change course. The output is a **risk register**, not a discussion.

## When to Use

- Before a launch, hire, investment, migration, vendor selection, or any consequential, hard-to-reverse commitment.
- When a plan has optimistic momentum and you suspect concerns are going unspoken.
- When you want risks expressed as observable signals and pre-decided responses, not a feeling of caution.
- Often *after* options have been compared and one has been chosen, as the last gate before committing.

## When NOT to Use

- **After the outcome is known.** That is a postmortem, a different tool.
- **For trivial or fully reversible (two-way-door) decisions.** The ceremony is not worth it.
- **To generate options or to choose among them.** Use an ideation skill or a decision-option review; premortem is a risk tool.
- **As a ritual to bless a decision already made.** If the mitigations will not be acted on, skip it; a premortem nobody acts on is theater.

## Instructions

When asked to run a premortem, follow these steps:

1. **Frame the decision and the horizon.** State the plan and intended outcome in one or two sentences, and pick a concrete time horizon (for example, "six months after launch"). If the decision is trivial or already irreversible, say so and stop.
2. **Declare the failure vividly.** Assert it in the definite past: "It is [horizon]. This plan has failed badly." Make the failure concrete and specific, not "it underperformed." Write it into the template's "The failure, declared" section as a past-tense scene of observed fact - it is part of the artifact, and every cause in the register must explain it in the past tense.
3. **Generate causes broadly, before judging.** List the plausible reasons the failure happened. Aim for breadth and specificity; include uncomfortable, political, and second-order causes, not just technical ones. Do not filter yet.
4. **Cluster and rank.** Group related causes and rank them by likelihood and impact (High/Medium/Low each). Keep the vital few; do not pad.
5. **Convert each top cause into action.** For each high-priority cause, define a **leading signal / tripwire** (the early sign it is happening), a **mitigation** (what reduces the risk now), an **owner**, and a **kill criterion** (the pre-decided condition under which you stop or change course). This conversion step is mandatory; a list of risks without it is not a premortem.
6. **Emit the risk register and a short summary.** Produce the artifact in `references/TEMPLATE.md`: the declared failure in the definite past, then a one-paragraph "top risks and what we will do" summary above a ranked register table.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the filled risk register plus its summary, not a prose essay.

## Quality Checklist

Before finalizing, verify:

- [ ] The failure was declared in the definite past, with a concrete horizon.
- [ ] Causes go beyond the obvious technical ones (include people, process, second-order, and external causes).
- [ ] Every high-priority cause has a tripwire, a mitigation, an owner, and a kill criterion (the conversion step is done).
- [ ] Risks are ranked, not an undifferentiated list.
- [ ] The output is the risk register artifact, not prose.
- [ ] No overclaiming: the skill does not promise a better outcome, only better-surfaced and better-handled risk (see `evidence/dossier.md`).

## Evidence

Tier **S/M** (contested). Prospective hindsight reliably increases the number and specificity of causes surfaced and reduces overconfidence in a plan (Mitchell, Russo & Pennington 1989; Veinott, Klein & Wiggins 2010). It does **not** have strong evidence of improving final outcomes, and the often-quoted "30%" figure measures the *number of reasons generated*, not decision quality. The evidence is transferred from human studies and has not been validated for AI-augmented use. Full grading, sources, and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed premortem on a real decision.
