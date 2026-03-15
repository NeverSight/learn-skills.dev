---
name: mkt-diagnosis
description: This skill should be used when the user asks to "diagnose the problem", "break down the issue", "build a logic tree", "what's causing this", or mentions problem diagnosis, logic trees, MECE decomposition, or structured problem solving. This is the ENTRY POINT for problem analysis — use when no diagnosis exists yet.
license: MIT
metadata:
  author: hungv47
  version: "2.1.0"
---

# Structured Problem Diagnosis

*Problem Track — Step 1 of 3. Defines the problem with numbers and decomposes it into testable parts.*

## Inputs Required
- A problem the user wants diagnosed (metric decline, performance gap, strategic question)

## Output
- `.agents/mkt/diagnosis.md`

## Quality Gate
Before delivering, verify:
- [ ] Problem statement contains two numbers (current state AND target state)
- [ ] Logic tree has 2-3 levels with ≥3 leaf nodes
- [ ] Each leaf is a testable cause (not a restatement like "conversion is low")
- [ ] MECE: fixing one branch doesn't auto-fix another; no cause is missing

## Chain Position
Previous: none | Next: `mkt-hypothesis`

---

## Before Starting

### Step 0: Product Context
Check for `.agents/mkt/product-context.md`. If missing: **INTERVIEW.** Ask the user 8 product questions (what, who, problem, differentiator, proof points, pricing, objections, voice) and save to `.agents/mkt/product-context.md`. Or recommend running `mkt-copywriting` to bootstrap it.

### Required Artifacts
None — this is the entry point for the Problem track.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | mkt-copywriting | Industry context for better tree construction and benchmark selection |

### Problem Interview
If the user describes a vague problem ("things aren't going well", "growth is slow"):
1. Ask for the specific metric and its current value
2. Ask for the target value and who set it
3. If user doesn't know the baseline, use WebSearch: `"[industry] [metric] benchmark [year]"` or `"[business type] average [metric]"`
4. Do NOT proceed until you have at least: metric name + current number + target number

---

## Step 1: Define the Problem

> **[Metric] is [current number] instead of [target number]**

Ask:
1. What metric specifically? (Not "growth" — which metric?)
2. What's the current number?
3. What's the target? Who set it?
4. When did it change? Was there an inflection point?
5. How big is the gap in absolute and relative terms?

---

## Step 2: Build a Logic Tree

### Choose Tree Type

| Type | When | Example Root |
|------|------|-------------|
| **Math Tree** | Metric can be decomposed into formula | Revenue = Traffic × Conversion × AOV |
| **Issue Tree** | Multi-factor, non-mathematical | "Why are customers churning?" |
| **Yes/No Tree** | Binary decision points | "Is the problem supply-side or demand-side?" |

### Build It

1. Put the problem statement at the top
2. Break into 2-4 mutually exclusive categories
3. For each category, break into 2-3 sub-factors
4. Stop at 2-3 levels deep
5. MECE check: Do branches cover everything? Does fixing A auto-fix B? (If yes → overlap, restructure)

**WebSearch directive:** If you need to understand what factors typically drive this metric, search: `"[metric] decomposition" OR "[metric] drivers" OR "what affects [metric]"`

---

## Artifact Template

On re-run: rename existing artifact to `diagnosis.v[N].md` and create new with incremented version.

```markdown
---
skill: mkt-diagnosis
version: 1
date: {{today}}
status: draft
---

# Diagnosis

## Problem Statement

[Metric] is [current] instead of [target], a gap of [X%/X units].
Started: [when]. Inflection point: [if known].

## Logic Tree

[Tree type: Math / Issue / Yes-No]

​```
[Problem statement]
├── [Branch 1]
│   ├── [Leaf 1a]
│   ├── [Leaf 1b]
│   └── [Leaf 1c]
├── [Branch 2]
│   ├── [Leaf 2a]
│   └── [Leaf 2b]
└── [Branch 3]
    ├── [Leaf 3a]
    └── [Leaf 3b]
​```

## MECE Check

- Mutually Exclusive: [confirm no overlaps]
- Collectively Exhaustive: [confirm no gaps]

## Next Step

Run `mkt-hypothesis` to form testable hypotheses for each leaf.
```

---

## Worked Example

**User:** "Our signups are declining."

**Interview:**
- "What's the current signup rate?" → "About 200/week, down from 350/week"
- "When did it start?" → "About 8 weeks ago"
- "Any changes around that time?" → "We launched a new homepage and changed our ad targeting"

**Artifact saved to `.agents/mkt/diagnosis.md`:**

```markdown
# Diagnosis

**Date:** 2026-03-13
**Skill:** mkt-diagnosis

## Problem Statement

Weekly signups are 200 instead of 350, a gap of 43%.
Started: ~8 weeks ago. Inflection point: homepage redesign + ad targeting change.

## Logic Tree

Math Tree

​```
Weekly signups declining (200 → 350 target)
├── Traffic volume declining (fewer people arriving)
│   ├── Paid traffic: ad targeting change reduced volume/quality
│   ├── Organic traffic: SEO impact from homepage redesign
│   └── Referral/direct: brand or word-of-mouth decline
├── Conversion rate declining (same traffic, fewer signups)
│   ├── Homepage redesign reduced clarity/trust
│   ├── Signup flow friction increased
│   └── Value proposition no longer resonates
└── Measurement change (signups happening but not counted)
    ├── Tracking code broken on new homepage
    └── Attribution model changed
​```

## MECE Check

- Mutually Exclusive: Traffic volume vs. conversion rate vs. measurement are independent
- Collectively Exhaustive: All signup decline must come from fewer visitors, lower conversion, or miscounting

## Next Step

Run `mkt-hypothesis` to form testable hypotheses for each leaf.
```

---

## References

- [references/watanabe-framework.md](references/watanabe-framework.md) — MECE principles and tree-building
- [references/logic-tree-examples.md](references/logic-tree-examples.md) — 4 worked examples (SaaS churn, e-commerce, content ROI, B2B pipeline)
