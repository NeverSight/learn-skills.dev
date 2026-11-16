---
name: iblai-marketing-ab-test-setup
description: When the user wants to plan, design, or implement an A/B test or experiment, or build a growth experimentation program. Also use when the user mentions "A/B test," "split test," "experiment," "test this change," "variant copy," "multivariate test," "hypothesis," "should I test this," "which version is better," "test two versions," "statistical significance," "how long should I run this test," "growth experiments," "experiment velocity," "experiment backlog," "ICE score," "experimentation program," or "experiment playbook." Use this whenever someone is comparing two approaches and wants to measure which performs better, or when they want to build a systematic experimentation practice. For tracking implementation, see iblai-marketing-analytics-tracking. For page-level conversion optimization, see iblai-marketing-page-cro.
globs:
alwaysApply: false
metadata:
  version: 1.2.0
---

# /iblai-marketing-ab-test-setup

Design and run A/B tests that produce statistically valid, actionable results.
Use this skill to scope a single experiment or stand up a continuous growth
experimentation program.

## Step 0: Context Check

Read `.agents/product-marketing-context.md` (or `.claude/product-marketing-context.md`
on older setups) first. Only ask for what isn't already there.

You need three things before designing a test:

1. **Test context** — what change is on the table, and why.
2. **Baseline** — current conversion rate and traffic volume.
3. **Constraints** — tooling, timeline, technical complexity.

---

## Core Principles

1. **Start with a hypothesis.** Not "let's see what happens." A specific prediction backed by reasoning or data.
2. **Test one thing.** One variable per test, or you won't know what moved the needle.
3. **Be statistically rigorous.** Pre-commit to sample size. Do NOT peek and stop early.
4. **Measure what matters.** One primary metric tied to business value, plus secondary and guardrail metrics.

---

## Hypothesis Framework

### Structure

```
Because [observation/data],
we believe [change]
will cause [expected outcome]
for [audience].
We'll know this is true when [metrics].
```

### Example

**Weak**: "Changing the button color might increase clicks."

**Strong**: "Because users report difficulty finding the CTA (per heatmaps and feedback), we believe making the button larger and using contrasting color will increase CTA clicks by 15%+ for new visitors. We'll measure click-through rate from page view to signup start."

---

## Test Types

| Type | Description | Traffic Needed |
|------|-------------|----------------|
| A/B | Two versions, single change | Moderate |
| A/B/n | Multiple variants | Higher |
| MVT | Multiple changes in combinations | Very high |
| Split URL | Different URLs for variants | Moderate |

---

## Sample Size

### Quick Reference

| Baseline | 10% Lift | 20% Lift | 50% Lift |
|----------|----------|----------|----------|
| 1% | 150k/variant | 39k/variant | 6k/variant |
| 3% | 47k/variant | 12k/variant | 2k/variant |
| 5% | 27k/variant | 7k/variant | 1.2k/variant |
| 10% | 12k/variant | 3k/variant | 550/variant |

**Calculators:**
- [Evan Miller's](https://www.evanmiller.org/ab-testing/sample-size.html)
- [Optimizely's](https://www.optimizely.com/sample-size-calculator/)

For detailed sample-size tables and duration math, see [references/sample-size-guide.md](references/sample-size-guide.md).

---

## Metrics

| Layer | Purpose |
|-------|---------|
| **Primary** | Single metric tied to the hypothesis. Calls the test. |
| **Secondary** | Explains *why* / *how* the change worked. |
| **Guardrail** | Things that must not get worse. Hard stop if they do. |

### Example: Pricing Page Test

- **Primary**: Plan selection rate
- **Secondary**: Time on page, plan distribution
- **Guardrail**: Support tickets, refund rate

---

## Designing Variants

### What to Vary

| Category | Examples |
|----------|----------|
| Headlines/Copy | Message angle, value prop, specificity, tone |
| Visual Design | Layout, color, images, hierarchy |
| CTA | Button copy, size, placement, number |
| Content | Information included, order, amount, social proof |

Make one meaningful change. Bold enough to detect; faithful to the hypothesis.

---

## Traffic Allocation

| Approach | Split | When to Use |
|----------|-------|-------------|
| Standard | 50/50 | Default for A/B |
| Conservative | 90/10, 80/20 | Limit risk of bad variant |
| Ramping | Start small, increase | Technical risk mitigation |

Hold users to the same variant on return. Spread exposure evenly across time-of-day and day-of-week.

---

## Implementation

### Client-Side

JavaScript mutates the page after load. Fast to ship; risks flicker. Tools: PostHog, Optimizely, VWO.

### Server-Side

Variant resolved before render. No flicker, requires dev work. Tools: PostHog, LaunchDarkly, Split.

---

## Running the Test

### Pre-Launch Checklist

- [ ] Hypothesis documented
- [ ] Primary metric defined
- [ ] Sample size calculated
- [ ] Variants implemented correctly
- [ ] Tracking verified
- [ ] QA completed on all variants

### During the Test

**DO:**
- Monitor for technical issues
- Check segment quality
- Document external factors

**Do NOT:**
- Peek at results and stop early
- Modify variants mid-flight
- Add new traffic sources mid-test

### The Peeking Problem

Looking at results before reaching sample size and stopping early produces false positives. Pre-commit to sample size and trust the process.

---

## Analyzing Results

### Statistical Significance

- 95% confidence = p-value < 0.05
- Means <5% chance the result is random
- Not a guarantee — just a threshold

### Analysis Checklist

1. **Reach sample size?** If not, the result is preliminary.
2. **Statistically significant?** Check confidence intervals.
3. **Effect size meaningful?** Compare to MDE; project the business impact.
4. **Secondary metrics consistent?** Do they support the primary?
5. **Guardrail concerns?** Anything regress?
6. **Segment differences?** Mobile vs. desktop? New vs. returning?

### Interpreting Results

| Result | Conclusion |
|--------|------------|
| Significant winner | Implement variant |
| Significant loser | Keep control, learn why |
| No significant difference | Need more traffic or bolder test |
| Mixed signals | Dig deeper, segment |

---

## Documentation

Document every test with:

- Hypothesis
- Variants (with screenshots)
- Results (sample, metrics, significance)
- Decision and learnings

Templates: see [references/test-templates.md](references/test-templates.md).

---

## Growth Experimentation Program

One test is data. A continuous program is a compounding asset. Run experiments as an ongoing growth engine — not one-offs.

### The Experiment Loop

```
1. Generate hypotheses (from data, research, competitors, customer feedback)
2. Prioritize with ICE scoring
3. Design and run the test
4. Analyze results with statistical rigor
5. Promote winners to a playbook
6. Generate new hypotheses from learnings
→ Repeat
```

### Hypothesis Sources

Feed the backlog from multiple places:

| Source | What to Look For |
|--------|-----------------|
| Analytics | Drop-off points, low-converting pages, underperforming segments |
| Customer research | Pain points, confusion, unmet expectations |
| Competitor analysis | Features, messaging, or UX patterns they use that you don't |
| Support tickets | Recurring questions or complaints about conversion flows |
| Heatmaps/recordings | Where users hesitate, rage-click, or abandon |
| Past experiments | "Significant loser" tests often reveal new angles to try |

### ICE Prioritization

Score each hypothesis 1-10:

| Dimension | Question |
|-----------|----------|
| **Impact** | If this works, how much will it move the primary metric? |
| **Confidence** | How sure are we this will work? (Based on data, not gut.) |
| **Ease** | How fast and cheap can we ship and measure this? |

**ICE Score** = (Impact + Confidence + Ease) / 3

Run highest scorers first. Re-score monthly as context shifts.

### Experiment Velocity

Treat experimentation rate as a leading indicator of growth:

| Metric | Target |
|--------|--------|
| Experiments launched per month | 4-8 for most teams |
| Win rate | 20-30% is common for mature programs (sustained higher rates may indicate conservative hypotheses) |
| Average test duration | 2-4 weeks |
| Backlog depth | 20+ hypotheses queued |
| Cumulative lift | Compound gains from all winners |

### The Experiment Playbook

When a test wins, document the pattern — not just the implementation:

```
## [Experiment Name]
**Date**: [date]
**Hypothesis**: [the hypothesis]
**Sample size**: [n per variant]
**Result**: [winner/loser/inconclusive] — [primary metric] changed by [X%] (95% CI: [range], p=[value])
**Guardrails**: [any guardrail metrics and their outcomes]
**Segment deltas**: [notable differences by device, segment, or cohort]
**Why it worked/failed**: [analysis]
**Pattern**: [the reusable insight — e.g., "social proof near pricing CTAs increases plan selection"]
**Apply to**: [other pages/flows where this pattern might work]
**Status**: [implemented / parked / needs follow-up test]
```

Over time the playbook becomes a library of growth patterns proven against your audience.

### Cadence

**Weekly (30 min)** — Review running experiments for technical issues and guardrail breaches. Do NOT call winners early. Do stop tests where guardrails are significantly negative.

**Bi-weekly** — Conclude completed experiments. Analyze, update playbook, launch next from backlog.

**Monthly (1 hour)** — Review velocity, win rate, cumulative lift. Refill the hypothesis backlog. Re-prioritize with ICE.

**Quarterly** — Audit the playbook. Which patterns have been applied broadly? Which winners haven't been scaled? Which areas of the funnel are under-tested?

---

## Common Mistakes

### Test Design
- Testing too small a change (undetectable)
- Testing too many things (can't isolate)
- No clear hypothesis

### Execution
- Stopping early
- Changing things mid-test
- Skipping implementation QA

### Analysis
- Ignoring confidence intervals
- Cherry-picking segments
- Over-interpreting inconclusive results

---

## Task-Specific Questions

1. What's your current conversion rate?
2. How much traffic does this page get?
3. What change are you considering and why?
4. What's the smallest improvement worth detecting?
5. What tools do you have for testing?
6. Have you tested this area before?

---

## Related Skills

- **iblai-marketing-page-cro**: For generating test ideas based on CRO principles
- **iblai-marketing-analytics-tracking**: For setting up test measurement
- **iblai-marketing-copywriting**: For creating variant copy
