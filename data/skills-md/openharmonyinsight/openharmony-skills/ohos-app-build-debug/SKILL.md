---
name: ohos-app-build-debug
description: "Build, install, launch, and debug HarmonyOS/OpenHarmony applications using DevEco Studio toolchain. Use when Claude needs to: (1) Build OHOS apps with hvigorw, (2) Install HAP files to devices via hdc, (3) Launch or debug OHOS applications, (4) Parse crash stacks with hstack, (5) Take device screenshots, or (6) Detect DevEco Studio environment and SDK tools. Automatically detects DevEco Studio installation and configures JAVA_HOME, PATH, and toolchain."
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# OHOS App Build & Debug

## When to Use This Skill

Use this skill when the user needs to work with HarmonyOS/OpenHarmony applications:

- **Building**: "Build my OHOS app", "Compile the project", "Run hvigorw"
- **Installing**: "Install this HAP", "Deploy to device", "Install app to device"
- **Launching**: "Launch the app", "Start the application", "Run on device"
- **Debugging**: "Take screenshot", "Parse crash stack", "Debug crash"
- **Environment**: "Check DevEco Studio", "Show SDK path", "Verify tools", "Detect environment"

## Quick Start

Build, install, and launch an OHOS application:

```bash
# Run scripts from skill directory
python3 $SKILL_DIR/scripts/build.py
python3 $SKILL_DIR/scripts/install.py -f entry/build/default/outputs/default/entry-default-signed.hap
python3 $SKILL_DIR/scripts/launch.py
```

## Bundled Resources

This skill includes executable scripts in `scripts/` that automatically detect DevEco Studio environment:

| Script | Purpose |
|--------|---------|
| `build.py` | Build OHOS application using hvigorw |
| `install.py` | Install HAP file to connected device |
| `launch.py` | Launch installed application |
| `screenshot.py` | Capture device screenshot |
| `parse_crash.py` | Parse crash stack using hstack |
| `env_detector.py` | Detect DevEco Studio and tools |
| `ohos_utils.py` | Shared utility functions |

For detailed command reference, see [references/command-reference.md](references/command-reference.md).

## Common Workflows

### Build and Install

```bash
# 1. Check environment
python3 $SKILL_DIR/scripts/env_detector.py

# 2. Build the application
python3 $SKILL_DIR/scripts/build.py

# 3. Install to device (output from build.py shows HAP path)
python3 $SKILL_DIR/scripts/install.py -f entry/build/default/outputs/default/entry-default-signed.hap

# 4. Launch the app
python3 $SKILL_DIR/scripts/launch.py
```

### One-line Build, Install, Launch

```bash
python3 $SKILL_DIR/scripts/build.py && \
python3 $SKILL_DIR/scripts/install.py -f $(find entry/build -name "*.hap" | head -1) && \
python3 $SKILL_DIR/scripts/launch.py
```

### Debug Workflow

```bash
# Launch app
python3 $SKILL_DIR/scripts/launch.py

# Take screenshot to verify
python3 $SKILL_DIR/scripts/screenshot.py -o ./screenshots
```

### Crash Analysis

```bash
# Parse crash stack from file
python3 $SKILL_DIR/scripts/parse_crash.py -f crash.txt

# Parse from string
python3 $SKILL_DIR/scripts/parse_crash.py -c "stack trace here"
```

## How It Works

### Automatic Environment Detection

All scripts automatically detect DevEco Studio installation and configure the environment:

1. **DevEco Studio Detection**
   - Windows: `C:\Program Files\Huawei\DevEco Studio\`
   - macOS: `/Applications/DevEco-Studio.app/`
   - Linux: `~/DevEco-Studio/` or `/opt/DevEco-Studio/`

2. **Toolchain Configuration**
   - Sets `JAVA_HOME` to DevEco's bundled JBR
   - Adds SDK tools to `PATH`
   - Configures `HDC_SERVER_PORT=7035`
   - Caches detection result for 24 hours

3. **Auto-Detected Tools**
   - **Core**: hdc, hvigorw, java
   - **LLVM**: clang, clang++, lld, llvm-*
   - **Profiler**: hiprofiler, hiperf
   - **Other**: hstack, ohpm, idl, restool, syscap_tool

## Response Guidelines

When helping users with OHOS development:

1. **Locate Skill Directory**
   - Replace `$SKILL_DIR` with the actual skill installation path
   - Common locations: `~/.claude/skills/ohos-app-build-debug` or project-specific paths

2. **Execute Scripts**
   - Call Python scripts in `scripts/` directory using absolute or relative paths
   - Always change to the OHOS project directory before running scripts

3. **Show Environment First**
   - Run `env_detector.py` when first building to show tool availability

4. **Provide One-liners**
   - Combine build, install, launch when appropriate for user convenience

5. **Show Actual Commands**
   - Display the hvigorw/hdc commands being executed for transparency

6. **Handle Errors Gracefully**
   - Provide troubleshooting guidance when commands fail
   - Reference [references/troubleshooting.md](references/troubleshooting.md) for detailed help

7. **Use Project Context**
   - Auto-detect bundle names and paths from project structure

## Error Handling

If DevEco Studio is not detected:
- Verify DevEco Studio is installed
- Check standard installation paths
- Set `DEVECO_STUDIO_PATH` environment variable

If device is not connected:
- Check USB cable connection
- Verify USB debugging is enabled on device
- Authorize USB debugging on device when prompted

For detailed troubleshooting, see [references/troubleshooting.md](references/troubleshooting.md).

## Prerequisites

- **DevEco Studio** 3.1+ (4.0+ recommended)
- **OHOS Device** with USB debugging enabled
- **Python** 3.7+ (for running scripts)

Download DevEco Studio: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-download
