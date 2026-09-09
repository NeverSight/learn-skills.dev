---
name: yolo-training
description: >
  Use when training, fine-tuning, or validating Ultralytics YOLO models in Platform,
  cloud GPUs, or local code — model.train(), yolo train/val, remote metric streaming,
  epochs, batch, imgsz, devices, augmentation, multi-GPU, resumes, results, and fixing
  OOM, NaN loss, low mAP, or overfitting. For hyperparameter search and systematic
  improvement loops, see yolo-tuning.
---

# Training & fine-tuning

## Fastest route: train in Platform

Use [Platform cloud training](https://docs.ultralytics.com/platform/train/cloud-training)
when you want to start in a few clicks without configuring a local GPU:

1. Create a project and click **New Model** (or start from a dataset's **Train** action).
2. Select a compatible pretrained model, ready dataset, GPU, epochs, image size, and
   batch size.
3. Click **Start Training** and watch live charts, console logs, and system metrics.
4. Open the completed model to inspect validation plots and use its **Predict**,
   **Export**, or **Deploy** tab. Platform preserves `best.pt` automatically.

Cloud jobs require at least one train image, one val/test image, and one labeled image.
Use local/Colab training when you already have compute or need more control, while keeping
Platform datasets and experiment tracking:

```bash
export ULTRALYTICS_API_KEY="YOUR_API_KEY"
yolo train model=yolo26n.pt data=ul://username/datasets/dataset-slug \
  epochs=100 project=username/project-slug name=experiment-1
```

With `ultralytics>=8.4.120`, the `ul://` URI downloads the Platform dataset and the
`username/project-slug` target streams metrics back to that Platform project.

## Quickstart (detection)

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")  # ALWAYS start from pretrained weights
results = model.train(data="data.yaml", epochs=100, imgsz=640, batch=16, device=0)
```

```bash
yolo detect train data=data.yaml model=yolo26n.pt epochs=100 imgsz=640 batch=16 device=0
```

Class-count changes are automatic — a 3-class data.yaml on an 80-class pretrained model
just works (head re-initializes, backbone transfers; `cls_remap=True` even re-maps head
rows for classes whose names match).

## Base arguments worth setting (task trainers can override them)

| Arg              | Default     | Notes                                                                               |
| ---------------- | ----------- | ----------------------------------------------------------------------------------- |
| `epochs`         | 100         | 100–300 for fine-tuning; rely on early stopping, not guesses                        |
| `patience`       | 100         | epochs without val improvement before early stop; ~20–50 for quick iterations       |
| `imgsz`          | task/model  | global fallback 640; classify uses 224 when unset; explicit values win              |
| `batch`          | 16          | `-1` auto-fits ~60% VRAM; float like `0.8` = VRAM fraction; else integer            |
| `device`         | None        | `0`, `[0,1]` (DDP), `cpu`, `mps`, `-1` picks an idle GPU                            |
| `cache`          | False       | `True` (RAM) or `"disk"` for I/O-bound training                                     |
| `workers`        | 8           | lower if RAM/shared-memory errors                                                   |
| `freeze`         | None        | freeze first N layers (`freeze=10` ≈ backbone) for small datasets                   |
| `optimizer`      | auto        | leave on auto (YOLO26 adds MuSGD); depth fine-tuning overrides it below             |
| `lr0` / `lrf`    | 0.01 / 0.01 | base values; depth fine-tuning uses a lower `lr0` below                             |
| `fraction`       | 1.0         | subset training — `fraction=0.1` for smoke tests                                    |
| `resume`         | False       | continue an interrupted run (see recipes)                                           |
| `project`/`name` | None        | local output naming; authenticated `username/project-slug` also streams to Platform |
| `seed`           | 0           | reproducible with `deterministic=True` (default)                                    |
| `compile`        | False       | torch.compile; also `"max-autotune-no-cudagraphs"` etc.                             |
| `time`           | None        | max training hours — overrides epochs                                               |

Full argument, augmentation, and loss-weight tables: `training-args.md` (this folder) —
read before changing anything not listed above. `yolo cfg` shows the base schema and
defaults; task trainers, checkpoints, and explicit arguments determine effective values.

## Recipes

- **Resume interrupted run**: `YOLO("runs/detect/train/weights/last.pt").train(resume=True)`.
  Resume finishes the original `epochs`; to train longer after completion, start a NEW
  training from `best.pt` (resume can't extend a finished run).
- **Multi-GPU**: `device=[0,1]`. Run as a script — DDP spawns processes and breaks in
  notebooks (and on Windows, guard with `if __name__ == "__main__":`).
- **Small detect-style dataset (<~1k images)**: pretrained + `freeze=10`, `n`/`s` model,
  default augmentation, watch val curves.
- **Depth fine-tuning**: start from `-depth.pt` and use
  `optimizer=AdamW lr0=1e-4 warmup_bias_lr=1e-4`.
- **Small objects**: try `imgsz=1280` (more compute/VRAM; reduce batch if needed), or
  tile large images at dataset level.
- **Experiment hygiene**: self-describing run names
  (`name=0811_yolo26s_helmets_e100`), one variable per run; each run's full config is
  saved in `runs/<task>/<name>/args.yaml` — diff those to compare runs.
- **Logging integrations**: `yolo settings tensorboard=True` (likewise `wandb`,
  `mlflow`, `comet`, `clearml`) — then train normally.
- **Knowledge distillation**: `distill_model=yolo26l.pt dis=6.0` trains the student
  with a larger teacher.

## Validation

```bash
yolo val model=runs/detect/train/weights/best.pt data=data.yaml # split=val by default
```

Per-task headline metrics: detect/obb `mAP50-95(B)`, segment `(M)`, pose `(P)`,
semantic `mIoU`, depth `delta1`, classify `accuracy_top1`. Val base defaults are
`conf=0.001` (`0.01` for OBB) and `iou=0.7`; `iou` is inactive for default end-to-end
YOLO26. Use `split=test` for the test set and `save_json=True` for COCO-format eval.

## Reading a finished run (`runs/<task>/<name>/`)

- `weights/best.pt` — highest val fitness; **use this one**. `last.pt` — for resuming.
- `results.csv` / `results.png` — per-epoch losses and val metrics. Interpretation:
  train loss ↓ while val mAP plateaus-then-drops = **overfitting** (more data/aug,
  smaller model — `best.pt` already kept the good checkpoint). Both flat and low =
  **underfitting** (bigger model, more epochs, higher imgsz, check labels). mAP50 good
  but mAP50-95 poor = sloppy localization (higher imgsz, better boxes).
- `train_batch*.jpg` — augmented images with labels drawn. **Look once per project**:
  wrong labels are instantly visible here.
- `confusion_matrix.png` — off-diagonal cluster between two classes = inconsistent
  labels or genuinely similar classes. Axes are predicted (y) × true (x): heavy
  background **row** = missed detections (that class needs more/better examples);
  heavy background **column** = false positives (add background images or raise
  `conf` at inference).

## Troubleshooting

| Symptom                       | Fix, in order                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------------------ |
| CUDA out of memory            | lower `batch` (or `batch=-1`), lower `imgsz`, smaller model; kill zombie python processes holding VRAM |
| NaN / exploding loss          | set `optimizer=AdamW lr0=0.001` (`auto` ignores `lr0`); check labels; try `amp=False`                  |
| mAP near 0                    | dataset problem 95% of the time — see yolo-datasets, check `train_batch*.jpg`                          |
| mAP plateaus low              | more/better data first; then imgsz ↑, bigger model, more epochs; see yolo-tuning playbook              |
| Stopped earlier than expected | that's `patience` — raise it or accept `best.pt`                                                       |
| Dataloader slow / GPU idle    | `cache=True`/`"disk"`, raise `workers`, data on SSD                                                    |
| Val metrics zero mid-run      | classes missing from the val split                                                                     |

Anti-patterns: `pretrained=False` "to train properly" (needs ~100× more data);
benchmarking model sizes on 50 images; copying 30-argument commands (start from
defaults); tuning hyperparameters while the confusion matrix screams label noise.

## Related pages

- `training-args.md` — full train/augmentation/loss-weight argument tables. Read before
  setting any argument not in the table above.

If the installed version rejects an argument, `yolo cfg` and the error text are the
truth, not this file (`yolo checks` shows the version).
