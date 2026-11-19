---
name: serp-source-configurator
description: Configure SERP/search-demand source settings before keyword harvesting. Use when a UI/UX, SEO, or site project needs a user-facing source setup gate, OpenSERP self-host settings, proxy provider/API-key fields such as AKE, checkbox selection of Google/Yandex/Bing/DuckDuckGo/Ecosia/Baidu/manual sources, paid-proxy/budget limits, approval notes, or preflight checks before `serp-keyword-harvester` sends external queries.
---

# SERP Source Configurator

This skill owns the setup gate before search-demand collection. It does not harvest keywords itself; it creates a redacted, approval-aware source configuration and hands it to `serp-keyword-harvester`.

## Operating Modes

- `design-ui`: define user-facing fields, checkboxes, statuses, and safe defaults for a source settings panel.
- `configure`: create or update a redacted `reports/serp-source-config.json`.
- `preflight`: check OpenSERP/base URL/proxy readiness and record `Ran`, `Skipped`, or `Planned`.
- `budget-gate`: set query limits, engine limits, cache TTL, timeout, and paid-proxy rules.
- `audit`: review an existing source config for secrets, missing approvals, unsafe paid settings, or unclear handoff.

## Required Workflow

1. Read [references/decision-framework.md](references/decision-framework.md).
2. If proxy providers, API keys, OpenSERP, AKE, paid traffic, or external network calls are involved, read [references/safety-boundaries.md](references/safety-boundaries.md).
3. For UI/dashboard requests, use [references/ui-controls.md](references/ui-controls.md) and [assets/source-config.template.json](assets/source-config.template.json).
4. Classify sources:
   - local/manual inputs: allowed by default;
   - direct OpenSERP engines: approval required before external queries;
   - proxy-backed engines: approval plus budget and proxy precheck required;
   - paid or account-mutating provider actions: explicit confirmation immediately before action.
5. Never store API keys, proxy credentials, cookies, recovery codes, or `.env` values in Markdown, HTML, task plans, wiki notes, reports, screenshots, or exported JSON.
6. Write only redacted configuration and runtime references such as `env:AKE_API_KEY`.
7. Validate the source config with [scripts/validate_serp_source_config.py](scripts/validate_serp_source_config.py).
8. Hand off to `serp-keyword-harvester` only after approval, selected engines, limits, and failure behavior are explicit.

## System Role

Use this skill between the SEO/site architecture layer and the keyword harvester:

```text
seo-llm-site-architect
-> serp-source-configurator
-> serp-keyword-harvester
-> semantic-core-builder
```

`serp-source-configurator` owns source settings, proxy gates, credential handling, budget limits, and preflight status. `serp-keyword-harvester` owns actual keyword/SERP evidence collection.

## Output Standard

```text
Mode:
Selected sources:
Disabled sources:
Proxy mode:
Credential handling:
Approval status:
Budget limits:
Preflight:
Output config:
Skipped/planned checks:
Next skill: serp-keyword-harvester
```

## Safety Rules

- Treat OpenSERP and provider APIs as `external-network`.
- User-entered API keys are runtime inputs only; redact them before any artifact is written.
- Do not create, refresh, rotate, buy, or mutate provider proxy ports unless the user explicitly asks for that specific action.
- Prefer direct/free engines first. Use paid proxy only for engines that need it, usually Google/Yandex.
- If proxy precheck fails, keep proxy sources `Skipped` and continue with direct/manual sources.
- Do not retry paid proxy failures aggressively.

## Validation

When editing this skill, run:

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/serp-source-configurator
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/serp-source-configurator
python3 $CODEX_HOME/skills/serp-source-configurator/scripts/validate_serp_source_config.py $CODEX_HOME/skills/serp-source-configurator/assets/source-config.template.json
```
