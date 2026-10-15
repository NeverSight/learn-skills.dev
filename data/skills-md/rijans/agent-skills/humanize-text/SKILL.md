---
name: humanize-text
description: Write and rewrite natural, human-authored prose while preserving voice, meaning, nuance, and facts. Use when drafting, editing, or reviewing articles, blogs, documentation, READMEs, tutorials, technical explanations, product copy, release notes, social posts, or other prose that should sound specific, natural, and non-formulaic.
---

# Humanize Text

Write like a sharp human writer who understands the subject, not like an AI assistant producing polished generic prose.

## Modes

### Edit
Improve supplied text with the minimum effective changes.

- Preserve meaning, facts, intent, voice, and personality.
- Keep strong original sentences.
- Fix awkward phrasing, repetition, filler, and formulaic language.
- Do not unnecessarily restructure the writing.
- If the supplied text is already natural and effective, make minimal changes or leave it unchanged.

### Draft
Create new prose from the user's brief, audience, context, and examples.

- Match the requested tone and format.
- Use natural structure instead of rigid templates.
- Never invent personal opinions, feelings, stories, experiences, achievements, or anecdotes.
- Never invent facts, statistics, dates, sources, quotations, or technical behavior.

### Detect
Audit text for formulaic or AI-like writing patterns without rewriting it.

- Identify observable patterns.
- Quote the relevant text.
- Explain briefly why it may sound formulaic.
- Suggest what could change.

Never claim to know whether a person or AI wrote the text.
Never assign an AI-generated probability or score.

## Preserve the writer

Preserve:

- Meaning and factual claims
- Nuance and uncertainty
- Intent
- Recognizable vocabulary
- Natural cadence
- Purposeful fragments
- Bluntness or informality
- Appropriate humor or profanity
- Deliberate rough edges

Do not normalize dialect, regional phrasing, slang, or non-standard grammar unless it reduces clarity or the user asks for a more standardized style.

Never invent:

- Facts
- Sources
- Quotes
- Personal experiences
- Emotions
- Opinions
- Achievements
- Benchmarks
- Technical behavior

Do not manufacture imperfections to make writing appear human.

## Improve the prose

Prefer:

- Concrete nouns and specific details
- Direct verbs
- Simple words
- Natural sentence-length variation
- Active voice when clearer
- Focused paragraphs
- Headings and lists only when useful

Cut:

- Repetition
- Filler
- Throat-clearing
- Empty qualifiers
- Unnecessary introductions and conclusions
- Inflated claims
- Adjective stacking
- Corporate language
- Repeated explanations

Do not make every paragraph equally polished, symmetrical, or similar in length.

## Watch for formulaic patterns

Treat these as contextual warnings, not banned words.

Watch for:

- Generic openings such as "In today's rapidly evolving..."
- "It's important to note..."
- "Furthermore", "Moreover", "In conclusion"
- Inflated or generic promotional language such as "groundbreaking", "revolutionary", "seamless", or "game-changing"
- Empty claims such as "plays a vital role"
- "Experts agree" or "studies show" without a named source
- Repeated "not X but Y" contrasts
- Forced rhetorical hooks
- Mechanical groups of three
- Decorative fragments
- Excessive em dashes or colons
- Repetitive punchy sentence patterns
- Synonym cycling
- Empty use of abstract or corporate vocabulary when a concrete word would be clearer
- Chatbot phrases such as "Of course", "I hope this helps", or "Let me know if..."

Keep these patterns when they are useful, intentional, or characteristic of the writer.
If a sentence sounds generically AI-written, rewrite the sentence rather than merely replacing one word.

## Technical documentation

For documentation:

1. Identify the audience and goal.
2. Verify behavior against code or an authoritative source when available.
3. Put useful information early.
4. Use a neutral instructional voice.
5. Address the reader as "you".
6. Prefer imperative verbs.
7. Use active voice and present tense.
8. Keep terminology consistent.
9. Define unfamiliar terms and acronyms.
10. Use inline code for commands, paths, identifiers, and values.
11. Keep examples minimal and runnable.
12. Never invent API behavior, configuration options, or command output.
13. Use descriptive link text.
14. Warn before destructive or irreversible operations.
15. Follow repository conventions when they conflict with these defaults.

## Final review

Before returning substantial prose:

1. Preserve meaning, facts, uncertainty, and voice.
2. Remove generic or formulaic language.
3. Remove repetition and unnecessary structure.
4. Check natural rhythm.
5. Match the author, audience, and format.
6. Confirm nothing was invented.
7. Read it once as a human reader.

The objective is not "perfect writing".

The objective is writing that feels intentional, specific, credible, and naturally written by a person.

## Default

Clear + natural + specific + concise + knowledgeable + appropriately conversational.

User style, audience, house style, and repository conventions take priority.
