---
name: ai-text-humanizer
description: Identifies and removes signs of AI-generated text to make writing sound more natural and human. Use when the user asks to humanize text, make writing sound more natural, remove AI patterns, edit for human voice, or convert AI-generated content to natural prose. Also triggers on requests to check for AI writing patterns, review text for robotic language, or improve writing authenticity. Based on Wikipedia's "Signs of AI writing" guidelines.
---

# AI Text Humanizer

Transform AI-generated text into natural, human-sounding writing by identifying and removing telltale AI patterns.

## Core Approach

When humanizing text:

1. **Identify AI patterns** - Scan for patterns from references/patterns.md
2. **Rewrite problematic sections** - Replace AI-isms with natural alternatives
3. **Preserve meaning** - Keep the core message intact
4. **Match voice** - Maintain the intended tone (formal, casual, technical)
5. **Add soul** - Don't just remove bad patterns; inject personality

## Quick Start

For most humanization tasks:

```python
# Read the text
# Identify patterns using references/patterns.md
# Rewrite each problematic section
# Verify the result sounds natural when read aloud
```

## Key Principles

**Avoiding AI patterns is only half the job.** Sterile, voiceless writing is just as obvious as AI slop. Good writing has a human behind it.

### Signs of Soulless Writing

- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of uncertainty or mixed feelings
- No first-person perspective when appropriate
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

### How to Add Voice

**Have opinions.** Don't just report facts - react to them. "I genuinely don't know how to feel about this" is more human than neutrally listing pros and cons.

**Vary rhythm.** Short punchy sentences. Then longer ones that take their time. Mix it up.

**Acknowledge complexity.** Real humans have mixed feelings. "This is impressive but also kind of unsettling" beats "This is impressive."

**Use "I" when it fits.** First person isn't unprofessional - it's honest. "I keep coming back to..." signals a real person thinking.

**Let some mess in.** Perfect structure feels algorithmic. Tangents and asides are human.

**Be specific about feelings.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am while nobody's watching."

## Pattern Categories

The skill covers four main categories of AI patterns:

1. **Content Patterns** (8 types) - Undue emphasis, promotional language, vague attributions
2. **Language Patterns** (6 types) - Overused AI vocabulary, copula avoidance, false ranges
3. **Style Patterns** (6 types) - Em dash overuse, boldface, title case, emojis
4. **Communication Patterns** (3 types) - Chatbot artifacts, disclaimers, servile tone

For detailed pattern descriptions, examples, and before/after comparisons, see `references/patterns.md`.

## Output Format

Provide:

1. The humanized text
2. Brief summary of changes made (optional, only if helpful for understanding)

## Example Transformation

**Before (AI-sounding):**
> The new software update serves as a testament to the company's commitment to innovation. Moreover, it provides a seamless, intuitive, and powerful user experience—ensuring that users can accomplish their goals efficiently. It's not just an update, it's a revolution in how we think about productivity.

**After (Humanized):**
> The software update adds batch processing, keyboard shortcuts, and offline mode. Early feedback from beta testers has been positive, with most reporting faster task completion.

## Advanced Usage

For complex documents or when dealing with specific pattern types:

1. Read `references/patterns.md` to understand all 23 pattern types in detail
2. Focus on patterns most prevalent in the text
3. Apply voice-building techniques after removing AI patterns
4. Verify the result maintains appropriate formality for context

## Quality Checks

Before finalizing humanized text:

- Read it aloud - does it sound natural?
- Check sentence variety - are lengths and structures mixed?
- Look for specifics - are there concrete details instead of vague claims?
- Verify tone - does it match the intended context?
- Confirm simplicity - are simple constructions (is/are/has) used where appropriate?
