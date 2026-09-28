---
name: publish-site-artifact
description: Create or publish research documents, guides, plans, Marp decks, and demos for sites.tanmoysarkar.me. Use for this archive, not for unrelated sites.
---

# Publish a site artifact

This archive lives in `tanmoysrt/sites.tanmoysarkar.me` on `main`. See [llms.txt](https://sites.tanmoysarkar.me/llms.txt) for paths and the required GitHub CLI publishing commands. In a checkout, read the local `llms.txt`.

Use this skill for artifacts intended for this archive. For this site, use it instead of artifact-design.

## Shape the artifact

- Prefer a slideshow for learning material, especially when a long page would make the sequence hard to follow. Honor an explicit request for a page or another format. If the format is still unclear and the choice matters, ask: "Would you like an artifact or a slideshow?" Use answers already given; do not repeat questions. Ask about audience or depth only when needed to make the result useful.
- Keep the artifact focused on the requested topic. Include neighboring components only when they are needed to explain it.
- Choose `research/<slug>/index.html` for reports, `learning/<slug>/index.html` for guides, `plans/<slug>/index.html` for project plans, and `demos/<slug>/index.html` for small static sites or interactive examples. Use lowercase kebab-case slugs. Use relative paths for demo assets.
- For direct HTML pages, write readable, self-contained HTML with inline CSS and any local assets in the page's folder. Keep the site minimal and light. Do not copy an existing page's wording or design wholesale.
- When a tool generates the page, keep its editable source, configuration, and source assets in `raw/<section>/<slug>/`; put the built site in `<section>/<slug>/`. Record the build command in `raw/<section>/<slug>/README.md` unless a repository script already does so. Commit source and output together. Direct HTML pages need no duplicate raw copy.
- Check factual claims against sources when the topic needs it. Keep links to the sources visible on the artifact.

## Explain for the reader

Write every reader-facing explanation in Simplified Technical English (STE). Use short sentences, common words, active voice, and one idea per sentence. Define each necessary technical term at first use, then use the same term throughout. Keep technical names, values, and meaning accurate. Check the official ASD-STE100 Dictionary before you claim formal compliance.

For a complex topic, begin with brief context: what the subject does, what problem the reader must understand, and why the problem matters. Start with the simplest useful case. Add one idea at a time, and explain its effect before you add the next. Use a small, concrete example when it helps. Include only the detail the reader needs at that point. Review each page or slide for unexplained terms, abrupt jumps, and excess detail that could overwhelm the reader.

## Written reports, guides, and plans

Write like a clear engineering note. Start with the concrete situation and why the reader should care. Explain in causal order: the constraint, the idea or change, how it works, evidence, limits, and what happens next. Use only the sections the subject needs. Define a component's job before describing its internals, then trace one realistic request, action, or piece of data through the system.

Use short paragraphs, direct headings, and specific examples. Show the relevant lines of code or configuration, a real UI state, or a measured before/after result when that makes the idea easier to verify. Give numbers units and measurement conditions. Distinguish what exists, what was tested, what is proposed, and what remains uncertain; include meaningful tradeoffs and failed approaches. Edit repetitions and rough phrasing rather than imitating the source posts verbatim.

Use diagrams to answer one question at a time. Use Rough.js for custom diagrams with a hand-drawn look; D2 is an option for ordinary static diagrams. Draw simple labeled components and directional arrows; show ownership or network boundaries when they matter. Label the data or action on important arrows, and use before/after diagrams for a redesign. Place each diagram next to its explanation and give it useful alternative text. Use plain lines and little color. Treat private reference posts as style examples; do not copy their text, screenshots, or infrastructure details into public artifacts.

For a guide, give actionable steps and expected results. For research, compare options using evidence and state a conclusion. For a plan, show sequence, dependencies, and how success will be checked.

## Presentations

Use Marp for presentations and place each deck in `research`, `learning`, or `plans` based on its purpose. Keep editable Markdown at `raw/<section>/<slug>/slides.md` and local assets under `raw/<section>/<slug>/assets/`. Set `marp: true` and a meaningful `title` in the frontmatter. Check `marp --version` first. If Marp CLI is missing, ask the user to install it globally with `npm install -g @marp-team/marp-cli`. Build with `npm run build:deck -- <section> <slug>`; commit the raw source and `<section>/<slug>/` output together.

Keep decks easy to scan: a white canvas, dark sans text, thin lines, plenty of empty space, and only a little color to mark the current state. Use one idea per slide and short labels or fragments instead of paragraphs. Show actual code, tables, or product screens when they explain the point faster than prose. A slide should make sense at a glance and need little effort to read. Use a brief question or section title as an occasional pause.

Build explanations from the plain case, then add one relevant layer at a time. Show real examples and field layouts when they carry the idea: for network topics, this can mean packet headers, source and destination addresses in braces, and the fields that change, rather than only boxes and arrows. Label illustrative data when real data is unavailable. Highlight every changed value, label, or path in each step; do not let muted text change unnoticed.

Keep the title at the same top position on every content slide. Center question and section slides vertically, with or without a short subtitle. Use the same type scale and spacing within each slide type throughout a deck.

For concepts and flows, draw simple diagrams with Rough.js. Use plain boxes, arrows, handwritten-feeling lines, and direct labels. Keep them deliberately rough and useful, without glossy icons, gradients, shadows, or decorative illustrations. Give each actor or operation a consistent color; use a stronger accent only for the path or state under discussion. Put short annotations next to the relevant part of the diagram.

Choose the pace that makes the idea easiest to follow. Keep a slide static when it reads at a glance. For a process with several states, reuse the same diagram across a few slides and change or highlight one step at a time. Use a brief Marp transition only when it clarifies the sequence. Let the complete state remain visible when it helps the explanation. Avoid decorative motion and honor reduced-motion preferences.

Marp references: [CLI](https://github.com/marp-team/marp-cli) and [slide transitions](https://github.com/marp-team/marp-cli/blob/main/docs/bespoke-transitions/README.md).

## Publish

Before publication, review all new or changed source and generated files. Never publish PII; remove private names, contact details, addresses, IDs, and personal records from `raw/` and public output. Ask the user about unexplained high-entropy data, including token-like strings, encoded blobs, or binaries, and leave it out until confirmed safe. Do not rely on `.gitignore` to catch sensitive content.

Run `gh auth status` before publication. For a new direct HTML page, use the `gh api` PUT command in `llms.txt`; include the existing file SHA when updating. For a generated or multi-file artifact, use `gh repo clone tanmoysrt/sites.tanmoysarkar.me`, then commit and push the source and generated files. Do not use raw token-based HTTP publishing. Publish only when the user has asked for it. Confirm the public URL works before reporting success.
