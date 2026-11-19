---
name: domain-dns-configurator
description: "Use when planning DNS records, nameservers, A/AAAA/CNAME/TXT/MX, SPF/DKIM/DMARC, CDN, propagation, and rollback. Dry-run only; do not change production DNS or store provider credentials without explicit approval."
---

# Domain DNS Configurator

Plan DNS changes and rollback without applying them by default.

## Workflow

1. Inventory existing records when evidence is available.
2. Prepare proposed records, TTL, propagation plan, and rollback.
3. Mark changes `Planned` until explicit approval exists.
4. Coordinate SSL and webmaster verification with downstream skills.

## Safety Rules

- Do not change nameservers, DNS records, mail records, CDN zones, or verification TXT records without approval.
- Do not store DNS API tokens, registrar credentials, or account screenshots.

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/domain-dns-configurator
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/domain-dns-configurator
python3 -m json.tool $CODEX_HOME/skills/domain-dns-configurator/evals/evals.json >/dev/null
```
