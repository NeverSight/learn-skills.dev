---
name: adp-controller-extension
description: Use when the user wants to make UI changes to a SAP Fiori adaptation project via the adaptation editor — adding buttons, fields, columns, or sections, changing labels or properties, hiding controls, or extending controllers with custom logic. Trigger on phrases like 'add a button', 'hide a field', 'add a column', 'customize the toolbar', or 'extend the controller' when working in an adaptation project context.
metadata:
  author: sap-fiori-tools
  version: "0.0.1"
---

# SAP Fiori ADP Controller Extension

Drive Runtime Authoring (RTA) in the SAP Fiori adaptation editor through the **`run_rta_workflow_step`** MCP tool exposed by `fiori-mcp-server`. The tool handles browser automation server-side; this skill orchestrates the step sequence and the AI decisions between steps.

> **Tool boundary.** `run_rta_workflow_step` is a **skill-internal** dispatcher. Don't call it ad-hoc — the value of this skill is in the AI decision points between steps (control selection, action selection, payload preparation). Calling out of order will fail with a descriptive error.

## Prerequisites

- **`@sap-ux/fiori-mcp-server` running as an MCP server.** It provides `run_rta_workflow_step` and the other `fiori-mcp` tools this skill drives without it none of the tool calls below resolve. See the package's install/setup instructions: https://www.npmjs.com/package/@sap-ux/fiori-mcp-server
- Adaptation editor URL (user-provided)
- A Chromium-based browser the server can launch. Resolution order:
  1. `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` env var (absolute path to a Chromium binary)
  2. `PLAYWRIGHT_BROWSER_CHANNEL` env var (`chrome`, `msedge`, `chrome-beta`, etc.)
  3. System Google Chrome (default channel)
  4. Playwright-managed Chromium (auto-fallback if 1–3 fail)

### Chromium fallback (no system Chrome)

If no system Chrome is found and no env override is set, the server falls back to Playwright's bundled Chromium. Install it once if needed:

```bash
npx playwright install chromium
```

The first install downloads ~120 MB. Subsequent runs reuse the cache. See the Error Handling table for the detection sequence on a `start` failure.

## Tool Contract

A single tool, dispatched by the `step` argument. `site` is the editor URL from `open_adaptation_editor` — pass it on every step. The tool keeps the browser session server-side, keyed per project (that is why `start`/`restart`/`get_odata_metadata` require `appPath`); each other step locates its page by `site`.

| step | site | frameId | payload | returns |
|------|------|---------|---------|---------|
| `start` | required | required (`"preview"`) | `{ agentName? }` | `{ site, frameId, rtaStarted: true }` |
| `describe_ui` | required | carry forward | `{ rootElementId? }` | `{ uiTree: UiElementNode }` |
| `execute_page_action` | required | carry forward | `{ actionName, elementId?, actionParameters? }` | `{ isSuccess: boolean, result? }` |
| `get_overlays` | required | carry forward | — | `{ overlays: Overlay[], actionsCatalog: { [actionId]: Action } }` |
| `get_context` | required | carry forward | `{ controlId, actionId }` | `{ context }` |
| `call_action` | required | carry forward | `{ controlId, actionId, actionPayload }` | `{ success: boolean }` |
| `save` | required | carry forward | — | `{ saved: boolean }` |
| `cleanup` | required | carry forward | `{ reason? }` | `{ cleaned: boolean }` |
| `restart` | required | carry forward | — | `{ site, frameId, rtaStarted: true }` |
| `stop` | required | carry forward | — | `{ stopped: true }` |

`Overlay` = `{ overlayId, controlId, label, controlType, parentElementId, parentAggregationName, index?, actionIds: string[] }` — `index` is the 0-based position within `parentAggregationName` and is omitted when the parent/aggregation can't be resolved or the aggregation is single-cardinality. `actionIds` lists the RTA actions available on this overlay; rich metadata for each id is in the top-level `actionsCatalog`.
`Action` = `{ id, label, description?, parameters: [{ name, type, required?, description? }] }` — keyed by `actionId` in `actionsCatalog`. The catalog is **deduplicated across all overlays** in a single `get_overlays` response, so an id appears once even when many overlays expose it.
`UiElementNode` = `{ id, type, label?, children?: UiElementNode[], truncated?, childCount? }` — one node in the UI element tree returned by `describe_ui`. `id` is the UI5 control id; pass it as `elementId` in `execute_page_action`. An unscoped `describe_ui` returns a **shallow overview** (top levels only); a node whose children were omitted is marked `truncated: true` with `childCount`. To see inside it, call `describe_ui` again with `rootElementId` set to that node's `id` — a scoped call returns that subtree at full depth.

For the standard adaptation editor preview iframe, pass `frameId: "preview"` in the `start` step.

> **When to reach for the navigation steps.** The RTA steps (`get_overlays` → … → `save`) assume the page is already showing the control to edit. In Fiori Elements apps that often isn't true on first load — a List Report shows no rows until "Go" is pressed; an Object Page is only reachable after picking a row. Use `describe_ui` / `execute_page_action` to drive these pre-RTA navigations from the skill instead of asking the user to click manually. See **Step 2 — Navigate the app** below.

## RTA Actions

`CTX_ADDXML` (fragment insert) and `CTX_EXTEND_CONTROLLER` (controller attach). Field schemas and disambiguation table: **[references/rta-actions.md](references/rta-actions.md)**.

## Confidence & HITL Gating

Three steps require AI judgment: control selection (Step 4), action selection (Step 5), and payload preparation (Step 8). Full rubric, per-decision thresholds, and gating rules: **[references/hitl-gating.md](references/hitl-gating.md)**.

## Workflow

> **One session per handover (hard rule).** Call `start` (Step 1) **exactly once**, `restart` (Step 13) **at most once** (only after all fragment/controller files have been written to disk), and `stop` (Step 14) **exactly once** at the very end, no matter how many changes are requested. Parse the full change list upfront, then run **all** changes as iterations of Steps 3–9 *inside* the single session, and `save` (Step 11) **once** at the end. **Never re-enter Step 1 (`start`) per change** — a fresh `start`/`stop` per change is the single most common misuse of this skill. When the handover prompt hands you a list of changes, that entire list is **one** session, not one session per bullet.

### Step 1 — Start RTA

Call `run_rta_workflow_step` with `step: "start"`, `site` (the editor URL from `open_adaptation_editor`), `frameId: "preview"`, and `appPath` (the adaptation project root — the same path passed to `open_adaptation_editor`) — all as **top-level parameters**, not inside `payload`. `appPath` is **required**: it identifies the project so an authenticated Cloud Foundry session is reused per project (and ABAP projects skip session handling). Optionally pass `payload: { agentName: "..." }` to have the status reporter identify the driving agent. Verify `rtaStarted: true`. Pass `site` and `frameId` to every subsequent step. On `false`, wait 3 s and retry once. If `rtaStarted: false` with `needsUserAction: "backend_login_required"`, the editor URL served a login page (CF XSUAA) — surface the message to the user to complete login once in the opened browser, then retry `start`.

### Step 2 — Navigate the app to the editing target

**When to skip Step 2.** If `get_overlays` already returns the control the user named (the page is on the right view from the start), skip to Step 3. Navigation is for reaching the target, not for editing.

The RTA flow assumes the control to edit is already on screen. For Fiori Elements apps this often isn't true on first load — a List Report shows no rows until the Filter Bar search is triggered; an Object Page is only reachable after picking a row. Drive that navigation through the Unified Frontend Actions (UFA) — the generic UI-introspection/interaction steps `describe_ui` and `execute_page_action` — before reaching for `get_overlays`.

**Navigation flow (UFA):**

1. Call `step: "describe_ui"` to get the current UI element tree. Each node has `id` (UI5 control id), `type`, `label`, and `children`. The unscoped call is a **shallow overview**: a node marked `truncated: true` (with `childCount`) has hidden children — if the control you need is inside one, call `describe_ui` again with `payload: { rootElementId: "<that node's id>" }` to expand just that subtree at full depth, rather than re-describing the whole page.
2. Pick the element whose `type`/`label` matches the interaction the user's intent needs — the generic rule is "read the tree, choose the control that advances toward the target." (On Fiori Elements that is typically a search/"Go" button to load data, then a row to open its Object Page, then a section link — but treat these as examples, not a fixed script; match on what the tree actually shows.)
3. Call `step: "execute_page_action"` with `payload: { actionName: "press", elementId: "<id>" }`.
4. Call `describe_ui` again to confirm the navigation succeeded (new page/section is now on screen).
5. Loop until the editing target is on screen, or the UI has not changed after a press (then ask the user).

**Heuristics for common Fiori Elements navigations (examples, not requirements).** List Report → Object Page usually means: load data first (press the search/"Go" button), then press a row's navigation cell — in the standard responsive table these cell ids often carry an `-imgNav` suffix, and a successful row press changes `window.location.hash` to the entity key. These are hints to speed up recognition in the tree, not mandatory steps; if the tree looks different, follow the tree.

If `execute_page_action` returns `isSuccess: false`, surface the failure to the user and ask how to proceed.

**When the UFA approach fails.** If `describe_ui` cannot identify a suitable element (the tree is too large to parse or no obvious control matches the navigation goal), surface that to the user and ask them to navigate manually to the target view, then re-run Step 2.

### Step 3 — Get overlays

Call `step: "get_overlays"`. Returns the editable controls on the page.

### Step 4 — Select target control (AI decision)

Match the user's instruction against the overlays, examples:
- "the title" → controls with `Title` or `Header` in `controlType`
- "the table" → `sap.ui.table.Table` or `sap.m.Table`
- "button X" → `sap.m.Button` with matching label
- "toolbar" → `sap.m.Toolbar` or `sap.m.OverflowToolbar`

**Template handling**

In RTA, changes are always made on template clones and mapped to the template internally. When you want to change a template of a binding, pick an arbitrary instance and pass it to further steps.

**Data-loaded gate (hard stop for data-bound containers).**

When the target is a `SmartTable`, `SmartList`, `sap.m.Table`, `sap.ui.table.Table`, `SmartChart`, or any control whose intent involves binding to rows/items, you **MUST** confirm row data is loaded before reading the overlay's `actionIds`. Structural overlays (columns, headers, toolbars) are **not** evidence of loaded data — they appear before any rows exist.

Evidence required (one of):
- The user explicitly states data is loaded.
- You observe row-level overlays in `get_overlays` (e.g. `sap.m.ColumnListItem`, `sap.ui.table.Row`, or overlays whose `controlId` contains a row index).

If neither is present, **do not proceed to action selection.** Resolution order:

1. **Use UFA navigation.** Call `describe_ui` and press whatever control in the tree triggers data loading for this view — on a Fiori Elements List Report that is typically the search/"Go" button, but choose based on what the tree shows. Press it via `execute_page_action` with `actionName: "press"` and the element's `id`, then re-run `get_overlays` and re-check the gate.
2. **Fall back to asking** if no obvious trigger is visible in the UFA tree. Surface the situation to the user and ask them to trigger data loading manually.

**The gate is unconditional.** It applies even when the change feels purely structural (adding a column, reordering, renaming, changing a header label). Do not reason about whether data "matters" for this particular change — if the target is a data-bound container and row-level overlays are absent, stop. The `actionIds` exposed by an overlay can differ based on data state, and a structurally-correct change against the wrong action variant is exactly the silent failure this skill is built to prevent. "This is just a structural edit, so the gate doesn't apply" is not a valid exception — it is the rationalization the gate exists to block.

Store the chosen `controlId` and its confidence for the final summary.

### Step 5 — Select action (AI decision)

The chosen overlay carries its available action ids in `actionIds`; the rich per-action metadata (label, description, parameters) for each id lives in the top-level `actionsCatalog` returned alongside `get_overlays`. There is no separate `get_actions` step — read both from the Step 3 response.

Pick an action by `id` from the **[RTA Actions](references/rta-actions.md)** — and only if that `id` is also present in the chosen overlay's `actionIds`. **Never invent an action id.** If the user's intent needs an action that isn't in the reference, surface the overlay's available actions and ask the user rather than picking.

Map user intent using the *Disambiguation by intent* table in the [RTA Actions](references/rta-actions.md). If the verb doesn't map cleanly (e.g. "tweak the toolbar"), confidence is low — list the actions from `actionIds` (with their labels from `actionsCatalog`) and ask.

**Confidence gating** (thresholds from [references/hitl-gating.md](references/hitl-gating.md#per-decision-thresholds)):
- **Schema-inspection prerequisite for High band:** Before assigning ≥ 0.85, you must have read the candidate's `parameters` schema (from `actionsCatalog[actionId]`) and confirmed it matches the kind of operation the user described. If you have not inspected the schema, cap confidence at **0.65** (medium → announce, do not run silently).
- **Same-verb penalty:** If two or more candidates share a verb token in their id or label (e.g. multiple `ADD_*` actions in `actionIds`), subtract **0.20** from the top candidate's confidence unless the schemas clearly distinguish them.
- **High-band requirement:** When proceeding silently, record an `Alternatives considered:` line stating which other actions were rejected and the schema/semantic reason. If you can't articulate the discriminator, the choice isn't High.
- If the verb doesn't map cleanly (e.g. "tweak the toolbar"), confidence is low — list the actions from `actionIds` (with their labels from `actionsCatalog`) and ask.

Store `actionId`, the action's `parameters` schema, and the confidence value.

### Step 6 — Get element context

Call `step: "get_context"`, payload `{ controlId, actionId }`. The response is rich and shapes the rest of the workflow:

- `elementType` — the chosen control's UI5 class.
- `parentAggregationName` — the aggregation slot this control occupies in its parent.
- `actionParameters` — the action's parameter schema (same shape as `actionsCatalog[actionId].parameters`).
- `defaultChildAggregation` (optional) — `{ name, controlType, content: [{ controlId }] }` for the control's default aggregation, listing the current direct children by id. Useful for "insert near child X" intents and as a quick sanity check that the control has the children you expect.
- `aggregationsByClass[]` — per-class breakdown of every aggregation defined on this control's inheritance chain, with `definedIn` + `libraryName`, plus `aggregations[].name`, `controlType`, `contentLength`. **Only populated when the action's parameters reference `aggregation` or `selectedElements`** (the server elides it for actions like rename/remove to keep LLM context small). If you need aggregation info for an action that doesn't take one of those params, the data isn't there — read from `defaultChildAggregation` or re-derive from the control class.
- `availableModels` — the binding environment in effect at this control, keyed by model name. Each entry has `modelName`, `modelClass`, `defaultBindingMode`, `contextPath`, and **`contextEntityType`** (resolved via OData V4 async meta model or V2 sync meta model). Non-OData models with no active binding context on this element are filtered out — they carry no payload-relevant information.
- `actionSpecificContext` — whatever the action's own `getContext` hook returns (action-dependent).

> **Grounding gate (hard rule).** `get_context` (this step) is **not optional** whenever the change involves a data binding, an entity, or any property/path. You MUST call it and read its output before Step 8. **Every binding path, entity type, entity set, and property name you emit in a payload or in generated fragment/controller content MUST come from `get_context` (`contextEntityType`, `contextPath`, `availableModels`) or from `read_odata_metadata_adp` (Step 7) — never from the control's id, the user's phrasing, or a plausible-looking guess.** If neither tool gives you the path you need, **stop and run Step 7**; if Step 7 still doesn't yield it, **ask the user** (Step 8 required-field rule). Inventing a binding is the single most common cause of "the button renders but the search/data never triggers" — a change that reports `success: true` yet does nothing. Never skip the tools because a binding "looks obvious."

#### Use `availableModels` before reaching for OData metadata

`availableModels[<name>].contextEntityType` already tells you which entity the control is bound to and `contextPath` gives you the OData path. For the common "what is this bound to / what's the entity type here" question that Step 7 (OData metadata) used to answer, **inspect `availableModels` first** — it short-circuits the metadata call entirely. Only fall through to `read_odata_metadata_adp` (Step 7) when you need information `availableModels` can't give you: property-level details, navigation paths, annotation-driven hints, alternative entity sets, or the full EDMX of an unbound area.

#### Mandatory aggregation/member verification (hard rule — no exceptions)

`get_context` tells you which aggregations exist (`aggregationsByClass[]`, `parentAggregationName`, `defaultChildAggregation`) and which control defines each one (`definedIn` + `libraryName`), but **not what they're for**. Before writing any fragment XML you MUST call `lookup_ui5_documentation` to verify the aggregation's accepted type and cardinality against the actual deployed UI5 version.

**Never skip this call.** Type contracts change between UI5 releases — the only safe source is the tool output.

Call `lookup_ui5_documentation` for every aggregation you plan to use:

```
lookup_ui5_documentation({
  lookupType: "aggregation",   // or "property" or "event"
  library: "<libraryName from aggregationsByClass>",
  control: "<control FQ name — leaf control is fine; the tool walks the chain>",
  member: "<aggregation / property / event name>",
  appPath: "<adaptation project root>"   // used to discover ui5.yaml version
})
```

Returns `description`, `type`, `since`, `definedIn`, `inherited`, plus lookup-type-specific fields (`cardinality` for aggregations; `defaultValue`/`group`/`bindable` for properties; `parameters` for events), and a `source` block.

**Do not write any fragment XML until you have called this tool for every aggregation you plan to use** — `targetAggregation`, every named child aggregation inside the fragment, AND the default aggregation of every non-trivial control you introduce inside the fragment (e.g. a `Dialog`, `SimpleForm`, `VBox`). The scope is all controls in the fragment, not just the outermost placement slot. Three hard rules on the output:

- **Missing:** an aggregation not returned does not exist; unknown aggregations are silently discarded while `call_action` still reports `success: true`.
- **Cardinality:** if the result is `0..1` but you need multiple instances (e.g. per-row content), this aggregation cannot serve that purpose — find the correct multi-instance aggregation on the parent container.
- **No existing children:** if the aggregation has no existing children in `get_overlays`, do not use it as a placement target — it may render hidden or inactive at runtime.

If the accepted type doesn't match, check for a wrapper before seeking an alternative placement. Before using a control from a library not in `aggregationsByClass[].libraryName` for this session, call the tool against one of its aggregations — a tool error indicating all fetches failed means the library is absent from this runtime.

#### XML namespace prefix rule (hard rule)

The `library` field in the tool response is the **exact string to use as the XML namespace** in the fragment. Never derive the namespace from the control name or from memory — sub-packages look similar to their parent library root but are distinct strings. Always read it from `library` in the tool output.

### Step 7 — Read OData metadata (conditional, only when a data binding is involved)

Run this step only if the user's intention involves binding the element to a data source **and** `availableModels` from Step 6 didn't already answer the question. For the simple "which entity is this control bound to" case, `availableModels[<name>].contextEntityType` is usually enough; reach for the EDMX only when you need richer information (property details, navigation paths, annotations, or entities outside the current binding context).

**IMPORTANT** Call `read_odata_metadata_adp` with the adaptation project path to retrieve the metadata (EDMX) of the OData services available to the application. Always use this tool — do not curl, fetch, or grep EDMX from disk. Use the returned entities, properties, navigation paths, key fields, and annotations as context to decide:

- Which entity set / entity type to bind against
- The exact property name and path (including any navigation traversal)
- Whether the property is suitable for the target control (type, nullability, length)
- Any annotation-driven formatting hints that should be applied

**Cloud Foundry (CF) projects — two-call flow.** CF adaptation projects have no ABAP backend to proxy `$metadata`, so for a CF project `read_odata_metadata_adp` returns each OData data source **with an empty `metadata` string** (it still gives you the data-source `id`, `url`, and bound model). To get the real EDMX for a CF project:

1. Call `read_odata_metadata_adp` to list the data sources and collect the `entries[].url` values (the service URIs).
2. With a live editor session already started (the `start` step of `run_rta_workflow_step` has succeeded), call `run_rta_workflow_step` with `step: "get_odata_metadata"`, `site` (top-level), `appPath` (top-level, **required** — the adaptation project root), and `payload: { uris: [...] }` passing those URIs. It fetches the real EDMX through the editor's authenticated approuter session and returns `{ entries: Array<{ url, metadata } | { url, metadataFile, sizeBytes } | { url, error }> }`:
   - `{ url, metadata }` — EDMX inline (small services); use it directly.
   - `{ url, metadataFile, sizeBytes }` — EDMX too large to inline; it was written to `<appPath>/.context/<name>-metadata.xml`. **Read that file** (e.g. with a targeted `jq`/grep for the entity you need) rather than loading the whole multi-megabyte document.
   - `{ url, error }` — the fetch failed (lost-auth login page, non-XML, or a foreign-origin URI was refused); re-run `start` if the session lapsed.

For the common "what is this control bound to" question you usually need **neither** call — `get_context`'s `availableModels[<name>].contextEntityType` (Step 6) already resolves the bound entity type through the authenticated browser's meta model, for both ABAP and CF. Reach for `get_odata_metadata` only when you need the richer EDMX (full entity sets, navigation paths, annotations, or services outside the current binding context) for a CF project. For an ABAP project, `read_odata_metadata_adp` returns the EDMX directly and no workflow step is needed — small services inline as `metadata`, large ones spilled to `<appPath>/.context/<service>-metadata.xml` and returned as `{ metadataFile, sizeBytes }`, and a service whose metadata fetch fails returned as `{ error }` (the other services are unaffected) — exactly as the CF `get_odata_metadata` step does. Read a spilled file rather than loading the whole document.

Typical triggers:

- Binding a control property to an OData field (e.g. `text="{Customer/Name}"`)
- Adding a bound text/value/description/title to a control
- Binding a table column or list item to an entity property
- Wiring a new control, fragment, or section to a backing entity set, navigation property, or function import
- A controller handler will read one or more model properties at runtime (e.g. to build a URL, compute a value, or populate a dialog)

If the change is purely structural or behavioral (static labels, visibility toggles, controller-only logic, etc.) and does not reference any backing data, skip this step.

Feed these decisions into Step 8 (payload preparation) and into the fragment XML / controller extension content generated in Step 12. If the metadata does not contain a property matching the user's request, stop and ask — do not invent a binding path.

### Step 8 — Prepare action payload (AI decision)

Build `actionPayload` from the action's `parameters` schema (Step 5), the element context (Step 6), and the user's instructions. **Use the exact field names from the [RTA Actions](references/rta-actions.md)** — `fragmentPath` (not `fragmentName`), `codeRef`, `viewId`, etc.

**For `CTX_ADDXML`:**
- `fragmentPath`: `fragments/<Name>.fragment.xml` — pick `<Name>` from the user's intent (e.g. `OrderDetailsButton`). The fragment file itself is created in Step 12.
- `targetAggregation`: from `get_context`. Always call `lookup_ui5_documentation` (see Step 6) to confirm the aggregation name exists on the control, its accepted `controlType`, and its cardinality before finalising the payload — getting this wrong inserts the fragment into the wrong slot and `call_action` will still report `success: true`.
- `index`: `0` for "at the beginning"; for "append at end" use the current child count, which is `aggregationsByClass[<class with the aggregation>].aggregations[<aggregation name>].contentLength` from the Step 6 response (fall back to `defaultChildAggregation.content.length` when the aggregation is the default and `aggregationsByClass` wasn't populated). Ask if the user said "after the X" and the position isn't determinable from context.

**For `CTX_EXTEND_CONTROLLER`:**
- `codeRef`: `coding/<Name>.js` — `<Name>` typically matches the fragment's controller name (e.g. `OrderDetailsExt`). The JS file itself is created in Step 12.
- `viewId`: the `controlId` of the current selection works; otherwise the view id from `get_context`.
- `instanceSpecific`: omit unless the user explicitly asked to scope to one instance.

General rules:
- Fill structural fields from `get_context`; fill value fields from instructions.
- **Binding provenance (hard rule):** any binding path, entity type, entity set, or property name in this payload (and in the Step 12 fragment/controller content) must trace to a specific field of the Step 6 `get_context` response or the Step 7 EDMX. If you cannot point to where a path came from, you are inventing it — stop, run Step 7, and if it still isn't there, ask. See the Grounding gate in Step 6.
- **Runtime property availability check (hard rule):** whenever a controller handler will read model properties at runtime (e.g. `getProperty`, `getObject`, or any expression binding), call `read_odata_metadata_adp` (Step 7) and derive the effective `$select` from the UI annotations on the bound entity type. Only properties provably included in that annotation-driven set may be read synchronously. Every other property — including annotation companions (`sap:unit`, `sap:text`, `sap:scale`, etc.) — must be fetched on demand with an explicit `$select`. When the handler constructs any computed output from the properties (URL, concatenated string, arithmetic), always fetch regardless of annotation membership — a silent `undefined` produces no error at `call_action` time and is only discoverable at runtime. **Dropping the property from the handler is never an acceptable alternative — if the user's intent requires it, fetch it.** The safe patterns are:
  - OData V2: `oModel.read(oContext.getPath(), { urlParameters: { "$select": "PropA,PropB" }, success: function(oData) { … } })`
  - OData V4: `oContext.requestProperty(["PropA", "PropB"]).then(function([vA, vB]) { … })`
- **Existing change awareness:** before finalising any payload or generated code, review the existing changes in the project (imported key user changes and any developer changes already in `webapp/changes/`) for related intent. When an existing change addresses something similar to the current requirement, align the new output with it — reuse the same property names, URL patterns, entity paths, and logic rather than re-deriving them independently. Silently diverging from an established pattern in the same project is a defect.
- Validate types match the schema (string vs int vs boolean — `index` is int, not string).

**Confidence gating** (thresholds from [references/hitl-gating.md](references/hitl-gating.md#per-decision-thresholds) — strictest of the three because a successful `call_action` with a wrong payload is the worst silent failure):
- Per-field confidence: use the rubric. Whole-payload confidence is the **minimum** of the per-field values.
- **Required-field rule:** see *Confidence & HITL Gating* — a required field with no derivable value caps whole-payload confidence at 0.55 (ask band).
- **High** → submit the payload silently.
- **Medium** → announce the payload: `Action <actionId> with payload <JSON> (confidence 0.7x). Continuing — interrupt to change.` Continue.
- **Low** → present the payload as a draft and ask for confirmation or corrections before calling.

Store the payload + confidence for the final summary.

### Step 9 — Execute action

Call `step: "call_action"`, payload `{ controlId, actionId, actionPayload }`. On `success: true`, continue. On error, report and offer to retry with adjusted parameters.

### Step 10 — Loop for multiple changes

If the user requested multiple changes, repeat **Steps 3–9 only** (never Steps 1–2, never a fresh `start`) once per change, all under the same `site`+`frameId`. The UI may have changed, so re-run `get_overlays` between changes — and re-run Step 2 navigation if the next target is on a different view.
A single change request can still require multiple operations and changes to be created.
If a single request implies multiple operations (e.g. "add a button that calls a function" = fragment + controller extension), execute each as a separate iteration.

Create all changes before saving.

### Step 11 — Save

Call `step: "save"`. Returns `{ saved: true }` on success.

### Step 12 — Generate fragment and controller extension content

After saving, use `adp_controller_extension` to fill in the content for any fragments and controller extensions that were created.

**Phase 1 — knowledge base.** Call with:
- `appPath`: adaptation project path
- `prompt`: describe the functionality (from user instructions)
- (do **not** pass `aiResponse`)

This returns project context, layer info, namespace rules, and existing files.

**Phase 2 — write content.** Generate controller extension and fragment XML using the Phase 1 knowledge base, then call again with:
- `appPath`: same path
- `prompt`: same prompt
- `aiResponse`: your generated code with `**Path:**` markers
- `controllerName`: the controller extension name

Format:

```
**Path:** webapp/changes/coding/MyExtension.js
```javascript
// controller extension code
```

**Path:** webapp/changes/fragments/MyFragment.fragment.xml
```xml
<!-- fragment code -->
```
```

Include XML comments inside fragments for context hints:
```xml
<!-- viewName: <from context> -->
<!-- controlType: <from context> -->
<!-- targetAggregation: <from context> -->
```

### Step 13 — Validate

> **Validate before stopping (hard rule).** After generating files (Step 12), you MUST call `restart` before `stop`. Fragment and controller extension controls only appear in `get_overlays` after the editor reloads with the written files on disk. **`stop` must never immediately follow file generation** — the step between them is always `restart` + overlay verification. Skipping this step means the change is unverified; calling `stop` first makes recovery impossible within the session.

After generating all files, call `restart` to reload the current editor browser with the newly written fragment and controller extension files.

```
run_rta_workflow_step { step: "restart", site, frameId, appPath }
→ { site, frameId, rtaStarted: true }
```

`appPath` is **required** for `restart` (same as `start`) — pass the adaptation project root.

Store the returned `site` and `frameId`. Navigate back to the editing target (repeat Step 2 navigation as needed — `restart` may reset the app to its initial view) and call `get_overlays`. Every control inserted via `CTX_ADDXML` must appear as an overlay — this is the confirmation that the fragment loaded correctly at runtime.

**Child overlay rule (hard rule).** For each control you added via `CTX_ADDXML`, you must find an overlay whose `controlId` matches that control's own id — not its parent's. The parent aggregation container appearing in `get_overlays` is **not** proof that the inserted child was accepted. If the parent is present but no overlay for the new control's id exists, the runtime silently rejected the fragment content (the change file was written and `call_action` returned `success: true`, but the control never rendered). This is a distinct failure state from "fragment not found."

**Absent child overlay → diagnose immediately:**
1. Check the wrapper element type used in the fragment. SAPUI5 aggregations enforce type contracts: e.g. `SmartForm.groupElements` requires children that implement `IFormGroupElement` (`sap.ui.comp.smartform.GroupElement` qualifies; `sap.ui.layout.HorizontalLayout` does not). A wrong wrapper is silently dropped with no error.
2. Call `lookup_ui5_documentation` (see Step 6) for the target aggregation and compare its accepted `controlType` against what your fragment root element actually is.
3. Replace the wrapper with the correct SAPUI5 type, write the corrected fragment file, call `restart`, re-navigate, and call `get_overlays` again.
4. Repeat until the new control's own overlay entry is present.

If an expected control is missing from the overlay list for other reasons (wrong `fragmentPath`, malformed XML, namespace mismatch): inspect the relevant change file and fragment XML, fix the file, call `restart` again with the same `site`+`frameId`, re-navigate, and call `get_overlays` again. Repeat until all inserted controls are confirmed present.

### Step 14 — Stop

Call `step: "stop"`. The server closes the session; if it was the last one, the browser shuts down too.

Then kill the editor server. `open_adaptation_editor` already returns ready-made kill instructions for the host platform — relay those. The manual forms, by platform:

**Mac/Linux:**
```
kill -9 $(lsof -ti:<port>)   # by port (recommended)
kill <processId>             # by PID
```

**Windows:**
```
for /f "tokens=5" %a in ('netstat -ano ^| findstr :<port>') do taskkill /PID %a /F   :: by port
taskkill /PID <processId> /F                                                          :: by PID
```

Report to the user: summary of all changes made, files created, any issues encountered, **plus the confidence the model assigned to each AI decision (control selection, action selection, payload prep) for every change** — this makes silent high-confidence decisions auditable after the fact.

## Error Handling

| Situation | Action |
|-----------|--------|
| Page not loading | Wait 30 s. If still nothing, verify URL and editor server is running. |
| `start` returns `rtaStarted: false` | Retry once after 3 s. If still false, the app may not support RTA. |
| `get_overlays` returns empty | Wait 5 s, retry. If still empty, ask the user to confirm the editor is on the right view. |
| Expected action id is not in the chosen overlay's `actionIds` | **Stop.** This is the hard-stop case from *Confidence & HITL Gating*. Do not silently switch controls or actions. Tell the user what you expected, what came back, and ask how to proceed. |
| Action execution fails | Report error, offer retry with different params. |
| Save fails | Report error. Inform user changes may be lost. |
| `adp_controller_extension` Phase 1 (knowledge base) fails | Surface the error and stop. Ask the user to verify `appPath` points to an adaptation project root (a folder containing `webapp/manifest.appdescr_variant`). |
| `Unknown site` or missing `site` field | Pass the `site` URL from `open_adaptation_editor` to every step. |
| `Frontend action ... not registered` | The editor hasn't finished loading, or wrong frame. Verify `frameId: "preview"` and retry `start`. |
| `Executable doesn't exist at .../chromium-...` or `browserType.launch: ...` referencing a missing browser | No system Chrome and no Playwright Chromium installed. (1) Prompt the user to run `npx playwright install chromium` (or run it on their behalf if they consent). (2) Retry `start` with the same payload. (3) If still failing, ask the user to set `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` to a known Chrome/Chromium binary. |

## Multi-Change Strategy

When the user requests multiple changes:
1. Parse all intended changes upfront.
2. Execute Steps 3–9 once per change, all under the same `site`+`frameId`.
3. Save once at the end (Step 11).
4. If one change fails, save the successful ones and report which failed.
5. Generate content for all fragments / extensions together in Step 12.
6. Stop the session (Step 14) only after everything is done.

## Example Session

Workflow example (button + dialog on an Object Page): **[references/example-session.md](references/example-session.md)**.