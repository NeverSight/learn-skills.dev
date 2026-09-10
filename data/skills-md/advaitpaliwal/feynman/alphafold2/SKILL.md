---
name: alphafold2
description: Predict or audit protein structures with AlphaFold2-style workflows. Use when a research task needs monomer/multimer structure prediction, MSA/template handling, confidence metrics, or comparison against PDB/AlphaFold references.
---

# AlphaFold2

Use this skill for protein-structure prediction or parity checks around AlphaFold2-style outputs.

Workflow:

1. Capture the biological question, sequence identifiers, FASTA input, oligomer state, organism, and expected cofactors or partners.
2. Verify the execution route before running: local install, managed endpoint, Modal/SSH job, or a documented public source. Do not assume weights, databases, or GPUs exist.
3. Save inputs, command or endpoint payload, model settings, stdout/stderr, and raw outputs under the active Feynman artifact folder.
4. Report pLDDT, PAE, ranking confidence, chain coverage, truncation, templates/MSA provenance, and any residues or interfaces that should not be trusted.
5. Compare against known structures or AlphaFold DB records when the claim depends on novelty, domain movement, interface geometry, or mutation impact.

Outputs should include the FASTA, predicted PDB/mmCIF, confidence files when available, a short method note, and a `.provenance.md` sidecar.
