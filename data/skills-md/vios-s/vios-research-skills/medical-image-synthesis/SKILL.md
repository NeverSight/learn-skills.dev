---
name: medical-image-synthesis
description: Use this skill when the user is generating, evaluating, or auditing synthetic medical images using generative models. Triggers include "evaluate my diffusion model for chest X-rays", "check if my model memorises training data", "generate counterfactual images", "concept erasure in my generative model", "benchmark my synthetic data quality", "does my synthetic data preserve clinical realism", or "evaluate generated MRI/X-ray quality". Handles generation pipeline design, clinical realism evaluation, memorisation detection, counterfactual generation, and bias in synthetic data. Do not use for fairness analysis of discriminative classifiers — use fairness-medical-imaging instead.
license: MIT
metadata:
  category: "Domain: Medical Imaging"
  version: "0.1.0"
  author: "VIOS Lab, University of Edinburgh"
---

# Medical Image Synthesis

A skill for designing, evaluating, and auditing generative models applied to medical imaging. VIOS has deep expertise here — including CheXGenBench (the first benchmark for chest X-ray generation), CRCE (concept erasure in diffusion models), MemControl (memorisation detection and mitigation), and causal counterfactual generation via Causal-Adapter.

## When to invoke this skill

- You are training or fine-tuning a diffusion model, GAN, or VAE on medical images and need an evaluation plan
- You want to assess whether synthetic images are clinically realistic beyond FID
- You need to detect or mitigate training data memorisation in a generative model
- You want to generate counterfactual images (e.g., "what would this scan look like if the patient were female?")
- You are using concept erasure to remove a spurious or sensitive concept from a generative model
- You are building a synthetic data augmentation pipeline and need to know whether it introduces or amplifies bias

## Workflow

### 1. Define the generation goal

Before writing any code, state the generation goal explicitly:

```
Goal: Generate [modality] images of [anatomy/pathology] 
      with the property [clinical condition / attribute / counterfactual contrast].
      These images will be used for [downstream task].
      The evaluation standard is [clinical realism / dataset augmentation / counterfactual analysis].
```

This goal determines which metrics matter:

| Use case | Primary metric | Secondary metrics |
|----------|---------------|-------------------|
| Dataset augmentation (train on synthetic) | Downstream classifier AUC on real test set | FID, diversity |
| Clinical realism benchmark | CSEval / radiologist study | FID, SSIM, LPIPS |
| Counterfactual generation | Attribute manipulation accuracy | Preservation of non-targeted features |
| Concept erasure | Concept probe accuracy post-erasure | Unrelated concept accuracy |
| Memorisation detection | Duplication score / MemControl metric | Coverage, diversity |

### 2. Generation pipeline design

**Modality-specific defaults:**

| Modality | Backbone | Conditioning | Typical training issues |
|----------|----------|--------------|------------------------|
| Chest X-ray | Stable Diffusion (fine-tuned) | Pathology label or report text | Label leakage, memorisation of rare cases |
| MRI (cardiac / brain) | DDPM or LDM | Anatomy mask or segmentation | Mode collapse on pathological shapes |
| Dermoscopy / histology | DinoV2 encoder + diffusion | Lesion class | Texture hallucination |

For text-conditioned generation (report → image): use anatomy-grounded prompt tuning rather than raw report embeddings — raw reports contain demographic proxies (patient name, age, site) that are encoded into the latent and produce biased outputs. See Vilouras et al. (arXiv 2025) for anatomy-grounded weakly supervised prompt tuning.

**Counterfactual generation checklist:**
- [ ] Identify the causal graph: which attribute is the intervention target? Is it a direct cause of pathology, or a confounder? Use `causal-dag-builder` if uncertain.
- [ ] Choose the intervention mechanism: latent space editing (e.g., Causal-Adapter, Tong et al. arXiv 2025) vs. concept erasure (CRCE, Xue et al. BMVC 2025) vs. classifier-free guidance reweighting.
- [ ] Verify counterfactual consistency: non-intervened regions must not change. Measure pixel-level similarity outside the intervention region.

### 3. Clinical realism evaluation

Do **not** rely on FID alone. FID captures distributional similarity but is insensitive to clinically implausible artefacts. A low-FID model can still hallucinate findings or suppress real pathology.

**Evaluation stack (in order of increasing cost):**

**Level 1 — Automated metrics (always run):**
- FID (Fréchet Inception Distance) — distributional similarity
- SSIM and LPIPS — structural similarity for paired synthesis
- Precision and Recall (Kynkäänniemi et al.) — separate fidelity from coverage
- Pathology prevalence match — does the synthetic dataset match the real class distribution?

**Level 2 — Clinical semantic evaluation:**
Use CSEval (Cronshaw et al., arXiv 2026) or equivalent: run a reference clinical classifier (e.g., CheXNet) on synthetic images. Report:
- Finding-level AUC on synthetic images vs. real label → "clinical accuracy"
- Finding presence rate in synthetic images matching real prevalence

**Level 3 — Downstream task evaluation:**
Train a downstream classifier on synthetic-only data; evaluate on a held-out real test set. Report the "synthetic-to-real gap":

```
Synthetic-to-Real Gap = AUC(real train) − AUC(synthetic train)
```

A gap < 0.03 AUC on the primary finding is considered acceptable for augmentation use cases.

**Level 4 — Human expert study (for publication):**
For Nature Medicine, MICCAI, or any clinical AI venue: include a Turing test (radiologist rates real vs. synthetic, report AUC) or a diagnostic equivalence study.

### 4. Memorisation detection and mitigation

Diffusion models fine-tuned on small medical datasets are at high risk of memorising training images, which is a privacy violation and inflates realism metrics.

**Detection — MemControl protocol (Dutt et al., WACV 2025):**
1. For each generated image, compute nearest-neighbour distance to all training images in feature space (use a DINO or CLIP encoder, not Inception — Inception is not specific enough for medical images).
2. Flag images where nearest-neighbour distance < memorisation threshold τ (set τ using a calibration set of known duplicates).
3. Report: memorisation rate (% flagged), average nearest-neighbour distance, worst-case memorisation score.

**Mitigation options:**

| Approach | When to use | Limitation |
|----------|-------------|------------|
| Differential privacy (DP-SGD) | Privacy guarantee required | Degrades image quality significantly |
| MemControl regularisation | Balancing privacy and quality | Requires memorisation-aware training loop |
| Output filtering | Post-hoc, fast | Reduces diversity; doesn't prevent memorisation in the model |
| Dataset deduplication | Before training | Doesn't help with near-duplicate augmentations |

### 5. Concept erasure

Use when a trained generative model has encoded a spurious or sensitive concept (e.g., race, scanner manufacturer, hospital watermark) that you want to remove without retraining from scratch.

**CRCE protocol (Xue et al., BMVC 2025):**
1. Define the target concept C and a set of coreference concepts {C₁, ..., Cₙ} that should be preserved (e.g., erase "scanner brand" while preserving "pathology").
2. Measure concept presence: train a linear concept probe on the diffusion model's U-Net activations. Record baseline probe accuracy for C and all Cᵢ.
3. Apply CRCE: fine-tune the cross-attention layers to minimise C-concept activation while maximising coreference retention loss.
4. Re-measure: probe accuracy for C should drop to ≤ chance; probe accuracy for Cᵢ should remain ≥ 95% of baseline.
5. Evaluate generation quality: run FID and CSEval. Report quality degradation from erasure.

**Do not** use naive negative fine-tuning (training on "this image has no [concept]") — it degrades generation quality for related concepts. CRCE's coreference-retention term specifically addresses this.

### 6. Benchmarking against CheXGenBench

For chest X-ray synthesis work, compare against the CheXGenBench (Dutt et al., arXiv 2025) leaderboard:

1. Use the CheXGenBench evaluation protocol: same splits, same reference classifiers, same memorisation detection threshold.
2. Report results in the CheXGenBench table format: FID / Precision / Recall / CSEval / Memorisation rate.
3. If claiming SOTA: verify the comparison models used the same training data and conditioning. CheXGenBench distinguishes unconditional, label-conditioned, and report-conditioned generation — compare within the same category.

### 7. Reporting checklist for publication

For MICCAI, Nature Machine Intelligence, Medical Image Analysis:
- [ ] Generation goal stated (augmentation / realism study / counterfactual / concept erasure)
- [ ] FID + at least one clinical realism metric (CSEval or radiologist AUC) reported
- [ ] Memorisation detection run and rate reported
- [ ] Counterfactual consistency verified quantitatively (for counterfactual generation)
- [ ] Synthetic-to-real gap reported (for augmentation use cases)
- [ ] Training dataset size and pathology prevalence reported (memorisation risk scales with dataset size)
- [ ] Limitations: which findings / subgroups had insufficient real training samples

## Anti-patterns

- **Do not** report only FID and claim clinical realism — FID does not detect hallucinated findings or suppressed pathology. A radiologist cannot diagnose from a low-FID but clinically wrong image.
- **Do not** evaluate synthetic data quality on the same dataset used for training — the model may have memorised those images. Always use a held-out reference set for all metrics.
- **Do not** use concept erasure and claim the model is "unbiased" — erasure removes a specific concept from the generative latent space but does not guarantee fairness in downstream discriminative models trained on the synthetic data. Use `fairness-medical-imaging` for that evaluation.
- **Do not** report synthetic-to-real gap as the only augmentation benefit — also check that the synthetic data adds diversity (not just copies of real images) using the Recall metric.
- **Do not** generate counterfactuals by directly interpolating in pixel space — this creates unrealistic mid-states. Use latent space interventions (Causal-Adapter) or guidance reweighting.

## See also

- `fairness-medical-imaging` for evaluating whether synthetic data pipelines inherit or amplify demographic biases.
- `causal-dag-builder` for defining the causal structure before designing counterfactual generation experiments.
- `venue-reviewer` for venue-specific evaluation requirements (MICCAI requires IRB; Nature Medicine requires radiologist studies).
