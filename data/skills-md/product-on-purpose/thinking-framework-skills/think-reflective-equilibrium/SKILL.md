---
name: think-reflective-equilibrium
description: Runs reflective equilibrium (mutual adjustment between considered case judgments, general principles, and background theories) caveat-first. It leads with the weak evidence (philosophically central since Rawls 1971 but empirically untested as a procedure, with three failure modes that bite in a bounded session), then forces the discipline a bare run lacks, namely an explicit revision ledger that records which commitment gave way and why. Use only when reflective equilibrium is asked for by name; for impartial allocation prefer think-veil-of-ignorance-reasoning, for a parties-by-principles audit think-ethical-matrix.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.reflective-equilibrium
  family: ethics-values-deliberation
  evidence-tier: "C"
  version: 0.1.0
  standard: "0.8"
  caveat-first: true
  posture: run_caveat_first
  recommendation-policy: explicit_request_only
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Reflective Equilibrium

Reflective equilibrium justifies a value position by mutual adjustment: you hold considered judgments about particular cases, general principles, and relevant background theories at once, and when a case and a principle conflict you revise whichever has less credibility on reflection, iterating until the set coheres. It is the de facto method of normative philosophy and it has three failure modes that bite in a bounded session. This skill runs it honestly. It leads with that caveat, then forces the one thing a bare run omits and that makes a run worth reading at all: an explicit revision ledger that records which commitment gave way and why, instead of a quiet declaration that "coherence was reached."

## Before you run this: the evidence caveat

Reflective equilibrium is tier **C** (conceptually plausible, philosophically central, empirically untested as a procedure). It has been the working method of normative philosophy since Rawls (1971), but no controlled study shows that performing it improves judgments, and three failure modes bite hardest in a single bounded session. (1) There is no externally checkable termination test: "equilibrium" cannot be distinguished from "I stopped looking for conflicts." (2) Garbage in, equilibrium out: Brandt (1979) warned the method can be "no more than a reshuffling of moral prejudices," and Singer (2005) sharpened this with evolutionary debunking, an objection that bites harder for an agent whose considered judgments are training-distribution intuitions. (3) A license to rationalize: because principles may be revised to fit cases, a motivated reasoner can quietly demote the principle that forbids a preferred outcome and report the result as a principled equilibrium. Even on its own idealized terms convergence is rare: Freivogel's (2023) simulations found different starting points reach identical equilibria only about 27 percent of the time. The revision ledger and the explicit honesty about these traps are the only thing that makes a run worth reading.

## When to Use

- The user asks for reflective equilibrium by name and you should run it honestly rather than refuse.
- A stated value, policy, or principle collides with a strong judgment about a concrete case, and the user wants the conflict adjudicated bidirectionally (the case may revise the principle, not only the reverse).
- You can produce, and the user wants, an explicit revision ledger showing which commitment gave way, not just an assertion that the set now coheres.

## When NOT to Use

- As a substitute for an external constraint, or to launder a preferred outcome into a "principled equilibrium" without recording the revisions (the documented failure mode).
- When the job is an impartial allocation or rule under uncertainty: use `think-veil-of-ignorance-reasoning`.
- When the job is auditing how an action treats each affected party against each principle: use `think-ethical-matrix`.
- When the job is disciplined revision of standing beliefs as new evidence arrives over time: use `think-belief-update-routine`.

## Instructions

When asked to run reflective equilibrium, follow these steps:

1. **Lead with the caveat.** State up front that the method's evidence is tier C (Rawls 1971; Brandt 1979; Singer 2005; Freivogel 2023), that "equilibrium" has no external stopping test, and that the value is the revision ledger below, not the declaration of coherence.
2. **List the considered judgments (tier a).** Write down the concrete case judgments in play, plainly. Tag each as held strongly or held weakly on reflection.
3. **State the general principles (tier b).** Write the principles that bear on the cases. Tag each strongly or weakly held.
4. **Name the background theories (tier c).** State the relevant background theories (about persons, fairness, how the judgments were formed) the wide variant uses to pressure-test the principles, so they are not merely a summary of the starting intuitions.
5. **Find the conflicts and revise the weaker member.** Where a case judgment and a principle collide, revise whichever has less credibility on reflection. This is bidirectional: sometimes the principle bends to the case, sometimes the case is overruled.
6. **Write the revision ledger.** For each conflict resolved, record which commitment gave way, why it was the weaker one, and what alternative was considered. This is the deliverable; a run with no ledger is the failure mode.
7. **State residual disagreements and stop honestly.** Note any conflict you did not resolve and say so. Do not declare global coherence; declare which conflicts you reconciled and which remain open. Emit per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the three-tier coherence set plus the revision ledger (which commitment gave way and why), with the caveat leading, not a bare assertion that "coherence was reached."

## Quality Checklist

Before finalizing, verify:

- [ ] Leads with the evidence caveat (Rawls 1971; tier C; Freivogel 2023) before the artifact; does not overclaim the method's value.
- [ ] All three tiers are present: considered case judgments, general principles, and background theories.
- [ ] At least one revision is bidirectional-aware (a case judgment is allowed to revise a principle, not only the reverse).
- [ ] The revision ledger records, for each resolved conflict, which commitment gave way and why it was the weaker one.
- [ ] Residual unresolved conflicts are stated; coherence is not declared globally where conflicts remain.
- [ ] No invented quantified claim about the method's effectiveness appears (the only figure supported is Freivogel's ~27 percent convergence).

## Evidence

Tier **C** (conceptually plausible, philosophically central, empirically untested as a procedure; normally would not ship). It ships as a contested lens, caveat-first and explicit-request-only, because users ask for reflective equilibrium by name and an honest run that leads with the deficiency and adds the missing discipline (the revision ledger) beats a flat refusal. The lineage is Goodman (1955), Rawls (1971), and Daniels (1979, the wide variant); the critique line is Brandt (1979) and Singer (2005); the only empirical-adjacent work simulates an idealized formal model (Beisbart, Betz and Brun 2021; Freivogel 2023, ~27 percent convergence) and tests the model, not people or agents. There is no transferred human-subject outcome evidence to flag: no controlled study of the procedure as an intervention exists, for humans or agents. The C grade rests on philosophical centrality plus idealized in-silico simulations that test the formal model, not people or agents - a clean C, not a transferred-and-capped split. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed three-tier coherence set with a worked revision ledger.
