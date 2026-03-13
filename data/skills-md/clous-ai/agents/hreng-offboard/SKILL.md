---
name: hreng-offboard
description: Use when the user is planning an exit or handoff for a departing team member; produce exit checklist (access, docs, knowledge transfer, last day), handoff doc, and access-revoke list.
version: 1.0.0
license: MIT
---

# Offboard / Exit

Produce an exit checklist, handoff plan, and access-revoke list to close the employee lifecycle cleanly.

## When to Use

Use this skill when:
- An employee is **leaving** (resignation, end of contract, termination) and you need a structured handoff.
- You want an **exit checklist** (access revoke, docs, knowledge transfer, last day).
- You need a **handoff doc** for continuity (owner, status, contacts).

Do **not** use this skill when:
- The focus is **onboarding a new hire** → use `hreng-onboard-306090`.
- The focus is **performance or PIP** → use `hreng-perf-diagnose` / pip command.

## Inputs Required

- Person, role, last day (if known).
- Systems they use, docs they own, key contacts (AskUserQuestion or Read).
- Handoff recipient(s) (manager, teammate, backup).

## Outputs Produced

- **Exit checklist**: access revoke list, doc ownership transfer, knowledge transfer items, final day logistics (equipment, badge, offboarding meeting).
- **Handoff doc**: projects/artifacts, status, next owner, contacts; use `templates/handoff-doc.md` when present.
- **Reminder**: coordinate with HR/IT for access and equipment; do not store passwords or sensitive access in the doc.

## Using Supporting Resources

### Templates
- **`templates/exit-checklist.md`** – Exit checklist (access, docs, knowledge transfer, last day).
- **`templates/handoff-doc.md`** – Handoff document (owner, status, contacts).

### References
- None in-repo; coordinate with HR/IT and onboarding (e.g. `hreng-onboard-306090`) for continuity.

### Scripts
- No validation script; rely on HR/IT workflows for access and equipment.

## Core Pattern

1. **List systems and access** (code, infra, SaaS, docs, keys).
2. **List deliverables and docs** they own; assign next owner per item.
3. **Knowledge transfer**: what only they know; suggest sessions or docs.
4. **Last day**: equipment return, access cut, final conversation, exit survey if applicable.
5. **Output** checklist + handoff doc; remind HR/IT coordination.

## Common Mistakes

- Listing credentials or secrets in the handoff doc; only list systems and owners.
- Skipping knowledge-transfer sessions when the leaver is the only expert.
- Not aligning with HR/IT on access cut timing and equipment return.

## Legal disclaimer

This skill supports exit and handoff logistics only; it is **not** legal advice. Termination, final pay, benefits, and restrictive covenants vary by jurisdiction and contract. Consult HR/legal for terminations and sensitive exits.

## Tips

- Prefer MCP for org/access data if available; do not exfiltrate credentials.
- Keep handoff doc in a shared, access-controlled location.
