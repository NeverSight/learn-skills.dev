---
name: sdlc-design
description: "Generate Design & Development documentation for SDLC projects. Covers System Design Document (SDD), Technical Specification, Interface Control Document (ICD), Database Design Document, Code Documentation standards, and API Documentation. Use when translating requirements into technical architecture and guiding development teams."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# SDLC Design Skill

Generate a complete **Design & Development** documentation suite for software development projects. This skill produces 6 design documents that translate requirements (from `sdlc-planning`) into actionable technical architecture and implementation guidance.

## When to Use

- Translating an **approved SRS** into a technical architecture and system design
- Documenting **database schemas, stored procedures, and data models** for a new system
- Specifying **API contracts** for frontend, mobile, and third-party consumers
- Defining **interface contracts** between system components and external systems
- Establishing **code documentation standards** before development begins
- Creating **technical specifications** for complex features or modules

## When NOT to Use

- **Gathering raw requirements** -- use `project-requirements` skill
- **Project-level planning** (SDP, QA Plan, Risk Plan) -- use `sdlc-planning` skill
- **Planning a single feature** (spec + implementation) -- use `feature-planning` skill
- **Writing test plans and test cases** -- use `sdlc-testing` skill
- **Writing deployment or user documentation** -- use `sdlc-user-deploy` skill
- **Planning an Android companion app** -- use `android-saas-planning` skill

## Document Inventory

| # | Document | File | Purpose | Audience | Length |
|---|----------|------|---------|----------|--------|
| 1 | System Design Document | `templates/system-design-document.md` | Overall architecture, components, interactions | Architects, senior devs, tech leads | 20-40 pages |
| 2 | Technical Specification | `templates/technical-specification.md` | Implementation details, algorithms, data structures | Developers implementing the system | 20-40 pages |
| 3 | Interface Control Document | `templates/interface-control-document.md` | Interface contracts between components/systems | Integration engineers, API consumers | 15-30 pages |
| 4 | Database Design Document | `templates/database-design-document.md` | Schema, data models, relationships, procedures | DBAs, backend developers | 20-40 pages |
| 5 | Code Documentation Standards | `templates/code-documentation-standards.md` | Inline comments, docstrings, documentation rules | All developers | 10-20 pages |
| 6 | API Documentation | `templates/api-documentation.md` | Endpoint specs, auth, errors, SDK examples | Frontend/mobile devs, integrators | 20-40 pages |

## Prerequisites

Before generating design documents, ensure these inputs exist:

| Input | Source | Required? |
|-------|--------|-----------|
| Software Requirements Spec (SRS) | `sdlc-planning` skill output | Yes |
| Project Vision & Scope | `sdlc-planning` skill output | Yes |
| Tech stack decisions | Project context or defaults | Yes |
| Approved feature list with priorities | SRS or stakeholder sign-off | Yes |
| Module inventory | SRS or `modular-saas-architecture` | Recommended |
| Existing database schemas (if migrating) | Codebase audit | If applicable |
| API consumers list (mobile, web, 3rd party) | Project context | Recommended |

## Generation Workflow

Generate documents in this order. Each builds on the previous.

```
Step 1: System Design Document (architecture baseline)
    |
Step 2: Database Design Document (data layer foundation)
    |
Step 3: Technical Specification (implementation details)
    |
Step 4: Interface Control Document (component contracts)
    |
Step 5: API Documentation (consumer-facing specs)
    |
Step 6: Code Documentation Standards (team conventions)
```

**Rationale:** Architecture drives database design. Database and architecture together inform technical specs. Interface contracts are defined after components are known. API docs are consumer-facing views of interface contracts. Code standards apply across all layers.

## Architecture Patterns Supported

| Pattern | Where Used | Skill Reference |
|---------|------------|-----------------|
| MVVM + Clean Architecture | Android (Presentation / Domain / Data layers) | `android-development` |
| Three-Panel Web Architecture | `/public/`, `/adminpanel/`, `/memberpanel/` | `multi-tenant-saas-architecture` |
| REST API + Dual Auth | Session (web) + JWT (mobile) | `dual-auth-rbac` |
| Row-Level Multi-Tenancy | `franchise_id` in every tenant-scoped query | `multi-tenant-saas-architecture` |
| Pluggable Module Architecture | Enable/disable business modules per tenant | `modular-saas-architecture` |
| Repository Pattern | Android data access abstraction | `android-data-persistence` |
| Service Layer Pattern | PHP business logic encapsulation | `php-modern-standards` |

## Cross-References to Existing Skills

### Upstream Skills (use BEFORE this skill)

| Skill | Relationship |
|-------|-------------|
| `sdlc-planning` | Provides SRS, Vision & Scope, SDP as inputs. Design docs implement what planning docs specify. |
| `project-requirements` | Raw requirements gathered via guided interview. Feed into SRS, then into design. |

### Parallel Skills (use ALONGSIDE this skill)

| Skill | Relationship |
|-------|-------------|
| `mysql-best-practices` | Database Design Document references these standards. Do not duplicate; cross-reference. |
| `api-error-handling` | API Documentation and Technical Spec reference error response patterns. |
| `api-pagination` | API Documentation references pagination patterns (offset-based). |
| `php-modern-standards` | Technical Spec and Code Documentation reference PHP 8+ standards. |
| `android-development` | Technical Spec references Android architecture layers (MVVM + Clean). |
| `multi-tenant-saas-architecture` | SDD references tenant isolation, three-panel architecture. |
| `dual-auth-rbac` | SDD and ICD reference dual auth flows and RBAC model. |
| `vibe-security-skill` | Security architecture sections in SDD. Always apply alongside. |

### Downstream Skills (use AFTER this skill)

| Skill | Relationship |
|-------|-------------|
| `feature-planning` | Uses design docs as input for individual feature specs and implementation plans. |
| `sdlc-testing` | Uses design docs to create test plans and test cases (future). |
| `sdlc-user-deploy` | Uses design docs for deployment guides and user manuals. |
| `saas-seeder` | Uses database design to bootstrap the SaaS template. |

## Adaptation Rules

### SaaS vs Standalone

| Aspect | Multi-Tenant SaaS | Standalone App |
|--------|-------------------|----------------|
| SDD scope | Three-panel architecture, tenant isolation | Single app architecture |
| Database design | `franchise_id` on all tenant tables | No tenant scoping |
| API auth | Dual auth (Session + JWT) | Single auth model |
| ICD complexity | Backend-Mobile-Web + external integrations | Fewer interface types |
| Security design | Zero-trust, audit trails, RBAC | Simpler security model |

### Mobile + Web vs Web-Only

| Aspect | Android + Web | Web-Only |
|--------|---------------|----------|
| SDD components | PHP backend + Android layers + Web frontend | PHP backend + Web frontend |
| ICD scope | REST API + internal Android layer boundaries | AJAX/fetch + internal PHP layers |
| API docs | JWT auth + session auth sections | Session auth only |
| Code docs | PHP + Kotlin + SQL standards | PHP + SQL standards |

### MVP vs Full Product

| Aspect | MVP | Full Product |
|--------|-----|--------------|
| SDD depth | Core modules only (3-5) | All modules (10-20+) |
| Database design | Core tables only | Complete schema |
| API endpoints | Authentication + core CRUD | Full endpoint inventory |
| ICD | Internal interfaces only | Internal + external integrations |

## Output Structure

When generating design documents for a project, create this structure:

```
docs/design/
├── 01-system-design-document.md
├── 01-sdd/
│   ├── component-design.md
│   ├── security-architecture.md
│   └── deployment-architecture.md
├── 02-database-design-document.md
├── 02-database/
│   ├── entity-relationship.md
│   ├── table-definitions.md
│   └── stored-procedures.md
├── 03-technical-specification.md
├── 03-tech-spec/
│   ├── module-specifications.md
│   └── algorithm-details.md
├── 04-interface-control-document.md
├── 05-api-documentation.md
├── 05-api/
│   ├── authentication-endpoints.md
│   ├── module-endpoints.md
│   └── error-reference.md
└── 06-code-documentation-standards.md
```

Each file must stay under 500 lines. Split into subdirectories as needed.

## Quality Checklist

Run after generating all documents:

- [ ] All 6 documents generated (or justified why one was skipped)
- [ ] Each document stays under 500 lines (split if needed)
- [ ] SDD references the correct tech stack with version numbers
- [ ] SDD includes ASCII architecture diagrams (system context, high-level, deployment) — visual-aid locations marked with `[DIAGRAM-PROMPT: <description>]`
- [ ] Every major design decision includes a `## Design Rationale` block: chosen approach, rejected alternatives, trade-off reasoning
- [ ] Major architectural decisions captured as Architecture Decision Records (ADRs): Context → Decision → Alternatives Considered → Consequences
- [ ] Database Design references `mysql-best-practices` skill, not duplicate it
- [ ] All tenant-scoped tables include `franchise_id` column
- [ ] API Documentation references `api-error-handling` and `api-pagination` skills
- [ ] ICD covers all interface types (backend-mobile, backend-web, external)
- [ ] Technical Spec includes real PHP/Kotlin/SQL code examples in fenced code blocks with language identifiers
- [ ] Code Documentation Standards cover PHP, Kotlin, and SQL
- [ ] Security architecture addresses dual auth, RBAC, encryption, audit trails
- [ ] Deployment environments (Windows dev, Ubuntu staging, Debian prod) documented
- [ ] All documents cross-reference each other and upstream SRS
- [ ] No vague language -- all specifications are measurable and concrete
- [ ] Examples are tailored to the project's actual tech stack and domain

## Anti-Patterns (What NOT to Do)

| Anti-Pattern | Why It Fails | Do This Instead |
|-------------|-------------|-----------------|
| Design without approved SRS | Architecture without requirements is guesswork | Complete `sdlc-planning` first |
| One massive design doc | Exceeds 500-line limit, hard to maintain | Split into 6 focused documents |
| No ASCII diagrams | Text-only architecture is hard to understand | Include system context, component, deployment diagrams — mark points needing visuals with `[DIAGRAM-PROMPT: <description>]` |
| Copy MySQL standards into DB design | Duplicates `mysql-best-practices`, goes stale | Cross-reference the skill |
| Skip tenant isolation design | Data leakage between tenants | Always document `franchise_id` strategy |
| API docs without error codes | Consumers can't handle failures | Include complete error reference table |
| No interface versioning strategy | Breaking changes cause outages | Document versioning in ICD |
| God classes in component design | Violates SRP, untestable | Define clear component boundaries |
| Design docs never updated | Docs become stale and misleading | Update at each phase gate |
| Platform-generic examples | Developers can't apply them | Use your actual tech stack in examples |
| Design decisions without rationale | Future maintainers cannot evaluate or change decisions | Add `## Design Rationale` to every key decision: state the chosen approach, rejected alternatives, and the trade-off reasoning |
| No Architecture Decision Records | Architecture history lost; audits fail | Capture each major architectural decision in a structured ADR: Context → Decision → Alternatives → Consequences |

## Template Files

Each template provides the complete structure, section-by-section guidance, example excerpts, anti-patterns, and a quality checklist.

1. [System Design Document](templates/system-design-document.md)
2. [Technical Specification](templates/technical-specification.md)
3. [Interface Control Document](templates/interface-control-document.md)
4. [Database Design Document](templates/database-design-document.md)
5. [Code Documentation Standards](templates/code-documentation-standards.md)
6. [API Documentation](templates/api-documentation.md)

---

**Back to:** [Skills Repository](../CLAUDE.md)
**Related:** [sdlc-planning](../sdlc-planning/SKILL.md) | [feature-planning](../feature-planning/SKILL.md) | [mysql-best-practices](../mysql-best-practices/SKILL.md) | [api-error-handling](../api-error-handling/SKILL.md)
**Last Updated:** 2026-03-15 (strengthened per Adjei 2023, Winston, Etter 2016)
