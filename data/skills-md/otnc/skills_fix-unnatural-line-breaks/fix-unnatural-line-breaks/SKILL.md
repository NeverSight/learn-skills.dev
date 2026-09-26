---
name: fix-unnatural-line-breaks
description: Detects and fixes "unnatural line breaks" in prose (Markdown/README-style documentation, and code comments or docstrings) — newlines inserted mid-sentence just to keep lines under some fixed column width. Works on both English and Japanese text. Use for requests like "fix the line breaks," "this is hard-wrapped," "the text is cut off mid-sentence," "unnatural line wrapping," "改行がおかしい," "文の途中で改行が入っている," "一定の文字数で折り返されている," as well as when writing, reviewing, or rewriting documentation and comments. Does not cover restructuring bullet lists, rewording headings, or removing AI-sounding phrasing/redundancy (those belong to other skills).
metadata:
  trigger: line-break/line-wrap checks and fixes in documentation and code comments
  language: en, ja
---

# fix-unnatural-line-breaks

A skill for eliminating a specific bad habit: inserting a newline mid-sentence just to keep the line under some fixed column width. Line breaks should only appear at meaningful boundaries — paragraph breaks, list item boundaries, and around headings.

## Core principle

Don't break a sentence or paragraph until it actually ends. Even when a line "feels" long, keep writing on the same line until the next meaningful boundary (end of paragraph, end of a list item, before/after a heading, before/after a code block). Let the editor, browser, or terminal handle visual wrapping (soft wrap) — the source itself should not contain a hard-coded newline chosen purely for line length.

This applies equally to English and Japanese, but the damage is arguably worse in Japanese. Japanese has no spaces between words, so an arbitrary line break doesn't look grammatically broken the way it might in English — yet breaking right after a comma, particle, or in the middle of a phrase still disrupts the reading rhythm and makes it easy to misread where a clause actually ends.

The target is both prose documentation (Markdown, README files) and code comments, docstrings, and JSDoc. For documentation, most Markdown renderers collapse a single newline inside a paragraph into a single space, so the rendered output often looks fine either way — but the raw source still suffers: it's harder to read as source, diffs get needlessly large when a whole paragraph reflows, and there are places where the raw newline is shown as-is (commit messages, terminals, an editor's hover tooltip for a code comment). For code comments there is no renderer to save you — the line break is shown exactly as written, so the harm is direct and immediate.

## Do

- When writing new prose (documentation or comments) from scratch, write one paragraph per line (or one sentence per line) from the start, and never wrap at an arbitrary column width.
- When reviewing or fixing existing prose, use the criteria in `references/detection.md` to find breaks that cut a sentence in the middle, then fix them following `references/rules.md`.
- To fix one, simply remove the line break and join the two lines: insert a single space for English, and nothing (no space) for Japanese. See `references/examples.md` for concrete cases where the right join is ambiguous.
- It's fine — expected, even — for the fixed line to become very long. The only thing that should trigger a new line break is a structural boundary (paragraph, list item, heading, code block), never a character count.
- In a comment block, if two paragraphs need a visible separator, use an unmarked blank line (no `//`/`#`/`*`) or no separator at all — never a bare comment marker with nothing after it. Nobody writes a lone `//` by hand; see `references/rules.md`.

## Don't

- Don't restructure content: splitting into bullet lists, rewording headings, removing redundant phrasing, or scrubbing AI-sounding style are out of scope (hand those off to a skill built for that, such as `natural-japanese` or `stop-ai-slop-jp` for Japanese text).
- Don't touch Markdown tables, code block contents, URLs, inline code spans, or intentional Markdown line breaks (two trailing spaces, a trailing backslash, or an explicit `<br>`).
- Don't touch commit messages or code formatting itself (that's Prettier/ESLint's job). The target here is prose meant for humans to read.
- Don't run this against structured config formats such as CI workflow YAML, JSON, or embedded shell scripts. `scripts/lint.mjs` recognizes YAML frontmatter and simple `key: value` lines well enough to avoid the worst false positives, but it has no real YAML parser and cannot tell a wrapped prose sentence inside a block scalar (`key: |`) from wrapped shell script. Structured config is out of scope; only apply this skill to Markdown prose and code comments/docstrings.

## Workflow

1. Identify what kind of file you're looking at — Markdown documentation, or code comments.
2. Read `references/detection.md` and keep the relevant criteria in mind for the language(s) involved (English, Japanese, or both mixed in the same file).
3. If Node.js is available (it almost always is, since Claude Code itself runs on it), run `node scripts/lint.mjs <file>` to mechanically surface suspicious breaks (add `--json` for structured output). No install or dependency is needed — it's plain Node.js with no third-party packages. Without Node.js, do the same review by eye using `references/detection.md`.
4. **`lint.mjs` output is not the full list of what to fix.** It's a small set of regex heuristics, so it both flags things that are fine (false positives) and misses real unnatural breaks it has no rule for (false negatives) — a break that doesn't end in a tracked particle/word but is still mid-sentence, for instance. Treat it as a starting hint, not a checklist to clear. Filter out its false positives (code blocks, tables, intentional breaks), then still read every paragraph and comment block in the file yourself against `references/detection.md`, including the parts the tool didn't flag at all.
5. Apply the fixes following `references/rules.md`: merge broken sentences back into one line, and leave paragraph/list/heading/code-block boundaries untouched.
6. Re-read the fixed paragraph to confirm the meaning and tone haven't shifted.

## Quick self-check

Before calling it done, confirm:

- [ ] No line break remains in the middle of a paragraph without a meaningful boundary justifying it
- [ ] No single list item is still wrapped across multiple lines (unless the item is genuinely long and that's intentional)
- [ ] No single sentence in a code comment or docstring still spans multiple comment lines
- [ ] The fix didn't touch code blocks, tables, URLs, or intentional line breaks
- [ ] No comment block uses a bare `//`/`#`/`*` marker as a paragraph separator
- [ ] Every paragraph and comment block was actually read end to end — not just the lines `lint.mjs` happened to flag
