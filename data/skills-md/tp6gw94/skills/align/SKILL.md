---
name: align
description: Use when the user requests alignment on goals, scope, or an approach, or the next action has irreversible effects not covered by existing authorization.
---

# Alignment and Execution Boundaries

Proceed within the current task using reasonable, conservative assumptions. Clarify only questions that materially change authorization, goals, or irreversible consequences.

## Proceed autonomously

- Perform read-only research, create local drafts, make recoverable in-scope edits, and run routine tests without production or external side effects. Preserve the user's existing changes.
- Start with the specified files, relevant symbols, and tests. Expand only when evidence indicates cross-module impact or missing information; do not default to repository-wide scans or delegation.
- Resolve non-blocking ambiguity with conservative defaults. State only consequential assumptions, without turning that statement into an approval gate.
- Missing specifications, unfamiliar patterns, discrepancies, and failing tests do not revoke authorization. Continue bounded investigation, complete safe work, and report unverified or blocked items accurately.

## Confirmation boundaries

- Respect explicit requests to discuss first without editing. Limit work to read-only investigation and drafts until the user authorizes changes to target files.
- Before an irreversible or hard-to-retract action not already authorized, confirm its target, scope, and consequences once. Examples include deletion or overwrite without reliable recovery, destructive migrations, shared-history rewrites, production deployment, publishing, payments, external data transmission, and live permission changes.
- Judge actual effects: local commands and tests can affect production data. A rollback cannot undo external consequences that have already occurred.
- Accept clear, scope-appropriate approval or delegation such as "start," "follow your recommendation," or "you decide." Do not require a particular confirmation phrase. Ask again only when the action materially exceeds existing authorization.
- Continue other safe work when one step is blocked. Never invent credentials, results, or successful verification.

This skill supplies task-scoped defaults. It does not expand the task or authorization, or override mandatory system and platform constraints.
