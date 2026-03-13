---
name: security-incident-response
description: "Security incident workflow for triage, containment, eradication, and recovery evidence handling. Use when suspected or confirmed security incidents require coordinated response actions; do not use for proactive threat modeling or routine vulnerability backlog grooming."
---

# Security Incident Response

## Overview
Use this skill to run a structured response that minimizes blast radius, preserves evidence, and restores service safely.

## Scope Boundaries
- Indicators of compromise or security alerts require investigation.
- Active abuse is suspected and containment decisions are needed.
- Security incident communications and recovery criteria must be formalized.

## Templates And Assets
- Incident timeline template:
  - `assets/security-incident-timeline-template.md`

## Inputs To Gather
- Detection source, initial evidence, and confidence level.
- Affected systems, data classes, and business criticality.
- Available responders and escalation contacts.
- Legal/compliance notification obligations and time limits.

## Deliverables
- Incident timeline with key decisions and evidence references.
- Containment and eradication action plan with owner and deadline.
- Stakeholder communication record and regulatory decision log.
- Recovery validation checklist and follow-up prevention actions.

## Workflow
1. Classify severity using impact, exploitability, and blast-radius evidence.
2. Start timeline capture with `assets/security-incident-timeline-template.md`.
3. Establish a command structure (incident lead, forensic owner, comms owner).
4. Contain actively exploited paths first, preserving forensic artifacts before destructive cleanup when feasible.
5. Scope affected identities, services, data stores, and downstream dependencies.
6. Eradicate root access path, rotate exposed credentials, and patch exploited weaknesses.
7. Recover in staged rollout with explicit rollback criteria and heightened monitoring.
8. Publish a post-incident action list with prevention owners and due dates.

## Quality Standard
- Severity classification is evidence-based and revisited as facts evolve.
- Containment actions are traceable and reversible when possible.
- Evidence handling preserves chain-of-custody requirements.
- Recovery criteria include security validation, not only availability checks.

## Failure Conditions
- Stop when roles and decision authority are unclear.
- Stop when evidence is being destroyed without explicit incident lead approval.
- Escalate when potential legal notification thresholds are crossed.
