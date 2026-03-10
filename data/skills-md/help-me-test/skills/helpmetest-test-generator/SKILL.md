---
name: helpmetest-test-generator
description: "Use this skill when the user wants tests written for a specific feature or flow. Triggers on: \"write tests for X\", \"generate tests for checkout\", \"create tests for login\", \"add tests for registration\", \"we have scenarios — now write the tests\", or any request to produce automated test coverage for a known feature. Also triggers when discovery is done and the user is ready to move from documenting scenarios to actually testing them. Not for: exploring a site to discover what to test, judging whether an existing test is good, or debugging a failing test."
allowed-tools: mcp__helpmetest-*
---

# QA Test Generator

Generates tests for ONE feature at a time.

**Scope:** This skill works on a SINGLE FEATURE. Use `/helpmetest` for comprehensive site testing.

**This skill is for PHASE 3 (Test Generation) - use it only after feature discovery is complete.**

Why this matters: Tests written without complete scenario enumeration end up being blind guesses. You need to know what SHOULD happen (from interactive exploration) before you can write a test that verifies it happens.

**Prerequisites before using this skill:**
- ✅ ALL features have been discovered
- ✅ ALL scenarios have been enumerated (functional + edge_cases + non_functional)
- ✅ Features have been explored interactively to discover test scenarios
- ✅ Phase 2 (Feature Enumeration) is 100% complete

**If you're still discovering features or enumerating scenarios, use /helpmetest-discover instead.**

## Prerequisites

Before generating tests, load the quality standards and debugging guidance. These define what makes a good test vs a bullshit test, and how to fix failures when they happen.

Call these before starting:
```
how_to({ type: "test_quality_guardrails" })
how_to({ type: "tag_schema" })
how_to({ type: "interactive_debugging" })
```

## Input

- Feature artifact ID (e.g., "feature-checkout") - optional if can be inferred

## Workflow

### Phase 0: Context Discovery

Check for existing work before asking the user for input. This prevents redundant questions and lets you resume where you left off.

Call `how_to({ type: "context_discovery" })` to see what's already been done.

- Prioritize features with `status: "untested"`
- Find scenarios with empty `test_ids` arrays
- **Sort scenarios by priority** - Test `priority:critical` scenarios first. These are the end-to-end flows that prove the core business value works. If you test 10 partial scenarios but skip the 1 critical end-to-end flow, you've missed the most important verification.
- **Validate coverage before claiming done** - Before saying "all features tested", check that ALL `priority:critical` scenarios have test_ids. Otherwise you're claiming coverage you don't have.
- If user says "continue"/"next" → auto-select first untested feature with critical scenarios

### Phase 1: Understand the Feature

1. **Read Feature artifact** using `helpmetest_get_artifact`
2. **Extract**:
   - goal - What must work?
   - persona_ids - Who can use this? (get auth_state from Persona)
   - functional - Main scenarios (Given/When/Then)
   - edge_cases - Boundary conditions
   - bugs - Known broken scenarios (skip these)

### Phase 1.5: Explore Before Writing

Before generating any test, run the scenario interactively using `helpmetest_run_interactive_command`. This isn't optional cleanup for vague scenarios — it's the default workflow for every scenario.

Why: a test written from a scenario description is a hypothesis. A test written after you ran it is a specification. The second kind uses real selectors, reflects actual UI behavior, and fails for the right reasons.

For each scenario (starting with priority:critical):

1. **Authenticate** — `As <auth_state>` to establish the session
2. **Navigate** — `Go To <scenario.url>` and observe what loads
3. **Execute the Given** — establish the precondition, confirm it's in place
4. **Execute the When** — perform the action, observe what happens next
5. **Verify the Then** — check the outcome. Try the actual assertion selectors.
6. **For edge cases** — try the invalid input, observe the exact error message and selector

After each interactive run, you have:
- Confirmed selectors (not guessed `data-testid` attributes that may not exist)
- Actual timing behavior (know where waits are needed)
- The real outcome text (not assumed "Success" when it says "Saved")

**If the backend is unavailable:** Fall back to extracting selectors from existing passing tests for the same feature (via `helpmetest_status` with verbose flag). This is the fallback, not the default.

### Phase 2: Generate Tests for Scenarios

**Test generation order matters:**
1. **Generate `priority:critical` scenarios FIRST** - These are end-to-end workflows that verify core business value
2. **Then generate `priority:high` scenarios** - Important but not mission-critical
3. **Finally generate `priority:medium/low` scenarios** - Nice-to-have coverage

Why this order? Critical scenarios prove the feature actually works for users. If you test 10 edge cases but never verify the happy path works end-to-end, you've missed the point. Test the core transaction first, then fill in the edges.

**Critical vs. Partial test distinction:**
- ❌ **PARTIAL test** - "User can view form page" (just navigation, verifies form fields exist)
- ✅ **CRITICAL test** - "User completes the workflow" (full end-to-end transaction from start to confirmation)

**Before claiming a feature is "tested":**
- ALL `priority:critical` scenarios need `test_ids` populated
- If ANY critical scenario is untested, the feature status is "untested"
- Don't generate 10 partial tests and skip the 1 critical end-to-end flow - that's false coverage

For each functional scenario (starting with critical), create test using `helpmetest_upsert_test`:

```robot
*** Test Cases ***
<scenario.name>
    [Documentation]    Given: <given> | When: <when> | Then: <then>
    [Tags]    priority:high    feature:<feature_id>    project:<project_id>

    # Setup - authenticate if needed
    As  <auth_state>
    Go To  <scenario.url>

    # Given - establish precondition
    <steps to establish 'given' state>

    # When - perform action
    <steps for 'when' action>

    # Then - verify outcome
    <assertions for 'then' expected outcome>
```

**Test naming rules:**
- **NO project/site names** in test names (e.g., NOT "EverShop User Login")
- **Use feature descriptions** from scenario.name (e.g., "User can login with valid credentials")
- **Format:** `<Actor> can <action> <object>` OR `<Feature> <behavior>`
- **Examples:**
  - ✅ "User can update profile email"
  - ✅ "Cart total updates when quantity changes"
  - ✅ "Registration validates email format"
  - ❌ "EverShop Registration Test"
  - ❌ "QA Playground Login"
  - ❌ "SiteName Profile Update"

**Test requirements:**
- 5+ meaningful steps
- Verify actual business outcomes
- Use stable selectors
- Include relevant assertions
- Use `Create Fake Email` for registration/email tests (never hardcode emails)

### Phase 3: Generate Edge Case Tests

For critical edge_cases:

```robot
*** Test Cases ***
Edge Case: <scenario.name>
    [Documentation]    Given: <given> | When: <when> | Then: <then>
    [Tags]    priority:medium    feature:<feature_id>    project:<project_id>

    # Setup and execute edge case scenario
    ...
```

### Phase 4: Validate Test Quality

Every test needs validation before running. This catches bullshit tests early - tests that verify page structure instead of business functionality, or tests that would pass even if the feature is broken.

Validate each test using `/helpmetest-validator`:

1. Pass test ID and feature ID to validator
2. Validator checks:
   - Business value (would test fail if feature broken?)
   - No bullshit patterns (element counting, click without verification)
   - Proper assertions and state verification
3. **If REJECTED:**
   - Read validator feedback
   - Fix test based on specific issues
   - Validate again
   - Repeat until PASSED
4. **If PASSED:**
   - Continue to Phase 6

Don't skip validation - running unvalidated tests wastes time when they fail for the wrong reasons or pass when the feature is broken.

### Phase 5: Link Tests to Scenarios

Update Feature artifact - add test_id to each scenario's test_ids:

```json
{
  "functional": [
    {
      "name": "Create new item",
      "given": "...",
      "when": "...",
      "then": "...",
      "test_ids": ["test-create-new-item"]
    }
  ]
}
```

### Phase 6: Run and Debug Tests

1. **Run test** using `helpmetest_run_test`

2. **If test PASSES:**
   - ✅ Move to next scenario
   - Update scenario status

3. **If test FAILS - use `/helpmetest-debugger`:**

   Don't guess or make blind fixes. The debugger skill reproduces failures interactively, identifies whether the problem is a test issue (fixable) or an application bug (document in Feature.bugs), and validates fixes before applying them.

   Pass it: the failing test ID, the error message, and the Feature artifact ID.

4. **Update Feature.status** based on results:
   - All tests pass → "working"
   - All tests fail due to bugs → "broken"
   - Mixed → "partial"

## Output

- Test files created via `helpmetest_upsert_test`
- All tests debugged and fixed OR bugs documented
- Feature artifact updated with test_ids on scenarios
- Feature.bugs[] populated for application bugs
- Feature.status updated
- Summary of tests generated, pass rates, bugs found

## Test Quality Requirements

Before creating tests, review what makes a test valuable vs worthless. This prevents writing tests that pass when the feature is broken, or tests that only verify page structure instead of functionality.

Load the quality standards:
```
how_to({ type: "test_quality_guardrails" })
```

This includes:
- ❌ Bullshit test anti-patterns (element counting, click without verification, etc.)
- ✅ Real test patterns (complete workflows with outcome verification)
- Quality checklist (5+ steps, business outcomes, state verification)
- Red flags to avoid

## Quality Checklist

**Before creating ANY test, answer:**
1. "What business capability does this test verify?"
2. "If this test passes but the feature is broken, is that possible?"
   - If YES → Test is bullshit, rewrite it
   - If NO → Test is valid

**A good test includes:**
- [ ] 5+ meaningful steps (not just navigation + counting)
- [ ] Verifies business outcome (data saved, filter applied, order created)
- [ ] Includes state change verification (before/after comparison OR API response check)
- [ ] Uses stable selectors (data-testid preferred)
- [ ] Has proper assertions that would FAIL if feature broken
- [ ] Was validated interactively first

**A bullshit test has:**
- [ ] Only navigation + element counting
- [ ] Click without verifying result of click
- [ ] Form display without testing form submission
- [ ] Success message verification without checking data persisted

## FakeMail Keywords

For registration and email verification tests, use FakeMail:

```robot
# Generate unique test email
${email}=  Create Fake Email
# Returns: adventure.acme@fakemail.helpmetest.com

# Use in registration
Fill Text  input[name=email]  ${email}
Click  button >> "Register"

# Get verification code from email
${code}=  Get Email Verification Code  ${email}
Fill Text  input[name=code]  ${code}

# Cleanup after test
Delete Email  ${email}
```

Always use `Create Fake Email` instead of hardcoding emails. Hardcoded emails cause conflicts when tests run in parallel or multiple times - the second run fails because the email already exists.

## Critical Rules

1. **No bullshit tests** - "Click button, verify page" is NOT a test
2. **Test interactively first** - Never create blind tests
3. **Given/When/Then** - Map scenario to test steps
4. **Link to scenario** - Add test_id to scenario.test_ids
5. **Use FakeMail** - Never hardcode test emails
6. **Tag properly** - All tests need `priority:` tag minimum

**Version:** 0.1
