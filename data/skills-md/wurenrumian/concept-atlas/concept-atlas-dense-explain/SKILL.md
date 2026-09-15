---
name: concept-atlas-dense-explain
description: Build structured explanation webpages with the bundled React/Vite/MDX components. Use this skill whenever the user asks for a technical explanation, concept map, layered knowledge page, interactive explanation, component-based knowledge page, or webpage resembling the Concept Atlas exemplar. Before generating anything, ask whether the user wants (A) a scrollable long-form page assembled from semantic components or (B) the full Concept Atlas interactive framework with concept navigation and relation graph. Do not choose the output mode silently.
---

# Concept Atlas Dense Explain

This is an Agent Skills-compatible skill. Keep the instructions and generated content portable across Claude Code, Codex, Cursor, Gemini CLI, OpenCode, Cline, GitHub Copilot, and other agents that support `SKILL.md`.

Use the bundled components and, when selected, the complete template to turn knowledge into a structured explanation. The required deliverable is a built webpage, normally `dist/index.html`; it may be a scrollable component page or a full interactive Concept Atlas.

## Mandatory mode selection

Before writing content, determine the output mode. If the user has not already chosen one, ask exactly one concise clarification:

> 你希望生成哪种形式？A. 使用语义组件组装的滚动型讲解网页；B. 使用完整 Concept Atlas 框架的交互式网页（概念树、节点下钻、关系图）。如果没有偏好，我推荐 B。

Do not start implementation until the user chooses A or B. If the user explicitly requests both, create separate outputs only when the workspace and scope support them.

### Mode A — Scrollable component page

Use the existing React/Vite shell and compose the page from supported semantic and presentation components. A natural vertical reading layout is valid in this mode. It does not require a 15–25 node concept graph or relation graph unless the user asks for those features. Keep content semantic and avoid handwritten CSS, SVG, or replacement app code.

### Mode B — Interactive Concept Atlas

Use the complete bundled template. The page must contain one `L0` root, multiple `L1` branches, lower-level nodes where useful, `Children` / `ConceptRef` navigation, and labeled cross-branch `Relation`s. The template provides the three-column node explorer, graph view, search, filters, URL node state, keyboard navigation, and responsive behavior.

## Mandatory preflight and mode-specific fallback rule

Before generating content, resolve the directory containing this `SKILL.md` and verify that these bundled files are readable:

- `assets/template/content/compile-runtime.mdx`
- `assets/template/src/app/App.jsx`
- `assets/template/src/components/MDXComponents.jsx`
- `assets/template/src/model/normalize-content.js`
- `references/components.md`

Read the component contract before writing. For Mode B, also read the exemplar and verify the complete template. If the bundled template is unavailable, report that Mode B cannot be completed and offer Mode A only after the user agrees. Never silently downgrade Mode B to a long page or custom mockup.

For Mode B, the template is the implementation boundary: do not edit `src/`, styles, `index.html`, Vite configuration, or package dependencies for a content task; replace only the MDX content after copying the template. For Mode A, use the host project's existing shell and do not introduce a replacement application unless requested.

## Step 0 — Read the exemplar before writing Mode B content

For Mode B, read [assets/template/content/compile-runtime.mdx](assets/template/content/compile-runtime.mdx) in full first. It is the **reference standard**, not just a file to overwrite. Study its shape before generating anything:

- 1 `L0` root, ~5 `L1` branches, 2–3 children per branch, descending to `L3`/`L4` where the topic deserves it.
- Every `title` is a claim ("ABI 破坏：能链接，不等于能调用"), and every `summary` is a one-sentence judgment.
- Important nodes carry 3–6 semantic components, not one lone paragraph.
- Claims are backed by concrete commands, numbers, or named artifacts (`readelf -Ws`, `nm -C`, `objdump -dr`, `.bss`, ASLR).
- Cross-branch meaning is encoded as labeled `Relation`s, not prose.

## Workflow

1. Ask for and record Mode A or Mode B before implementation.
2. Read [references/components.md](references/components.md); for Mode B, resolve and copy the complete `assets/template` directory and read the exemplar first.
3. Mode A: create the requested scrollable content using semantic components and the existing shell. Mode B: replace only the template content MDX, preserving React, CSS, graph, and build files.
4. Mode B: model one `L0` root, then `L1` structure, `L2` mechanisms, and optional `L3/L4` boundaries or failures. Add `parent`/`Children` and labeled cross-branch `Relation`s.
5. In either mode, keep content semantic: do not encode layout, coordinates, CSS, or SVG in MDX. Use supported model and presentation components where they clarify structure.
6. Run the relevant validator, then `npm install` and `npm run build`. If validation or build fails, revise the content rather than returning an unverified substitute.
7. Mode B: verify node switching, graph mode, search, URL `#node=...`, keyboard navigation, and responsive layout. Return the built output path and state which mode was used.

## Delivery summary

After generation, briefly explain:

- which mode the user selected (`A` scrollable component page or `B` interactive Concept Atlas);
- what the skill contributed (semantic components, concept tree, relations, or template interactions);
- the output path and the main ways to inspect or continue editing it.

Keep this summary concise. Do not merely list files or claim interactive features that were not built.

## Content rules

- Start with a one- or two-sentence core judgment.
- Use tables/flows for comparison and causality; use short paragraphs only for explanation.
- Every dense block should contain a conclusion, evidence, or limitation.
- Prefer 2–4 columns on wide screens and natural stacking on narrow screens.
- Do not invent unsupported components or relation types. Read [references/components.md](references/components.md) for the supported semantic API.
- Mode B should aim for the exemplar's scale: roughly 1 root, 4–5 `L1` branches, ~15–25 nodes total. A thin graph is a failure in Mode B, but is not a requirement for Mode A.

## Self-check before finishing

Run this checklist and revise until every item passes. If an item fails, fix the content instead of adding decoration.

- [ ] The user selected Mode A or Mode B before implementation.
- [ ] Every key section or node has a claim, summary, or clear reading purpose.
- [ ] Mode B has one `L0`, multiple `L1`s, useful depth, concrete evidence, and labeled whitelisted relations.
- [ ] First screen shows the core claim plus 3–5 key facts; long detail lives in `Details` / `Tabs` when appropriate.
- [ ] No CSS, coordinates, SVG, or layout instructions appear in the MDX.
- [ ] Mode B changes only the template's MDX content; no replacement JSX or custom vertical article page was created.
- [ ] The relevant validator passes before the build.
- [ ] Mode B builds and node switching, graph mode, search, `#node=...`, and keyboard navigation all work.

## Portable template

The self-contained React/Vite/MDX implementation is in [assets/template](assets/template). It is required for Mode B and optional for Mode A when the host project already provides an equivalent shell. For Mode B, copy it into a project, replace `content/compile-runtime.mdx` **after studying it**, run `npm install`, then `npm run build`. The template has no dependency on the source repository's absolute paths.

For the component contract, relation whitelist, and level semantics, read [references/components.md](references/components.md). For the exemplar breakdown, density targets, and prompt wording, read [references/prompting.md](references/prompting.md).
