---
name: ml-engineering
description: >-
  Plan and execute production ML engineering work — model training and
  fine-tuning (LoRA/QLoRA), evaluation and eval-set design, quantization
  decisions, inference deployment, lineage, feature parity, drift response, and
  regression triage, grounded in practical engineering patterns for production ML
  systems. Do not use for statistical
  modeling and experimental design (that's the data scientist) or for operating
  a specific inference engine (that's a tool skill such as llama-cpp or vllm).
license: MIT
metadata:
  tags: ml, machine-learning, fine-tuning, training, evaluation, quantization, mlops,
    inference, vllm, gguf
  source_repo: https://github.com/magnus919/hermes-profiles
---

# ML Engineering Methodology

Machine learning engineering is the bridge between model research and production systems. This methodology covers the engineering disciplines needed to train, evaluate, deploy, and maintain ML models reliably.

## The ML Engineer's Domain

| You own | You don't own |
|---------|--------------|
| Model training — LoRA/QLoRA fine-tuning, full fine-tuning, distributed training | Statistical modeling and experimental design — that's the data scientist |
| Model evaluation — benchmark suites, custom eval sets, regression testing | Causal inference and hypothesis testing — that's the data scientist |
| Quantization — GGUF, GPTQ, AWQ, bitsandbytes | Training data collection and labeling — that's the data/ML ops team |
| Inference serving — [vLLM](../vllm/SKILL.md), [llama.cpp](../llama-cpp/SKILL.md), TGI, Triton | Business metrics and KPI definition — that's the product manager |
| Evaluation harness — lm-eval-harness, custom pipelines | Data pipeline architecture — that's the data engineer |
| Model deployment — containerization, versioning, A/B testing | Infrastructure provisioning — that's the platform engineer |

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/fine-tuning.md` | Setting up a LoRA/QLoRA/ full fine-tuning run — data prep, hyperparameters, validation strategy |
| `references/evaluation.md` | Evaluating a model — benchmark selection, custom eval sets, regression tracking, comparison methodology |
| `references/evaluation-and-lineage.md` | Metric/configuration decisions, repeated stochastic comparisons, end-to-end lineage, temporal feature parity, drift response, and adaptation/serving tradeoffs |
| `references/quantization-inference.md` | Quantizing a model and serving it — GGUF/GPTQ/AWQ/bitsandbytes comparison, calibration data strategies, KV cache quantization, vLLM/llama.cpp/TGI/Triton architecture, production considerations |
| `references/training-infrastructure.md` | Selecting and provisioning training infrastructure — GPU selection, VRAM budgeting, multi-GPU strategies (DDP/FSDP/DeepSpeed), cloud vs on-prem, storage, monitoring |

## Templates

| Template | When to Use |
|-----------|-------------|
| `templates/training-run-record.md` | Recording a training or fine-tuning run — model and data versions, full config, environment, eval results — so it can be reproduced |
| `templates/eval-regression-table.md` | Tracking model quality across runs and triaging a regression — one row per eval case or capability subset |
| `templates/quantization-decision-record.md` | Recording a quantization decision — baseline, candidates compared, quality threshold, and rollback path |
| `templates/model-lineage-record.md` | Linking data/features, code/configuration, runs, artifacts, evaluations, registry state, and deployed serving versions |
| `templates/drift-response-record.md` | Recording drift signals, thresholds, diagnosis, retrain/rollback decisions, and post-action evidence |

## Scripts

| Script | When to Use |
|-----------|-------------|
| `scripts/check-eval-overlap.py` | Checking a training corpus against an eval corpus for test-set leakage (shared n-grams); `--json` for CI, exit 1 when an eval file exceeds the overlap threshold |

## Evals

`evals/evals.json` — output-quality eval manifest for this skill: fine-tuning plan review, eval-set design, quantization decision, deployment plan, regression triage, and training-run reproducibility.

## Core Principles

**Measure before you optimize** — Never quantize, prune, or distill a model without first measuring its baseline performance. Optimization without measurement is guessing.

**Reproducibility is non-negotiable** — Every training run needs a reproducible config: seed, data version, hyperparameters, and evaluation methodology. If you can't reproduce it, you can't ship it.

**Baseline first** — Before running an expensive fine-tuning run, establish a baseline with the base model. If the base model is already good enough, the fine-tuning budget is better spent elsewhere.

**Test at the boundary** — Model evaluation is most informative at the edges of the capability distribution, not at the center. Hard examples reveal more than easy ones.

**The evaluation set is a liability** — Every example in your eval set is a potential test-set leak. Use held-out sets, rotate examples, and periodically audit for contamination with the overlap checker.

## When not to use

Do not use this skill for statistical modeling, experimental design, or causal inference — that's the data scientist's discipline. Do not use it to operate a specific inference engine: for llama.cpp installation, model loading, benchmarking, and troubleshooting, load the [llama-cpp](../llama-cpp/SKILL.md) tool skill instead; for vLLM deployment, model configuration, benchmarking, batching tuning, GPU operation, and upgrade/rollback, load the [vllm](../vllm/SKILL.md) tool skill instead. This skill provides the methodology (eval-set design, quantization trade-offs, deployment plans, regression triage); the tool skills own the runbooks.
