---
name: playwright-e2e-testing
description: |
  Automated end-to-end testing with comprehensive evidence collection using Playwright MCP tools.
  Use when you need to test user flows, validate workflows, run E2E tests, verify application
  behavior, or collect evidence for bug reports. Triggers on "test the user flow", "run E2E test",
  "validate the workflow", "automated testing", "test this feature", or "check if this works".
  Works with web applications, forms, SPAs, and any browser-based interfaces.

---

# Playwright E2E Testing

## Quick Start

Test a login flow with evidence collection:

```
You: "Test the login flow at http://localhost:3000"

Claude: [Runs E2E test with]:
1. Initial state capture (snapshot + screenshot)
2. Form interaction (username/password)
3. Console error monitoring
4. Network request verification
5. Final state capture
6. Comprehensive test report
```

**Result:** Complete test report with screenshots, console logs, network activity, and pass/fail status.

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. E2E Testing Workflow
   3.1. Initial State Capture
   3.2. Test Execution
   3.3. Evidence Collection
   3.4. Final Verification
   3.5. Report Generation
4. Common Test Scenarios
5. Supporting Files
6. Expected Outcomes
7. Requirements
8. Red Flags to Avoid

## When to Use This Skill

### Explicit Triggers
- "Test the user flow for [feature]"
- "Run E2E test on [URL]"
- "Validate the [workflow/form/checkout] process"
- "Check if [feature] works end-to-end"
- "Automated testing for [scenario]"
- "Verify [user journey]"

### Implicit Triggers
- Need to validate multi-step workflows (login, checkout, signup)
- Regression testing after changes
- Collecting evidence for bug reports
- Verifying form submissions work correctly
- Testing SPA navigation and state changes
- Validating API interactions from browser

### Debugging Triggers
- "Why is [feature] not working?"
- "Check console for errors during [action]"
- "Monitor network requests during [workflow]"
- "Capture evidence of [bug]"

## What This Skill Does

This skill standardizes end-to-end testing with comprehensive evidence collection:

1. **State Capture** - Takes snapshots and screenshots before and after tests
2. **Interaction Execution** - Fills forms, clicks buttons, navigates pages
3. **Error Monitoring** - Watches console for errors and warnings
4. **Network Verification** - Tracks API calls and responses
5. **Evidence Collection** - Generates reports with all artifacts
6. **Pass/Fail Determination** - Validates expected outcomes

## E2E Testing Workflow

### 3.1. Initial State Capture

**Purpose:** Establish baseline before test execution

```
Step 1: Navigate to application
  browser_navigate(url="http://localhost:3000")

Step 2: Wait for page load
  browser_wait_for(time=2)

Step 3: Capture accessibility snapshot
  browser_snapshot()
  → Save as "initial-state.md"

Step 4: Take screenshot
  browser_take_screenshot(filename="initial-state.png")
```

**Why this matters:** Initial state provides context for test failures and debugging.

### 3.2. Test Execution

**Purpose:** Execute user interactions systematically

```
Step 1: Identify form elements
  browser_snapshot()
  → Find refs for input fields

Step 2: Fill form fields
  browser_fill_form(fields=[
    {name: "Email", ref: "ref_5", type: "textbox", value: "user@test.com"},
    {name: "Password", ref: "ref_6", type: "textbox", value: "password123"}
  ])

Step 3: Submit form
  browser_click(element="Login button", ref="ref_7")

Step 4: Wait for response
  browser_wait_for(text="Welcome")
```

**Pattern:** Snapshot → Identify refs → Interact → Verify

### 3.3. Evidence Collection

**Purpose:** Gather diagnostic information during test

```
Step 1: Check console messages
  browser_console_messages(level="error")
  → Capture any errors/warnings

Step 2: Monitor network requests
  browser_network_requests()
  → Verify API calls succeeded

Step 3: Capture intermediate states
  browser_take_screenshot(filename="step-2-after-login.png")
```

**Evidence types:**
- Console logs (errors, warnings, info)
- Network requests (status codes, URLs, timing)
- Screenshots (visual confirmation)
- Accessibility snapshots (DOM state)

### 3.4. Final Verification

**Purpose:** Validate test success criteria

```
Step 1: Verify expected elements
  browser_snapshot()
  → Check for success indicators

Step 2: Capture final state
  browser_take_screenshot(filename="final-state.png")

Step 3: Check for errors
  browser_console_messages(level="error")
  → Ensure no errors during workflow
```

**Success criteria:**
- Expected text/elements present
- No console errors
- Network requests succeeded (2xx status codes)
- Final state matches expectations

### 3.5. Report Generation

**Purpose:** Create comprehensive test documentation

```
Use scripts/generate_test_report.py:

python scripts/generate_test_report.py \
  --test-name "Login Flow" \
  --initial-snapshot initial-state.md \
  --final-snapshot final-state.md \
  --screenshots initial-state.png,final-state.png \
  --console-logs console.json \
  --network-requests network.json \
  --output test-report.md
```

**Report includes:**
- Test metadata (name, URL, timestamp)
- Pass/fail status with reasoning
- Console error summary
- Network request summary
- Screenshot gallery
- Accessibility snapshots
- Recommendations for failures

See `references/report-template.md` for structure.

## Common Test Scenarios

**Login Flow:** Navigate → Capture state → Fill credentials → Submit → Wait for success → Verify console/network → Capture final state → Report

**Form Submission:** Navigate → Capture state → Fill fields → Submit → Wait for confirmation → Verify POST request → Check validation → Capture state → Report

**Multi-Step Checkout:** Add to cart → Checkout → Fill shipping/payment (capture each) → Submit order → Verify confirmation → Check all APIs → Report

**SPA Navigation:** Navigate → Click nav links → Verify URL changes → Check content updates → Monitor console/network → Capture states → Report

See `examples/examples.md` for 10+ detailed scenarios with complete code.

## Supporting Files

**scripts/** - `generate_test_report.py` (creates markdown reports), `setup_test_env.py` (initializes directories)

**references/** - `report-template.md` (report structure), `troubleshooting.md` (common issues/solutions)

**examples/** - `examples.md` (10+ complete test scenarios with code)

## Expected Outcomes

### Successful Test

```
✅ Test Passed: Login Flow

Test Summary:
- URL: http://localhost:3000/login
- Duration: 5.2 seconds
- Steps: 4
- Console Errors: 0
- Network Failures: 0

Evidence:
- Initial state: initial-state.png
- Final state: final-state.png
- Accessibility snapshots: 2
- Network requests: 3 (all 200 OK)

Verification:
✅ "Welcome, User" text found
✅ No console errors
✅ POST /api/login returned 200
✅ Dashboard loaded successfully

Full report: test-reports/login-flow-2025-12-20.md
```

### Failed Test

```
❌ Test Failed: Login Flow

Test Summary:
- URL: http://localhost:3000/login
- Duration: 3.1 seconds (stopped early)
- Steps: 2 of 4 completed
- Console Errors: 2
- Network Failures: 1

Failure Reason:
Network request POST /api/login returned 401 Unauthorized

Console Errors:
1. [Error] Authentication failed: Invalid credentials
2. [Error] Uncaught TypeError: Cannot read property 'token' of undefined

Evidence:
- Initial state: initial-state.png
- Error state: error-state.png
- Network log: network.json

Recommendations:
1. Check API endpoint credentials
2. Verify authentication token handling
3. Add error handling for failed login attempts

Full report: test-reports/login-flow-failed-2025-12-20.md
```

## Requirements

**Tools:**
- Playwright MCP tools (browser_navigate, browser_snapshot, etc.)
- Python 3.8+ (for report generation scripts)
- Write access to test output directory

**Environment:**
- Application running and accessible (local or remote)
- Network connectivity for API calls
- Sufficient disk space for screenshots

**Knowledge:**
- Basic understanding of web application flows
- Familiarity with CSS selectors or accessibility roles
- Understanding of HTTP status codes

## Red Flags to Avoid

**Testing Anti-Patterns:**
- [ ] Starting test without capturing initial state
- [ ] Ignoring console errors during test execution
- [ ] Not verifying network requests succeeded
- [ ] Skipping final state capture
- [ ] Proceeding with test after clear failure
- [ ] Not waiting for async operations to complete
- [ ] Using hardcoded waits instead of `wait_for` text/elements
- [ ] Generating report without all evidence files

**Evidence Collection:**
- [ ] Missing screenshots for critical steps
- [ ] Not checking console messages after interactions
- [ ] Ignoring network request failures
- [ ] Not capturing intermediate states for multi-step flows

**Report Quality:**
- [ ] Vague test names ("Test 1", "Flow 2")
- [ ] Missing pass/fail criteria
- [ ] No recommendations for failures
- [ ] Incomplete evidence references

**Security:**
- [ ] Including credentials in screenshots
- [ ] Committing sensitive test data to git
- [ ] Exposing API keys in network logs
- [ ] Sharing test reports with PII

## Notes

**Best Practices:**
1. Always capture initial and final state (snapshot + screenshot)
2. Check console after every significant interaction
3. Verify network requests for expected status codes
4. Use descriptive test names and step descriptions
5. Generate reports immediately after test completion
6. Store test artifacts in organized directory structure

**Performance Tips:**
- Use `browser_wait_for(text="...")` instead of fixed time waits
- Take screenshots only at key steps (not every interaction)
- Filter console messages by level to reduce noise
- Clear network requests between test runs

**Integration:**
- Combine with CI/CD for automated regression testing
- Use with bug tracking to attach evidence to issues
- Share reports with team for test documentation
- Archive test artifacts for historical analysis
