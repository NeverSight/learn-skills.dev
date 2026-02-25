---
name: arkweb-app-debug
description: "Debug HarmonyOS ArkWeb applications using Chrome DevTools Protocol. Use when Claude needs to: (1) Start ArkWeb debugging sessions, (2) Connect Chrome DevTools to HarmonyOS apps via hdc, (3) Inspect webview elements, console, and network, (4) Test ArkWeb applications with Chrome DevTools MCP, (5) Troubleshoot webview debugging issues, or (6) Manage port forwarding and debugging sessions. Automatically detects project configuration, device connection, and debugging sockets. Works with ohos-app-build-debug skill for complete workflow."
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# ArkWeb App Debug

## When to Use This Skill

Use this skill when the user needs to debug HarmonyOS ArkWeb (webview) applications:

- **Debugging**: "Debug my webview", "Connect DevTools to app", "Inspect webview"
- **Testing**: "Test the web page", "Automate webview testing", "Check webview elements"
- **Troubleshooting**: "Webview not working", "Can't connect DevTools", "Socket not found"
- **Inspection**: "Show me webview console", "Inspect network requests", "Check web elements"

## Quick Start

Start an ArkWeb debugging session:

```bash
# Using the debug script (auto-configures environment)
$SKILL_DIR/scripts/start-debug.sh

# Or with explicit package name
$SKILL_DIR/scripts/start-debug.sh --package com.example.app
```

## Bundled Resources

This skill includes debugging scripts in `scripts/`:

| Script | Purpose |
|--------|---------|
| `start-debug.sh` | Start debugging session (macOS/Linux, auto-configures environment) |
| `start-debug.py` | Start debugging session (cross-platform Python) |
| `start-debug.bat` | Start debugging session (Windows, auto-configures environment) |

All scripts automatically:
- Detect DevEco Studio installation (via ohos-app-build-debug skill)
- Configure environment for hdc and other tools
- Find HarmonyOS project configuration
- Connect to device and create port forwarding
- Open Chrome DevTools on http://127.0.0.1:9222

For detailed documentation, see [references/](references/).

## Common Workflows

### Start Debugging Session

```bash
# Run the debug script from your HarmonyOS project directory
cd /path/to/harmonyos/project
$SKILL_DIR/scripts/start-debug.sh

# The script automatically:
# - Detects project configuration (package name, HAP path)
# - Connects to device
# - Creates port forwarding to webview_devtools socket
# - Opens Chrome DevTools
```

### Integration with ohos-app-build-debug

For complete development workflow:

```bash
# 1. Build and install app (using ohos-app-build-debug skill)
$OHOS_SKILL_DIR/scripts/build.py
$OHOS_SKILL_DIR/scripts/install.py -f entry/build/default/outputs/default/entry-default-signed.hap
$OHOS_SKILL_DIR/scripts/launch.py

# 2. Start debugging (this skill)
$SKILL_DIR/scripts/start-debug.sh
```

### AI Automated Testing (with MCP)

When Chrome DevTools MCP is configured, Claude can automatically test webview functionality:

```
User: Please test the login functionality in my webview
Claude: (Automatically uses Chrome DevTools MCP)
  - Opens DevTools connection
  - Navigates to login page
  - Fills out form
  - Submits and verifies results
```

See [references/mcp-guide.md](references/mcp-guide.md) for MCP setup and available tools.

## How It Works

### Automatic Detection

The debug scripts automatically:

1. **Detect DevEco Studio**: Uses ohos-app-build-debug skill to find DevEco Studio and configure hdc
2. **Find Project**: Searches upward for HarmonyOS project root (max 5 levels)
3. **Read Configuration**: Extracts package name from `AppScope/app.json5`
4. **Connect Device**: Uses hdc to connect to HarmonyOS device
5. **Find Socket**: Dynamically locates webview_devtools socket (handles PID changes)
6. **Create Port Forward**: Sets up port forwarding from device to localhost:9222
7. **Open DevTools**: Launches Chrome/Chromium with DevTools

### Critical Timing

Based on real debugging experience:
- **After app start**: Wait 10 seconds for Web component to create debugging socket
- **After port forward**: Wait 2 seconds for socket initialization
- **Socket finding**: Retry every 2 seconds for up to 15 seconds

The scripts handle these timings automatically.

## Response Guidelines

When helping users with ArkWeb debugging:

1. **Check Environment First**
   - Verify hdc is available (should be auto-detected by scripts)
   - Check device connection: `hdc list targets`
   - Ensure app has `setWebDebuggingAccess(true)` in `aboutToAppear()`

2. **Use Scripts**
   - Call scripts in `scripts/` directory
   - Replace `$SKILL_DIR` with actual skill installation path
   - Replace `$OHOS_SKILL_DIR` with ohos-app-build-debug skill path

3. **Handle Common Issues**
   - **Socket not found**: Wait 10-15s for app initialization, ensure Web component rendered
   - **Port in use**: Previous session may be running, check with `hdc fport list`
   - **Device not found**: Check USB connection and authorization
   - **hdc not found**: Scripts should auto-detect via ohos-app-build-debug

4. **Coordinate with ohos-app-build-debug**
   - For build/install issues, use ohos-app-build-debug skill
   - This skill focuses on debugging only

5. **Show Actual Commands**
   - Display the hdc commands being executed for transparency
   - Show port forwarding setup
   - Indicate DevTools URL

## Application Requirements

ArkWeb applications **must** enable debugging in `aboutToAppear()`:

```typescript
import { webview } from '@kit.ArkWeb';

@Entry
@Component
struct Index {
  controller: webview.WebviewController = new webview.WebviewController();

  aboutToAppear() {
    // CRITICAL: Enable debugging BEFORE Web component renders
    webview.WebviewController.setWebDebuggingAccess(true);
  }

  build() {
    Web({ src: this.currentUrl, controller: this.controller })
  }
}
```

## Error Handling

If DevEco Studio/hdc is not detected:
- Verify DevEco Studio is installed
- Ensure ohos-app-build-debug skill is available
- Scripts will attempt to auto-configure environment

If device is not connected:
- Check USB cable connection
- Verify USB debugging is enabled on device
- Authorize USB debugging on device when prompted

If socket is not found:
- Ensure app has `setWebDebuggingAccess(true)` in code
- Wait 10-15 seconds for app to fully initialize
- Verify Web component has rendered (navigate to a URL)
- Check if app crashed: `hdc shell ps -A | grep <package>`

For detailed troubleshooting, see [references/troubleshooting.md](references/troubleshooting.md).

## Prerequisites

- **DevEco Studio** 3.1+ (4.0+ recommended) OR **hdc** in PATH
- **HarmonyOS device** with USB debugging enabled
- **ArkWeb app** with `setWebDebuggingAccess(true)` enabled
- **Python** 3.8+ (for start-debug.py script)
- **Chrome/Chromium** browser (for DevTools)

Optional: **Chrome DevTools MCP** for AI automated testing

Download DevEco Studio: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-download
