---
name: qa-test-cases
description: Generate production-ready BDD/Gherkin test cases from acceptance criteria using ISTQB techniques. Use when writing test specifications.
allowed-tools: Read, Glob, Grep, Write($JAAN_OUTPUTS_DIR/qa/**), Task, WebSearch, Edit(jaan-to/config/settings.yaml)
argument-hint: [acceptance-criteria | prd-path | jira-id | (interactive)]
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# qa-test-cases

> Generate production-ready BDD/Gherkin test cases from acceptance criteria.

## Context Files

- `$JAAN_LEARN_DIR/jaan-to-qa-test-cases.learn.md` - Past lessons (loaded in Pre-Execution)
- `$JAAN_TEMPLATES_DIR/jaan-to-qa-test-cases.template.md` - BDD/Gherkin template
- `$JAAN_TEMPLATES_DIR/jaan-to-qa-test-cases-quality-checklist.template.md` - Quality checklist template
- Research: `$JAAN_OUTPUTS_DIR/research/50-qa-test-cases.md` - ISTQB standards, test design techniques
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

## Input

**Acceptance Criteria Source**: $ARGUMENTS

Input modes:
1. **Direct text**: Paste acceptance criteria directly
2. **PRD path**: Path to PRD file (from /jaan-to:pm-prd-write output)
3. **Jira ID**: Story ID (if Jira MCP available)
4. **Interactive**: Empty arguments triggers wizard

IMPORTANT: The input above is your starting point. Determine mode and proceed accordingly.

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `qa-test-cases`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

Also read the comprehensive research document:
`$JAAN_OUTPUTS_DIR/research/50-qa-test-cases.md`

This provides:
- ISTQB test case specification standards (Section 2)
- BDD/Gherkin format guidance (Section 2)
- Test design techniques: Equivalence Partitioning, BVA, Decision Tables (Section 3)
- Eight-step transformation workflow (Section 4)
- Edge case taxonomy - 5 priority categories (Section 5)
- Quality validation checklist (Section 6)
- AI failure mode mitigation patterns (Section 8)

If files do not exist, continue without them.

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_qa-test-cases`

---

# PHASE 1: Analysis (Read-Only)

## Step 1: Determine Input Mode and Extract AC

Check $ARGUMENTS to identify input mode:

**Mode A - Direct Text Input:**
If $ARGUMENTS contains acceptance criteria text:
1. Parse the AC directly
2. Extract testable conditions
3. Proceed to Step 2

**Mode B - PRD File Path:**
If $ARGUMENTS contains file path pattern (e.g., ".md" or "$JAAN_OUTPUTS_DIR/"):
1. Use Read tool to open the file
2. Locate "Acceptance Criteria" or "User Stories" section
3. Extract all AC statements
4. Preview extracted AC:
   ```
   EXTRACTED ACCEPTANCE CRITERIA
   ──────────────────────────────
   1. {ac_1}
   2. {ac_2}
   3. {ac_3}
   ```
5. Ask: "Use these acceptance criteria? [y/edit]"

**Mode C - Jira MCP Integration:**
If $ARGUMENTS matches pattern "PROJ-123" or "JIRA-123":
1. Check if Jira MCP is available
2. If available: Fetch story → extract AC → preview
3. If unavailable: "Jira MCP not detected. Please paste AC or provide file path."

**Mode D - Interactive Wizard:**
If $ARGUMENTS is empty:
1. Ask: "How would you like to provide acceptance criteria?"
   > [1] Paste AC text directly
   > [2] Provide PRD file path
   > [3] Enter Jira story ID
2. Based on selection, route to appropriate mode

**Ambiguity Resolution (from research Section 4):**

If AC is vague, ask these questions before proceeding:
1. "What happens when required fields are empty?"
2. "What are the min/max boundaries for each input field?"
3. "What specific error messages should display for each failure?"
4. "What happens on system/network failure mid-operation?"
5. "Are there concurrent user scenarios to consider?"
6. "What permissions/roles are required for this action?"

## Step 2: Apply Test Design Techniques

For each acceptance criterion, analyze using research Section 3 methodologies:

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/qa-test-cases-reference.md` section "Test Design Techniques" for Equivalence Partitioning, Boundary Value Analysis, Edge Case Categorization (5 priority categories), and Test Generation Ratio (minimum 10 tests per AC).

## Step 3: Generate Test Inventory Summary

Calculate totals and show plan:

```
TEST GENERATION PLAN
────────────────────────────────────────
Acceptance Criteria: {n} criteria

Test Breakdown (per AC):
  - Positive tests: {n} × 3 = {total}
  - Negative tests: {n} × 3 = {total}
  - Boundary tests: {n} × 2 = {total}
  - Edge case tests: {n} × 2 = {total}

Total Test Cases: {grand_total}

Edge Case Distribution:
  - Empty/Null States: {count}
  - Boundary Values: {count}
  - Error Conditions: {count}
  - Concurrent Operations: {count}
  - State Transitions: {count}

Coverage Targets (Research Section 5):
  - Positive: 30%
  - Negative: 40%
  - Edge: 30%
  - Industry standard: 70-80% coverage
```

Ask: "Proceed with test case generation? [y/edit]"

---

# HARD STOP - Human Review Check

Show complete plan before generating:

```
FINAL CONFIRMATION
──────────────────────────────────────
Source: {input_mode}
Acceptance Criteria: {n} criteria
Total Test Cases: {count}

Output Format: BDD/Gherkin (with ISTQB conversion notes)
Output Folder: $JAAN_OUTPUTS_DIR/qa/cases/{id}-{slug}/
Main File: {id}-test-cases-{slug}.md
Quality Checklist: {id}-test-cases-quality-checklist-{slug}.md

Process:
1. Generate BDD/Gherkin scenarios using research patterns
2. Apply concrete test data values (no placeholders)
3. Add @tags for traceability and filtering
4. Include ISTQB conversion notes (research Section 2)
5. Generate quality checklist (research Section 6)
6. Preview before writing
```

> "Proceed with test case generation? [y/n]"

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Generation (Write Phase)

## Step 4: Generate BDD/Gherkin Test Cases

Following research Section 2 patterns and Section 4 worked examples.

### 4.0 Declarative Gherkin Enforcement Rule

**CRITICAL**: All scenarios MUST use declarative style (describe BEHAVIOR, not UI actions).

**BAD (Imperative -- NEVER use):**
```gherkin
When I click the "Login" button
When I enter "test@example.com" in the email field
When I scroll down to the footer
When I select "Option A" from the dropdown
```

**GOOD (Declarative -- ALWAYS use):**
```gherkin
When the user submits valid credentials
When the user requests password reset
When the user selects their preferred plan
When the user completes the checkout process
```

**Rule**: NEVER use imperative UI interaction steps. Describe BEHAVIOR, not UI actions. Steps should be understandable by non-technical stakeholders.

### 4.0.1 Scenario Structure Limits

- **Steps per scenario**: 3-5 (Given/When/Then combined). If exceeding 5, split into multiple scenarios.
- **Scenarios per feature**: 5-10. If exceeding 10, split into sub-features.
- **Scenario Outline promotion**: Use `Scenario Outline` with `Examples` tables when 3+ input combinations exist for the same behavior pattern.

Example Scenario Outline:
```gherkin
Scenario Outline: User login with various credential types
  Given a registered user with <credential_type>
  When the user submits valid credentials
  Then the user should be authenticated within 3 seconds

  Examples:
    | credential_type     |
    | email and password  |
    | social login        |
    | SSO token           |
```

### 4.0.2 Standardized Step Templates

Use these declarative patterns as starting points:
- `Given a {entity} exists with {attribute} "{value}"`
- `Given the user is authenticated as {role}`
- `When the user {action} the {entity}`
- `When the user submits {valid/invalid} {data_type}`
- `Then the {entity} should have {attribute} "{value}"`
- `Then the user should see {feedback_type}`
- `Then the system should {expected_behavior}`

### 4.1 Feature Header

```gherkin
@{test-type} @priority-{level} @REQ-{id}
Feature: {Feature Name}
  As a {role}
  I want {goal}
  So that {benefit}
```

### 4.2 Background Section

Common preconditions shared across scenarios:

```gherkin
  Background:
    Given {common_precondition_1 with concrete data}
    And {common_precondition_2}
    And {system_state}
```

### 4.3 Generate Scenarios (Research Section 4 pattern)

**Positive Tests (3 per AC):**

```gherkin
  @smoke @positive @priority-critical @REQ-{id}
  Scenario: {Main happy path}
    Given I am on the {page_name} page
    When I enter "{concrete_value}" in the {field_name} field
    And I enter "{concrete_value}" in the {field_name} field
    And I click the "{button_label}" button
    Then I should be redirected to {path} within {n} seconds
    And I should see "{exact_message}" in the {element}

  @regression @positive @priority-high @REQ-{id}
  Scenario: {Alternative happy path}
    Given {different_valid_state}
    When {valid_action_variation}
    Then {expected_outcome_with_threshold}
```

**Negative Tests (3 per AC):**

```gherkin
  @regression @negative @priority-high @REQ-{id}
  Scenario: {Invalid input scenario}
    Given {precondition}
    When I enter "{invalid_concrete_value}" in the {field} field
    And I click the "{button}" button
    Then I should see error "{exact_error_text}"
    And I should remain on the {page} page
    And {system_state_unchanged}
```

**Boundary Tests (2 per AC):**

```gherkin
  @boundary @edge-case @priority-medium @REQ-{id}
  Scenario: {Minimum boundary}
    Given {setup}
    When I enter "{min_value}" in the {field} field
    Then {expected_result_at_boundary}

  @boundary @edge-case @priority-medium @REQ-{id}
  Scenario: {Maximum boundary}
    Given {setup}
    When I enter "{max_value}" in the {field} field
    Then {expected_result_at_boundary}
```

**Edge Case Tests (2 per AC from priority categories):**

```gherkin
  @edge-case @empty-state @priority-low @REQ-{id}
  Scenario: {Empty/null handling}
    Given {setup}
    When I leave {field} field empty
    Then I should see validation error "{exact_text}"

  @edge-case @concurrent @priority-high @REQ-{id}
  Scenario: {Concurrent operation}
    Given {multi_user_state}
    When {user_1_action} and {user_2_action} occur simultaneously
    Then {system_prevents_race_condition}
```

### 4.4 Test Data Standards

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/qa-test-cases-reference.md` section "Test Data Standards" for concrete value examples, BAD/GOOD patterns, and standard test data values.

### 4.5 Tagging Strategy

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/qa-test-cases-reference.md` section "Tagging Strategy" for systematic tag application guidelines (@smoke, @regression, @priority, @REQ, etc.).

## Step 5: Generate ISTQB Conversion Notes

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/qa-test-cases-reference.md` section "ISTQB Field Mapping" for the BDD-to-ISTQB field mapping table and example conversion from Gherkin to ISTQB format.

## Step 6: Quality Validation (Research Section 6)

Before preview, validate against 10-point checklist:

**Universal Checks:**
- [ ] All tests map to an AC (Alignment)
- [ ] All steps unambiguous with specific elements (Clarity)
- [ ] All preconditions/data/results documented (Completeness)
- [ ] Expected results measurable with thresholds (Measurable)
- [ ] All test data explicit values, no placeholders (Test Data)
- [ ] Traceability tags present (@REQ-{id})
- [ ] Tests independent, no hidden dependencies (Independence)
- [ ] Tests reproducible by any tester (Reproducibility)
- [ ] Negative coverage included (30%+) (Negative Coverage)
- [ ] Edge coverage addressed (5 categories) (Edge Coverage)

**AI Failure Mode Checks (Research Section 8):**
- [ ] No vague steps ("properly", "correctly", "works")
- [ ] No missing preconditions
- [ ] No non-reproducible scenarios (relative dates, undefined entities)
- [ ] No over-specification (database/internal references)
- [ ] 30/40/30 distribution (positive/negative/edge)

If any check fails, fix before proceeding.

## Step 7: Preview & Approval

### 7.1 Generate Output Metadata

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/id-generator.sh"
SUBDOMAIN_DIR="$JAAN_OUTPUTS_DIR/qa/cases"
mkdir -p "$SUBDOMAIN_DIR"
NEXT_ID=$(generate_next_id "$SUBDOMAIN_DIR")
```

Generate slug:
- Extract feature name from AC or user title
- Convert to lowercase-kebab-case
- Max 50 characters
- Example: "User Login Authentication" → "user-login-authentication"

### 7.2 Generate Executive Summary

Template:
```
Production-ready BDD/Gherkin test cases for {feature_name} covering {n} acceptance criteria with {total_tests} test scenarios. Includes {positive_count} positive tests, {negative_count} negative tests, {boundary_count} boundary tests, and {edge_count} edge case tests across 5 priority categories (empty/null, boundary, error, concurrent, state transition). All tests use concrete test data values and include traceability tags.
```

### 7.3 Show Preview

```
OUTPUT PREVIEW
──────────────────────────────────────
ID: {NEXT_ID}
Folder: $JAAN_OUTPUTS_DIR/qa/cases/{NEXT_ID}-{slug}/
Main: {NEXT_ID}-test-cases-{slug}.md
Checklist: {NEXT_ID}-test-cases-quality-checklist-{slug}.md

# Test Cases: {Feature Name}

## Executive Summary
{executive_summary}

## Metadata
- Acceptance Criteria: {n}
- Total Test Cases: {count}
- Coverage: Positive {pct}%, Negative {pct}%, Edge {pct}%

[Show first 3 scenarios as preview]

@smoke @positive @priority-critical @REQ-001
Scenario: Successful login with valid credentials
  Given I am on the login page
  When I enter "test@example.com" in the email field
  And I enter "ValidP@ss123!" in the password field
  And I click the "Login" button
  Then I should be redirected to the dashboard within 3 seconds
  And I should see "Welcome, Test User" in the header

[Full output contains {total_tests} scenarios]
```

Ask: "Write these output files? [y/n]"

## Step 8: Write Output Files

If approved:

### 8.1 Create Folder

```bash
OUTPUT_FOLDER="$JAAN_OUTPUTS_DIR/qa/cases/${NEXT_ID}-${slug}"
mkdir -p "$OUTPUT_FOLDER"
```

### 8.2 Write Main File

Path: `$OUTPUT_FOLDER/${NEXT_ID}-test-cases-${slug}.md`

Use template from: `$JAAN_TEMPLATES_DIR/jaan-to-qa-test-cases.template.md`

Fill sections:
- Title, Executive Summary
- Metadata table
- Acceptance Criteria Coverage table
- BDD/Gherkin Test Scenarios (all scenarios)
- ISTQB Conversion Notes
- Traceability Matrix
- Test Execution Guidelines
- Quality Checklist Reference
- Appendix

### 8.3 Write Quality Checklist File

Path: `$OUTPUT_FOLDER/${NEXT_ID}-test-cases-quality-checklist-${slug}.md`

Use template from: `$JAAN_TEMPLATES_DIR/jaan-to-qa-test-cases-quality-checklist.template.md`

Fill sections:
- 10-Point Peer Review Checklist
- Anti-Patterns to Reject
- Quality Scoring Rubric (100-point scale with 6 dimensions)
- Coverage Sufficiency Analysis

### 8.4 Update Index

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/index-updater.sh"
add_to_index \
  "$SUBDOMAIN_DIR/README.md" \
  "$NEXT_ID" \
  "${NEXT_ID}-${slug}" \
  "{Feature Name} Test Cases" \
  "{Executive Summary}"
```

### 8.5 Confirm Completion

```
✅ TEST CASES GENERATED
───────────────────────────────────
ID: {NEXT_ID}
Folder: $JAAN_OUTPUTS_DIR/qa/cases/{NEXT_ID}-{slug}/
Main: {NEXT_ID}-test-cases-{slug}.md
Checklist: {NEXT_ID}-test-cases-quality-checklist-{slug}.md
Index: Updated $JAAN_OUTPUTS_DIR/qa/cases/README.md

Total: {count} test cases
Coverage: {positive_pct}% positive, {negative_pct}% negative, {edge_pct}% edge
```

## Step 9: Capture Feedback

Ask: "Any feedback on the test cases? [y/n]"

If yes:
> "[1] Fix now  [2] Learn  [3] Both"

**Option 1 - Fix now:**
- Ask what to improve
- Apply feedback
- Re-validate (Step 6)
- Re-preview (Step 7)
- Re-write

**Option 2 - Learn:**
- Run: `/jaan-to:learn-add qa-test-cases "{feedback}"`

**Option 3 - Both:**
- Fix current output (Option 1)
- Save lesson (Option 2)

If no: Complete

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Multi-stack support via `tech.md` detection
- Template-driven output structure
- Output to standardized `$JAAN_OUTPUTS_DIR` path

## Definition of Done

- [ ] AC extracted and parsed
- [ ] Test design techniques applied (EP, BVA, edge cases)
- [ ] BDD/Gherkin scenarios generated
- [ ] Concrete test data values (no placeholders)
- [ ] Quality validation passed (10-point checklist)
- [ ] ISTQB conversion notes included
- [ ] Executive Summary generated
- [ ] Sequential ID generated
- [ ] Folder created: `{id}-{slug}/`
- [ ] Main file written: `{id}-test-cases-{slug}.md`
- [ ] Quality checklist written: `{id}-test-cases-quality-checklist-{slug}.md`
- [ ] Index updated
- [ ] User approved
