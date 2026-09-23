---
name: go-to-market
description: >-
  Plan and evaluate go-to-market strategy using positioning, acquisition,
  growth economics, market-entry, competitive-response, and governed
  agent-assisted acquisition experiments. Use for ICP, messaging, channel,
  CAC/LTV, beachhead, or automated-GTM strategy decisions. Do not use for
  campaign execution, CRM mutations, legal interpretation, product strategy,
  or visual brand design.
license: MIT
metadata:
  tags: go-to-market, cmo, marketing, positioning, messaging, acquisition, brand-architecture,
    growth-modeling, competitive-response, plg, slg
  source_repo: https://github.com/magnus919/hermes-profiles
---

# Go-to-Market — CMO Methodology

CMO-level methodology for go-to-market strategy, positioning, acquisition, brand, and growth modeling. This skill provides the frameworks and reference material for a chief marketing officer profile.

## When to Load

| Trigger | What's Needed |
|---------|---------------|
| Define positioning and messaging | `references/positioning-messaging.md` — Dunford framework, message hierarchy |
| Build acquisition channel strategy | `references/acquisition-strategy.md` — channel mix, PLG/SLG, funnel metrics |
| Design brand architecture | `references/acquisition-strategy.md` — brand systems, visual identity, brand health |
| Model growth economics | `references/growth-modeling.md` — CAC/LTV, cohort analysis, market entry |
| Develop competitive response | `references/acquisition-strategy.md` — pricing wars, feature races, brand defense |
| Plan market entry | `references/growth-modeling.md` — beachhead, land-and-expand, channel economics |
| Design AI-assisted or automated acquisition experiments | `references/agent-assisted-acquisition-experiments.md` — experiment contract, readiness gate, earned authority, signal quality, stop rules |

## Loading Order

```text
skill_view('go-to-market')
# Then domain-specific references:
skill_view('go-to-market', file_path='references/positioning-messaging.md')
skill_view('go-to-market', file_path='references/acquisition-strategy.md')
skill_view('go-to-market', file_path='references/growth-modeling.md')
# For AI-assisted targeting, outreach, reply handling, or optimization:
skill_view('go-to-market', file_path='references/agent-assisted-acquisition-experiments.md')
```

## Reference Files

| Reference | Purpose |
|-----------|---------|
| `references/positioning-messaging.md` | April Dunford positioning, message hierarchy (elevator pitch → value prop → narrative), positioning diagnostic |
| `references/acquisition-strategy.md` | Channel taxonomy, PLG vs SLG playbooks, sales funnel ratios, competitive response playbook, brand architecture |
| `references/growth-modeling.md` | CAC/LTV deep dive, cohort analysis practical guide, NRR, market entry strategy (beachhead, land-and-expand) |
| `references/decision-workflow.md` | Bounded launch/channel decisions, worked beachhead example, reusable memo, and owner routing matrix |
| `references/agent-assisted-acquisition-experiments.md` | Bounded experiment contract, readiness and responsibility gate, capability-specific earned authority, signal-quality ladder, decision loop, and stop conditions |


## Output Contract

The profile using this skill produces artifact pyramids. The response to any caller is the absolute path to `00-index.md`. See `artifact-pyramids` skill for the specification.

## When not to use

- **Sales execution and pipeline management** — this skill owns acquisition *strategy*, not running the funnel. CRM operations (contact lookup, deal pipeline views, confirmed stage changes) belong to [crm](../crm/SKILL.md).
- **Product strategy and roadmap** — product vision, PMF, and prioritization belong to `product-strategy` and `product-methodology`.
- **Visual brand identity design** — logo, palette, and brand systems belong to `brand-designer`.
- **Marketing campaign execution** — this skill defines the channel strategy and positioning; operating the channel tools is the corresponding tool skill's job.
- **Legal interpretation** — this skill records the jurisdiction, recipient type, and responsible owner as readiness inputs; `legal-strategy` or qualified counsel determines what law permits.

## Related Skills

- [artifact-pyramids](../artifact-pyramids/SKILL.md) — output contract
- [product-strategy](../product-strategy/SKILL.md) — CPO methodology (product vision, PMF, market sizing)
- [brand-designer](../brand-designer/SKILL.md) — visual brand identity design
- [seo](../seo/SKILL.md) — organic search, answer-engine, and generative-search audit and content strategy
- [crm](../crm/SKILL.md) — HubSpot CRM operations: contact lookup, deal pipeline views, and confirmed deal stage changes
- [ai-governance](../ai-governance/SKILL.md) — organizational AI risk, lifecycle gates, decision rights, and agentic controls
- [legal-strategy](../legal-strategy/SKILL.md) — legal analysis when outreach or data-use rules require interpretation
