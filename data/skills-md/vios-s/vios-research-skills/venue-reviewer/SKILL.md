---
name: venue-reviewer
description: Use this skill when the user wants to evaluate a paper against specific venue acceptance criteria. Triggers include "will this be accepted at NeurIPS", "review from a MICCAI perspective", "what does Nature look for", "NeurIPS reproducibility checklist", "ICLR review criteria", "CVPR acceptance bar", "check for MICCAI requirements", "is this too incremental for ICML", or naming any specific conference or journal as a target. Applies venue-specific checklists and rejection-risk analysis. Covers NeurIPS, ICLR, ICML, CVPR/ICCV/ECCV, MICCAI, Nature family, IEEE TPAMI, and Medical Image Analysis. For a general pre-submission quality check before venue selection, use pre-submission-review first.
license: MIT
metadata:
  category: "Review & Dissemination"
  version: "0.1.0"
  author: "VIOS Lab, University of Edinburgh"
---

# Venue Reviewer

A skill for stress-testing a paper against the specific acceptance culture and criteria of a target venue. Different venues reward very different things — a NeurIPS-style paper with 12 ablation tables will feel over-engineered for Nature; a Nature-style narrative paper will feel under-specified for ICLR.

## When to invoke this skill

- You have a paper near completion and are choosing or have chosen a venue
- You want to know the top 3 reasons your paper might be rejected at a specific venue
- You need to check venue-specific mandatory requirements (e.g., NeurIPS checklist, MICCAI ethics statement)
- You want to reframe or rewrite the paper for a different venue than the one it was originally written for

Run `pre-submission-review` first for a general quality check. This skill adds the venue lens on top.

## Workflow

### 1. Confirm the venue and paper

Ask:
- Which venue exactly? (NeurIPS 2025, MICCAI 2025, Nature, etc.)
- Is this the primary target or a fallback?
- Is the paper available for review?

### 2. Apply venue-specific checklist

Select the section for the target venue below.

---

## Venue Profiles

---

### NeurIPS

**Format:** 9 pages content + unlimited references + appendix. Double-blind.

**Review criteria (1–4 scale each):**
- **Soundness**: Is the work technically correct and rigorous?
- **Significance**: Does it advance the field in a meaningful way?
- **Originality**: Is the core idea new?
- **Presentation**: Is it clear and well-organised?

**Mandatory:**
- [ ] NeurIPS Paper Checklist completed (available on the submission site — 15 items covering claims, limitations, theory, experiments, reproducibility, ethics, broader societal impact)
- [ ] Broader impact statement in the paper body
- [ ] Code/data availability statement

**Acceptance culture:**
- NeurIPS rewards rigour and reproducibility above all. A beautiful idea with weak experiments will be rejected; solid experiments on a known idea can still be accepted if they resolve an open question.
- Ablations are expected. A methods paper without ablations is almost always desk-rejected at review stage.
- Theoretical grounding is valued but not required — empirical papers are common, but claims must be tightly supported.
- The bar for novelty has risen sharply; incremental improvements on benchmark datasets without insight are increasingly rejected.

**Top rejection risks:**
1. Reproducibility checklist not filled or filled superficially
2. Missing ablation or ablation not isolating claimed contributions
3. Experiments only on small or toy datasets when SOTA benchmarks exist

**Reframe tips:**
- Lead with the insight, not the method. NeurIPS reviewers respond to "we discover that X happens because Y" more than "we propose method Z".
- Put the checklist first in the supplementary — reviewers look for it.
- Report mean ± std over 5 seeds, not single-run results.

---

### ICLR

**Format:** 8 pages + appendix. Double-blind. OpenReview (reviews are public).

**Review criteria:** Soundness, presentation, contribution — rated 1–10 with detailed written justification. Reviews, rebuttals, and author responses are all public.

**Acceptance culture:**
- ICLR is representation learning focused but has broadened considerably. Generative models, foundation models, and theory all appear.
- Reproducibility is paramount — code must be submitted with the paper (or clearly stated why not).
- The public nature of OpenReview means reviewers write more carefully; use this by writing clear, citable responses in the rebuttal.
- Average acceptance rate ~30% (oral ~5%). Borderline papers often get rejected if the rebuttal does not convincingly close the gap.
- Strong empirical results on well-known benchmarks (ImageNet, GLUE, etc.) are expected for methods papers.

**Top rejection risks:**
1. No code or clear code commitment
2. Results not reproducible from the paper description alone
3. Related work misses close concurrent work (OpenReview reviewers cross-reference easily)

**Reframe tips:**
- Spend the first page establishing the research question, not the method — ICLR readers are diverse.
- If your ablation shows a component is marginal, acknowledge it; ICLR reviewers respect honesty.
- Cite recent arXiv preprints that are relevant even if unpublished.

---

### ICML

**Format:** 8 pages + appendix. Double-blind.

**Acceptance culture:**
- ICML has a strong theory culture alongside empirical work. Even empirical papers benefit from a theoretical section explaining *why* the method works.
- Generalisation across tasks is valued — experiments on one dataset with one architecture raise concerns.
- ICML rejects papers that are correct but not *interesting*. The "so what" question is taken seriously.
- Machine learning for science papers are increasingly welcome; clinical/medical papers need to make a machine learning contribution, not just an application.

**Top rejection risks:**
1. No theoretical grounding or intuition for why the method works
2. Experiments limited to a single benchmark or architecture family
3. Contribution positioned as "we apply X to Y" rather than "we discover/enable/prove Z"

---

### CVPR / ICCV / ECCV

**Format:** 8 pages + references. Double-blind. (CVPR/ICCV are annual; ECCV biennial.)

**Acceptance culture:**
- The big three computer vision conferences care most about: visual quality of results, ablation thoroughness, and whether the method achieves new state of the art on accepted benchmarks.
- Qualitative results matter more than at ML-focused venues — figures must show the method working convincingly.
- Dataset and benchmark diversity is expected: COCO, ImageNet, ADE20K, Cityscapes depending on the task.
- Compute efficiency is increasingly valued — a method 10× slower than the baseline must offer commensurate improvement.

**Top rejection risks:**
1. Weak or missing qualitative results (reviewers expect figure-heavy appendices)
2. Not evaluated on the standard benchmark for the claimed task
3. Ablation on a toy dataset, main results on the real one — mismatch undermines trust

**Reframe tips:**
- Lead the paper visually — a compelling teaser figure is expected and influences first impressions.
- Put the core architecture figure before the equations.
- CVPR/ICCV/ECCV reviewers check the project page if you link one — make sure the demo is clean.

---

### MICCAI

**Format:** 8 pages (LNCS) + 1 page references. Double-blind.

**Acceptance criteria:** Clinical relevance, methodological soundness, experimental validation, clarity. Acceptance rate ~30%.

**Mandatory for clinical datasets:**
- [ ] IRB / ethics approval statement (or exemption justification)
- [ ] Dataset demographics (age, sex, scanner, institution, pathology distribution)
- [ ] Train/val/test split at patient level, not image/slice level
- [ ] Comparison to radiologist or clinical baseline where applicable

**Acceptance culture:**
- MICCAI requires clinical motivation. A technically excellent paper without a clear clinical need is rejected. The first paragraph of the introduction must answer "why does a clinician care?"
- Datasets must be described in sufficient detail for reproducibility. Proprietary datasets without a plan for release are accepted if the justification is compelling, but public datasets are strongly preferred.
- Evaluation protocol must match clinical practice — Dice alone for segmentation is no longer sufficient; HD95 and inference time expected.
- The methods must be evaluated on at least one public benchmark to enable comparison.

**Top rejection risks:**
1. No clinical motivation stated (the "so what for a patient?" question unanswered)
2. Evaluation only on private/proprietary data
3. Missing IRB statement for human data
4. Patient-level vs. slice-level split confusion inflating results

**Reframe tips:**
- Start with a clinical vignette or statistic that motivates the problem.
- Put the IRB statement in the methods section, not the appendix.
- Compare to the clinical standard of care, not just the ML baseline.

---

### Nature / Nature Machine Intelligence / Nature Medicine

**Format:**
- Nature Article: ~3000 words body + 6 display items (figures/tables) + unlimited supplementary
- Nature Letter (now "Brief Communication"): ~1500 words
- Nature Machine Intelligence: ~15 pages with full methods section
- Nature Medicine: similar to NMI but clinical focus

**Review process:** Initial editor screening (2–4 weeks; >50% rejected before external review). Then 2–3 external reviewers. Rebuttal + revision allowed.

**Acceptance culture:**
- Broad significance to the scientific community — the finding must matter beyond the specific subfield. Ask: "Would a biologist, a clinician, and a computer scientist all care about this?"
- Accessibility: the main text must be readable by a Nature editor (often not a specialist). Jargon and equations belong in the Methods or Supplementary.
- Open data and code are expected: "all data and code required to reproduce the results are available at [URL]."
- Nature Machine Intelligence specifically looks for AI methods with demonstrable real-world impact — pure benchmark improvements without insight are rare acceptances.
- Nature Medicine requires clinical validation — not just promising results in silico.

**Top rejection risks:**
1. Fails the initial editor screen: too narrow, too incremental, or poorly written abstract
2. Broad impact not argued persuasively in the first paragraph
3. Results are state-of-the-art on a benchmark but do not provide a scientific insight

**Reframe tips:**
- The one-sentence summary (required) is your most important sentence — editors use it to decide who to send the paper to.
- Write the abstract for a Science journalist, not a machine learning reviewer.
- Extended Data (up to 10 figures) is where ablations and robustness checks live.
- Avoid jargon in the first two paragraphs of the main text.

---

### IEEE TPAMI / Medical Image Analysis (MIA)

**Format:** Journal — no strict page limit. Single or double review depending on track.

**Acceptance culture:**
- TPAMI expects thoroughness: complete experimental evaluation, strong related work, and often a theoretical contribution.
- MIA expects clinical relevance + methodological novelty + strong evaluation on multiple datasets.
- Both journals accept extended versions of conference papers — expect to add 30% new content (experiments, ablations, or applications).
- Review process is slow (6–18 months for first decision) — plan accordingly.

**Top rejection risks (MIA):**
1. Evaluated only on a single dataset; MIA expects multi-dataset validation
2. No comparison to clinical standard of care
3. Conference extension with insufficient new contribution

**Top rejection risks (TPAMI):**
1. Missing theoretical analysis where the community expects one
2. Related work does not cover the full relevant literature (reviewers are specialists)
3. Experiments do not include the canonical TPAMI benchmarks for the task

---

## 3. Output: Rejection Risk Report

After applying the venue checklist, output:

```
VENUE: [name + year if applicable]

MANDATORY REQUIREMENTS:
  ✓ [met]  /  ✗ [missing]

TOP 3 REJECTION RISKS:
  1. [risk] — [specific evidence from the paper]
  2. ...
  3. ...

VENUE FIT SCORE: [Strong | Good | Marginal | Mismatch]
  Rationale: [1–2 sentences]

RECOMMENDED FIXES (in priority order):
  1. [fix] — effort [low/medium/high]
  2. ...

ALTERNATIVE VENUES (if fit is Marginal or Mismatch):
  - [venue] — reason it may be a better fit
```

## Anti-patterns

- **Do not** apply NeurIPS criteria to a Nature submission or vice versa — the cultures are incompatible.
- **Do not** suggest rewriting the entire paper — focus on the highest-leverage changes for the specific venue.
- **Do not** guarantee acceptance — venue reviewer behaviour is variable; this skill predicts the risks, not the outcome.

## See also

- `pre-submission-review` for general quality check before applying this venue lens.
- `paper-rebuttal-helper` for responding to reviewer concerns after submission.
- `research-paper-writing` for rewriting sections identified as venue-mismatched.
