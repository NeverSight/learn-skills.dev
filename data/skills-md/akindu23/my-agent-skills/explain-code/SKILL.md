---
name: explain-code
description: Explains code in a short, scannable structure with a TL;DR, sectioned ideas, and small code examples.
disable-model-invocation: true
---

# Explain Code

Explain the user-scoped code as a short, scannable post. Prefer small code sketches over exhaustive walkthroughs.

Read [`../simplify-this/references/ste.md`](../simplify-this/references/ste.md). Apply rules 1, 2, 3, and 5 to the title, the TL;DR, and each section lead-in. Keep Format as the structure. Name identifiers from the code.

**Done when:** every scoped idea has a section with a sketch, and those four STE rules hold on the title, TL;DR, and lead-ins.

## Defaults

- Match the user's scope exactly.
- Use this structure: `#` title, `## TL;DR`, then one or more `##` sections.
- Each `##` section covers one idea and includes at least one fenced code block.
- Keep snippets small.
- Simplify code when useful, but stay faithful to behavior.
- State only intent the code or prompt supports.

## Format

### `#` Title

One line naming the topic.

### `## TL;DR`

Write 2-3 short sentences that give the gist to someone who did not write the code.

Optional: include one small `mermaid` block only when the main story is easier to grasp as flow or handoff.

After the TL;DR section, add a horizontal rule: `---`.

### `##` Sections

For each section:

1. Write a `##` title (no emoji required).
2. Add a one- or two-sentence lead-in.
3. Show one fenced code block.

Stop the section after the code block.

Separate body sections with a horizontal rule: `---`.

## Code

- Show only the code needed for the current section's point.
- Default to about 10 non-blank lines or fewer.
- Omit anything that does not help explain the current point.
- Use `...`, `// ...`, placeholders, or simplified identifiers when that makes the idea easier to see.
- Every snippet must include short intent comments on the key lines. Use them to tell the reader what this line is doing here and why it matters.
- Prefer behavior-faithful sketches over verbatim excerpts.

## User clarifications

For a discrete decision with about 2-6 clear options, use the session's structured MCQ tool.

1. Probe the tool list for `AskQuestion` (Cursor) or `AskUserQuestion` (Claude Code).
2. Call the one that exists, using that tool's schema from the session - field names are not interchangeable.
3. If neither exists, ask the same choices in ordinary chat, same options and order.

Put every fact the user needs to choose inside the question and option text. Some clients hide assistant preamble in the same turn as the tool call.

Free-form answers stay in plain chat.

Ask **one decision at a time** when this skill already sequences questions that way.

## Scope fallback

- If the user gives no scope and there are unstaged changes, default to the unstaged diff.
- If the user gives no scope and there are no unstaged changes, ask the user to identify the file, diff, or area they want explained.