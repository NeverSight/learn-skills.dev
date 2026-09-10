---
name: ligandmpnn
description: Design protein sequences around ligand or small-molecule contexts with LigandMPNN-style workflows. Use when a task asks for ligand-aware protein design, residue redesign, constraints, or design ranking.
---

# LigandMPNN

Use this skill for ligand-aware protein sequence design.

Workflow:

1. Record the input structure, ligand identity, chain/residue design mask, fixed residues, symmetry, and design objective.
2. Verify the execution route and model availability before running.
3. Save input structure, ligand file, residue masks, command, seeds, model version, generated FASTA, and score tables.
4. Filter outputs by constraint satisfaction, sequence diversity, known motifs, predicted structure confidence, and ligand-contact plausibility.
5. Send shortlisted designs through an independent structural or literature/database check before presenting them as candidates.

Generated designs must remain tied to exact input structures and constraints.
