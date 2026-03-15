---
name: render-json-ui
description: Render JSON artifacts into readable UI with an inspect-first, facts-first workflow. Use when Codex needs to turn JSON files, JSON-producing shell commands, CLI output artifacts, or unknown structured payloads into a declarative UI spec that can be rendered natively by the harness or through a terminal-native reference renderer, including cases with repeated child records encoded as aligned arrays.
---

# Render JSON UI

Turn unknown JSON into a readable presentation without assuming domain knowledge or a browser surface. Inspect shape first, emit structural evidence, and let the LLM derive a declarative UI spec from that evidence.

## Quick Start

1. Identify the input.
2. If needed, run the shell command that generates or refreshes the JSON artifact.
3. Run `scripts/profile_json.py <path>` to classify the payload and extract structural evidence.
4. Build a declarative UI spec using `references/ui-schema.md`.
5. Render that spec natively in the harness, or through the terminal reference renderer.

## Workflow

### 1. Locate the JSON artifact

Prefer explicit file paths. If the user gives a shell command instead, run it first and then locate the resulting JSON file.

If multiple JSON files are plausible candidates, prefer the file that best matches:

- the user’s wording
- recent modification time
- recognizable output names such as `*_data.json`, `results.json`, `report.json`

### 2. Profile before rendering

Run:

```bash
python3 <skill-dir>/scripts/profile_json.py path/to/file.json
```

Use the profile to answer:

- Is this an array of records, a record map, metadata plus row arrays, a nested document, or a scalar?
- How many rows or entities exist?
- Which fields look numeric, date-like, nested, or overly verbose?
- Which branches are sections, and which arrays form repeated child records?

Treat the profiler output as factual evidence, not as a UI recommendation.

### 3. Choose the surface

Use this fixed order:

1. Harness-native generative UI via declarative spec
2. Terminal-native reference renderer
3. Inline Markdown only as a fallback

Read `references/surface-selection.md` before selecting the output path.

### 4. Render conservatively

Start with:

- one-sentence dataset description
- row or entity count
- the most useful dimensions and metrics
- a compact primary section or table

Then add detail sections only if they improve usability.

Do not dump raw JSON unless the shape is too irregular to summarize safely.

## Rendering Rules

### Arrays of objects

Render:

- summary metrics
- a compact table with the most informative columns
- optional ranked slices for notable numeric fields

### Metadata plus data payloads

Resolve row arrays into labeled columns before presenting them. If the payload contains:

- `metadata.<section>` as column names
- `data.<entity>.<section>` as row arrays

then use the profiler's `detected_sections` to build sections such as `data.api` or `data.xbrl`.

### Record maps

Promote the map key into an explicit `entity_key` column before rendering.

### Nested objects

Prefer sectioned summaries first. Show the most informative branches and avoid flattening deeply nested structures into unreadable tables.

### Repeated child records

When aligned arrays describe repeated entities, convert them into child rows or child tables. Do not leave them as opaque arrays inside a parent record when the alignment is strong.

### Large or noisy fields

Truncate long strings in overview views. Summarize arrays and nested objects by size or type unless they qualify as repeated child records.

## Shell Guidance

When the user gives a shell command instead of a path:

- run the command
- locate the JSON artifact it generated
- profile the artifact
- derive a declarative UI spec
- render the result using the native harness or the terminal renderer

If the command produces multiple JSON files, summarize the candidates and pick the best match using recency and filename relevance.

## Resources

- Use `scripts/profile_json.py` for deterministic shape inspection.
- Read `references/ui-schema.md` for the declarative UI contract.
- Read `references/surface-selection.md` for the exact rendering order and environment heuristics.
- Read `references/presentation-patterns.md` for layout patterns by JSON shape.
