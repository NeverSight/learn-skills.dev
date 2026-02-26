---
name: qa-test-generate
description: Generate runnable Vitest and Playwright test files from BDD test cases and scaffold code. Use when generating test implementations.
allowed-tools: Read, Glob, Grep, Write($JAAN_OUTPUTS_DIR/qa/test-generate/**), Task, WebSearch, AskUserQuestion, Edit(jaan-to/config/settings.yaml)
argument-hint: [qa-test-cases, backend-scaffold | frontend-scaffold]
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# qa-test-generate

> Produce runnable Vitest unit tests and Playwright E2E specs from BDD test cases and scaffold code.

## Context Files

- `$JAAN_CONTEXT_DIR/tech.md` - Tech stack context (CRITICAL -- determines test frameworks, runners, patterns)
  - Uses sections: `#current-stack`, `#frameworks`, `#constraints`, `#patterns`
- `$JAAN_CONTEXT_DIR/config.md` - Project configuration
- `$JAAN_TEMPLATES_DIR/jaan-to-qa-test-generate.template.md` - Output template
- `$JAAN_LEARN_DIR/jaan-to-qa-test-generate.learn.md` - Past lessons (loaded in Pre-Execution)
- Research: `$JAAN_OUTPUTS_DIR/research/71-qa-bdd-gherkin-test-code-generation.md` - playwright-bdd, jest-cucumber, tag routing, test data factories, MSW, Vitest workspaces, CI execution
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

## Input

**Upstream Artifacts**: $ARGUMENTS

Accepts 1-3 file paths or descriptions:
- **qa-test-cases** (REQUIRED in standard mode) -- Path to BDD/Gherkin test cases output (from `/jaan-to:qa-test-cases`)
- **backend-scaffold** OR **frontend-scaffold** (REQUIRED in standard mode) -- Path to scaffold output (from `/jaan-to:backend-scaffold` or `/jaan-to:frontend-scaffold`)
- **backend-api-contract** (optional) -- Path to OpenAPI YAML (from `/jaan-to:backend-api-contract`) for MSW handler generation and API assertion data
- **backend-service-implement** (optional) -- Path to filled service files for deeper unit test generation
- **--from-mutants {survivors-json-path}** -- Mutation-guided mode: reads survivors JSON from `/jaan-to:qa-test-mutate` and generates targeted tests to kill surviving mutants
- **Empty** -- Interactive wizard prompting for each artifact

IMPORTANT: The input above is your starting point. Determine mode and proceed accordingly.

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `qa-test-generate`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

Also read the comprehensive research document:
`$JAAN_OUTPUTS_DIR/research/71-qa-bdd-gherkin-test-code-generation.md`

This provides:
- BDD-to-assertion mapping patterns: Cucumber.js classic, jest-cucumber binding, playwright-bdd decorator (Section 1)
- Test data factory generation with Fishery and @anatine/zod-mock (Section 2)
- MSW mock handler generation from OpenAPI contracts (Section 3)
- Vitest workspace configuration for BDD test separation (Section 4)
- Playwright configuration for BDD with playwright-bdd (Section 5)
- Tag-based test routing architecture (Section 6)
- Coverage target strategies and tiered model (Section 7)
- Fixture management and centralized architecture (Section 8)
- Database seeding for integration tests (Section 9)
- CI-friendly execution with GitHub Actions (Section 10)

Also read context files if available:
- `$JAAN_CONTEXT_DIR/tech.md` -- Know the tech stack for framework-specific test generation

If files do not exist, continue without them.

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_qa-test-generate`

> **Language exception**: Generated code output (variable names, code blocks, test files, config files) is NOT affected by this setting and remains in the project's programming language.

---

# PHASE 1: Analysis (Read-Only)

## Thinking Mode

ultrathink

Use extended reasoning for:
- Parsing BDD scenarios and mapping @tags to test tiers
- Analyzing scaffold code to identify testable units
- Planning test data factory structure from schemas
- Designing MSW handler strategy from API contract
- Mapping Given/When/Then to Vitest assertions and Playwright actions

## Step 0: Detect Input Mode

Check if $ARGUMENTS contains `--from-mutants`:
- If yes: enter **Mutation-Guided Mode** (Step 0.1)
- If no: enter **Standard Mode** (Step 1)

### Step 0.1: Mutation-Guided Mode

Read the survivors JSON file from the provided path. Validate against handoff contract:

```json
{
  "schema_version": "1.0",
  "tool": "{framework}",
  "mutation_score": {number or null},
  "survivors": [
    {
      "file": "src/services/auth.ts",
      "line": 42,
      "original": "return balance > 0;",
      "mutated": "return balance >= 0;",
      "mutator": "ConditionalBoundary"
    }
  ]
}
```

For each survivor entry:
1. Read the source file at `survivor.file`, locate `survivor.line`
2. Understand the **original** code behavior and the **mutated** variant
3. Generate a targeted test that:
   - Exercises the code path at `survivor.line`
   - Asserts behavior that the `original` version produces correctly
   - Would FAIL if the `mutated` version were substituted
4. Name tests descriptively: `test("{mutator} at {file}:{line} -- {behavior description}")`

**Testing pyramid check**: After generating mutation-targeted tests, validate ratio:
- 60-70% unit tests (function-level assertions)
- 20-25% integration tests (cross-module flows)
- 5-10% E2E tests (user-visible behavior)
- If mutation-targeted tests skew heavily toward one tier, emit a warning

**Output**: Same folder structure as standard mode, but test files are prefixed with `mutation-` (e.g., `mutation-auth-service.test.ts`).

After generating mutation-targeted tests, skip to Step 10 (Quality Check).

### Step 0.2: Optional Companion Config Generation

For JS/TS projects: generate optional `stryker.config.mjs` companion if not already present in project root.
For PHP projects: generate optional `infection.json5` companion if not already present in project root.

These configs are placed in the output `config/` subfolder as suggestions, not auto-applied.

---

## Step 1: Validate & Parse Inputs

For each provided path:

**qa-test-cases** (REQUIRED in standard mode):
1. Read the BDD/Gherkin test cases markdown
2. Extract all `Feature:` blocks with `@tags`
3. Parse each `Scenario:` extracting Given/When/Then steps
4. Build tag inventory: count of @smoke, @e2e, @unit, @integration, @boundary, @edge-case, etc.
5. Extract concrete test data values from steps

**backend-scaffold OR frontend-scaffold** (REQUIRED):
1. Read scaffold output files
2. Extract service layer functions (unit test targets)
3. Extract route handlers (integration test targets)
4. Extract component files (frontend hook/component test targets)
5. Identify validation schemas (Zod, yup, or similar)

**backend-api-contract** (optional):
1. Read OpenAPI YAML/JSON
2. Extract endpoint paths, methods, request/response schemas
3. Map to MSW handler generation targets
4. Extract example request/response payloads for assertions

**backend-service-implement** (optional):
1. Read filled service files
2. Identify business logic branches for deeper unit tests
3. Extract dependency injection points for mocking

Present input summary:
```
INPUT SUMMARY
-------------------------------------------------------------
Sources Found:      {list of found artifacts}
Sources Missing:    {list with impact assessment}

BDD Scenarios:      {total count}
  @smoke:           {count}
  @unit:            {count}
  @integration:     {count}
  @e2e:             {count}
  @boundary:        {count}
  @edge-case:       {count}

Testable Code Units:
  Services:         {count from scaffold}
  Routes/Handlers:  {count from scaffold}
  Components/Hooks: {count if frontend}
  Schemas:          {count}

API Endpoints:      {count from contract, or "N/A"}
```

## Step 2: Detect Test Framework Preferences

Read `$JAAN_CONTEXT_DIR/tech.md` for test framework detection:
- Extract test runner from `#frameworks` (default: Vitest for unit/integration, Playwright for E2E)
- Extract existing test setup patterns
- Check for existing factory libraries (Fishery, faker.js)
- Check for existing mock libraries (MSW, nock)

If tech.md missing or incomplete, use AskUserQuestion:
- "Which test runner for unit/integration tests?" -- Options: "Vitest" (default), "Jest", "Other"
- "Which E2E framework?" -- Options: "Playwright" (default), "Cypress", "Other"
- "Any existing test data libraries?" -- Options: "Fishery", "@anatine/zod-mock", "faker.js only", "None"
- "Any existing API mocking?" -- Options: "MSW", "nock", "None"

## Step 3: Map Tags to Test Tiers (Research Section 6)

Route BDD scenarios to test tiers based on tag taxonomy.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/qa-test-generate-reference.md` section "Detailed Tag Routing Map" for the full tag-to-tier routing table with target descriptions.

## Step 4: Plan Test Generation Inventory

Calculate totals and present plan:

```
TEST GENERATION PLAN
-------------------------------------------------------------
Config Files:
  - vitest.config.ts (workspace with unit + integration)
  - playwright.config.ts (with playwright-bdd)
  - test/setup/unit.ts (MSW server setup)
  - test/setup/integration.ts (DB + MSW setup)
  - test/mocks/server.ts (MSW server instance)
  - test/mocks/handlers.ts (auto-generated from API contract)

Test Data:
  - test/factories/{entity}.factory.ts ({count} factories)
  - test/fixtures/db-seed.ts (DB seeding scenarios)
  - test/utils/test-utils.ts (shared test helpers)

Unit Tests ({count} files):
  {list of service.test.ts and hook.test.ts files}

Integration Tests ({count} files):
  {list of integration.test.ts files}

E2E Tests ({count} files):
  {list of Playwright .spec.ts files per user flow}

Coverage Targets:
  - Unit: 80% line, 70% branch
  - Integration: 60% line
  - E2E: 100% of acceptance criteria scenarios
  - BDD: All Given/When/Then steps mapped to assertions
```

---

# HARD STOP -- Human Review Check

Show complete plan before generating:

```
FINAL CONFIRMATION
-------------------------------------------------------------
Source Artifacts:
  - qa-test-cases: {path}
  - scaffold: {path}
  - api-contract: {path or "N/A"}

Test Framework Stack:
  - Unit/Integration: {Vitest/Jest}
  - E2E: {Playwright/Cypress}
  - BDD Binding: {jest-cucumber adapted for Vitest / playwright-bdd}
  - Mocking: {MSW / nock}
  - Factories: {Fishery + @anatine/zod-mock / faker.js}

Output Folder: $JAAN_OUTPUTS_DIR/qa/test-generate/{id}-{slug}/
Total Files: {count}

Files to Generate:
  Config:       {count} files (vitest.config.ts, playwright.config.ts, setup files)
  Factories:    {count} files (test data factories + db-seed)
  Unit Tests:   {count} files ({total_scenarios} scenarios)
  Integration:  {count} files ({total_scenarios} scenarios)
  E2E Tests:    {count} files ({total_scenarios} scenarios)
  Utilities:    {count} files (test-utils, msw-handlers)
```

Use AskUserQuestion:
- Question: "Proceed with test file generation?"
- Header: "Generate Tests"
- Options:
  - "Yes" -- Generate all test files
  - "No" -- Cancel
  - "Edit" -- Let me revise the scope or framework choices

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Generation (Write Phase)

## Step 5: Generate Config Files

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/qa-test-generate-reference.md` section "Config Generation Specifications" for Vitest workspace, Playwright, and setup file configurations.

## Step 6: Generate Test Data Layer

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/qa-test-generate-reference.md` section "Test Data Layer Patterns" for factory, MSW handler, DB seed, and test utility generation patterns.

## Step 7: Generate Unit Tests

For each BDD scenario tagged @unit, @smoke (unit portion), @boundary, @negative (unit portion):

### 7.1 Convert Given/When/Then to Vitest Assertions

Map each BDD scenario to a Vitest describe/it block using jest-cucumber binding pattern adapted for Vitest.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/qa-test-generate-reference.md` section "BDD Binding Code Templates" for the feature-scoped step definition code template.

### 7.2 Service Unit Tests

For each service function in scaffold:
- Import service and create test file
- Mock dependencies (Prisma, external APIs) using `vi.mock()`
- Map BDD Given steps to mock setup
- Map BDD When steps to service function calls
- Map BDD Then steps to `expect()` assertions
- Include boundary value tests from @boundary scenarios
- Include error handling tests from @negative scenarios

### 7.3 Hook/Component Tests (Frontend)

If frontend-scaffold provided:
- Generate React hook tests using `renderHook` from @testing-library/react
- Generate component tests using `render` from @testing-library/react
- Mock API calls with MSW handlers
- Map BDD UI scenarios to component assertions

## Step 8: Generate Integration Tests

For each BDD scenario tagged @integration, @api:

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/qa-test-generate-reference.md` section "Integration Test Patterns" for API and service integration test generation patterns.

## Step 9: Generate E2E Tests

For each BDD scenario tagged @e2e, @smoke (E2E portion), @mobile:

### 9.1 Playwright BDD Specs (Research Section 5)

Generate step definitions using playwright-bdd's `createBdd` pattern with Given/When/Then mapped to Playwright page actions.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/qa-test-generate-reference.md` section "Playwright BDD Step Templates" for the playwright-bdd step definition code template.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/qa-test-generate-reference.md` section "E2E Page Object Patterns" for page object generation and fixture composition patterns.

## Step 10: Quality Check

Before preview, validate generated tests against all quality criteria.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/qa-test-generate-reference.md` section "Quality Check Checklist" for the full validation checklist (completeness, test data, configuration, code quality).

If any check fails, fix before proceeding.

## Step 11: Preview & Approval

### 11.1 Generate Output Metadata

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/id-generator.sh"
SUBDOMAIN_DIR="$JAAN_OUTPUTS_DIR/qa/test-generate"
mkdir -p "$SUBDOMAIN_DIR"
NEXT_ID=$(generate_next_id "$SUBDOMAIN_DIR")
```

Generate slug:
- Extract feature name from primary BDD test case title
- Convert to lowercase-kebab-case
- Max 50 characters

### 11.2 Generate Executive Summary

Template:
```
Runnable test suite for {feature_name} generated from {scenario_count} BDD scenarios
and {scaffold_type} scaffold code. Includes {unit_count} Vitest unit tests,
{integration_count} integration tests, and {e2e_count} Playwright E2E specs.
Test infrastructure: {factory_count} data factories, MSW mock handlers,
Vitest workspace config, and Playwright BDD config. Coverage targets:
80% line (unit), 60% line (integration), 100% scenario (E2E).
```

### 11.3 Show Preview

```
OUTPUT PREVIEW
-------------------------------------------------------------
ID:     {NEXT_ID}
Folder: $JAAN_OUTPUTS_DIR/qa/test-generate/{NEXT_ID}-{slug}/

Files:
  {NEXT_ID}-{slug}.md                    (Test strategy + coverage map)
  config/
    vitest.config.ts                      (Workspace config)
    playwright.config.ts                  (BDD + projects config)
    setup/unit.ts                         (MSW lifecycle)
    setup/integration.ts                  (DB + MSW setup)
    mocks/server.ts                       (MSW server)
    mocks/handlers.ts                     (Auto-generated handlers)
    test-utils.ts                         (Shared helpers + matchers)
  unit/
    {service-name}.test.ts                ({n} scenarios)
    ...
  integration/
    {resource-name}.integration.test.ts   ({n} scenarios)
    ...
  e2e/
    {flow-name}.spec.ts                   ({n} scenarios)
    steps/{feature}.steps.ts              (Step definitions)
    steps/fixtures.ts                     (Page object fixtures)
    pages/{page}.page.ts                  (Page objects)
  fixtures/
    factories/{entity}.factory.ts         ({n} factories)
    db-seed.ts                            (Seed scenarios)

[Show first unit test file as preview snippet]
[Show first E2E step definition as preview snippet]
```

Use AskUserQuestion:
- Question: "Write test files to output?"
- Header: "Write Files"
- Options:
  - "Yes" -- Write all files
  - "No" -- Cancel
  - "Refine" -- Make adjustments first

## Step 12: Write Output Files

If approved:

### 12.1 Create Folder

```bash
OUTPUT_FOLDER="$JAAN_OUTPUTS_DIR/qa/test-generate/${NEXT_ID}-${slug}"
mkdir -p "$OUTPUT_FOLDER"
mkdir -p "$OUTPUT_FOLDER/config/setup"
mkdir -p "$OUTPUT_FOLDER/config/mocks"
mkdir -p "$OUTPUT_FOLDER/unit"
mkdir -p "$OUTPUT_FOLDER/integration"
mkdir -p "$OUTPUT_FOLDER/e2e/steps"
mkdir -p "$OUTPUT_FOLDER/e2e/pages"
mkdir -p "$OUTPUT_FOLDER/fixtures/factories"
```

### 12.2 Write Main Document

Path: `$OUTPUT_FOLDER/${NEXT_ID}-${slug}.md`

Use template from: `$JAAN_TEMPLATES_DIR/jaan-to-qa-test-generate.template.md`

Fill sections:
- Title, Executive Summary
- Test Strategy (tag routing, tier mapping)
- Coverage Map (BDD scenario -> test file mapping)
- Framework Configuration Summary
- Test Data Strategy
- CI Execution Guide
- Metadata

### 12.3 Write Config Files

Write all configuration and setup files to `$OUTPUT_FOLDER/config/`

### 12.4 Write Unit Tests

Write all unit test files to `$OUTPUT_FOLDER/unit/`

### 12.5 Write Integration Tests

Write all integration test files to `$OUTPUT_FOLDER/integration/`

### 12.6 Write E2E Tests

Write all E2E test files to `$OUTPUT_FOLDER/e2e/`

### 12.7 Write Fixtures

Write all factory and seed files to `$OUTPUT_FOLDER/fixtures/`

### 12.8 Update Index

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/index-updater.sh"
add_to_index \
  "$SUBDOMAIN_DIR/README.md" \
  "$NEXT_ID" \
  "${NEXT_ID}-${slug}" \
  "{Feature Name} Test Suite" \
  "{Executive Summary}"
```

### 12.9 Confirm Completion

```
TEST SUITE GENERATED
-------------------------------------------------------------
ID:          {NEXT_ID}
Folder:      $JAAN_OUTPUTS_DIR/qa/test-generate/{NEXT_ID}-{slug}/
Index:       Updated $JAAN_OUTPUTS_DIR/qa/test-generate/README.md

Total Files: {count}
  Config:        {count}
  Unit Tests:    {count} ({scenario_count} scenarios)
  Integration:   {count} ({scenario_count} scenarios)
  E2E Tests:     {count} ({scenario_count} scenarios)
  Fixtures:      {count} ({factory_count} factories)

Coverage Targets:
  Unit:        80% line, 70% branch
  Integration: 60% line
  E2E:         100% of acceptance criteria
```

## Step 13: Suggest Next Actions

> **Test suite generated successfully!**
>
> **Next Steps:**
> - Copy test files to your project's `test/` directory
> - Run `npm install` to add test dependencies (vitest, playwright, fishery, msw, etc.)
> - Run `npx vitest run --workspace=unit` to execute unit tests
> - Run `npx playwright test` to execute E2E tests
> - Run `/jaan-to:qa-test-review` to review test quality (when available)
> - See the main document for full CI integration guide

## Step 14: Capture Feedback

Use AskUserQuestion:
- Question: "How did the test generation turn out?"
- Header: "Feedback"
- Options:
  - "Perfect!" -- Done
  - "Needs fixes" -- What should I improve?
  - "Learn from this" -- Capture a lesson for future runs

If "Learn from this": Run `/jaan-to:learn-add qa-test-generate "{feedback}"`

---

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/qa-test-generate-reference.md` section "Key Generation Rules" for BDD-to-assertion mapping table, tag-to-tier routing, test data factory and MSW handler patterns, and anti-patterns to avoid.

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Multi-stack support via `tech.md` detection
- Template-driven output structure
- Output to standardized `$JAAN_OUTPUTS_DIR` path

## Definition of Done

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/qa-test-generate-reference.md` section "Definition of Done Checklist" for the complete checklist.
