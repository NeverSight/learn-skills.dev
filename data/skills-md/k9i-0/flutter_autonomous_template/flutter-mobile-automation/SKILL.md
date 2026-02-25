---
name: flutter-mobile-automation
description: E2E testing and mobile automation for Flutter apps. Use when creating/running tests with Maestro, Mobile MCP, and Dart MCP.
---

# Flutter Mobile Automation

Covers both E2E test automation and development workflow automation.

## Recommended Setup: Maestro MCP + Dart MCP

**Maestro MCP + Dart MCP** combination is optimal for Flutter app E2E testing and development automation.

## Dart MCP vs CLI Usage

**Principle: Use MCP for operations requiring DTD connection, CLI for everything else**

### MCP Recommended (No CLI Alternative)

| Operation | Tool | Reason |
|-----------|------|--------|
| Launch app | `launch_app` | Requires DTD URI |
| DTD connection | `connect_dart_tooling_daemon` | MCP only |
| Hot reload | `hot_reload` | Executed via DTD |
| Hot restart | `hot_restart` | Executed via DTD |
| Widget tree | `get_widget_tree` | Only available via DTD |
| Runtime errors | `get_runtime_errors` | Only available via DTD |
| App logs | `get_app_logs` | Get logs from running app |

### CLI Recommended (More Efficient Than MCP)

| Operation | CLI Command | Reason |
|-----------|-------------|--------|
| Device list | `flutter devices` | Simpler output |
| Run tests | `flutter test` | Better output, more options |
| Static analysis | `dart analyze` | Better output |
| Format | `dart format .` | Fast, shows diff |
| Add dependency | `flutter pub add <pkg>` | Interactive |
| Get dependencies | `flutter pub get` | Fast |
| Create project | `flutter create` | More options |
| Build | `flutter build ios/apk` | Detailed output |

### Typical Workflow

```bash
# 1. CLI: Build & Install
flutter build ios --simulator
xcrun simctl install booted build/ios/iphonesimulator/Runner.app

# 2. MCP: Launch app & DTD connection
# -> launch_app -> connect_dart_tooling_daemon

# 3. MCP: Debug during development
# -> get_widget_tree, get_runtime_errors, hot_reload

# 4. CLI: Test & Analyze
flutter test
dart analyze
```

## Tool Overview

### Maestro / Maestro MCP
- E2E testing framework with first-class Flutter support
- **CLI**: Write tests in YAML (`maestro test .maestro/test.yaml`)
- **MCP**: Interactive operation from Claude Code (no YAML needed)
  - Take screenshots
  - Tap operations (text/id specification, no coordinate calculation)
  - Get view hierarchy

### Dart MCP Server
- MCP server for Flutter development integration
- Get widget tree (Flutter internal structure)
- Hot reload/restart
- Get runtime errors

### Mobile MCP (Reference)
- Usually not needed as Maestro MCP can substitute
- Use only for special cases requiring coordinate-based operations

## Claude Code Setup

### Recommended Settings (.claude/settings.json)

Share common permission settings in repository:

```json
{
  "permissions": {
    "allow": [
      "Bash(flutter:*)",
      "Bash(dart:*)",
      "Bash(adb:*)",
      "Bash(xcrun simctl:*)",
      "Bash(maestro:*)",
      "Bash(MAESTRO_DRIVER_STARTUP_TIMEOUT=* maestro:*)",
      "Bash(git:*)",
      "Bash(gh:*)",
      "WebSearch",
      "WebFetch(domain:github.com)",
      "WebFetch(domain:docs.maestro.dev)",
      "mcp__dart-mcp__*",
      "mcp__maestro__*"
    ]
  }
}
```

## Maestro CLI Platform Selection

### Recommended: iOS Simulator

**iOS Simulator** recommended for Maestro CLI execution.

| Platform | launchApp | Stability | Notes |
|----------|-----------|-----------|-------|
| **iOS 18.x** | OK | High | Recommended |
| Android API 30 | Warning | Low | Only works first time, then unstable |
| Android API 34+ | NG | - | TCP forwarding / timeout errors |

### iOS E2E Test Execution

```bash
# Start iOS simulator
xcrun simctl boot "iPhone 16 Pro"

# Build & install iOS app
flutter build ios --simulator
xcrun simctl install booted build/ios/iphonesimulator/Runner.app

# Run test (increased timeout recommended)
MAESTRO_DRIVER_STARTUP_TIMEOUT=120000 \
maestro --device "<DEVICE_ID>" \
  test -e APP_ID=com.example.app \
  .maestro/test.yaml
```

## Flutter + Maestro Best Practices

### Using Semantics Widget

Maestro recognizes elements by semantic information. In Flutter, provide accessibility info with `Semantics` widget:

```dart
// Make identifiable by label
Semantics(
  label: 'submit-button',
  child: ElevatedButton(
    onPressed: _submit,
    child: Text('Submit'),
  ),
)

// Use identifier attribute (Flutter 3.19+)
Semantics(
  identifier: 'login-button',
  child: ElevatedButton(...),
)
```

### Element Specification in Maestro

```yaml
# Recognize by tooltip text (FloatingActionButton etc.)
- tapOn: "Increment"

# Recognize by text
- tapOn: "Submit"

# Regex
- tapOn:
    text: ".*Login.*"

# Using identifier (recommended)
- tapOn:
    id: "login-button"
```

### Semantics Naming Convention (Verified)

```
Pattern: {feature}-{element-type}[-{dynamic-id}]

Static elements:
- todo-fab-add       # FAB
- search-field       # Search field
- save-button        # Save button
- category-chip-work # Category chip

Dynamic elements:
- todo-tile-{uuid}     # Todo tile
- todo-checkbox-{uuid} # Checkbox
```

## Tool Selection Guide

### Feature Comparison

| Feature | Dart MCP | Maestro MCP |
|---------|----------|-------------|
| Widget tree | Detailed (Flutter internal) | - |
| Accessibility info | - | accessibilityText |
| Screenshot | - | Available |
| Element list | - | CSV format |
| Tap operation | Requires setup | Text/id specification |
| Hot reload | Available | - |
| Runtime errors | Available | - |
| E2E scenario | - | YAML / Interactive |

### Recommended Usage

**Maestro MCP** (UI operation & verification)
- Take screenshots
- Tap operations (text specification, no coordinate calculation)
- View hierarchy verification
- Create/run E2E test scenarios

**Dart MCP** (Development & debugging)
- Detailed widget tree verification
- Get runtime errors
- Hot reload/restart
- App launch and DTD connection

### Typical Workflow

```
1. Dart MCP: Launch app -> DTD connection
2. Dart MCP: Check UI structure with widget tree
3. Maestro MCP: Visual verification with screenshot
4. Maestro MCP: Interactive tap operations
5. Maestro CLI: Create/run E2E test scenarios
6. Dart MCP: Check runtime errors on failure
```

## Efficient State Verification Pattern

**Recommended: Prioritize Accessibility Info**

Verify screen state in this order:

1. **inspect_view_hierarchy (First Priority)**
   - Lightweight and fast
   - Get resource-id, accessibilityText, bounds info
   - Sufficient for identifying operation targets

2. **take_screenshot (Only When Needed)**
   - Use only when visual verification is required
   - Layout issues, colors, images
   - Reporting results to user

```
NG: screenshot -> verify -> operate -> screenshot -> ...
OK: hierarchy -> operate -> hierarchy -> ... -> screenshot (final verification)
```

## Development Flow

### Feature Implementation Flow

```
1. Planning (Plan Mode)
   - Start design with EnterPlanMode
   - Clarify questions with AskUserQuestion
   - Write implementation details in plan file
   - Get approval with ExitPlanMode

2. Implementation
   - Break down tasks with TodoWrite
   - Update to completed after each task
   - Minimize code changes

3. E2E Testing
   - Dart MCP: Launch app & DTD connection
   - Maestro MCP: Verify state with inspect_view_hierarchy (lightweight)
   - Maestro MCP: Operate with tap_on / input_text
   - Maestro MCP: Visual verification with take_screenshot (only when needed)

4. Commit & Push
   - Conventional Commits format
   - Commit per feature
   - Push at appropriate timing
```

## References

- [Maestro Flutter Testing](https://docs.maestro.dev/platform-support/flutter)
- [Mobile MCP](https://github.com/mobile-next/mobile-mcp)
- [Dart MCP Server](https://github.com/dart-lang/ai/tree/main/pkgs/dart_mcp_server)
