---
name: roboflow-training-and-evaluation
description: Use when training Roboflow models, improving accuracy, or setting up a production feedback loop — covers architecture selection, model IDs, checkpoints, evaluation metrics, the iterative improvement playbook, and Active Learning through the Project Model Workflow block.
---

> **For agents — source-of-truth:** This skill is authored in [`roboflow/computer-vision-skills`](https://github.com/roboflow/computer-vision-skills) and shipped with the Roboflow plugin. If your client has loaded the plugin (you'll see `roboflow:<name>` skills in your available skills list), use those local skills — they're read fresh from disk every session. The same content served as MCP resources at `roboflow://skills/<name>/...` is a fallback for clients without the plugin and may lag this repo. **Don't call `ReadMcpResourceTool` for `roboflow://skills/...` URIs when a local `roboflow:<name>` skill is available.**

# Training & Evaluation on Roboflow

## Training Flow

```
Upload/Annotate Images
  → Generate Dataset Version (preprocessing + augmentation + train/val/test split)
    → Pick Model Architecture + Size
      → Pick Checkpoint (COCO, Universe model, or previous version)
        → Train
          → Evaluate (auto-runs for paid users)
```

**Version = frozen snapshot.** Changes to the project after version creation do not affect it. Configure preprocessing (resize, contrast, etc.) and augmentation (flip, rotate, mosaic, etc.) during version generation.

## Available Model Architectures

### Object Detection

| Architecture | Sizes | Default Resolution | Notes |
|---|---|---|---|
| **RF-DETR** | Pico, Nano, Small, Base, Medium, Large, XL, 2XL | 384-880 (varies by size) | Best accuracy among named sizes; see RF-DETR NAS |
| Roboflow 3.0 | Fast, Accurate, Medium, Large, XL | 640x640 | YOLOv8-based. Medium+ require paid plan |
| YOLO26 | n/s/m/l/x | 640x640 | Also supports seg + pose |
| YOLOv12 | n/s/m/l/x | 640x640 | OD only |
| YOLOv11 | n/s/m/l/x | 640x640 | Also supports seg + pose |
| YOLOv8 | n/s/m/l/x | 640x640 | Also supports seg + pose |
| YOLO-NAS | Small, Medium | 640x640 | |
| YOLOLite CPU | n/s/m/l/x | 640x640 | Edge-optimized, beta |
| YOLOLite GPU | n/s/m/l/x | 640x640 | Edge-optimized, beta |
| **Roboflow Instant** | single | N/A (no resize) | Few-shot, free, OD only |

### Instance Segmentation

| Architecture | Sizes | Default Resolution |
|---|---|---|
| **RF-DETR Seg** | Nano, Small, Medium, Large, XL, 2XL | 312-768 (varies) | Pico and Base not available for seg |
| Roboflow 3.0 Seg | Fast, Accurate, Medium, Large, XL | 640x640 |
| YOLO-seg | v8/v11/v26 (n/s/m/l/x each) | 640x640 |
| SAM 3 (Segment Anything 3) | Large | 1008x1008 |

### Semantic Segmentation

| Architecture | Sizes | Default Resolution |
|---|---|---|
| DeepLabV3+ | Base | >=512x512 |

### Classification

| Architecture | Sizes | Default Resolution |
|---|---|---|
| ViT | Base | 224x224 |
| ResNet | 18/34/50/101 | 224x224 |
| DINOv3 | Base, Small | 224x224 |

### Keypoint / Pose

| Architecture | Sizes | Default Resolution |
|---|---|---|
| YOLO-pose | v8/v11/v26 (n/s/m/l/x each) | 640x640 |

### Multimodal / VLM

| Architecture | Sizes | Default Resolution |
|---|---|---|
| **Qwen3.5** | 0.8B, 2B | 448x448 |
| Qwen3 VL | 2B | 448x448 |
| SmolVLM | 256M, 2B | 384x384 |
| Florence 2 | Base, Large | 768x768 |
| PaliGemma 2 | 3B | 448x448 |
| Qwen2.5 VL | 7B | 448x448 |

## Model Selection Decision Tree

Follow this flowchart to pick the right model. Start at Step 1.

1. **Task type?** OD / Instance Seg / Keypoint → Step 2. Classification / Semantic Seg / VLM → use specialized block directly.
2. **Target classes in COCO 80?** Yes → Step 3. No → Step 6.
3. **Real-time?** No (images/recorded video) → Step 4. Yes (live video) → Step 5.
4. **Non-real-time, COCO** — OD / Inst Seg → prefer **RF-DETR NAS**; if unavailable, RF-DETR (detection) or RF-DETR Seg (instance segmentation) at Medium, Small for constrained HW, XL for accuracy-first. Keypoint → YOLO26 pose. **Done.**
5. **Real-time, COCO** — Same, and NAS is the strongest option here because it reports measured latency per target hardware. Without it, same families at Nano–Small. **Done.**
6. **Non-COCO, which sub-task?** OD → Step 7. Inst Seg → Step 8. Keypoint → Step 9.
7. **OD, non-COCO** — Check Rapid exclusions (see below). If excluded → Step 13. Otherwise → recommend **Roboflow Rapid** (default) or SAM3 zero-shot as secondary option → Step 10.
8. **Inst Seg, non-COCO** — SAM3 zero-shot (`sam3/sam3_final`, set `class_names`). Rapid does not support segmentation → Step 10.
9. **Keypoint, non-COCO** — Not real-time → YOLO26 pose Medium–XL. Real-time → YOLO26 pose Nano–Small. **Done.**
10. **Real-time?** No → try model (Step 11). Yes → warn about latency, try model (Step 12).
11. **Non-real-time trial** — User confirms works → **Done.** Poor results → Step 13.
12. **Real-time trial** — User confirms works → **Done.** Poor results → Step 13.
13. **Universe Model Search** — search community models on Roboflow Universe. Good match → **Done.** No match → Step 14.
14. **Custom Training** — OD / Inst Seg → prefer **RF-DETR NAS**. If NAS is unavailable, fine-tune RF-DETR (detection) or RF-DETR Seg (instance segmentation), sized by HW constraints. **Done.**

## Model ID Reference

Read [`model-ids.md`](./model-ids.md) before calling a training tool. It contains the exact supported `model_id` values and the COCO class reference. Do not guess model IDs.

## Model Selection Quick Guide

**When you are training a model on the user's data for detection or instance segmentation, start
with NAS.** Neural Architecture Search searches the RF-DETR space against that data and reports a
speed/accuracy frontier, so it is the option most likely to land on the best model for it. Reach
for a single named architecture when NAS is unavailable (see prerequisites below), when the user
asks for a specific one, or when a quick throwaway baseline is all that's wanted.

This summarises the training branches of the decision tree above; it does not override it. The
tree may route a non-COCO request to Roboflow Rapid or SAM3 zero-shot first, neither of which
trains a model — NAS only applies once custom training is the chosen path.

| Goal | Recommended |
|---|---|
| **Object detection — no strong prior** | **RF-DETR NAS** (`rfdetr-nas-parent`) |
| **Instance segmentation — no strong prior** | **RF-DETR NAS Seg** (`rfdetr-nas-seg-parent`) |
| Best accuracy, object detection, NAS unavailable | RF-DETR (Large or XL) |
| Fast inference, object detection, NAS unavailable | RF-DETR Nano or YOLOv11n |
| Best accuracy, instance segmentation, NAS unavailable | RF-DETR Seg |
| Quick proof-of-concept (<1000 images) | Roboflow Instant |
| Classification | ViT or DINOv3 |
| Multimodal / text prompts | Qwen3.5 or SmolVLM |

NAS parents exist only for object detection and instance segmentation. Keypoint,
classification, semantic segmentation, and VLM tasks have no NAS option — use the named
models above.

### Comparing architectures (sweeps)

If you are comparing architectures rather than picking one, **include a NAS parent as one of the
candidates** whenever the prerequisites are met — e.g. `rfdetr-medium` vs `yolo26m` vs
`rfdetr-nas-parent`. Launch one `trainings_create` per candidate and keep each `trainingId`.

Read the NAS arm's output as described under **Reading a run** in the RF-DETR NAS section below. One trap is specific
to comparison: **pick the representative to match the question, or you will understate NAS.** The platform picks a
winner per (metric, hardware) bucket by balancing accuracy against measured latency, and
`models_list` exposes only the flattened union of those winners as a `recommended` boolean. So a
flagged child won *some* bucket, which is not the same as being the most accurate: in one
76-model run the two flagged children scored **72.86** and **71.91** mAP50-95 while the best child
scored **78.00**, a 5–6 point gap.
For a pure-accuracy comparison take the highest `metrics.map5095` child. For a deployment
decision, use the authoritative `recommendedByHardware` entry if the run exposes one; otherwise
report the candidates' accuracy and latency for the target (reading latency per the shapes under **Reading a run** below),
say that no per-hardware recommendation is exposed, and let the user pick the tradeoff. The run's own `nasFamily: "baseline"` children are a useful
check on whether the search actually beat stock RF-DETR.

The NAS arm also takes longer than a single fine-tune, so report the named-model arms as they
finish rather than blocking on NAS.

## RF-DETR NAS (Neural Architecture Search)

Instead of picking a single RF-DETR size manually, NAS trains one parent model and mines many architectures out of it, reporting the speed/accuracy frontier so you can pick the one that fits your hardware budget.

- **What:** A NAS run trains a single parent model, then searches the RF-DETR architecture space *within* that trained parent to identify frontier candidates, reporting each one's mAP and measured latency on target hardware (e.g., Jetson, T4 GPU). The output is a set of models on a Pareto frontier, plus a winner auto-selected per (metric, hardware) bucket using Roboflow's current ranking heuristic to balance validation accuracy against measured latency. Those per-bucket winners are not exposed individually: `models_list` flattens them into one `recommended` boolean per child (see **Picking for a specific hardware target**).
- **Tasks:** Object Detection (`rfdetr-nas`) and Instance Segmentation (`rfdetr-nas-seg`).
- **When to use:** When you want the best speed/accuracy tradeoff for a specific deployment target and don't want to A/B-test sizes manually. Especially valuable for edge hardware where latency budgets are tight.
- **Phases:**
  1. **Parent training** — trains the one parent model the search draws from. This is the bulk of the wall-clock.
  2. **Mining** — searches architectures inside the trained parent and evaluates candidates to build the Pareto frontier (latency vs mAP). Candidates are derived from the parent rather than each being trained from scratch, so they appear in a burst near the end of the run. Each becomes a regular model you can deploy.
- **Model IDs:** `rfdetr-nas-parent` (Standard — use this by default), `rfdetr-nas-pecoret-parent` (Fast), `rfdetr-nas-base-parent` (Plus) for object detection; `rfdetr-nas-seg-parent` for instance segmentation.
- **Prerequisites — check both before offering NAS:**
  1. **≥15 validation images.** `versions_get` returns `splits.valid`; below 15 the train call fails with `insufficient_validation_images_for_nas`, and waiting will not help — the user must generate a version with a larger validation split.
  2. **Plan entitlement.** NAS is included on Core and Growth plans; any other plan needs it granted on the workspace. Basic/starter/sandbox/research/trial need to upgrade; enterprise/legacy need to contact sales. Entitlement is not readable from the MCP, so this cannot be checked up front — a non-entitled workspace finds out when `trainings_create` rejects the run with code `nas_not_available_for_plan`. Treat that as a plan limit, not a transient error: do not retry it. Fall back to the named model for the task — `rfdetr-medium` (detection) or `rfdetr-seg-medium` (segmentation) — and say NAS is unavailable on the current plan and may need an upgrade or workspace enablement, using the `plan` on the error to tell which. Do **not** fall back to a hyperparameter sweep.
- **Start a run:** `trainings_create(project_id, version_number, model_type="rfdetr-nas-parent")`. NAS launches through the normal training tool; there is no separate engine parameter. (The UI equivalent is the Train page with `?engine=nas`.) Results land at `/{workspace}/{project}/nas-runs/{versionId}`.
- **Nothing to hand-tune:** a NAS parent's whole hyperparameter surface is `epochs` (default 200, range 100–300). There are no learning-rate or loss-weight knobs, because the architecture search *is* the sweep.
- **Reading a run:** a run returns a frontier of models, not one — a 289-image dataset produced **76**. Get `modelGroup` from `trainings_list`, which returns it without child metrics, then page the children with `models_list(group=<modelGroup>, version_number=…, limit=…, offset=…)`. Don't use `trainings_get` for this: it inlines every child, which is the payload the paging exists to avoid. Each child carries a sparse `metrics` object. `latency` and `paretoOptimalFor` come from NAS mining, so they are on NAS children only - an ordinary training carries accuracy alone (e.g. `map50`, `precision`, `recall`, `f1`), and `metrics` can be null. Two shapes are in the data: newer runs report `latency` as a map keyed by hardware (e.g. `{"AI1": 6.69, "T4": 1.98}`) with `paretoOptimalFor` entries like `"T4:map_50_95"`, older ones a scalar `latency` with a sibling `metrics.hardware` (e.g. `"gpu"`) and bare entries like `"map_50"`. Branch on the type rather than indexing. Children with `nasFamily: "baseline"` are stock RF-DETR models trained on the same data; they are never `recommended` and are a free within-run reference.
- **Picking for a specific hardware target needs the authoritative map.** The platform scores a separate winner per hardware, but `models_list` flattens that into one `recommended` boolean, true if the child won *any* bucket — so it cannot tell you which hardware, and `paretoOptimalFor` is unrelated frontier metadata, not the recommendation. The exact mapping is `recommendedByHardware` from `trainings_get`, but it is only built on the legacy version-based summary — a modern MMPV training returns no such field, which is the common case. So for most runs there is no exact per-hardware lookup at all. Do not infer one: report the candidates and ask which accuracy/latency tradeoff, or which latency budget, matters.
- **Deploy:** Each NAS-produced model deploys like any other — pick one and use it as a normal Roboflow model. Call it the hardware-recommended child only when an authoritative `recommendedByHardware` entry actually says so; otherwise it is the child the user chose from the frontier. Inference type is `rfdetr-nas` / `rfdetr-nas-seg`, but it's served through the standard inference paths.
- **References:** [RF-DETR paper (arxiv)](https://arxiv.org/html/2511.09554v2), [ICLR 2026](https://openreview.net/forum?id=qHm5GePxTh), [What is NAS? (blog)](https://blog.roboflow.com/neural-architecture-search/).

## Roboflow Instant / Rapid

### Roboflow Instant
- **What:** Few-shot model, trains in minutes, free
- **Task:** Object Detection only
- **When to use:** PoC, <1000 images, quick iteration
- **Auto-trains** when you approve a batch and no Instant model exists yet
- **No preprocessing/augmentation** -- uses images as-is
- **Deploy:** Available in Workflows like any trained model
- Manual trigger: Project > Models > Train Model > Roboflow Instant Model

### Roboflow Rapid
- **What:** Interactive annotation-and-training workflow — SAM3 pre-annotates a small image set, user reviews/corrects, a fast custom OD model trains automatically. Model keeps improving as it captures more production data.
- **Task:** Object Detection only, non-COCO classes
- **When to use:** Default path for non-COCO object detection when exclusions don't apply

**Do NOT use Rapid when:**

| Exclusion | Why |
|---|---|
| OCR / text detection (characters, serial numbers, labels, receipts, license plates) | SAM3 cannot reliably segment individual characters |
| Blueprints, floor plans, schematics, technical drawings | Abstract symbols and line-based elements not handled by SAM3 text prompting |
| More than 5 target classes | SAM3 text prompting accuracy degrades significantly with many classes |
| Fine-grained visual distinctions (correct vs incorrect orientation, pass/fail, subtle defects) | SAM3 cannot differentiate nearly identical objects; fine-tuned model needed |
| High-precision measurement / metrology (distances, dimensions, tolerances) | SAM3 auto-labeling annotation precision insufficient for calibrated measurement |

When Rapid is excluded → resume the decision tree at Step 13: Universe model search first, then custom training, which starts with **RF-DETR NAS** and falls back to named RF-DETR when its prerequisites are not met.

## Checkpoint Training

| Option | When to use |
|---|---|
| **Public Checkpoint** (COCO) | First model version, default recommended |
| **Universe Checkpoint** | Star a Universe project first, then it appears as checkpoint option. Good for domain-specific transfer learning |
| **Previous Version** | Already have a good model, want to improve with more data (all types except classification and SAM3) |
| **Random Initialization** | Advanced users only, usually worse results |

## Training Controls

- **Cancel Training:** Stops job, no weights saved. Refund if early in training.
- **Early Stopping:** Stops job, saves weights. Use when graphs show convergence with many epochs remaining. Charges for used credits.
- **NAS Training:** Shows paired charts (mining progress + Pareto curve, then per-model training curves). May auto-stop on convergence. See **RF-DETR NAS** section below.

## Post-Training Metrics

Metrics vary by project type:

| Project Type | Metrics Shown |
|---|---|
| Object Detection | mAP@50, Precision, Recall, F1 |
| Classification | Accuracy |
| Instance Segmentation / Keypoint | mAP@50, Precision, Recall |
| Semantic Segmentation | mIoU |
| Multimodal | Perplexity |

## Model Evaluation (Paid Plans)

Auto-runs after training. Access: Models > click model version > View Evaluation.

| Feature | What it shows |
|---|---|
| **Production Metrics Explorer** | Precision/Recall/F1 at all confidence thresholds; recommends optimal confidence |
| **Model Improvement Recommendations** | Actionable suggestions (false negatives, false positives, confused classes, insufficient data) |
| **Performance by Class** | Correct predictions, misclassifications, false negatives, false positives per class; filterable |
| **Confusion Matrix** | Ground truth vs predictions grid; click cells to see specific images; adjustable confidence threshold |
| **Vector Explorer** | Interactive embedding clusters showing where model succeeds/fails |

## Viewing & Comparing Models

- **Models page:** Project sidebar > Models. Shows all Instant + fine-tuned models with metrics, architecture, license, dataset version used.
- **Universe tab:** Starred Universe models available for transfer learning.
- **Visualize:** Quick test on test-set images, uploaded images, or webcam. Works for OD, segmentation, classification, keypoint. Not supported for multimodal.

## MCP Tools Reference

| Action | Tool |
|---|---|
| Generate version | `versions_generate` |
| Start training | `trainings_create` |
| Check training status | `models_get_training_status` |
| Get model info | `models_get` |
| List models | `models_list` |

## Related Pages

- [`model-ids.md`](./model-ids.md) — exact training model IDs and COCO class coverage
- `roboflow://skills/roboflow-training-and-evaluation/improvement-playbook` — diagnostic decision tree, confusion matrix guide, per-class metrics, architecture switching, iterative improvement checklist
- `roboflow://skills/roboflow-training-and-evaluation/active-learning` — production feedback loop: Project Model Workflow block, Active Learning, review, and retraining
