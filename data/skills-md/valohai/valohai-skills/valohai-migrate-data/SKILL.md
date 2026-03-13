---
name: valohai-migrate-data
description: Migrate data loading and model saving in ML code to use Valohai's input/output system. Use this skill when a user wants to configure data inputs from cloud storage (S3, Azure Blob, GCS), save model outputs to Valohai, replace hardcoded file paths, remove boto3/cloud SDK code, or set up the Valohai file I/O system. Triggers on mentions of inputs, outputs, data loading, model saving, S3, cloud storage, file paths, or Valohai data migration.
license: Apache-2.0
metadata:
  author: valohai
  version: "1.0"
compatibility: Requires Python. Designed for Claude Code or similar AI coding agents.
---

# Valohai Data I/O Migration

Migrate data loading and model saving to use Valohai's managed input/output system. This eliminates cloud SDK boilerplate, handles authentication automatically, and enables full data lineage tracking.

## Philosophy

Valohai separates data access from code. Inputs are declared in `valohai.yaml` with cloud storage URLs. Valohai downloads them to `/valohai/inputs/{name}/` before your code runs. Outputs are saved to `/valohai/outputs/` and automatically uploaded. No boto3, no credentials in code, no download logic.

## Step-by-Step: Inputs

### 1. Identify Data Loading Code

Look for patterns like:
- `boto3.client('s3')` / `s3.download_file()`
- `from google.cloud import storage`
- `azure.storage.blob`
- `requests.get()` for downloading datasets
- `wget` or `curl` in shell commands
- Hardcoded local paths like `/data/train/`, `./datasets/`
- `pd.read_csv("path/to/data.csv")`
- `torch.load("model.pth")` for pretrained models

### Design Principle: Always Set Default Values for Inputs

**IMPORTANT**: Whenever possible, give every input a `default` value so the step can run independently without a pipeline. This lets users test individual steps with `vh execution run step-name --adhoc`. Pipeline edges override defaults at runtime.

Look for default values in the existing code, README, documentation, config files, or data paths already referenced in the project. Only add a default if you can find a real, meaningful value. Do not invent placeholder URLs or dummy paths.

### 2. Define Inputs in valohai.yaml

```yaml
- step:
    name: train-model
    image: tensorflow/tensorflow:2.6.0
    command:
      - pip install -r requirements.txt
      - python train.py
    inputs:
      - name: training-data
        default: s3://my-bucket/datasets/train.csv
      - name: pretrained-model
        default: datum://production-model-latest
        filename: model.h5
```

#### Input Options

```yaml
inputs:
  # Single file
  - name: config
    default: s3://bucket/config.json

  # Multiple files with wildcard
  - name: images
    default:
      - s3://bucket/images/*.jpg
      - s3://bucket/images/*.png

  # Multiple cloud sources
  - name: data
    default:
      - s3://aws-bucket/data.csv
      - azure://container/data.csv
      - gs://gcs-bucket/data.csv

  # Rename on download
  - name: model
    default: s3://bucket/models/v42-best.h5
    filename: model.h5

  # Preserve directory structure
  - name: dataset
    default: s3://bucket/dataset/**/*.json
    keep-directories: suffix

  # Optional input (can be empty)
  - name: checkpoint
    optional: true

  # Reference a Valohai datum (output from another execution)
  - name: pretrained
    default: datum://my-model-alias
```

#### keep-directories Options

- `none` (default): All files flat in `/valohai/inputs/{name}/`
- `suffix`: Keeps path after the wildcard root
- `full`: Keeps the full storage path

### 3. Update Python Code

Replace cloud SDK / download code with simple local file reads:

#### Before (with boto3)

```python
import boto3

s3 = boto3.client('s3', aws_access_key_id=KEY, aws_secret_access_key=SECRET)
s3.download_file('my-bucket', 'datasets/train.csv', '/tmp/train.csv')
df = pd.read_csv('/tmp/train.csv')
```

#### After (Valohai)

```python
import pandas as pd

# Files are already downloaded to /valohai/inputs/
df = pd.read_csv("/valohai/inputs/training-data/train.csv")
```

#### Reading Multiple Input Files

```python
import os
import glob

# All files in the input directory
image_dir = "/valohai/inputs/images/"
image_files = glob.glob(os.path.join(image_dir, "*.jpg"))

for image_path in image_files:
    process_image(image_path)
```

#### Loading a Model

```python
import tensorflow as tf

# With filename option, the file is always named model.h5
model = tf.keras.models.load_model("/valohai/inputs/pretrained-model/model.h5")
```

### 4. Override Inputs at Runtime

```shell
# Override via CLI
vh execution run train-model --training-data=s3://different-bucket/new-data.csv --adhoc

# Or use the web UI to browse and select files
```

## Step-by-Step: Outputs

### 1. Identify Output/Save Code

Look for:
- `model.save("model.h5")` / `torch.save(model, "model.pth")`
- `df.to_csv("results.csv")`
- `plt.savefig("plot.png")`
- `joblib.dump(model, "model.pkl")`
- Any code saving files locally

### 2. Update Save Paths

Simply change the output path to `/valohai/outputs/`:

#### Before

```python
model.save("model.h5")
df.to_csv("results.csv")
plt.savefig("loss_curve.png")
```

#### After

```python
model.save("/valohai/outputs/model.h5")
df.to_csv("/valohai/outputs/results.csv")
plt.savefig("/valohai/outputs/loss_curve.png")
```

That's the only change needed. Valohai automatically uploads everything in `/valohai/outputs/` to your configured cloud storage when the execution completes.

### 3. Directory Structure in Outputs

Subdirectories are preserved:

```python
import os

os.makedirs("/valohai/outputs/models", exist_ok=True)
os.makedirs("/valohai/outputs/plots", exist_ok=True)

model.save("/valohai/outputs/models/best_model.h5")
plt.savefig("/valohai/outputs/plots/training_curve.png")
```

### 4. Live Upload During Training (Checkpoints)

Files marked read-only are uploaded immediately, without waiting for execution to end:

```python
import os
from stat import S_IREAD, S_IRGRP, S_IROTH

for epoch in range(epochs):
    # Training...
    if epoch % 10 == 0:
        path = f"/valohai/outputs/checkpoint_epoch_{epoch}.pt"
        torch.save(model.state_dict(), path)
        os.chmod(path, S_IREAD | S_IRGRP | S_IROTH)  # Triggers immediate upload
```

### 5. Package Large Numbers of Output Files

**IMPORTANT**: If your code produces thousands of individual files (e.g., preprocessed images, tokenized text shards, tile crops), **package them into a single archive** before writing to `/valohai/outputs/`. Do NOT write thousands of small files individually.

Valohai makes a separate HTTPS request with a presigned URL for every file it uploads and downloads. With tens of thousands of small files, you'll spend more time on HTTP overhead than actual data transfer.

Use `tar` (without compression) to bundle files — this keeps packaging fast while eliminating the per-file HTTP overhead:

```python
import tarfile
import os

# WRONG - 20,000 individual files = 20,000 HTTPS requests on download
for i, image in enumerate(processed_images):
    save_image(image, f"/valohai/outputs/image_{i}.png")

# CORRECT - 1 tar archive = 1 HTTPS request on download
output_dir = "/tmp/processed_images"
os.makedirs(output_dir, exist_ok=True)
for i, image in enumerate(processed_images):
    save_image(image, f"{output_dir}/image_{i}.png")

# Package without compression (fast, no CPU overhead)
with tarfile.open("/valohai/outputs/processed_images.tar", "w") as tar:
    tar.add(output_dir, arcname="processed_images")
```

**Rule of thumb**: If you're writing more than ~1,000 files to outputs, tar them up. A few large files are always faster than many small ones on Valohai.

### 6. No Need to Declare Outputs in YAML

You do **not** need to add an `outputs` section to `valohai.yaml`. Any file your code writes to `/valohai/outputs/` is automatically captured and uploaded. Just save files there and Valohai handles the rest.

## Validate the YAML

**IMPORTANT**: After adding inputs to `valohai.yaml`, always run `vh lint` to validate:

```shell
vh lint
```

This catches issues like invalid input names, bad URL formats in defaults, and YAML syntax errors. Fix any errors before running.

## Common Migration Patterns

### Full Training Script Migration

```python
import argparse
import json
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

parser = argparse.ArgumentParser()
parser.add_argument("--n_estimators", type=int, default=100)
parser.add_argument("--max_depth", type=int, default=10)
args = parser.parse_args()

# Load data from Valohai inputs
train_df = pd.read_csv("/valohai/inputs/training-data/train.csv")
test_df = pd.read_csv("/valohai/inputs/test-data/test.csv")

X_train, y_train = train_df.drop("target", axis=1), train_df["target"]
X_test, y_test = test_df.drop("target", axis=1), test_df["target"]

# Train model
model = RandomForestClassifier(n_estimators=args.n_estimators, max_depth=args.max_depth)
model.fit(X_train, y_train)

# Evaluate and log metrics
accuracy = accuracy_score(y_test, model.predict(X_test))
print(json.dumps({"accuracy": round(accuracy, 4)}))

# Save model to Valohai outputs
joblib.dump(model, "/valohai/outputs/model.pkl")
```

### Using datum:// References in Pipelines

Outputs from one execution can be referenced by another using `datum://` aliases:

```yaml
inputs:
  - name: model
    default: datum://production-model-latest
```

This references a specific versioned file by its alias, enabling reproducible pipeline connections.

## Creating Datasets with JSONL Metadata

Valohai uses a special metadata file (`valohai.metadata.jsonl`) to create and version datasets. Write this file to `/valohai/outputs/` alongside your output files.

### Before Creating a Dataset Version: Check Existing Versions

**IMPORTANT**: When creating a dataset version that builds on a previous version (using `from`), **always confirm with the user** which dataset version or alias to base it on. Do not guess or hardcode version numbers.

Use the CLI to fetch available data and aliases in the project:

```shell
# List data files in the project (shows datum URLs)
vh data list

# List aliases (shows named references like "production", "latest")
vh alias list
```

Ask the user:
1. Which dataset and version to base the new version on (e.g., `dataset://my-dataset/v2`)
2. Or which alias to use (e.g., `dataset://my-dataset/production`)
3. Or whether to skip basing it on a previous version entirely and create a fresh dataset

### Basic Dataset Creation

```python
import json

# Save your output files to /valohai/outputs/ as usual
df.to_csv("/valohai/outputs/processed_data.csv")

# Create the metadata file to register it as a dataset version
metadata = {
    "processed_data.csv": {
        "valohai.dataset-versions": ["dataset://my-dataset/v1"],
    },
}

with open("/valohai/outputs/valohai.metadata.jsonl", "w") as f:
    for file_name, file_metadata in metadata.items():
        json.dump({"file": file_name, "metadata": file_metadata}, f)
        f.write("\n")
```

### Dataset with Multiple Files

```python
import json

metadata = {}

# Save multiple files and register them all in the same dataset version
for split in ["train", "val", "test"]:
    filename = f"{split}.csv"
    df.to_csv(f"/valohai/outputs/{filename}")
    metadata[filename] = {
        "valohai.dataset-versions": ["dataset://my-dataset/v1"],
    }

with open("/valohai/outputs/valohai.metadata.jsonl", "w") as f:
    for file_name, file_metadata in metadata.items():
        json.dump({"file": file_name, "metadata": file_metadata}, f)
        f.write("\n")
```

### Incremental Dataset Updates

Create a new version based on a previous one, adding or excluding files:

```python
import json

metadata = {
    "new_data.csv": {
        "valohai.dataset-versions": [
            {
                "uri": "dataset://my-dataset/v3",
                "from": "dataset://my-dataset/v2",
                "start_fresh": False,
                "exclude": ["bad_file.csv", "old_file.csv"],
            },
        ],
    },
}

with open("/valohai/outputs/valohai.metadata.jsonl", "w") as f:
    for file_name, file_metadata in metadata.items():
        json.dump({"file": file_name, "metadata": file_metadata}, f)
        f.write("\n")
```

### Dataset with Aliases

Aliases let you reference datasets by name (e.g., `production`, `latest`) instead of version number:

```python
import json

metadata = {
    "model.pkl": {
        "valohai.dataset-versions": [
            {
                "uri": "dataset://my-models/v5",
                "from": "dataset://my-models/v4",
                "targeting_aliases": ["production", "stable"],
            },
        ],
    },
}

with open("/valohai/outputs/valohai.metadata.jsonl", "w") as f:
    for file_name, file_metadata in metadata.items():
        json.dump({"file": file_name, "metadata": file_metadata}, f)
        f.write("\n")
```

### Packaged Datasets (Large File Collections)

For datasets with 10,000+ small files, use packaging for 10-100x faster downloads:

```python
import json

metadata = {
    "images.tar": {
        "valohai.dataset-versions": [
            {
                "uri": "dataset://my-images/train-v1",
                "packaging": True,
            },
        ],
    },
}

with open("/valohai/outputs/valohai.metadata.jsonl", "w") as f:
    for file_name, file_metadata in metadata.items():
        json.dump({"file": file_name, "metadata": file_metadata}, f)
        f.write("\n")
```

### Consuming Datasets as Inputs

Reference datasets in `valohai.yaml` inputs using the `dataset://` URI:

```yaml
inputs:
  - name: training-data
    default: dataset://my-dataset/latest
  - name: model
    default: dataset://my-models/production
```

## Execution Environment Reference

Every Valohai execution has:
- `/valohai/repository/` - Your code (working directory)
- `/valohai/inputs/{input-name}/` - Downloaded input files (read-only)
- `/valohai/outputs/` - Write output files here
- `/valohai/config/parameters.json` - Auto-generated parameter config

## Edge Cases

- Input directories are read-only - never write to `/valohai/inputs/`
- Input names in YAML map to directory names under `/valohai/inputs/`
- If multiple files have the same name across different default URLs, they overwrite each other
- When running locally (not on Valohai), `/valohai/inputs/` won't exist - consider adding a fallback path for local development
- No file size limits on outputs
- Any file type is supported for both inputs and outputs
- Wildcard inputs: all matching files are downloaded to the same directory
