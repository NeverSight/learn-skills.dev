---
name: paid-traffic-architect
description: "Use when a website needs paid traffic planning: campaigns, audience hypotheses, UTM maps, landing requirements, creative briefs, budget placeholders, and SEO/ads handoffs. Planning only; never launch campaigns, spend budget, or mutate ad accounts without explicit approval."
---

# Paid Traffic Architect

This skill prepares paid traffic plans and landing requirements. It does not access or change ad accounts by default.

## Operating Modes

- `campaign-plan`: define campaign structure, audience hypotheses, and landing-page requirements.
- `utm-map`: create UTM conventions and reporting alignment.
- `creative-brief`: define ad angles and asset requirements.
- `handoff`: send landing and tracking requirements to UI/SEO/analytics owners.

## Required Workflow

1. Read [references/paid-traffic-safety-contract.md](references/paid-traffic-safety-contract.md).
2. Use [assets/paid-traffic-plan.template.md](assets/paid-traffic-plan.template.md).
3. Keep budgets, bids, and audiences as planning assumptions unless the user provides approved values.
4. Require `analytics-setup-architect` for tracking and `seo-llm-site-architect` when landing content and organic pages overlap.

## Safety Rules

- Do not launch campaigns, spend money, edit pixels, upload audiences, or change ad accounts without approval.
- Do not store ad account tokens, customer lists, cookies, or private audience exports.
- Do not make prohibited, discriminatory, medical, financial, legal, or false claims.

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/paid-traffic-architect
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/paid-traffic-architect
python3 -m json.tool $CODEX_HOME/skills/paid-traffic-architect/evals/evals.json >/dev/null
```
