---
name: yolo-tuning
description: >
  Use when improving or comparing Ultralytics YOLO models in Platform or code, or running hyperparameter search/autotraining — Platform experiment comparison, the systematic improvement playbook, model.tune() genetic evolution, Ray Tune, search spaces, and deciding whether tuning is worthwhile. For one training run and its arguments, see yolo-training.
---

# Improving models & hyperparameter tuning

## The improvement playbook (follow in order — tuning is the LAST step)

Hyperparameter tuning is expensive and usually not the bottleneck. Escalate in this order, re-validating after each step:

1. **Fix the data** — check `confusion_matrix.png` and `train_batch*.jpg` for label noise; review the top false-negative/false-positive val images; add examples of failing classes and true-background images. Data quality beats every other lever.
2. **Train longer** — if val mAP was still rising at the end: more `epochs`, higher `patience`.
3. **Bigger input** — small objects or mAP<sub>50</sub> ≫ mAP<sub>50-95</sub>: raise `imgsz` (640 → 960/1280).
4. **Bigger model** — underfitting (train and val both mediocre): n → s → m → l.
5. **Domain-matched augmentation** — aerial `degrees=180 flipud=0.5`, crowded scenes `mixup=0.1` (plus `copy_paste=0.3` for segment/OBB), color-critical classes lower `hsv_h` (see yolo-training's `training-args.md`).
6. **Only now: hyperparameter tuning** — worth ~0.5–2 mAP when everything above is exhausted.

Decision signals: overfitting (val drops while train improves) → more data/aug or smaller model, NOT tuning. Underfitting → bigger model/longer, NOT tuning. Label noise in the confusion matrix → nothing else matters until fixed.

## Compare experiments in Platform

Keep candidates in one [Platform project](https://docs.ultralytics.com/platform/train/projects). Train from the **New Model** dialog, ask **Ask AI** to run and compare experiments ([AutoTrain](https://docs.ultralytics.com/platform/train/autotrain)), or stream authenticated local runs by setting `project=username/project-slug` and a unique `name`. Select models together in the project charts, or use **Table > Diff** to compare training arguments and final metrics.

Platform tracks and charts experiments; the built-in genetic tuner and Ray Tune below run only in Python. Use a completed Platform model as the next base checkpoint, or download its `.pt` file, after the comparison identifies a winner.

## Built-in genetic tuner

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")
model.tune(data="data.yaml", epochs=30, iterations=300, plots=False, save=False, val=False)
```

Tuning is Python-only — there is no `yolo tune` CLI mode (MODES are train/val/predict/export/track/benchmark).

- Each iteration = one full (short) training with mutated hyperparameters; fitness is read from the run's val metrics. Iterations set `project` internally, so with an API key available on Python 3.11+ each one uploads to Platform; unset the key to tune locally.
- Default search space: 26 keys — `lr0`, `lrf`, `momentum`, `weight_decay`, `warmup_epochs`, `warmup_momentum`, loss weights (`box`, `cls`, `cls_pw`, `dfl`), augmentation knobs (`hsv_*`, `degrees`, `translate`, `scale`, `shear`, `perspective`, `flipud`, `fliplr`, `bgr`, `mosaic`, `mixup`, `cutmix`, `copy_paste`), `close_mosaic`.
- Custom space (subset + ranges as `(min, max)`):
  ```python
  model.tune(data="data.yaml", epochs=30, iterations=100, space={"lr0": (1e-5, 1e-2), "mosaic": (0.5, 1.0)})
  ```
- Results: `runs/<task>/tune/` — `best_hyperparameters.yaml`, `tune_results.ndjson`, fitness plots. Retrain fully with those values and `optimizer=AdamW` (the tuner's default); `optimizer=auto` would ignore the tuned `lr0` and `momentum`.
- Distributed tuning across machines: pass `mongodb_uri=` (+ optional `mongodb_db=`, `mongodb_collection=`) — workers share one result pool via MongoDB.

## Ray Tune (advanced search algorithms, parallel trials)

```python
model = YOLO("yolo26n.pt")
result_grid = model.tune(use_ray=True, data="data.yaml", iterations=20, epochs=30, gpu_per_trial=1)
```

- Requires `pip install "ray[tune]"`. Default scheduler is ASHA (early-kills bad trials after `grace_period` epochs, default 10).
- `search_alg=` defaults to `"optuna"`; other strings are `"ax"`, `"bayesopt"`, `"bohb"`, `"hebo"`, `"hyperopt"`, `"nevergrad"`, `"zoopt"`, and `"random"`, or pass any Ray Tune searcher object (BOHB swaps ASHA for HyperBandForBOHB).
- W&B logs each trial when `wandb` is installed and enabled (`yolo settings wandb=True`). Use Ray when you have multiple GPUs to parallelize trials or want smarter-than-genetic search; the built-in tuner is simpler and has no extra dependency.

## Evolution best practices ("autotraining" recipe)

- **Search cheap, retrain expensive**: tune with a small model (`n`/`s`), reduced `epochs` (~30), `plots=False save=False val=False`; then retrain the best config at full size/epochs.
- Budget: iterations × epochs × time-per-epoch. 100–300 iterations is a realistic minimum for the genetic tuner to beat defaults.
- Keep `data` fixed during the search — changing data invalidates all prior fitness.
- One fitness target: the tuner maximizes validation `fitness` (box mAP<sub>50-95</sub> for detect; segment and pose combine box and mask/pose mAP<sub>50-95</sub>); confirm that matches what you actually care about before burning GPU days.
- Sanity-check the winner on the val AND test split — tuned configs can overfit the val split when iterations are high.

If the installed version rejects an argument (`yolo checks` shows the version), trust the error text and `yolo cfg` over this file.
