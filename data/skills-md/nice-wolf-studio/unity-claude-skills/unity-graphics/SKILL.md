---
name: unity-graphics
description: >
  Unity 6 graphics and rendering guide. Use when working with render pipelines (URP, HDRP, Built-in), shaders, Shader Graph, materials, textures, cameras, post-processing, or rendering optimization. Covers Render Graph, batching, draw call optimization, and GPU instancing. Based on Unity 6.3 LTS documentation.
globs:
  - "**/*.shader"
  - "**/*.hlsl"
  - "**/*.shadergraph"
  - "**/*.shadersubgraph"
  - "**/*.mat"
---

# Unity Graphics and Rendering

## Render Pipeline Selection Guide

A render pipeline performs a series of operations that take the contents of a scene and displays them on a screen. Unity provides three render pipelines:

| Criteria | Built-in Render Pipeline | Universal Render Pipeline (URP) | High Definition Render Pipeline (HDRP) |
|---|---|---|---|
| **Target** | Legacy projects | Mobile to high-end consoles/PCs | AAA, automotive, architectural |
| **Customization** | Limited | Scriptable, extensible via Renderer Features | Scriptable, Custom Passes, Full Frame Settings |
| **Rendering Paths** | Forward, Deferred | Forward, Forward+, Deferred | Forward, Deferred (hybrid tile/cluster) |
| **Shader Authoring** | ShaderLab + Surface Shaders | Shader Graph (recommended), HLSL | Shader Graph (recommended), HLSL |
| **SRP Batcher** | No | Yes | Yes |
| **Ray Tracing** | No | No | Yes (DXR) |
| **Volumetrics** | No | No | Yes (fog, clouds) |
| **Anti-Aliasing** | MSAA | FXAA, SMAA, TAA, MSAA | FXAA, SMAA, TAA, MSAA |
| **Platforms** | All | All (scalable) | High-end (DX11/12, Metal, Vulkan) |
| **GPU Requirement** | Standard | Standard | Compute shader capable |

**Decision flow:**
1. Need ray tracing, volumetric clouds, or physically-based sky? --> HDRP
2. Need to target mobile, WebGL, or widest platform range? --> URP
3. Maintaining a legacy project with no migration budget? --> Built-in
4. Starting a new project? --> URP (most projects) or HDRP (high fidelity)

> **Warning:** Render pipelines are NOT interchangeable. Materials, shaders, and post-processing from one pipeline do not work in another without conversion. Upgrading Built-in materials to URP/HDRP requires the pipeline's material upgrader; objects render bright pink if their shader is incompatible.

Source: [Render Pipelines](https://docs.unity3d.com/6000.3/Documentation/Manual/render-pipelines.html)

## URP (Universal Render Pipeline)

URP is a prebuilt Scriptable Render Pipeline made by Unity for creating optimized graphics across a range of platforms, from mobile to high-end consoles and PCs.

**Key features:**
- Forward, Forward+, and Deferred rendering paths
- Anti-aliasing: FXAA, SMAA, TAA, MSAA
- 2D Renderer for 2D games
- Renderer Features for custom rendering injection
- SRP Batcher for draw call optimization
- Built-in post-processing via Volume system

See: [references/urp-guide.md](references/urp-guide.md)
Source: [URP](https://docs.unity3d.com/6000.3/Documentation/Manual/universal-render-pipeline.html)

## HDRP (High Definition Render Pipeline)

HDRP is a prebuilt Scriptable Render Pipeline targeting AAA-quality games, automotive demos, and architectural visualization on high-end hardware. It requires compute shader-capable GPUs (DirectX 11/12, Metal, Vulkan).

**Key features:**
- Physically-based lighting with Physical Light Units
- Material types: Lit, StackLit, Layered Lit, Hair, Fabric, Eye, AxF, Terrain
- Ray tracing: reflections, GI, shadows, AO, subsurface scattering
- Volumetric fog and volumetric clouds
- Physically Based Sky, HDRI Sky, Gradient Sky
- Path tracing with denoising (Optix, Intel Open Image Denoise)
- Water system with caustics and underwater rendering
- Dynamic resolution with DLSS, FSR 1.0, TAA Upscaling

See: [references/hdrp-guide.md](references/hdrp-guide.md)
Source: [HDRP](https://docs.unity3d.com/6000.3/Documentation/Manual/high-definition-render-pipeline.html)

## Shader Graph

Shader Graph enables building shaders visually by creating and connecting nodes in a graph framework instead of writing code. Changes are reflected with instant feedback.

**Render pipeline compatibility:**

| Pipeline | Supported |
|---|---|
| URP | Yes |
| HDRP | Yes |
| Built-in Render Pipeline | Yes |
| Custom SRP | No |

Shader Graph is included automatically when you install URP or HDRP.

**Custom Function Node** -- Inject custom HLSL code into Shader Graphs:
- **String mode**: Write HLSL directly; use `$precision` token for half/float
- **File mode**: Reference external `.hlsl` files with include guards

```hlsl
// File mode example with include guards
//UNITY_SHADER_NO_UPGRADE
#ifndef MYHLSLINCLUDE_INCLUDED
#define MYHLSLINCLUDE_INCLUDED

void MyFunction_float(float3 A, float B, out float3 Out)
{
    Out = A + B;
}
#endif //MYHLSLINCLUDE_INCLUDED
```

**Pipeline detection in Custom Function nodes:**
```hlsl
#ifdef SHADERGRAPH_PREVIEW
    half3 color = half3(0,0,0);
#else
    #if defined(UNIVERSAL_PIPELINE_CORE_INCLUDED)
        half4 shadowCoord = TransformWorldToShadowCoord(WorldPosition);
        Light mainLight = GetMainLight(shadowCoord);
        half3 color = mainLight.color;
    #else
        half3 color = half3(0, 0, 0);
    #endif
#endif
```

**Conditional keywords by pipeline:**
- Built-in: `BUILTIN_PIPELINE_CORE_INCLUDED`
- URP: `UNIVERSAL_PIPELINE_CORE_INCLUDED`
- HDRP: `UNITY_HEADER_HD_INCLUDED`
- Preview window: `SHADERGRAPH_PREVIEW`

See: [references/shader-graph.md](references/shader-graph.md)
Source: [Shader Graph](https://docs.unity3d.com/6000.3/Documentation/Manual/shader-graph.html)

## Shaders

A shader is a program that runs on the GPU. Unity categorizes shaders into three types:

1. **Graphics Pipeline Shaders** -- Most common; work with Shader objects to determine scene appearance
2. **Compute Shaders** -- Perform GPU calculations outside the regular graphics pipeline
3. **Ray Tracing Shaders** -- Handle ray tracing calculations (HDRP only)

**Key terminology:**
- **Shader Object** -- Instance of the `Shader` class wrapping shader programs and GPU instructions
- **ShaderLab** -- Unity's language for defining Shader object structure
- **Shader Graph** -- Visual, code-free shader creation tool
- **Shader Asset** -- A `.shader` file defining a Shader object
- **HLSL** -- High Level Shader Language used inside shader code blocks

**Surface Shaders** (Built-in pipeline ONLY):
- Streamlined way to write lighting-interactive shaders
- Auto-generates vertex/pixel shaders and rendering passes
- NOT supported in URP or HDRP; use Shader Graph instead

**HLSL in ShaderLab:**
- Use `HLSLPROGRAM` directive to add shader code to Pass blocks
- Declare structs connecting shader variables to mesh vertex data
- Use `#pragma` directives to control compilation
- Support 16-bit precision for mobile optimization

Source: [Shaders Introduction](https://docs.unity3d.com/6000.3/Documentation/Manual/shader-introduction.html)

## Materials and Textures

Materials and shaders work together to define the appearance of a scene.

### Materials

**Key workflows:**
- Create material assets and assign them to GameObjects
- Modify material properties at runtime via scripting
- Use Material Variants for managing large material collections
- Upgrade Built-in materials to URP/HDRP to prevent pink rendering

**Material API -- Key properties and methods:**

| Property/Method | Purpose |
|---|---|
| `color` | Main color of the material |
| `mainTexture` | Primary texture |
| `shader` | Assigned shader reference |
| `renderQueue` | Render order override |
| `enableInstancing` | GPU instancing toggle |
| `SetColor(name, color)` | Change a color property |
| `SetFloat(name, value)` | Set a float property |
| `SetTexture(name, texture)` | Assign a texture |
| `SetVector(name, vector)` | Set a vector property |
| `SetMatrix(name, matrix)` | Set a matrix property |
| `HasProperty(name)` | Check if property exists |
| `EnableKeyword(keyword)` | Enable a shader keyword |
| `CopyPropertiesFromMaterial(mat)` | Copy from another material |
| `Lerp(start, end, t)` | Interpolate between materials |

> **Important:** Set your desired shader BEFORE modifying properties. Property assignments have no effect if the current shader does not support them.

### Textures

Textures are bitmap images applied to mesh surfaces. Key concepts:
- **Power-of-two dimensions** recommended: 32, 64, 128, 256, 512, 1024, 2048, 4096
- **LDR** (Low Dynamic Range): PNG, JPG -- values 0.0-1.0
- **HDR** (High Dynamic Range): EXR, HDR -- extended color ranges
- **RGBA**: RGB color plus alpha channel for transparency
- **Bits per pixel (bpp)**: Lower values reduce memory and improve GPU cache
- **Anisotropic filtering**: Improves quality at steep viewing angles

See: [references/materials-textures.md](references/materials-textures.md)
Source: [Materials](https://docs.unity3d.com/6000.3/Documentation/Manual/Materials.html), [Textures](https://docs.unity3d.com/6000.3/Documentation/Manual/Textures.html)

## Cameras

Cameras create an image of a particular viewpoint in a scene, with output displayed on-screen or captured as a texture.

**Projection modes:**
- **Perspective** -- Replicates human vision; distant objects appear smaller (default)
- **Orthographic** -- No perspective; objects render at consistent size regardless of distance; useful for isometric/2D games

**Key details:**
- At least one camera required per scene
- Multiple cameras supported with configurable render order
- Render path set in Player settings; overridable per camera
- URP and HDRP have pipeline-specific camera documentation
- Orthographic cameras render fog uniformly rather than depth-based

**Common camera setups:**
- Puzzle games: static camera for full visibility
- FPS: camera parented to player at eye level
- Racing: camera following the vehicle

Source: [Cameras](https://docs.unity3d.com/6000.3/Documentation/Manual/Cameras.html)

## Post-Processing

Post-processing effects simulate physical camera/film properties or enable stylized visuals.

| Pipeline | Post-Processing Solution |
|---|---|
| URP | Built-in (installed with URP template) |
| HDRP | Built-in (installed with HDRP template) |
| Built-in | Post-Processing Version 2 package (separate) |

> **Warning:** Post-processing solutions are NOT interchangeable across render pipelines. Each pipeline's effects and implementation methods differ.

**HDRP anti-aliasing options:**
- MSAA -- Most resource-intensive
- TAA -- Motion-dependent temporal smoothing
- SMAA -- Pattern-based edge blending
- FXAA -- Per-pixel; least intensive

**HDRP exposure:** Histogram-based with percentile selection, metering modes, and pre-exposure for precision with Physical Light Units.

Source: [Post-Processing](https://docs.unity3d.com/6000.3/Documentation/Manual/PostProcessingOverview.html)

## Render Graph (Unity 6)

The Render Graph system provides a high-level representation of custom SRP render passes, explicitly stating how passes use resources. Both URP and HDRP use Render Graph.

### Core Principles

1. **Handle-based resources** -- Use `TextureHandle`, `BufferHandle`, `RendererListHandle` instead of direct references
2. **Scoped access** -- Actual resources only accessible inside render pass execution code
3. **Explicit declaration** -- Each pass declares reads/writes, enabling dependency tracking
4. **No persistence** -- Resources created within one execution cannot carry to the next
5. **RTHandle dependency** -- Textures use RTHandle system

### Three-Phase Execution (per frame)

1. **Setup** -- Declare all render passes and resource dependencies
2. **Compilation** -- System culls unused passes, calculates resource lifetimes for efficient allocation
3. **Execution** -- Run non-culled passes in declaration order

### Key API Pattern -- AddRenderPass

```csharp
using UnityEngine.Rendering;
using UnityEngine.Rendering.RenderGraphModule;

// 1. Define pass data
class MyPassData { public TextureHandle input, output; public float param; }

// 2. Create and configure pass
using (var builder = renderGraph.AddRenderPass<MyPassData>("MyPass", out var passData))
{
    passData.input = builder.ReadTexture(inputTexture);
    passData.output = builder.UseColorBuffer(
        renderGraph.CreateTexture(new TextureDesc(Vector2.one, true, true)
        { colorFormat = GraphicsFormat.R8G8B8A8_UNorm, name = "Output" }), 0);
    passData.param = 2.5f;

    builder.SetRenderFunc((MyPassData data, RenderGraphContext ctx) =>
    {
        var mpb = ctx.renderGraphPool.GetTempMaterialPropertyBlock();
        mpb.SetTexture("_MainTexture", data.input);
        mpb.SetFloat("_FloatParam", data.param);
        CoreUtils.DrawFullScreen(ctx.cmd, material, mpb);
    });
}

// 3. Lifecycle: new RenderGraph() -> BeginRecording() -> AddPasses -> EndRecordingAndExecute() -> Cleanup()
```

### RenderGraphBuilder Key Methods

| Method | Purpose |
|---|---|
| `ReadTexture` / `WriteTexture` | Declare texture read/write dependency |
| `UseColorBuffer` / `UseDepthBuffer` | Write + auto-bind as render/depth target |
| `CreateTransientTexture` | Temporary texture scoped to pass |
| `ReadComputeBuffer` / `WriteComputeBuffer` | Declare buffer read/write |
| `UseRendererList` | Declare renderer list usage |
| `SetRenderFunc` | Set rendering callback |
| `EnableAsyncCompute` / `AllowPassCulling` | Control pass behavior |

**Resource creation:** `CreateTexture()`, `CreateComputeBuffer()`, `CreateRendererList()`
**Import external:** `ImportTexture()`, `ImportBackbuffer()`, `ImportBuffer()`

Source: [Render Graph](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/manual/render-graph-system.html)

## Rendering Optimization

### Draw Call Batching

Batching combines meshes using the same material so Unity renders them with fewer render state updates.

**SRP Batcher** (URP/HDRP only):
- Reduces CPU time for draw calls by minimizing render-state changes between calls
- Material data persists in GPU memory
- Uses dedicated per-object GPU constant buffer
- For best results: use as few shader variants as possible
- Compatible with URP, HDRP, and custom SRP; NOT Built-in pipeline

**Static Batching:**
- Merges stationary meshes into unified vertex/index buffers (world-space)
- Each buffer supports up to 64,000 vertices
- Works at build time or runtime
- Only for Mesh Renderers (not Skinned Mesh Renderers)

**Dynamic Batching:**
- Transforms vertices to world space on CPU at runtime
- Useful for procedurally generated geometry (particles, lines, trails)
- Meshes limited to 900 vertex attributes or 300 vertices
- **Not recommended** for most uses: CPU overhead may exceed draw call savings
- Not supported in HDRP

**GPU Instancing:**
- Renders multiple instances of the same mesh in one draw call
- Enable via `Material.enableInstancing`
- Add per-instance properties (color, transform) via HLSL macros
- Requires shader support with instancing macros

### Occlusion Culling

Prevents rendering of GameObjects hidden behind others. Works with frustum culling.

- **Baking phase** (Editor): Divides scene into cells, generates visibility data
- **Runtime**: Loads baked data, performs per-camera visibility queries
- **Best for**: GPU-bound projects with overdraw; small areas separated by solid geometry
- **Limitation**: Dynamic objects can be occluded but cannot occlude others
- URP/HDRP: Can use GPU occlusion culling instead of CPU-based approach

Source: [Draw Call Batching](https://docs.unity3d.com/6000.3/Documentation/Manual/DrawCallBatching.html), [SRP Batcher](https://docs.unity3d.com/6000.3/Documentation/Manual/SRPBatcher.html)

## Common Patterns (C#)

### Material Property Access at Runtime

```csharp
// Set shader before modifying properties
material.SetColor("_BaseColor", Color.red);
material.SetFloat("_Smoothness", 0.8f);
material.SetTexture("_BaseMap", myTexture);
if (material.HasProperty("_Metallic"))
    material.SetFloat("_Metallic", 1.0f);
material.EnableKeyword("_EMISSION");
```

### Instance vs Shared Material

```csharp
Renderer rend = GetComponent<Renderer>();
rend.material.color = Color.blue;        // SAFE: creates per-object instance
// rend.sharedMaterial.color = Color.blue; // DANGEROUS: modifies asset for ALL objects
```

### MaterialPropertyBlock (Per-Object Variation Without Material Instances)

```csharp
// WARNING: MaterialPropertyBlock BREAKS SRP Batcher compatibility.
// Use only when SRP Batcher is not critical (e.g., Built-in pipeline, few unique objects).
// For SRP Batcher-compatible per-object variation, use GPU Instancing with instance properties
// or create material instances via renderer.material.
private static readonly int BaseColorID = Shader.PropertyToID("_BaseColor");
private MaterialPropertyBlock _propBlock = new MaterialPropertyBlock();

void SetColor(Color color)
{
    Renderer rend = GetComponent<Renderer>();
    rend.GetPropertyBlock(_propBlock);
    _propBlock.SetColor(BaseColorID, color);
    rend.SetPropertyBlock(_propBlock);
}
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|---|---|---|
| Modifying `renderer.sharedMaterial` at runtime | Changes the material asset; affects ALL objects using it | Use `renderer.material` (creates instance) or `MaterialPropertyBlock` |
| Creating new Material instances every frame | Memory leak; unbounded allocations | Cache material instances; use `MaterialPropertyBlock` for per-object variation |
| Using Surface Shaders in URP/HDRP | Not supported; will fail or render pink | Use Shader Graph or write HLSL shaders |
| Mixing render pipeline assets | Shaders/materials from wrong pipeline render pink | Use pipeline-specific shaders; run material upgrader when switching |
| Non-power-of-two texture dimensions | Compression fails; higher memory usage | Use 32, 64, 128, 256, 512, 1024, 2048, 4096 |
| Enabling dynamic batching by default | CPU overhead often exceeds draw call savings | Prefer SRP Batcher (URP/HDRP) or static batching |
| Too many shader variants | Increased build time, memory, and load time | Strip unused variants; minimize keyword usage |
| Using `Shader.Find()` at runtime | Slow; may fail if shader not included in build | Cache shader references; assign in Inspector |
| Forgetting to call `m_RenderGraph.Cleanup()` | GPU resource leak | Always cleanup in pipeline `Dispose()` |
| Ignoring render queue for transparent objects | Z-fighting, incorrect sort order | Set appropriate `renderQueue`; sort transparent back-to-front |

## Key API Quick Reference

| Class/Struct | Namespace | Purpose |
|---|---|---|
| `Material` | `UnityEngine` | Controls shader properties on a renderer |
| `Shader` | `UnityEngine` | References compiled shader programs |
| `Texture2D` | `UnityEngine` | 2D texture asset |
| `RenderTexture` | `UnityEngine` | GPU-rendered texture target |
| `Camera` | `UnityEngine` | Scene viewpoint and rendering control |
| `Renderer` | `UnityEngine` | Base class for all renderers |
| `MaterialPropertyBlock` | `UnityEngine` | Per-object shader properties without instancing |
| `CommandBuffer` | `UnityEngine.Rendering` | GPU command list |
| `RenderGraph` | `UnityEngine.Rendering.RenderGraphModule` | Frame render pass management |
| `TextureHandle` | `UnityEngine.Rendering.RenderGraphModule` | Render Graph texture reference |
| `BufferHandle` | `UnityEngine.Rendering.RenderGraphModule` | Render Graph buffer reference |
| `RenderGraphBuilder` | `UnityEngine.Rendering.RenderGraphModule` | Configures individual render passes |
| `CoreUtils` | `UnityEngine.Rendering` | Utility methods (DrawFullScreen, etc.) |
| `Volume` | `UnityEngine.Rendering` | Post-processing/environment effect container |
| `VolumeProfile` | `UnityEngine.Rendering` | Collection of volume effect overrides |

## Related Skills

- **unity-lighting-vfx** -- Lighting setup, light types, baking, VFX Graph, particle systems
- **unity-platforms** -- Platform-specific rendering settings, quality tiers, shader stripping
- **unity-2d** -- 2D Renderer (URP), sprite rendering, tilemap rendering

## Additional Resources

- [Render Pipelines Overview](https://docs.unity3d.com/6000.3/Documentation/Manual/render-pipelines.html)
- [URP Documentation](https://docs.unity3d.com/6000.3/Documentation/Manual/universal-render-pipeline.html)
- [HDRP Documentation](https://docs.unity3d.com/6000.3/Documentation/Manual/high-definition-render-pipeline.html)
- [Shader Introduction](https://docs.unity3d.com/6000.3/Documentation/Manual/shader-introduction.html)
- [Shader Graph](https://docs.unity3d.com/6000.3/Documentation/Manual/shader-graph.html)
- [Materials](https://docs.unity3d.com/6000.3/Documentation/Manual/Materials.html)
- [Textures](https://docs.unity3d.com/6000.3/Documentation/Manual/Textures.html)
- [Cameras](https://docs.unity3d.com/6000.3/Documentation/Manual/Cameras.html)
- [Post-Processing](https://docs.unity3d.com/6000.3/Documentation/Manual/PostProcessingOverview.html)
- [Draw Call Batching](https://docs.unity3d.com/6000.3/Documentation/Manual/DrawCallBatching.html)
- [SRP Batcher](https://docs.unity3d.com/6000.3/Documentation/Manual/SRPBatcher.html)
- [Occlusion Culling](https://docs.unity3d.com/6000.3/Documentation/Manual/OcclusionCulling.html)
- [Render Graph API (SRP Core 17.0)](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/manual/render-graph-system.html)
- [Shader Graph 17.0](https://docs.unity3d.com/Packages/com.unity.shadergraph@17.0/manual/index.html)
- [HDRP Features](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@17.0/manual/HDRP-Features.html)
- [Material Scripting API](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/Material.html)
