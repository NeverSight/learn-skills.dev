---
name: run
description: Run the Keychat app on a device or simulator
argument-hint: "[device-id]"
disable-model-invocation: true
allowed-tools: Bash(flutter *)
---

Run the Keychat app on a device or simulator.

## Arguments
- `$ARGUMENTS` - Optional: device ID to run on

## Workflow

1. First list available devices:
   ```bash
   flutter devices
   ```

2. If `$ARGUMENTS` is provided, run on that device:
   ```bash
   cd packages/app && flutter run -d $ARGUMENTS
   ```

3. If no device specified:
   - If only one device is available, use it
   - If multiple devices, show the list and ask user to specify

## Alternative entry points

The app has multiple entry points for different environments:
- `lib/main.dart` - Production
- `lib/main_dev1.dart` - Development 1
- `lib/main_dev2.dart` - Development 2
- `lib/main_dev3.dart` - Development 3

To run with a specific entry point:
```bash
cd packages/app && flutter run -d <device> -t lib/main_dev1.dart
```
