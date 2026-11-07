---
name: xcode-build-device
description: 'This skill should be used when the user invokes "/xcode-build-device" to build the current Xcode project for a physical iOS device (generic destination).'
tools: Bash
disable-model-invocation: true
---

# Build Xcode project for iOS device

Build the Xcode workspace or project under the current working directory for a physical iOS device. Uses a *generic* device destination (no specific UDID). Requires a configured signing team in the project — otherwise `xcodebuild` will fail with a code-signing error.

## How to build

The shared `agent-skill-xcode.el` lives in the sibling `xcode-shared` directory at `skills/xcode-shared/agent-skill-xcode.el` in the emacs-skills plugin. All four `/xcode-*` skills load it from there.

```sh
emacsclient --eval "(progn (load \"/path/to/skills/xcode-shared/agent-skill-xcode.el\" nil t) (agent-skill-xcode-build-device :project-dir \"$(pwd)\"))"
```

The function:
- Locates the first `.xcworkspace` (preferred) or `.xcodeproj` in `:project-dir`.
- Picks a scheme via `xcodebuild -list -json`.
- Runs `xcodebuild build -destination 'generic/platform=iOS'`.
- Returns `"Build succeeded: ..."` on success, or `"Build FAILED: ...\n--- last 40 lines ---\n..."` on failure.

## Rules

- Pass the agent's current working directory as `:project-dir` via `$(pwd)`. Do not assume a hard-coded path.
- The shared elisp lives under `xcode-shared/agent-skill-xcode.el` — load it from there, not from this skill's directory.
- Run via the Bash tool with a single `emacsclient --eval` invocation.
- Report the returned status string verbatim on failure.
- If the failure mentions code signing, point the user to Xcode → target → Signing & Capabilities → Team. Don't try to fix signing automatically.
- If the user wants to also run the app on-device, suggest `/xcode-run-device`.
