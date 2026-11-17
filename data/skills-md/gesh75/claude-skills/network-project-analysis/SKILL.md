---
name: network-project-analysis
description: Deep-analyze a network project — RFC, design, SOW, cutover, gaps, blast radius, cost, risk. Use for campus/DC/WAN/cloud/wireless programs, vendor proposals, or "review this design". Pair with healthcare-network when clinical.
origin: snm-pack
---

# Network project analysis

Produce a **decision-grade** review, not a summary. Assume the reader must
approve, defer, or send back. If facts are missing, list them as blockers;
do not invent topology, part numbers, or circuit IDs.

## When to use

- RFC / HLD / LLD / vendor SOW / RFP response
- "What's wrong with this network project?"
- Refresh, SD-WAN, DC fabric, wireless, segmentation, internet edge
- Go-live readiness, gap analysis vs current state

## Method (do in order)

1. **Frame** — business outcome, sites, apps, constraints (budget, freeze, clinical, compliance).
2. **Current state** — what exists, what is actually true (not the last Visio).
3. **Target state** — L1/L2/L3, overlay, identity, ops tooling, failure domains.
4. **Delta** — work packages, sequence, dependencies, vendor vs in-house.
5. **Blast radius** — what dies if this is wrong; dual-homing; rollback.
6. **Score** — see [reference/scoring-model.md](reference/scoring-model.md).
7. **Verdict** — approve / approve-with-conditions / rework / reject.

Healthcare, PHI, biomedical, EHR: also load `healthcare-network`.

## Required review lenses

| Lens | Fail if |
|------|---------|
| Availability | Single points of failure on the critical path; untested failover |
| Change | No freeze map, no rollback, no peer review, no named verifier |
| Security | Flat L2, shared management, vendor jump hosts, no NAC plan |
| Operability | No monitoring, no config backup, no as-built, hero-only knowledge |
| Capacity | No 3-year growth, oversubscription unstated, license bombs |
| Cost | Capex-only; opex, optics, TAC, optics, professional services omitted |
| Compliance | No BAA, no logging retention, no ePHI path map (healthcare) |

## Output

```text
VERDICT
- approve | approve-with-conditions | rework | reject
- one-paragraph why

SCORECARD
- availability / security / operability / cost / compliance  (1–5 each)
- see scoring-model.md

GAPS (ranked)
- id · severity · evidence · treatment · owner

BLAST RADIUS
- sites, VRFs, apps, clinical services
- rollback time and trigger

CONDITIONS TO APPROVE
- must-fix before CAB
- watch-items after go-live

NEXT ARTIFACTS
- Jira epics · Notion RFC · Lucid target-state · CAB date
```

Draw the as-is / to-be with `network-diagrams` (fast) or `lucid-diagrams`
(stakeholder). File the RFC via `atlassian-ops` + `notion-ops`.

## Anti-patterns to call out

- "Big bang" cutovers with no canary site
- Collapsing OOB management into in-band
- Wireless as an afterthought
- Copy-paste QoS from a different campus
- Vendor BoM with no optics/licensing/spares
- SD-WAN overlay with an unowned underlay
- "We'll segment later"
- Packet capture as the monitoring strategy (especially on clinical VLANs)

## Reference Files
- [reference/scoring-model.md](reference/scoring-model.md) — 1–5 scorecard
- [reference/rfc-template.md](reference/rfc-template.md) — RFC / HLD skeleton
