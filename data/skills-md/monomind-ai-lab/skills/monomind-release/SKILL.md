---
name: monomind-release
description: "Assess, prepare, or execute a production release, migration, or staged rollout with explicit gates, observability, and rollback. Use when work is approaching a live environment or the user asks for launch readiness. Readiness review does not itself authorize deployment."
---

# Monomind Release

Make the release target exact, the health decision observable, and the path backward credible before changing live state.

## Frame authority and risk

1. If a profile or managed policy exists, require the installed workflow script's `check --gate release --repo <repository>` before executing deployment, migration, or release. Integration or merge alone uses `--gate integration`. Reuse a valid check for the same policy/tool version; after relevant changes, rerun the affected gate. Route only that boundary's missing policy to onboarding. Read-only assessment may continue with gaps stated.
2. Identify the exact revision, artifact, environment, audience, data boundary, and requested operation.
3. Distinguish readiness assessment, preparation, and live execution. Deploy, migrate, change traffic, or notify others only when the user's authority covers that exact action and target.
4. Classify the dominant risks: correctness, security/privacy, data compatibility, availability, performance, accessibility, and operator recovery.

## Build the release contract

Use repository-native quality gates and add only risk-relevant checks. The contract must include:

- acceptance and regression evidence for the exact artifact;
- configuration, secret, dependency, migration, and compatibility checks;
- success and failure signals visible during rollout;
- release owner, observation window, and decision maker;
- rollback triggers, steps, data implications, and estimated recovery time.

Derive advance, hold, and rollback thresholds from project SLOs, historical baselines, contractual limits, or an explicit user decision. Do not import generic percentages as if they were facts.

For each new operational path, start from the questions an operator will ask. Use metrics to show that something is wrong, traces to show where, and structured logs to show why. Keep identifiers bounded in metric labels and keep secrets and personal data out of telemetry.

When several entry points feed one job and log sink, record the entry point at the boundary and carry it with the run's correlation ID through queues and calls. A correlation ID alone cannot tell an operator whether a scheduler, replay endpoint, or manual run started the work.

For each actionable release alert, link an owned runbook that states what the alert means, the first diagnostic check, and who to escalate to if that check does not resolve it. Verify the check and escalation path before rollout; correct the runbook when an incident reveals a missing or wrong step.

## Roll out proportionally

When the platform and risk justify staging:

1. Verify in the closest safe environment.
2. Deploy inert or compatibility-preserving code where possible.
3. Expose the smallest meaningful cohort.
4. Observe the predeclared signals for the agreed window.
5. Advance, hold, or roll back from evidence—not schedule pressure.
6. Remove temporary compatibility paths and flags after the defined stability condition.

Flags need an owner, default state, both-state verification, and removal condition. Database changes prefer expand–migrate–contract so rollback does not require impossible data reconstruction.

Rehearse the rollback or validate every command against a safe target. Never claim rollback is available merely because a previous artifact exists.

## Release record

Record the artifact, environment, checks, approvals, start/end times, observed signals, decisions, incidents, and cleanup work. Keep credentials and sensitive runtime data out of the record.

## Completion criteria

- The exact target and execution authority are explicit.
- Gates and thresholds come from project evidence or a recorded decision.
- Monitoring answers the release's dominant risk questions.
- Rollback is executable and accounts for data compatibility.
- The release record ties observed outcomes to the deployed artifact.
- Temporary flags and compatibility paths have owners and removal conditions.
