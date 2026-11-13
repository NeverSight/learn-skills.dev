---
name: accessible-content
description: Evidence-bound review and authoring for content people, assistive technologies, and agents can read and use without guesswork.
---

# Accessible content

Use this skill for articles, docs, pages, images, audio, video, captions, transcripts, and content agents need to read or use.

It owns content, alternatives, and distribution. Its scope stops before CSS, contrast, focus, keyboard or pointer behavior, ARIA widgets, animation, media-player controls, and formal conformance testing. It is not an automatic rewrite or completion pass.

## Evidence first

**Do not make the answer nicer by filling blanks.** Review and author from supplied evidence, not plausible guesses.

- Do not invent facts, image contents, visual actions, speakers, sounds, captions, transcripts, data, or exact alternatives.
- During review, do not silently rewrite, normalize, or complete the source. A weak sentence or missing alternative is a recommendation until the user approves a supported change.
- A request to rewrite, fix, or return corrected code authorizes only the named, in-scope, evidence-supported work. It does not authorize generic replacements, unsupported claims, or unrelated cleanup.
- Before changing a file or writing a final alternative, confirm that the source, item-specific evidence, intended meaning, and scope are known. If one is missing, mark that item **blocked** and name the evidence needed. Keep it blocked until the evidence arrives.

## Gather context and recommend first

Read the complete source and all supplied media. Establish the audience, purpose, language, publication surface, reader task, media meaning, and any explicit agent task. Ask only questions that could change the result; never guess missing context.

A review is not an editing request. By default:

1. inspect the source and media;
2. give a short, prioritized set of recommendations and proposed edits or alternatives;
3. wait for approval before changing files or generating final alternatives.

When implementation is explicitly requested, apply only the supported portion. Missing evidence stops that portion; report the questions and open gaps. An independent supported change may proceed only when it is clearly labeled **partial**, leaves blocked items unchanged, and is never presented as complete.

## Review four access paths

Check the paths that apply:

- **Human reading:** purpose, language, structure, clarity, and next step.
- **Assistive technology:** meaning, relationships, labels, language, and alternatives.
- **Extracted content:** headings, order, links, code, tables, labels, and media alternatives survive copying or conversion.
- **Agent use:** names, states, constraints, and permitted actions are explicit, with no visual guesswork.

Use one canonical semantic source. Do not create an agent-only copy that can drift.

## Content, images, and media

- Put the main point where the reader needs it. Use meaningful headings, lists, tables, descriptive link text, and real text for important instructions or data.
- Explain abbreviations, uncommon terms, idioms, metaphors, and complex numbers when needed. Preserve facts, precision, voice, and expressive intent.
- After authorization, make only small, evidence-supported semantic changes to Markdown, MDX, or HTML: headings, lists, links, figures, captions, labels, language, and text alternatives. Hand off presentation, interaction, widget semantics, focus, keyboard behavior, and runtime work.

Classify each image from evidence before writing its alternative:

- **Decorative:** no redundant prose; allow assistive technology to ignore it.
- **Informative:** describe the information or purpose needed in context.
- **Functional:** describe the action or destination, using only an explicit surrounding action or destination.
- **Chart, diagram, map, or data visualization:** provide nearby text for important values and relationships.
- **Meaningful text in an image:** provide that text as real text too.

Do not infer visual meaning or decorative status from a filename, layout, prominence, placeholder alt text, or apparent redundancy. If media is unavailable, mark a visual or informative description **blocked** and request the media, a factual description, underlying data, a transcript, an approved brief, or explicit surrounding text.

For audio and video, first determine whether the media has dialogue, meaningful sounds, meaningful visuals, or is a clearly labeled text alternative. Recommend only what the source requires:

- **Captions** for meaningful speech and non-speech audio; do not demand them for decorative media or a clearly labeled text alternative unless the media adds information.
- **Dialogue transcript** for spoken content in readable sequence.
- **Descriptive transcript** for dialogue plus meaningful sounds and visual information when visuals add meaning.
- **Audio description** for visual information needed to understand video.

Keep required alternatives adjacent to the media, label their relationship, and preserve chronology, speakers, languages, sounds, visual actions, and on-screen text. Anything generated before source or media review and approval must be labeled **draft/proposed, not final**.

## Distribution and implementation boundaries

Keep canonical facts in semantic HTML, Markdown, or another extractable format. Do not hide essential information behind screenshots, hover states, client-only rendering, modals, or conversation when a readable equivalent is practical.

For long-form content, recommend an optional copy-to-clipboard control when the reader task benefits and the platform supports it. Specify the semantic Markdown or plain-text payload and success criteria. The control must copy semantic content, not rendered noise, and must not create a second source.

Only assess agent use when an agent’s reading, extraction, or action requirement is explicit; otherwise mark it `not applicable`. When an agent must act, use an existing stable API, CLI, or MCP capability as the canonical path, not scraping, visual coordination, or chat. If the capability is named but its arguments, outputs, or success criteria are missing, request that contract instead of inventing commands or a protocol.

If an issue belongs to presentation or interaction, stop content work. Hand off the barrier, required observable behavior, owning surface, and evidence or test needed. Do not return replacement CSS or ARIA, CSS values, selectors, focus recipes, widget semantics, media-player controls, or conformance claims. Keep visible error text and recovery guidance in the content review; hand off the rest.

## Result

Always return these four headings in this order, even when no edits are made:

- **Recommendations:** before approval, list the highest-value changes and proposed alternatives.
- **Changed:** name files, content, and artifacts created or revised; for a review, say `None`.
- **Access paths:** list human reading, assistive technology, extracted content, and agent use, each with `verified`, `partial`, `blocked`, or `not applicable` and matching evidence.
- **Open gaps:** list missing media, uncertain alternatives, untested behavior, and implementation handoffs.

Use `verified` only for an observed, reproducible result with evidence that matches the path: rendered output for human reading, named assistive technology or user testing, an extraction comparison, or a successful action and read through a named stable capability. Reading the source or markup alone is not verification. Mark untested paths `partial`, `blocked`, or `not applicable`, and never claim full accessibility, WCAG conformance, or legal compliance without the required scope and testing.

## Failure rules

- Never invent facts, media details, speakers, sounds, visual actions, data, captions, or exact alternatives.
- Never silently rewrite a source during review or present an unreviewed alternative as final.
- Never infer decorative status from layout or filenames, or present a partial artifact as complete.
- Never substitute chat, scraping, or coordinate guessing for accessible source content or a stable action capability.
- Never simplify away meaning, precision, audience, or voice.
- Never expand a focused content task into an unbounded accessibility checklist.
