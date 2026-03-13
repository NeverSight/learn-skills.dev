---
name: integration-test
version: 1.0.0
description: '[Testing] Generate or review integration tests. Modes: generate (from git changes or prompt), review (quality audit of existing tests), diagnose (analyze test failures). Subcutaneous tests with real DI, no mocks.'
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, TaskCreate, AskUserQuestion
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/understand-code-first-protocol.md`
- `.claude/skills/shared/cross-cutting-quality-concerns-protocol.md` — Authorization testing, test data setup, seed data patterns
- `references/integration-test-patterns.md`
- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)
- `docs/test-specs/` — Test specifications by module (read existing TCs for expected behavior; verify test-to-spec traceability)

> **CRITICAL: Search existing patterns FIRST.** Before generating ANY test, grep for existing integration test files in the same service. Read at least 1 existing test file to match conventions (namespace, usings, collection name, base class, helper usage). Never generate tests that contradict established patterns in the codebase.

> **For test specifications and test case generation from PBIs, use `/tdd-spec` skill (preferred) or `/test-spec` skill instead.**

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

> **Process Discipline:** MUST READ `.claude/skills/shared/red-flag-stop-conditions-protocol.md` — STOP when test passes but behavior differs from expectation, or when 3+ fix attempts fail.

> **Process Discipline:** MUST READ `.claude/skills/shared/rationalization-prevention-protocol.md` — counter "tests aren't relevant" and "I'll test after" evasions.

## Quick Summary

**Goal:** Generate integration test files for commands/queries using real DI (no mocks).

## Project Pattern Discovery

Before implementation, search your codebase for project-specific patterns:

- Search for: `IntegrationTest`, `TestFixture`, `TestUserContext`, `IntegrationTestBase`
- Look for: existing test projects, test collection definitions, service-specific test base classes

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ `integration-test-reference.md` for project-specific patterns and code examples.
> If file not found, continue with search-based discovery above.

**Five modes:** (1) From git changes (default) — detects uncommitted command/query files and generates matching tests. (2) From prompt — user specifies what to test. (3) Review — audit existing tests for quality, best practices, and flaky patterns. (4) Diagnose — analyze test failures to determine root cause (test bug vs code bug). (5) Verify-traceability — check test code matches test specs and feature docs.

**Workflow:**

1. **Detect mode** — See Mode Detection section below
2. **Find targets** — Identify test/command/query files
3. **Gather context** — Read relevant files for the detected mode
4. **Execute** — Generate, review, diagnose, or verify depending on mode
5. **Report** — Build check (generate), quality report (review), root cause (diagnose)

**Key Rules:**

- MUST search for existing test patterns in the same service BEFORE generating
- MUST READ `references/integration-test-patterns.md` before writing any test
- **Organize by domain feature, NOT by type** — command and query tests for the same domain go in the same folder (e.g., `Orders/OrderCommandIntegrationTests.cs` + `Orders/OrderQueryIntegrationTests.cs`). NEVER create a `Queries/` or `Commands/` folder.
- Use `IntegrationTestHelper.UniqueName()` for ALL string test data
- Use `AssertEntityMatchesAsync<T>` for DB verification (built-in WaitUntil polling)
- **IMPORTANT MUST ENSURE:** When asserting DB state changed by **async event handlers** (entity event handlers, message bus consumers), ALWAYS wrap assertions in `PlatformIntegrationTestHelper.WaitUntilAsync()`. Direct `ExecuteWithServicesAsync` without retry will flake because handlers run in background threads. Only synchronous command results can be asserted directly.
- Minimum 3 test methods: happy path, validation failure, DB state check
- **Authorization tests:** Include tests with multiple user contexts (`TestUserContextFactory.CreateAdmin()`, `CreateRegularUser()`, etc.) — verify authorized access succeeds AND unauthorized access is rejected
- Every test method MUST have `// TC-{MOD}-XXX: Description` comment AND `[Trait("TestSpec", "TC-{MOD}-XXX")]` — placed **before** `[Fact]`, outside method body
- If no TC exists in feature docs, **auto-create** it in Section 17 before generating the test
- For comprehensive test spec generation before coding, use `/tdd-spec` first

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

## Mandatory Task Ordering (MUST FOLLOW)

When generating integration tests, ALWAYS create and execute tasks in this exact order:

1. **FIRST task: Verify/upsert test specs in feature docs**
    - Read feature doc Section 17 (`docs/business-features/{App}/detailed-features/`) for the target domain
    - Read test-specs doc (`docs/test-specs/{App}/README.md`) if exists
    - For each test case to generate: verify a matching `TC-{MOD}-XXX` exists in docs
    - If TC is MISSING: create the TC entry in Section 17 with Priority, Status, GIVEN/WHEN/THEN, Evidence
    - If TC is INCORRECT: update it to reflect current command/query behavior
    - Output: a TC mapping list (TC code → test method name) for subsequent tasks

2. **MIDDLE tasks: Implement integration tests**
    - Generate test files using the TC mapping from task 1
    - Each `[Fact]` method gets annotation before it (outside method body):
        ```csharp
        // TC-OM-001: Create valid order — happy path
        [Trait("TestSpec", "TC-OM-001")]
        [Fact]
        public async Task CreateOrder_WhenValidData_ShouldCreateSuccessfully()
        ```
    - Follow all existing patterns (Collection, Trait("Category"), UniqueName, AssertEntity\*, etc.)

3. **FINAL task: Verify bidirectional traceability**
    - Grep all `[Trait("TestSpec", ...)]` in the test project
    - Grep all `TC-{MOD}-XXX` in feature doc Section 17 / test-specs doc
    - Verify every test method links to a doc TC, and every doc TC links back to a test
    - Flag orphans: tests without doc TCs, or doc TCs without matching tests
    - Update `IntegrationTest` field in feature doc TCs with `{File}::{MethodName}`

## Module Abbreviation Registry

| Module                  | Abbreviation | Test Folder      |
| ----------------------- | ------------ | ---------------- |
| Order Management        | OM           | `Orders/`        |
| Inventory               | INV          | `Inventory/`     |
| User Profiles           | UP           | `UserProfiles/`  |
| Notification Management | NM           | `Notifications/` |
| Report Generation       | RG           | `Reports/`       |
| Feedback                | FB           | `Feedback/`      |
| Background Jobs         | BJ           | —                |

## TC Code Numbering Rules

When creating new `TC-{MOD}-{NNN}` codes:

1. **Always check the feature doc's first** — `docs/business-features/{App}/detailed-features/` contains existing TC codes. New codes must not collide.
2. **Existing docs use decade-based grouping** — e.g., OM: 001-004 (CRUD), 011-013 (validation), 021-023 (permissions), 031-033 (events). Find the next free decade.
3. **If a collision is unavoidable** — renumber in the doc side only (e.g., TC-OM-031 → TC-OM-034). Keep `[Trait("TestSpec")]` in the .cs file unchanged and add a renumbering note in the doc.
4. **Feature doc is the canonical registry** — the `[Trait("TestSpec")]` in test files is for traceability, not the source of truth for numbering.

# Integration Test Generation

## Mode Detection

```
Args = command/query name (e.g., "/integration-test CreateOrderCommand")
  → FROM-PROMPT mode: generate tests for the specified command/query

No args (e.g., "/integration-test")
  → FROM-CHANGES mode: detect changed command/query files from git

Args = "review" (e.g., "/integration-test review Orders")
  → REVIEW mode: audit existing test quality, find flaky patterns, check best practices

Args = "diagnose" (e.g., "/integration-test diagnose OrderCommandIntegrationTests")
  → DIAGNOSE mode: analyze why tests fail — determine test bug vs code bug

Args = "verify" (e.g., "/integration-test verify {Service}")
  → VERIFY-TRACEABILITY mode: check test code matches specs and feature docs
```

## Step 1: Find Targets

### From-Changes Mode (default)

Run via Bash tool:

```bash
git diff --name-only; git diff --cached --name-only
```

Filter for `*Command.cs` or `*Query.cs` under `src/Services/`. Extract service from path:

| Path pattern                                       | Service   | Test project                 |
| -------------------------------------------------- | --------- | ---------------------------- |
| `src/Services/{ServiceDir}/{Service}.Application/` | {Service} | `{Service}.IntegrationTests` |

Search your codebase for existing `*.IntegrationTests` projects to find the correct mapping.

If no test project exists: inform user "No integration test project for {service}. See CLAUDE.md Integration Testing section to create one."

If test file already exists: ask user overwrite or skip.

### From-Prompt Mode

User specifies command/query name. Use Grep tool (NOT bash grep):

```
Grep pattern="class {CommandName}" path="src/Services/" glob="*.cs"
```

## Step 2: Gather Context

For each target, read these files (in parallel):

1. **Command/query file** — extract: class name, result type, DTO property, entity type
2. **Existing test files in same service** — use Glob `{Service}.IntegrationTests/**/*IntegrationTests.cs`, read 1+ for conventions (collection name, trait, namespace, usings, base class)
3. **Service integration test base class** — grep: `class.*ServiceIntegrationTestBase`
4. **`references/integration-test-patterns.md`** — canonical templates (adapt {Service} placeholders)

## Step 2b: Look Up TC Codes

For each target domain, read the matching test spec:

- `docs/business-features/{App}/detailed-features/` Section 17 (primary source of truth)
- `docs/test-specs/{App}/README.md` (secondary reference)

Build a mapping: test case description → TC code (e.g., "create valid order" → TC-OM-001).
If no TC exists, **CREATE IT** in the feature doc Section 17 before generating the test.
If TC is outdated or incorrect, **UPDATE IT** first.
This is NOT optional — the doc is the source of truth and must be correct before tests reference it.
If no TC exists and feature doc Section 17 is missing, run `/tdd-spec` first to generate test specifications.

## Step 3: Generate Test File

**File path:** `src/Services/{ServiceDir}/{Service}.IntegrationTests/{Domain}/{CommandName}IntegrationTests.cs`

> **Folder = domain feature.** `{Domain}` is the business domain (Orders, Inventory, Notifications, UserProfiles, etc.), NOT the CQRS type. Both command and query tests for the same domain live in the same folder.

**Structure:**

```csharp
#region
using FluentAssertions;
// ... service-specific usings (copy from existing tests)
#endregion

namespace {Service}.IntegrationTests.{Domain};

[Collection({Service}IntegrationTestCollection.Name)]
[Trait("Category", "Command")]  // or "Query"
public class {CommandName}IntegrationTests : {Service}ServiceIntegrationTestBase
{
    // Minimum 3 tests: happy path, validation failure, DB state verification
}
```

**Test method naming:** `{CommandName}_When{Condition}_Should{Expectation}`

**Required patterns per command type:**

| Command type | Required tests                                     |
| ------------ | -------------------------------------------------- |
| Save/Create  | Happy path + validation failure + DB state         |
| Update       | Create-then-update + verify updated fields in DB   |
| Delete       | Create-then-delete + `AssertEntityDeletedAsync`    |
| Query        | Filter returns results + pagination + empty result |

## Step 4: Verify

```bash
dotnet build {test-project-path}
```

Check:

- [ ] `[Collection]` attribute present with correct collection name
- [ ] `[Trait("Category", ...)]` present
- [ ] All string test data uses `IntegrationTestHelper.UniqueName()`
- [ ] User context via `TestUserContextFactory.Create*()`
- [ ] DB assertions use `AssertEntityMatchesAsync` or `AssertEntityDeletedAsync`
- [ ] No mocks — real DI only
- [ ] Every `[Fact]` method has `// TC-{MOD}-XXX: Description` comment + `[Trait("TestSpec", "TC-{MOD}-XXX")]`

## Example Files to Study

Search your codebase for existing integration test files to use as reference:

```bash
# Find existing integration test files
find src/Services -name "*IntegrationTests.cs" -type f
find src/Services -name "*IntegrationTestBase.cs" -type f
find src/Services -name "*IntegrationTestFixture.cs" -type f
```

| Pattern                                                             | Shows                        |
| ------------------------------------------------------------------- | ---------------------------- |
| `{Service}.IntegrationTests/{Domain}/*CommandIntegrationTests.cs`   | Create + update + validation |
| `{Service}.IntegrationTests/{Domain}/*QueryIntegrationTests.cs`     | Query with create-then-query |
| `{Service}.IntegrationTests/{Domain}/Delete*IntegrationTests.cs`    | Delete + cascade             |
| `{Service}.IntegrationTests/{Service}ServiceIntegrationTestBase.cs` | Service base class pattern   |

## Related

| Skill             | Relationship                                         | When to Use                                                               |
| ----------------- | ---------------------------------------------------- | ------------------------------------------------------------------------- |
| `tdd-spec`        | TC source — generates test specs this skill consumes | Run FIRST to create TCs in feature doc Section 17 before generating tests |
| `test-spec`       | Heavyweight planning — feeds test strategies         | Use for complex test planning requiring deep investigation                |
| `test-specs-docs` | Dashboard sync — keeps docs/test-specs/ in sync      | Run AFTER generating tests to update the cross-module dashboard           |
| `test`            | Test runner — executes the generated tests           | Run AFTER generating tests to verify they pass                            |
| `review-changes`  | Change review — reviews uncommitted changes          | Run to review test files before committing                                |

### How to Use for Each Case

**Case: Generate tests from existing test specs (feature docs Section 17)**

```
/integration-test CreateOrderCommand
```

→ Reads Section 17 TCs, generates test file with TC annotations

**Case: Generate tests from git changes (default)**

```
/integration-test
```

→ Detects changed command/query files, checks Section 17 for matching TCs, generates tests

**Case: Generate tests after /tdd-spec created new TCs**

```
/tdd-spec → /integration-test
```

→ tdd-spec writes TCs to Section 17, then integration-test generates tests from those TCs

**Case: Review existing tests for quality**

```
/integration-test review Orders
```

→ Audits test quality, finds flaky patterns, checks best practices

**Case: Diagnose test failures**

```
/integration-test diagnose OrderCommandIntegrationTests
```

→ Analyzes failures, determines test bug vs code bug

**Case: Verify test-spec traceability**

```
/integration-test verify {Service}
```

→ Checks test code matches specs and feature docs bidirectionally

---

# REVIEW Mode — Test Quality Audit

When mode = REVIEW, audit existing integration tests for quality, flaky patterns, and best practices.

## Review Workflow

1. **Find test files** — Glob `{Service}.IntegrationTests/{Domain}/**/*IntegrationTests.*`
2. **Read each test file** — analyze for quality issues
3. **Generate quality report** — categorized findings with severity

## Review Checklist

### Flaky Test Detection (CRITICAL)

These patterns cause intermittent failures — flag as HIGH severity:

- [ ] **Missing async polling** — DB assertions after async event handlers without `WaitUntilAsync()` or equivalent retry/polling. Direct assertions on state changed by background threads WILL flake.
- [ ] **Missing retry for eventual consistency** — Any assertion that checks state modified by message bus consumers, event handlers, or background jobs without polling/retry wrapper
- [ ] **Hardcoded delays** — `Thread.Sleep()`, `Task.Delay()` instead of condition-based polling (`WaitUntil`, retry loops with timeout)
- [ ] **Race conditions** — Multiple tests modifying shared state without isolation (e.g., same entity ID, same user context)
- [ ] **Non-unique test data** — Hardcoded strings/IDs instead of unique generators (e.g., `IntegrationTestHelper.UniqueName()` or equivalent)
- [ ] **Time-dependent assertions** — Tests that depend on `DateTime.Now` without time abstraction

### Best Practice Checks

- [ ] **Collection/group attribute** — All test classes have correct collection/group for shared fixture
- [ ] **Category trait** — `[Trait("Category", "Command")]` or equivalent categorization present
- [ ] **TC annotation** — Every test method has TC code comment + test spec trait/attribute
- [ ] **Minimum test coverage** — At least 3 tests per command: happy path, validation, DB state
- [ ] **No mocks** — Real DI only, no mock frameworks in integration tests
- [ ] **Unique test data** — All string data uses unique generators
- [ ] **User context** — Test user context via factory, not hardcoded
- [ ] **DB assertions** — Uses entity assertion helpers (not raw DB queries)
- [ ] **Cleanup** — Tests don't leave orphaned data that affects other tests

### Code Quality Checks

- [ ] **Method naming** — Follows `{Action}_When{Condition}_Should{Expectation}` pattern
- [ ] **Arrange-Act-Assert** — Clear separation in test methods
- [ ] **No logic in tests** — No conditionals, loops, or complex setup in test methods
- [ ] **Test independence** — Each test can run in isolation

## Review Report Format

```markdown
# Integration Test Quality Report — {Domain}

## Summary

- Tests scanned: {N}
- Issues found: {N} (HIGH: {n}, MEDIUM: {n}, LOW: {n})
- Overall quality: {GOOD|NEEDS_WORK|CRITICAL}

## HIGH Severity Issues (Flaky Risk)

| Test         | Issue                                            | Fix                      |
| ------------ | ------------------------------------------------ | ------------------------ |
| {MethodName} | DB assertion without polling after async handler | Wrap in WaitUntilAsync() |

## MEDIUM Severity Issues (Best Practice)

| Test | Issue | Fix |
| ---- | ----- | --- |

## LOW Severity Issues (Style)

| Test | Issue | Fix |
| ---- | ----- | --- |

## Recommendations

1. {Prioritized fix suggestions}
```

---

# DIAGNOSE Mode — Test Failure Root Cause Analysis

When mode = DIAGNOSE, analyze failing tests to determine whether the failure is a test bug or an application code bug.

## Diagnose Workflow

1. **Identify failing tests** — User provides test class name or run test suite to collect failures
2. **Read test code** — Understand what the test expects
3. **Read application code** — Trace the command/query handler path
4. **Compare expected vs actual** — Determine root cause
5. **Classify** — Test bug vs code bug vs infrastructure issue
6. **Report** — Root cause + recommended fix

## Root Cause Decision Tree

```
Test fails
├── Compilation error?
│   ├── Missing type/method → Code changed, test not updated → TEST BUG
│   └── Wrong import/namespace → TEST BUG
├── Timeout/hang?
│   ├── Missing async/await → TEST BUG
│   ├── Deadlock in handler → CODE BUG
│   └── Infrastructure down → INFRA ISSUE
├── Assertion failure?
│   ├── Expected value wrong?
│   │   ├── Test hardcoded old behavior → TEST BUG
│   │   └── Business logic changed → CODE BUG (if unintended) or TEST BUG (if intended change)
│   ├── Null/empty result?
│   │   ├── Entity not found → Check if create step succeeded → TEST BUG (setup) or CODE BUG (handler)
│   │   └── Query returns empty → Check filters/predicates → CODE BUG
│   ├── Intermittent (passes sometimes)?
│   │   ├── Async assertion without polling → TEST BUG (add WaitUntilAsync)
│   │   ├── Non-unique test data collision → TEST BUG (use UniqueName)
│   │   └── Race condition in handler → CODE BUG
│   └── Wrong count/order?
│       ├── Test data leak from other tests → TEST BUG (isolation)
│       └── Logic error in query → CODE BUG
├── Validation error (expected success)?
│   ├── Test sends invalid data → TEST BUG
│   └── Validation rule too strict → CODE BUG
└── Exception thrown?
    ├── Known exception type in handler → CODE BUG
    └── DI/config error → INFRA ISSUE
```

## Diagnose Report Format

```markdown
# Test Failure Diagnosis — {TestClass}

## Failing Tests

| Test Method | Error Type        | Root Cause    | Classification              |
| ----------- | ----------------- | ------------- | --------------------------- |
| {Method}    | {AssertionFailed} | {Description} | TEST BUG / CODE BUG / INFRA |

## Detailed Analysis

### {MethodName}

**Error:** {error message}
**Expected:** {what test expected}
**Actual:** {what happened}
**Root Cause:** {explanation with code evidence}
**Classification:** TEST BUG | CODE BUG | INFRA ISSUE
**Evidence:** `{file}:{line}` — {what the code does}
**Recommended Fix:** {specific fix with code location}

## Summary

- Test bugs: {N} — fix in test code
- Code bugs: {N} — fix in application code
- Infra issues: {N} — fix in configuration/environment
```

---

# VERIFY-TRACEABILITY Mode — Test ↔ Spec ↔ Feature Doc Verification

When mode = VERIFY, perform bidirectional traceability check between test code, test specifications, and feature documentation.

## Verify Workflow

1. **Collect test methods** — Grep for test spec annotations in test project
2. **Collect doc TCs** — Read feature doc Section 17 for all TC entries
3. **Build 3-way matrix** — Test code ↔ test-specs/ ↔ feature doc Section 17
4. **Identify mismatches** — Orphans, stale references, behavior drift
5. **Classify mismatches** — Which source is correct?
6. **Report** — Traceability matrix + recommended fixes

## Mismatch Classification

When test code and spec disagree, determine which is correct:

| Scenario                                          | Likely Correct Source         | Action                       |
| ------------------------------------------------- | ----------------------------- | ---------------------------- |
| Test passes, spec describes different behavior    | Test (reflects current code)  | Update spec to match test    |
| Test fails, spec describes expected behavior      | Spec (test is stale)          | Update test to match spec    |
| Test exists, no spec                              | Test (spec was never written) | Create spec from test        |
| Spec exists, no test                              | Spec (test was never written) | Generate test from spec      |
| Test and spec agree, but code behaves differently | Spec (code has regression)    | Fix code or update spec+test |

## Verification Checklist

- [ ] Every test method has a matching TC in feature doc Section 17
- [ ] Every TC in Section 17 has a matching test method (or is marked `Status: Untested`)
- [ ] TC descriptions in docs match what the test actually validates
- [ ] Evidence file paths in TCs point to current (not stale) code locations
- [ ] Test annotations match TC IDs (no typos, no orphaned IDs)
- [ ] Priority levels in docs match test categorization
- [ ] `docs/test-specs/` dashboard is in sync with feature doc Section 17

## Verify Report Format

```markdown
# Traceability Report — {Service}

## Summary

- TCs in feature docs: {N}
- Test methods with TC annotations: {N}
- Fully traced (both directions): {N}
- Orphaned tests (no matching TC): {N}
- Orphaned TCs (no matching test): {N}
- Mismatched behavior: {N}

## Traceability Matrix

| TC ID     | Feature Doc? | Test Code? | Dashboard? | Status       |
| --------- | ------------ | ---------- | ---------- | ------------ |
| TC-OM-001 | ✅           | ✅         | ✅         | Traced       |
| TC-OM-005 | ✅           | ❌         | ✅         | Missing test |
| TC-OM-010 | ❌           | ✅         | ❌         | Missing spec |

## Orphaned Tests (no matching TC in docs)

| Test File | Method   | Annotation | Action                   |
| --------- | -------- | ---------- | ------------------------ |
| {file}    | {method} | TC-OM-010  | Create TC in feature doc |

## Orphaned TCs (no matching test)

| TC ID     | Doc Location | Priority | Action                              |
| --------- | ------------ | -------- | ----------------------------------- |
| TC-OM-005 | Section 17   | P0       | Generate test via /integration-test |

## Behavior Mismatches

| TC ID | Doc Says | Test Does | Correct Source | Action |
| ----- | -------- | --------- | -------------- | ------ |

## Recommendations

1. {Prioritized actions}
```

---

## Test Data Setup Guidelines

> Ref: `.claude/skills/shared/cross-cutting-quality-concerns-protocol.md` §3

| Pattern             | When to Use                        | Example                                                      |
| ------------------- | ---------------------------------- | ------------------------------------------------------------ |
| **Per-test inline** | Simple tests, unique data          | `var order = new CreateOrderCommand { Name = UniqueName() }` |
| **Factory methods** | Repeated entity creation           | `TestDataFactory.CreateValidOrder()`                         |
| **Builder pattern** | Complex entities with many fields  | `new OrderBuilder().WithStatus(Active).WithItems(3).Build()` |
| **Shared fixture**  | Reference data needed by all tests | `CollectionFixture.SeedReferenceData()`                      |

**Rules:**

- Every test creates its own data — no shared mutable state between tests
- Use unique identifiers for ALL string data (`IntegrationTestHelper.UniqueName()`)
- Factory methods return valid entities by default — tests override only what they test
- Cross-entity dependencies: create parent first, then child (e.g., create User, then create Order for that User)
- **Seed data:** If the feature requires reference/lookup data, set up seed data in the collection fixture or per-test preconditions

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements

---

## Workflow Recommendation

> **IMPORTANT MUST:** If you are NOT already in a workflow, use `AskUserQuestion` to ask the user:
>
> 1. **Activate `test-to-integration` workflow** (Recommended) — scout → integration-test → test
> 2. **Execute `/integration-test` directly** — run this skill standalone

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/test (Recommended)"** — Run full test suite to verify integration tests pass
- **"/review-changes"** — Review all changes before committing
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
