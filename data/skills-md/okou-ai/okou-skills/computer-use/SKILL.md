---
name: computer-use
description: Operate apps on a desktop host through Computer Use, whether surfaced as Okou Desktop or the still-supported legacy Zero Desktop, when APIs are not enough. Not for remote browser sessions (`okou browser use`), surfaced as Okou Browser or legacy Zero Browser.
---

# Computer Use

## Overview

Use `okou computer-use <command>` to inspect and operate apps on the connected desktop host. Current clients present this as Okou Desktop; still-supported legacy clients may call it Zero Desktop. Treat it as an accessibility-first GUI control surface: read the app state, act through accessibility elements, and inspect screenshots only when visual information is required or the accessibility state is insufficient.

`--app` accepts an app bundle id only, such as `com.apple.Safari` or `com.google.Chrome`. App names like `Safari`, `Google Chrome`, `Slack`, or `WeChat` are display labels only and must not be passed to `--app`.

## Core Workflow

1. List apps and choose the target app's `bundleId`:

```bash
okou computer-use list-apps
```

Use the `name` field only to identify the app for yourself, then copy the `bundleId` field. Apps listed without a `bundleId` cannot be targeted.

2. Set the bundle id you found:

```bash
app_bundle_id="com.apple.Safari"
```

3. If the app is not running, open it by bundle id:

```bash
okou computer-use open-app --app "$app_bundle_id" --timeout 10
```

4. Inspect the target app by bundle id:

```bash
okou computer-use get-app-state --app "$app_bundle_id" --timeout 10
```

5. Read the JSON result:

- `snapshotId` is required for follow-up actions against the same state.
- `appState` is expected to be a local file path containing the full accessibility tree. Read or filter that file to find element indexes, roles, labels, URLs, and the focused element.
- `screenshot` is a local image path under `/tmp/vm0/computer-use/...`. Do not inspect it by default; use the image viewer only when visual judgment matters or the accessibility tree does not expose a usable target.
- During rollout, older CLI versions may still return `appState` as an inline string. If it is not a path, save the JSON output to a temp file and extract/filter the inline string.

6. Act on elements first, using the same bundle id and snapshot:

```bash
okou computer-use click --app "$app_bundle_id" --snapshot-id <snapshotId> --element-index <index>
okou computer-use set-value --app "$app_bundle_id" --snapshot-id <snapshotId> --element-index <index> --value "text"
okou computer-use type-text --app "$app_bundle_id" --snapshot-id <snapshotId> --text "literal text"
okou computer-use press-key --app "$app_bundle_id" --snapshot-id <snapshotId> --key Command+L
okou computer-use scroll --app "$app_bundle_id" --snapshot-id <snapshotId> --element-index <index> --direction down --pages 1
```

7. Re-read state after every meaningful UI change. Element indexes and coordinates can become stale after navigation, scrolling, or opening a new window.

If a post-action command returns a new `snapshotId` and `appState`, use that new snapshot. Otherwise, explicitly run `get-app-state` again before choosing the next element index or coordinate.

## Accessibility-First Policy

- Start with the `appState` accessibility tree. For routine forms, buttons, lists, links, and navigation, do not inspect the screenshot when accessibility roles and labels provide enough information to act safely.
- If the UI behaves unexpectedly, re-read and filter the latest `appState` before falling back to the screenshot.
- Inspect the screenshot when the accessibility tree is incomplete or ambiguous, the task depends on visual appearance or layout, or no useful accessibility element exists and coordinate input is required.
- Use coordinates only after inspecting the screenshot from the same snapshot. Return to element-index actions as soon as the accessibility tree exposes a reliable target.

## App Identity Rules

- Always run `list-apps` before targeting an app unless you already know the exact bundle id from the same host.
- Always pass the `bundleId` value to `--app`.
- Never pass display names such as `Slack`, `Safari`, `Google Chrome`, or `WeChat` to `--app`.
- If a command fails with `app_not_found` and the `--app` value looks like a name, re-run `list-apps`, find the app record, and retry with its `bundleId`.
- If the target app has no `bundleId` in `list-apps`, report that it is not targetable through Computer Use.

To search the `list-apps` output for a likely target:

```bash
apps_json=/tmp/computer-use-apps.json
okou computer-use list-apps > "$apps_json"
node -e "const fs=require('fs'); const q=(process.argv[2]||'').toLowerCase(); const apps=JSON.parse(fs.readFileSync(process.argv[1],'utf8')).apps || []; for (const a of apps) { if (!q || String(a.name || '').toLowerCase().includes(q)) console.log([a.name || '', a.bundleId || 'NO_BUNDLE_ID', a.running ? 'running' : 'not running'].join('\t')); }" "$apps_json" "Slack"
```

Copy the exact `bundleId` from the matching row into `app_bundle_id`.

## Reading App State

Accessibility trees can be very large. Prefer the `appState` file returned by the command:

```bash
app_bundle_id="com.apple.Safari"
state_json=/tmp/computer-use-state.json
okou computer-use get-app-state --app "$app_bundle_id" --timeout 10 > "$state_json"
app_state_path=$(node -e "const fs=require('fs'); const r=JSON.parse(fs.readFileSync(process.argv[1],'utf8')); console.log(r.appState)" "$state_json")
rg -n "Ethan|showcase|sites\\.vm0|Send now" "$app_state_path"
```

If the CLI still returns inline app state instead of a path, use the transition workaround:

```bash
state_json=/tmp/computer-use-state.json
okou computer-use get-app-state --app "$app_bundle_id" --timeout 10 > "$state_json"
node -e "const fs=require('fs'); const s=JSON.parse(fs.readFileSync(process.argv[1],'utf8')).appState; s.split('\\n').forEach((l,i)=>{ if(/Ethan|showcase|sites\\.vm0|Send now/.test(l)) console.log((i+1)+': '+l) })" "$state_json"
```

Use filtered output to locate clickable `link`, `button`, `text field`, `checkbox`, or `outline row` entries and their element indexes.

## Action Rules

- Use the same bundle id for `get-app-state` and follow-up actions against that snapshot.
- Prefer `--element-index` or `--element` over coordinate clicks.
- Use `--x/--y` only when the screenshot clearly shows the target but the accessibility tree has no useful element.
- Always pass the matching `--snapshot-id` from the state used to pick the element or coordinate.
- Use `open-app --app <bundleId>` when the app is not visible or not running.
- Use `press-key` for reliable shortcuts such as `Command+L`, `Command+T`, `Command+W`, `Enter`, and arrow keys.
- Use `type-text` only after confirming focus is in the right field.
- If `type-text` fails with `element_not_editable`, click into a text field first or use `set-value` on a settable text field.
- Avoid destructive UI actions unless the user explicitly requested them and the current state confirms the target.

## Browser Pattern

After clicking a link from another app:

1. Use `list-apps` to find the browser bundle id, such as `com.apple.Safari`, `com.google.Chrome`, or the Arc bundle id returned by the host.
2. Read or filter the browser `appState` for the address field, page title, links, controls, and focused element.
3. Use `press-key --app <browserBundleId> --snapshot-id <snapshotId> --key Command+L` plus `type-text` and `Enter` when direct navigation is faster than finding a link.
4. Inspect the screenshot only when the task depends on layout, design, images, canvas content, or another detail that the accessibility tree does not represent reliably.

## Failure Handling

- `app_not_found`: check whether `--app` was a display name. If so, retry with the app's `bundleId` from `list-apps`. If it was already a bundle id, the app may not be installed, not running, or not targetable on the host.
- `window_unavailable`: try `open-app --app <bundleId>`, then run `get-app-state` again. If it still fails, report that the app has no controllable window.
- `element_not_editable`: click into the target text field, re-read state, then use `type-text`; or use `set-value` when a settable text field is available.
- `permission_denied`, `accessibility_unavailable`, or `screen_recording_unavailable`: report the missing Desktop permission instead of retrying the same command.

## Reporting Back

State what was actually done through Computer Use: apps inspected by bundle id, whether screenshot fallback was needed, and whether actions succeeded. If a desktop action times out or the host is unavailable, say that directly and use a stable fallback only when it still satisfies the user request.
