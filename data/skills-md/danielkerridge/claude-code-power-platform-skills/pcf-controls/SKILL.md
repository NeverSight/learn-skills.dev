---
name: pcf-controls
description: >
  Use when building, deploying, or using PowerApps Component Framework (PCF) controls.
  Covers field controls and dataset controls, React virtual controls, control lifecycle,
  manifest configuration, solution packaging, and deployment. Triggers on: "pcf",
  "custom control", "component framework", "dataset control", "virtual control",
  "pac pcf", "pcf init", "pcf push", "ControlManifest", "StandardControl",
  "ReactControl", "updateView", "getOutputs".
license: MIT
compatibility: "Power Apps Component Framework, Dataverse"
metadata:
  author: custom
  version: "1.0.0"
  platform: "Microsoft Power Platform / Dataverse"
---

# PCF Controls Skill

You are an expert at building PowerApps Component Framework (PCF) controls for Microsoft Power Platform. You know the full PCF development lifecycle — from scaffolding with `pac pcf init`, through TypeScript implementation, test harness debugging, solution packaging, and deployment to Dataverse environments. You build both **field controls** (bound to a single column) and **dataset controls** (bound to views/subgrids), and you leverage **React virtual controls** for complex UIs that need the full React component model with Fluent UI integration.

## CRITICAL RULES

1. **Use `pac pcf init` to scaffold — never create from scratch.** The CLI generates the correct project structure, tsconfig, manifest, and build pipeline. Hand-creating these files leads to subtle build errors and missing type definitions.

2. **TypeScript is required (not plain JS).** PCF controls must be authored in TypeScript. The framework's type system (`ComponentFramework.StandardControl<IInputs, IOutputs>`) provides compile-time safety for the context object, parameters, and outputs. Never use plain JavaScript.

3. **React virtual controls for complex UIs (`--framework react`).** When your control needs rich interactivity (lists, drag-drop, modals, complex state), use virtual controls. These return React elements from `updateView()` instead of manipulating the DOM directly. The platform hosts the React tree — do not install or bundle your own React. Use `--framework react` during `pac pcf init`.

4. **Field controls vs Dataset controls — know the difference.**
   - **Field controls** bind to a single column value. Use `--template field`. The control reads/writes one value via `context.parameters.<propertyName>` and notifies the host via `notifyOutputChanged()` + `getOutputs()`.
   - **Dataset controls** bind to a view or subgrid. Use `--template dataset`. The control receives a full record set via `context.parameters.dataSet` with sorting, filtering, and paging APIs. Dataset controls render collections of records (grids, calendars, kanban boards, galleries).

5. **Always test in harness first (`npm start watch`).** The test harness provides a sandboxed environment with mock data, parameter configuration, and hot reload. Never deploy untested controls to an environment. The harness catches most manifest misconfigurations and runtime errors before they reach production.

6. **Solution packaging required for production deployment.** While `pac pcf push` is convenient for development (pushes directly to a dev environment), production deployment requires proper solution packaging: `pac solution init` → `pac solution add-reference` → `msbuild /t:build /restore` → `pac solution import`. This produces a managed or unmanaged solution .zip that can be transported across environments.

7. **Never modify auto-generated files (`generated/*.ts`).** The `ManifestTypes.d.ts` and other files under `generated/` are regenerated on every build from the manifest XML. Any manual edits will be overwritten. If you need to change types, update `ControlManifest.Input.xml` and rebuild.

8. **Use `context.webAPI` for Dataverse operations within controls.** For CRUD operations inside a control, use the provided `context.webAPI.createRecord()`, `retrieveMultipleRecords()`, `updateRecord()`, `deleteRecord()`. Do not import or use the Xrm global object — it is not guaranteed to be available and is not part of the supported PCF API surface.

## Quick Reference — PAC PCF Commands

| Command | Purpose |
|---|---|
| `pac pcf init --namespace NS --name Name --template field` | Scaffold a standard field control |
| `pac pcf init --namespace NS --name Name --template dataset` | Scaffold a standard dataset control |
| `pac pcf init --namespace NS --name Name --template field --framework react` | Scaffold a React virtual field control |
| `pac pcf init --namespace NS --name Name --template dataset --framework react` | Scaffold a React virtual dataset control |
| `npm install` | Install dependencies after scaffolding |
| `npm run build` | Build the control (compiles TS, bundles output) |
| `npm start watch` | Launch test harness with hot reload |
| `pac pcf push --publisher-prefix pic` | Push control to connected dev environment |
| `pac solution init --publisher-name PIC --publisher-prefix pic` | Initialize a solution project for packaging |
| `pac solution add-reference --path ../MyControl` | Add a PCF control project to the solution |
| `msbuild /t:build /restore` | Build the solution .zip |
| `pac solution import --path bin/Debug/Solution.zip` | Import solution to connected environment |
| `pac pcf version --strategy manifest` | Bump version based on manifest |

## Decision Guide — PCF vs OOB vs Web Resources

| Scenario | Recommendation | Rationale |
|---|---|---|
| Need a slider, toggle, or rating input on a form | **PCF field control** | Bound to column, participates in form save, type-safe |
| Need a custom grid/calendar/kanban for a view | **PCF dataset control** | Gets full dataset API with sort/filter/paging |
| Need a dashboard with charts and custom HTML | **Web resource** | Not column-bound, standalone HTML page |
| Need to change field visibility/requirement on form events | **Form script (web resource JS)** | PCF controls cannot modify other form fields |
| Need a button on the command bar | **Command bar customization / Ribbon** | PCF controls live inside field or subgrid areas, not command bar |
| Need complex interactive UI (drag-drop, modals, trees) | **PCF React virtual control** | Full React component model, Fluent UI, platform-managed React |
| Simple formatting change (bold, color, icon) | **OOB column formatting (Power FX)** | No code deployment needed, column formatting rules suffice |
| Need to override the entire form experience | **Custom page / Code App** | PCF controls are per-field or per-subgrid, not full-page |
| Need offline support in mobile app | **PCF field control** (with caveats) | PCF supports offline if control does not depend on webAPI calls |
| Need to call external APIs from UI | **PCF control with `context.webAPI` or fetch** | Controls can make HTTP calls; use environment variables for URLs |

## Resource Files

| File | Contents |
|---|---|
| `resources/pcf-lifecycle.md` | Control lifecycle (`init` → `updateView` → `getOutputs` → `destroy`), StandardControl and ReactControl interfaces, context object deep dive, dataset APIs, scaffolding and debugging |
| `resources/component-patterns.md` | 11 common PCF control patterns (slider, toggle, rating, color picker, rich text, map, kanban, calendar, gallery, chart, file upload) with implementation guidance and manifest config |
| `resources/manifest-reference.md` | Complete `ControlManifest.Input.xml` schema reference, property types, data-set elements, resources, feature-usage, solution packaging workflow, and full XML examples |
