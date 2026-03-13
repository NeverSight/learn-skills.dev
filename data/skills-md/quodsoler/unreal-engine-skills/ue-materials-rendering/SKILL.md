---
name: ue-materials-rendering
description: "Use when the user is working with material, shader, MID, dynamic material, material instance, post-process, render target, parameter collection, decal, Nanite, Lumen, or rendering in Unreal Engine. See references/material-parameter-reference.md for parameter patterns and references/post-process-settings.md for post-process settings. For particle rendering, see ue-niagara-effects."
metadata:
  version: 1.0.0
---

# UE Materials and Rendering

You are an expert in Unreal Engine's material and rendering systems. You provide accurate C++ patterns for dynamic materials, parameter collections, post-process, render targets, decals, and UE5 rendering features (Nanite, Lumen, Virtual Shadow Maps).

---

## Step 1: Read Project Context

Read `.agents/ue-project-context.md` before giving advice. From it, extract:

- **Engine version** — UE5.0–5.4 APIs differ (e.g., `SetNaniteOverride` added in 5.x; `CopyScalarAndVectorParameters` signature changed in 5.7)
- **Target platforms** — Mobile requires forward rendering; many post-process features are desktop-only
- **Rendering settings** — Nanite/Lumen enabled status affects which material features are safe
- **Module names** — needed for correct `#include` paths and `Build.cs` dependencies

If the context file is missing, ask for engine version and target platforms before proceeding.

---

## Step 2: Clarify the Rendering Need

Ask which area the user needs:

1. **Dynamic Material Instances (MID)** — runtime parameter changes on mesh components
2. **Material Parameter Collections** — global parameters shared across all materials
3. **Post-Process** — bloom, exposure, color grading, DOF, AO via volumes or components
4. **Render Targets** — scene capture, minimap, security camera, canvas drawing
5. **Decals** — deferred decals spawned at runtime, fade, sort order
6. **Rendering Pipeline / UE5 Features** — Nanite, Lumen, Virtual Shadow Maps, custom depth/stencil

Multiple areas can be combined.

---

## Core Patterns

### 1. Dynamic Material Instances (MID)

#### Creation

**Pattern A — from UMaterialInterface (standalone, not tied to a component slot):**

```cpp
// Header
UPROPERTY()
TObjectPtr<UMaterialInstanceDynamic> MyMID;

// Implementation — call once (BeginPlay or equivalent), cache the result
UMaterialInterface* BaseMat = LoadObject<UMaterialInterface>(
    nullptr, TEXT("/Game/Materials/M_MyBase.M_MyBase"));

MyMID = UMaterialInstanceDynamic::Create(BaseMat, this);
```

**Pattern B — via component slot (preferred for meshes):**

```cpp
// UMeshComponent::CreateDynamicMaterialInstance creates a MID for the given
// element index and assigns it to the slot automatically.
// Signature: CreateDynamicMaterialInstance(int32 ElementIndex,
//                UMaterialInterface* SourceMaterial = nullptr,
//                FName OptionalName = NAME_None)

UMaterialInstanceDynamic* MID = MeshComponent->CreateDynamicMaterialInstance(
    0,            // element index
    nullptr,      // nullptr = use the slot's current material as parent
    TEXT("MyMID") // optional debug name
);
```

Source: `MaterialInstanceDynamic.h`, `PrimitiveComponent.h`. Build.cs: `"Engine"`.

#### Setting Parameters

```cpp
MyMID->SetScalarParameterValue(TEXT("Opacity"), 0.5f);
MyMID->SetVectorParameterValue(TEXT("BaseColor"), FLinearColor(1.f, 0.2f, 0.1f, 1.f));
MyMID->SetVectorParameterValue(TEXT("Offset"), FLinearColor(0.f, 0.f, 100.f, 0.f)); // XYZ via FLinearColor
MyMID->SetTextureParameterValue(TEXT("DamageMask"), MyTexture);
MyMID->SetTextureParameterValue(TEXT("SecurityFeed"), RenderTargetAsset); // RT as texture
```

Full setter signatures from `MaterialInstanceDynamic.h`:
```cpp
void SetScalarParameterValue(FName ParameterName, float Value);
void SetVectorParameterValue(FName ParameterName, FLinearColor Value);  // Pass FLinearColor; no implicit conversion from FVector
void SetTextureParameterValue(FName ParameterName, UTexture* Value);
```

#### High-Frequency Updates — Index-Based API

When setting dozens of parameters per frame (rare but valid), use index caching:

```cpp
// In BeginPlay or initialization — call once per parameter name:
int32 OpacityIndex = -1;
MyMID->InitializeScalarParameterAndGetIndex(TEXT("Opacity"), 1.0f, OpacityIndex);

// In Tick — use index, no name lookup:
if (OpacityIndex >= 0)
{
    MyMID->SetScalarParameterByIndex(OpacityIndex, NewOpacity);
}
```

Index is invalidated if the parent material changes. Do not share indices across different MID instances.

#### MID Lifecycle and GC

MIDs are `UObject`s — they are garbage collected when unreferenced. To keep a MID alive:

```cpp
// In your class header — must be UPROPERTY to prevent GC
UPROPERTY()
TObjectPtr<UMaterialInstanceDynamic> CachedMID;
```

Never store MIDs in raw pointers or local variables across frames.

#### Additional MID Operations

```cpp
// Lerp between two instances' scalar/vector params
MyMID->K2_InterpolateMaterialInstanceParams(InstanceA, InstanceB, Alpha);

// Assign Nanite-compatible override material (UE5)
MyMID->SetNaniteOverride(NaniteCompatibleMaterial);
```

---

### 2. Material Parameter Collections

`UMaterialParameterCollection` is an asset holding scalar and vector parameters accessible from any material via `CollectionParameter` expression. One GPU buffer update propagates to all referencing materials. Source: `MaterialParameterCollection.h`, `MaterialParameterCollectionInstance.h`.

#### Setting Parameters at Runtime

```cpp
// MyCollection is a UPROPERTY(EditAnywhere) pointing to the MPC asset.
UPROPERTY(EditAnywhere, Category="Rendering")
TObjectPtr<UMaterialParameterCollection> GlobalRenderingCollection;

// At runtime — get the per-world instance and set values:
void AMyActor::UpdateGlobalWeather(float RainIntensity, FLinearColor FogColor)
{
    UMaterialParameterCollectionInstance* Instance =
        GetWorld()->GetParameterCollectionInstance(GlobalRenderingCollection);

    if (Instance)
    {
        Instance->SetScalarParameterValue(TEXT("RainIntensity"), RainIntensity);
        Instance->SetVectorParameterValue(TEXT("FogColor"), FogColor);
    }
}
```

Both setters return `false` if the parameter name is not found. Names are case-sensitive. Limits: max 1024 scalars + 1024 vectors per collection; no texture parameters; global to the world instance.

---

### 3. Post-Process Volumes

`APostProcessVolume` wraps `FPostProcessSettings` and controls how the camera is rendered when inside (or globally when `bUnbound = true`).

From `PostProcessVolume.h`:
```cpp
struct FPostProcessSettings Settings; // The settings payload
float Priority;      // Higher priority wins on overlap (undefined order when equal)
float BlendRadius;   // World-space blend distance in cm (only when bUnbound = false)
float BlendWeight;   // 0 = no effect, 1 = full effect
uint32 bEnabled:1;
uint32 bUnbound:1;   // true = applies globally regardless of camera position
```

#### Modifying a Post-Process Volume from C++

```cpp
// Assume PostProcessVolume is assigned or found:
APostProcessVolume* PPV = /* find or spawn */;

// Enable and configure
PPV->bEnabled = true;
PPV->bUnbound = true; // global effect
PPV->BlendWeight = 1.0f;

// Bloom
PPV->Settings.bOverride_BloomIntensity = true;
PPV->Settings.BloomIntensity = 0.5f;

// Auto Exposure
PPV->Settings.bOverride_AutoExposureMinBrightness = true;
PPV->Settings.AutoExposureMinBrightness = 0.1f;
PPV->Settings.bOverride_AutoExposureMaxBrightness = true;
PPV->Settings.AutoExposureMaxBrightness = 2.0f;

// Depth of Field (Cinematic DOF)
PPV->Settings.bOverride_DepthOfFieldFstop = true;
PPV->Settings.DepthOfFieldFstop = 2.8f;
PPV->Settings.bOverride_DepthOfFieldFocalDistance = true;
PPV->Settings.DepthOfFieldFocalDistance = 300.0f; // cm

// Ambient Occlusion
PPV->Settings.bOverride_AmbientOcclusionIntensity = true;
PPV->Settings.AmbientOcclusionIntensity = 0.5f;

// Vignette
PPV->Settings.bOverride_VignetteIntensity = true;
PPV->Settings.VignetteIntensity = 0.4f;

// Color Grading
PPV->Settings.bOverride_ColorSaturation = true;
PPV->Settings.ColorSaturation = FVector4(1.2f, 1.0f, 0.8f, 1.0f); // per-channel RGBA
PPV->Settings.bOverride_FilmSlope = true;
PPV->Settings.FilmSlope = 0.88f; // 0–1 (default 0.88)
```

Every field in `FPostProcessSettings` has a corresponding `bOverride_*` bool that must be set to `true` for the value to take effect. See `references/post-process-settings.md` for a full field reference.

#### Post-Process Materials (Blendables)

Material Domain must be "Post Process". Add via:
```cpp
PPV->AddOrUpdateBlendable(PostProcessMaterial, 1.0f); // weight 0.0–1.0
```

#### UPostProcessComponent (Actor-Owned)

```cpp
// Constructor
PostProcessComp = CreateDefaultSubobject<UPostProcessComponent>(TEXT("PostProcess"));
PostProcessComp->bUnbound = true;
PostProcessComp->Priority = 5.0f;

// Runtime
PostProcessComp->Settings.bOverride_BloomIntensity = true;
PostProcessComp->Settings.BloomIntensity = 1.5f;
```

Includes: `"Components/PostProcessComponent.h"`, `"Engine/PostProcessVolume.h"`, `"Engine/Scene.h"`.

---

### 4. Render Targets

#### Creating a Render Target in C++

```cpp
#include "Engine/TextureRenderTarget2D.h"
#include "Kismet/KismetRenderingLibrary.h"

// Option A — via UKismetRenderingLibrary (handles resource init automatically)
UTextureRenderTarget2D* RT = UKismetRenderingLibrary::CreateRenderTarget2D(
    this,          // WorldContextObject
    512,           // Width
    512,           // Height
    RTF_RGBA16f,   // Format (see ETextureRenderTargetFormat)
    FLinearColor::Black,
    false          // bAutoGenerateMipMaps
);

// Option B — manual creation
UTextureRenderTarget2D* RT = NewObject<UTextureRenderTarget2D>(this);
RT->InitCustomFormat(512, 512, PF_FloatRGBA, /*bInForceLinearGamma=*/true);
RT->UpdateResourceImmediate(/*bClearRenderTarget=*/true);
```

`ETextureRenderTargetFormat` values from `TextureRenderTarget2D.h`:
| Format | Channels | Bits/Channel | Use Case |
|--------|----------|-------------|----------|
| `RTF_RGBA8` | RGBA | 8 fixed | LDR color, UI |
| `RTF_RGBA8_SRGB` | RGBA | 8 fixed | sRGB color |
| `RTF_RGBA16f` | RGBA | 16 float | HDR color (default) |
| `RTF_RGBA32f` | RGBA | 32 float | High precision data |
| `RTF_R16f` | R | 16 float | Single channel data |
| `RTF_RGB10A2` | RGB+A | 10+2 bit | Display output |

#### Scene Capture (Security Camera / Minimap)

```cpp
#include "Components/SceneCaptureComponent2D.h"

// In actor constructor
SceneCapture = CreateDefaultSubobject<USceneCaptureComponent2D>(TEXT("SceneCapture"));
SceneCapture->SetupAttachment(RootComponent);
SceneCapture->FOVAngle = 90.f;
SceneCapture->CaptureSource = ESceneCaptureSource::SCS_FinalColorLDR; // or SCS_SceneColorHDR
SceneCapture->bCaptureEveryFrame = true;  // continuous update

// Assign a render target asset or a runtime-created one
SceneCapture->TextureTarget = MyRenderTargetAsset;

// Limit what's captured for performance
SceneCapture->ShowFlags.SetAtmosphere(false);
SceneCapture->ShowFlags.SetFog(false);
```

#### Drawing a Material to a Render Target

```cpp
// Renders a full-screen quad with Material applied to TextureTarget.
// This is expensive (sets render target each call); use canvas API for batching.
UKismetRenderingLibrary::DrawMaterialToRenderTarget(
    this,         // WorldContextObject
    RT,           // UTextureRenderTarget2D*
    MyMaterial    // UMaterialInterface*
);
```

#### Canvas Drawing (Batched)

```cpp
UCanvas* Canvas;
FVector2D CanvasSize;
FDrawToRenderTargetContext Context;

UKismetRenderingLibrary::BeginDrawCanvasToRenderTarget(this, RT, Canvas, CanvasSize, Context);

// Draw primitives to Canvas here...
Canvas->K2_DrawMaterial(MyMaterial, FVector2D(0, 0), CanvasSize, FVector2D(0, 0), FVector2D(1, 1));

UKismetRenderingLibrary::EndDrawCanvasToRenderTarget(this, Context);
```

**`UCanvasRenderTarget2D`** — subclass of `UTextureRenderTarget2D` with a built-in `OnCanvasRenderTargetUpdate` delegate. Use for automatic 2D canvas redraw (minimaps, runtime texture painting) instead of manual `BeginDrawCanvasToRenderTarget` calls.

#### Reading Pixels (GPU Stall — Offline Only)

```cpp
// WARNING: stalls GPU pipeline. Editor tools / screenshot only, never per-frame.
FColor Pixel = UKismetRenderingLibrary::ReadRenderTargetPixel(this, RT, X, Y);
TArray<FColor> Pixels;
UKismetRenderingLibrary::ReadRenderTarget(this, RT, Pixels);               // whole RT, 8-bit sRGB
FLinearColor Raw = UKismetRenderingLibrary::ReadRenderTargetRawPixel(this, RT, X, Y);
```

---

### 5. Decals

`UDecalComponent` projects a material onto surfaces. Key API from `DecalComponent.h`:

```cpp
void SetDecalMaterial(UMaterialInterface* NewDecalMaterial);
UMaterialInstanceDynamic* CreateDynamicMaterialInstance(); // MID on the decal
void SetFadeOut(float StartDelay, float Duration, bool DestroyOwnerAfterFade = true);
void SetFadeIn(float StartDelay, float Duration);
void SetSortOrder(int32 Value);  // higher = draws on top
void SetLifeSpan(float LifeSpan);
FVector DecalSize; // local-space extent (not component scale)
```

#### Spawning Decals at Runtime

```cpp
// 0.0f lifespan = persistent; >0.0f = auto-destroy after N seconds
UDecalComponent* Decal = UGameplayStatics::SpawnDecalAtLocation(
    this, DecalMaterial, FVector(200.f), HitLocation, HitNormal.Rotation(), 0.0f);

// Dynamic parameters on the decal
UMaterialInstanceDynamic* DecalMID = Decal->CreateDynamicMaterialInstance();
DecalMID->SetScalarParameterValue(TEXT("Opacity"), 0.8f);
```

#### DBuffer vs Non-DBuffer Decals

- **DBuffer** (Translucent + DBuffer enabled): writes before lighting, affects diffuse/normals/roughness. Enable via `Project Settings > Rendering > DBuffer Decals`.
- **Non-DBuffer**: rendered after lighting, emissive/opacity only; cheaper but limited.

For level-placed decals, use `ADecalActor` (a wrapper around `UDecalComponent`). For runtime-spawned decals, prefer `UGameplayStatics::SpawnDecalAtLocation` or `SpawnDecalAttached`.

---

### 6. Nanite and Lumen (UE5)

#### Nanite

Nanite is UE5's virtualized geometry system. Material compatibility rules:

| Feature | Nanite Compatible |
|---------|------------------|
| Opaque materials | Yes |
| Two-sided materials | Yes |
| Masked materials | Yes (with `r.Nanite.AllowMaskedMaterials=1`) |
| Translucent materials | No — falls back to non-Nanite path |
| World Position Offset (WPO) | Supported in UE 5.1+ (`bEvaluateWorldPositionOffset` on mesh) |
| Pixel Depth Offset | No |
| Custom vertex normals via shader | Limited |

Check at runtime:
```cpp
// Check if a static mesh component is using Nanite (IsNaniteEnabled is on UStaticMesh, not on the component)
bool bIsNanite = StaticMeshComponent->GetStaticMesh() && StaticMeshComponent->GetStaticMesh()->IsNaniteEnabled();
```

Override material for Nanite path:
```cpp
MyMID->SetNaniteOverride(NaniteCompatibleMaterial);
```

#### Lumen

Lumen is UE5's dynamic GI and reflections system. Emissive surfaces can act as lights. Translucent surfaces are not traced by default. Control quality via post-process settings:

```cpp
PPV->Settings.bOverride_LumenReflectionQuality = true;
PPV->Settings.LumenReflectionQuality = 1.0f;         // 0–4

PPV->Settings.bOverride_LumenSceneDetail = true;
PPV->Settings.LumenSceneDetail = 1.0f;               // surface cache resolution multiplier

PPV->Settings.bOverride_LumenSceneLightingQuality = true;
PPV->Settings.LumenSceneLightingQuality = 1.0f;
```

Performance: `r.Lumen.SurfaceCache.UpdateDownsampleFactor` controls cache update rate.

#### Deferred vs Forward Rendering

**Deferred vs Forward**: UE5 desktop uses deferred rendering by default — geometry writes to GBuffer, then lighting is computed per-pixel. Forward rendering (mobile, VR) processes lighting per-object, supports MSAA, but limits dynamic light count. Set via `Project Settings > Rendering > Forward Shading`.

**Scalability**: Use `Scalability::SetQualityLevels()` (in `Scalability.h`) or console commands such as `sg.PostProcessQuality 0-3` to adjust rendering quality at runtime. Configure presets in `BaseScalability.ini`.

#### Virtual Shadow Maps (VSM)

- WPO materials: enable "Evaluate World Position Offset" in the material's Details panel (material editor setting, not a C++ property) for correct VSM shadows.
- Masked materials: opacity masks respected correctly.
- Decals do not cast VSM shadows.

#### Custom Depth / Stencil (Outlines and Effects)

```cpp
MeshComponent->SetRenderCustomDepth(true);
MeshComponent->SetCustomDepthStencilValue(1); // 0–255
// Sample CustomDepth / CustomStencil nodes in a post-process material for outlines, X-ray, highlight effects.
```

Enable: `Project Settings > Rendering > Custom Depth-Stencil Pass > Enabled with Stencil`.

---

## Common Mistakes and Anti-Patterns

**Creating MIDs every frame** — Each `CreateDynamicMaterialInstance` call allocates a new GPU resource. Create once in `BeginPlay`, cache, update in `Tick`:

```cpp
// BeginPlay
CachedMID = MeshComponent->CreateDynamicMaterialInstance(0);

// Tick
if (CachedMID) { CachedMID->SetScalarParameterValue(TEXT("Time"), GetWorld()->TimeSeconds); }
```

**Not caching MID as UPROPERTY** — Raw `UMaterialInstanceDynamic*` is invisible to GC and collected on the next GC pass. Use `UPROPERTY() TObjectPtr<UMaterialInstanceDynamic> CachedMID;`.

**Wrong parameter names** — Names are case-sensitive exact matches. `"basecolor"`, `"Base Color"`, and `"Base_Color"` all silently fail if the material uses `"BaseColor"`.

**Render target resolution** — Match resolution to use: 256–512 for minimap/security camera, 512 max for mirrors; use planar reflections for large mirrors. Full-screen: use `bMainViewResolution` on `USceneCaptureComponent2D`.

**Reading render target pixels per frame** — `ReadRenderTargetPixel` stalls the GPU pipeline. Never call per frame. Use `FRHIGPUTextureReadback` for async non-stalling reads.

**MIDs on replicated actors** — MIDs are client-local. Do not replicate the MID pointer. Replicate the scalar/vector values and re-apply via `OnRep` functions on each client.

**Post-process bOverride not set** — Every `FPostProcessSettings` field requires its paired `bOverride_*` bool set to `true`. Setting a value without the override is a silent no-op.

**Nanite translucency fallback** — Translucent materials on Nanite meshes revert the full mesh to non-Nanite rendering. Split into separate opaque and translucent components.

---

## Required Build.cs Dependencies

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "Engine",           // Materials, render targets, UTextureRenderTarget2D
    "RenderCore",       // Low-level render utilities
    "RHI",              // RHI types (EPixelFormat, etc.)
});

// For UKismetRenderingLibrary:
// Already available via "Engine" — no separate module needed.
```

---

## Related Skills

- `ue-cpp-foundations` — UObject management, UPROPERTY, TObjectPtr, garbage collection
- `ue-actor-component-architecture` — setting up components (UDecalComponent, USceneCaptureComponent2D, UPostProcessComponent)
- `ue-niagara-effects` — particle materials use MIDs; parameter passing into Niagara from C++
- `ue-project-context` — engine version, target platforms, rendering feature flags
