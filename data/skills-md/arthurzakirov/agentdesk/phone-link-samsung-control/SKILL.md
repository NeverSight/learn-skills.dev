---
name: phone-link-samsung-control
description: Control a Samsung phone through Windows Phone Link using Codex Computer Use. Use when asked to operate, configure, or test the mirrored Samsung phone from the Windows desktop; do not use for ordinary browser-only or Android-advice tasks.
---

# Phone Link Samsung Control

Use this skill when a task needs direct interaction with a Samsung phone as mirrored through the Windows Phone Link app.

This skill captures a previously tested native Windows control path. The important distinction is that Phone Link is a native Windows app, not a browser tab. Do not conclude that control is unavailable merely because browser tools cannot see it.

## Required Computer Use Setup

Before controlling Windows apps, load the bundled `computer-use` skill and its required docs. Use the JavaScript execution surface that can import `@oai/sky`; if that tool is not currently loaded, search for `node_repl` or Computer Use tools rather than using browser-only automation.

Initialize the runtime once per fresh JavaScript session:

```js
if (!globalThis.sky) {
  const { sky } = await import("@oai/sky");
  globalThis.sky = sky;
}
nodeRepl.write("sky initialized");
```

## Find The Phone Link Windows

Phone Link has been observed under this native Windows app id:

```text
Microsoft.YourPhone_8wekyb3d8bbwe!App
```

List apps or windows and filter for that app id plus titles such as:

- `YOUR PHONE TITLE`
- `Phone Link`
- `Einstellungen`

Prefer the device window titled `YOUR PHONE TITLE` for touch interaction with the mirrored phone. Use `Phone Link` only for the main app shell, and `Einstellungen` only when the Android Settings app is open inside the mirrored phone.

Known working selection pattern:

```js
globalThis.apps = await sky.list_apps();
const candidates = apps.flatMap(app => app.windows || [])
  .filter(w => w.app === "Microsoft.YourPhone_8wekyb3d8bbwe!App" && w.title === "YOUR PHONE TITLE");

if (candidates.length !== 1) {
  nodeRepl.write(JSON.stringify(candidates.map(w => ({ id: w.id, app: w.app, title: w.title })), null, 2));
  throw new Error(`Expected exactly one selected Phone Link window; found ${candidates.length}`);
}

globalThis.targetWindow = await sky.get_window({ id: candidates[0].id, app: candidates[0].app });
await sky.activate_window({ window: targetWindow });
globalThis.state = await sky.get_window_state({
  window: targetWindow,
  include_screenshot: true,
  include_text: false
});
globalThis.targetWindow = state.window;
```

If the JavaScript session loses state, reinitialize `sky`, find the target window again, and re-observe before acting.

## Act Through Screenshots

For phone interaction, use screenshots and coordinates against the latest observation. Keep `include_text: false` unless text is necessary and safe to inspect. This avoids exposing private messages, emails, notifications, or app contents.

Before every click, drag, or scroll:

- Re-observe the relevant Phone Link window if the current screenshot may be stale.
- Use the `screenshotId` from the latest observation.
- Clear or replace stale cached state after the action.
- Re-observe after the action to verify the visible result.

Known working harmless proof action:

```js
const observation = globalThis.state;
const screenshotId = observation.screenshots?.[0]?.id;
if (!screenshotId) throw new Error("No screenshotId returned by latest observation");

globalThis.state = null;
await sky.drag({
  window: observation.window,
  screenshotId,
  from_x: 560,
  from_y: 1160,
  to_x: 120,
  to_y: 1160
});

globalThis.state = await sky.get_window_state({
  window: observation.window,
  include_screenshot: true,
  include_text: false
});
globalThis.targetWindow = state.window;
```

In the successful run, this horizontal drag on the Android home screen produced a visible Android edge/swipe response in the `YOUR PHONE TITLE` window. That proved Phone Link accepted touch gestures.

## Safety Boundaries

Treat phone control as privacy-sensitive.

- Do not open, read, summarize, or expose private content such as emails, messages, notifications, browsing history, account details, or app contents.
- Do not purchase anything, add items to a cart, enter credentials, approve payments, or approve paid plans.
- Stop and ask before installing third-party apps, granting sensitive permissions, changing account settings, choosing allowed contacts/callers, or changing alarms.
- Prefer harmless system navigation such as Back, Home, Recents, Settings navigation, or empty-area gestures when testing control.
- Avoid actions that could make sound unexpectedly louder, such as disconnecting Bluetooth while media might continue through phone speakers.

## Personal device and routine context

For a user's saved device title and routine preferences, read `~/.config/AgentDesk/workstation/phone-link-guidance.md` when available. If that path is absent, read `~/.config/AgentDesk/workstation-root.txt` as a plain absolute directory path and load the same filename there. It is private context installed separately; do not publish its values here. If absent, discover the actual window title and ask for only the routine details needed by the current request.

Saved routine preferences describe intent, not verified current settings. Verify the UI before claiming a schedule, alarm or restriction is configured.
