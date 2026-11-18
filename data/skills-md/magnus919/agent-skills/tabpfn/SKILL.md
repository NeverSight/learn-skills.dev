---
name: tabpfn
description: >-
  Operate and evaluate TabPFN for local tabular classification, regression and
  dataset-specific fine-tuning: checkpoint selection, weight licensing, environment
  setup, training-context leakage, calibration, resource budgeting and reproducible
  inference artifacts. Use for TabPFN package or checkpoint workflows. Do not use
  for generic model selection, operating TabICL, or language-model fine-tuning;
  use ml-engineering, the selected tool, or unsloth respectively.
license: MIT
metadata:
  research-date: "2026-10-13"
  source: "https://github.com/PriorLabs/TabPFN"
---

# TabPFN

Deliver a pinned, task-evaluated TabPFN workflow rather than treating a sklearn-like
API as proof of compatibility, permission or predictive quality. TabPFN learns a
synthetic-data prior during pretraining and conditions on a labeled training table
at inference. Its ordinary `fit` is not necessarily dataset-specific gradient
training; explicit fine-tuning is a distinct operation.

## When not to use

- For choosing among trees, TabPFN, TabICL, sequence models and LLMs, load
  [ml-engineering](../ml-engineering/SKILL.md).
- For statistical design/calibration, use [data-scientist](../data-scientist/SKILL.md).
- For language-model SFT/LoRA/RL, use [unsloth](../unsloth/SKILL.md).
- TabICL has different models/APIs and terms. This skill does not operate it.

## First decision and authority

Identify classification versus regression, local package versus hosted client,
checkpoint generation, data schema and permission, commercial/production scope,
selected accelerator and run destination. Do not silently choose the latest
checkpoint: code and weight terms differ by release. A download may involve
license acceptance and authentication; task authorization does not authorize
accepting terms for the user or sending private tables to a hosted client.

This skill can install packages, download weights, cache labeled tables, run GPU
work and write artifacts. Before first mutation:

> Confirm the target, scope, and rollback path before acting. Read-only discovery may proceed without confirmation.

Use existing explicit authorization when it supplies these facts. Use isolated
run directories and preserve the accepted environment/artifact. Do not delete
models, change drivers or open a service as an incidental setup repair.

## Guide routing

| Task | Read |
|---|---|
| Understand ICL, choose checkpoints, review applicability and limits | [Model and capacity decisions](references/models.md) |
| Install/authenticate, local versus hosted, license and offline boundaries | [Installation and artifacts](references/operations.md) |
| Prepare/split data, preserve prediction-time features, calibrate and compare | [Evaluation workflow](references/evaluation.md) |
| Fine-tune, reload, recover, resolve capacity/column/class failures | [Adaptation and recovery](references/adaptation.md) |
| Check evidence quality, exact sources and unresolved contradictions | [Source ledger](references/sources.md) |

## Execution sequence

1. Run the read-only doctor; record installed package versions. Metadata is not
   import/CUDA compatibility. Select the version-matched official recipe.
2. Record package, checkpoint, tokenizer/text preprocessing if used, code/weight
   license decisions, inference ensemble/subsample settings and local/hosted scope.
3. Freeze train, development/calibration and forward held-out groups. The labeled
   training table is part of the inference artifact; exclude holdout labels/context.
4. Use the local manifest audit to screen limits, group/exact-feature overlap,
   prediction-time feature availability, label maturity and unseen classes.
   It only checks declared timestamps/groups and policy; semantic data review
   remains necessary. Align columns/types and preserve train-only preprocessing.
5. Run a small version-matched load/fit/predict with actual device/memory and
   offline/egress evidence. Never equate model ceilings to capacity of this GPU.
6. Compare a simple/tree incumbent and TabPFN on identical rows, permitted
   features, tuning budgets and calibration policy. Keep per-class/time/group
   regressions and complete-task resource/cost results.
7. Fresh-process reload must preserve checkpoint plus labeled context, columns,
   transforms and configuration. Test independently scored holdout predictions.

Use [the run worksheet](templates/run-record.md). Complete when the requested
surface executes, original evidence is retained, fresh reload and task scoring
are verified, and all agreed quality/resource/permission constraints hold.
Otherwise report exact failed/not-run stages. Stop after three nonconverging
compatibility passes with a minimal reproducer and version inventory.

## Local helper

From this skill root, Python 3.10+ and standard library only:

```bash
python3 scripts/tabpfn_check.py doctor
python3 scripts/tabpfn_check.py audit templates/task-manifest.json
python3 -m unittest discover -s scripts -p 'test_*.py'
```

The bundled manifest is a synthetic contract example, not a measured model run.
The auditor accepts classification/regression, three nonempty grouped forward
splits, checkpoint/package/license records and explicit row/feature policy limits.
It prints counts/codes/row numbers and a file hash, never table values or group
identities. Exit 0 clears those checks, 1 means findings/invalid input, 2 means
invalid CLI arguments. It neither loads models nor proves license approval,
true feature timestamps, calibration, GPU placement or absence of semantic leakage.
Maximum manifest size is 16 MiB. It intentionally does not audit arbitrary CSV,
pretrained-model leakage, GPU capacity or hosted payload transfers.

## Evidence boundary

The offline helper tests ran. Local TabPFN loading, checkpoint authentication,
prediction, fine-tuning and GPU execution were not performed for this skill's
research. Official reports and vendor limits are source evidence, not locally
reproduced performance. Keep these distinctions in every delivery record.
