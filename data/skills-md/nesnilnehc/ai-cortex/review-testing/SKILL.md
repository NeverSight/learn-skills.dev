---
name: review-testing
description: "Review code for testing: test existence, coverage adequacy, test quality and structure, edge-case and error-path coverage, and test maintainability. Cognitive-only atomic skill; output is a findings list."
tags: [eng-standards]
related_skills: [review-diff, review-codebase, review-code, run-automated-tests]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# Skill: Review Testing

## Purpose

Review code for **testing** concerns only. Do not define scope (diff vs codebase) or perform language/framework/security/architecture analysis; those are separate atomic skills. Emit a **findings list** in the standard format for aggregation. Focus on test existence and coverage, test quality and structure, test types and layering, edge-case and error-path coverage, and test maintainability.

---

## Core Objective

**Primary Goal**: Produce a testing-focused findings list covering test existence, coverage adequacy, test quality/structure, test types/layering, edge-case coverage, and test maintainability for the given code scope.

**Success Criteria** (ALL must be met):

1. ✅ **Testing-only scope**: Only testing dimensions are reviewed; no scope selection, language/framework conventions, security, performance, or architecture analysis performed
2. ✅ **All six testing dimensions covered**: Test existence, coverage adequacy, quality/structure, types/layering, edge cases/error paths, and maintainability are assessed where relevant
3. ✅ **Findings format compliant**: Each finding includes Location, Category (`cognitive-testing`), Severity, Title, Description, and optional Suggestion
4. ✅ **High-risk gaps flagged**: Untested or poorly tested high-risk code paths (auth, payment, data mutation) are marked `critical` or `major`
5. ✅ **Analysis from code only**: Test adequacy is assessed from code structure and available artifacts, without running tests or generating coverage reports

**Acceptance Test**: Does the output contain a testing findings list covering all relevant dimensions with risk-appropriate severity ratings and actionable suggestions for improving test coverage and quality?

---

## Scope Boundaries

**This skill handles**:
- Test existence checks (missing test files for key modules, services, public functions)
- Coverage adequacy analysis (high-risk path coverage: auth, payment, data mutation)
- Test quality and structure (arrange-act-assert, meaningful assertions, behavior-not-implementation)
- Test types and layering (unit, integration, e2e balance; mock/stub isolation)
- Edge case and error path coverage (boundary conditions, invalid inputs, failure modes)
- Test maintainability (DRY without sacrificing readability, fixture organization, brittle test detection)

**This skill does NOT handle**:
- Scope selection (deciding which files/paths to analyze) — scope is provided by the caller
- Running tests or generating coverage reports — use `run-automated-tests` for test execution
- Language/framework-specific test conventions — use `review-dotnet`, `review-java`, `review-go`, etc.
- Security, performance, or architecture review — use respective atomic skills
- Full orchestrated review — use `review-code`

**Handoff point**: When all testing findings are emitted, hand off to `review-code` for aggregation in an orchestrated review. For actually running tests, redirect to `run-automated-tests`.

---

## Use Cases

- **Orchestrated review**: Used as a cognitive step when [review-code](../review-code/SKILL.md) runs scope → language → framework → library → cognitive.
- **Testing-focused review**: When the user wants only test health and coverage evaluated (e.g. before release, after major refactor, or during onboarding).
- **Gap analysis**: Identify untested modules, missing test types (unit/integration/e2e), or low-quality tests that provide false confidence.

**When to use**: When the task includes testing review. Scope and code scope are determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: Testing dimensions in the **given code scope** (files or diff provided by the caller). Do not decide scope; accept the code range as input.
- **Do not**: Perform scope selection, language/framework conventions, security, performance, or architecture review. Focus only on testing.

### Review checklist (testing dimension only)

1. **Test existence**: Do key modules, services, and public functions have corresponding test files? Are there obvious gaps where critical logic has no tests at all?
2. **Coverage adequacy**: Is test coverage sufficient for the risk level of the code? Are high-risk paths (authentication, payment, data mutation) tested? Note: if coverage reports or metrics are available, reference them; otherwise assess structurally.
3. **Test quality and structure**: Are tests well-structured (arrange-act-assert or given-when-then)? Do test names clearly describe the scenario? Are assertions meaningful (not just "no exception thrown")? Do tests verify behavior rather than implementation details?
4. **Test types and layering**: Is there an appropriate mix of unit, integration, and end-to-end tests? Are unit tests isolated (mocks/stubs for external dependencies)? Are integration tests testing real interactions where needed?
5. **Edge cases and error paths**: Do tests cover boundary conditions, invalid inputs, empty/null cases, concurrency scenarios, and expected error responses? Are failure modes explicitly tested?
6. **Test maintainability**: Are tests DRY without sacrificing readability? Are test fixtures and helpers well-organized? Are tests brittle (tightly coupled to implementation, excessive mocking, or reliant on execution order)? Is test data management clean (factories, builders, or fixtures rather than hardcoded magic values)?

### Tone and references

- **Professional and technical**: Reference specific locations (file:line or module). Emit findings with Location, Category, Severity, Title, Description, Suggestion. Use severity `major` or `critical` for untested high-risk code paths.

---

## Input & Output

### Input

- **Code scope**: Files or directories (or diff) already selected by the user or scope skill. This skill does not decide scope; it reviews the provided code for testing only.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **cognitive-testing**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform scope selection, language, framework, security, performance, or architecture review. Stay within testing dimensions.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** require running tests or generating coverage reports. Analyze test adequacy from the code and available artifacts (e.g. existing coverage files). For actually running tests, use [run-automated-tests](../run-automated-tests/SKILL.md).
- **Do not** penalize absence of tests for trivial code (simple getters, constants, generated code) unless it masks a real risk.

### Skill Boundaries

**Do NOT do these** (other skills handle them):
- Do NOT select or define the code scope — scope is determined by the caller or `review-code`
- Do NOT run or execute tests — use `run-automated-tests` for test execution
- Do NOT perform language/framework-specific test convention analysis — use respective language skills
- Do NOT perform security, performance, or architecture analysis — use respective atomic skills

**When to stop and hand off**:
- When all testing findings are emitted, hand off to `review-code` for aggregation in an orchestrated review
- When the user needs tests to actually run, redirect to `run-automated-tests`
- When the user needs a full review (scope + language + cognitive), redirect to `review-code`

---

## Self-Check

### Core Success Criteria

- [ ] **Testing-only scope**: Only testing dimensions are reviewed; no scope selection, language/framework conventions, security, performance, or architecture analysis performed
- [ ] **All six testing dimensions covered**: Test existence, coverage adequacy, quality/structure, types/layering, edge cases/error paths, and maintainability are assessed where relevant
- [ ] **Findings format compliant**: Each finding includes Location, Category (`cognitive-testing`), Severity, Title, Description, and optional Suggestion
- [ ] **High-risk gaps flagged**: Untested or poorly tested high-risk code paths (auth, payment, data mutation) are marked `critical` or `major`
- [ ] **Analysis from code only**: Test adequacy is assessed from code structure and available artifacts, without running tests or generating coverage reports

### Process Quality Checks

- [ ] Was only the testing dimension reviewed (no scope/language/security/architecture)?
- [ ] Are test existence, coverage adequacy, quality/structure, types/layering, edge cases, and maintainability covered where relevant?
- [ ] Is each finding emitted with Location, Category=cognitive-testing, Severity, Title, Description, and optional Suggestion?
- [ ] Are critical gaps (untested high-risk code) clearly flagged and actionable?

### Acceptance Test

Does the output contain a testing findings list covering all relevant dimensions with risk-appropriate severity ratings and actionable suggestions for improving test coverage and quality?

---

## Examples

### Example 1: Missing tests for critical module

- **Input**: Payment processing module with no test files.
- **Expected**: Emit a critical finding for missing tests on high-risk code; suggest creating unit tests for core payment logic and integration tests for gateway interactions. Category = cognitive-testing.

### Example 2: Tests exist but are shallow

- **Input**: Auth module has tests, but they only cover the happy path (valid login) and skip invalid credentials, expired tokens, rate limiting, and account lockout.
- **Expected**: Emit a major finding for insufficient edge-case coverage; list specific scenarios to add. Category = cognitive-testing.

### Edge case: Well-tested codebase

- **Input**: Module has comprehensive unit, integration, and e2e tests with clear structure and good coverage.
- **Expected**: Emit zero findings or a suggestion-level finding for minor improvements (e.g. test naming consistency). Do not invent issues.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` or module name (optional line or range). |
| **Category** | `cognitive-testing`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1–3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `src/payment/processor.go`
- **Category**: cognitive-testing
- **Severity**: critical
- **Title**: No tests for payment processing module
- **Description**: The payment processor handles charge, refund, and webhook verification but has no corresponding test file. This is high-risk code that directly affects revenue.
- **Suggestion**: Create `processor_test.go` with unit tests for charge/refund logic (mock gateway) and integration tests for webhook signature verification.
```
