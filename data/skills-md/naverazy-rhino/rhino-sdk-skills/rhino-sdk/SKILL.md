---
name: rhino-sdk
description: "Plan and execute federated analytics workflows with the Rhino Health Python SDK. Use when the user wants to run survival analysis, metrics, data harmonization, model training, or any multi-step SDK workflow. Takes high-level research goals and produces phased execution plans with runnable code. Also handles SDK questions, debugging rhino_health errors, and metric selection. Triggers on: rhino-health, rhino_health, RhinoSession, FCP, federated analytics, OMOP, FHIR, harmonization, or any of the 40+ federated metrics."
metadata:
  author: rhino-health
  version: "0.1.0"
---

# Rhino Health SDK — Workflow Planner & Code Expert

Plan-first skill for the `rhino-health` Python SDK (v2.1.x). Takes high-level research and analytics goals, decomposes them into phased execution plans, and generates complete runnable Python code.

## Context Loading

Before responding, read ALL reference files — planning requires the full SDK picture:

1. **API Reference** — `references/sdk_reference.md`
   Endpoint classes, methods, enums, CreateInput summaries, dataclass fields, import paths.

2. **Patterns & Gotchas** — `references/patterns_and_gotchas.md`
   Auth patterns, resource lookup, metrics execution, filtering, code objects, async, and pitfalls.

3. **Metrics Reference** — `references/metrics_reference.md`
   All 40+ federated metric classes with parameters, import paths, and decision guide.

4. **Example Index** — `references/examples/INDEX.md`
   Mapping of use cases to working example files with key methods and difficulty levels.

For SDK questions that don't require planning, you may selectively load only the relevant files.

## Request Routing

Determine what the user needs and follow the appropriate workflow:

| User intent | Action |
|---|---|
| High-level goal, multi-step workflow, "plan", "design", "how should I approach" | Full planning workflow (Sections 3-6) |
| "Write code", "generate a script", single-task code generation | Code generation with validation (Section 6) |
| "How do I...", SDK concept question | Answer from reference files (Section 9) |
| Error, traceback, "why is this failing" | Error diagnosis (Section 8) |
| "Which metric for...", metric configuration | Metric selection (Section 7) |
| "Show me an example", "sample code" | Example matching from `references/examples/INDEX.md` |

## Planning Process

Follow these four steps for any multi-step goal:

### Step 1: Analyze the Goal

Extract from the user's request:

- **Data**: What data sources? Do datasets already exist, or need ingestion/creation?
- **Analysis**: What computation? Metrics, custom code, harmonization, or a combination?
- **Output**: What does the user want? Numbers, transformed datasets, trained models, exported files?
- **Constraints**: Filters (age > 50, gender = F), specific sites, time ranges, target data models (OMOP/FHIR)?

If any of these are unclear, ask the user before producing the plan.

### Step 2: Select Workflow Templates

Match the goal to one or more composable SDK pipeline templates:

#### Template A: Federated Analytics

Run statistical metrics across one or more sites without moving data.

```
Auth → Project → Datasets → Metric Config → Execute → Results
```

| Step | SDK Method | Notes |
|---|---|---|
| Authenticate | `rh.login()` | Always first |
| Get project | `session.project.get_project_by_name()` | Check for None |
| Get datasets | `project.get_dataset_by_name()` or list all | One per site |
| Configure metric | `Mean(variable=...)`, `Cox(...)`, etc. | Add filters/group_by as needed |
| Execute per-site | `session.dataset.get_dataset_metric(uid, config)` | Single site |
| Execute aggregated | `session.project.aggregate_dataset_metric(uids, config)` | Cross-site, `List[str]` of UIDs |
| Execute joined | `session.project.joined_dataset_metric(config, query, filter)` | Federated join with shared identifiers |

**Use when:** descriptive stats, survival analysis, hypothesis tests, or any metric-based analysis.

#### Template B: Code Object Execution

Run custom containerized or Python code across federated sites.

```
Auth → Project → Data Schema → Code Object Create → Build → Run → Wait → Output Datasets
```

| Step | SDK Method | Notes |
|---|---|---|
| Authenticate | `rh.login()` | |
| Get/create project | `session.project.get_project_by_name()` | |
| Get/create schema | `session.data_schema.create_data_schema()` | Only if new data format |
| Create code object | `session.code_object.create_code_object()` | `GENERALIZED_COMPUTE` or `PYTHON_CODE` |
| Wait for build | `code_object.wait_for_build()` | Only for `GENERALIZED_COMPUTE` |
| Run | `session.code_object.run_code_object()` | `input_dataset_uids=[[uid]]` double-nested |
| Wait for completion | `code_run.wait_for_completion()` | |
| Access outputs | `result.output_dataset_uids.root[0].root[0].root[0]` | Triply nested |

**Use when:** custom computation — train/test splits, feature engineering, model training, any logic that metrics alone cannot express.

#### Template C: Data Harmonization

Transform source data into a target data model (OMOP, FHIR, custom).

```
Auth → Project → Vocabulary → Semantic Mapping → Syntactic Mapping → Config → Run → Output
```

| Step | SDK Method | Notes |
|---|---|---|
| Authenticate | `rh.login()` | |
| Get project | `session.project.get_project_by_name()` | |
| Create semantic mapping | `session.semantic_mapping.create_semantic_mapping()` | Optional; for vocabulary lookups |
| Wait for indexing | `semantic_mapping.wait_for_completion()` | Can be slow (minutes) |
| Create syntactic mapping | `session.syntactic_mapping.create_syntactic_mapping()` | Defines column transformations |
| Generate/set config | `session.syntactic_mapping.generate_config()` | LLM-based auto-generation or manual |
| Run harmonization | `session.syntactic_mapping.run_data_harmonization()` | Preferred path |
| Wait for completion | `code_run.wait_for_completion()` | |
| Access outputs | `result.output_dataset_uids.root[0].root[0].root[0]` | Triply nested |

Key harmonization types: `TransformationType.SPECIFIC_VALUE`, `SOURCE_DATA_VALUE`, `ROW_PYTHON`, `TABLE_PYTHON`, `SEMANTIC_MAPPING`, `VLOOKUP`, `DATE`, `SECURE_UUID`.

Target models: `SyntacticMappingDataModel.OMOP`, `.FHIR`, `.CUSTOM`.

**Use when:** source data needs transformation before analysis — different column names, value encodings, or target standards like OMOP/FHIR.

#### Template D: SQL Data Ingestion

Pull data from an on-prem database into the Rhino platform.

```
Auth → Project → Connection Details → SQL Query → Import as Dataset → Verify
```

| Step | SDK Method | Notes |
|---|---|---|
| Authenticate | `rh.login()` | |
| Get project | `session.project.get_project_by_name()` | |
| Define connection | `ConnectionDetails(server_type=..., server_url=..., ...)` | PostgreSQL, MySQL, etc. |
| Run metrics on query | `session.sql_query.run_sql_query(SQLQueryInput(...))` | Does NOT return raw data |
| Import as dataset | `session.sql_query.import_dataset_from_sql_query(SQLQueryImportInput(...))` | Creates a Dataset from query results |
| Wait | `sql_query.wait_for_completion()` | |

**Use when:** data lives in a relational database and needs to be brought into the platform as a Dataset.

#### Template E: Model Training + Inference

Train a federated model, then run inference on new data. This is Template B applied twice:

1. **Train phase:** Code Object with training logic → produces model artifacts
2. **Inference phase:** `session.code_run.run_inference()` using the trained model

| Step | SDK Method | Notes |
|---|---|---|
| Train (Template B) | `create_code_object` → `run_code_object` → `wait_for_completion` | Full code object lifecycle |
| Run inference | `session.code_run.run_inference(code_run_uid, validation_dataset_uids, ...)` | Uses trained model |
| Get model params | `session.code_run.get_model_params(code_run_uid)` | Download model weights |

**Use when:** federated ML model training and validation.

#### Template F: Multi-Pipeline Composition

Chain 2+ templates when a single template cannot satisfy the goal:

| Goal pattern | Composition |
|---|---|
| Harmonize then analyze | Template C → Template A |
| Ingest from SQL then analyze | Template D → Template A |
| Harmonize then train model | Template C → Template E |
| Ingest, harmonize, analyze, train | Template D → Template C → Template A → Template E |
| Custom preprocessing then analytics | Template B → Template A |

**Chaining rule:** the output datasets of one phase become the input datasets of the next. Use `result.output_dataset_uids.root[0].root[0].root[0]` to extract UIDs and pass them forward.

### Step 3: Compose the Plan

1. **Authentication is always Phase 0** — shared across all phases. Include project and workgroup discovery.
2. **One template per phase** — if the goal requires Templates C → A → B, that is three phases plus Phase 0.
3. **Chain outputs to inputs** — explicitly state which output from Phase N feeds into Phase N+1.
4. **Add checkpoints** — after each phase, include a verification step (print status, check dataset count, verify output exists).
5. **Surface prerequisites** — list what must already exist vs. what will be created.
6. **Note alternatives** — if there are multiple valid approaches, briefly state why you chose one.

### Step 4: Generate Implementation

After presenting the plan, generate the complete runnable code following ALL validation rules in Section 6.

## Plan Output Format

Structure every planning response as:

```
## Goal
[1-2 sentence restatement]

## Prerequisites
- **Must exist:** [project, datasets, schemas, workgroup access]
- **Created by this plan:** [new code objects, schemas, harmonized datasets]

## Plan

### Phase 0: Setup
- Authenticate and discover project/workgroup/datasets
- Checkpoint: print project name and dataset count

### Phase 1: [Name] — Template [X]
- Step 1.1: [description] — `session.X.method()`
- Step 1.2: [description] — `session.Y.method()`
- Checkpoint: [how to verify]

### Phase 2: [Name] — Template [Y]
- Depends on: Phase 1 output datasets
- Step 2.1: ...
- Checkpoint: [how to verify]

## Alternatives Considered
[Other approaches and why this plan is preferred]

## Implementation
[Complete, runnable Python script]
```

## Decision Guidance

When the goal is ambiguous, use this table:

| User signal | Template | Reasoning |
|---|---|---|
| "analyze", "measure", "statistics", "compare" | A (Analytics) | Metric-based, no custom code needed |
| "run code", "custom analysis", "process data", "split", "transform" | B (Code Object) | Needs logic beyond built-in metrics |
| "harmonize", "OMOP", "FHIR", "map columns", "standardize" | C (Harmonization) | Data transformation to target model |
| "SQL", "database", "import from DB", "ingest" | D (SQL Ingestion) | Data lives in a relational database |
| "train model", "predict", "inference", "ML" | E (Model Train) | Federated model training + validation |
| Multiple of the above | F (Composition) | Chain templates in dependency order |

## Validation Checklist

Apply every item to ALL generated code — plans and standalone scripts alike.

### Endpoint Accessors

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

### Environment

- Default `rh.login()` connects to **production**. For dev/QA/staging, pass `rhino_api_url`:
  `rh.login(..., rhino_api_url=ApiEnvironment.DEV1_AWS_URL)`
- Import: `from rhino_health.lib.constants import ApiEnvironment`
- If user mentions dev1/dev2/QA/staging environment, ALWAYS add `rhino_api_url` parameter

### Import Paths

| Wrong | Correct |
|---|---|
| `from rhino_health.metrics import X` | `from rhino_health.lib.metrics import X` |
| `from rhino_health.endpoints.X import Y` | `from rhino_health.lib.endpoints.X.X_dataclass import Y` |

### Metric Calls

- `aggregate_dataset_metric` takes `List[str]` of UIDs: `[str(d.uid) for d in datasets]`
- `get_dataset_metric` takes a single `dataset_uid: str`
- `joined_dataset_metric` takes `query_datasets` and optional `filter_datasets` as `List[str]`
- Metric config objects require `data_column` (not `column` or `field`)
- `FilterVariable` uses keys: `data_column`, `filter_column`, `filter_value`, `filter_type`

### CreateInput Alias Fields

| Field name | Alias (use this) |
|---|---|
| `project_uid` | `project` |
| `workgroup_uid` | `workgroup` |

### Nested Structures & RootModels

- `CodeObjectRunInput.input_dataset_uids` is `List[List[str]]`: `[[uid1, uid2]]`
- `output_dataset_uids` is triply nested RootModel: access via `.root[0].root[0].root[0]`
- `DataSchema.schema_fields` is a `SchemaFields` RootModel: access list via `.root`, names via `.field_names`
- `group_by` format: `{"groupings": [{"data_column": "col"}]}`
- `data_filters` list: `[FilterVariable(data_column="col", filter_column="col", filter_value="val", filter_type=FilterType.EQUALS)]`
- Enum display: use `.value` for clean strings (e.g. `status.value` → `'Approved'`)

### Async Operations

- Call `wait_for_build()` after creating Generalized Compute code objects
- Call `wait_for_completion()` after `run_code_object()`, `run_data_harmonization()`, `run_sql_query()`

### None Checks

Every `get_*_by_name()` call must be followed by a None check:

```python
dataset = project.get_dataset_by_name("Name")
if dataset is None:
    raise ValueError("Dataset not found")
```

### Code Template

Every generated script must follow this structure:

```python
import rhino_health as rh
from getpass import getpass
# ... additional imports ...

# For non-production environments, add rhino_api_url:
# from rhino_health.lib.constants import ApiEnvironment
# session = rh.login(username="my_email@example.com", password=getpass(),
#                    rhino_api_url=ApiEnvironment.DEV1_AWS_URL)

session = rh.login(username="my_email@example.com", password=getpass())

PROJECT_NAME = "My Project"
# ... constants ...

project = session.project.get_project_by_name(PROJECT_NAME)
if project is None:
    raise ValueError(f"Project '{PROJECT_NAME}' not found")

# ... core logic ...
print(result)
```

## Metric Selection Tree

Map natural language to the right metric class:

| User asks about... | Metric class | Category |
|---|---|---|
| Counts, frequencies | `Count` | Basic |
| Averages, means | `Mean` | Basic |
| Spread, variability | `StandardDeviation`, `Variance` | Basic |
| Totals, sums | `Sum` | Basic |
| Percentiles, medians, quartiles | `Percentile`, `NPercentile` | Quantile |
| Survival time, time-to-event | `KaplanMeier` | Survival |
| Hazard ratios, covariates + survival | `Cox` | Survival |
| ROC curves, AUC | `RocAuc` | ROC/AUC |
| ROC with confidence intervals | `RocAucWithCI` | ROC/AUC |
| Correlation between variables | `Pearson`, `Spearman` | Statistics |
| Inter-rater reliability | `ICC` | Statistics |
| Compare two group means | `TTest` | Statistics |
| Compare 3+ group means | `OneWayANOVA` | Statistics |
| Categorical association | `ChiSquare` | Statistics |
| 2x2 contingency table | `TwoByTwoTable` | Epidemiology |
| Odds ratio | `OddsRatio` | Epidemiology |
| Risk ratio / relative risk | `RiskRatio` | Epidemiology |
| Risk difference | `RiskDifference` | Epidemiology |
| Incidence rates | `Incidence` | Epidemiology |

All metrics: `from rhino_health.lib.metrics import ClassName`

### Execution modes

| Scope | Method |
|---|---|
| Single site | `session.dataset.get_dataset_metric(dataset_uid, config)` |
| Aggregated across sites | `session.project.aggregate_dataset_metric(dataset_uids, config)` — `List[str]` UIDs |
| Federated join | `session.project.joined_dataset_metric(config, query_datasets, filter_datasets)` |

### Filtering example

```python
from rhino_health.lib.metrics import Mean, FilterType, FilterVariable

config = Mean(
    variable="Height",
    data_filters=[
        FilterVariable(
            data_column="Gender",
            filter_column="Gender",
            filter_value="Female",
            filter_type=FilterType.EQUALS,
        )
    ],
    group_by={"groupings": ["Gender"]},
)
```

## Error-to-Fix Reference

When the user encounters an error, diagnose using this table:

| Error pattern | Root cause | Fix |
|---|---|---|
| `NotAuthenticatedError` / HTTP 401 | Token expired, wrong creds, or MFA | Re-login; pass `otp_code` if MFA enabled |
| HTTP 401 with correct credentials | Wrong environment URL | Add `rhino_api_url=ApiEnvironment.DEV1_AWS_URL` (or QA/staging). Default is production |
| `AttributeError: 'NoneType'` | `get_*_by_name()` returned None | Add None check after every `get_*_by_name()` |
| `ValidationError` (pydantic) | Wrong field names — alias confusion | Use aliases: `project` not `project_uid`, `workgroup` not `workgroup_uid` |
| `TypeError` in metric config | String where FilterVariable expected | Use `FilterVariable(data_column=..., filter_column=..., filter_value=..., filter_type=...)` |
| `ImportError` / `ModuleNotFoundError` | Wrong import path | `from rhino_health.lib.metrics import X` (NOT `rhino_health.metrics`) |
| `TypeError: aggregate_dataset_metric()` | `List[Dataset]` instead of `List[str]` | Convert: `[str(d.uid) for d in datasets]` |
| `IndexError` on `output_dataset_uids` | Accessing as flat list | Use `.root[0].root[0].root[0]` (triply nested RootModel) |
| `TypeError` / `AttributeError` on `schema_fields` | `SchemaFields` is a RootModel, not a list | Use `schema.schema_fields.root` for the list, `.field_names` for names |
| `TimeoutError` / operation hangs | Default timeout too low | Increase `timeout_seconds` in `wait_for_completion()` |
| `TypeError: input_dataset_uids` | `List[str]` instead of `List[List[str]]` | Must be double-nested: `[[uid1, uid2]]` |
| `KeyError` / None in metric results | Wrong `data_column` name | Verify column name matches dataset schema (case-sensitive) |
| Enum shows full path (e.g. `Status.APPROVED`) | Printing enum object directly | Use `.value` for clean string: `status.value` → `'Approved'` |
| `ValidationError` on enum field (e.g. `indexing_status`) | SDK/API version mismatch — backend added new value | Use `session.get()` raw API escape hatch (§17 in patterns_and_gotchas.md), or `pip install --upgrade rhino-health` |

Diagnostic process: identify exception class → locate failing SDK call → cross-reference correct signature in `references/sdk_reference.md` → check for compound errors.

## Question Routing

For non-planning SDK questions, locate the right context section:

| Question type | Source file | Section |
|---|---|---|
| Authentication, login, MFA | patterns_and_gotchas.md | §1 |
| Finding projects/datasets by name | patterns_and_gotchas.md | §2 |
| Creating/updating resources (upsert) | patterns_and_gotchas.md | §3 |
| Running per-site or aggregated metrics | patterns_and_gotchas.md | §4 |
| Filtering data | patterns_and_gotchas.md | §5 |
| Group-by analysis | patterns_and_gotchas.md | §6 |
| Federated joins | patterns_and_gotchas.md | §7 |
| Code objects (create, build, run) | patterns_and_gotchas.md | §8 |
| Async operations / waiting | patterns_and_gotchas.md | §9 |
| Correct import paths | patterns_and_gotchas.md | §11 |
| Environment URL (dev1, QA, staging) | patterns_and_gotchas.md | §13 |
| RootModel access (SchemaFields, output UIDs) | patterns_and_gotchas.md | §14 |
| Semantic mapping entries / data | patterns_and_gotchas.md | §15 |
| Session persistence / SSO | patterns_and_gotchas.md | §16 |
| SDK crash on valid API data, ValidationError on enum | patterns_and_gotchas.md | §17 |
| Raw API calls, session.get(), bypassing Pydantic | patterns_and_gotchas.md | §17 |
| Vocabularies, vocabulary types | sdk_reference.md | §SemanticMappingEndpoints, §Key Enums |
| Data schema fields, column info | sdk_reference.md | §DataSchema, §SchemaFields |
| Specific endpoint methods | sdk_reference.md | §[EndpointName]Endpoints |
| Enums and constants | sdk_reference.md | §Key Enums |
| API environment URLs | sdk_reference.md | §ApiEnvironment |
| Metric configuration | metrics_reference.md | §[Category] |
| "Which metric for...?" | metrics_reference.md | §Quick Decision Guide |

## Working Examples

Match the user's goal to verified working examples from `references/examples/INDEX.md`:

| Template | Example files |
|---|---|
| A (Analytics) | `eda.py`, `cox.py`, `metrics_examples.py`, `roc_analysis.py`, `aggregate_quantile.py`, `federated_join.py` |
| B (Code Object) | `train_test_split.py`, `runtime_external_files.py` |
| C (Harmonization) | `fhir_pipeline.py` |
| D (SQL Ingestion) | `sql_data_ingestion.py` |
| E (Model Training) | `train_test_split.py` (training portion) |
| F (Composition) | `fhir_pipeline.py` (harmonization + code object + export) |

Read the relevant example file before generating code to follow its proven patterns.
