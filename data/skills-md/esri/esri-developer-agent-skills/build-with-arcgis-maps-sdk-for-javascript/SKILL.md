---
name: build-with-arcgis-maps-sdk-for-javascript
license: Apache-2.0
description: "ArcGIS Maps SDK for JavaScript (@arcgis/core, @arcgis/*-components, @arcgis/create) skill for frontend application development, and its public documentation. Use when building, designing, configuring, debugging, upgrading, or explaining an app that uses the SDK - including Core API modules, web components/custom elements, widgets, maps, scenes, link charts, layers, graphics, popups, Arcade, geometry operators, queries/SQL, utility network, CIMSymbols, authentication, routing, editing, guides, tutorials, samples, references, release notes, or  app templates."
---

# Build with the ArcGIS Maps SDK for JavaScript

Use the ArcGIS Maps SDK for JavaScript when users are building web-based mapping, visualization, editing, data collection, or spatial analysis applications.

The SDK is based on a Web GIS approach where applications are built with reusable, preconfigured resources such as web maps, web scenes, and layers authored in ArcGIS Pro, Map Viewer, or Scene Viewer.
The SDK provides web components and APIs to view and interact with an item, which holds the metadata and settings that define its content.
Prefer loading a configured item rather than constructing them entirely from scratch through imperative code.

The core API (`@arcgis/core`) provides maps, web maps (2D), web scenes (3D), link charts (knowledge graphs), layers, visualization, authentication, identity management, and client-side analysis through its classes, methods, properties, events, and types.

The SDK's component are web components for declarative use in any frontend:
Map Components (`@arcgis/map-components`), AI Components (`@arcgis/ai-components`), Charts Components (`@arcgis/charts-components`), Coding Components (`@arcgis/coding-components`), Common Components (`@arcgis/common-components`), and Embeddable Components (`@arcgis/embeddable-components`).

The component packages build on Calcite Design System (`@esri/calcite-components`) for consistent, responsive, and accessible UI. For frontend design and layout, also read the `build-with-calcite-design-system` skill.

## Application requirements

If the application's development requirements are unclear, use the `gather-arcgis-application-requirements` skill to review project context and clarify consequential unknowns before proceeding. Then apply this skill's technology-specific guidance, reusing requirements already clear from the request or project.

## ArcGIS account requirements

Developers must have one of the following ArcGIS accounts to create applications: ArcGIS Location Platform (free), or ArcGIS Online or ArcGIS Enterprise with a Creator, Professional, or Professional Plus user type. The account's user type, role, and privileges provide access to different resources and operations.

## Authentication

DO NOT SKIP: Refer to the `follow-arcgis-authentication-patterns` skill for ArcGIS authentication requirements, including the appropriate type of authentication for different audiences, use cases, and types of application. If the skill is not available, search the project for any existing authentication patterns, and if none are found, query the Esri MCP server for developer documentation for authentication best practices.

## Installation and setup

### Existing applications

Read the project source code before providing implementation guidance based on it. For a standalone question about a Core API module, a component, or which package provides it, consult the documentation first, and inspect the app only if the context changes the answer.

Check these details before giving app-specific guidance:

- **App type** — For a package-managed app, check the lockfile. For a CDN app, check the `js.arcgis.com` script URL; it has no package manager.
- **Framework and language** — Check the config files and source extensions to identify the framework, build tool, and whether the app uses JavaScript or TypeScript.
- **SDK version** — Check `package.json` or the CDN script URL. Do not assume a version; API availability depends on it.
- **Platform** — Identify ArcGIS Online, Enterprise, or Location Platform from the account and authentication settings. API key authentication is available for Location Platform, Online, and Enterprise 11.4 or later, so an API key alone does not identify the platform.
- **Portal** — Check `esriConfig.portalUrl` and each item's `portalItem.portal.url`; an item can use a different portal. For Enterprise, include the configured web adaptor or context path, not just the host.
- **SDK usage** — Check for `@arcgis/core` modules and types, and `@arcgis/*-components` packages and `arcgis-*` elements.
- **Global setup** — Check `esriConfig` for `applicationName`, `portalUrl`, authentication, `request` settings, and relevant `RequestOptions`. Check the root `<html lang>` and Core API `intl.setLocale()` for locale.
- **Local assets** — For disconnected apps, check the Core API's `esriConfig.assetsPath` and the component asset path passed to each package's `setAssetPath()`.

Use this to avoid giving CDN instructions to a package-managed app, one framework's patterns to another, or guidance for a newer SDK version to an app that uses an older version.

To update an existing app, use the matching guide — [Get started](https://developers.arcgis.com/javascript/latest/get-started/), [Vite](https://developers.arcgis.com/javascript/latest/vite/), [React](https://developers.arcgis.com/javascript/latest/react/), [Angular](https://developers.arcgis.com/javascript/latest/angular/), or [TypeScript](https://developers.arcgis.com/javascript/latest/typescript/) — and review the [release notes](https://developers.arcgis.com/javascript/latest/release-notes/) for changes that affect it.

### New applications

To create a new application, review available app templates with:

```bash
npx -y @arcgis/create --help
```

Use the user’s specified template and app name, or select suitable defaults. Create the app non-interactively:

```bash
npx -y @arcgis/create --name <app-name> --template <template-name>
```

If npx isn’t available, use the relevant template from [jsapi-resources template](https://github.com/Esri/jsapi-resources/tree/main/templates).

## How to query documentation

Installing this skill individually does not configure **Esri MCP server for developer documentation** (`esri-mcp-server-for-developer-documentation`). Add that server at `https://developers-mcp.arcgis.com/mcp` using your client's MCP settings, or install the full **ArcGIS SDKs and APIs** plugin (`arcgis-sdks-and-apis-plugin`). If the MCP server is unavailable, consult the linked official Esri documentation.

Documentation can be queried using the Esri MCP server for developer documentation (`esri-mcp-server-for-developer-documentation`):

```txt
https://developers-mcp.arcgis.com/mcp
```
Use the `search_esri_developer_docs` tool to surface authoritative documentation pages with `javascript-sdk` as the `focus_area` parameter in addition to a specified `search_term`. Use the `fetch_esri_developer_docs` tool with the `page_url` parameter set to return the full content of a documentation page in Markdown format. 

Clearly indicate any recommendations and assumptions that are not grounded in the official documentation. If the MCP server is unavailable, consult official documentation URLs below.

## Documentation links

Start with the current SDK documentation page that best matches the app. Check official tutorials, samples, and [Esri/jsapi-resources](https://github.com/Esri/jsapi-resources) templates for an established pattern before inventing one, adapting what fits to the app's framework and conventions.
Follow links from the best-matching page rather than re-searching the same topic with different wording. Do not treat source filenames as public URLs.

Choose the page type that matches the question:

- **References:** exact details about classes, modules, components, properties, methods, events, slots, types, and CSS variables.
  - Use the app's exact ESM imports, `$arcgis.import()` module paths, and `arcgis-*` element names to find the right reference.
  - Reference roots include `references/core/`, `references/map-components/`, `references/coding-components/`, `references/charts-components/`, `references/ai-components/`, `references/common-components/`, and `references/embeddable-components/`.
  - Component references use `references/<component-package>/components/<arcgis-*>/`; Core API references use either `references/core/<ClassName>/` for top-level modules or `references/core/<namespace>/<...>/<ClassName>/` for namespaced modules. For example: `references/map-components/components/arcgis-map/`, `references/charts-components/components/arcgis-chart/`, `references/core/Map/`, `references/core/layers/CSVLayer/`, and `references/core/geometry/operators/alphaShapeOperator/`.
  - Follow links from a reference to related guides, tutorials, or samples when needed.
- **Samples:** complete working implementations to adapt to an existing app. Use `sample-code/<sample-name>/`.
- **Tutorials:** step-by-step workflows such as adding layers, authentication, editing, routing, and portal items. Use `tutorials/<tutorial-name>/`.
- **Guides:** concepts, framework setup, programming patterns, components, authentication, Arcade, popups, and migration.
  - Guide pages use paths directly below the documentation root, with optional nested directories; there is no `guides/` path segment. For example: `authentication/access-tokens/` resolves to `<documentation-root>/authentication/access-tokens/`.
- **Release notes:** version-specific features, deprecations, migrations, and breaking changes. Use `/release-notes/` for the current release or a versioned page such as `/v5-1/`.

Key documentation pages:

**[Components instead of widgets](https://developers.arcgis.com/javascript/latest/components-transition-plan/):** Use components for all new development. Core API widgets are deprecated as of v5.0. Read the [migration guide](https://developers.arcgis.com/javascript/latest/migrating-to-components/) when you update an app that uses widgets.
**[Programming patterns](https://developers.arcgis.com/javascript/latest/programming-patterns/):** Use this guide for common component and Core API patterns. Read it for attributes and properties, HTML, Map and Scene setup, component visibility, portal items, multiple portals, localization, and widget view models.
**[Authentication](https://developers.arcgis.com/javascript/latest/authentication/access-tokens/):** Use this guide to choose user, app, or API key authentication. Then read [secure resources](https://developers.arcgis.com/javascript/latest/secure-resources/), the [user authentication tutorial](https://developers.arcgis.com/javascript/latest/tutorials/implement-user-authentication/), the [Core API OAuth sample](https://developers.arcgis.com/javascript/latest/sample-code/identity-oauth-basic/), the [component OAuth sample](https://developers.arcgis.com/javascript/latest/sample-code/identity-oauth-component/), and the [IdentityManager](https://developers.arcgis.com/javascript/latest/references/core/identity/IdentityManager/) and [OAuthInfo](https://developers.arcgis.com/javascript/latest/references/core/identity/OAuthInfo/) references.
**[Async work and resources](https://developers.arcgis.com/javascript/latest/async-cancellation-with-abortcontroller/):** Pass an `AbortSignal`, handle `AbortError`, and cancel old work before starting new work. For React, follow the [React guidance](https://developers.arcgis.com/javascript/latest/react/).
**[Queries and SQL](https://developers.arcgis.com/javascript/latest/query-filter/):** Read this guide before querying or filtering, especially to choose between server-side and client-side. Build where clauses with `@arcgis/core/core/sql.js` rather than string concatenation, and note that `createQuery()` returns the layer's `definitionExpression` as `where`.
**[Geometry operators](https://developers.arcgis.com/javascript/latest/spatial-analysis/intro-geometry-operators/):** Use geometry operators for spatial calculations, not for getting or filtering features.
**Navigation and selection:** Use [arcgis-map.goTo()](https://developers.arcgis.com/javascript/latest/references/map-components/components/arcgis-map/#goTo) and [arcgis-scene.goTo()](https://developers.arcgis.com/javascript/latest/references/map-components/components/arcgis-scene/#goTo) for component-based navigation. Use [MapView](https://developers.arcgis.com/javascript/latest/references/core/views/MapView/) and [SceneView](https://developers.arcgis.com/javascript/latest/references/core/views/SceneView/) when working directly with views. For canceling or interrupting navigation, refer to [Handling interrupted view navigation](https://developers.arcgis.com/javascript/latest/async-cancellation-with-abortcontroller/#handling-interrupted-view-navigation). Use the [LayerView](https://developers.arcgis.com/javascript/latest/references/core/views/layers/LayerView/) reference for querying and highlighting visible features.
**[Calcite and application UI](https://developers.arcgis.com/calcite-design-system/):** Use Calcite components, foundations, and accessibility guidance. Read the [UI placement guide](https://developers.arcgis.com/javascript/latest/building-your-ui/) for map and scene slots. Read the [application layouts guide](https://developers.arcgis.com/javascript/latest/creating-app-layouts/) for shells, panels, and navigation.
**[Accessibility](https://developers.arcgis.com/javascript/latest/accessibility/):** Check keyboard use, focus, assistive technology, reduced motion, color contrast, and language.
**[Localization](https://developers.arcgis.com/javascript/latest/localization/):** Set the app locale and support translated strings, right-to-left text, and locale-aware dates, times, and numbers. Use the [intl reference](https://developers.arcgis.com/javascript/latest/references/core/intl/) for locale APIs.

For older versions of the SDK, visit the [archive page](https://developers.arcgis.com/javascript/latest/downloads-and-previous-versions/) for links.

## Patterns and guidelines

Use the Core API and components according to the application's delivery model.

After identifying the app's delivery model, read exactly one matching reference: [package-managed apps](./references/package-managed.md) or [CDN apps](./references/cdn.md). Do not load both for a single-model task.

When the task involves reusing a layer across components, read [sharing data across components](./references/sharing-data.md). When it involves configuration saved in web maps or layer items, read [configuration saved with layers and items](./references/saved-layer-configuration.md).

Import classes, functions, and types directly from their modules, using `import type` for type-only imports and the exported types rather than the deprecated `__esri` types.

Avoid generating unnecessarily complex `@arcgis/core` implementations when a component package provides an equivalent solution.

Match generated code to the user's frontend library and follow that library's conventions.

## Validation process

Label claims by how certain they are:

- **Confirmed:** verified by local types, JSDoc, package metadata, or SDK documentation.
- **Recommendation:** an approach selected for the application's context and goal.
- **Assumption:** a detail not established by the code or documentation.

Before coding, inspect the items and layers an existing app loads. After coding, run the app, test its main workflows, and fix what fails. Repeat the relevant checks after changes.

- For package-managed apps, run the relevant build and type checks, then start the development server and confirm the app loads from it.
- For CDN apps, compare API and type usage against the declarations in the matching published SDK package on npmjs.com, and confirm its version matches the CDN SDK version.
- Use a browser tool such as Chrome DevTools, Playwright, or Puppeteer to open the running app. Wait for the UI, map, layers, and data to render; a running server alone does not confirm the app works.
- Read item and layer details from the loaded app rather than inferring them from source, item titles, or layer titles. A loaded layer exposes `fields`, `objectIdField`, `displayField`, `definitionExpression`, `charts`, `attributeTableTemplate`, `popupTemplate`, and `portalItem.access`. Some populate lazily, so read after the UI settles: `attributeTableTemplate` can be null immediately after `load()` and present once a table component has rendered.
- Secure items need no extra setup, because requests run inside the app and carry its credential — but only if the browser session has signed in, and a fresh automation profile has not. Use a profile the user has already signed into, check `esriId.findCredential("<portalUrl>/sharing")` per portal before reading, and expect `access` to still govern what that account can see.
- Determine the display field rather than assuming one. `displayField` is frequently empty on services published from shapefiles or CSVs, which turns a `displayField || objectIdField` fallback into popups that show an object id. Prefer, in order: `popupTemplate.title`, the first `attributeTableTemplate` column, a field used in `labelingInfo`, then `displayField`, then `objectIdField`. Service metadata such as `fieldValueType` is visible only in raw service JSON, not on a loaded layer. Query by a field's `name` and display its `alias`; never query by alias.
- Dev-server tooling can produce console errors that are not app defects, such as failed dynamic imports after a dependency graph change. Confirm an error reproduces in a production build before treating it as a code defect. Check failed network requests when they may explain missing data.
- Visually inspect the result at relevant screen sizes, against Calcite guidance and the SDK's design documentation, including layout, readability, and accessibility.
- Interact with the app and test representative user flows. Check that controls change the expected state and that displayed data matches the underlying data, including relevant SDK features such as effects and queries.
- Note any checks you could not run. If item or layer details could not be read, ask for them rather than inferring a schema, and do not substitute a different item to make progress.
