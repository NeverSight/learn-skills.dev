---
name: ux-writing
description: >-
  Review and write UI text following Material Design 3 UX writing best
  practices. Use when writing new UI text (buttons, labels, dialogs, error
  messages, notifications, titles, menus, tooltips, empty states, form fields)
  or reviewing and fixing existing UI text for clarity, consistency, and
  accessibility. Covers sentence case, word choice, grammar, punctuation,
  pronouns, abbreviations, and consequence communication. Triggers on any task
  involving microcopy, interface copy, UI strings, or UX text.
---

# UX Writing

Review and write UI text based on the Material Design 3 style guide.

## Workflow

Determine whether the task is a **review** of existing text or **creation** of new text, then follow the appropriate workflow.

### Review workflow

1. Read the target file(s)
2. Load `references/md3-style-guide.md`
3. Check all text against the three rule categories:
   - Best practices (consequences, scannability, sentence case, abbreviations)
   - Word choice (second person, pronoun consistency, first-person caution)
   - Grammar and punctuation (periods, contractions, commas, colons, exclamation points, ellipses, parentheses, ampersands, dashes, hyphens, italics, caps)
4. Report each finding in this format:
   ```
   file:line — "original text" — [Rule N.N name] — Suggested: "improved text"
   ```
5. Summarize findings grouped by category

### Creation workflow

1. Identify the UI element type (button, error message, dialog, tooltip, label, heading, empty state, notification, menu item, form field)
2. Load `references/md3-style-guide.md`
3. Apply the rules relevant to the element type:
   - **Buttons**: Sentence case, skip periods, use contractions, skip ellipses
   - **Error messages**: Explain consequences, use second person, skip exclamation points
   - **Dialogs**: Explain consequences, skip periods for single sentences, use contractions
   - **Headings/titles**: Sentence case, skip colons, use scannable words
   - **Labels/tooltips**: Sentence case, skip periods, spell out abbreviations
   - **Empty states**: Use second person, skip exclamation points, explain next steps
   - **Notifications**: Explain consequences, use second person, use contractions
4. Draft the text
5. Self-check the draft against all applicable rules
6. Present the text with a brief rationale citing the rules applied

## Quick reference

Key rules to check first:

| Rule | Summary |
|------|---------|
| Sentence case | Capitalize only the first word (not Title Case) |
| Second person | Use "you/your", not "the user" |
| No mixed pronouns | Don't combine "my" with "your" in the same context |
| Skip periods | Omit periods for single-sentence UI text |
| Use contractions | "Don't" instead of "Do not" for natural tone |
| Serial comma | "Folders, files, and images" (Oxford comma) |
| No caps blocks | Never use ALL CAPS — use sentence case |
| No exclamation points | Reserve for greetings or celebrations only |
| Explain consequences | State what happens and how to undo |

## Full style guide

For the complete set of 20 rules with Do/Don't examples, load `references/md3-style-guide.md`.
