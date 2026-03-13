---
name: brainstorm
description: Structured creative ideation for exploring problems and solutions. Use when running /brainstorm-board or when user wants to explore ideas divergently before converging.
---

# Brainstorm Skill

Procedural knowledge for facilitating structured creative ideation sessions.

## When to Use

- Running `/brainstorm-board [topic]`
- User says "let's brainstorm", "explore options", "what are the possibilities"
- Early-stage problem exploration before research or PRD
- Generating multiple solution approaches

## Brainstorming Principles

### Diverge Before Converging
1. **Quantity first** - Generate many ideas without judgment
2. **Build on ideas** - "Yes, and..." not "No, but..."
3. **Wild ideas welcome** - Extreme ideas often lead to practical innovations
4. **Defer judgment** - Evaluation comes later

### Tyler's Thinking Style
Reference `tyler-context.md` - Tyler processes through conversation. Ask probing questions, don't solve immediately.

## Process

### Step 1: Frame the Problem

Ask clarifying questions:
- What's the core problem we're solving?
- Who has this problem? (Which persona?)
- What does success look like?
- What constraints exist?

Create a problem statement:
```
For [persona], who [situation/need],
the [feature/solution] is a [category]
that [key benefit].
Unlike [current alternative],
our solution [key differentiator].
```

### Step 2: Generate Ideas (Diverge)

Use multiple ideation techniques:

**How Might We (HMW)**
Reframe problem as opportunity questions:
- "How might we make [problem] easier?"
- "How might we eliminate [friction]?"
- "How might we turn [negative] into [positive]?"

**Analogies**
- "How does [other industry] solve this?"
- "What would [company/product] do?"
- "If this were [physical/digital/game], how would it work?"

**Extremes**
- "What if we had unlimited resources?"
- "What if we had to ship in 24 hours?"
- "What if users had zero training?"
- "What if AI could do anything?"

**Reversal**
- "What would make this problem worse?"
- "What's the opposite approach?"

### Step 3: Cluster & Theme

Group ideas by:
- **Approach type** - Automation vs. augmentation vs. information
- **User effort** - High-touch vs. low-touch
- **Technical complexity** - Quick win vs. infrastructure investment
- **Persona fit** - Which ideas fit which users

### Step 4: Rough Evaluation

Score each promising idea:

| Criteria | Questions |
|----------|-----------|
| **Impact** | How much does this reduce user pain? |
| **Confidence** | How sure are we users want this? |
| **Effort** | How hard to build/test? |
| **Alignment** | Does it fit product vision? |

Use simple High/Medium/Low ratings.

### Step 5: Select Next Steps

Based on evaluation:
- **High confidence, high impact** → Move to research/validation
- **Low confidence, high impact** → Need more evidence first
- **Quick wins** → Consider for near-term roadmap
- **Big bets** → Document for future consideration

## Output Format

```markdown
# Brainstorm: [Topic]

**Date:** YYYY-MM-DD
**Participants:** [who was involved]

## Problem Statement
[Framed problem]

## Ideas Generated

### Theme 1: [Name]
| Idea | Description | Impact | Effort |
|------|-------------|--------|--------|
| [Idea A] | [Brief] | H/M/L | H/M/L |
| [Idea B] | [Brief] | H/M/L | H/M/L |

### Theme 2: [Name]
...

## Top Candidates

### 1. [Best Idea]
- **Why promising:** [reason]
- **Key risk:** [concern]
- **Next step:** [action]

### 2. [Second Idea]
...

## Parked Ideas
Ideas worth revisiting later:
- [Idea] - [why parked]

## Questions to Answer
1. [Open question needing research]
2. [Assumption to validate]

## Recommended Next Steps
- [ ] [Specific action 1]
- [ ] [Specific action 2]
```

## Save Location

`pm-workspace-docs/research/brainstorms/YYYY-MM-DD-[topic].md`

## Anti-Patterns

🚩 **Converging too early** - Let ideas flow before evaluating
🚩 **Solution-first** - Always start with problem framing
🚩 **Single idea** - Push for at least 5-10 ideas before narrowing
🚩 **Ignoring constraints** - Note constraints but don't let them kill creativity
🚩 **No next step** - Always end with actionable recommendations

## Integration with Other Commands

After brainstorming:
- Test assumptions → `/hypothesis new [name]`
- Start initiative → `/new-initiative [name]`
- Need user evidence → `/research [name]`
- Ready for definition → `/pm [name]`
