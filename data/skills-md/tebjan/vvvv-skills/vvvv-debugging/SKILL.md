---
name: vvvv-debugging
description: "Set up debugging for vvvv gamma C# node projects -- generate VS Code launch.json and tasks.json configurations, attach debugger to running vvvv, configure Visual Studio debug profiles, and use debugging best practices. Use when setting up a debugger for vvvv, creating launch configurations, attaching to vvvv process, or troubleshooting breakpoints in C# nodes. Supports multiple launch configs for different test scenarios/patches."
license: CC-BY-SA-4.0
compatibility: Designed for coding AI agents assisting with vvvv gamma development
metadata:
  author: Tebjan Halm
  version: "1.1"
---

# Debugging vvvv gamma C# Projects

For CLI arguments and session files, see the **vvvv-startup** skill.

## Context-Aware Setup Workflow

When the user asks to set up debugging, follow this workflow. **Ask ALL configuration questions upfront** using AskUserQuestion before generating any files. Do NOT assume defaults — always confirm with the user.

### 1. Detect vvvv Installation

Find vvvv.exe automatically by scanning `C:\Program Files\vvvv\` for `vvvv_gamma_*` directories:

```bash
ls -d "/c/Program Files/vvvv/vvvv_gamma_"* 2>/dev/null | sort -r
```

Directory name format: `vvvv_gamma_MAJOR.MINOR[-BUILD-gHASH-PLATFORM]`. Sort by version descending. Filter out `-beta`, `-alpha`, `-rc`, `-test`, `-dev` variants unless no stable version exists.

### 2. Scan Workspace

Detect what exists in the workspace:
- `.csproj` / `.sln` files (may or may not need build tasks -- see step 3)
- `.vl` files (candidates for `--open`)
- `help/` folders (common location for test patches)
- Existing `.vscode/launch.json` (extend rather than overwrite)
- Git submodules (especially `VL.StandardLibs` — see package repos warning below)
- Package names from repo folder name, main *.vl file or `.csproj` `<PackageId>` (for `--editable-packages`)

### 3. Ask User — ALL Questions Before Generating

**CRITICAL: Ask all of these questions using AskUserQuestion BEFORE generating any configuration.** Use multi-question format to batch related questions. Do not generate launch.json until all answers are collected.

#### Question Group 1: vvvv Version & Patch
- **Which vvvv version?** — Present detected versions, recommend the latest stable. Let user pick or specify a custom path.
- **Which .vl patch to open?** — List found `.vl` files as options. If `help/` folder exists, suggest those.

#### Question Group 2: Launch Flags
- **`--debug` flag?** — Enables debug symbols for breakpoints but slows patching. Ask: "Enable `--debug` for breakpoints? (slower startup)" Default: No for fast iteration, Yes if user explicitly wants breakpoints.
- **`--allowmultiple`?** — Allows launching a second vvvv instance. Ask: "Allow multiple vvvv instances? If No, launch will fail if vvvv is already running (useful to detect stale instances)." Default: No.
- **`--package-repositories`?** — Points vvvv to scan a folder for packages. **WARNING: If the workspace contains git submodules like `VL.StandardLibs/`, using `--package-repositories ${workspaceFolder}` will cause vvvv to recompile ALL core libraries from source, taking many minutes.** Ask: "Add `--package-repositories`? Only needed if vvvv can't find your package. WARNING: if your repo has VL.StandardLibs or other library submodules, this will trigger full recompilation." Default: No.
- **`--editable-packages`?** — Loads specified packages from source. Only useful with `--package-repositories`. Ask only if package-repositories is enabled.

#### Question Group 3: Build Mode
- **Source reference or DLL?** — "Does your .vl document reference the .csproj directly (source reference, most common) or a pre-built DLL?" Source reference = no build task. DLL = add `preLaunchTask: "build"`.

### 4. Generate Configuration

Only after all questions are answered, generate `.vscode/launch.json` and optionally `.vscode/tasks.json`.

**Always generate these configurations:**
1. A launch config with the user's chosen flags
2. An "Attach to vvvv" config for attaching to an already-running instance

**Optionally generate:**
- A second launch config with `--debug` if the first one doesn't have it (or vice versa)
- A `tasks.json` if DLL/binary build mode was selected

## VS Code launch.json

### Minimal Config (source reference, no extras)

The simplest possible config — just open a patch:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "vvvv — MyPatch",
      "type": "coreclr",
      "request": "launch",
      "program": "C:\\Program Files\\vvvv\\vvvv_gamma_7.1-win-x64\\vvvv.exe",
      "args": [
        "-o",
        "${workspaceFolder}/help/HowTo Use MyFeature.vl"
      ],
      "cwd": "${workspaceFolder}",
      "stopAtEntry": false,
      "console": "internalConsole"
    },
    {
      "name": "Attach to vvvv",
      "type": "coreclr",
      "request": "attach",
      "processName": "vvvv.exe"
    }
  ]
}
```

### Full Config (with all optional flags)

When the user opts in to all flags:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug with vvvv",
      "type": "coreclr",
      "request": "launch",
      "program": "C:\\Program Files\\vvvv\\vvvv_gamma_7.0-win-x64\\vvvv.exe",
      "args": [
        "--package-repositories",
        "${workspaceFolder}",
        "--editable-packages",
        "VL.MyPackage*",
        "-o",
        "${workspaceFolder}/help/HowTo Use MyFeature.vl",
        "--debug",
        "--allowmultiple"
      ],
      "cwd": "${workspaceFolder}",
      "stopAtEntry": false,
      "console": "internalConsole"
    },
    {
      "name": "Attach to vvvv",
      "type": "coreclr",
      "request": "attach",
      "processName": "vvvv.exe"
    }
  ]
}
```

### DLL/Binary Reference (external build required)

Add `preLaunchTask` to build C# before launching vvvv:

```json
{
  "name": "Debug with vvvv (pre-build)",
  "type": "coreclr",
  "request": "launch",
  "preLaunchTask": "build",
  "program": "C:\\Program Files\\vvvv\\vvvv_gamma_7.0-win-x64\\vvvv.exe",
  "args": [
    "-o",
    "${workspaceFolder}/help/HowTo Use MyFeature.vl",
    "--debug"
  ],
  "cwd": "${workspaceFolder}",
  "stopAtEntry": false,
  "console": "internalConsole"
}
```

Key points:
- **Omit `preLaunchTask`** for source references -- vvvv handles C# compilation via Roslyn
- **Add `preLaunchTask: "build"`** only for DLL/binary references or complex build scenarios
- `--debug` enables debug symbols (needed for breakpoints, but slows down patching)
- `--package-repositories` tells vvvv where to find your package — **WARNING: will recompile any VL library submodules found in the scanned folder tree**
- `--editable-packages` loads specified packages from source (glob patterns supported)
- `-o` opens the specified .vl patch on startup
- `--allowmultiple` allows a second vvvv instance — omit to detect stale instances
- Use array items for args (not a single string) for readability

### Attach to Running vvvv

Use attach when vvvv is already running and you want to debug without restarting:

```json
{
  "name": "Attach to vvvv",
  "type": "coreclr",
  "request": "attach",
  "processName": "vvvv.exe"
}
```

## VS Code tasks.json (only for DLL/binary reference setups)

Only generate tasks.json when the project requires external building (DLL references, native dependencies, Release builds). Skip this entirely for source project references where vvvv compiles C# at runtime.

### Build with dotnet

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "build",
      "command": "dotnet",
      "type": "process",
      "args": ["build", "${workspaceFolder}/src/MyProject.csproj", "-c", "Debug"],
      "problemMatcher": "$msCompile",
      "group": { "kind": "build", "isDefault": true }
    },
    {
      "label": "build-release",
      "command": "dotnet",
      "type": "process",
      "args": ["build", "${workspaceFolder}/src/MyProject.csproj", "-c", "Release"],
      "problemMatcher": "$msCompile"
    }
  ]
}
```

### Build with MSBuild (for .sln or projects requiring Visual Studio toolchain)

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "build",
      "type": "shell",
      "command": "& 'C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\MSBuild\\Current\\Bin\\MSBuild.exe' '${workspaceFolder}/src/MyProject.sln' -p:Configuration=Debug -p:Platform=x64 -t:Rebuild -v:minimal",
      "options": {
        "shell": { "executable": "powershell.exe", "args": ["-Command"] }
      },
      "problemMatcher": "$msCompile",
      "group": { "kind": "build", "isDefault": true }
    }
  ]
}
```

Prefer `dotnet build` unless the project requires MSBuild-specific features or a .sln with platform targets.

## Visual Studio Setup

### Debug via External Program

1. Open `.csproj` in Visual Studio
2. **Debug** > **Debug Properties** (or Project Properties > Debug > General)
3. Create a new launch profile:
   - **Command**: path to `vvvv.exe`
   - **Command line arguments**: `-o YourPatch.vl` (add `--debug` when breakpoints are needed)
   - **Working directory**: project folder
4. Press F5 to launch with debugger attached

### Attach to Process

1. Launch vvvv normally (add `--debug` if you need breakpoints)
2. **Debug** > **Attach to Process** (Ctrl+Alt+P)
3. Find `vvvv.exe` in the process list
4. Select **Managed (.NET Core, .NET 5+)** as code type
5. Click Attach

### launchSettings.json (dotnet tooling)

```json
{
  "profiles": {
    "Debug vvvv": {
      "commandName": "Executable",
      "executablePath": "C:\\Program Files\\vvvv\\vvvv_gamma_6.8-win-x64\\vvvv.exe",
      "commandLineArgs": "-o YourPatch.vl",
      "workingDirectory": "$(ProjectDir)"
    }
  }
}
```

## Debugging Tips

- **`--debug`** -- forces debug symbol emission for reliable breakpoints, but adds overhead. Use in the Debug config; omit for performance/deployment testing.
- **`--stoppedonstartup`** -- launch paused so you can set breakpoints before any Update() runs
- **`--nocache`** -- if breakpoints won't bind, force recompilation from source
- **`Debugger.Break()`** -- add to C# code to programmatically trigger a breakpoint
- **Conditional breakpoints in Update()** -- Update() runs every frame, so use hit counts or conditions
- **Constructor breakpoints** -- fire on each live-reload cycle too (Dispose then new Constructor)
- **`console: "internalConsole"`** -- captures Console.WriteLine output in VS Code debug console
- **Debugger-attached behavior** -- when a .NET debugger is attached, vvvv initialization runs synchronously (no async exception trapping), so startup breakpoints work reliably

## Common Pitfalls

- **`--package-repositories` + VL.StandardLibs submodule** — If your workspace has a `VL.StandardLibs/` git submodule (common in vvvv contrib repos), `--package-repositories ${workspaceFolder}` will cause vvvv to discover and recompile ALL standard libraries from source. This takes many minutes and is almost never what you want. Either omit `--package-repositories` or point it at a specific subfolder that doesn't contain library submodules.
- **`--allowmultiple` hiding stale instances** — Without this flag, vvvv refuses to start if another instance is running. This is useful: it tells you there's a stale vvvv process. With `--allowmultiple`, you might accidentally run two instances consuming double resources.
- **`--debug` slowing everything** — Debug symbol emission significantly slows vvvv's live compilation. Only enable when you actually need breakpoints. For quick iteration (testing UI, checking behavior), omit it.
