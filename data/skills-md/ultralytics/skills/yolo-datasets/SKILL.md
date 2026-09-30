---
name: yolo-datasets
description: >
  Use when uploading, annotating, building, converting, analyzing, or debugging datasets
  in Ultralytics Platform or local YOLO — Platform dataset management and Smart
  Annotation, data.yaml, YOLO label .txt formats, COCO/DOTA/mask conversion,
  auto-labeling, splits, validation, and errors like "no labels found" or mAP near 0.
  Covers detect, segment, semantic, depth, classify, pose, and OBB data.
---

# Ultralytics YOLO datasets

The #1 cause of silent training failure is a malformed dataset — validate before training.

## Fastest route: prepare data in Platform

1. Open [Platform](https://platform.ultralytics.com), create a dataset under
   **Annotate**, and choose its task.
2. Upload images, videos, ZIP/TAR archives, or NDJSON. Existing YOLO labels and COCO JSON
   can be imported; cloud-storage integrations can keep supported data in place.
3. Open an image in the fullscreen editor. Use manual tools for detect, segment,
   semantic, classify, pose, or OBB. For detect, segment, semantic, and OBB, switch to
   **Smart** mode to label with SAM or predictions from a compatible official/custom YOLO
   model.
4. Review the **Classes**, **Charts**, and **Errors** tabs, fix the split, and create a
   numbered dataset version before important runs.

Platform datasets cover all seven YOLO tasks. Depth targets are imported rather than
drawn in the editor. See
[Platform Data](https://docs.ultralytics.com/platform/data) and the
[Annotation Editor](https://docs.ultralytics.com/platform/data/annotation).

To train on the same dataset from local code, create an API key under **Settings > API
Keys**, set `ULTRALYTICS_API_KEY`, and use its URI directly:

```bash
yolo train model=yolo26n.pt data=ul://username/datasets/dataset-slug epochs=100
```

Export NDJSON when you need a portable snapshot instead of live Platform access.

## The `images` → `labels` mirror rule

Ultralytics finds a label file by replacing the **last** `/images/` path segment with
`/labels/` and the image extension with `.txt`:

```
dataset/
├── data.yaml
├── images/train/  img001.jpg ...     ├── images/val/  ...
└── labels/train/  img001.txt ...     └── labels/val/  ...
```

- Labels next to images, or in a dir not named `labels`, are **not found** → silent
  all-background training.
- Filenames must match stems exactly (case-sensitive on Linux).
- An image with no/empty label file trains as a **background image**. A few percent of
  true backgrounds reduce false positives; accidentally missing labels destroy recall.

## data.yaml anatomy

```yaml
path: /abs/dataset/root # relative paths resolve against `yolo settings` datasets_dir — prefer absolute
train: images/train # dir, .txt file of image paths, or list of dirs
val: images/val
test: images/test # optional
names: # 0-based, contiguous indices
  0: person
  1: helmet
# pose only:
kpt_shape: [17, 3] # [num_keypoints, dims]; dims 2 (x,y) or 3 (x,y,visibility)
flip_idx: [0, 2, 1, ...] # L/R keypoint swap map — without it, flip augs are auto-disabled
# semantic only (optional — polygon labels/ also work):
masks_dir: masks # per-pixel PNG mask images
# depth only (replace names above; pair depth/{train,val}/*.png or float .npy maps):
# nc: 1
# names: {0: depth}
# depth_scale: 1000 # PNG units per meter; default millimeters
```

- Classification datasets use **no yaml**: folder structure is the label
  (`dataset/train/<class>/*.jpg`, `dataset/val/<class>/*.jpg`); train with
  `data=path/to/dataset`.
- Per-task label line formats and their gotchas: read `label-formats.md` (this folder)
  whenever writing or debugging label files.

## Converting from other formats — use built-ins first

```python
from ultralytics.data.converter import convert_coco

convert_coco(labels_dir="coco/annotations/", use_segments=True)  # COCO → detect/segment
convert_coco(labels_dir="coco/annotations/", use_keypoints=True)  # COCO → pose
```

Also in `ultralytics.data.converter`: `convert_dota_to_yolo_obb(root)` (DOTA → OBB),
`convert_segment_masks_to_yolo_seg(masks_dir, output_dir, classes)` (index PNGs →
polygons), `yolo_bbox2segment(im_dir)` (upgrade detect labels to segment via SAM),
`convert_to_multispectral(path, n_channels)`.

Auto-label a raw image folder (detector proposes boxes, SAM refines masks):

```python
from ultralytics.data.annotator import auto_annotate

auto_annotate(data="path/to/images", det_model="yolo26x.pt", sam_model="sam_b.pt")
```

For VOC XML/CSV there is no converter — write a small script emitting the per-task line
format (normalize coords, center-based boxes).

## Splitting

```python
from ultralytics.data.split import autosplit

autosplit(path="dataset/images", weights=(0.9, 0.1, 0.0))  # writes autosplit_*.txt lists
```

Point `train:`/`val:` at the generated `.txt` files. Keep frames from the same
video/scene in ONE split — per-image random splits of video frames leak near-duplicates
into val and inflate mAP. For classify: `split_classify_dataset(source_dir, 0.8)`.

## Validate before training (use the task-relevant steps in order)

1. **YAML/path check (non-classification)** — validates required fields, resolves
   configured paths, checks the requested split (default `val`), and may auto-download a
   known dataset. It does not count or parse individual images and targets:

   ```python
   from ultralytics.data.utils import check_det_dataset

   check_det_dataset("data.yaml")  # detect/segment/pose/obb/semantic/depth
   ```

2. **Detection-only visual spot check** — this helper accepts five-column
   `class cx cy w h` rows; wrong normalization or swapped axes become visible:

   ```python
   from ultralytics.data.utils import visualize_image_annotations

   visualize_image_annotations(
       "images/train/img001.jpg",
       "labels/train/img001.txt",
       label_map={0: "person", 1: "helmet"},
   )
   ```

   Do not use this helper for segment, pose, OBB, semantic, depth, or classify targets;
   use their task-aware trainer plots instead.

3. **Task-loader smoke test** — run one epoch with matching task/model/data; this builds
   the real dataset and produces task-aware training plots (detection example):
   ```bash
   yolo detect train data=data.yaml model=yolo26n.pt epochs=1 fraction=0.1
   # inspect runs/detect/train/train_batch0.jpg — boxes must sit on objects
   ```
4. **Distribution sanity** — check task-appropriate class/target balance and split
   leakage. For box tasks, also inspect very small boxes at train `imgsz` and the
   background-image share.

Known-good tiny datasets for pipeline smoke tests (auto-download): `coco8.yaml`,
`coco8-seg.yaml`, `coco8-pose.yaml`, `dota8.yaml`, `cityscapes8.yaml`, `depth8.yaml`,
`imagenet10`.

## Related pages

- `label-formats.md` — exact per-task label line formats + symptom→cause table. Read
  when writing labels, converting formats, or any label-related error.

If the installed version rejects an argument or format here, trust its error message and
`yolo checks` over this file.
