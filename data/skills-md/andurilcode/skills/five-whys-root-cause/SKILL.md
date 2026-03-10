---
name: five-whys-root-cause
description: Apply 5 Whys and root cause analysis whenever a problem keeps recurring, a fix didn't hold, or the user is trying to understand why something went wrong. Triggers on phrases like "this keeps happening", "we fixed it but it came back", "why did this fail?", "what caused X?", "we keep having this issue", "post-mortem", "incident review", "the same bug appeared again", "why isn't this working?", or any situation where symptoms have been identified but root causes haven't. Also trigger when a proposed solution feels like a workaround rather than a fix — this skill helps validate whether the real cause has been found. Don't let the agent stop at symptoms.
---

# 5 Whys & Root Cause Analysis

**Core principle**: Every visible problem is a symptom. The root cause is the systemic condition that makes the symptom inevitable. Fix the symptom and it returns. Fix the root cause and the symptom disappears — along with related ones you haven't noticed yet.

---

## The 5 Whys Method

Start with the problem statement. Ask "why did this happen?" Keep asking why until you reach a cause you can actually fix — one that is **actionable**, **systemic**, and **doesn't have another why behind it**.

### The Process

```
Problem: [State clearly and specifically]
  Why 1: [Immediate cause]
    Why 2: [Cause of the cause]
      Why 3: [Deeper cause]
        Why 4: [Systemic cause]
          Why 5: [Root cause — systemic, actionable]
```

**Stop when you reach a cause that is:**
- Actionable (you can actually change it)
- Systemic (fixing it prevents recurrence)
- Not just another symptom

**Don't stop when:**
- The answer is "human error" (that's a symptom — why did human error occur?)
- The answer is "bad luck" (luck is not a root cause)
- The answer blames a person (people operate within systems — blame the system)

---

## Common Root Cause Categories

| Category | Examples |
|----------|---------|
| **Process gap** | No process existed, process was unclear, process wasn't followed |
| **Knowledge gap** | Team didn't know X, information wasn't shared, no documentation |
| **Tooling gap** | Wrong tool, missing tool, tool not configured correctly |
| **Incentive misalignment** | Rewards and desired behavior point in different directions |
| **Feedback loop missing** | No signal that something was going wrong |
| **Assumption failure** | A belief about the system was wrong |
| **Capacity constraint** | Not enough time, people, or resources to do it right |
| **Communication failure** | Decision made without relevant parties knowing |

---

## Multi-Branch Analysis

The 5 Whys often reveals **multiple root causes** (not one). Use branching when you hit a "why" with more than one answer:

```
Problem: Deployment failed
  Why? → Tests didn't catch the bug
    Branch A: Why? → Test coverage was insufficient
      Why? → No policy requiring coverage thresholds
        Root cause A: No coverage gate in CI pipeline
    Branch B: Why? → Test environment differed from production
      Why? → Config was not environment-parity checked
        Root cause B: No config parity validation step
```

Each branch may have a different fix.

---

## Output Format

### 🔍 Problem Statement
Restate the problem **specifically and observably**:
- What happened?
- When? How often?
- What's the impact?
- What did *not* happen (that should have)?

### 🪢 The Why Chain(s)
Present the full chain(s) from symptom to root cause. Use branching if multiple causes exist.

### 🎯 Root Cause(s) Identified
For each root cause:
- **Statement**: Clear, systemic description
- **Category**: Process / Knowledge / Tooling / Incentive / Feedback / Assumption / Capacity / Communication
- **Recurrence risk**: How likely is this to cause the same or similar problem again without a fix?

### 🚫 Rejected Explanations
List causes that were considered but rejected, and why:
- "Human error" → Why did it occur? What enabled it?
- "One-off event" → Why was the system vulnerable to it?
- Personal blame → Replaced with systemic explanation

### 🛠️ Corrective Actions
For each root cause, a specific countermeasure:
- **Action**: What exactly changes?
- **Owner**: Who is responsible?
- **Verification**: How do we know the fix worked?
- **Timeline**: When?

### 📊 Recurrence Prevention
- What monitoring/alerting detects this root cause activating again?
- What review process catches this category of problem in the future?
- Is this root cause related to any other known issues? (often one root cause explains multiple symptoms)

---

## Quality Checks for Root Causes

Before accepting a root cause, verify:
- ✅ **Reversibility test**: If we fixed this, would the problem go away?
- ✅ **Recurrence test**: If this root cause is present, does the problem reliably occur?
- ✅ **Actionability test**: Can we actually change this?
- ✅ **Systemic test**: Does this explain the pattern, not just the one incident?
- ❌ **Blame test**: If the answer names a person as the root cause, keep asking why

---

## Common Traps to Avoid

- **Stopping too early**: "The developer made a mistake" is not a root cause
- **Single-cause bias**: Most failures have 2–4 contributing root causes
- **Hindsight framing**: "They should have known" — why didn't the system make it knowable?
- **Fixing the last step**: Catching the bug in prod is not the fix; preventing the condition that allowed it is
- **Symptom substitution**: Fixing one symptom without the root cause → a different symptom appears

---

## Example Walk-Through

**Problem**: The agent pipeline produced incorrect output on 30% of runs last week.

| Level | Why? | Answer |
|-------|------|--------|
| Why 1 | Why incorrect output? | Agent used stale context from prior step |
| Why 2 | Why stale context? | Context was not cleared between runs |
| Why 3 | Why not cleared? | No reset mechanism in handoff protocol |
| Why 4 | Why no reset mechanism? | Handoff spec was never formalized |
| Why 5 | Why never formalized? | No process requires handoff specs before agent goes to production |

**Root cause**: No policy requiring formalized handoff specs before production deployment.

**Fix**: Add handoff spec requirement to the agent deployment checklist.
