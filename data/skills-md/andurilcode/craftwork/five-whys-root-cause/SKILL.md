---
name: five-whys-root-cause
description: Apply 5 Whys and root cause analysis whenever a problem keeps recurring, a fix didn't hold, or the user is trying to understand why something went wrong. Triggers on phrases like "this keeps happening", "we fixed it but it came back", "why did this fail?", "what caused X?", "we keep having this issue", "post-mortem", "incident review", "the same bug appeared again", "why isn't this working?", or any situation where symptoms have been identified but root causes haven't. Also trigger when a proposed solution feels like a workaround rather than a fix — this skill helps validate whether the real cause has been found. Don't let the agent stop at symptoms.
---

# 5 Whys & Root Cause Analysis

**Core**: Visible problems are symptoms. The root cause is the systemic condition that makes the symptom inevitable. Fix the symptom and it returns. Fix the root cause and the symptom (plus related ones) disappears.

---

## The 5 Whys Method

State the problem. Ask "why?" Keep asking until you reach a cause that is **actionable**, **systemic**, and has no further "why" behind it.

```
Problem: [Specific statement]
  Why 1: [Immediate cause]
    Why 2: [Cause of the cause]
      Why 3: [Deeper cause]
        Why 4: [Systemic cause]
          Why 5: [Root cause]
```

**Stop when** the cause is actionable, systemic, and not another symptom.

**Don't stop at:**
- "Human error" — why did it occur?
- "Bad luck" — luck is not a root cause
- Personal blame — people operate within systems; blame the system

---

## Common Root Cause Categories

| Category | Examples |
|----------|---------|
| **Process gap** | No process, unclear process, process not followed |
| **Knowledge gap** | Team didn't know X, no documentation |
| **Tooling gap** | Wrong/missing tool, misconfigured |
| **Incentive misalignment** | Rewards point away from desired behavior |
| **Feedback loop missing** | No signal that something was going wrong |
| **Assumption failure** | A belief about the system was wrong |
| **Capacity constraint** | Not enough time/people/resources to do it right |
| **Communication failure** | Decision made without relevant parties knowing |

---

## Multi-Branch Analysis

5 Whys often reveals **multiple root causes**. Branch when a "why" has more than one answer:

```
Problem: Deployment failed
  Why? → Tests didn't catch the bug
    A: → Test coverage insufficient → No coverage policy → No CI coverage gate
    B: → Test env differed from prod → No parity check → No config parity step
```

Each branch may have a different fix.

---

## Output Format

### 🔍 Problem Statement
What happened? When/how often? Impact? What did *not* happen that should have?

### 🪢 Why Chain(s)
Full chain(s) from symptom to root cause. Branch if multiple causes.

### 🎯 Root Cause(s)
For each:
- **Statement**: Clear, systemic
- **Category**: Process / Knowledge / Tooling / Incentive / Feedback / Assumption / Capacity / Communication
- **Recurrence risk**: Likelihood of repeat without fix

### 🚫 Rejected Explanations
- "Human error" → why did it occur, what enabled it?
- "One-off" → why was the system vulnerable?
- Personal blame → replaced with systemic explanation

### 🛠️ Corrective Actions
For each root cause: **Action**, **Owner**, **Verification**, **Timeline**.

### 📊 Recurrence Prevention
Monitoring/alerting that detects this root cause again. Review process to catch this category. Related known issues (one root cause often explains multiple symptoms).

---

## Quality Checks

- ✅ **Reversibility**: If fixed, would the problem go away?
- ✅ **Recurrence**: If this cause is present, does the problem reliably occur?
- ✅ **Actionability**: Can we change it?
- ✅ **Systemic**: Explains the pattern, not just one incident?
- ❌ **Blame**: Names a person → keep asking why

---

## Common Traps

- **Stopping too early**: "Developer made a mistake" is not a root cause
- **Single-cause bias**: Most failures have 2–4 contributing root causes
- **Hindsight framing**: "They should have known" — why didn't the system make it knowable?
- **Fixing the last step**: Catching a bug in prod isn't the fix; preventing the condition is
- **Symptom substitution**: Fix one symptom without root cause → different symptom appears

---

## Example

**Problem**: Agent pipeline produced incorrect output on 30% of runs last week.

| Why | Answer |
|-----|--------|
| 1. Why incorrect? | Stale context from prior step |
| 2. Why stale? | Context not cleared between runs |
| 3. Why not cleared? | No reset mechanism in handoff protocol |
| 4. Why no mechanism? | Handoff spec never formalized |
| 5. Why? | No process requires handoff specs before production |

**Root cause**: No policy requiring formalized handoff specs before production deployment.
**Fix**: Add handoff spec to the agent deployment checklist.
