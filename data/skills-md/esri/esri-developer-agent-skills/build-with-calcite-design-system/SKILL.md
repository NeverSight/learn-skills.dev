---
name: build-with-calcite-design-system
license: Apache-2.0
description: "Use when building, integrating, styling, or reviewing accessible web interfaces with Calcite Design System. Inspect the app's framework and package manager, follow official setup guidance, use Calcite components and design tokens for reusable UI, apply accessible interaction and theming patterns, and validate component behavior. Use for frontend work with Esri SDKs when Calcite is the design system. Do not use for guidance on other design systems."
---

# Build with Calcite Design System

Use Calcite to build cohesive interfaces without creating common controls from scratch. It can be used independently or alongside an Esri SDK, and integrates with various frontend frameworks. Calcite provides reusable UI components and documented behavior, while the application code manages application state, data, and workflows.

Calcite components are designed with accessibility in mind, but applications still require appropriate content and configuration to support diverse audiences.

## Application requirements

If the application's development requirements are unclear, use the `gather-arcgis-application-requirements` skill to review project context and clarify consequential unknowns before proceeding. Then apply this skill's technology-specific guidance, reusing requirements already clear from the request or project.

## ArcGIS account requirements

Developers must have one of the following ArcGIS accounts to create applications: ArcGIS Location Platform (free), or ArcGIS Online or ArcGIS Enterprise with a Creator, Professional, or Professional Plus user type. The account's user type, role, and privileges provide access to different resources and operations.

## Installation and setup

1. Inspect the app's framework, package manager, installed Calcite version, and current component-loading approach. Reuse the existing setup and conventions; change dependencies only when the task requires it.
2. Choose a loading approach from the official [Get started](https://developers.arcgis.com/calcite-design-system/get-started/) guide: use the CDN for a page without a package build, or the existing package manager for a managed app. The Custom Elements build supports importing the components an app uses and is recommended for framework projects; choose the Distribution build when global registration is needed.
3. Consult [Framework integration](https://developers.arcgis.com/calcite-design-system/resources/frameworks/) only for requirements relevant to the app. For React, use the current guidance for its version: React 19+ supports custom elements directly, and the React wrapper is deprecated in Calcite 5.0. If using ArcGIS Maps SDK for JavaScript, check its Calcite loading and version-compatibility guidance before adding imports or changing versions.
4. Load styles and assets as needed for the selected framework and hosting setup. Follow the framework's CSS guidance; Calcite assets are CDN-hosted by default, so configure an asset path when hosting them locally or using a custom CDN.
5. Validate the setup in the app: confirm the components in use register and render, and their styles and required assets load. Consult [System requirements](https://developers.arcgis.com/calcite-design-system/resources/system-requirements/) when selecting supported browsers.

## How to query documentation

Installing this skill individually does not configure **Esri MCP server for developer documentation** (`esri-mcp-server-for-developer-documentation`). Add that server at `https://developers-mcp.arcgis.com/mcp` using your client's MCP settings, or install the full **ArcGIS SDKs and APIs** plugin (`arcgis-sdks-and-apis-plugin`). If the MCP server is unavailable, consult the linked official Esri documentation.

Documentation can be queried using the Esri MCP server for developer documentation (`esri-mcp-server-for-developer-documentation`):

```txt
https://developers-mcp.arcgis.com/mcp
```
Use the `search_esri_developer_docs` tool to surface authoritative documentation pages with `calcite-design-system` as the `focus_area` parameter in addition to a specified `search_term`. Use the `fetch_esri_developer_docs` tool with the `page_url` parameter set to return the full content of a documentation page in Markdown format. 

Clearly indicate any recommendations and assumptions that are not grounded in the official documentation. If the MCP server is unavailable, consult official documentation URLs below.

## Documentation links

- [Calcite Design System overview](https://developers.arcgis.com/calcite-design-system/) - Use for an overview of Calcite's purpose and the main documentation areas.
- [Get started](https://developers.arcgis.com/calcite-design-system/get-started/) - Use for adding Calcite through a CDN or npm, loading styles and assets, and choosing a component build.
- [Core concepts](https://developers.arcgis.com/calcite-design-system/core-concepts/) - Use for understanding how Calcite works with these core web component concepts: custom elements, slots, shadow DOM, CSS variables, component loading, attributes and properties, events, global configuration, forms, and modes.
- [Tutorials](https://developers.arcgis.com/calcite-design-system/tutorials/) - Use to follow tutorials for building apps with Calcite components and patterns, including apps that use ArcGIS Maps SDK functionality.
- [Components](https://developers.arcgis.com/calcite-design-system/components/) - Use to find a component and access its usage guidance and API details, including properties, slots, styles, events, and accessibility.
- [Button component reference](https://developers.arcgis.com/calcite-design-system/components/button/) - Use for the Button component's purpose, usage recommendations, accessibility, properties, slots, styles, and methods. Consult the corresponding page for other components.
- [Accessibility](https://developers.arcgis.com/calcite-design-system/foundations/accessibility/) - Use when designing or reviewing keyboard access, focus, content, color use, forms, and support for assistive technologies.
- [Colors and theming](https://developers.arcgis.com/calcite-design-system/foundations/colors/) - Use when applying color tokens, choosing light or dark mode, or customizing the theme.
- [Design tokens usage](https://developers.arcgis.com/calcite-design-system/foundations/tokens/usage/) - Use for understanding what design tokens are and how they work in Calcite. Explains core, semantic, and component token tiers, their intended scope, how to override them, naming, and structure.
- [Design tokens reference](https://developers.arcgis.com/calcite-design-system/foundations/tokens/reference/) - Use for a complete reference of available design tokens, including their names, values, and and deprecation status.
- [Calcite UI Icons](https://developers.arcgis.com/calcite-design-system/foundations/iconography/ui-icons/) - Use when selecting or integrating Calcite UI icons. For icons in web components, consult the `calcite-icon` component guidance.
- [Framework integration](https://developers.arcgis.com/calcite-design-system/resources/frameworks/) - Use for framework and TypeScript configuration, test runner setup, and Visual Studio Code IntelliSense.
- [Sample code](https://developers.arcgis.com/calcite-design-system/sample-code/) - Use for complete examples of application layouts and component workflows that can be adapted to a project.

## Patterns and guidelines

### Design principles

- Keep the user's main work area as the focus. Secondary controls should take only the space they need.
- Choose the layout component that fits the workflow and the context users need to keep in view. Do not scatter positioned controls across the page.
- Compose existing Calcite components before creating a new component. A Panel, Block, Action Bar, List, Sheet, or other group of Calcite components can often provide the needed experience without creating a custom component.
- Create a custom component only when it provides behavior or interaction that cannot be expressed clearly by composing Calcite components. Avoid one-off wrappers that only restyle or rename an existing Calcite component.
- Separate responsive behavior from adaptive behavior. Components can resize or overflow on their own, but the app may still need to move, hide, or replace content.
- Keep critical actions available at every supported size. Let secondary actions overflow, move to a menu, or appear only when needed.
- Keep the current context and focus when a Panel, Sheet, Dialog, Action Bar, or navigation mode opens, closes, or changes.

### Choose the right component

| Component                               | Use it for                                                                                           |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `calcite-shell`                         | The application frame, including the header, content, Panels, Sheets, and Dialogs.                   |
| `calcite-navigation`                    | App identity, primary navigation, user content, and compact navigation actions.                      |
| `calcite-shell-panel`                   | Side or bottom regions that are docked, floating, collapsible, or resizable.                         |
| `calcite-panel`                         | A headed area for related content, controls, or status.                                              |
| `calcite-sheet`                         | Contextual or mobile content that should temporarily slide over a Shell.                             |
| `calcite-dialog`                        | A focused, movable, resizable, or modal workspace area. needed.                                      |
| `calcite-action-bar`                    | A compact group of related Actions, with overflow when needed.                                       |
| `calcite-flow`                          | Step-by-step or nested navigation between related views. It is one option for master/detail layouts. |
| `calcite-block`                         | An expandable group of related controls inside a Panel.                                              |
| `calcite-list`                          | Dense selectable, filterable, or hierarchical items.                                                 |
| `calcite-tabs`                          | Related views that should stay in the same workspace.                                                |
| `calcite-card-group` and `calcite-card` | Browse, catalog, gallery, and other repeated content.                                                |
| `calcite-tile-group` and `calcite-tile` | Compact metrics, choices, or summary values.                                                         |

### Application shell

Start with `calcite-shell`. Put app identity and global Navigation in the `header` slot. Put secondary regions in Shell slots and keep the main work area in the default content area.

```html
<calcite-shell>
  <calcite-navigation slot="header">
    <calcite-navigation-logo
      slot="logo"
      heading="Map workspace"
      alt="Application logo"
    ></calcite-navigation-logo>
  </calcite-navigation>

  <calcite-shell-panel slot="panel-start" resizable>
    <calcite-panel heading="Layers">
      <calcite-block heading="Visible layers" expanded>
        <calcite-list label="Map layers"></calcite-list>
      </calcite-block>
    </calcite-panel>
  </calcite-shell-panel>

  <arcgis-map id="map"></arcgis-map>
</calcite-shell>
```

Use `panel-start` or `panel-end` for side regions, `panel-bottom` or `content-bottom` for bottom workspaces, `header` for navigation, `dialogs` for Dialogs, and `sheets` for Sheets owned by the Shell. Put an Action Bar and Panel in the same Shell Panel when users need both tool navigation and detailed controls.

For a map or scene behind floating UI, use `content-behind`. Size and place the overlay so it does not block the main map interaction:

```html
<calcite-shell content-behind>
  <calcite-navigation slot="header">
    <calcite-navigation-logo
      slot="logo"
      heading="Map details"
    ></calcite-navigation-logo>
  </calcite-navigation>

  <calcite-shell-panel slot="panel-end" display-mode="float">
    <calcite-panel heading="Details">
      <calcite-block heading="Summary" expanded></calcite-block>
    </calcite-panel>
  </calcite-shell-panel>

  <arcgis-map id="map"></arcgis-map>
</calcite-shell>
```

### Layout patterns

Choose the smallest layout that supports the workflow.

#### Sidebar and overlay

Use a resizable, docked Shell Panel when controls need to stay beside the main work area. Use `display-mode="float"` when the panel should overlay the work area and open or close as needed. Set useful minimum and maximum sizes for resizable regions using the `--calcite-shell-panel-min-width` and `--calcite-shell-panel-max-width` CSS tokens.

#### Dashboard and adaptive grid

Use CSS Grid inside the Shell when several metrics, configuration controls, and a main map or chart should stay visible together. Put dashboard panels in the Shell's default content area. Use a Sheet for controls that need to move into a smaller layout.

```css
.dashboard-grid {
  display: grid;
  grid-template-columns: minmax(18rem, 0.5fr) 1fr 1fr;
  grid-template-areas:
    "options metric-a metric-b"
    "options map map";
  gap: 1rem;
  height: 100%;
}

@media (max-width: 799px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    grid-template-areas:
      "metric-a"
      "metric-b"
      "map";
  }
}
```

For a multi-view editing workspace, keep the layout choice in an Action Group and use CSS for the arrangements. At smaller widths, change the Shell Panel to an overlay, hide controls that only change the layout, and combine views when the full grid no longer works.

#### Browse and catalog

Use Navigation, Menu, Tabs, Tile Groups, Card Groups, and Cards when users scan and filter repeated content. Keep navigation available on small screens by replacing desktop menus with a Sheet opened by a Navigation action. Let Tabs scroll, and change Card Groups from three columns to two and then one as space decreases.

```html
<calcite-navigation slot="header">
  <calcite-navigation-logo
    slot="logo"
    heading="Catalog"
  ></calcite-navigation-logo>
  <calcite-action
    slot="navigation-action"
    icon="hamburger"
    text="Navigation"
  ></calcite-action>
  <calcite-menu slot="content-start" label="Main navigation"></calcite-menu>
</calcite-navigation>

<calcite-sheet heading="Navigation" display-mode="float">
  <calcite-menu layout="vertical" label="Mobile navigation"></calcite-menu>
</calcite-sheet>

<calcite-card-group label="Available courses"></calcite-card-group>
```

#### Detail and gallery

Keep the main map, image, or canvas dominant. On wide screens, place details in a CSS Grid Panel beside it. On small screens, show the same details in a contextual Sheet opened by an Action. In a framework app, render one content model in the right container instead of keeping two separate copies in sync.

```html
<calcite-shell>
  <calcite-panel class="map-panel">
    <calcite-action-bar slot="header-actions-end" layout="horizontal">
      <calcite-action
        id="details-action"
        icon="information"
        text="Map details"
      ></calcite-action>
    </calcite-action-bar>
    <calcite-sheet id="details-sheet" slot="sheets" heading="Map details">
      <calcite-panel id="details-panel" heading="Map details"></calcite-panel>
    </calcite-sheet>
    <arcgis-map id="map"></arcgis-map>
  </calcite-panel>
</calcite-shell>
```

#### Configuration and preview

For authoring or configuration workflows, make the preview the main focus. Use a Shell Panel for configuration controls. Nest a Shell inside the preview Panel when the preview needs its own app frame. Keep undo, redo, save, and publish visible; let secondary add-content actions overflow.

#### Workspace and pop-out content

For complex customizable workflows, let users choose how supporting content is shown. The component samples use a resizable bottom Shell Panel for docked work and a draggable, resizable Dialog for a pop-out view. A Sheet can provide a compact list of open items.

```html
<calcite-shell>
  <arcgis-map id="map"></arcgis-map>
  <calcite-shell-panel slot="panel-bottom" resizable>
    <calcite-panel heading="Open projects"></calcite-panel>
  </calcite-shell-panel>
  <calcite-dialog
    slot="dialogs"
    heading="Open projects"
    drag-enabled
    resizable
    placement="bottom-end"
  ></calcite-dialog>
</calcite-shell>
```

When the same workflow can appear in two places, keep the selected item and active tab in sync. When switching places, hide one before showing the other and move focus to the matching control.

#### Nested and resizable regions

Nested Shells work well for dense monitoring or analysis workflows with several adjustable regions. Use `scale="s"` when more content needs to fit, but keep headings and resize controls usable. Set minimum and maximum bounds for every resizable region:

```css
#results-panel[resizable] {
  --calcite-shell-panel-min-height: 3rem;
  --calcite-shell-panel-height: 40vh;
  --calcite-shell-panel-max-height: 70vh;
}
```

Do not let a Panel become smaller than the space needed for its heading, controls, or keyboard interaction. Consider the limits of nested Panels, not only the outer Shell Panel.

### Responsive and adaptive behavior

#### Responsive behavior

Many Calcite components handle common responsive behavior for you. Action Bars can overflow into an Action Menu, Tabs can scroll, Shell Panels fit the available space, and components can adjust their internal spacing. Use these built-in behaviors before writing breakpoint logic.

#### Adaptive behavior

Adaptive behavior changes the app layout at a breakpoint or when a container changes size. This can mean changing properties, moving content between slots, changing CSS Grid areas, hiding nonessential content, or replacing a Panel with a Sheet.

Use CSS for presentation and JavaScript for component state and surface changes:

```js
const panel = document.querySelector("#config-panel");
const sheet = document.querySelector("#config-sheet");
const navigationAction = document.querySelector("#navigation-action");

navigationAction?.addEventListener("click", () => {
  sheet.open = true;
});

window.addEventListener("resize", () => {
  const compact = window.innerWidth < 800;
  panel.hidden = compact;
  if (!compact) sheet.open = false;
});
```

In production apps, use the framework's reactive state or a `ResizeObserver` when the container, rather than the viewport, controls the layout. Close or move content when it no longer fits, and do not leave focus inside a hidden element.

The samples use these adaptive changes:

- Replace desktop Navigation menus with a mobile Sheet and Navigation action.
- Move desktop detail Panels into contextual Sheets.
- Change Shell Panel `displayMode` from `"dock"` to `"overlay"`.
- Hide viewport-only or decorative content while preserving primary actions.
- Remove long Navigation Logo or user text at compact widths.
- Consolidate multiple map views into one arrangement when the grid becomes unusable.
- Keep critical actions visible by disabling Action Bar overflow for that group, while allowing secondary actions to overflow.

### Actions and contextual controls

Use an Action Bar for a stable set of related tools and Action Groups for selection and grouping. For contextual workflows, show a second or third Action Bar instead of every possible control at once. Add a clear back or close Action, explain whether closing discards changes, move focus to the new controls, and return focus to the Action that opened them.

Set `text` on every Action, including icon-only ones, so each has an accessible name. Add a Tooltip when compact UI removes visible text, but do not make a Tooltip the only explanation for a critical Action.

### Forms, status, and feedback

Use Calcite for actions and inputs instead of mixing unrelated control styles:

```html
<calcite-button appearance="solid" kind="brand" icon-start="plus">
  Add feature
</calcite-button>
<calcite-action icon="layers" text="Layers"></calcite-action>
<calcite-combobox
  placeholder="Select categories"
  label-text="Category"
  selection-mode="multiple"
>
  <calcite-combobox-item
    value="parks"
    text-label="Parks"
  ></calcite-combobox-item>
</calcite-combobox>
<calcite-label>
  Show labels
  <calcite-switch checked></calcite-switch>
</calcite-label>
```

Use Alert for temporary notifications and Notice for messages that stay in the page. Use Chips for compact status or metadata. At small sizes, remove or shorten nonessential text, but keep an icon, accessible label, and Tooltip when needed. Use a Split Button or Action Menu when the primary action must stay prominent.

## Validation process

- [ ] Verify that Calcite is installed correctly. If the app uses a package manager, confirm that `@esri/calcite-components` is listed in the project's dependency file, that the lockfile resolves the intended version, and that the package installs and the app builds. In a CDN app, confirm that the script tag loads the intended Calcite version.
- [ ] Verify the chosen loading method registers the components used by the app. Confirm Calcite styles load and required assets, such as icons, can be fetched in the target environment. Check the browser console and network panel for missing modules, styles, or assets.
- [ ] Run the app using its normal development or production setup. Confirm each changed Calcite component renders after hydration and that its labels, content, and expected initial state are visible.
- [ ] Complete the user workflow affected by the change. Activate controls with a pointer and keyboard, then verify the expected state change, emitted event, navigation, or submitted value. For forms, check required fields, validation messages, and submitted values when relevant.
- [ ] Check keyboard access and visible focus for changed controls. Confirm controls have accessible names, focus follows the intended order, and status or selection is not communicated by color alone.
- [ ] Compare each changed component's properties, events, slots, and supported styles with its Calcite component reference. Confirm styling uses documented design tokens or CSS variables rather than selectors into component internals. Visually check that the theme applies to the whole app, including small details such as scrollbars. Confirm that the app still uses Calcite's [Avenir Next font](https://developers.arcgis.com/calcite-design-system/foundations/typography/) unless the user requested a different font.
