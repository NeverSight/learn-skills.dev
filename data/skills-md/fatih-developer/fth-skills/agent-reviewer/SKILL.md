---
name: agent-reviewer
description: After an agentic task completes, perform a retrospective analysis across 6 dimensions (goal alignment, efficiency, decision quality, error handling, communication, reusability). Score performance, identify inefficiency patterns, evaluate skill usage, and produce actionable improvement recommendations. Triggers on "how did it go", "retrospective", "review performance", "what could be better", or after any long agentic task completes.
---

# Agent Reviewer Protocol

Task is done — now look back. What went well, what went wrong, what should be different next time? Goal: never repeat the same mistake and continuously improve skills and processes.

**Core principle:** Retrospectives are painful but necessary. A good agent evaluates itself.

---

## 6 Review Dimensions

### 1. Goal Alignment
Did the result match the original intent?
- Was the user's actual request met?
- Did scope creep occur?
- Over-delivery or under-delivery?

### 2. Efficiency
Did the task take longer than necessary?
- Unnecessary tool calls?
- Repeated operations?
- Sequential steps that could have been parallel?
- Token/resource waste?

### 3. Decision Quality
Were decisions well-reasoned?
- Were assumptions verified?
- Were alternatives considered?
- Did early decisions cause later problems?

### 4. Error Handling
How were errors addressed?
- Detected quickly?
- Right strategy applied?
- Same error repeated?

### 5. Communication
How was user interaction quality?
- Unnecessary confirmations requested?
- Critical information missing at key points?
- Too many or too few questions?

### 6. Reusability
Can lessons from this task transfer to the next?
- General patterns discovered?
- Which skills were missing or insufficient?
- Which decisions should become standard?

---

## Finding Severity

| Severity | Meaning | Action |
|----------|---------|--------|
| CRITICAL | Endangered the task or significantly reduced quality | Must fix |
| MODERATE | Created inefficiency but didn't break the result | Improve |
| POSITIVE | Something that went better than expected | Repeat, standardize |

---

## Output Format

```
AGENT REVIEWER — Task Retrospective
Task     : [task name]
Score    : X/10
Findings : N critical | N moderate | N positive

## Dimension Scores

| Dimension | Score | Summary |
|-----------|-------|---------|
| Goal Alignment | X/10 | ... |
| Efficiency | X/10 | ... |
| Decision Quality | X/10 | ... |
| Error Handling | X/10 | ... |
| Communication | X/10 | ... |
| Reusability | X/10 | ... |
| **Overall** | **X/10** | |

## Critical Findings
[If any — what happened, why critical, how to prevent]

## Improvement Areas
[Inefficiencies, missed opportunities]

## What Went Well
[Decisions and approaches worth repeating]

## Action Items

### For Next Task
1. [Concrete change — what to do]
2. [Concrete change]

### Skill / Process Improvement
1. [Which skill should be updated / added]
2. [Which pattern should be standardized]

## Lessons Learned
[Items a future agent instance should know — candidates for memory-ledger]
```

---

## Inefficiency Patterns — Auto-Detect

Scan the task history for these patterns:

| Pattern | Symptom | Fix |
|---------|---------|-----|
| Repeated tool call | Same file/API read 2+ times | Cache it |
| Unnecessary confirmation | Low-risk step triggered approval | Adjust checkpoint-guardian threshold |
| Late assumption discovery | "Actually it should be..." after error | Trigger assumption-checker earlier |
| Sequential parallel steps | Independent steps ran sequentially | Use parallel-planner |
| Blind retry | Logic error treated as transient | Fix error-recovery categorization |
| Context loss | Previous step info forgotten | Memory-ledger not updated |
| Over-decomposition | 2-step task split into 8 | Adjust task-decomposer granularity |

---

## Skill Performance Evaluation

Evaluate skills used during the task:

```
## Skills Used

| Skill | Used? | Effective? | Notes |
|-------|-------|------------|-------|
| task-decomposer | Yes/No | Good/Fair/Poor | ... |
| checkpoint-guardian | Yes/No | Good/Fair/Poor | ... |
| assumption-checker | Yes/No | Good/Fair/Poor | ... |
| tool-selector | Yes/No | Good/Fair/Poor | ... |
| parallel-planner | Yes/No | Good/Fair/Poor | ... |
| error-recovery | Yes/No | Good/Fair/Poor | ... |
| memory-ledger | Yes/No | Good/Fair/Poor | ... |
| output-critic | Yes/No | Good/Fair/Poor | ... |

Missing / untriggered skills and why?
```

---

## When to Skip

- Task was single-step or under 5 minutes
- Prototype / experimental task
- User said "no retrospective needed"

---

## Guardrails

- **Be honest, not kind** — the value is in finding problems, not hiding them.
- **Concrete suggestions only** — "do better" is useless; "cache file reads to avoid 3 redundant calls" is actionable.
- **Cross-skill**: this is the ecosystem's feedback loop — findings here should update other skills and processes.
