---
name: flutter-control-and-screenshot
description: Guide on how to control a Flutter app using flutter_driver via MCP and capture screenshots.
---

# Flutter Driver Control & Screenshot

This skill outlines the process of adding `flutter_driver` support to a Flutter application, launching it via the Dart MCP server, controlling it (tapping, finding widgets), and capturing screenshots (handling Web/Desktop specific constraints).

## Prerequisites

1.  **Dart MCP Server**: Ensure the `dart-mcp-server` is active.
2.  **Flutter Project**: You need a working Flutter project.

## Step 1: Add Dependency

Add `flutter_driver` to the `dev_dependencies` in your `pubspec.yaml`.

```yaml
dev_dependencies:
  flutter_driver:
    sdk: flutter
```

Run `dart pub get` or use the `mcp_dart-mcp-server_pub` tool.

## Step 2: Create Driver Entry Point

Create a separate entry point, typically `test_driver/app.dart`, to enable the driver extension without polluting `main.dart`.

> [!IMPORTANT]
> Replace `your_app_package_name` with the actual name of your package as defined in `pubspec.yaml`.

```dart
// test_driver/app.dart
import 'package:flutter_driver/driver_extension.dart';
import 'package:your_app_package_name/main.dart' as app; // Import your main app

void main() {
  // Enable the extension
  enableFlutterDriverExtension();

  // Run the app
  app.main();
}
```

## Step 3: Launch App via MCP

Use the `mcp_dart-mcp-server_launch_app` tool.

-   `target`: `test_driver/app.dart`
-   `device`: `chrome` (or `macos`, `linux`, `windows`)
-   `root`: Absolute path to your project root.

**Note**: The tool returns a **DTD URI** (Data Tooling Daemon) and a PID. Save these.

## Step 4: Connect to DTD

Use `mcp_dart-mcp-server_connect_dart_tooling_daemon` with the URI returned from the launch step.

```json
{
  "uri": "ws://127.0.0.1:..."
}
```

## Step 5: Web Screenshot Strategy (Browser Subagent)

If running on **Web (Chrome)**, `flutter_driver`'s screenshot command may not work or may not be supported directly in all environments. A robust fallback is to use the `browser_subagent`.

1.  **Get App URL**: Use `mcp_dart-mcp-server_get_app_logs` with the app's PID. Look for lines like `A Dart VM Service on Chrome is available at: http://127.0.0.1:XXXXX`. The app logs usually contain the local HTTP URL.
2.  **Navigate & Snapshot**: Call `browser_subagent`.
    -   **Task**: "Navigate to [URL]. Wait for render. Take a screenshot."

## Step 6: Control the App (Flutter Driver)

Use `mcp_dart-mcp-server_flutter_driver` to interact with the app.

-   **Get Widget Tree**: `mcp_dart-mcp-server_get_widget_tree` (useful to find keys/labels).
-   **Tap**:
    ```json
    {
      "command": "tap",
      "finderType": "ByText",
      "text": "Settings"
    }
    ```
-   **Scroll**, **Enter Text**, etc. are also available.

## Step 7: Cleanup

Always stop the app when done to free up ports and resources.

-   Use `mcp_dart-mcp-server_stop_app` with the PID.

## Example Workflow

1.  **Launch** `test_driver/app.dart`.
2.  **Connect** DTD.
3.  **Log Check**: Find localhost URL.
4.  **Browser Subagent**: Navigate & Screenshot (Home/Dashboard).
5.  **Flutter Driver**: Tap "Tasks" tab.
6.  **Browser Subagent**: Screenshot (Tasks).
7.  **Flutter Driver**: Tap "Settings" tab.
8.  **Browser Subagent**: Screenshot (Settings).
9.  **Stop App**.
