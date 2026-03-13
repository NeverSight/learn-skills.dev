---
name: incident-hotfix
description: Use this skill for incident response and hotfix deployment. Invoke when production issues occur requiring immediate attention.
---

# Incident Hotfix

Structured incident response, hotfix, and postmortem process.

## Severity Levels

| Level | Impact | Response Time | Examples |
|-------|--------|---------------|----------|
| P0 | System down | Immediate | Complete outage, data loss |
| P1 | Major feature broken | < 1 hour | Auth broken, payments failing |
| P2 | Feature degraded | < 4 hours | Slow performance, partial outage |
| P3 | Minor issue | < 24 hours | UI bug, non-critical error |

## Incident Response

### 1. Assess

- [ ] Identify the symptom
- [ ] Determine severity level
- [ ] Check monitoring dashboards
- [ ] Review recent deployments
- [ ] Communicate status

### 2. Isolate

- [ ] Identify affected components
- [ ] Check error logs
- [ ] Review recent changes
- [ ] Determine blast radius

### 3. Mitigate

Choose one:

**Rollback** (safest)
- Revert to last known good state
- Apply when cause is unclear

**Hotfix** (targeted)
- Minimal change to fix issue
- Apply when cause is clear and fix is simple

**Feature Flag** (quick)
- Disable problematic feature
- Apply when feature is isolatable

### 4. Verify

- [ ] Issue resolved
- [ ] Error rates normalized
- [ ] Performance restored
- [ ] No side effects

### 5. Communicate

- [ ] Update status page
- [ ] Notify stakeholders
- [ ] Document timeline

## Hotfix Process

### 1. Create Hotfix Branch

```bash
# From production/main branch
git checkout main
git pull origin main
git checkout -b hotfix/issue-description
```

### 2. Minimal Fix

Rules for hotfix code:
- **Smallest possible change**
- **No refactoring**
- **No unrelated changes**
- **Must pass tests**

### 3. Verify

```bash
bun run lint:fix
bun run build
bun run test

# Test the specific fix
# Verify in staging if time permits
```

### 4. Deploy

```bash
# Merge to main
git checkout main
git merge hotfix/issue-description

# Tag and deploy
git tag -a v1.2.4 -m "Hotfix: issue description"
git push origin main --tags
```

### 5. Backport

```bash
# Merge hotfix to develop branch
git checkout develop
git merge hotfix/issue-description
git push origin develop
```

## Postmortem Template

Write a postmortem within 48 hours of resolution.

```markdown
# Incident Postmortem: [Title]

## Summary

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Duration | X hours Y minutes |
| Severity | P0/P1/P2/P3 |
| Author | [Name] |

## Impact

- [Number of users affected]
- [Revenue impact if applicable]
- [Other business impact]

## Timeline (UTC)

| Time | Event |
|------|-------|
| HH:MM | Issue first detected |
| HH:MM | Team alerted |
| HH:MM | Root cause identified |
| HH:MM | Fix deployed |
| HH:MM | Issue resolved |

## Root Cause

[Clear, technical explanation of what caused the incident]

## Detection

How was the incident detected?
- [ ] Monitoring alert
- [ ] Customer report
- [ ] Internal discovery

Could we have detected it earlier?
- [Analysis]

## Resolution

What fixed the issue?
- [Description of fix]

Was it a rollback or hotfix?
- [Details]

## Lessons Learned

### What Went Well
- [Point 1]
- [Point 2]

### What Went Wrong
- [Point 1]
- [Point 2]

### Where We Got Lucky
- [Point 1]

## Action Items

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Action 1] | [Name] | YYYY-MM-DD | [ ] |
| [Action 2] | [Name] | YYYY-MM-DD | [ ] |

## Prevention

How do we prevent this class of issue?

- [ ] Add monitoring for [X]
- [ ] Add test for [Y]
- [ ] Improve process for [Z]
```

## Communication Templates

### Initial Alert

```text
🚨 [P1] Investigating issues with [service]

Impact: [Brief description]
Status: Investigating
ETA: Unknown

Updates to follow.
```

### Update

```text
🔄 [P1] Update on [service] issue

Status: Root cause identified, fix in progress
Impact: [Updated impact]
ETA: [Time estimate]

Next update in [X] minutes.
```

### Resolution

```text
✅ [P1] Resolved: [service] issue

Duration: [X hours Y minutes]
Resolution: [Brief description]

Postmortem to follow within 48 hours.
```
