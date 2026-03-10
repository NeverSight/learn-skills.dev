---
name: helpmetest-validator
description: "Invoke this skill when a user shares test code and questions whether it actually works as intended — not to run or fix the test, but to evaluate whether the test has real value. Triggers on: \"is this test any good?\", \"would this catch a real bug?\", \"this test always passes — is that normal?\", \"review these tests before I commit\", or \"does this test verify anything meaningful?\". Also triggers when someone suspects a test is useless, wants a pre-commit quality gate, or is unsure if an auto-generated test is worth keeping. The core question this skill answers: \"Would this test fail if the feature broke?\" If not, the test gets rejected. Do NOT use for generating new tests, fixing failing tests, or exploring application features."
allowed-tools: mcp__helpmetest-*
---

# QA Validator

Validates and scores test quality. Rejects tests that don't meet quality standards.

## Prerequisites

```
how_to({ type: "context_discovery" })
how_to({ type: "test_quality_guardrails" })
```

`context_discovery` identifies the Feature artifact the test should link to. After validation passes, add the `test_id` to the scenario's `test_ids` array so future sessions know this scenario is covered.

## Input

- Test ID or test content to validate
- Feature artifact it should test

## Validation Workflow

### Step 1: The Business Value Question (MOST IMPORTANT)

Before checking anything else, answer these two questions:

1. **"What business capability does this test verify?"**
2. **"If this test passes but the feature is broken, is that possible?"**

**If answer to #2 is YES → IMMEDIATE REJECTION**

This is the ONLY question that truly matters. A test that passes when the feature is broken is worthless.

Examples of worthless tests:
- Test only counts form fields → REJECT (form could be broken, test still passes)
- Test clicks button, waits for same element → REJECT (button could do nothing, test still passes)
- Test navigates, verifies title → REJECT (navigation works, feature could be broken)

### Step 2: Check for Anti-Patterns (Auto-Reject)

Check for these bullshit patterns:

- ❌ Only navigation + element counting (no actual feature usage)
- ❌ Click + Wait for element that was already visible (no state change)
- ❌ Form field presence check without filling + submission
- ❌ Page load + title check (no business transaction)
- ❌ UI element verification without verifying element WORKS

**If ANY anti-pattern found → IMMEDIATE REJECTION**

### Step 3: Check Minimum Quality Requirements

- Step count >= 5 meaningful steps?
- Has >= 2 assertions (Get Text, Should Be, Wait For)?
- Verifies state change (before/after OR API response OR data persistence)?
- Tests scenario's Given/When/Then, not just "page loads"?
- Uses stable selectors?
- Has [Documentation]?
- Tags use category:value format (priority:high)?
- Has required tags: priority:?
- Tags include feature:?
- No invalid tags?

**If ANY requirement fails → REJECT with specific feedback**

### Step 4: Generate Validation Report

Output either:
- **✅ PASS:** Test verifies feature works, would fail if feature broken
- **❌ REJECT:** [Specific reason] - Test doesn't verify feature functionality

Include:
- Test ID
- Feature ID
- Scenario name
- Status (PASS/REJECT)
- If REJECT: specific feedback on what needs to be fixed
- If PASS: any optional recommendations for improvement

## Output

- Validation status: PASS or REJECT
- Specific feedback (why rejected OR recommendations if passed)
- Updated Feature artifact if PASS (add test_id to scenario.test_ids)

## Rejection Examples

### REJECT: Element Counting

```robot
Go To  /profile
Get Element Count  input[placeholder='John']  ==  1
Get Element Count  button[type='submit']  ==  1
```
**Reason:** Only counts elements, doesn't test if form works. Test passes even if form submission broken.

### REJECT: Click Without Verification

```robot
Go To  /videos
Click  [data-testid='category-python']
Wait For Elements State  [data-testid='category-python']  visible
```
**Reason:** Waits for element that was already visible. Doesn't verify videos were filtered. Test passes even if filter broken.

### REJECT: Navigation Only

```robot
Go To  /checkout
Get Title  ==  Checkout
Get Element Count  input[name='address']  ==  1
```
**Reason:** Only navigation + element existence. Doesn't test checkout works. Test passes even if checkout endpoint broken.

### REJECT: Form Display Without Submission

```robot
Go To  /register
Get Element Count  input[type='email']  ==  1
Get Element Count  input[type='password']  ==  1
```
**Reason:** Only checks form exists, doesn't test registration. Test passes even if registration endpoint returns 500.

### PASS: Complete Workflow

```robot
Go To  /profile
Fill Text  input[name='firstName']  John
Click  button[type='submit']
Wait For Response  url=/api/profile  status=200
Reload
Get Attribute  input[name='firstName']  value  ==  John
```
**Reason:** Tests complete workflow - user can update AND data persists. Would fail if feature broken.

**Version:** 0.1
