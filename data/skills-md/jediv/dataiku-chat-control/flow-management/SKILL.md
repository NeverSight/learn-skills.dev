---
name: flow-management
description: "Use when building datasets, running multi-step pipelines, managing dependencies, or orchestrating recipe execution order"
---

# Flow Management Patterns

Reference patterns for building and orchestrating Dataiku flows via the Python API.

## When to Use This Skill

- Building datasets that depend on upstream datasets
- Running multiple recipes in the correct order
- Creating multi-step pipelines (e.g., aggregate then join then train)
- Checking job status and handling failures mid-pipeline

## Build a Single Dataset

```python
recipe = project.get_recipe("my_recipe")
job = recipe.run(job_type='NON_RECURSIVE_FORCED_BUILD', partitions=None, wait=True, no_fail=False)
state = job.get_status()["baseStatus"]["state"]  # "DONE" or "FAILED"
```

> `recipe.run()` already waits for completion. Use `no_fail=True` to prevent exceptions on failure.

Note: `job_type` options are `NON_RECURSIVE_FORCED_BUILD` (default), `RECURSIVE_BUILD`, `RECURSIVE_FORCED_BUILD`.

## Build Multiple Datasets in Dependency Order

When downstream datasets depend on upstream ones, build them sequentially:

```python
def build_recipe(project, recipe_name):
    """Build a recipe and return success status."""
    print(f"Building {recipe_name}...")
    recipe = project.get_recipe(recipe_name)
    job = recipe.run(no_fail=True)
    status = job.get_status()
    state = status.get("baseStatus", {}).get("state")

    if state == "DONE":
        print(f"  {recipe_name}: success")
        return True
    else:
        # Extract error details
        activities = status.get("baseStatus", {}).get("activities", {})
        for name, info in activities.items():
            if info.get("firstFailure"):
                print(f"  {recipe_name} error: {info['firstFailure'].get('message')}")
        return False


# Build in dependency order: upstream first, then downstream
pipeline = [
    "group_LAB_RESULTS_AGG",       # Step 1: aggregate
    "group_CLINICAL_NOTES_AGG",    # Step 2: aggregate (independent of step 1)
    "join_ML_TRAINING_DATA",       # Step 3: join (depends on steps 1 & 2)
]

for recipe_name in pipeline:
    success = build_recipe(project, recipe_name)
    if not success:
        print(f"Pipeline failed at {recipe_name}. Fix and retry.")
        break
```

## Build Independent Recipes in Parallel

For recipes with no dependency between them, you can build the output datasets directly:

```python
# These two aggregations are independent — build them before the join
ds1 = project.get_dataset("LAB_RESULTS_AGG")
ds2 = project.get_dataset("CLINICAL_NOTES_AGG")

# Build both (sequentially via API, but could overlap in Dataiku)
job1 = project.get_recipe("group_LAB_RESULTS_AGG").run(no_fail=True)
job2 = project.get_recipe("group_CLINICAL_NOTES_AGG").run(no_fail=True)

# Then build the dependent join
job3 = project.get_recipe("join_ML_TRAINING_DATA").run(no_fail=True)
```

## Check What Exists Before Creating

Before creating recipes or datasets, check if they already exist to make scripts idempotent:

```python
existing_datasets = [d.get("name") for d in project.list_datasets()]
existing_recipes = [r.get("name") for r in project.list_recipes()]

if "MY_OUTPUT" not in existing_datasets:
    # Create the dataset...
    pass

if "my_recipe" not in existing_recipes:
    # Create the recipe...
    pass
```

## Verify Pipeline Results

After building a pipeline, verify the final output:

```python
ds = project.get_dataset("ML_TRAINING_DATA")
schema = ds.get_settings().get_raw().get("schema", {}).get("columns", [])

print(f"Output has {len(schema)} columns:")
for col in schema:
    print(f"  - {col['name']} ({col.get('type', 'unknown')})")
```

## Common Pipeline Patterns

| Pattern | Steps | Key Concern |
|---------|-------|-------------|
| **Aggregate + Join** | Group inputs → Join aggregated outputs | Build aggregations before the join |
| **Clean + Transform** | Prepare recipe → Group/Join | Schema updates after each step |
| **ETL to Warehouse** | Prepare → Sync to SQL connection | Set SQL schema before sync |
| **ML Pipeline** | Prep → Aggregate → Join → Train | Full dependency chain, verify schema at each step |

## Handling Failures Mid-Pipeline

```python
for recipe_name in pipeline:
    success = build_recipe(project, recipe_name)
    if not success:
        # Get detailed error info
        jobs = project.list_jobs()
        job = project.get_job(jobs[0]['def']['id'])
        print(job.get_log()[-2000:])  # Last 2000 chars of log
        break
```

See [skills/troubleshooting/](../troubleshooting/) for detailed error diagnosis patterns.

## Schema Propagation

When an upstream schema changes, propagate it through the flow:

```python
flow = project.get_flow()
propagation = flow.new_schema_propagation("source_dataset")
future = propagation.start()
future.wait_for_result()
```

For more control, use the builder options:

```python
propagation.set_auto_rebuild(True)
propagation.stop_at("recipe_name")
propagation.mark_recipe_as_ok("recipe_name")
```

## Build Datasets via Project API

For more control than `recipe.run()`, use the project-level job builder:

```python
job = project.new_job('RECURSIVE_FORCED_BUILD')
job.with_output('dataset_name', object_type='DATASET')
result = job.start_and_wait(no_fail=True)
```

This supports building multiple outputs in one job:

```python
job = project.new_job('NON_RECURSIVE_FORCED_BUILD')
job.with_output('dataset_1', object_type='DATASET')
job.with_output('dataset_2', object_type='DATASET')
job.start_and_wait()
```

## Detailed References

- [references/build-strategies.md](references/build-strategies.md) — Dependency ordering, idempotent builds, dataset status checks

## Related Skills

- [skills/recipe-patterns/](../recipe-patterns/) — How to create and configure individual recipes
- [skills/dataset-management/](../dataset-management/) — How to create and manage datasets
- [skills/troubleshooting/](../troubleshooting/) — How to debug failed builds
