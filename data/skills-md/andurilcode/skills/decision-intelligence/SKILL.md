---
name: decision-intelligence
description: "Apply this skill when ALL THREE conditions are true: (1) a single decision or belief is being evaluated — not a comparison between multiple options; (2) probability and outcome magnitude are both estimable, even roughly; (3) human bias is likely distorting the reasoning — sunk costs already paid, vivid success stories dominating, intuition pulling against the math, or real money/time at stake. Triggers on phrases like 'should I do this?', 'is this worth it?', 'I've already put so much into this', 'everyone seems to be succeeding at this', 'how much should I commit?', or any single-path decision involving financial bets, career moves, or long-term commitments where bias and probability both matter. Do NOT use for comparing multiple options (use decision-synthesis), pure probability estimation (use probabilistic-thinking), or estimation only (use fermi-estimation). This skill is mandatory-process: it applies all 6 models to every input without exception. Never skip a model."
---

# Decision Intelligence — 6-Model Framework

**Core principle**: Every decision is a probability problem. Human intuition systematically misprices risk, overweights recent vivid stories, and confuses past costs with future value. This skill applies six mental models rigorously and in sequence — not as a checklist to rush through, but as a structured correction to the ways human reasoning predictably fails.

**MANDATORY**: Apply all 6 models to every input. Never skip. Never default to "follow your gut." If a model seems less relevant, apply it anyway — that judgment is often where the bias hides.

---

## Mandatory 4-Step Process

### Step 0: Clarify the Core Question
Before applying any model, restate the decision or belief in one sentence:
> *"The real question is: [single clear question]."*

This prevents the analysis from drifting. If the user's stated question is fuzzy, sharpen it before proceeding.

---

### Step 1 — Expected Value (EV)

**Mechanic**: EV = Σ (probability × payoff)

Every outcome has a probability and a payoff (positive or negative). Calculate the average long-term value across all plausible outcomes. The decision with the highest EV is the rational choice — unless risk of ruin makes variance itself a cost.

**Process**:
1. List all meaningful outcomes (don't just consider the best and worst — include the most likely)
2. Assign realistic probabilities to each (they must sum to 100%)
3. Estimate the payoff for each outcome (financial, time, opportunity cost, emotional — be explicit about units)
4. Calculate EV = Σ (p × payoff)
5. Flag if loss aversion is inflating the perceived cost of the negative outcomes

**Output format**:
| Outcome | Probability | Payoff | EV contribution |
|---------|------------|--------|----------------|
| [Outcome A] | X% | +€Y | +€Z |
| [Outcome B] | X% | -€Y | -€Z |
| **Total EV** | 100% | | **€[sum]** |

**Key bias to flag**: Loss aversion — humans feel losses ~2× more intensely than equivalent gains. If the EV is positive but the user is hesitating, loss aversion is likely the reason.

---

### Step 2 — Base Rate Neglect

**Mechanic**: Always start with the historical base rate for this category of decision before adjusting for specifics.

The base rate is what happens to people who do this thing, on average, in the absence of any special information about the individual case. It is the prior. Everything else — the unique advantages, the special circumstances, the vivid success stories — is the update.

**Process**:
1. Identify the reference class: *"What category of decision/person/situation is this?"*
2. Find or estimate the base rate for success/failure in that reference class
3. Only after anchoring on the base rate, apply specific adjustments
4. Flag if the user is reasoning primarily from vivid anecdotes rather than rates

**Common base rates worth knowing**:
- Startups reaching profitability: ~10–20%
- New restaurants surviving year 1: ~40% (year 5: ~20%)
- New products achieving product-market fit: ~5–15%
- Day traders beating the market consistently: ~1–5%
- People who start a new habit maintaining it after 6 months: ~20%
- Projects delivered on time and budget: ~30–35%

**Key bias to flag**: Availability bias — the cases we hear about are systematically unrepresentative (we hear about the successes). The silent majority of failures is invisible.

---

### Step 3 — Sunk Cost Fallacy

**Mechanic**: Ignore everything already spent. Evaluate the decision as if starting today.

Past investment — time, money, emotion, reputation — is gone regardless of what decision is made now. It is irrelevant to the forward-looking question. The only question is: *"Knowing what I know now, would I choose this path if I were starting fresh today?"*

**Process**:
1. Identify all sunk costs: money spent, time invested, emotional commitment, public statements made
2. Explicitly set them to zero
3. Re-evaluate the decision based only on future costs, future benefits, and current probabilities
4. If the answer changes when sunk costs are zeroed out, sunk cost fallacy is active

**Diagnostic question**: *"If I had not already invested [X], would I start this today?"*
- If yes → proceed, but for the right reasons
- If no → sunk cost is the only reason to continue; this is the fallacy in operation

**Key bias to flag**: Escalation of commitment — the more we've invested, the harder it becomes to walk away, even when walking away is clearly correct.

---

### Step 4 — Bayesian Thinking

**Mechanic**: Update beliefs proportionally to evidence strength.

```
P(belief | evidence) = P(evidence | belief) × P(belief) / P(evidence)
```

In plain terms:
- **Prior**: What did you believe before this new information?
- **Likelihood**: How probable is this evidence if the belief is true? How probable if it's false?
- **Posterior**: What should you believe now, after seeing the evidence?

**Process**:
1. State the prior explicitly (as a probability, not a vague impression)
2. Identify the new evidence
3. Estimate the likelihood ratio: how much more likely is this evidence if the hypothesis is true vs. false?
4. Update the prior proportionally — not to 0% or 100%, and not by ignoring the prior entirely
5. State the posterior

**Key bias to flag**: Overreaction to single data points — one success story, one failure, one friend's experience. A single data point should move your prior, but rarely more than a few percentage points unless it was a highly diagnostic test.

---

### Step 5 — Survivorship Bias

**Mechanic**: When seeing success stories, actively estimate the invisible denominator.

The cases you observe are not a random sample. They are the survivors — the ones visible precisely because they succeeded. The failures are silent. Every "how I made it" story is missing the untold "how I didn't make it" stories from people who did the same thing.

**Process**:
1. Count the visible successes you're aware of
2. Estimate the invisible denominator: *"How many people tried this? How many are you not hearing from?"*
3. Calculate the implied success rate: visible successes / estimated total attempts
4. Check if this rate is consistent with the base rate from Step 2

**Diagnostic question**: *"What would I need to see to hear about the failures? Why don't I?"*

**Key bias to flag**: Narrative bias — success stories have protagonists, arcs, and lessons. Failure is quiet and diffuse. Our mental model of what's possible is built almost entirely from the survivors.

---

### Step 6 — Kelly Criterion

**Mechanic**: When you have an edge, size the bet to maximize long-term growth without risking ruin.

```
f* = (p × b - q) / b
```

Where:
- `f*` = fraction of capital to bet
- `p` = probability of winning
- `q` = probability of losing (1 - p)
- `b` = net odds (what you win per unit risked)

**In practice**: Use fractional Kelly (¼ to ½ of f*) for real-life decisions. Full Kelly maximizes long-term growth in theory but produces terrifying variance in practice. Half-Kelly gives ~75% of the growth with much less volatility.

**Process**:
1. Estimate p (win probability) from Steps 1–5
2. Estimate b (the odds — what does a win return relative to the loss?)
3. Calculate f*
4. Recommend fractional Kelly (½f* for moderate confidence, ¼f* for high uncertainty)
5. If f* is negative or near zero: no edge exists. Do not bet.
6. If f* > 1: Kelly is flagging extreme edge — treat with suspicion, recheck your probability estimates

**Key bias to flag**: Overbetting — humans tend to size positions too large relative to their actual edge, especially after a few wins. Kelly provides the mathematical guardrail.

---

## Step 2 (Final): Synthesized Recommendation

After all 6 models, synthesize:

```
DECISION INTELLIGENCE SYNTHESIS

Core question: [restated from Step 0]

Model verdicts:
- EV: [positive/negative/marginal, key number]
- Base rate: [X% success rate for this category]
- Sunk cost: [active / not active — decision changes / doesn't change when zeroed out]
- Bayesian update: [prior → evidence → posterior]
- Survivorship bias: [estimated true success rate vs. observed stories]
- Kelly sizing: [f* = X%, recommended allocation = Y%]

Primary bias in play: [the one bias most likely distorting this decision]

Recommendation: [clear action]
Confidence: [0–100%]
Key risks: [top 2–3]
What would change this view: [specific evidence that would shift the recommendation]
```

Be direct. If the math contradicts intuition, say so explicitly. Discomfort with the conclusion is often a sign the analysis is working.

---

## Relationship to Other Skills

- Run **before** `decision-synthesis` when the decision involves quantifiable stakes — this provides the probabilistic inputs that decision-synthesis weighs
- Complements `probabilistic-thinking` (which covers Bayesian updating in depth) and `cognitive-bias-detection` (which audits reasoning broadly) — but this skill applies both specifically to decision sizing and commitment
- When `scenario-planning` has produced multiple futures, run this skill on the decision *within* each scenario to assess EV across them
- `fermi-estimation` feeds directly into Step 1 (EV) and Step 2 (base rates) when numbers aren't readily available
