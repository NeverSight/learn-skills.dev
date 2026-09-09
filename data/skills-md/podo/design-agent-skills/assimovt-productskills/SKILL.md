---
name: assimovt-productskills
description: |
  16 focused product-management skills spanning the full lifecycle: discovery
  (user interviews, problem validation, JTBD, research synthesis), strategy
  (competitor analysis, positioning, strategy docs), prioritization (RICE,
  Shape Up scope-cutting and bet-sizing), evidence-first PRDs, plus launch
  plans, North Star metrics frameworks, A/B experiment design, and
  Now/Next/Later roadmaps.
triggers:
  - "productskills"
  - "assimovt"
  - "roadmap planning"
  - "metrics framework"
  - "North Star metric"
  - "experiment design"
  - "competitor analysis"
  - "Shape Up"
  - "bet sizing"
das:
  type: package
  category: product-pm
  upstream: "https://github.com/assimovt/productskills"
  version: latest
---

# assimovt-productskills

> Catalogue stub — full package: [assimovt/productskills](https://github.com/assimovt/productskills)

## Install the full skill

```bash
# Global
npx skills add assimovt/productskills -g -y

# Project
npx skills add assimovt/productskills -y
```

Install a single skill instead:

```bash
npx skills add assimovt/productskills --skill roadmap-planning metrics-framework
```

## What it does

16 evidence-first PM skills, each shipped with a worked example. Strongest on the
areas the other catalogue PM packages don't cover deeply — roadmaps, metrics,
experimentation, competitive analysis, strategy, and Shape Up scoping.

| Sub-skill | Best for |
|-----------|----------|
| `user-interview` | Mom Test + YC's Five Questions — unbiased user interviews |
| `problem-validation` | Score problems on frequency × intensity × willingness-to-pay |
| `jtbd-analysis` | Jobs-to-be-Done + Forces of Progress |
| `research-synthesis` | Turn interview notes into atomic insights and patterns |
| `opportunity-mapping` | Opportunity Solution Trees (Teresa Torres) |
| `competitor-analysis` | Feature matrix, positioning map, strategic gaps |
| `product-positioning` | April Dunford's Obviously Awesome framework |
| `strategy-doc` | Playing to Win + Rumelt's Strategy Kernel |
| `feature-prioritization` | RICE scoring with enablers vs blockers lens |
| `scope-cutting` | Shape Up appetite — fixed time, variable scope |
| `bet-sizing` | Shape Up pitch format + Type 1/2 decision framework |
| `prd-writing` | Evidence-first, concise, measurable PRDs |
| `launch-plan` | Launch tiers (silent / soft / big-bang) with checklists |
| `metrics-framework` | North Star + input/output tree + counter-metrics |
| `experiment-design` | Hypothesis-driven A/B tests with a sample-size plan |
| `roadmap-planning` | Now/Next/Later roadmaps — outcomes, not features |

## When NOT to use

- Customer journey maps / user story mapping → use `deanpeters-pm-skills`
- Triple Diamond / Design Sprint facilitation → use `pm-skills`
- Broad 65-skill PM marketplace (GTM, data analytics) → use `phuryn-pm-skills`
- Behavioral product design, growth loops → use `lenny-skills`
- Go-to-market and sales motion → use `chadboyda-gtm`
