---
name: write-incident-runbook
description: >
  Create structured incident runbooks with diagnostic steps, resolution procedures, escalation
  paths, and communication templates for effective incident response. Use when documenting
  response procedures for recurring alerts, standardizing incident response across an on-call
  rotation, reducing MTTR with clear diagnostic steps, creating training materials for new
  team members, or linking alert annotations directly to resolution procedures.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: observability
  complexity: basic
  language: multi
  tags: runbook, incident-response, diagnostics, escalation, documentation
---

# Write Incident Runbook

Create actionable runbooks that guide responders through incident diagnosis and resolution.

## When to Use

- Documenting response procedures for recurring alerts or incidents
- Standardizing incident response across on-call rotation members
- Reducing mean time to resolution (MTTR) with clear diagnostic steps
- Creating training materials for new team members on incident handling
- Establishing escalation paths and communication protocols
- Migrating tribal knowledge to written documentation
- Linking alerts to resolution procedures (alert annotations)

## Inputs

- **Required**: Incident or alert name/description
- **Required**: Historical incident data and resolution patterns
- **Optional**: Diagnostic queries (Prometheus, logs, traces)
- **Optional**: Escalation contacts and communication channels
- **Optional**: Previous incident post-mortems

## Procedure

### Step 1: Choose Runbook Template Structure

> See [Extended Examples](references/EXAMPLES.md#step-1-runbook-template-examples) for complete template files.

Select an appropriate template based on incident type and complexity.

**Basic runbook template structure**:
```markdown
# [Alert/Incident Name] Runbook
## Overview | Severity | Symptoms
## Diagnostic Steps | Resolution Steps
## Escalation | Communication | Prevention | Related
```

**Advanced SRE runbook template** (excerpt):
```markdown
# [Service Name] - [Incident Type] Runbook

## Metadata
- Service, Owner, Severity, On-Call, Last Updated

## Diagnostic Phase
### Quick Health Check (< 5 min): Dashboard, error rate, deployments
### Detailed Investigation (5-20 min): Metrics, logs, traces, failure patterns
# ... (see EXAMPLES.md for complete template)
```

Key template components:
- **Metadata**: Service ownership, severity, on-call rotation
- **Diagnostic Phase**: Quick checks → detailed investigation → failure patterns
- **Resolution Phase**: Immediate mitigation → root cause fix → verification
- **Escalation**: Criteria and contact paths
- **Communication**: Internal/external templates
- **Prevention**: Short/long-term actions

**Expected:** Template selected matches incident complexity, sections appropriate for service type.

**On failure:**
- Start with basic template, iterate based on incident patterns
- Review industry examples (Google SRE books, vendor runbooks)
- Adapt template based on team feedback after first use

### Step 2: Document Diagnostic Procedures

> See [Extended Examples](references/EXAMPLES.md#step-2-complete-diagnostic-procedures) for complete diagnostic queries and decision trees.

Create step-by-step investigation procedures with specific queries.

**Six-step diagnostic checklist**:

1. **Verify Service Health**: Health endpoint checks and uptime metrics
   ```bash
   curl -I https://api.example.com/health  # Expected: HTTP 200 OK
   ```
   ```promql
   up{job="api-service"}  # Expected: 1 for all instances
   ```

2. **Check Error Rate**: Current error percentage and breakdown by endpoint
   ```promql
   sum(rate(http_requests_total{status=~"5.."}[5m]))
   / sum(rate(http_requests_total[5m])) * 100  # Expected: < 1%
   ```

3. **Analyze Logs**: Recent errors and top error messages from Loki
   ```logql
   {job="api-service"} |= "error" | json | level="error"
   ```

4. **Check Resource Utilization**: CPU, memory, and connection pool status
   ```promql
   avg(rate(container_cpu_usage_seconds_total{pod=~"api-service.*"}[5m])) * 100
   # Expected: < 70%
   ```

5. **Review Recent Changes**: Deployments, git commits, infrastructure changes

6. **Examine Dependencies**: Downstream service health, database/API latency

**Failure pattern decision tree** (excerpt):
- Service down? → Check all pods/instances
- Error rate elevated? → Check specific error types (5xx, gateway, database, timeouts)
- When did it start? → After deployment (rollback), gradual (resource leak), sudden (traffic/dependency)

**Expected:** Diagnostic procedures are specific, include expected vs actual values, guide responder through investigation.

**On failure:**
- Test queries in actual monitoring system before documenting
- Include screenshots of dashboards for visual reference
- Add "Common mistakes" section for frequently missed steps
- Iterate based on feedback from incident responders

### Step 3: Define Resolution Procedures

> See [Extended Examples](references/EXAMPLES.md#step-3-complete-resolution-procedures) for all 5 resolution options with full commands and rollback procedures.

Document step-by-step remediation with rollback options.

**Five resolution options** (brief summary):

1. **Rollback Deployment** (fastest): For post-deployment errors
   ```bash
   kubectl rollout undo deployment/api-service
   ```
   Verify → Monitor → Confirm resolution (error rate < 1%, latency normal, no alerts)

2. **Scale Up Resources**: For high CPU/memory, connection pool exhaustion
   ```bash
   kubectl scale deployment/api-service --replicas=$((current * 3/2))
   ```

3. **Restart Service**: For memory leaks, stuck connections, cache corruption
   ```bash
   kubectl rollout restart deployment/api-service
   ```

4. **Feature Flag / Circuit Breaker**: For specific feature errors or external dependency failures
   ```bash
   kubectl set env deployment/api-service FEATURE_NAME=false
   ```

5. **Database Remediation**: For database connections, slow queries, pool exhaustion
   ```sql
   -- Kill long-running queries, restart connection pool, increase pool size
   ```

**Universal verification checklist**:
- [ ] Error rate < 1%
- [ ] Latency P99 < threshold
- [ ] Throughput at baseline
- [ ] Resource usage healthy (CPU < 70%, Memory < 80%)
- [ ] Dependencies healthy
- [ ] User-facing tests pass
- [ ] No active alerts

**Rollback procedure**: If resolution worsens situation → pause/cancel → revert → reassess

**Expected:** Resolution steps are clear, include verification checks, provide rollback options for each action.

**On failure:**
- Add more granular steps for complex procedures
- Include screenshots or diagrams for multi-step processes
- Document command outputs (expected vs actual)
- Create separate runbook for complex resolution procedures

### Step 4: Establish Escalation Paths

> See [Extended Examples](references/EXAMPLES.md#step-4-complete-escalation-guidelines) for full escalation levels and contact directory template.

Define when and how to escalate incidents.

**When to escalate immediately**:
- Customer-facing outage > 15 minutes
- SLO error budget > 10% depleted
- Data loss/corruption or security breach suspected
- Unable to identify root cause within 20 minutes
- Mitigation attempts fail or worsen situation

**Five escalation levels**:
1. **Primary On-Call** (5 min response): Deploy fixes, rollback, scale (up to 30 min solo)
2. **Secondary On-Call** (auto after 15 min): Additional investigation support
3. **Team Lead** (architectural decisions): Database changes, vendor escalation, incidents > 1 hour
4. **Incident Commander** (cross-team coord): Multiple teams, customer comms, incidents > 2 hours
5. **Executive** (C-level): Major impact (>50% users), SLA breach, media/PR, outages > 4 hours

**Escalation process**:
1. Notify target with: current status, impact, actions taken, help needed, dashboard link
2. Handoff if needed: share timeline, actions, access, remain available
3. Don't go silent: update every 15 min, ask questions, provide feedback

**Contact directory**: Maintain table with role, Slack, phone, PagerDuty for:
- Platform/Database/Security/Network teams
- Incident Commander
- External vendors (AWS, database vendor, CDN provider)

**Expected:** Clear criteria for escalation, contact information readily accessible, escalation paths aligned with organizational structure.

**On failure:**
- Validate contact information is current (test quarterly)
- Add decision tree for when to escalate
- Include examples of escalation messages
- Document response time expectations for each level

### Step 5: Create Communication Templates

> See [Extended Examples](references/EXAMPLES.md#step-5-complete-communication-templates) for all internal and external templates with full formatting.

Provide pre-written messages for incident updates.

**Internal templates** (Slack #incident-response):

1. **Initial Declaration**:
   ```
   🚨 INCIDENT: [Title] | Severity: [Critical/High/Medium]
   Impact: [users/services] | Owner: @username | Dashboard: [link]
   Quick Summary: [1-2 sentences] | Next update: 15 min
   ```

2. **Progress Update** (every 15-30 min):
   ```
   📊 UPDATE #N | Status: [Investigating/Mitigating/Monitoring]
   Actions: [what we tried and outcomes]
   Theory: [what we think is happening]
   Next: [planned actions]
   ```

3. **Mitigation Complete**:
   ```
   ✅ MITIGATION | Metrics: Error [before→after], Latency [before→after]
   Root Cause: [brief or "investigating"] | Monitoring 30min before resolved
   ```

4. **Resolution**:
   ```
   🎉 RESOLVED | Duration: [time] | Root Cause + Impact + Follow-up actions
   ```

5. **False Alarm**: No impact, no follow-up needed

**External templates** (status page):
- **Initial**: Investigating, started time, next update in 15 min
- **Progress**: Identified cause (customer-friendly), implementing fix, estimated resolution
- **Resolution**: Resolved time, root cause (simple), duration, prevention measures

**Customer email template**: Timeline, impact description, resolution, prevention, compensation (if applicable)

**Expected:** Templates save time during incidents, ensure consistent communication, reduce cognitive load on responders.

**On failure:**
- Customize templates to match company communication style
- Pre-fill templates with common incident types
- Create Slack workflow/bot to populate templates automatically
- Review templates during incident retrospectives

### Step 6: Link Runbook to Monitoring

> See [Extended Examples](references/EXAMPLES.md#step-6-alert-integration-examples) for complete Prometheus alert configuration and Grafana dashboard JSON.

Integrate runbook with alerts and dashboards.

**Add runbook links to Prometheus alerts**:
```yaml
- alert: HighErrorRate
  annotations:
    runbook_url: "https://wiki.example.com/runbooks/high-error-rate"
    dashboard_url: "https://grafana.example.com/d/service-overview"
    incident_channel: "#incident-platform"
```

**Embed quick diagnostic links in runbook**:
- Service Overview Dashboard
- Error Rate Last 1h (Prometheus direct link)
- Recent Error Logs (Loki/Grafana Explore)
- Recent Deployments (GitHub/CI)
- PagerDuty Incidents

**Create Grafana dashboard panel** with runbook links (markdown panel listing all incident runbooks with on-call and escalation info)

**Expected:** Responders can access runbooks directly from alerts or dashboards, diagnostic queries pre-filled, one-click access to relevant tools.

**On failure:**
- Verify runbook URLs are accessible without VPN/login
- Use URL shorteners for complex Grafana/Prometheus links
- Test links quarterly to ensure they don't break
- Create browser bookmarks for frequently used runbooks

## Validation

- [ ] Runbook follows consistent template structure
- [ ] Diagnostic procedures include specific queries and expected values
- [ ] Resolution steps are actionable with clear commands
- [ ] Escalation criteria and contacts are current
- [ ] Communication templates provided for internal and external audiences
- [ ] Runbook linked from monitoring alerts and dashboards
- [ ] Runbook tested during incident simulation or actual incident
- [ ] Feedback from responders incorporated into runbook
- [ ] Revision history tracked with dates and authors
- [ ] Runbook accessible without authentication (or cached offline)

## Common Pitfalls

- **Too generic**: Runbooks with vague steps like "check the logs" without specific queries are not actionable. Be specific.
- **Outdated information**: Runbooks referencing old systems or commands become useless. Review quarterly.
- **No verification steps**: Resolution without verification leads to false positives. Always include "how to confirm it's fixed."
- **Missing rollback procedures**: Every action should have a rollback plan. Don't trap responders in worse state.
- **Assuming knowledge**: Runbooks for experts only exclude junior engineers. Write for the least experienced person on rotation.
- **No ownership**: Runbooks without owners become stale. Assign team/person responsible for updates.
- **Hidden behind auth**: Runbooks inaccessible during VPN/SSO issues are useless during crisis. Cache copies or use public wiki.

## Related Skills

- `configure-alerting-rules` - Link runbooks to alert annotations for immediate access during incidents
- `build-grafana-dashboards` - Embed runbook links in dashboards and diagnostic panels
- `setup-prometheus-monitoring` - Include diagnostic queries from Prometheus in runbook procedures
- `define-slo-sli-sla` - Reference SLO impact in incident severity classification
