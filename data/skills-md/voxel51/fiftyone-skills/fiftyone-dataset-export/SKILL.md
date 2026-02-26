---
name: fiftyone-dataset-export
description: Exports FiftyOne datasets to standard formats (COCO, YOLO, VOC, CVAT, CSV, etc.) and Hugging Face Hub. Use when converting datasets, exporting for training, creating archives, sharing data in specific formats, or publishing datasets to Hugging Face.
---

# Export FiftyOne Datasets

## Key Directives

**ALWAYS follow these rules:**

### 1. Load and understand the dataset first
```python
set_context(dataset_name="my-dataset")
dataset_summary(name="my-dataset")
```

### 2. Confirm export settings with user
Before exporting, present:
- Dataset name and sample count
- Available label fields and their types
- Proposed export format
- Export directory path

### 3. Match format to label types
Different formats support different label types:

| Format | Label Types |
|--------|-------------|
| COCO | detections, segmentations, keypoints |
| YOLO (v4, v5) | detections |
| VOC | detections |
| CVAT | classifications, detections, polylines, keypoints |
| CSV | all (custom fields) |
| Image Classification Directory Tree | classification |

### 4. Use absolute paths
Always use absolute paths for export directories:
```python
params={
    "export_dir": {"absolute_path": "/path/to/export"}
}
```

### 5. Warn about overwriting
Check if export directory exists before exporting. If it does, ask user whether to overwrite.

## Complete Workflow

### Step 1: Load Dataset and Understand Content

```python
# Set context
set_context(dataset_name="my-dataset")

# Get dataset summary to see fields and label types
dataset_summary(name="my-dataset")
```

Identify:
- Total sample count
- Media type (images, videos, point clouds)
- Available label fields and their types (Detections, Classifications, etc.)

### Step 2: Get Export Operator Schema

```python
# Discover export parameters dynamically
get_operator_schema(operator_uri="@voxel51/io/export_samples")
```

### Step 3: Present Export Options to User

Before exporting, confirm with the user:

```
Dataset: my-dataset (5,000 samples)
Media type: image

Available label fields:
  - ground_truth (Detections)
  - predictions (Detections)

Export options:
  - Format: COCO (recommended for detections)
  - Export directory: /path/to/export
  - Label field: ground_truth

Proceed with export?
```

### Step 4: Execute Export

**Export media and labels:**
```python
execute_operator(
    operator_uri="@voxel51/io/export_samples",
    params={
        "export_type": "MEDIA_AND_LABELS",
        "dataset_type": "COCO",
        "export_dir": {"absolute_path": "/path/to/export"},
        "label_field": "ground_truth"
    }
)
```

**Export labels only (no media copy):**
```python
execute_operator(
    operator_uri="@voxel51/io/export_samples",
    params={
        "export_type": "LABELS_ONLY",
        "dataset_type": "COCO",
        "labels_path": {"absolute_path": "/path/to/labels.json"},
        "label_field": "ground_truth"
    }
)
```

**Export media only (no labels):**
```python
execute_operator(
    operator_uri="@voxel51/io/export_samples",
    params={
        "export_type": "MEDIA_ONLY",
        "export_dir": {"absolute_path": "/path/to/media"}
    }
)
```

### Step 5: Verify Export

After export, verify the output:

```bash
ls -la /path/to/export
```

Report exported file count and structure to user.

## Supported Export Formats

### Detection Formats

| Format | `dataset_type` Value | Label Types | Labels-Only |
|--------|----------------------|-------------|-------------|
| COCO | `"COCO"` | detections, segmentations, keypoints | Yes |
| YOLOv4 | `"YOLOv4"` | detections | Yes |
| YOLOv5 | `"YOLOv5"` | detections | No |
| VOC | `"VOC"` | detections | Yes |
| KITTI | `"KITTI"` | detections | Yes |
| CVAT Image | `"CVAT Image"` | classifications, detections, polylines, keypoints | Yes |
| CVAT Video | `"CVAT Video"` | frame labels | Yes |
| TF Object Detection | `"TF Object Detection"` | detections | No |

### Classification Formats

| Format | `dataset_type` Value | Media Type | Labels-Only |
|--------|----------------------|------------|-------------|
| Image Classification Directory Tree | `"Image Classification Directory Tree"` | image | No |
| Video Classification Directory Tree | `"Video Classification Directory Tree"` | video | No |
| TF Image Classification | `"TF Image Classification"` | image | No |

### Segmentation Formats

| Format | `dataset_type` Value | Label Types | Labels-Only |
|--------|----------------------|-------------|-------------|
| Image Segmentation | `"Image Segmentation"` | segmentation | Yes |

### General Formats

| Format | `dataset_type` Value | Best For | Labels-Only |
|--------|----------------------|----------|-------------|
| CSV | `"CSV"` | Custom fields, spreadsheet analysis | Yes |
| GeoJSON | `"GeoJSON"` | Geolocation data | Yes |
| FiftyOne Dataset | `"FiftyOne Dataset"` | Full dataset backup with all metadata | Yes |

**Note:** Formats with "Labels-Only: No" require `export_type: "MEDIA_AND_LABELS"` (cannot export labels without media).

## Export Type Options

| `export_type` Value | Description |
|---------------------|-------------|
| `"MEDIA_AND_LABELS"` | Export both media files and labels |
| `"LABELS_ONLY"` | Export labels only (use `labels_path` instead of `export_dir`) |
| `"MEDIA_ONLY"` | Export media files only (no labels) |
| `"FILEPATHS_ONLY"` | Export CSV with filepaths only |

## Target Options

Export from different sources:

| `target` Value | Description |
|----------------|-------------|
| `"DATASET"` | Export entire dataset (default) |
| `"CURRENT_VIEW"` | Export current filtered view |
| `"SELECTED_SAMPLES"` | Export selected samples only |

## Common Use Cases

### Use Case 1: Export to COCO Format

For training with frameworks that use COCO format:

```python
set_context(dataset_name="my-dataset")

execute_operator(
    operator_uri="@voxel51/io/export_samples",
    params={
        "export_type": "MEDIA_AND_LABELS",
        "dataset_type": "COCO",
        "export_dir": {"absolute_path": "/path/to/coco_export"},
        "label_field": "ground_truth"
    }
)
```

Output structure:
```
coco_export/
├── data/
│   ├── image1.jpg
│   └── image2.jpg
└── labels.json
```

### Use Case 2: Export to YOLO Format

For training YOLOv5/v8 models:

```python
set_context(dataset_name="my-dataset")

execute_operator(
    operator_uri="@voxel51/io/export_samples",
    params={
        "export_type": "MEDIA_AND_LABELS",
        "dataset_type": "YOLOv5",
        "export_dir": {"absolute_path": "/path/to/yolo_export"},
        "label_field": "ground_truth"
    }
)
```

Output structure:
```
yolo_export/
├── images/
│   └── train/
│       └── image1.jpg
├── labels/
│   └── train/
│       └── image1.txt
└── dataset.yaml
```

### Use Case 3: Export Filtered View

Export only a subset of samples:

```python
# Set context
set_context(dataset_name="my-dataset")

# Filter samples in the App
set_view(tags=["validated"])

# Export the filtered view
execute_operator(
    operator_uri="@voxel51/io/export_samples",
    params={
        "target": "CURRENT_VIEW",
        "export_type": "MEDIA_AND_LABELS",
        "dataset_type": "COCO",
        "export_dir": {"absolute_path": "/path/to/validated_export"},
        "label_field": "ground_truth"
    }
)
```

### Use Case 4: Export Labels Only

When media should stay in place:

```python
set_context(dataset_name="my-dataset")

execute_operator(
    operator_uri="@voxel51/io/export_samples",
    params={
        "export_type": "LABELS_ONLY",
        "dataset_type": "COCO",
        "labels_path": {"absolute_path": "/path/to/annotations.json"},
        "label_field": "ground_truth"
    }
)
```

### Use Case 5: Export for Classification Training

For image classification datasets:

```python
set_context(dataset_name="my-classification-dataset")

execute_operator(
    operator_uri="@voxel51/io/export_samples",
    params={
        "export_type": "MEDIA_AND_LABELS",
        "dataset_type": "Image Classification Directory Tree",
        "export_dir": {"absolute_path": "/path/to/classification_export"},
        "label_field": "ground_truth"
    }
)
```

Output structure:
```
classification_export/
├── cat/
│   ├── cat1.jpg
│   └── cat2.jpg
└── dog/
    ├── dog1.jpg
    └── dog2.jpg
```

### Use Case 6: Export to CSV

For analysis in spreadsheets:

```python
set_context(dataset_name="my-dataset")

execute_operator(
    operator_uri="@voxel51/io/export_samples",
    params={
        "export_type": "LABELS_ONLY",
        "dataset_type": "CSV",
        "labels_path": {"absolute_path": "/path/to/data.csv"},
        "csv_fields": ["filepath", "ground_truth.detections.label"]
    }
)
```

### Use Case 7: Export FiftyOne Dataset (Full Backup)

For complete dataset backup including all metadata:

```python
set_context(dataset_name="my-dataset")

execute_operator(
    operator_uri="@voxel51/io/export_samples",
    params={
        "export_type": "MEDIA_AND_LABELS",
        "dataset_type": "FiftyOne Dataset",
        "export_dir": {"absolute_path": "/path/to/backup"}
    }
)
```

Output structure:
```
backup/
├── metadata.json
├── samples.json
├── data/
│   └── ...
├── annotations/
├── brain/
└── evaluations/
```

## Python SDK Alternative

For more control, guide users to use the Python SDK directly:

```python
import fiftyone as fo
import fiftyone.types as fot

# Load dataset
dataset = fo.load_dataset("my-dataset")

# Export to COCO format
dataset.export(
    export_dir="/path/to/export",
    dataset_type=fot.COCODetectionDataset,
    label_field="ground_truth",
)

# Export labels only
dataset.export(
    labels_path="/path/to/labels.json",
    dataset_type=fot.COCODetectionDataset,
    label_field="ground_truth",
)

# Export a filtered view
view = dataset.match_tags("validated")
view.export(
    export_dir="/path/to/validated",
    dataset_type=fot.YOLOv5Dataset,
    label_field="ground_truth",
)
```

**Python SDK dataset types:**
- `fot.COCODetectionDataset` - COCO format
- `fot.YOLOv4Dataset` - YOLOv4 format
- `fot.YOLOv5Dataset` - YOLOv5 format
- `fot.VOCDetectionDataset` - Pascal VOC format
- `fot.KITTIDetectionDataset` - KITTI format
- `fot.CVATImageDataset` - CVAT image format
- `fot.CVATVideoDataset` - CVAT video format
- `fot.TFObjectDetectionDataset` - TensorFlow Object Detection format
- `fot.ImageClassificationDirectoryTree` - Classification folder structure
- `fot.VideoClassificationDirectoryTree` - Video classification folders
- `fot.TFImageClassificationDataset` - TensorFlow classification format
- `fot.ImageSegmentationDirectory` - Segmentation masks
- `fot.CSVDataset` - CSV format
- `fot.GeoJSONDataset` - GeoJSON format
- `fot.FiftyOneDataset` - Native FiftyOne format

## Exporting to Hugging Face Hub

For complete HF Hub export documentation, see [HF-HUB-EXPORT.md](HF-HUB-EXPORT.md).

**Quick reference:**

| Method | Use Case |
|--------|----------|
| `push_to_hub()` | Personal accounts, simple upload |
| Manual upload | Organizations, private org repos |

**Quick start:**
```python
from fiftyone.utils.huggingface import push_to_hub

# Personal account
push_to_hub(dataset, repo_name="my-dataset", private=False)

# With options
push_to_hub(
    dataset,
    repo_name="my-dataset",
    description="My dataset description",
    license="apache-2.0",
    private=True,
)
```

**IMPORTANT:** Always generate and get user approval for dataset card before uploading. See [HF-HUB-EXPORT.md](HF-HUB-EXPORT.md) for complete documentation including authentication setup, dataset card workflow, parameters reference, use cases, and troubleshooting.

## Troubleshooting

**Error: "Export directory already exists"**
- Add `"overwrite": true` to params
- Or specify a different export directory

**Error: "Label field not found"**
- Use `dataset_summary()` to see available label fields
- Verify the field name spelling

**Error: "Unsupported label type for format"**
- Check that the export format supports your label type
- COCO: detections, segmentations, keypoints
- YOLO: detections only
- Classification formats: classification labels only

**Error: "Permission denied"**
- Verify write permissions for the export directory
- Check parent directory exists

**Export is slow**
- Large datasets take time; consider exporting a view first
- Export to local disk rather than network drives
- For labels only, use `LABELS_ONLY` export type

## Best Practices

1. **Understand your data first** - Use `dataset_summary()` to know what fields and label types exist
2. **Match format to purpose** - Use COCO/YOLO for training, CSV for analysis, FiftyOne Dataset for backups
3. **Confirm with user** - Present export settings before executing
4. **Export filtered views** - Only export what's needed rather than entire datasets
5. **Verify after export** - Check exported file counts match expectations
6. **Use labels_path for LABELS_ONLY** - When exporting labels only, use `labels_path` not `export_dir`

## Resources

- [FiftyOne Export Guide](https://docs.voxel51.com/user_guide/export_datasets.html)
- [Supported Export Formats](https://docs.voxel51.com/user_guide/export_datasets.html#supported-formats)
- [FiftyOne I/O Plugin](https://github.com/voxel51/fiftyone-plugins/tree/main/plugins/io)
- [FiftyOne Hugging Face Integration](https://docs.voxel51.com/integrations/huggingface.html)
- [Hugging Face Hub Documentation](https://huggingface.co/docs/hub/index)
