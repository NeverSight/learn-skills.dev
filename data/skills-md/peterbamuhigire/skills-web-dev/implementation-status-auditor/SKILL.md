---
name: implementation-status-auditor
description: "Conduct a comprehensive implementation status audit of any software project. Produces structured documentation in docs/implementation/review-{date}/ with gap analysis, schema audit, integration status, completion blueprint, and prioritized action items. Use when the user wants to know exactly where a project stands and what remains to finish it."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# Implementation Status Auditor

## Overview

This skill transforms Claude into an elite Enterprise Software Architect and Technical Auditor. It conducts a brutal, no-stones-unturned analysis of a project's implementation status, producing actionable documentation that serves as both a status report and a completion blueprint.

**When to use:** User asks to audit a project, check implementation status, identify gaps, or generate a completion roadmap.

## Core Workflow

### Step 0: Prepare Output Directory

Create the review directory with today's date:

```
docs/implementation/review-{DD-MMM-YYYY}/
```

Example: `docs/implementation/review-21-Feb-2026/`

If the directory exists (re-run), append a sequence: `review-21-Feb-2026-v2/`.

### Step 1: Discovery Phase (Gather Inputs)

Before any analysis, systematically collect all project materials. Use the Explore agent and direct file reads.

**Required discovery targets:**

| Source | What to Find | How |
|--------|-------------|-----|
| Database schemas | Tables, migrations, ERDs | Glob `**/*.sql`, `**/migrations/**`, schema dumps |
| Project documentation | PRDs, SRS, architecture docs | Glob `docs/**/*.md`, `**/AGENTS.md`, `**/CLAUDE.md` |
| Project plans | Milestones, task lists, roadmaps | Glob `**/plans/**`, `**/NEXT_FEATURES.md`, `**/requirements.md` |
| API contracts | Endpoints, payloads, auth | Glob `**/routes/**`, `**/api/**`, Swagger/OpenAPI files |
| Source code structure | Controllers, models, services | Directory tree of `src/`, `app/`, project root |
| Related projects | Sister apps, shared libraries | Check for monorepo siblings, API consumers |
| Test coverage | Existing tests, test plans | Glob `**/tests/**`, `**/test/**`, `**/*Test.*` |
| Config & infra | CI/CD, deployment, env | Glob `**/docker*`, `**/.github/**`, `**/deploy/**` |

**Discovery SOP:**

1. Read `CLAUDE.md`, `AGENTS.md`, `README.md` at project root
2. Read `docs/` directory tree for all planning/architecture docs
3. Scan database directory for schema files and migrations
4. Map the source code directory structure (top 2 levels)
5. Identify all API route/controller files
6. Check for sister/related project references
7. Locate test files and coverage reports

### Step 2: Analysis Phase (Five Audit Pillars)

Analyze gathered materials against five pillars:

#### Pillar 1: Schema & Data Model Reality Check

Cross-reference database schemas against project documentation.

**Checklist:**

- [ ] All planned entities have corresponding tables
- [ ] Foreign keys enforce documented relationships
- [ ] Multi-tenancy isolation is schema-enforced (tenant_id scoping)
- [ ] Indexes support documented query patterns
- [ ] Normalization level is appropriate (3NF minimum for transactional)
- [ ] Audit columns exist (created_at, updated_at, created_by)
- [ ] Soft-delete support where documented
- [ ] Character set/collation consistency (utf8mb4_unicode_ci)

**Cross-reference with:** `mysql-best-practices` skill for schema standards.

#### Pillar 2: Implementation vs. Plan Gap Analysis

Compare current codebase against project plans and requirements.

**Classification system:**

| Status | Definition | Evidence Required |
|--------|-----------|-------------------|
| **Complete** | Feature fully functional | Routes + Controllers + Models + UI + Tests |
| **Partial** | Some layers exist | Schema exists but no endpoints, or UI stub only |
| **Phantom** | In plan, zero footprint | No schema, no code, no routes — only in docs |
| **Undocumented** | Exists in code, not in plans | Code present but no matching requirement |

**Cross-reference with:** `feature-planning` skill for spec-to-implementation mapping.

#### Pillar 3: Cross-Platform & Integration Integrity

Evaluate API contracts and data flow between systems.

**Checklist:**

- [ ] All documented API endpoints exist in code
- [ ] Authentication/authorization covers all endpoints
- [ ] Response payloads match expected client schemas
- [ ] Pagination implemented where needed
- [ ] Error responses follow consistent format
- [ ] Webhook/callback endpoints documented and implemented
- [ ] Data sync mechanisms between platforms verified

**Cross-reference with:** `api-pagination`, `api-error-handling`, `dual-auth-rbac` skills.

#### Pillar 4: Technical Risk & Debt Assessment

Identify blockers, debt, and architectural concerns.

**Risk categories:**

- **Critical Blocker** — Prevents next milestone, must fix immediately
- **High Debt** — Works now but will break at scale
- **Medium Debt** — Suboptimal but functional
- **Low Debt** — Cosmetic or minor improvement

#### Pillar 5: Completion Blueprint

Transform gaps into an actionable completion plan.

**Blueprint structure:**

- Group remaining work by module/feature
- Prioritize by dependency order (foundations first)
- Estimate complexity (S/M/L/XL)
- Map each item to the skills needed for implementation
- Define acceptance criteria for each item

### Step 3: Documentation Output Phase

Generate the following files in the review directory:

```
docs/implementation/review-{date}/
├── 00-executive-summary.md          # Project health overview
├── 01-schema-audit.md               # Database & data model analysis
├── 02-implementation-progress.md    # Module-by-module status
├── 03-integration-status.md         # Cross-platform & API analysis
├── 04-technical-risks.md            # Risks, debt, and blockers
├── 05-completion-blueprint.md       # Actionable roadmap to finish
├── 06-module-details/               # Per-module deep dives
│   ├── {module-name}-status.md      # One file per major module
│   └── ...
└── 07-appendices/                   # Supporting data
    ├── schema-entity-map.md         # Table-to-feature mapping
    ├── api-endpoint-inventory.md    # Full endpoint listing
    └── test-coverage-map.md         # Test status per module
```

## Report Templates

### 00-executive-summary.md

```markdown
# Implementation Status Audit — Executive Summary
**Project:** {name}
**Date:** {date}
**Auditor:** Claude (Implementation Status Auditor Skill)

## Project Health Score: {X}/10

## Completion Overview
| Category | Complete | Partial | Missing | Total |
|----------|----------|---------|---------|-------|
| Database Schema | X | X | X | X |
| Backend API | X | X | X | X |
| Frontend UI | X | X | X | X |
| Authentication | X | X | X | X |
| Testing | X | X | X | X |
| **Overall** | **X%** | **X%** | **X%** | — |

## Top 3 Critical Findings
1. {finding}
2. {finding}
3. {finding}

## Recommended Immediate Actions
1. {action} — Skill: `{skill-name}`
2. {action} — Skill: `{skill-name}`
3. {action} — Skill: `{skill-name}`
```

### 02-implementation-progress.md

```markdown
# Implementation Progress by Module

## Module: {name}
**Status:** Complete | Partial | Missing
**Completion:** {X}%

### What Exists
- {component}: {status with evidence}

### What's Missing
- {component}: {what needs to be built}
- **Skill to use:** `{skill-name}`
- **Complexity:** S | M | L | XL
- **Blocked by:** {dependency or "None"}
```

### 05-completion-blueprint.md

```markdown
# Completion Blueprint

## Phase 1: Foundation (Must Complete First)
| # | Task | Module | Complexity | Skill | Blocked By |
|---|------|--------|-----------|-------|------------|
| 1 | {task} | {module} | S/M/L/XL | `{skill}` | None |

## Phase 2: Core Features
...

## Phase 3: Integration & Polish
...

## Phase 4: Testing & Hardening
...
```

## Cross-Skill Integration Map

This auditor leverages other skills for both analysis and recommended actions:

| Audit Area | Analysis Skill | Action Skill |
|------------|---------------|--------------|
| Database schema gaps | `mysql-best-practices` | `mysql-best-practices` |
| Missing features | `feature-planning` | `feature-planning` |
| API gaps | `api-error-handling` | `api-pagination`, `dual-auth-rbac` |
| Multi-tenant issues | `multi-tenant-saas-architecture` | `multi-tenant-saas-architecture` |
| Documentation gaps | `doc-architect` | `update-claude-documentation` |
| Testing gaps | `sdlc-testing` | `sdlc-testing` |
| Planning gaps | `sdlc-planning` | `sdlc-planning` |
| UI issues | `webapp-gui-design` | `jetpack-compose-ui` |
| Mobile integration | `android-development` | `android-saas-planning` |
| Security concerns | `vibe-security-skill` | `web-app-security-audit` |
| Code quality tooling | `php-modern-standards` | `php-modern-standards` |
| User docs missing | `manual-guide` | `sdlc-user-deploy` |
| Module architecture | `modular-saas-architecture` | `modular-saas-architecture` |

## Iterative Drilling

After the initial audit, the user can request deep dives:

- **"Drill into {module}"** — Generate detailed `06-module-details/{module}-status.md`
- **"Show me the API payloads for {feature}"** — Extract expected JSON from schema
- **"What tests are missing for {module}"** — Cross-reference with `sdlc-testing`
- **"Generate the completion plan for {phase}"** — Expand blueprint phase into tasks

## Anti-Patterns

| Don't | Do Instead |
|-------|-----------|
| Guess about features without reading code | Read actual route files and controllers |
| Mark features "complete" based on schema alone | Verify full stack: schema + API + UI + tests |
| Skip sister project analysis | Always check for API consumers/mobile apps |
| Write one massive file | Break into the defined file structure |
| Ignore test coverage | Always report testing status per module |
| Make vague recommendations | Map every action to a specific skill |

## Output Standards

- All generated files follow `doc-standards.md` (500-line max per file)
- Use tables for status mappings (scannable, not prose)
- Every gap must have: description, severity, recommended skill, complexity
- Blueprint must be dependency-ordered (no orphan tasks)
- Executive summary must fit on one screen (< 40 lines of content)

## See Also

- `references/audit-checklist.md` — Complete pre-flight checklist
- `references/gap-analysis-patterns.md` — Classification methodology
- `references/drill-down-templates.md` — Templates for iterative deep dives
