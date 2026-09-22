---
name: html-prototype-build
description: Build, annotate, review, screenshot, and deliver native HTML UI prototypes with AI agents using reusable UI packs, DOM-bound product annotations, in-browser Direct Edit, browser review pins, a local authoring server, an element-to-source Inspector, and multi-state screenshots. Use when the user mentions /html-prototype-build or asks to reconstruct UI in HTML, create product annotations, edit prototype styles, review or mark DOM elements, capture prototype states, or package prototype deliverables. Works with Claude Code, Codex, Cursor, and other Agent Skills clients; do not use for generic source-code navigation, ordinary documentation, or production frontend development.
---

# HTML Prototype Build

## Quick start

1. Confirm the prototype type and business facts from the user's materials; ask first when information is insufficient, do not guess.
2. When generating or heavily changing UI, run `node <skill-root>/scripts/resolve-pack.mjs --list`, then `node <skill-root>/scripts/resolve-pack.mjs --pack=<pack-id> --select=<preset, pattern, or component id>` and read only the minimal file closure it outputs.
3. Generate the complete `<prototype-name>/` delivery directory per [shared generation contract §7](references/generation-contract.md#7-delivery-files); route all business state through `PrototypeViewers`, and use the Runtime copy as-is for the formal Client Runtime.
4. When done, run `npm test` at the repository root; start the authoring server or scenario screenshots only when the task needs them.

## Route the task first

Read only the entry that matches the current task; do not read all references at once:

| User goal | Required entry | Main output or tool |
|---|---|---|
| Generate, rebuild, or heavily change UI | [UI generation](references/ui-generation.md) | HTML prototype and on-demand UI components |
| Install or download missing UI packs | [Pack install](references/pack-install.md) | `scripts/install-pack.mjs` |
| Understand Viewer, note cards, SVG connectors, or interaction lightning | [Product annotations](references/product-annotations.md) | snapshot + Client Runtime |
| Start the authoring environment, direct edit, edit notes, or jump to source | [Local authoring](references/local-authoring.md) | `runtime/server/index.mjs` + Author Tools |
| Add review pins to a page, export For AI | [Review mark](references/review-mark.md) | `runtime/author/tools/mark/` |
| Batch screenshots by page state | [Scenario screenshots](references/screenshots.md) | `runtime/cli/screenshot.mjs` |
| Prepare final files | [Delivery & iteration](references/delivery.md) | Final delivery files |
| Final check before delivery | [Delivery checklist](references/delivery-checklist.md) | Per-item checkboxes |

When generating or heavily changing UI, read the [shared generation contract](references/generation-contract.md) first; for other tasks read the matching entry above without reading the full contract.

For visual tasks, discover packs, pick a foundation and providers via the [UI pack catalog](ui/catalog.md), resolve the minimal closure, and follow the [consumer pack rules](ui/contract.md). When no pack is installed, follow [Pack install](references/pack-install.md).

`scripts/` holds the agent's deterministic tools. `runtime/` is split by execution boundary: `client/` formal browser runtime, `author/` browser authoring tools, `server/` local Node authoring service, `cli/` standalone command-line tools.

## Terminology

- **`ponytail:`** — in-place comment marking an intentional prototype shortcut or uncollected state; replace it after you have real screenshots, computed styles, or interaction evidence.
- **Project materials** — screenshots, requirements, and confirmed facts for the current task (not generic framework defaults).

## Core boundaries

- Every prototype must use the distributed copies of `runtime/client/core/display-mode.js`, `runtime/client/core/state.js`, `runtime/client/notes/model.js`, `runtime/client/notes/viewer.js` in order; `state.js` provides the single `PrototypeViewers` state source, `model.js` handles only note scenario metadata and pure `when` matching, and Notes Viewer handles only DOM/connector rendering. Do not fold these responsibilities back into the Viewer.
- Formal notes are written back to `prototype/notes.snapshot.js` only through `runtime/server/index.mjs` + Notes editor; do not inline a notes editor in `prototype.html` and do not store formal notes in localStorage.
- Mark is a temporary review tool in the Author Tools panel alongside Direct edit; its data goes to page-path-scoped localStorage, is never written to the snapshot, and is not injected into the source HTML.
- Direct edit previews in the authoring session only and writes back to the source HTML safely through the server.
- The authoring service only handles local editing and in-prototype source lookup; it never enters the source HTML or the final deliverable.
- Screenshots consume only the URL scene and formal annotation data; they do not generate business state.
- System names, menus, fields, states, and business data must come from the user's materials; ask when information is unclear, never guess.
