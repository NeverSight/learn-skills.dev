---
name: unsloth
description: >-
  Install, operate, and troubleshoot Unsloth Core, Studio, and Desktop for local
  inference and model training. Use for Unsloth environment setup, LoRA/QLoRA
  supervised fine-tuning, coding specialization, verifier audits, chat templates,
  GRPO and preference training, vision
  and audio workflows, decision models, local coding agents and tools, dynamic
  quantization, checkpoint recovery, multi-GPU training, and model export
  to GGUF or serving engines. Do not use for framework-neutral ML strategy or
  operating a standalone inference server unrelated to Unsloth.
license: MIT
metadata:
  research-date: "2026-10-13"
  source: "https://github.com/unslothai/unsloth"
---

# Unsloth

Turn an Unsloth request into a reproducible installation, bounded experiment, or
verified model artifact. Unsloth provides an optimized Python training stack
(Core), a browser interface (Studio), and a native application (Desktop).
Capabilities differ by product, backend, model, and release. Read the relevant
official page before selecting a new hardware or model path; never promote a
vendor speed or minimum-memory claim into a promise about the user's workload.

## When not to use

- For deciding whether ML, retrieval, or fine-tuning is appropriate, use
  `ml-engineering`; return here for Unsloth execution.
- For operating exported models in a standalone engine, use `llama-cpp` or
  `vllm`. This skill owns the export and parity checks at that boundary.
- For container platform design use `platform-engineering`; for Docker Compose
  mechanics use `docker-compose`. Do not turn this skill into a platform manual.

For direct weight inspection or targeted tensor editing, route to
[ml-engineering](../ml-engineering/SKILL.md). Weight-space programming research
does not establish an Unsloth editing recipe. Reuse reload/export checks only
after verifying edited-checkpoint compatibility; repeat task and regression
evaluation in the target runtime.

## Start here

1. Identify the requested surface: Core Python/notebook, Studio web UI, or
   Desktop. Determine inference, SFT, preference optimization, online RL, or
   decision-model training, media generation, coding-agent/tool use, or
   another model-specific task. Default to Core for reproducible coded
   training, and Desktop/Studio when a GUI is requested.
2. Discover OS, Python, accelerator/backend, free VRAM/RAM/disk, installed
   versions, model ID and revision, input format, target context, and output
   destination. Use existing task context; ask only for unresolved choices that
   affect feasibility. Run the read-only helper before prescribing packages.
3. Establish a measurable baseline, held-out dataset, budget, and stop condition
   before training. Capture these in [the run record](templates/run-record.md).
4. This skill can install software, download weights, consume GPU resources,
   write checkpoints, expose services, and publish models. Before first mutation:

   > Confirm the target, scope, and rollback path before acting. Read-only discovery may proceed without confirmation.

   Existing explicit authorization can establish these facts; do not ask again
   when the session already supplies them. Keep a previous environment/artifact
   available; use a new run directory. Publishing and opening remote access need
   their own authorized destination/scope. Deletion needs an explicit directive.

## Load only the relevant guide

| Situation | Read |
|---|---|
| Explain Unsloth, select a surface, assess fit | [Capabilities and decisions](references/capabilities.md) |
| Install, upgrade, select hardware/backend, use containers | [Installation](references/installation.md) |
| Run the observed RTX 5070 Ti text-SFT smoke recipe | [Validated executable SFT](references/validated-sft.md) |
| Prepare data, run text SFT, choose LoRA settings | [Data and supervised training](references/sft.md) |
| Prepare coding datasets, label audits, SFT and real-task acceptance | [Coding specialization](references/coding-specialization.md) |
| Local GRPO/RLVR, verifier challenges, rollout budgets and failure analysis | [Local RLVR](references/local-rlvr.md) |
| Specialization research, contradictions and evidence boundaries | [Specialization evidence](references/specialization-evidence.md) |
| GRPO, DPO, vision/audio, continued pretraining, multi-GPU | [Advanced training](references/advanced-training.md) |
| Train/serve choice, yes/no or score decision models | [Decision models](references/decision-models.md) |
| Connect coding agents, execute/search with tools, MCP, Data Recipes | [Agents and tools](references/agents-and-tools.md) |
| Generate/edit images, video or audio in Desktop/Studio | [Media workflows](references/media-workflows.md) |
| Choose UD GGUF or NVFP4; measure low-bit tradeoffs | [Quantization selection](references/quantization-selection.md) |
| Save/resume, export, run inference, use Studio API | [Artifacts and serving](references/artifacts-serving.md) |
| Import errors, OOM, zero loss, bad exports, hangs | [Troubleshooting](references/troubleshooting.md) |
| Check currency, resolve conflicting docs, find a model notebook | [Source ledger](references/sources.md) |

## Bounded workflow

1. **Prove the environment.** Inventory first, then select the official backend
   recipe. Use an isolated environment. Restart notebook kernels after package
   changes. Import Unsloth before Transformers/PEFT/TRL in training code. Check
   the accelerator in the same Python process/environment that will train.
2. **Prove the data.** Audit structure and exact duplicates with the helper;
   separately check source/group leakage, permission, quality, and tokenizer
   lengths. Render real examples using the selected tokenizer's chat template.
   Inspect a collated batch, including decoded non-ignored labels. A syntactically
   valid conversation is not proof of correct loss masking.
3. **Prove a small run.** Start with a supported model-specific notebook/script,
   pin its revision and dependencies, and adapt one dimension at a time. Execute
   a short run with finite loss and a saved/reloaded artifact before committing
   the full budget. Record peak memory and tokens/sec after warmup.
4. **Train with checkpoints.** Track training and validation signals separately.
   End at the budget, nonfinite loss, repeated infrastructure failure, or the
   agreed regression threshold. Do not tune on the final test set.
5. **Compare behavior.** Run the base model and candidate on identical held-out
   prompts with equivalent decoding, task scoring, and critical failure checks.
   Training loss alone does not demonstrate improvement. Keep negative results.
6. **Verify delivery.** Save tokenizer/processor and adapter or merged weights;
   test reload in a fresh process. Compare target-runtime behavior after export.
   Report exact artifacts, versions, checks actually run, missing evidence, and
   how to resume or roll back.

## Validated GPU workflow

For an executable text-SFT baseline, read [the observed recipe](references/validated-sft.md).
It pins the public Qwen3-0.6B revision and resolved dependencies and uses
`scripts/sft_smoke.py`, `scripts/sft_audit.py`, `scripts/verify_export.py`,
and `scripts/gpu_completion.cpp` with `assets/smoke-config.json`,
`assets/train.jsonl`, `assets/heldout.jsonl`, and
`assets/requirements-gpuslut01.lock`. The scripts implement target-retention and
actual collated-label audits, fixed-prompt base/adapter scoring, full checkpoints,
fresh-process reload, stateful resume, merge, and GPU F16 GGUF parity. Read the
recipe before execution; its package installation and GPU work mutate only the
authorized isolated directory. No automatic CPU fallback, upload or service start.

This observed path is BF16 LoRA on one RTX 5070 Ti. Other installation/backend,
QLoRA, UI, advanced-training and quantized-export guidance remains unverified by
this run. Output-quality eval manifests are review assets, not executed semantic
passes. Do not generalize the toy formatting-task score to real workloads.

## Researched capabilities beyond text SFT

The decision, agent/tool, media and low-bit guides above are grounded in dated
official docs, a pinned upstream implementation and notebook, and explicit
contradictions. Their runtime stages are not validated by our text-SFT run. Use
[the capability record](templates/feature-validation.md) for a new operation.
Decision outputs require head/calibration preservation and probability checks;
local inference does not establish offline search, tool confinement or GPU-only
placement. Verify default CPU fallback and process lifetime in the installed build.

## Real-task specialization

Before training, route model choice to `ml-engineering`: classification may need
a simpler classifier or decision head rather than generative fine-tuning.
For coding, use the coding/RLVR guides above,
[the specialization plan](templates/specialization-plan.md) and
[the reward contract](templates/reward-contract.md). Split repositories/source
families before deriving examples; audit actual target retention and independently
executed task outcomes. Do not generalize the observed formatting smoke to code
quality or use the single-turn trainer as a multi-turn tool trainer unchanged.

The new offline helper audits provenance/splits and verifier receipts only.
[sample receipts](templates/verifier-receipts.json) are synthetic contract examples,
not execution evidence. Route annotation/provenance to `training-data-annotation`,
agent task evaluation to `agent-evals-and-observability`, isolation design to
`secure-software-engineering`, container mechanics to `docker-compose`, and
serving to `llama-cpp`/`vllm`. No new GPU training/RL path is validated here.

## Local helpers

Run these commands from this skill's root with Python 3.10+. They require no
Unsloth installation, GPU, network, or credentials and do not modify inputs.

```bash
python3 scripts/unsloth_preflight.py doctor --json
python3 scripts/unsloth_preflight.py dataset train.jsonl --eval-file valid.jsonl --json
python3 scripts/decision_audit.py assets/decision-train.jsonl \
  --calibration-file assets/decision-calibration.jsonl --test-file assets/decision-test.jsonl --json
python3 scripts/specialization_audit.py data --train train.jsonl \
  --development development.jsonl --test test.jsonl
python3 scripts/specialization_audit.py rewards templates/verifier-receipts.json
python3 -m unittest discover -s scripts -p 'test_*.py'
```

`doctor` inventories installed package metadata and available executables; it
does **not** certify compatibility or execute package imports. Dataset auditing
supports only text SFT JSONL (`text` or `messages`, one consistent format per
file pair). It rejects unsupported multimodal/tool/preference shapes explicitly.
It checks exact content duplicates and cross-split overlap, ignores row metadata
when comparing content, and emits counts/line numbers without training text.
Exit 0 means the selected checks completed without blocking findings, 1 means
findings or incomplete scanning, 2 means invalid CLI arguments. No tokenization,
semantic deduplication, quality assessment, or GPU execution is implied.

`decision_audit.py` independently checks three hard-label decision splits for
question/gold validity, content duplicates and state/group leakage. It supports
string states and object-valued hard-label rows only; soft targets and JSON-string
columns require upstream/tokenizer auditing. It prints counts/codes/line numbers
without state text, and stops on scan limits. Exit 0/1/2 has the same audit/CLI
meaning. It does not certify calibration, token retention or model compatibility.

## Non-obvious failure boundaries

- The driver's advertised CUDA capability, Torch's compiled runtime, and an
  installed CUDA toolkit are different facts. Do not select a wheel by copying
  the `nvidia-smi` version string blindly.
- QLoRA trains adapters on a quantized base; it does not make all training state
  four-bit. GGUF inference quantization is a separate artifact/workflow.
- Never use a Llama response delimiter for another model without inspecting
  rendered tokens. Zero supervised tokens can masquerade as a fast, low-loss run.
- A LoRA export is not a standalone model or a full optimizer checkpoint.
- Multiple GPUs do not automatically pool memory under DDP; model replication
  and sharding solve different problems.
- A working NVIDIA Core recipe is not a Mac/AMD/Intel recipe. Current Mac UI/MLX
  support does not prove the same Core CUDA script runs on Apple Silicon.
- Documentation and installed TRL can differ on `processing_class`/`tokenizer`
  and `max_length`/`max_seq_length`; inspect the installed signature and matched
  notebook instead of combining snippets from different versions.

## Completion and escalation

For research: deliver sourced decisions and explicit unknowns. For installation:
prove the requested surface starts and the selected backend runs a tiny operation.
For training: deliver the run record, held-out comparison, reloadable artifact,
and recovery instructions. For export: additionally prove the intended runtime
loads it and passes the agreed parity checks. If hardware or access is absent,
deliver the prepared commands and mark execution unverified.

After three diagnostic passes without new evidence, stop and provide the minimal
reproducer, version inventory, observed failing layer, attempted hypotheses,
and the specific missing prerequisite. Do not loop through global reinstalls.
