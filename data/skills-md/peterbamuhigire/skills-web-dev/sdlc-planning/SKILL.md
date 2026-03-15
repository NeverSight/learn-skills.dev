---
name: sdlc-planning
description: "Generate Planning & Management documentation for SDLC projects. Covers Project Vision & Scope, SDP, SCMP, QA Plan, Risk Plan, SRS, and Feasibility Study. Use when starting a new project, conducting project governance, or establishing the planning baseline before development begins."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# SDLC Planning Skill

Generate a complete **Planning & Management** documentation suite for software development projects. This skill produces 7 foundational documents that establish the project baseline before any code is written.

## When to Use

- Starting a **new SaaS project** and need a governance baseline
- Establishing **project planning documents** for stakeholders or investors
- Conducting a **feasibility study** before committing resources
- Setting up **configuration management** and **quality assurance** processes
- Creating a **software development plan** for the team
- Building a **risk management framework** for an upcoming project
- Preparing a **full-system SRS** (not just requirements interview or Android-only)

## When NOT to Use

- **Gathering raw requirements via interview** -- use `project-requirements` skill instead
- **Planning a single feature** (spec + implementation) -- use `feature-planning` skill
- **Planning an Android companion app** (PRD, SDS, API Contract) -- use `android-saas-planning` skill
- **Writing design documents** (SDD, architecture, database design) -- use `sdlc-design` skill
- **Writing test plans with test cases** -- use `sdlc-testing` skill
- **Writing deployment or user documentation** -- use `sdlc-user-deploy` skill

## Document Inventory

| # | Document | File | Purpose | Audience | Length |
|---|----------|------|---------|----------|--------|
| 1 | Project Vision & Scope | `templates/project-vision-scope.md` | Establish the "why" and "what" | Stakeholders, sponsors, investors | 15-30 pages |
| 2 | Software Development Plan | `templates/software-development-plan.md` | Management & technical approach | PM, dev leads, QA | 20-40 pages |
| 3 | Configuration Management Plan | `templates/configuration-management-plan.md` | Change & version control processes | DevOps, dev leads, release mgrs | 15-25 pages |
| 4 | Quality Assurance Plan | `templates/quality-assurance-plan.md` | Quality processes & standards | QA team, devs, PM | 15-25 pages |
| 5 | Risk Management Plan | `templates/risk-management-plan.md` | Identify, assess, mitigate risks | PM, stakeholders, dev leads | 15-25 pages |
| 6 | Software Requirements Spec | `templates/software-requirements-spec.md` | Full functional & non-functional requirements | Devs, QA, stakeholders, architects | 30-60 pages |
| 7 | Feasibility Study Report | `templates/feasibility-study-report.md` | Viability analysis before commitment | Decision makers, investors, sponsors | 15-30 pages |

## Generation Workflow

Generate documents in this order. Each builds on the previous.

```
Step 1: Gather context (use project-requirements skill if not done)
    |
Step 2: Feasibility Study Report (Go/No-Go decision)
    |
Step 3: Project Vision & Scope (approved vision)
    |
Step 4: Software Requirements Specification (full requirements)
    |
Step 5: Software Development Plan (how to build it)
    |
Step 6: Configuration Management Plan (how to manage changes)
    |
Step 7: Quality Assurance Plan (how to ensure quality)
    |
Step 8: Risk Management Plan (what can go wrong)
```

### Prerequisites

Before generating any documents, gather or confirm:

| Input | Source | Required? |
|-------|--------|-----------|
| Project name & domain | User interview | Yes |
| Target market & users | User interview | Yes |
| Core feature list | `project-requirements` output or user | Yes |
| Tech stack decisions | Project context or defaults | Yes |
| Budget & timeline constraints | User or stakeholder | Recommended |
| Existing system inventory | Codebase audit | If migrating |
| Regulatory requirements | User or domain research | If applicable |

## Cross-References to Existing Skills

### Upstream Skills (use BEFORE this skill)

| Skill | Relationship |
|-------|-------------|
| `project-requirements` | Gathers raw requirements via guided interview. Feed its output (requirements.md, business-rules.md, user-types.md, workflows.md) into this skill's SRS and Vision documents. |

### Parallel Skills (use ALONGSIDE this skill)

| Skill | Relationship |
|-------|-------------|
| `feature-planning` | For individual feature specs and implementation plans. This skill covers project-level planning; `feature-planning` covers feature-level planning. |
| `vibe-security-skill` | Security baseline for all web applications. Reference in QA Plan and Risk Plan. |

### Downstream Skills (use AFTER this skill)

| Skill | Relationship |
|-------|-------------|
| `android-saas-planning` | For Android companion app planning (PRD, SDS, API Contract). Uses this skill's SRS as input. |
| `multi-tenant-saas-architecture` | Backend architecture patterns. Uses SDP and SRS as input. |
| `modular-saas-architecture` | Pluggable module architecture. Uses SRS module inventory. |
| `saas-seeder` | Bootstrap the SaaS template. Uses requirements from SRS. |
| `sdlc-design` | Design documentation phase. Uses approved SRS as primary input. |
| `sdlc-testing` | Testing documentation. Uses SRS requirement IDs for test case traceability. |

> **Future skills to add (identified from ISO/IEC 14764-2006):** Software Maintenance Plan (Corrective/Adaptive/Perfective/Preventive maintenance types) and Post-Deployment Evaluation Report are not yet implemented as skills but should be generated at project close.

### Available SDLC Skills

| Skill | Phase | Documents |
|-------|-------|-----------|
| `sdlc-design` | Design | SDD, Database Design, API Design, UI/UX Spec |
| `sdlc-testing` | Testing | Test Plan, Test Cases, V&V Plan, Test Report, Peer Review |

### Available SDLC Skills (continued)

| Skill | Phase | Documents |
|-------|-------|-----------|
| `sdlc-user-deploy` | Delivery | User Manual, Deployment Guide, Release Notes, Training Plan |

## Adaptation Rules

### SaaS vs Standalone

| Aspect | Multi-Tenant SaaS | Standalone App |
|--------|-------------------|----------------|
| Data isolation | Row-level via `franchise_id` | Not applicable |
| Auth model | Dual auth (Session + JWT) | Single auth model |
| Deployment | 3-env (dev/staging/prod) | May be simpler |
| Scaling | Per-tenant growth planning | Single-instance scaling |
| SRS sections | Include NFR-MT (multi-tenancy) | Omit multi-tenancy NFRs |
| Risk register | Include tenant data leakage risks | Omit tenant-specific risks |

### Android + Web vs Web-Only

| Aspect | Android + Web | Web-Only |
|--------|---------------|----------|
| SRS scope | Include mobile NFRs (offline, app store) | Web NFRs only |
| SDP | Include Android build pipeline | Web pipeline only |
| SCMP | Include Gradle + PHP configs | PHP configs only |
| QA Plan | Include Android testing (Compose UI, JUnit 5) | Web testing only |
| Risk Plan | Include app store rejection risks | Omit mobile risks |

### MVP vs Full Product

| Aspect | MVP | Full Product |
|--------|-----|--------------|
| Vision scope | P0 features only | P0 + P1 + P2 features |
| SDP phases | 2-3 phases | 5-8 phases |
| SRS depth | Core modules only | All modules |
| Feasibility | Focus on technical + economic | All five feasibility types |
| Risk register | Top 10 risks | Comprehensive (20-30 risks) |

## Output Structure

When generating documents for a project, create this structure:

```
docs/planning/
├── 01-feasibility-study.md
├── 02-project-vision-scope.md
├── 03-software-requirements-spec.md
├── 03-srs/
│   ├── functional-requirements.md
│   ├── non-functional-requirements.md
│   └── traceability-matrix.md
├── 04-software-development-plan.md
├── 05-configuration-management-plan.md
├── 06-quality-assurance-plan.md
└── 07-risk-management-plan.md
```

Each file must stay under 500 lines. Split into subdirectories as needed.

## Phase Gate Exit Criteria

Every project passes through six risk-based milestones (Disciplined Agile, 2020). Each milestone has mandatory exit criteria verified before proceeding. These map to the six DA milestones.

| Gate | DA Milestone | Triggered By | Exit Criteria |
|------|-------------|--------------|---------------|
| **G1** | Stakeholder Vision | End of Skill 01–03 | Vision documented; stakeholder register complete; scope agreed with Out of Scope listed; domain confirmed |
| **G2** | Proven Architecture | End of Skill 04 | Interface spec complete; architecture strategy selected; key risks identified; no unresolved [CONTEXT-GAP] tags |
| **G3** | Requirements Complete | End of Skill 05 | All FRs have GWT stubs; all NFRs have SMART metrics; every FR traced to business goal; zero [V&V-FAIL] tags |
| **G4** | Logic Validated | End of Skill 06–07 | All LaTeX formulas verified; attribute mapping complete; no conflicts in Section 3.4 |
| **G5** | Audit Passed | End of Skill 08 | Zero [V&V-FAIL], [GLOSSARY-GAP], [TRACE-GAP], [SMART-FAIL] tags; SRS approved by consultant |
| **G6** | Production Ready | Post-testing | Test plan complete; no open must-fix defects; Go/No-Go approved in phase exit meeting |

**Anti-pattern:** Advancing to the next gate without resolving all tags from the current gate propagates defects downstream. One unresolved [V&V-FAIL] at G3 typically generates 5–10 downstream rework items.

## Quality Checklist

Run after generating all documents:

- [ ] All 7 documents generated (or justified why one was skipped)
- [ ] Each document stays under 500 lines (split if needed)
- [ ] Vision & Scope has measurable success metrics with numeric targets
- [ ] SRS has numbered requirement IDs (FR-MOD-001, NFR-PERF-001)
- [ ] SRS Section 1.2 includes an explicit `## Out of Scope` subsection
- [ ] Every NFR is SMART: Specific, Measurable, Achievable, Relevant, Time-bound — flag `[V&V-FAIL: SMART metric not defined]` for any that are not
- [ ] Every SHALL requirement has an inline acceptance stub: `**Acceptance:** Given [state], When [action], Then [outcome]`
- [ ] Requirements are prioritized using MoSCoW; time-sensitive features additionally scored with Cost of Delay
- [ ] SDP references the correct tech stack with version numbers
- [ ] SCMP describes the actual Git branching strategy being used
- [ ] QA Plan references `vibe-security-skill` for security quality gates
- [ ] Risk Register includes at least 8 pre-populated SaaS-specific risks
- [ ] Feasibility Study ends with a clear Go/No-Go/Conditional recommendation
- [ ] All documents cross-reference each other where relevant
- [ ] Multi-tenant isolation addressed in SRS, QA Plan, and Risk Plan
- [ ] Deployment environments (Windows dev, Ubuntu staging, Debian prod) documented in SDP
- [ ] No vague language ("user-friendly", "fast", "secure") -- all measurable
- [ ] Examples are tailored to the project's actual tech stack and domain

## Anti-Patterns (What NOT to Do)

| Anti-Pattern | Why It Fails | Do This Instead |
|-------------|-------------|-----------------|
| Skip feasibility, jump to coding | Wastes resources on unviable projects | Always do feasibility first |
| Copy-paste generic templates | Documents don't match your project | Customize every section to your context |
| Write SRS without stakeholder input | Requirements will be wrong | Use `project-requirements` skill first |
| No measurable success metrics | Can't tell if project succeeded | Define KPIs with specific numeric targets |
| Ignore multi-tenant requirements | Data leakage between tenants | Always include NFR-MT requirements |
| One massive document | Exceeds 500-line limit, hard to maintain | Split into index + sub-files |
| No risk register | Risks become surprises | Pre-populate with common SaaS risks |
| Skip configuration management | Deployment chaos, lost changes | Document branching, releases, migrations |
| Write plans and never update them | Plans become stale and useless | Review and update at each phase gate |
| Omit Out of Scope section from SRS | Scope creep is invisible | SRS Section 1.2 must include explicit `## Out of Scope` subsection |
| Vague NFRs without SMART metrics | Cannot verify or test non-functional requirements | Each NFR must be Specific, Measurable, Achievable, Relevant, Time-bound |
| No Given-When-Then acceptance stubs | Requirements written without verification linkage | Add inline `**Acceptance:** Given [state], When [action], Then [outcome]` to every SHALL requirement |
| Prioritize only by gut feel | High-value work delayed; delivery misaligned with business | Use Cost of Delay (CoD) for time-sensitive requirements alongside MoSCoW |

## Template Files

Each template provides the complete structure, section-by-section guidance, example excerpts, anti-patterns, and a quality checklist.

1. [Project Vision & Scope](templates/project-vision-scope.md)
2. [Software Development Plan](templates/software-development-plan.md)
3. [Configuration Management Plan](templates/configuration-management-plan.md)
4. [Quality Assurance Plan](templates/quality-assurance-plan.md)
5. [Risk Management Plan](templates/risk-management-plan.md)
6. [Software Requirements Specification](templates/software-requirements-spec.md)
7. [Feasibility Study Report](templates/feasibility-study-report.md)

---

**Back to:** [Skills Repository](../CLAUDE.md)
**Related:** [project-requirements](../project-requirements/SKILL.md) | [feature-planning](../feature-planning/SKILL.md) | [android-saas-planning](../android-saas-planning/SKILL.md)
**Last Updated:** 2026-03-15 (strengthened per Adjei 2023, Winston, Etter 2016, Cone 2023)
