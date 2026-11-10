---
name: pre-submission-review
description: Use this skill when the user wants a comprehensive quality check of a paper before submission. Triggers include "review my paper before I submit", "is this paper ready to submit", "check my paper for issues", "pre-submission check", "find weaknesses in my paper", or "what would a reviewer complain about". Acts as an honest internal reviewer covering completeness, logical consistency, experimental rigour, and writing quality. For venue-specific criteria after this general check, use venue-reviewer.
license: MIT
metadata:
  category: "Review & Dissemination"
  version: "0.1.0"
  author: "VIOS Lab, University of Edinburgh"
---

# Pre-Submission Review

A skill that acts as an honest, constructive internal reviewer before your paper goes to a programme committee. The goal is to surface the problems reviewers will find — so you can fix them first.

## When to invoke this skill

- You think the paper is done but want a final check
- You want to know your paper's weakest points before committing to a venue
- You have a tight deadline and need to know which issues to fix first
- Co-authors want a shared baseline assessment before finalising

Do NOT use this as a substitute for co-author review. Human expertise on the specific domain matters more. Use this as a structural and consistency check.

## Workflow

### 1. Ask for the paper

Request the paper (as pasted text, PDF, or arXiv link). If only a specific section is provided, note that the review will be partial.

### 2. Structural audit

Check the following exist and are in the right place:

| Element | Check |
|---------|-------|
| Abstract | States problem, method, result, and impact with numbers |
| Introduction | Has a contribution list with 3–5 verifiable, verb-led bullets |
| Related work | Groups by theme; differentiates from each cited approach |
| Method | Contains formal problem setup + algorithm/architecture + training details |
| Experiments | Has datasets, baselines, metrics, main results table, ablation, qualitative |
| Conclusion | States limitations; no new claims |
| References | All cited works appear; no dangling citations |

Flag every missing element as a **blocker** — reviewers will mark it as a major weakness.

### 3. Claim–evidence consistency

For each contribution claim in the introduction:
- Find the experiment or proof that supports it.
- Check the numbers in the abstract match the numbers in the tables.
- Check that the strongest claim in the conclusion is backed by the weakest test (if it holds on the hardest case, say so; if not, soften the claim).

Report any claim that is not backed by direct evidence as a **red flag**.

### 4. Experimental rigour

| Check | Pass condition |
|-------|---------------|
| Baselines | Include the strongest published baseline on each benchmark |
| Evaluation | Metrics are appropriate for the task (e.g., Dice not accuracy for imbalanced segmentation) |
| Statistical reporting | Mean ± std over multiple runs or cross-validation folds |
| Ablation | Each claimed component removed independently; table provided |
| Dataset split | No test-set leakage; for medical data, split is patient-level |
| Reproducibility | Hyperparameters, random seeds, and data preprocessing described |

### 5. Writing quality scan

- **Claim density**: Are there sentences that make claims but cite nothing and prove nothing? Flag each one.
- **Vague language**: "significantly", "substantially", "outperforms" — quantify or remove.
- **Figure quality**: Are axes labelled with units? Are error bars defined? Are colours distinguishable in greyscale?
- **Notation consistency**: Is the same symbol used for two different things? Are all symbols defined before use?
- **Passive voice overuse**: "The threshold was set" → by whom and why?

### 6. Prioritised report

Output issues grouped by severity:

```
BLOCKERS (must fix before submission):
  - [Issue] — [Why it would cause rejection]

MAJOR WEAKNESSES (will likely cause major revision requests):
  - [Issue] — [Suggested fix]

MINOR ISSUES (easy to fix, worth doing):
  - [Issue]

STRENGTHS (keep these; they are selling points):
  - [Strength]

READINESS VERDICT: [Ready | Ready after blockers fixed | Needs significant work]
```

## Anti-patterns

- **Do not** give only positive feedback to avoid uncomfortable truths — that defeats the purpose.
- **Do not** review style when there are substantive gaps — fix the gaps first.
- **Do not** suggest experiments that cannot be done before the deadline — focus on what is fixable.

## See also

- `venue-reviewer` for applying venue-specific criteria after this general check.
- `internal-meta-review` for the VIOS scored meta-review and red-team (reasons to reject, checkmate questions).
- `paper-rebuttal-helper` for when reviews arrive after submission.
- `research-paper-writing` for rewriting sections flagged by this review.
