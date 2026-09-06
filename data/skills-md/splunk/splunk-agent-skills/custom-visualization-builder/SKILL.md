---
name: custom-visualization-builder
description: Scaffold, build, package, and install a custom visualization into Splunk using the dashboard-studio-extension framework. Use when the user wants to create a new custom viz, add a visualization to an existing project, or migrate a legacy custom viz.
license: Apache-2.0
allowed-tools:
  - shell
requires-mcp: false
metadata:
  splunk:
    domain: dashboarding
    products:
      - splunk-enterprise
      - splunk-cloud-platform
      - dashboard-studio
    entities:
      - custom visualizations
      - dashboard extension projects
      - Splunk apps
      - SPL data contracts
      - visualization config.json files
    triggers:
      - Custom Visualization Builder
      - custom viz
      - custom visualization
      - dashboard-studio-extension
      - build custom visualization
      - migrate legacy visualization
    not-for:
      - production Splunk app installation without explicit user approval
      - credential collection
      - Splunk configuration changes outside the visualization app
    outcomes:
      - scaffolded visualization project
      - packaged Splunk visualization app
      - migrated legacy custom visualization
      - sample SPL data contract
---

# Custom Visualization Builder

Scaffold, build, package, and install a custom Splunk dashboard visualization using the `@splunk/dashboard-studio-extension` framework. Vizzes run in a sandboxed iframe and receive data from Splunk searches. You can build them with plain JavaScript or React — pick based on what the viz needs.

No local Splunk instance is required for development. Build and package locally, then install the `.spl` into a supported instance. Requires Splunk Enterprise 10.4+ or Splunk Cloud Platform (equivalent release).

## When to Use

Use this skill when a user asks to create a new Splunk custom visualization, add a visualization to an existing dashboard-studio-extension project, package a visualization as a Splunk app, or migrate a legacy RequireJS custom viz to the current extension framework.

Do not install or update a visualization in a production or shared Splunk environment unless the user explicitly confirms that target. Do not ask users for raw credentials; use already configured local Splunk auth or a user-run install command.

---

## Prerequisites

- Node.js >= 22
- Yarn >= 1.22
- Target instance: Splunk Enterprise 10.4+ or Splunk Cloud Platform (equivalent release)

---

## Choose a framework

| | JavaScript (`@splunk/dashboard-studio-extension`) | React (`@splunk/dashboard-studio-extension/react`) |
|---|---|---|
| Use when | Canvas rendering, D3, plain DOM, minimal deps | Component-heavy UI, hooks-based state, most new projects |
| API style | Event listeners + getters | Hooks (`useDataSources`, `useDimensions`, `useOptions`, …) |
| Entry file | `visualization.js` | `visualization.jsx` |
| Extra deps | None | `react`, `react-dom` (peer deps, added by scaffold) |

---

## Project Structure

A project is a Splunk app that can contain one or more visualizations under `visualizations/`. Each viz has its own directory with `config.json`, `src/`, and `SPL.md`.

```
my-viz-project/
├── package.json
├── build.mjs                    # esbuild orchestrator
├── build-plugins/
│   └── css-and-size.mjs         # CSS injection + asset inlining plugin
├── package.mjs                  # .spl packager
├── package/
│   └── app/
│       └── app.conf             # Splunk app identity (source of truth for id/version)
├── visualizations/
│   ├── <viz-one>/
│   │   ├── SPL.md               # SPL reference for this viz (you create this)
│   │   ├── config.json
│   │   └── src/
│   │       ├── visualization.js(x)
│   │       └── visualization.css
│   └── <viz-two>/
│       ├── SPL.md
│       ├── config.json
│       └── src/
│           ├── visualization.js(x)
│           └── visualization.css
└── dist/                        # build output (generated)
```

The build system automatically discovers all directories under `visualizations/` and builds them all. Name the project folder after the collection, not a single viz (e.g. `splunk-custom-vizzes`, not `gauge`).

---

## Workflow Overview

### 1. Gather requirements

Before generating any code, ask the user (or extract from context):

1. **Project name** — used as the Splunk app ID. Only letters, numbers, dots, and underscores. Cannot start or end with a dot or underscore. E.g. `my_custom_viz`.
2. **Viz slug** — the directory name under `visualizations/`. Only lowercase letters, numbers, and underscores (`[a-z0-9_]`). No dots, slashes, or spaces. Reject any value that would place files outside `visualizations/<viz-slug>/`. E.g. `network_graph`.
3. **Viz display label** — human-readable name shown in the Splunk UI, e.g. "Network Graph".
4. **Description** — one-line description of what the viz does.
5. **Author** — for `app.conf`.
6. **Expected SPL columns** — which fields the search must produce. Distinguish required from optional.
7. **Configurable settings** — what the user should be able to tweak (colors, thresholds, toggles). For each: name, type, default.
8. **Rendering approach** — what to draw/render (canvas shapes, chart, table, map, etc.) to inform framework choice.

Apply the defaults in [Accessibility & safe rendering](#accessibility--safe-rendering) unless the user's request or context makes them clearly inapplicable.

If the user's request is vague, ask before scaffolding.

### 2. Determine project location

Ask the user where to create the project if not specified. This can be any empty directory — no existing dashboard-enterprise repo required.

**Adding a viz to an existing project**: If a project already exists with build infrastructure, skip step 3 entirely. Just create `visualizations/<viz-name>/` with `config.json`, `src/visualization.js(x)`, `src/visualization.css`, and `SPL.md`. The build discovers all viz directories automatically — no registration needed. Then go to step 5.

### 3. Scaffold the project

The `@splunk/create` CLI currently requires interactive prompts for label, description, author, and template — only the project name can be passed as a positional arg. Full non-interactive support is planned. Ask the user to run the command and answer the remaining prompts:

> "Please run this in your terminal and follow the prompts, then let me know when done:"
> ```
> mkdir <project-name> && cd <project-name>
> npx @splunk/create@latest --mode=dashboard-studio-extension <app_id>
> ```
> Use these values when prompted:
> - **Display label**: `<Human Readable Label>`
> - **Description**: `<description>`
> - **Author**: `<author>`
> - **Template**: JavaScript or React (per your framework choice above)
>
> Then run `yarn` to install dependencies.

Wait for the user to confirm the scaffold is complete before proceeding.

After scaffolding, verify `package/app/app.conf` has the correct app identity. The
scaffold generates this shape (values filled from your prompt answers):

```ini
[package]
id = <app_id>

[id]
version = 0.1.0
name = <app_id>

[ui]
is_visible = 1
label = <Human Readable Label>
show_in_nav = 0

[launcher]
author = <author>
description = <description>
version = 0.1.0

[install]
is_configured = 0
build = <@- buildNumber @>
check_for_updates = 0

[manifest]
category = Custom
```

App `id`: only letters, numbers, dots, underscores. Cannot start or end with a dot or underscore.

> **Leave `build = <@- buildNumber @>` exactly as-is.** That template tag is intentional —
> the packager (`yarn package`) substitutes a real build number when it stages the app.
> Do not replace it with a literal.

Then create `SPL.md` inside the viz directory (`visualizations/<viz-name>/SPL.md`):

```markdown
# <Display Label> — SPL Reference

## Expected Columns

| Column | Type | Required? | Description |
|--------|------|-----------|-------------|
| <col>  | <type> | Yes/Optional | <what it is> |

## Notes

- Key data assumptions, units, fallback behavior, etc.

## Full SPL

\`\`\`spl
<full working SPL query>
\`\`\`

## Time range

`rt-1m` to `rt` (or `-60m` to `now` for historical)
```

### 4. Create the visualization

**`visualizations/<viz-name>/config.json`** — see `references/config-json.md` for full field reference including `optionsSchema` and `editorConfig`:

```json
{
  "showTitleAndDescription": true,
  "includeInToolbar": true,
  "includeInVizSwitcher": true,
  "showDrilldown": false,
  "canSetTokens": [],
  "hasEventHandlers": false,
  "config": {
    "name": "<Human Readable Name>",
    "description": "<description>",
    "category": "Custom",
    "icon": null,
    "dataContract": {
      "requiredDataSources": ["primary"],
      "optionalDataSources": []
    },
    "size": { "initialWidth": 600, "initialHeight": 500 },
    "optionsSchema": {},
    "editorConfig": []
  }
}
```

---

**JavaScript — `visualization.js`**:

Data always arrives in columnar format: `{ fields: [{name}, ...], columns: [[col0val0, col0val1, ...], ...] }`. All values are strings — parse numerics explicitly. Listener methods return a cleanup function.

```js
import { VisualizationAPI } from '@splunk/dashboard-studio-extension';
import './visualization.css';

const container = document.createElement('div');
container.className = 'viz-container';
document.body.appendChild(container);

const state = { data: null, loading: false, options: {}, width: 0, height: 0, theme: 'light' };

function render() {
    if (state.loading) { container.innerHTML = '<div class="loading">Loading...</div>'; return; }
    if (!state.data)   { container.innerHTML = '<div class="empty">No data</div>'; return; }

    const { fields, columns } = state.data;
    if (!columns?.length || !columns[0].length) {
        container.innerHTML = '<div class="empty">No data</div>';
        return;
    }

    // Always provide fallbacks — options may be unset even if optionsSchema declares defaults
    const myOption = state.options.myOption ?? 'default';
    const isDark = state.theme === 'dark';

    // implement visualization here
}

VisualizationAPI.addDataSourcesListener(
    ({ dataSources, loading }) => {
        state.loading = loading;
        state.data = dataSources?.primary?.data ?? null;
        render();
    },
    { invokeImmediately: true }
);

VisualizationAPI.addOptionsListener(({ options }) => {
    state.options = options;
    render();
});

VisualizationAPI.addDimensionsListener(({ width, height }) => {
    state.width = width;
    state.height = height;
    render();
}, { invokeImmediately: true });

VisualizationAPI.addThemeListener(({ theme }) => {
    state.theme = theme;
    render();
}, { invokeImmediately: true });
```

---

**React — `visualization.jsx`**:

Call the hooks directly from your component.

```jsx
import {
    useDataSources,
    useDimensions,
    useOptions,
    useTheme,
} from '@splunk/dashboard-studio-extension/react';
import { createRoot } from 'react-dom/client';
import './visualization.css';

function Viz() {
    const { dataSources, loading } = useDataSources();
    const { width, height } = useDimensions();
    const { options } = useOptions();
    const { theme } = useTheme();

    // Always provide fallbacks — options may be unset even if optionsSchema declares defaults
    const myOption = options?.myOption ?? 'default';
    const isDark = theme === 'dark';

    if (loading) return <div className="loading">Loading...</div>;

    const data = dataSources?.primary?.data;
    if (!data?.columns?.length || !data.columns[0].length)
        return <div className="empty">No data</div>;

    const { fields, columns } = data;

    // implement visualization here
    return <div style={{ width, height }} />;
}

createRoot(document.getElementById('root')).render(<Viz />);
```

---

### 5. Develop

```bash
# Watch mode — rebuilds on file changes
yarn dev
```

Verify `dist/<viz-name>/visualization.js` is created. Hard-refresh the browser to see changes.

### 6. Build for production

```bash
yarn build:prod
```

### 7. Package

```bash
yarn package
```

Output: `dist/<app-id>-<version>-<hash>.spl`

The packager auto-generates `default/visualizations.conf` (with `framework_type = studio_visualization`) and `metadata/default.meta` from the vizzes it finds in `dist/`.

### 8. Install into Splunk

**Splunk Enterprise (10.4+)**: Apps > Manage Apps > Install app from file → select the `.spl`. No restart needed — the app loads immediately.

**Splunk Cloud Platform**: Private app installation requires the ACS CLI and AppInspect vetting. Do not direct Cloud users to the Splunk Web install UI — it will not work for private apps. Direct the user to the Splunk ACS documentation for the private app submission process.

**Local Docker**: Copy the `.spl` into the container and install via the Splunk CLI:
```
docker cp dist/<app-id>-<version>-<hash>.spl <container>:/tmp/app.spl
docker exec <container> /opt/splunk/bin/splunk install app /tmp/app.spl -update 1
```

### 9. Tell the user

- The Splunk app ID
- The viz type string for dashboard JSON: `<app-id>.<viz-name>`
- A sample SPL query to wire up data

Before reporting the viz as complete, verify (unless the request made them inapplicable):
- Untrusted search values are escaped before being written to the DOM
- Interactive elements are keyboard-reachable and have accessible labels
- Text and icon colors meet WCAG AA contrast against their backgrounds in both light and dark theme
- Animations respect `prefers-reduced-motion`

---

## Examples

**New canvas viz from scratch:**
> "Build me a network graph visualization that shows connections between hosts."

Skill gathers requirements, asks the user to scaffold, creates `visualization.js` with canvas rendering, wires up data/dimensions/theme listeners, and packages the `.spl`.

**Adding a viz to an existing project:**
> "Add a gauge viz to my existing custom viz project."

Skill skips scaffolding, creates `visualizations/gauge/` with `config.json`, `src/visualization.js`, and `SPL.md`, and instructs the user to rebuild.

**Migrating a legacy viz:**
> "Migrate my RequireJS custom viz to the new framework."

Skill reads the existing viz, maps `updateView` → `render()`, replaces `SplunkVisualizationBase` with `VisualizationAPI` listeners, removes RequireJS wrapper, and re-scaffolds the project.

---

## Updating the viz (fast iteration)

For changes to visualization code only, copy the built JS directly — no reinstall needed:

```bash
yarn dev  # or yarn build:prod

cp dist/<viz-name>/visualization.js \
   $SPLUNK_HOME/etc/apps/<app-id>/appserver/static/visualizations/<viz-name>/visualization.js
```

Hard-refresh the browser. No Splunk restart needed.

For changes to `app.conf`, `config.json`, or adding a new viz, do a full reinstall (step 7–8).

> **Restart required for `showDrilldown`**: After enabling `showDrilldown: true` in an already-installed app, Splunk must be restarted — the REST layer caches `config.json` at startup, and reinstalling alone won't update the Interactions panel.

---

## Theme support

Vizzes should respond to Splunk's light/dark theme. The iframe is sandboxed — CSS custom properties from the host page are not inherited. Use hardcoded enterprise theme values.

**JavaScript:**

```js
const THEME_COLORS = {
    light: { background: '#ffffff', text: '#1a1a1a', accent: '#4e9cf5' },
    dark:  { background: '#1a1c21', text: '#c3cbd4', accent: '#4e9cf5' },
};

VisualizationAPI.addThemeListener(({ theme }) => {
    state.theme = theme;
    render();
}, { invokeImmediately: true });

function render() {
    const colors = THEME_COLORS[state.theme] ?? THEME_COLORS.light;
    container.style.background = colors.background;
    // use colors.text, colors.accent in drawing logic
}
```

**React:**

```jsx
const THEME_COLORS = {
    light: { background: '#ffffff', text: '#1a1a1a', accent: '#4e9cf5' },
    dark:  { background: '#1a1c21', text: '#c3cbd4', accent: '#4e9cf5' },
};

function Viz() {
    const { theme } = useTheme();
    const colors = THEME_COLORS[theme] ?? THEME_COLORS.light;
    return <div style={{ background: colors.background, color: colors.text }}>...</div>;
}
```

---

## Accessibility & safe rendering

These are defaults — apply them unless the user's request or context makes them clearly inapplicable.

**Escape untrusted search values before writing to the DOM.** Never use `innerHTML` or `insertAdjacentHTML` with raw field values from `dataSources`. Use `textContent`, `createElement`, or a sanitizing helper instead.

```js
// safe
const el = document.createElement('div');
el.textContent = row.label;

// unsafe — do not do this
container.innerHTML = `<div>${row.label}</div>`;
```

**Make interactive elements keyboard-reachable.** If clicking or hovering triggers behavior, ensure the element has `tabIndex="0"` and handles `keydown` for Enter/Space.

```js
el.setAttribute('tabindex', '0');
el.setAttribute('role', 'button');
el.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') handleClick();
});
```

**Provide text alternatives.** Canvas elements and icon-only controls need an accessible label.

```js
canvas.setAttribute('role', 'img');
canvas.setAttribute('aria-label', 'Network graph showing host connections');
```

**Meet WCAG AA contrast.** Foreground text and icons must have at least 4.5:1 contrast against their background (3:1 for large text). The hardcoded `THEME_COLORS` values in [Theme support](#theme-support) already satisfy this for default text — use them as the baseline and verify any custom accent or status colors.

**Respect `prefers-reduced-motion`.** If the viz uses animation, check the media query and skip or minimise motion when it is set.

```js
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!reduceMotion) requestAnimationFrame(animate);
```

---

## Canvas

See `references/canvas.md` for sizing, interactivity, and drilldown patterns.

---

## How the scaffolded build picks entry files

The scaffolded `build.mjs` does **not** auto-detect each viz's extension. Every
`package.json` script passes a single global `--entry=<filename>`, and the build applies
that one filename to **every** directory under `visualizations/`:

```js
const entryArg = process.argv.find((a) => a.startsWith('--entry='));
const entryFileName = entryArg ? entryArg.split('=')[1] : 'visualization.js';
// for each viz: build visualizations/<viz>/src/<entryFileName>
// if that file is missing: "Warning: <viz>/src/<entryFileName> not found, skipping"
```

`jsx: 'automatic'` is enabled only when `entryFileName` ends in `.jsx`.

Consequences you must design around:
- **All vizzes in one scaffolded project share one extension.** A JavaScript-scaffolded
  project (`--entry=visualization.js`) builds only `visualization.js` files; a
  React-scaffolded project (`--entry=visualization.jsx`) builds only `visualization.jsx`.
- **Mismatched files are silently skipped** — the build warns and exits 0, so a viz can
  vanish from `dist/` without an obvious error. If a viz doesn't appear in `dist/`, check
  that its entry file matches the project's `--entry` extension.

### Adding a React viz

- **React-scaffolded project:** just add `visualizations/<viz>/src/visualization.jsx` —
  it builds automatically.
- **JavaScript-scaffolded project, no JS vizzes worth keeping:** the simplest path is to
  flip the whole project to `.jsx`. Add React (`yarn add react react-dom`), rename the
  existing entry to `visualization.jsx`, and change every `--entry=visualization.js` to
  `--entry=visualization.jsx` in `package.json`. `jsx: 'automatic'` turns on by itself.
- **You truly need both `.js` and `.jsx` vizzes in one project:** the scaffolded
  single-`--entry` build can't do this. Replace the entry lookup in `build.mjs` with
  per-viz resolution (prefer `.jsx`, fall back to `.js`) and always set
  `jsx: 'automatic'`:

   ```js
   const buildOptions = { jsx: 'automatic', /* ... */ };

   function resolveEntry(vizName) {
       for (const name of ['visualization.jsx', 'visualization.js']) {
           const p = join(visualizationsDir, vizName, 'src', name);
           if (existsSync(p)) return p;
       }
       return null;
   }
   ```

   Then drop the `--entry` flag from the `package.json` scripts. (This is a local
   modification, not what `@splunk/create` produces.)

> **Avoid `@splunk/react-ui` in the entry file.** The scaffolded React template's default
> viz imports `@splunk/react-ui` components (`Table`, `Paragraph`, `WaitSpinner`), but
> those are pre-bundled CommonJS and their default exports do **not** survive the
> scaffold's esbuild ESM pipeline — the built viz throws `Minified React error #130`
> (got an object instead of a component) on load. Build your UI with plain elements (or
> your own components). If you must use `@splunk/react-ui`, expect to add esbuild interop
> configuration to `build.mjs` first.

---

## Migrating a legacy custom viz

See `references/migration.md` for a full mapping from `SplunkVisualizationBase` to the new framework and step-by-step migration instructions.

---

## Troubleshooting

See `references/troubleshooting.md`.

---

## Key Constraints

- `app.conf` uses literal values **except** `build = <@- buildNumber @>` — that template tag is intentional and the packager fills it in. Don't replace it with a literal.
- App `id`: only letters, numbers, dots, underscores. Cannot start or end with a dot or underscore.
- Viz slug: only `[a-z0-9_]`. Reject values containing dots, slashes, or spaces. Confirm the resolved path is `visualizations/<viz-slug>/` with no traversal.
- CSS is injected into the iframe via the build plugin — no separate `<link>` tag needed
- Images, SVGs, and fonts are inlined as data URLs by the build — import them directly
- Do not load fonts or other assets from external URLs at runtime. Vendor them locally and import from `src/` so the build inlines them as data URLs.
- `setOptions` is silently ignored in view mode — only works during edit mode
- Always provide option fallback values — `optionsSchema` defaults are not guaranteed at runtime
- The viz runs in a sandboxed iframe — `window.parent` is not accessible and CSS custom properties from the host page are not inherited

---

## References

- `references/api-reference.md` — full API listing for JavaScript and React
- `references/config-json.md` — `config.json` field reference, `optionsSchema`, `editorConfig` editor types
- `references/drilldown-and-tokens.md` — drilldown patterns and token read/write
- `references/canvas.md` — canvas sizing, interactivity, and drilldown patterns
- `references/migration.md` — migrating from legacy `SplunkVisualizationBase` vizzes
- `references/troubleshooting.md` — common errors and fixes
