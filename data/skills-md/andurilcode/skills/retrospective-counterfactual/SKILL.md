---
name: retrospective-counterfactual
description: Apply retrospective and counterfactual reasoning whenever something has already happened and the user needs to understand why — or learn from it to improve future decisions. Triggers on phrases like "what went wrong?", "why did this fail?", "post-mortem", "incident review", "we just shipped and it didn't go well", "let's debrief", "what would we have done differently?", "should we have seen this coming?", "what did we miss?", "what would have happened if we'd done X instead?", or any after-the-fact analysis of a completed event. Also trigger to prevent survivorship bias in success analyses — "what made this succeed?" deserves as much causal scrutiny as failure. Look backwards with as much rigor as you look forward.
---

# Retrospective & Counterfactual Reasoning

**Core principle**: Looking backwards is not about blame — it's about extracting signal. A well-run retrospective or post-mortem separates what was predictable from what was genuinely unforeseeable, identifies what conditions made failure likely, and generates changes that prevent the same failure mode from recurring under different surface conditions.

Counterfactual reasoning — "what would have happened if we'd done X?" — is the backward-looking complement to the forward-looking pre-mortem. Both require the same discipline: rigorous causal thinking, not narrative construction after the fact.

---

## Two Modes

### Mode 1: Post-Mortem / Retrospective
*Something happened. What caused it and what do we change?*

Focus: Causal reconstruction, systemic learning, forward-looking change.

### Mode 2: Counterfactual Analysis
*What would have happened if we'd made a different decision?*

Focus: Decision quality assessment, calibration, learning from near-misses and successes.

---

## Mode 1: Post-Mortem Process

### Step 1: Reconstruct the Timeline
Before analyzing, establish what actually happened — in sequence, with timestamps where possible:
- What was the state before the event?
- What were the triggering conditions?
- What was the sequence of events?
- What was the decision point (if any) where the outcome could have diverged?

**Separate facts from interpretations** at this stage. "The deployment failed at 14:32" is a fact. "The team didn't notice in time" is an interpretation — needs evidence.

### Step 2: Identify Contributing Causes
Use layered causal analysis:
- **Immediate cause**: The direct trigger (the thing that "broke")
- **Enabling conditions**: What made the system vulnerable to that trigger
- **Root causes**: The systemic conditions that produced the enabling conditions
- **Contributing factors**: Context that increased probability or severity

Avoid stopping at the immediate cause — it's almost always the least actionable finding.

**Avoid blame by design**: Replace "person X failed to do Y" with "the system didn't ensure Y happened." People operate within systems. The question is what in the system failed.

### Step 3: Classify What Was Knowable
For each contributing cause, ask:
- **Predictable**: Was this foreseeable given available information? Was it foreseen by anyone?
- **Detectable**: Could monitoring or process have surfaced this earlier?
- **Preventable**: Was there a plausible intervention that would have avoided this?
- **Unforeseeable**: Genuinely novel or outside reasonable expectation?

This classification determines the quality of the corrective actions:
- Predictable + Preventable = highest-priority systemic fix
- Predictable + Not Prevented = process or incentive problem
- Detectable but Not Detected = monitoring/observability problem
- Genuinely Unforeseeable = resilience and recovery design problem

### Step 4: Generate Corrective Actions
For each systemic finding:
- What specifically changes?
- What does "done" look like?
- Who owns it?
- How do we verify it worked?

**Corrective action quality test**: If the same team, same system, same situation — does this change prevent the same failure? If yes only for this exact scenario, the action is too narrow.

---

## Mode 2: Counterfactual Analysis

### The Core Question
*"What would have happened if decision D had been different?"*

This requires:
1. Identifying the specific decision or condition to vary
2. Reasoning about the causal chain that would have followed
3. Being honest about uncertainty — counterfactuals are inherently speculative

### Counterfactual Validity Rules
A useful counterfactual is:
- **Tractable**: The alternative decision was actually available (not hindsight-only)
- **Isolated**: Only one factor is varied at a time (otherwise you're comparing incomparables)
- **Causal**: The alternative path follows from the changed decision through a plausible causal mechanism

A poor counterfactual:
- Assumes information that wasn't available at decision time
- Changes multiple things simultaneously
- Is constructed to justify a preferred conclusion

### Decision Quality vs. Outcome Quality
A critical distinction:

**Bad decision, good outcome**: Survivorship bias risk. "It worked" doesn't validate the decision process.
**Good decision, bad outcome**: The process was right; the outcome was unlucky. Don't over-update on this.
**Bad decision, bad outcome**: The outcome was predictable.
**Good decision, bad outcome (systematically)**: The model of the world was wrong — update the model.

Evaluate decisions by the quality of reasoning *at the time*, not by the outcome.

---

## Output Format

### 📋 Event Summary
- **What happened**: [Factual, sequenced description]
- **Impact**: [Quantified where possible]
- **Timeline**: [Key moments from precondition to resolution]

### 🔍 Causal Analysis

**Immediate cause**: [The direct trigger]

**Enabling conditions**: [What made the system vulnerable]

**Root causes**: [Systemic conditions]

**Contributing factors**: [Context that amplified probability or severity]

### 🗂️ Knowability Classification
| Cause | Predictable? | Detectable? | Preventable? | Classification |
|-------|-------------|------------|--------------|----------------|
| [Cause 1] | Yes/No/Partially | Yes/No | Yes/No | [Type] |

### 🔄 Counterfactual Scenarios (if applicable)
For each decision point worth examining:
- **Decision made**: [What was decided]
- **Alternative considered**: [What could have been done instead]
- **Counterfactual path**: [What would plausibly have followed]
- **Confidence in counterfactual**: [High / Medium / Low — and why]
- **Decision quality assessment**: [Was the original decision reasonable given available information?]

### 🛠️ Corrective Actions
| Finding | Action | Owner | Verification | Timeline |
|---------|--------|-------|-------------|---------|
| [Systemic finding] | [Specific change] | [Who] | [How we know it worked] | [When] |

### 📚 Learning Extraction
- **What does this tell us about the system** (beyond this specific event)?
- **What assumption was wrong** — and should be updated?
- **What category of problem does this represent** — and are there other instances?
- **What early warning signal existed** that we should have been monitoring?

---

## Anti-Patterns to Avoid

**Hindsight bias**: "We should have known" — without asking whether the information was actually available and acted on at the time.

**Blame focus**: Naming people as causes rather than the systemic conditions that made their actions likely.

**Single-cause narrative**: Incidents almost always have multiple contributing causes. A single neat story is usually incomplete.

**Action theater**: Generating long lists of corrective actions, few of which get done. Better: 2–3 high-quality, owned, verified changes.

**Success blindness**: Only running retrospectives on failures. Successes with good outcomes due to luck are as worth examining as failures.

**Stopping at the immediate cause**: Fixing the last link in the chain without addressing the conditions that made the chain possible.

---

## Thinking Triggers

- *"Was this predictable? By whom? Why wasn't it acted on?"*
- *"What systemic condition made this failure possible — not just probable?"*
- *"If the same situation arose next month with a different person, would the outcome be different? Why?"*
- *"What's the difference between the decision process and the decision outcome here?"*
- *"What would we have needed to know, at decision time, to choose differently?"*
- *"Are we fixing the last event, or the class of events?"*
