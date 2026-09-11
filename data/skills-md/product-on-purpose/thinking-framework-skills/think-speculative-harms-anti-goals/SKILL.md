---
name: think-speculative-harms-anti-goals
description: Produces an anti-goals register by assuming a design succeeds at scale, narrating the near-future in which that success harms third parties (including non-users) and is exploited in bad faith by named bad actors, then converting each speculated harm into a standing design constraint bound into the requirements. Use when a feature's success case could externalize harm onto people outside the customer relationship (location, ranking, inference, targeting, automation) and the team's risk review is entirely project-centric. Not a premortem (route plan-survival risk there), not for present documented harms (route to incident analysis), and not a security threat model.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.speculative-harms-anti-goals
  family: ethics-values-deliberation
  evidence-tier: "A"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Speculative Harms and Anti-Goals

Most risk review is project-centric: premortems, risk registers, and launch checklists all ask whether the *plan* survives. They are structurally blind to the harms that arrive precisely when the plan succeeds - when the feature ships, works as designed, and reaches scale, and in doing so externalizes harm onto people who never chose to be users, or hands a weapon to someone who exploits it on purpose. Speculative harms and anti-goals exists to reach those harms. It assumes success, narrates the concrete near-future in which that success hurts people, casts the third-party victims and the bad-faith misuse actors (the stalker, the scammer, the data broker, the abusive ex, the authoritarian buyer), and then converts each speculated harm into an **anti-goal**: a named outcome the design commits to prevent, carried as a standing constraint on what the product must never do, enable, or optimize for.

The durable move is not the dystopian story. It is the success anchor (not failure), the cast of non-users and exploiters (not the project team), and the binding of each harm into a design constraint (not a monitoring control). The output is an **anti-goals register**: per harm, the narrative in brief, the harmed parties, the misuse actor and pathway, the anti-goal it implies, and the design implication that operationalizes it. The popular framings are called "Black Mirror brainstorms" and the "Black Mirror Writers Room"; the skill ships de-branded, because "Black Mirror" is a trademark of the television series' rights holders, and the move itself is community design-ethics practice (Mauldin 2018; Fiesler's writers-room exercise, studied by Klassen and Fiesler 2022).

## When to Use

- A feature's *success case* could externalize harm: recommendation and ranking systems, location and presence features, data collection and inference, targeting, content amplification, or automation applied to vulnerable populations.
- The team's risk apparatus is entirely project-centric and nobody has yet asked who outside the customer relationship gets hurt, or who would weaponize the feature on purpose.
- Abstract ethics principles are failing to bite, and a concrete narrative is needed to make harms specific and discussable.
- The decision is consequential and hard to reverse, and the anti-goals produced will actually be bound into requirements, acceptance criteria, or a review gate.

## When NOT to Use

- **Do not use it for project-survival risk.** "Will this plan fail, and why?" is `think-premortem`. Running dystopian speculation to find schedule, market, and execution risk produces lurid stories and misses the boring causes. Route plan-survival risk to the premortem.
- **Do not use it for harms that are already present and documented.** Speculation is for harms that have not happened yet. If users are being hurt now, the job is incident analysis and remediation, not fiction. This is the method's own documented failure mode (Fiesler's "case and caution"): speculation can foreground distant, cinematic dystopias while the mundane harms of the current release go unexamined. Pair it with present-tense methods, or skip it.
- **Do not use it on trivial or fully reversible decisions.** The method will manufacture dystopian gravity for a button color. A two-way-door triage belongs upstream of it.
- **Do not run it if the anti-goals will never be bound into the design.** An anti-goals register that no requirement, acceptance criterion, or review gate ever references is ethics theater - the same wall the premortem draws against rituals that bless a decision already made.
- **Do not use it for complete adversarial-coverage assurance.** Narrative speculation is an elicitation device, not an enumeration guarantee. The nearest controlled cousin found a structured decomposition (attack trees) identified more threats than narrative misuse cases (Opdahl and Sindre, 2009). Where systematic security coverage matters, use structured threat modeling; this method is at best its warm-up.
- **Do not use it to produce a compliance artifact.** An algorithmic impact assessment or formal harm audit is governance process work, not a thinking move, and belongs to a governance toolkit, not this library.

## Instructions

When asked to stress-test a design for the harms that coexist with its success, follow these steps:

1. **State the focal design and the success anchor.** In one line, name the product, feature, or decision under examination, and assume it *succeeds* - it ships, works as designed, and reaches scale. The whole method runs off this anchor; if the real worry is the plan failing, stop and route to `think-premortem`.
2. **Narrate the dystopian near-future.** Write the concrete, specific story in which that success harms people: how did the good intention go wrong at scale, and what does the harm look like in a single vivid scene. Keep it near-future and plausible, not far-fetched science fiction - the documented failure mode is drifting to the cinematically distant while present harms go unexamined.
3. **Cast the harmed parties, including non-users.** Name who is hurt, with explicit attention to people who never chose to be users (the person located by someone else's app, the population a model infers about, the bystander surfaced by content amplification).
4. **Ask the misuse-actor question.** For each harm, ask who exploits the system in bad faith - the stalker, the scammer, the data broker, the abusive ex, the authoritarian buyer - and name the concrete pathway by which they weaponize the feature. This is the method's sharpest single prompt; do not skip it.
5. **Convert each harm into an anti-goal.** Bind every speculated harm into a standing design constraint: a named outcome the design commits to prevent, phrased as what the product must never do, enable, or optimize for ("never make location visible by default"; "the product must not let a third party reconstruct someone's schedule").
6. **Operationalize each anti-goal as a design implication.** For each anti-goal, name the requirement, acceptance criterion, default setting, or review gate it becomes. An anti-goal with no design implication is not yet bound, and an unbound register is theater.
7. **Name where each anti-goal will live.** State explicitly where in the requirements, backlog, or review process each anti-goal is carried forward, so the register binds into the design rather than sitting beside it.
8. **Emit the anti-goals register artifact** per `references/TEMPLATE.md`, carrying the pre-printed evidence caveat (tier A, transferred from human studies) by construction.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the filled anti-goals register - the focal design and success anchor, then one row per speculated harm carrying the narrative, the harmed parties, the misuse actor and pathway, the anti-goal, and the design implication - plus the binding line and the evidence caveat. It is not a prose essay and not a ranked risk list.

## Quality Checklist

Before finalizing, verify:

- [ ] The focal design and the **success anchor** are stated in one line, and the harms narrated are ones that coexist with success - not ways the plan fails.
- [ ] At least one harm is narrated concretely (a specific near-future scene), not abstractly, and the narration stays near-future rather than drifting to the cinematically far-fetched.
- [ ] The harmed parties are named, with explicit attention to **non-users** (people who never chose to use the product).
- [ ] The **misuse-actor question** is asked for the adversarial harms: who exploits this in bad faith, and by what concrete pathway.
- [ ] Every speculated harm is converted into an **anti-goal** - a standing constraint on what the product must never do, enable, or optimize for - not into a mitigation, tripwire, or kill criterion.
- [ ] Every anti-goal has a **design implication** (a requirement, acceptance criterion, default, or review gate) and a stated home in the requirements - the register is bound, not theater.
- [ ] The output is the anti-goals register artifact, not prose.
- [ ] No overclaiming: the evidence is anecdotal (tier A) and transferred from human classrooms and workshops; claim a harm-elicitation aid that forces a discipline, never a measured improvement in harm anticipation or a security-coverage guarantee (see `evidence/dossier.md`).

## Evidence

Tier **A** (anecdotal; governing). Speculative harms and anti-goals is a real, named, documented design-ethics practice with case accounts (Mauldin 2018, UX Collective, names the anti-goals conversion) and one peer-reviewed qualitative study of its classroom use (Klassen and Fiesler 2022, SIGCSE, 12 instructors). What the record does **not** contain is any controlled, comparative, or outcome study showing that dystopian narration improves harm anticipation, design decisions, or anything measurable - not for this method, and not for any of its genre siblings (Consequence Scanning, Judgment Call, Tarot Cards of Tech, Ethical OS). The strongest study measures instructor *perceptions of a teaching exercise*, not whether teams ship safer products, and it candidly records the method's own failure modes. The nearest controlled evidence is a *caution*: Opdahl and Sindre (2009) found a structured decomposition (attack trees) identified more threats than narrative misuse cases, so where systematic coverage matters the narrative format underperforms. All evidence is transferred from human classrooms and workshops; nothing studies an AI agent running the move, and the engagement and de-inhibition benefits the pedagogy literature describes are human social dynamics an agent does not have. What plausibly transfers is the structural prompt set (assume success, cast the victims and exploiters, convert to constraints), not the documented benefits. The skill ships honestly flagged at A: the value is that it forces the discipline and produces a bound, inspectable artifact, not any outcome claim. Full grading, sources, and the honest demotion case (a maintainer could defensibly fold this into `think-premortem`): `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed anti-goals register on a real decision.
</content>
