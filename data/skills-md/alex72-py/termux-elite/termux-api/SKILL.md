---
name: termux-api
description: Attribute a hanging, empty, or failing termux-* command to the right layer (Termux:API app, termux-api package, or an Android runtime permission) before relying on it. Use when termux-battery-status, termux-notification, termux-clipboard-get, termux-location, or similar commands hang, print nothing, or report a permission error. Do NOT use for storage links (see storage-permissions), for commands inside proot, or for ordinary shell failures.
license: MIT
compatibility: Termux on Android (Bionic libc, usually aarch64). Where a skill says so, also usable from a proot distro.
metadata:
  risk: "low"
  triggers: "termux-api,termux api,termux-battery-status,termux command hangs,termux-notification,termux-clipboard-get,termux-location"
---
# Termux:API

## Purpose
Separate three independent requirements (the Termux:API Android app, the `termux-api` package, and Android runtime permissions) so a failing `termux-*` command is attributed to the right layer.

## When to use
A `termux-*` command that talks to Android (`termux-battery-status`, `termux-clipboard-get`, `termux-notification`, `termux-location`, `termux-sms-send`, `termux-camera-photo`) hangs, prints nothing, or reports a permission error.

## When NOT to use
- Storage links and shared storage: `storage-permissions`.
- Commands inside proot: they are usually unusable there; `proot-boundaries`.
- Core Termux commands such as `termux-wake-lock` and `termux-setup-storage`; they do not need the Termux:API app.

## Preconditions
Native Termux only. Run `sh scripts/check-termux-api.sh`; it is bounded and read-only.

## Decision tree
1. No `termux-*` API binaries on `PATH`: the `termux-api` package is missing in this environment.
2. Binaries exist but calls time out: the Termux:API Android app is missing, stopped, or restricted by battery optimization.
3. App and package both present but calls fail: Termux and plugin apps came from different sources or signing keys. Reinstall them from one source.
4. One command reports a permission error: grant the matching Android runtime permission to Termux:API (location, SMS, camera, contacts, call log) in Android settings. Unix modes are irrelevant.
5. `termux-notification` shows nothing on recent Android: the notification permission for Termux:API may be off (Android 13 and later).
6. `termux-clipboard-get` returns empty while the screen or another app has focus: Android restricts background clipboard reads (Android 10 and later). Retry with Termux in the foreground before blaming the package.
7. Always call with `timeout`, for example `timeout 10 termux-battery-status`, so a missing app cannot block the agent.

## Example
- Situation: termux-battery-status hangs with no output.
- Without the skill: Reinstalls the termux-api package repeatedly.
- With the skill: Wraps the call in `timeout 10`, sees binaries present but the call timing out, and points at the Termux:API app being missing, stopped, or battery-restricted.

## Safety
Many commands expose sensitive data (location, SMS, contacts, call log, clipboard). Request only the one capability the task needs, do not echo results beyond the task, and ask before any command that sends, calls, writes, or notifies.

## Verification
Run one harmless read, `timeout 10 termux-battery-status`, and confirm structured JSON output.

## Handoffs
- `termux-environment` for Android version and Termux source facts.
- `background-processes` when Termux:API is killed or restricted by battery settings.
- `storage-permissions` when the real failure is a path, not an API call.
- `proot-boundaries` when the call was made inside proot.

## Report
Which layer failed (package, app, permission, or foreground restriction), the single user-side action required, and the result of the verification read.
