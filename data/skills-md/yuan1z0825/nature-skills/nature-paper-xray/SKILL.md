---
name: nature-paper-xray
description: >-
  Read one supplied paper closely enough to reconstruct how its authors actually got there, rather
  than restating what the abstract claims. Use for 精读论文, 讲透这篇论文, 把这篇读懂, 作者为什么这么设计,
  这个公式怎么推出来的, paper x-ray, and deep single-paper comprehension before building on,
  reviewing, presenting, or citing that paper. Recovers the real starting point and the bet the
  authors placed, separates load-bearing design from decoration, grounds each key formula in a
  worked micro-example with concrete numbers, and checks how far the evidence actually reaches,
  including where the authors are confident and where the paper does not report something. Delivers
  a structured Markdown long-read by default. Not a summary, not a translation, not a peer review.
---

# Nature Paper X-Ray

Read a paper the way a researcher explains it at a whiteboard to a colleague: what the authors saw, why they believed it, where they hesitated, what they gave up, and which numbers would change the conclusion.

The delivered artifact is a Markdown long-read. A section-by-section summary of the paper is a failure mode, not a fallback.

## Default stance

- The method section is a teaching order, not the order the work happened in. The introduction's story is arranged after the fact. The contribution list is written for reviewers.
- The judgments that decided the paper — what the authors noticed, why they trusted it, what they abandoned — are mostly not written down. Recovering them is the job.
- Every figure was chosen. Ask what the authors want a reader to believe from this one, then look for details inside it that do not support that reading.
- A figure contains its own counter-evidence more often than the text does: a curve that crosses later, an error bar wider than the gap between compared methods, a log axis hiding a constant-factor difference, one seed standing in for a variance claim.
- Name a mechanism or say the paper does not name one. Do not supply a motive the authors never stated.

## Workflow

1. **Read the whole source first** — body, appendix, footnotes, figure and table captions, and supplementary material if supplied. Appendices carry what the body declined to print: real hyperparameter search ranges, unflattering ablations, reviewer-response material. Record disagreements between the body and the appendix as findings.
2. **Reconstruct the research path.** Name the concrete failure the work reacts to, and the bet the authors placed on their strongest evidence. The first figure usually carries that bet and deserves separate treatment.
3. **Separate load-bearing from decoration.** For each distinctive design choice, judge whether removing it collapses the result or merely accompanies it. Cite the ablation, appendix table, or controlled comparison that settles it. When no such control exists, write that the paper does not run it.
4. **Ground the mathematics.** Give every symbol its shape and meaning, state what a formula is for before stating the formula, and follow each key formula with a micro-example using concrete numbers carried to the end. See `references/deep-reading-protocol.md`.
5. **Check the evidence boundary.** Agreement between body text, tables, and figures; whether baselines share data, steps, and tuning budget; whether hyperparameters were selected on the test set; preprocessing leakage; cost and the conditions under which the claim stops holding. See `references/evidence-boundary.md`.
6. **Preserve hedging strength.** "May" is not "does", "suggests" is not "shows", "some settings" is not "all settings". Where the paper does not report something the conclusion needs, write that it is not reported. Never substitute a plausible number, an assumed default, or a value remembered from a similar paper.
7. **Deliver the long-read.** Lead with what the paper is actually claiming, then the reconstructed path, the load-bearing judgment, the worked examples, and the evidence boundary. Close with what a reader should carry away and what remains open. State the scope read — body, appendix, supplementary, or a stated subset — and never imply fuller coverage than was achieved.

## Paper-type adaptation

Reading emphasis shifts with the paper type. Load `../nature-shared/core/paper-type-taxonomy.md` when the type is not obvious:

- **algorithmic** — fair-comparison discipline dominates: are baselines tuned as hard as the proposal, and where does it fail?
- **methods** — reproducibility dominates: would the protocol work in another lab, and what is left implicit?
- **hypothesis** — the strength of the causal evidence dominates: does the evidence rule out the alternative explanation?
- **research** — what was found, and how far the observation generalizes beyond the studied system.
- **review** — how the field is organized, where sources disagree, and what remains open.

## Boundaries

- Reading sets no verdict. This skill reports what the paper does and how far its evidence reaches. It does not score, rank, or judge acceptance readiness, novelty, or significance — that is `nature-reviewer`.
- It does not extract reusable writing patterns from a paper — that is `nature-writing` and its exemplar material.
- It does not translate a paper or produce a bilingual reader — that is `nature-reader`.
- It does not search the literature, verify citations, or cite sources on the paper's behalf — those are `nature-academic-search`, `nature-citation`, and `nature-ref-verifier`.
- It does not draft manuscript prose. Use the reading as input to `nature-writing` when writing related work or positioning.

## Output discipline

- Write in the language the user is using. A Chinese request produces Chinese prose with English technical terms preserved exactly.
- Quote the source only where an anchor requires it; do not reproduce the paper at length.
- Formulas use `$...$` inline and `$$...$$` on their own line. Never place a formula in backticks or a code block.
- A long paper is not a reason to degrade the output into a summary. If the reading is incomplete, say where it stopped.
