---
name: human-writing
description: Write documents in a natural, human style. Use when writing essays, papers, documentation, reports, articles, or any prose content. Avoids common AI writing patterns.
argument-hint: [topic or instructions]
---

# Human Writing Style Guide

When writing prose content, follow these guidelines to produce natural, human-like writing.

## Model-Specific Patterns

Different Claude models have different writing quirks:

| Pattern | Opus 4.5 | Sonnet 4 | Sonnet 3.7 | Haiku 3 |
|---------|----------|----------|------------|---------|
| Em dash overuse | **16.8x** | 0.9x | 0.8x | 0.0x |
| "robust" | 3.1x | 7.7x | 6.5x | **43.2x** |
| "comprehensive" | 24.4x | 37.9x | 30.1x | **39.5x** |
| "nuanced" | 17.0x | **56.1x** | high | 0x |
| "paradigm" | 15.1x | **37.4x** | 24.0x | 7.5x |

*Values show ratio vs human baseline. Bold = worst offender.*

**Key takeaway:** Em dash overuse is primarily an Opus 4.5 issue. Other models have different word preferences to watch.

## Punctuation

Avoid overusing these punctuation marks:

| Avoid | Use Instead | Notes |
|-------|-------------|-------|
| Em dash (—) | Commas, periods, or parentheses | Mainly Opus 4.5 issue (16.8x human) |
| Semicolons | Two separate sentences | Opus 4.5 uses 3x human rate |
| Colons for lists | Integrate into prose | All models use 2-5x human rate |

## Words to Avoid

Replace these AI-favored words with simpler alternatives:

| Avoid | Use Instead |
|-------|-------------|
| comprehensive | complete, full, thorough |
| utilize | use |
| leverage | use, apply |
| facilitate | help, enable |
| robust | strong, solid |
| nuanced | subtle, detailed |
| paradigm | model, approach |
| multifaceted | complex, varied |
| iterative | repeated, step-by-step |
| delve | explore, examine, look at |
| tapestry | mix, combination |
| myriad | many, numerous |
| plethora | many, lots of |
| fostering | building, encouraging |
| underscores | shows, highlights |
| realm | area, field |
| landscape | field, situation |
| crucial | important, key |
| pivotal | important, central |
| noteworthy | notable, worth mentioning |
| intricate | complex, detailed |

## Phrases to Avoid

These phrases strongly signal AI writing:

| Avoid | Use Instead |
|-------|-------------|
| in essence | basically, or delete entirely |
| fundamentally | basically, or delete entirely |
| essentially | basically, or delete entirely |
| it's important to note | delete entirely |
| it's worth noting | delete entirely |
| it should be noted | delete entirely |
| in order to | to |
| due to the fact that | because |
| at the end of the day | ultimately, or delete |
| that being said | but, however |
| in today's world | now, today |
| in the realm of | in |
| when it comes to | for, regarding |
| serves as a | is a |
| plays a crucial role | matters, is important |

## Sentence Starters to Avoid

Don't begin sentences with these formulaic patterns (from analysis):

| Avoid | Ratio vs Human |
|-------|----------------|
| "This document/guide/article..." | 623x |
| "Comprehensive..." | 680x |
| "Introduction..." | 58x |
| "Let's..." | high |
| "In this..." | high |

Also avoid:
- "It's worth noting that..."
- "In today's [anything]..."
- "When it comes to..."
- "At its core..."

## Hedging Language

AI overuses these qualifying words. Use sparingly:

| Word | AI Overuse Ratio |
|------|------------------|
| typically | 9.6x |
| often | 4.9x |
| sometimes | 4.2x |
| potentially | 3.4x |
| usually | 3.4x |
| rather | 3.3x |

**Be more direct.** Instead of "This typically works well," write "This works well."

## Transition Words (Counterintuitive)

AI uses FEWER transition words than humans, not more:
- AI: 0.3 formal transitions per 100 sentences
- Human: 0.9 formal transitions per 100 sentences

Only "conversely" (50x) and "nevertheless" (8x) are AI-overused. "However" is actually more common in human writing (0.52 vs 0.08 per 100 sentences).

**Don't avoid all transitions** - just the overused ones like "Furthermore," "Moreover," "Additionally."

## Structure Guidelines

### Paragraph Length (Critical)

AI fragments text into many short paragraphs (avg 16 words). Human writing uses longer, developed paragraphs.

- **Combine related ideas** into single paragraphs
- **Develop thoughts fully** before moving on
- **Avoid one-sentence paragraphs** unless for emphasis
- Aim for 3-5 sentences per paragraph in most cases

### Sentence Length Distribution

AI alternates between very short and very long sentences. Human writing clusters around medium length.

- **Favor medium-length sentences** (11-25 words)
- Don't alternate between fragments and run-ons
- Maintain consistent rhythm within paragraphs

### Lists and Bullets

AI overuses bullet points (9.5 items/doc vs near zero for humans).

- **Convert lists to prose** when possible
- Reserve bullets for truly parallel items
- Don't use bullets as a crutch for organizing thoughts

### Passive Voice (Counterintuitive)

AI uses LESS passive voice (4.7%) than humans (14.9%). Don't over-correct.

- Passive voice is fine when the action matters more than the actor
- "The experiment was conducted" is acceptable
- Don't contort sentences just to avoid passive

### Other Structure Tips

1. **Start sentences differently** - Don't begin multiple paragraphs the same way
2. **Use contractions** - Write "don't" not "do not" in casual contexts
3. **Be direct** - State things plainly without excessive hedging
4. **Cut filler** - Remove words that add no meaning
5. **Avoid formulaic transitions** - Don't use "Furthermore," "Moreover," "Additionally" repeatedly

## Tone

- Be conversational where appropriate
- Don't over-explain obvious points
- Trust the reader's intelligence
- Express opinions directly when asked
- Avoid excessive qualifiers and hedges

## What Good Human Writing Looks Like

Human writing tends to:
- Get to the point faster
- Use simpler words for the same meaning
- Have more variation in rhythm
- Include occasional sentence fragments
- Use "I" and "you" naturally
- Have personality and voice

## When Writing

Before each paragraph, ask yourself:
1. Could I say this more simply?
2. Am I using any AI-favorite words?
3. Does this sound like something a person would actually write?
4. Have I used an em dash? (If yes, try a comma or period instead)
5. Is this paragraph too short? Should it be combined with the next one?
6. Am I using bullets when prose would work better?
