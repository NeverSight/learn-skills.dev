---
name: spec-reviewer
description: >
  Review and challenge spec documents against the project's codebase, best practices, and
  guidelines. Spawns a team of parallel agents to analyze consistency, code reuse, performance,
  scope, and testability. Use when the user says "challenge", "review spec", "check spec",
  "audit spec", or asks to validate a spec file against the codebase. Triggers on spec file
  paths (e.g., specs/037-hover-brackets-info.md).
---

# Spec Reviewer

Parallel-agent review of spec documents. Produces a findings report without modifying the spec.

## Workflow

1. Read the spec file provided by the user
2. Read `AGENTS.md` and `architecture.md` for project context and conventions
3. Create a team of 5 Explore agents — one per review dimension (see references/review-dimensions.md)
4. Wait for all agents to complete
5. Compile findings into a single report
6. Shut down the team

## Team Setup

Create a team named `spec-review`. Spawn 5 agents using the Task tool with `subagent_type: "Explore"` and `team_name: "spec-review"`. Run all 5 in parallel.

Each agent receives:
- The full spec content (inline in the prompt — do NOT tell agents to read files)
- The project guidelines from AGENTS.md and architecture.md (inline)
- Its specific review dimension and checklist from references/review-dimensions.md

Agent prompts must instruct: "Search the codebase thoroughly. Return a structured list of findings. Each finding must include: the spec section it relates to, the issue or suggestion, severity (critical/warning/info), and evidence (file paths, code snippets, or reasoning)."

### Agent Assignments

| Agent Name | Dimension | Focus |
|------------|-----------|-------|
| `consistency` | Codebase Consistency | Patterns, naming, architecture alignment |
| `reuse` | Code Reuse | Existing utilities, components, patterns to leverage |
| `performance` | Performance | CPU/GPU optimization, R3F best practices |
| `scope` | Scope & Complexity | Size, splitting, dependency risks |
| `testability` | Testability | Test coverage feasibility, determinism |

Read `references/review-dimensions.md` for the full checklist to include in each agent's prompt.

## Report Format

After all agents return, compile a single report using this structure:

```
# Spec Review: {spec name}

## Summary
{1-2 sentence overall assessment: is this spec ready, or does it need revision?}

## Critical Issues
{List any critical findings across all dimensions. If none, state "None found."}

## Findings by Dimension

### Codebase Consistency
{Bulleted findings from the consistency agent, each with severity tag}

### Code Reuse Opportunities
{Bulleted findings from the reuse agent}

### Performance
{Bulleted findings from the performance agent}

### Scope & Complexity
{Bulleted findings from the scope agent}

### Testability
{Bulleted findings from the testability agent}

## Verdict
{One of: READY / NEEDS REVISION / MAJOR REWORK, with a brief justification}
```

Omit dimensions with zero findings — don't include empty sections.
