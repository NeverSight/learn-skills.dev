---
name: esmfold2
description: Predict quick protein structures with ESMFold-style workflows. Use when a task needs fast MSA-free folding, sequence triage, variant structure screening, or confidence review.
---

# ESMFold2

Use this skill when a fast protein fold hypothesis is useful before heavier structure prediction.

Workflow:

1. Normalize sequences into FASTA and record identifiers, mutations, truncations, domains, and oligomer assumptions.
2. Verify the local or endpoint route before running.
3. Save FASTA, model version, command or request body, predicted PDB/mmCIF, pLDDT/confidence outputs, and logs.
4. Flag low-confidence regions, missing multimers, disorder, membrane regions, and sequence lengths outside the chosen route's limits.
5. Use RDKit/3Dmol/PDB previews and source-backed comparisons when the output influences a research decision.

Use ESMFold-style predictions for triage unless an independent check supports the structural claim.
