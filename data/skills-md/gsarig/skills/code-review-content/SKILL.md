---
name: code-review-content
description: "Reviews changes to prose files (markdown, text, blog posts, docs). Focuses on voice, grammar, factual claims, dead links, and structure. Loads the project's voice or style guide when one exists. Skips linter and Actions hash verification."
when_to_use: "Use when reviewing changes to prose files (`.md`, `.mdx`, `.txt`, `.rst`) or content under `docs/`, `content/`, `posts/`. Invoked directly with a PR URL or diff file path, or dispatched by `/code-review`. Follow all steps in order; do not shortcut based on this description."
argument-hint: "[PR URL | path to diff file] [--source=...] [--pr=<URL>] [--file=<path>]"
effort: medium
allowed-tools: Bash(git *) Bash(gh *) Read Grep
---

## Steps

### 1. Source and diff

Read `~/.claude/skills/code-review/references/review-shared.md` and follow its source detection and diff fetching sections. If `--source` and the corresponding identifier args were passed, use those and skip any prompting.

### 2. Load voice reference (conditional)

If the project defines a voice or style guide (a styleguide doc, a writing-voice skill, or a CLAUDE.md section on tone), read it and apply its rules throughout the review.

### 3. Review

Read `~/.claude/skills/code-review/references/review-checklist.md` first for any general principles.

Focus on:

- Voice consistency. When a voice guide is loaded, follow its rules. Otherwise match the tone of adjacent prose.
- Grammar and tense agreement.
- Factual claims that can be verified (dates, numbers, names, attributions). Flag those you cannot verify and ask the user to confirm rather than guessing.
- Dead or wrong links. Fetch reachable URLs if helpful; flag any you cannot verify.
- Structure and flow. Section ordering, missing or redundant transitions, headings that don't match their content.
- Redundant phrasing.
- Accidental tone shifts within or across paragraphs.

Do not flag established prose-style preferences if they are already consistent with adjacent posts. Honour the common review rules in the shared doc.

### 4. Output

Format per the output section of `~/.claude/skills/code-review/references/review-shared.md`. The linter and GitHub Actions hash verification sections do not apply to content reviews; do not run those steps.
