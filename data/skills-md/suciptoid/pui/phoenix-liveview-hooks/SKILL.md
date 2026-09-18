---
name: phoenix-liveview-hooks
description: Implement Phoenix LiveView JavaScript hooks correctly. Use when adding or reviewing `phx-hook` behavior in HEEx, choosing between colocated hook scripts and external hooks in `assets/js`, wiring hook registration into `LiveSocket`, or enforcing hook safety rules like unique IDs and `phx-update=\"ignore\"` for DOM-managed nodes.
---

# LiveView Hooks

Use this skill to choose and implement the right LiveView hook pattern.

## Quick Decision

1. Use a colocated hook when behavior is local to one template and should ship with that HEEx file.
2. Use an external hook when behavior is reused across multiple pages/components.

## Colocated Hook Pattern

1. Add a unique element id and a dot-prefixed hook name on the element.
2. Add a colocated script block with `:type={Phoenix.LiveView.ColocatedHook}`.
3. Keep the hook name dot-prefixed (example: `.PhoneNumber`).
4. Do not use raw `<script>` tags in HEEx.

Reference example: `references/liveview-js-hooks.md` (`Inline colocated js hooks`).

## External Hook Pattern

1. Define hook object in `assets/js`.
2. Register it in `LiveSocket` under `hooks`.
3. Use the hook via `phx-hook="HookName"` on elements with stable DOM ids.
4. If the hook manages its own DOM updates, set `phx-update="ignore"` on that node.

Reference example: `references/liveview-js-hooks.md` (`External phx-hook`).

## Interop Rules

1. Always provide a unique DOM id for elements with `phx-hook`.
2. Rebind or return the socket from `push_event/3` calls.

See complete extracted guidance and examples in `references/liveview-js-hooks.md`.
