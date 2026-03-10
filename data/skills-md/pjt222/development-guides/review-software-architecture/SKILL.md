---
name: review-software-architecture
description: >
  Review software architecture for coupling, cohesion, SOLID principles, API
  design, scalability, and technical debt. Covers system-level evaluation,
  architecture decision record review, and improvement recommendations. Use
  when evaluating a proposed architecture before implementation, assessing an
  existing system for scalability or security, reviewing ADRs, performing a
  technical debt assessment, or evaluating readiness for significant scale-up.
license: MIT
allowed-tools: Read Grep Glob Bash WebFetch
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: review
  complexity: advanced
  language: multi
  tags: architecture, solid, coupling, cohesion, api-design, scalability, tech-debt, adr
---

# Review Software Architecture

Evaluate software architecture at the system level for quality attributes, design principles adherence, and long-term maintainability.

## When to Use

- Evaluating a proposed architecture before implementation begins
- Assessing an existing system for scalability, maintainability, or security
- Reviewing Architecture Decision Records (ADRs) for a project
- Performing a technical debt assessment
- Evaluating whether a system is ready for a significant scale-up or feature expansion
- Differentiating from line-level code review (which focuses on PR-level changes)

## Inputs

- **Required**: System codebase or architecture documentation (diagrams, ADRs, README)
- **Required**: Context about the system's purpose, scale, and constraints
- **Optional**: Non-functional requirements (latency, throughput, availability targets)
- **Optional**: Team size and skill composition
- **Optional**: Technology constraints or preferences
- **Optional**: Known pain points or areas of concern

## Procedure

### Step 1: Understand the System Context

Map the system boundaries and interfaces:

```markdown
## System Context
- **Name**: [System name]
- **Purpose**: [One-line description]
- **Users**: [Who uses it and how]
- **Scale**: [Requests/sec, data volume, user count]
- **Age**: [Years in production, major versions]
- **Team**: [Size, composition]

## External Dependencies
| Dependency | Type | Criticality | Notes |
|-----------|------|-------------|-------|
| PostgreSQL | Database | Critical | Primary data store |
| Redis | Cache | High | Session store + caching |
| Stripe | External API | Critical | Payment processing |
| S3 | Object storage | High | File uploads |
```

**Expected:** Clear picture of what the system does and what it depends on.
**On failure:** If architecture documentation is missing, derive the context from code structure, configs, and deployment files.

### Step 2: Evaluate Structural Quality

#### Coupling Assessment
Examine how tightly modules depend on each other:

- [ ] **Dependency direction**: Do dependencies flow in one direction (layered) or circular?
- [ ] **Interface boundaries**: Are modules connected through defined interfaces/contracts or direct implementation references?
- [ ] **Shared state**: Is mutable state shared between modules?
- [ ] **Database coupling**: Do multiple services read/write the same tables directly?
- [ ] **Temporal coupling**: Must operations happen in a specific order without explicit orchestration?

```bash
# Detect circular dependencies (JavaScript/TypeScript)
npx madge --circular src/

# Detect import patterns (Python)
# Look for deep cross-package imports
grep -r "from app\." --include="*.py" | sort | uniq -c | sort -rn | head -20
```

#### Cohesion Assessment
Evaluate whether each module has a single, clear responsibility:

- [ ] **Module naming**: Does the name accurately describe what the module does?
- [ ] **File size**: Are files or classes excessively large (>500 lines suggests multiple responsibilities)?
- [ ] **Change frequency**: Do unrelated features require changes to the same module?
- [ ] **God objects**: Are there classes/modules that everything depends on?

| Coupling Level | Description | Example |
|---------------|-------------|---------|
| Low (good) | Modules communicate through interfaces | Service A calls Service B's API |
| Medium | Modules share data structures | Shared DTO/model library |
| High (concern) | Modules reference each other's internals | Direct database access across modules |
| Pathological | Modules modify each other's internal state | Global mutable state |

**Expected:** Coupling and cohesion assessed with specific examples from the codebase.
**On failure:** If the codebase is too large for manual review, sample 3-5 key modules and the most-changed files.

### Step 3: Assess SOLID Principles

| Principle | Question | Red Flags |
|-----------|----------|-----------|
| **S**ingle Responsibility | Does each class/module have one reason to change? | Classes with >5 public methods on unrelated concerns |
| **O**pen/Closed | Can behavior be extended without modifying existing code? | Frequent modifications to core classes for each new feature |
| **L**iskov Substitution | Can subtypes replace their base types without breaking behavior? | Type checks (`instanceof`) scattered through consumer code |
| **I**nterface Segregation | Are interfaces focused and minimal? | "Fat" interfaces where consumers implement unused methods |
| **D**ependency Inversion | Do high-level modules depend on abstractions, not details? | Direct instantiation of infrastructure classes in business logic |

```markdown
## SOLID Assessment
| Principle | Status | Evidence | Impact |
|-----------|--------|----------|--------|
| SRP | Concern | UserService handles auth, profile, notifications, and billing | High — changes to billing risk breaking auth |
| OCP | Good | Plugin system for payment providers | Low |
| LSP | Good | No type-checking anti-patterns found | Low |
| ISP | Concern | IRepository has 15 methods, most implementors use 3-4 | Medium |
| DIP | Concern | Controllers directly instantiate database repositories | Medium |
```

**Expected:** Each principle assessed with at least one specific example.
**On failure:** Not all principles apply equally to every architecture style. Note when a principle is less relevant (e.g., ISP matters less in functional codebases).

### Step 4: Review API Design

For systems that expose APIs (REST, GraphQL, gRPC):

- [ ] **Consistency**: Naming conventions, error formats, pagination patterns uniform
- [ ] **Versioning**: Strategy exists and is applied (URL, header, content negotiation)
- [ ] **Error handling**: Error responses are structured, consistent, and don't leak internals
- [ ] **Authentication/Authorization**: Properly enforced at the API layer
- [ ] **Rate limiting**: Protection against abuse
- [ ] **Documentation**: OpenAPI/Swagger, GraphQL schema, or protobuf definitions maintained
- [ ] **Idempotency**: Mutating operations (POST/PUT) handle retries safely

```markdown
## API Design Review
| Aspect | Status | Notes |
|--------|--------|-------|
| Naming consistency | Good | RESTful resource naming throughout |
| Versioning | Concern | No versioning strategy — breaking changes affect all clients |
| Error format | Good | RFC 7807 Problem Details used consistently |
| Auth | Good | JWT with role-based scopes |
| Rate limiting | Missing | No rate limiting on any endpoint |
| Documentation | Concern | OpenAPI spec exists but 6 months out of date |
```

**Expected:** API design reviewed against common standards with specific findings.
**On failure:** If no API is exposed, skip this step and focus on internal module interfaces.

### Step 5: Evaluate Scalability and Reliability

- [ ] **Statelessness**: Can the application scale horizontally (no local state)?
- [ ] **Database scalability**: Are queries indexed? Is the schema suitable for the data volume?
- [ ] **Caching strategy**: Is caching applied at appropriate layers (database, application, CDN)?
- [ ] **Failure handling**: What happens when a dependency is unavailable (circuit breaker, retry, fallback)?
- [ ] **Observability**: Are logs, metrics, and traces implemented?
- [ ] **Data consistency**: Is eventual consistency acceptable or is strong consistency required?

**Expected:** Scalability and reliability assessed relative to stated non-functional requirements.
**On failure:** If non-functional requirements are undocumented, recommend defining them as a first step.

### Step 6: Assess Technical Debt

```markdown
## Technical Debt Inventory
| Item | Severity | Impact | Estimated Effort | Recommendation |
|------|----------|--------|-----------------|----------------|
| No database migrations | High | Schema changes are manual and error-prone | 1 sprint | Adopt Alembic/Flyway |
| Monolithic test suite | Medium | Tests take 45 min, developers skip them | 2 sprints | Split into unit/integration/e2e |
| Hardcoded config values | Medium | Environment-specific values in source code | 1 sprint | Extract to env vars/config service |
| No CI/CD pipeline | High | Manual deployment prone to errors | 1 sprint | Set up GitHub Actions |
```

**Expected:** Technical debt catalogued with severity, impact, and effort estimates.
**On failure:** If the debt inventory is overwhelming, prioritize the top 5 items by impact/effort ratio.

### Step 7: Review Architecture Decision Records (ADRs)

If ADRs exist, evaluate:
- [ ] Decisions have clear context (what problem was being solved)
- [ ] Alternatives were considered and documented
- [ ] Trade-offs are explicit
- [ ] Decisions are still current (not superseded without documentation)
- [ ] New significant decisions have ADRs

If ADRs don't exist, recommend establishing them for key decisions.

### Step 8: Write the Architecture Review

```markdown
## Architecture Review Report

### Executive Summary
[2-3 sentences: overall health, key concerns, recommended actions]

### Strengths
1. [Specific architectural strength with evidence]
2. ...

### Concerns (by severity)

#### Critical
1. **[Title]**: [Description, impact, recommendation]

#### Major
1. **[Title]**: [Description, impact, recommendation]

#### Minor
1. **[Title]**: [Description, recommendation]

### Technical Debt Summary
[Top 5 debt items with prioritized recommendations]

### Recommended Next Steps
1. [Actionable recommendation with clear scope]
2. ...
```

**Expected:** Review report is actionable with prioritized recommendations.
**On failure:** If the review is time-boxed, clearly state what was covered and what remains unassessed.

## Validation

- [ ] System context documented (purpose, scale, dependencies, team)
- [ ] Coupling and cohesion assessed with specific code examples
- [ ] SOLID principles evaluated where applicable
- [ ] API design reviewed (if applicable)
- [ ] Scalability and reliability assessed against requirements
- [ ] Technical debt catalogued and prioritized
- [ ] ADRs reviewed or their absence noted
- [ ] Recommendations are specific, prioritized, and actionable

## Common Pitfalls

- **Reviewing code instead of architecture**: This skill is about system-level design, not line-level code quality. Use `code-reviewer` for PR-level feedback.
- **Prescribing a specific technology**: Architecture reviews should identify problems, not mandate specific tools unless there's a clear technical reason.
- **Ignoring team context**: The "best" architecture for a 3-person team differs from a 30-person team. Consider organizational constraints.
- **Perfectionism**: Every system has tech debt. Focus on debt that is actively causing pain or blocking future work.
- **Assuming scale**: Don't recommend distributed systems for an app serving 100 users. Match architecture to actual requirements.

## Related Skills

- `security-audit-codebase` — security-focused code and configuration review
- `configure-git-repository` — repository structure and conventions
- `design-serialization-schema` — data schema design and evolution
- `review-data-analysis` — review of analytical correctness (complementary perspective)
