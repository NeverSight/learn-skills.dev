---
name: helpmetest-debugger
description: "When a test is broken and you need to know why, use this skill. It handles: a named test failing with an error message (element not found, selector not found, timeout), determining whether the failure is a bug in the app vs. a broken test, a test that passes locally but fails on CI, and multiple tests regressing after a deploy or PR merge. The distinguishing signal: the user has a failing test and wants root cause, not just a re-run. Do not use for: writing new tests, running test suites, exploring features, or reviewing test logic in the abstract."
allowed-tools: mcp__helpmetest-*
---

# QA Debugger

Debugs failing tests to determine root cause and fix.

**Golden Rule: ALWAYS reproduce interactively before fixing. Never guess. Never make blind fixes.**

## Prerequisites

Before debugging, load the project context and debugging guides:

```
how_to({ type: "context_discovery" })
how_to({ type: "interactive_debugging" })
how_to({ type: "debugging_self_healing" })
```

`context_discovery` tells you which Feature artifact the failing test belongs to, what scenarios are covered, and whether the bug is already known. This prevents documenting a bug that's already in `feature.bugs[]`.

## Input

- Failing test ID
- Error message/logs
- Feature artifact the test belongs to

## Workflow

### Phase 1: Understand the Failure

1. **Get test details** using `helpmetest_open_test`
2. **Get test history** using `helpmetest_status({ id: "test-id", testRunLimit: 10 })`
3. **Classify failure pattern** (see the self-healing guide loaded above):
   - Selector issue? Timing issue? State issue? API issue? Data issue? **Test isolation?**
   - Refer to pattern categories to identify symptoms and determine root cause
4. **Get Feature** using `helpmetest_get_artifact`
5. **Identify failure point**:
   - Which step failed?
   - What was the error?
   - What was expected vs actual?

### Phase 2: Reproduce Interactively

**Don't skip this step.** Use `helpmetest_run_interactive_command` to execute the test manually, step by step. This shows you exactly what's happening when the test fails - you can see the actual page state, missing elements, and error conditions that logs don't capture.

1. **Get Persona** for auth_state if needed

2. **Start interactive session** - Execute steps ONE AT A TIME, observing after EACH step:
   ```robot
   As  <auth_state>
   Go To  <url>
   ```
   **→ Observe:** Did page load? Check URL. Look at page content.

3. **Execute steps leading up to failure** - Run each step separately:
   ```robot
   Fill Text  <selector>  <value>
   ```
   **→ Observe:** Did field get filled? Check with `Get Attribute  <selector>  value`

   ```robot
   Click  <button-selector>
   ```
   **→ Observe:** What happened after click? Did page change? Check `Get Url`

4. **When you reach the failing step, investigate based on error type:**

   **Element not found:**
   - List all elements of that type on the page (buttons, inputs, etc.)
   - Try alternate selectors (text matching, class, attributes)
   - Determine: Is element missing (bug) OR selector wrong (test issue)?

   **Element not interactable:**
   - Check if element is visible and enabled
   - Check if need to scroll to element
   - Check if multiple matches exist
   - Check if need to wait for element to become interactable
   - Determine: What's blocking interaction?

   **Wrong value/assertion failed:**
   - Check what's actually displayed
   - Check what page you're on
   - Check for error messages on page
   - Determine: Is behavior a bug OR did expectations change?

   **Timeout/page load failure:**
   - Try with longer timeout
   - Check where you ended up (Get Url)
   - Check for API responses
   - Wait for key elements that indicate page loaded
   - Determine: Is app slow (increase timeout) OR broken (bug)?

5. **Document findings after investigation:**
   - Exact step that failed
   - What you expected
   - What actually happened
   - Root cause (selector wrong, timing issue, feature broken, etc.)

### Phase 3: Determine Root Cause

Refer to the self-healing guide (loaded above via `how_to`) for all failure pattern categories and fixes.

Quick reference:
- **Test isolation**: Alternating PASS/FAIL + changing error values + shared state → Make idempotent
- **Selector issues**: Element not found → Fix selector or document bug
- **Timing issues**: Timeouts, element not visible → Add waits
- **State issues**: Auth/session problems → Verify state restoration
- **API issues**: Backend errors → Document as bug
- **Data issues**: Conflicts, duplicates → Use unique data or cleanup

### Phase 4A: Fix Test Issue

If problem is with the test (NOT a bug in the application):

1. **Identify fix** based on interactive investigation:
   - Update selector (found correct selector during investigation)
   - Add wait/timeout (saw element appears after delay)
   - Fix expected value (saw actual correct value during investigation)
   - Add missing setup step (discovered required state during investigation)

2. **Validate fix interactively before updating test:**

   Run the COMPLETE corrected flow interactively to prove it works. Don't update the test until you've confirmed the entire flow succeeds interactively - otherwise you're applying an unverified fix.
   ```robot
   # Run the FULL test with fixes applied
   As  <auth_state>
   Go To  <url>

   # Step 1 with fix
   Fill Text  <corrected-selector>  <value>
   Get Attribute  <corrected-selector>  value  ==  <value>  # Verify it worked

   # Step 2 with fix
   Wait For Elements State  <button>  enabled  timeout=5000  # Added wait
   Click  <button>

   # Step 3 with fix
   Wait For Response  url=/api/submit  status=200  # Verify API call
   Get Text  .success  ==  Saved successfully  # Updated expected text

   # Verify outcome
   Go To  <url>  # Reload to verify persistence
   Get Attribute  <selector>  value  ==  <value>  # Confirm data saved
   ```

   **→ If ANY step fails during interactive validation, STOP and investigate more**
   **→ Only proceed when ENTIRE flow runs successfully interactively**

3. **Update test** using `helpmetest_upsert_test` with validated fixes

4. **Run test** using `helpmetest_run_test` to confirm automated version works

5. **If test STILL fails:**
   - Return to Phase 2 (reproduce interactively)
   - Compare automated test output with interactive output
   - Find the difference
   - Repeat until test passes

### Phase 4B: Document Bug

If problem is with the feature:

1. **Add bug to Feature.bugs**:
   ```json
   {
     "name": "Brief description",
     "given": "Precondition",
     "when": "Action taken",
     "then": "Expected outcome",
     "actual": "What actually happens",
     "severity": "blocker|critical|major|minor",
     "url": "http://example.com/page",
     "tags": ["affects:all-users"],
     "test_ids": []
   }
   ```

2. **Update Feature.status** to "broken" or "partial"

3. **Skip or tag test** until bug is fixed

### Phase 5: Update Feature Status

After debugging:

1. **Update Feature.status**:
   - "working": All scenarios pass
   - "broken": Critical scenarios fail due to bugs
   - "partial": Some scenarios pass, some fail

2. **Update ProjectOverview.features** with works: true/false

## Output

- Root cause identified
- Test fixed OR bug documented
- Feature.status updated
- Summary of actions taken

## Self-Healing Patterns

Refer to the self-healing guide (loaded above via `how_to`) for all auto-fixable patterns and strategies.

## Critical Rules

1. **Always reproduce first** - Don't guess, verify
2. **Determine bug vs test issue** - Different actions needed
3. **Update artifacts** - All findings go into Feature
4. **Verify fixes** - Run test after fixing

**Version:** 0.1
