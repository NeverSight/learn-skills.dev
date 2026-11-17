---
name: atlassian-ops
description: Operate Jira, Jira Service Management, and Confluence for network work — changes, incidents, problems, RFC epics, CAB, knowledge. Use when filing or triaging tickets, writing Confluence KB, or mapping ITIL. Notion narrative stays in notion-ops.
origin: snm-pack
---

# Atlassian ops (network)

Jira/JSM is **execution**. Confluence is **KB that the service desk
searches**. Notion may hold the RFC narrative — do not fork the ticket.

## When to use

- Open/triage Change, Incident, Problem, Request
- CAB agenda from Jira
- Confluence runbook the NOC actually uses
- "Put this in Jira" / JSM portal categories for network

## Object model

| Issue type | Use | Required fields |
|------------|-----|-----------------|
| Incident | unplanned impact | sev, service, clinical?, ePHI? (flag only) |
| Problem | recurring / unknown error | linked incidents, RCA due |
| Change (JSM) | production mutation | window, risk, rollback, RFC, verifier |
| Request | access, circuit, port | approver, expiry |
| Epic / Story | project execution | RFC id, site, wave |

Standard: [reference/jsm-schemas.md](reference/jsm-schemas.md).
Confluence tree: [reference/confluence-ia.md](reference/confluence-ia.md).

## Workflows you must follow

**Incident:** detect → triage (clinical safety first) → mitigate →
communicate → problem link → postmortem if Sev1/Sev2 or clinical.

**Change:** RFC in Notion/Confluence → JSM Change → peer review → CAB
(if normal/major) → implement via `netops-mcp` consent gate → verify →
close with evidence. Emergency change: SNM + InfoSec, post-CAB.

**Problem:** do not close the incident by renaming it. Open Problem,
tie incidents, date the RCA.

## Ticket writing bar

- Title: `site · service · symptom` ("MAI · EHR · Interconnect packet loss")
- Description: impact, since-when, what we know, what we tried (read-only)
- No PHI, no passwords, no full captures
- Links: Lucid, RFC, monitoring, related changes in the window
- Assignee is a person; SNM is not the default owner of every port request

## Confluence vs Notion

- Confluence: NOC-facing runbooks, how-to, portal KB
- Notion: RFC narrative, CMDB-lite, board pack
- If the org is Confluence-only, put RFCs there and say so — do not
  invent a Notion migration in the same breath as a Sev1

## Output

```text
ISSUE
- type · key (or "create") · title

FIELDS
- sev/risk · window · rollback · verifier · services

LINKS
- RFC · Lucid · Notion · monitoring

NEXT
- who does what by when
```

## Reference Files
- [reference/jsm-schemas.md](reference/jsm-schemas.md)
- [reference/confluence-ia.md](reference/confluence-ia.md)
