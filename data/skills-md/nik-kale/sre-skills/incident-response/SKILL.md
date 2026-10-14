---
name: incident-response
description: Guide systematic investigation of production incidents including triage, data gathering, impact assessment, and root cause analysis. Use when investigating outages, service degradation, production errors, alerts firing, or when the user mentions incident, outage, downtime, or production issues.
---

# Incident Response

Systematic framework for investigating and resolving production incidents.

## When to Use This Skill

- Production alert firing
- Service outage or degradation reported
- Error rates spiking
- User-reported issues affecting production
- On-call escalation received

## Initial Triage (First 5 Minutes)

Copy and track progress:

```
Incident Triage:
- [ ] Confirm the incident is real (not false positive)
- [ ] Identify affected service(s)
- [ ] Assess severity level
- [ ] Start incident channel/thread
- [ ] Page additional responders if needed
```

### Severity Assessment

Quickly determine severity to guide response urgency:

| Severity | Criteria                                         | Response Time             |
| -------- | ------------------------------------------------ | ------------------------- |
| **SEV1** | Complete outage, data loss risk, security breach | Immediate, all hands      |
| **SEV2** | Major degradation, significant user impact       | < 15 min, primary on-call |
| **SEV3** | Partial degradation, limited user impact         | < 1 hour                  |
| **SEV4** | Minor issue, workaround available                | Next business day         |

For detailed severity definitions, see [references/severity-levels.md](references/severity-levels.md).

## Data Gathering

Collect evidence systematically. Don't jump to conclusions.

### 1. Timeline Construction

```
Timeline:
- [TIME] First alert/report
- [TIME] ...
- [TIME] Current status
```

### 2. Key Data Sources

**Metrics** - Check in this order:

1. Error rates (5xx, exceptions)
2. Latency (p50, p95, p99)
3. Traffic volume (requests/sec)
4. Resource utilization (CPU, memory, disk, connections)
5. Dependency health

**Logs** - Search for:

```
# Error patterns
level:error OR level:fatal
exception OR panic OR crash

# Correlation
trace_id:<id> OR request_id:<id>
```

**Traces** - Find:

- Slowest traces in affected timeframe
- Error traces
- Traces crossing service boundaries

### 3. Change Correlation

Recent changes are the most common incident cause. Check:

```
Change Audit:
- [ ] Recent deployments (last 24h)
- [ ] Config changes
- [ ] Feature flag changes
- [ ] Infrastructure changes
- [ ] Database migrations
- [ ] Dependency updates
```

## Impact Assessment

Quantify the blast radius:

```
Impact Assessment:
- Affected users: [count or percentage]
- Affected regions: [list]
- Revenue impact: [if calculable]
- Data integrity: [confirmed OK / under investigation]
- Duration so far: [time]
```

## Mitigation Actions

Prioritize stopping the bleeding over finding root cause.

### Quick Mitigation Options

| Action               | When to Use                | Risk   |
| -------------------- | -------------------------- | ------ |
| Rollback             | Bad deployment identified  | Low    |
| Feature flag disable | New feature causing issues | Low    |
| Scale up             | Capacity exhaustion        | Low    |
| Restart              | Memory leak, stuck process | Medium |
| Failover             | Regional/AZ issue          | Medium |
| Circuit breaker      | Dependency failure         | Low    |

### Mitigation Checklist

```
Mitigation:
- [ ] Identify mitigation action
- [ ] Assess rollback risk
- [ ] Execute mitigation
- [ ] Verify improvement
- [ ] Monitor for recurrence
```

## Communication

### Status Update Template

```markdown
**Incident Update - [SERVICE] - [SEV LEVEL]**

**Status**: Investigating / Identified / Mitigating / Resolved
**Impact**: [Brief description of user impact]
**Current Actions**: [What's being done now]
**Next Update**: [Time or "when we have new information"]
```

### Stakeholder Communication

- **SEV1/SEV2**: Proactive updates every 15-30 minutes
- **SEV3**: Update when status changes
- **SEV4**: Update in ticket

## Root Cause Analysis

Only after mitigation. Don't debug while the site is down.

### The 5 Whys

```
Why 1: [Immediate cause]
  ↓
Why 2: [Underlying cause]
  ↓
Why 3: [Contributing factor]
  ↓
Why 4: [Process/system gap]
  ↓
Why 5: [Root cause]
```

### Common Failure Modes

Before deep investigation, check common patterns in [references/common-failure-modes.md](references/common-failure-modes.md).

### Evidence Collection

Preserve for post-incident:

- Screenshots of dashboards
- Relevant log snippets
- Timeline of events
- Commands executed
- Configuration at time of incident

## Resolution & Handoff

```
Resolution Checklist:
- [ ] Service restored to normal
- [ ] Monitoring confirms stability (15+ min)
- [ ] Incident channel updated with resolution
- [ ] Follow-up items captured
- [ ] Post-incident review scheduled (SEV1/SEV2)
```

### Handoff Template

If handing off to another responder:

```
Incident Handoff:
- Summary: [1-2 sentences]
- Current status: [state]
- What's been tried: [list]
- Working theory: [hypothesis]
- Next steps: [recommended actions]
- Key links: [dashboards, logs, docs]
```

## Post-Incident Review

For SEV1/SEV2 incidents, schedule within 48-72 hours.

### Blameless Review Questions

1. What happened? (Timeline)
2. What was the impact?
3. How was it detected?
4. How was it mitigated?
5. What was the root cause?
6. What could we do differently?
7. What action items will prevent recurrence?

### Action Item Template

```
Action Item:
- Title: [Brief description]
- Owner: [Person/team]
- Priority: [P0/P1/P2]
- Due: [Date]
- Type: [Prevention / Detection / Response]
```

## Quick Reference Commands

### Kubernetes

```bash
# Pod status
kubectl get pods -n <namespace> | grep -v Running

# Recent events
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | tail -20

# Pod logs
kubectl logs <pod> -n <namespace> --tail=100
```

### Docker

```bash
# Container status
docker ps -a | head -20

# Container logs
docker logs --tail 100 <container>

# Resource usage
docker stats --no-stream
```

### System

```bash
# Resource pressure
top -bn1 | head -20
df -h
free -m

# Network connections
netstat -tuln | grep LISTEN
ss -tuln
```

## Additional Resources

- [Severity Level Definitions](references/severity-levels.md)
- [Common Failure Modes](references/common-failure-modes.md)
