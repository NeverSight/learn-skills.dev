---
name: andon
description: "Make software health, failure, degradation, and recovery visible through useful observability and diagnostics. Use when adding logs, metrics, traces, health checks, alerts, incident signals, or operational feedback."
---

# Andon

Andon is a visible signal that makes a problem impossible to ignore. In
software, observability should help a person detect, understand, and recover
from meaningful behavior. This is a Japanese-inspired engineering metaphor,
not a demand to instrument every line.

## Use this skill when

- a feature or service changes important behavior;
- an incident was difficult to diagnose;
- failures are silent, ambiguous, or discovered too late;
- adding logs, metrics, traces, health checks, dashboards, or alerts;
- designing retries, degradation, recovery, or operational ownership; or
- a release needs signals that prove it is healthy.

## Outcome

Produce an observability plan or implementation that answers:

- what happened;
- who or what was affected;
- when and where it happened;
- how severe it is;
- what the operator or user should do next; and
- whether the system recovered.

## Workflow

### 1. Identify decisions and failure modes

List the behavior that needs observation, the failure or degradation modes, the
people who respond, and the decisions the signals must support. Start with
actionable questions, not a preferred telemetry product.

### 2. Choose the smallest useful signals

Use structured logs for event context, metrics for rates and saturation,
traces for distributed causality, and health checks for readiness or liveness.
Choose only signals that help detect, diagnose, operate, or improve the system.

### 3. Preserve context safely

Include correlation identifiers, stable dimensions, error categories, timing,
and relevant state. Redact secrets and personal data. Avoid high-cardinality,
duplicated, or noisy signals that hide the useful signal or create unsafe cost.

### 4. Make recovery visible

Represent failure, retry, degradation, fallback, recovery, and permanent error
as distinguishable states. Health checks must reflect the dependency and
readiness semantics that operators actually need.

### 5. Exercise the signals

Trigger representative success and failure paths. Confirm that signals appear
with enough context during the failure they are meant to explain and that
alerts have an owner and a meaningful action.

## Evidence standard

An observability change is useful only when a person can use it to make a
decision. Verify the signal in the relevant runtime or test environment and
state what remains unverified.

## Boundaries

- Do not log secrets, credentials, tokens, or unnecessary personal data.
- Do not add dashboards or alerts without an operational question and owner.
- Do not use logs to compensate for missing correctness checks.
- Do not treat a green health check as proof that user behavior is correct.
- Do not make the system noisy enough that meaningful failures disappear.

## Handoff

Document the signals, meanings, owners, redaction rules, and response path.
Use `jidoka` for the underlying defect, `kodawari` for review, `shukka` for
release checks, or `hansei` when observability failed during an incident.

If a referenced skill is not installed, apply its named lens inline instead of
trying to invoke it.
