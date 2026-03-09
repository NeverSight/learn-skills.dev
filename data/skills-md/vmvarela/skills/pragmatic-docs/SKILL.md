---
name: pragmatic-docs
description: Write concise, useful project documentation (READMEs, guides, docs/) inspired by Philip Greenspun's pragmatic style. Use when creating or improving README.md, writing module docs, CONTRIBUTING.md, or structuring any project documentation for software projects.
---

# Pragmatic Documentation

Write documentation that respects the reader's time, explains *why* before *how*, uses real examples instead of abstract descriptions, and isn't afraid to have an opinion. Inspired by Philip Greenspun's approach: start with the big idea, show real code in context, acknowledge trade-offs honestly, and stop writing before the reader stops reading.

## Core Principles

### 1. Start With Why

Every document opens with **The Big Idea**: what this thing is, why it exists, and what problem it solves — in 1–3 paragraphs. If you can't explain why someone should care in three paragraphs, you don't understand the project well enough.

Bad: "This module provides a flexible, extensible, enterprise-grade solution for..."
Good: "Users kept asking the same five questions. This tool answers them automatically so maintainers can sleep."

### 2. Examples Over Abstractions

A single real example communicates more than three paragraphs of explanation. Show actual commands, real data, genuine output. Never invent `foo`, `bar`, `WidgetFactory`, or `MyApp` when you can show a concrete scenario.

Weave code into the narrative — don't banish it to a separate "Examples" ghetto. When explaining a data model, show the schema right there. When explaining a CLI, show the command and its output inline.

### 3. Opinions Are Valuable

Say what you think. "X is better than Y for this because..." is more useful than "X and Y are both options." Acknowledge trade-offs, recommend a path, explain your reasoning. Readers can disagree — but at least they have a position to evaluate.

### 4. Honest About Limitations

If something doesn't work well, say so. If there's a better tool for a specific use case, point to it. "The /news module is better if you want date-based display" is more helpful than pretending your module does everything.

### 5. Brevity Is Respect

A README over 300 lines is a sign that it should be split into separate docs. Don't pad with boilerplate sections. Every sentence should earn its place. If a section would be empty or contain a single trivial line — omit it.

---

## Document Structure

Adapt this structure to context. Not every section applies to every project. **Never include empty sections or sections with trivial content just to fill a template.**

### The Big Idea (required)

Always present. 1–3 paragraphs covering:
- What is this?
- Why does it exist? What problem does it solve?
- Who is it for?

Write it so someone can read just this section and decide whether to keep reading. No jargon without immediate context. No "aims to provide" — just state what it does.

```markdown
## What is this?

PhotoResize watches a directory for new images and resizes them to three
standard sizes for web delivery. We built it because our CMS required
manual image processing and editors were wasting 20 minutes per article
on something a script handles in 2 seconds.
```

### Quick Start (when applicable)

The shortest possible path from "I found this" to "it works on my machine." Maximum 10 lines of commands. If setup genuinely requires more, the quick start shows the happy path and links to detailed installation docs.

```markdown
## Quick Start

pip install photoresize
photoresize watch ./uploads --output ./public/images
```

Don't repeat what the package manager already tells the user. Don't list every flag. Just get them to a working state.

### Under the Hood (when applicable)

How the thing works internally — but only when understanding internals actually helps the user. Architecture decisions explained narratively, not as a spec. Data models shown as actual schemas or type definitions, not UML diagrams or prose descriptions of fields.

Follow Greenspun's pattern: show the data model, then explain the interesting decisions. What constraints did you add and why? What did you choose *not* to store and why?

```markdown
## Under the Hood

The core data model is simple — one table per feed source, one table
for processed items:

    create table feed_sources (
        source_id   serial primary key,
        url         text not null unique,
        check_interval_minutes  integer default 60
    );

We chose not to store the full article body because it doubles storage
without clear benefit — the original URL is always one click away.
```

### Configuration / API (when applicable)

Only document what isn't obvious from types, signatures, or `--help` output. Focus on:
- Non-obvious defaults and why they were chosen
- Combinations of options that interact in surprising ways
- The one config key that 90% of users will need to change

Don't reproduce your entire type system or CLI `--help` in Markdown. That's what `--help` is for.

### Examples (recommended)

Real scenarios, not abstract demos. Each example should solve a problem someone actually has. Introduce each example with one sentence explaining *when* you'd use this pattern.

```markdown
### Resizing for social media cards

Social platforms crop unpredictably. Force a 2:1 aspect ratio and let
the smart-crop algorithm pick the focal point:

    photoresize convert photo.jpg --aspect 2:1 --smart-crop --output card.jpg
```

### Related Projects / Modules (when applicable)

Cross-references to alternatives or complementary tools. For each one, explain in one sentence *when* the reader should use that instead. This is not a competitors list — it's honest guidance.

```markdown
## Related

- **ImageMagick** — better if you need arbitrary image transformations
  beyond resizing. We actually shell out to it under the hood.
- **sharp** — faster for Node.js projects; PhotoResize is for Python
  shops that want a CLI-first workflow.
```

### Limitations / Future (optional)

Only if there are genuine, non-obvious limitations the user will hit. Don't include a roadmap of features you might never build.

```markdown
## Limitations

- No WebP output yet (tracking in #142)
- Smart cropping works poorly on images with multiple faces
```

---

## Writing Rules

### Voice and Tone

- Use active voice. "The server sends a response" not "A response is sent by the server."
- First person is fine when sharing design rationale. "We chose X because..." or "I built this after..."
- Write as one competent engineer explaining to another. Not as a marketing team, not as a legal department.
- Humor and personality are welcome when they emerge naturally. Don't force it.

### What to Include

- **Why** decisions were made — not just what was decided.
- **Real** commands, real data, real output.
- **Trade-offs** — what you gave up and what you gained.
- **Cross-references** as links, not as inlined content from other docs.
- **One** sentence explaining each code block before showing it.

### What to Omit

- Badges beyond 2–3 genuinely useful ones (build status, version, license).
- Table of contents for documents under 100 lines.
- Sections that repeat information available via `--help`, type signatures, or JSDoc.
- The words "aims to", "leverages", "utilizes", "facilitates", or "enterprise-grade."
- Auto-generated API docs inlined into a README — link to them instead.
- Empty template sections ("## Contributing", "## License" with no content).

### Code in Documentation

- Show code inline with the narrative, right after the sentence that explains it.
- Use the actual language of the project for code blocks (not pseudocode).
- Keep snippets short — 5–15 lines ideal. If longer, you're showing too much at once.
- Annotate the *interesting* lines with comments. Don't comment the obvious.

### Length Guidelines

| Document | Target length | Notes |
|----------|--------------|-------|
| README.md | 50–200 lines | The front door. Concise. Links out for details. |
| Module doc | 30–150 lines | One module = one concern = one doc. |
| CONTRIBUTING.md | 30–80 lines | Setup + conventions + PR process. Nothing more. |
| Architecture doc | 100–300 lines | The Big Idea + data model + key decisions. |

If a document exceeds its target, consider splitting rather than truncating. Two focused docs beat one sprawling one.

---

## Anti-Patterns to Avoid

**The Template Cemetery.** A README with 15 sections, half of them containing "TODO" or a single sentence. Every section must earn its place.

**The API Mirror.** Documentation that reproduces every function signature and parameter type already visible in the code. Document *behavior*, *decisions*, and *gotchas* — not signatures.

**The Corporate Voice.** "This project aims to provide a comprehensive, scalable solution for..." — nobody talks like this. Say what the thing does.

**The Completeness Trap.** Trying to document every edge case and option upfront. Document the 80% path well. Let issues and discussions handle the edge cases.

**The Changelog README.** A README that's mostly a history of changes. That's what CHANGELOG.md and git log are for.

**The Badge Wall.** Twelve badges at the top of the README, half of them broken. Pick the 2–3 that genuinely help (CI status, npm version, license).

---

## When to Apply This Skill

Use this approach when:

- Creating a new `README.md` for any software project
- Improving or rewriting existing documentation
- Writing module-level docs in a `docs/` directory
- Creating `CONTRIBUTING.md`, architecture docs, or setup guides
- Documenting a new feature, API, or service
- Reviewing documentation for conciseness and usefulness

### Adaptation by Project Type

**Libraries/Packages:** Lead with Quick Start (install + basic usage). The Big Idea explains *when* to reach for this library over alternatives.

**CLIs:** Lead with the single most common command. Show real terminal output. Document flags that aren't self-explanatory from `--help`.

**APIs/Services:** Lead with The Big Idea (what does this service do). Show a real request/response pair. Data model in Under the Hood.

**Frameworks:** Lead with The Big Idea (what this framework believes). Quick Start gets to "hello world." Under the Hood explains the mental model.

**Internal tools:** Be more honest about limitations. Your audience can't switch to a competitor — help them work around known issues.
