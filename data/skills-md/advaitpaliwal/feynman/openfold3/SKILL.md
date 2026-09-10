---
name: openfold3
description: Run or plan OpenFold3-style structure prediction workflows. Use when a task asks for open protein or complex prediction, setup, model comparison, or reproducibility around OpenFold-family outputs.
---

# OpenFold3

Use this skill for OpenFold-family structure prediction or comparison.

Workflow:

1. Normalize FASTA, chains, templates, MSAs, ligands or partners, seeds, and expected output format.
2. Verify model code, checkpoints, databases, and GPU route before running.
3. Save the input manifest, environment lockfile, command, logs, structure outputs, confidence files, and runtime metadata.
4. Compare against AlphaFold-style, ESMFold-style, PDB, or literature evidence when the result affects a decision.
5. Report reproducibility gaps such as missing databases, unavailable weights, failed templates, or route-specific approximations.

Do not present an OpenFold-family output without version and input provenance.
