---
name: cynefin-framework
description: Apply the Cynefin framework whenever the user is deciding how to approach a problem, choosing between solutions, or asking why a previous solution didn't work. Triggers on phrases like "how should we approach this?", "which solution is better?", "we tried X but it didn't work", "this is complicated", "this feels unpredictable", "we don't know what to do", "what's the right process here?", or when evaluating whether to apply best practices, run experiments, or call in experts. Also trigger when the user is applying a structured/rigid process to something that might be complex or chaotic — this is a common mismatch that Cynefin catches. Use this skill before recommending any solution approach.
---

# Cynefin Framework

**Core principle**: Before applying any solution, classify the problem domain. The right action in one domain is the wrong action in another. Misclassifying the domain is one of the most common causes of failed interventions.

---

## The Five Domains

### 1. 🟢 Clear (formerly "Simple")
**Relationship**: Cause and effect are obvious to everyone.
**Nature**: Best practices exist and are well-known.
**Approach**: **Sense → Categorize → Respond**
- Apply the known best practice
- Automate where possible
- Don't over-complicate it

**Signs you're here**: The answer is obvious. Anyone competent would do the same thing.

**Danger**: Complacency. Clear domains can suddenly become chaotic if conditions change and nobody noticed.

**Examples**: Resetting a password, deploying a known-working config, following a checklist.

---

### 2. 🔵 Complicated
**Relationship**: Cause and effect exist but require analysis or expertise to see.
**Nature**: Multiple right answers exist; good practice (not best practice).
**Approach**: **Sense → Analyze → Respond**
- Bring in experts or do analysis
- Evaluate trade-offs between valid options
- Allow time for assessment before acting

**Signs you're here**: You need an expert, but once they analyze it, the answer becomes clear. There's a knowable right answer.

**Danger**: Expert overconfidence. Experts can mistake complicated for clear and stop questioning assumptions.

**Examples**: Software architecture decisions, performance tuning, medical diagnosis, legal strategy.

---

### 3. 🟡 Complex
**Relationship**: Cause and effect are only visible **in retrospect**. You can't predict outcomes.
**Nature**: Emergent practice — no "right answer" exists in advance.
**Approach**: **Probe → Sense → Respond**
- Run safe-to-fail experiments (small, reversible, parallel)
- Amplify what works, dampen what doesn't
- Expect and embrace emergence
- Don't plan for a single outcome

**Signs you're here**: Experts disagree. Past data is unreliable. The system involves human behavior, social dynamics, or high interconnectedness.

**Danger**: Applying complicated or clear approaches (best practices, expert analysis, big-bang solutions) to complex problems. This is the most common mistake.

**Examples**: Product-market fit discovery, organizational culture change, user behavior patterns, AI system behavior, team dynamics.

---

### 4. 🔴 Chaotic
**Relationship**: No discernible cause and effect. The system is in crisis.
**Nature**: Novel practice — act first to stabilize.
**Approach**: **Act → Sense → Respond**
- Take immediate action to reduce harm and establish order
- Don't wait for analysis — the situation is changing faster than analysis can help
- Move to complex or complicated once stability is achieved

**Signs you're here**: Crisis. System is actively failing. No time for deliberation.

**Danger**: Staying in chaotic mode too long. Once the crisis is contained, move to a more deliberate approach.

**Examples**: Production outage, security breach, public crisis, team breakdown.

---

### 5. ⚫ Disorder (the center)
**Relationship**: Unknown. You don't know which domain you're in.
**Approach**: Break the situation into parts and classify each one.
- Multiple people will interpret the situation through their own domain lens (causing conflict)
- Get clarity before acting

---

## Output Format

### 🗺️ Domain Classification
- **Assessed domain**: Clear / Complicated / Complex / Chaotic / Disorder
- **Confidence**: High / Medium / Low
- **Key signals** that led to this classification
- **Alternative interpretation**: Could this be misclassified? What would that imply?

### ⚠️ Domain Mismatch Check
Is the user (or current plan) applying an approach from the **wrong domain**?

| Current approach | Actual domain | Mismatch risk |
|-----------------|---------------|---------------|
| Best practice playbook | Complex | High — will fail |
| Big analysis, single solution | Chaotic | High — too slow |
| Experiments / probing | Clear | Waste of time |

### 🎯 Recommended Approach
Based on the domain:
- **Clear**: Apply best practice [name it]. Consider automating.
- **Complicated**: Engage expert analysis. Evaluate trade-offs between [option A] and [option B].
- **Complex**: Design 2–3 safe-to-fail experiments. Define what "amplify" and "dampen" signals look like.
- **Chaotic**: Act immediately on [specific stabilizing action]. Reassess domain once stable.

### 🔁 Domain Transitions to Watch
- Is this domain **shifting**? (e.g., a complicated situation becoming complex due to new uncertainty)
- What would cause the situation to move into **chaos**?
- What's the path toward **clear** once this is resolved?

---

## Practical Heuristics

- **If experts disagree** → probably Complex, not Complicated
- **If it involves people and behavior at scale** → probably Complex
- **If it's urgent and breaking** → probably Chaotic; act first
- **If there's a known playbook** → probably Clear or Complicated
- **If past solutions stopped working** → domain may have shifted

---

## The Most Common Mistake
Treating a **Complex** problem as **Complicated**: hiring a consultant to define "the right answer" and then executing a big plan — when the system is actually emergent and unpredictable. The result: the plan doesn't work, more consultants are hired, the plan gets bigger, it still doesn't work.

**Fix**: Run small experiments instead. Let patterns emerge. Amplify what works.
