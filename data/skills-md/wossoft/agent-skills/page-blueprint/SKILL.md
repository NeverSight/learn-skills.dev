---
name: page-blueprint
description: Describe pages that do not exist yet as structured text blueprints agents can implement directly — a directory tree mirroring routes, per-page YAML layout trees whose nodes are real shadcn/ui (or other declared library) component names, navigation actions, and dialog/sheet/drawer behavior. Use for a new app, a new module or batch of pages in an existing app, or a major restructuring of page layout or flow, when the user wants a text prototype, low-fidelity wireframe, or "what goes where" description before building UI; also for greybox previews and for checking a fresh implementation against its blueprint. Not for incremental changes to pages that already exist in code, visual branding, pixel mockups, or design-tool files.
---

# Page Blueprint

Turn "this page has X on the left and Y on top" into a blueprint an agent can map one-to-one onto components. The blueprint is a requirements artifact kept in the repository, not a drawing.

## Scope: new pages only

A blueprint is the input for going from nothing to a first implementation. Once a page exists in code, the code is the source of truth.

- **Use a blueprint for:** a new app; a new module or batch of related pages inside an existing app; a major restructuring of existing pages' layout or flow (blueprint only the restructured part); or handing new pages to another person or agent.
- **Do not use a blueprint for:** changes to pages that already exist (add a column, a button, a dialog, a field). Read the existing code and implement the requested change directly. Do not create a blueprint for it, and do not update an old blueprint to record it.
- **Inside an existing app:** take shells, shared composites, and conventions from the current code rather than redefining them; blueprint only the new pages.
- **After implementation:** set the page's `status: implemented` and treat the blueprint as archived. Later work reads the code, not the blueprint. If a request would require keeping a blueprint in sync over time, point out that this conflicts with the scope above and let the user decide.

## Principles

- **Structure over pictures.** Layout is a YAML tree of regions and components; an optional ASCII sketch is only an aid for humans. When they disagree, the YAML wins.
- **Name real components.** Use the component names of the library declared in `app.md` (shadcn/ui by default), so nothing has to be guessed from a box. Read [references/components.md](references/components.md) for the vocabulary and cross-library mapping.
- **Say what matters, omit the rest.** Record hierarchy, content, behavior, data, states, and responsive changes. Do not specify colors, pixel sizes, fonts, or shadows; those come from the library's design tokens.
- **Patterns first.** State a pattern's parameters and only the differences. Admin pages (list, detail, form, settings, dashboard): [references/patterns.md](references/patterns.md). Public website pages (landing, article, hub, comparison): [references/site-patterns.md](references/site-patterns.md). Write a full layout tree only for pages that fit no pattern.
- **Copy stays in content.** For website pages, reference sections of the Markdown content source (for example from `seo-content-architect`) instead of repeating copy in the blueprint.
- **Stable ids.** Give every interactive or data-bearing node an id (`Button#create`). Ids connect the blueprint to flows, actions, code, and review findings.
- **Facts vs assumptions.** Mark guessed content, fields, or endpoints with `# assumed` and list them under `Open questions`. Ask only when a choice would materially change page structure.

## Files

```text
blueprint/              # or the location the user/project specifies
  app.md                # library, menu, conventions, shared composites
  _layout.md            # root shell; nested _layout.md files wrap their subtree
  orders/
    page.md             # /orders
    _overlays/          # overlays shared within this subtree (optional)
    [id]/page.md        # /orders/[id]
```

The directory tree is the route tree and the route path is the page id. Navigation between pages is a graph expressed by `navigate()` actions, not by the tree. Dialogs, sheets, and drawers are defined once with their inputs, outcomes, and what the opener does after each outcome; overlays that need their own URL become pages with a `presentation`. Small requests (one or two pages) may stay in a single `blueprint.md`. The full format is in [references/spec-format.md](references/spec-format.md); a worked example is in [references/example/](references/example/).

## Modes

Identify which mode the user wants; several can run in sequence.

### 1. Author

1. Inspect the project first when one exists. For a website with an SEO plan, read `sitemap.md` and the `content/` front matter: each planned page becomes a `page.md` at the same path, and its `page_type` selects the pattern. In a codebase, also inspect `components.json`, installed `components/ui/*`, routes, existing layouts, and API types. Reuse what exists instead of inventing parallel structures.
2. Write or update `app.md` (library, menu, conventions, shared composites) and the `_layout.md` shells.
3. Create one `page.md` per route: front matter, purpose, then either a `Pattern` (+ `Changes`) or a full `Layout`, followed by overlays, states, interactions, data, and open questions — each only where it differs from pattern defaults and app conventions.
4. Self-check before handing over:
   - every `navigate(...)` target has a matching `page.md`, and every `open(#...)` resolves to an overlay in the page or an ancestor `_overlays/`;
   - every overlay that changes data declares its outcomes and `onClose` handling;
   - every `Changes` operation targets an id that exists in the expanded pattern;
   - every node type is a library component, a layout primitive, or a declared `@Composite`;
   - every data-bearing component states its source and its loading / empty / error behavior;
   - ids are unique within the page.
5. When the user gives one or two pages as a sample, follow that sample's conventions for the remaining pages.
6. End with a review summary following [references/review-summary.md](references/review-summary.md): pages, generated flow, overlays, deviations, and numbered questions. The user reviews the summary, not the YAML; when they answer by number, apply the answers and clear the corresponding `# assumed` marks.

### 2. Preview (optional)

Only when the user asks. Render the blueprint, with patterns expanded, to a single self-contained greybox HTML following [references/greybox.md](references/greybox.md). When the user asks for a page inventory or flow diagram, generate it from the directory tree and the `navigate()` / `open()` actions instead of maintaining one by hand. Do not open browsers or run automation to check it unless the user authorizes that.

### 3. Implement

1. Treat the blueprint as the requirements source. Expand patterns using their documented defaults, then apply `Changes`. Map each node id to code; keep ids recognizable in component or handler names where natural.
2. Check which library components are installed. Add missing shadcn/ui components with the project's CLI (for example `npx shadcn@latest add <name>`) when dependency changes are allowed; otherwise report what is missing.
3. Never edit generated shadcn/ui primitives in `components/ui`. Put composition in feature or shared components; customize appearance only through CSS variables or design tokens. If a requirement seems to need patching a primitive, stop and ask.
4. Implement all declared states and responsive rules, not just the happy path.
5. If implementation must deviate (missing API, library limitation), report the deviation explicitly before finishing.
6. When the page is done, set `status: implemented`. From then on the code, not the blueprint, is the source for further changes.

### 4. Check

Use as acceptance right after implementing from a blueprint; do not use archived blueprints to judge pages that have since evolved. Compare the implementation to its blueprint node by node. Report missing or extra regions, wrong components, unhandled states, broken flow targets, and responsive gaps, citing node ids and files. A check does not authorize fixes.
