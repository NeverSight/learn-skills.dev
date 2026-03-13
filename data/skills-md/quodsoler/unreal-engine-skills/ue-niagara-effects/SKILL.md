---
name: ue-niagara-effects
description: "Use this skill when working with Niagara particle systems, VFX, effects, emitter, Niagara component, or Niagara parameter in Unreal Engine C++. Covers spawning systems, setting parameters, data interfaces (SkeletalMesh, StaticMesh, Curve, Array), OnSystemFinished delegate, and performance tuning. See references/niagara-parameter-types.md for type mapping and references/niagara-data-interfaces.md for data interface catalogue. For particle materials, see ue-materials-rendering."
metadata:
  version: 1.0.0
---

# UE Niagara Effects

You are an expert in controlling Unreal Engine's Niagara VFX system from C++.

## Context Check

Read `.agents/ue-project-context.md` before proceeding. Confirm:

- The `Niagara` plugin is listed under enabled plugins (`Plugins/FX/Niagara`).
- The target module's `Build.cs` has `"Niagara"` (and optionally `"NiagaraCore"`) in `PublicDependencyModuleNames`.
- Platform targets: note whether mobile or dedicated-server builds are in scope, because Niagara is
  typically suppressed on dedicated servers and may need LOD simplification on mobile.

## Information Gathering

Before writing Niagara C++ code, clarify:

1. **Effect lifecycle** — one-shot (fire and forget) or persistent / looping?
2. **Parameter needs** — which Niagara User Parameters must be set from gameplay (positions, colors, scalars)?
3. **Data interfaces required** — SkeletalMesh, StaticMesh, Curve, Array, or custom?
4. **Simulation target** — CPU or GPU sim? (affects which DI features are available)
5. **Performance budget** — pooling required? Mobile scalability tier?
6. **Completion handling** — does gameplay need a callback when the effect finishes?

---

## System Structure (UE Concept Map)

```
UNiagaraSystem  (asset: UNiagaraSystem)
  └── UNiagaraEmitter[]         (per-emitter asset, referenced via FNiagaraEmitterHandle)
        └── UNiagaraScript[]   (Spawn / Update / Event scripts; authored in Niagara editor)
              └── Modules       (stack of NiagaraScript nodes; not C++ classes)

Runtime instances:
  UNiagaraComponent             (scene component that drives one UNiagaraSystem instance)
    └── FNiagaraSystemInstance  (internal runtime state; access via GetSystemInstanceController())
```

**Key rule**: authors expose parameters to C++ by setting their namespace to `User.` in the Niagara
editor. Only `User.*` parameters can be overridden at runtime from C++.

---

## Spawning Niagara Systems

### Fire-and-Forget (One-Shot) at World Location

```cpp
#include "NiagaraFunctionLibrary.h"
#include "NiagaraComponent.h"

// Minimal one-shot spawn — component auto-destroys when the system completes.
UNiagaraComponent* NiagaraComp = UNiagaraFunctionLibrary::SpawnSystemAtLocation(
    this,                           // WorldContextObject
    ImpactVFXSystem,                // UPROPERTY(EditAnywhere) UNiagaraSystem*
    HitLocation,                    // FVector Location
    FRotator::ZeroRotator,          // FRotator Rotation
    FVector(1.f),                   // FVector Scale
    /*bAutoDestroy=*/ true,
    /*bAutoActivate=*/ true,
    /*PoolingMethod=*/ ENCPoolMethod::AutoRelease,   // use pool when available
    /*bPreCullCheck=*/ true
);

// Set parameters before the first tick if needed.
if (NiagaraComp)
{
    NiagaraComp->SetVariableVec3(FName("User.HitNormal"), HitNormal);
    NiagaraComp->SetVariableLinearColor(FName("User.HitColor"), DamageColor);
}
```

### Attached to a Component (Persistent / Looping)

```cpp
// Attaches to a socket and stays active until manually deactivated.
UNiagaraComponent* TrailComp = UNiagaraFunctionLibrary::SpawnSystemAttached(
    TrailVFXSystem,
    WeaponMesh,                             // USceneComponent* AttachToComponent
    FName("MuzzleSocket"),                  // FName AttachPointName
    FVector::ZeroVector,
    FRotator::ZeroRotator,
    EAttachLocation::SnapToTarget,
    /*bAutoDestroy=*/ false,
    /*bAutoActivate=*/ true,
    ENCPoolMethod::ManualRelease,
    /*bPreCullCheck=*/ true
);
```

### Persistent Component on an Actor (Preferred for Repeated Use)

```cpp
// In header:
UPROPERTY(VisibleAnywhere)
TObjectPtr<UNiagaraComponent> EngineTrailVFX;

// In constructor:
EngineTrailVFX = CreateDefaultSubobject<UNiagaraComponent>(TEXT("EngineTrailVFX"));
EngineTrailVFX->SetupAttachment(GetRootComponent());
EngineTrailVFX->SetAutoActivate(false);   // start inactive; activate via gameplay

// In gameplay code:
EngineTrailVFX->SetAsset(EngineTrailSystem);    // swap asset without destroying component
EngineTrailVFX->Activate(/*bReset=*/ true);
```

### Lifecycle Control

```cpp
NiagaraComp->Activate(/*bReset=*/ false);       // activate; resume if paused
NiagaraComp->Activate(/*bReset=*/ true);        // activate with full reset
NiagaraComp->Deactivate();                      // stop spawning, let particles drain
NiagaraComp->DeactivateImmediate();             // kill all particles immediately
NiagaraComp->ResetSystem();                     // restart from time 0
NiagaraComp->ReinitializeSystem();              // full re-init + restart (expensive; prefer ResetSystem)
NiagaraComp->SetPaused(true);                   // pause simulation
NiagaraComp->SetAutoDestroy(true);              // destroy component when system finishes
```

---

## Setting Parameters from C++

All setter variants accept the parameter name as `FName` prefixed with its namespace.
User-exposed parameters use the `User.` prefix.

```cpp
// Scalar types
NiagaraComp->SetVariableFloat(FName("User.DamageAmount"), 150.f);
NiagaraComp->SetVariableInt(FName("User.ProjectileCount"), 12);
NiagaraComp->SetVariableBool(FName("User.bIsCritical"), bIsCriticalHit);

// Vector types
NiagaraComp->SetVariableVec2(FName("User.UVOffset"), FVector2D(0.5, 0.25));
NiagaraComp->SetVariableVec3(FName("User.TargetPosition"), TargetLocation);
NiagaraComp->SetVariableVec4(FName("User.CustomData"), FVector4(1, 0.5, 0, 1));
NiagaraComp->SetVariableLinearColor(FName("User.TintColor"), FLinearColor::Red);
NiagaraComp->SetVariableQuat(FName("User.Orientation"), GetActorQuat());

// Object / Actor references (binds DI override)
NiagaraComp->SetVariableObject(FName("User.TargetMesh"), SkeletalMeshComponent);
NiagaraComp->SetVariableActor(FName("User.SourceActor"), this);

// Position (LWC-aware alias for vec3)
NiagaraComp->SetVariablePosition(FName("User.WorldOrigin"), WorldSpaceOrigin);

// Material / Texture overrides
NiagaraComp->SetVariableMaterial(FName("User.FXMaterial"), DynamicMaterial);
NiagaraComp->SetVariableTexture(FName("User.FlowMap"), FlowTexture);

// Read a float parameter back (returns bIsValid=false when name not found)
bool bIsValid = false;
float CurrentValue = NiagaraComp->GetVariableFloat(FName("User.EmitRate"), bIsValid);
```

### Blueprint-Accessible Legacy Signatures (prefer FName variants above)

```cpp
// Old FString signatures still work but are slower due to FName conversion.
NiagaraComp->SetNiagaraVariableFloat(TEXT("User.SpeedScale"), 2.f);
NiagaraComp->SetNiagaraVariableVec3(TEXT("User.ImpactPoint"), Location);
NiagaraComp->SetNiagaraVariableLinearColor(TEXT("User.Color"), FLinearColor::Blue);
```

### Parameter Namespaces Reference

| Namespace prefix | Settable from C++ | Description                          |
|------------------|-------------------|--------------------------------------|
| `User.`          | Yes               | User-exposed; main runtime override  |
| `System.`        | No (read-only)    | System-level built-ins (Age, DeltaTime, etc.) |
| `Emitter.`       | No (internal)     | Per-emitter variables                |
| `Particle.`      | No (internal)     | Per-particle variables               |

See `references/niagara-parameter-types.md` for the full C++ type to Niagara type mapping.

---

## Data Interfaces from C++

Data interfaces (DIs) are `UObject`-derived assets that expose structured external data to Niagara
scripts. They appear as `User.*` parameters of DI type in the Niagara editor, and are overridden
at runtime via `SetVariableObject` or the specialized function library helpers.

### Binding Skeletal Mesh DI

```cpp
#include "NiagaraFunctionLibrary.h"

// Override the "User.SourceMesh" skeletal mesh DI on a running component.
UNiagaraFunctionLibrary::OverrideSystemUserVariableSkeletalMeshComponent(
    NiagaraComp,
    TEXT("User.SourceMesh"),    // must match the DI's User parameter name in the asset
    GetMesh()                   // USkeletalMeshComponent*
);

// Restrict which bones spawn from (destructive — modifies the DI instance data).
UNiagaraFunctionLibrary::SetSkeletalMeshDataInterfaceFilteredBones(
    NiagaraComp,
    TEXT("User.SourceMesh"),
    { FName("hand_l"), FName("hand_r") }
);

// Restrict which sampling regions to use.
UNiagaraFunctionLibrary::SetSkeletalMeshDataInterfaceSamplingRegions(
    NiagaraComp,
    TEXT("User.SourceMesh"),
    { FName("HeadRegion") }
);
```

### Binding Static Mesh DI

```cpp
// Override via component reference.
UNiagaraFunctionLibrary::OverrideSystemUserVariableStaticMeshComponent(
    NiagaraComp,
    TEXT("User.ScatterMesh"),
    StaticMeshComp
);

// Override with a raw UStaticMesh asset pointer.
UNiagaraFunctionLibrary::OverrideSystemUserVariableStaticMesh(
    NiagaraComp,
    TEXT("User.ScatterMesh"),
    LoadedStaticMesh
);
```

### Reading / Modifying an Array DI at Runtime

```cpp
#include "NiagaraDataInterfaceArrayFunctionLibrary.h"

// Push a new float array into the effect (e.g., damage heatmap values).
TArray<float> HeatValues = ComputeHeatValues();
UNiagaraDataInterfaceArrayFunctionLibrary::SetNiagaraArrayFloat(
    NiagaraComp, FName("User.HeatData"), HeatValues
);

// Update a single element without replacing the whole array.
UNiagaraDataInterfaceArrayFunctionLibrary::SetNiagaraArrayFloatValue(
    NiagaraComp, FName("User.HeatData"), /*Index=*/ 5, /*Value=*/ 0.9f, /*bSizeToFit=*/ false
);

// Other strongly-typed array setters available:
// SetNiagaraArrayVector, SetNiagaraArrayVector4, SetNiagaraArrayColor,
// SetNiagaraArrayQuat, SetNiagaraArrayInt32, SetNiagaraArrayBool, etc.
```

### Direct DI Object Access (Advanced)

```cpp
// Retrieve the actual DI UObject to mutate its properties directly.
// Template variant resolves the cast automatically.
UNiagaraDataInterfaceCurve* CurveDI =
    UNiagaraFunctionLibrary::GetDataInterface<UNiagaraDataInterfaceCurve>(
        NiagaraComp, FName("User.SpeedCurve")
    );

if (CurveDI)
{
    // Mutate curve keyframes at runtime (rebuilds LUT internally).
    CurveDI->Curve.AddKey(0.f, 0.f);
    CurveDI->Curve.AddKey(1.f, 500.f);
    // UpdateLUT() is WITH_EDITORONLY_DATA — only call in editor builds.
#if WITH_EDITORONLY_DATA
    CurveDI->UpdateLUT();
#endif
}

// Non-template variant when the DI class is only known at runtime.
UNiagaraDataInterface* GenericDI =
    UNiagaraFunctionLibrary::GetDataInterface(
        UNiagaraDataInterfaceStaticMesh::StaticClass(),
        NiagaraComp,
        FName("User.ImpactMesh")
    );
```

See `references/niagara-data-interfaces.md` for the full built-in DI catalogue.

**Custom Data Interfaces**: Subclass `UNiagaraDataInterface`, override `GetFunctions()` to define
available functions, `GetVMExternalFunction()` to bind C++ implementations, and optionally
`ProvidePerInstanceDataForRenderThread()` for GPU access. Register in the module's `StartupModule`.
This enables game-specific data (inventory, terrain) to feed directly into Niagara systems.

---

## Completion Callbacks

```cpp
// Bind a C++ delegate to fire when the Niagara system finishes all particles.
// FOnNiagaraSystemFinished is DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(, UNiagaraComponent*)
NiagaraComp->OnSystemFinished.AddDynamic(this, &UMyComponent::OnVFXFinished);

// The callback signature:
UFUNCTION()
void UMyComponent::OnVFXFinished(UNiagaraComponent* FinishedComponent)
{
    // Called on game thread when every particle has expired and the system is done.
    FinishedComponent->DestroyComponent();
    // or return it to pool, notify gameplay, etc.
}

// Unbind when the owner is destroyed to avoid stale delegates.
NiagaraComp->OnSystemFinished.RemoveDynamic(this, &UMyComponent::OnVFXFinished);
```

---

## Performance: Pooling

`ENCPoolMethod` controls the pool behavior on every spawn call:

- `AutoRelease` — component returns to the world pool automatically when the system finishes.
  Pass `bAutoDestroy=true`; the pool handles actual reclaim.
- `ManualRelease` — you control when the component returns; call `ReleaseToPool()` to reclaim.
- `None` — no pooling; component is destroyed when finished if `bAutoDestroy=true`.

```cpp
// AutoRelease: most common for one-shots (explosions, impacts).
UNiagaraComponent* Comp = UNiagaraFunctionLibrary::SpawnSystemAtLocation(
    this, ExplosionSystem, Location, FRotator::ZeroRotator,
    FVector(1.f), /*bAutoDestroy=*/true, /*bAutoActivate=*/true,
    ENCPoolMethod::AutoRelease
);

// ManualRelease: for effects you pause/resume (e.g., a beam while a button is held).
// Reclaim by calling ReleaseToPool() when done.
TrailComp->ReleaseToPool();

// Prime the pool before a gameplay-critical moment via FNiagaraWorldManager.
if (FNiagaraWorldManager* NiagaraWorldMan = FNiagaraWorldManager::Get(GetWorld()))
{
    NiagaraWorldMan->GetComponentPool()->PrimePool(ExplosionSystem, GetWorld());
}
```

Pool capacity is configured per-system in the `UNiagaraSystem` pooling settings (not a global CVar).
Relevant global pool CVars: `FX.NiagaraComponentPool.Enable` (1/0) and
`FX.NiagaraComponentPool.KillUnusedTime` (seconds before idle components are culled).

---

## Performance: Scalability and LOD

```cpp
// Allow the scalability manager to cull this component based on distance and budget.
NiagaraComp->SetAllowScalability(true);   // default true; disable for gameplay-critical VFX

// Adjust tick behavior to avoid unnecessary dependency resolution.
// ENiagaraTickBehavior::UsePrereqs  — default; ticks after its prerequisites
// ENiagaraTickBehavior::ForceTickFirst — useful for VFX that leads all tick groups
NiagaraComp->SetTickBehavior(ENiagaraTickBehavior::UsePrereqs);
```

Scalability per platform is configured in the `UNiagaraEffectType` asset assigned to the
`UNiagaraSystem`. The effect type defines quality tiers (Low / Medium / High / Epic) and which
emitters are stripped at each tier. This is data-driven; no C++ changes needed per platform.

**GPU vs CPU simulation trade-offs**:
- CPU sim: particle data is readable/writable from C++ each frame; lower particle counts; supports
  all DI types.
- GPU sim: supports hundreds of thousands of particles; DI support is limited (not all CPU-side DIs
  have GPU equivalents); particle data is not readable back to CPU without readbacks.

**Determinism**: GPU simulations are inherently non-deterministic. For multiplayer VFX that must
match across clients, use CPU simulation with `FixedTickDelta` on the emitter. Cosmetic-only
effects should spawn client-side only — skip them on dedicated servers entirely.

---

## Warm-Up, Server Handling, and Events

**Pre-simulation (warm-up)**: seek to a desired age before the effect is visible.
```cpp
NiagaraComp->SetDesiredAge(2.5f);    // age in seconds
NiagaraComp->SeekToDesiredAge(2.5f); // perform seek immediately (skips simulation steps)
// FFXSystemSpawnParameters (used by SpawnSystemAtLocationWithParams) also exposes DesiredAge.
```

**Dedicated server**: `SpawnSystemAtLocation` returns `nullptr` on dedicated servers. Always null-check
the returned component and guard VFX spawns with `!IsRunningDedicatedServer()` where needed.

**Gameplay events to Niagara**: Niagara's internal event system (Location Events, Death Events,
Collision Events) is configured in the Niagara editor between emitters. From C++, trigger a
gameplay-driven burst by updating a User bool parameter that the spawn script reads:
```cpp
NiagaraComp->SetVariableBool(FName("User.bJustDied"), true);
// Niagara reads this flag on the next spawn script tick and fires the burst.
// There is no C++ API to inject raw Niagara events directly — use User parameters as the bridge.
```

---

## Required Build.cs

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "Core",
    "CoreUObject",
    "Engine",
    "Niagara",         // UNiagaraComponent, UNiagaraFunctionLibrary, UNiagaraSystem
    "NiagaraCore",     // UNiagaraDataInterface base (NiagaraCore module)
});
```

---

## Common Mistakes and Anti-Patterns

**Spawning a new system component every tick**
```cpp
// BAD: Creates a new UNiagaraComponent each frame. Destroys performance.
void AMyActor::Tick(float DeltaTime)
{
    UNiagaraFunctionLibrary::SpawnSystemAtLocation(this, TrailFX, GetActorLocation());
}

// GOOD: Create the component once in BeginPlay or constructor; activate/deactivate as needed.
```

**Wrong parameter namespace**
```cpp
// BAD: "Emitter.Speed" is an internal emitter parameter; cannot be set from C++.
NiagaraComp->SetVariableFloat(FName("Emitter.Speed"), 300.f);

// GOOD: The Niagara author must expose the parameter under "User.*".
NiagaraComp->SetVariableFloat(FName("User.Speed"), 300.f);
```

**Type mismatch between C++ and Niagara**
```cpp
// BAD: Calling SetVariableVec3 on a parameter that is typed as "Color" in Niagara.
// Silently fails — no runtime error, parameter is just not updated.
NiagaraComp->SetVariableVec3(FName("User.TintColor"), FVector(1, 0, 0));

// GOOD: Match the C++ call to the Niagara parameter type.
NiagaraComp->SetVariableLinearColor(FName("User.TintColor"), FLinearColor::Red);
```

**Setting parameters after system completes**
```cpp
// The component is valid but the system instance may be inactive. Check before setting.
if (NiagaraComp && NiagaraComp->IsActive())
{
    NiagaraComp->SetVariableFloat(FName("User.Intensity"), NewIntensity);
}
```

**Forgetting to check nullptr on spawn (especially on server)**
```cpp
UNiagaraComponent* Comp = UNiagaraFunctionLibrary::SpawnSystemAtLocation(...);
// Comp can be nullptr on dedicated server or when bPreCullCheck rejects the spawn.
if (Comp)
{
    Comp->SetVariableFloat(FName("User.Scale"), 2.f);
}
```

**Not removing delegates before destruction**
```cpp
// BAD: OnSystemFinished fires after owner is garbage collected → crash.
// GOOD: Always RemoveDynamic in BeginDestroy or EndPlay.
void AMyActor::EndPlay(const EEndPlayReason::Type Reason)
{
    if (NiagaraComp)
    {
        NiagaraComp->OnSystemFinished.RemoveDynamic(this, &AMyActor::OnVFXFinished);
    }
    Super::EndPlay(Reason);
}
```

**Niagara Fluids (experimental)**: The Niagara Fluids plugin provides GPU-based fluid and gas
simulations. It is experimental, GPU-only, and carries a high performance cost — profile carefully
before shipping and restrict use to hero effects where visual impact justifies the budget.

**World space vs local space**: Use local-space simulation for effects attached to moving actors
(particles inherit the parent component's transform and move with it). Use world-space simulation
for effects that should remain stationary after emission (e.g., a ground impact crater where
particles should not follow a moving actor). The space setting lives on each emitter in the Niagara editor.

---

## Related Skills

- `ue-actor-component-architecture` — component creation, attachment, lifecycle
- `ue-materials-rendering` — particle material setup, dynamic material instances
- `ue-cpp-foundations` — UObject lifetime, delegates, UPROPERTY references
