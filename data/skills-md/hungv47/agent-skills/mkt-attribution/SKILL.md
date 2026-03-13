---
name: mkt-attribution
description: This skill should be used when the user asks to "map attribution", "connect initiatives to KPIs", "trace content to goals", "audit coverage", "check KPI alignment", "find orphan initiatives", or mentions attribution mapping, KPI hierarchy, coverage analysis, or initiative alignment.
license: MIT
metadata:
  author: hungv47
  version: "2.1.0"
---

# Attribution Mapping

*Communicate Track — Step 4 of 4. Validates the system — every initiative and content piece connects to a KPI, with action items for every gap.*

## Inputs Required
- KPIs from `.agents/mkt/targets.md` or existing OKRs
- Initiatives from `.agents/mkt/prioritized-initiatives.md`
- Content from `.agents/mkt/imc-plan.md` or `.agents/mkt/content/`

## Output
- `.agents/mkt/attribution.md`

## Quality Gate
Before delivering, verify:
- [ ] Every KPI has ≥1 initiative mapped or is explicitly flagged with an action item
- [ ] Every initiative maps to a KPI or has a "Kill" recommendation with reason
- [ ] Every recommendation is a verb (Create / Kill / Rebalance / Test) — not an observation ("this seems low")
- [ ] Review date is set (~4 weeks from today)

## Chain Position
Previous: `mkt-content-create` | Next: Monthly review (re-run this skill)

---

## Before Starting

### Step 0: Product Context
Check for `.agents/mkt/product-context.md`. If available, read for product context.

### Required Artifacts
None — can build from scratch by interviewing.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `targets.md` | mkt-funnel-planner | KPI baselines |
| `prioritized-initiatives.md` | mkt-initiative-prioritize | Initiative list to map |
| `imc-plan.md` | mkt-imc | Content plan to audit |
| Previous `attribution.md` | mkt-attribution | Check progress on prior action items |

Read upstream files if they exist: `.agents/mkt/targets.md`, `.agents/mkt/prioritized-initiatives.md`, `.agents/mkt/imc-plan.md`. If previous `.agents/mkt/attribution.md` exists, read it — check progress on prior action items before building new map.

If no upstream files exist, build from scratch by interviewing:
1. "What's your North Star metric?"
2. "What are your 3-5 primary KPIs?"
3. "What initiatives are you running or planning?"
4. "What content are you producing?"

---

## Step 1: KPI Hierarchy

```
North Star: [metric] — [current] → [target]
├── KPI 1: [metric] — [current] → [target] — Owner: [person]
├── KPI 2: [metric] — [current] → [target] — Owner: [person]
└── KPI 3: [metric] — [current] → [target] — Owner: [person]
```

---

## Step 2: Map Initiatives → KPIs

| Initiative | Primary KPI | Contribution | Confidence |
|------------|-------------|-------------|------------|
| [Name] | [KPI] | ~X% of target | H/M/L |

**Unknown contributions:** If you can't estimate contribution, mark "Unknown" and add action item: "Run `mkt-experiment` to measure actual impact."

### Flag Orphans

| Orphan Initiative | Action |
|-------------------|--------|
| [Name] | **Kill** — no KPI connection / **Reframe** — target [KPI] / **Test** — run experiment |

---

## Step 3: Map Content → Initiatives

| Content | Initiative | Type | Channel |
|---------|-----------|------|---------|
| [Piece] | [Initiative] | Reach / Trust / Conversion | [Channel] |

### Flag Orphan Content

| Orphan Content | Action |
|----------------|--------|
| [Piece] | **Assign** to [initiative] / **Repurpose** for [initiative] / **Sunset** |

---

## Step 4: Gap Analysis → Action Items

This is the core deliverable. Every gap produces a specific action.

| Gap | Action | Owner | Deadline |
|-----|--------|-------|----------|
| [KPI X uncovered] | **Create:** Run `mkt-initiative-generate` targeting this KPI | [Who] | [When] |
| [Initiative Y orphaned] | **Kill:** Archive, remove from roster | [Who] | Now |
| [Content Z unassigned] | **Rebalance:** Redirect to support [initiative] | [Who] | [When] |
| [Contribution unknown] | **Test:** Design experiment via `mkt-experiment` | [Who] | [When] |
| [Stage imbalanced] | **Rebalance:** Shift X% effort from [over] to [under] | [Who] | [When] |

---

## Re-Run Protocol

Attribution maps should be reviewed and refreshed regularly:

1. **Monthly review cycle:** Set review date ~4 weeks from creation
2. **On re-run:**
   - Read previous `.agents/mkt/attribution.md`
   - Check status of each prior action item (Done / In Progress / Blocked / Dropped)
   - Rename previous file to `attribution.v[N].md`
   - Rebuild map with current state
   - Compare: Did action items move the needle? Which KPIs improved?
3. **Escalation:** If same gaps persist across 2+ reviews, escalate from "Rebalance" to "Kill" or "Create"

---

## Artifact Template

```markdown
---
skill: mkt-attribution
version: 1
date: [today's date]
status: draft
---

# Attribution Map

**Date:** [today]
**Skill:** mkt-attribution
**Review date:** [today + 4 weeks]

## KPI Hierarchy

​```
North Star: [metric] — [current] → [target]
├── KPI 1: [metric] — [current] → [target] — Owner: [person]
├── KPI 2: ...
└── KPI 3: ...
​```

## Initiative → KPI Mapping

| Initiative | KPI | Contribution | Confidence |
|------------|-----|-------------|------------|
| ... | ... | ... | ... |

### Orphan Initiatives
| Initiative | Action |
|------------|--------|
| ... | ... |

## Content → Initiative Mapping

| Content | Initiative | Type | Channel |
|---------|-----------|------|---------|
| ... | ... | ... | ... |

### Orphan Content
| Content | Action |
|---------|--------|
| ... | ... |

## Action Items

| # | Gap | Action | Owner | Deadline |
|---|-----|--------|-------|----------|
| 1 | ... | ... | ... | ... |

## Previous Review Progress
[If re-running: status of prior action items]

> On re-run: rename existing artifact to `attribution.v[N].md` and create new with incremented version.
```

---

## Worked Example

```markdown
# Attribution Map

**Date:** 2026-03-13
**Skill:** mkt-attribution
**Review date:** 2026-04-10

## KPI Hierarchy

​```
North Star: Weekly Signups — 200 → 350
├── KPI 1: Paid signup rate — 1.2% → 3.0% — Owner: Sarah
├── KPI 2: Homepage bounce rate — 52% → 40% — Owner: James
└── KPI 3: Organic signups — 80/wk → 120/wk — Owner: (unassigned)
​```

## Initiative → KPI Mapping

| Initiative | KPI | Contribution | Confidence |
|------------|-----|-------------|------------|
| Restore Paid Targeting | Paid signup rate | ~55% of total gap | H |
| Restore Social Proof | Homepage bounce | ~35% of total gap | M |

### Orphan Initiatives
None — both initiatives map to KPIs.

## Content → Initiative Mapping

| Content | Initiative | Type | Channel |
|---------|-----------|------|---------|
| Status Update Carousel | (none — brand awareness) | Reach | LinkedIn |

### Orphan Content
| Content | Action |
|---------|--------|
| Status Update Carousel | **Rebalance:** Add CTA linking to product page, reframe as supporting Paid Targeting initiative |

## Action Items

| # | Gap | Action | Owner | Deadline |
|---|-----|--------|-------|----------|
| 1 | KPI 3 (organic) uncovered | **Create:** Run `mkt-diagnosis` on organic traffic stagnation | James | 2026-03-20 |
| 2 | KPI 3 has no owner | **Assign:** Name an owner for organic signups KPI | Marketing lead | 2026-03-14 |
| 3 | Carousel content orphaned | **Rebalance:** Add product CTA to carousel, track as Paid Targeting support | Content lead | 2026-03-17 |
```

---

## References

- [references/attribution-examples.md](references/attribution-examples.md) — Worked examples across business types
