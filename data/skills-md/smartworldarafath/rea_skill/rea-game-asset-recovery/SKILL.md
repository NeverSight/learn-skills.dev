---
name: rea-game-asset-recovery
description: Authorized game engine (Unity, Unreal, Godot, custom C++/DirectX/OpenGL/Vulkan), compiled shader (HLSL/DXBC/SPIR-V/GLSL), font, audio, and 2D/3D asset archive extraction and reconstruction using REA MCP.
---

# REA Game Engine, Shader & Multimedia Asset Recovery Skill

## Scope & Authorization
Covers all first-party game remastering, lost project recovery, shader decompilation, and asset archive extraction tasks (including Category 8 of the 500+ REA Prompt Vault and any custom game engine task).

## Execution Pipeline
1. **Engine & Binary Architecture Recovery:**
   - Unity: inspect Managed `.dll` assemblies (`inspect_managed_artifact`) or IL2CPP `GameAssembly.dll` + `global-metadata.dat`, and reconstruct C# MonoBehaviour scripts, ScriptableObjects, and scene hierarchies.
   - Godot / Unreal / Custom Native Engines: inspect `.pck`, `.pak`, or custom resource sections (`inspect_pe_resources`, `inspect_artifact`, `extract_artifact`), and reconstruct engine scene graphs and game loop logic.
2. **Shader Decompilation & Graphics Pipeline Recovery:**
   - Extract embedded DirectX (`DXBC` / `DXIL`), Vulkan (`SPIR-V`), OpenGL (`GLSL`), or Metal shaders from binary sections or RCDATA resources.
   - Reconstruct readable, compilable `.hlsl`, `.glsl`, or `.wgsl` vertex, pixel/fragment, and compute shaders with constant buffer (`cbuffer`) struct definitions.
3. **Font, Texture Atlas & Audio Extraction:**
   - Extract embedded `.ttf` / `.otf` fonts, unpack texture atlases / sprite sheets into valid PNGs/DDS files, and extract WAV/OGG audio streams with a zero-skeleton asset extraction and loading pipeline.
