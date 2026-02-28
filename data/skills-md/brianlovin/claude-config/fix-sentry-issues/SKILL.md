---
name: fix-sentry-issues
description: Use Sentry MCP to discover, triage, and fix production issues with root-cause analysis. Use when asked to fix Sentry issues, triage production errors, investigate error spikes, or clean up Sentry noise. Requires Sentry MCP server. Triggers on "fix sentry", "triage errors", "production bugs", "sentry issues".
---

# Fix Sentry Issues

Systematically discover, triage, investigate, and fix production issues using Sentry MCP. One PR per issue, root-cause analysis required.

## Critical Rule: Truth-Seek, Don't Suppress

**NEVER** treat log level changes as fixes. Changing `logger.error` to `logger.warn` or `logger.info` silences Sentry but doesn't fix the user's experience.

For every failing code path, ask **"Why does this fail?"** — not **"How do I make Sentry quiet?"**

### Anti-patterns to avoid

These are specific failure modes from real experience. Do NOT do these:

1. **Batch-classifying issues as "expected" without investigating each one.** Reading an error message and seeing a fallback path does NOT mean you understand the failure. You must trace the full input path to understand what's being sent and why it fails.

2. **Treating "has a fallback" as "not a problem."** A fallback means the user gets degraded results. Ask: why does the primary path fail? Can we prevent the failure upstream? Is the input wrong? Is the timeout too tight? Is there a missing filter?

3. **Combining multiple issues into one "noise reduction" PR.** Each issue has its own root cause. Investigate and fix them individually. The only exception is issues that share an identical root cause discovered through investigation.

4. **Throwing away error details.** Never change `catch (error) { logger.error(..., error) }` to `catch { logger.info(...) }`. The structured error data (status codes, messages, stack traces) is exactly what you need to understand the failure.

5. **Deciding the fix during triage.** The triage table should classify issues as "Investigate" or "Ignore" — never pre-decide that the fix is a log level change. You don't know the fix until you've completed investigation.

### When a log level change IS valid

A downgrade to `logger.info` is valid ONLY for genuinely expected operational states — NOT for failures with fallbacks. Examples:

- **Valid:** User's Notion database doesn't have an optional "Author" column → property skipped. This is user configuration, not a failure.
- **Valid:** Supabase returns 404 for a link the user deleted. The resource genuinely doesn't exist.
- **Invalid:** Firecrawl scrape fails 300 times/day → downgrade to info. WHY is it failing? Are we sending URLs it can't handle? Are we hitting rate limits?
- **Invalid:** Summary generation times out → downgrade to info. WHY is the API slow? Is the content too large? Is there a network issue?

## Phase 1: Discover

Use Sentry MCP to find the org, project, and all unresolved issues. Use `ToolSearch` first to load the Sentry MCP tools.

```
mcp__sentry__find_organizations()
mcp__sentry__find_projects(organizationSlug, regionUrl)
mcp__sentry__search_issues(
  organizationSlug, projectSlugOrId, regionUrl,
  naturalLanguageQuery: "all unresolved issues sorted by events",
  limit: 25
)
```

Build a triage table. The Action column should be **Investigate** or **Ignore** — never a pre-decided fix:

```markdown
| ID | Title | Events | Action | Reason |
|----|-------|--------|--------|--------|
| PROJ-A | Error in save | 14 | Investigate | User-facing save failure |
| PROJ-B | GM_register... | 3 | Ignore | Greasemonkey extension |
```

## Phase 2: Triage

Classify every issue before writing any code. Only two categories at this stage:

### Investigate (our code, worth understanding)
- Multiple events establishing a pattern
- User sees degraded experience (error status, missing data, broken UI)
- High-volume warnings that might indicate an upstream problem
- Recurring on every run/sync (stale references, cron-triggered)

### Ignore (third-party noise)
- Browser extension code (`GM_registerMenuCommand`, `CONFIG`, `currentInset`, MetaMask JSON-RPC)
- Stale module imports after deploy (`ChunkLoadError` — self-resolving)
- Single-event transients with no reproduction path
- Issues already fixed by a recent commit

Apply triage decisions:
```
mcp__sentry__update_issue(issueId, organizationSlug, regionUrl, status: "ignored")  // noise
mcp__sentry__update_issue(issueId, organizationSlug, regionUrl, status: "resolved") // already fixed
```

## Phase 3: Investigate (one issue at a time)

For each "Investigate" issue, work through these steps **in order**. Do NOT skip steps or batch multiple issues together.

### 3a. Pull event-level data

Issue summaries hide the details you need. Always pull actual events AND the full issue details:

```
mcp__sentry__get_issue_details(issueId, organizationSlug, regionUrl)
mcp__sentry__search_issue_events(
  issueId, organizationSlug, regionUrl,
  naturalLanguageQuery: "all events with extra data",
  limit: 15
)
```

Extract from the events: actual URLs, request parameters, stack traces, timestamps, user context, extra data fields (status codes, content lengths, etc.). These are the real inputs that triggered the failure.

### 3b. Cross-reference with Axiom logs

Axiom events include `traceId` fields that correlate with Sentry errors. Use the Axiom CLI to pull surrounding logs for richer context:

```bash
# Get the traceId from the Sentry event's trace context
# Then query Axiom for all events with that traceId
axiom query "['shiori-events'] | where traceId == '<traceId>'" -f json

# Or search by userId around the error timestamp for broader context
axiom query "['shiori-events'] | where userId == '<userId>' | where _time > datetime('2025-01-01T00:00:00Z') and _time < datetime('2025-01-01T01:00:00Z')" -f json
```

Axiom logs include fields like `authMethod`, `client_version`, `event` type, and request metadata that Sentry often lacks. This helps you understand what the user was doing before and after the error.

### 3c. Read the failing code path

Follow the stack trace. Read every file in the chain. Understand what the code does before proposing changes. Use subagents for parallel file exploration if the stack is deep.

### 3d. Trace the input path upstream

This is the step most often skipped, and the most important:

- **What data reaches the failing function?** Trace backwards from the error to the original input. What URL/payload/parameters were passed?
- **Should this input have reached this code path at all?** Is there a missing filter, validation, or early return upstream?
- **What does the input look like?** For URL-based failures: is it a binary file? A redirect? A localhost URL? Something the API can't handle?
- **Is the failure in our code or an external service?** If external: can we prevent sending bad inputs? Can we add better pre-filtering?

### 3e. Reproduce and verify

Use the actual failing inputs from Sentry events:
- Call the function with the exact data that failed
- `fetch()` the actual URLs that timed out — are they reachable?
- Add temporary `console.log` statements to verify your understanding of the code flow
- Check if the failure is in our code or an external service

### 3f. Identify root cause

Ask these questions in order:

1. **Why does this specific input fail?** (e.g., "Firecrawl can't scrape a .png URL")
2. **Why does this input reach this code path?** (e.g., "No extension check before calling Firecrawl")
3. **What's the right fix?** (e.g., "Filter binary URLs before calling Firecrawl" — not "suppress the log")
4. **Should we also improve observability?** (e.g., "Add status code to the log so we can see the failure distribution")

Common root causes:

| Pattern | Root Cause | Real Fix |
|---------|-----------|----------|
| External API fails on certain URLs | Wrong inputs being sent (binary files, bad formats) | Filter/validate inputs before sending |
| External API timeout | Timeout too tight, or input too large, or missing retry | Investigate what's slow, adjust timeout or input size |
| DB rejects "invalid json" | Unsanitized input (null bytes, control chars) | Sanitize before insert |
| Processing stuck in "error" | Timeout budget doesn't account for full pipeline | Adjust timeouts, save partial results on timeout |
| Same error on every cron run | Stale reference to deleted external resource | Detect staleness, auto-clean |
| Error logged but details not useful | Error object not included, or status code missing | Improve the log to include actionable details |

### 3g. Know your log levels

Log levels control what reaches Sentry:

| Level | Sends to Sentry? | Use for |
|-------|-------------------|---------|
| `logger.error` | Yes (error) | Unexpected bugs, states that should never occur |
| `logger.warn` | Yes (warning) | Handled failures worth monitoring — keep until you understand the pattern |
| `logger.info` | No | Genuinely expected operational states (not "failures with fallbacks") |

## Phase 4: Fix

### 4a. Branch from main
```bash
git checkout main && git pull
git checkout -b fix/<descriptive-name>
```

One branch per issue. Keep fixes focused.

### 4b. Write tests first

Tests must use data derived from actual Sentry events, not hypothetical inputs. The test should fail before the fix and pass after.

### 4c. Implement the fix

Fix the root cause, not the symptom.

**Self-check before committing:** If the fix is primarily a log level change, STOP. Ask yourself:
- Did I investigate why this fails, or did I just see a fallback and suppress?
- Can I prevent the failure upstream instead of silencing it?
- Am I throwing away error details that would help debug future occurrences?
- Would a staff engineer look at this PR and say "but why does it fail in the first place?"

### 4d. Verify

- Run tests (e.g., `bun run test`)
- Run lint
- Confirm the fix handles the actual failing inputs from Sentry events
- Remove any temporary `console.log` statements

### 4e. Create PR

```bash
git push -u origin fix/<descriptive-name>
gh pr create --title "<short title>" --body "$(cat <<'EOF'
## Summary
- **Root cause**: [What was actually wrong — the upstream reason, not just "it throws an error"]
- **Fix**: [What changed and why this prevents the failure, not just silences it]

## Test plan
- [x] Tests written using data from Sentry events
- [x] All tests pass
- [x] Lint passes
EOF
)"
```

### 4f. Resolve in Sentry

After PR is merged:
```bash
git checkout main && git pull
```
```
mcp__sentry__update_issue(issueId, organizationSlug, regionUrl, status: "resolved")
```

## Phase 5: Repeat

Work through issues by priority (most events first). After each PR:
1. Return to main, pull latest
2. Pick next issue from the triage table
3. Start Phase 3 again — full investigation for each issue

## Checklist Per Issue

```
[ ] Pulled event-level data (not just issue summary)
[ ] Cross-referenced with Axiom logs using traceId for surrounding context
[ ] Read the failing code path end-to-end
[ ] Traced the input path upstream — understood what data triggers the failure
[ ] Identified root cause (not just "it has a fallback")
[ ] Fix prevents the failure, not just suppresses the log
[ ] Tests use real-world data from Sentry events
[ ] Tests pass, lint passes
[ ] No error details thrown away (catch variables, status codes, etc.)
[ ] PR created with upstream root cause explanation
[ ] Sentry issue resolved after merge
```
