---
name: product-strategy
description: >-
  Set product vision, positioning, market strategy, and portfolio direction with a
  CPO methodology. Route tactical prioritization, specifications, and backlog
  decisions to `product-methodology`; do not use this skill for delivery-level
  product decisions or unrelated requests.
license: MIT
metadata:
  tags: product-strategy, cpo, product-management, competitive-analysis, market-sizing,
    roadmap-prioritization, platform-strategy, product-lifecycle
  source_repo: https://github.com/magnus919/hermes-profiles
---

# Product Strategy — CPO Methodology

CPO-level methodology for product strategy, market analysis, competitive positioning, and platform thinking. This skill provides the frameworks and reference material for a chief product officer profile.

## When to Load

| Trigger | What's Needed |
|---------|---------------|
| Define product vision and North Star metric | `references/product-strategy.md` — North Star, product principles, vision |
| Analyze competitive landscape | `references/competitive-positioning.md` — Porter's Five Forces, Blue Ocean, positioning |
| Size a market opportunity | `references/market-analysis.md` — TAM/SAM/SOM, PMF, lifecycle |
| Prioritize a roadmap | `references/product-strategy.md` — RICE, Kano, OST |
| Assess product-market fit | `references/market-analysis.md` — Sean Ellis test, retention curves |
| Plan a platform or ecosystem strategy | `references/product-strategy.md` — API-first, marketplace, ecosystem |
| Develop market entry strategy | `references/market-analysis.md` — beachhead, land-and-expand, platform entry |

## Loading Order

```text
skill_view('product-strategy')
# Then domain-specific references:
skill_view('product-strategy', file_path='references/product-strategy.md')
skill_view('product-strategy', file_path='references/competitive-positioning.md')
skill_view('product-strategy', file_path='references/market-analysis.md')
```

## Reference Files

| Reference | Purpose |
|-----------|---------|
| `references/product-strategy.md` | North Star, product principles, RICE/Kano/OST, platform strategy, product lifecycle |
| `references/competitive-positioning.md` | Competitive landscape mapping, Porter's Five Forces, April Dunford positioning, differentiation strategies, competitive response playbook |
| `references/market-analysis.md` | TAM/SAM/SOM deep dive, PMF assessment (Sean Ellis test, retention curves), market entry strategy, product lifecycle management |

## Output Contract

The profile using this skill produces artifact pyramids. The response to any caller is the absolute path to `00-index.md`. See `artifact-pyramids` skill for the specification.

## Related Skills

- `artifact-pyramids` — output contract
- `product-methodology` — tactical product management: route validated evidence here for prioritization, specifications, decision logs, and backlog decisions; this skill does not own those delivery-level choices.
- `go-to-market` — CMO methodology (positioning, acquisition, brand, growth modeling)
- `implementation-planning` — work breakdown and dependency ordering
