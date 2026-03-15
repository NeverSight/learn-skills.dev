---
name: decision-synthesis
description: Apply decision synthesis whenever the user has completed analysis — run multiple frameworks, mapped the problem, identified options — and now needs to actually choose. Triggers on phrases like "so what should we do?", "how do we decide between these?", "we have too many options", "everything seems equally valid", "how do we weigh these trade-offs?", "we can't agree on which direction", "given all this, what's the call?", or when a rich diagnostic phase has produced competing insights without a clear winner. Also trigger when a decision involves multiple stakeholders with different priorities, multiple criteria that pull in different directions, or significant irreversibility. This skill bridges analysis to action — don't leave a decision unmade because the map is rich.
---

# Decision Synthesis

**Core principle**: Analysis produces options and criteria. Synthesis produces a decision. Most frameworks are good at divergence — generating possibilities, mapping complexity. This skill is about convergence: taking what you know and making a defensible, traceable choice.

A good decision process doesn't guarantee the right outcome. It maximizes the quality of reasoning given available information, and it's transparent enough to learn from when outcomes arrive.

---

## When to Use This Skill

Use after other reasoning frameworks have done their work:
- Systems Thinking mapped the structure
- 5 Whys found the root causes
- Scenario Planning produced multiple futures
- Red Teaming attacked the options
- Stakeholder Mapping identified who needs to align

Now you have a rich picture and multiple options. Decision Synthesis is how you land.

---

## The Core Process

### Step 1: Clarify What's Actually Being Decided
Before evaluating options, make the decision crisp:
- What is the exact choice being made?
- What's the decision horizon? (reversible in 3 months? irreversible?)
- Who has final authority?
- What's the cost of delaying the decision?

Many decision processes fail because people are evaluating different questions without realizing it.

### Step 2: Surface All Options
List every viable option explicitly — including:
- The status quo (doing nothing is always an option)
- Hybrid approaches
- Sequenced approaches (do A now, revisit B in 6 months)
- Options that were dismissed early but deserve a formal look

### Step 3: Define Criteria
What matters in this decision? List the criteria explicitly:
- **Must-haves** (binary — options failing these are eliminated)
- **Want-to-haves** (graded — options are compared on these)

Good criteria are:
- Specific enough to score (not "good quality" but "error rate < 1%")
- Independent of each other (avoid double-counting)
- Tied to the actual goal, not proxies

### Step 4: Weight the Criteria
Not all criteria are equally important. Assign weights explicitly — this forces clarity about what actually matters most and exposes hidden disagreements between stakeholders.

Simple approach: distribute 100 points across criteria. The allocation is the conversation.

### Step 5: Score the Options
For each option against each criterion, score 1–5 (or 1–10). Be explicit about the reasoning for each score — scores without reasoning can't be challenged or improved.

### Step 6: Compute and Challenge
Weighted scores give a quantitative signal — not a verdict. Use the result to:
- Check: does the top scorer match intuition? If not, why not?
- Interrogate: which criteria are driving the result? Are they the right ones?
- Stress-test: if the top two criteria swap weights, does the answer change?
- Sanity-check: would you be comfortable explaining this choice to a critic?

---

## Output Format

### 🎯 Decision Statement
- **Decision**: [The exact choice being made]
- **Horizon**: [Reversible / Partially reversible / Irreversible]
- **Decider**: [Who has authority]
- **Deadline**: [When this must be resolved]

### 📋 Options
| # | Option | Brief description |
|---|--------|------------------|
| 1 | [Name] | [One line] |
| 2 | ... | |

### ⚖️ Criteria & Weights
| Criterion | Type | Weight | Rationale |
|-----------|------|--------|-----------|
| [Criterion 1] | Must-have | — | [Why it's binary] |
| [Criterion 2] | Want-to-have | 35 | [Why this weight] |
| [Criterion 3] | Want-to-have | 25 | |
| ... | | **100** | |

### 📊 Scoring Matrix
| Option | Criterion 1 | Criterion 2 (×35) | Criterion 3 (×25) | ... | **Weighted Total** |
|--------|------------|------------------|------------------|-----|--------------------|
| Option A | ✅ Pass | 4 → 140 | 3 → 75 | | **X** |
| Option B | ✅ Pass | 2 → 70 | 5 → 125 | | **Y** |
| Option C | ❌ Fail | — | — | | **Eliminated** |

### 🏆 Recommendation
- **Recommended option**: [Name]
- **Primary reason**: [The 1–2 criteria that drove the result]
- **Main trade-off**: [What this option sacrifices]
- **Confidence**: [High / Medium / Low — based on quality of information, not strength of preference]

### ⚠️ Sensitivity Check
- If [top-weighted criterion] changes in importance, does the answer change?
- What assumption, if wrong, most undermines this recommendation?
- What new information would cause a re-evaluation?

### 🔁 Reversibility & Regret
- Can this be undone? At what cost?
- **Regret minimization**: Which choice produces the least regret if the situation changes significantly?
- If confidence is low and the decision is irreversible — flag this explicitly before committing.

---

## Decision Traps to Avoid

**False consensus**: Everyone nods but the criteria weights were never made explicit — different people were solving for different things.

**Analysis paralysis**: More analysis rarely resolves genuine value disagreements. Name the disagreement and make the call.

**Criteria inflation**: Adding more criteria to feel thorough — but irrelevant criteria add noise, not signal. Keep the list short and honest.

**Anchoring on the first option**: The option framed first gets disproportionate attention. Evaluate all options in parallel, not sequentially.

**Score laundering**: Working backwards from a preferred conclusion to assign scores that justify it. The matrix is a thinking tool, not a legitimacy machine.

---

## Thinking Triggers

- *"If I had to make this decision alone, with no politics involved, what would I choose?"*
- *"Which criteria are we weighting based on what actually matters vs. what's easy to measure?"*
- *"Is there a hybrid option we haven't named?"*
- *"What would a regret minimizer choose? A risk minimizer? A maximizer?"*
- *"Are we delaying because we need more information, or because we don't want to own the decision?"*
