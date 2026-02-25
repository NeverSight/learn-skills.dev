---
name: harmonyos-dev
description: Initialize HarmonyOS project templates (Standard ArkTS or Native C++) and perform initial build verification.
---

# HarmonyOS Development Skill (Template Initialization)

## Directives
- **Single Purpose:** This skill is strictly for project scaffolding and initial build verification.
- **Templates:** Supports two templates: Standard (ArkTS only) and Native C++ (ArkTS + Native API).
- **Post-Initialization:** After successful build and git initialization, suggest using Conductor for project orchestration.
- **PowerShell Compatibility:** All commands MUST be PowerShell-compatible.
  - Use `;` as a statement separator.
  - Use `New-Item -ItemType Directory -Path <path> -Force` instead of `mkdir -p`.
  - Use `(Get-ChildItem -Name)` instead of `ls /b` or `dir /b`.
  - Use `Test-Path <path>` to check for existence before operating on files.

## Initialization Workflow
1. **Environment Check:** Verify `ohpm`, `hvigorw`, and `codelinter` are installed by running `ohpm -v; hvigorw -v; codelinter -h`.
2. **Template Selection:** Default to **Standard** ArkTS project unless the user explicitly mentions "Native C++" or "Native API". Do not ask for confirmation if the request is generic.
3. **Directory Check:** Ensure the target directory is suitable for a new project.
4. **Execution:**
   - **Project Files:** Use `xcopy /E /I /Y "assets/harmonyos-project-template/*" "."` (or the native template path) to copy project files.
   - **Scripts:** Use `xcopy /E /I /Y "scripts/*" "scripts/"` to copy verification scripts.
   - **Dependency Installation:** Run `ohpm install`.
   - **Environment Check:** Run `node scripts/check_env.cjs`.
   - **Git Initialization:** If the build succeeds, run `git init ; git add . ; git commit -m "Initial commit from HarmonyOS template"`.
   - **User Hint:** Advise the user that they can now use the `conductor-dev` skill to initialize a `conductor/` directory for project orchestration and further implementation.
   - **Shell Usage:** Always use `;` as the command separator. Prefer `xcopy` or `robocopy` for directory copies on Windows to ensure recursive copying and directory creation. Avoid `mkdir -p` and `&&`.

## Implementation Workflow
1. **Lint Before Commit:** Execute `codelinter` on all modified `.ets` or `.ts` files immediately after editing.
   - **Command:** `codelinter <file_path>`
   - **Requirement:** All linting errors must be resolved or explicitly justified before proceeding. Do NOT run unit tests (`hvigorw test`) or full project builds (`assembleHap`) during task implementation.
2. **UI Component Optimization:** When implementing UI components, prioritize performance by minimizing nested containers and using efficient layout managers.
3. **Self-Learning & Optimization:** After completing a task, analyze the implementation for potential optimizations or reusable patterns. Document these "lessons learned" in the task summary or the project's internal knowledge base to improve future development speed and quality.

## Core Capabilities

### 1. Initialize Project
Spatially sets up the project structure and installs dependencies.
- **Trigger:** "Initialize new project", "Create new HarmonyOS app", "Scaffold template"
- **Action:**
  1. Default to Standard ArkTS template unless Native C++ is requested.
  2. Copies the selected template (`assets/harmonyos-project-template/` or `assets/nativec-template/`) to the root.
  3. Copies `scripts/*` into the `scripts/` directory.
  4. Installs dependencies, runs the environment check, and performs an initial build.
  5. Runs `git init` upon successful build completion.
  6. **Hint:** Provide a clear hint that the user are adviced to use `conductor` for advanced project orchestration.
  7. **Shell Usage:** Always use `;` as the command separator and ensure PowerShell compatibility. Use `New-Item -ItemType Directory -Force` for directory creation.

### 2. Build & Verify
Ensures the application compiles correctly and uses correct SDK versions.
- **Trigger:** "Build the app", "Check for errors", "Verify template"
- **Action:**
  1. **SDK Verification:** You MUST read `build-profile.json5` to identify the `targetSdkVersion` and `compatibleSdkVersion`. Use the "Version to API Level Mapping" table below to cross-reference and verify the versioning.
  2. **Build:** Run `ohpm install; node scripts/check_env.cjs`.

## Resources
- **Standard Template:** `assets/harmonyos-project-template/`
- **NativeC Template:** `assets/nativec-template/`
- **Environment Scripts:** `scripts/`

## Reference: Version to API Level Mapping
| Version | API Level |
| :--- | :--- |
| 4.0 | 10 |
| 4.1 | 11 |
| 5.0.0 | 12 |
| 5.0.1 | 13 |
| 5.0.2 | 14 |
| 5.0.3 | 15 |
| 5.1.0 | 18 |
| 5.1.1 | 19 |
| 6.0 | 20 |

**Note:** If the version string in `build-profile.json5` includes a number in parentheses, such as `6.0.0(20)`, the number in the parentheses is the API Level.

