---
name: notion-ops
description: Operate Notion as the network knowledge system — runbooks, RFC narrative, CMDB-lite, CAB packs, ADRs, postmortems. Use when creating or restructuring Notion databases/pages for NetOps, not for Jira tickets (atlassian-ops) or drawings (lucid-diagrams).
origin: snm-pack
---

# Notion ops (network)

Notion is the **narrative source of truth**. Jira is execution. Lucid is
pictures. Do not duplicate all three.

## When to use

- Runbooks, ADRs, RFC write-ups, postmortems, vendor QBRs
- CMDB-lite (sites, circuits, devices-as-pages)
- CAB agenda pack, board narrative
- "Put this in Notion" / restructure a messy wiki

If the user only has Confluence, use `atlassian-ops` instead and say so.

## Information architecture (default)

One parent page **Network** with linked databases (not 40 orphan pages):

| Database | Key properties | Relation |
|----------|----------------|----------|
| Sites | region, type (hospital/clinic/DC), criticality | → Circuits, Devices |
| Circuits | carrier, ID, A/Z, bandwidth, contract end | → Sites |
| Devices / stacks | role, platform, mgmt IP (no secrets), site | → Sites, Services |
| Services | SLO, owner, zone | → Devices |
| RFCs | status, CAB date, risk | → Services, Changes |
| Changes | window, rollback, verifier | → RFC, Jira URL |
| Incidents | sev, ePHI?, clinical impact | → Services, Postmortems |
| Runbooks | service, last-tested | → Services |
| Vendors | BAA?, TAC, QBR | → Circuits, Devices |

Page templates: RFC (from `network-project-analysis`), incident, QBR,
board pack (from `senior-network-manager`).

Details: [reference/schema-templates.md](reference/schema-templates.md).

## Workflow

1. **Find the canonical page** — search, then check parent + database.
   Do not create a parallel "Network v2".
2. **Inspect schema** before editing. Add a property rather than a new
   database when the row type is the same.
3. **Edit surgically.** Headings, callouts for risk, tables for
   inventories. Keep secrets out — link to the vault, do not paste TACACS.
4. **Cross-link** Jira keys and Lucid URLs in properties, not in prose only.
5. **PHI:** no patient identifiers, no room+time that identifies a
   patient, no capture snippets from clinical VLANs.

## Page quality bar

- Title is searchable ("CAB 2026-08-27" not "Meeting notes")
- Status property on every RFC/change/incident
- Last-tested date on every runbook
- One owner (person) — not a team name
- Diagrams are embeds/links, not screenshots that rot

## Output

```text
ASSET
- page/database URL or title
- why this is canonical

SCHEMA
- properties added/changed

EDITS
- what landed

FOLLOW-UPS
- Jira link · Lucid link · stale pages to archive
```

## Reference Files
- [reference/schema-templates.md](reference/schema-templates.md) — DB properties and page templates
