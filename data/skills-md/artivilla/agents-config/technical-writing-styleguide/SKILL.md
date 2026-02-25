---
name: technical-writing-styleguide
description: Technical writing styleguide for clear, consistent documentation. Use when writing, editing, or reviewing technical content, guides, tutorials, or documentation. Triggers on article review, writing style, brand names, grammar check, screenshot guidelines, guide audit, technical docs.
---

# Technical Writing Styleguide

## Quick Reference

**Voice**: first person plural ("we'll install..."), active voice, friendly and informal tone.

**Point of view priority**:
1. First person plural to include the reader: "Next, we'll configure the server."
2. Second person imperative for instructions: "Type `npm install`."

**Key rules**:
- Be opinionated, not comprehensive — pick one approach and recommend it
- Never tell the reader something is "easy" or "obvious"
- Never start with personal background or definitions
- Avoid marketing speak and encyclopaedia-style content
- Use serial commas, common contractions, and sentence case for headings
- Place inline code between backticks, but use fenced code blocks for any runnable commands
- Put text before screenshots, never two screenshots in a row without text between them

**Brand names**: many tech brand names have irregular capitalization (JavaScript not Javascript, GitHub not Github, Node.js not NodeJS). Always verify against the brand-names reference.

**Numbers**: spell out numbers under ten and at the start of sentences. Use numerals for 10 and above. Numbers over three digits get commas (1,000).

**Code blocks**: always use fenced code blocks with language specifiers for code samples. Use backticks only for inline single-word references.

## Principles

- **Clear**: keep words and sentences as simple as possible
- **Useful**: deliver on the promise your headline made
- **Friendly**: use informal language without patronizing the reader

## Progressive Disclosure

- **Full styleguide**: see [references/styleguide.md](references/styleguide.md) for voice, tone, structure, headings, code samples, and formatting conventions
- **Grammar**: see [references/grammar.md](references/grammar.md) for punctuation, capitalization, contractions, numbers, pronouns, and word list
- **Brand names**: see [references/brand-names.md](references/brand-names.md) for correct capitalization of tech brand names
- **Screenshots**: see [references/screenshots.md](references/screenshots.md) for resolution, annotations, gifs, and combining screenshots with text
- **Guide audit**: see [references/guide-audit.md](references/guide-audit.md) for pre-commit checklist when reviewing articles

## Decision Guide

### When reviewing or editing existing content
Load the **grammar** and **styleguide** references. Check brand names against the **brand-names** reference.

### When writing a new tutorial or guide
Load the **styleguide** for structure and voice. Use the **screenshots** reference when adding visuals.

### When doing a final review before publishing
Run through the **guide-audit** checklist to verify word count, structure, and content quality.
