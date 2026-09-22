---
name: roboflow-universe
description: Use when searching for or using public datasets/models on Roboflow Universe (universe.roboflow.com), the open repository of 1M+ computer vision datasets and 50K+ pre-trained models.
---

> **For agents — source-of-truth:** This skill is authored in [`roboflow/computer-vision-skills`](https://github.com/roboflow/computer-vision-skills) and shipped with the Roboflow plugin. If your client has loaded the plugin (you'll see `roboflow:<name>` skills in your available skills list), use those local skills — they're read fresh from disk every session. The same content served as MCP resources at `roboflow://skills/<name>/...` is a fallback for clients without the plugin and may lag this repo. **Don't call `ReadMcpResourceTool` for `roboflow://skills/...` URIs when a local `roboflow:<name>` skill is available.**

# Roboflow Universe

Open repository of 1M+ computer vision datasets and 50K+ pre-trained models at `universe.roboflow.com`.

## URL Patterns

| Page | URL | Content |
|------|-----|---------|
| Home | `universe.roboflow.com` | Search, trending projects, categories |
| Project | `universe.roboflow.com/{owner}/{project}` | Overview, classes, metrics, license, fork |
| Images | `universe.roboflow.com/{owner}/{project}/browse` | Browse images with annotations |
| Dataset version | `universe.roboflow.com/{owner}/{project}/dataset/{version}` | Version details, splits, download |
| Model | `universe.roboflow.com/{owner}/{project}/model/{version}` | Try model, metrics, deploy snippet |

## Searching Universe

### MCP app (`universe_search_app`)

Use when someone must **choose a dataset after seeing it**: previews, classes, license, image counts, etc. Pure MCP JSON hits from `universe_search` are not a substitute for that UX — open the app when the decision needs eyes on the listings.


### MCP Tool

Use `universe_search` to find datasets/models programmatically. Pass a descriptive query (e.g. "hard hat detection construction site").

### Web Search

Search is **hybrid** — combines semantic similarity with keyword matching. Use specific, descriptive queries for best results.

### Query Operators

All operators can be mixed with free-text: `fire smoke class:fire,smoke images>200 model`

| Operator | Example | Effect |
|----------|---------|--------|
| `model` | `waste detection model` | Only datasets with a trained model |
| `object detection` | `helmet object detection` | Filter by project type (also: `classification`, `instance segmentation`, `keypoint detection`) |
| `class:X` | `class:helmet,person` | Must contain these classes |
| `tag:X` | `tag:safety` | Filter by Universe tag |
| `model:X` | `model:yolov8` | Filter by trained model architecture |
| `images>N` | `images>500` | Min image count (also `>=`, `<`, `<=`, `=`) |
| `stars>=N` | `stars>=5` | Min star count |
| `views>N` | `views>1000` | Min view count |
| `downloads>N` | `downloads>100` | Min download count |
| `updated:Nd` | `updated:30d` | Updated within N days (also `h`, `w`, `mo`, `y`) |
| `sort:X` | `sort:stars` | Sort by field (stars, images, updated, downloads, views) |
| `like:dataset-url` | `like:coco` | Find similar datasets |

### Tips for Effective Queries

- Combine free-text with operators: `pothole road damage class:pothole images>100 sort:stars`
- Add `model` to only get inference-ready datasets
- Include project type keywords to filter: `helmet instance segmentation`
- Use `class:` when you know exactly what classes you need
- Use specific object names, not generic terms ("forklift in warehouse" > "vehicle")

## Evaluating a Dataset

Before forking, check these signals:

| Criterion | Where to Look | Good Sign |
|-----------|---------------|-----------|
| Class coverage | Classes list on project page | All your target classes present |
| Image count | Project overview | 500+ images per class for detection |
| Annotation quality | Browse > click individual images | Tight bounding boxes, consistent labels |
| Class balance | Project overview / health | No extreme class imbalance |
| Image diversity | Browse images | Varied lighting, angles, backgrounds |
| License | "Cite this Project" section | Compatible with your use case (see below) |
| Model metrics | Model tab (if available) | mAP > 70% suggests decent annotations |

## Licenses

Found in the "Cite this Project" section on the project page. No license listed = all rights reserved.

| License | Commercial Use | Modify | Attribution Required |
|---------|---------------|--------|---------------------|
| Public Domain | Yes | Yes | No |
| CC BY 4.0 | Yes | Yes | Yes |
| MIT | Yes | Yes | Yes (in license copy) |
| BY-NC-SA 4.0 | No | Yes (share-alike) | Yes |
| ODbL v1.0 | Yes | Yes (share-alike for DB) | Yes |
| No license specified | Assume No | Assume No | N/A |

## Forking a Dataset

Fork = copy a Universe dataset into your workspace (no download/re-upload needed).

1. Open dataset on Universe
2. Click **Download Dataset** button
3. Choose **Train a model with this dataset** (full fork) or **Train from a portion of this dataset** (partial clone)
4. Dataset copies into your workspace

After forking you can: rename classes, add/remove images, generate versions, train models.

**Requires:** Logged-in Roboflow account.

## Downloading a Dataset

For local/notebook training instead of Roboflow cloud training.

| Method | When to Use |
|--------|-------------|
| Train a model with this dataset (fork) | Training on Roboflow, want full data in workspace |
| Train from a portion (clone) | Want a subset or to combine with other data |
| Download dataset | Local training via code snippet or ZIP file |

Supports all standard export formats (COCO, YOLO, VOC, CreateML, TFRecord, etc.).

Path: Project page > **Download Dataset** button > choose method.

## Using a Universe Model

### Direct Inference via Workflows

1. Create a Workflow in Roboflow
2. Add a model block
3. Switch to **Public Models** tab
4. Paste the model ID from the Universe model page (copy icon at top)
5. Click **Use model ID**

Model ID format: `{owner}/{project}/{version}` (shown on Universe model page).

### Checkpoint Training

Fork the dataset, then train your own model using the forked data. Use a Universe model's architecture as a starting point via Roboflow Train.

### Inference Metrics (shown on model page)

| Project Type | Metrics Shown |
|--------------|---------------|
| Object Detection | mAP, precision, recall |
| Classification | Accuracy |
| Segmentation | mAP, precision, recall |

## MCP Tool Reference

`universe_search` — Search Universe for datasets/models.

| Param | Type | Default | Notes |
|-------|------|---------|-------|
| `query` | str (required) | — | Search query text |
| `result_type` | `"dataset"` \| `"model"` \| null | null | Filter by result type |
| `limit` | int | 12 | Max results per page |
| `page` | int | 1 | Page number (1-indexed) |

Returns: name, url, type, classes, classCount, images, description, tags, license, stars, views, downloads, modelCount, latestVersion.

## Related Skills

- `roboflow://skills/roboflow-data-management/SKILL` — managing datasets after import
- `roboflow://skills/roboflow-training-and-evaluation/SKILL` — training on forked data
