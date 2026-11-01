---
name: project-structure-review
description: use when a completed change adds directories, reshapes packages, introduces shared modules, or makes it harder to find where responsibilities live. trigger after implementation when the file tree no longer matches the product model, when a new shared/utils location has appeared, or when a reader needs to hop between four folders to understand one feature.
---

# Project Structure Review

Announce at the start: "I'm using project-structure-review to check whether the file tree still behaves like a useful interface."

## Core idea

Treat the file tree as a product interface for engineers. If a reader cannot find where a feature lives in under a minute, the structure is already failing.

## Workflow

1. Open the repo at the top level and name each directory's purpose in one sentence without opening files. Directories that resist a one-sentence purpose are findings.
2. Pick the feature most affected by the recent change. Trace the feature end-to-end: where is the entry point, the orchestration, the domain logic, the adapter, the test? Count how many top-level folders the trace visits.
3. Run [`checklist.md`](./checklist.md) against the changed areas.
4. Classify findings using [`../../references/severity-model.md`](../../references/severity-model.md). Most structure issues are Medium unless they actively mislead.

## Heuristics

Prefer:

- local ownership over distant generic folders
- obvious entry points over clever folder taxonomies
- structure that matches how engineers actually navigate, not an idealized diagram

## Do not

- propose a full reorganization when two file moves would fix the problem
- flag structure that is merely unfamiliar; flag structure that misleads
- redesign the layout to match a framework convention the repo does not otherwise use

## Supporting files

- [`checklist.md`](./checklist.md) — the inspection steps for directories, naming, placement, and shared locations.
- [`anti-patterns.md`](./anti-patterns.md) — structure-specific anti-patterns extending [`../../references/anti-patterns.md`](../../references/anti-patterns.md).

## Output

Use the review report format in [`../../references/report-templates.md`](../../references/report-templates.md). Recommend a target structure only when it materially improves the *next* likely change, not when it is theoretically cleaner.
