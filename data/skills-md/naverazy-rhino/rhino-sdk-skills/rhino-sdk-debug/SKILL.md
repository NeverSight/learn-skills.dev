---
name: rhino-sdk-debug
description: "This skill should be used when the user encounters an error or traceback from the Rhino Health Python SDK, needs to debug rhino_health code, sees NotAuthenticatedError, ValidationError, TypeError, ImportError, or any exception mentioning rhino_health, or asks why their SDK code is failing."
metadata:
  author: rhino-health
  version: "0.1.0"
---

# Rhino Health SDK — Error Debugger

Diagnose errors in `rhino-health` Python SDK code (v2.1.x) and provide corrected, runnable fixes.

## Context Loading

Before diagnosing, read these reference files:

1. **Patterns & Gotchas** — `../../context/patterns_and_gotchas.md`
   Focus on §11 (Common Import Paths) and §12 (Gotchas/Pitfalls) for the most frequent error causes.

2. **API Reference** — `../../context/sdk_reference.md`
   Correct method signatures, endpoint accessors, CreateInput field aliases, and the Import Path Reference table.

## Error-to-Fix Reference

Use this table to quickly identify the root cause. Then confirm against the context files before responding.

| Error pattern | Root cause | Fix |
|---|---|---|
| `NotAuthenticatedError` / HTTP 401 | Token expired, wrong credentials, or MFA required | Re-login with `rh.login()`; pass `otp_code` param if MFA is enabled |
| `AttributeError: 'NoneType' has no attribute` | `get_*_by_name()` returned `None` because the resource was not found | Add a None check immediately after every `get_*_by_name()` call |
| `ValidationError` (pydantic) | Wrong field names or types in a CreateInput class — often alias confusion | Use Pydantic alias names: `project` not `project_uid`, `workgroup` not `workgroup_uid`. Check CreateInput summaries in sdk_reference.md |
| `TypeError` in metric configuration | Passed a raw string where a `FilterVariable` dict or metric object is expected | Use `FilterVariable(data_column=..., filter_column=..., filter_value=..., filter_type=FilterType.EQUALS)` |
| `ImportError` / `ModuleNotFoundError` | Wrong import path — SDK uses deep paths that differ from guesses | `from rhino_health.lib.metrics import X` (NOT `rhino_health.metrics`); `from rhino_health.lib.endpoints.X.X_dataclass import Y` (NOT `rhino_health.endpoints.X`) |
| `TypeError: aggregate_dataset_metric()` argument | Passing `List[Dataset]` objects instead of `List[str]` UIDs | Convert: `[str(d.uid) for d in datasets]` |
| `IndexError` on `output_dataset_uids` | Accessing as flat list — structure is triply nested | Use `.root[0].root[0].root[0]` to access the first output dataset UID |
| `TimeoutError` / operation hangs | Default `timeout_seconds` too low for large datasets | Increase `timeout_seconds` in `wait_for_completion()` or `wait_for_build()` |
| `TypeError: input_dataset_uids` | Passing `List[str]` instead of `List[List[str]]` | `CodeObjectRunInput.input_dataset_uids` must be double-nested: `[[uid1, uid2]]` |
| `KeyError` / unexpected `None` in metric results | Wrong `data_column` name or missing column in dataset | Verify column name matches the dataset schema exactly (case-sensitive) |

## Diagnostic Process

When the user provides an error or traceback:

1. **Identify the exception class** — match it to the table above.
2. **Locate the failing line** — find the SDK call that triggered the error.
3. **Cross-reference with context** — check the correct signature/pattern in sdk_reference.md or patterns_and_gotchas.md.
4. **Check for compound errors** — one fix may reveal a second issue (e.g., fixing an import may expose an alias field error).

## Response Format

Structure every response in three parts:

### 1. What went wrong

Identify the specific error and the SDK call that caused it. Quote the relevant line from the traceback.

### 2. Why

Explain the root cause with reference to SDK behavior. For example: "`get_dataset_by_name()` returns `None` when no dataset matches — it does not raise an exception. The subsequent `.uid` access fails because `None` has no `uid` attribute."

### 3. Corrected code

Provide the complete corrected code block with:
- Fixed imports (exact paths from the Import Path Reference table)
- The fix applied with a brief inline comment explaining what changed
- Any defensive checks added (None guards, type conversions)

```python
# WRONG
from rhino_health.metrics import Mean

# CORRECT
from rhino_health.lib.metrics import Mean
```

## Common Multi-Error Patterns

Watch for these combinations that frequently appear together:

- **Import error + alias error**: User copied code from an older example. Fix both the import path and the CreateInput field names.
- **NoneType + no error handling**: User chained calls without checking `get_*_by_name()` returns. Add None checks for every lookup.
- **Metric TypeError + wrong execution method**: User confused `get_dataset_metric` (per-site, single UID) with `aggregate_dataset_metric` (cross-site, list of UIDs).

## Import Path Quick Reference

When the error is an `ImportError`, consult this cheatsheet:

```python
# Metrics (CORRECT)
from rhino_health.lib.metrics import Mean, Count, Cox, KaplanMeier, RocAuc

# Dataclasses (CORRECT pattern)
from rhino_health.lib.endpoints.project.project_dataclass import ProjectCreateInput
from rhino_health.lib.endpoints.dataset.dataset_dataclass import DatasetCreateInput
from rhino_health.lib.endpoints.code_object.code_object_dataclass import CodeObjectCreateInput, CodeObjectRunInput, CodeTypes
from rhino_health.lib.endpoints.syntactic_mapping.syntactic_mapping_dataclass import DataHarmonizationRunInput

# Enums (CORRECT)
from rhino_health.lib.endpoints.endpoint import VersionMode, NameFilterMode
from rhino_health.lib.metrics import FilterType, FilterVariable
```

For the full list, see the Import Path Reference table at the end of `sdk_reference.md`.
