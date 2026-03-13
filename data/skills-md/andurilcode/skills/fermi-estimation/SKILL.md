---
name: fermi-estimation
description: Apply Fermi estimation whenever the user needs a quantitative answer but lacks precise data — or when a number is needed quickly to inform a decision, sanity-check a plan, or evaluate feasibility. Triggers on phrases like "how long will this take?", "how much will this cost?", "is this feasible?", "how many X are there?", "what's the order of magnitude?", "rough estimate?", "ballpark this for me", "how many tokens does this use?", "how does this scale?", or any situation requiring a quantitative judgment under uncertainty. Also trigger to sanity-check existing estimates — a Fermi calculation that disagrees with an official estimate by an order of magnitude is a signal worth investigating. Don't refuse to estimate because you lack data. Decompose and calculate.
---

# Fermi Estimation

**Core principle**: Almost any quantity can be estimated to within an order of magnitude by decomposing it into components you *can* estimate, then multiplying through. The goal is not precision — it's getting the right number of zeros. A 10× error is informative. A 1000× error changes the decision.

> *"It is better to be approximately right than precisely wrong."* — Carveth Read

---

## Why Fermi Estimation

You're not always in a position to measure. But you often need to decide. Fermi estimation gives you:
- A defensible, traceable quantitative estimate from reasoning alone
- A sanity check on received numbers ("does this feel right order-of-magnitude?")
- Identification of the key driver — the variable that dominates the result
- A structured way to surface which sub-estimates need validation most

---

## The Core Process

### Step 1: Define the Target Quantity Precisely
Ambiguous questions produce useless estimates. Before decomposing, specify:
- What exactly is being estimated?
- Over what time period?
- For what population or scope?
- In what units?

*"How many tokens does this use?"* → *"What is the total token count of a single Constellation pipeline run, processing a medium-complexity feature request, across all agent turns?"*

### Step 2: Decompose into Estimable Factors
Break the unknown quantity into a product of factors you can estimate:

```
Target = Factor_1 × Factor_2 × Factor_3 × ...
```

Look for a decomposition where:
- Each factor can be estimated independently
- The factors multiply to the target (check the units — they should cancel correctly)
- No factor is itself the original unknown in disguise

**Useful decomposition patterns**:
- *Rate × Time*: (requests/hour) × (hours)
- *Count × Average*: (number of items) × (average size per item)
- *Population × Fraction*: (total users) × (% who do X)
- *Flow × Duration*: (throughput) × (duration)

### Step 3: Estimate Each Factor
For each factor, make an explicit estimate with reasoning:
- What do you know about this?
- What analogies can you draw on?
- What's a plausible range?

Use round numbers — the goal is order of magnitude, not false precision.

### Step 4: Compute and Sanity-Check
Multiply through. Then:
- Does the result feel right? Does it pass common sense?
- Does it match any reference points you know?
- Which factor, if wrong, would most change the result?

### Step 5: Bound the Estimate
- **Low estimate**: Use the low end of each factor's range
- **Central estimate**: Use your best guess for each
- **High estimate**: Use the high end

If high/low are within a factor of 3× each side, the estimate is well-bounded. If they're orders of magnitude apart, one factor is too uncertain — that's what to validate.

---

## Output Format

### 🎯 Target Quantity
- **Estimating**: [Precisely defined quantity]
- **Units**: [What we're counting in]

### 🧮 Decomposition
| Factor | Estimate | Reasoning |
|--------|----------|-----------|
| [Factor 1] | [Value] | [Why you believe this] |
| [Factor 2] | [Value] | [Why you believe this] |
| [Factor 3] | [Value] | [Why you believe this] |
| **Product** | **= [Result]** | |

### 📊 Range
| Scenario | Estimate | Key driver |
|----------|----------|-----------|
| Low | [Value] | [Which factor is at its low] |
| Central | [Value] | Best guess |
| High | [Value] | [Which factor is at its high] |

### 🔍 Key Driver
- Which factor contributes most to the result?
- If you could only validate one factor, which would it be?
- A 2× error in [key factor] produces a [2×] error in the result — worth checking.

### ✅ Sanity Checks
- Reference point comparison: [Known comparable value]
- Does this pass common sense? [Yes / No — if no, which factor is suspect?]
- Order-of-magnitude conclusion: [The number of zeros that matter here]

---

## Common Useful Reference Points

Keep these in rough memory for decomposition:

**Time**
- Person-hour of engineering work: ~1–4 hours of focused effort
- Working hours per week: ~40 (effective: ~25–30)
- Days per month: ~22 working days

**Compute / LLM**
- Typical prose token density: ~750 words per 1,000 tokens
- GPT-4-class input cost: ~$2–10 per million tokens (varies by model)
- Average LLM response time: 1–10 seconds depending on length and model
- Code file: 50–500 lines typical; ~100–2,000 tokens

**Scale**
- Small SaaS: 1k–10k MAU
- Mid-size product: 100k–1M MAU
- Large platform: 10M+ MAU

**Money**
- Fully-loaded engineer cost (EU/US): €80k–€200k/year
- Per-hour cost: €40–€100/hour
- AWS small instance: ~$10–50/month

---

## Estimation Anti-Patterns

**False precision**: Reporting "42,381 tokens" when the estimate is order-of-magnitude. Use round numbers.

**Single-path decomposition**: Only one way to decompose the problem. Cross-check with an independent decomposition — if they agree, confidence is higher.

**Forgetting to check units**: If units don't cancel correctly, the decomposition is wrong.

**Treating the estimate as the answer**: A Fermi estimate is a starting point and a sanity check, not a substitute for measurement when measurement is possible and the decision warrants it.

**Refusing to estimate**: *"I don't have enough data"* is rarely the right answer when a decision needs to be made. Decompose what you can; flag what you can't.

---

## Thinking Triggers

- *"What does this quantity equal, as a product of things I can estimate?"*
- *"What's the right number of zeros here?"*
- *"Which single factor, if wrong by 10×, changes my conclusion?"*
- *"What reference point can I use to sanity-check this?"*
- *"If the estimate is off by 2×, does it change the decision? By 10×?"*

---

## Example: Token Budget for an Agent Pipeline

**Question**: How many tokens does one Constellation run consume?

| Factor | Estimate | Reasoning |
|--------|----------|-----------|
| Number of agent turns | 8 | 6 agents + 1 orchestrator + 1 review |
| Avg input tokens per turn | 4,000 | System prompt ~1k + context ~2k + task ~1k |
| Avg output tokens per turn | 1,000 | Structured response, not prose-heavy |
| **Total per run** | **= 8 × 5,000 = 40,000 tokens** | |

**Range**: 20k (simple task, short context) to 120k (complex task, full history passed through)

**Key driver**: Input context size — it dominates. Compressing context is highest-leverage.

**Sanity check**: A 40k-token run at $5/M tokens = $0.20/run. At 100 runs/day = $20/day = ~$600/month. Plausible for a dev tool.
