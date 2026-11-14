---
name: repro-pack
description: "Plan and track baseline/method reproduction and build reproducibility packages: code, data provenance, environment, configs, exact commands, seeds, logs, metrics, figures, checksums, and known issues. Use for baseline reproduction, reproducing paper results, Repro Pack, artifact appendices, open-source release prep, or experiment handoff."
---

# Repro Pack

Create a runnable, reviewable package, not just a README.

## Baseline Reproduction

For reproducing a paper/method inside a research project, follow the Reproduction section of [`ai-research-workflow/references/project-workflow.md`](../ai-research-workflow/references/project-workflow.md#reproduction从方法到可信-baseline) and its method template. Keep the target paper setting distinct from evaluation on the user's own dataset, inspect official code availability, fix data/evaluation versions, run a small smoke test, and verify the precommitted target before marking the result reproduced. Preserve partial/failed/stopped runs and deviations. Formal run reports use [`experiment-report-writing`](../experiment-report-writing/SKILL.md); data source/copy handling uses [`research-dev-standards`](../research-dev-standards/SKILL.md). Package artifacts for handoff/release when that is the requested deliverable.

## Reproducibility Package

Recommended structure:

```text
repro-pack/
  README.md
  environment.yml / requirements.txt / Dockerfile
  data/README.md
  data/checksums.txt
  configs/
  scripts/train.sh
  scripts/eval.sh
  scripts/reproduce_tables.sh
  logs/
  results/tables/
  results/figures/
  model_cards/
  commit.txt
  known_issues.md
```

Always capture exact commands, commit hash, dataset version, seeds, hardware, runtime, and expected outputs. Validate by running the smallest representative reproduce command when feasible.

Link original dataset manifests, project-derived versions and preprocessing configs, fixed split lists/hashes, and the evaluation protocol version. Do not copy protected/raw datasets into a release package by default; include permitted acquisition and independent-copy/processing instructions. Record both the paper's reported result and the inspected reproduction result with their comparability limits.
