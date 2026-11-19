---
name: rebuild-or-improve-advisor
description: Decide whether an existing site should be improved in place, redesigned, partially rebuilt, or fully rebuilt after an evidence-backed audit. Use when the project needs a governed improve/redesign/rebuild recommendation balancing UX, SEO/LLM, migration risk, technical debt, timeline, and implementation cost.
---

# Rebuild Or Improve Advisor

This skill converts existing-site evidence into a strategy decision. It does not implement the redesign and does not change production systems.

## Operating Modes

- `decision`: choose improve, redesign, partial rebuild, or full rebuild.
- `tradeoff`: compare strategy options with risks, costs, and proof needed.
- `handoff`: prepare next steps for `migration-planner`, `marketing-site-skill`, `webapp-ui-skill`, or `senior-ui-ux-orchestrator`.
- `council-input`: prepare a concise position for senior council when UX, SEO, migration, or business constraints conflict.

## Required Workflow

1. Read [references/rebuild-decision-contract.md](references/rebuild-decision-contract.md).
2. Start from an `existing-site-analyzer` report or clearly label missing evidence.
3. Compare options:
   - improve in place;
   - visual redesign on current stack;
   - partial rebuild;
   - full rebuild and migration.
4. Use [assets/rebuild-decision-record.template.md](assets/rebuild-decision-record.template.md).
5. If URLs, redirects, canonical pages, sitemap, robots, schema, or GSC/webmaster verification may change, require `migration-planner`.
6. If the recommendation affects SEO/LLM, public facts, or conversion structure, route conflicts to `senior-ui-ux-orchestrator` council.

## Safety Rules

- Do not recommend full rebuild only because visual design is weak; include migration and maintainability tradeoffs.
- Do not recommend in-place improvements when severe technical, content, or SEO issues make that unsafe.
- Do not claim search traffic, rankings, or conversion data unless source evidence exists.
- Do not change production files, redirects, analytics, DNS, CMS, or deployment settings.

## Handoff Shape

```text
Decision:
Evidence used:
Options compared:
Recommended path:
Why not the alternatives:
Migration planner required:
Implementation owner:
Validation gates:
Open risks:
```

## Validation

When editing this skill, run:

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/rebuild-or-improve-advisor
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/rebuild-or-improve-advisor
python3 -m json.tool $CODEX_HOME/skills/rebuild-or-improve-advisor/evals/evals.json >/dev/null
```
