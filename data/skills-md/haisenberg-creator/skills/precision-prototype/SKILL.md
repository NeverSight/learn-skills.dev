---
name: precision-prototype
description: Build a single, highly-detailed prototype workbench with custom viewports, live in-canvas sync, and bake-to-code persistence after relentlessly interviewing the user.
---

# Precision Prototype

A precision prototype is **throwaway or dev-only code that answers a specific UI, layout, and interactivity design question**. Unlike general prototypes that produce multiple rapid variations, a precision prototype focuses on **exactly one UI design** built to precise user specifications gathered through an upfront grilling session.

It provides a dedicated workbench that embeds the real production component, isolates the viewport across devices and kiosk displays, syncs adjustments live in memory, and bakes validated parameters directly down to source code files with a single click.

## 1. Interview the user relentlessly (Grilling)

Before writing any code, walk through an intense, one-by-one grilling session using the `grilling` loop. Ask questions **one at a time**, waiting for feedback on each before moving to the next.

For each question, provide your recommended answer.

Walk down the decision tree resolving dependencies one-by-one:

1. **Purpose:** What exact question or hypothesis is this prototype testing?
2. **Target UI Scope:** Which specific page, section, component, or part of the page are we creating a prototype for?
3. **Target Elements:** Which specific elements need the ability to adjust scale, position, alignment, or layout dynamically?
4. **Control Mechanisms:** What exact control functions or UI mechanisms should adjust those properties (such as range sliders, +/- step buttons, numeric inputs, or toggle buttons)?
5. **Target Viewports & Displays:** Which specific device resolutions, aspect ratios, or kiosk displays must be simulated (such as mobile, tablet, desktop, 1080x1920 portrait kiosk TV, or 4K landscape)?
6. **Code Mapping & Bake Targets:** Which production files, CSS custom properties, tokens, or component props should receive the baked parameters when syncing down to code?
7. **State & Constraints:** What constraints, boundaries, or live state readouts must be visible on the screen while tweaking parameters?

Do not start coding until the user explicitly confirms that a shared understanding has been reached.

## 2. Build the precision prototype workbench

Once aligned, create a single, clean prototype workbench tailored to the exact specifications. The workbench must satisfy three core structural criteria:

### A. Isolated iframe canvas with scale-to-fit zoom

- Render the target UI inside an isolated `<iframe>` element so that CSS media queries (`@media screen`) evaluate strictly against the simulated viewport resolution, rather than the developer's browser window.
- Provide viewport presets out of the box:
  - Mobile (such as 390x844)
  - Tablet (such as 768x1024)
  - Desktop (such as 1440x900, 1920x1080)
  - Kiosk TV Landscape 16:9 (1920x1080, 3840x2160 4K)
  - Kiosk TV Portrait 9:16 (1080x1920)
- Support custom numeric Width and Height inputs, aspect ratio locking, and an orientation toggle (Landscape and Portrait).
- Include transform scaling (`transform: scale(...)`) with a "Fit to Screen" auto-zoom mode and preset zoom factors (100%, 75%, 50%, 25%) so massive displays (like a 4K kiosk TV) fit comfortably on a laptop screen without clipping or overflow.

### B. Anti-clumping workbench layout

- The target viewport sits centered in an outer letterboxed canvas workspace with neutral padding.
- All controls (viewport selectors, zoom controls, parameter sliders, readouts, and bake buttons) must live in a dedicated external workbench sidebar strictly outside the canvas.
- The controls must never overlap or cover the preview area, remaining fully usable when browser DevTools (F12) are opened.
- Include a collapse/expand toggle to hide the sidebar when inspecting, and an undock or pop-out button (`window.open`) so the control panel can run in a separate floating window when screen space is tight.

### C. Live direct-in-canvas sync

- The prototype workbench wraps the real production component or route directly.
- Adjusting sliders, inputs, or toggles mutates live CSS custom properties, design tokens, or reactive props in memory instantaneously, reflecting changes live in the viewport without page reloads or layout thrashing.

## 3. Bake validated parameters down to code

The workbench provides a one-click **"Bake to Code"** button that synchronizes tuned parameters directly to the codebase:

1. **Dev-native write endpoint:** Implement a temporary dev API route (such as `/api/__precision_bake` in Next.js, SvelteKit, Astro, or Remix, or a Vite dev server middleware). If the project has no server runtime, generate a tiny standalone helper script (such as `node scripts/prototype-bake.mjs` or Python/Bun equivalent).
2. **Direct file update:** When "Bake to Code" is clicked, the endpoint parses the target production source files or stylesheets mapped during the interview and replaces default or placeholder values with the exact validated parameters.
3. **Visual feedback & undo:** Display an immediate summary toast listing the modified files and updated values, alongside an "Undo" button to revert to the initial pre-bake state.
4. **Verify alignment:** Ensure production code compiles cleanly and matches the prototype values.

## Rules

1. **Dev-only retention.** Guard the prototype route, workbench UI, and bake endpoint with development-only checks (such as `process.env.NODE_ENV === 'development'`). Keep the workbench accessible during development so values can be revisited and retuned anytime, while ensuring nothing leaks into production builds.
2. **One command to run.** Whatever the project's existing task runner supports (such as `pnpm dev`, `npm run dev`, `bun dev`, or `python <path>`), the user must be able to start the workbench without manual setup.
3. **No clumping on F12.** Controls must reside strictly outside the viewport canvas. Opening DevTools or resizing the window must scale or pan the canvas, never squish controls over previewed elements.
4. **Skip the polish.** Focus on high-fidelity interactivity for the target controls and accurate viewport emulation. No automated tests or production error handling for the prototype workbench itself.
5. **Surface the state.** Display live parameter readouts alongside sliders so exact numbers are visible and inspectable at all times.
6. **Capture when done.** Commit the baked production code to the feature branch. Keep prototype workbench files organized under dev-only namespaces or folders.
