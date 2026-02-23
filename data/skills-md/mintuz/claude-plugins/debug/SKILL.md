---
name: debug
description: WHEN users express issues with app behavior, visual appearance, or functionality in the iOS simulator collaborate on fixes with a structured feedback loop.
---

# Debug - iOS App Debugging Loop

Use XcodeBuildMCP and ios-simulator MCPs to diagnose issues, capture app state, and collaborate with users on fixes. Always confirm before making changes.

## Workflow

1. **Capture current state** — Use ios-simulator to capture screenshots and understand the current visual state of the app. Use XcodeBuildMCP to read build logs and runtime errors.

2. **Gather diagnostic information** — Collect relevant information:

   - Screenshot of the issue using ios-simulator
   - Console logs and error messages from XcodeBuildMCP
   - App state and behavior observations
   - Ask: "Looking at this screenshot and these logs, can you describe exactly what's wrong or what you expected to happen?"

3. **Analyze the problem** — Review the captured information:

   - Identify error patterns in logs
   - Compare visual output to expected behavior
   - Locate relevant code sections that might be causing the issue

4. **Propose changes clearly** — Describe intended fixes with specifics:

   - Bad: "I'll fix the layout"
   - Good: "I'll update the VStack spacing from 8 to 16 points and add .padding(.horizontal, 20) to fix the alignment issue shown in the screenshot"

5. **Confirm before implementing** — Use AskUserQuestion to get explicit approval. Never modify code without confirmation.

6. **Verify with comparison** — After changes:
   - Rebuild the app using XcodeBuildMCP
   - Capture a new screenshot to confirm the fix
   - Check logs to ensure errors are resolved
   - Ask: "Does this match what you were looking for?"

## XcodeBuildMCP Tools

Use these XcodeBuildMCP tools for building and analyzing:

- `build` — Build the Xcode project/workspace
- `get-build-logs` — Retrieve build logs to diagnose compilation errors
- `get-runtime-logs` — Get runtime logs from the running app
- `clean` — Clean build artifacts before rebuilding
- `test` — Run unit tests to verify fixes

## ios-simulator Tools

Use these ios-simulator tools for app interaction and state capture:

- `launch-app` — Launch the app in the simulator
- `take-screenshot` — Capture the current simulator screen
- `tap` — Tap at specific coordinates on the screen
- `swipe` — Perform swipe gestures
- `enter-text` — Type text into focused text fields
- `get-device-info` — Get simulator device information
- `install-app` — Install the app on the simulator
- `uninstall-app` — Uninstall the app from the simulator

## Related Skills

When implementing fixes, load these skills for guidance:

- **`app:swiftui-architecture`** — SwiftUI patterns, state management, and architectural guidance
- **`app:swift-testing`** — Testing patterns and best practices

## Debugging Workflow Example

1. User reports: "The login button doesn't work"
2. Capture screenshot showing the button
3. Check runtime logs for tap events or errors
4. Identify the issue in code (e.g., missing action binding)
5. Propose fix: "I'll connect the button's action to the LoginIntent as defined in app-intent-driven-development"
6. Get confirmation
7. Implement fix
8. Rebuild app
9. Take new screenshot showing working button
10. Verify logs show successful tap handling

## Before/After Verification

After implementing changes:

1. Rebuild the app with XcodeBuildMCP
2. Launch the updated app in the simulator
3. Take a new screenshot of the same view
4. Compare build/runtime logs (before and after)
5. Present screenshots side by side
6. Ask: "Does this resolve the issue?"
7. If not, repeat the feedback loop
