---
name: jev
description: "Run optional advisory triage through TypeSafe's Jev model for a structured finding or a bounded Lead-facing fork, such as agent-delivery-workflow's fork routing, returning a bounded judgment or an unavailable result. Use when a finding or fork needs machine-assisted triage before a deterministic rule or Human gate decides it. Do not use it to resolve a Human gate itself, authorize an action, or replace source review or deterministic rules; the judgment is advisory only."
---

# Jev

Jev sends structured input to TypeSafe System One and returns advisory judgments. Use it only when advisory triage helps; callers must keep their deterministic behavior when a request is unavailable. Never treat a judgment as authorization, a gate resolution, proof of correctness, or a replacement for reading the cited source.

Run `python3 <this-skill>/scripts/jev.py finding --file <finding.json>` to assess whether a structured finding describes an actionable misfit, cites an artifact, and its severity. Run `python3 <this-skill>/scripts/jev.py fork --file <fork.json>` to advise on a bounded Lead-facing fork. Fork input has a `fork` object with boolean `hard_gate` and optional `delegation` object with boolean `in_force`. Hard gates and forks without an in-force delegation deterministically route to `human_gate`; other forks route to `supervisor_decide` only when Jev selects it with confidence of at least `FORK_CONFIDENCE_FLOOR`. Every route remains advisory.

The CLI reads the key at call time from the macOS Keychain generic-password item named by `KEYCHAIN_SERVICE` and `KEYCHAIN_ACCOUNT` in `scripts/jev.py`; a missing item gives the unavailable result. `KEYCHAIN_ACCOUNT` is the account of the single machine jev runs on; it stays a constant until jev runs on a second machine. It prints bounded JSON and never prints the key or raw model answers. Missing credentials, transport failures, invalid inputs, and invalid answers produce an unavailable result or input error; they do not authorize a fallback action. The CLI uses the standard library and makes a single request with `API_TIMEOUT_SECONDS`.
