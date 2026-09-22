---
name: roboflow-data-management
description: Use when uploading images, labeling, organizing datasets, creating Roboflow projects (detection/segmentation/keypoint/classification), tags, splits, versions, or RoboQL search.
---

> **For agents — source-of-truth:** This skill is authored in [`roboflow/computer-vision-skills`](https://github.com/roboflow/computer-vision-skills) and shipped with the Roboflow plugin. If your client has loaded the plugin (you'll see `roboflow:<name>` skills in your available skills list), use those local skills — they're read fresh from disk every session. The same content served as MCP resources at `roboflow://skills/<name>/...` is a fallback for clients without the plugin and may lag this repo. **Don't call `ReadMcpResourceTool` for `roboflow://skills/...` URIs when a local `roboflow:<name>` skill is available.**

# Data Management on Roboflow

## Project Types

| Type | Annotation Format | Use Case |
|------|-------------------|----------|
| Object Detection | Bounding box (polygon/mask auto-converted) | Locate objects with boxes |
| Instance Segmentation | Polygon, Mask | Pixel-level per-object boundaries |
| Semantic Segmentation | Polygon, Mask | Pixel-level class regions |
| Keypoint Detection | Keypoints (skeleton) | Pose/skeleton estimation |
| Single-Label Classification | Image-level label (no drawn annotations) | One class per image |
| Multi-Label Classification | Image-level labels | Multiple classes per image |

Project type is set at creation and **cannot be changed later**.

## Uploading Data

### Methods

| Method | Best For | Formats |
|--------|----------|---------|
| Web UI drag-and-drop | < 1,000 images | JPG, PNG, WEBP, AVIF, BMP, MOV, MP4, PDF + 40+ annotation formats |
| CLI (`roboflow import`) | > 1,000 images (images only) | Same image formats, no video |
| Cloud storage bucket mirror | Extensive or continuously-growing data already in S3 / GCS | See `roboflow://skills/roboflow-cloud-storage/SKILL` |
| Dataset Upload Workflow Block | Collecting from production Workflows | Programmatic |
| Universe fork | Starting from a public dataset | Any Universe dataset |

**Limits:** Max 20 MB per image, max 16,400 x 10,900 px. Duplicate images are skipped automatically.

### Video Upload

Videos are split into frames at a configurable rate (1 frame/60s to 60 fps). Supported formats depend on browser (MP4 H.264 most compatible).

### CLI Upload

```bash
pip install roboflow
roboflow import -w <workspace> -p <project-id> /path/to/dataset
```

## Tags

Tags are free-form labels on images for organization and filtering.

| Action | How |
|--------|-----|
| Add during upload | Tag selector in upload dialog or via API |
| Add to existing images | Select images -> "Images Selected" -> "Apply tags" |
| Rename/delete in bulk | Project Settings -> Tags -> "Modify Tags" |
| Filter by tag | Search with `tag:<name>` or use Assign page filter |
| Use in versions | "Filter by Tag" preprocessing step (require/exclude/allow) |

## Dataset Search (RoboQL)

Search images via the Images page search bar. Combine filters with boolean logic.

### Filters

| Filter | Example | Description |
|--------|---------|-------------|
| _(free text)_ | `person on sidewalk` | Semantic search (CLIP-based) |
| `like-image:<ID>` | `like-image:abc123` | Find visually similar images |
| `filename:` | `filename:*factory*` | Filename match (`*` for partial) |
| `tag:` | `tag:factory` | Filter by tag |
| `split:` | `split:train` | Filter by split |
| `job:` | `job:<JOB_ID>` | Filter by annotation job |
| `class:` | `class:helmet` | Has annotation with class |
| `metadata:` | `metadata:key=value` | Filter by user metadata |
| `project:` | `project:my-project` | Filter by project (workspace search) |
| `sort:` | `sort:updated` | Sort results |
| `min-width:` / `max-width:` | `min-width:1000` | Image dimension filters |
| `min-height:` / `max-height:` | `max-height:800` | Image dimension filters |
| `min-annotations:` / `max-annotations:` | `max-annotations:1` | Annotation count filters |

### Boolean Logic

- `AND`, `OR`, `NOT`, parentheses: `class:helmet AND NOT (tag:v1 OR tag:v2)`
- Inverted filter with `-`: `-class:vest`
- Comparison operators on numeric filters: `>`, `<`, `>=`, `<=`, `=` (e.g., `class:helmet>=3`)

## Splits (Train / Valid / Test)

Images are assigned to train, valid, or test splits. Splits are rebalanced during version generation (Step 2 in version creation). Augmentations only apply to train split.

## Dataset Versions

A version is a **frozen snapshot** of the dataset at a point in time. Changes to the project after version creation do not affect existing versions.

### Version Creation Pipeline

1. **Source selection** — images from the dataset split
2. **Train/Test split** — rebalance percentages
3. **Preprocessing** — applied to all splits (train + valid + test)
4. **Augmentation** — applied only to train split
5. **Generate** — creates immutable version

### Preprocessing Options

| Step | Effect |
|------|--------|
| Auto-Orient | Strips EXIF, normalizes orientation |
| Resize | Stretch to / Fit within / Fit (black edges) / Fit (white edges) |
| Grayscale | Convert RGB to single channel |
| Auto-Adjust Contrast | Contrast Stretching / Histogram Equalization / Adaptive (CLAHE) |
| Isolate Objects | Crop each bbox into separate image (converts OD to classification) |
| Static Crop | Crop all images to fixed region |
| Tile | Split images into NxN grid (default 2x2, helps small object detection) |
| Dynamic Crop | Crop images around a specific class |
| Modify Classes | Remap/omit classes for this version only |
| Filter Null | Control percentage of unannotated images |
| Filter by Tag | Require / Exclude / Allow images by tag |
| Random Sample | Sample a percentage of images per split |

### Augmentation Options

Applied to train images only. Configurable max version size (e.g., 3x = source + 2 augmented copies).

| Augmentation | Image Level | BBox Level | Tier |
|--------------|:-----------:|:----------:|------|
| Flip | yes | yes | Basic |
| 90 deg Rotate | yes | yes | Basic |
| Crop | yes | yes | Basic |
| Rotation | yes | yes | Basic |
| Shear | yes | yes | Basic |
| Grayscale | yes | no | Basic |
| Hue | yes | no | Basic |
| Saturation | yes | no | Basic |
| Brightness | yes | yes | Basic |
| Exposure | yes | yes | Basic |
| Blur | yes | yes | Basic |
| Noise | yes | yes | Basic |
| Camera Gain | yes | yes | Basic |
| Motion Blur | yes | yes | Basic |
| Cutout | yes | no | Enhanced (paid) |
| Mosaic | yes | no | Enhanced (paid) |

## Dataset Analytics

Available at project sidebar -> "Analytics". Shows:

- Image count, annotation count, avg image size, median aspect ratio
- Missing and null annotation counts
- Class distribution across train/valid/test
- Image dimension insights (size + aspect ratio distribution)
- Annotation heatmap (click-drag to filter images by region)
- Object count histogram (click bars to see matching images)

## Classes

Managed at Project Settings -> Classes.

| Action | Description |
|--------|-------------|
| Rename | Type new name in Override column |
| Merge | Override multiple classes to same name |
| Delete | Check Delete checkbox |
| Lock | "Lock Annotation Classes" prevents new class creation |

**Warning:** Class changes at project level affect all images (irreversible). Use version-level "Modify Classes" preprocessing for non-destructive changes.

## Annotation Groups

Annotation group = the category encompassing all classes in a project. Projects sharing the same annotation group **share their class list and annotations**.

- Enable during project creation: "Share image annotations with other projects"
- Shared annotations: editing in one project affects all linked projects
- Look for chain-link icon to identify shared images/projects
- Images shared across projects count only once toward usage

## Project Folders

Folders group projects for organization. SSO workspaces can restrict folder access to specific team members.

| Action | How |
|--------|-----|
| Create | "+ New Folder" from workspace view |
| Move project | Project menu -> "Move Project" |
| Delete folder | Folder menu -> "Delete" (projects move to workspace root, not deleted) |

## Export Formats

Versions can be exported as `.zip` download or `curl` command. 40+ formats supported including COCO, YOLO, Pascal VOC, TFRecord, and more. Full list at `roboflow.com/formats`.

Export via Python SDK:

```python
project.version(1).download("yolov8")
```

## MCP apps vs plain tools

Prefab MCP apps (`create_project_app`) exist when parameters are unclear, you need real UX, or a human must confirm after seeing form fields — plain chat/MCP calls should not guess project type and license alone.


## MCP Tools Available

| Tool | Purpose |
|------|---------|
| `projects_create` | Create a new project (specify type, annotation group) |
| `projects_list` / `projects_get` | List or get project details |
| `images_search` | Search images using RoboQL filters |
| `image_upload` / `image_upload_status` | Prepare zip image upload and poll status |
| `versions_generate` | Generate a dataset version with preprocessing/augmentation |
| `versions_get` | Inspect a version |
| `versions_export` | Export a version in a given format |

## Related Pages

- `roboflow://skills/roboflow-data-management/labeling` — annotation tools, AI labeling, Label Assist, Smart Polygon, Auto Label, annotation jobs
- `roboflow://skills/roboflow-cloud-storage/SKILL` — mirror an S3/GCS bucket into the workspace (credentials, datasources, glob rules, scheduled sync)
