---
name: skill-system-workflow
description: "Dynamic orchestration engine that plans multi-step agent work as DAGs with Mermaid visualization."
license: MIT
compatibility: opencode
metadata:
  os: windows, linux, macos
---

# Skill System Workflow

Dynamic orchestration engine that plans multi-step agent work as DAGs (Directed Acyclic Graphs) and always produces a renderable Mermaid diagram.

This skill is designed to bridge: (1) repeatable best-practice playbooks (recipes) and (2) one-off, context-specific plans generated on demand.

## Overview

- Input: a goal (and optional context)
- Output: a `workflow-dag.yaml` document plus a Mermaid `flowchart TD` diagram
- Planning strategy: try to match a pre-defined recipe first; otherwise generate a custom DAG in one pass

## Architecture

### 1) Recipe matching (goal -> recipe)

When a goal resembles a common workflow, the planner matches the goal against `recipes/*.yaml` using each recipe's `trigger_patterns`.

- Benefits: consistent structure, fewer planning errors, repeatable waves, easier to refine over time
- Output: a DAG derived from the recipe, then customized with goal-specific details (files, commands, constraints)

### 2) Dynamic planning (no recipe -> custom DAG)

If no recipe matches strongly, the planner uses `prompts/plan-workflow.md` to generate a custom workflow DAG.

- The planner explicitly separates independent tasks (parallelizable) from dependent tasks (sequential)
- The planner assigns an `agent_type` per task based on strengths (explore vs librarian vs oracle vs build)
- The planner keeps each task atomic and verifiable

### 3) Mermaid output (every plan -> diagram)

Every plan includes a Mermaid diagram so the workflow is easy to review, discuss, and iterate.

- One subgraph per wave
- Dependencies are explicit edges
- Nodes are styled by task `status`

## How To Use

### `plan`

Analyze a goal and produce a workflow DAG plus Mermaid visualization.

1. Read all files in `recipes/`
2. Match `goal` against `trigger_patterns`
3. If a match exists: use the recipe as the base plan and tailor it to the goal
4. Otherwise: use `prompts/plan-workflow.md` to generate a custom DAG
5. Generate Mermaid from the DAG using the conventions in this document

Procedure: `scripts/plan-and-visualize.md`

### `visualize`

Convert an existing DAG YAML into a Mermaid flowchart.

- Parse `waves[*].tasks[*]` and build `flowchart TD`
- Use one Mermaid `subgraph` per wave
- Add edges for `depends_on`
- Apply status styling (pending/running/done/failed)

### `list-recipes`

List available workflow recipes.

- Enumerate files in `recipes/`
- For each file: return `name` and `description`

## File Layout

- `prompts/plan-workflow.md`: one-pass dynamic DAG planning prompt
- `schema/workflow-dag.yaml`: workflow DAG shape specification
- `schema/recipe.yaml`: recipe shape specification
- `recipes/*.yaml`: reusable workflow templates
- `scripts/plan-and-visualize.md`: human procedure for plan -> DAG -> Mermaid

## Recipe Format Reference

Recipes are small YAML documents that describe reusable waves and tasks.

- `name`: recipe identifier (must match the filename without extension)
- `trigger_patterns`: goal keywords/phrases that indicate the recipe is applicable
- `waves`: ordered execution waves
- `waves[*].parallel`: whether tasks in the wave can be performed simultaneously
- `waves[*].tasks[*].depends_on`: task ids from earlier waves that must complete first

See: `schema/recipe.yaml`

## Mermaid Conventions

### Diagram structure

- Graph direction: `flowchart TD`
- One subgraph per wave:
  - `subgraph waveN [Wave N: <description>]`
- Each task is a node with id `task_id`
- Node label format:
  - `<agent_type>\n<task name>`

### Node shapes

- Task nodes: rounded rectangles: `task_id(["<agent_type>\\n<name>"])`
- Optional start/end anchors (if used): circles: `start((Start))`, `end((End))`

### Status styling

Use Mermaid classes based on each task's `status`:

```
classDef pending fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#92400e
classDef running fill:#dbeafe,stroke:#3b82f6,stroke-width:2px,stroke-dasharray: 5 5,color:#1e40af
classDef done fill:#d1fae5,stroke:#10b981,stroke-width:2px,color:#065f46
classDef failed fill:#fee2e2,stroke:#ef4444,stroke-width:3px,color:#991b1b
```

Convention:

- `pending`: not started
- `running`: in progress
- `done`: completed successfully
- `failed`: needs intervention

## Operational Notes

- Keep waves small (2-6 tasks) so the diagram remains readable.
- Prefer parallelism inside a wave; use `depends_on` for cross-wave ordering.
- Every task should have a clear verification outcome (tests, diagnostics, file outputs, or explicit checks).

```skill-manifest
{
  "schema_version": "2.0",
  "id": "skill-system-workflow",
  "version": "1.0.0",
  "capabilities": ["workflow-plan", "workflow-visualize", "workflow-list-recipes"],
  "effects": ["fs.read", "db.read"],
  "operations": {
    "plan": {
      "description": "Analyze a goal and produce an execution plan as a DAG with Mermaid visualization.",
      "input": {
        "goal": {"type": "string", "required": true, "description": "User's goal or task description"},
        "context": {"type": "string", "required": false, "description": "Additional context (files, constraints)"}
      },
      "output": {
        "description": "Workflow DAG YAML + Mermaid diagram",
        "fields": {"dag": "YAML", "mermaid": "string"}
      },
      "entrypoints": {
        "agent": "Follow scripts/plan-and-visualize.md procedure"
      }
    },
    "visualize": {
      "description": "Convert an existing DAG YAML to a Mermaid flowchart.",
      "input": {
        "dag_yaml": {"type": "string", "required": true, "description": "DAG YAML content"}
      },
      "output": {
        "description": "Mermaid flowchart string",
        "fields": {"mermaid": "string"}
      },
      "entrypoints": {
        "agent": "Apply Mermaid conventions from SKILL.md to the DAG"
      }
    },
    "list-recipes": {
      "description": "List available workflow recipes.",
      "input": {},
      "output": {
        "description": "Array of recipe names and descriptions",
        "fields": {"recipes": "array"}
      },
      "entrypoints": {
        "agent": "List files in recipes/ directory"
      }
    }
  },
  "stdout_contract": {
    "last_line_json": false,
    "note": "Agent-executed procedures; output is DAG YAML + Mermaid text."
  }
}
```
