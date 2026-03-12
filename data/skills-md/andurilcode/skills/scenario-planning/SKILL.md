---
name: scenario-planning
description: Apply scenario planning whenever the user is making long-term decisions, building roadmaps, evaluating strategies, or operating in an environment with significant uncertainty about how the future will unfold. Triggers on phrases like "what should our roadmap look like?", "how do we plan for the future?", "what if things change?", "we're not sure which direction the market will go", "how do we make this strategy resilient?", "what's our plan B?", "what are the different futures we could face?", or when a plan assumes a single future state. Also trigger when someone is over-committed to one expected outcome and hasn't stress-tested the strategy against alternative futures. Don't plan for one future — plan for multiple.
---

# Scenario Planning

**Core principle**: The future is uncertain. Scenario planning doesn't try to predict which future will happen — it maps a set of plausible futures and tests strategies against each. A robust strategy performs reasonably well across multiple scenarios. A fragile strategy only works if one specific future occurs.

---

## The Core Process

### Step 1: Define the Decision or Strategy
What are we planning for?
- What time horizon? (6 months / 2 years / 5 years)
- What decision needs to be made now?
- What would "good" look like across different futures?

### Step 2: Identify Key Uncertainties
What are the 2–3 most important factors that are both:
- **Highly uncertain** (we genuinely don't know how they'll unfold)
- **Highly impactful** (they would significantly change what the right strategy is)

These are the **scenario axes** — the dimensions along which futures differ most.

Avoid certainties (things that will definitely happen) and minor factors. Focus on the pivotal unknowns.

### Step 3: Build the Scenarios
From the key uncertainties, construct 3–4 distinct, internally consistent futures. Each scenario should be:
- **Plausible**: Not science fiction — could actually happen
- **Distinct**: Each scenario is meaningfully different from the others
- **Challenging**: At least one scenario is uncomfortable for the current plan

**Common scenario structures:**

*Two-axis matrix (for two key uncertainties):*
```
         High market adoption
              |
Slow tech  ──┼── Fast tech
 change       |     change
              |
         Low market adoption
```
This generates 4 quadrant scenarios.

*Three narrative scenarios:*
- **Expected**: The future most people are implicitly planning for
- **Optimistic**: Key uncertainties resolve favorably
- **Pessimistic**: Key uncertainties resolve adversarially
- **Wild card**: A low-probability, high-impact disruption

### Step 4: Stress-Test the Strategy
For each scenario:
- Does the current strategy work well / adequately / poorly?
- What would need to change in the strategy for it to work in this scenario?
- What's the cost of being wrong about which scenario occurs?

### Step 5: Identify Robust Actions
Find actions that perform well across *multiple* scenarios — these are the highest-confidence moves regardless of which future occurs.

Also find **hedging options** — small bets that preserve flexibility and cost little in the expected scenario but pay off in unlikely ones.

---

## Output Format

### 🌐 Key Uncertainties
| Uncertainty | Why it matters | Range of outcomes |
|------------|----------------|------------------|
| [Factor 1] | [Impact on strategy] | [From X to Y] |
| [Factor 2] | [Impact on strategy] | [From A to B] |

### 📖 The Scenarios

For each scenario (3–4 total):

**Scenario Name** *(give it a memorable name)*
- **Description**: 2–3 sentences painting the picture of this future
- **Key conditions**: What's true in this world?
- **Probability estimate**: Rough likelihood (should sum to ~100% across scenarios)
- **Key signals**: What early indicators would tell us we're in this scenario?

### 🧪 Strategy Stress Test

| Scenario | Current strategy performs... | Why | What must change |
|----------|---------------------------|-----|------------------|
| Scenario A | Well | [Reason] | Nothing |
| Scenario B | Adequately | [Reason] | [Adjustment] |
| Scenario C | Poorly | [Reason] | [Major pivot] |
| Scenario D | Catastrophically | [Reason] | [Fundamental rethink] |

### 🏆 Robust Actions
Actions that make sense across most or all scenarios:
- [Action 1] — works because [reason across scenarios]
- [Action 2] — works because [reason across scenarios]

### 🎯 Scenario-Specific Actions
If a particular scenario becomes likely, what additional actions should be taken?
| Scenario | Trigger signal | Response action |
|----------|---------------|----------------|
| Scenario B | [Leading indicator] | [Action to take] |
| Scenario C | [Leading indicator] | [Action to take] |

### 🚨 Fragility Assessment
- Which scenario would the current plan handle worst?
- What's the single assumption the plan most depends on?
- What's the cheapest hedge against the worst scenario?

---

## Scenario Planning Pitfalls

- **Too many scenarios**: 3–4 is ideal. More becomes unmanageable.
- **Scenarios too similar**: Each must be meaningfully distinct — different enough to require different strategies.
- **Anchoring on the expected scenario**: Give real attention to uncomfortable scenarios, not just the comfortable one.
- **No early warning signals**: Every scenario needs leading indicators — how do we know we're in it before it's too late to adapt?
- **Planning for the scenario, not the strategy**: The goal isn't to predict which scenario occurs. It's to build a strategy resilient enough to handle whichever one does.

---

## Thinking Triggers

- *"What are we implicitly assuming about the future in this plan?"*
- *"What's the world where this strategy fails completely — and how likely is it?"*
- *"What would we do differently if we knew we were in Scenario C?"*
- *"What are the early signals that would tell us which future we're heading into?"*
- *"What's the cheapest move that protects us in the bad scenarios without sacrificing the good ones?"*

---

## Example Applications
- **Product roadmap**: What if AI commoditizes our core feature? What if regulation changes the market? What if a major platform shifts behavior?
- **Architecture decision**: What if traffic grows 10x? What if the third-party API sunsets? What if the team doubles?
- **Business strategy**: What if the funding environment tightens? What if the key competitor undercuts pricing? What if adoption is 5x faster than projected?
- **Agent pipeline design**: What if LLM costs drop 90%? What if context windows become unlimited? What if a single agent becomes capable enough to replace the pipeline?
