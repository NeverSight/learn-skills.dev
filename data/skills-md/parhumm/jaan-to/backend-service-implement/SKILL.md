---
name: backend-service-implement
description: Generate service implementations with business logic from specs and scaffold stubs. Use when implementing backend services.
allowed-tools: Read, Glob, Grep, Write($JAAN_OUTPUTS_DIR/backend/service-implement/**), Task, WebSearch, AskUserQuestion, Edit(jaan-to/config/settings.yaml)
argument-hint: [backend-scaffold, backend-api-contract, backend-data-model, backend-task-breakdown]
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# backend-service-implement

> Bridge spec to code — generate full service implementations with business logic from TODO stubs and upstream specs.

## Context Files

- `$JAAN_CONTEXT_DIR/tech.md` - Tech stack context (CRITICAL — determines framework, ORM, patterns)
  - Uses sections: `#current-stack`, `#frameworks`, `#constraints`, `#patterns`
- `$JAAN_CONTEXT_DIR/config.md` - Project configuration
- `$JAAN_TEMPLATES_DIR/jaan-to-backend-service-implement.template.md` - Output template
- `$JAAN_LEARN_DIR/jaan-to-backend-service-implement.learn.md` - Past lessons (loaded in Pre-Execution)
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol
- `${CLAUDE_PLUGIN_ROOT}/docs/research/70-dev-backend-service-implementation-generation.md` - Research: service layer architecture, ORM queries, RFC 9457 errors, pagination, transactions, idempotency, JWT lifecycle

## Input

**Upstream Artifacts**: $ARGUMENTS

Accepts 1-4 file paths or directory references:
- **backend-scaffold** — Path to scaffold output (route handlers with TODO stubs, service stubs, ORM schema)
- **backend-api-contract** — Path to OpenAPI 3.1 YAML (endpoint specs, request/response schemas, error codes)
- **backend-data-model** — Path to data model document (table definitions, relationships, constraints, indexes)
- **backend-task-breakdown** — Path to BE task breakdown (vertical slices with implementation notes)
- **Empty** — Interactive wizard prompting for each artifact

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `backend-service-implement`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

Also read context files if available:
- `$JAAN_CONTEXT_DIR/tech.md` — Know the tech stack for framework-specific service generation
- `$JAAN_CONTEXT_DIR/config.md` — Project configuration

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_backend-service-implement`

> **Language exception**: Generated code output (variable names, code blocks, schemas, SQL, API specs) is NOT affected by this setting and remains in the project's programming language.

---

# PHASE 1: Analysis (Read-Only)

## Thinking Mode

ultrathink

Use extended reasoning for:
- Cross-referencing scaffold TODO stubs against API contract + data model + task breakdown
- Deriving business logic from endpoint relationships and status code semantics
- Planning service implementation order (dependency graph)
- Identifying state machines, transactions, and idempotency requirements

## Step 1: Validate & Parse Inputs

For each provided path:
- **backend-scaffold**: Read route handlers, service stubs, ORM schema. Extract all `// TODO` comments and map to endpoint operations
- **backend-api-contract**: Read api.yaml. Extract paths, schemas, error responses, security schemes, pagination config
- **backend-data-model**: Read data model doc. Extract table definitions, constraints, indexes, relationships, migration notes
- **backend-task-breakdown**: Read task breakdown. Extract vertical slices, implementation notes, acceptance criteria, business rules

Report which inputs found vs missing; suggest fallback for missing:
- Missing scaffold: generate service implementations from API contract + data model (scaffold-less mode)
- Missing API contract: derive endpoints from scaffold route definitions
- Missing data model: derive from Prisma/Eloquent schema in scaffold
- Missing task breakdown: derive business rules from API contract status codes and schema differences

Present input summary:
```
INPUT SUMMARY
─────────────
Sources Found:    {list}
Sources Missing:  {list with fallback suggestions}
Entities:         {extracted entity/resource names}
TODO Stubs:       {count from scaffold}
Endpoints:        {count from API contract}
Tables:           {count from data model}
Task Slices:      {count from task breakdown}
Business Rules:   {count of derived rules}
```

## Step 2: Detect Tech Stack

Read `$JAAN_CONTEXT_DIR/tech.md`:
- Extract framework from `#current-stack` (default: Fastify v5+)
- Extract ORM from `#current-stack` (default: Prisma)
- Extract DB from `#current-stack` (default: PostgreSQL)
- Extract patterns from `#patterns` (auth, error handling, logging)
- If tech.md missing: ask framework/ORM/DB via AskUserQuestion

**Multi-Stack Detection:**

| tech.md value | Framework | ORM/DB | Service Pattern | Output |
|---------------|-----------|--------|-----------------|--------|
| Node.js / TypeScript | Fastify v5+ | Prisma | Plain exported functions + Prisma singleton | `.ts` files |
| PHP | Laravel 12 / Symfony 7 | Eloquent / Doctrine | Service classes + Repository pattern | `.php` files |
| Go | Chi / stdlib (Go 1.22+) | sqlc / GORM | Feature-based internal packages | `.go` files |

## Step 3: Map TODOs to Implementation Plan

### 3.1: TODO Inventory

Parse all `// TODO: implement` stubs from scaffold. For each:
1. Identify the endpoint (method + path)
2. Match to API contract operation (request/response schemas, error codes)
3. Match to data model tables (required queries, relationships)
4. Match to task breakdown slice (business rules, acceptance criteria)

### 3.2: Business Logic Derivation

Derive implementation patterns from API spec semantics:

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/backend-service-implement-reference.md` section "Business Logic Derivation Patterns" for HTTP status code patterns, schema difference analysis, endpoint relationship patterns, and task breakdown derivation rules.

### 3.3: State Machine Detection

When API specs include status fields with constrained transitions:
- Extract enum values from schema
- Map action endpoints to transitions (e.g., POST /orders/{id}/confirm)
- Generate transition map and validation function

### 3.4: Dependency Graph

1. Shared helpers (error factory, pagination, cursor encoding)
2. Auth service (JWT lifecycle — if auth endpoints exist)
3. Independent resource services (no cross-service dependencies)
4. Dependent resource services (reference other services)
5. Cross-cutting middleware (idempotency, rate limiting)

## Step 4: Clarify Implementation Scope

Use AskUserQuestion:

1. **Scope question:**
   - Question: "Implement all TODOs or select vertical slices?"
   - Header: "Scope"
   - Options:
     - "All TODOs" — Implement every TODO stub found
     - "Select slices" — Choose specific vertical slices from task breakdown
     - "Priority subset" — Start with core CRUD, add complex logic later

2. **Auth question** (if auth endpoints detected):
   - Question: "What JWT library should be used for authentication?"
   - Header: "Auth"
   - Options:
     - "jose (Recommended)" — Modern JWT with Web Crypto API, edge-compatible
     - "jsonwebtoken" — Legacy but widely used
     - "Already implemented" — Auth service exists, skip generation
     - "No auth" — Skip auth implementation

3. **Pagination question** (if list endpoints detected):
   - Question: "Which pagination strategy for list endpoints?"
   - Header: "Pagination"
   - Options:
     - "Cursor-based (Recommended)" — Stable under writes, O(1) seek, opaque cursor
     - "Offset-based" — Simple page + limit, for admin/dashboard endpoints
     - "Both" — Cursor for public API, offset for admin
     - "Already implemented" — Pagination helpers exist

4. **Transaction depth** (if multi-step operations detected):
   - Question: "How should multi-step operations be handled?"
   - Header: "Transactions"
   - Options:
     - "Interactive transactions (Recommended)" — Prisma $transaction with isolation levels
     - "Sequential batch" — Simple array transactions for independent writes
     - "Optimistic concurrency" — Version-based updates with conflict detection
     - "Mix by operation" — Choose per operation based on complexity

5. **Idempotency question** (if POST/PUT endpoints exist):
   - Question: "Should POST/PUT endpoints support idempotency keys?"
   - Header: "Idempotency"
   - Options:
     - "Yes (Recommended)" — Idempotency-Key header with DB storage, 24h TTL
     - "Critical endpoints only" — Only for payment/order creation
     - "No" — Skip idempotency support

## Step 5: Present Implementation Plan

```
IMPLEMENTATION PLAN
═══════════════════

STACK: {framework} + {orm} + {database}

TODO COVERAGE
─────────────
Total TODOs:     {count}
Implementing:    {count} ({scope choice})
Skipping:        {count} (if partial scope)

SERVICES ({count})
──────────────────
{For each service:}
  {resource}.service.ts
    - {method}: {description} ({status codes})
    ...

SHARED HELPERS
──────────────
  - error-factory.ts (RFC 9457 problem details, error type registry)
  - pagination.ts ({strategy} pagination helper)
  {- cursor.ts (cursor encode/decode) — if cursor pagination}
  {- auth.service.ts (JWT lifecycle with jose) — if auth}
  {- idempotency.ts (Idempotency-Key middleware) — if enabled}

STATE MACHINES ({count if any})
───────────────────────────────
  {resource}: {state1} → {state2} → ...

DEPENDENCY ORDER
────────────────
1. Shared helpers
2. {ordered service list}
```

---

# HARD STOP — Review Implementation Plan

Use AskUserQuestion:
- Question: "Proceed with generating service implementations?"
- Header: "Generate"
- Options:
  - "Yes" — Generate all planned service files
  - "No" — Cancel
  - "Edit" — Let me revise the scope or architecture first

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Generation (Write Phase)

## Phase 2 Output — Flat folder (no nested subfolder)

All files in `$JAAN_OUTPUTS_DIR/backend/service-implement/{id}-{slug}/`:

```
{id}-{slug}/
├── {id}-{slug}.md                        # Implementation guide + decisions log
├── {id}-{slug}-services/                  # Service files by domain
│   ├── {resource}.service.ts              # Per-resource service implementation
│   ├── auth.service.ts                    # Auth/JWT service (if applicable)
│   └── ...
├── {id}-{slug}-helpers/                   # Shared helper files
│   ├── error-factory.ts                   # RFC 9457 error creation
│   ├── pagination.ts                      # Pagination utility
│   ├── cursor.ts                          # Cursor encode/decode (if cursor pagination)
│   └── idempotency.ts                     # Idempotency middleware (if enabled)
└── {id}-{slug}-readme.md                  # Integration instructions
```

> File extensions adapt to detected stack (.ts for Node.js, .php for PHP, .go for Go).

## Step 6: Generate Shared Helpers

Generate helpers in dependency order (these are used by services):

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/backend-service-implement-reference.md` section "Helper Generation Patterns" for Error Factory (RFC 9457), Pagination Helper, Auth Service, and Idempotency Middleware generation templates.

## Step 7: Generate Service Implementations

### 7.1: Service Structure

**Node.js/TypeScript (Fastify + Prisma):**
```typescript
// Plain exported functions importing Prisma singleton
// Module caching acts as built-in singleton (no DI container needed)
// Testable via vi.mock()

import { prisma } from '../lib/prisma.js';
import { createProblemDetail, BusinessError } from '../helpers/error-factory.js';
import { paginateWithCursor } from '../helpers/pagination.js';
import type { RequestContext } from '../types.js';
```

**PHP (Laravel + Eloquent):**
```php
// Service class with constructor injection
// Repository pattern optional (Eloquent IS the repository)
// API Resources for response transformation
```

**Go (Chi/stdlib + sqlc):**
```go
// Feature-based internal package
// Constructor injection with small interfaces (1-3 methods)
// Accept interfaces, return structs
```

### 7.2: Per-Method Implementation

For each TODO stub, generate the full implementation:

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/backend-service-implement-reference.md` section "Per-Method Implementation Patterns" for CREATE, READ, LIST, UPDATE, DELETE, and ACTION operation implementation steps.

### 7.3: State Machine Generation

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/backend-service-implement-reference.md` section "State Machine Generation" for transition map template and validation function code.

### 7.4: Cross-Service Operations

For operations spanning multiple services:
- Use Prisma interactive `$transaction` with explicit isolation level
- Pass `tx` (transaction client) to all participating service methods
- Keep transactions short — move side effects outside
- Set `maxWait: 5000` and `timeout: 10000`

## Step 8: Generate Implementation Guide

### 8.1: Executive Summary
1-2 sentences: resource count, stack, key patterns implemented (pagination, auth, idempotency).

### 8.2: Implementation Decisions Log
For each decision made during generation:
| Decision | Choice | Rationale |
|----------|--------|-----------|
| Pagination | Cursor-based | Stable under concurrent writes, O(1) seek |
| Auth | jose JWT | Web Crypto API, edge-compatible |
| Transactions | Interactive | Multi-step inventory reservation |
| ... | ... | ... |

### 8.3: TODO Coverage Report
| Service | TODOs Found | TODOs Implemented | Coverage |
|---------|------------|-------------------|----------|
| user.service.ts | 5 | 5 | 100% |
| order.service.ts | 8 | 8 | 100% |
| ... | ... | ... | ... |
| **Total** | **{n}** | **{n}** | **100%** |

### 8.4: Service Dependency Map
Mermaid diagram showing service dependencies and shared helpers.

## Step 9: Generate Integration README

1. **Setup** — How to integrate generated services into the scaffold project
2. **File Placement** — Where each generated file goes relative to the project root
3. **Dependencies** — NPM packages to install (jose, etc.)
4. **Configuration** — Environment variables needed (JWT_SECRET, etc.)
5. **Testing** — How to test individual services (`vi.mock()` pattern)
6. **Next Steps** — Downstream skills:
   - `/jaan-to:qa-test-generate` — Generate tests for these implementations
   - `/jaan-to:sec-audit-remediate` — Security audit the implementations

## Step 10: Quality Check

Before preview, verify every item in the checklist (coverage, error handling, patterns, security, code quality).

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/backend-service-implement-reference.md` section "Quality Check Checklist" for the full verification checklist.

If any check fails, fix before preview.

## Step 11: Preview & Approval

Present generated output summary:
- File count and total lines
- TODO coverage percentage
- Service list with method counts
- Helpers generated

Use AskUserQuestion:
- Question: "Write service implementation files to output?"
- Header: "Write Files"
- Options:
  - "Yes" — Write the files
  - "No" — Cancel
  - "Refine" — Make adjustments first

## Step 12: Generate ID and Folder Structure

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/id-generator.sh"
SUBDOMAIN_DIR="$JAAN_OUTPUTS_DIR/backend/service-implement"
mkdir -p "$SUBDOMAIN_DIR"
NEXT_ID=$(generate_next_id "$SUBDOMAIN_DIR")
slug="{project-name-slug}"
OUTPUT_FOLDER="${SUBDOMAIN_DIR}/${NEXT_ID}-${slug}"
```

Preview output configuration:
> **Output Configuration**
> - ID: {NEXT_ID}
> - Folder: `$JAAN_OUTPUTS_DIR/backend/service-implement/{NEXT_ID}-{slug}/`
> - Main file: `{NEXT_ID}-{slug}.md`

## Step 13: Write Output

1. Create output folder: `mkdir -p "$OUTPUT_FOLDER"`
2. Create services subdirectory: `mkdir -p "$OUTPUT_FOLDER/${NEXT_ID}-${slug}-services"`
3. Create helpers subdirectory: `mkdir -p "$OUTPUT_FOLDER/${NEXT_ID}-${slug}-helpers"`
4. Write all files:
   - Main doc: `$OUTPUT_FOLDER/${NEXT_ID}-${slug}.md`
   - Service files: `$OUTPUT_FOLDER/${NEXT_ID}-${slug}-services/{resource}.service.ts`
   - Helper files: `$OUTPUT_FOLDER/${NEXT_ID}-${slug}-helpers/{helper}.ts`
   - Integration readme: `$OUTPUT_FOLDER/${NEXT_ID}-${slug}-readme.md`
5. Update subdomain index:
```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/index-updater.sh"
add_to_index \
  "$SUBDOMAIN_DIR/README.md" \
  "$NEXT_ID" \
  "${NEXT_ID}-${slug}" \
  "{Project Title} Service Implementations" \
  "{Executive summary — 1-2 sentences}"
```

6. Confirm completion:
> Service implementations written to: `$JAAN_OUTPUTS_DIR/backend/service-implement/{NEXT_ID}-{slug}/`
> Index updated: `$JAAN_OUTPUTS_DIR/backend/service-implement/README.md`

## Step 14: Suggest Next Actions

> **Service implementations generated successfully!**
>
> **TODO Coverage: {n}/{n} (100%)**
>
> **Next Steps:**
> - Copy service files to your project (see integration readme for placement)
> - Run `/jaan-to:qa-test-generate` to generate tests for these implementations
> - Run `/jaan-to:sec-audit-remediate` to audit the implementations for security issues
> - Run your existing test suite to verify integration

## Step 15: Capture Feedback

Use AskUserQuestion:
- Question: "How did the service implementations turn out?"
- Header: "Feedback"
- Options:
  - "Perfect!" — Done
  - "Needs fixes" — What should I improve?
  - "Learn from this" — Capture a lesson for future runs

If "Learn from this": Run `/jaan-to:learn-add backend-service-implement "{feedback}"`

---

## Key Generation Rules — Node.js/TypeScript (Research-Informed)

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/backend-service-implement-reference.md` section "Key Generation Rules — Node.js/TypeScript (Research-Informed)" for the full rules list covering Service Layer, Prisma Queries, Error Handler, RFC 9457, JWT, Cursor Pagination, Idempotency, Transactions, Import Extensions, and DTO Mapping.

## Multi-Stack Support (Research-Informed)

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/backend-service-implement-reference.md` section "Multi-Stack Service Patterns" for PHP (Laravel + Symfony) and Go stack-specific service patterns.

## Anti-Patterns to NEVER Generate

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/backend-service-implement-reference.md` section "Anti-Patterns" for per-stack anti-pattern lists (All Stacks, Node.js, PHP, Go).

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Multi-stack support via `tech.md` detection
- Template-driven output structure
- Output to standardized `$JAAN_OUTPUTS_DIR` path

## Definition of Done

- [ ] All TODO stubs from scaffold have corresponding implementations
- [ ] Every API contract endpoint has service method coverage
- [ ] RFC 9457 error handling implemented with type registry
- [ ] Pagination helper generated and used in all list endpoints
- [ ] Auth service generated (if auth endpoints exist) with JWT lifecycle
- [ ] Idempotency middleware generated (if enabled) for POST/PUT
- [ ] State machines generated for resources with status transitions
- [ ] Transactions used for multi-step operations with side effects outside
- [ ] Quality checks passed (coverage, error handling, patterns, security, code quality)
- [ ] Implementation guide with decisions log and TODO coverage report
- [ ] Integration readme with setup instructions and next steps
- [ ] Output follows v3.0.0 structure (ID, folder, index)
- [ ] Index updated with executive summary
- [ ] User approved final result
