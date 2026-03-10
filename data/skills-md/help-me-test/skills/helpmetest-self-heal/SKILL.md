---
name: helpmetest-self-heal
description: "Autonomous test maintenance agent. Monitors test failures and fixes them automatically. Always use this when tests start failing after a UI or code change — it's far more systematic than trying to fix tests manually one by one. Use when user mentions 'fix failing tests', 'heal tests', 'auto-fix', 'monitor test health', 'tests broke after deploy', or test suite has multiple failures needing systematic repair. Distinguishes fixable test issues (selector changes, timing) from real application bugs."
allowed-tools: mcp__helpmetest-*
---

# Self-Healing Agent

Monitors test failures and fixes them autonomously.

**Mode:** On startup, fix all existing failures. Then monitor for new failures and fix them as they occur.

## Prerequisites

**MANDATORY:** Before healing, call:
```
how_to({ type: "context_discovery" })
how_to({ type: "debugging_self_healing" })
how_to({ type: "interactive_debugging" })
```

Use `context_discovery` to find the existing SelfHealing artifact (if any) and resume from it rather than creating a duplicate. Also identifies which Feature artifacts have known bugs so you don't try to heal tests that are failing due to real application bugs.

## Startup: Fix Existing Failures

On startup, check all tests for failures:

1. Get list of all failing tests using `helpmetest_status`
2. For each failing test:
   - Get recent test history to understand failure pattern
   - Classify failure type (selector change, timing issue, etc.)
   - Determine if fixable or not

3. For fixable failures (test issues):
   - Investigate interactively using `helpmetest_run_interactive_command`
   - Find the fix (new selector, longer timeout, etc.)
   - Apply fix using `helpmetest_upsert_test`
   - Verify fix works using `helpmetest_run_test`
   - Document the fix in SelfHealing artifact

4. For non-fixable failures (likely bugs):
   - Document why not fixable in SelfHealing artifact
   - Include issue type, error message, recommendation

5. After processing all existing failures, enter monitoring mode

## Monitoring: Respond to New Failures

After startup, monitor for test failures using `listen_to_events`:

When a test fails:
1. Get error details
2. Classify failure pattern
3. If fixable: investigate, fix, verify, document
4. If not fixable: document as potential bug
5. Continue monitoring

## Healing Workflow

Use this workflow for both startup failures and new failures during monitoring:

1. **Fetch test history:**
   - Get last 10 runs using `helpmetest_status`
   - Look for patterns (alternating PASS/FAIL? changing error values?)

2. **Classify failure pattern:**
   - Check error type (selector? timeout? assertion?)
   - Determine root cause using `debugging_self_healing.md` categories
   - Decide: test issue (fixable) vs app bug (not fixable)

3. **If fixable (test issue):**
   - Investigate interactively using `helpmetest_run_interactive_command`
   - Find the fix (new selector, longer timeout, etc.)
   - Validate fix works interactively first
   - Apply fix using `helpmetest_upsert_test`
   - Verify fix by running test multiple times (especially for isolation issues)
   - Document in SelfHealing artifact:
     * test_id, pattern_detected, fix_applied, verification_result, timestamp
     * Tags: feature:self-healing, test:, pattern:

4. **If not fixable (app bug):**
   - Document in SelfHealing artifact:
     * issue_type, error_message, why_not_fixable, recommendation

5. **Continue monitoring** for new failures

## Fixable vs Not Fixable

**Fixable (test issues):**
- Selector changed (element still exists, different selector needed)
- Timing issue (element appears later, need longer wait)
- Form field added/removed (form structure changed)
- Button moved (still exists, different location)
- Test isolation (shared state between tests, make idempotent)

**Not fixable (likely bugs):**
- Authentication broken
- Server errors (500, 404)
- Missing pages/features
- Data corruption
- API endpoints removed

## SelfHealing Artifact

Track all healing activity in a SelfHealing artifact. This gives the user a clear record of what was fixed automatically vs what needs human attention.

```json
{
  "type": "SelfHealing",
  "id": "self-healing-log",
  "name": "SelfHealing: Test Maintenance Log",
  "content": {
    "fixed": [
      {
        "test_id": "test-login",
        "pattern_detected": "selector_change",
        "error": "Element not found: button.submit",
        "fix_applied": "Updated selector to [data-testid='submit-btn']",
        "verification_result": "Test passed on re-run",
        "timestamp": "2024-01-15T10:30:00Z",
        "tags": ["feature:authentication", "pattern:selector_change"]
      }
    ],
    "not_fixed": [
      {
        "test_id": "test-checkout",
        "issue_type": "server_error",
        "error_message": "500 Internal Server Error on POST /api/checkout",
        "why_not_fixable": "Backend endpoint returning 500 - application bug, not a test issue",
        "recommendation": "Investigate checkout API endpoint",
        "timestamp": "2024-01-15T10:35:00Z"
      }
    ],
    "summary": {
      "total_processed": 5,
      "fixed": 3,
      "not_fixable": 2,
      "last_run": "2024-01-15T10:35:00Z"
    }
  }
}
```

## Monitoring Loop

The monitor must run in the background — otherwise the agent is blocked while healing a test and can't receive new events at the same time.

**Preferred: use `/loop` if available.** The `/loop` skill provides background execution and will handle the event loop for you. Pass it the monitoring logic below.

**Fallback: spawn as a background Task.** If `/loop` isn't available, spawn a subagent with the Task tool and let it run the loop independently. The foreground conversation stays free while the background agent heals tests.

**Monitoring logic (runs inside the background agent):**

```
listen_to_events({ type: "test_run_completed" })
```

When an event arrives with a failed test:
1. Check `event.test_id` and `event.error`
2. Get test history: `helpmetest_status({ id: event.test_id, testRunLimit: 10 })`
3. Run the healing workflow (classify → investigate → fix or document)
4. Update SelfHealing artifact with result
5. Resume listening

Events that arrive while healing a test are queued — they'll be processed once the current fix completes. Report a summary to the SelfHealing artifact periodically so the user can check in at any time.
