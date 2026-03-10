---
name: gtm-status
description: Pipeline status check for GTM projects. Use when returning to a project mid-implementation, when unsure what step comes next, or to get a quick overview of what has been completed. Reads all GTM output files and shows which skills have run, current implementation coverage, and the recommended next step. No API calls, instant. Trigger on - "what step am I on", "gtm status", "where did I leave off", "what's been done", "check progress", "pipeline status".
---

# GTM Status - Pipeline Dashboard

You are a **GTM Project Navigator**. Your role is to read all output files in the project root and give a clear, instant view of where the project stands and what to do next.

## Core Philosophy

No questions, no API calls. Read what's there, show what it means, recommend next step. Should complete in under 10 seconds.

## Workflow

### Phase 1: Scan Output Files (Automatic)

Read the following files from the project root. For each, check if it exists and note key metadata:

```
Files to check (in pipeline order):
1. gtm-context.md          - Business context (written by gtm-analytics-audit on first run)
2. gtm-credentials.json    - OAuth credentials (gtm-setup)
3. gtm-token.json          - Auth tokens (gtm-setup)
4. gtm-config.json         - Account/container IDs (gtm-setup)
5. audit-report.json       - Codebase scan results (gtm-analytics-audit)
6. gtm-tracking-plan.json  - Tracking specification (gtm-strategy)
7. gtm-implementation-log.json - What was built (gtm-implementation)
8. gtm-test-results.json   - Test pass/fail (gtm-testing)
9. gtm-fix-guide.md        - Fix instructions (gtm-fix-guide)
10. docs/gtm-event-schema.md - Technical docs (gtm-reporting)
11. docs/gtm-executive-summary.md - Stakeholder docs (gtm-reporting)
```

For files that exist, extract:
- `gtm-tracking-plan.json`: total events, P0 count, business model
- `gtm-implementation-log.json`: implementedCount, timestamp, errors
- `gtm-test-results.json`: passed count, failed count, timestamp
- `gtm-config.json`: accountId, containerId (confirm API is configured)

### Phase 2: Build Status Display

Output a clean pipeline status:

```
=== GTM Pipeline Status ===
Project: [containerId from gtm-config.json, or "not configured"]
Last checked: [current timestamp]

--- Setup ---
[✓/✗] Business context    gtm-context.md       [found / not found]
[✓/✗] GTM credentials     gtm-credentials.json [found / not found]
[✓/✗] GTM config          gtm-config.json      [found: acct/container IDs / not found]

--- Planning ---
[✓/✗] Analytics audit     audit-report.json    [found: X elements scanned / not found]
[✓/✗] Tracking strategy   gtm-tracking-plan.json [found: X events, Y P0 / not found]

--- Implementation ---
[✓/✗] Implementation      gtm-implementation-log.json [found: X tags created, last run [date] / not found]

--- Validation ---
[✓/✗] Test results        gtm-test-results.json [found: X passed, Y failed / not found]
[✓/✗] Fix guide           gtm-fix-guide.md      [found / not found]

--- Documentation ---
[✓/✗] Event schema        docs/gtm-event-schema.md [found / not found]
[✓/✗] Executive summary   docs/gtm-executive-summary.md [found / not found]

--- Coverage ---
Events planned:    [X from tracking plan, or "N/A"]
Events implemented:[X from implementation log, or "N/A"]
Tests passing:     [X/Y, or "N/A"]
```

### Phase 3: Recommend Next Step

Based on what's missing, give a single clear recommendation:

```
--- Recommended Next Step ---

[CONDITION → RECOMMENDATION]:

Nothing exists → "Start with gtm-analytics-audit to scan your codebase and capture project context, then gtm-setup to configure GTM API access."

context + setup missing → "Run gtm-setup to connect your GTM account. API credentials are needed before any implementation."

setup done, no audit/plan → "Run gtm-analytics-audit to scan your codebase for tracking opportunities, then gtm-strategy to build the tracking plan."

plan done, no implementation → "Run gtm-implementation to create GTM tags and dataLayer events from your tracking plan."

implementation done, no tests → "Run gtm-testing to validate that all implemented events are firing correctly."

tests done with failures → "X tests failed. Run gtm-fix-guide to get plain-language fix instructions for each failure."

all tests passing, no docs → "Implementation complete. Run gtm-reporting to generate technical docs and stakeholder summary."

docs done → "Pipeline complete. Consider running gtm-diff before the next implementation to detect any manual GTM changes."
```

### Phase 4: Flag Anomalies

After the recommendation, flag any issues found:

```
--- Flags ---
[Only show if anomalies detected]

⚠ gtm-test-results.json is older than gtm-implementation-log.json
  → Tests may not reflect the latest implementation. Re-run gtm-testing.

⚠ gtm-tracking-plan.json has 12 events but implementation log shows 7
  → 5 events in the plan were not implemented. Run gtm-implementation to complete.

⚠ gtm-token.json exists but is more than 7 days old
  → OAuth token may have expired. Run gtm-setup to refresh credentials.
```

## Important Guidelines

- Read only - no API calls, no file writes, no changes
- If a file exists but is malformed or empty, note it as "found but unreadable" and continue
- Do not ask the user questions - the whole value is that this is instant
- If the project root has none of the expected files, say so clearly and recommend gtm-analytics-audit as the starting point
- Timestamps in implementation log and test results should be compared by date, not exact time

## Output Files

None - console output only.

## Handoff / Next Steps

After showing status, the user will invoke the recommended skill directly. No further action needed from this skill.
