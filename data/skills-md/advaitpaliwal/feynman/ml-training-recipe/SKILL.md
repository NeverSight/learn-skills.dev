---
name: ml-training-recipe
description: Find implementable ML training recipes from papers, datasets, docs, and code. Use when the user wants to fine-tune, train, reproduce, or choose a practical ML method, dataset, hyperparameter setup, or benchmark recipe.
---

# ML Training Recipe

Run the `/recipe` workflow. The slash command expands the full workflow instructions in the active session; do not try to read a relative prompt-template path from the installed skill directory.

Agents used: `researcher`, optionally `verifier`

Output: ranked recipe brief in `outputs/` with dataset, method, code, and source provenance.
