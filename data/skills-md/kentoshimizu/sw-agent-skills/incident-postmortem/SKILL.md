---
name: incident-postmortem
description: "Incident postmortem workflow for evidence-backed root cause analysis and systemic prevention actions. Use after incident stabilization when teams need timeline, root-cause chain, contributing factors, and owned prevention actions; do not use for active incident command and real-time mitigation."
---

# Incident Postmortem

## Overview
Use this skill to turn incidents into concrete learning and prevention changes, not just narrative summaries.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Root-cause evidence rules:
  - `references/root-cause-evidence-rules.md`

## Templates And Assets
- Postmortem report template:
  - `assets/postmortem-report-template.md`
- Incident timeline template:
  - `assets/incident-timeline-template.csv`
- Corrective action tracker:
  - `assets/corrective-action-tracker-template.csv`

## Inputs To Gather
- Incident timeline signals and operational evidence.
- Customer/business impact and severity context.
- Mitigation and recovery actions taken.
- Known system/process constraints.

## Deliverables
- Evidence-backed postmortem report.
- Timeline artifact linking events to signals.
- Corrective action plan with owner, due date, and verification.
- Residual risk statement and follow-up tracking.

## Workflow
1. Build timeline in `assets/incident-timeline-template.csv`.
2. Analyze trigger, root causes, and contributors using `references/root-cause-evidence-rules.md`.
3. Draft report in `assets/postmortem-report-template.md`.
4. Track prevention actions in `assets/corrective-action-tracker-template.csv`.
5. Publish and align owners on verification timelines.

## Quality Standard
- Root cause is evidence-backed, not speculative.
- Timeline and impact statements are explicit and auditable.
- Corrective actions are specific, owned, and verifiable.
- System/process improvements are prioritized over blame narratives.

## Failure Conditions
- Stop when root-cause claims lack supporting evidence.
- Stop when action items have no owner or verification method.
- Escalate when residual risk exceeds accepted reliability policy.
