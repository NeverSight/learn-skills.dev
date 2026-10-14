---
name: control-ui
description: Drive and inspect a requested UI using the active host’s browser or desktop
  controls, collecting evidence from the actual affected surface.
license: MIT
---

# Control UI

Read [the runtime contract](../hap-mode/references/runtime.md). Use browser/desktop controls supplied by the active host. Inspect the affected surface before interacting; prefer observed accessible locators over coordinates. On T3 start with `preview_status`, then `preview_open` if needed, and use the collaborative preview tools. Respect human tab ownership and explicitly requested or repository-required browser workflows.

For a bug, reproduce the reported behavior, gather the smallest useful evidence, make authorized changes, and repeat the same interaction. For a visual task, inspect only the affected screen and capture its relevant state. A generated mockup, successful build, or another agent's report does not prove the real UI works.

Use native app/simulator controls only when that surface is available. Report missing access, authentication, or device controls and what was inspected. Never claim a browser check verifies a native app. Use available authorized controls as far as possible before asking for user-provided screenshots.

Do not submit messages, transactions, deployments, or other external writes as tests without authority for that action. Exclude credentials and private screenshots from public artifacts.
