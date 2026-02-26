---
name: rilldata
description: Use when developing, reviewing, or explaining Rill projects and project files (connectors, models, metrics views, explores, canvases, themes, rill.yaml, sources, alerts, reports, APIs). Apply runtime workflow guidance and project-file reference docs, and cite rule files and source URLs.
---

# Rill

Comprehensive guidance for building and operating Rill projects using modular rules sourced from:
- `runtime/ai/instructions/data` (agent workflow + resource authoring guidance)
- `docs.rilldata.com/reference/project-files` (project file reference)

## How To Use This Skill

1. Identify the task type and load only relevant rule files from `rules/`.
2. For implementation guidance, read `runtime-*` rules first.
3. For full property-level syntax and examples, read corresponding `project-files-*` rules.
4. Cite rule file names and source URLs in responses.

## Rule Routing

- Project-level workflow and DAG reasoning:
  - `runtime-development.md`
- Connector work:
  - `runtime-connector.md`
  - `project-files-connectors.md`
- Model work:
  - `runtime-model.md`
  - `project-files-models.md`
  - `project-files-sources.md` (when source resources are involved)
- Metrics layer work:
  - `runtime-metrics-view.md`
  - `project-files-metrics-views.md`
- Explore dashboards:
  - `runtime-explore.md`
  - `project-files-explore-dashboards.md`
- Canvas dashboards and components:
  - `runtime-canvas.md`
  - `project-files-canvas-dashboards.md`
  - `project-files-component.md`
- Theme configuration:
  - `runtime-theme.md`
  - `project-files-themes.md`
- Project-level configuration:
  - `runtime-rillyaml.md`
  - `project-files-rill-yaml.md`
- Product features beyond the core 8 runtime docs:
  - `project-files-alerts.md`
  - `project-files-reports.md`
  - `project-files-apis.md`
  - `project-files-index.md`

## Review Procedure

When reviewing a Rill change:
1. Load the runtime and project-files rule pair for each changed resource type.
2. Validate compatibility with project DAG expectations and environment configuration.
3. Flag missing fields, unsafe defaults, or likely reconciliation/runtime issues.
4. Provide specific corrections with concrete YAML or SQL snippets.

## Output Requirements

- Always reference the consulted rule files by filename.
- Always include canonical source links from each rule's `sourceUrl`.
- If multiple resource types are involved, provide findings by resource type.
