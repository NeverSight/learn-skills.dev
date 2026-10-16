---
name: monogame-effects
description: MonoGame custom effects guide covering MGFX runtime, stock effects (BasicEffect, SpriteEffect, etc.), cross-platform shader compilation (HLSL vs GLSL), shader model targets, preprocessor symbols, and portability pitfalls. Use this skill whenever the user asks about custom effects, MGFX, stock effects, cross-platform shaders, shader model compatibility, porting a shader to MonoGame, preprocessor conditionals in .fx files, or gets compilation errors with shaders — even if they just say "my shader doesn't work on Linux" or "which shader model should I use".
---

# MonoGame Custom Effects Implementation Guide

This skill covers the MGFX effect system, stock effects, and cross-platform shader compilation. For HLSL syntax, the Material pattern, and SpriteBatch integration, see the `monogame-shaders` skill. For compiled API signatures, see `references/effects.md`.

## MGFX — MonoGame's Effect System

MonoGame uses its own FX runtime called **MGFX**, designed to support multiple shader backends from a single `.fx` source file. Core capabilities:

- Same technique/pass/shader structure as Microsoft FX files.
- Textual `.fx` source compiled to optimized `.mgfxo` binary at build time.
- Cross-platform: targets DirectX HLSL and OpenGL GLSL from one source via MojoShader.

Pipeline:
```
MyEffect.fx  →  MGFXC (or MGCB)  →  MyEffect.mgfxo  →  Content.Load<Effect>()
```

## Stock Effects

MonoGame ships six built-in effects, all fully supported on current platforms:

| Effect | Purpose |
|--------|---------|
| `SpriteEffect` | Default 2D sprite rendering — used internally by `SpriteBatch` |
| `BasicEffect` | Simple 3D with lighting, fog, and vertex colors |
| `AlphaTestEffect` | Alpha-tested cutout rendering (no blending) |
| `DualTextureEffect` | Two-texture blending (detail maps, lightmaps) |
| `EnvironmentMapEffect` | Cubemap reflections for 3D surfaces |
| `SkinnedEffect` | GPU skinning for animated models (up to 72 bones) |

These are built with the same MGFX pipeline. To optimize a stock effect for your target platform, copy it from `MonoGame.Framework/Platform/Graphics/Effect/Resources`, edit out unused features, and recompile with MGFXC.

## Shader Model Targets

### DirectX targets

| Shader model | Minimum `GraphicsProfile` |
|---|---|
| `vs_4_0_level_9_1` / `ps_4_0_level_9_1` | `Reach` |
| `vs_4_0_level_9_3` / `ps_4_0_level_9_3` | `Reach` |
| `vs_4_0` / `ps_4_0` | `HiDef` |
| `vs_4_1` / `ps_4_1` | `HiDef` |
| `vs_5_0` / `ps_5_0` | `HiDef` |

### OpenGL/GLSL targets (via MojoShader)

| Shader model |
|---|
| `vs_2_0` / `ps_2_0` |
| `vs_3_0` / `ps_3_0` |

OpenGL targets are limited to SM 3.0 — do not use SM 4+ features in code paths that must run on GL platforms.

## Cross-Platform Preprocessor Symbols

MonoGame defines these symbols when compiling `.fx` files:

| Symbol | When defined |
|--------|-------------|
| `2MGFX` | Always (marks that MGFX is the compiler, not FXC) |
| `HLSL` | DirectX builds |
| `SM4` | DirectX builds |
| `OpenGL` | OpenGL builds |
| `GLSL` | OpenGL builds |

### Canonical cross-platform shader model selection

Always use `#if OPENGL` guards to pick the right shader model — never hardcode `vs_4_0` in portable shaders:

```hlsl
#if OPENGL
    #define VS_SHADERMODEL vs_3_0
    #define PS_SHADERMODEL ps_3_0
#else
    #define VS_SHADERMODEL vs_4_0_level_9_1
    #define PS_SHADERMODEL ps_4_0_level_9_1
#endif

technique MyTechnique
{
    pass Pass1
    {
        VertexShader = compile VS_SHADERMODEL MainVS();
        PixelShader  = compile PS_SHADERMODEL MainPS();
    }
}
```

Custom symbols can be defined via the MGCB Editor (per-asset **Defines** field) or the MGFXC command line (`--defines`).

## Effect Writing Rules

These prevent silent bugs and cross-platform breakage:

1. **Vertex shader outputs must exactly match pixel shader inputs** — same types, same semantic order. Omitting a parameter may compile but will pass garbage in the wrong register on some platforms.

2. **No default values on GL platforms** — `float Intensity = 0.5;` in the effect file works on DX but is silently ignored on OpenGL. Either set the value from C# after loading, or use `#define`:
   ```hlsl
   #define INTENSITY 0.5
   ```

3. **Unused parameters are aggressively stripped** — if you declare a parameter but never read it in a shader, the compiler removes it. `Parameters["MyParam"].SetValue(...)` will then silently fail (the parameter won't exist). Ensure every declared parameter is actually read in the shader body.

4. **Preshaders are not supported** — MonoGame ignores preshader blocks.

5. **Test on both DX and GL** — a shader that compiles on DX may fail on GL due to SM level differences or MojoShader translation limits.

## Two Ways to Use Custom Effects

| Method | When to use |
|--------|------------|
| MGCB (`Effect - MonoGame` processor) | Standard workflow — assets managed with Content Pipeline, loaded via `ContentManager` |
| MGFXC standalone tool | Runtime-loaded effects, build scripts, CI pipelines without MGCB |

Prefer MGCB for all game assets. Use MGFXC directly only for tools or editor workflows that bypass the Content Pipeline.

## Reference

For HLSL code templates, parameter setting patterns, and multi-pass effect examples, see `references/effects.md`.
For SpriteBatch integration, post-processing pipelines, and the Material class pattern, see the `monogame-shaders` skill.
