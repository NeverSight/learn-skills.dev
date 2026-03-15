---
name: scan-backend-patterns
version: 1.0.0
description: '[Documentation] Scan project and populate/sync docs/project-reference/backend-patterns-reference.md with repository patterns, CQRS, validation, entities, events, migrations.'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/scan-and-update-reference-doc-protocol.md`
- `.claude/skills/shared/understand-code-first-protocol.md`

## Quick Summary

**Goal:** Scan backend codebase and populate `docs/project-reference/backend-patterns-reference.md` with actual repository patterns, CQRS command/query structures, validation patterns, entity conventions, event handlers, and migration approaches.

**Workflow:**

1. **Read** — Load current target doc, detect init vs sync mode
2. **Scan** — Discover backend patterns via parallel sub-agents
3. **Report** — Write findings to external report file
4. **Generate** — Build/update reference doc from report
5. **Verify** — Validate code examples reference real files

**Key Rules:**

- Generic — works with any backend framework (.NET, Node.js, Java, etc.)
- Detect framework first, then scan for framework-specific patterns
- Every code example must come from actual project files with file:line references

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Scan Backend Patterns

## Phase 0: Read & Assess

1. Read `docs/project-reference/backend-patterns-reference.md`
2. Detect mode: init (placeholder) or sync (populated)
3. If sync: extract existing sections and note what's already well-documented

## Phase 1: Plan Scan Strategy

Detect backend framework:

- `.csproj` files → .NET (check for MediatR, CQRS patterns)
- `package.json` with express/fastify/nestjs → Node.js
- `pom.xml` / `build.gradle` → Java/Kotlin
- `requirements.txt` / `pyproject.toml` → Python

Use `docs/project-config.json` contextGroups/modules if available for service paths.

## Phase 2: Execute Scan (Parallel Sub-Agents)

Launch **3 Explore agents** in parallel:

### Agent 1: Repository & Entity Patterns

- Grep for repository interfaces (`interface I*Repository`, `extends Repository`)
- Find entity/model classes (base class inheritance, attributes/annotations)
- Find DTO classes and mapping patterns (AutoMapper, manual mapping, `MapTo*` methods)
- Discover data access patterns (Unit of Work, DbContext, MongoDB collections)
- Look for extension methods on repositories

### Agent 2: CQRS & Command/Query Patterns

- Grep for command handlers (`IRequestHandler`, `CommandHandler`, `@CommandHandler`)
- Grep for query handlers, query objects
- Find validation patterns (FluentValidation, class-level validators, middleware)
- Discover request/response wrapper patterns (Result<T>, ApiResponse)
- Find authorization attributes/decorators on handlers

### Agent 3: Events, Migrations & Infrastructure

- Grep for event handlers, domain events, integration events
- Find message bus consumers/publishers (MassTransit, RabbitMQ, Kafka patterns)
- Discover migration patterns (EF migrations, Flyway, custom migrators)
- Find background job patterns (Hangfire, Quartz, hosted services)
- Grep for middleware, filters, interceptors

Write all findings to: `plans/reports/scan-backend-patterns-{YYMMDD}-{HHMM}-report.md`

## Phase 3: Analyze & Generate

Read the report. Build these sections:

### Target Sections

| Section                 | Content                                                                                 |
| ----------------------- | --------------------------------------------------------------------------------------- |
| **Repository Pattern**  | Interface naming, base classes, service-specific repos, extension methods with examples |
| **CQRS Patterns**       | Command structure, query structure, handler patterns, file organization conventions     |
| **Validation Patterns** | Validation approach (fluent API, attributes, etc.), common rules, error response format |
| **Entity Patterns**     | Base classes, property conventions, factory methods, domain logic placement             |
| **DTO Mapping**         | Mapping approach, who owns mapping (DTO, handler, or service), examples                 |
| **Event Handlers**      | Domain events vs integration events, handler discovery, side-effect placement           |
| **Message Bus**         | Cross-service communication patterns, consumer conventions, message contracts           |
| **Migrations**          | Migration strategy, naming conventions, data migration patterns                         |
| **Background Jobs**     | Job scheduling, recurring jobs, one-time jobs, conventions                              |
| **Authorization**       | Auth patterns, permission checks, role-based access                                     |

### Content Rules

- Show actual code snippets (5-15 lines) from the project with `file:line` references
- Include "DO" and "DON'T" examples where anti-patterns are clear
- Use tables for convention summaries (naming, file locations, base classes)
- Group patterns by concern, not by framework feature

## Phase 4: Write & Verify

1. Write updated doc with `<!-- Last scanned: YYYY-MM-DD -->` at top
2. Verify: 5 code example file paths exist (Glob check)
3. Verify: class names in examples match actual class definitions
4. Report: sections updated, patterns discovered, coverage gaps

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using TaskCreate
- Always add a final review todo task to verify work quality and identify fixes/enhancements
