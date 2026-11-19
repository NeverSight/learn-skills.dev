---
name: migration-planner
description: Plan safe website migrations when existing URLs, redirects, sitemap, robots, schema, canonical pages, metadata, analytics, webmaster tools, or launch monitoring may change. Use after existing-site analysis or rebuild decisions; never apply production redirects, DNS, deploy, or webmaster mutations without explicit approval.
---

# Migration Planner

This skill creates a rollback-aware migration plan for existing sites. It is planning and validation-first, not a production mutation tool.

## Operating Modes

- `url-map`: map old URLs to new URLs and identify canonical decisions.
- `redirect-plan`: plan 301/302 rules without applying them.
- `seo-surface`: preserve titles, descriptions, headings, schema, sitemap, robots, llms.txt, and internal links.
- `launch-checklist`: define pre-launch, launch, and post-launch verification.
- `rollback`: prepare rollback, monitoring, and alert criteria.

## Required Workflow

1. Read [references/migration-safety-contract.md](references/migration-safety-contract.md).
2. Start from `existing-site-analyzer` evidence and `rebuild-or-improve-advisor` decision.
3. Use [assets/migration-plan.template.md](assets/migration-plan.template.md).
4. Build a URL/change map:
   - old URL;
   - new URL;
   - status;
   - redirect type;
   - canonical rule;
   - metadata/schema preservation note.
5. Add sitemap, robots, schema, internal links, llms.txt, analytics, and webmaster verification checks.
6. Mark production actions as `Planned` until the user explicitly approves deploy, DNS, redirects, GSC/webmaster, or server changes.

## Safety Rules

- Do not apply redirects, edit robots/sitemap in production, deploy, change DNS, or submit GSC/webmaster changes without explicit approval.
- Do not store private analytics exports, tokens, cookies, or verification codes in the plan.
- Do not mark migration checks `Ran` unless the command or artifact exists.
- If high SEO risk remains, block launch handoff until rollback and monitoring are defined.

## Handoff Shape

```text
Migration mode:
Decision source:
URL map path:
Redirect plan:
SEO surface preservation:
Launch approvals needed:
Rollback plan:
Monitoring:
Next owner:
Checks:
```

## Validation

When editing this skill, run:

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/migration-planner
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/migration-planner
python3 -m json.tool $CODEX_HOME/skills/migration-planner/evals/evals.json >/dev/null
```
