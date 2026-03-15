---
name: flashcard-creator
description: Extract language learning content from web pages and create structured flashcards in markdown format for spaced repetition study (Anki decks). Works with ANY language (Spanish, Japanese, Arabic, Chinese, etc.). Use when the user asks to create flashcards, flash cards, study cards, Anki decks, or mentions spaced repetition from online content. Supports grammar lessons, vocabulary, and exercises. Converts to Anki-importable format.
allowed-tools:
  - Read
  - Bash
  - mcp__claude-in-chrome__tabs_context_mcp
  - mcp__claude-in-chrome__read_page
  - mcp__claude-in-chrome__get_page_text
  - mcp__claude-in-chrome__computer
  - Write
---

# Flashcard Creator

## Overview

This Skill extracts language learning content from web pages and converts it into structured flashcards optimized for spaced repetition software like Anki. Works with **any language** (Spanish, Japanese, Arabic, Chinese, etc.) and adapts to different writing systems and grammar structures. Creates multiple card types (grammar rules, drills, translations, Q&A) from a single source to maximize repetition value.

## Prerequisites

- Browser must be open with Claude in Chrome extension active
- Target page should contain structured learning content (grammar lessons, vocabulary, exercises)
- Python script `parse_flashcards.py` available in the project root for Anki conversion

## ⚠️ CRITICAL: Markdown Format Requirements

**THE PYTHON PARSER DEPENDS ON EXACT KEYWORD MATCHING. YOU MUST USE THIS FORMAT:**

```markdown
**Front:** Question, prompt, or term here
**Back:** Answer, explanation, or definition here
```

**Strict Requirements:**
1. Use `**Front:**` exactly - with bold markdown (`**`) and colon
2. Use `**Back:**` exactly - with bold markdown (`**`) and colon
3. Front and Back must be on separate, consecutive lines
4. Both keywords are case-sensitive
5. Include the space after the colon

**DO NOT USE:**
- ❌ `Front:` (without bold)
- ❌ `Question:` or `Q:`
- ❌ `**Front**:` (bold without the colon inside)
- ❌ `**Front :**` (space before colon)
- ❌ Any other variations

**Why This Matters:**
The Python parser (`parse_flashcards.py`) uses this code:
```python
if line.startswith('**Front:**'):
    front = line.replace('**Front:**', '').strip()
```

Any deviation from this exact format will cause cards to be silently skipped during parsing.

### Example Block (Correct Format)

```markdown
## Grammar Rules

**Front:** Cuando + presente de subjuntivo (futuro)
**Back:** Cuando me jubile, me iré a vivir a la costa.

**Front:** antes de que + presente de subjuntivo
**Back:** Los pájaros emigran a lugares más cálidos antes de que empiece el invierno.

## Fill-in-the-Blank Exercises

**Front:** Cuando _____ (tener - yo) vacaciones, _____ (soler) viajar a destinos exóticos.
**Back:** Cuando tengo vacaciones, suelo viajar a destinos exóticos.
```

## Instructions

### Step 1: Access the Web Content

1. Use `tabs_context_mcp` to get available tabs
2. Use `read_page` or `get_page_text` to extract content from the current page
3. Take a screenshot if visual context would be helpful

### Step 2: Analyze Content Structure

Identify these elements on the page:
- **Grammar rules** (with examples in different tenses/moods)
- **Vocabulary lists** (with definitions, translations, or context)
- **Example sentences** (showing usage patterns)
- **Exercises** (fill-in-blank, translation, matching)
- **Explanations** (rules, tips, memory aids)

### Step 3: Extract and Structure Content

Create flashcards organized by category using markdown headers (`##`, `###`).

**Recommended categories (adapt based on language type):**
- Grammar Patterns/Rules (word order, particles, connectors, etc.)
- Application Exercises (fill-in-the-blank, sentence building, etc.)
- Vocabulary (with definitions, translations, or usage context)
- Translation Practice (bidirectional)
- Quick Reference Q&A (grammar/usage rules)
- Common Mistakes/Corrections
- Memory Aids (mnemonics for grammar patterns)

**Note:** For inflected languages (Spanish, Russian, Arabic), add "Conjugation/Declension Drills". For tonal languages (Mandarin, Vietnamese), add "Tone Practice". For character-based writing (Japanese, Chinese), add "Character Recognition".

**Categories to AVOID:**
- ❌ Story/plot summaries (unless the vocabulary/structures themselves are the learning goal)
- ❌ Cultural trivia or facts (unless they illustrate language usage)
- ❌ Topic-specific knowledge unrelated to language (e.g., historical dates, scientific facts)
- ❌ Author information or website metadata

### Step 4: Create Multiple Card Types for Maximum Repetition

For each grammar concept or vocabulary item, create multiple card types. Adapt to your target language.

**Example 1: Spanish Grammar (Inflected Language)**

1. **Rule Card** - Present the grammar pattern
   ```markdown
   **Front:** Cuando + presente de subjuntivo (futuro)
   **Back:** Cuando me jubile, me iré a vivir a la costa.
   ```

2. **Fill-in-blank Card** - Test conjugation/application
   ```markdown
   **Front:** Cuando _____ (jubilarse - yo), me _____ (ir) a vivir a la costa.
   **Back:** Cuando me jubile, me iré a vivir a la costa.
   ```

3. **Translation Card** - Apply in context
   ```markdown
   **Front:** When I retire, I will go live on the coast.
   **Back:** Cuando me jubile, me iré a vivir a la costa.
   ```

4. **Quick Reference Card** - Test rule knowledge
   ```markdown
   **Front:** ¿Cómo se expresa el futuro con "cuando"?
   **Back:** Cuando + presente de subjuntivo
   ```

**Example 2: Japanese Vocabulary (Logographic + Syllabic)**

1. **Recognition Card**
   ```markdown
   **Front:** 食べる
   **Back:** たべる (taberu) - to eat [ru-verb]
   ```

2. **Production Card**
   ```markdown
   **Front:** How do you write "to eat" (ru-verb)?
   **Back:** 食べる (たべる / taberu)
   ```

3. **Context Card**
   ```markdown
   **Front:** 私は寿司を_____ (I ___ sushi)
   **Back:** 私は寿司を食べる (I eat sushi)
   ```

**Example 3: Arabic Grammar (Root-Pattern System)**

1. **Root Card**
   ```markdown
   **Front:** What is the root of كَتَبَ (kataba - "he wrote")?
   **Back:** ك-ت-ب (k-t-b) - root meaning "writing"
   ```

2. **Pattern Card**
   ```markdown
   **Front:** Form I past tense of root ك-ت-ب with "he"
   **Back:** كَتَبَ (kataba) - he wrote
   ```

### Step 5: Apply Language Learning Best Practices

**For Grammar:**
- Show the pattern in multiple contexts
- Include both affirmative and negative forms (if applicable)
- Show edge cases and exceptions
- Create "common mistakes" correction cards

**For Vocabulary:**
- Include context sentences, not just definitions
- Show collocations and usage patterns
- Group semantically related words
- Note register (formal/informal) when relevant

**For Language-Specific Features:**
- **Inflected languages** (Spanish, Russian, Arabic): Test conjugations/declensions across persons, tenses, cases
- **Tonal languages** (Mandarin, Vietnamese): Include tone marks and minimal pairs
- **Character-based** (Japanese, Chinese): Create recognition cards (character → reading/meaning)
- **Agglutinative languages** (Turkish, Finnish): Practice suffix combinations
- **Analytic languages** (English, Chinese grammar): Focus on word order and particles

**For Application Drills:**
- Use fill-in-the-blank format with hints (infinitive, tone, character reading, etc.)
- Progress from easier to harder
- Mix different concepts in later sections

### Step 6: Verify Quality

Before finalizing, verify:
- [ ] All cards use `**Front:**` and `**Back:**` format exactly
- [ ] Front and Back are on consecutive lines
- [ ] Content is in logical categories with headers
- [ ] Grammar rules are accurate
- [ ] Examples show proper usage patterns
- [ ] Fill-in-blank exercises include appropriate hints (verb infinitives, tone marks, readings, etc.)
- [ ] Progressive difficulty (basic → advanced)
- [ ] Mix of card types (rules, drills, translation, Q&A)
- [ ] Special characters are correct (accents, tone marks, diacritics, etc. appropriate for the language)
- [ ] At least 50+ cards for a comprehensive topic

### Step 7: Save Output File

- Use descriptive names: `<topic>.md`
- Write to `flashcards/` directory
- Include a header with title and description
- Include the URL of the source page
- Add a study strategy section at the end

### Step 8: Convert to Anki Format (REQUIRED)

**CRITICAL: This step is NOT optional. You MUST complete it automatically.**

After creating the markdown file:

1. **Immediately run the conversion script**:
   ```bash
   python3 parse_flashcards.py flashcards/<filename>.md
   ```
   - Do NOT just tell the user to run it - RUN IT YOURSELF
   - This is a required step to complete the task

2. **Verify the output**:
   ```bash
   wc -l flashcards/<filename>.txt
   ```
   - Check that cards were created successfully

**Why this matters**: The user expects a complete, ready-to-use Anki deck file. Creating only the markdown file is incomplete work. Always finish the conversion.

### Step 9: Report Results to the User

After successfully converting to Anki format, inform the user:

1. **Files created**:
   - **Markdown source**: `flashcards/<filename>.md`
   - **Anki deck file**: `flashcards/<filename>.txt` with [X] flashcards

2. **Next steps**:
   - **Ready to import**: The `.txt` file can be imported directly into Anki
   - **Optional grammar check**: "To verify grammar, ask a subagent to review the markdown file"

## Content Extraction Strategy

### ⚠️ CRITICAL: Focus on LANGUAGE, Not Content

**Extract ONLY reusable language elements: grammar, vocabulary, and usage patterns.**

**Ask yourself:** "Will this card help me use the language, or just remember facts ABOUT the content?"

✅ **DO extract:**
- Grammar patterns and rules
- Vocabulary with translations/definitions
- Usage examples and collocations
- Language-specific conventions (formality levels, register, etc.)

❌ **DON'T extract:**
- Plot summaries or story content (unless the vocabulary/structures themselves are the learning goal)
- Cultural/historical facts mentioned in passing
- Topic-specific knowledge that won't transfer to other contexts
- Website navigation or course structure information

**Example of what NOT to include:**
- "What are the stages of [story concept]?" - Content knowledge, not language
- "Who invented [theory]?" - Trivia, not language learning
- "What does [topic-specific term] mean?" - Unless it's widely-used vocabulary

**Example of what TO include:**
- "Cuando + presente de subjuntivo" - Grammar pattern (Spanish)
- "食べる (taberu) - to eat" - Vocabulary with reading (Japanese)
- "How to express future time with 'cuando'" - Language usage rule

### What to Prioritize

1. **Grammar patterns with examples** - highest value for language learning
2. **Conjugation tables** - convert to fill-in-blank exercises
3. **Vocabulary words and phrases** - with translations and context
4. **Example sentences** - use as-is or convert to translation practice
5. **Language rules and explanations** - convert to Q&A format
6. **Common mistakes sections** - create error correction cards
7. **Idiomatic expressions** - with usage examples

### What to Skip or Minimize

- ❌ Long reading passages (not suitable for flashcards)
- ❌ Complex multi-paragraph explanations (summarize language aspects only)
- ❌ Navigation elements, ads, site metadata
- ❌ Author bios, course promotions
- ❌ **Content-specific information** (stories, plots, cultural facts used as context)
- ❌ **Topical knowledge** that won't help learn the language itself

### Handling Different Content Types

**From a grammar lesson:**
- Extract the rule statement
- Gather all example sentences
- Create variations for different tenses
- Note exceptions explicitly

**From vocabulary lists:**
- Word + definition/translation
- Word in context sentence
- Collocations

**From exercises:**
- Convert multiple choice to fill-in-blank
- Extract correct answers
- Include explanation if provided

## Example Markdown Output Structure

```markdown
# [Topic Name] - Flashcards for Spaced Repetition

**Source:** [URL of the original page]

**Topics Covered:**
- [List of grammar/vocabulary topics]

---

## Grammar Patterns - [Concept Name]

**Front:** [Pattern description or rule]
**Back:** [Example demonstrating usage]

**Front:** [Variation or related pattern]
**Back:** [Example showing difference]

**Key rule:** [Important note or exception]

---

## Application Exercises

**Front:** [Prompt with blank or transformation task]
**Back:** [Correct answer with explanation if needed]

**Front:** [Another exercise]
**Back:** [Answer]

---

## Vocabulary

**Front:** [Word/phrase in target language]
**Back:** [Definition/translation + example sentence]

**Front:** [Another word]
**Back:** [Definition + context]

---

## Translation Practice

**Front:** [Sentence in native language]
**Back:** [Sentence in target language]

**Front:** [Another sentence]
**Back:** [Translation]

---

## Quick Reference

**Front:** [Question about usage/grammar]
**Back:** [Rule or explanation]

---

## Common Mistakes

**Front:** ❌ [Incorrect usage] → ✅ ?
**Back:** ✅ [Correct usage] ([explanation])

---

## Memory Aids

**Front:** [Question about remembering pattern]
**Back:** [Mnemonic or memory trick]

---

## Study Notes

- Study strategy tips
- Recommended order
- Focus areas

Good luck with your studies! 🎯
```

## Common Pitfalls to Avoid

1. **Wrong Keywords** - Not using `**Front:**` and `**Back:**` exactly
2. **Merged Lines** - Putting Front and Back on the same line
3. **Too Much Text** - Making cards too long (keep under 2-3 sentences)
4. **No Organization** - Not using headers to categorize cards
5. **Missing Hints** - Fill-in-blanks without verb/tense hints
6. **No Variety** - Only one card type (need drills, Q&A, translation, etc.)
7. **Skipping Verification** - Not checking accent marks and grammar
8. **Random Order** - Not organizing by difficulty or category

## Examples

### Example: Complete Workflow

**User request**: "Create flashcards from this Spanish grammar page about time expressions"

**Claude's process**:

1. **Access content**: Use `tabs_context_mcp` and `get_page_text`
2. **Analyze**: Identify temporal connectors lesson with 6 main concepts
3. **Extract language elements**:
   - ✅ Grammar patterns (cuando, antes de, mientras, etc.)
   - ✅ Example sentences showing usage
   - ✅ Vocabulary (valiente, cruel, etc.)
   - ❌ Skip: Story content used as examples (extract language, not plot)
   - ❌ Skip: Trivia about theories or concepts mentioned on the page
4. **Structure content**:
   - Grammar rules with examples in different tenses
   - Vocabulary with translations
   - Fill-in-blank application drills
   - Translation practice
   - Quick reference Q&A
   - Common mistakes
   - Memory aids
5. **Write file**: `flashcards/temporal-connectors.md`
6. **Convert**: Run `python3 parse_flashcards.py flashcards/temporal-connectors.md`
7. **Verify**: Check line count shows 153 flashcards created
8. **Report**: "Created temporal-connectors.txt with 153 flashcards ready to import into Anki"

### Example: Flashcard Format

See the "CRITICAL: Markdown Format Requirements" section above for the exact required format.

## Key Principles

**Maximum repetition value**: Create multiple cards for the same concept from different angles (rule, drill, translation, Q&A).

**Progressive difficulty**: Start with basic patterns, move to complex applications.

**Context over memorization**: Always include example sentences, not just isolated rules or definitions.
