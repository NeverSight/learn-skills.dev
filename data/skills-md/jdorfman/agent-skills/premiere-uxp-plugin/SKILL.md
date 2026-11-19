---
name: premiere-uxp-plugin
description: >-
  Scaffold, build, debug, and package Adobe UXP plugins (panels) for Premiere
  Pro, Photoshop, and other Creative Cloud apps. Use when the user wants to
  create or fix an Adobe plugin/panel/extension, mentions UXP, manifest.json,
  UDT / UXP Developer Tool, a .ccx package, the `premierepro` or `photoshop`
  scripting module, or is migrating from deprecated CEP/ExtendScript. Covers the
  panel scaffold, the manifest v5 schema, the lockedAccess+executeTransaction
  action pattern, DevTools logging, and packaging to .ccx.
---

# UXP plugin builder (Adobe Creative Cloud)

UXP = Adobe's current extensibility platform. It replaces CEP/ExtendScript,
which is deprecated. Premiere Pro 26 and current Photoshop/InDesign ship UXP.
Default to UXP for any new Adobe panel; only touch CEP for legacy maintenance.

A UXP plugin is: a `manifest.json` + an HTML panel + JS that calls the host
app's scripting module (`require("premierepro")`, `require("photoshop")`, …).

## When to use

- "Create an Adobe / Premiere / Photoshop plugin, panel, or extension"
- Anything mentioning UXP, `manifest.json`, UDT, `.ccx`, `premierepro` module
- Fixing a UXP error (esp. **"The script object is no longer valid"** — see below)
- Migrating a CEP/ExtendScript plugin to UXP

## Build workflow

1. **Scaffold** from `assets/` (copy manifest, index.html, main.js, icons/).
   Set a unique reverse-DNS `id`, the `host.app`, and a `host.minVersion` that
   matches the oldest API you call (see the "Since" note on each API in docs).
2. **Write panel logic** in `main.js`. Import the host module and follow the
   host-specific patterns — for Premiere see `references/premiere-uxp-api.md`.
3. **Load in UDT** (UXP Developer Tool, free from Creative Cloud → Marketplace →
   Manage): **Add Plugin** → pick `manifest.json` → **Load**. The panel appears
   under **Window → (UXP / Extensions)**.
4. **Iterate**: after editing JS/HTML, hit **Reload (⟳)** in UDT. No app restart,
   no reinstall for code changes. Manifest changes need a fresh Load.
5. **Package** for distribution: UDT plugin row → `•••` → **Package** → `.ccx`.
   Double-clicking the `.ccx` installs via Creative Cloud (no dev mode required).

## Debugging & logs (there is no log file)

UXP logs go to a **Chrome DevTools** window, not disk:

**UDT → plugin row → `•••` (Actions) → Debug** → **Console** tab.

`console.log` / `console.error` print there. Open it *before* reproducing a bug.
Add `console.error("[plugin]", e)` in every catch — surface the message in the
panel UI too, but the stack trace only shows in DevTools.

## The #1 UXP gotcha: "The script object is no longer valid"

Thrown by `create...Action()` calls (setColorLabel, moveItem, setValue, keyframe,
etc.). Root cause: **host actions must be *created* inside BOTH
`project.lockedAccess()` AND `project.executeTransaction()`, together.** Creating
an action anywhere else — or before entering the lock — invalidates it.

Both callbacks are **synchronous**. Do every `await` (getItems, getRootItem,
reads) *first*, outside the lock; then create + add actions inside:

```js
// async reads FIRST (outside any lock)
const project = await ppro.Project.getActiveProject();
const root = await project.getRootItem();
const targets = await collect(root);        // your async traversal

// then sync mutation: lockedAccess wraps executeTransaction
project.lockedAccess(() => {
  project.executeTransaction((compoundAction) => {
    for (const t of targets) {
      const action = t.item.createSetColorLabelAction(t.index); // created in-scope
      if (action) compoundAction.addAction(action);
    }
  }, "Undo label");   // 2nd arg = the undo-history string; whole block = 1 undo
});
```

Never `await` inside `lockedAccess` / `executeTransaction`. Never build actions
before the lock and stash them for later.

## Verifying API facts (don't guess signatures)

The UXP APIs are new and change. Confirm any method before relying on it:

- Reference: `developer.adobe.com/premiere-pro/uxp/` (and `/photoshop/uxp/`).
- Source of truth for signatures + version gating (the "Since: 25.x" line):
  `github.com/AdobeDocs/uxp-premiere-pro` under `src/pages/ppro-reference/classes/`.
  Fetch a class's `.md` with `gh api` to read exact params.
- Samples: `github.com/AdobeDocs/uxp-premiere-pro-samples`.

## Files

- `assets/` — copy-ready starter: `manifest.json`, `index.html`, `main.js`, `icons/`.
- `references/manifest.md` — manifest v5 field reference.
- `references/premiere-uxp-api.md` — verified Premiere project/item/action patterns.
