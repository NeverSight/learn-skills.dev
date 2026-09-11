---
name: stop-slop
description: "Remove AI writing patterns from prose. Scores on 5 dimensions, rewrites to sound human."
version: "1.0.0"
metadata:
  {"openclaw":{"emoji":"","requires":{},"tags":["writing","editing","email","prose","humanize"]}}
---

# Stop Slop

Strip AI writing patterns from prose. Based on [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) (MIT).

## Usage

```
/stop-slop <text or instruction>
```

**Examples:**
```
/stop-slop Here's the email I need to send to my attorney: ...
/stop-slop rewrite this paragraph to sound human: ...
/stop-slop score this draft and fix anything that reads like AI
```

## Execution

When invoked with text:

1. **Score** the input on the 5 dimensions (see Scoring below)
2. **Identify** every violation of the 8 core rules
3. **Rewrite** the text with all violations fixed
4. **Re-score** the rewritten version
5. **Show** before/after scores and the rewritten text

When invoked with an instruction (e.g., "write an email to..."):

1. **Draft** the text following all 8 rules from the start
2. **Score** the draft
3. **If below 35/50**, revise until it passes

## Core Rules

1. **Cut filler phrases.** Remove throat-clearing openers, emphasis crutches, and all adverbs.
2. **Break formulaic structures.** No binary contrasts, negative listings, dramatic fragmentation, rhetorical setups, false agency.
3. **Use active voice.** Every sentence needs a human subject doing something. No passive constructions. No inanimate objects performing human actions.
4. **Be specific.** No vague declaratives. Name the specific thing. No lazy extremes ("every," "always," "never").
5. **Put the reader in the room.** No narrator-from-a-distance voice. "You" beats "People." Specifics beat abstractions.
6. **Vary rhythm.** Mix sentence lengths. Two items beat three. End paragraphs differently. No em dashes.
7. **Trust readers.** State facts directly. Skip softening, justification, hand-holding.
8. **Cut quotables.** If it sounds like a pull-quote, rewrite it.

## Phrases to Remove

### Throat-Clearing Openers
Remove these — state the content directly:
- "Here's the thing:" / "Here's what/this/that [X]" / "Here's why [X]"
- "The uncomfortable truth is" / "It turns out" / "The real [X] is"
- "Let me be clear" / "The truth is," / "I'll say it again:"
- "Can we talk about" / "Here's what I find interesting"

### Emphasis Crutches
Add no meaning — delete them:
- "Full stop." / "Period." / "Let that sink in."
- "This matters because" / "Make no mistake" / "Here's why that matters"

### Business Jargon
| Avoid | Use instead |
|-------|-------------|
| Navigate (challenges) | Handle, address |
| Unpack (analysis) | Explain, examine |
| Lean into | Accept, embrace |
| Landscape (context) | Situation, field |
| Game-changer | Significant, important |
| Deep dive | Analysis, examination |
| Circle back | Return to, revisit |
| Moving forward | Next, from now |

### Adverbs — Kill All
No -ly words. No softeners, intensifiers, or hedges:
- really, just, literally, genuinely, honestly, simply, actually
- deeply, truly, fundamentally, inherently, inevitably
- interestingly, importantly, crucially

### Filler Phrases
- "At its core" / "In today's [X]" / "It's worth noting"
- "At the end of the day" / "When it comes to" / "In a world where"

### Meta-Commentary
Remove self-referential asides:
- "Hint:" / "Plot twist:" / "Spoiler:"
- "But that's another post" / "The rest of this essay explains..."
- "Let me walk you through..." / "As we'll see..."

### Vague Declaratives
Sentences that announce importance without naming the specific thing:
- "The reasons are structural" / "The implications are significant"
- "The stakes are high" / "The consequences are real"

## Structures to Avoid

### Binary Contrasts
State the point directly — drop the negation:
- "Not because X. Because Y." → State Y directly
- "[X] isn't the problem. [Y] is." → "The problem is Y."
- "It's not this. It's that." → State that.

### Negative Listing
Listing what something is NOT before revealing what it IS:
- "Not a X... Not a Y... A Z." → State Z. The reader doesn't need the runway.

### Dramatic Fragmentation
Sentence fragments for emphasis = manufactured profundity:
- "[Noun]. That's it. That's the [thing]." → Complete sentences.
- "This unlocks something. [Word]." → Complete sentences.

### Rhetorical Setups
Announce insight rather than deliver it:
- "What if [reframe]?" / "Here's what I mean:" / "Think about it:"
- "And that's okay." → Cut the permission-granting.

### False Agency
Inanimate things performing human actions. Name the human:
- "a complaint becomes a fix" → "The team fixed it that week"
- "the decision emerges" → Someone decides. Name them.
- "the data tells us" → Someone reads it and draws a conclusion.
- "the market rewards" → Buyers pay for things.

### Narrator-from-a-Distance
- "Nobody designed this." → "You don't sit down one day and decide to..."
- "People tend to..." → Put the reader in the room.

### Passive Voice
Find the actor. Put them at the front:
- "X was created" → Name who created it
- "Mistakes were made" → Name who made them

### Rhythm Patterns
- Three-item lists → Use two items or one
- Questions answered immediately → Let questions breathe or cut them
- Every paragraph ends punchily → Vary endings
- Em-dashes → Remove. Use commas or periods.
- Lazy extremes (every, always, never, everyone, nobody) → Use specifics

## Quick Checks

Before delivering prose:

- Any adverbs? Kill them.
- Any passive voice? Find the actor, make them the subject.
- Inanimate thing doing a human verb? Name the person.
- Sentence starts with a Wh- word? Restructure it.
- Any "here's what/this/that" throat-clearing? Cut to the point.
- Any "not X, it's Y" contrasts? State Y directly.
- Three consecutive sentences match length? Break one.
- Paragraph ends with punchy one-liner? Vary it.
- Em-dash anywhere? Remove it.
- Vague declarative? Name the specific implication.
- Meta-joiners ("The rest of this essay...")? Delete.

## Scoring

Rate 1-10 on each dimension:

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Rhythm | Varied or metronomic? |
| Trust | Respects reader intelligence? |
| Authenticity | Sounds human? |
| Density | Anything cuttable? |

**Below 35/50: revise.**

## Examples

### Example 1: Throat-Clearing + Binary Contrast

**Before:**
> "Here's the thing: building products is hard. Not because the technology is complex. Because people are complex. Let that sink in."

**After:**
> "Building products is hard. Technology is manageable. People aren't."

### Example 2: Filler + Unnecessary Reassurance

**Before:**
> "It turns out that most teams struggle with alignment. The uncomfortable truth is that nobody wants to admit they're confused. And that's okay."

**After:**
> "Teams struggle with alignment. Nobody admits confusion."

### Example 3: Business Jargon Stack

**Before:**
> "In today's fast-paced landscape, we need to lean into discomfort and navigate uncertainty with clarity. This matters because your competition isn't waiting."

**After:**
> "Move faster. Your competition is."

### Example 4: Dramatic Fragmentation

**Before:**
> "Speed. Quality. Cost. You can only pick two. That's it. That's the tradeoff."

**After:**
> "Speed, quality, cost — pick two."

### Example 5: Rhetorical Setup

**Before:**
> "What if I told you that the best teams don't optimize for productivity? Here's what I mean: they optimize for learning. Think about it."

**After:**
> "The best teams optimize for learning, not productivity."

## Feedback Log

**Before executing this skill, read `feedback.log` in this skill's directory.**

The feedback log contains corrections and preferences from previous sessions. Apply all entries to the current task.

**During execution:** When the user gives a correction or preference, append it to `feedback.log`. Only log general preferences that apply to future sessions, not task-specific details.
