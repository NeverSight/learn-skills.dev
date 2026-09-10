---
name: proteinmpnn
description: Design protein sequences from fixed backbone structures with ProteinMPNN-style workflows. Use when a task asks for backbone-conditioned sequence design, mutation suggestions, fixed residues, or design filtering.
---

# ProteinMPNN

Use this skill for fixed-backbone protein sequence design.

Workflow:

1. Record input structure, chain ids, designed positions, fixed residues, tied positions, symmetry, and design objective.
2. Verify the local or remote execution route before running.
3. Save PDB/mmCIF inputs, design masks, command, seeds, model version, FASTA outputs, and score tables.
4. Filter designs by constraints, diversity, motifs, structure prediction, conservation, and assay-ready feasibility.
5. Attach provenance and a verification plan before recommending candidates.

Treat generated sequences as candidates that require structural and experimental validation.
