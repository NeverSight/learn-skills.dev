---
name: decision-recording
description: Recording architecture and engineering decisions with one-shot decision recording and search.
---

# Skill: Decision Recording and Search

> **This is the DEFAULT tool for documenting decisions.** When a user asks you to "document a decision", "record a decision", or "make a decision record", use `decision_record` (one-shot). Do NOT use the multi-step `decision_create` / `decision_add_context` / `decision_close` workflow unless you need data product operations (reads, writes, policy evaluations, or approvals).

## Purpose
This skill teaches how to record architectural and engineering decisions using TraceMem's one-shot recording and how to search for existing decisions to build on precedent.

## When to Use
- When a user asks you to "document a decision" or "record a decision" -- **this is the right tool**
- When you make an architecture decision (e.g., choosing a database, designing an API)
- When you choose a dependency, library, or tool over alternatives
- When you change a schema or data model
- When you make an infrastructure decision
- When you need to document an engineering tradeoff or convention
- When you want to check if a similar decision was already made

## When NOT to Use
- When you need to perform data product operations (reads, writes, policy evaluations) as part of the decision -- use the full `decision_create` / `decision_close` workflow instead
- When the decision requires human approval workflow
- For trivial or obvious decisions that don't need audit trails

## Core Tools

### `decision_record` -- One-Shot Recording
Records a complete decision in a single call. The decision is automatically created, populated with context, committed, and snapshotted.

### `decision_search` -- Finding Precedent
Searches your agent's previous decisions by text, category, tags, or status.

## Mandatory Workflow

### Step 1: Search for Existing Decisions

**Always search first** to avoid duplicating decisions or to find decisions to supersede:

```
Tool: decision_search
Parameters:
  - query: "database storage events"  (free-text search)
  - category: "architecture"  (optional filter)
  - tags: ["postgresql"]  (optional filter)
  - status: "committed"  (optional filter)
Returns: Array of matching decisions with supersession indicators
```

### Step 2: Record or Supersede

**If no existing decision found** -- record a new one:

```
Tool: decision_record
Parameters:
  - title: "Use PostgreSQL with JSONB for event storage"
  - category: "architecture"
  - context: "We need a storage backend for decision trace events..."
  - decision: "Use PostgreSQL with JSONB columns for event payload storage..."
  - rationale: "PostgreSQL provides ACID guarantees needed for audit trails..."
  - alternatives_considered:
      - option: "MongoDB"
        rejected_because: "Team lacks MongoDB expertise..."
      - option: "Kafka + ClickHouse"
        rejected_because: "Over-engineered for current volume..."
  - tags: ["postgresql", "events", "storage"]
  - constraints: "Must support ACID transactions"
  - consequences: "Will need partitioning at 10M events/day"
Returns: Complete decision with trace and snapshot
```

**If superseding an existing decision** -- reference the old one:

```
Tool: decision_record
Parameters:
  - title: "Migrate event storage to TimescaleDB"
  - category: "architecture"
  - context: "Event volume now exceeds 10M/day, partitioning needed..."
  - decision: "Switch from plain PostgreSQL to TimescaleDB hypertables..."
  - rationale: "TimescaleDB provides automatic partitioning and compression..."
  - supersedes: "TMEM_abc123"  (ID of the old decision)
  - tags: ["timescaledb", "events", "storage"]
Returns: Decision linked to the superseded one
```

## Categories

Choose the most specific applicable category:

| Category | Use For |
|----------|---------|
| `architecture` | System design, component structure, data flow |
| `dependency` | Library, framework, or tool choices |
| `schema` | Database schema, data model changes |
| `api_design` | API endpoint design, contract decisions |
| `infra` | Infrastructure, deployment, hosting decisions |
| `tradeoff` | Engineering tradeoffs with clear pros/cons |
| `convention` | Coding standards, naming conventions |
| `other` | Anything that doesn't fit above |

## Writing Good Decisions

### Title
- Be specific: "Use worker pool pattern for concurrent processing" not "Concurrency decision"
- Include the key technology or approach

### Context
- Write as a problem description, not a conversation excerpt
- Include constraints and requirements
- A reader 6 months from now should understand the situation

### Decision
- State clearly what was chosen
- Include specific implementation details

### Rationale
- Explain *why* this approach over others
- Reference specific requirements or constraints

### Alternatives Considered
- **This is the highest-value field.** When someone later questions the decision, documented alternatives prevent re-evaluating the same options.
- Include at least one alternative for non-trivial decisions

### Tags
- Use technology names: `postgresql`, `go`, `grpc`
- Use concern areas: `concurrency`, `security`, `performance`
- Use project names if applicable

## Common Mistakes
- **Not searching first**: Always check for existing decisions before recording a new one
- **Vague context**: Writing "We needed to pick a database" instead of describing the actual requirements
- **Missing alternatives**: Not documenting what was considered and rejected
- **Generic tags**: Using tags like "decision" or "important" instead of specific technology/topic tags
- **Using `decision_record` when data operations are needed**: If you need to read/write data products as part of the decision, use the full envelope workflow

## Safety Notes
- Decisions are **immutable** once committed. Write them carefully.
- Do not include secrets, credentials, or PII in any field.
- The `supersedes` field creates an auditable chain -- use it to show decision evolution rather than deleting old decisions.
