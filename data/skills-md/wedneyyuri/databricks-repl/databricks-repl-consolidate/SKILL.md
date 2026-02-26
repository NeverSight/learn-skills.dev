---
name: databricks-repl-consolidate
description: Consolidate a Databricks REPL session into a single, clean Python file. Use this skill when the user wants to finalize, export, or consolidate a REPL session into a committable script. Triggers on requests to consolidate session output, produce a final script from REPL commands, export session to Python, clean up REPL artifacts into production code, or finalize a Databricks workflow.
---

# Session Consolidation

Produce a single, clean `.py` file from a Databricks REPL session by reading `session.json` and the `.cmd.py` files.

## Workflow

1. **Read session.json** — the `steps` array contains the ordered list of steps with status and command file paths.
2. **Read each `.cmd.py` file** — in step order, skipping failed steps (only successful steps survive).
3. **Strip REPL boilerplate** — remove or convert REPL-specific calls (see [Boilerplate Rules](#boilerplate-rules)).
4. **Deduplicate** — if a step was retried after an error, only keep the final successful version.
5. **Resolve imports** — collect all imports from across cells and deduplicate them at the top of the file.
6. **Write the output** — a single `.py` file with a clear structure.

## Output Structure

```python
"""
Consolidated from session: <session_name>
Source: <session_file_path>
Steps: <N> (of <total> attempted)
"""

# --- Dependencies ---
# Requires: scikit-learn, xgboost

# --- Imports ---
import os
import json
from sklearn.ensemble import RandomForestClassifier
# ...

# --- Step 1: load_data ---
df = spark.read.table("catalog.schema.table")
# ...

# --- Step 2: feature_engineering ---
# ...

# --- Step 3: train ---
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
joblib.dump(model, "/Volumes/catalog/schema/vol/model.pkl")
# ...

# --- Step 4: evaluate ---
# ...
```

## Boilerplate Rules

Transform REPL-specific code into clean Python:

| REPL Code | Consolidated Form |
|---|---|
| `%pip install xgboost` | Move to `# Requires: xgboost` in header |
| `sub_llm(prompt, ...)` | Keep as-is (it's business logic) |
| `sub_llm_batch(prompts, ...)` | Keep as-is (it's business logic) |

**Key distinctions:**
- `%pip install` → collect into a `# Requires:` header comment
- `sub_llm()` / `sub_llm_batch()` → keep unchanged, these are meaningful business logic
- `print()` statements used only for REPL feedback → remove
- `print()` statements that display meaningful results → keep

## Deduplication Rules

Sessions often contain retries after errors. When multiple steps share the same tag:

1. Find all steps with the same tag in `session.json`
2. Keep only the last one with `status: "Finished"`
3. Discard earlier failed attempts

When adjacent steps do the same thing (e.g., loading the same table with slight variations), keep only the final version.

## Import Resolution

1. Scan all surviving steps for `import` and `from ... import` statements
2. Deduplicate — same import appearing in multiple steps becomes one line
3. Place all imports at the top of the file, after the docstring and dependencies comment
4. Remove imports that are no longer used after boilerplate stripping

## Before / After Example

### Before (3 separate `.cmd.py` files)

**001_install.cmd.py:**
```python
%pip install scikit-learn pandas
```

**002_load.cmd.py:**
```python
import pandas as pd
df = spark.read.table("catalog.schema.customers").toPandas()
print(f"Loaded {len(df)} rows")
```

**003_train.cmd.py:**
```python
from sklearn.ensemble import RandomForestClassifier
import joblib

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(df[features], df["label"])
joblib.dump(model, "/Volumes/catalog/schema/vol/model.pkl")
print("Training complete")
```

### After (consolidated `.py`)

```python
"""
Consolidated from session: customer-classifier
Source: ./session.json
Steps: 3 (of 3 attempted)
"""

# --- Dependencies ---
# Requires: scikit-learn, pandas

# --- Imports ---
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# --- Step 1: load ---
df = spark.read.table("catalog.schema.customers").toPandas()

# --- Step 2: train ---
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(df[features], df["label"])
joblib.dump(model, "/Volumes/catalog/schema/vol/model.pkl")
```

## Usage

1. Ensure `session.json` has a `steps` array with at least one successful step
2. Read `session.json` to understand the session structure
3. Read each `.cmd.py` file referenced in the steps
4. Apply the boilerplate rules, deduplication, and import resolution
5. Write the consolidated file (default: `<session_name>.py` in the repo root)
6. Review the output for correctness — automated consolidation may miss nuances in variable dependencies across steps
