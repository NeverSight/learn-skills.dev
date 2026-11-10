---
name: postmortem
description: "Deliver a structured post-mortem after incidents, mistakes, or stuck sessions. Use when the user requests a structured post-mortem after incidents, mistakes, or stuck sessions."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# Lessons Learned: Structured Retrospective

Analyse incidents using a structured framework, identify root causes, and encode preventive measures directly into skills, guards, or documentation. The goal is systematic improvement, not blame.

## When to Use

- After incidents, mistakes, rollbacks, or near-misses
- When the user says "what went wrong", "lessons learned", "post-mortem", "retrospective", or "how do we prevent this"
- After a stuck session where significant time was lost
- After a wrong-approach event (plan existed but execution diverged)

## Process

### Phase 1: Incident Definition

Capture the facts first, analysis later.

```markdown
## Incident Summary

**What happened:** [Factual description]
**When:** [Date/time]
**Impact:** [What was affected, scope]
**Resolution:** [How it was fixed/rolled back]
**Time to resolution:** [How long to fix]
```

### Phase 2: Timeline Reconstruction

Build a chronological sequence of events:

| Time | Action | Actor | Outcome |
|------|--------|-------|---------|
| HH:MM | [What was done] | [Claude/User] | [Result] |

Key questions:
- What was the trigger?
- Where did the sequence diverge from expected?
- What was the point of no return?

### Phase 3: Root Cause Analysis (5 Whys)

```
1. Why did [incident] happen?
   → Because [immediate cause]

2. Why did [immediate cause] happen?
   → Because [deeper cause]

3. Why did [deeper cause] happen?
   → Because [systemic issue]

4. Why did [systemic issue] exist?
   → Because [process gap]

5. Why did [process gap] exist?
   → Because [root cause]
```

Stop when you reach a cause that can be addressed by a concrete change to the system (skill, rule, hook, doc).

### Phase 4: Contributing Factors

Identify all factors, not just the root cause:

| Category | Factor | Contribution |
|----------|--------|--------------|
| **Process** | Missing checkpoint, unclear workflow | [How it contributed] |
| **Communication** | Ambiguous instructions, assumed consent | [How it contributed] |
| **Technical** | Missing guard, no validation | [How it contributed] |
| **Context** | Session continuation, prior assumptions | [How it contributed] |
| **Human** | Fatigue, time pressure, overconfidence | [How it contributed] |

### Phase 5: Fix Classification

Classify each fix by type:

| Fix Type | When to Use | How to Encode |
|----------|-------------|---------------|
| **Skill** | Recurring workflow needs structure | Create SKILL.md via `skill-extract` |
| **Guard** | Action requires mandatory checkpoint | Add approval gate to existing skill |
| **Rule** | Behavioural constraint needed globally | Create `rules/*.md` |
| **Documentation** | Knowledge gap caused the issue | Update CLAUDE.md, MEMORY.md, or docs/ |
| **Hook** | Manual step was forgotten | Create script in hooks/ |
| **Checklist** | Multiple steps need verification | Add to existing skill |

### Phase 6: Fix Implementation

**Implement fixes during the retrospective, not after.** This is the critical difference from a report-only post-mortem.

For each fix:
1. Implement it (create/edit the file)
2. Record what was done:

| Fix | Type | Location | Status |
|-----|------|----------|--------|
| [Description] | Skill/Guard/Rule/Doc/Hook | [File path] | Created/Updated |

Also record a `[LEARN]` tag in MEMORY.md for each key correction (per the `learn-tags` rule).

### Phase 7: Verification

Define how to verify the fix works:

```markdown
## Verification

**Test scenario:** [How to test the fix]
**Success criteria:** [What "fixed" looks like]
**Review date:** [When to check if fix is working — default: 2 weeks]
```

## Output

Write the report to `log/incidents/YYYY-MM-DD_short-description.md`:

```markdown
# Lessons Learned: [Incident Title]

**Date:** YYYY-MM-DD
**Severity:** [Low|Medium|High|Critical]
**Status:** [Resolved|Monitoring|Open]

## Incident Summary
[Brief description]

## Timeline
| Time | Action | Actor | Outcome |
|------|--------|-------|---------|

## Root Cause
[The fundamental issue]

## Contributing Factors
- [Factor 1]
- [Factor 2]

## Fixes Implemented
| Fix | Type | Location | Status |
|-----|------|----------|--------|

## Prevention
[How this prevents recurrence]

## Lessons
1. [Key takeaway 1]
2. [Key takeaway 2]
```

Create `log/incidents/` if it doesn't exist.

## Common Incident Patterns

| Pattern | Symptom | Root Cause | Typical Fix |
|---------|---------|------------|-------------|
| Premature action | Action taken before approval | Implied consent ≠ explicit | Add approval gate to skill |
| Sequence error | Steps in wrong order | Missing dependency chain | Encode sequence in skill |
| Missing validation | Bad data passed through | No checkpoint | Add pre-flight check |
| Context carryover | Stale assumptions from prior session | State assumed to persist | Explicit context verification |
| Scope creep | Did more than requested | Task scope too broad | Clarifying questions first |
| Planning loop | Re-planned instead of executing | Perfectionism / uncertainty | Execution stall detector |

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| Blame assignment | Creates defensiveness | Focus on process, not people |
| Single-cause thinking | Oversimplifies | Use 5 Whys, multiple factors |
| Recommend without acting | Lessons forgotten, recurs | Implement fixes during retro |
| Vague fixes ("be more careful") | Not verifiable | Encode specific changes |
| Skip verification | No way to know if fix worked | Define success criteria |

## Cross-References

- **`[LEARN]` tags** — record one-liner corrections in MEMORY.md (the quick complement to this skill)
- **`skill-extract`** — extract a full skill from a session (when the fix type is "Skill")
- **`ideas`** — if a fix is too large for this session, capture as an idea for later

## Success Criteria

The retrospective is complete when:
- [ ] Incident clearly defined with timeline
- [ ] Root cause identified (not just symptoms)
- [ ] Contributing factors documented
- [ ] At least one fix implemented (not just recommended)
- [ ] Fix encoded in appropriate location (skill, rule, hook, doc)
- [ ] `[LEARN]` tags recorded in MEMORY.md
- [ ] Verification criteria defined
- [ ] Report written to `log/incidents/`
