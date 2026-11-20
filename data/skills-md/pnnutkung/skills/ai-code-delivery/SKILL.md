---
name: ai-code-delivery
description: "Use when shipping, reviewing or releasing code written by an AI agent: deciding how to gate it behind a feature flag, how deeply to review it, what proof a PR must carry, or how to roll it out. Not for the production-hazard review of a diff itself; that is zero-trust-review."
---

# AI Code Delivery

Delivery gates for agent-written code: gate it, triage review depth, demand proof, review in a fresh context, audit before GA, ramp behind the flag. The full human-followable runbook is [`runbook.md`](./runbook.md); read only the sections for your role.

## Pick your role

| Role | Do | Runbook |
|---|---|---|
| Author (before opening the PR) | Create the flag before any feature code; fill the PR template; get CI lint/type/format green | 1, 3, 4 |
| Reviewer (gating the PR) | Classify trunk vs leaf; reject a PR missing proof; run the independent review | 2, 3, 5 |
| Release owner (turning it on) | Run the 80/20 audit; canary, soak, ramp; flip the flag off on a trip | 6, 7 |

## Rules

- **Flag first.** No feature code is written until the flag exists and integration points sit behind it.
- **Proof or reject.** A PR missing the flag name, test results, runtime/visual proof or a concise summary is rejected; name the missing item.
- **Trunk gets read, leaf gets skimmed.** Deep line-by-line only for trunk code; a gated leaf needs tests and artifacts.
- **Fresh reviewer.** The authoring session never reviews its own diff.
- **Flag off, not revert.** Roll back by flipping the flag.

## Hand-offs

- Independent review of the diff (runbook 5.1): **REQUIRED SUB-SKILL:** use `zero-trust-review` in a new session. It owns production-hazard and test-integrity findings, including feature-flag ON/OFF paths.
- PR babysitting (runbook 5.2): use the host's review bot or any skill you have that reads PR comments, fixes, reruns checks and pushes. This skill does not ship one.

## Common mistakes

- Reviewing agent output in the session that wrote it.
- Treating "merged behind a flag" as done; skipping the 20% audit before GA.
- Reading every line of a gated leaf while skimming the trunk change that wires it in.
