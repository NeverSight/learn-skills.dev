---
name: rhino-sdk-harmonize
description: "This skill should be used when the user asks about data harmonization using the Rhino Health Python SDK, semantic or syntactic mappings, vocabulary mappings, OMOP, FHIR, data transformation pipelines, DataHarmonizationRunInput, SyntacticMappingDataModel, TransformationType, or converting source data to a target data model."
metadata:
  author: rhino-health
  version: "0.1.0"
---

# Rhino Health SDK — Data Harmonization Guide

Guide users through the data harmonization pipeline in the `rhino-health` Python SDK (v2.1.x): vocabulary setup, semantic mappings, syntactic mappings, configuration, and execution.

## Context Loading

Before responding, read these reference files:

1. **API Reference** — `../../context/sdk_reference.md`
   Focus on §SemanticMappingEndpoints (line ~282) and §SyntacticMappingEndpoints (line ~306) for method signatures, and §CreateInput Summaries for `DataHarmonizationRunInput`.

2. **Patterns & Gotchas** — `../../context/patterns_and_gotchas.md`
   Focus on §9 (Async/Wait) for harmonization wait patterns, §11 (Common Import Paths) for harmonization imports, and §12 (Gotchas) for `output_dataset_uids` triple nesting.

## Pipeline Overview

Data harmonization transforms source data into a target data model (OMOP, FHIR, or custom). The end-to-end flow:

```
1. Create Vocabulary (optional, for semantic lookups)
       ↓
2. Create Semantic Mapping → wait_for_completion()
       ↓
3. Create Syntactic Mapping (references semantic mappings)
       ↓
4. Configure mapping (global_configuration + table_configurations)
   — or use generate_config() for LLM-based auto-generation
       ↓
5. Run harmonization → wait_for_completion()
       ↓
6. Access output datasets (triply nested UIDs)
```

Not every step is required — simple transformations may skip vocabularies and semantic mappings.

## Key Concepts

### Target Data Models

```python
from rhino_health.lib.endpoints.syntactic_mapping.syntactic_mapping_dataclass import SyntacticMappingDataModel

SyntacticMappingDataModel.OMOP    # OMOP Common Data Model
SyntacticMappingDataModel.FHIR    # HL7 FHIR resources
SyntacticMappingDataModel.CUSTOM  # User-defined schema
```

### Transformation Types

Each column mapping uses a `TransformationType` to define how source values become target values:

```python
from rhino_health.lib.endpoints.syntactic_mapping.syntactic_mapping_dataclass import TransformationType
```

| Type | When to use |
|---|---|
| `SPECIFIC_VALUE` | Hardcode a constant value for the target column |
| `SOURCE_DATA_VALUE` | Direct pass-through of the source column value |
| `ROW_PYTHON` | Custom Python code executed per row |
| `TABLE_PYTHON` | Custom Python code executed on the full table |
| `SEMANTIC_MAPPING` | Map values using a semantic mapping vocabulary lookup |
| `VLOOKUP` | Look up values from another data source |
| `CUSTOM_MAPPING` | User-defined mapping logic |
| `SECURE_UUID` | Generate a secure UUID |
| `DATE` | Date format transformation |

### Vocabulary Types

```python
from rhino_health.lib.endpoints.semantic_mapping.semantic_mapping_dataclass import VocabularyType
```

Used when creating semantic mappings to define the vocabulary standard (e.g., ICD-10, SNOMED, LOINC).

### Configuration Structure

Syntactic mappings use a two-level configuration:

- **`global_configuration`** — settings that apply to the entire mapping (target model, global transforms)
- **`table_configurations`** — per-table column mappings, each specifying source column, target column, and transformation type

Use `session.syntactic_mapping.generate_config()` for LLM-based auto-generation of the configuration (async operation).

## Endpoint Methods

### Semantic Mappings

```python
# Create
mapping = session.semantic_mapping.create_semantic_mapping(
    semantic_mapping_create_input=SemanticMappingCreateInput(...),
    return_existing=True,
)
# Wait for indexing (can be slow)
mapping.wait_for_completion(timeout_seconds=6000)

# Lookup
mapping = session.semantic_mapping.get_semantic_mapping_by_name("My Mapping")
```

### Syntactic Mappings

```python
# Create
mapping = session.syntactic_mapping.create_syntactic_mapping(
    syntactic_mapping_input=SyntacticMappingCreateInput(...),
    return_existing=True,
)

# Auto-generate config (async, LLM-based)
response = session.syntactic_mapping.generate_config(mapping.uid)

# Lookup
mapping = session.syntactic_mapping.get_syntactic_mapping_by_name("My Mapping")
```

## Running Harmonization

Two execution paths exist:

### Preferred: via SyntacticMappingEndpoints

```python
from rhino_health.lib.endpoints.syntactic_mapping.syntactic_mapping_dataclass import (
    DataHarmonizationRunInput,
)

run_params = DataHarmonizationRunInput(
    input_dataset_uids=[dataset.uid],              # List[str]
    semantic_mapping_uids_by_vocabularies={},       # dict: vocab_uid → semantic_mapping_uid
    timeout_seconds=600.0,
)

code_run = session.syntactic_mapping.run_data_harmonization(
    syntactic_mapping_or_uid=mapping.uid,
    run_params=run_params,
)
result = code_run.wait_for_completion()
```

### Legacy: via CodeObjectEndpoints

Used in older examples (e.g., `fhir_pipeline.py`). Requires a pre-existing harmonization code object:

```python
code_run = session.code_object.run_data_harmonization(
    code_object_uid=harmonization_code_object_uid,
    run_params=run_params,
)
result = code_run.wait_for_completion()
```

### Accessing Output Datasets

Output UIDs are triply nested — `List[workgroups][slots][dataset_uids]`:

```python
output_uid = result.output_dataset_uids.root[0].root[0].root[0]
```

## Response Format

Structure every response as:

1. **Where in the pipeline** — identify which step the user is at or needs help with
2. **Next step with code** — complete, runnable code for that step with correct imports
3. **Gotchas** — triply nested output UIDs, long `wait_for_completion` timeouts for semantic mapping indexing, correct import paths

## Working Example

Check `../../context/examples/INDEX.md` for matching examples. The key harmonization example is:

- **`fhir_pipeline.py`** — end-to-end: data harmonization, FHIR resource generation, CSV export. Read the full file at `../../context/examples/fhir_pipeline.py` when relevant.
