---
name: infra-launch-orchestrator
description: "Use when a project needs launch/infrastructure coordination across domains, registrars, servers, DNS, deploy, SSL, webmaster tools, monitoring, and launch readiness. Dry-run first; do not purchase, provision, deploy, or mutate production without explicit approval."
---

# Infra Launch Orchestrator

This skill coordinates the infra/launch layer. It is not the central UI/UX chair and does not execute irreversible actions by default.

## Operating Modes

- `plan`: map launch scope, owners, approvals, rollback, and dependencies.
- `dry-run`: prepare commands/checklists without applying them.
- `handoff`: route to specialist infra skills.
- `launch-gate`: collect readiness evidence before any production action.

## Required Workflow

1. Identify requested action: advisory, dry-run, or production execution.
2. Route specialists:
   - domain ideas: `domain-name-generator`;
   - registrar choice: `domain-registrar-advisor`;
   - hosting choice: `server-selector`;
   - provisioning plan: `server-provisioner`;
   - deploy plan: `deploy-orchestrator`;
   - DNS plan: `domain-dns-configurator`;
   - SSL/security: `ssl-and-security-hardener`;
   - webmaster tools: `webmaster-registrar`;
   - final gate: `launch-readiness-auditor`.
3. Keep all irreversible or paid steps `Planned` until explicit production approval is recorded.
4. Require rollback and monitoring before launch.

## Safety Rules

- Do not buy domains, change DNS, provision paid servers, deploy production, issue destructive commands, submit webmaster changes, or store credentials without explicit approval.
- Do not print API tokens, provider credentials, SSH keys, DNS tokens, cookies, or `.env` values.
- If approval is missing, provide a dry-run plan only.

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/infra-launch-orchestrator
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/infra-launch-orchestrator
python3 -m json.tool $CODEX_HOME/skills/infra-launch-orchestrator/evals/evals.json >/dev/null
```
