---
name: rhino-sdk-plan
description: "This skill should be used when the user describes a high-level research or analytics goal using the Rhino Health Python SDK, wants to plan a multi-step workflow, says 'plan', 'design a workflow', 'how should I approach', 'what are the steps to', 'architect', 'set up a pipeline', wants to combine analytics with code objects or harmonization, or needs help decomposing a complex federated computing task into ordered SDK operations."
metadata:
  author: rhino-health
  version: "0.1.0"
---

# Rhino Health SDK — Workflow Planner

Decompose high-level research and analytics goals into structured, phased execution plans using the `rhino-health` Python SDK (v2.1.x). Identify which SDK capabilities to compose, order steps by dependency, surface prerequisites, and generate the complete runnable implementation.

## Context Loading

Before planning, read ALL of these reference files — planning requires the full SDK picture:

1. **API Reference** — `../../context/sdk_reference.md`
   Endpoint classes, methods, enums, CreateInput summaries, dataclass fields, import paths.

2. **Patterns & Gotchas** — `../../context/patterns_and_gotchas.md`
   Auth patterns, resource lookup, metrics execution, filtering, code objects, async, and pitfalls.

3. **Metrics Reference** — `../../context/metrics_reference.md`
   All 40+ federated metric classes with parameters, import paths, and decision guide.

4. **Example Index** — `../../context/examples/INDEX.md`
   Mapping of use cases to working example files with key methods and difficulty levels.

## Planning Process

Follow these four steps in order:

### Step 1: Analyze the Goal

Extract from the user's request:

- **Data**: What data sources? Do datasets already exist on the platform, or do they need to be ingested/created?
- **Analysis**: What computation or analytics? Metrics, custom code, harmonization, or a combination?
- **Output**: What does the user want at the end? Numbers, transformed datasets, trained models, exported files?
- **Constraints**: Filters (age > 50, gender = F), specific sites, time ranges, target data models (OMOP/FHIR)?

If any of these are unclear, ask the user before producing the plan.

### Step 2: Select Workflow Templates

Match the goal to one or more of these composable SDK workflow templates:

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

**Use when:** user wants descriptive stats, survival analysis, hypothesis tests, or any metric-based analysis.

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

**Use when:** user needs custom computation — train/test splits, feature engineering, model training, any logic that metrics alone cannot express.

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

**Use when:** source data needs to be transformed before analysis — different column names, value encodings, or target standards like OMOP/FHIR.

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

**Use when:** data lives in a relational database and needs to be brought into the platform as a Dataset before other operations.

#### Template E: Model Training + Inference

Train a federated model, then run inference on new data.

```
Auth → Project → Training Code Object → Train → Wait → Inference → Validate
```

This is Template B applied twice in sequence:

1. **Train phase:** Code Object with training logic → produces model artifacts (stored in the code run)
2. **Inference phase:** `session.code_run.run_inference()` using the trained model on validation datasets

| Step | SDK Method | Notes |
|---|---|---|
| Train (Template B) | `create_code_object` → `run_code_object` → `wait_for_completion` | Full code object lifecycle |
| Run inference | `session.code_run.run_inference(code_run_uid, validation_dataset_uids, ...)` | Uses trained model |
| Get model params | `session.code_run.get_model_params(code_run_uid)` | Download model weights |

**Use when:** user wants to train an ML model across federated sites and validate it.

#### Template F: Multi-Pipeline Composition

Chain 2+ templates when a single template cannot satisfy the goal. Common compositions:

| Goal pattern | Composition |
|---|---|
| Harmonize then analyze | Template C → Template A |
| Ingest from SQL then analyze | Template D → Template A |
| Harmonize then train model | Template C → Template E |
| Ingest, harmonize, analyze, train | Template D → Template C → Template A → Template E |
| Custom preprocessing then analytics | Template B → Template A |

**Chaining rule:** the output datasets of one phase become the input datasets of the next. Use `result.output_dataset_uids.root[0].root[0].root[0]` to extract UIDs and pass them forward.

### Step 3: Compose the Plan

Build a phased plan following these rules:

1. **Authentication is always Phase 0** — shared across all subsequent phases. Include project and workgroup discovery here.
2. **One template per phase** — each phase maps to one template. If the goal requires Templates C → A → B, that is three phases plus Phase 0.
3. **Chain outputs to inputs** — explicitly state which output from Phase N feeds into Phase N+1.
4. **Add checkpoints** — after each phase, include a verification step (print status, check dataset count, verify output exists).
5. **Surface prerequisites** — if the plan assumes a project, datasets, or schemas exist, list them in the Prerequisites section. Distinguish between "must already exist" and "will be created by this plan".
6. **Note alternatives** — if there are multiple valid approaches (per-site vs aggregated, PYTHON_CODE vs GENERALIZED_COMPUTE), briefly state why you chose one.

### Step 4: Generate Implementation

After presenting the plan, generate the complete runnable code:

- Follow ALL rules from the `write` skill's validation checklist: correct endpoint accessors, import paths, `List[str]` for UIDs, None checks, double-nested `input_dataset_uids`, triply-nested `output_dataset_uids`.
- Produce a **single script** with clear phase-separator comments (`# === Phase 1: ... ===`).
- For very large plans (4+ phases), offer to split into separate scripts per phase.
- Use named constants for all configurable values (project names, UIDs, column names, thresholds) at the top of the script.
- Include the authentication block only once at the top.

## Plan Output Format

Structure every response as:

```
## Goal
[1-2 sentence restatement of what the user wants to achieve]

## Prerequisites
- **Must exist:** [project, datasets, schemas, workgroup access, etc.]
- **Created by this plan:** [new code objects, new schemas, harmonized datasets, etc.]

## Plan

### Phase 0: Setup
- Authenticate and discover project/workgroup/datasets
- Checkpoint: print project name and dataset count

### Phase 1: [Name] — [Template X]
- Step 1.1: [description] — `session.X.method()`
- Step 1.2: [description] — `session.Y.method()`
- Checkpoint: [how to verify]

### Phase 2: [Name] — [Template Y]
- Depends on: Phase 1 output datasets
- Step 2.1: ...
- Checkpoint: [how to verify]

## Alternatives Considered
[Other approaches and why this plan is preferred]

## Implementation
[Complete, runnable Python script]
```

## Decision Guidance

Use this table when the goal is ambiguous:

| User signal | Template | Reasoning |
|---|---|---|
| "analyze", "measure", "statistics", "compare" | A (Analytics) | Metric-based, no custom code needed |
| "run code", "custom analysis", "process data", "split", "transform" | B (Code Object) | Needs logic beyond built-in metrics |
| "harmonize", "OMOP", "FHIR", "map columns", "standardize" | C (Harmonization) | Data transformation to target model |
| "SQL", "database", "import from DB", "ingest" | D (SQL Ingestion) | Data lives in a relational database |
| "train model", "predict", "inference", "ML", "machine learning" | E (Model Train) | Federated model training + validation |
| Multiple of the above | F (Composition) | Chain templates in dependency order |

## Working Examples

Check `../../context/examples/INDEX.md` for working examples that demonstrate individual templates:

| Template | Example files |
|---|---|
| A (Analytics) | `eda.py`, `cox.py`, `metrics_examples.py`, `roc_analysis.py`, `aggregate_quantile.py`, `federated_join.py` |
| B (Code Object) | `train_test_split.py`, `runtime_external_files.py` |
| C (Harmonization) | `fhir_pipeline.py` |
| D (SQL Ingestion) | `sql_data_ingestion.py` |
| E (Model Training) | `train_test_split.py` (training portion) |
| F (Composition) | `fhir_pipeline.py` (harmonization + code object + export) |

Read the relevant example files before generating implementation code to follow their proven patterns.
