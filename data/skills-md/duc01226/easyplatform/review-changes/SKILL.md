---
name: review-changes
description: '[Review & Quality] Review all uncommitted changes before commit'
---

# Code Review: Uncommitted Changes

Perform a comprehensive code review of all uncommitted git changes following EasyPlatform standards.

## Summary

**Goal:** Review all uncommitted changes via a report-driven four-phase process before commit.

| Phase | Action                          | Key Notes                                                              |
| ----- | ------------------------------- | ---------------------------------------------------------------------- |
| 0     | Collect changes & create report | `git status`, `git diff HEAD`, create `plans/reports/code-review-*.md` |
| 1     | File-by-file review             | Read each diff, update report with summary/purpose/issues              |
| 2     | Holistic review                 | Re-read accumulated report for architecture coherence                  |
| 3     | Finalize findings               | Critical issues, recommendations, suggestions, commit message          |

**Key Principles:**

- **Be skeptical. Critical thinking. Everything needs traced proof.** — Never accept code at face value; verify claims against actual behavior, trace data flow end-to-end, and demand evidence (file:line references, grep results, runtime confirmation) for every finding
- **Ensure code quality: no flaws, no bugs** — Verify correctness of logic, data flow, edge cases, and error handling. Flag anything that could fail at runtime
- **Clean code and DRY** — No duplication, clear naming, single responsibility, early returns. Code should be self-documenting
- **Follow existing conventions** — Match project patterns, naming style, file organization, and architectural decisions already established in the codebase. Grep for similar implementations before flagging deviations
- **Docs must match code** — If changes affect behavior, APIs, or features, verify related docs are updated: feature docs (`docs/business-features/`), test specs (`docs/test-specs/`), CHANGELOG, README, architecture docs, and inline code comments. Flag any doc that describes old behavior
- Build report incrementally — update after EACH file, not at the end
- Check logic placement in lowest layer (Entity > Service > Component)
- Always suggest conventional commit message based on changes

## Review Approach (Report-Driven Four-Phase - CRITICAL)

**⛔ MANDATORY FIRST: Create Todo Tasks for Review Phases**
Before starting, call TodoWrite with:

- [ ] `[Review Phase 0] Get git changes and create report file` - in_progress
- [ ] `[Review Phase 1] Review file-by-file and update report` - pending
- [ ] `[Review Phase 2] Re-read report for holistic assessment` - pending
- [ ] `[Review Phase 3] Generate final review findings` - pending

Update todo status as each phase completes. This ensures review is tracked.

---

## Phase 0: Get Changes & Create Report

### 0.1 Get Change Summary

```bash
# See all changed files
git status

# See actual changes (staged and unstaged)
git diff HEAD
```

### 0.2 Create Report File

- [ ] Create `plans/reports/code-review-{date}-{slug}.md`
- [ ] Initialize with Scope (list of changed files), Change Type (feature/bugfix/refactor)

---

## Phase 1: File-by-File Review (Build Report Incrementally)

For EACH changed file, read the diff and **immediately update report** with:

- [ ] File path and change type (added/modified/deleted)
- [ ] Change Summary: what was modified/added/deleted
- [ ] Purpose: why this change exists (infer from context)
- [ ] Issues Found: naming, typing, responsibility, patterns
- [ ] Continue to next file, repeat

### Review Checklist Per File

#### Architecture Compliance

- [ ] Follows Clean Architecture layers (Domain, Application, Persistence, Service)
- [ ] Uses correct repository pattern (I{Service}RootRepository<T>)
- [ ] CQRS pattern: Command/Query + Handler + Result in ONE file
- [ ] No cross-service direct database access

#### Code Quality

- [ ] Single Responsibility Principle
- [ ] No code duplication (DRY)
- [ ] Appropriate error handling with PlatformValidationResult
- [ ] No magic numbers/strings (extract to named constants)
- [ ] Type annotations on all functions
- [ ] No implicit any types
- [ ] Early returns/guard clauses used

#### Naming Conventions

- [ ] Names reveal intent (WHAT not HOW)
- [ ] Specific names, not generic (`employeeRecords` not `data`)
- [ ] Methods: Verb + Noun (`getEmployee`, `validateInput`)
- [ ] Booleans: is/has/can/should prefix (`isActive`, `hasPermission`)
- [ ] No cryptic abbreviations (`employeeCount` not `empCnt`)

#### Platform Patterns

- [ ] Uses platform validation fluent API (.And(), .AndAsync())
- [ ] No direct side effects in command handlers (use entity events)
- [ ] DTO mapping in DTO classes, not handlers
- [ ] Static expressions for entity queries

#### Security

- [ ] No hardcoded credentials or secrets
- [ ] Proper authorization checks
- [ ] Input validation at boundaries
- [ ] No SQL injection risks

#### Performance

- [ ] No O(n²) complexity (use dictionary for lookups)
- [ ] No N+1 query patterns (batch load related entities)
- [ ] Project only needed properties (don't load all then select one)
- [ ] Pagination for all list queries (never get all without paging)
- [ ] Parallel queries for independent operations
- [ ] Appropriate use of async/await
- [ ] Entity query expressions have database indexes configured
- [ ] MongoDB collections have `Ensure*IndexesAsync()` methods
- [ ] EF Core migrations include indexes for WHERE clause columns

### Backend-Specific Checks

- [ ] CQRS patterns followed correctly
- [ ] Repository usage (no direct DbContext access)
- [ ] Entity DTO mapping patterns
- [ ] Validation using PlatformValidationResult

### Frontend-Specific Checks

- [ ] Component base class inheritance correct (AppBase\*)
- [ ] State management via PlatformVmStore
- [ ] Memory leaks (missing .pipe(this.untilDestroyed()))
- [ ] Template binding issues
- [ ] BEM classes on ALL template elements

### Common Anti-Patterns to Flag

- [ ] Unused imports or variables
- [ ] Console.log/Debug.WriteLine left in code
- [ ] Hardcoded values that should be configuration
- [ ] Missing async/await keywords
- [ ] Incorrect exception handling
- [ ] Missing validation

### Test-Specific Checks (When Diff Includes Test Files)

Apply these checks ONLY to files matching `*.Tests.*/*.cs` or `e2e/tests/**/*.spec.ts`:

#### Assertion Quality

- [ ] Every mutation test (create/update/delete) asserts at least one domain field, not just HTTP status
- [ ] Preferred: follow-up query verification after mutations (proves DB round-trip)
- [ ] Validation error tests parse response body and inspect error content (not just `IsSuccessStatusCode.Should().BeFalse()`)
- [ ] Setup steps (arrange phase HTTP calls) have status assertion with descriptive `because` string
- [ ] Domain boolean flags verified where applicable (`wasCreated`, `wasSoftDeleted`, `wasRestored`)
- [ ] E2E update tests include post-mutation field re-read (not just `waitForLoading()`)

#### Data Verification

- [ ] After create: asserts `id` not null + at least 1 domain field matches input
- [ ] After update: asserts same `id` retained + at least 1 changed field
- [ ] After delete: asserts domain flag or absence from list
- [ ] Search tests: verify matched item contains search term (not just count > 0)

#### Test Structure

- [ ] TC-ID annotation present (`[Trait("TestCase", "...")]` or TC-ID in test title)
- [ ] No hardcoded test data (uses `TestDataHelper` / `createTestSnippet()`)
- [ ] Cleanup tracked in `currentTestData` (E2E) or UUID-isolated (integration)
- [ ] `because` strings on FluentAssertions calls (C#) are descriptive and unique

#### Anti-Patterns to Flag in Tests

- [ ] Status-only assertions: `response.StatusCode.Should().Be(OK)` with no body check or follow-up query
- [ ] Missing intermediate assertions: setup calls without status verification
- [ ] E2E tests ending at `waitForLoading()` with no field verification
- [ ] Validation tests checking only `IsSuccessStatusCode.Should().BeFalse()`
- [ ] Identical `because` strings across multiple assertions

---

## Phase 2: Holistic Review (Review the Accumulated Report)

After ALL files reviewed, **re-read the report** to see big picture:

- [ ] Overall technical approach makes sense?
- [ ] Solution architecture coherent as unified plan?
- [ ] New files in correct layers (Domain/Application/Presentation)?
- [ ] Logic in LOWEST appropriate layer?
- [ ] Backend: mapping in Command/DTO (not Handler)?
- [ ] Frontend: constants/columns in Model (not Component)?
- [ ] No duplicated logic across changes?
- [ ] Service boundaries respected?
- [ ] No circular dependencies?
- [ ] Test assertion density adequate? (each test verifies meaningful domain state, not just HTTP status)
- [ ] No "placeholder" tests that only check HTTP status and defer real assertions?
- [ ] Assertion patterns consistent across test files in the same feature area?
- [ ] Related documentation updated? (feature docs, test specs, CHANGELOG, README, architecture docs)
- [ ] No docs describe old/removed behavior that conflicts with current changes?
- [ ] New APIs, entities, or features have corresponding doc entries?

---

## Phase 3: Generate Final Review Result

Update report with final sections:

### Output Format

**Summary:** Brief overall assessment of the changes

**Critical Issues:** (Must fix before commit)

- Issue 1: Description and suggested fix
- Issue 2: Description and suggested fix

**High Priority:** (Should fix)

- Issue 1: Description
- Issue 2: Description

**Suggestions:** (Nice to have)

- Suggestion 1
- Suggestion 2

**Positive Notes:**

- What was done well

**Architecture Recommendations:** (If applicable)

- Recommendation 1

**Suggested Commit Message:** Based on changes (conventional commit format)

```
<type>(<scope>): <description>

<body - what and why>
```

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
