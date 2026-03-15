---
name: sdlc-testing
description: "Generate Testing & Quality documentation for SDLC projects. Compliant with BS ISO/IEC/IEEE 29119-3:2013 (supersedes IEEE 829:2008 and BS 7925-2:1998). Covers Software Test Plan, Test Case Specifications (with normative 29119-3 fields), V&V Plan, Validation Test Report, Incident Report, Test Completion Report, and Peer Review Reports. Use when establishing testing strategy, creating test documentation, or conducting quality validation."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# SDLC Testing Skill

Generate a complete **Testing & Quality** documentation suite for software development projects. This skill produces 5 documents that establish the testing baseline, define test cases, verify and validate the system, report results, and standardize peer reviews.

## When to Use

- Establishing a **testing strategy** for a SaaS project
- Writing **formal test plans** aligned with IEEE 829
- Creating **test case specifications** with traceability to requirements
- Planning **verification and validation** activities (V&V)
- Documenting **validation test results** for release decisions
- Standardizing **peer review and code inspection** processes
- Preparing for **phase gate reviews** that require test evidence

## When NOT to Use

- **Writing actual test code** (unit tests, integration tests) -- use `android-tdd` skill instead
- **Validating AI-generated code** -- use `ai-error-handling` skill (5-layer validation)
- **Planning security testing only** -- use `vibe-security-skill` for security patterns
- **Planning a single feature** -- use `feature-planning` skill (includes testing strategy)
- **Creating project plans** -- use `sdlc-planning` skill (SDP, QA Plan, SRS)
- **Designing architecture** -- use `sdlc-design` skill

## Document Inventory

| # | Document | File | Purpose | Audience | Phase |
|---|----------|------|---------|----------|-------|
| 1 | Software Test Plan | `templates/software-test-plan.md` | Testing strategy, tools, environments, schedule, completion criteria | QA leads, PMs, devs | After SRS + SDD |
| 2 | Test Case Specifications | `templates/test-case-specifications.md` | Normative 29119-3 test cases: ID, objective, priority, traceability, preconditions, input, expected result | Test engineers, devs | During development |
| 3 | Validation & Verification Plan | `templates/validation-verification-plan.md` | V&V approach (built right + right product) | QA mgrs, PMs, compliance | After SRS + SDD |
| 4 | Validation Test Report | `templates/validation-test-report.md` | Test execution results and Go/No-Go release decision | PMs, stakeholders, QA | Before release |
| 5 | Peer Review Report | `templates/peer-review-report.md` | Code, design, and document review findings | Dev team, tech leads | Throughout SDLC |
| 6 | Incident Report | `templates/incident-report.md` | Anomaly record: ID, timing, context, description, impact, urgency, status | QA, dev leads | During execution |
| 7 | Test Completion Report | `templates/test-completion-report.md` | Test summary, deviations, completion criteria met, residual risks, lessons learned | PMs, stakeholders, compliance | End of test phase |

## Standards Basis

This skill generates documentation compliant with **BS ISO/IEC/IEEE 29119-3:2013**, the current international standard for software test documentation. It supersedes IEEE 829:2008 and BS 7925-2:1998. Key structural difference: 29119-3 defines a strict document hierarchy — Organizational Test Strategy → Project Test Plan → Sub-process Test Plans → Test Design Specification → Test Case Specification → Incident Report → Test Completion Report. Annex T provides clause-level cross-walks from legacy standards for migration.

**Normative Test Case Fields (BS 29119-3 §7.3):** Every test case must include: (1) Unique ID, (2) Objective/Purpose, (3) Priority (H/M/L), (4) Traceability to requirement ID, (5) Preconditions (exact system state), (6) Input (exact stimulus), (7) Expected Result (deterministic pass/fail — the test oracle), (8) Actual Result (populated during execution), (9) Test Result (Pass / Incident Report number).

**Test Oracle Rule:** Every expected result must be specific enough to yield an unambiguous Pass or Fail without interpretation. If the expected result depends on judgment ("the response looks reasonable"), the requirement has not been adequately specified — flag `[VERIFIABILITY-FAIL]` and return to Skill 05 for clarification.

## Testing Philosophy

### TDD-First Development

All production code follows the **Red-Green-Refactor** cycle. Tests are written before implementation. Reference the `android-tdd` skill for the complete TDD workflow.

### Test Pyramid (70/20/10)

```
        /  UI/E2E  \       10% - Compose Testing, Espresso, browser E2E
       /------------\
      / Integration  \     20% - Room+MockWebServer, API with real DB
     /----------------\
    /   Unit Tests     \   70% - JUnit 5, MockK, PHPUnit (fast, isolated)
   /====================\
```

### Shift-Left Testing

Move testing activities as early as possible in the SDLC:

| Activity | Traditional Phase | Shift-Left Phase |
|----------|------------------|-----------------|
| Unit testing | After coding | During coding (TDD) |
| Security testing | Pre-release | During design + development |
| Performance testing | Pre-release | During development (benchmarks) |
| Code review | After feature complete | Per-commit (PR-based) |
| Requirements review | After SRS finalized | During requirements gathering |

## Generation Workflow

Generate documents in this order. Each builds on the previous.

```
Prerequisite: SRS from sdlc-planning + SDD from sdlc-design
    |
Step 1: Software Test Plan (overall strategy)
    |
Step 2: Validation & Verification Plan (V&V approach)
    |
Step 3: Test Case Specifications (detailed test cases)
    |
    [--- Development & testing execution happens here ---]
    |
Step 4: Peer Review Reports (during development)
    |
Step 5: Validation Test Report (before release)
```

### Prerequisites

| Input | Source | Required? |
|-------|--------|-----------|
| Software Requirements Spec (SRS) | `sdlc-planning` output | Yes |
| Software Design Document (SDD) | `sdlc-design` output | Recommended |
| Quality Assurance Plan | `sdlc-planning` output | Recommended |
| Risk Management Plan | `sdlc-planning` output | Recommended |
| Feature specifications | `feature-planning` output | If feature-level |

## Testing Layers Overview

### Unit Testing

| Platform | Framework | Scope | Speed |
|----------|-----------|-------|-------|
| Android | JUnit 5 + MockK + Turbine | ViewModels, UseCases, Repositories, Mappers | <1ms each |
| PHP | PHPUnit | Services, validators, business logic, helpers | <10ms each |

### Integration Testing

| Platform | Framework | Scope |
|----------|-----------|-------|
| Android | Room in-memory DB + MockWebServer | DAO queries, API contracts, auth flows |
| PHP | PHPUnit + real MySQL test DB | API endpoints, stored procedures, multi-table ops |

### UI / E2E Testing

| Platform | Framework | Scope |
|----------|-----------|-------|
| Android | Compose Testing + Espresso | Screen rendering, navigation, user flows |
| Web | Browser testing (manual + automated) | CRUD workflows, form validation, responsive layout |

### User Acceptance Testing (UAT)

Distinguish Alpha and Beta testing explicitly in the Test Plan:

| Stage | Location | Testers | Focus |
|-------|----------|---------|-------|
| **Alpha** | Controlled environment (internal/QA lab) | Internal testers, stakeholders | Functional correctness, defect discovery |
| **Beta** | Real-world environment (staging/limited production) | Selected external users | Real-world usability, edge-case discovery, performance under real load |

### Seven-Step Defect Resolution Protocol *(Rex Black, 2009)*

Every bug report triggers this handoff sequence. The boundary between Step 3 and Step 4 is the critical management line — testers own isolation; developers own debugging.

| Step | Owner | Action |
|------|-------|--------|
| 1 | Tester | **Reproduce** — determine exact minimal sequence; check for intermittence |
| 2 | Tester | **Discriminate** — test bug or system bug? |
| 3 | Tester | **Isolate** — identify external factors (config, data, workflows) affecting symptoms |
| 4 | Developer | **Root cause** — find cause in code, hardware, network, or environment |
| 5 | Developer | **Repair** — fix without introducing new problems |
| 6 | Developer | **Verify fix** — confirm the fix is clean before handoff |
| 7 | Tester | **Confirm + Regression** — does it pass the failing test? Does everything else still work? |

If the fix fails Step 7: reopen the bug report. If it passes but breaks a different test: open a new bug report.

### Regression Testing

Regression testing is a first-class test type and must be documented separately in the Test Plan. Define: the regression suite scope (which previously-passing test cases are re-run), the trigger conditions (every PR merge, every release candidate), and the acceptable pass rate before proceeding.

### Test Data Management

The Test Plan must include a `## Test Data Management` section covering: how test fixtures are created, how tenant isolation is maintained in test data (separate `franchise_id` values per test scenario), how sensitive data is anonymized in non-production environments, and who owns test data lifecycle.

#### Test Data Readiness Report (B-08)

Before test execution begins, confirm:
- [ ] Test fixtures created for all scenarios (normal, boundary, error)
- [ ] Tenant isolation verified — each test scenario uses a distinct `franchise_id` (or equivalent)
- [ ] Sensitive production data anonymised in all non-production environments
- [ ] Test data owner identified and data lifecycle documented
- [ ] Rollback/reset procedure defined for test data after execution

#### Test Environment Readiness Report (B-08)

Before test execution begins, confirm:
- [ ] All hardware/software components match production specifications
- [ ] All software components under formal CM control with release notes
- [ ] Test environment access provisioned for all testers
- [ ] Monitoring and logging enabled in test environment
- [ ] Smoke test completed successfully (entry criterion for system test phase)
- [ ] Config ID documented (coded identifier for the exact environment composition)

### Security Testing

| Area | Method | Reference |
|------|--------|-----------|
| Tenant isolation | Automated + manual: cross-tenant access denied | `vibe-security-skill` |
| Auth bypass | Token manipulation, session hijacking attempts | `dual-auth-rbac` |
| Injection | SQL injection, XSS, CSRF payloads | OWASP Top 10 |
| Data exposure | API response auditing, error message review | `vibe-security-skill` |

### Performance Testing

| Metric | Target | Tool |
|--------|--------|------|
| API response time | < 500ms (P95) | curl timing, load test tools |
| Web page load | < 2s (first contentful paint) | Browser DevTools, Lighthouse |
| Android cold start | < 3s | Android Profiler |
| Database query | < 100ms (P95) | MySQL slow query log, EXPLAIN |

## Cross-References to Existing Skills

### Upstream Skills (use BEFORE this skill)

| Skill | Relationship |
|-------|-------------|
| `sdlc-planning` | Provides SRS (requirement IDs for traceability), QA Plan (quality standards), Risk Plan (test-specific risks). |
| `sdlc-design` | Provides SDD (architecture to verify), database design (schema to test), API design (contracts to validate). |
| `project-requirements` | Raw requirements gathered via interview. Feed into SRS before creating test docs. |

### Parallel Skills (use ALONGSIDE this skill)

| Skill | Relationship |
|-------|-------------|
| `android-tdd` | Actual TDD implementation patterns (Red-Green-Refactor, layer-specific tests). This skill documents; `android-tdd` implements. |
| `ai-error-handling` | 5-layer validation stack for AI-generated code. Complements this skill's formal V&V processes. |
| `ai-error-prevention` | "Trust but verify" patterns. Use alongside peer review processes. |
| `vibe-security-skill` | Security testing patterns, OWASP mapping. Reference in test plans and security test cases. |
| `feature-planning` | Feature-level testing strategy. This skill covers project-level testing. |

### Downstream Skills (use AFTER this skill)

| Skill | Relationship |
|-------|-------------|
| `google-play-store-review` | Play Store compliance testing. Uses test results from this skill's reports. |

### Sibling SDLC Skills

| Skill | Phase | Status |
|-------|-------|--------|
| `sdlc-planning` | Planning & Management | Available |
| `sdlc-design` | Design & Architecture | Available |
| `sdlc-testing` | Testing & Quality | **This Skill** |
| `sdlc-user-deploy` | Delivery & Deployment | Available |

## Adaptation Rules

### SaaS vs Standalone

| Aspect | Multi-Tenant SaaS | Standalone App |
|--------|-------------------|----------------|
| Tenant isolation tests | Required (franchise_id in every query) | Not applicable |
| RBAC test cases | Full matrix (super_admin, owner, staff) | Simple role tests |
| Cross-tenant security | Dedicated test suite | Omit |
| Test data setup | Per-tenant fixtures (franchise_id = 1, 2) | Single dataset |

### Android + Web vs Web-Only

| Aspect | Android + Web | Web-Only |
|--------|---------------|----------|
| Test frameworks | JUnit 5, MockK, Compose Testing + PHPUnit | PHPUnit only |
| UI testing | Compose tests + browser tests | Browser tests only |
| Offline testing | Room caching, network error scenarios | N/A |
| Device matrix | API levels 26-35, multiple screen sizes | Browser matrix |

### CI/CD Integration

| Stage | Trigger | Tests Run |
|-------|---------|-----------|
| Pre-commit | Local commit | Unit tests (fast) |
| PR validation | PR created/updated | Unit + integration tests |
| Merge to develop | PR merged | Full test suite + coverage |
| Release candidate | Tag created | Full suite + security + performance |
| Post-deploy | Production deploy | Smoke tests only |

## Quality Checklist

- [ ] All 7 documents generated (or justified why one was skipped)
- [ ] Each document stays under 500 lines
- [ ] Test Plan references SRS requirement IDs for traceability
- [ ] Test Plan includes: risk register, completion criteria, suspension/resumption criteria, communication plan, environment requirements, roles (per 29119-3 §6.2)
- [ ] Test cases use naming convention TC-[MODULE]-[TYPE]-[###]
- [ ] Every test case has the 9 normative 29119-3 fields (ID, objective, priority, traceability, preconditions, input, expected result, actual result, test result)
- [ ] Every expected result is a deterministic test oracle — no judgment calls
- [ ] Every SRS requirement ID (FR-xxx, NFR-xxx) is traced to at least one test case
- [ ] V&V Plan covers both verification (built right) and validation (right product)
- [ ] Test Plan distinguishes Alpha UAT (internal controlled) from Beta UAT (real-world users)
- [ ] Regression testing section covers: suite scope, trigger conditions, pass rate threshold
- [ ] Test Data Management section covers: fixture creation, tenant isolation, data anonymization
- [ ] Test Data Readiness Report completed before execution begins
- [ ] Test Environment Readiness Report completed before execution begins
- [ ] Test Report includes pass rates, coverage, defect resolution protocol, and Go/No-Go recommendation
- [ ] Incident Report template populated for every detected anomaly
- [ ] Test Completion Report produced at phase close: summary, deviations, residual risks, lessons learned
- [ ] Peer Review Report includes tech-stack-specific checklists
- [ ] Multi-tenant isolation addressed in test cases and V&V plan
- [ ] Test environments match deployment environments (Windows/Ubuntu/Debian)
- [ ] Security test cases reference `vibe-security-skill` OWASP mapping
- [ ] Performance benchmarks have numeric targets (not vague language)
- [ ] Documents cross-reference each other and upstream SRS/SDD

## Anti-Patterns

| Anti-Pattern | Why It Fails | Do This Instead |
|-------------|-------------|-----------------|
| No formal test plan | Ad-hoc testing misses critical paths | Write STP before testing begins |
| Test cases without expected results | Can't determine pass/fail | Every TC has explicit expected results (test oracle) |
| Vague expected results ("response looks OK") | Not a test oracle; tester must interpret | State exact output: value, format, timing, error code |
| No traceability to requirements | Can't prove coverage | Map every TC to FR-xxx or NFR-xxx |
| Testing only happy paths | Edge cases cause production failures | Include negative, boundary, and error cases |
| No test data strategy | Inconsistent, flaky tests | Define fixtures, factories, seed data with tenant isolation |
| Skipping security testing | Vulnerabilities ship to production | Include security test suite in every release |
| No peer review process | Bugs caught late, inconsistent code | Standardize reviews with checklists |
| Rubber-stamp reviews | Reviews provide no value | Require findings documented, metrics tracked |
| Testing in production only | Users find bugs, not testers | Test in staging first, smoke test prod |
| No regression suite | Passing tests break silently between releases | Define regression suite, trigger on every RC |
| No incident tracking | Anomalies lose context | Open an Incident Report for every anomaly during execution |
| No Test Completion Report | Phase never formally closes | Produce TCR before passing to next lifecycle phase |

## Template Files

Each template provides the complete structure, section-by-section guidance, examples tailored to the tech stack, anti-patterns, and a quality checklist.

1. [Software Test Plan](templates/software-test-plan.md)
2. [Test Case Specifications](templates/test-case-specifications.md)
3. [Validation & Verification Plan](templates/validation-verification-plan.md)
4. [Validation Test Report](templates/validation-test-report.md)
5. [Peer Review / Inspection Report](templates/peer-review-report.md)
6. [Incident Report](templates/incident-report.md)
7. [Test Completion Report](templates/test-completion-report.md)

---

**Back to:** [Skills Repository](../CLAUDE.md)
**Related:** [sdlc-planning](../sdlc-planning/SKILL.md) | [android-tdd](../android-tdd/SKILL.md) | [vibe-security-skill](../vibe-security-skill/SKILL.md) | [ai-error-handling](../ai-error-handling/SKILL.md)
**Last Updated:** 2026-03-15 (upgraded to BS ISO/IEC/IEEE 29119-3:2013 per Winston, BS Standards; strengthened per Adjei 2023, Splunk Product is Docs)
