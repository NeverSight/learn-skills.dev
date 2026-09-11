---
name: think-ethical-matrix
description: Produces an ethical matrix, a grid that cross-references affected parties (rows, deliberately including voiceless ones such as future generations and the environment) against prima facie principles (columns of wellbeing, autonomy, fairness), specifying the option's impact in every cell and reading the result as a trade-off pattern rather than a score. Use when a concrete proposal affects multiple parties with a genuine moral trade-off among them, some affected parties have no voice, and an ethics debate keeps sliding between groups and principles. Not a decision calculator and not an option-versus-criteria scorer; the matrix maps the terrain and leaves the weighing to deliberation.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.ethical-matrix
  family: ethics-values-deliberation
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Ethical Matrix

An "is this ethical?" debate over a concrete proposal tends to slide: it starts on one affected group, drifts to a principle, jumps to a different group, and never holds both axes at once - so the trade-offs that actually matter (a benefit to one party paid for by a burden on another, on a different principle) stay invisible. The ethical matrix refuses that slide. It cross-references the affected parties (rows) against a small fixed set of prima facie ethical principles (columns), and forces a concrete impact specification in every party-by-principle cell. The rows deliberately include parties who cannot speak for themselves - animals, ecosystems, future generations, absent groups - because they get a row whether or not anyone in the room represents them. The durable move is **principled cross-referencing**: making the trade-offs a single-axis analysis hides become visible and individually contestable.

Two design choices are load-bearing and frequently misunderstood. First, **the matrix maps the moral terrain; it does not weigh it.** The grid is not an algorithm and emits no verdict - the weighing happens in deliberation over the filled grid. Second, **the cells are impact specifications** ("how does this affect the wellbeing of small producers"), not perspective voicings ("what would small producers say"). That second point is what separates it from stakeholder perspective-taking. The output is an **ethical matrix**: a party-by-principle impact grid with each cell tagged factual or contested, a trade-off pattern read-out, and an explicit no-verdict footer.

## When to Use

- A concrete proposal, technology, policy, or feature has multiple affected parties and a genuine moral trade-off among them: who gains, who pays, and on what dimension.
- Some affected parties have no voice - non-human, future, or absent groups that need representing even though nobody in the room speaks for them.
- An ethics debate keeps sliding between groups and principles without anyone noticing the slide, and disagreement needs to attach to specific cells rather than to vague unease.
- A group needs a shared, inspectable structure for a values trade-off, so a position can be defended cell by cell.

## When NOT to Use

- **Do not present it as a decision calculator.** The matrix cannot weigh the problems it uncovers (Schroeder and Palmer, 2003: helpful for fact-finding, "much less helpful" for weighing). A filled grid presented as an answer is the method's signature abuse. This is the central wall.
- **Do not use it to score options against the decider's own criteria.** That is `think-decision-option-review` (options by weighted criteria, aggregated to a recommendation). The ethical matrix maps one proposal's impacts on affected parties against impartial principles and refuses to aggregate.
- **Do not use it when who counts as affected is the live dispute.** The matrix takes its row roster as given. If frame membership is contested, audit the boundary first with `think-boundary-critique`, then populate the rows.
- **Do not impose the principle columns unreflectively.** The fixed principlist columns can crowd out the values participants actually hold (Cotton, 2009). The columns may be adapted, but adaptation must be deliberate and stated, not silent.
- **Do not run it as completeness theater.** A fully populated grid looks rigorous while the substantive judgments hide inside cell wording. The cells are claims to challenge, not boxes to tick.

## Instructions

When asked to assess the ethics of a concrete proposal across affected parties, follow these steps:

1. **State the option in one line.** Name the single concrete proposal, technology, policy, or feature under analysis. The matrix evaluates one option's impacts; it is not a comparison of options (that is `think-decision-option-review`).
2. **Roster the affected parties (rows).** List the groups the option affects. Deliberately include parties who cannot speak for themselves - animals, ecosystems, future generations, absent or unrepresented groups. Each gets a row whether or not anyone present represents them. If who counts as affected is itself the contested question, stop and run `think-boundary-critique` first.
3. **State the principle columns.** Use the default prima facie set - wellbeing (beneficence and non-maleficence together), autonomy, and fairness (justice). If the situation needs an adapted set (for example a future-generations or solidarity column for an algorithmic-audit context), state the adaptation and justify it explicitly. Never swap the columns silently.
4. **Fill every cell with an impact specification.** For each party-by-principle intersection, write how the option affects THIS party on THIS principle - a concrete, checkable claim, not a perspective voicing. Do not leave cells blank; "no material effect" is itself a claim worth recording.
5. **Tag each cell factual or contested.** Mark each cell **[factual]** (a checkable empirical claim) or **[contested]** (an encoded value judgment reasonable people dispute). This is where the substantive disagreements surface instead of hiding in cell wording.
6. **Read the grid as a trade-off pattern.** Name which groups bear which burdens on which principles, where a benefit to one party is paid for by a burden on another, and which contested cells the whole assessment turns on. This pattern read-out is the payoff, not the filled grid.
7. **Close with an explicit no-verdict footer.** State plainly that the matrix maps the terrain and does not weigh it: the grid is not a score and emits no recommendation; the weighing is left to deliberation. Carry the evidence caveat (tier P, transferred from human practice) into the artifact.
8. **Emit the ethical matrix artifact** per `references/TEMPLATE.md`: the option line, the party rows (voiceless ones marked), the stated principle columns, the filled and tagged grid, the trade-off pattern read-out, and the no-verdict and evidence-caveat footer.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the filled ethical matrix - party rows (voiceless ones marked) by principle columns, every cell a tagged impact specification, plus the trade-off pattern read-out and the no-verdict footer - not a prose essay. Never present the grid as a score, a ranking, or a recommendation.

## Quality Checklist

Before finalizing, verify:

- [ ] The option under analysis is stated in one line, and it is a single proposal, not a set of options to score.
- [ ] The party rows include any voiceless parties (non-human, future, absent), each marked - not only the parties present to speak.
- [ ] The principle columns are stated (wellbeing, autonomy, fairness by default), and any adaptation is deliberate and justified, never silent.
- [ ] Every cell is filled with a concrete impact specification (how the option affects THIS party on THIS principle), not a perspective voicing and not a blank.
- [ ] Every cell is tagged **[factual]** or **[contested]**, so the value judgments surface instead of hiding in cell wording.
- [ ] The trade-off pattern read-out names which groups bear which burdens and where one party's benefit is paid for by another's burden.
- [ ] An explicit no-verdict footer states the matrix maps and does not weigh - no score, no ranking, no recommendation.
- [ ] No overclaiming: the evidence is practitioner-grade and transferred from human deliberation; claim a trade-off-mapping aid, not a measured improvement in ethical judgment and not a verdict (see `evidence/dossier.md`).

## Evidence

Tier **P** (governing). The ethical matrix is a genuinely established practitioner method with roughly twenty-five years of multi-domain application - GM crops (Mepham, 2000), participatory fisheries assessment (Kaiser and Forsberg, 2001), radioactive-waste deliberation (Cotton, 2009), an EU-project practitioner manual (Mepham et al., 2006), and current commercial algorithmic auditing (O'Neil and Gunn, 2020) - plus a peer-reviewed methodological literature including serious critiques. What the record does NOT contain is any controlled outcome study: no experiment measures whether matrix users produce better or more defensible assessments than non-users, and no effect size exists to quote (none is quoted here). It is not M (no controlled or comparative study) and not C (well past plausible-but-untested - a sustained, scrutinized, multi-domain record). All evidence is human group-deliberation practice; none is on AI agents, so the transfer to an agent-run skill is an explicit, untested assumption. The skill ships as a trade-off-mapping aid with a hard "the matrix maps, deliberation weighs" wall, never as a verdict machine. Full grading, sources, and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed ethical matrix on a real decision.
