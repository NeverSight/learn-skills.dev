---
name: rhino-sdk-write
description: "This skill should be used when the user wants to write code using the Rhino Health Python SDK, generate a script, create a workflow, implement federated analytics, run metrics across sites, or is writing Python that imports rhino_health."
metadata:
  author: rhino-health
  version: "0.1.0"
---

# Rhino Health SDK — Code Generator

Generate production-ready `rhino-health` Python SDK code from natural language descriptions.

## Context Loading

Before generating code, read all of these reference files:

1. **API Reference** — `../../context/sdk_reference.md`
   Endpoint classes, methods, enums, CreateInput summaries, dataclass fields, import paths.

2. **Patterns & Gotchas** — `../../context/patterns_and_gotchas.md`
   Auth patterns, resource lookup, metrics execution, filtering, code objects, async, and pitfalls.

3. **Metrics Reference** — `../../context/metrics_reference.md`
   All 40+ federated metrics with parameters, import paths, and decision guide.

4. **Example Index** — `../../context/examples/INDEX.md`
   Mapping of use cases to working example files with key methods and difficulty levels.

## Example Matching

After loading context, check the example index for a matching use case. If one exists, read the full example file from `../../context/examples/<filename>` and follow its patterns. The examples are verified working code from the official Rhino GitHub repository.

## Code Template

Every generated script must follow this structure:

```python
# --- Imports ---
import rhino_health as rh
from getpass import getpass
# ... additional imports (metrics, dataclasses, enums) ...

# --- Authentication ---
session = rh.login(username="my_email@example.com", password=getpass())

# --- Configuration ---
PROJECT_NAME = "My Project"
DATASET_UIDS = ["uid-1", "uid-2"]  # Replace with actual UIDs

# --- Resource Lookup ---
project = session.project.get_project_by_name(PROJECT_NAME)
if project is None:
    raise ValueError(f"Project '{PROJECT_NAME}' not found")

# --- Core Logic ---
# ... SDK calls ...

# --- Result Handling ---
print(result)
```

### Template Rules

- **Authentication**: Always use `getpass()`. Never hardcode passwords. Support MFA with `otp_code` parameter.
- **Imports**: Place all imports at the top. Use exact paths from the Import Path Reference table in `sdk_reference.md`.
- **Resource lookup**: Use `get_*_by_name()` for human-friendly lookups. Always check for `None` returns.
- **Constants**: Define project names, UIDs, and configuration values as named constants near the top.
- **Type hints**: Add type hints to function signatures when generating functions or classes.

## Validation Checklist

Run through every item before returning generated code. Flag violations and fix them.

### Endpoint Accessors

Verify the correct accessor is used for each operation:

| Operation | Correct accessor |
|---|---|
| Project-level operations, aggregate/joined metrics | `session.project` |
| Dataset-level operations, per-site metrics | `session.dataset` |
| Code objects, builds, runs, harmonization | `session.code_object` |
| Run status, inference results | `session.code_run` |
| SQL queries | `session.sql_query` |
| Semantic mappings, vocabularies | `session.semantic_mapping` |
| Syntactic mappings, harmonization config | `session.syntactic_mapping` |
| Data schemas | `session.data_schema` |

### Import Paths

Verify every import against the Import Path Reference in `sdk_reference.md`. Common mistakes:

| Wrong | Correct |
|---|---|
| `from rhino_health.metrics import X` | `from rhino_health.lib.metrics import X` |
| `from rhino_health.endpoints.X import Y` | `from rhino_health.lib.endpoints.X.X_dataclass import Y` |

### Metric Calls

- `aggregate_dataset_metric` takes `List[str]` of UIDs: `[str(d.uid) for d in datasets]`
- `get_dataset_metric` takes a single `dataset_uid: str`
- `joined_dataset_metric` takes `query_datasets` and optional `filter_datasets` as `List[str]`
- Metric configuration objects require `data_column` (not `column` or `field`)
- `FilterVariable` dicts use keys: `data_column`, `filter_column`, `filter_value`, `filter_type`

### CreateInput Alias Fields

Several CreateInput classes use Pydantic aliases. Pass the alias name, not the field name:

| Field name | Alias (use this) |
|---|---|
| `project_uid` | `project` |
| `workgroup_uid` | `workgroup` |

### Nested Structures

- `CodeObjectRunInput.input_dataset_uids` is `List[List[str]]`: `[[uid1, uid2]]`
- `output_dataset_uids` is triply nested: access via `.root[0].root[0].root[0]`
- `group_by` parameter format: `{"groupings": [{"data_column": "col"}]}`
- `data_filters` list: `[FilterVariable(data_column="col", filter_column="col", filter_value="val", filter_type=FilterType.EQUALS)]`

### Async Operations

- Call `wait_for_build()` after creating Generalized Compute code objects
- Call `wait_for_completion()` after `run_code_object()`, `run_data_harmonization()`, and `run_sql_query()`
- Both methods block until the operation finishes or times out

### None Checks

Every `get_*_by_name()` call must be followed by a None check:

```python
dataset = project.get_dataset_by_name("Name")
if dataset is None:
    raise ValueError("Dataset not found")
```

## Output Format

Return a single, complete, runnable `.py` script. Include:

- All necessary imports at the top
- Authentication block
- Constants for configurable values (project names, UIDs, column names)
- Inline comments explaining non-obvious SDK behavior (e.g., why UIDs are stringified, why None-checks are needed)
- A brief header comment describing what the script does

Do not split the code across multiple blocks. The user should be able to copy the entire output into a `.py` file and run it (after replacing placeholder values).

## Additional Guidance

### Choosing Between Per-Site, Aggregated, and Joined Metrics

Refer to patterns_and_gotchas.md section 4 for the decision:

- **Per-site** (`get_dataset_metric`): results from one dataset/site
- **Aggregated** (`aggregate_dataset_metric`): combined results across multiple datasets
- **Federated join** (`joined_dataset_metric`): SQL-like join across distributed datasets

### Choosing the Right Metric

Consult the Quick Decision Guide in metrics_reference.md:

- "How many..." -> `Count`
- "Average/mean..." -> `Mean`
- "Survival time..." -> `KaplanMeier` or `Cox`
- "Correlation..." -> `Pearson`, `Spearman`, `ICC`
- "Compare groups..." -> `TTest`, `OneWayANOVA`, `ChiSquare`
- "Risk/odds..." -> `TwoByTwoTable`, `OddsRatio`, `RiskRatio`
- "ROC curve..." -> `RocAuc`, `RocAucWithCI`
