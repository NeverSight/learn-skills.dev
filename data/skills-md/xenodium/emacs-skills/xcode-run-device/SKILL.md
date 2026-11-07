---
name: xcode-run-device
description: 'This skill should be used when the user invokes "/xcode-run-device" to build the current Xcode project, install the app on a connected iOS device, and launch it.'
tools: Bash
disable-model-invocation: true
---

# Build + run on a connected iOS device

Build the Xcode workspace or project under the current working directory and launch it on a wired-connected iOS device via Xcode 15+ `devicectl`. Requires a configured signing team in the project and a trusted, paired device.

## How to run

The shared `agent-skill-xcode.el` lives in the sibling `xcode-shared` directory at `skills/xcode-shared/agent-skill-xcode.el` in the emacs-skills plugin. All four `/xcode-*` skills load it from there.

```sh
emacsclient --eval "(progn (load \"/path/to/skills/xcode-shared/agent-skill-xcode.el\" nil t) (agent-skill-xcode-run-device :project-dir \"$(pwd)\"))"
```

The function:
- Locates the workspace/project and picks a scheme.
- Locates the first connected device via `xcrun devicectl list devices -j`.
- Runs `xcodebuild build` against the device's specific UDID.
- Reads `BUILT_PRODUCTS_DIR` / `WRAPPER_NAME` / `PRODUCT_BUNDLE_IDENTIFIER` from `-showBuildSettings -json`.
- Installs (`xcrun devicectl device install app`) and launches (`xcrun devicectl device process launch`).
- Returns a multi-line status string. On build failure, returns the same error format as `/xcode-build-device`.

## Rules

- Pass the agent's current working directory as `:project-dir` via `$(pwd)`.
- The shared elisp lives under `xcode-shared/agent-skill-xcode.el` — load it from there.
- Run via the Bash tool with a single `emacsclient --eval` invocation. Builds can take minutes; consider extending the Bash timeout if known to be slow.
- Report the returned status string verbatim.
- If the function signals "No connected iOS device found", tell the user to plug in a device and trust the Mac on it.
- If the build fails with a code-signing error, point them at Xcode → target → Signing & Capabilities → Team. Don't try to fix signing automatically.
- Requires Xcode 15+ for `devicectl`. If `xcrun devicectl` is missing, tell the user to update Xcode.
