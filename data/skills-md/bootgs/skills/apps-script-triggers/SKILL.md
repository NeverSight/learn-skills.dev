---
name: apps-script-triggers
description: Explains Google Apps Script's simple vs installable triggers, their event object shapes, authorization differences, and how to register/manage installable triggers programmatically without duplicating them. Use when adding onOpen/onEdit/onChange/onFormSubmit/time-driven behavior, or when a trigger isn't firing, is duplicated, or fails with an authorization error. Framework-agnostic — applies with or without bootgs. Not for quota-safe service usage or locking (`apps-script-services`), nor for getting a fix out to installed users (`apps-script-clasp-workflow`).
license: Apache-2.0
metadata:
  author: Maksym Stoianov
  version: "1.0.0"
---

# Apps Script Triggers

## Simple vs installable

| | Simple (`onOpen`, `onEdit`, `onInstall`, `onSelectionChange`) | Installable (`ScriptApp.newTrigger(...)`) |
|---|---|---|
| Registration | Automatic — GAS calls the global function by name | Explicit — created programmatically or via the Triggers UI |
| Runs as | The user currently viewing the file, with **their** authorization | The user who created the trigger, with **that user's** authorization, regardless of who triggers it |
| Can call authorized services | No — no `UrlFetchApp`, no most advanced services, no services needing OAuth consent | Yes — full access to whatever the installing user has authorized |
| Typical use | UI-only reactions (build a menu, format a cell) | Anything that calls an external API, sends email, or must run reliably regardless of viewer permissions |

If a simple `onEdit` needs to call `UrlFetchApp` or `MailApp`, it will silently fail or throw a permission error — convert it to an installable trigger instead. This is the most common "trigger works when I test it, breaks for other users" bug: the simple trigger works for you (the owner, already authorized) and fails for a viewer/editor without those grants.

## Event object shapes

| Trigger | Event object fields |
|---|---|
| `onEdit` | `{ range, oldValue, value, source, user, authMode }` — `oldValue`/`value` are only present for single-cell edits with a scalar value; multi-cell pastes omit them (check `range.getNumRows()/getNumColumns()` instead of assuming `value` exists) |
| `onChange` | `{ changeType, source, user }` — `changeType` is one of `EDIT`, `INSERT_ROW`, `INSERT_COLUMN`, `REMOVE_ROW`, `REMOVE_COLUMN`, `INSERT_GRID`, `REMOVE_GRID`, `FORMAT`, `OTHER` |
| `onFormSubmit` | `{ values, namedValues, response, source, triggerUid }` — `namedValues` maps question titles to arrays (a checkbox question yields multiple values) |
| Time-driven | No event object — the handler runs with no arguments |

## Quotas

Execution time limit: 6 minutes per invocation, for both consumer and Google Workspace accounts as of this writing. Trigger-specific caps (total triggers per user/script, total trigger runtime per day) differ by account type and change without notice — don't trust a number pasted into a skill, including this one. Query the live docs instead of the number above:

```bash
../apps-script-services/scripts/check-quotas.sh "Trigger"
../apps-script-services/scripts/check-quotas.sh "runtime"
```

(The script lives in the `apps-script-services` skill, which owns the broader quota reference — see that skill if it isn't installed alongside this one.)

## Registering installable triggers without duplicating them

`ScriptApp.newTrigger(...).create()` is not idempotent — running the setup code twice creates two triggers calling the same handler, which then runs twice per event. Always check existing triggers by handler function name before creating:

```ts
function ensureEditTrigger(spreadsheetId: string, handlerFunctionName: string): void {
  const alreadyExists = ScriptApp.getProjectTriggers().some(
    (trigger) => trigger.getHandlerFunction() === handlerFunctionName,
  );
  if (alreadyExists) return;

  ScriptApp.newTrigger(handlerFunctionName)
    .forSpreadsheet(spreadsheetId)
    .onEdit()
    .create();
}
```

Run this kind of setup once, from an explicit "install" action (a menu item, `onInstall`, or a setup script) — not from inside the trigger handler itself.

## Verification

- [ ] Any handler calling an authorized service (`UrlFetchApp`, `MailApp`, advanced services) is registered as an installable trigger, not left as a simple trigger.
- [ ] Trigger setup code checks `ScriptApp.getProjectTriggers()` before creating a new one.
- [ ] `onEdit`/`onChange` handlers don't assume `event.value` exists — they branch on `event.range` dimensions first.
