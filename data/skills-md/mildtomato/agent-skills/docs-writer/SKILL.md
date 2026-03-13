---
name: docs-writer
description: |
  Always use this skill when writing, reviewing, or editing documentation,
  specifically for files in `apps/docs/` or any `.md`/`.mdx` files in the
  repository.
license: MIT
metadata:
  author: MildTomato
  version: '1.0.0'
---

# Documentation writer

This skill provides standards for writing, reviewing, and editing documentation.

## Phase 1: Documentation standards

Adhere to these principles when writing, editing, and reviewing documentation.

### Voice and tone

Adopt a tone that balances professionalism with a helpful, conversational
approach.

- **Perspective and tense:** Address the reader as "you." Use active voice and
  present tense (for example, "The API returns...").
- **Tone:** Professional, friendly, and direct.
- **Clarity:** Use simple vocabulary. Avoid jargon, slang, and marketing hype.
- **Global audience:** Write in standard US English. Avoid idioms and cultural
  references.
- **Requirements:** Be clear about requirements ("must") vs. recommendations
  ("we recommend"). Avoid "should."
- **Word choice:** Avoid "please" and anthropomorphism (for example, "the server
  thinks"). Use contractions (don't, it's).

### Language and grammar

Write precisely to ensure your instructions are unambiguous.

- **Abbreviations:** Avoid Latin abbreviations; use "for example" (not "e.g.")
  and "that is" (not "i.e.").
- **Punctuation:** Use the serial comma. Place periods and commas inside
  quotation marks.
- **Dates:** Use unambiguous formats (for example, "January 22, 2026").
- **Conciseness:** Use "lets you" instead of "allows you to." Use precise,
  specific verbs.
- **Examples:** Use meaningful names in examples; avoid placeholders like
  "foo" or "bar."

### Formatting and syntax

Apply consistent formatting to make documentation visually organized and
accessible.

- **Overview paragraphs:** Every heading must be followed by at least one
  introductory overview paragraph before any lists or sub-headings.
- **Text wrap:** Wrap text at 80 characters (except long links or tables).
- **Casing:** Use sentence case for headings, titles, and bolded text.
- **Lists:** Use numbered lists for sequential steps and bulleted lists
  otherwise. Keep list items parallel in structure.
- **UI and code:** Use **bold** for UI elements and `code font` for filenames,
  snippets, commands, and API elements. Focus on the task when discussing
  interaction.
- **Links:** Use descriptive anchor text; avoid "click here." Ensure the link
  makes sense out of context.
- **Accessibility:** Use semantic HTML elements correctly (headings, lists,
  tables).
- **Media:** Use lowercase hyphenated filenames. Provide descriptive alt text
  for all images.

### Structure

Follow these structural guidelines:

- **BLUF:** Start with an introduction explaining what to expect.
- **Experimental features:** If a feature is clearly noted as experimental, add
  the following note immediately after the introductory paragraph:
  `> **Note:** This is a preview feature currently under active development.`
- **Headings:** Use hierarchical headings to support the user journey.
- **Procedures:**
  - Introduce lists of steps with a complete sentence.
  - Start each step with an imperative verb.
  - Number sequential steps; use bullets for non-sequential lists.
  - Put conditions before instructions (for example, "On the Settings page,
    click...").
  - Provide clear context for where the action takes place.
  - Indicate optional steps clearly (for example, "Optional: ...").
- **Elements:** Use bullet lists, tables, notes (`> **Note:**`), and warnings
  (`> **Warning:**`).
- **Avoid table of contents:** If a table of contents is present, remove it.
- **Next steps:** Conclude with a "Next steps" section if applicable.

## Phase 2: Preparation

Before modifying any documentation, thoroughly investigate the request and the
surrounding context.

1. **Clarify:** Understand the core request. Differentiate between writing new
   content and editing existing content. If the request is ambiguous (for
   example, "fix the docs"), ask for clarification.
2. **Investigate:** Examine relevant code for accuracy.
3. **Audit:** Read the latest versions of relevant files in `apps/docs/`.
4. **Connect:** Identify all referencing pages if changing behavior.
5. **Plan:** Create a step-by-step plan before making changes.

## Phase 3: Execution

Implement your plan by either updating existing files or creating new ones.

### Editing existing documentation

Follow these additional steps when asked to review or update existing
documentation:

- **Gaps:** Identify areas where the documentation is incomplete or no longer
  reflects existing code.
- **Structure:** Apply structure rules (BLUF, headings, etc.) when adding new
  sections to existing pages.
- **Tone:** Ensure the tone is active and engaging. Use "you" and contractions.
- **Clarity:** Correct awkward wording, spelling, and grammar. Rephrase
  sentences to make them easier for users to understand.
- **Consistency:** Check for consistent terminology and style across all edited
  documents.

## Phase 4: Verification and finalization

Perform a final quality check to ensure that all changes are correctly formatted
and that all links are functional.

1. **Accuracy:** Ensure content accurately reflects the implementation and
   technical behavior.
2. **Self-review:** Re-read changes for formatting, correctness, and flow.
3. **Link check:** Verify all new and existing links leading to or from modified
   pages.
