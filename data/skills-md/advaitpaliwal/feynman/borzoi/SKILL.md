---
name: borzoi
description: Use Borzoi-style regulatory genomics models for sequence-to-expression or variant-effect analysis. Use when the task asks for noncoding variant impact, regulatory sequence design, or expression prediction.
---

# Borzoi

Use this skill for regulatory genomics modeling around sequence, variant, and expression effects.

Workflow:

1. Pin genome build, interval coordinates, reference/alternate alleles, cell type or tissue, strand, and window size.
2. Confirm the model route: local checkpoint, managed endpoint, notebook package, or external documented service. Record missing checkpoints as setup work, not as a completed model run.
3. Build input FASTA/variant manifests with source URLs or accession IDs.
4. Save prediction arrays, summary tables, plots, model version, and runtime metadata as Feynman artifacts.
5. Compare predicted effects against GTEx, ENCODE, literature, or other source-backed evidence when available.

Keep source-owned genomic coordinates separate from model-owned effect predictions in every output.
