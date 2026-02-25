---
name: on-writing-well
description: Write and edit technical documentation in a clear, concise, reader-focused style. Use this when asked to draft or revise docs, READMEs, guides, help pages, tutorials, or other instructional technical content.
---

# Clear technical documentation

## When to use this skill

Use this skill whenever the user asks you to write or edit documentation, instructions, README content, tutorials, reference material, release notes, or other technical explanatory writing.

## Skill instructions

Apply the rules below whenever you produce documentation. These principles are grounded in William Zinsser's *On Writing Well*, a proven foundation for clear, concise technical writing. Use them to explain technical topics effectively to your readers.

### General behaviour

- Grounded in the principles from William Zinsser's *On Writing Well*, a foundational work on clear, concise writing for readers.
- Default to concise, reader-focused, practice-oriented technical writing.
- Your goal is to explain technical topics clearly to an intelligent but busy reader.
- Write as if to one specific reader who wants to get something done.
- If repository or project documentation style guides exist, follow them first. Apply this skill for anything those guides do not specify.
- If there is any conflict between these style rules and later user instructions, obey the user’s explicit instructions first, and apply these rules where they still fit.
- When asked to “write documentation”, respond with the documentation itself – not with a description of your process.

### Purpose and audience

- Start by making the purpose clear: what this is, who it is for, and what it helps them do.
- Keep a consistent audience in mind (e.g. beginner, intermediate, expert) and match the depth to that level.
- Stay focused on the purpose; remove or de-emphasise anything that does not help the reader achieve it.

### Structure and organisation

- Organise from “why” → “what” → “how” where appropriate:
  - Why this matters or when to use it.
  - What it is (concepts, components).
  - How to use or do it (procedures, examples).
- Use a simple, logical structure with clear, descriptive headings and subheadings.
- Put related information together; avoid scattering explanations of the same idea.
- Use lists for steps, sequences, and collections of related items. Keep list items grammatically parallel.
- For procedures, use numbered steps, each starting with a clear action verb.

### Clarity and style

- Prefer short, familiar words over long or abstract ones, as long as they are accurate.
- Prefer concrete language over vague language – show what things are, what they depend on, and what they do.
- Aim for one main idea per sentence, and one controlling idea per paragraph.
- Use active voice by default: “Run the command…” rather than “The command should be run…”.
- Avoid clutter:
  - Cut empty fillers like “really”, “actually”, “in order to”, “due to the fact that”.
  - Replace wordy phrases with simpler ones when meaning stays the same.
- Be direct and human: professional, calm, and confident, without hype or slang.

### Terminology, jargon, and consistency

- Introduce each new or specialist term the first time it appears, then use it consistently.
- Use technical terms when they are the precise, standard words for your audience; avoid unnecessary jargon and acronyms.
- Avoid long “noun clusters”; break them into clearer phrases.
- Keep naming and formatting consistent for commands, options, APIs, and UI labels.

### Examples and explanations

- Whenever you introduce a key concept, include a small, concrete example when it improves clarity. Ask the user only if example choice depends on missing requirements.
- Use realistic, minimal examples that focus on the concept being explained.
- For code or commands:
  - Prefer complete, runnable snippets where feasible.
  - Highlight only what is relevant; avoid distracting extra details.
- Explain complex processes step by step, in the order a real user would follow.
- Make important constraints and edge cases explicit; do not hide them deep in dense paragraphs.

#### Before / after: clarity rewrite

**Before:**
> The current way you might configure the system is to go into the settings area and fiddle with the network options; this can be confusing and takes longer than it should.

**After:**
> Open **Settings** → **Network**. Under **Connection**, set **Mode** to **Automatic** and click **Save**.

### Reader support and navigation

- Provide signposts so readers always know where they are and what comes next.
- At the start of important sections, give a brief sentence or two about what the reader will learn or achieve.
- Make prerequisites clear (knowledge, tools, access) before instructions that depend on them.
- Put warnings, notes, and “gotchas” next to the steps or concepts they relate to, not far away in separate sections.
- Use “you” where it helps clarity: address the reader directly when giving instructions.

### Accessibility & inclusivity

- Use descriptive headings and meaningful link text.
- Provide alt text for images and captions for diagrams.
- Keep sentences short and avoid idioms; prefer clear verbs and concrete language.
- Use inclusive, neutral language and avoid gendered or culturally specific examples.
- If the content includes screenshots, ensure critical visual information is described in the text.

### Formatting conventions

- Use backticks for inline code and single commands: `npm install`.
- Use fenced code blocks with language tags for examples (for example, a `bash` or `python` fenced block). Example:

  ```bash
  # Install dependencies
  npm install
  ```

- Format UI elements as **bold** (e.g., **Settings** → **Update**) and options as `--flag`.
- Numbered steps should be imperative and start with action verbs.
- Keep examples minimal and highlight only the relevant parts.

### Accuracy, assumptions, and unknowns

- Be precise about behaviour, conditions, and limitations.
- If the user has not provided necessary details, either:
  - State reasonable assumptions explicitly, or
  - Ask for the missing information if the task truly depends on it.
- Do not invent non-obvious facts about specific systems, APIs, or environments; say when something is uncertain or implementation-dependent.

### Rewriting existing docs

- Preserve meaning and technical accuracy; confirm uncertain details with the user or an authoritative source when available.
- When assumptions are necessary, state them explicitly and label them as assumptions.
- Prefer small iterative edits rather than large rewrites when reviewers or maintainers are unsure.

### Internationalisation

- Use short sentences and avoid idioms to make content easier to translate.
- Default to SI units, but follow audience or domain conventions when needed. Prefer unambiguous date/time formats (e.g., 2026-02-11).
- Make locale-specific notes explicit (dates, currency, keyboard shortcuts).

## Internal revision checklist

Before finalising your answer, quickly check the draft against these questions and revise as needed:

1. Purpose and focus
   - Is the purpose stated clearly near the start?
   - Does every major section support that purpose?

2. Structure
   - Do sections appear in an order that matches how a real user would approach the task?
   - Are headings specific and informative?

3. Clarity and brevity
   - Are any sentences long or tangled? Can they be split or simplified?
   - Have I removed obvious filler words and redundant phrases?
   - Is each paragraph about one clear idea?

4. Technical completeness
   - Are key concepts defined the first time they appear?
   - Are steps complete, in the right order, and executable as written?
   - Are important constraints, edge cases, and failure modes clearly mentioned?

5. Navigation and examples
   - Can a reader skim the headings and quickly find the section they need?
   - Do important concepts and procedures have at least one helpful example?
