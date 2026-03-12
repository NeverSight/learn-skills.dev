---
name: conduct-post-mortem
description: >
  Conduct a blameless post-mortem analysis after an incident. Build timeline
  reconstruction, identify contributing factors, and generate actionable
  improvements. Focus on systemic issues rather than individual blame. Use
  after any production incident or service degradation, following a near-miss,
  when investigating recurring issues, or to share systemic learnings across
  teams.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: observability
  complexity: basic
  language: multi
  tags: post-mortem, incident-review, blameless, timeline, action-items
---

# Conduct Post-Mortem

Lead a blameless post-mortem to learn from incidents and improve system resilience.

## When to Use

- After any production incident or service degradation
- Following a near-miss or close call
- When investigating recurring issues
- To share learnings across teams

## Inputs

- **Required**: Incident details (start/end time, services affected, severity)
- **Required**: Access to logs, metrics, and alerts during the incident window
- **Optional**: Runbook used during incident response
- **Optional**: Communication logs (Slack, PagerDuty)

## Procedure

### Step 1: Collect Raw Data

Gather all artifacts from the incident:

```bash
# Export relevant logs (adjust timerange)
kubectl logs deployment/api-service \
  --since-time="2025-02-09T10:00:00Z" \
  --until-time="2025-02-09T11:30:00Z" > incident-logs.txt

# Export Prometheus metrics snapshot
curl -G 'http://prometheus:9090/api/v1/query_range' \
  --data-urlencode 'query=rate(http_requests_total{job="api"}[5m])' \
  --data-urlencode 'start=2025-02-09T10:00:00Z' \
  --data-urlencode 'end=2025-02-09T11:30:00Z' \
  --data-urlencode 'step=15s' > metrics.json

# Export alert history
amtool alert query --within=2h alertname="HighErrorRate" --output json > alerts.json
```

**Expected:** Logs, metrics, and alerts covering the full incident timeline.

**On failure:** If data is incomplete, note gaps in the report. Set up longer retention for next time.

### Step 2: Build the Timeline

Create a chronological reconstruction:

```markdown
## Timeline (all times UTC)

| Time     | Event | Source | Actor |
|----------|-------|--------|-------|
| 10:05:23 | First 5xx errors appear | nginx access logs | - |
| 10:06:45 | High error rate alert fires | Prometheus | - |
| 10:08:12 | On-call engineer paged | PagerDuty | System |
| 10:12:00 | Engineer acknowledges alert | PagerDuty | @alice |
| 10:15:30 | Database connection pool exhausted | app logs | - |
| 10:18:45 | Database queries identified as slow | pganalyze | @alice |
| 10:22:10 | Cache layer deployed as mitigation | kubectl | @alice |
| 10:35:00 | Error rate returns to normal | Prometheus | - |
| 10:40:00 | Incident marked resolved | PagerDuty | @alice |
```

**Expected:** A clear, minute-by-minute sequence showing what happened and when.

**On failure:** Timestamp mismatches. Ensure all systems use NTP and log in UTC.

### Step 3: Identify Contributing Factors

Use the Five Whys or fishbone analysis:

```markdown
## Contributing Factors

### Immediate Cause
- Database connection pool exhausted (max 20 connections)
- Query introduced in v2.3.0 deployment lacked index

### Contributing Factors
1. **Monitoring Gap**: Connection pool utilization not monitored
2. **Testing Gap**: Load testing didn't include new query pattern
3. **Runbook Gap**: No documented procedure for DB connection issues
4. **Capacity Planning**: Pool size unchanged despite 3x traffic growth

### Systemic Issues
- No pre-deployment query plan review
- Database alerts only fire on total failure, not degradation
```

**Expected:** Multiple layers of causation identified, avoiding blame.

**On failure:** If analysis stops at "engineer made a mistake", dig deeper. What allowed that mistake?

### Step 4: Generate Action Items

Create concrete, trackable improvements:

```markdown
## Action Items

| ID | Action | Owner | Deadline | Priority |
|----|--------|-------|----------|----------|
| AI-001 | Add connection pool metrics to Grafana | @bob | 2025-02-16 | High |
| AI-002 | Create runbook: DB connection saturation | @alice | 2025-02-20 | High |
| AI-003 | Add DB query plan check to CI/CD | @charlie | 2025-03-01 | Medium |
| AI-004 | Review and adjust connection pool size | @dan | 2025-02-14 | High |
| AI-005 | Implement DB slow query alerts (<100ms) | @bob | 2025-02-23 | Medium |
| AI-006 | Add load testing for new query patterns | @charlie | 2025-03-15 | Low |
```

**Expected:** Each action has an owner, deadline, and clear deliverable.

**On failure:** Vague actions like "improve testing" won't get done. Make specific.

### Step 5: Write and Distribute Report

Use this template structure:

```markdown
# Post-Mortem: API Service Degradation (2025-02-09)

**Date**: 2025-02-09
**Duration**: 1h 35min (10:05 - 11:40 UTC)
**Severity**: P1 (Critical service degraded)
**Authors**: @alice, @bob
**Reviewed**: 2025-02-10

## Summary
The API service experienced elevated error rates (40% of requests) due to
database connection pool exhaustion. Service was restored by deploying a
cache layer. No data loss occurred.

## Impact
- 40,000 failed requests over 1.5 hours
- 2,000 customers affected
- Revenue impact: ~$5,000 (estimated)

## Root Cause
Query introduced in v2.3.0 deployment performed a full table scan due to
missing index. Under increased load, this saturated the connection pool.

[... timeline, contributing factors, action items as above ...]

## What Went Well
- Alert fired within 90 seconds of first errors
- Mitigation deployed quickly (10 minutes from page to fix)
- Communication to customers was clear and timely

## Lessons Learned
- Database monitoring is insufficient; need connection-level metrics
- Load testing must cover new query patterns, not just volume
- Connection pool sizing hasn't kept pace with traffic growth

## Prevention
See Action Items above.
```

**Expected:** Report shared with team and stakeholders within 48 hours of incident.

**On failure:** If report delays exceed 1 week, insights grow stale. Prioritize post-mortems.

### Step 6: Review Action Items in Standup/Retros

Track action item progress:

```bash
# Create GitHub issues from action items
gh issue create --title "AI-001: Add connection pool metrics" \
  --body "From post-mortem PM-2025-02-09. Owner: @bob. Deadline: 2025-02-16" \
  --label "post-mortem,observability" \
  --assignee bob

# Set up recurring reminder
# Add to team calendar: Weekly review of open post-mortem items
```

**Expected:** Action items tracked in project management tool, reviewed weekly.

**On failure:** If action items languish, incidents will recur. Assign executive sponsor for high-priority items.

## Validation

- [ ] Timeline is complete and chronologically accurate
- [ ] Multiple contributing factors identified (not just one)
- [ ] Action items have owners, deadlines, and priorities
- [ ] Report uses blameless language (no "X caused the issue")
- [ ] Report distributed to all stakeholders within 48 hours
- [ ] Action items tracked in ticketing system
- [ ] Follow-up review scheduled for 4 weeks out

## Common Pitfalls

- **Blame culture**: Using "who" language instead of "what/why". Focus on systems, not people.
- **Shallow analysis**: Stopping at the first cause. Always ask "why" at least 5 times.
- **Vague action items**: "Improve monitoring" is not actionable. "Add metric X to dashboard Y by date Z" is.
- **No follow-through**: Action items created but never reviewed. Set calendar reminders.
- **Fear of transparency**: Hiding incidents reduces learning. Share widely (within appropriate security boundaries).

## Related Skills

- `write-incident-runbook` - create runbooks referenced during incidents
- `configure-alerting-rules` - improve alerts based on post-mortem findings
