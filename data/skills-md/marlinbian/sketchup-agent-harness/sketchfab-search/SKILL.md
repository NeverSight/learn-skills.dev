---
name: sketchfab-search
description: Search external 3D model sources when packaged components are insufficient.
---

# Sketchfab Search Skill

## Purpose

Use external model discovery only after the packaged component registry cannot
satisfy the request. External downloads help the designer find assets, but they
are not yet guaranteed automatic SketchUp placement.

## Tool Flow

1. Search the packaged registry first:

   ```python
   search_local_library(query="floor lamp", category="lighting", limit=5)
   ```

2. If no suitable registry component exists, search Sketchfab:

   ```python
   search_sketchfab_models(query="minimalist floor lamp", count=10)
   ```

3. Inspect a selected result:

   ```python
   get_sketchfab_model(model_uid="<uid>")
   ```

4. Download only when the license and format are acceptable:

   ```python
   download_sketchfab_model(model_uid="<uid>", format_hint="obj")
   ```

## Reporting

When using external sources, report:

- model name and source URL when available
- license and attribution requirements when available
- downloaded file path when a download succeeds
- whether manual SketchUp import is still required

## Guardrails

- Do not add downloaded assets to the packaged registry without license review.
- Do not promise automatic placement for arbitrary downloaded models.
- Prefer OBJ or other SketchUp-compatible formats when downloading.
- Keep `design_model.json` as the project truth, not the downloaded asset file.
