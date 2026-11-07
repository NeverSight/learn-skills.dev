---
name: html-artifacts
description: Use when the user asks to create, generate, visualize, or turn material into a standalone HTML artifact, self-contained or single-file .html report, interactive explainer, interactive illustration or visualization, visual walkthrough or handoff, or HTML presentation or slide deck. Handles source-grounded codebase and architecture, feature, PR or diff, implementation recap, incident timeline, option comparison, causal, and data-report explanations. Not for prose-only analysis or reviews, production web apps or dashboards, websites, HTML email, or ordinary frontend/UI implementation.
---

# HTML Artifacts

Generate a visual document that earns its use of HTML: the result should be easier to look at, compare, or manipulate than prose alone. Default to a self-contained local `.html` document, not a website, dashboard, or slide deck.

## Non-Negotiables

- **Ground first.** Read the source material and trace the relevant behavior before designing the artifact.
- **Default to document mode.** The artifact must stand on its own for an asynchronous reader. Use presentation mode only when explicitly requested or clearly intended for a live talk.
- **Keep the static story complete.** Interaction may deepen the explanation; it must not be required to discover the main conclusion.
- **Make interaction answer a question.** Every control must satisfy: reader question → action → immediate visible answer. Remove controls that do not.
- **Produce one true offline file by default.** Inline CSS, JavaScript, SVG, data, and essential assets. Do not rely on CDNs, remote fonts, `fetch`, or a server.
- **Keep it local unless asked.** Artifacts may expose source code, architecture, or review findings. Do not publish, upload, or create a public URL without explicit permission.
- **Validate the final file in a browser.** Do not call an artifact finished from source inspection alone.

## Choose the Mode

| Mode | Use for | Shape |
|------|---------|-------|
| **Document** (default) | Codebase, feature, PR, plan, incident, or research explanation | Scrollable, skimmable, complete prose, stable anchors, citations, print-friendly |
| **Explorable document** | Causal mechanisms, parameter tradeoffs, before/after states, coupled representations | Complete default state plus a few local controls with immediate feedback |
| **Presentation** | A live walkthrough where a speaker supplies context | One idea per view, keyboard navigation, explicit progress, speaker notes or captions |

If HTML adds no useful spatial comparison, diagram, or interaction, say so. If the user explicitly requested HTML, honor the request and make a restrained document rather than inventing spectacle.

## Workflow

### 1. Frame the explanation

Establish these from context; ask only when a consequential ambiguity remains:

- **Reader:** Who will use this, and what do they already know?
- **Governing question:** What should they understand, verify, compare, or decide?
- **Scope:** Which repository, revision, diff, feature, time range, or dataset is authoritative?
- **Mode:** Document, explorable document, or presentation?
- **Retention:** Temporary local file or a named project deliverable?

For a temporary artifact, use a unique file in the system temp directory. Do not add generated reports to the repository unless the user asks to retain them.

### 2. Build an evidence ledger

Before writing HTML:

1. Inspect the exact source identity and revision.
2. Read relevant files in full enough to understand their role.
3. Trace representative entry points, state changes, side effects, and failure paths.
4. Collect a stable locator appropriate to each source: path/line, revision, query, dataset row/field, URL, or provided input.
5. Separate **observed**, **inferred**, and **proposed** material.
6. Record important unknowns instead of smoothing them over.

For PR or diff artifacts, inspect every changed file plus the relevant surrounding paths needed to verify behavior, contracts, tests, and risk. Stop when additional exploration no longer changes one of those judgments.

Load only the matching subject section(s) and **Diagram Rules** from [content patterns](references/content-patterns.md) before outlining.

### 3. Outline the reading path

Write the artifact's argument before choosing its chrome:

1. Lead with the answer, change, or governing question.
2. Give the minimum context needed to interpret it.
3. Show the primary spatial model: flow, topology, state, comparison, timeline, or data relationship.
4. Walk through one concrete example.
5. Surface risks, limits, unknowns, or decision points.
6. End with a source index and the next useful action.

Choose representation by the reader's verb:

| Reader needs to… | Prefer |
|------------------|--------|
| understand where things are | containment or topology diagram |
| follow what happens | sequence or data-flow diagram |
| see what changed | aligned before/after or annotated diff |
| understand possible states | state diagram or transition table |
| compare options | semantic table or aligned small multiples |
| inspect values or trends | chart with direct labels and annotations |
| understand causality | a controlled parameter paired with immediate output |
| find evidence | searchable source/file map |

Use one overview plus focused detail instead of one giant diagram. A diagram should answer one question for one audience.

### 4. Design against the subject

Use the source project's visual language when one exists. Otherwise choose a quiet editorial direction based on the subject matter, not a generic product aesthetic. Choose one dominant explanatory composition—such as an annotated map, aligned comparison, mechanism stage, or timeline—and make the rest of the page support it.

Do not generate “presentation slop”:

- no giant gradient hero for a technical explanation
- no glassmorphism, glowing orbs, decorative grids, or fake browser chrome
- no card grid when headings, prose, or a table express the hierarchy better
- no fake KPIs, badges, severity labels, or status colors without source evidence
- no repeated oversized section titles and empty viewport-height panels in document mode
- no autoplay entrances, pulsing nodes, parallax, or animation that does not encode change
- no architecture inferred from directory names alone
- no unlabeled arrows, unexplained colors, or diagrams mixing abstraction levels

Use whitespace to separate ideas, not to make the artifact look expensive. Use cards only for genuine peers with repeated structure or independent actions.

### 5. Implement the smallest suitable artifact

Prefer plain semantic HTML, CSS, inline SVG, and a small amount of vanilla JavaScript. Use a framework only when state complexity justifies it; bundle the final result back into one offline HTML file.

Load [component contracts](references/component-contracts.md). Add `<style id="html-artifacts-components"></style>` to the document, then run `python scripts/inline-components.py /absolute/path/to/artifact.html` to inline `assets/artifact-components.css`. When the artifact needs a provided page grid, figure shell, control, stepper, outcome panel, or scroll region, use the canonical markup and classes instead of recreating it. Steppers must use the contract's inline SVG line and marker; never substitute a CSS pseudo-element, border, clip path, or arrow character. Override subject tokens; do not fork connector geometry, responsive state layouts, or interaction mechanics. Build custom visuals only when no provided component fits the governing question.

Required implementation qualities:

- semantic landmarks and ordered headings
- native buttons, links, tables, and `<details>` where appropriate
- visible keyboard focus and no hover-only information
- responsive reflow at 320 CSS px; intentional overflow only for irreducible diagrams/tables
- no color-only meaning; label states and relationships directly
- accessible text equivalent for complex diagrams
- `prefers-reduced-motion` support whenever motion exists
- print styles that remove controls, expand disclosures, and preserve the canonical explanation
- escaped untrusted/code text; safely serialized embedded data
- no secrets, tokens, private environment values, or unrelated source content

Load [quality and validation](references/quality-and-validation.md) while implementing.

### 6. Validate the bundled result

Use available browser automation; if a browser-testing skill is installed, load it. Test the actual final `.html` file, not only an authoring source or development server.

At minimum:

1. Open the artifact and wait for it to settle.
2. Check console errors, page errors, failed requests, and unexpected network access.
3. Capture and inspect desktop and 320–390 px mobile screenshots.
4. Run the **Visual Polish Gate** in [quality and validation](references/quality-and-validation.md) on the full page and a 1:1 crop of the dominant composition.
5. Exercise every control with pointer and keyboard, if controls exist.
6. Verify focus visibility, heading order, text alternatives, contrast, and non-color cues.
7. Check reduced-motion behavior if motion exists.
8. Check print preview or print CSS for document mode when the environment supports it.
9. Verify citations, source identity, numbers, and visible unknowns against the evidence ledger.
10. Fix issues and repeat the checks on the final file.

If browser automation is unavailable, perform the checks you can and explicitly report that visual and interaction QA remain unverified.

### 7. Deliver

After validation, open the final artifact with:

```bash
xdg-open /absolute/path/to/artifact.html
```

Run `xdg-open` as the last artifact action so the user sees the same file that passed validation. If `xdg-open` is unavailable or fails, report that instead of claiming the artifact was opened. Do not substitute publishing or uploading.

Then report:

- the exact file path
- its mode and governing question in one sentence
- what was validated
- any known omissions or unverified behavior

Do not paste the full HTML into chat unless asked.

## References

- [Content patterns](references/content-patterns.md) — load for codebase, feature, PR/diff, incident, data, causal, and presentation artifacts.
- [Component contracts](references/component-contracts.md) — load before implementation; use the canonical component markup with `assets/artifact-components.css`.
- [Quality and validation](references/quality-and-validation.md) — load while implementing and testing the HTML.
- [Research basis](references/research-basis.md) — read when maintaining or revising this skill's guidance.
