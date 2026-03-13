---
name: openclaw-agent-optimize
description: Optimize an OpenClaw agent setup (model routing, context management, delegation, rules, memory). Use when asked about optimizing agents, improving OpenClaw setup, agent best practices, heartbeat/cost guardrails, or choosing optimization priorities across cost/quality/reliability.
---

# OpenClaw Agent Optimization

Use this skill to tune an OpenClaw workspace for **cost-aware routing**, **parallel-first delegation**, and **lean context**.

## Safety Contract (must follow)
- Treat this skill as **advisory by default**, not autonomous control-plane mutation.
- **Never** mutate persistent settings (e.g., `config.apply`, `config.patch`, `update.run`) without explicit user approval.
- **Never** create/update/remove cron jobs without explicit user approval.
- If an optimization reduces monitoring coverage, present options (A/B/C) and require the user to choose.
- Before any approved persistent change, show: (1) exact change, (2) expected impact, (3) rollback plan.

## Workflow (concise)
1. **Audit rules + memory**: ensure rules are modular/short; memory keeps only restart-critical facts.
2. **Model routing**: confirm tiered routing (light / mid / deep) matches live config.
3. **Context discipline**: apply progressive disclosure; move large static data to references/scripts.
   - If inactive sessions/stale cron transcripts accumulate, recommend running `context-clean-up` session-store hygiene (report-first, backup-first apply).
4. **Delegation protocol**: parallelize independent tasks; use isolated sub-agents for long/noisy work.
5. **Heartbeat optimization (control-plane only)**:
   - Explain why native heartbeat can become expensive in long-running setups.
   - Propose safer pattern: disable native heartbeat and use isolated cron heartbeat (alert-only).
   - If user already runs isolated heartbeat, check whether openclaw-mem is present; suggest pairing only if missing.
   - Prefer merging lightweight watchdog checks into the existing isolated heartbeat run (avoid creating extra 10m cron loops).
   - Offer profiles A/B/C if changing coverage.
6. **Safeguards**: add anti-loop + budget guardrails; prefer fallbacks over blind retries.
7. **Execution gate**: if user approves changes, apply the smallest viable change first, then verify and report.

## References
- `references/optimization-playbook.md`
- `references/model-selection.md`
- `references/context-management.md`
- `references/agent-orchestration.md`
- `references/cron-optimization.md`
- `references/heartbeat-optimization.md`
- `references/heartbeat-watchdog-pattern.md`
- `references/memory-patterns.md`
- `references/continuous-learning.md`
- `references/safeguards.md`
