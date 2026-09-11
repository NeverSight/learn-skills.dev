---
name: think-boundary-critique
description: Audits the boundary judgments that silently define a problem frame. For each of four sources, who benefits, who decides, whose knowledge counts, who has standing, it contrasts the descriptive is boundary against the normative ought boundary, names the gaps, and lists the affected-but-excluded parties who have no voice in the frame, producing a boundary-judgment audit rather than a stakeholder round-up. Use when a plan, metric, or proposal already encodes who matters and who does not and the risk is solving a tidy problem for the people inside the line while pushing harm onto people outside it, when an improvement claim rests on an unexamined judgment about whose improvement, or on contested, value-laden, multi-party situations.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.boundary-critique
  family: problem-framing
  evidence-tier: "C/P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Boundary Critique

Every problem frame draws a line before any reasoning starts: who counts, what counts, whose improvement is the point, and who is left on the other side of the line. Those prior decisions are **boundary judgments**, and they condition both the facts you collect and the values you weigh. The reflex is to reason inside the frame as given. Boundary critique refuses that reflex and makes the frame itself the suspect object. It interrogates each boundary judgment in two modes - how the frame currently draws the line (the **is** mode) and how it ought to (the **ought** mode) - and forces an explicit account of the parties who have a stake in the consequences but no seat in the frame. The move is the de-branded core of Critical Systems Heuristics (Werner Ulrich, from 1983, later with Martin Reynolds). The output is a **boundary-judgment audit**, not a discussion.

## When to Use

- A plan, metric, proposal, or "solution" already encodes who matters and who does not, and the risk is solving a tidy problem for the people inside the line while externalizing harm onto people outside it.
- An "improvement" claim rests on an unexamined judgment about *whose* improvement (a growth metric, an efficiency gain, a success measure that quietly picks a beneficiary).
- The situation is contested, value-laden, or multi-party: policy, programme or intervention design, evaluation, or any decision where reasonable parties would draw the boundary differently.
- You suspect a frame is illegitimately bounded - that the affected-but-excluded exist - and want them surfaced before the frame is acted on.

## When NOT to Use

- **The frame is genuinely settled and uncontested.** If the stakeholder set and the success measure are already agreed and legitimate, auditing the boundary manufactures doubt and stalls execution. This is the same failure as reframing a correct problem. This is the central wall.
- **The problem is technical or single-party.** With one obviously-correct beneficiary and no excluded affected parties, the audit produces empty "ought" columns - ritual, not insight.
- **You expect it to resolve the disputed boundary.** Boundary critique *surfaces and debates* the is-vs-ought gap; it does not adjudicate it. It exposes the boundary question and names who is excluded; it does not settle who is right or compel a powerful actor to widen the line. When the gap is real, route the decision onward (e.g. to `think-decision-option-review`) - the audit informs that choice, it is not the choice.
- **You only need to hear the stakeholders.** If you just want each in-scope party voiced, that is a stakeholder round-up - use `think-parallel-perspectives-review` (stakeholder mode) or `think-problem-restatement` (its stakeholder shift). Boundary critique is the different, upstream move: it takes the stakeholder *set itself* as suspect and audits inclusion-versus-exclusion in is/ought terms. Run it as a round-up and it collapses into the move the library already ships.

## Instructions

When asked to audit who a frame includes and excludes, follow these steps:

1. **State the frame under audit.** Record the plan, metric, proposal, or decision exactly as given, in one line, plus the improvement it claims to deliver. If the frame is already settled, agreed, and legitimate, say so and stop - do not manufacture doubt.
2. **Audit the four sources, each in is then ought mode.** For each source, answer the boundary question first descriptively (how the frame currently draws the line), then normatively (how it ought to):
   - **Motivation - who benefits.** Who is the client/beneficiary; what is the purpose; what is the measure of improvement or success? (Is: whose improvement does the current frame actually serve? Ought: whose improvement should it serve?)
   - **Power/control - who decides.** Who is the decision-maker; what is under their control; what is in the decision environment, outside it? (Is vs ought for who holds the decision.)
   - **Knowledge - whose expertise counts.** Who is treated as expert; what expertise actually applies; what is assumed to guarantee success - and are those false guarantors? (Is vs ought for whose knowledge is admitted.)
   - **Legitimacy - who has standing.** Who witnesses for those affected but not involved; what worldview is treated as authoritative; how are competing worldviews reconciled? (Is vs ought for who has standing.)
3. **Name the is-vs-ought gaps.** For each source, state the gap between the is-boundary and the ought-boundary in one line. The gap is the finding - where the frame draws the line versus where it should. A source with no gap is a legitimate boundary; say so rather than padding.
4. **List the affected-but-excluded.** This is the move the rest of the library does not have. Enumerate the parties with a real stake in the consequences who hold no seat, no voice, and no expertise-standing inside the frame, and for each note who, if anyone, currently witnesses for them. Do not fold this into "voice the stakeholders" - these are precisely the parties a stakeholder walk-through cannot reach, because they are outside the line.
5. **Emit the boundary-judgment audit.** Produce the artifact in `references/TEMPLATE.md`: the four sources answered in both is and ought modes, the is-vs-ought gaps named, and the explicit list of the affected-but-excluded. End by stating what the audit does NOT do - it surfaces the boundary question, it does not adjudicate it - and, where a real gap exists, the onward route for deciding under it. The template's pre-printed evidence caveat is part of the artifact; carry it through verbatim.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the filled audit - the four sources in is/ought, the named gaps, and the affected-but-excluded list - not a prose essay.

## Quality Checklist

Before finalizing, verify:

- [ ] The frame under audit is captured verbatim, with the improvement it claims, in one line.
- [ ] All four sources (who benefits, who decides, whose knowledge counts, who has standing) are answered in *both* is and ought modes - no source left in one mode only.
- [ ] Each source has an explicit is-vs-ought gap stated (or an honest "no gap - legitimate boundary"), not a restatement of the answers.
- [ ] The affected-but-excluded are listed as a distinct section - parties outside the line with a stake but no voice - not merged into a stakeholder voicing of in-scope parties.
- [ ] The output names what it does NOT do (surfaces the boundary question, does not adjudicate it) and routes a real gap onward (e.g. to `think-decision-option-review`) rather than presenting itself as the resolution.
- [ ] The output is the boundary-judgment audit artifact, not prose.
- [ ] No overclaiming: the evidence is conceptual and transferred; claim "surfaces who the frame illegitimately includes or excludes, descriptively versus normatively," not a measured improvement in decisions (see `evidence/dossier.md`).

## Evidence

Tier **C** (governing; honest read **C/P**, capped at C). Critical Systems Heuristics is an influential, well-developed framework in systems thinking, operational research, and evaluation, with a forty-year literature and a clear, teachable apparatus (the twelve boundary questions, the four sources, the is/ought pairing). A 2024 systematic review (Hutcheson, Morton and Blair, *Systemic Practice and Action Research* 37(4): 499-514) examined 77 peer-reviewed papers and found a real body of applied case work, with utility "best exemplified in an action research context." But there is **no controlled, comparative, or outcome study** of boundary critique - the same review reports many papers are theoretical rather than applied, contains no trials or comparison groups, and calls CSH a "relatively underutilised method." The evidence is the existence and reasoned application of the method, not evidence that running it produces better frames - which is the line between C and P, and why the grade caps at C. All of it is transferred from human policy, evaluation, and action-research practice; none studies an AI-produced boundary critique. No effect-size figure is cited, because none exists. Full grading, sources, and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed boundary-judgment audit on a real decision.
