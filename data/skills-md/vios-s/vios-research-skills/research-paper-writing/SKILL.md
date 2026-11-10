---
name: research-paper-writing
description: Use this skill when the user wants to draft, structure, or improve an academic paper or a specific section of one. Triggers include "write my paper", "help me write the introduction", "structure my methods section", "draft my abstract", "improve my related work", "write up my results", "help me write contributions", or "make this section clearer". Handles full drafts and section-by-section writing for conference and journal formats. Do not use for rebuttal writing — use paper-rebuttal-helper; do not use for literature synthesis alone — use literature-review.
license: MIT
metadata:
  category: "Writing"
  version: "0.1.0"
  author: "VIOS Lab, University of Edinburgh"
---

# Research Paper Writing

A skill for drafting and improving academic papers across all sections. Good academic writing is precise, honest, and structured so a reader can verify every claim.

## When to invoke this skill

- You have results and need to write them up
- You are stuck on a specific section (commonly: introduction or related work)
- You want the abstract tightened or the contributions sharpened
- You need a first draft to iterate from
- Your writing is clear to you but others say it is confusing

## Workflow

### 1. Establish the paper's core

Before writing anything, lock in:
- **One-sentence contribution**: "We show that [method/finding] achieves [result] on [task/data], which enables [application/insight]."
- **Target venue**: this sets page limit, style, and expected rigour level.
- **The three reviewers you are writing for**: a specialist, a methodologist, and a sceptic.

If the contribution cannot be stated in one sentence, the paper is not ready to write — use `research-question-framing` first.

### 2. Section-by-section guidance

#### Abstract (150–250 words)

Four-sentence structure:
1. **Context**: What problem does the field care about?
2. **Gap**: What is missing or wrong with current approaches?
3. **Contribution**: What do you do and what key result do you get?
4. **Impact**: Why does this matter?

Do not put citations in the abstract. Do not use "novel" or "state-of-the-art" without the result that justifies it.

#### Introduction (10–15% of page budget)

Five-paragraph structure:
1. **Hook**: The phenomenon or problem, stated in terms anyone in the field recognises.
2. **State of the art**: What the best current approaches do and where they fall short.
3. **Gap / motivation**: The specific inadequacy your paper addresses.
4. **Your approach**: One paragraph — what you do (not how you do it in detail).
5. **Contributions**: A bulleted list, 3–5 items, each starting with a verb. Each bullet must be verifiable in the paper. End with a roadmap sentence: "Section 2 reviews... Section 3 describes...".

Never bury contributions at the end of a long introduction. Reviewers scan for them.

#### Related Work

Group by theme, not chronology. For each group:
- State what these methods do.
- State their limitation relative to yours.
- Cite representative works, not exhaustively.

Do not use related work to showboat your reading. Use it to situate your work. If a method is close to yours, say so clearly and explain the difference — reviewers will find it anyway.

#### Method

Write for reproducibility. A reader should be able to reimplement from your description alone.

Structure:
1. **Problem setup**: formal notation, what is given, what is inferred.
2. **Architecture / algorithm**: top-down (overview first, then details).
3. **Training / inference details**: loss function, optimiser, hyperparameters, any tricks needed to make it work.
4. **Complexity**: time and space, if non-obvious.

Use one consistent notation throughout. Define all symbols when first used.

#### Experiments

Structure:
1. **Datasets**: name, size, train/val/test split (state if patient-level or sample-level for medical data), any preprocessing.
2. **Baselines**: why these and not others? Each baseline should be a fair and representative competitor.
3. **Metrics**: what you measure and why it is the right measure.
4. **Main results**: a table, cleanly formatted, with standard deviations. Bold the best result per row.
5. **Ablation**: one table that isolates each claimed component by removing it. If your ablation is on a different dataset or task, explain why.
6. **Qualitative results**: figures that show where the method works and where it fails.

Do not cherry-pick qualitative examples. Show at least one failure case.

#### Discussion / Conclusion

- Restate the contribution briefly (do not copy the abstract).
- State limitations honestly — reviewers will find them; better to name them first.
- Give 2–3 concrete future directions (not vague "future work").
- Do not introduce new results or claims.

### 3. Writing quality checklist

Run through before submitting to co-authors:

- [ ] Every claim has a citation or a result number.
- [ ] Every figure is referenced in text before it appears.
- [ ] Figure captions are self-contained (reader should understand the figure without reading the body).
- [ ] Abbreviations are defined at first use.
- [ ] Tense is consistent: present for general facts, past for your experiments.
- [ ] No "we believe", "we hope", "it seems" — either you know or you don't claim it.
- [ ] Numbers agree: abstract claims match table results.
- [ ] Limitations are stated.

### 4. Common section anti-patterns

| Section | Anti-pattern | Fix |
|---------|-------------|-----|
| Abstract | Results without numbers | Add the actual metric value |
| Introduction | Contribution list says "we propose" | Start with the actual contribution: "A new loss that..." |
| Related work | Chronological survey | Group by theme and add your differentiator |
| Method | Algorithm described only in text | Add a figure or pseudocode |
| Experiments | Only top-line results, no ablation | Isolate each component |
| Conclusion | "Future work: extend to more tasks" | Name the specific task and what would enable it |

## Anti-patterns

- **Do not** write the introduction last and then forget to update the contributions to match the actual paper.
- **Do not** use passive voice to hide your choices: "the threshold was set to 0.5" → "we set the threshold to 0.5 based on validation performance."
- **Do not** conflate the method section and the experiments section.
- **Do not** write related work as a literature dump — every cited paper should be differentiated from yours in one clause.

## See also

- `paper-rebuttal-helper` when reviews arrive.
- `pre-submission-review` for a final quality pass before submission.
- `venue-reviewer` for venue-specific formatting and acceptance criteria.
- `literature-review` for building the related work section's source material.
