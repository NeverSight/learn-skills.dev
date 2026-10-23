---
name: writing-settings-forms
description: Write Celigo settings forms -- the form definition (settingsForm) the Celigo UI renders to collect a resource's settings, on integrations, flow groups, flows, exports, imports, connections, and iClients. Covers the seven scopes and how steps read their values, fields and types, options, conditions, layouts and containers, init scripts, and the dynamic exportSelect and staticMap fields. Use when adding or changing a settings form, giving users a setting that steps read at run time, building a dropdown from an export or a value-mapping table, or working out why a form or a setting doesn't show what you expect.
---

<!-- TIER:1 -->

# Writing Settings Forms

A settings form (`settingsForm`) is the form the Celigo UI renders to collect a resource's `settings`: which fields appear, their labels and choices, how they're grouped, and which show when. The values it collects are stored in the same resource's `settings`, and that's what steps read at run time -- `{{settings.flow.region}}` in a template, `options.settings.flow.region` in a script.

Seven places carry a form, each with its own `settings`: an integration, each of an integration's flow groups (`flowGroupings[]`), a flow, an export, an import, a connection, and an iClient. An Integration App's settings are a different mechanism, driven by the app's own code -- see [managing-integrations > Integration Apps](../managing-integrations/references/integration-apps.md).

What a form is not:

- **Not validation.** Only the UI renders the form and applies its rules. An API, CLI, or MCP write of `settings` stores the object it's given: a field the form marks `required` can be missing, keys the form doesn't define are kept, and nothing checks types or choices.
- **Not checked on save.** A layout entry or a condition naming a field the form doesn't have is stored as sent. Only `form` and `init` are kept: any other top-level key in `settingsForm` is dropped without an error.
- **Not what steps read.** Steps read `settings`, never the form. A new field gives steps nothing until its value is in `settings`, so write the value along with the field.

## How to Run the Steps

This skill names each step by what it reads or changes; the exact calls depend on how you reach the account. Read the one reference that matches your tools -- both follow the step numbers of How to Build a Settings Form, then How to Check a Form:

- **Celigo MCP tools** (`list_integrations`, `upsert_integration`, `upsert_flow`, `upsert_export`, ...) -- [references/mcp.md](references/mcp.md). The deployed server writes forms only through the full-replace `upsert_*` tools, and can't run an init script or preview a dropdown's export.
- **The `celigo` CLI** -- [references/cli.md](references/cli.md)

Reading a resource only reads. Writing a form or its `settings` updates the resource, and a full update replaces the whole document: a body that leaves out `settingsForm` or `settings` erases them.

## The Seven Scopes

| Scope | Form | Values | Steps read them as |
|---|---|---|---|
| Integration | `settingsForm` | `settings` | `settings.integration.<name>`, in every flow of the integration |
| Flow group | `flowGroupings[].settingsForm` on the integration | `flowGroupings[].settings` | `settings.flowGrouping.<name>`, in the flows of that group |
| Flow | `settingsForm` | `settings` | `settings.flow.<name>`, in the flow's steps |
| Export (lookups too) | `settingsForm` | `settings` | `settings.export.<name>`, in that step only |
| Import | `settingsForm` | `settings` | `settings.import.<name>`, in that step only |
| Connection | `settingsForm` | `settings` | `settings.connection.<name>`, in steps using the connection |
| iClient | `settingsForm` | `settings` | `settings.iClient.<name>`, in steps whose connection uses it |

The scope key is literal: `{{settings.region}}` (no scope) and paths built from field labels or section names render empty. After the scope, the path follows the stored JSON -- a top-level value is `settings.flow.region`, and each nested key adds a segment. Templates, filters, and Mapper 2.0 read these paths ([writing-handlebars > Context Decision Matrix](../writing-handlebars/SKILL.md#context-decision-matrix-afe-20)); scripts read `options.settings.<scope>` ([writing-scripts > Common Options](../writing-scripts/SKILL.md#common-options-available-to-all-hooks)).

Which scopes a step sees depends on how it runs:

- **A flow run** gives the whole chain: integration, flow group, flow, connection, iClient, and the step's own scope.
- **A step inside an API or a Tool** gets only its own scope plus connection and iClient; integration, flow group, and flow resolve empty there.
- **A step run on its own** -- an export or import invoke with no parent -- gets only its own scope. An import invoke run as a step of a flow sees the flow's chain.

Pick the narrowest scope that every step reading the value shares: a whole integration, a flow group for flows that share a region or subsidiary, a flow, or a step's own form for a knob only that step uses.

## Quick Reference

### The Shape

```json
{
  "settingsForm": {
    "form": {
      "fieldMap": {
        "region": {
          "id": "region", "name": "region", "type": "select", "label": "Region", "required": true,
          "options": [{ "items": [{ "label": "United States", "value": "us" }, { "label": "Europe", "value": "eu" }] }]
        },
        "vatNumber": {
          "id": "vatNumber", "name": "vatNumber", "type": "text", "label": "VAT number",
          "visibleWhen": [{ "field": "region", "is": ["eu"] }]
        },
        "statusMap": {
          "id": "statusMap", "name": "statusMap", "type": "staticMap", "label": "Order status map",
          "keyName": "source", "keyLabel": "Source status", "valueName": "target", "valueLabel": "Destination status",
          "valueOptions": [{ "label": "Open", "value": "open" }, { "label": "Closed", "value": "closed" }]
        }
      },
      "layout": {
        "type": "collapse",
        "containers": [
          { "label": "General", "fields": ["region", "vatNumber"] },
          { "label": "Advanced", "type": "box", "containers": [{ "label": "Status mapping", "fields": ["statusMap"] }] }
        ]
      }
    }
  },
  "settings": { "region": "eu", "vatNumber": "EU123", "statusMap": [{ "source": "pending", "target": "open" }] }
}
```

### Field Properties

| Property | Rules |
|---|---|
| fieldMap key, `id`, `name` | Use one string for all three. `name` is the key the value is saved under, directly in `settings`; `id` is how the layout and conditions refer to the field. Keep it a plain key with no dots: the UI saves `a.b` as nested objects but reads it back from a flat `a.b` key, so the field reloads empty |
| `type` | The control -- see Field Types |
| `label`, `description`, `helpText` | The label beside the field, a line of text under it, and the help icon's text |
| `required` | Blocks the UI's Save while the field is empty (default `false`); API writes skip it |
| `defaultValue` | What the UI shows while `settings` holds no value under the field's `name` |
| `options` | The choices of a `select`, `multiselect`, or `radiogroup`: groups (`[{"items": [...]}]`, each item a string or a `{label, value}` pair) or bare `{label, value}` entries. A `toggle` takes bare `{label, value}` entries. The saved value is the item's `value` |
| Conditions | `visibleWhen` and its relatives -- see Conditions |
| `omitWhenHidden` | `true` leaves the field's value out of a save while it's hidden; without it, a hidden field's value is saved like any other |

### Field Types

| `type` | Control | Saved value |
|---|---|---|
| `text` | Text input; `multiline: true` for a text area, `inputType` (`number`, `email`, `password`, `tel`, `url`) for a typed input, `delimiter` to split the input into an array | String (array with `delimiter`) |
| `checkbox` | Checkbox | Boolean |
| `toggle` | A switch between the entries of `options` | The chosen entry's `value` |
| `select`, `radiogroup` | Dropdown, radio buttons | The chosen item's `value` |
| `multiselect` | Dropdown allowing several choices | Array of `value`s |
| `date`, `datetime` | Date or date-and-time picker; `doNotAllowFutureDates`, `skipTimezoneConversion` | The picked date |
| `relativeuri` | Text input for a relative URI | String |
| `editor` | Code editor; `mode` is `json`, `xml`, `csv`, or `text` | The editor's content |
| `keyvalue` | Rows of two free-text inputs; `keyName` / `valueName` name them (default `key` / `value`), `showDelete` adds a delete button per row | Array of `{<keyName>, <valueName>}` rows |
| `staticMap` | Two-column mapping table whose columns can offer choices | Array of `{<keyName>, <valueName>}` rows -- see Dynamic Fields |
| `exportSelect` | Dropdown whose options an export returns | The chosen option's `value` (an array with `multiselect: true`) -- see Dynamic Fields |

### Conditions

A condition rule is `{"field": "<field id>", "is": [<values>]}` (or `"isNot"`). Two set values compare as strings, so `"is": ["true"]` and `"is": [true]` both match a checked checkbox; match an unchecked one with `[false]`.

- `visibleWhen` shows the field while **any** rule matches; `visibleWhenAll` while **all** of them do. With neither, the field always shows.
- `requiredWhen` / `requiredWhenAll` and `disabledWhen` / `disabledWhenAll` make the field required or read-only the same way.
- A rule can hold nested `"AND": [rules]` or `"OR": [rules]` in place of `field`.
- A rule naming a field the form doesn't have counts as matching for `visibleWhen` (the field always shows) and as not matching for `requiredWhen` and `disabledWhen` -- the save doesn't catch it.

### Layout

`form.layout` arranges fields; a field the layout doesn't list isn't shown, and a layout id with no `fieldMap` entry renders nothing.

- A layout has a `type`, `containers`, and optionally `fields` (ids shown before the containers).
- The layout's `type` sets how its containers render: `column` side by side, `collapse` as collapsible sections (closed until opened; `"collapsed": false` opens one), `box` as bordered groups, `indent` as indented groups, `tabWithoutSave` and `verticalTabWithoutSave` as tabs.
- Each container has a `label` (its heading) and `fields`, and can carry its own `type` and `containers` to nest another level, as the Advanced container does in The Shape.

### Init Scripts

`settingsForm.init` -- `{"_scriptId": "<scriptId>", "function": "<name>"}` -- runs a script function each time the UI opens the form. The UI renders the form the function returns **instead of** `settingsForm.form`, then fills in the values from `settings`; a throw shows its message in place of the form.

```javascript
function initForm(options) {
  var form = options.resource.settingsForm.form;
  // add, remove, or change fields from the resource's own state
  return form;
}
```

- **What the function gets:** `options.resource` (the resource whose form it is -- for a flow group, the group: `_id`, `name`, `settings`, `settingsForm`), `options.sandbox`, and on an integration and a flow group the parents: a flow group gets its integration as `parentResource` (and a parent integration as `grandparentResource`), a child integration gets its parent as `parentResource`. `options.license` and `options.parentLicense` appear only in Integration Apps. Flows, exports, imports, and connections get only `resource` and `sandbox`.
- **The script must be the account's own.** Any other `_scriptId` is refused with 422 "Only a script owned by the user or a script shared by the Integration App can be used at settingsForm.init._scriptId" (on a flow group the path is `flowGroupings.<index>.settingsForm.init._scriptId`).
- **Not on iClients.** The platform's form-init route serves integrations, flow groups, flows, exports, imports, and connections only, so an iClient form with an `init` shows an error instead of the form -- and an iClient save stores any `_scriptId` without checking it.
- **Testing:** no CLI command or MCP tool calls the init route. Run the function through the JavaScript processor with an `options` object you build -- see How to Check a Form.

### Schema Index

The form's full shape is the `Form` schema on the API reference's [Integrations](https://developer.celigo.com/api/api-reference/integrations-and-flows/integrations.md) page (agent-readable markdown; exports and imports embed the same schema), and `settings` is a free-form object on every scope. Over MCP, `get_schema({ target: "resource", name: "common/form" })` returns it.

## Related Skills

- [writing-handlebars > Context Decision Matrix](../writing-handlebars/SKILL.md#context-decision-matrix-afe-20) -- reading settings values in templates
- [writing-scripts > Common Options](../writing-scripts/SKILL.md#common-options-available-to-all-hooks) -- `options.settings` in hooks, and the init function point
- [configuring-filters > Gotchas](../configuring-filters/SKILL.md#gotchas) -- settings scopes in filter operands
- [configuring-exports](../configuring-exports/SKILL.md) -- the export body an `exportSelect` runs
- [managing-integrations > Organize the resources inside](../managing-integrations/SKILL.md#4-organize-the-resources-inside) -- creating flow groups and putting flows in them
- [managing-integrations > Integration Apps](../managing-integrations/references/integration-apps.md) -- app settings, which the app's own code saves
- [configuring-connections](../configuring-connections/SKILL.md) -- full updates of connections and iClients, which carry masked secrets

<!-- TIER:2 -->

## Dynamic Fields: exportSelect and staticMap

### exportSelect

A dropdown whose options come from an export the form carries inline, in `resource.virtual`:

```json
"fieldMap": {
  "warehouse": {
    "id": "warehouse", "name": "warehouse", "type": "exportSelect", "label": "Warehouse",
    "resource": {
      "virtual": {
        "_connectionId": "<connectionId>",
        "adaptorType": "HTTPExport",
        "http": { "relativeURI": "/v1/warehouses", "method": "GET", "formType": "http", "response": { "resourcePath": "warehouses" } },
        "transform": {
          "type": "expression",
          "expression": {
            "version": "2",
            "rulesTwoDotZero": {
              "mode": "create",
              "mappings": [
                { "generate": "label", "extract": "$.name", "dataType": "string", "status": "Active" },
                { "generate": "value", "extract": "$.code", "dataType": "string", "status": "Active" }
              ]
            }
          }
        }
      }
    }
  },
  "carrier": { "id": "carrier", "name": "carrier", "type": "select", "label": "Carrier" }
}
```

The `exportSelect` entry nests six levels deep; check that the next field (`carrier` here) still sits in `fieldMap`, beside it -- one closing brace too many puts it under `form`, outside `fieldMap`, and a layout id with no `fieldMap` entry renders nothing.

- **The export is an export body, not a reference.** There's no way to point at a saved export by id: put `adaptorType`, its adaptor block, and an optional `transform` in `virtual`. Without `resource.virtual` the field shows "requires export resource." `_connectionId` defaults to the connection of the export or import the form is on; on any other scope, set it.
- **The UI previews the export when the form opens (and on Refresh)** and lists the preview's `data` -- the records after the transform, output filter, and preSavePage hook. Each record needs a `value` and a `label`; a bare string or number serves as both. The preview reads at most 100 records: the UI sends `test.limit` 100 unless the export sets its own, which can't exceed 100. An HTTP export that finds no records answers without a `data` list, so the field shows "expecting array. try transform?" rather than an empty list -- as it does for any answer that isn't a list.
- **`multiselect: true`** allows several choices, saved as an array.
- **`supportHandlebars: true`** renders the export body as a template before each preview (everything but `transform`, `hooks`, and `filter`). The template's context isn't the runtime's: the form's current values sit under the form's own scope name (`integration`, `flowGrouping`, `flow`, `export`, or `import`), beside the saved settings of the scopes above it and, on an export or import form, the whole document of the connection the export uses -- with no `settings.` prefix: `{{integration.accountId}}`, `{{export.country}}`. Connection and iClient forms get an empty context. A templated list doesn't load on its own when the form opens: it loads through `refreshOptionsOnChangesTo` or `typeAheadSearch`, or when the user clicks Refresh.
- **`refreshOptionsOnChangesTo: ["<field id>", ...]`** loads the templated list once one of those fields has a value and reloads it whenever one changes -- a cascading dropdown. It works only with `supportHandlebars`.
- **`typeAheadSearch: true`** reloads it as the user types (300 ms after the last keystroke), with the typed text as this field's own value in the context; an empty box clears the list, and free text is accepted.

### staticMap

A two-column table, saved under the field's `name` as an array of rows: `[{"source": "pending", "target": "open"}]`.

- **`keyName` / `valueName`** name the columns -- the keys of each saved row. **`keyLabel` / `valueLabel`** head them.
- **`keyOptions` / `valueOptions`** give a column a suggestion list: `{label, value}` items (`{id, text}` and `[value, label]` work too). The cell still accepts typed values.
- **`keyResource` / `valueResource`** -- `{"virtual": {<export body>}}` -- fill a column's suggestions from an inline export, previewed as for `exportSelect` (no templating). With either one set, both columns are required unless the field sets `keyValueRequired: false`, and the UI drops incomplete rows when it saves.
- Steps read the whole array: `options.settings.flow.statusMap.find(r => r.source === status)` in a script, or `#each` over it in a template.

## How to Build a Settings Form

### 1. Decide the scope

Who reads the value? Put the form where every reader shares it ([The Seven Scopes](#the-seven-scopes)), and remember that steps in an API or a Tool see only their own scope plus connection and iClient. For a flow group, create the group first and put the flows in it ([managing-integrations > Organize the resources inside](../managing-integrations/SKILL.md#4-organize-the-resources-inside)).

### 2. Read the resource

Read the whole resource: an existing `settingsForm` to extend, the current `settings`, and everything else a full update must send back. On an integration, a flow group's form and values live in its `flowGroupings[]` entry.

### 3. Write the fields

One `fieldMap` entry per setting, with the same string as key, `id`, and `name` -- a plain key, no dots. Choose the `type` (Field Types), give `options` to choice fields, and a `defaultValue` where the UI should suggest one. For a list of values the user picks from another system, use an `exportSelect`; for a value-to-value table, a `staticMap` (step 6).

### 4. Lay the fields out

List every field in the layout exactly once. Choose the top-level `type`, group related fields into labeled containers, and nest a container's own `type` and `containers` for a second level.

### 5. Add conditions

Show, require, or lock fields with `visibleWhen` / `requiredWhen` / `disabledWhen` (or their `*All` forms), naming fields by id. Add `omitWhenHidden: true` to a field whose value shouldn't be saved while it's hidden.

### 6. Build the dynamic fields

Write the inline export of each `exportSelect` (or a `staticMap` column's `keyResource` / `valueResource`) and preview it before you save the form: it must return `label` / `value` records -- shape them with a `transform`. Add `supportHandlebars` and `refreshOptionsOnChangesTo` for a dropdown that depends on another field.

### 7. Add an init script (optional)

When the form must change with the resource's state, write an init function that returns the form, test it (How to Check a Form), save the script, and set `settingsForm.init`. The returned form replaces `settingsForm.form` in the UI, so keep `form` as the fallback the function starts from.

### 8. Save the form and the values together

Send the form and the matching `settings` values in one update -- the full document, read in step 2 -- so steps have values before anyone opens the form. The form you send replaces the stored one, so to change one field start from the stored `settingsForm` and keep every other `fieldMap` entry and layout id. Before sending, check the whole body rather than the field you changed: `fieldMap` and `layout` sit side by side directly in `form`, and every id in `layout` is a key directly in `fieldMap`. Keep every value steps read in the form: a save in the UI writes `settings` from the form's fields.

### 9. Read the values in steps

Reference each value through its scope key: `{{settings.flowGrouping.region}}` in a template or filter operand, `options.settings.export.batchLimit` in a script, or `$.settings.flow.region` in a Mapper 2.0 extract with the envelope input context ([writing-mappings > Choose the input context](../writing-mappings/SKILL.md#4-choose-the-input-context)).

## How to Check a Form

1. **Read the resource back** and compare `settingsForm` and `settings` with what you sent. A save never validates the form, so check it yourself: every layout id has a `fieldMap` entry, every field is in the layout once, every condition names an existing field, key = `id` = `name` on each field, and choice fields have `options`.
2. **Preview each inline export** an `exportSelect` or `staticMap` runs, with `"test": {"limit": 100}` added the way the UI sends it -- a preview without it returns one record. Its `data` must be a list of `label` / `value` records.
3. **Run the init function** through the JavaScript processor, with the `options` object it will receive (`resource`, `sandbox`, and the parents its scope gets). The reply's `data` is the form it returns; a throw comes back as 422 with the message.
4. **Render a template that reads the values** with the Handlebars processor, with `settings` in its data (`{"record": {...}, "settings": {"flow": {"region": "eu"}}}`), or preview the step with `settings` in the document. An import invoke writes to the destination; run one only against a test destination.
5. **Open the form in the UI.** Only the UI renders it -- the layout, the conditions, the dropdowns, and the init script's result.

<!-- TIER:3 -->

## Pre-Submit Checklist

- [ ] The form sits on the narrowest scope every reading step shares
- [ ] Each field's `fieldMap` key, `id`, and `name` are the same plain string
- [ ] Every field appears in the layout once, and every layout id and condition names an existing field
- [ ] Choice fields have `options`; each `exportSelect` has `resource.virtual` whose preview returns `label` / `value` records
- [ ] An `init._scriptId` names a script in this account, and the function was tested; not on an iClient
- [ ] `settings` holds a value for every field steps read, written in the same update as the form
- [ ] The update sent the complete document: `settingsForm`, `settings`, and everything else the resource had
- [ ] Steps reference each value through its scope key

## Gotchas

1. **A full update erases what it omits.** A body without `settingsForm` or `settings` removes them, and a body whose `settingsForm` has no `init` removes the init script. Read the whole resource first, and change only `settingsForm.form` when that's all you mean to change.
2. **Saves aren't checked against the form.** A missing `required` value, extra keys, wrong types, and dangling layout ids or conditions all save; only the UI enforces the form.
3. **Only `form` and `init` are kept.** Anything else at the top of `settingsForm` is dropped silently.
4. **Values sit directly under `settings`, keyed by `name`.** A dotted `name` saves as nested objects but reloads empty, and a value under any other key is invisible to the field.
5. **Steps need the scope key.** `{{settings.region}}` renders empty; so does a path built from a field's label or a section heading.
6. **A step run on its own sees only its own scope.** An export or import invoke without a parent renders `settings.integration`, `settings.flowGrouping`, and `settings.flow` empty -- run it as a step of the flow, or the flow itself, to see them.
7. **A hidden field is still saved** unless it sets `omitWhenHidden`.
8. **A condition on a missing field fails open for visibility.** `visibleWhen` naming a field that isn't there leaves the field always visible; `requiredWhen` and `disabledWhen` never apply.
9. **The init script replaces the form.** The UI shows what the function returns, not `settingsForm.form`; a throw replaces the form with the error message.
10. **iClient forms can't use init,** and an iClient save accepts any `_scriptId` unchecked.
11. **An exportSelect lists the preview's `data`, at most 100 records.** Records without `label` and `value` don't make usable options, and an HTTP export that finds nothing shows an error instead of an empty list.
12. **Keep every value steps read in the form.** A UI save writes `settings` from the form's fields, so a key you wrote over the API that the form doesn't define won't survive someone saving the form.
13. **Integration App settings are separate.** An app's settings form is in its `settings` (`settings.general`, `settings.sections`), and changes go through the app's own save route -- see [managing-integrations > Integration Apps](../managing-integrations/references/integration-apps.md).

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| 422 "Only a script owned by the user or a script shared by the Integration App can be used at settingsForm.init._scriptId" | `init._scriptId` names a script this account doesn't have | Use the `_id` of one of the account's scripts |
| The form shows an error message instead of fields | The init function threw (or the form is on an iClient with an `init`) | Run the function through the JavaScript processor to see the error; remove `init` from an iClient |
| "requires export resource." under an exportSelect | No `resource.virtual` | Add the inline export body |
| "expecting array. try transform?" | The exportSelect's export found no records (an HTTP preview then has no `data`) or returned something other than a list | Preview the export with `test.limit` 100; shape records into `label` / `value` with a `transform` |
| An exportSelect's options are blank or can't be chosen | The records have no `label` / `value` | Map them in the export's `transform` |
| A field always shows despite `visibleWhen` | The rule names a field id that isn't in `fieldMap` | Name the controlling field's id |
| A field reloads empty after saving | Its `name` contains a dot, or differs from the key steps read | Use one plain string for key, `id`, and `name` |
| `{{settings.<scope>.<name>}}` renders empty | No scope key, the wrong scope, the value isn't in `settings`, or the step ran outside its flow | Check the path against The Seven Scopes and read `settings` back |
| A whole form or `settings` disappeared | A full update left it out | Write it back from your copy or the resource's audit log (an update's `fieldChanges` keep the old values), and send complete documents |
