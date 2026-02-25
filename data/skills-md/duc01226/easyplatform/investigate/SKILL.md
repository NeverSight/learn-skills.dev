---
name: investigate
description: '[Fix & Debug] Investigate and explain how existing features or logic work. READ-ONLY exploration with no code changes.'
version: 2.0.0
allowed-tools: Read, Grep, Glob, Task, WebFetch, WebSearch, TodoWrite
---

# Feature Investigation

READ-ONLY exploration skill for understanding existing features. No code changes.

## Summary

**Goal:** READ-ONLY exploration of existing features and logic — understand how code works without making changes.

| Step | Action          | Key Notes                                                                      |
| ---- | --------------- | ------------------------------------------------------------------------------ |
| 1    | Discovery       | Search codebase for related files (Entities > Commands > Events > Controllers) |
| 2    | Knowledge Graph | Read and document purpose, symbols, dependencies per file                      |
| 3    | Flow Mapping    | Trace entry points through pipeline to exit points                             |
| 4    | Analysis        | Extract business rules, validation, authorization, error handling              |
| 5    | Synthesis       | Write executive summary with key files and flow diagrams                       |
| 6    | Present         | Deliver findings, offer deeper dives on subtopics                              |

**Key Principles:**

- **Be skeptical. Critical thinking. Everything needs traced proof.** — Never accept code at face value; verify claims against actual behavior, trace data flow end-to-end, and demand evidence (file:line references, grep results, runtime confirmation) for every finding
- Strictly READ-ONLY — no code changes allowed
- MUST read anti-hallucination-protocol.md and knowledge-graph-template.md before starting
- Evidence-based: validate every assumption with actual code references

## Mode Selection

| Mode            | Use When                                     | Workflow                                           |
| --------------- | -------------------------------------------- | -------------------------------------------------- |
| **Interactive** | User available, exploratory question         | Real-time collaboration, iterative tracing         |
| **Autonomous**  | Deep analysis, complex cross-service tracing | Structured 4-phase workflow with analysis artifact |

## Workflow

1. **Discovery** - Search codebase for all files related to the feature/question. Prioritize: Entities > Commands/Queries > EventHandlers > Controllers > Consumers > Components.
2. **Knowledge Graph** - Read and analyze each file. Document purpose, symbols, dependencies, data flow. Batch in groups of 10, update progress after each batch.
3. **Flow Mapping** - Trace entry points through processing pipeline to exit points. Map data transformations, persistence, side effects, cross-service boundaries.
4. **Analysis** - Extract business rules, validation logic, authorization, error handling. Document happy path and edge cases.
5. **Synthesis** - Write executive summary answering the original question. Include key files, patterns used, and text-based flow diagrams.
6. **Present** - Deliver findings using the structured output format. Offer deeper dives on subtopics.

## ⚠️ MUST READ Before Investigation

**IMPORTANT: You MUST read these files before starting. Do NOT skip.**

- **⚠️ MUST READ** `.claude/skills/shared/anti-hallucination-protocol.md` — Assumption validation, evidence chains, context anchoring
- **⚠️ MUST READ** `.claude/skills/shared/knowledge-graph-template.md` — Per-file analysis structure

**If preceded by `/scout`:** Use Scout's numbered file list as analysis targets. Skip redundant discovery. Prioritize HIGH PRIORITY files first.

## Investigation Techniques

### Discovery Search Patterns

#### File Discovery by Feature Name

```regex
.*EventHandler.*{FeatureName}|{FeatureName}.*EventHandler
.*BackgroundJob.*{FeatureName}|{FeatureName}.*BackgroundJob
.*Consumer.*{FeatureName}|{FeatureName}.*Consumer
.*Service.*{FeatureName}|{FeatureName}.*Service
.*Component.*{FeatureName}|{FeatureName}.*Component
```

#### Priority Order for Analysis

1. **Domain Entities** - Core business objects
2. **Commands/Queries** - CQRS entry points (`UseCaseCommands/`, `UseCaseQueries/`)
3. **Event Handlers** - Side effects (`UseCaseEvents/`, `*EventHandler.cs`)
4. **Controllers** - API endpoints (`Controllers/`, `*Controller.cs`)
5. **Consumers** - Cross-service (`*Consumer.cs`, `*BusMessage.cs`)
6. **Background Jobs** - Scheduled processing (`*BackgroundJob*.cs`, `*Job.cs`)
7. **Components/Stores** - Frontend (`*.component.ts`, `*.store.ts`)
8. **Services/Helpers** - Supporting logic (`*Service.cs`, `*Helper.cs`)

### Dependency Tracing

#### Backend (C#)

| Looking for                    | Search pattern                                                                  |
| ------------------------------ | ------------------------------------------------------------------------------- |
| Who calls this method          | Grep method name across `*.cs`                                                  |
| Who injects this service       | Grep interface name in constructors                                             |
| What events this entity raises | Grep `PlatformCqrsEntityEvent<EntityName>`                                      |
| Cross-service consumers        | Grep `*BusMessage` type across all services                                     |
| Repository usage               | Grep `IRepository<EntityName>` or `IPlatformQueryableRootRepository<EntityName` |

#### Frontend (TypeScript)

| Looking for              | Search pattern                                                    |
| ------------------------ | ----------------------------------------------------------------- |
| Who uses this component  | Grep selector `app-component-name` in `*.html`                    |
| Who imports this service | Grep service class name in `*.ts`                                 |
| Store effects chain      | Trace `effectSimple` -> API call -> `tapResponse` -> state update |
| Route entry              | Grep component name in `*routing*.ts`                             |

### Data Flow Mapping

Document flow as text diagram:

```text
[Entry Point] --> [Step 1: Validation] --> [Step 2: Processing] --> [Step 3: Persistence]
                                                  |
                                                  v
                                          [Side Effect: Event]
```

#### Flow Documentation Checklist

1. **Entry Points** - API endpoint, UI action, scheduled job, message bus
2. **Processing Pipeline** - Step-by-step through handlers
3. **Data Transformations** - How data changes at each step
4. **Persistence Points** - Where data is saved/loaded
5. **Exit Points** - Responses, events, side effects
6. **Cross-Service Flows** - Message bus boundaries

### Common Investigation Scenarios

#### "How does feature X work?"

1. Find entry points (API, UI, job)
2. Trace through command/query handlers
3. Document entity changes
4. Map side effects (events, notifications)

#### "Where is the logic for Y?"

1. Search keywords in commands, queries, entities
2. Check event handlers for side effect logic
3. Look in helper/service classes
4. Check frontend stores and components

#### "What happens when Z occurs?"

1. Identify trigger (user action, event, schedule)
2. Trace the handler chain
3. Document all side effects
4. Map error handling

#### "Why does A behave like B?"

1. Find the relevant code path
2. Identify decision points
3. Check configuration/feature flags
4. Document business rules

### Platform Pattern Recognition

#### Backend Patterns

- `PlatformCqrsCommand` / `PlatformCqrsQuery` - CQRS entry points
- `PlatformCqrsEntityEventApplicationHandler` - Side effects
- `PlatformApplicationMessageBusConsumer` - Cross-service consumers
- `IPlatformQueryableRootRepository` - Data access
- `PlatformValidationResult` - Validation logic
- `[PlatformAuthorize]` - Authorization

#### Frontend Patterns

- `AppBaseVmStoreComponent` - State management components
- `PlatformVmStore` - Store implementations
- `effectSimple` / `tapResponse` - Effect handling
- `observerLoadingErrorState` - Loading/error states
- API services extending `PlatformApiService`

## Evidence Collection

### Analysis File Setup

Autonomous mode writes analysis to `.ai/workspace/analysis/[feature-name]-investigation.md` with:

```markdown
## Metadata

> Original question: [user's exact question]

## Investigation Question

[Clearly stated investigation goal]

## Progress

- **Phase**: 1
- **Items Processed**: 0 / [total]
- **Current Focus**: [original question]

## File List

[All discovered files, grouped by priority]

## Knowledge Graph

[Per-file analysis entries - see template below]

## Data Flow

[Flow diagrams and pipeline documentation]

## Findings

[Populated in Phase 2+]
```

### Per-File Analysis Entry

For each file, document in `## Knowledge Graph`:

#### Core Fields

- `filePath`: Full path
- `type`: Component classification (Entity, Command, Handler, Controller, Component, Store, etc.)
- `architecturalPattern`: Design pattern used
- `content`: Purpose and logic summary
- `symbols`: Key classes, interfaces, methods
- `dependencies`: Imports/injections
- `relevanceScore`: 1-10 (to investigation question)
- `evidenceLevel`: "verified" or "inferred"

#### Investigation-Specific Fields

- `entryPoints`: How this code is triggered/called
- `outputPoints`: What this code produces/returns
- `dataTransformations`: How data is modified
- `conditionalLogic`: Key decision points and branches
- `errorScenarios`: What can go wrong, error handling
- `externalDependencies`: External services, APIs, databases

#### Cross-Service Fields (if applicable)

- `messageBusMessage`: Message type consumed/produced
- `messageBusProducers`: Who sends this message
- `crossServiceIntegration`: Cross-service data flow

**Rule:** After every 10 files, update progress and re-check alignment with original question.

### Structured Findings Format

#### Phase 2: Comprehensive Analysis

##### Workflow Analysis

1. **Happy Path** - Normal successful execution flow
2. **Error Paths** - How errors are handled at each stage
3. **Edge Cases** - Special conditions
4. **Authorization** - Permission checks
5. **Validation** - Input validation at each layer

##### Business Logic Extraction

1. **Core Business Rules** - What rules govern this feature
2. **State Transitions** - Entity state changes
3. **Side Effects** - Notifications, events, external calls

#### Phase 3: Synthesis

##### Executive Summary

- One-paragraph answer to user's question
- Top 5-10 key files
- Key patterns used

##### Detailed Explanation

- Step-by-step walkthrough with `file:line` references
- Architectural decisions explained

##### Diagrams

```text
+-----------+     +-----------+     +-----------+
| Component |---->|  Command  |---->|  Handler  |
+-----------+     +-----------+     +-----------+
                                          |
                                          v
                                    +-----------+
                                    |Repository |
                                    +-----------+
```

## Output Format

```markdown
## Answer

[Direct answer in 1-2 paragraphs]

## How It Works

### 1. [Step] - [Explanation with `file:line` reference]

### 2. [Step] - [Explanation with `file:line` reference]

## Key Files

| File | Purpose |
| ---- | ------- |

## Data Flow

[Text diagram: Entry -> Processing -> Persistence -> Side Effects]

## Want to Know More?

- [Subtopic 1]
- [Subtopic 2]
```

## Guidelines

- **Evidence-based**: Every claim needs code evidence. Mark unverified claims as "inferred".
- **Question-focused**: Tie all findings back to the original question.
- **Read-only**: Never suggest changes unless explicitly asked.
- **Layered explanation**: Start simple, offer deeper detail on request.

## Related Skills

- `feature` - Implementing new features (code changes)
- `debug` - Debugging and fixing issues
- `scout` - Quick codebase discovery (run before investigation)

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
