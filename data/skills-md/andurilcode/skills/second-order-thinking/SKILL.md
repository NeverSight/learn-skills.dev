---
name: second-order-thinking
description: Apply second-order thinking whenever the user is making a decision, proposing a change, or evaluating an action — especially one that seems obviously good or obviously safe. Triggers on phrases like "let's just do X", "the obvious answer is", "we should change Y", "what happens if we do Z?", "should we implement this?", "will this work?", or any time a user proposes an intervention in a system involving people, incentives, markets, or complex processes. Also trigger when first-order analysis has already been done and the user needs to go deeper. Second-order thinking should be applied before any significant decision is made — don't wait to be asked.
---

# Second-Order Thinking

**Core principle**: First-order thinking asks "what happens next?" Second-order thinking asks "and then what?" Most people stop at the first answer. The most consequential effects — intended and unintended — live in the second and third order.

---

## The Core Loop

For any action or decision, trace the consequence chain:

```
Action
  → 1st order effect (immediate, obvious)
      → 2nd order effect (who responds? what changes?)
          → 3rd order effect (what does that change produce?)
              → ... (stop when effects become negligible or too uncertain)
```

At each level ask:
- **Who is affected?** (not just the intended target)
- **How do they respond?** (assume rational actors adapting to the new reality)
- **What new equilibrium does that create?**
- **Does this feedback back into the original action?**

---

## Key Mental Models Within Second-Order Thinking

### Unintended Consequences
Most "obvious" interventions fail because of unintended consequences. Classic patterns:

| Intervention | 1st Order | 2nd Order (unintended) |
|---|---|---|
| Rent control | Rents don't rise | Landlords convert to condos, housing supply shrinks |
| Add more lanes to highway | More capacity | More drivers, same congestion (induced demand) |
| Reward engineers for lines of code | More code written | Code quality drops, complexity explodes |
| Add more process to prevent mistakes | Fewer mistakes | Slower delivery, process-worship, talent leaves |
| Fix every bug immediately | Cleaner code | Team never works on features, roadmap stalls |

### Goodhart's Law
*"When a measure becomes a target, it ceases to be a good measure."*

When you optimize for a metric, behavior shifts to game the metric — the underlying goal is lost.

Ask: *What happens to this metric if people optimize for it directly?*

### Cobra Effect
Incentives designed to solve a problem can make it worse. (British offered bounties for dead cobras in India → people bred cobras to collect bounties.)

Ask: *Could the incentive structure we're creating be gamed in a way that produces more of what we're trying to eliminate?*

### Equilibrium Shifts
Systems seek equilibrium. When you disturb them, they rebalance — often in ways that cancel your intervention.

Ask: *What new equilibrium does this create? Is it better or worse than the current one?*

---

## Output Format

### 🎯 First-Order Effects
The immediate, obvious results of the action:
- What changes directly?
- Who benefits immediately?
- What problem does this solve?

### 🔄 Second-Order Effects
Who adapts? What do they do in response?
- **Actors affected**: Who is impacted and how might they respond?
- **Behavioral shifts**: How does behavior change in response to the new reality?
- **New dynamics**: What new relationships, incentives, or tensions emerge?

### 🌊 Third-Order Effects (if significant)
What does the second-order response produce?
- Does this reinforce or undermine the original intent?
- Does this create a new problem to solve?
- Does this change the system's equilibrium permanently?

### ⚠️ Unintended Consequences to Watch
List the most likely negative second/third-order effects:
- **Probability**: Low / Medium / High
- **Severity**: Minor / Significant / Critical
- **Reversibility**: Easily reversible / Hard to undo / Irreversible

### 🛡️ Design Adjustments
How can the action be modified to preserve first-order benefits while mitigating second-order risks?
- Add constraints or safeguards
- Phase the change (test before full rollout)
- Monitor early signals of bad second-order effects
- Build in a reversal mechanism

---

## Thinking Triggers

Use these to deepen the analysis:
- *"Who benefits from the current state and will resist this change?"*
- *"If this works exactly as intended, what new problem does it create?"*
- *"What gets optimized for, and what happens when people optimize for it directly?"*
- *"10 minutes / 10 months / 10 years from now — how does this look different?"*
- *"What's the equilibrium this produces? Do we want to live there?"*
- *"Who isn't in the room that this affects?"*

---

## Time Horizons Framework

Deliberately apply three time horizons:

| Horizon | Question | Typical blind spot |
|---------|----------|-------------------|
| **10 minutes** | What happens immediately? | Usually well-understood |
| **10 months** | Who has adapted and how? | Often overlooked |
| **10 years** | What's the long-term equilibrium? | Almost always ignored |

The 10-month window is where most unintended consequences first become visible.

---

## Example Applications
- **"Let's add a KPI for deployment frequency"** → Engineers start splitting PRs artificially, code quality drops
- **"We should make the AI agent more autonomous"** → Fewer interruptions (good) → harder to catch drift → errors compound silently
- **"Let's reduce meeting time"** → More focus time (good) → alignment gaps emerge → decisions made in silos → rework increases
- **"We should charge for the API to reduce abuse"** → Less abuse (good) → legitimate experimenters leave → ecosystem shrinks → competitors gain ground
