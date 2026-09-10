---
name: indication-dossier
description: Build a source-backed biomedical indication dossier. Use when a research task asks for disease biology, target rationale, patient segmentation, biomarkers, trials, drugs, competitive landscape, or translational evidence.
---

# Indication Dossier

Use this skill to assemble a biomedical evidence packet for a disease, target, mechanism, biomarker, or therapy.

Workflow:

1. Define the indication, patient segment, intervention or target, and decision the dossier must support.
2. Gather evidence from literature, clinical trials, Open Targets, ChEMBL, CIViC, ClinGen, cBioPortal, DepMap/COSMIC-compatible sources, and other Feynman Bio Tools as relevant.
3. Separate human evidence, model-system evidence, mechanism, biomarkers, clinical precedent, safety, and open questions.
4. Rank claims by source strength and reproducibility. Flag missing cohorts, confounders, and assay limitations.
5. Save the dossier and provenance sidecar in `outputs/`.

Do not turn sparse evidence into a clinical recommendation.
