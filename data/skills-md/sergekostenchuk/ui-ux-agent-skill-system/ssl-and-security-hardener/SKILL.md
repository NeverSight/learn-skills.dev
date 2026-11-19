---
name: ssl-and-security-hardener
description: "Use when planning SSL/TLS, HTTPS redirects, HSTS, security headers, CSP, cookie flags, backups, monitoring, and basic launch hardening. Dry-run first; do not mutate production server, DNS, certificates, or secrets without explicit approval."
---

# SSL And Security Hardener

Plan launch security hardening and verification without mutating production.

## Workflow

1. Identify target stack, hosting, domain, and approval status.
2. Plan SSL/TLS, redirects, HSTS, headers, CSP, cookies, backups, monitoring, and vulnerability basics.
3. Define verification commands and rollback.
4. Coordinate final gate with `launch-readiness-auditor`.

## Safety Rules

- Do not issue certificates, change server config, force HTTPS, edit CSP, or rotate secrets in production without approval.
- Do not store private keys, cert private material, tokens, or `.env`.

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/ssl-and-security-hardener
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/ssl-and-security-hardener
python3 -m json.tool $CODEX_HOME/skills/ssl-and-security-hardener/evals/evals.json >/dev/null
```
