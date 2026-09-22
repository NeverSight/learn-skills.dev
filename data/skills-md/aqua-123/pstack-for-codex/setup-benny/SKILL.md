---
name: setup-benny
description: "Install, inspect, upgrade, or remove the dormant Benny polling pack for Codex. Use when configuring Benny's Slack, tracker, repository, control adapter, canonical state, canaries, or two paused automations."
---

# Set up Benny for Codex

Benny is an optional, dormant automation pack. Setup never activates external writes. Operational instructions are copied from `../../automations/benny/` into the target project at `.codex/automations/benny/`; they are not registered skills. Read that pack's `FOR_AGENTS.md` and `README.md` before any setup action.

## Authority and ownership

- Require explicit user authority to install, upgrade, uninstall, purge state, run a live canary, create automations, or change automation status.
- Default all automation descriptors to `PAUSED`. Never infer activation authority from installation or configuration.
- Copy only source-managed pack paths. Keep configuration, feature maps, routing maps, receipts, and mutable state under `.codex/benny/` or a configured canonical user-owned state root.
- Record hashes of installed pack files. Upgrade or uninstall only unchanged, receipted files. Preserve user configuration and canonical state by default.
- Never write credential values. Configuration may contain only `env:NAME`, `keychain:HANDLE`, or `secret-manager:HANDLE` references.

## Setup gate

Collect and validate:

1. exact workspace/team, source channel, trusted triage identity, repository, default branch, tracker, control adapter, and approved feature/routing map hash;
2. a canonical absolute state root shared by both scheduler worktrees, outside every repository checkout, owner-only, source-control excluded, and capable of atomic create/rename;
3. least-privilege scopes and qualified destination idempotency or authoritative operation-key lookup for every writing adapter;
4. credential-free repository execution with network denied by default and every exceptional host explicitly receipted;
5. attachment HTTPS/domain/redirect/DNS/MIME/size/archive limits, polling cutoff/overlap/page/batch limits, retry/backoff/retention budgets, and outbound minimization limits;
6. the read-only, test-channel triage, repro-only, bounded-fix, concurrent-race, and ambiguous-write canaries.

Use `automations/benny/scripts/reconcile-state.mjs` to validate state behavior. Missing or unobservable capabilities are named activation blockers, not assumptions.

## Automation lifecycle

Only after the user explicitly authorizes automation creation or update, use the supported Codex automation surface to reconcile exactly two project cron automations by stable name:

- `pstack-benny-triage`
- `pstack-benny-reproduce`

Search existing automations by name and stored ID first. Update the existing IDs; never create duplicates. Create or update both as `PAUSED`, with local project execution and the copied prompt files. A separate, later explicit request is required to activate either one. If any blocker remains, keep both paused.

## Report

Return the installed and preserved paths, source hashes, canonical state root and permissions, external credential reference names (never values), adapter qualifications, allowed network hosts, canary results, stable automation IDs, status of both automations, activation blockers, retention policy, and reversible uninstall/purge instructions.
