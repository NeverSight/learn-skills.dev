---
name: diffdock
description: Run or plan DiffDock molecular docking workflows. Use when a task asks for protein-ligand pose prediction, docking setup, ligand/protein preparation, pose ranking, or docking-result verification.
---

# DiffDock

Use this skill for protein-ligand docking and pose review.

Workflow:

1. Record protein source, chain selection, binding site context, ligand identity, protonation/tautomer assumptions, and known cofactors.
2. Verify the available execution path and dependency stack before claiming a docking run is possible.
3. Preserve input PDB/mmCIF, ligand SDF/SMILES, prepared structures, command, seed, package version, and logs.
4. Save ranked poses, confidence scores, contact summaries, and 3D previews as Feynman artifacts.
5. Compare poses against known ligands, active-site residues, experimental structures, or orthogonal docking where the conclusion matters.

Report docking as a ranked hypothesis, not binding proof.
