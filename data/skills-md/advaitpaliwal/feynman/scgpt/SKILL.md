---
name: scgpt
description: Use scGPT-style single-cell foundation model workflows. Use when a task asks for single-cell embeddings, perturbation prediction, cell annotation, batch transfer, or gene-program analysis.
---

# scGPT

Use this skill for single-cell foundation model analysis.

Workflow:

1. Record dataset source, organism, modality, preprocessing, gene identifiers, cell labels, and perturbation design.
2. Verify model/checkpoint/package availability before running.
3. Save AnnData or matrix manifests, preprocessing code, model version, embeddings, predictions, plots, and logs.
4. Compare labels or predictions against source metadata, marker genes, perturbation controls, and literature.
5. Preserve batch, donor, disease, and assay provenance in every summary table.

Do not present cell-state labels without marker or metadata support.
