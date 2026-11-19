---
name: deploy-orchestrator
description: "Use when planning deployments, build commands, environment checks, CI/CD, release steps, smoke tests, rollback, and monitoring. Dry-run first; do not deploy to production, change secrets, or mutate live services without explicit approval."
---

# Deploy Orchestrator

Plan deploys and verification without pushing production by default.

## Workflow

1. Detect stack, build command, environment variables, target, and approval status.
2. Prepare dry-run build/deploy plan, smoke tests, rollback, and monitoring.
3. Keep production deploy blocked until explicit approval.
4. Hand off final readiness to `launch-readiness-auditor`.

## Safety Rules

- Do not deploy production, rotate secrets, run migrations, or change live services without approval.
- Do not store or print `.env`, tokens, cookies, private URLs, or deployment secrets.

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/deploy-orchestrator
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/deploy-orchestrator
python3 -m json.tool $CODEX_HOME/skills/deploy-orchestrator/evals/evals.json >/dev/null
```
