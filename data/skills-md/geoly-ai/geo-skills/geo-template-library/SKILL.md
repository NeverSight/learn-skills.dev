---
name: geo-template-library
description: >
  Standardized GEO template library for AI-citable content. Use this skill whenever the user mentions
  creating, reusing, or standardizing templates for GEO-optimized content (FAQ pages, definition
  articles, comparison guides, how-to guides, statistics roundups, landing pages, and similar formats),
  or wants cross-team consistency and speed in producing AI-citable content. Always consider this
  skill when the user asks for "a template" or "reusable structure" for GEO content, even if they do
  not explicitly mention GEO or AI citations.
---

# GEO Template Library

A **template-focused skill** that provides **ready-to-use, GEO-aware content templates** for common
high-citation formats. It lowers the barrier to using authoring skills like `geo-citation-writer` by
providing battle-tested skeletons that teams can fill in quickly and reuse across products, markets,
and languages.

This skill focuses on:

- Defining a **catalog of template types** and when to use each
- Providing **clear, copy-pasteable scaffolds** in markdown
- Highlighting **GEO-critical fields** that should be filled carefully
- Making templates **consistent across teams** while still flexible

The skill does **not** replace content-writing or optimization skills. It **prepares the canvas** so
other skills (like `geo-citation-writer`, `geo-content-optimizer`, `geo-structured-writer`) can work
on top of a solid structure.

At a glance, the main template families covered are:

- **Definition article** – "What is X?" style pages
- **FAQ page** – focused question-and-answer collections
- **Comparison guide** – A vs B vs C style breakdowns
- **How-to / tutorial** – step-based guides and playbooks
- **Statistics roundup** – "X statistics in YEAR" or benchmark collections
- **Product / feature page** – product detail and solution pages
- **GEO blog / deep-dive** – longer-form educational or thought-leadership pieces

---

## When to use this skill

Invoke this skill whenever:

- The user asks for a **template**, **blueprint**, or **content skeleton** for:
  - FAQ pages (`FAQPage`-style content)
  - Definition / "What is X?" articles
  - Comparison guides (A vs B vs C)
  - How-to / step-by-step guides
  - Original data / statistics roundups
  - Product or feature landing pages
  - GEO-ready blog posts or documentation sections
- The user wants to **standardize** how their org writes certain page types:
  - Cross-team content playbooks
  - Brand-wide GEO templates stored in a knowledge base
- The user mentions:
  - "We keep rebuilding similar pages; can we standardize?"
  - "Give me a template that our team can reuse"
  - "We want AI engines to cite our FAQ / guide / comparison page"

Do **not** restrict triggering only to these phrases. Trigger whenever the **intent** is:
“Give me a reusable, GEO-aware content template for this scenario.”

If the user only wants **one-off copy** (not a template), other skills may be a better fit, but you
can still output a template and then show how to fill it once.

---

## Relationship to other GEO skills

When available, this skill should **cooperate** with other GEO skills:

- `geo-citation-writer`: uses the templates as starting points for high-citation content
- `geo-content-optimizer`: optimizes filled-in templates for GEO performance
- `geo-structured-writer`: enriches templates with additional structure where needed
- `geo-schema-gen`: maps templates to Schema.org types and JSON-LD scaffolds
- `geo-llms-txt`: uses finished pages built from templates in AI-facing index structures

If these skills are not present, still:

- Provide high-quality templates
- Clearly mark **which sections are most important** for AI citation
- Offer suggestions for how a human can fill and refine them manually

---

## High-level workflow

Whenever this skill is used, follow this workflow, unless the user explicitly asks for a subset:

1. Clarify the scenario and constraints
2. Select the best-matching template type(s)
3. Generate one or more templates with GEO-focused annotations
4. Show example filled-in snippets (optional but recommended)
5. Provide usage notes and team guidelines

### 1. Clarify scenario and constraints

Briefly capture:

- **Content goal**:
  - e.g., "FAQ page for B2B SaaS pricing", "What is zero-shot learning?", "Compare our product vs X"
- **Primary audience and expertise level**:
  - Beginner, practitioner, executive, technical buyer, etc.
- **Channel / surface**:
  - Main website, docs, blog, knowledge base, product page, landing page, etc.
- **AI / GEO priorities**:
  - Become default answer for a query
  - Clarify entity definition
  - Provide trusted statistics or benchmarks

Output a short `## Scenario Summary` section (5–8 bullets) so the chosen template is clearly framed.

### 2. Select template type(s)

Map the scenario to one or more **template families**. Use the catalog from
`references/templates-catalog.md`:

- Definition article (`definition-article`)
- FAQ page (`faq-page`)
- Comparison guide (`comparison-guide`)
- How-to / tutorial (`howto-guide`)
- Statistics roundup (`stats-roundup`)
- Product / feature page (`product-page`)
- GEO blog / deep-dive (`geo-blog`)

In the answer, output a brief `## Template Selection` section that:

- Names the chosen template type(s)
- Explains **why** they fit this scenario
- Mentions any **secondary templates** that might also be useful later

If the scenario is ambiguous, pick the **closest** template type and adapt it, explaining your choice.
When it is clearly helpful, you may also **return multiple templates** (for example, a `product-page`
template plus an embedded `faq-page` template).

### 3. Generate templates with GEO annotations

For each selected template type:

- Output a **markdown template** that:
  - Uses clear headings and subheadings
  - Includes placeholder fields in square brackets (e.g., `[Product Name]`, `[Key Definition]`)
  - Marks GEO-critical sections using inline comments like:
    - `<!-- GEO: concise definition, 2–3 sentences -->`
    - `<!-- GEO: high-confidence facts AI can quote safely -->`
  - Is easy to copy into a doc, CMS, or another tool
- Keep the template reasonably compact but **complete enough** to avoid guesswork.

Example structure (for a definition article template):

```markdown
# [Primary Topic]: Clear, Entity-Focused Title
<!-- GEO: Include the main entity name exactly as you want AI to use it. -->

## Summary
- [1–3 bullet points summarizing what this topic is and why it matters]
<!-- GEO: Make these bullets fact-focused and quoteable. -->

## What is [Primary Topic]?
[1–3 concise paragraphs with a clear definition]
<!-- GEO: This is the core definition models will likely cite. -->

## Key Concepts and Components
- [Concept 1]: [Short explanation]
- [Concept 2]: [Short explanation]

## Examples
- Example 1: [Short, concrete example]
- Example 2: [Short, concrete example]

## How [Your Brand / Product] Relates
[Explain how your brand/product interacts with or supports this topic]

## FAQ
Q1: [Common question]
A1: [Clear, factual answer]

Q2: [Common question]
A2: [Clear, factual answer]
```

When generating templates, **do not pre-fill** brand-specific content unless the user provides it.
Instead, use neutral placeholders and short instructions.

### 4. Provide sample filled-in snippets (optional but helpful)

If the user wants extra guidance or explicitly asks for **examples**, provide:

- One or two **short, filled-in snippets** for key sections, such as:
  - Definition paragraph
  - One FAQ entry
  - One row of a comparison table

Make these:

- Concrete, but clearly labeled as **examples**, not generic boilerplate
- Safe to copy as inspiration, but easy to adapt

Output these under `## Example Filled Sections` and clearly indicate which template they belong to.

### 5. Usage notes and team guidelines

Close with a `## Implementation & Team Guidelines` section that gives:

- Tips for **keeping templates consistent** across teams:
  - Where to store them (docs, wiki, knowledge base)
  - How to version and update them
- Advice for **using templates with other GEO skills**:
  - "After filling this template, run it through `geo-citation-writer` for refinement"
  - "Use `geo-schema-gen` to mirror this structure in JSON-LD"
- Reminders about **AI-citable content**:
  - Prioritize factual, verifiable statements
  - Avoid over-claiming or vague marketing language in GEO-critical sections

---

## Output format

Unless the user requests a different format, structure responses as:

1. `## Scenario Summary`
2. `## Template Selection`
3. `## Templates`
4. `## Example Filled Sections` (if applicable)
5. `## Implementation & Team Guidelines`

Within `## Templates`, include one or more clearly labeled subheadings:

- `### [Template Type Name] Template`
- Under each, output a complete markdown template.

Use:

- Markdown headings
- Bullet lists
- Short comments explaining GEO-significant parts

If the user only asks for a **single template**, still keep this top-level structure, but it is fine
to keep the unused sections very short (e.g., “Not requested for this use case.”).

---

## Example triggering prompts (for reference)

These are **internal examples** to clarify when this skill should trigger:

- "Give me a reusable template for a GEO-optimized FAQ page about our B2B SaaS product."
- "I want a standard 'What is X?' article template that our content team can reuse across topics."
- "We keep writing comparison pages like 'Product A vs Product B'. Can you give us a robust template
  that AI models will love to cite?"
- "Design a set of templates for stats roundups and data summary posts that are easy for LLMs to
  reference."

You do **not** need to surface this list directly to the user; it simply refines intent.

---

