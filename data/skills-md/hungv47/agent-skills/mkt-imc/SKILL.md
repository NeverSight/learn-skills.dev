---
name: mkt-imc
description: This skill should be used when the user asks to "create an IMC plan", "develop integrated marketing", "build a campaign strategy", "plan a product launch", or mentions IMC, integrated marketing, multi-channel marketing, or campaign planning.
license: MIT
metadata:
  author: hungv47
  version: "7.1.0"
---

# Integrated Marketing Communication (IMC)

*Communicate Track — Step 2 of 4. Turns audience insights into pillars, tested angles, channel assignments, and a phased timeline.*

## Inputs Required
- ICP research from `.agents/mkt/icp-research.md`

## Output
- `.agents/mkt/imc-plan.md`

## Quality Gate
Before delivering, verify:
- [ ] Every pillar traces to a specific pain or aspiration from ICP research (can you quote the VoC source?)
- [ ] Every angle passes ALL three questions: visual? falsifiable? uniquely yours?
- [ ] Every channel assignment cites the habitat map (not guessed)
- [ ] Timeline has specific dates, not just "Phase 1"

## Chain Position
Previous: `mkt-icp-research` | Next: `mkt-content-create`

---

## Before Starting

### Step 0: Product Context
Check for `.agents/mkt/product-context.md`. If available, read for product positioning context.

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `icp-research.md` | mkt-icp-research | **STOP.** "Run mkt-icp-research first — guessed audiences produce weak IMC plans." |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | mkt-copywriting | Product positioning context |
| `prioritized-initiatives.md` | mkt-initiative-prioritize | Aligns content pillars with solution priorities |

Read `.agents/mkt/icp-research.md`. Import personas, pains, habitat maps, VoC quotes.

---

## Step 1: Foundation

**Goals:** What are you trying to achieve? (Awareness / Leads / Sales / Retention) Timeline? Situation? (Launch / Ongoing / Seasonal)

**Core Message:** If the audience remembers one thing, what is it?

**Awareness Levels:** Where is the audience now?

| Stage | They think... | Your job |
|-------|---------------|----------|
| Unaware | "No problem" | Surface it |
| Problem Aware | "Problem, no fix" | Show you understand |
| Solution Aware | "Fixes exist, which?" | Differentiate |
| Product Aware | "I know you, not sure" | Overcome objections |
| Most Aware | "Ready" | Clear CTA |

---

## Step 2: Pillars (from ICP pains)

Extract 3-5 pillars from ICP research:

| Source | Pillar Type | % Content |
|--------|------------|-----------|
| Top Pain Points | Problem | 25-30% |
| Aspirational Identity | Transformation | 30-35% |
| Current Workarounds | Alternative | 20-25% |
| Decision Criteria | Trust | 15-20% |

Each pillar MUST trace to a VoC quote or ICP finding. No made-up pillars.

---

## Step 3: Angles (3 per pillar, tested)

For each pillar, generate 3 angles combining: hook type + awareness stage + emotional trigger.

### The 3-Question Test

Every angle must pass ALL three:

1. **Visual?** Close your eyes — can you see it? ("12 hours lost to status updates" = yes. "Improve productivity" = no.)
2. **Falsifiable?** Can it be proven true or false? ("31 hrs/month in unproductive meetings" = yes. "We help teams succeed" = no.)
3. **Uniquely yours?** Could a competitor use this? ("The dating app designed to be deleted" = only Hinge. "The best project tool" = anyone.)

3 yeses → keep. Any no → rewrite or cut. No exceptions.

See [references/3d-angle-framework.md](references/3d-angle-framework.md) for hook types and generation framework.

---

## Step 4: Channels (from habitat map)

Use the persona habitat maps from ICP research. Don't guess where the audience is — the research already tells you.

Assign one clear angle per channel:

| Platform | Specific Channel | Angle | Why (habitat evidence) |
|----------|-----------------|-------|----------------------|
| [Platform] | [Specific group/account] | "[Angle text]" | [Density + engagement from ICP] |

See [references/channel-strategy.md](references/channel-strategy.md) for channel hierarchy.

---

## Step 5: Phase Timeline

| Phase | Dates | Focus | Content Mix |
|-------|-------|-------|-------------|
| Pre-launch | [start–end] | Build anticipation, educate on problem | 70% Problem, 30% Solution |
| Launch | [start–end] | Drive action, prove value | 30% Problem, 40% Proof, 30% CTA |
| Sustain | [start–ongoing] | Maintain presence, deepen trust | 40% Solution, 30% Proof, 30% Brand |

---

## Artifact Template

```markdown
---
skill: mkt-imc
version: 1
date: [today's date]
status: draft
---

# IMC Plan

**Date:** [today]
**Skill:** mkt-imc
**Core Message:** [one sentence]
**Audience:** [primary persona from ICP]

## Pillars

| # | Pillar | Type | Source (ICP) | % Content |
|---|--------|------|-------------|-----------|
| 1 | [Name] | Problem | VoC: "[quote]" | 30% |
| 2 | [Name] | Transformation | Aspiration: [from ICP] | 30% |
| 3 | [Name] | Trust | Criteria: [from ICP] | 20% |
| 4 | [Name] | Brand | — | 20% |

## Angle Bank

| Pillar | Angle | Hook Type | Stage | 3Q: V/F/U |
|--------|-------|-----------|-------|-----------|
| 1 | "[angle text]" | Data | Problem Aware | Y/Y/Y |
| 1 | "[angle text]" | Contrarian | Solution Aware | Y/Y/Y |
| 1 | "[angle text]" | Story | Unaware | Y/Y/Y |
| 2 | ... | ... | ... | ... |

## Channel Assignments

| Platform | Channel | Angle | Habitat Evidence |
|----------|---------|-------|-----------------|
| Reddit | r/[subreddit] | "[angle]" | Density: H, Engagement: Lurker→Engager |
| LinkedIn | [group/feed] | "[angle]" | Density: M, Engagement: Creator |

## Timeline

| Phase | Dates | Focus | Key Actions |
|-------|-------|-------|-------------|
| Pre-launch | [date–date] | Problem awareness | [Specific actions] |
| Launch | [date–date] | Drive action | [Specific actions] |
| Sustain | [date–ongoing] | Trust + brand | [Specific actions] |

## Next Step

Run `mkt-content-create` to turn angles into production-ready content.

> On re-run: rename existing artifact to `imc-plan.v[N].md` and create new with incremented version.
```

---

## References

- [references/3d-angle-framework.md](references/3d-angle-framework.md) — Hook types × awareness × triggers
- [references/channel-strategy.md](references/channel-strategy.md) — Channel types and fit matrices
- [references/examples.md](references/examples.md) — Worked examples across B2B SaaS, D2C, Creator, Crypto
