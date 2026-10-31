---
name: raylib
description: Guide for developing 2D and 3D games using the Raylib framework (v6.0). Use for creating, structuring, and building games in C/C++ or Go, handling graphics, input, audio, 3D models, and compiling to WebAssembly.
license: Complete terms in LICENSE.txt
---

# Raylib Game Development

This skill provides guidelines and patterns for building 2D and 3D games using Raylib, focusing on version 6.0 features.

## Overview

Raylib is a highly modular, simple, and easy-to-use C library for videogame programming. It abstracts OpenGL and provides a straightforward imperative API without forcing any specific engine architecture (no built-in ECS, no hidden object models). It is widely used in C/C++, but also has extremely popular Go bindings (`raylib-go`).

Raylib 6.0 introduces major features like a Software Renderer backend (`rlsw`) for CPU-only rendering, new memory and Win32/Emscripten backends, redesigned Skeletal Animation System (GPU skinning with blending), redesigned fullscreen modes, and a massive new File System and Text Management API. It also introduces `rexm`, the official Raylib examples manager.

## Reading Documentation

For detailed API usage and architectural patterns, read the bundled references:
- **`references/architecture_patterns.md`**: Core concepts, game loop, memory management, and Web/HTML5 specific patterns.
- **`references/api_cheatsheet.md`**: Quick reference for window, drawing, input, textures, text, 3D models, and audio.
- **`references/deployment_guide.md`**: Production build pipelines, CMake setup, Emscripten (WebAssembly) compilation, and Go cross-compilation.
- **`references/ecosystem_libraries.md`**: Curated list of the best Raylib ecosystem libraries, GUI frameworks (raygui, Dear ImGui), extensions, and tools.

## Templates and Scripts

Use bundled scaffolding instead of regenerating build files from memory.

- **Run** `scripts/new_project.py` when creating a new raylib project. Prefer this over hand-assembling files.
  - Example: `python scripts/new_project.py --out ./my-game --name "My Game" --lang c --layout single`
  - Supports `--lang c|cpp|go` and `--layout single|multi`.
- **Read** files under `templates/` when adding a missing build file or matching the canonical project shape.
  - `templates/c/main.c`: desktop and web loop with `UpdateDrawFrame()` and `emscripten_set_main_loop()`.
  - `templates/c/CMakeLists.txt`: raylib 6.0 FetchContent pattern.
  - `templates/multi-file/`: screen-state-machine layout for larger games.
- **Run** `scripts/build.sh` or `scripts/build.ps1` for CMake desktop builds.
- **Run** `scripts/build_web.sh` or `scripts/build_web.ps1` for Emscripten web builds (set `RAYLIB_PATH` first).
- **Run** `scripts/cross_compile_go.sh` or `scripts/cross_compile_go.ps1` for raylib-go cross-compilation.

On Windows, use the `.ps1` scripts. On Linux and macOS, use the `.sh` scripts. Run scripts from the skill directory or pass the user's project path as the first argument.

Do not read script source into context unless debugging the skill itself; execute scripts and use their output.

## Best Practices

1. **Window Initialization First**: You MUST call `InitWindow()` before loading any textures, models, or shaders, because these require an active OpenGL context.
2. **Flipping Textures**: To draw a texture flipped horizontally or vertically, use `DrawTextureRec()` or `DrawTexturePro()` and pass a source rectangle with a *negative* width or height.
3. **Audio Streaming**: Short sound effects should use `Sound` (`LoadSound`, `PlaySound`). Long background music must use `Music` (`LoadMusicStream`, `PlayMusicStream`) and MUST call `UpdateMusicStream()` every frame.
4. **Web/HTML5 Loop**: When targeting the web via Emscripten, you cannot use a blocking `while(!WindowShouldClose())` loop. Extract the loop body into an `UpdateDrawFrame()` function and use `emscripten_set_main_loop()`.
5. **Memory Leaks**: Always pair `Load*` with `Unload*` (e.g., `LoadTexture` -> `UnloadTexture`).
6. **No Built-in Timers**: Raylib does not have a built-in timer object. Manage time manually using `GetTime()` (total time) and `GetFrameTime()` (delta time).
7. **3D GPU Skinning**: For animated 3D models, Raylib 5.5+ supports GPU skinning. Ensure you use the updated skeletal animation API if performance is a concern.
8. **Language Choice**: While Raylib is written in C, Alvar Laigna frequently uses Go (`raylib-go`). When writing Go code, ensure you use `github.com/gen2brain/raylib-go/raylib` and handle CGO dependencies correctly. Before building ask developer which language is preferred for the project - C or Go.
