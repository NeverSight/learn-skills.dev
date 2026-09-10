---
name: evo2
description: Use Evo2-style biological sequence models for generation, scoring, or variant-effect analysis. Use when a task asks about DNA/RNA/protein sequence likelihood, editing, design, or long-context biological modeling.
---

# Evo2

Use this skill for biological sequence-model work.

Workflow:

1. Define the sequence type, coordinate system, genome/proteome source, objective, constraints, and evaluation metric.
2. Verify the model endpoint, checkpoint, tokenizer, max context, and license/access boundary before running.
3. Save input sequences, prompts or scoring windows, model version, parameters, seeds, raw outputs, and parsed tables.
4. Separate source-owned biological facts from model-owned scores, generated variants, or predictions.
5. Validate top candidates against databases, conservation, known motifs, structure, or experiments before presenting them as actionable.

Keep generated sequences bounded and auditable.
