---
name: experiment-code
description: Write ML experiment code with iterative improvement. Generate training/evaluation pipelines, debug errors, and optimize results through code reflection. Use when implementing experiments for a research paper.
argument-hint: [plan-or-idea]
---

# Experiment Code

Generate and iteratively improve ML experiment code for research papers.

## Input

- `$0` — Task: `generate`, `improve`, `debug`, `plot`
- `$1` — Research plan, idea description, or error message

## References

- Experiment prompts and patterns: `~/.claude/skills/experiment-code/references/experiment-prompts.md`
- Code patterns (error handling, repair, hill-climbing): `~/.claude/skills/experiment-code/references/code-patterns.md`

## Action: `generate`

Generate initial experiment code following this structure:

1. **Plan experiments first** — List all runs needed (hyperparameter sweeps, ablations, baselines)
2. **Write self-contained code** — All code in project directory, no external imports from reference repos
3. **Include proper logging** — Save results to JSON, print intermediate metrics
4. **Generate figures** — At minimum Figure_1.png and Figure_2.png

### Mandatory Structure
```
project/
├── experiment.py      # Main experiment script
├── plot.py            # Visualization script
├── notes.txt          # Experiment descriptions and results
├── run_1/             # Results from run 1
│   └── final_info.json
├── run_2/
└── ...
```

### Constraints
- No placeholder code (`pass`, `...`, `raise NotImplementedError`)
- Must use actual datasets (not toy data unless explicitly requested)
- PyTorch or scikit-learn preferred (no TensorFlow/Keras)
- Each run uses: `python experiment.py --out_dir=run_i`

## Action: `improve`

Improve existing experiment code:
1. Read current code and results
2. Reflect on what worked and what didn't
3. Apply targeted edits (prefer small edits over full rewrites)
4. Re-run and compare scores
5. Keep the best-performing code variant

## Action: `debug`

Fix experiment code errors:
1. Read the error message (truncate to last 1500 chars if very long)
2. Identify the root cause
3. Apply minimal fix
4. Up to 4 retry attempts before changing approach

## Action: `plot`

Generate publication-quality plots from experiment results:
1. Read all `run_*/final_info.json` files
2. Generate comparison plots with proper labels
3. Use the figure-generation skill for styling

## Rules

- Always plan experiments before writing code
- After each run, document results in notes.txt
- Include print statements explaining what results show
- Method MUST not get 0% accuracy — verify accuracy calculations
- Use seeds for reproducibility
- Before each experiment include a print statement explaining exactly what the results are meant to show

## Related Skills
- Upstream: [experiment-design](../experiment-design/), [algorithm-design](../algorithm-design/)
- Downstream: [data-analysis](../data-analysis/), [backward-traceability](../backward-traceability/)
- See also: [code-debugging](../code-debugging/), [paper-to-code](../paper-to-code/)
