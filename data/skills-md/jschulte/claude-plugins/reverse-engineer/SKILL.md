---
name: reverse-engineer
description: Deep codebase analysis to generate 11 comprehensive documentation files. Adapts based on path choice - Greenfield extracts business logic only (tech-agnostic), Brownfield extracts business logic + technical implementation (tech-prescriptive). This is Step 2 of 6 in the reverse engineering process.
---

# Reverse Engineer (Path-Aware)

**Step 2 of 6** in the Reverse Engineering to Spec-Driven Development process.

**Estimated Time:** 30-45 minutes
**Prerequisites:** Step 1 completed (`analysis-report.md` and path selection)
**Output:** 11 comprehensive documentation files in `docs/reverse-engineering/`

**Path-Dependent Behavior:**
- **Greenfield:** Extract business logic only (framework-agnostic)
- **Brownfield:** Extract business logic + technical implementation details

**Note:** Output is the same regardless of implementation framework (Spec Kit, BMAD, or BMAD Auto-Pilot). The framework choice only affects what happens after Gear 2.

---

## When to Use This Skill

Use this skill when:
- You've completed Step 1 (Initial Analysis) with path selection
- Ready to extract comprehensive documentation from code
- Path has been chosen (greenfield or brownfield)
- Preparing to create formal specifications

**Trigger Phrases:**
- "Reverse engineer the codebase"
- "Generate comprehensive documentation"
- "Extract business logic" (greenfield)
- "Document the full implementation" (brownfield)

---

## What This Skill Does

This skill performs deep codebase analysis and generates **11 comprehensive documentation files**.

**Content adapts based on your route (greenfield vs brownfield):**

### Path A: Greenfield (Business Logic Only)
- Focus on WHAT the system does
- Avoid framework/technology specifics
- Extract user stories, business rules, workflows
- Framework-agnostic functional requirements
- Can be implemented in any tech stack

### Path B: Brownfield (Business Logic + Technical)
- Focus on WHAT and HOW
- Document exact frameworks, libraries, versions
- Extract file paths, configurations, schemas
- Prescriptive technical requirements
- Enables `/speckit.analyze` validation

**11 Documentation Files Generated:**

1. **functional-specification.md** - Business logic, requirements, user stories, personas (+ tech details for brownfield)
2. **integration-points.md** - External services, APIs, dependencies, data flows (single source of truth)
3. **configuration-reference.md** - Config options (business-level for greenfield, all details for brownfield)
4. **data-architecture.md** - Data models, API contracts, domain boundaries (abstract for greenfield, schemas for brownfield)
5. **operations-guide.md** - Operational needs + scalability strategy (requirements for greenfield, current setup for brownfield)
6. **technical-debt-analysis.md** - Issues, improvements, migration priority matrix
7. **observability-requirements.md** - Monitoring needs (goals for greenfield, current state for brownfield)
8. **visual-design-system.md** - UI/UX patterns (requirements for greenfield, implementation for brownfield)
9. **test-documentation.md** - Testing requirements (targets for greenfield, current state for brownfield)
10. **business-context.md** - Product vision, personas, business goals, competitive landscape, stakeholder map
11. **decision-rationale.md** - Technology selection rationale, ADRs, design principles, trade-offs

---

## Configuration Check (FIRST STEP!)

**Load state file to check detection type and route:**

```bash
# Check what kind of application we're analyzing
DETECTION_TYPE=$(cat .stackshift-state.json | jq -r '.detection_type // .path')
echo "Detection: $DETECTION_TYPE"

# Check extraction approach
ROUTE=$(cat .stackshift-state.json | jq -r '.route // .path')
echo "Route: $ROUTE"

# Check spec output location (Greenfield only)
SPEC_OUTPUT=$(cat .stackshift-state.json | jq -r '.config.spec_output_location // "."')
echo "Writing specs to: $SPEC_OUTPUT"

# Create output directories if needed
if [ "$SPEC_OUTPUT" != "." ]; then
  mkdir -p "$SPEC_OUTPUT/docs/reverse-engineering"
  mkdir -p "$SPEC_OUTPUT/.specify/memory/specifications"
fi
```

**State file structure:**
```json
{
  "detection_type": "monorepo-service",  // What kind of app
  "route": "greenfield",                  // How to spec it
  "implementation_framework": "speckit",  // speckit, bmad, or bmad-autopilot
  "config": {
    "spec_output_location": "~/git/my-new-app",
    "build_location": "~/git/my-new-app",
    "target_stack": "Next.js 15..."
  }
}
```

**Capture commit hash for incremental updates:**
```bash
# Record current commit hash — used by /stackshift.refresh-docs for incremental updates
COMMIT_HASH=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
COMMIT_DATE=$(git log -1 --format=%ci 2>/dev/null || date -u +"%Y-%m-%d %H:%M:%S")
echo "Pinning docs to commit: $COMMIT_HASH"
```

**Output structure (same for all frameworks):**
```
docs/reverse-engineering/
├── .stackshift-docs-meta.json   # Commit hash + generation metadata
├── functional-specification.md
├── integration-points.md
├── configuration-reference.md
├── data-architecture.md
├── operations-guide.md
├── technical-debt-analysis.md
├── observability-requirements.md
├── visual-design-system.md
├── test-documentation.md
├── business-context.md
└── decision-rationale.md
```

**Extraction approach based on detection + route:**

| Detection Type | + Greenfield | + Brownfield |
|----------------|--------------|--------------|
| **Monorepo Service** | Business logic only (tech-agnostic) | Full implementation + shared packages (tech-prescriptive) |
| **Nx App** | Business logic only (framework-agnostic) | Full Nx/Angular implementation details |
| **Generic App** | Business logic only | Full implementation |

**How it works:**
- `detection_type` determines WHAT patterns to look for (shared packages, Nx project config, monorepo structure, etc.)
- `route` determines HOW to document them (tech-agnostic vs tech-prescriptive)

**Examples:**
- Monorepo Service + Greenfield → Extract what the service does (not React/Express specifics)
- Monorepo Service + Brownfield → Extract full Express routes, React components, shared utilities
- Nx App + Greenfield → Extract business logic (not Angular specifics)
- Nx App + Brownfield → Extract full Nx configuration, Angular components, project graph

---

## Process Overview

### Phase 1: Deep Codebase Analysis

**Approach depends on path:**

Use the Task tool with `subagent_type=stackshift:code-analyzer` (or `Explore` as fallback) to analyze:

#### 1.1 Backend Analysis
- All API endpoints (method, path, auth, params, purpose)
- Data models (schemas, types, interfaces, fields)
- Configuration (env vars, config files, settings)
- External integrations (APIs, services, databases)
- Business logic (services, utilities, algorithms)

#### 1.2 Frontend Analysis
- All pages/routes (path, purpose, auth requirement)
- Components catalog (layout, form, UI components)
- State management (store structure, global state)
- API client (how frontend calls backend)
- Styling (design system, themes, component styles)

#### 1.3 Infrastructure Analysis
- Deployment (IaC tools, configuration)
- CI/CD (pipelines, workflows)
- Hosting (cloud provider, services)
- Database (type, schema, migrations)
- Storage (object storage, file systems)

#### 1.4 Testing Analysis
- Test files (location, framework, coverage)
- Test types (unit, integration, E2E)
- Coverage estimates (% covered)
- Test data (mocks, fixtures, seeds)

#### 1.5 Business Context Analysis
- README, CONTRIBUTING, marketing pages, landing pages
- Package descriptions, repository metadata
- Comment patterns indicating user-facing features
- Error messages and user-facing strings
- Naming conventions revealing domain concepts
- Git history for decision archaeology

#### 1.6 Decision Archaeology
- Package.json / go.mod / requirements.txt for technology choices
- Config files (tsconfig, eslint, prettier) for design philosophy
- CI/CD configuration for deployment decisions
- Git blame on key architectural files
- Comments with "why" explanations (TODO, HACK, FIXME, NOTE)
- Rejected alternatives visible in git history or comments

### Phase 2: Generate Documentation

Create `docs/reverse-engineering/` directory and generate all 11 documentation files.

**Step 2.1: Write metadata file FIRST**

Before writing any docs, create the metadata file that tracks the commit hash:

```bash
COMMIT_HASH=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
COMMIT_DATE=$(git log -1 --format=%ci 2>/dev/null || date -u +"%Y-%m-%d %H:%M:%S")
GENERATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
```

Write `docs/reverse-engineering/.stackshift-docs-meta.json`:
```json
{
  "commit_hash": "<COMMIT_HASH>",
  "commit_date": "<COMMIT_DATE>",
  "generated_at": "<GENERATED_AT>",
  "doc_count": 11,
  "route": "<greenfield|brownfield>",
  "docs": {
    "functional-specification.md": { "generated_at": "<GENERATED_AT>", "commit_hash": "<COMMIT_HASH>" },
    "integration-points.md": { "generated_at": "<GENERATED_AT>", "commit_hash": "<COMMIT_HASH>" },
    "configuration-reference.md": { "generated_at": "<GENERATED_AT>", "commit_hash": "<COMMIT_HASH>" },
    "data-architecture.md": { "generated_at": "<GENERATED_AT>", "commit_hash": "<COMMIT_HASH>" },
    "operations-guide.md": { "generated_at": "<GENERATED_AT>", "commit_hash": "<COMMIT_HASH>" },
    "technical-debt-analysis.md": { "generated_at": "<GENERATED_AT>", "commit_hash": "<COMMIT_HASH>" },
    "observability-requirements.md": { "generated_at": "<GENERATED_AT>", "commit_hash": "<COMMIT_HASH>" },
    "visual-design-system.md": { "generated_at": "<GENERATED_AT>", "commit_hash": "<COMMIT_HASH>" },
    "test-documentation.md": { "generated_at": "<GENERATED_AT>", "commit_hash": "<COMMIT_HASH>" },
    "business-context.md": { "generated_at": "<GENERATED_AT>", "commit_hash": "<COMMIT_HASH>" },
    "decision-rationale.md": { "generated_at": "<GENERATED_AT>", "commit_hash": "<COMMIT_HASH>" }
  }
}
```

**Step 2.2: Add metadata header to each doc**

Every generated doc should start with this header (after the title):

```markdown
# [Document Title]

> **Generated by StackShift** | Commit: `<short-hash>` | Date: `<GENERATED_AT>`
> Run `/stackshift.refresh-docs` to update with latest changes.
```

This gives readers instant visibility into doc freshness. The metadata JSON file is what the refresh command actually reads.

---

## Output Files

All 11 documentation files are written to `docs/reverse-engineering/` regardless of implementation framework choice.

---

### 1. functional-specification.md
**Focus:** Business logic, WHAT the system does (not HOW)

**Sections:**
- Executive Summary (purpose, users, value)
- **User Personas** (inferred from user-facing features, auth roles, UI flows)
  - For each persona: Name, Role, Goals, Pain Points, Key Workflows
  - Greenfield: Infer from feature set and user stories
  - Brownfield: Infer from auth roles, UI routes, API consumers
- **Product Positioning** (inferred from README, package description, marketing copy)
  - What problem does this solve?
  - Who is the target audience?
  - What makes this approach unique?
- Functional Requirements (FR-001, FR-002, ...)
- User Stories (P0/P1/P2/P3 priorities, tied to personas)
- Non-Functional Requirements (NFR-001, ...)
- Business Rules (validation, authorization, workflows)
- System Boundaries (scope, integrations)
- Success Criteria (measurable outcomes)

**Critical:** Framework-agnostic, testable, measurable. Personas and positioning may be partially inferred — mark uncertain items with `[INFERRED]`.

### 2. integration-points.md
**Single source of truth** for all external dependencies and data flows:

**Sections:**
- **External Services & APIs Consumed**
  - For each: Service name, purpose, authentication method, endpoints used
  - SDKs and client libraries in use
  - Rate limits and quotas (if documented)
- **Internal Service Dependencies** (for microservices/monorepos)
  - Service-to-service calls
  - Shared databases or message queues
  - Event bus / pub-sub topics
- **Data Flow Diagrams** (Mermaid)
  - Request flows for key user journeys
  - Data pipeline flows (ETL, streaming)
  - Event propagation paths
- **Authentication & Authorization Flows**
  - OAuth/OIDC providers
  - Token lifecycle
  - Permission model
- **Third-Party SDK Usage**
  - Payment processors, email providers, analytics
  - Version pinning and update strategy
- **Webhook & Event Integrations**
  - Incoming webhooks (endpoints, payloads)
  - Outgoing events (triggers, formats)
  - Retry and failure handling

### 3. configuration-reference.md
**Complete inventory** of all configuration:
- Environment variables
- Config file options
- Feature flags
- Secrets and credentials (how managed)
- Default values

### 4. data-architecture.md
**All data models and API contracts:**
- Data models (with field types, constraints, relationships)
- API endpoints (request/response formats)
- JSON Schemas
- GraphQL schemas (if applicable)
- Database ER diagram (textual)
- **Domain Model / Bounded Contexts**
  - Identify natural domain boundaries in the codebase
  - Map aggregates and entities per domain
  - Document cross-domain relationships and dependencies
  - Greenfield: Abstract domain model (implementation-agnostic)
  - Brownfield: Current domain boundaries with file/module mapping

### 5. operations-guide.md
**How to deploy and maintain:**
- Deployment procedures
- Infrastructure overview
- Monitoring and alerting
- Backup and recovery
- Troubleshooting runbooks
- **Scalability & Growth Strategy**
  - Current bottlenecks and capacity limits
  - Horizontal vs vertical scaling opportunities
  - Caching strategy (current and recommended)
  - Database scaling approach (read replicas, sharding, partitioning)
  - CDN and edge deployment opportunities
  - Greenfield: Scalability requirements and targets
  - Brownfield: Current capacity + recommended evolution

### 6. technical-debt-analysis.md
**Issues and improvements:**
- Code quality issues
- Missing tests
- Security vulnerabilities
- Performance bottlenecks
- Refactoring opportunities
- **Migration Priority Matrix**
  - Categorize all debt items by: Impact (High/Medium/Low) x Effort (High/Medium/Low)
  - Quadrant mapping:
    - **Quick Wins**: High Impact + Low Effort (do first)
    - **Strategic**: High Impact + High Effort (plan carefully)
    - **Fill-ins**: Low Impact + Low Effort (do opportunistically)
    - **Deprioritize**: Low Impact + High Effort (defer or skip)
  - Dependency ordering: Which items must be done before others?
  - Estimated effort per item (hours/days)
  - Suggested migration phases with ordering

### 7. observability-requirements.md
**Logging, monitoring, alerting:**
- What to log (events, errors, metrics)
- Monitoring requirements (uptime, latency, errors)
- Alerting rules and thresholds
- Debugging capabilities

### 8. visual-design-system.md
**UI/UX patterns:**
- Component library
- Design tokens (colors, typography, spacing)
- Responsive breakpoints
- Accessibility standards
- User flows

### 9. test-documentation.md
**Testing requirements:**
- Test strategy
- Coverage requirements
- Test patterns and conventions
- E2E scenarios
- Performance testing

### 10. business-context.md
**Product vision and business context — the "why" behind the system.**

This document captures context that cannot be fully determined from code alone. Use all available signals (README, comments, naming, architecture, user-facing strings, marketing pages) to infer as much as possible. Mark uncertain items with `[INFERRED]` and genuinely unknown items with `[NEEDS USER INPUT]`.

**Sections:**

- **Product Vision**
  - What problem does this product solve?
  - What is the core value proposition?
  - What would the elevator pitch be?
  - Infer from: README, package description, landing pages, app title/tagline

- **Target Users & Personas**
  - Primary persona (the main user — infer from UI flows, auth roles)
  - Secondary personas (admins, API consumers, operators)
  - For each: Goals, pain points, technical sophistication
  - Infer from: Auth roles, UI complexity, API design, error messages

- **Business Goals & Success Metrics**
  - What does success look like for this product?
  - Revenue model (if detectable: SaaS, marketplace, enterprise, etc.)
  - Growth metrics (users, transactions, data volume)
  - Infer from: Pricing pages, subscription models, analytics integrations, billing code

- **Competitive Landscape** `[INFERRED]`
  - What category does this product compete in?
  - What alternatives likely exist?
  - What differentiates this approach?
  - Infer from: Feature set, technology choices, target market signals

- **Stakeholder Map**
  - End users (who uses the product)
  - Operators (who deploys and maintains)
  - Decision makers (who approves changes — infer from approval workflows, CODEOWNERS)
  - API consumers (downstream systems)
  - Infer from: Auth roles, admin panels, API keys, deployment scripts

- **Business Constraints**
  - Compliance & regulatory (HIPAA, GDPR, SOC2 — infer from data handling patterns)
  - Budget indicators (cloud provider choices, self-hosted vs managed)
  - Team size indicators (CODEOWNERS, commit patterns, PR templates)
  - Timeline pressure (TODO density, shortcut patterns, technical debt level)

- **Market Context** `[INFERRED]`
  - Industry vertical (healthcare, fintech, e-commerce, developer tools, etc.)
  - Market maturity signals
  - Infer from: Domain vocabulary, data models, compliance patterns

**Greenfield vs Brownfield:**
- Greenfield: Focus on what the product DOES and WHO it serves (inform new implementation choices)
- Brownfield: Focus on what the product DOES, WHO it serves, and WHY it was built this way (inform maintenance decisions)

### 11. decision-rationale.md
**Technology selection rationale and architectural decisions — the "why" behind technical choices.**

This document captures the reasoning behind key technical decisions. Much of this can be inferred from configuration files, dependency choices, and code patterns. Mark inferred items with `[INFERRED]`.

**Sections:**

- **Technology Selection**
  - **Language**: Why this language? (Infer from ecosystem, team patterns, problem domain fit)
  - **Framework**: Why this framework? (Infer from features used, configuration complexity, alternatives in package.json history)
  - **Database**: Why this database? (Infer from data patterns, query complexity, scaling needs)
  - **Infrastructure**: Why this deployment model? (Infer from IaC files, cloud provider, container setup)
  - For each: Document what was chosen, why it fits, and what alternatives were likely considered

- **Architectural Decisions (ADR Format)**
  - Extract key decisions visible in the codebase
  - For each decision:
    - **Context**: What problem was being solved?
    - **Decision**: What was chosen?
    - **Rationale**: Why was this the right choice? `[INFERRED]`
    - **Consequences**: What trade-offs resulted?
  - Example decisions to look for:
    - Monolith vs microservices (infer from project structure)
    - REST vs GraphQL vs gRPC (infer from API implementation)
    - SQL vs NoSQL (infer from database choice)
    - Server-side vs client-side rendering (infer from framework)
    - Authentication approach (infer from auth implementation)
    - State management approach (infer from frontend architecture)
    - Testing strategy (infer from test framework and patterns)

- **Design Principles** (inferred from code patterns)
  - What values does the codebase prioritize?
  - Examples: "Type safety over convenience" (strict TypeScript), "Convention over configuration" (Rails/Next.js), "Explicit over implicit" (Go-style error handling)
  - Infer from: Linter config strictness, type system usage, error handling patterns, abstraction levels

- **Trade-offs Made**
  - What was sacrificed for what? Cross-reference with technical-debt-analysis.md
  - Examples: "Speed over safety" (few tests), "Simplicity over scalability" (monolith), "Control over convenience" (no ORM)
  - Look for: Missing features that similar products have, unusually simple or complex implementations, comments explaining shortcuts

- **Historical Context** (if detectable)
  - Major refactors visible in git history
  - Deprecated patterns still present
  - Migration artifacts (old config files, compatibility layers)
  - Infer from: Git history, deprecated code, TODO/FIXME comments, version suffixes

**Greenfield vs Brownfield:**
- Greenfield: Focus on WHAT decisions were made and WHY — helps inform whether to repeat or diverge
- Brownfield: Focus on WHAT, WHY, and WHAT TO CHANGE — helps inform evolution strategy

---

## Success Criteria

- ✅ `docs/reverse-engineering/` directory created
- ✅ All 11 documentation files generated
- ✅ Comprehensive coverage of all application aspects
- ✅ Framework-agnostic functional specification (for greenfield)
- ✅ Complete data model documentation
- ✅ Business context captured with clear `[INFERRED]` / `[NEEDS USER INPUT]` markers
- ✅ Decision rationale documented with ADR format
- ✅ Integration points fully mapped with data flow diagrams
- ✅ `.stackshift-docs-meta.json` created with commit hash for incremental updates
- ✅ Each doc has metadata header with commit hash and generation date
- ✅ Ready to proceed to Step 3 (Create Specifications) or BMAD Synthesize

---

## Next Step

Once all documentation is generated and reviewed:

**For GitHub Spec Kit** (`implementation_framework: speckit`):
- Proceed to **Step 3: Create Specifications** - Use `/stackshift.create-specs` to transform docs into `.specify/` specs

**For BMAD Method** (`implementation_framework: bmad`):
- Proceed to **Step 6: Implementation** which will hand off to BMAD's `*workflow-init`
- BMAD's PM and Architect agents will use the reverse-engineering docs as rich context
- They will collaboratively create the PRD and architecture through conversation

**For BMAD Auto-Pilot** (`implementation_framework: bmad-autopilot`):
- Proceed to `/stackshift.bmad-synthesize` to auto-generate BMAD artifacts
- Choose mode: YOLO (fully automatic), Guided (ask on ambiguities), or Interactive (full conversation)
- The 11 reverse-engineering docs provide ~90% of what BMAD needs

---

## Important Guidelines

### Framework-Agnostic Documentation

**DO:**
- Describe WHAT, not HOW
- Focus on business logic and requirements
- Use generic terms (e.g., "HTTP API" not "Express routes")

**DON'T:**
- Hard-code framework names in functional specs
- Describe implementation details in requirements
- Mix business logic with technical implementation

### Inference Guidelines (for business-context.md and decision-rationale.md)

**DO:**
- Use all available signals: README, comments, naming, config, git history
- Mark confidence levels: no marker = confident, `[INFERRED]` = reasonable inference, `[NEEDS USER INPUT]` = genuinely unknown
- Cross-reference between docs (e.g., tech debt informs trade-offs)
- Be specific about WHAT evidence supports each inference

**DON'T:**
- Fabricate business goals with no supporting evidence
- Guess at competitive landscape without domain signals
- State inferences as facts without marking them
- Skip a section just because it requires inference — attempt it and mark confidence

### Completeness

Use the Explore agent to ensure you find:
- ALL API endpoints (not just the obvious ones)
- ALL data models (including DTOs, types, interfaces)
- ALL configuration options (check multiple files)
- ALL external integrations
- ALL user-facing strings and error messages (for persona/context inference)
- ALL config files (for decision rationale inference)

### Quality Standards

Each document must be:
- **Comprehensive** - Nothing important missing
- **Accurate** - Reflects actual code, not assumptions
- **Organized** - Clear sections, easy to navigate
- **Actionable** - Can be used to rebuild the system
- **Honest** - Clearly marks inferred vs verified information

---

## Technical Notes

- Use Task tool with `subagent_type=stackshift:code-analyzer` for path-aware extraction
- Fallback to `subagent_type=Explore` if StackShift agent not available
- Parallel analysis: Run backend, frontend, infrastructure, business context, and decision archaeology concurrently
- Use multiple rounds of exploration for complex codebases
- Cross-reference findings across different parts of the codebase
- The `stackshift:code-analyzer` agent understands greenfield vs brownfield routes automatically

---

**Remember:** This is Step 2 of 6. The documentation you generate here will be transformed into formal specifications in Step 3, or fed directly into BMAD artifact generation via `/stackshift.bmad-synthesize`.
