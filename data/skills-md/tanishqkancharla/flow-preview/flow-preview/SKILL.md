---
name: flow-preview
description: Generates interactive Maui user-flow canvases using a bundled CLI, with linked states and persistent review checkboxes. Use when previewing, comparing, or reviewing a user journey across multiple UI states.
---

# Flow preview

Generate a temporary, self-contained preview using this skill's `scripts/generate.mjs`. Keep this entire skill folder together when moving it. The CLI uses only Node built-ins and works from any project's root, without Halo packages or workspace configuration. The canvas is a development tool, not production application state.

## Derive the story from the real UI

- Read the production component, its consumers, and its state transitions. Map the user's entry point, actions, success, loading, validation, failure, retry, and permission branches that matter to the request. Do not invent screens to fill a grid.
- Adapt the actual production component through props and local fixture callbacks. If it combines server calls with rendering, propose a small presentational extraction; do not maintain a second lookalike UI.
- Render exactly what the product renders. Components often depend on styles outside their own files: the app's global stylesheet (including rules a component's class names reference there), its font faces and the root classes that apply them, font smoothing, and the attribute or class its theme tokens key off. Load those same files into the preview instead of approximating them, and compare a screenshot of each state against the running app in light and dark. When comparing two revisions, load each revision's own global styles, since a rule removed in one branch can still be what the other branch's component needs.
- To compare two revisions, check both out side by side (for example as two git worktrees), import each revision's real components into one preview, and give both the same fixtures and the same inputs. Label which column is which in the scenario's notes, not inside the product UI.
- Reach each state the way a person would. Thumbnails apply the end state instantly through the component's own handlers so they stay deterministic. The interactive preview should get there through the same controls a person uses: press the real buttons, type amounts one keystroke at a time, open real menus and pick their items, at a pace a reviewer can follow. That lets the product's own transitions (height changes, sliding switches, menus, validation messages) play exactly as they do in the app, rather than appearing already finished. Fall back to calling the handler only when the control is not reachable, and keep the product's reduced-motion behavior intact.
- Keep fixtures and simulated requests in the temporary preview, not production conditionals. Thumbnails mount every state simultaneously: rendering them must not send requests, start real work, or mutate production data. Use deterministic values, not timestamps or random content.
- Use the Maui skill, when available, for UI composition. Keep flow-specific copy and business data in the scenario/adapter, not the generic canvas.
- Render only the production UI inside the preview panel, without added surface labels, headers, instruction panels, simulation buttons, or disclaimer footers. Model external events such as provider approval, confirmation, and account loading as next journey steps with explicit incoming `action` labels, using the canvas's existing forward navigation. Do not duplicate these transitions with “Simulate…” or “Return to app preview” controls inside the UI. Keep actual application controls interactive through local fixture callbacks. Put context in the node's `note`.
- Write each node's description (`note`) as a short explanation of the runtime state and how the user reached it: what action or event just happened, what is saved or still pending, and what the user can do next when relevant. Do not substitute layout instructions, implementation tasks, or fixture-control instructions for that explanation. Briefly mark proposed behavior as proposed rather than implying it exists today.
- Wrap each map node's title, review checkbox, and thumbnail in one padded surface with a subtle shadow. Give the selected node a solid subtle accent background (`colors.accent[3]`, not an alpha fill) and accent border; keep that selection visible on hover. Preserve the production component's own surfaces. The selected interactive preview gets a full-width gallery-style dotted panel, with the UI centered inside it at its own width cap. Use plain state titles without number prefixes; the graph and outline already communicate order.

## Generate and serve

From the target project's root, run the script at its installed skill location. The Skills CLI normally installs it at `.agents/skills/flow-preview`; adjust the path if your agent uses a different directory:

```sh
node .agents/skills/flow-preview/scripts/generate.mjs preferences-flow 4180
npm --prefix tmp/preferences-flow install --workspaces=false
```

Arguments are `<lowercase-name> [port]`; the default port is 4180. Names cannot contain paths. Existing previews are never overwritten. The script creates `tmp/<name>/` relative to the current directory, not relative to the skill. It copies the canvas and Vite helper alongside `scenario.tsx`, `main.tsx`, `index.html`, `vite.config.mjs`, and a private `package.json`. Generated previews do not import from this skill or from Halo; the skill can move without breaking them.

Edit **`tmp/<name>/scenario.tsx`**. Install dependencies in that preview only; do not add it to the project's workspace. When importing real application components, align React and Maui versions with that project and retain the Vite helper's deduplication. If the project pins a different major of a deduplicated package (for example `motion`), pass `previewConfig` a `dedupe` list without it so the project's components keep their own copy. In `vite.config.mjs`, pass only the required source directories as `sourceRoots` to `previewConfig` (paths are relative to the preview directory, for example `sourceRoots: ["../../packages/web/src"]`). The default allowlist covers the preview directory only; never allow the project root or runtime workspace. Credential files, `.git`, `.halo`, and `.amp` remain denied even inside an allowed source directory. Verify these boundaries through HTTP before sharing a portal.

In an Amp orb, follow the exact supervised command printed by the script:

```sh
amp orb service start flow-preferences-flow --command 'npm --prefix tmp/preferences-flow run dev' --port 4180 --portal
```

Share the returned portal URL; do not share localhost or direct orb host URLs. Outside an orb, use `npm --prefix tmp/preferences-flow run dev`. Stop the service before removing its preview directory. Never start preview servers with `nohup` or a shell background process in an orb.

## Describe states

`FlowScenario` and `FlowNode` are exported from the generated `./FlowCanvas.tsx`:

- Scenario: stable `id`, `title`, `initialState`, and `nodes`; optional `description`, `navigationLabel`, and `dimensions`.
- Optional `persistentPreview({ selected, revision })` replaces the per-state preview with one UI that stays mounted while the reviewer moves between states. Use it when the transitions between states are part of what is being reviewed: drive that single instance from its current state to `selected` through the same handlers and controls a person would use, so the product's own animations play instead of a remount. Run only the steps that differ, track what has been applied after each finished step so a selection made mid-transition continues from where the UI actually is, and cancel the previous run when `selected` or `revision` changes. `revision` increases on every selection, including reselecting the current state, so the same `selected` with a new `revision` is a replay. Thumbnails still use `render({ mode: "thumbnail" })` and stay deterministic end states. The title, note and navigation still crossfade; only the panel stays mounted.
- Each node: unique stable `id`, `title`, `action` (incoming user action), optional `parent`, nonnegative `row`, and `render({ mode })`. Keep parents before children; roots omit `parent`. The initial state must exist. Use a separate occurrence ID when a journey revisits a state rather than creating a cycle.
- Columns follow parent depth and pack vertically without empty slots. `row` orders states within their own column; it does not reserve a global lane. Arrows still connect the actual parent and child, even when their vertical positions differ.
- `render` returns the real component adapter. `mode` is `thumbnail` or `preview`; use distinct DOM IDs for each. Keep the visible content equivalent. Optional `note` appears only in the interactive preview, never beneath thumbnail titles.
- `dimensions`: `previewWidth` is the default unscaled component width; `nodeWidth` is the thumbnail width and `nodeHeight` its maximum height. Each node can set `maxWidth` and `maxHeight` in unscaled pixels. Use the production component's existing width cap so its content fills the thumbnail instead of shrinking inside unused space. The interactive UI fills available width up to that cap, grows with its content, and scrolls at the smaller of its height cap (by default the unscaled thumbnail height) and the available pane height. Keep the title and navigation outside that scroll area. Shorter previews shrink to their rendered height, including their hit targets and arrow anchors. Title rows use their natural height, not a fixed-height heading slot. `columnGap`/`rowGap` separate branches. Set the maximum height large enough that relevant content is visible.

The canvas supplies the hierarchical outline, title/checkbox above each thumbnail, pan by scrolling, zoom, animated selection/crossfade, stateful journey breadcrumbs, and animated sidebar toggle. Above the preview, show the journey's titles as quiet buttons separated by chevrons, wrapping at narrow widths. Each title selects that state; clicking the current title restores its initial fixture without changing reviews. Keep later breadcrumbs when selecting an earlier state through breadcrumbs, the map, the outline, or Previous state, so the reviewer can move forward again. Mark only the selected state with `aria-current="step"`. Selecting outside the retained journey replaces it with the new state's declared parent chain; selecting a descendant extends it. Use that parent chain, not click history, so direct selection still shows how to reach the state. Keep the journey in canvas state for the current page session; individual interactive drafts still reset on selection. Do not add a separate Reset preview button. Keep preview chrome to the breadcrumbs, state title, review checkbox, and navigation actions; do not repeat “Interactive preview” or “Follow this flow” headings. Both sidebars use Maui's raised element surface. Each map node has a raised surface, subtle shadow, and even 12px padding around its title, checkbox, and thumbnail. A single native CSS `:hover` on the whole node supplies an instant Maui hover background, without transitions, geometry changes, or title-color changes. The selected node retains its solid subtle accent background and accent border, including on hover; use a shadow ring for the border so selection does not shift geometry. The header, checkbox, thumbnail, and their gaps stay inside that continuous hover area. Keep the selection button transparent on native `:hover`, not only React Aria's delayed `data-hovered`, to prevent a first-frame fill flashing over the UI. Selection makes the title semibold with `colors.accent[12]`; unselected titles keep their neutral high-contrast color. Clicking the title or thumbnail selects the state; the checkbox only changes its review. Hovering does not select or reset a state. Outgoing scenes and thumbnail contents are inert; use the interactive preview to exercise their controls. Reduced motion removes travel while retaining the crossfade.

Center the selected UI in a panel matching Maui gallery's `Panel` recipe: gray-1 surface, gray-alpha-3 dots at 12px intervals, outline border, and extra-large radius. Use the same dotted background recipe for the map canvas. The panel fills the available sidebar width; cap only the UI inside it at the node's maximum width. Use an even, compact inset on all four sides and no minimum panel height. The padded panel owns scrolling, not a tight wrapper around the UI: preserve the production component's shadow instead of clipping it into corner marks. Give thumbnails a small overflow clip margin for shadows while still bounding tall content. Preserve padding owned by the production UI. This is gallery styling, not a `Panel` package import. Keep Previous state and forward actions outside that panel with the same default button styling. Do not add a disclaimer footer. Both sidebar boundaries support dragging and keyboard resizing; widths persist per scenario in browser localStorage. The outline selection background wraps the whole row, including its review checkbox; clicking that checkbox still only changes the review. Clamp sidebars to leave space for the map, and hide resize handles in the stacked narrow layout without replacing the saved desktop widths.

Align Previous state to the left and group all next-step actions on the right. Allow the next-step group to wrap while retaining its right alignment.

Keep the visible space around the selected UI even: when the panel is wider than the UI's width cap, increase its top and bottom inset to match the side gaps. Keep at least the compact gallery inset at narrower widths and include the inset in the panel's height limit.

In the stacked narrow layout, keep each scene's natural content height and let the preview sidebar scroll. Breadcrumbs and long notes must not squeeze the UI panel down to its padding.

Use default-size quiet buttons for breadcrumb titles, with the selected title in the theme's accent color. Keep unselected titles neutral.

## Review and verify

Review checkboxes in the outline, canvas, and interactive preview share one per-state value. A check dims only its thumbnail and overlays a green circle with a checkmark. The mark stays fully visible and does not block selecting the state. Browser localStorage stores a fingerprint per scenario/state; reset, theme changes, and reloads preserve it. Changed rendered content or style classes invalidate only the affected state. Fingerprints ignore generated IDs, theme values, and transient animation transforms/opacity. They describe the deterministic thumbnail, not an edited interactive draft. Keep scenario/state IDs stable; a new ID is a new review. Reviews are local to that browser and origin, not shared reviewer storage.

For a new scenario, drive all relevant states and real interactions in its portal. Use the using-agent-browser skill before browser work when available. Check light, dark, narrow layout, keyboard navigation, breadcrumb ancestry, backward/forward navigation without losing later steps, branch replacement, reselection, review synchronization/persistence, and reduced motion. Inspect screenshots, not only DOM assertions. In an Amp orb, save reviewable final screenshots/recordings under `.amp/in/artifacts/`. Otherwise, use the project's artifact directory. Keep scratch captures in the preview's `tmp/` folder. Do not treat a fixture preview as proof that the real backend operation succeeds.

## Maintain the skill

The bundled `assets/FlowCanvas.tsx` and `assets/previewConfig.mjs` are the sources copied by the CLI. After editing those files or the generator, run from this skill's directory:

```sh
npm install --workspaces=false
npm run typecheck
npm run lint
npm run format:check
npm run test:e2e
```

The browser tests copy the skill to a separate consumer project, generate a notification-preferences flow, remove that skill copy, and exercise the resulting preview. Install Playwright Chromium with `npx playwright install chromium` if needed, or set `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` to an installed browser. This skill has no dependency on repository lint or TypeScript configuration. Changes to the skill do not silently update existing generated previews; create a new preview or deliberately refresh its copied canvas/helper while preserving scenario IDs and fixtures.
