---
name: think-process-tracing
description: Evaluates rival causal explanations of a single case by typing each piece of within-case evidence by its diagnosticity (hoop, smoking-gun, straw-in-the-wind, doubly-decisive tests) against each rival's mechanism chain, then eliminating or confirming rivals item by item rather than by tallying. Use when one outcome has happened, several genuine rival explanations compete to explain it, and mechanism-level evidence (logs, timestamps, documents, who knew what when) is available to discriminate them - an incident postmortem, a churn spike, a lost deal, a metric anomaly. Not for cross-case generalization, not a consistency-matrix scoring tally, and not for cases with no rivals on the table.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.process-tracing
  family: systems-and-consequences
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Process Tracing (rival-explanation adjudication)

When one thing has happened and several stories compete to explain why, the instinct is to tally evidence: pile up what supports each story and pick the side with the bigger pile. That rewards whichever explanation attracted the most loosely-relevant chatter. Process tracing refuses the tally. It weighs each piece of within-case evidence by its **diagnosticity** - its power to eliminate or confirm an explanation - so that one decisive observation outranks any amount of weak, ambiguous support. The durable move is to make each rival explanation concrete as a causal mechanism chain (the step-by-step way that story would have produced this outcome, and the observable fingerprints each step would leave), state those expected fingerprints **before** weighing the evidence, then type each piece of evidence by certainty (if the explanation is true, must we see this?) and uniqueness (could the rivals also produce it?). A single failed hoop test eliminates a rival no matter how much straw-in-the-wind support it had. The output is a **rival-explanation evidence ledger**: the rivals, each one's mechanism chain, every evidence item typed per rival, the surviving explanation with its residual uncertainty, and the single most decisive observation still missing. It is explicitly not a cross-case generalization, not a consistency-scoring matrix, and not a manufactured winner when nothing available is diagnostic.

## When to Use

- One outcome has occurred and there are genuinely rival stories about why it happened: an incident postmortem with three competing root-cause theories, a churn spike (a pricing change versus a competitor launch versus an onboarding regression), a lost deal, a metric anomaly, a contested past decision.
- Mechanism-level evidence is available or obtainable - logs, timestamps, documents, sequence of events, who knew what when - that could discriminate the rivals rather than merely decorate them.
- The argument has become a shouting match between narratives, and the useful reframing is "what would I expect to see if THIS story were true that the others would not produce?"

## When NOT to Use

- **Do not use it when there are no rivals on the table.** With a single causal story there is nothing to discriminate. Descend the levels of that one story with `think-iceberg-model`, or decompose its coverage with `think-issue-tree`. Process tracing needs at least two genuine rival explanations.
- **Do not use it for cross-case generalization.** "Does X generally cause Y?" or "which combination of conditions produces success across our markets?" is comparative and configurational work over many cases. Process tracing's jurisdiction is one case, N equals one. (That cross-case space is QCA's territory, rejected in this library for fit.)
- **Do not run it on an all-straw-in-the-wind evidence pool.** When nothing available is diagnostic, running the ritual anyway produces false confidence. The honest output is "non-diagnostic - here is the observation that would discriminate," never a manufactured winner. This is the central wall.
- **Do not let it degenerate into an evidence-by-hypothesis tally matrix.** Scoring every item against every hypothesis for consistency and picking the least-inconsistent is Analysis of Competing Hypotheses, whose controlled record with professional analysts is null-to-negative (see `evidence/dossier.md`). If there is no single case and no mechanism chain - just generic multi-hypothesis scoring - decline rather than becoming that matrix under another name. The value lives in the mechanism chains and the per-item typing, not in a tally.
- **Do not assign test types after seeing the evidence.** Grading a found item as a "smoking gun" post hoc inflates its diagnosticity and invites motivated grading. The expected fingerprints for each rival must be stated before the evidence is weighed.

## Instructions

When asked to figure out which of several explanations actually caused a single outcome, follow these steps:

1. **State the focal outcome and the case.** Name, in one line, the specific thing that happened and the single case it happened in. If the question is really cross-case ("does this generally happen?"), stop - this is the wrong tool.
2. **Surface the rival explanations.** List the genuinely competing stories for why the outcome occurred. There must be at least two; if there is only one, stop and use a single-story diagnosis instead. Keep the rivals genuinely distinct, not relabelings of one story.
3. **Make each rival a mechanism chain.** For each rival, write the step-by-step causal chain by which that story would have produced this outcome in this case. Each chain is the spine the evidence will be tested against.
4. **State the expected fingerprints per step, before weighing evidence.** For each step in each chain, name the observable traces it would have left if it actually operated (logs, timestamps, documents, sequence, who knew what when). Write these down before grading any actual evidence - this is what blocks post-hoc inflation.
5. **Type each evidence item per rival.** For each piece of evidence, ask the two questions against each rival: certainty (if this rival is true, must we see this?) and uniqueness (could the other rivals also produce it?). Classify the resulting diagnosticity:
   - **Hoop** (certain, not unique): failing it eliminates the rival; passing keeps it alive without confirming it.
   - **Smoking gun** (unique, not certain): finding it strongly confirms the rival; not finding it only mildly weakens it.
   - **Straw in the wind** (neither): a weak nudge, never decisive.
   - **Doubly decisive** (both): confirms one rival and eliminates the others - rare, and what the search aims at.
6. **Update each rival item by item.** Let the decisive items do the work. A single failed hoop eliminates a rival regardless of how much straw-in-the-wind support it had. Track the running status of each rival (alive / eliminated / confirmed).
7. **Read the result honestly.** Name the surviving explanation and its residual uncertainty. If every available item is straw-in-the-wind and nothing discriminates, say so: the output is "non-diagnostic," not a winner.
8. **Name the single most decisive missing observation.** State the one observation - ideally a hoop or doubly-decisive test - that would most cut the remaining uncertainty if it could be obtained next.
9. **Emit the rival-explanation evidence ledger** per `references/TEMPLATE.md`: the outcome and case, the rivals with their mechanism chains and expected fingerprints, the typed evidence table, the surviving explanation with residual uncertainty, and the most decisive missing observation. Carry the evidence caveat through into the artifact.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the filled rival-explanation evidence ledger - the rivals, their mechanism chains, the per-item diagnosticity typing, the surviving explanation with residual uncertainty, and the most decisive missing observation - not a prose essay and not a tally. Never select a winner by counting supporting items; let the typed, decisive items decide. When nothing is diagnostic, the ledger says "non-diagnostic" and names the discriminating observation to seek.

## Quality Checklist

Before finalizing, verify:

- [ ] The focal outcome and single case are stated in one line, and the question is genuinely within-case (not cross-case generalization).
- [ ] There are at least two genuinely rival explanations, each made concrete as a step-by-step causal mechanism chain.
- [ ] The expected observable fingerprints for each step are stated before any evidence is graded (no post-hoc test-type assignment).
- [ ] Each evidence item is typed per rival by certainty and uniqueness into hoop / smoking gun / straw-in-the-wind / doubly decisive.
- [ ] Rivals are updated item by item, with a single failed hoop eliminating a rival - not selected by counting supporting items.
- [ ] If the evidence pool is all straw-in-the-wind, the output is "non-diagnostic" with the discriminating observation named - not a manufactured winner.
- [ ] It has not become a consistency-matrix tally across hypotheses (that is ACH, declined here); the work is in the mechanism chains and the per-item typing.
- [ ] The surviving explanation is reported with its residual uncertainty, and the single most decisive missing observation is named.
- [ ] The output is the rival-explanation evidence ledger artifact, not prose.
- [ ] No overclaiming: the evidence is practitioner-grade methodology and transferred from human case-study research; claim a structured-adjudication aid, not a measured gain in reasoning accuracy (see `evidence/dossier.md`).

## Evidence

Tier **P** (governing). Process tracing has a deep, peer-reviewed, actively self-critical methodological literature (Van Evera 1997; George and Bennett 2005; Collier 2011; Mahoney 2012; Bennett and Checkel 2015; Beach and Pedersen 2019; the Bayesian formalization by Fairfield and Charman 2017), but that literature concerns inferential validity in case-study research - whether and when this logic licenses causal conclusions - not controlled human-reasoning outcomes. There is no randomized or controlled trial testing whether using process tracing improves judgment accuracy, for humans or for agents; one external research run graded it S on methodological pedigree and that grade is rejected here, because pedigree is not outcome evidence. The only nearby controlled evidence is negative and belongs to the cousin method ACH (Mandel, Karvetski and Dhami 2018; Dhami, Belton and Mandel 2019); it attaches to ACH's matrix-tally procedure, sets no tier here in either direction, and motivates the hard anti-ACH wall. All of it is transferred from human methodological contexts and not validated for AI-augmented use, which independently caps the grade at P. The skill ships as a structured single-case adjudication aid with a hard "non-diagnostic is a valid answer" wall, never as a measured accuracy improver. Full grading, sources, and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed rival-explanation evidence ledger on a real decision.
