---
name: xcode-run-simulator
description: 'This skill should be used when the user invokes "/xcode-run-simulator" to build the current Xcode project, install the app on an iOS Simulator, and launch it.'
tools: Bash
disable-model-invocation: true
---

# Build + run on iOS Simulator

Build the Xcode workspace or project under the current working directory and launch it on an iOS Simulator. If a simulator is already booted, that one is used. Otherwise the latest available iPhone simulator is booted automatically and `Simulator.app` is brought to the foreground.

## How to run

The shared `agent-skill-xcode.el` lives in the sibling `xcode-shared` directory at `skills/xcode-shared/agent-skill-xcode.el` in the emacs-skills plugin. All four `/xcode-*` skills load it from there.

```sh
emacsclient --eval "(progn (load \"/path/to/skills/xcode-shared/agent-skill-xcode.el\" nil t) (agent-skill-xcode-run-simulator :project-dir \"$(pwd)\"))"
```

The function:
- Locates the workspace/project and picks a scheme (same heuristic as `/xcode-build-simulator`).
- Picks a simulator: first booted iOS simulator if any; else the latest available iPhone (boots it and opens Simulator.app).
- Runs `xcodebuild build` against the simulator's specific UDID.
- Reads `BUILT_PRODUCTS_DIR` / `WRAPPER_NAME` / `PRODUCT_BUNDLE_IDENTIFIER` from `-showBuildSettings -json`.
- Installs (`xcrun simctl install`) and launches (`xcrun simctl launch`).
- Returns a multi-line status string with the bundle id, simulator UDID, .app path, install result, and launch result. On build failure, returns the same error format as `/xcode-build-simulator`.

## Rules

- Pass the agent's current working directory as `:project-dir` via `$(pwd)`.
- The shared elisp lives under `xcode-shared/agent-skill-xcode.el` — load it from there.
- Run via the Bash tool with a single `emacsclient --eval` invocation. Builds can take minutes; consider extending the Bash timeout if known to be slow.
- Report the returned status string verbatim. It already contains everything the user needs.
- Do not try to choose a different simulator if one is already booted — the whole point is reuse.
- If the build fails, point at the truncated tail in the output; do not re-run the build.
