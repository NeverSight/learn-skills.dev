---
name: grapesjs
description: GrapesJS web builder framework. Use when working with GrapesJS editor, components, blocks, style manager, theming, custom component types, plugins, storage, panels, commands, traits, canvas (zoom/pan/drag), layers, assets, responsive design, modal, pages, data sources, i18n, RTE, keymaps, undo/redo, component scripts, symbols, CssComposer, resizable/draggable/droppable/locked properties, or any drag-and-drop page builder task with GrapesJS.
---

# GrapesJS Skill

## Quick Start

Initialize the editor:

```js
import 'grapesjs/dist/css/grapes.min.css';
import grapesjs from 'grapesjs';

const editor = grapesjs.init({
  container: '#gjs',
  fromElement: true,
  storageManager: false,
  plugins: [],
});
```

## Core API Modules

Access modules from the editor instance:

```js
editor.DomComponents   // Component management (alias: editor.Components)
editor.BlockManager     // Block management (alias: editor.Blocks)
editor.StyleManager     // Style properties
editor.Panels           // UI panels
editor.Commands         // Command system
editor.Canvas           // Canvas control
editor.StorageManager   // Data persistence (alias: editor.Storage)
editor.DeviceManager    // Responsive devices
editor.SelectorManager  // CSS selectors/classes
editor.Modal            // Modal dialogs
editor.Pages            // Multi-page support
editor.I18n             // Internationalization
editor.AssetManager     // Asset/media management (alias: editor.Assets)
editor.LayerManager     // Layer tree (alias: editor.Layers)
editor.TraitManager     // Trait/settings (alias: editor.Traits)
editor.RichTextEditor   // RTE customization
editor.Keymaps          // Keyboard shortcuts
editor.UndoManager      // Undo/Redo
editor.Parser           // HTML/CSS parser
```

## Key Editor Methods

```js
editor.getHtml()              // Get HTML output
editor.getCss()               // Get CSS output
editor.getJs()                // Get JS output
editor.getProjectData()       // Get full project JSON
editor.loadProjectData(json)  // Load project from JSON
editor.getWrapper()           // Root component
editor.getSelected()          // Last selected component
editor.getSelectedAll()       // All selected components
editor.select(component)      // Select a component
editor.selectAdd(component)   // Add to selection
editor.selectRemove(component)// Remove from selection
editor.addComponents(html)    // Add components
editor.setComponents(html)    // Replace components
editor.addStyle(css)          // Add CSS rules
editor.setStyle(css)          // Replace all CSS rules
editor.on(event, callback)    // Listen to events
editor.off(event, callback)   // Remove listener
editor.once(event, callback)  // Listen once
editor.runCommand(id, opts)   // Run command
editor.stopCommand(id, opts)  // Stop command
editor.store()                // Save to storage
editor.load()                 // Load from storage
editor.getDevice()            // Get current device name
editor.setDevice('Mobile')    // Switch device
editor.getDirtyCount()        // Unsaved changes count
editor.clearDirtyCount()      // Reset changes counter
editor.getContainer()         // Editor container HTMLElement
editor.onReady(callback)      // Run when editor is fully loaded
editor.destroy()              // Destroy editor
editor.refresh()              // Update editor dimensions
editor.setCustomRte(obj)      // Replace built-in RTE
editor.setDragMode(mode)      // 'absolute' | 'translate'
```

## Plugins

Plugins are functions executed on editor init. **Always define custom component types inside plugins** (necessary so types exist before templates are loaded from storage).

```js
const myPlugin = (editor, options) => {
  editor.DomComponents.addType('my-type', { /* ... */ });
  editor.BlockManager.add('my-block', { /* ... */ });
};

grapesjs.init({
  plugins: [myPlugin],
  pluginsOpts: { [myPlugin]: { opt1: 'value' } },
});
```

### TypeScript Usage

```ts
import grapesjs, { usePlugin } from 'grapesjs';
import type { Plugin } from 'grapesjs';

interface MyPluginOptions { opt1: string; opt2?: number; }

const myPlugin: Plugin<MyPluginOptions> = (editor, options) => { /* ... */ };

grapesjs.init({
  plugins: [usePlugin(myPlugin, { opt1: 'A', opt2: 1 })],
});
```

## Default Commands

Built-in commands use `core:*` namespace. Full list in [references/commands-reference.md](references/commands-reference.md). Key commands:

`core:canvas-clear`, `core:component-delete`, `core:component-enter` (select child), `core:component-exit` (select parent), `core:component-next/prev`, `core:component-outline`, `core:component-offset`, `core:component-select`, `core:copy`/`core:paste`, `core:preview`, `core:fullscreen`, `core:open-code`, `core:open-layers`, `core:open-styles`, `core:open-traits`, `core:open-blocks`, `core:open-assets`, `core:undo`/`core:redo`.

## Editor Init Config Reference

Key `grapesjs.init({...})` options:

```js
grapesjs.init({
  container: '#gjs',           // Selector or HTMLElement
  fromElement: false,          // Load content from container
  height: '100%',              // Editor height
  width: 'auto',               // Editor width
  projectData: {},             // Initial project data (skips storage load)
  mediaCondition: 'max-width', // or 'min-width' for mobile-first
  plugins: [],
  pluginsOpts: {},
  panels: { defaults: [] },
  blockManager: { blocks: [], appendTo: '.container' },
  layerManager: { appendTo: '.container' },
  styleManager: { appendTo: '.container', sectors: [] },
  selectorManager: { appendTo: '.container', componentFirst: false },
  traitManager: { appendTo: '.container' },
  storageManager: { type: 'local', autosave: true, autoload: true },
  deviceManager: { devices: [] },
  assetManager: { assets: [], upload: false },
  canvas: {
    scripts: [],               // JS files to load in canvas iframe
    styles: [],                // CSS files to load in canvas iframe
  },
  keymaps: { defaults: {} },   // Custom keyboard shortcuts
});
```

## Common Pitfalls

### 1. Component scripts run in an isolated iframe
All component scripts execute inside the canvas iframe, NOT in the editor's document. You cannot reference external variables, editor APIs, or outer-scope libraries inside `script`. Use `script-props` to pass data. See [references/components-js-reference.md](references/components-js-reference.md).

### 2. `find()` only works after render, `findType()` works always
`component.find('.my-class')` uses CSS selectors and requires the component to be rendered in the canvas. Use `component.findType('image')` or `component.closestType('section')` when working with components before render (e.g., in `init()` hooks or plugins).

### 3. Don't put styles or scripts in blocks
Block content should be component-oriented. Declare `styles` in the component type `defaults`, not in the block `content`. Scripts belong in the component type definition, not in block HTML.

### 4. `isComponent` is NOT called for objects or `data-gjs-type`
When you add components via objects (`{ type: 'my-type' }`) or HTML with `data-gjs-type`, the `isComponent` function is skipped. It only runs for plain HTML strings without `data-gjs-type`.

### 5. Component-scoped styles are grouped per type
Styles defined in `defaults.styles` are shared across all instances of that type and auto-removed only when ALL instances of that type are removed. Follow component-oriented styling: each type owns its own styles.

### 6. `locked` cascades to children
Setting `locked: true` on a component disables selection for it AND all its children. A child can opt out by explicitly setting its own `locked: false`.

### 7. `propagate` applies to NEW children only
The `propagate` array only affects components appended AFTER the property is set. Existing children are not retroactively updated.

### 8. UndoManager tracks components and CSS rules automatically
You don't need to manually add components or CSS rules to the UndoManager — they're auto-tracked. Use `um.skip(() => { ... })` for batch programmatic changes you don't want in the undo stack.

### 9. Aborting component removal
Listen to `component:remove:before` and set `opts.abort = true` to prevent deletion. Call the provided `removeFn()` later to complete it.

### 10. Canvas dependencies are NOT in exported HTML
Scripts/styles added via `canvas.scripts` / `canvas.styles` config are loaded in the editor's iframe but NOT included in `editor.getHtml()` output. You must include them separately in your final template.

## Detailed References

- **API Reference** (components, blocks, commands, storage, events, traits, canvas, assets, layers, pages): See [references/api-reference.md](references/api-reference.md)
- **Core API** (UndoManager, Canvas zoom/coords/drag, CssComposer, Keymaps, component properties like draggable/droppable/resizable/locked/selectable): See [references/core-api-reference.md](references/core-api-reference.md)
- **Components & JS + Symbols** (component scripts, script-props, dependencies, symbols/instances, overrides): See [references/components-js-reference.md](references/components-js-reference.md)
- **Style Customization** (Style Manager, theming, CSS variables, custom types): See [references/style-customization.md](references/style-customization.md)
- **Traits & Settings** (built-in types, custom types, custom UI, categories, i18n): See [references/traits-reference.md](references/traits-reference.md)
- **Canvas & Spots** (canvas spots, custom overlays, disabling built-in spots): See [references/canvas-reference.md](references/canvas-reference.md)
- **Storage Deep Dive** (local, remote, custom storage, inline, project data): See [references/storage-reference.md](references/storage-reference.md)
- **Commands Deep Dive** (stateful commands, extending, events, aborting): See [references/commands-reference.md](references/commands-reference.md)
- **UI Layout Patterns** (panels, layers, sidebar, switchers): See [references/ui-layout-patterns.md](references/ui-layout-patterns.md)
- **MJML Plugin** (email builder, MJML components, export MJML/HTML, custom components, preMjml/postMjml): See [references/mjml-plugin-reference.md](references/mjml-plugin-reference.md)
