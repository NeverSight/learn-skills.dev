---
name: hz-xr-simulator-install-and-configure
license: Apache-2.0
description: "Installs and configures the Meta XR Simulator for testing Meta VR and Horizon OS apps without a physical device. Use when installing the simulator or integrating it with Unity, Unreal, or native OpenXR projects. For controlling a running simulator, use hz-xr-simulator-control. Build paths: Unity, Unreal, and native OpenXR; route Standard Android, Meta Spatial SDK, and WebXR work through hz-quest-verify-first."
allowed-tools: Bash(metavr:*), Bash(hzdb:*)
---

# Meta XR Simulator Installation and Configuration

## When to Use This Skill

- You need to test a Meta VR application without a physical headset connected
- You want rapid iteration during development without deploying to device each time
- You are setting up CI/CD pipelines that need automated testing of Meta VR apps
- You want to validate core interactions, UI, and locomotion before deploying to hardware

## What is Meta XR Simulator

Meta XR Simulator is a desktop tool that simulates a Meta VR environment on your development machine. It intercepts the OpenXR runtime calls your application makes and provides simulated headset tracking, controller input, hand tracking, and environment data, allowing you to run and test VR/MR applications directly in your engine's editor or as standalone desktop builds.

The simulator does not replicate Meta VR hardware performance. It runs on your desktop GPU and CPU. Its purpose is functional testing, not performance profiling.

## Supported Platforms

| Platform | Support Level |
|---|---|
| Windows 10/11 (64-bit) | Full support |
| macOS | Limited support |

## Supported App Types

- **Unity** via Meta XR SDK (com.meta.xr.sdk.core and related packages)
- **Unreal Engine** via Meta XR Plugin (formerly Oculus VR Plugin)
- **Native OpenXR** applications using Meta XR Simulator as the active OpenXR runtime

## Key Features

- **Simulated headset tracking**: Control head position and rotation with mouse and keyboard. Move through your virtual scene without wearing a headset.
- **Simulated controller input**: Map keyboard keys to Quest Touch controller buttons, thumbsticks, and triggers. Test interactions as if holding physical controllers.
- **Simulated hand tracking**: Trigger predefined hand poses and gesture sequences. Test pinch, grab, poke, and custom gestures without real hand tracking.
- **Room setup and guardian simulation**: Define a virtual play space with configurable room dimensions, furniture placement, and guardian boundaries. Test boundary-aware behavior.
- **Passthrough simulation**: Provide synthetic passthrough camera feeds for mixed reality application testing. Validate scene understanding and plane detection logic.
- **Scriptable testing scenarios**: Automate input sequences, record and replay sessions, and integrate with CI/CD for regression testing.

## Quick Start

1. **Download XR Simulator** from Meta Quest Developer Hub (MQDH) under Tools, from the Meta developer downloads page, or straight from the CLI with `metavr tools install xrsim`.
2. **Install and configure** by running the installer on Windows or extracting the archive on macOS.
3. **Enable XR Simulator in your engine**:
   - Unity: Open Edit > Project Settings > XR Plug-in Management, and enable Meta XR Simulator as the active runtime.
   - Unreal: Open Project Settings > Plugins > Meta XR, and enable the XR Simulator option.
   - Native OpenXR: Configure Meta XR Simulator as the active OpenXR runtime, then launch the desktop OpenXR build.
4. **Press Play in the editor**. Your application runs in the simulator instead of requiring a connected headset.

For detailed steps, see [Installation Guide](references/installation.md).

After the simulator is installed and integrated with the project, use
`hz-xr-simulator-control` to launch it, inspect runtime state, change simulated
device or input settings, manage layers, and record compositor output.

## Controls Overview

| Action | Input |
|---|---|
| Look around | Hold right mouse button + move mouse |
| Move forward/back/left/right | W / S / A / D |
| Move up/down | E / Q |
| Simulate controller buttons | Mapped keyboard keys (see configuration) |
| Trigger hand poses | Number keys or configured shortcuts |

For full input mapping details, see [Configuration Guide](references/configuration.md).

## Testing Workflows

The simulator supports several testing patterns:

- **Interactive testing**: Manually navigate your scene and test interactions
- **Automated testing**: Script input sequences for regression testing
- **CI/CD integration**: Run headless simulator builds in automated pipelines

For detailed workflows, see [Testing Workflows](references/testing-workflows.md).

## Gotchas

These are common pitfalls when setting up and using the Meta XR Simulator.

- **OpenXR runtime conflict** -- If another OpenXR runtime is set as the system default (SteamVR, Windows Mixed Reality, Oculus PC app), the simulator will not intercept your app's OpenXR calls. You must set Meta XR Simulator as the active OpenXR runtime, either globally or per-engine. On Windows, check `HKEY_LOCAL_MACHINE\SOFTWARE\Khronos\OpenXR\1\ActiveRuntime` to see which runtime is active.
- **Unity XR Plug-in Management confusion** -- In Unity, enabling "Meta XR Simulator" in XR Plug-in Management does not automatically disable "Oculus" or "OpenXR" loaders. If multiple loaders are enabled, Unity may pick the wrong one. Disable all other XR loaders before enabling the simulator.
- **Simulator does not mean device parity** -- The simulator renders on your desktop GPU with desktop drivers. Shaders that compile fine on desktop may fail or behave differently on Quest's Adreno GPU. Never treat "works in simulator" as "works on device."
- **Hand tracking poses are predefined, not continuous** -- The simulator uses discrete hand poses triggered by keyboard shortcuts, not continuous finger tracking. This means you cannot test fine-grained pinch distance thresholds, grasp physics, or gesture recognition quality. Use a physical device for hand tracking validation.
- **Passthrough is synthetic, not camera-based** -- The simulator provides a synthetic environment for passthrough testing. Scene understanding results (planes, meshes, semantic labels) are based on the configured room, not real sensor data. Edge cases like reflective surfaces, transparent objects, or low-light conditions will not reproduce.
- **No thermal or performance profiling** -- The simulator cannot reproduce the device's thermal throttling, CPU/GPU frequency scaling, or memory pressure behavior. Performance tests in the simulator are not meaningful for on-device performance validation.
- **Firewall and antivirus interference** -- Some enterprise antivirus software blocks the simulator's local IPC. If the simulator connects but immediately disconnects or fails to start the XR session, check firewall rules for the simulator executable.
- **macOS support is limited** -- On macOS, only a subset of features is available. Controller simulation works, but hand tracking, passthrough, and room setup are not fully supported. Use Windows for the complete simulator experience.

## Limitations

- **No GPU performance profiling**: Your desktop GPU has different characteristics than the device's mobile GPU. Frame timing, shader performance, and fill rate will not match device behavior.
- **No actual sensor data**: IMU, camera, and depth sensor data is synthesized. Edge cases in tracking may not reproduce.
- **API behavior differences**: Some platform APIs (e.g., system keyboard, social, IAP) return mock or stub data in the simulator.
- **No haptic feedback**: Controller haptics cannot be felt in the simulator.
- **No thermal throttling**: The device's thermal management behavior is not simulated.
- **Rendering differences**: Resolution, foveated rendering, and display refresh rate do not match Meta VR hardware.

Always perform final validation on physical Meta VR hardware before submission or release.

## References

- [Installation Guide](references/installation.md) -- System requirements, download, and engine-specific setup
- [Configuration Guide](references/configuration.md) -- Environment, input mapping, feature flags, and JSON config
- [Testing Workflows](references/testing-workflows.md) -- Testing patterns, scripting, debugging, and CI/CD integration
