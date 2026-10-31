---
name: xcode-build-simulator
description: 'This skill should be used when the user invokes "/xcode-build-simulator" to build the current Xcode project for the iOS Simulator (generic destination).'
tools: Bash
disable-model-invocation: true
---

# Build Xcode project for iOS Simulator

Build the Xcode workspace or project under the current working directory for the iOS Simulator. Uses a *generic* simulator destination (no specific UDID), so no simulator needs to be booted.

## How to build

The shared `agent-skill-xcode.el` lives in the sibling `xcode-shared` directory at `skills/xcode-shared/agent-skill-xcode.el` in the emacs-skills plugin. All four `/xcode-*` skills load it from there.

```sh
emacsclient --eval "(progn (load \"/path/to/skills/xcode-shared/agent-skill-xcode.el\" nil t) (agent-skill-xcode-build-simulator :project-dir \"$(pwd)\"))"
```

The function:
- Locates the first `.xcworkspace` (preferred) or `.xcodeproj` in `:project-dir`.
- Picks a scheme via `xcodebuild -list -json`: prefers the scheme matching the project basename, else the first non-test scheme.
- Runs `xcodebuild build -destination 'generic/platform=iOS Simulator'`.
- Returns `"Build succeeded: ..."` on success, or `"Build FAILED: ...\n--- last 40 lines ---\n..."` on failure.

## Rules

- Pass the agent's current working directory as `:project-dir` via `$(pwd)`. Do not assume a hard-coded path.
- Run via the Bash tool with a single `emacsclient --eval` invocation.
- Report the returned status string to the user verbatim on failure (truncated tail is already included).
- On success, a one-line confirmation is enough.
- If the user wants to also run the app, suggest `/xcode-run-simulator`.
