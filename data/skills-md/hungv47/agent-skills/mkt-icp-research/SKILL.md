---
name: mkt-icp-research
description: This skill should be used when the user asks to "research my ICP", "understand my target audience", "create customer personas", "analyze customer pain points", "find voice of customer data", or mentions ICP, ideal customer profile, target audience research, persona development, or customer research.
license: MIT
metadata:
  author: hungv47
  version: "2.1.0"
---

# ICP Research & Audience Intelligence

*Communicate Track — Step 1 of 4. Builds deep audience intelligence from real research, not assumptions.*

## Inputs Required
- Product context from `.agents/mkt/product-context.md` (or willingness to answer product questions)

## Output
- `.agents/mkt/icp-research.md`

## Quality Gate
Before delivering, verify:
- [ ] Every VoC quote includes platform name and is from a real source (not agent-generated)
- [ ] Each persona has a habitat map with ≥3 specific channels (not just "Reddit" — which subreddit?)
- [ ] Each emotional driver is traced to ≥2 specific quotes
- [ ] Decision psychology section names specific cognitive biases and objections (not generic "they need trust")

## Chain Position
Previous: none (or any skill needing audience context) | Next: `mkt-imc`

---

## Before Starting

### Step 0: Product Context
Check for `.agents/mkt/product-context.md`. If missing: **INTERVIEW.** Ask the user to describe their product (what, who, problem, differentiator) and save to `.agents/mkt/product-context.md`. Or recommend running `mkt-copywriting` to bootstrap it.

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `product-context.md` | mkt-copywriting | **INTERVIEW.** Ask user to describe product (what, who, problem, differentiator) and save to `.agents/mkt/product-context.md`. Or recommend running `mkt-copywriting`. |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `diagnosis.md` | mkt-diagnosis | Problem context sharpens audience research |
| `root-cause.md` | mkt-root-cause | Focuses research on confirmed issues |

---

## Phase 1: Scope

Ask:
1. **Who are we researching?** (Job role, mindset, community, or use case)
2. **What decisions will this inform?** (Messaging? Channels? Positioning? All three?)
3. **B2C or B2B?** Geography? Specific segments to focus or exclude?

---

## Phase 2: Research

**You MUST use WebSearch for real discussions.** Do NOT generate hypothetical quotes, invented personas, or assumed pain points.

### Search Query Patterns

Use these specific queries. Adapt [topic] to the product/audience:

| Goal | Query Pattern |
|------|--------------|
| Find communities | `site:reddit.com "[topic]" subreddit` |
| Find pain points | `site:reddit.com "[topic]" frustrated OR struggling OR hate` |
| Find reviews | `site:g2.com "[product category]" OR site:capterra.com "[product category]"` |
| Find discussions | `"[topic]" forum OR community best OR worst` |
| Find Twitter takes | `site:twitter.com "[topic]" thread` |
| Find decision criteria | `"[product category]" vs OR alternative OR switch from` |
| Find objections | `"[product/competitor]" not worth OR overpriced OR disappointing` |

### Multi-Platform Coverage

Search ≥4 of these categories:

| Category | Where | What to Extract |
|----------|-------|----------------|
| Communities | Reddit, Facebook Groups, LinkedIn Groups | Pain expressions, solution attempts |
| Social | Twitter/X, TikTok | Real-time frustrations, opinions |
| Reviews | G2, Capterra, App Store, Amazon | Feature complaints, switching reasons |
| Content | YouTube comments, Quora | Questions asked, knowledge gaps |
| Professional | Discord, Slack communities, industry forums | Unfiltered opinions, workflow details |

### VoC Quality Criteria

A **good quote** has:
- Emotional intensity (frustration, excitement, relief — not neutral)
- Specificity (mentions a specific tool, workflow, number, or scenario)
- Recency (within last 12 months)
- Relevance to the product category

A **bad quote** is:
- Generic ("I wish there was a better way")
- Old (2+ years, industry may have shifted)
- From a seller/marketer, not a real user
- A one-word reaction with no context

Collect 3 quotes per pain category. Stop when patterns repeat.

### Pain Analysis (3 Levels)

| Level | What | Where to Find |
|-------|------|--------------|
| **Surface** | What they openly complain about | Public forums, review sites |
| **Hidden** | What they say anonymously | Reddit throwaways, anonymous reviews |
| **Emotional** | Identity threats, status anxiety, fear | Language intensity, desperation indicators |

### MANDATORY: Habitat Mapping

For every platform where you find audience activity, document specifically:

| Platform | Specific Community | Density | Engagement Type | Role |
|----------|-------------------|---------|----------------|------|
| Reddit | r/[specific subreddit] | H/M/L | Lurker/Engager/Creator | Discovery/Trust/Conversion |

Not "Reddit" — which subreddit. Not "LinkedIn" — which group or content type.

See [references/habitat-mapping.md](references/habitat-mapping.md) for density definitions.

### Decision Psychology

Document:
- **Trigger:** What event makes them seek solutions?
- **Research behavior:** Where they go first, second, third
- **Cognitive biases:** Which are strongest? (Loss aversion? Social proof? Authority?)
- **Top 3 objections:** What stops them from buying? What's the psychological root of each?
- **Trust signals:** Who/what do they trust? What creates instant distrust?

---

## Phase 3: Synthesize

### 2 Personas (max)

For each persona, provide ALL of:
- **Demographics:** Age range, role, industry, company size
- **Pain Profile:** Top 3 pains with triggers, impact, and quotes
- **Decision Psychology:** Research behavior, biases, objections + roots
- **Habitat Map:** ≥3 specific channels with density and engagement type
- **VoC Quotes:** 3-5 most revealing, with platform attribution

### Top 3 Emotional Drivers
Core psychological motivations. Each traced to ≥2 specific quotes.

### Red Flags
Language or positioning that triggers instant skepticism for this audience.

---

## Artifact Template

```markdown
---
skill: mkt-icp-research
version: 1
date: [today's date]
status: draft
---

# ICP Research

**Date:** [today]
**Skill:** mkt-icp-research
**Product:** [from product-context.md]

## Persona 1: [Name/Archetype]

**Demographics:** [Age, role, industry, company size]

### Pain Profile
1. **[Pain name]** — [description]
   - Trigger: [what causes acute pain]
   - Impact: [daily/financial/professional]
   - Quote: "[exact quote]" — [Platform, context]
   - Quote: "[exact quote]" — [Platform, context]

2. **[Pain name]** — [description]
   [Same format]

3. **[Pain name]** — [description]
   [Same format]

### Decision Psychology
- **Trigger:** [what event starts their search]
- **Research path:** [where they go 1st → 2nd → 3rd]
- **Key biases:** [which cognitive biases are strongest]
- **Objections:** (1) [objection] — root: [psychological reason]. (2) [objection] — root: [reason]. (3) [objection] — root: [reason].
- **Trust signals:** [what they trust]
- **Distrust triggers:** [what kills credibility]

### Habitat Map
| Platform | Community | Density | Engagement | Role |
|----------|-----------|---------|-----------|------|
| [Specific] | [Specific] | H/M/L | [Type] | [Role] |

## Persona 2: [Name/Archetype]
[Same format]

## Top 3 Emotional Drivers
1. **[Driver]** — [explanation]. Quotes: "[quote 1]" ([source]), "[quote 2]" ([source])
2. **[Driver]** — [explanation]. Quotes: ...
3. **[Driver]** — [explanation]. Quotes: ...

## Red Flags
- [Language/positioning that triggers skepticism and why]

## Next Step
Run `mkt-imc` to turn these insights into a communication plan.

> On re-run: rename existing artifact to `icp-research.v[N].md` and create new with incremented version.
```

---

## References

- [references/habitat-mapping.md](references/habitat-mapping.md) — Density definitions, cross-persona analysis
- [references/icp-to-imc-handoff.md](references/icp-to-imc-handoff.md) — How to package outputs for IMC
- [references/voice-of-customer.md](references/voice-of-customer.md) — VoC collection patterns
