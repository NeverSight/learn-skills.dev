---
name: planning-implementation
description: Use when converting architecture or design documents into structured, dependency-ordered implementation task lists for autonomous agent execution via dark-factory
disable-model-invocation: true
---

# Planning Implementation

## Overview

Extract every implementation task from architecture document(s) into a structured JSON task graph. The output is a DAG of tasks sized for autonomous agent workers — each task self-contained, dependency-ordered, and verifiable without access to the full architecture.

## Before Planning Begins

1. **Get existing state**: Run `dark-factory list --job $JOB --status pending --include-content` to see outstanding tasks already in the graph
2. **Explore the codebase**: Dispatch background explore agents to review files relevant to each section of the document — understand existing patterns, types, and integration points before writing tasks
3. **Research dependencies**: Use web search to research any libraries, frameworks, or tools referenced in the architecture that you're unfamiliar with

## Output Schema

Write valid JSON to the specified output path:

```json
{
  "project": "<project name>",
  "tasks": [
    {
      "id": "T001",
      "title": "Short task title",
      "description": "Detailed description of what to implement",
      "dependencies": ["T000"],
      "files": ["src/path/to/file.ts"],
      "acceptance_criteria": "Specific, verifiable criteria",
      "verification_steps": ["cargo build", "bun test"],
      "context_files": ["specs/ARCHITECTURE.md"],
      "estimated_complexity": "low|medium|high",
      "implementation_details": "Markdown with ### headers"
    }
  ]
}
```

- Sequential IDs: T001, T002, ...
- Dependencies must reference valid task IDs within the list
- Extract EVERY task mentioned in the document — do not skip or merge

## Task Sizing

Each task should represent **1-3 hours of human developer work** and stay under **500 LOC** unless the changes are boilerplate or generated code. If a task exceeds this, split it.

## Field Guide

### `dependencies`

- Organize for **maximum parallelism** — only add a dependency when a task literally cannot be worked on, or its acceptance criteria cannot be verified, until the dependency completes
- Avoid unnecessary serial chains

### `files`

Files this task will directly add, modify, or delete.

### `context_files`

Other codebase files the agent should read before starting. **Prefer inlining** relevant architecture content in `implementation_details` rather than listing the architecture doc as a context file — workers see only their task.

### `acceptance_criteria`

The most important field for verification:

- Enumerate **all cases** that need automated tests, including edge cases not mentioned in the architecture docs
- If automated tests aren't possible, describe steps an agent can perform to verify the work
- Be specific about what behaviour must be proven
- Include specific test fixtures and validation cases

### `verification_steps`

Concrete commands to run: `bun test`, `cargo build`, `bun run typecheck`, etc.

### `implementation_details`

**This is the most valuable field.** Write as if briefing a senior developer who has never seen the codebase:

- **Inline** specific sections, patterns, and code examples from the architecture doc(s)
- Include: function signatures, struct/type definitions, trait impls, API shapes
- Include: integration points — existing modules/functions this code must connect to
- Include: edge cases, error handling requirements, known gotchas
- Include: example code snippets showing expected patterns when the docs provide them
- Format with markdown headers: `### Pattern`, `### Integration Points`, `### Edge Cases`
- **Self-contained** — workers see ONLY their task, not the full architecture

Scale detail to complexity:
| Complexity | Word count |
|-----------|------------|
| Low | ~50-100 |
| Medium | ~100-200 |
| High | ~200-400 |

## Validation

**CRITICAL:** After writing the output file, read it back and validate it parses as valid JSON matching the schema. If it doesn't parse, fix and re-write. Do not finish until the file contains valid JSON.
