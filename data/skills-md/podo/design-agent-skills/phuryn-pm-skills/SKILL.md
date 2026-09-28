---
name: phuryn-pm-skills
description: |
  PM Skills Marketplace — 65 product-management skills and 36 chained workflows
  across 8 plugins: product discovery, product strategy, execution (PRDs, OKRs,
  roadmaps, sprints, retros, release notes), market research, data analytics
  (SQL, cohort analysis, A/B testing), go-to-market, marketing & growth, and a
  PM toolkit. Encodes proven frameworks for discovery → strategy → execution →
  launch → growth.
triggers:
  - "phuryn"
  - "PM skills marketplace"
  - "JTBD personas"
  - "interview script"
  - "feature prioritization"
  - "analyze feature requests"
  - "create PRD"
das:
  type: package
  category: product-pm
  upstream: "https://github.com/phuryn/pm-skills"
  version: latest
---

# phuryn-pm-skills

> Catalogue stub — full package: [phuryn/pm-skills](https://github.com/phuryn/pm-skills)

## Install the full skill

This package ships as a Claude plugin marketplace (8 plugins), not as a single
`npx skills add` bundle. Add the marketplace, then install the plugins you need:

```bash
claude plugin marketplace add phuryn/pm-skills
```

Then install individual plugins:

```bash
claude plugin install pm-product-discovery@pm-skills
claude plugin install pm-product-strategy@pm-skills
claude plugin install pm-execution@pm-skills
claude plugin install pm-market-research@pm-skills
claude plugin install pm-data-analytics@pm-skills
claude plugin install pm-go-to-market@pm-skills
claude plugin install pm-marketing-growth@pm-skills
claude plugin install pm-toolkit@pm-skills
```

In Claude Cowork: **Customize → Browse plugins → Personal → + → Add marketplace
from GitHub → `phuryn/pm-skills`**.

## What it does

65 PM skills + 36 chained workflows across 8 plugins:

| Plugin | Covers |
|--------|--------|
| `pm-product-discovery` | Ideation, assumptions, experiments, customer interviews |
| `pm-product-strategy` | Vision, business models, pricing, competitive analysis |
| `pm-execution` | PRDs, OKRs, roadmaps, sprints, retrospectives, release notes |
| `pm-market-research` | Personas, segmentation, journey maps, market sizing |
| `pm-data-analytics` | SQL queries, cohort analysis, A/B test analysis |
| `pm-go-to-market` | GTM strategy, beachhead segments, battlecards |
| `pm-marketing-growth` | Marketing ideas, positioning, North Star metrics |
| `pm-toolkit` | Resume review, legal templates, proofreading |

## When NOT to use

- Lightweight discovery + roadmaps/metrics in one bundle → use `assimovt-productskills`
- Customer journey maps / story mapping → use `deanpeters-pm-skills`
- Triple Diamond / Design Sprint facilitation → use `pm-skills`
- Behavioral product design, growth loops → use `lenny-skills`
