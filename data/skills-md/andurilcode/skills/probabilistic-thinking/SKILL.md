---
name: probabilistic-thinking
description: Apply probabilistic and Bayesian thinking whenever the user needs to reason under uncertainty, compare risks, prioritize between options, update beliefs based on new evidence, or make decisions without complete information. Triggers on phrases like "what are the odds?", "how likely is this?", "should I be worried about X?", "which risk is bigger?", "does this data change anything?", "is this a signal or noise?", "what's the probability?", "how confident are we?", or any situation where decisions are being made based on incomplete or ambiguous evidence. Also trigger when someone is treating uncertain outcomes as certainties, or when probability language is being used loosely ("probably", "unlikely", "very likely") without quantification. Don't leave uncertainty unexamined.
---

# Probabilistic & Bayesian Thinking

**Core principle**: Most real decisions happen under uncertainty. Probabilistic thinking replaces vague confidence with calibrated estimates. Bayesian thinking adds the discipline of *updating* those estimates as new evidence arrives — neither clinging to prior beliefs nor overreacting to new data.

---

## Core Concepts

### Probability as Degree of Belief
Probability isn't just for coin flips. It's a measure of how confident we are in any claim, given current evidence.

- "This will probably work" → What probability? 60%? 90%? The difference matters.
- Forcing a number exposes vague confidence and creates a baseline for updating.

### Base Rates
Before estimating the probability of a specific event, find the **base rate** — how often does this type of event occur in a reference class?

*"Will this feature succeed?"* → What % of similar features in similar products succeeded?

Ignoring base rates (the **base rate fallacy**) is one of the most common reasoning errors.

### Bayesian Updating
When new evidence arrives, update beliefs proportionally — not by ignoring prior beliefs, and not by overwriting them entirely.

```
New Belief = Prior Belief × Weight of New Evidence
```

Key questions:
- **Prior**: What did we believe before this evidence?
- **Likelihood**: How probable is this evidence if the hypothesis is true? If it's false?
- **Posterior**: What should we believe now?

### Expected Value
When choosing between options under uncertainty, compare expected values:
```
EV = Probability of outcome × Value of outcome
```
A 10% chance of +€100 (EV = €10) is better than a 90% chance of +€5 (EV = €4.50).

### Confidence Intervals
Point estimates are almost always wrong. Ranges are more honest.
- Instead of "this will take 4 weeks" → "this will take 3–7 weeks (80% confidence)"
- Wide intervals are not weakness — they're calibration. Narrow intervals on uncertain things are overconfidence.

---

## Output Format

### 📊 Probability Estimates
For each key claim or outcome:
| Claim | Prior probability | Evidence | Updated probability | Confidence |
|-------|-----------------|----------|-------------------|------------|
| "Feature will succeed" | 30% (base rate) | Strong user signal | 55% | Medium |
| "This will ship on time" | 40% (historical) | Team is experienced | 50% | Low |

### 🔢 Base Rate Check
- What is the reference class for this situation?
- What is the historical base rate for this type of outcome?
- How does this specific case differ from the base rate (and does that justify adjusting up or down)?

### 🔄 Bayesian Update
When new evidence has arrived:
- **Prior belief**: What did we think before?
- **New evidence**: What do we now know?
- **Likelihood ratio**: Is this evidence more consistent with the hypothesis being true or false?
- **Posterior belief**: What should we believe now?
- **Update size**: Did this evidence move the needle significantly? (Strong evidence = large update. Weak evidence = small update.)

### ⚖️ Expected Value Comparison
When choosing between options:
| Option | Probability | Value if succeeds | Value if fails | Expected Value |
|--------|------------|------------------|----------------|----------------|
| Option A | 70% | +€50k | -€10k | +€32k |
| Option B | 30% | +€200k | -€20k | +€46k |

### 📏 Confidence Ranges
Replace point estimates with ranges:
- **Optimistic case** (10th percentile): [value]
- **Expected case** (50th percentile): [value]
- **Pessimistic case** (90th percentile): [value]
- **Black swan scenario**: [What happens in the tail?]

### ⚠️ Probability Hygiene Flags
- Are any probabilities being treated as certainties (0% or 100%)? Almost nothing is certain.
- Is base rate being ignored in favor of the specific case?
- Is new evidence causing overreaction (anchoring to latest data)?
- Is there a conjunction fallacy? (P(A and B) < P(A) always — the more specific the scenario, the lower its probability)

---

## Calibration Heuristics

**Fermi Estimation** — For unknown quantities, break into smaller estimable parts:
- Instead of "how many users will we get?" → estimate: market size × awareness % × conversion % × retention %

**Reference Class Forecasting** — Use historical data from similar projects:
- "This type of feature took 4–8 weeks for 80% of teams in our reference class"

**Outside View vs. Inside View**:
- **Inside view**: "Our situation is special, we'll beat the average"
- **Outside view**: "What does the data say for projects like this?"
- Default to the outside view. Adjust only with specific, strong evidence.

**Pre-commit to what would change your mind**:
- "If we see X, I will update my probability from 60% to below 30%"
- This prevents post-hoc rationalization of new evidence

---

## Thinking Triggers

- *"What's the base rate for this?"*
- *"Are we treating a 70% probability like a certainty?"*
- *"What's the expected value of each option, not just the upside?"*
- *"How much should this new evidence actually move our belief?"*
- *"What would we need to see to change our mind significantly?"*
- *"Are we in the reference class we think we're in?"*
- *"What's the downside scenario, and are we weighting it correctly?"*

---

## Example Applications
- **"Should we build this feature?"** → What % of similar features drove meaningful retention? What's the cost if it fails?
- **"This A/B test showed a lift"** → Is the sample size sufficient? What's the prior for this type of change?
- **"We'll ship in 2 weeks"** → What's the historical distribution for similar tasks? What's the 80th percentile?
- **"The agent failed once — is it a bug?"** → What's the base rate of one-off failures? What evidence would confirm it's systematic?
