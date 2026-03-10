---
name: cognitive-bias-detection
description: Apply cognitive bias detection whenever the user (or Claude itself) is making an evaluation, recommendation, or decision that could be silently distorted by systematic thinking errors. Triggers on phrases like "I'm pretty sure", "obviously", "everyone agrees", "we already invested so much", "this has always worked", "just one more try", "I knew it", "the data confirms what we thought", "we can't go back now", or when analysis feels suspiciously aligned with what someone wanted to hear. Also trigger proactively when evaluating high-stakes decisions, plans with significant sunk costs, or conclusions that conveniently support the evaluator's existing position. The goal is not to paralyze — it's to flag where reasoning may be compromised so it can be corrected.
---

# Cognitive Bias Detection

**Core principle**: Human (and AI) reasoning is systematically distorted by cognitive biases — predictable errors in judgment that operate below conscious awareness. The most dangerous analyses are the ones that *feel* most certain. This skill audits the reasoning process itself, not just the conclusions.

---

## The Most Impactful Biases to Check

### Evaluation & Decision Biases

**Confirmation Bias**
Seeking, interpreting, and remembering information that confirms existing beliefs. Disconfirming evidence is dismissed or reframed.
- *Signal*: "The data confirms what we suspected." / Evidence against the conclusion gets less attention than evidence for it.
- *Fix*: Actively seek the strongest case *against* the conclusion. Assign someone to argue the opposite.

**Anchoring**
Over-weighting the first number, estimate, or framing encountered.
- *Signal*: Estimates cluster around an initial figure. Comparisons are made relative to a reference point that was never validated.
- *Fix*: Generate estimates independently before seeing others. Ask "what would this look like if the anchor didn't exist?"

**Availability Heuristic**
Overweighting recent, memorable, or vivid events when estimating likelihood.
- *Signal*: "We just had an incident like this" leads to overestimating its probability. Quiet failures are underweighted.
- *Fix*: Use base rates. Ask "how often does this actually happen over a long period?"

**Sunk Cost Fallacy**
Continuing a course of action because of past investment, not future value.
- *Signal*: "We've already put 6 months into this." / Reluctance to abandon despite evidence it's not working.
- *Fix*: Ask "if we hadn't invested anything yet, would we start this today?"

**Planning Fallacy**
Systematic underestimation of time, cost, and risk — even when we know past projects ran over.
- *Signal*: Estimates feel optimistic. No buffer for unknowns. Past projects are treated as exceptions.
- *Fix*: Use reference class forecasting: how long did similar projects actually take?

### Social & Group Biases

**Groupthink**
Desire for group harmony overrides realistic appraisal. Dissent is suppressed.
- *Signal*: Everyone agrees quickly. No one plays devil's advocate. Contrarian views are dismissed socially.
- *Fix*: Assign a formal devil's advocate. Ask people to write independent opinions before group discussion.

**Authority Bias**
Overweighting the opinion of someone perceived as an authority, independent of their actual expertise.
- *Signal*: "The CTO/senior person thinks X, so it must be right." Analysis stops when authority speaks.
- *Fix*: Evaluate the argument on its merits, not its source. Ask "what's the evidence, separate from who said it?"

**In-group Bias**
Favoring people, ideas, and solutions associated with one's own group.
- *Signal*: Solutions from the team are evaluated more generously than identical solutions from outside.
- *Fix*: Blind evaluation where possible. Ask "would we accept this if a competitor proposed it?"

### Framing & Perception Biases

**Framing Effect**
The same information leads to different decisions depending on how it's presented (gain vs. loss framing).
- *Signal*: "90% success rate" vs. "10% failure rate" trigger different reactions to the same fact.
- *Fix*: Reframe every option in multiple ways before deciding. Check if the decision changes.

**Survivorship Bias**
Drawing conclusions from visible successes while ignoring invisible failures.
- *Signal*: "Company X did Y and succeeded" — but how many companies did Y and failed?
- *Fix*: Actively seek the failure cases. Ask "what don't we see because they didn't survive?"

**Dunning-Kruger Effect**
Low competence in a domain produces overconfidence; high competence produces underconfidence.
- *Signal*: Extreme certainty in a novel or complex domain. Or excessive hedging from a genuine expert.
- *Fix*: Calibrate confidence against demonstrated track record in this specific domain.

**Recency Bias**
Overweighting recent data and underweighting long-term patterns.
- *Signal*: Last quarter's results dominate the analysis. Historical base rates are ignored.
- *Fix*: Extend the time window. Look at multi-year trends, not just recent performance.

---

## Output Format

### 🔍 Bias Scan Results
For each bias checked:
| Bias | Present? | Signal Observed | Severity |
|------|----------|----------------|----------|
| Confirmation Bias | Yes / Possible / No | [Evidence] | Low/Med/High |
| Sunk Cost | Yes / Possible / No | [Evidence] | Low/Med/High |
| ... | | | |

### ⚠️ High-Risk Findings
For each high-severity bias detected:
- **Bias**: Name and brief description
- **How it's showing up**: Specific evidence in the reasoning or decision
- **What it's distorting**: What conclusion or estimate is being skewed, and in which direction?
- **Debiasing move**: Concrete action to correct or validate

### 🧹 Debiased Re-evaluation
After flagging biases, offer a corrected version of the analysis:
- What changes if we remove the bias?
- What evidence is actually strong vs. inflated by bias?
- Does the conclusion still hold?

### 🎯 Confidence Calibration
- What is the actual confidence level warranted by the evidence, absent bias?
- What would need to be true to justify higher confidence?
- What's the most important thing to validate before committing?

---

## Meta-Check: Is Claude Biased Here?

This skill also applies to Claude's own analysis. When generating evaluations, check:
- Am I confirming what the user wants to hear? (sycophancy / confirmation bias)
- Am I anchoring to the first framing the user gave me?
- Am I overweighting the most vivid or recent example?
- Am I assuming the user's group/team/approach is better without evidence?

If yes to any — flag it and correct.

---

## Thinking Triggers

- *"How would this analysis look if we had concluded the opposite from the start?"*
- *"What's the strongest evidence against the current conclusion?"*
- *"Are we continuing because it's right, or because we've invested too much to stop?"*
- *"Who benefits from this conclusion, and are they also the ones evaluating it?"*
- *"If a stranger reviewed this reasoning, what would they say we're missing?"*
