---
name: org-design
description: Design organizational topology, talent, rewards, culture, and health decisions with explicit decision rights and validation. Do not use for legal advice, project delivery planning, financial modeling, or technology implementation.
  reporting structures), talent strategy (make-vs-buy, skill taxonomies, succession
  planning), compensation frameworks (market benchmarking, equity design, leveling),
  culture architecture (values codification, rituals, psychological safety), organizational
  health metrics (eNPS, retention risk, engagement surveys), DEI strategy (inclusive
  design, equitable systems, belonging).
license: MIT
metadata:
  tags: org-design, chro, hr, talent-strategy, compensation, culture, organizational-health,
    dei, succession-planning
  source_repo: https://github.com/magnus919/hermes-profiles
---

# Organizational Design — CHRO Methodology

CHRO-level methodology for organizational design, talent strategy, compensation, culture, and organizational health. This skill provides the frameworks and reference material for a chief human resources officer profile.

## When to Load

| Trigger | What's Needed |
|---------|---------------|
| Design organizational structure | `references/organizational-design.md` — team topologies, span of control, reporting structures, health metrics |
| Develop talent strategy | `references/talent-strategy.md` — make-vs-buy, skill taxonomies, succession planning, 9-box grid |
| Build compensation frameworks | `references/compensation-frameworks.md` — market benchmarking, equity design, leveling bands, variable pay |
| Define culture and values | `references/culture-architecture.md` — values codification, rituals, psychological safety, eNPS, DEI |
| Assess org health | `references/culture-architecture.md` — engagement drivers, retention indicators, DEI maturity |
| Plan succession pipeline | `references/talent-strategy.md` — pipeline coverage, 9-box grid, talent review cadence |

## Loading Order

```text
skill_view('org-design')
# Then domain-specific references:
skill_view('org-design', file_path='references/organizational-design.md')
skill_view('org-design', file_path='references/talent-strategy.md')
skill_view('org-design', file_path='references/compensation-frameworks.md')
skill_view('org-design', file_path='references/culture-architecture.md')
```

## Reference Files

| Reference | Purpose |
|-----------|---------|
| `references/organizational-design.md` | Team topologies (stream-aligned, enabling, complicated-subsystem, platform), span of control, reporting structures (functional, matrix, stream-aligned), organizational health metrics |
| `references/talent-strategy.md` | Make-vs-buy decision matrix, skill taxonomies, succession planning (pipeline coverage, 9-box grid), talent review cadence, retention risk indicators |
| `references/compensation-frameworks.md` | Market benchmarking (Radford, Levels.fyi), equity instruments (ISO, NSO, RSU), grant benchmarks by level, vesting schedules, leveling bands, variable pay, comp review cadence |
| `references/culture-architecture.md` | Values codification template, rituals cadence, psychological safety (4 stages, measurement, building), organizational health metrics (eNPS benchmarks, engagement drivers, retention indicators), DEI strategy and maturity model |
| `references/decision-workflow.md` | Bounded topology/talent/reward/culture decisions, worked example, reusable record, and owner routing matrix |

## Output Contract

The profile using this skill produces artifact pyramids. The response to any caller is the absolute path to `00-index.md`. See `artifact-pyramids` skill for the specification.

## Decision Workflow

For topology, talent, reward, or culture choices, load `references/decision-workflow.md`. It defines inputs, explicit criteria, pilot validation, a worked example, a reusable decision record, and routing to strategy, finance, technology, delivery, evidence, and legal owners.

## Related Skills

- `artifact-pyramids` — output contract
- `implementation-planning` — team-level work breakdown
- `product-strategy` — CPO methodology (complementary for org design around product teams)
