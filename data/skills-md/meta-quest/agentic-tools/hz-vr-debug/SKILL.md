---
name: hz-vr-debug
license: Apache-2.0
description: "Debugs Meta VR and Horizon OS VR, MR, and Android applications using the metavr CLI — view logs, capture screenshots, and diagnose common issues. Use when troubleshooting crashes, errors, or unexpected behavior on Meta VR devices. Build paths: All; use hz-quest-verify-first if the path is unclear."
allowed-tools: Bash(metavr:*), Bash(hzdb:*), Bash(npx:*)
---

# VR Debug Skill

Debug Meta VR, MR, and Android applications using the `metavr` command-line
interface. This skill covers viewing application logs, capturing device state,
diagnosing crashes, and resolving common issues encountered during Meta VR
development.

## When to Use This Skill

Use this skill when you need to:

- Debug an application running on a connected Meta VR device
- View real-time or historical application logs (logcat)
- Capture screenshots of the VR/MR view
- Diagnose application crashes, rendering glitches, or performance problems
- Investigate tracking, controller, audio, or permission issues
- Pull diagnostic files from the device for offline analysis

This skill is relevant for Meta VR Glasses and Meta Quest headsets (Quest 2, Quest 3, Quest 3S, Quest Pro) running Horizon OS.

## Prerequisites

Before using this skill, ensure the following are in place:

1. **metavr CLI installed** -- Install the standalone `metavr` CLI binary on your PATH (see the `metavr-cli` skill), or invoke it on demand via `npx` with no install:
   ```bash
   metavr --version
   ```
   metavr wraps ADB and adds Meta VR-specific device management, log viewing, screenshot capture, and file management. Examples below use the bare `metavr` command. If `metavr` is not on PATH, invoke the same CLI via `npx -y metavr <args>` (published as the npm package `metavr`).
2. **Meta VR device connected via USB** -- Use a USB-C cable that supports data transfer (not charge-only).
3. **Developer mode enabled** -- Developer mode must be turned on in the Meta Horizon app on your phone, under your headset's settings.
4. **ADB authorization accepted** -- The first time you connect, you must put on the headset and accept the "Allow USB debugging" prompt.

## Quick Start Workflow

The fastest way to begin debugging a Meta VR application:

```bash
# 1. Verify the device is connected and recognized
metavr device list

# 2. List applications currently installed
metavr app list

# 3. View live logs (most recent 100 lines)
metavr log

# 4. Capture a screenshot of the current VR view
metavr capture screenshot
```

If `metavr device list` returns no devices, check the USB cable, developer mode, and ADB authorization.

## Key Debugging Commands

### Device Commands

| Command                    | Description                                      |
| -------------------------- | ------------------------------------------------ |
| `metavr device list`         | List all connected Meta VR devices             |
| `metavr device info <id>`    | Show device model, OS version, and more          |
| `metavr device battery`      | Show battery level and charging status           |
| `metavr device wake`         | Wake the device from sleep                       |
| `metavr device reboot`       | Reboot the device                                |
| `metavr device connect <ip>` | Connect to a device over WiFi                    |

### Log Commands

| Command                              | Description                                    |
| ------------------------------------ | ---------------------------------------------- |
| `metavr log`                           | View the last 100 log lines                    |
| `metavr log -n 500`                    | View the last 500 log lines                    |
| `metavr log --tag Unity`               | Filter logs by tag                             |
| `metavr log --level E`                 | Filter by severity (V, D, I, W, E, F)          |
| `metavr adb logcat`                    | Full logcat with advanced filtering options    |
| `metavr adb logcat --follow`           | Stream logs continuously                       |

### Application Commands

| Command                          | Description                                    |
| -------------------------------- | ---------------------------------------------- |
| `metavr app list`                  | List installed applications                    |
| `metavr app info <package>`        | Show detailed info about an app                |
| `metavr app launch <package>`      | Launch an application by package name          |
| `metavr app stop <package>`        | Force-stop a running application               |
| `metavr app clear <package>`       | Clear application data and cache               |
| `metavr app install <apk>`         | Install an APK to the device                   |
| `metavr app uninstall <package>`   | Uninstall an application                       |

### Capture Commands

| Command                              | Description                                        |
| ------------------------------------ | -------------------------------------------------- |
| `metavr capture screenshot`            | Capture a screenshot of the current VR/MR view     |
| `metavr capture screenshot -o file.png`| Save screenshot to a specific file                 |

### File Commands

| Command                                          | Description                              |
| ------------------------------------------------ | ---------------------------------------- |
| `metavr files ls /sdcard/`                         | List files on the device                 |
| `metavr files pull /sdcard/path/file ./local/`     | Pull a file from the device              |
| `metavr files push ./local/file /sdcard/path/`     | Push a file to the device                |
| `metavr files rm /sdcard/path/file`                | Delete a file on the device              |
| `metavr files mkdir /sdcard/path/dir`              | Create a directory on the device         |

## Common Debugging Workflow

A typical debugging session follows this pattern:

### 1. Connect and Verify

```bash
metavr device list
metavr device info <device_id>
```

Confirm the device is recognized, check the OS version, and note the battery level. A low battery can cause thermal throttling that affects performance tests.

### 2. Identify the Application

```bash
metavr app list
```

Find the package name for the application you want to debug. Package names typically follow the pattern `com.company.appname`.

### 3. Reproduce and Capture Logs

```bash
# Start logging before reproducing the issue
metavr adb logcat --follow
```

Put on the headset and reproduce the issue. The logs stream in real time to your terminal. Press Ctrl+C to stop.

### 4. Capture Visual State

```bash
# Take a screenshot at the moment of the issue
metavr capture screenshot
```

### 5. Analyze and Diagnose

Review the captured logs for errors, warnings, and crash signatures. Look for:

- `FATAL EXCEPTION` -- Unhandled Java/Kotlin exceptions
- `native crash` or `SIGABRT` / `SIGSEGV` -- Native code crashes
- `ANR` -- Application Not Responding (frozen UI thread)
- `OOM` or `OutOfMemoryError` -- Memory exhaustion

### 6. Iterate

Make code changes, rebuild, deploy, and test again:

```bash
metavr app stop com.example.myapp
metavr app launch com.example.myapp
metavr log --tag Unity --level W
```

## Symptom-to-Diagnosis Decision Trees

When a developer reports a problem, use these decision trees to systematically diagnose the root cause. Start with the reported symptom and follow the branches.

The general Android crash, ANR, memory, and logcat branches apply to every build
path. Use branches involving VrApi, OpenXR sessions, immersive frame rates,
tracking, controllers, or spatial audio only for an immersive VR or MR app. For
a Standard Android panel app, stay with the Android application, rendering,
layout, and input branches.

### App Crashes on Launch

```
App crashes on launch
├── Does `metavr app launch <pkg>` show "Error: Activity not found"?
│   └── YES → Package name is wrong or app is not installed.
│       Run `metavr app list` to verify the correct package name.
├── Does logcat show `FATAL EXCEPTION` in the first 5 seconds?
│   ├── YES, with `ClassNotFoundException` or `NoClassDefFoundError`
│   │   └── Missing native library or wrong ABI. Check the APK is built for ARM64.
│   │       Run: `metavr adb shell getprop ro.product.cpu.abi` → must show "arm64-v8a"
│   ├── YES, with `SecurityException` or `Permission denied`
│   │   └── Missing manifest permission. Check the logcat message for which permission.
│   │       Common: hand tracking, scene, camera permissions not declared.
│   └── YES, with `NullPointerException` or other Java exception
│       └── Application code bug. Read the stack trace for the failing class and method.
├── Does logcat show `native crash` / `SIGSEGV` / `SIGABRT`?
│   ├── Check if the crash is in a Unity/Unreal library (libunity.so, libUE4.so)
│   │   └── Engine bug or incompatible SDK version. Check Meta XR SDK release notes
│   │       for known issues with your engine version.
│   └── Check if the crash is in your own native code
│       └── Debug with `metavr adb logcat --buffer crash` for the tombstone, then use
│           `addr2line` or `ndk-stack` on the crash address.
└── No crash visible in logs?
    └── Check if the app is being killed by the system.
        Run: `metavr adb logcat --tag ActivityManager --level W`
        Look for "Force stopping" or "Process died" messages. Common cause: OOM killer
        triggered by excessive memory usage on launch.
```

### App Freezes / ANR (Application Not Responding)

```
App freezes or ANR dialog appears
├── Does logcat show "ANR in <package>"?
│   ├── YES, with "Reason: Input dispatching timed out"
│   │   └── The main/UI thread is blocked. Check for:
│   │       - Synchronous network calls on the main thread
│   │       - Large file I/O on the main thread
│   │       - Deadlocks between threads
│   │       Run: `metavr adb shell kill -3 <pid>` to dump thread stacks, then
│   │       `metavr files pull /data/anr/traces.txt ./` to retrieve the ANR trace.
│   └── YES, with "Reason: executing service"
│       └── A background service is taking too long. Check the service implementation.
└── No ANR, but app appears frozen?
    ├── Is the render loop still running? (Check VrApi logs for frame submission)
    │   ├── YES → The app is rendering but not processing input. Check input system.
    │   └── NO → The render thread is blocked or crashed silently.
    │       Check: `metavr adb logcat --tag VrApi` for "FPS" lines stopping.
    └── Is the device overheating?
        Run: `metavr device battery` — if battery temperature > 40°C, thermal
        throttling may have halted the app. Let device cool down and retry.
```

### Black Screen in Headset

```
Black screen after app launch
├── Is the app actually running?
│   Run: `metavr adb shell pidof <package>` — if empty, app crashed silently.
│   └── Check crash logs: `metavr adb logcat --buffer crash`
├── Is VrApi initialized?
│   Check: `metavr adb logcat --tag VrApi | grep "VrApi" | head -20`
│   ├── No VrApi output → XR session never started. Check OpenXR/OVR initialization code.
│   └── VrApi output exists → Frames are being submitted but may be empty.
│       └── Check: rendering pipeline, camera setup, shader compilation errors.
├── Unity-specific: "Shader compiler" or "Compiling shaders" in logs?
│   └── Shader warmup can cause a black screen for several seconds on first launch.
│       Use shader prewarming/variant preloading to avoid this.
└── Is the correct rendering API being used?
    Check: `metavr adb logcat --tag Unity --level E` for Vulkan/GLES errors.
    Quest requires OpenGL ES 3.0 minimum. Vulkan is preferred on Quest 3.
```

### Frame Drops / Stuttering

```
App stutters or drops frames
├── Check current FPS:
│   `metavr adb logcat --tag VrApi | grep FPS`
│   ├── FPS consistently below 72 → GPU or CPU bottleneck.
│   │   ├── Check GPU: use Perfetto or OVR Metrics Tool. Look for GPU completion
│   │   │   time > 13.8ms (72Hz) or > 11.1ms (90Hz).
│   │   └── Check CPU: look for game thread or render thread exceeding frame budget.
│   └── FPS mostly stable but periodic drops
│       ├── Check for GC pauses: `metavr adb logcat --tag dalvikvm --level D`
│       │   or `metavr adb logcat --regex "GC_|clamp"` → reduce allocations per frame.
│       ├── Check for thermal throttling: `metavr adb logcat --tag ThermalService --level W`
│       │   → sustained heavy load causes CPU/GPU frequency reduction.
│       └── Check for asset loading on main thread: large textures or models loaded
│           synchronously will cause frame spikes. Use async loading.
└── Only stutters in specific scenes?
    └── Profile that scene. Common causes: too many draw calls (>100), unculled
        off-screen geometry, expensive shaders, excessive overdraw, uncompressed textures.
```

### Tracking Issues

```
Controllers or hands not tracking correctly
├── Are controllers paired and connected?
│   `metavr device info <id>` — check controller connection status.
├── Is hand tracking enabled in device settings?
│   Check: Settings > Movement Tracking > Hand and Body Tracking.
├── Does the app request the correct tracking mode?
│   ├── For hand tracking: manifest must include
│   │   `com.oculus.permission.HAND_TRACKING` and
│   │   `com.oculus.handtracking.frequency` set to "HIGH" if needed.
│   └── For controller tracking: ensure the app is not forcing hand-tracking-only mode.
└── Tracking works but is jittery or delayed?
    ├── Check lighting: tracking cameras need adequate, even lighting. Very bright
    │   or very dim environments degrade tracking quality.
    └── Check for occlusion: hands or controllers held outside the tracking camera
        FOV will lose tracking. The camera FOV is approximately 110 degrees.
```

### Audio Issues

```
No audio or wrong audio output
├── Is audio playing through the headset speakers?
│   └── Check: Settings > Sound — ensure headset speakers are selected, not Bluetooth.
├── Does the app use spatial audio?
│   ├── Check for FMOD/Wwise initialization errors in logcat.
│   └── Check that audio sources have correct 3D settings and are not muted.
├── Audio is distorted or crackling?
│   └── Audio buffer underruns. Check for CPU overload causing audio thread starvation.
│       Reduce audio complexity or increase buffer size.
└── Audio plays from wrong position?
    └── Check spatial audio source positions match visual object positions.
        Common issue: audio listener not attached to the camera/head transform.
```

## Gotchas

These are common debugging pitfalls specific to Meta VR development.

- **Logcat buffer overflow** -- On Meta VR devices, the logcat ring buffer fills quickly because the OS and other apps generate constant output. If you do not start logging before reproducing the issue, the crash logs may already be evicted. Start `metavr adb logcat --follow` before reproducing.
- **USB cable quality matters** -- Many USB-C cables are charge-only and do not carry data. If `metavr device list` shows nothing, try a different cable before troubleshooting software. The cable that came with the Quest works for data.
- **WiFi debugging disconnects** -- WiFi ADB connections (`metavr device connect <ip>`) drop after the device sleeps. You must reconnect after waking the device. USB is more reliable for sustained debugging sessions.
- **Release builds strip logs** -- If your app uses `android:debuggable="false"` (release builds), some log output is suppressed. Debug with a debug build when investigating issues. Do not ship debuggable builds to the store.
- **Multiple logcat tags for the same component** -- Unity uses tags `Unity`, `il2cpp`, and `mono` depending on the scripting backend. Unreal uses `UE`, `LogVR`, and `LogOnline`. Filter broadly at first, then narrow down.
- **OVR Metrics Tool overlay conflicts** -- The OVR Metrics Tool overlay can interfere with your app's rendering or input. If your app behaves oddly, disable the metrics overlay and retest before filing a bug.

## Tips and Best Practices

### Filtering Logs Effectively

Use severity filters to cut through noise:

```bash
# Show only errors
metavr log --level E

# Show warnings and above
metavr log --level W
```

Filter by tag to focus on specific subsystems:

```bash
metavr adb logcat --tag VrApi
metavr adb logcat --tag Unity
```

Use advanced filters with `metavr adb logcat`:

```bash
# Complex filter expressions
metavr adb logcat --filter "Unity:W ActivityManager:I"

# Regex pattern matching
metavr adb logcat --regex "error|exception"

# Specific log buffer
metavr adb logcat --buffer crash
```

See [logcat-filtering.md](references/logcat-filtering.md) for a full guide on log filtering techniques.

### Searching for Crash Signatures

When investigating crashes, search the log output for known patterns:

```bash
metavr log | grep -i "fatal\|crash\|exception\|anr"
```

Common crash-related tags include `AndroidRuntime`, `DEBUG`, and `libc`.

### Checking Permissions

Many Horizon OS features require specific manifest permissions. If a feature silently fails, check that the application manifest includes the required permissions. Common ones:

- `com.oculus.permission.HAND_TRACKING` -- Hand tracking access
- `com.oculus.permission.USE_SCENE` -- Scene API spatial data access
- `android.permission.RECORD_AUDIO` -- Microphone access
- `android.permission.CAMERA` -- Camera access (for mixed reality)

### Performance Debugging

If the application stutters or drops frames:

```bash
# Check device battery and thermal state
metavr device battery

# Watch for thermal throttling messages in logs
metavr adb logcat --tag ThermalService --level W

# Check VrApi frame timing
metavr adb logcat --tag VrApi | grep FPS
```

See [common-issues.md](references/common-issues.md) for a catalog of known issues and their solutions.

## References

### Skill References

- [Logcat Filtering Guide](references/logcat-filtering.md) -- Detailed guide to filtering and interpreting device logs
- [Screenshots and Video Capture](references/screenshots-video.md) -- Capturing visual state from the device
- [Common Issues and Diagnostics](references/common-issues.md) -- Catalog of common Meta VR development issues and solutions
