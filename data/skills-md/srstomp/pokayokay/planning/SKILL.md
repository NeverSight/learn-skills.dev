---
name: planning
agents: [yokay-planner]
description: Use when analyzing PRD documents, concept briefs, or feature specs to create implementation plans, breaking work into epics/stories/tasks with dependencies and estimates, or generating PROJECT.md and kanban tracking.
---

# PRD Analyzer & Implementation Planner

Transform product requirements into actionable implementation plans with visual kanban tracking.

## Key Principles

- All outputs go to `.claude/` folder (PROJECT.md, tasks.db, features.json, kanban.html)
- Break work into epic → story → task hierarchy (tasks ≤ 8h each)
- Assign skills to features based on type (api-design, database-design, etc.)
- Flag ambiguities before planning — don't assume unclear requirements

## Quick Start Checklist

1. Read the full PRD/brief document
2. Extract goals, features, constraints, and dependencies
3. Classify priorities (P0-P3) and flag ambiguities
4. Break features into epics → stories → tasks with estimates
5. Generate `.claude/` outputs (PROJECT.md, tasks.db, features.json, kanban.html)
6. Identify first skill to run and hand off

## Skill Assignment

| Feature Type | Primary Skill | Secondary Skills |
|--------------|---------------|------------------|
| REST/GraphQL APIs | api-design | testing-strategy |
| Database schemas | database-design | — |
| SDK/library | sdk-development | — |
| Auth/Security | api-design | — |
| Testing infrastructure | testing-strategy | — |
| AWS/Cloud provisioning | cloud-infrastructure | — |
| Serverless/Lambda | cloud-infrastructure | api-design |
| Container deployment | cloud-infrastructure | ci-cd |

## References

| Reference | Description |
|-----------|-------------|
| [prd-analysis.md](references/prd-analysis.md) | Deep dive on document analysis |
| [task-breakdown.md](references/task-breakdown.md) | Detailed breakdown methodology |
| [kanban-setup.md](references/kanban-setup.md) | Database schema and HTML generation |
| [skill-routing.md](references/skill-routing.md) | Skill assignment logic |
| [project-md-template.md](references/project-md-template.md) | PROJECT.md template and format |
| [database-schema.md](references/database-schema.md) | Full SQLite schema for tasks.db |
| [features-json.md](references/features-json.md) | features.json format and integration points |
| [anti-patterns.md](references/anti-patterns.md) | Analysis, breakdown, and output anti-patterns |
| [design-integration.md](references/design-integration.md) | Design plugin detection, UI/UX workflows, design-first routing |
| [kanban-template.html](references/kanban-template.html) | HTML template for interactive kanban board |
