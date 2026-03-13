---
name: cbeams-git-commit-messages
description: Write clear, consistent Git commit messages following Chris Beams' seven rules. Use when the user asks for a commit message, asks to improve one, or shares a diff and wants commit wording.
metadata:
  version: "1.1.0"
---

# cbeams-git-commit-messages

## Purpose

Help the user write, revise, or review Git commit messages that are easy to scan, consistent across a repo, and informative in history.

This skill supports both single-line commits and multi-paragraph commit bodies.

## When to use

Use this skill whenever the user:
- asks for a commit message,
- pastes a diff / summary and asks what to commit,
- asks you to improve a commit message,
- asks you to review whether a commit message is "good".

## Instructions

When producing a commit message:

1. Subject line rules
   - Output a single subject line first.
   - Use the imperative mood (a command) - e.g. "Add", "Fix", "Refactor", "Remove", "Update".
   - Capitalise the first character.
   - Do not end with a full stop.
   - Aim for 50 characters or fewer.
   - Treat 72 characters as a hard ceiling - if it will exceed 72, rewrite.
   - Prefer rewriting over truncation.
   - Do not sacrifice clarity only to force 50 characters; preserve meaning.
   - Avoid past tense subjects such as "Added" or "Fixed".
   - Avoid vague subjects such as "Update stuff" or "Misc changes".
   - Only use ASCII characters in the subject and body.

2. Body rules
   - Only include a body if it adds value.
   - Separate subject and body with a single blank line.
   - Wrap body lines at 72 characters.
   - Explain what changed and why it changed.
   - Avoid explaining how it changed (the diff already shows how).
   - Use short paragraphs separated by blank lines when there are multiple ideas.
   - Separate paragraphs in the body with a single blank line.
   - Prefer bullet points to organize multiple points; keep each bullet concise.
   - Use this structure when helpful: Context -> Change -> Reason/impact.

3. Optional footer
   - If the user provides an issue / ticket reference, include it at the end as a footer
     line (or lines), after a blank line.
   - Prefer forms like:
     - "Refs: #123"
     - "Resolves: #123"
     - "Fixes: #123"
   - If the repo uses another tracker format (for example, "ABC-123"), preserve that
     format instead of converting to "#123".
   - Do not invent issue references.

## Output format

Always output:
- The subject line on the first line.
- Then the body (if any), starting after one blank line.
- No surrounding quotation marks.
- No Markdown formatting.
- Separate paragraphs in the body with a single blank line.

If the user provides insufficient context (no summary of changes), ask for:
- a one-two sentence summary of what changed, why it changed, and expected impact or risk,
or
- the diff / list of files changed.

## Examples

Good subject only:
Refactor cache key generation

Good subject and body (prose):
Fix race condition in webhook retries

Prevent concurrent retry workers from processing the same webhook event.

This avoids duplicate outbound calls and inconsistent delivery state
during peak traffic.

Good subject and body (bullets):
Improve commit-message skill and examples

- Move version into metadata.version to match the Agent Skills specification
- Add examples and a body template: Context -> Change -> Reason/impact
- Expand subject anti-patterns and quality checks; prefer rewriting over
  truncation to preserve meaning
- Remove frontmatter tags to comply with the spec

Bad -> better rewrite:
Bad: Updated things
Better: Update deployment health check defaults

## Quality checks (do before finalising)

- Subject <= 50 characters where possible; never > 72.
- Subject is imperative, capitalised, and has no trailing full stop.
- If there is a body: wrapped at 72 characters, explains what + why, not how.
- Output has no Markdown formatting, quotation marks, or code fences.
- Output has no trailing whitespace.
