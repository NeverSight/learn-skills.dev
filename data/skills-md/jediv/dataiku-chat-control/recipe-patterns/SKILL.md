---
name: recipe-patterns
description: "Use when creating, configuring, or running any Dataiku recipe (prepare, join, group, sync, python) including data cleaning, formulas, and GREL"
---

# Dataiku Recipe Patterns

Reference patterns for creating different recipe types via the Python API.

## Before Writing Code

**MANDATORY**: Read the relevant reference file before writing any recipe code.

- GREL formulas → read [references/grel-functions.md](references/grel-functions.md) first
- Prepare steps → read [references/processors.md](references/processors.md) first
- Joins → read [references/join-recipe.md](references/join-recipe.md) first
- Grouping → read [references/group-recipe.md](references/group-recipe.md) first
- Python recipes → read [references/python-recipe.md](references/python-recipe.md) first
- Sync recipes → read [references/sync-recipe.md](references/sync-recipe.md) first
- Date handling → read [references/date-operations.md](references/date-operations.md) first
- Pitfalls index → [references/pitfalls.md](references/pitfalls.md) (recipe-type reference files also have a Pitfalls section at the top)

**Do NOT rely on general knowledge for GREL functions or API methods.** Dataiku GREL differs from OpenRefine GREL and other variants. Always verify function names against the reference.

## Recipe Type Decision Table

| Recipe Type | Use When | Key Method |
|-------------|----------|------------|
| **Prepare** | Column transforms, filtering, formula columns, renaming, data cleaning | `project.new_recipe("prepare", ...)` |
| **Join** | Combining datasets on key columns (LEFT, INNER, RIGHT, OUTER) | `project.new_recipe("join", ...)` |
| **Group** | Aggregations: sum, count, avg, min, max, stddev, etc. | `project.new_recipe("grouping", ...)` |
| **Sync** | Copying data between connections (e.g., to a data warehouse) | `project.new_recipe("sync", ...)` |
| **Python** | Custom transformations not possible with visual recipes | `project.new_recipe("python", ...)` |

## Universal Builder Pattern

Every recipe follows the same create-configure-run lifecycle:

```python
# 1. Create via builder
builder = project.new_recipe("<type>", "<recipe_name>")
builder.with_input("<input_dataset>")
builder.with_new_output("<output_dataset>", "<connection>")  # creates output dataset
recipe = builder.create()

# 2. Configure settings
settings = recipe.get_settings()
# ... recipe-specific configuration ...
settings.save()

# 3. Apply schema updates
schema_updates = recipe.compute_schema_updates()
if schema_updates.any_action_required():
    schema_updates.apply()

# 4. Run and check
job = recipe.run(no_fail=True)
state = job.get_status()["baseStatus"]["state"]  # "DONE" or "FAILED"
```

## After Running Any Recipe

**Always sample the output and verify the result before reporting success.** Silent data issues (wrong values, all nulls, unexpected types) are common.

```python
from helpers.export import sample
rows = sample(client, "PROJECT_KEY", "output_dataset", 5)
for r in rows:
    print(r)
```

## Always Remember

1. Call `settings.save()` after configuration changes
2. Call `compute_schema_updates().apply()` for visual recipes
3. Call `recipe.run(no_fail=True)` to execute (already waits for completion)
4. Check `job.get_status()["baseStatus"]["state"]` for `"DONE"` or `"FAILED"`
5. **Sample and verify the output data** before reporting success

## Tested Patterns

Copy-paste patterns that have been validated against a live Dataiku instance:

- [patterns/bin-numeric-column.py](references/patterns/bin-numeric-column.py) — Bin a string numeric column into ranges
- [patterns/calculated-columns.py](references/patterns/calculated-columns.py) — Common GREL formula patterns
- [patterns/filter-and-clean.py](references/patterns/filter-and-clean.py) — Data cleaning pipeline

## Detailed References

**Recipe types:**
- [references/prepare-recipe.md](references/prepare-recipe.md) — Prepare recipe builder, `add_processor_step()` API
- [references/join-recipe.md](references/join-recipe.md) — Join configuration, multi-table joins, column selection
- [references/group-recipe.md](references/group-recipe.md) — Aggregation flags, output naming, type compatibility
- [references/sync-recipe.md](references/sync-recipe.md) — Sync recipe pattern
- [references/python-recipe.md](references/python-recipe.md) — Python recipe with `set_code`

**Data preparation:**
- [references/processors.md](references/processors.md) — All processor types with parameters and complete example
- [references/grel-functions.md](references/grel-functions.md) — Full GREL function table and formula syntax
- [references/date-operations.md](references/date-operations.md) — DateParser, DateFormatter, datePart examples

**Troubleshooting:**
- [references/pitfalls.md](references/pitfalls.md) — Index of all pitfalls (details are inline in each reference file)
