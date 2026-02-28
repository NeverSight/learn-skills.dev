---
name: anki
description: >-
  Generates Anki flashcards in TSV format from source material using spaced
  repetition best practices. Supports Basic, Reversed (bidirectional), and Cloze
  card types with configurable quantity and difficulty. Use when generating
  flashcards, creating Anki cards, making study cards, converting notes to
  flashcards, turning a transcript into flashcards, or building a spaced
  repetition deck.
---

# Anki Flashcard Generator

Generate Anki flashcards from any source material. Produces TSV files ready for direct import.

## Reference Files

| File | Read When |
|------|-----------|
| `references/card-design-rules.md` | Default: card construction, anti-patterns, bidirectional rules |
| `references/tsv-format-spec.md` | Formatting output as TSV |
| `references/difficulty-calibration.md` | Applying difficulty and quantity settings |

## Parameters

Ask the user for these before generating. Default to Standard / Medium if not specified.

### Number of cards

| Setting | Cards | Strategy |
|---------|-------|----------|
| Fewer | 15-25 | High-priority concepts only. Every card earns its place. |
| Standard | 30-50 | Balanced coverage. Core concepts plus important supporting detail. |
| More | 60-100+ | Comprehensive. Includes nuance, edge cases, and worked examples. |

### Difficulty

| Level | Cognitive task | Card style |
|-------|---------------|------------|
| Easy | Recognition, definition, identification | "What is X?", "Define X", single-fact cloze |
| Medium | Application, comparison, analysis | "Why does X matter?", "Compare X and Y", multi-cloze |
| Hard | Synthesis, evaluation, multi-step reasoning | "How would you apply X to Y?", scenario-based, chained cloze |

## Workflow

```
- [ ] 1. Collect source material
- [ ] 2. Confirm parameters
- [ ] 3. Identify key concepts
- [ ] 4. Assign topics and priorities
- [ ] 5. Choose card types
- [ ] 6. Draft cards
- [ ] 7. Format as TSV
- [ ] 8. Self-review
- [ ] 9. Output
```

### 1. Collect source material

Read the provided content (transcript, document, skill, etc.). Every card must trace to the source material. Do not generate cards from general knowledge.

### 2. Confirm parameters

Ask the user for card count and difficulty if not specified. Default to Standard / Medium.

### 3. Identify key concepts

Extract core facts, definitions, relationships, formulas, benchmarks, and frameworks from the source. Group by topic.

### 4. Assign topics and priorities

Map each concept to a topic tag (kebab-case). Assign priority levels:

- `priority::high` — Core concepts that appear repeatedly or underpin other ideas
- `priority::medium` — Supporting detail that strengthens understanding
- `priority::low` — Reference knowledge, nice to have

### 5. Choose card types

Select the card type based on what is being tested:

**Basic** — Direct Q&A for explanations, reasoning, comparisons, processes.
- Front: A specific question. Never yes/no. Never vague ("Tell me about X").
- Back: Concise answer with `<b>bold</b>` on the key phrase the learner must recall.

**Reversed (bidirectional)** — For terminology, translations, concept ↔ example pairs.
- Generate two separate Basic cards: Term → Definition AND Definition → Term.
- Only reverse when both directions produce useful recall. Do NOT reverse explanatory or reasoning cards.
- Tag both cards with `reversed` modifier.

**Cloze** — For port numbers, specific values, command syntax, formulas, numeric benchmarks.
- Text: Complete sentence with `{{c1::blanks}}` replacing key values.
- Use multiple deletions (c1, c2, c3...) when values belong to one coherent fact.
- Tag with `formulas` for formulas, `benchmarks` for numeric thresholds.

### 6. Draft cards

Write each card following the design rules in `references/card-design-rules.md`. Apply difficulty calibration from `references/difficulty-calibration.md`.

### 7. Format as TSV

Format cards following the exact specification in `references/tsv-format-spec.md`.

### 8. Self-review

Check every card against the quality checklist below. Remove or rewrite any that fail.

### 9. Output

Present Basic cards and Cloze cards as separate TSV code blocks. Include count summary and import instructions:

1. Open Anki → File → Import
2. Select the TSV file
3. Set note type to "Basic" or "Cloze" as appropriate
4. Map fields: Field 1 → Front/Text, Field 2 → Back/Extra, Field 3 → Tags

## Quality Checklist

Every card must pass all of these:

- [ ] **Atomic** — Tests exactly one fact. If you need "and" to describe what it tests, split it.
- [ ] **8-second rule** — A prepared learner can answer in under 8 seconds.
- [ ] **Source-grounded** — The answer comes from the provided source material, not general knowledge.
- [ ] **Useful for recall** — Tests meaningful knowledge, not trivial facts.
- [ ] **No orphans** — The learner can understand this card without needing another card first.
- [ ] **Bold highlight** — The answer has at least one `<b>bold</b>` phrase marking the key recall target.
- [ ] **Specific question** — The front asks a precise question, not "Tell me about X".
- [ ] **No yes/no** — Never a question answerable with yes or no.
- [ ] **No shopping lists** — Never "List the 7 types of..." (break into individual cards or use cloze).
- [ ] **Tagged** — Has exactly one topic tag and one priority level.
- [ ] **Difficulty-appropriate** — Matches the requested difficulty level.

## Tag Syntax

Tags are space-separated within the Tags field. Order: topic tag, then priority, then modifiers.

```
topic-name priority::high
topic-name priority::medium formulas
topic-name priority::low reversed
```

- Topic tags: kebab-case (`python-basics`, `web-security`)
- Hierarchical topics: use `::` separator (`networking::protocols`)
- Priority: `priority::high`, `priority::medium`, `priority::low`
- Modifiers: `formulas`, `benchmarks`, `reversed`

## Output Format

**Basic cards:**

```
Question text here	Answer with <b>bold</b> key terms	topic-tag priority::level
```

**Cloze cards:**

```
Text with {{c1::blanks}} for key values		topic-tag priority::level formulas
```

Note: Cloze cards have an empty second field (two consecutive tabs).
