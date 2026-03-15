---
name: scan-integration-tests
version: 1.0.0
description: '[Documentation] Scan project and populate/sync docs/project-reference/integration-test-reference.md with test base classes, fixtures, helpers, configuration, and service-specific setup.'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/scan-and-update-reference-doc-protocol.md`
- `.claude/skills/shared/understand-code-first-protocol.md`

## Quick Summary

**Goal:** Scan test codebase and populate `docs/project-reference/integration-test-reference.md` with test architecture, base classes, fixtures, helpers, configuration patterns, and service-specific setup conventions.

**Workflow:**

1. **Read** — Load current target doc, detect init vs sync mode
2. **Scan** — Discover test patterns via parallel sub-agents
3. **Report** — Write findings to external report file
4. **Generate** — Build/update reference doc from report
5. **Verify** — Validate code examples reference real files

**Key Rules:**

- Generic — works with any test framework (xUnit, NUnit, Jest, Vitest, pytest, JUnit, etc.)
- Detect test framework first, then scan for framework-specific patterns
- Focus on integration/E2E tests (not unit tests) — tests that touch real infrastructure
- Every code example must come from actual project files with file:line references

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Scan Integration Tests

## Phase 0: Read & Assess

1. Read `docs/project-reference/integration-test-reference.md`
2. Detect mode: init (placeholder) or sync (populated)
3. If sync: extract existing sections and note what's already well-documented

## Phase 1: Plan Scan Strategy

Detect test framework and infrastructure:

- `*.csproj` with xUnit/NUnit/MSTest references → .NET tests
- `package.json` with jest/vitest/playwright/cypress → JS/TS tests
- `pom.xml` with junit/testcontainers → Java tests
- `pytest.ini` / `conftest.py` → Python tests

Identify test infrastructure:

- Testcontainers usage (Docker-based test infra)
- In-memory databases vs real databases
- Custom test fixtures and factories
- WebApplicationFactory / TestServer patterns

Use `docs/project-config.json` if available for test project locations.

## Phase 2: Execute Scan (Parallel Sub-Agents)

Launch **2 Explore agents** in parallel:

### Agent 1: Test Infrastructure

- Grep for test base classes (`extends.*Test`, `TestBase`, `IntegrationTest`, `[Collection]`)
- Find test fixtures and factories (WebApplicationFactory, TestFixture, conftest)
- Discover test configuration (appsettings.test.json, .env.test, test containers setup)
- Find DI/service registration overrides for testing
- Look for test data builders and seed data patterns

### Agent 2: Test Patterns & Conventions

- Grep for test helper methods (assertion helpers, setup utilities, cleanup methods)
- Find common test patterns (Arrange-Act-Assert, Given-When-Then)
- Discover test categorization (traits, categories, tags for grouping)
- Find test data patterns (unique name generators, random data, factory patterns)
- Look for infrastructure interaction patterns (database reset, queue drain, cache clear)
- Count test files per service/module to assess coverage distribution

Write all findings to: `plans/reports/scan-integration-tests-{YYMMDD}-{HHMM}-report.md`

## Phase 3: Analyze & Generate

Read the report. Build these sections:

### Target Sections

| Section                    | Content                                                                          |
| -------------------------- | -------------------------------------------------------------------------------- |
| **Test Architecture**      | Overall test strategy, framework choice, infrastructure approach, test isolation |
| **Test Base Classes**      | Base class hierarchy, what each provides, when to use which                      |
| **Fixtures & Factories**   | Test fixture setup, service factory, DI container configuration                  |
| **Test Helpers**           | Assertion helpers, data builders, utility methods with examples                  |
| **Configuration**          | Test config files, connection strings, environment variables                     |
| **Service-Specific Setup** | Per-service test setup differences, module abbreviations, custom overrides       |
| **Test Data Patterns**     | How test data is created, unique naming, cleanup strategies                      |
| **Running Tests**          | Commands to run tests, filtering, parallel execution, CI integration             |

### Content Rules

- Show actual code snippets (5-15 lines) from the project with `file:line` references
- Include a "New Test Quickstart" section showing minimal steps to add a new test
- Use tables for convention summaries (base classes, config files, commands)
- Highlight infrastructure requirements (what must be running for tests to pass)

## Phase 4: Write & Verify

1. Write updated doc with `<!-- Last scanned: YYYY-MM-DD -->` at top
2. Verify: 5 code example file paths exist (Glob check)
3. Verify: test base class names match actual class definitions
4. Report: sections updated, test count per service, coverage gaps

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using TaskCreate
- Always add a final review todo task to verify work quality and identify fixes/enhancements
