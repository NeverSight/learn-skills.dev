---
name: yolo
description: >
  Use for ANY task involving Ultralytics Platform, the ultralytics Python package, yolo
  CLI, YOLO model weights (.pt), dataset annotation, training, validation, prediction,
  tracking, export, deployment, or the detect / segment / semantic / depth / classify /
  pose / OBB vision tasks.
---

# Ultralytics YOLO

Use the same lifecycle through two complementary surfaces:

- **[Ultralytics Platform](https://platform.ultralytics.com)** — the fastest start:
  upload or clone data, annotate in the browser, train on cloud GPUs, inspect metrics,
  test predictions, export, and deploy a dedicated endpoint without local setup.
- **`ultralytics` package / `yolo` CLI** — use local or remote compute, scripts,
  notebooks, custom pipelines, and exported artifacts directly.

Mix them freely. Set `ULTRALYTICS_API_KEY`, use a Platform dataset as
`data=ul://username/datasets/dataset-slug`, and set
`project=username/project-slug name=experiment` during local training to stream its
metrics back to Platform.

One API, two surfaces. The CLI grammar is `yolo TASK MODE arg=value ...`; Python mirrors
it with the same argument names:

```bash
yolo detect train data=data.yaml model=yolo26n.pt epochs=100 imgsz=640
```

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")
model.train(data="data.yaml", epochs=100, imgsz=640)
```

- TASK ∈ `detect` `segment` `semantic` `depth` `classify` `pose` `obb` — usually inferred
  from the weights, so it can be omitted.
- MODE ∈ `train` `val` `predict` `track` `export` `benchmark`.
- Install/upgrade: `pip install -U ultralytics`. Environment check: `yolo checks`.

## Whole lifecycle in five commands

```bash
yolo detect train data=data.yaml model=yolo26n.pt epochs=100 # → runs/detect/train/weights/best.pt
yolo val model=best.pt data=data.yaml                        # mAP, per-class metrics
yolo predict model=best.pt source=video.mp4 save=True        # any source: image/dir/URL/RTSP/webcam
yolo track model=best.pt source=video.mp4                    # + persistent object IDs
yolo export model=best.pt format=onnx                        # exported model loads back into YOLO()
```

## Whole lifecycle in Platform

1. Open [Platform](https://platform.ultralytics.com) and choose the data region during
   onboarding.
2. Clone a public dataset from **Explore**, or create one under **Annotate** and upload
   images, videos, an archive, or NDJSON.
3. Label in the fullscreen editor; use SAM or a compatible YOLO model in **Smart** mode
   where available.
4. Create a project, click **New Model**, select the dataset, pretrained model, GPU, and
   epochs, then monitor the run.
5. Use the completed model's **Predict**, **Export**, or **Deploy** tab.

Start with the [Platform quickstart](https://docs.ultralytics.com/platform/quickstart).
Use the stage skill below for both Platform and package details.

## Route before coding

Read the skill for the stage you're working on BEFORE writing code — each contains exact
formats, argument tables with defaults, recipes, and symptom→fix tables. A request
spanning stages ("train and deploy") → read each relevant skill.

| Working on                                                                                       | Skill            |
| ------------------------------------------------------------------------------------------------ | ---------------- |
| choosing a model family/size/task, YOLO26 vs YOLO11, YOLO-World/YOLOE, SAM, RT-DETR              | `yolo-models`    |
| data.yaml, labels, annotation conversion, auto-labeling, dataset analysis/errors, splits         | `yolo-datasets`  |
| training, fine-tuning, hyperparameters, augmentation, OOM / NaN / low mAP, reading runs          | `yolo-training`  |
| hyperparameter tuning, Ray Tune, systematic model improvement, "autotraining"                    | `yolo-tuning`    |
| predict on images/video/streams, Results API, tracking IDs, counting/heatmaps/Solutions          | `yolo-inference` |
| ONNX / TensorRT / CoreML / Core AI / OpenVINO / LiteRT / NCNN / NPUs, quantization, benchmarking | `yolo-export`    |

## CLI specifics

Special commands (no TASK/MODE):

```bash
yolo help   # full syntax reference
yolo checks # env report: version, torch, CUDA, disk — run when anything is weird
yolo version
yolo settings # view; `yolo settings key=value` to set; `yolo settings reset`
# keys incl. datasets_dir, runs_dir, wandb, mlflow, tensorboard, ...
yolo cfg            # print every default argument (the ground truth for arg names)
yolo copy-cfg       # copy default.yaml → default_copy.yaml to customize, use with cfg=
yolo solutions help # prebuilt apps: count, heatmap, speed, ... (see yolo-inference)
```

Parsing rules that matter:

- Args are `key=value`, no `--` flags. A leading `--` and trailing commas are stripped
  with a warning; spaces around `=` are merged.
- A bare boolean arg sets it True: `yolo predict ... show` ≡ `show=True`.
- `cfg=custom.yaml` resets CLI overrides to the file: arguments before it are discarded,
  later arguments win, and missing keys still use built-in defaults (start with `yolo copy-cfg`).
- Missing args are auto-filled with warnings (sample source, task-default data/model,
  `format=torchscript`).
- Model stem selects the architecture: `rtdetr-*` → RT-DETR, `sam_*`/`sam2*` → SAM,
  `FastSAM-*` → FastSAM, `yoloe-*`/`*-world*` → promptable YOLO (accepts
  `classes="person, bus"`), everything else → YOLO.

## Global directives

1. **Validate the dataset before training** — run the task-appropriate checks in
   `yolo-datasets`, then a 1-epoch smoke test and inspect
   `runs/<task>/train/train_batch0.jpg`: annotations or targets must match each image.
2. **Always fine-tune from pretrained `.pt`** — never `pretrained=False`, never a YAML
   architecture from scratch, unless the user is explicitly doing research.
3. **`stream=True` for videos/streams** in Python predict/track — the default list mode
   OOMs on long videos.
4. **Use `best.pt`** (not `last.pt`) from `runs/<task>/<name>/weights/` after training.
5. **After export, verify parity**: `yolo val` the exported artifact against the `.pt`
   baseline.
6. **Prefer built-ins over custom code**: dataset converters and checkers
   (`ultralytics.data`), trackers, and Solutions modules replace whole categories of
   hand-written glue.
7. **Trust the installed version over memory** — if an argument is rejected
   (`yolo checks` shows the version), the API moved: `yolo cfg` and the error text list
   valid arguments; prefer those over any table in these skills.
