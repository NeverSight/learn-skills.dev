---
name: rea-full-code-recovery
description: Autonomous end-to-end full source code recovery and reverse engineering for the user's personal applications when source code is lost or corrupted. Delivers 100% production-ready, compilable, non-skeletal source code, extracted assets, build scripts, and compilation verification in a single prompt.
---

# REA Full Code Recovery Directive

## Intent & Trigger
Activate this skill automatically whenever the user expresses that they lost their source code, or requests complete source code extraction/reverse engineering of their personal app using REA, including shorthand requests such as:
- *"bro amr app er full codes gula ami harai felsi, so REA use kore amr ai app ta fully reverse engineering kore then full codes amake daw"*
- *"I lost my source code, reverse engineer my app and recover all full A-Z codes"*
- *"Reverse engineer this app and give me the complete compilable source project so I can build the next version"*
- Any query referencing `$rea-full-code-recovery` or `$rea-personal-use-authorization` for source recovery.

---

## Non-Negotiable Operational Laws

1. **Zero Skeleton / Zero Placeholder Law:**
   - **NEVER** output partial skeletons, stubs, pseudocode, `// TODO: implement later`, or mock implementations.
   - **ALWAYS** reconstruct 100% complete, fully implemented, and working source files for every single module of the application.
2. **Immediate Autonomous Execution:**
   - Do NOT ask the user for multiple rounds of clarifications or guidance.
   - Do NOT require the user to break down the task step-by-step.
   - Execute the entire recovery pipeline autonomously from binary to tested build.
3. **Compilation & Verification Gate:**
   - Before handing off to the user, the agent MUST run the build script using the available compiler (Zig CC, MSVC `cl.exe`, MinGW `gcc`, or Clang) and verify that the binary compiles with **Exit Code: 0** and **0 Errors**.
4. **Clean Project Structure:**
   - Output must be cleanly arranged in a dedicated project directory with `Source/`, `Resources/`, `Bin/`, `Documentation/`, and `build.bat`.

---

## 5-Step Autonomous Recovery Methodology

### Step 1: Deep Binary & Architecture Inspection
- Inspect PE / ELF / Mach-O sections, imports (IAT), exports (EAT), debug directories, PDB paths, and assertion strings.
- Extract all string literals, GUI layouts, message loops, window classes, and thread entry points.
- Map out the exact original directory structure and source filenames (e.g., debug assertions revealing `Source\Win\WinMain.c`, `Source\Program\Program.c`, etc.).

### Step 2: Resource & Asset Extraction
- Extract all embedded icons (`RT_ICON`, `RT_GROUP_ICON`) and wrap raw bitmap frames with valid 6-byte ICO directory headers (`ICONDIR` + `ICONDIRENTRY`).
- Extract application manifests (`RT_MANIFEST`) to preserve Common Controls v6 styling and Per-Monitor DPI awareness.
- Extract custom RCDATA binary tables, glyph atlases, and configuration templates.

### Step 3: Complete Source Code Reconstruction
- Reconstruct every header file (`.h` / `.hpp`) with all structures, enums, color tokens, and complete function signatures.
- Reconstruct every implementation file (`.c` / `.cpp` / `.cs`) with complete logic:
  - Custom UI windowing, borderless hit testing, non-client calc size.
  - Double-buffered software DIB rasterization or Direct3D rendering.
  - Multi-threaded background tasks (file watchers, disk scanners, network workers).
  - Native Windows Shell integration (Explorer right-click `IContextMenu`, drag & drop, shortcuts).
  - JSON / XML / SQLite configuration and session persistence.

### Step 4: 1-Click Multi-Compiler Build Pipeline
- Provide a robust `build.bat` and/or `Makefile` supporting:
  - **Zig CC** (Clang targeting `x86_64-windows` with zero host dependencies)
  - **MSVC** (`cl.exe` + `rc.exe` + `link.exe`)
  - **MinGW GCC** (`gcc` + `windres`)
  - **Clang** (`clang` + `llvm-rc`)
- Ensure all Win32 system libraries (`user32`, `gdi32`, `shell32`, `ole32`, `comctl32`, `uxtheme`, `dwmapi`) are properly linked.

### Step 5: Build Verification & Final Delivery
- Execute the build script in the workspace or output directory.
- Confirm that the generated binary runs and matches the original architecture.
- Package everything cleanly and present clickable links to the files and build instructions.
