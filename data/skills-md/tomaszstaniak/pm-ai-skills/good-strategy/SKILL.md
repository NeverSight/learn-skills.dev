---
name: good-strategy
description: 'Strategy evaluation and design framework based on Richard Rumelt''s "Good Strategy Bad Strategy" and Michael Porter''s "What Is Strategy?". Use when you need to: (1) evaluate whether a strategy is good or bad, (2) diagnose the core challenge before proposing solutions, (3) build a coherent strategy kernel (diagnosis + guiding policy + coherent actions), (4) stress-test strategic plans with pre-mortem analysis, (5) distinguish strategy from goals, ambitions, or wish lists.'
license: CC-BY-SA-4.0
metadata:
  author: Tomasz Staniak
  version: "1.0.0"
---

# Good Strategy Framework

A framework for evaluating, designing, and stress-testing strategies. Based on Richard Rumelt's "Good Strategy Bad Strategy" and enriched with Michael Porter's "What Is Strategy?" — the definitive works on distinguishing real strategy from the fluff that passes for it. Includes a built-in pre-mortem stress test.

## Core Principle

**Strategy is not a goal. Strategy is a coherent response to a challenge.** Most organizations confuse strategy with ambition ("be the market leader"), goals ("grow 30% YoY"), or a list of priorities ("our strategic priorities are..."). None of these are strategy. A strategy is a diagnosis of the situation, a guiding policy for dealing with it, and a set of coherent actions designed to carry out the policy.

Porter adds a critical insight: **Strategy is about choosing what NOT to do.** The essence of strategy is choosing a set of activities that are different from competitors. Operational effectiveness (doing the same things better) is not strategy. Competitive advantage comes from performing different activities or performing similar activities in different ways.

## Scoring

**Goal: 10/10.** When evaluating a strategy, rate it 0-10:

| Score | Description |
|-------|-------------|
| 0-2 | No strategy. What exists is a list of goals, a vision statement, or a budget dressed up as a strategy. |
| 3-4 | Bad strategy. Contains fluff (inflated language saying nothing), fails to diagnose the challenge, or lists disconnected actions. |
| 5-6 | Partial strategy. Some elements of the kernel exist but they don't cohere. Actions don't flow from the diagnosis. |
| 7-8 | Good strategy. Clear diagnosis, guiding policy that leverages advantage, coherent actions. Trade-offs are explicit. |
| 9-10 | Exceptional strategy. The kernel is tight. Every action reinforces the others. Clear what the organization will NOT do. Creates a system of activities that is hard to imitate. Porter's "activity fit" is present. |

## The Strategy Kernel (Rumelt)

Every good strategy has three elements — the "kernel":

```
┌─────────────────────────┐
│      DIAGNOSIS          │  What's really going on?
│  (the critical challenge)│  Simplify complexity into
│                         │  an actionable framing
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│    GUIDING POLICY       │  The approach chosen to
│  (the overall approach) │  deal with the challenge
│                         │  — includes trade-offs
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│   COHERENT ACTIONS      │  Specific, coordinated
│  (what we actually do)  │  steps that execute the
│                         │  policy — they reinforce
│                         │  each other
└─────────────────────────┘
```

### 1. Diagnosis

**Core concept:** The diagnosis defines the challenge. It simplifies the overwhelming complexity of reality into a manageable problem by identifying the critical factors at work. A good diagnosis is like a doctor's diagnosis — it names the disease, not the symptoms.

**Why it works:** Without diagnosis, organizations treat symptoms or address everything at once (which means addressing nothing). The diagnosis creates leverage by focusing energy on what actually matters.

**Key insights:**
- The diagnosis is NOT "we need to grow" — that's an ambition
- The diagnosis identifies the SPECIFIC obstacle or opportunity
- A good diagnosis often reframes the problem in a way that makes the solution more obvious
- The most powerful diagnoses reveal an asymmetry the organization can exploit
- If your diagnosis could apply to any company in any industry, it's too generic

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Product strategy | Diagnose why growth stalled | "Our core users love us but can't convince their teams to adopt — this is a bottom-up tool trying to sell top-down" |
| Competitive response | Diagnose competitor's actual advantage | "They're not winning on features; they're winning on distribution through their existing platform" |
| Turnaround | Name the real problem | "We don't have a product problem; we have a positioning problem — buyers don't understand what category we're in" |

**Copy patterns:**
- "The core challenge is not [symptom] — it's [root cause]"
- "We diagnosed the situation as [specific framing], which means [implication for action]"
- "Other companies in our position mistakenly treat this as a [wrong framing] problem. It's actually a [correct framing] problem."

**Ethical boundary:** Never frame the diagnosis to justify a pre-chosen solution. The diagnosis must be honest, even when it's uncomfortable.

See: [references/strategic-diagnosis.md](references/strategic-diagnosis.md)

### 2. Guiding Policy

**Core concept:** The guiding policy is the overall approach chosen to cope with the challenge identified in the diagnosis. It is not a goal or a vision — it's a direction that rules out many possible actions and focuses effort.

**Why it works:** A guiding policy creates boundaries that make decisions easier. Without it, every decision is debated from scratch. With it, teams can make autonomous decisions that are coherent because they follow the same policy.

**Key insights:**
- A guiding policy says what you WILL do AND what you WON'T do (trade-offs)
- "Focus on enterprise customers" is a guiding policy — it rules out SMB, consumer, and horizontal plays
- Porter's key insight: strategy requires trade-offs. If there's no trade-off, there's no strategy — just operational improvement
- The guiding policy should create advantage through focus, leverage, or positioning
- Test: if the opposite of your guiding policy is also reasonable, you have a real strategic choice

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Resource allocation | Use the policy to say "no" | "Our guiding policy is depth over breadth — we won't add integrations until core workflows are excellent" |
| Hiring | Align hiring with strategic direction | "We're going enterprise, so we hire enterprise sales before product-led growth engineers" |
| Feature requests | Filter through the guiding policy | "Does this request align with our policy of serving power users? If not, it's a 'not now.'" |

**Copy patterns:**
- "Our guiding policy is [policy]. This means we will [do X] and will NOT [do Y]."
- "Every decision passes the [policy] test: does this deepen our [focus area] or dilute it?"
- "We chose [approach] over [alternative] because [trade-off rationale]."

**Ethical boundary:** A guiding policy must reflect genuine trade-offs, not empty statements that sound strategic but rule nothing out. "We will focus on quality" is not a guiding policy unless you're explicitly accepting slower shipping speed, fewer features, or higher cost.

See: [references/guiding-policy.md](references/guiding-policy.md)

### 3. Coherent Actions

**Core concept:** Actions must be coordinated and mutually reinforcing. Coherence means the actions work together — each one amplifies the others. An incoherent strategy has actions pulling in different directions.

**Why it works:** Isolated actions are easy to copy. A system of coherent actions creates Porter's "activity fit" — a web of activities where each strengthens the others, making the whole much harder to replicate than any single piece.

**Key insights:**
- Coherent actions are NOT a to-do list — they must reinforce each other
- Porter's three levels of fit: (1) simple consistency, (2) activities reinforce each other, (3) optimization of effort — each level is harder to imitate
- If an action doesn't connect to other actions, it's probably not strategic
- Resource allocation IS strategy — where you put money and people reveals your real strategy, regardless of what documents say

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Roadmap review | Check that planned work is coherent | "Our actions: simplify onboarding + add team features + enterprise pricing — these cohere around a 'go enterprise' policy" |
| Activity system map | Draw connections between actions | If pricing, features, hiring, and marketing all reinforce one another, the strategy is coherent |
| Competitive defense | Design activity systems that are hard to copy | "A competitor can copy one feature, but they can't copy our entire system of content + community + certification" |

**Copy patterns:**
- "These [N] actions reinforce each other: [action A] enables [action B], which amplifies [action C]"
- "A competitor could replicate [single action], but they can't replicate the system of [action A + B + C] working together"
- "Resource allocation reflects strategy: we put [X%] of [resource] into [priority], signaling [strategic intent]"

**Ethical boundary:** Never present disconnected initiatives as coherent by drawing superficial connections. If actions don't genuinely reinforce each other, acknowledge the incoherence and fix it rather than disguising it with narrative.

See: [references/coherent-actions.md](references/coherent-actions.md)

## The Four Hallmarks of Bad Strategy (Rumelt)

| Hallmark | Definition | Example | Detection test |
|----------|-----------|---------|----------------|
| **Fluff** | Inflated, abstract language that says nothing | "We will leverage our synergistic capabilities to deliver stakeholder value" | Remove all adjectives. Is there any content left? |
| **Failure to face the challenge** | Avoids naming the problem | Strategy document talks about "opportunities" but never identifies what's actually hard | Can you state the challenge in one sentence? If not, it's being avoided |
| **Mistaking goals for strategy** | States desired outcomes without a plan | "Our strategy is to be #1 in the market" — that's an ambition, not a strategy | Does it tell you HOW, or just WHAT? |
| **Bad strategic objectives** | Long list of disconnected objectives | "Our 12 strategic priorities" — if everything is a priority, nothing is | Could you execute #5 without #1? If yes, they're not coherent |

## Strategy Stress Test: Pre-Mortem

**After completing the strategy kernel, subject it to a pre-mortem.** Assume the strategy has been executed for 18 months and has failed. What went wrong?

**Pre-mortem prompt:**
```
"It is 18 months from now. We fully committed to this strategy.
It failed. The diagnosis was wrong, the guiding policy didn't work,
or the actions didn't produce the expected results. What happened?"
```

**Generate failure scenarios across these dimensions:**

| Dimension | Pre-mortem question | Example failure |
|-----------|-------------------|-----------------|
| Diagnosis | Was the diagnosis wrong? | "We thought the problem was distribution, but it was actually product-market fit" |
| Guiding policy | Did we choose the wrong trade-off? | "We went enterprise but our product DNA was consumer — the culture couldn't adapt" |
| Coherence | Did actions pull in different directions? | "Marketing targeted SMB while product built enterprise features — wasted effort" |
| Execution | Could we actually do what we planned? | "We didn't have the engineering talent for the platform play" |
| Environment | Did the market shift? | "The regulatory change we bet on didn't happen" |
| Competition | Did competitors respond? | "Incumbent matched our key feature in 3 months — our window was shorter than assumed" |

**For each scenario:**
1. **Likelihood** (High / Medium / Low)
2. **Impact** (High / Medium / Low)
3. **Early warning signal** — what would you see in the first 3 months?
4. **Mitigation** — what changes now to reduce this risk?

**Key insight:** If the pre-mortem reveals that your diagnosis might be wrong, go back and stress-test the diagnosis before proceeding. A strategy built on a wrong diagnosis is worse than no strategy at all.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Strategy = goal-setting | Goals without a plan are wishes | Start with diagnosis, not targets |
| No trade-offs | If you're not saying "no" to something, you don't have a strategy | Name 3 things you will NOT do |
| Actions copied from competitors | Competing to be the best is not strategy — competing to be unique is (Porter) | Ask: "What activity system do we have that competitors can't easily replicate?" |
| 50-page strategy document | Long documents hide lack of clarity | If you can't state the kernel in 3 paragraphs, it's not clear |
| Strategy by committee | Consensus strategies avoid hard trade-offs | Strategy requires a decision-maker willing to make enemies |
| Never updating the diagnosis | The world changes; your diagnosis might be wrong | Revisit the diagnosis quarterly — use the pre-mortem as a trigger |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can you state the core challenge in one sentence? | Diagnosis is missing | Stop everything and diagnose the real challenge |
| Does your guiding policy rule things out? | No trade-offs = no strategy | List 3 things the guiding policy says "no" to |
| Do your actions reinforce each other? | Incoherent strategy | Draw an activity map. Remove actions that don't connect. |
| Have you run a pre-mortem? | Optimism bias unchecked | Imagine failure in 18 months — list top 5 causes |
| Could a competitor copy your strategy easily? | No activity fit / no moat | Design for Porter's second/third level of fit |

## Reference Files

- [Strategic Diagnosis](references/strategic-diagnosis.md) — How to diagnose the critical challenge, reframing techniques, asymmetry identification, common diagnostic traps, and worked examples across product, market, and organizational challenges
- [Guiding Policy Design](references/guiding-policy.md) — Trade-off identification, the "opposite test" for real strategic choices, policy-to-action translation, and examples of strong vs. weak guiding policies
- [Coherent Actions](references/coherent-actions.md) — Porter's three levels of activity fit, activity system mapping, coherence audits, resource allocation as strategy, and how to detect and fix incoherence
- [Bad Strategy Detection](references/bad-strategy-detection.md) — The four hallmarks in depth with real-world examples, fluff-detection techniques, the "goals vs. strategy" trap, and how to convert bad strategy into good strategy

## Further Reading

- [Good Strategy Bad Strategy by Richard Rumelt](https://www.amazon.com/Good-Strategy-Bad-Difference-Matters/dp/0307886239?tag=wondelai00-20)
- [What Is Strategy? by Michael Porter (HBR)](https://hbr.org/1996/11/what-is-strategy)

## About the Authors

Richard Rumelt is a professor at UCLA Anderson School of Management and one of the most influential thinkers in the strategy field. McKinsey & Company named him "strategy's strategist." Michael Porter is a professor at Harvard Business School and the founder of modern competitive strategy. His frameworks (Five Forces, Value Chain, Generic Strategies) are taught in every business school in the world.
