---
name: pm-jobs-to-be-done
description: Jobs-to-be-Done framework for understanding customer motivations and building solutions that get "hired".
triggers:
  - jobs to be done
  - jtbd
  - customer jobs
  - hiring criteria
  - firing criteria
disable-model-invocation: true
---

# Jobs-to-be-Done (JTBD)

Framework for understanding why customers "hire" and "fire" solutions.

## Job Statement Format

```
When [situation/trigger],
I want to [motivation/goal],
so I can [expected outcome].
```

**Example:**
```
When I receive customer feedback after a product launch,
I want to quickly identify common themes,
so I can prioritize fixes before the next sprint.
```

## JTBD Canvas

```markdown
## Job: [Core functional job]

### Trigger/Situation
- When does this job arise?
- What context are they in?

### Functional Job (what they're trying to do)
[Action verb] + [object] + [clarifying context]
Example: "Organize customer feedback by theme before weekly product meeting"

### Emotional Job (how they want to feel)
- Feel [emotion] about [situation]
Example: "Feel confident presenting insights to leadership"

### Social Job (how they want to be perceived)
- Be seen as [perception] by [audience]
Example: "Be seen as data-driven by the exec team"

### Current Solutions
| Solution | Hiring Criteria | Firing Criteria |
|----------|-----------------|-----------------|
| [Tool/workaround] | [Why they use it] | [Why they'd stop] |

### Outcome Metrics
What does "job done well" look like?
- Speed: [Complete X in Y minutes]
- Quality: [Z accuracy/completeness]
- Confidence: [Feel certain about decision]
```

## Hiring & Firing Criteria

**Hiring Criteria** (why they start using):
- Solves the functional job better
- Makes them feel the emotional job
- Improves their social perception
- Lower switching cost than pain of status quo

**Firing Criteria** (why they stop using):
- Job changes or goes away
- Better solution emerges
- Switching cost decreases
- Pain of current solution exceeds benefit

## Job Mapping Questions

```markdown
### Situation
- "When did you first realize you needed something like this?"
- "What was happening right before you started looking?"

### Push/Pull Forces
- "What made the old way unacceptable?" (push away)
- "What attracted you to the new solution?" (pull toward)

### Anxiety/Habit
- "What concerns did you have about switching?"
- "What kept you using the old way for so long?"
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Too broad | "Manage my business" | Add context/constraints |
| Solution-focused | "Use a spreadsheet" | Focus on outcome |
| Missing emotion | Just functional | Add emotional/social jobs |
| Ignoring context | Generic job | Specify situation/trigger |
