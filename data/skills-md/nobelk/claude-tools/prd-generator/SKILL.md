---
name: prd-generator
description: Reverse-engineer a codebase into a formal Product Requirements Document (PRD) structured for Jira work item creation. Use when the user wants to analyze an existing codebase to document all features, identify missing functionality, catalog bugs and technical debt, generate epics/stories/tasks for Jira, or create formal product documentation from source code. Triggers on requests containing "generate PRD", "analyze codebase", "document requirements", "reverse-engineer features", "prepare Jira epics from code", "what does this software do", or "create product requirements".
---

# PRD Generator

Analyze a codebase to produce `prd_doc.md` — a formal Product Requirements Document structured for direct conversion to Jira epics, user stories, and tasks.

## Constraints

- DO NOT write, generate, or modify any code
- DO NOT search the web or use external information
- Rely solely on the local codebase and its documentation
- Use Context7 MCP if available for enhanced code understanding

## Workflow Overview

PRD generation follows five sequential phases:

1. **Discover** — Map project structure, stack, and architecture
2. **Analyze** — Extract all features, logic, data, integrations, and security
3. **Audit** — Identify missing features, bugs, performance issues, and technical debt
4. **Validate** — Cross-reference findings against `onboarding.md`
5. **Generate** — Write `prd_doc.md` using the output template

## Phase 1: Discover

Identify the project foundation:

1. List all directories and key source files
2. Determine the technology stack from config files (`.csproj`, `package.json`, `requirements.txt`, `Cargo.toml`, `*.sln`, `Dockerfile`, etc.)
3. Locate entry points (`Program.cs`, `Startup.cs`, `main.*`, `index.*`, `app.*`)
4. Find existing documentation: README, architecture docs, wiki pages
5. **Confirm whether `onboarding.md` exists** — note its location for Phase 4

**For .NET/C# projects:** Read `references/analysis-patterns.md` § ".NET/C# Discovery" for framework-specific file and configuration patterns.

**Architecture mapping:**
- Identify layers: presentation, API, business/domain, data/infrastructure
- Note project references and dependency graph (for multi-project solutions)
- Document external service integrations

## Phase 2: Analyze

Extract every feature systematically. For each feature found, record: what it does, who uses it, and where the code lives.

**Feature categories to examine:**

- **User-facing capabilities** — screens, pages, workflows, CLI commands
- **API surface** — endpoints, controllers, gRPC services, message handlers
- **Business rules** — validations, calculations, domain logic, state machines
- **Data layer** — models/entities, schemas, migrations, repositories
- **Security** — authentication, authorization, roles, policies, encryption
- **Infrastructure** — caching, queuing, logging, health checks, background jobs
- **Configuration** — settings, feature flags, environment-specific behavior

**For .NET/C# projects:** Read `references/analysis-patterns.md` § ".NET/C# Feature Detection" for framework-specific patterns including ASP.NET controllers, EF Core models, MediatR handlers, SignalR hubs, Blazor components, and middleware.

## Phase 3: Audit

### 3a: Missing Features

Identify gaps by comparing what exists against what is standard for this type of software:

- Search for `TODO`, `FIXME`, `HACK`, `UNDONE`, `NotImplementedException` comments
- Check for stub or skeleton implementations
- Compare against common expectations for the application type

**For .NET/C# projects:** Read `references/analysis-patterns.md` § ".NET/C# Gap Detection" for framework-specific gap patterns.

### 3b: Issues and Technical Debt

Catalog problems across four dimensions:

| Category | What to look for |
|----------|-----------------|
| **Logical** | Null reference risks, incorrect conditionals, race conditions, off-by-one errors, unhandled edge cases |
| **Performance** | N+1 queries, missing indexes, unbounded fetches, sync-over-async, memory leaks, missing caching |
| **Security** | Injection vectors, hardcoded secrets, missing input validation, insecure defaults, broken auth |
| **Code quality** | Dead code, duplication, high complexity, inconsistent patterns, missing error handling |

**For .NET/C# projects:** Read `references/analysis-patterns.md` § ".NET/C# Issue Detection" for patterns like `async void`, `IDisposable` leaks, EF Core anti-patterns, and middleware ordering issues.

For every issue, record: location (file + line/method), description, impact, and recommended fix approach.

## Phase 4: Validate

After completing analysis, read `onboarding.md` (if found in Phase 1) and:

1. Cross-reference discovered features against onboarding descriptions
2. Correct any misinterpretations of feature purpose or scope
3. Add features mentioned in onboarding but missed in code analysis
4. Align terminology with project conventions
5. Verify architectural understanding matches documented intent

If `onboarding.md` is not found, note this in the document and proceed.

## Phase 5: Generate

Create `prd_doc.md` in the current working directory using the template in `assets/prd-template.md`.

**Key output rules:**

- Use consistent ID prefixes: `FR-`, `NFR-`, `GAP-`, `ISSUE-`, `PERF-`, `SEC-`, `QUAL-`, `EPIC-`, `US-`, `TASK-`
- Every functional requirement MUST include a user story in standard format
- Every issue MUST include file location and impact
- Jira section MUST be directly actionable — ready for import as work items
- Acceptance criteria MUST be testable (use Given/When/Then where appropriate)
- Story points use Fibonacci scale: 1, 2, 3, 5, 8, 13

**Before finalizing, verify:**
- All major code modules analyzed
- Features described from user perspective
- Traceability maintained: features → epics → stories → tasks
- Terminology consistent throughout
- No code written, no web sources used
