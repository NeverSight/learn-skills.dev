---
name: mkt-funnel-planner
description: This skill should be used when the user asks to "set targets", "plan a funnel", "create OKRs", "set quarterly goals", "benchmark metrics", "validate targets", or mentions conversion funnel, funnel metrics, OKRs, or target-setting.
license: MIT
metadata:
  author: hungv47
  version: "3.1.0"
---

# Funnel Planner — Target Setting

*Solution Track — Step 3 of 4. Sets data-driven targets for each prioritized initiative.*

## Inputs Required
- Prioritized initiatives from `.agents/mkt/prioritized-initiatives.md` (preferred)
- OR: A business with metrics that need targets

## Output
- `.agents/mkt/targets.md`

## Quality Gate
Before delivering, verify:
- [ ] Every target has a numeric baseline (zero "TBD" values)
- [ ] Every target cites a justification: historical data, benchmark, or calculated improvement factor
- [ ] 70% test passes: hitting 70% of each target is still valuable
- [ ] LTV:CAC ≥ 3:1 (if acquisition targets involved) — or flagged as unhealthy

## Chain Position
Previous: `mkt-initiative-prioritize` | Next: `mkt-experiment`

---

## Before Starting

### Step 0: Product Context
Check for `.agents/mkt/product-context.md`. If missing: **INTERVIEW.** Ask the user 8 product questions (what, who, problem, differentiator, proof points, pricing, objections, voice) and save to `.agents/mkt/product-context.md`. Or recommend running `mkt-copywriting` to bootstrap it.

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `prioritized-initiatives.md` | mkt-initiative-prioritize | **INTERVIEW.** Ask what initiatives to set targets for. |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | mkt-copywriting | Business model context for benchmark selection |

Read `.agents/mkt/prioritized-initiatives.md` if it exists — set a target for each "Proceed" initiative. If it doesn't exist, interview the user:
- What business type? (SaaS, e-commerce, B2B services, etc.)
- What stage? (Pre-launch, early traction, growth, mature)
- What metrics need targets?

---

## Step 1: Choose Funnel Model

| Model | Best For | Stages |
|-------|----------|--------|
| **AARRR** | SaaS, apps | Acquisition → Activation → Retention → Revenue → Referral |
| **AIDA** | E-commerce, D2C | Awareness → Interest → Desire → Action |
| **TOFU-MOFU-BOFU** | B2B, long sales | Top → Middle → Bottom |

See [references/funnel-models.md](references/funnel-models.md) for detailed stage definitions.

---

## Step 2: Collect Baselines

Baselines are non-negotiable. For each metric, get the current number.

If user lacks data, use WebSearch:
- `"[industry] [metric] benchmark [year]"` (e.g., "B2B SaaS trial conversion benchmark 2025")
- `"[business type] average [metric] by stage"` (e.g., "Series A SaaS average churn rate")
- `"[metric] good vs bad [industry]"` (e.g., "email open rate good vs bad SaaS")

See [references/benchmarks.md](references/benchmarks.md) for reference ranges. Note: benchmarks are starting points, not guarantees.

---

## Step 3: Set Targets

For each initiative/metric:

| Scenario | Improvement Factor |
|----------|-------------------|
| No optimization yet | 20-30% lift |
| Basic optimization done | 10-15% |
| Mature funnel | 5-10% |
| Major redesign or fix | 30-50% |

**LTV:CAC sanity check** (for acquisition targets):
- LTV:CAC should be ≥ 3:1, ideally 5:1
- Payback < 12 months (SMB) or < 18 months (mid-market)
- If targets imply unhealthy economics, flag it explicitly

See [references/unit-economics.md](references/unit-economics.md) for formulas.

---

## Step 4: Validate

### Anti-Pattern Check

| Anti-Pattern | Detection |
|--------------|-----------|
| **Vanity Metric** | Doesn't connect to revenue → find the revenue-connected metric |
| **Sandbagging** | 100% confidence, zero stretch → add 30-50% |
| **Moonshot** | 10x improvement, no plan → work backwards from realistic |
| **Orphan Target** | Owner is "the team" → assign a person |
| **Input Trap** | Measuring activities ("publish 4 posts") → measure the output ("organic signups") |

See [references/anti-patterns.md](references/anti-patterns.md) for detailed detection.

### Stress Tests

1. **Revenue test:** If we hit this but revenue doesn't move, was it worth it?
2. **70% test:** If we hit 70%, is that still valuable?
3. **Ownership test:** Who owns this? What are they NOT doing to focus on it?
4. **Measurement test:** Can we check this weekly, or only at period end?

See [references/stress-tests.md](references/stress-tests.md) for stage-specific questions.

---

## Artifact Template

On re-run: rename existing artifact to `targets.v[N].md` and create new with incremented version.

```markdown
---
skill: mkt-funnel-planner
version: 1
date: {{today}}
status: draft
---

# Targets

**Funnel Model:** [AARRR / AIDA / TOFU-MOFU-BOFU]

## Target Table

| Initiative | Metric | Baseline | Benchmark | Target | Justification | Owner |
|-----------|--------|----------|-----------|--------|---------------|-------|
| [Name] | [Metric] | [Current] | [Industry ref] | [Goal] | [Why achievable] | [Person] |

## Validation

### Anti-Patterns: [None detected / List any found + fixes]
### 70% Test: [Pass/fail per target]
### LTV:CAC Check: [Ratio] — [Healthy / Flag]

## Next Step

Run `mkt-experiment` to design minimum viable tests before full rollout.
```

---

## Worked Example

```markdown
# Targets

**Date:** 2026-03-13
**Skill:** mkt-funnel-planner
**Funnel Model:** AARRR

## Target Table

| Initiative | Metric | Baseline | Benchmark | Target | Justification | Owner |
|-----------|--------|----------|-----------|--------|---------------|-------|
| Restore Paid Targeting | Paid visitor signup rate | 1.2% | 3-5% (B2B SaaS median) | 3.0% | Was 3.5% before targeting change; conservative recovery with lookalike | Sarah |
| Restore Social Proof | Homepage bounce rate | 52% | 30-40% (B2B SaaS) | 40% | Old homepage was 35%; restoring trust signals should recover most of gap | James |
| Overall | Weekly signups | 200 | — | 300 | Combined effect: paid fix (150 → 225 from paid) + bounce fix (all sources) | Sarah (owner) |

## Validation

### Anti-Patterns: None detected. All targets have baselines, single owners, revenue connection.
### 70% Test: Hitting 70% (2.5% paid rate, 43% bounce, 270 signups) still represents meaningful recovery from 200.
### LTV:CAC Check: Current CAC $120, LTV $1,800 → 15:1 ratio. Healthy even if CAC rises 50%.

## Next Step

Run `mkt-experiment` to design A/B test for paid targeting and before-after for social proof restoration.
```

---

## References

| Reference | Use For |
|-----------|---------|
| [funnel-models.md](references/funnel-models.md) | Stage definitions, model selection |
| [benchmarks.md](references/benchmarks.md) | Industry benchmarks by stage |
| [anti-patterns.md](references/anti-patterns.md) | Target-setting pitfalls |
| [stress-tests.md](references/stress-tests.md) | Target validation questions |
| [unit-economics.md](references/unit-economics.md) | LTV:CAC, payback formulas |
