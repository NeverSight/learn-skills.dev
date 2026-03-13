---
name: data-catalog
description: "Use when working with data collections, dataset metadata, tags, meanings, or AI-generated descriptions"
---

# Data Catalog Patterns

Reference patterns for managing the Dataiku data catalog via the Python API.

## Key Concepts

| Concept | What it is | Scope |
|---------|-----------|-------|
| **Data Collection** | A curated group of datasets, visible across projects | Instance-level (`client`) |
| **Metadata** | Label, description, tags, checklists, custom key-value pairs | Per dataset or project |
| **Meaning** | A semantic type for columns (e.g., "Email", "Country Code") | Instance-level (`client`) |
| **Tags** | Freeform labels on datasets or projects | Per dataset or project |

## Data Collections

### List Collections
```python
collections = client.list_data_collections(as_type="dict")
for c in collections:
    print(f"{c['displayName']} ({c['id']}) — {c['itemCount']} items")
```

### Create a Collection
```python
dc = client.create_data_collection(
    displayName="Customer Data",
    description="All customer-related datasets",
    tags=["customers", "production"]
)
```

### Add Datasets to a Collection
```python
dc = client.get_data_collection("collection_id")

# Add by dataset handle
ds = project.get_dataset("MY_DATASET")
dc.add_object(ds)

# Add by dict (for cross-project datasets)
dc.add_object({"type": "DATASET", "projectKey": "PROJECT_A", "id": "DATASET_NAME"})
```

### List and Remove Objects
```python
dc = client.get_data_collection("collection_id")
objects = dc.list_objects()
for obj in objects:
    raw = obj.get_raw()
    print(f"  {raw['projectKey']}.{raw['id']}")

    # Get as a dataset handle
    ds = obj.get_as_dataset()

    # Remove from collection
    obj.remove()
```

### Update Collection Settings
```python
dc = client.get_data_collection("collection_id")
settings = dc.get_settings()
settings.display_name = "Renamed Collection"
settings.description = "Updated description"
settings.tags = ["new-tag", "production"]
settings.save()
```

## Dataset Metadata

### Get and Set Metadata
```python
ds = project.get_dataset("MY_DATASET")
metadata = ds.get_metadata()

# Metadata structure:
# {
#   "label": "...",
#   "description": "...",
#   "tags": ["tag1", "tag2"],
#   "checklists": {"checklists": [...]},
#   "custom": {"kv": {"key1": "value1"}}
# }

metadata["tags"] = ["cleaned", "production"]
metadata["custom"]["kv"]["owner"] = "data-team"
ds.set_metadata(metadata)
```

### AI-Generated Descriptions
```python
# Generate descriptions for dataset and columns (requires AI Services enabled)
result = ds.generate_ai_description(language="english", save_description=True)
```

> Rate-limited: 1000 requests/day, then throttled to ~60s per call.

## Meanings (Semantic Column Types)

### List and Create Meanings
```python
# List existing meanings
meanings = client.list_meanings()

# Create a values-list meaning
client.create_meaning(
    id="country_code",
    label="Country Code",
    type="VALUES_LIST",
    values=["US", "UK", "FR", "DE", "JP"],
    normalizationMode="EXACT",
    detectable=True
)

# Create a pattern-based meaning
client.create_meaning(
    id="email_address",
    label="Email Address",
    type="PATTERN",
    pattern=r"^[\w.-]+@[\w.-]+\.\w+$",
    detectable=True
)
```

### Update a Meaning
```python
meaning = client.get_meaning("country_code")
definition = meaning.get_definition()
definition["entries"].append({"value": "CA"})
meaning.set_definition(definition)
```

## Catalog Indexing

Trigger re-indexing of connections so new tables appear in the catalog:
```python
# Index specific connections
client.catalog_index_connections(connection_names=["my_snowflake", "my_postgres"])

# Index all connections
client.catalog_index_connections(all_connections=True)
```

## Detailed References

- [references/data-collections.md](references/data-collections.md) — Permissions, completeness checks, cross-project patterns
- [references/metadata-and-tags.md](references/metadata-and-tags.md) — Full metadata structure, project tags, custom metadata
- [references/meanings.md](references/meanings.md) — All meaning types, normalization modes, detectable meanings
