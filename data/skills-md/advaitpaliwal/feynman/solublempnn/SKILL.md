---
name: solublempnn
description: Design or screen protein sequences for solubility-aware constraints with SolubleMPNN-style workflows. Use when a task asks for soluble protein design, expression-friendly variants, or solubility risk filtering.
---

# SolubleMPNN

Use this skill for solubility-aware protein design.

Workflow:

1. Record input structure or sequence, design positions, expression system, forbidden motifs, and stability/solubility constraints.
2. Verify model availability and execution path before running.
3. Save input files, masks, command, model version, generated sequences, scores, and filtering tables.
4. Filter candidates for hydrophobic patches, charge balance, repeats, liabilities, conservation, and structure-confidence impact.
5. Attach assay or expression-screen recommendations when a decision depends on solubility.

Do not equate a solubility score with confirmed expression.
