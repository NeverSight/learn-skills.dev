---
name: technical-presentations
description: Create and deliver effective technical presentations, demos, and talks. Provides frameworks for structuring content, designing slides, and handling live demos.
allowed-tools: Read, Glob, Grep
---

# Technical Presentations Skill

Create compelling technical presentations that educate, persuade, and engage developer audiences.

## Keywords

presentation, slides, talk, demo, speaking, pitch, architecture review, tech talk, brown bag, lightning talk, conference, meetup, powerpoint, keynote, google slides

## When to Use This Skill

This skill provides guidance when developers need to:

- Structure a technical presentation or talk
- Create effective slides for developer audiences
- Plan and execute live demos
- Present architecture decisions or proposals
- Deliver knowledge-sharing sessions
- Pitch technical solutions to stakeholders

## Core Framework: What-Why-How

Every technical presentation should follow this structure:

```text
┌─────────────────────────────────────────────────────────────┐
│  WHAT (10% of time) - The Hook                              │
│  "Here's the problem/opportunity we're addressing"          │
├─────────────────────────────────────────────────────────────┤
│  WHY (30% of time) - The Context                            │
│  "Here's why it matters and why you should care"            │
├─────────────────────────────────────────────────────────────┤
│  HOW (50% of time) - The Solution                           │
│  "Here's how we solve it / how it works"                    │
├─────────────────────────────────────────────────────────────┤
│  CLOSE (10% of time) - The Call to Action                   │
│  "Here's what you should do next / key takeaways"           │
└─────────────────────────────────────────────────────────────┘
```

### WHAT: The Hook (First 2-3 Minutes)

**Goal:** Grab attention and establish relevance.

**Techniques:**

- Start with a problem the audience recognizes
- Open with a surprising statistic or fact
- Ask a provocative question
- Tell a brief story that illustrates the pain

**What to avoid:**

- "Today I'm going to talk about..."
- Agenda slides before you've hooked them
- Starting with definitions or background
- Apologizing for anything

### WHY: The Context (Next 30% of Time)

**Goal:** Build the case for why this matters.

**Include:**

- Background that's essential to understanding
- The stakes (what happens if we don't act)
- The opportunity (what's possible)
- Why now (urgency or timing)

**Calibrate for audience:**

- Technical peers: Less context, more depth
- Mixed audience: More context, less jargon
- Leadership: Business impact focus

### HOW: The Solution (Main Body - 50%)

**Goal:** Deliver the substance.

**Structure options:**

- Chronological (the journey)
- Problem → Solution → Proof
- Three key points with examples
- Before → Change → After

**For technical content:**

- Architecture diagrams
- Code examples (simplified)
- Live demos (with backups)
- Metrics and data

### CLOSE: The Call to Action (Final 10%)

**Goal:** Make it stick and drive action.

**Include:**

- Summary (3 key takeaways max)
- Clear next steps
- Resources for going deeper
- Time for Q&A

## Presentation Types

### Type 1: Architecture Review / RFC

**Purpose:** Get feedback on technical approach.

**Structure:**

1. Problem statement (2 min)
2. Constraints and requirements (3 min)
3. Options considered (5 min)
4. Proposed solution (10 min)
5. Trade-offs acknowledged (3 min)
6. Open questions (2 min)
7. Discussion (15+ min)

**Keys to success:**

- Share materials beforehand
- Focus on decisions, not implementation details
- Explicitly call out what you're NOT doing
- Prepare for tough questions

### Type 2: Demo / Walkthrough

**Purpose:** Show how something works.

**Structure:**

1. What problem this solves (2 min)
2. Quick overview (3 min)
3. Live demonstration (15-20 min)
4. Under the hood (optional, 5-10 min)
5. Q&A (5-10 min)

**Keys to success:**

- Always have a backup (screenshots, video)
- Use realistic but safe data
- Explain what you're doing as you do it
- Have rollback plan for failures

### Type 3: Knowledge Share / Brown Bag

**Purpose:** Teach something useful.

**Structure:**

1. Why this topic matters (3 min)
2. Core concepts (10 min)
3. Practical application (10 min)
4. Gotchas and tips (5 min)
5. Resources and Q&A (5 min)

**Keys to success:**

- Know your audience's level
- Include actionable takeaways
- Provide follow-up resources
- Make it interactive

### Type 4: Decision Pitch

**Purpose:** Get buy-in for a proposal.

**Structure:**

1. The problem/opportunity (3 min)
2. Options we considered (5 min)
3. Our recommendation (10 min)
4. Why this over alternatives (5 min)
5. Risk mitigation (3 min)
6. Ask for decision/next steps (2 min)

**Keys to success:**

- Lead with recommendation (don't bury it)
- Anticipate objections
- Have data to support claims
- Be clear about what you're asking for

## Slide Design Principles

### The Rules

1. **One idea per slide** - If you need "and" in the title, split it
2. **5-7 words per bullet** - Slides are cues, not scripts
3. **Visual > Text** - Diagrams, screenshots, code
4. **Consistent design** - Same fonts, colors, layouts
5. **Readable from the back** - 24pt minimum for body text

### What Works

| Element | Good | Bad |
| --- | --- | --- |
| Titles | Action-oriented, specific | Generic, vague |
| Bullets | Keywords and phrases | Complete sentences |
| Diagrams | Simplified, labeled | Busy, tiny labels |
| Code | Highlighted key lines | Full files |
| Data | One clear point | Multiple charts |

### Slide Types

**Title slide:** Topic, your name, date, context

**Agenda slide:** Use sparingly, after hook

**Content slides:** One point with support

**Diagram slides:** Visual with minimal text

**Code slides:** Syntax highlighted, key lines marked

**Summary slides:** 3 key takeaways

**Q&A slide:** Signal for questions

## Live Demo Best Practices

### Preparation

- [ ] Test everything the morning of
- [ ] Have screenshots/video backup
- [ ] Use realistic but safe data
- [ ] Increase font size (18pt+ for terminal)
- [ ] Disable notifications
- [ ] Pre-stage browser tabs/windows
- [ ] Have recovery plan

### Execution

- Narrate what you're doing
- Pause to let audience catch up
- Point out what to look at
- Acknowledge when things go wrong
- Have "get out of jail" plan

### When Things Break

1. Acknowledge it briefly
2. Try one quick fix (30 seconds max)
3. If still broken, switch to backup
4. Continue with confidence
5. Don't apologize excessively

## Handling Q&A

### Techniques

**Repeat the question:** Ensures everyone heard and gives you time to think.

**Clarify if needed:** "Are you asking about X or Y?"

**Acknowledge good questions:** "That's a great point..."

**It's okay to not know:** "I don't have the answer to that, but I can find out."

**Defer if needed:** "That's a bigger topic—let's discuss offline."

**Bridge to your message:** "That relates to the point about..."

### Difficult Questions

| Type | Response |
| --- | --- |
| Challenge to your approach | "That's a valid concern. Here's how we thought about it..." |
| Out of scope | "Good question—that's outside what we covered. Let's take it offline." |
| Hostile tone | Stay calm, address the content, not the tone |
| Show-off question | "Interesting point. Let me address the practical aspect..." |
| Rambling non-question | "Let me make sure I understand your question..." |

## Timing and Pacing

### Time Allocation

| Duration | Content | Q&A |
| --- | --- | --- |
| 5-10 min (lightning) | 8 min | None or 2 min |
| 20-30 min (standard) | 20-25 min | 5-10 min |
| 45-60 min (deep dive) | 35-45 min | 10-15 min |

### Pacing Tips

- Start strong (don't waste opening minutes)
- Vary energy (not monotone)
- Build to key points
- Use silence strategically
- End on time (or early!)

### Practice Routine

1. **Read-through:** Time yourself reading slides aloud
2. **Talk-through:** Practice without looking at slides
3. **Full run:** Present to someone or record yourself
4. **Cut ruthlessly:** If over time, remove content

## References

For detailed guidance, see:

- `references/slide-design-guide.md` - Comprehensive slide creation guidance
- `references/demo-playbook.md` - Live demo preparation and execution
- `references/presentation-checklist.md` - Pre-presentation preparation list

## Related Commands

- `/soft-skills:structure-presentation` - Generate presentation outline
- `/soft-skills:write-cfp` - Write conference proposals

## Anti-Patterns to Avoid

- Starting with "Today I'm going to talk about..."
- Reading slides verbatim
- Too much text on slides
- Live demos without backup
- Running over time
- Apologizing for content
- Skipping Q&A
- No clear takeaways

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
