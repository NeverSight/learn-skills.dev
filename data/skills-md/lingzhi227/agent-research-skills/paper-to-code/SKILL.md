---
name: paper-to-code
description: Convert an ML research paper into a complete, runnable code repository. 3-stage pipeline from Paper2Code — Planning (UML + dependency graph) → Analysis (per-file logic) → Coding (dependency-ordered generation). Use for reproducing paper methods.
argument-hint: [paper-pdf-or-text]
---

# Paper to Code

Convert a research paper into a complete, runnable code repository.

## Input

- `$0` — Paper PDF path, paper text, or paper URL

## References

- Paper2Code prompts (planning, analysis, coding stages): `~/.claude/skills/paper-to-code/references/paper-to-code-prompts.md`

## Workflow (from Paper2Code)

### Stage 1: Planning
Four-turn conversation to create a comprehensive plan:

1. **Overall Plan**: Extract methodology, experiments, datasets, hyperparameters, evaluation metrics
2. **Architecture Design**: Generate file list, Mermaid classDiagram, sequenceDiagram
3. **Task Breakdown**: Logic analysis per file, dependency-ordered task list, required packages
4. **Configuration**: Extract training details into `config.yaml`

### Stage 2: Analysis
For each file in the task list (dependency order):
1. Conduct detailed logic analysis
2. Map paper methodology to code structure
3. Reference the config.yaml for all settings
4. Follow the UML class diagram interfaces strictly

### Stage 3: Coding
For each file in dependency order:
1. Generate code with access to all previously generated files
2. Follow the design's data structures and interfaces exactly
3. Reference config.yaml — never fabricate configuration values
4. Write complete code — no TODOs or placeholders

### Stage 4: Debugging (if needed)
If execution fails:
1. Collect error messages
2. Identify root cause using SEARCH/REPLACE diff format
3. Apply minimal fixes preserving original intent
4. Re-run until successful

## Output Structure

```
reproduced_code/
├── config.yaml        # Training configuration
├── main.py            # Entry point
├── model.py           # Model architecture
├── dataset_loader.py  # Data loading
├── trainer.py         # Training loop
├── evaluation.py      # Metrics and evaluation
├── reproduce.sh       # Run script
└── requirements.txt   # Dependencies
```

## Key Constraints

- **Dependency order**: Each file is generated with access to all previously generated files
- **Interface contracts**: Mermaid diagrams serve as rigid interface definitions across all stages
- **No fabrication**: Only use configurations explicitly stated in the paper
- **Complete code**: Every function must be fully implemented

## Rules

- Follow the paper's methodology exactly — do not invent improvements
- Generate code in dependency order (data loading → model → training → evaluation → main)
- Use config.yaml for all hyperparameters and settings
- Every class/method in UML diagram must exist in code
- Generate a reproduce.sh script for one-command execution
- If paper details are ambiguous, note them explicitly

## Related Skills
- Upstream: [literature-search](../literature-search/)
- Downstream: [experiment-code](../experiment-code/)
- See also: [code-debugging](../code-debugging/), [algorithm-design](../algorithm-design/)
