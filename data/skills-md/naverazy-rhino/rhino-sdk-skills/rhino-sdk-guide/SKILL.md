---
name: rhino-sdk-guide
description: "This skill should be used when the user asks about the Rhino Health Python SDK API, asks 'how do I...' questions about rhino-health, needs to understand SDK concepts like endpoints, sessions, metrics, or dataclasses, or mentions rhino_health, RhinoSession, FCP, federated analytics, or rhino-health SDK."
metadata:
  author: rhino-health
  version: "0.1.0"
---

# Rhino Health SDK — Guide

Expert guidance for the `rhino-health` Python SDK (v2.1.x). Answer questions about API surface, patterns, imports, and best practices.

## Context Loading

Before answering, read these reference files:

1. **API Reference** — `../../context/sdk_reference.md`
   Full API surface: authentication, all endpoint classes and their methods, enums, CreateInput summaries, dataclass fields, and import paths.

2. **Patterns & Gotchas** — `../../context/patterns_and_gotchas.md`
   Practical patterns (auth, resource lookup, metrics, filtering, code objects, async) and known pitfalls.

Load both files in full before responding. If the question involves metrics or analytics, also load:

3. **Metrics Reference** — `../../context/metrics_reference.md`
   All 40+ federated metric classes with parameters, import paths, and a decision guide.

## Response Rules

### Import Paths

Always include the exact import statement. The SDK uses deep import paths that differ from what most users guess:

- Metrics: `from rhino_health.lib.metrics import ClassName` (NOT `from rhino_health.metrics`)
- Dataclasses: `from rhino_health.lib.endpoints.<endpoint>.<endpoint>_dataclass import ClassName`
- Enums: `from rhino_health.lib.endpoints.<endpoint>.<endpoint>_dataclass import EnumName`
- Filters: `from rhino_health.lib.metrics import FilterType, FilterVariable, FilterBetweenRange`

Consult the "Import Path Reference" table in `sdk_reference.md` for the authoritative list.

### Code Snippets

Always show complete, runnable snippets — include the import block and authentication, not just the API call. Use `getpass()` for passwords (never hardcode). Example structure:

```python
import rhino_health as rh
from getpass import getpass

session = rh.login(username="my_email@example.com", password=getpass())
# ... SDK calls ...
```

### Resource Lookup

Prefer `get_*_by_name()` for discovery. Always warn that these methods return `None` (not an exception) when the resource is not found:

```python
project = session.project.get_project_by_name("My Project")
if project is None:
    raise ValueError("Project not found")
```

### Upsert and Versioning

When the question involves creating or updating resources, mention `return_existing`, `add_version_if_exists`, `VersionMode`, and `NameFilterMode` from patterns_and_gotchas.md section 3.

### Gotchas

Flag relevant pitfalls from patterns_and_gotchas.md section 12 whenever they apply:

- `aggregate_dataset_metric` takes `List[str]` of UIDs, not `List[Dataset]`
- `CodeObjectRunInput.input_dataset_uids` is `List[List[str]]` (double nested)
- `output_dataset_uids` is triply nested: `.root[0].root[0].root[0]`
- Alias fields in CreateInput: `project_uid` aliased as `'project'`, `workgroup_uid` as `'workgroup'`
- `get_*_by_name` returns `None`, not an exception

## Response Format

Structure every response as:

1. **Brief answer** — 1-3 sentences explaining the concept or approach
2. **Code snippet** — complete, runnable example with correct imports
3. **Gotchas** (if any) — relevant pitfalls from the list above
4. **See also** — point to a matching example from the examples index if one exists

## Question Routing

Use this table to locate the right context section for common question types:

| Question type | Primary source | Section |
|---|---|---|
| Authentication, login, MFA | patterns_and_gotchas.md | §1 |
| Finding projects/datasets by name | patterns_and_gotchas.md | §2 |
| Creating/updating resources (upsert) | patterns_and_gotchas.md | §3 |
| Running per-site or aggregated metrics | patterns_and_gotchas.md | §4 |
| Filtering data | patterns_and_gotchas.md | §5 |
| Group-by analysis | patterns_and_gotchas.md | §6 |
| Federated joins across datasets | patterns_and_gotchas.md | §7 |
| Code objects (create, build, run) | patterns_and_gotchas.md | §8 |
| Waiting for async operations | patterns_and_gotchas.md | §9 |
| External storage / S3 files | patterns_and_gotchas.md | §10 |
| Correct import paths | patterns_and_gotchas.md | §11, sdk_reference.md §Import Path Reference |
| Specific endpoint methods | sdk_reference.md | §[EndpointName]Endpoints |
| Enums and constants | sdk_reference.md | §Key Enums |
| CreateInput field names | sdk_reference.md | §CreateInput Summaries |
| Metric configuration | metrics_reference.md | §[Category] |
| "Which metric for...?" | metrics_reference.md | §Quick Decision Guide |

## Working Examples

Check `../../context/examples/INDEX.md` for a matching working example. When one exists, reference it by filename and describe which pattern it demonstrates. Read the example file to verify details before citing it.
