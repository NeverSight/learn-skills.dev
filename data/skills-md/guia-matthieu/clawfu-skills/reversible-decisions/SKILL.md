---
name: reversible-decisions
description: "Know when to move fast and when to move carefully. Master Jeff Bezos' framework for distinguishing high-stakes irreversible decisions from low-stakes reversible ones. Use when: **Prioritizing decisions** to know where to invest time; **Team empowerment** to understand what to delegate vs. escalate; **Avoiding analysis paralysis** on decisions that don't matter; **Risk management** to identify where caution is truly warranted; **Speed vs. thoroughness** trade-offs in any context"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Reversible Decisions (Type 1 vs. Type 2)

> Know when to move fast and when to move carefully. Master Jeff Bezos' framework for distinguishing high-stakes irreversible decisions from low-stakes reversible ones.

## When to Use This Skill

- **Prioritizing decisions** to know where to invest time
- **Team empowerment** to understand what to delegate vs. escalate
- **Avoiding analysis paralysis** on decisions that don't matter
- **Risk management** to identify where caution is truly warranted
- **Speed vs. thoroughness** trade-offs in any context
- **Building decision-making culture** in organizations

## Methodology Foundation

| Aspect | Details |
|--------|---------|
| **Source** | Jeff Bezos - Amazon shareholder letters (2015-2016) |
| **Core Principle** | "Some decisions are irreversible and consequential (Type 1). Most are reversible and low-consequence (Type 2). Use the right process for each." |
| **Why This Matters** | Most people treat all decisions like Type 1—slow, deliberate, requiring full information. This leads to paralysis and missed opportunities. The best decision-makers move fast on Type 2 and slow on Type 1. |


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures content frameworks | Final messaging |
| Suggests persuasion techniques | Brand voice |
| Creates draft variations | Version selection |
| Identifies optimization opportunities | Publication timing |
| Analyzes competitor approaches | Strategic direction |

## What This Skill Does

1. **Classifies decisions** - Is this Type 1 or Type 2?
2. **Calibrates process to stakes** - Right speed for right decision
3. **Enables delegation** - Type 2 can be pushed down
4. **Prevents over-analysis** - Stop treating reversible decisions as irreversible
5. **Improves organizational speed** - Teams move faster on the right things
6. **Reduces decision fatigue** - Don't waste energy on low-stakes choices

## How to Use

### Classify a Decision
```
Help me classify this decision:
[Describe the decision]
Is this Type 1 (irreversible) or Type 2 (reversible)?
What process should I use?
```

### Speed Up Decision-Making
```
I'm spending too much time on [decision].
Apply the Type 1/Type 2 framework to help me move faster.
```

### Build Decision-Making Process
```
Help me design a decision-making framework for my team.
Which decisions should require consensus vs. individual judgment?
```

## Instructions

### Step 1: Understand the Framework

```
## Type 1 vs. Type 2 Decisions

### Bezos' Definition

**Type 1: One-Way Doors**
"Some decisions are consequential and irreversible or nearly irreversible—
one-way doors—and these decisions must be made methodically, carefully,
slowly, with great deliberation and consultation."

**Type 2: Two-Way Doors**
"But most decisions aren't like that—they are changeable, reversible—
they're two-way doors. If you've made a suboptimal Type 2 decision,
you don't have to live with the consequences for that long.
You can reopen the door and go back through."

### The Problem

"As organizations get larger, there seems to be a tendency to use
the heavy-weight Type 1 decision-making process on most decisions,
including many Type 2 decisions. The end result of this is slowness,
unthoughtful risk aversion, failure to experiment sufficiently,
and consequently diminished invention."

### The Solution

"We must resist this tendency."

Type 2 decisions should be made quickly by high-judgment individuals
or small groups. Type 1 decisions require the full deliberative process.
```

---

### Step 2: Classification Framework

```
## How to Classify Decisions

### The Two Questions

**Question 1: Is it reversible?**
Can you undo this decision with reasonable effort and cost?

| Reversibility | Examples |
|---------------|----------|
| **Easily reversible** | Pricing change, A/B test, new feature flag, hire (with trial), campaign |
| **Hard to reverse** | Architecture choice, brand name, key hire (C-level), market exit |
| **Irreversible** | Selling company, shutting down product, firing someone, legal action |

**Question 2: What are the consequences?**
If this decision is wrong, what happens?

| Consequence Level | Examples |
|-------------------|----------|
| **Low** | Internal process change, small experiment, minor feature |
| **Medium** | New product launch, pricing tier, team restructure |
| **High** | Major strategic pivot, large investment, partnership |
| **Existential** | Acquisition, shutdown, bet-the-company move |

### The Matrix

```
                    CONSEQUENCES
                    Low         High
REVERSIBILITY  ┌────────────┬────────────┐
    High       │   TYPE 2   │   TYPE 2   │
    (Easy)     │   (Fast)   │  (Fast w/  │
               │            │  monitoring)│
               ├────────────┼────────────┤
    Low        │   TYPE 2   │   TYPE 1   │
    (Hard)     │  (Careful) │   (Slow)   │
               └────────────┴────────────┘
```

### Quick Classification

**TYPE 2 (Move Fast):**
- Can be undone
- Low/medium consequences
- Learning opportunity
- Failure is recoverable
- Most business decisions

**TYPE 1 (Move Carefully):**
- Can't be undone
- High/existential consequences
- Mistakes are permanent
- One-way door
- ~5-10% of decisions
```

---

### Step 3: Match Process to Type

```
## Decision Process by Type

### Type 2 Process (70% of Decisions)

**Time:** Hours to days (not weeks)
**Who:** Individual or small group with context
**Information:** Good enough, not perfect
**Approval:** None or single level
**Documentation:** Minimal (decision log)

**The Mantra:**
"Disagree and commit" - If you have 70% of the information you wish you had,
make the decision. Waiting for 90% is usually too slow.

**Process:**
1. Identify it's Type 2 (reversible, recoverable)
2. Gather available information quickly
3. Make the call
4. Communicate the decision
5. Monitor and adjust

**Examples:**
- Feature prioritization
- Hiring most roles
- Process changes
- Pricing experiments
- Marketing campaigns
- Internal tools
- Meeting schedules

---

### Type 1 Process (5-10% of Decisions)

**Time:** Weeks to months
**Who:** Senior leadership, broad input
**Information:** As complete as reasonably possible
**Approval:** Multiple stakeholders
**Documentation:** Thorough (rationale, alternatives, risks)

**The Mantra:**
"Measure twice, cut once" - This is permanent. Get it right.

**Process:**
1. Confirm it's Type 1 (irreversible, consequential)
2. Define decision criteria clearly
3. Gather comprehensive information
4. Consider alternatives thoroughly
5. Consult relevant stakeholders
6. Document the reasoning
7. Make the decision
8. Communicate extensively

**Examples:**
- M&A decisions
- Major strategic pivots
- Leadership hires (C-level)
- Market entry/exit
- Large capital allocation
- Shutting down products
- Legal/regulatory choices
```

---

### Step 4: Common Traps

```
## Decision-Making Traps

### Trap 1: Treating Type 2 as Type 1

**Symptom:** Analysis paralysis on small decisions
**Example:** 2-week committee review for a landing page change
**Problem:** Slows innovation, frustrates teams, misses opportunities
**Fix:** Ask "What's the worst case if we're wrong? Can we fix it?"

### Trap 2: Treating Type 1 as Type 2

**Symptom:** Moving too fast on irreversible choices
**Example:** Acquiring a company in 2 weeks
**Problem:** Permanent mistakes, existential risk
**Fix:** Ask "If this goes wrong, can we undo it?"

### Trap 3: Requiring Consensus on Type 2

**Symptom:** Everyone needs to agree before action
**Example:** 10-person meeting to decide email copy
**Problem:** Slowest person becomes bottleneck
**Fix:** Empower individuals to make Type 2 calls

### Trap 4: Not Recognizing Type 1 in Disguise

**Symptom:** Missing irreversibility hidden in details
**Example:** "Small" technical choice that creates years of debt
**Problem:** Accumulated Type 1 decisions dressed as Type 2
**Fix:** Consider second-order effects

### Trap 5: Using Decision Type as Excuse

**Symptom:** Calling everything Type 1 to avoid responsibility
**Example:** "We need more research" on every decision
**Problem:** Becomes cover for inaction
**Fix:** Default assumption = Type 2 unless proven otherwise
```

---

### Step 5: Decision Process Template

```
## Decision Classification Template

### The Decision
[What are you deciding?]

### Classification Checklist

**Reversibility Assessment:**
□ Can this be undone in days/weeks?
□ What's the cost of reversing?
□ Are there path dependencies that make reversal hard?
□ Will this create commitments we can't exit?

**Consequence Assessment:**
□ If wrong, what's the impact on revenue?
□ If wrong, what's the impact on reputation?
□ If wrong, what's the impact on team?
□ If wrong, is the company at risk?

### Classification: ____________

| Factor | Type 1 Indicator | Type 2 Indicator | This Decision |
|--------|------------------|------------------|---------------|
| Reversibility | Can't undo | Can undo | |
| Time to undo | Months/Never | Days/Weeks | |
| Cost to undo | High/Impossible | Low/Moderate | |
| Consequence | Existential | Recoverable | |
| Frequency | Rare | Common | |

### Process to Use

**If Type 2:**
- Who should decide? _______________
- Timeline: _______________ (days, not weeks)
- Information needed: _______________
- Communication: _______________

**If Type 1:**
- Who needs to be involved? _______________
- Timeline: _______________ (weeks/months)
- What information is missing? _______________
- What alternatives exist? _______________
- What's the documentation plan? _______________
```

---

## Examples

### Example 1: Product Feature Decision

**Input:**
> "Should we add a dark mode to our app? My team is debating this for two weeks."

**Output:**

## Decision Analysis: Dark Mode Feature

### Classification

| Factor | Assessment |
|--------|------------|
| **Reversible?** | YES - Can ship, can remove if bad |
| **Cost to undo** | LOW - One sprint to remove |
| **Consequence if wrong** | LOW - Users toggle it off, minor wasted effort |
| **Consequence if right** | MEDIUM - Better user experience, some retention |

### Verdict: **TYPE 2 (Two-Way Door)**

Two weeks of debate on a reversible feature decision is organizational dysfunction.

### Recommended Process

**Time allowed:** 2-3 days max
**Who decides:** Product manager + 1 engineer
**Information needed:**
- Quick user survey (100 responses)
- Competitive analysis (2 hours)
- Engineering estimate (30 min)

**The decision:**
1. Is there signal users want it? (Survey >30% interest = yes)
2. Is the cost reasonable? (<1 week engineering = yes)
3. Does it conflict with anything? (Check roadmap)

**If yes to 1 & 2, and no to 3:** Ship it.
**If uncertain:** Ship it behind a feature flag. Measure.

### What NOT To Do

❌ Two weeks of meetings
❌ Executive approval
❌ Perfect user research
❌ Consensus across org
❌ Waiting for more data

### The Bezos Test

"If we ship dark mode and it's wrong, what happens?"

Answer: We remove it in a sprint. A few users briefly confused. No real damage.

**Conclusion:** Make the call. Move on. Spend your deliberation budget on something that matters.

---

### Example 2: Pricing Strategy Change

**Input:**
> "We're considering changing from per-seat pricing to usage-based pricing. How should we approach this?"

**Output:**

## Decision Analysis: Pricing Model Change

### Classification

| Factor | Assessment |
|--------|------------|
| **Reversible?** | PARTIALLY - Technically yes, but... |
| **Cost to undo** | HIGH - Customer confusion, churn, internal systems |
| **Path dependencies** | HIGH - New customers on new model can't easily migrate |
| **Consequence if wrong** | HIGH - Revenue impact, customer churn, competitive exposure |

### Deeper Analysis

**Why this isn't purely Type 2:**
- Existing customers expect current pricing
- Changing back signals instability
- Systems, contracts, sales comp all need updating
- Market perception shifts

**Why it's not purely Type 1:**
- You CAN grandfather existing customers
- You CAN run both models in parallel
- You CAN test with new customers only first

### Verdict: **TYPE 1.5 (Needs Careful Handling)**

This is a major strategic decision with reversibility caveats.

### Recommended Process

**Time:** 4-6 weeks of analysis
**Who:** CEO, CFO, Head of Product, Head of Sales
**Information needed:**
- Financial modeling of both scenarios
- Customer interviews (willingness to switch)
- Competitive analysis
- Engineering/ops assessment
- Sales compensation impact

**Risk Mitigation:**
1. Test with new customers only first (Type 2 experiment)
2. Keep existing customers on old pricing (reversibility hedge)
3. Run for 6 months before migrating anyone
4. Build systems for both models

### Decision Framework

| Approach | Reversibility | Speed | Risk |
|----------|---------------|-------|------|
| Full switch | Low | Fast | High |
| New customers only | High | Medium | Medium |
| Parallel models | High | Slow | Low |

**Recommendation:** Start with new customers only (Type 2). Migrate existing only after validation (then it becomes Type 1).

---

### Example 3: Team/Organization Decision

**Input:**
> "We're debating whether to restructure the engineering team. Some want squads, some want feature teams. We've been discussing for a month."

**Output:**

## Decision Analysis: Team Structure

### Classification

| Factor | Assessment |
|--------|------------|
| **Reversible?** | YES - Reorgs happen all the time |
| **Cost to undo** | MEDIUM - Productivity dip during change |
| **Consequence if wrong** | MEDIUM - Slower delivery for a quarter |
| **Path dependencies** | LOW - People can move teams |

### Verdict: **TYPE 2 (But Feels Like Type 1)**

This FEELS irreversible because it affects people and emotions are high.
But practically? Teams restructure regularly. This is recoverable.

### The Real Problem

A month of debate isn't analysis—it's conflict avoidance.

**What's actually happening:**
- People have opinions and aren't yielding
- No one wants to make a call and be "responsible"
- The debate is comfortable; the decision is uncomfortable

### Recommended Process

**Time:** 1 more week, max
**Who decides:** Engineering lead (or whoever is accountable)
**Process:**
1. Write up both options (1 page each)
2. Define success criteria (what metrics improve?)
3. Pick one
4. Commit for 6 months (review then)
5. "Disagree and commit" - those who disagree still execute

### The Forcing Function

"We will decide by [Friday]. Whoever feels strongest makes the call and is accountable for making it work. We all commit to supporting it for 6 months before reassessing."

### Type 2 Permission

**Say this to the team:**
"This is a two-way door. We can change it later. But we can't debate forever. Let's pick one, run it for 6 months, measure, and adjust. The worst outcome is paralysis."

---

## Checklists & Templates

### Quick Classification Checklist

```
## Is This Type 1 or Type 2?

□ Can we undo this in <30 days?
□ If wrong, will we lose <10% of something important?
□ Is this a common decision (we'll make many like it)?
□ Can we experiment/test before committing?
□ Are the consequences contained?

**Mostly YES → Type 2 (Move fast)**
**Mostly NO → Type 1 (Move carefully)**

### Default Rule
"When in doubt, it's Type 2. Most decisions are."
```

---

### Team Decision Matrix Template

```
## Team Decision-Making Framework

### Type 2 Decisions (Individual/Small Group)
- Feature prioritization
- Bug fixes
- Process improvements
- Hiring (non-leadership)
- Tool selection
- Meeting schedules
- Internal communications

**Process:** Inform, decide, execute
**Timeline:** Hours to days
**Approval:** None needed

### Type 1 Decisions (Leadership/Broader Input)
- Strategic direction
- Major investments (>$X)
- Leadership hiring
- Pricing strategy
- Market entry/exit
- Partnerships
- Shutting down products

**Process:** Analyze, consult, deliberate, decide
**Timeline:** Weeks
**Approval:** [Define levels]

### Escalation Criteria
Escalate Type 2 to Type 1 if:
- Cost exceeds $[X]
- Affects >N customers
- Creates legal/compliance risk
- Changes company strategy
- Irreversible commitment
```

---

## Skill Boundaries

### What This Skill Does Well
- Structuring persuasive content
- Applying copywriting frameworks
- Creating draft variations
- Analyzing competitor approaches

### What This Skill Cannot Do
- Guarantee conversion rates
- Replace brand voice development
- Know your specific audience
- Make final approval decisions

## References

- Bezos, Jeff. "Amazon Shareholder Letters" (2015, 2016) - Type 1/Type 2 framework
- Blank, Steve. "The Four Steps to the Epiphany" - Speed in startups
- Ries, Eric. "The Lean Startup" - Reversible experiments
- Farnam Street. "Mental Models" - Decision frameworks
- Amazon. "Leadership Principles" - Bias for action

## Related Skills

- [second-order-thinking](../second-order-thinking/) - Consider consequences
- [regret-minimization](../regret-minimization/) - Long-term decision view
- [first-principles](../../strategy/first-principles/) - Challenge assumptions
- [pre-mortem](../../strategy/pre-mortem/) - Anticipate failures
- [eisenhower-matrix](../../strategy/eisenhower-matrix/) - Prioritization

---

## Skill Metadata


- **Mode**: cyborg
```yaml
name: reversible-decisions
category: thinking
subcategory: decision-making
version: 1.0
author: MKTG Skills
source_expert: Jeff Bezos
source_work: Amazon Shareholder Letters
difficulty: beginner
estimated_value: $2,000 management consulting session
tags: [decisions, Bezos, Amazon, speed, reversibility, management, delegation]
created: 2026-01-25
updated: 2026-01-25
```
