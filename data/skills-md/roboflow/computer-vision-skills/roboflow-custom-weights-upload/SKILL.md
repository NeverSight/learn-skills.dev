---
name: roboflow-custom-weights-upload
description: Use when uploading locally trained model weights (YOLO, RF-DETR, YOLO-NAS, PaliGemma, Florence-2) to Roboflow — the client-side Python SDK upload flow, safe API key handling, per-family packaging requirements, and verifying the upload.
---

> **For agents — source-of-truth:** This skill is authored in [`roboflow/computer-vision-skills`](https://github.com/roboflow/computer-vision-skills) and shipped with the Roboflow plugin. If your client has loaded the plugin (you'll see `roboflow:<name>` skills in your available skills list), use those local skills — they're read fresh from disk every session. The same content served as MCP resources at `roboflow://skills/<name>/...` is a fallback for clients without the plugin and may lag this repo. **Don't call `ReadMcpResourceTool` for `roboflow://skills/...` URIs when a local `roboflow:<name>` skill is available.**

# Custom Weights Upload

Register weights from a model trained outside Roboflow (a laptop, a training
server, Colab) so Roboflow can convert, host, and serve it.

## Where the upload runs

Packaging reads the checkpoint from disk, so the upload always runs on the
machine that has the weights — client-side, with the Python SDK flow below.

The `models_upload_custom_weights` MCP tool is a guide, not an uploader:
calling it returns this recipe and echoes back the arguments you passed
(its `upload_mode` field says whether they describe a versioned or a
workspace upload, or `undetermined` when they pin down neither). It never
packages or uploads anything, because the MCP server cannot read the user's
filesystem.

## Client-side upload with the Python SDK

Run this on the machine that has the weights, ideally in the same Python
environment used for training (it already has `torch` and the matching
`ultralytics`).

1. **Install the SDK**: both `roboflow>=1.3.13` and `rfdetr` require
   **Python >= 3.10**; check `python3 --version` first (macOS ships 3.9). If
   it is too old, create a venv: `uv venv --python 3.12 && source
   .venv/bin/activate`. Then `pip install "roboflow>=1.3.13"`.
2. **Handle the API key safely**: never ask the user to paste a private API
   key into chat, and never scan dotfiles, shell profiles, or config files
   hunting for one — permission systems rightly block that. If
   `ROBOFLOW_API_KEY` is already set in the environment
   (`test -n "$ROBOFLOW_API_KEY"`) or the working project has a `.env` that
   defines it, use it. Otherwise mint a scoped key with the MCP
   `api_keys_create` tool — it returns the secret once (`api_keys_roll` is
   the only other tool that does; `api_keys_list` / `api_keys_get` return
   masked metadata) — and write it yourself to a `.gitignore`'d `.env` as
   `ROBOFLOW_API_KEY`. Writing `.env` does not populate `os.environ`: load it
   before running. For a `.env` you just wrote yourself,
   `set -a; source .env; set +a` is fine. For a pre-existing `.env`, never
   `source` it — sourcing executes any shell in the file and exports every
   other secret it holds into the process. Read only the one key instead,
   e.g. with `python-dotenv` (`pip install python-dotenv`) in the script:

   ```python
   import os
   from dotenv import dotenv_values

   os.environ["ROBOFLOW_API_KEY"] = dotenv_values(".env")["ROBOFLOW_API_KEY"]
   ```

   Scope the key for the whole deploy flow, not minimally: the SDK's
   `rf.workspace()` reads the workspace and its project list before
   deploying, so `project:read` plus `model:deploy` alone fails with missing
   permissions. Include `workspace:read`, `project:read`, `model:deploy`,
   and for a versioned deploy also `version:read` and `version:update`.
   Getting the scopes right at mint time is what protects the upload: the
   preflight below only confirms the key and the workspace read, not the
   deploy scope.

   If the `api_keys_create` call is denied (permission systems may flag
   credential creation during an upload task) or unavailable, do not work
   around the denial. Ask the user to choose: (a) explicitly authorize
   minting a temporary scoped key, which you revoke with `api_keys_revoke`
   after the upload; (b) set `ROBOFLOW_API_KEY` themselves in their shell or
   a `.env`; or (c) point you at an existing `.env` that already defines it.
3. **Confirm the destination and the name with the user**: registering a
   model is not easily undone. Never infer the target project or version from
   the checkpoint's class count or filename — ask. The same goes for
   `model_name` on a workspace upload: ask the user what the model should be
   called; do not invent a name.

### Preflight before packaging

Packaging plus a 100 MB+ upload is slow; run the cheap checks first and
report every gap at once instead of failing one step at a time:

1. Python is >= 3.10 (`python3 --version`).
2. Required imports load: `torch` for YOLO, RF-DETR, and YOLO-NAS;
   `ultralytics` for YOLO v8/v10/v11/v12/26; `rfdetr>=1.8.0` for raw
   PyTorch-Lightning RF-DETR checkpoints.
3. The key is valid and covers the workspace read — one cheap call that
   exercises the same workspace/project-list read `deploy_model` starts with:

   ```python
   import os
   from roboflow import Roboflow

   Roboflow(api_key=os.environ["ROBOFLOW_API_KEY"]).workspace()
   ```

   Be honest about the limit of this check: it does not exercise
   `model:deploy`, which the platform only tests at `models/prepareUpload`,
   after packaging. That is why step 2 mints the key with the full scope set
   up front — the preflight catches a bad or under-read key, not a missing
   deploy scope on an existing key.

Only package and upload after all three pass.

Workspace model upload (no dataset version required):

```python
import os
from roboflow import Roboflow

rf = Roboflow(api_key=os.environ["ROBOFLOW_API_KEY"])
workspace = rf.workspace("WORKSPACE_SLUG")
workspace.deploy_model(
    model_type="rfdetr-base",
    model_path="/path/to/training/output",
    project_ids=["PROJECT_SLUG"],
    model_name="MODEL_NAME",
    filename="checkpoint_best_total.pth",  # relative to model_path
)
```

Versioned deploy (attach weights to an existing dataset version):

```python
import os
from roboflow import Roboflow

rf = Roboflow(api_key=os.environ["ROBOFLOW_API_KEY"])
version = rf.workspace("WORKSPACE_SLUG").project("PROJECT_SLUG").version(3)
version.deploy(
    model_type="yolov8n",
    model_path="/path/to/runs/detect/train",
    filename="weights/best.pt",
)
```

`model_type` must name the real architecture (`yolov8n`, `yolov11s`,
`rfdetr-base`, `rfdetr-seg-medium`, `yolonas`, a supported PaliGemma or
Florence-2 type). For YOLO families the SDK infers a missing size suffix
from the weights; RF-DETR accepts no bare `rfdetr` — pass the exact variant,
which the SDK cross-checks against the checkpoint.

On a size/variant or dependency mismatch, `deploy_model` / `version.deploy`
print the error and then **interactively prompt** "Would you like to continue
anyway? y/n" — in a headless run the prompt surfaces as an `EOFError` right
after the printed error. Recover by error type:

- **Size/variant mismatch**: when the error names the type that fits, fix
  `model_type` to it and rerun; when it says the size could not be inferred,
  pass an explicit size.
- **Dependency mismatch**: the error names a pip pin, not a model type
  (`yolov8` recommends `ultralytics==8.0.196`, so most current training
  environments hit this prompt). Install the named version, or — only with
  the user's explicit confirmation — answer `y` (headless:
  `printf 'y\n' | python upload.py`) to continue with the installed version.

Never force past either prompt without the user explicitly confirming the
override is intentional.

## Per-family requirements

- **YOLO v8/v10/v11/v12/YOLO26**: needs `torch` and `ultralytics` importable
  (`yolov8` recommends `ultralytics==8.0.196`; see the dependency-mismatch
  note above). **Legacy YOLO v5/v7/v9**: needs `torch` plus an `opt.yaml` in
  `model_path` with `imgsz` (or `img_size`) and `batch_size`; `ultralytics`
  is not used. There is no yolov6 support.
- **RF-DETR**: needs `torch` to read the checkpoint. If a `class_names.txt`
  (one class per line) sits in `model_path` it is used; otherwise class names
  come from the checkpoint's `args`. Raw PyTorch-Lightning checkpoints
  additionally need `rfdetr>=1.8.0` installed (the SDK's error names the
  exact minimum if yours is older). An explicit `filename` that does not
  exist is a hard error; the default `weights/best.pt` falls back to the
  first top-level `.pt`/`.pth` file, with a warning.
- **YOLO-NAS**: `model_type="yolonas"` plus an `opt.yaml` in `model_path`
  with `imgsz`, `batch_size`, and `architecture`.
- **PaliGemma / Florence-2**: `model_path` is the Hugging Face save directory
  (config, tokenizer, and weights files); no `torch` needed.

## Verify the upload

Conversion runs server-side after the upload and usually takes a few minutes.
Check it with the MCP `models_list` / `models_get` tools or at
`app.roboflow.com/WORKSPACE/PROJECT/models`, then run a test inference on a
sample image to confirm classes and predictions look right.
