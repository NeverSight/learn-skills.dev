---
name: paper-analyst
description: Use this skill when the user wants to deeply analyse a single academic paper — beyond summarising, into methodology validity, contribution clarity, and implications. Triggers include "analyse this paper", "break down this paper", "what are the weaknesses of X", "Heilmeier catechism on this paper", "critically read this", or providing a PDF/arXiv link for deep reading. Do not use for surveys across multiple papers — use literature-review instead.
license: MIT
metadata:
  category: "Reading & Analysis"
  version: "0.1.0"
  author: "VIOS Lab, University of Edinburgh"
---

# Paper Analyst

A skill for deep critical reading of a single paper. The goal is to understand not just what the paper claims, but whether those claims are well-founded, what assumptions are hidden, and what it actually adds to the field.

## When to invoke this skill

- Evaluating a paper before citing it seriously
- Deciding whether a method is worth replicating
- Preparing critique for a group reading or journal club
- Checking whether a competitor's result applies to your setting
- Getting a fast but honest read before a meeting

Do **not** invoke for broad literature synthesis — use `literature-review` instead. Do not invoke for a 30-second skim — this is for papers that merit 20–40 minutes of careful reading.

## Workflow

### 1. Extract the core claim

Before anything else, state in one sentence what the paper actually claims to show. This is the anchor for everything that follows. If you cannot write this sentence, the paper may be unclear — that is itself a finding.

### 2. Heilmeier catechism

Apply all eight questions. Answer each in 1–3 sentences based on the paper's content:

1. **What are you trying to do?** (The problem, plainly stated)
2. **How is it done today? What are the limits?** (Prior work and its gaps)
3. **What is new in your approach? Why will it succeed?** (The key technical idea)
4. **Who cares?** (Who benefits and why they should adopt this)
5. **If successful, what difference will it make?** (Quantified impact, not vague claims)
6. **What are the risks and how are they mitigated?** (Failure modes the authors acknowledge)
7. **How long will it take?** (Scope of contribution — is this a full system or a component?)
8. **What are the mid-term and final exams?** (Experiments — are they the right tests of the claim?)

Flag any question the paper dodges or answers poorly — these are the paper's weak points.

### 3. Methodology audit

For each major methodological choice, ask:
- **Is the choice justified?** (Or assumed without argument)
- **What happens if the assumption is wrong?** (Sensitivity)
- **Was this choice made before or after seeing the results?** (HARKing risk)

Specific checks by paper type:

| Paper type | Key questions |
|------------|--------------|
| Empirical ML | Hyperparameter search scope, random seed disclosure, test set used for early stopping?, statistical significance |
| Medical imaging | Dataset demographics, IRB statement, train/val/test split (patient-level, not slice-level), comparison to radiologist baseline |
| Causal / theoretical | Assumptions stated explicitly?, identifiability proven or assumed?, simulation vs. real data |
| Survey / position | Coverage systematic or cherry-picked?, criteria for inclusion stated? |

### 4. Results honesty check

- Do the numbers in the abstract match the tables?
- Are error bars/standard deviations reported?
- Is the best result the average or the cherry-picked run?
- Are negative results or failure cases shown?
- Does the ablation actually isolate the claimed contribution, or does it bundle multiple changes?

### 5. Significance assessment

Rate on three axes (1–3):

| Axis | 1 | 2 | 3 |
|------|---|---|---|
| **Novelty** | Incremental variation | Clear new idea | Paradigm shift |
| **Rigour** | Missing baselines / stats | Adequate | Exemplary |
| **Relevance to VIOS** | Tangential | Useful component | Core to ongoing work |

### 6. Output

Structure the output as:

```
CORE CLAIM: <one sentence>

HEILMEIER ANSWERS:
  1. ...  2. ...  (etc.)

METHODOLOGY CONCERNS:
  - [concern] — [why it matters]

RESULTS HONESTY:
  - [finding]

SIGNIFICANCE: Novelty X/3 | Rigour X/3 | VIOS Relevance X/3

VERDICT: [Cite confidently | Cite with caveats (state them) | Do not cite | Replicate and verify]

FOLLOW-UP ACTIONS:
  - [e.g., "Ask authors for code", "Check if dataset is publicly available", "Compare against our baseline on X"]
```

## Anti-patterns

- **Do not** summarise the abstract and call it analysis.
- **Do not** assume the numbers in the paper are correct — check internal consistency.
- **Do not** confuse novelty with significance. A novel trick can be insignificant; a known technique applied to a new domain can be highly significant.
- **Do not** treat a missing ablation as a minor issue — it often means the claimed contribution is not isolated.

## See also

- `literature-review` for synthesis across multiple papers.
- `venue-reviewer` if the paper is yours and you want venue-specific critique.
- `pre-submission-review` if you are the author.
