---
name: technical-documentation
description: Use this skill when the user wants to write, rewrite, structure, or review technical documentation for software developers. Covers READMEs, tutorials, how-to guides, concepts, API references, troubleshooting guides, release notes, and documentation audits. Trigger for requests to document a feature, improve docs, explain an API, create setup instructions, or review documentation quality, even when the user does not name a style guide.
license: Apache-2.0
metadata:
  author: dsebastien
  version: "1.0.0"
  repository: "https://github.com/dsebastien/technical-documentation-skill"
  source: "https://developers.google.com/style"
---

# Technical documentation

Create accurate, useful, and accessible technical documentation. Follow
project-specific writing rules first, then this skill, then the Google developer
documentation style guide.

## Start with a documentation contract

Before drafting, determine the following information from the request and the
available project context:

- Audience and assumed technical knowledge
- Reader's goal or question
- Document type
- Product, API, or software version
- Prerequisites and environment
- Scope and explicit exclusions
- Evidence that the reader succeeded

Ask a focused question only when a missing answer would materially change the
document. Otherwise, make the smallest reasonable assumption and state it
briefly.

## Ground the content

Inspect the relevant source code, API schema, commands, tests, user interface,
configuration, and existing documentation before writing. Prefer primary
sources and behavior that you can verify.

Never invent any of the following details:

- Commands, flags, parameters, endpoints, or configuration keys
- Default values, limits, permissions, or compatibility claims
- Output, error messages, side effects, or recovery behavior
- Version support, deprecation status, or security guarantees

If a detail cannot be verified, label it as an assumption or omit it. Preserve
important project terminology even when a different term might sound better.

## Choose the document type

Use the structure that matches the reader's need:

- **Tutorial**: help a learner complete a guided, end-to-end experience.
- **How-to guide**: help a reader complete one practical goal.
- **Concept**: explain how or why something works.
- **Reference**: provide precise facts that readers can scan and look up.
- **Troubleshooting guide**: connect symptoms to causes, diagnostics, and
  recovery steps.
- **README**: explain the project's purpose and provide the shortest path to a
  working result.
- **Release note**: explain a user-visible change, its impact, and any required
  action.

For ready-to-use outlines, read
[document patterns](references/document-patterns.md).

## Draft for task completion

Lead with what the document helps the reader do or understand. Put critical
information before background details.

For task-oriented documents:

1. State the outcome.
2. List prerequisites before the procedure.
3. Present steps in the order that the reader performs them.
4. Include commands and code where they are needed.
5. Explain how to verify success.
6. Add troubleshooting only for likely or costly failures.
7. End when the reader has achieved the stated outcome.

For conceptual and reference documents, organize information around reader
questions and lookup tasks, not the internal structure of the implementation.

## Apply the writing rules

Use these defaults unless project-specific guidance requires otherwise:

- Write in a conversational, respectful, and direct tone.
- Address the reader as "you." Use imperative verbs for instructions.
- Prefer active voice and present tense.
- Use simple, precise words and consistent terminology.
- Keep sentences focused. Aim for fewer than 26 words when practical.
- Give each paragraph one main idea and put that idea first.
- Remove throat-clearing, repetition, filler, and unnecessary background.
- Define unfamiliar abbreviations on first use.
- Avoid idioms, jokes, slang, buzzwords, and culture-specific references.
- Avoid claims such as "easy," "simple," "obvious," or "just."
- Avoid placeholder phrases such as "please note" and "at this time."
- Use inclusive language and examples that work for a global audience.

Read [Google style guidance](references/google-style-guide.md) when you need
detailed rules or source links.

## Write headings and structure

- Use sentence case for titles and headings.
- Use a unique level-1 heading for the page title.
- Keep the heading hierarchy logical; don't skip levels.
- Start task headings with a bare verb, such as "Create an API key."
- Use noun phrases for conceptual headings, such as "API key lifecycle."
- Use `Optional:` at the start of an optional section heading.
- Avoid links, sequence numbers, and unnecessary punctuation in headings.
- Add content between a parent heading and its first child heading.

Make the page scannable with short sections, informative headings, lists, and
tables only where those structures improve comprehension.

## Write procedures

- Use a numbered list when order matters.
- Start every step with an imperative verb.
- Put the location or context before the action.
- Keep one main action in each step.
- Put a goal before its action and a result after its action.
- Start optional steps with `Optional:`.
- Use bullets instead of a numbered list for a single-step procedure.
- Keep list items parallel in grammar, capitalization, and punctuation.
- Don't repeat a procedure when a precise link can reuse it safely.

Include enough context for the reader to act, but don't explain obvious UI
gestures or implementation details that don't affect the task.

## Present code and technical elements

- Introduce every code sample and explain its purpose.
- Prefer minimal, runnable examples over fragments that hide required context.
- Follow the project's code style and use a language identifier on fenced code
  blocks.
- Keep commands copyable. Separate commands from their output.
- Explain placeholders immediately after the sample.
- Use uppercase snake case for placeholders, such as `PROJECT_ID`.
- Use code font for commands, filenames, paths, methods, fields, and literal
  values.
- Use bold for visible UI labels, such as **Save**.
- Don't use screenshots for code, terminal output, or essential text.
- Verify examples when the environment permits it.

## Create useful links

- Use short, descriptive link text that makes sense out of context.
- Link to the most specific relevant page or section.
- Provide brief context locally instead of sending the reader elsewhere for a
  small fact.
- Avoid vague link text such as "click here," "this page," or raw URLs.
- Explain downloads, new windows, or other unexpected link behavior.
- Avoid duplicate links unless distant sections need separate entry points.

## Make the document accessible and global

- Don't rely on color, position, size, or images alone to convey meaning.
- Provide meaningful alt text for informative images and empty alt text for
  decorative images.
- Use semantic headings, lists, tables, and HTML elements.
- Use descriptive labels and link text that remain clear to screen-reader users.
- Avoid directional references such as "above," "below," or "on the right."
- Use unambiguous dates, times, units, and examples.
- Avoid figurative, violent, ableist, and unnecessarily gendered language.
- Don't encode essential information only in a table, image, audio file, or
  video.

## Review in separate passes

Review the draft in this order:

1. **Technical accuracy**: verify behavior, names, versions, commands, and
   examples against primary sources.
2. **Task completion**: confirm that the reader can reach and verify the stated
   outcome.
3. **Structure**: check the document type, information order, headings, and
   navigation.
4. **Clarity**: remove ambiguity, passive voice, excessive words, and undefined
   terminology.
5. **Accessibility and inclusion**: check links, images, semantic structure,
   language, and global usability.
6. **Consistency**: check terminology, formatting, capitalization, and list
   structure.

For a detailed final pass, read the
[documentation review checklist](references/review-checklist.md).

## Deliver the result

When writing or rewriting documentation, return the publication-ready content
unless the user requests commentary. Preserve valid project conventions and
explain only material assumptions, unresolved accuracy gaps, or intentional
departures from local style.

When reviewing documentation, prioritize findings that affect correctness,
task completion, safety, accessibility, or comprehension. Cite the exact
section and propose a concrete replacement. Don't report subjective preferences
as defects.

## Source hierarchy

Apply sources in this order:

1. Project-specific style, terminology, and templates
2. Verified product behavior and primary technical sources
3. This skill
4. [Google developer documentation style guide](https://developers.google.com/style)
5. Relevant language or publishing standards

Depart from a style recommendation when doing so makes the content clearer or
more accurate for the intended reader. Apply that departure consistently.
