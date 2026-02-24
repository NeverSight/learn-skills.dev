---
name: book-writer
description: |
  Comprehensive book writing assistant and memory maintainer. Use when tasked with:
  - Writing books, novels, fiction, non-fiction, or any long-form manuscript
  - Creating characters, outlining chapters, building worlds
  - Drafting, reviewing, or revising chapters
  - "initialize memory bank", "update memory bank", "start a new book", "let's start building"
  - Planning book structure (MVB, short book, full book, literary novel)
  - Checking continuity or consistency across chapters
  - Any request involving book chapters, manuscripts, or story development

  Provides specialized guidelines to write like a master author while maintaining an automated book memory bank to preserve context across sessions.
---

# Book Writer

## Overview

This skill equips Claude with the capabilities of a world-class fiction author and a robust system for maintaining story context ("Book Memory Bank") across long writing sessions. With this skill, Claude acts as a creative collaborator while automatically keeping characters, plots, and world-building details consistent.

## Features

This skill combines capabilities from multiple specialized writing disciplines:

- **Book Memory Bank** — Automatic context preservation across sessions (characters, plots, world, progress)
- **The Story Forge** — One-time onboarding conversation with fast-track option, draft import, and genre detection
- **Multi-Genre Mastery** — Literary fiction, historical, fantasy, sci-fi, thriller, romance, horror, YA, and more
- **Historical Genre Features** — Title/honorific timeline rules, `[FICTION]` marking, contextual address rules, fact-checking flags
- **Dialogue Language Support** — Weave local languages (Hinglish, Hindi, Marathi, French, Spanish, etc.) into dialogue naturally
- **Character Profiles** — Structured 19-field character tables with historical title timelines
- **Worldbuilding Tables** — 10-category structured world profiles with sensory details
- **Conflict Mapping** — External/internal/thematic conflict structure with stakes
- **Synopsis & Timeline Templates** — Beginning/middle/end narrative beats; chronological event tracking
- **Chapter Craft** — Opening/closing formulas, structure templates, engagement techniques for fiction and non-fiction
- **Book Size Planning** — MVB (15–20K words), Short (25–40K), Full (50–80K), Literary Novel (60–100K)
- **Revision Checklists** — Comprehensive quality gates: story, prose, voice, characters, continuity, engagement
- **Anti-AI Writing Rules** — Hype test, voice authenticity checks, DO/DON'T quick-scan lists
- **Continuity Diagnostics** — Cross-chapter consistency checks generating question-based diagnostic reports
- **Automated Memory Updates** — Triggered after chapter completion, outline creation, or on-demand
- **Compilation** — Combine all chapters into a single manuscript file via scripts or AI
- **README Generation** — Auto-generated project README with progress tracking and badges

## Workflows

### 1. Initialization: Starting a New Book Project
When the user asks to start a new book project or "initialize the memory bank", follow these steps:

0. **Run The Story Forge first.** Read `references/story_forge.md` in full and follow its instructions. Ask questions one at a time to gather book details. Every question is skippable. If the memory bank Core files already exist, skip this step entirely — just read the memory bank and assist.
1. Copy the `assets/book-memory-bank/` directory to the root of the user's project workspace.
2. Read `references/author_rules.md` to adopt the persona and style of a master fiction author.
3. Help the user establish the foundational elements (concept, style, characters) by discussing the book's plan.
4. Use `references/character_worldbuilding_tables.md` for structured character profiles and worldbuilding tables when building out characters and settings.
5. Record these elements into the newly created `book-memory-bank/Core/` and `book-memory-bank/Style/` Markdown files.
6. **Generate the project README.** Read `references/readme_template.md`, fill all `{{TOKEN}}` placeholders using answers from the brainstorming gate and the newly written memory bank files, and write the completed file as `README.md` in the project root. Do not ask the user to review it — just create it silently.

### 2. Writing & Outlining
When the user asks to outline or write chapters:
1. Always start by reading ALL memory bank files (`book-memory-bank/Core/`, `book-memory-bank/Style/`, and any existing master outline) to regain context.
2. Adopt the instructions in `references/author_rules.md` for generating high-quality narrative prose, realistic dialogue, and engaging scenes.
3. Consult `references/chapter_craft.md` for chapter structure templates, opening/closing formulas, and engagement techniques appropriate to the book type.
4. Write outlines in the `Outlines/Chapter_Outlines/` directory.
5. Write chapters in the `Chapters/` directory.

### 3. Compilation
If the user asks YOU (the AI) to compile or combine the book (rather than running the included scripts themselves):
1. Determine the user's OS. If Mac/Linux, attempt to run the provided bash script `book-memory-bank/Production/Scripts/combine_chapters.sh`. If Windows, run `combine_chapters.ps1`.
2. If the script fails or is unavailable, create the `Manuscript/` directory in the project root if it does not already exist.
3. Read all files from `Chapters/` in numerical order, combine them into a single file, and save it inside the `Manuscript/` folder (e.g., `Manuscript/Complete_Manuscript.md`).

### 4. Memory Updating Protocol (CRITICAL)
Maintaining the Book Memory Bank is essential for consistency. You must seamlessly and *automatically* update the memory bank whenever substantive writing is done. No scripts or manual user steps should be required.
1. Consult `references/book_memory_protocol.md` for the strict rules on how and when to update the memory bank files.
2. Consult `references/memory_update_prompts.md` for specific criteria on what changes should trigger file modifications (e.g., character traits, plot developments, world-building).
3. If the user explicitly says "update memory bank", perform a comprehensive audit and update across all memory files based on the most recent chapter or outline. Always provide a clear summary of which files were updated and what changed.

### 5. Chapter Review & Revision
When the user asks to review, revise, or polish a chapter:
1. Read the chapter draft, its outline, adjacent chapters (for continuity), and all context files (Style, Characters, Worldbuilding).
2. Consult `references/revision_checklist.md` for the quality gates and review focus areas.
3. Review in this order: Language → Emotion → Dialogue → Pacing → Continuity.
4. Apply revision principles: preserve voice above all, revise gently, clarify emotion without explaining, respect ambiguity.
5. **Never** introduce new scenes, events, or characters during review. **Never** resolve conflicts the author left open intentionally.
6. Save revised version and announce changes.

### 6. Continuity Check
When the user asks to "check continuity", "run continuity check", or "check for consistency":
1. Follow the Continuity Diagnostic Report process in `references/book_memory_protocol.md`.
2. Cross-check all chapters against the memory bank for timeline, character, worldbuilding, emotional, and thematic consistency.
3. Generate a diagnostic report saved to `Research/continuity_diagnostic_report.md`.
4. Use question-based language — flag issues, don't impose fixes.

## References
This skill relies on the following reference documents to guide the AI's behavior:
- `references/author_rules.md`: Provides the artistic identity, style guidelines, and quality standards for fiction writing. Includes dialogue language handling, historical title/honorific rules, and contextual address rules.
- `references/book_memory_protocol.md`: Outlines the architecture of the Book Memory Bank, explicit rules for maintaining context files, and the Continuity Diagnostic Report process.
- `references/memory_update_prompts.md`: Contains criteria and expected templates for auditing and updating the memory bank when significant story changes occur.
- `references/story_forge.md`: **The Story Forge** — governs the one-time onboarding conversation for new book projects. Includes genre selection, emotional core discovery, narrative structure choice, and dialogue language preference. Run only at initialization; never repeat.
- `references/readme_template.md`: Template for generating the project `README.md` after initialization.
- `references/chapter_craft.md`: Chapter-level writing techniques — opening/closing formulas, book size options, chapter structure templates, reader engagement techniques, drafting best practices.
- `references/revision_checklist.md`: Comprehensive quality checklist for chapters — story, prose, voice, characters, continuity, engagement, historical accuracy checks, and DO/DON'T quick-scan list.
- `references/character_worldbuilding_tables.md`: Structured table templates for character profiles (19 fields), worldbuilding (10 categories), conflict mapping, synopsis structure, and timeline tracking.
- `docs/USAGE.md`: Human-readable guide with real example dialogues for every stage of using this skill.
