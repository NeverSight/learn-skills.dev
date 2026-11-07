---
name: wtk-ship
description: Ship a proven feature through verification, local gates, lifecycle closeout, and authorized branch delivery. Use when asked to ship a proven feature.
disable-model-invocation: true
argument-hint: "[the work, in your own words]"
---

# Workflow Toolkit Ship

Deliver the requested branch using the scope rules in `.agents/skills/wtk/references/validation.md`.

At delivery start, read [execution metrics](../wtk/references/execution-metrics.md). Reuse collected
stage receipts and append the footer at the authorized stopping point; missing usage is not a gate.

Before delivery closeout or worktree removal, apply
[runtime lifecycle](../wtk/references/runtime-lifecycle.md) and include cleanup/retention evidence
in the normal handoff.

## Previously verified work

Identify the recorded verified base and the subsequent diff. If that diff is bounded maintenance,
use the existing receipt plus its scoped evidence and proceed to delivery. A merge request does not
trigger a new full-branch Verifier, full gate or QA cycle. Closed artifacts may remain in Git; do not
recreate them merely to satisfy this entrypoint. Apply active feature closeout only to unverified
feature work or a substantive change whose named risk requires that scope.

## Active feature closeout

An active Lean feature has `.specs/features/<feature>/plan.md`, `checks.md`, and independent
`verification.md`. The following steps apply to that feature scope.

Resolve or resume the approved selection through `.agents/skills/wtk-lean/scripts/workflow_route.py`
when a feature snapshot is required. Proposed delegation follows
[agent selection](../wtk/references/agent-selection.md) in the current checkout.

1. Confirm the feature's verification report passes the profile recorded in `checks.md` by running
   `.agents/skills/wtk-lean/scripts/validate_verification.py <feature>`.
2. Apply incremental impact selection from `.agents/skills/wtk/references/validation.md`, including merges from main.
   Run invalidated proofs and reuse valid evidence; a full gate needs that reference's trigger or an
   explicit human request. Run selected `wtk-deep-review`, security, UI and QA procedures only for
   their affected scope.
3. Promote durable decisions, lessons, product promises, architecture rules, and QA evidence to
   their owning stores. Promotion is semantic work; do not invent an automatic knowledge merger.
4. After promotion is complete, delete the entire transient feature directory with
   `python3 .agents/skills/wtk-ship/scripts/close_feature.py <feature> --promoted`. The helper refuses
   cleanup without a passing verification receipt and explicit promotion confirmation.

## Delivery authority

Invoking this skill authorizes the feature branch push, one pull request, and merge after readiness
is rechecked immediately before the merge. Do not pause between those scoped delivery steps. Deploy,
release, production mutations, force-push, direct push to `main`, and unrelated remote actions remain
separately authorized.

If required readiness evidence is missing, name the affected scope and required check. A builder
never certifies its own feature; feature verification uses a fresh agent over the complete feature
range. Confirmed Critical, Major,
and Minor Deep Review findings are fixed in the feature run before delivery.
