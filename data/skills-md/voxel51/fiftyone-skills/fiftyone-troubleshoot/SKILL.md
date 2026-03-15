---
name: fiftyone-troubleshoot
description: Diagnose and fix common FiftyOne issues automatically. Use when a dataset disappeared, the App won't open, changes aren't saving, MongoDB errors occur, video codecs fail, notebook connectivity breaks, operators are missing, or any recurring FiftyOne pain point needs solving.
---

# FiftyOne Troubleshoot

## Overview

Diagnose and fix common FiftyOne pain points. Match the user's symptom to the [Issue Index](#issue-index), explain the root cause and proposed fix, get approval, then apply.

> Shell commands in this skill are written for macOS/Linux. On Windows (non-WSL), adapt using PowerShell equivalents or use WSL.

Designed to grow: add new issues at the bottom as they are encountered.

## Prerequisites

- FiftyOne installed: `pip install fiftyone`
- MCP server running (optional, for plugin-related fixes)

## Key Directives

### 1. Always explain, propose, and confirm before acting
**NEVER run a fix without first:**
1. Explaining what is wrong and why
2. Describing what the fix will do
3. Asking the user to confirm: *"Should I apply this fix?"*

Wait for explicit user confirmation before executing anything that modifies files, config, or data.

### 2. Never touch user datasets — FiftyOne is the source of truth
- Except when given explicit and direct instructions by the user:
    - NEVER modify, edit, delete, or clone user datasets as part of troubleshooting
    - NEVER call `fo.delete_dataset()`
    - NEVER truncate, wipe, or alter dataset contents or sample fields to diagnose an issue
- Use FiftyOne's read-only API to inspect state: `fo.list_datasets()`, `fo.load_dataset()`, `len(dataset)`, `dataset.get_field_schema()` — these are safe
- FiftyOne's state (datasets, fields, brain runs) is the ground truth; read it, never rewrite it to "fix" a problem

### 3. Never directly manipulate MongoDB
- NEVER use `pymongo`, `db.drop_collection()`, or raw MongoDB shell commands
- All data operations must go through the FiftyOne Python API

### 4. Never modify config or files silently
- NEVER change `database_uri`, `database_name`, or any config file without showing what will change and getting approval
- NEVER append to shell profiles (`.zshrc`, `.bash_profile`, virtualenv `activate`) without showing the exact line change and getting explicit user confirmation to apply

### 5. Restart processes after env / config changes
Any fix that sets an environment variable or modifies a config file only takes effect for **new** processes. Already-running App servers, service managers, and Python scripts will NOT pick up the change.
- After setting `FIFTYONE_DATABASE_NAME` or similar env vars, identify and restart any running FiftyOne processes
- Check with: `ps aux | grep fiftyone`
- Stop stale processes: `pkill -f "fiftyone"` (confirm with user first)

### 6. Always verify after fixing
Run the [Health Check](#health-check) after every fix to confirm the environment is operational.

---

## Workflow

1. **Diagnose** — run the Diagnostic Quick-Check
2. **Explain** — describe the root cause in plain language
3. **Propose** — show the fix and what it will change
4. **Confirm** — ask the user: *"Should I apply this?"*
5. **Execute** — apply the fix only after approval
6. **Verify** — run the Health Check

---

## Diagnostic Quick-Check

Handles connection failures gracefully — always produce useful output:

```python
import sys

print(f"Python:  {sys.executable}")
print(f"Version: {sys.version.split()[0]}")

try:
    import fiftyone as fo
    print(f"FiftyOne: {fo.__version__}")
    print(f"Database: {fo.config.database_name}")
    print(f"DB URI:   {fo.config.database_uri or '(internal MongoDB)'}")
except ImportError:
    print("ERROR: fiftyone not installed — check Python environment, if needed run: pip install fiftyone")
    sys.exit(1)

try:
    print(f"Datasets: {fo.list_datasets()}")
    print("Connection: OK")
except Exception as e:
    print(f"Connection ERROR: {e}")
    print("→ Match this error to the Issue Index below")
```

---

## Health Check

Run after any fix to confirm the environment is fully operational.

> This script creates and destroys a **temporary test dataset** (`_fo_health_check`). It does not touch any user datasets. Do not manually create a dataset with the name "_fo_health_check".

```python
import fiftyone as fo
import tempfile, os

TEST_NAME = "_fo_health_check"

try:
    # Clean up any debris from a previous failed check
    if TEST_NAME in fo.list_datasets():
        fo.delete_dataset(TEST_NAME)

    # Non-persistent: auto-removed if Python exits before cleanup
    dataset = fo.Dataset(TEST_NAME, persistent=False)
    dataset.add_sample(fo.Sample(
        filepath=os.path.join(tempfile.gettempdir(), "health_check.jpg")
    ))
    assert len(dataset) == 1, "Sample write failed"

    # Verify connection round-trip
    assert TEST_NAME in fo.list_datasets(), "Dataset not listed"

    print(f"OK — FiftyOne {fo.__version__} on database '{fo.config.database_name}'")

finally:
    # Always clean up, even on failure
    if TEST_NAME in fo.list_datasets():
        fo.delete_dataset(TEST_NAME)
```

---

## Issue Index

| Symptom | Section |
|---------|---------|
| Dataset disappeared after restart | [Dataset Persistence](#issue-dataset-disappeared) |
| App won't open / not connected | [App Connection](#issue-app-wont-open) |
| Changes not saved | [Unsaved Changes](#issue-changes-not-saved) |
| Video not playing / codec error | [Video Codec](#issue-video-codec) |
| Too many open files (macOS) | [Open Files Limit](#issue-too-many-open-files-macos) |
| App not loading in notebook / remote | [Notebook / Remote](#issue-app-not-loading-in-notebook-or-remote) |
| Plots not showing in notebook | [Notebook Plots](#issue-plots-not-appearing-in-notebook) |
| MongoDB connection failure | [MongoDB](#issue-mongodb-connection-error) |
| Operator not found / plugin missing | [Missing Plugin](#issue-operator-not-found) |
| "No executor available" | [Delegated Operators](#issue-no-executor-available) |
| Dataset is read-only | [Read-Only Dataset](#issue-dataset-is-read-only) |
| Slow performance on large datasets | [Performance](#issue-slow-performance) |
| App showing stale / wrong data | [Stale Data](#issue-stale-app-data) |
| Downgrading FiftyOne | [Downgrading](#issue-downgrading-fiftyone) |
| Database version mismatch | [DB Version Mismatch](#issue-database-version-mismatch) |
| Teams / OSS client type mismatch | [Teams vs OSS](#issue-fiftyone-teams-vs-oss-type-mismatch) |

---

## Issue: Dataset Disappeared

**Cause:** Datasets are non-persistent by default and are deleted when Python exits.

**Fix:**
```python
import fiftyone as fo

# Make an existing dataset persistent
dataset = fo.load_dataset("my-dataset")
dataset.persistent = True

# Prevention: always create persistent datasets
dataset = fo.Dataset("my-dataset", persistent=True)
```

> If the dataset is already gone from `fo.list_datasets()`, it cannot be recovered through FiftyOne — re-import from source files.

---

## Issue: App Won't Open

**Cause A — Script exits before the App loads.** Fix: add `session.wait()`.
```python
session = fo.launch_app(dataset)
session.wait()  # keeps the process alive
```

**Cause B — Windows multiprocessing.** Fix: add the `__main__` guard.
```python
if __name__ == "__main__":
    session = fo.launch_app(dataset)
    session.wait()
```

**Cause C — Port already in use.**
```python
session = fo.launch_app(dataset, port=<alternative-port>)  # e.g. 5152, 5153
```

**Cause D — Stale process.**
```bash
pkill -f "fiftyone"
```

---

## Issue: Changes Not Saved

**Fix — sample edits:**
```python
sample["my_field"] = "new_value"
sample.save()  # required
```

**Fix — dataset-level properties:**
```python
dataset.info["description"] = "Updated"
dataset.save()  # required
```

**Fix — bulk updates (no `.save()` needed):**
```python
dataset.set_values("my_field", [v1, v2, ...])
```

---

## Issue: Video Codec

**Cause:** Video codec not supported by the browser's HTML5 player (requires MP4/H.264, WebM, or Ogg).

> ⚠️ Re-encoding **overwrites files on disk**. Show the user the exact paths that will be modified and get explicit confirmation before running.

```python
import fiftyone.utils.video as fouv

# Re-encode all videos in a dataset
fouv.reencode_videos(fo.load_dataset("my-dataset"))

# Or a single file
fouv.reencode_video("/path/to/input.avi", "/path/to/output.mp4")
```

---

## Issue: Too Many Open Files (macOS)

```bash
# Temporary (current session only)
ulimit -n 65536

# Permanent — add to your shell profile and reload it
# bash: ~/.bash_profile or ~/.bashrc
# zsh:  ~/.zshrc
echo "ulimit -n 65536" >> <your-shell-profile> && source <your-shell-profile>
```

---

## Issue: App Not Loading in Notebook or Remote

**Cause A — Remote Jupyter:** localhost URL not reachable from browser.
```python
fo.app_config.proxy_url = "http://your-server:<app-port>/proxy/<app-port>"
session = fo.launch_app(dataset)
```

**Cause B — Google Colab / Databricks:** works out of the box, no proxy needed.

**Cause C — SSH remote:** forward the port locally.
```bash
# Use the same port FiftyOne is listening on (default: 5151)
ssh -L <app-port>:localhost:<app-port> user@remote-server
```

---

## Issue: Plots Not Appearing in Notebook

```bash
pip install plotly
jupyter labextension install jupyterlab-plotly
```

```python
import plotly.offline as pyo
pyo.init_notebook_mode(connected=True)
```

---

## Issue: MongoDB Connection Error

**Symptoms:** `ConnectionFailure`, `ServerSelectionTimeoutError`, hangs on import, port 27017 errors.

**Diagnose:**
```bash
ps aux | grep mongod     # is MongoDB running?
df -h                    # is disk full?
```

**Fix A — Restart FiftyOne's MongoDB:**
```bash
pkill -f "fiftyone.*mongod"   # kill stale process, then re-import fiftyone
```

**Fix B — Free disk space.** MongoDB will not start on a full disk.

**Fix C — Use an external MongoDB instance** (requires user confirmation):
```json
// ~/.fiftyone/config.json
{ "database_uri": "mongodb://localhost:27017" }
```

**Fix D — Reset internal MongoDB (last resort, destroys all datasets):**
> ⚠️ Requires explicit user confirmation.
```bash
ls -la ~/.fiftyone/          # show what will be deleted
rm -rf ~/.fiftyone/var/      # only after user confirms
```

---

## Issue: Operator Not Found

**Diagnose:**
```python
fo.list_plugins()
# Via MCP:
list_plugins(enabled=True)
list_operators(builtin_only=False)
```

**Fix:**
```python
fo.download_plugin("voxel51/fiftyone-plugins", plugin_names=["@voxel51/brain"])
fo.enable_plugin("@voxel51/brain")
# Via MCP:
download_plugin(url_or_repo="voxel51/fiftyone-plugins", plugin_names=["@voxel51/brain"])
enable_plugin(plugin_name="@voxel51/brain")
```

| Operator prefix | Plugin |
|----------------|--------|
| `@voxel51/brain/*` | `@voxel51/brain` |
| `@voxel51/io/*` | `@voxel51/io` |
| `@voxel51/utils/*` | `@voxel51/utils` |
| `@voxel51/evaluation/*` | `@voxel51/evaluation` |
| `@voxel51/zoo/*` | `@voxel51/zoo` |

---

## Issue: No Executor Available

**Cause:** Brain, evaluation, and annotation operators require the FiftyOne App running as executor.

```python
launch_app()              # 1. launch app first
# wait 5-10 seconds
execute_operator(...)     # 2. then run the operator
```

---

## Issue: Dataset is Read-Only

```python
writable = fo.load_dataset("read-only-dataset").clone("my-writable-dataset")
writable.persistent = True
```

---

## Issue: Slow Performance

```python
# Use views, not full dataset iteration
view = dataset.match({"label": "cat"}).take(1000)

# Bulk updates over per-sample saves
dataset.set_values("my_score", values_list)   # fast
# vs: sample["my_score"] = v; sample.save()  # slow

# Add indexes for frequently filtered fields
dataset.create_index("ground_truth.detections.label")
```

---

## Issue: Stale App Data

```python
dataset.reload()
# or
session.dataset = fo.load_dataset("my-dataset")
session.refresh()
```

Browser: `Cmd+Shift+R` (macOS) / `Ctrl+Shift+R` (Windows/Linux).

---

## Issue: Downgrading FiftyOne

```bash
pip install fiftyone==X.Y.Z
python -c "import fiftyone as fo; fo.migrate_database_if_necessary()"
```

> ⚠️ Export important datasets before downgrading.

---

## Issue: Database Version Mismatch

**Symptom:**
```
OSError: You must have fiftyone>=X.Y.Z to migrate from vX.Y.Z to vA.B.C
```

**Cause:** All FiftyOne installs on a machine share the same MongoDB database (`fiftyone` by default). A newer version writes a forward-only version marker that older installs cannot read. Common when a dev virtualenv runs an older version than the system pip install.

**Diagnose:**
```bash
# Current env
python -c "import fiftyone as fo; print(fo.__version__, fo.config.database_name)"

# Check if the database is accessible at all
python -c "
import fiftyone as fo
try:
    print('datasets:', fo.list_datasets())
except Exception as e:
    print('inaccessible:', e)
"

# All Python installs on this machine
which -a python python3 | xargs -I{} sh -c '{} -c "import fiftyone as fo; print(\"{}: \", fo.__version__)" 2>/dev/null'
```

**Fix A — Isolate the environment (recommended, no data loss):**

Give the affected env its own database so it never conflicts with other installs.

```bash
# Find the virtualenv activate script
ACTIVATE=$(python -c "import sys; print(sys.prefix)")/bin/activate
echo $ACTIVATE   # confirm before editing

# Append isolation — pick a name that reflects your project
echo '
# Isolate FiftyOne database from other installations
export FIFTYONE_DATABASE_NAME=fiftyone-<your-project>' >> $ACTIVATE

source $ACTIVATE
python -c "import fiftyone as fo; print(fo.config.database_name)"
```

Then run the Health Check.

> ⚠️ After applying this fix, **restart any running FiftyOne App or Python processes** — env var changes only affect new processes. Check for stale processes: `ps aux | grep fiftyone`. Confirm with user before killing them.

**Fix B — Per-session (no file changes):**
```bash
FIFTYONE_DATABASE_NAME=fiftyone-<your-project> python your_script.py
```

**Fix C — Upgrade to match the database version:**
```bash
pip install "fiftyone>=X.Y.Z"
```

**Fix D — Global config (affects all installs, confirm with user):**
```json
// ~/.fiftyone/config.json
{ "database_name": "fiftyone-<your-project>" }
```

---

## Issue: FiftyOne Teams vs OSS Type Mismatch

**Symptom:**
```
ConnectionError: Cannot connect to database type 'fiftyone' with client type 'fiftyone-teams'
```
(or the inverse)

**Cause:** Teams and OSS clients use incompatible database types and cannot share a database.

**Diagnose:**
```python
import fiftyone as fo
print(fo.__version__)
print(fo.config.database_name)
print(fo.config.database_uri or "(internal MongoDB)")
try:
    fo.list_datasets()
except Exception as e:
    print(e)
```

**Fix — Isolate the OSS environment:**
```bash
ACTIVATE=$(python -c "import sys; print(sys.prefix)")/bin/activate
echo $ACTIVATE   # confirm before editing
echo '
# Isolate FiftyOne database from Teams installation
export FIFTYONE_DATABASE_NAME=fiftyone-<your-project>' >> $ACTIVATE
source $ACTIVATE
```

**Fix — Inspect Teams config if the error is unexpected:**
```bash
cat ~/.fiftyone/config.json 2>/dev/null || echo "(no config)"
python -c "import fiftyone as fo; import json; print(json.dumps(fo.config.serialize(), indent=2))"
```

---

## Adding a New Issue

1. Add a row to the Issue Index
2. Add a `## Issue: <Name>` section with: **Symptom** → **Cause** → **Fix**
3. Keep it self-contained — each section should be readable in isolation

---

## Resources

- [FiftyOne FAQ](https://docs.voxel51.com/faq/index.html)
- [FiftyOne Installation Guide](https://docs.voxel51.com/getting_started/install.html)
- [FiftyOne Discord](https://discord.gg/fiftyone-community)
- [FiftyOne GitHub Issues](https://github.com/voxel51/fiftyone/issues)
