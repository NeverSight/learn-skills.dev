---
name: ue-physics-collision
description: "Use when implementing collision detection, trace queries, physics simulation, or physical interactions in Unreal Engine. Triggers on: 'collision', 'trace', 'LineTrace', 'line trace', 'overlap', 'physics', 'hit result', 'sweep', 'collision channel', 'physics body', 'Chaos', 'raytrace', 'OnHit', 'OnBeginOverlap'. See related skills for component architecture and AI navigation."
metadata:
  version: 1.0.0
---

# UE Physics & Collision

You are an expert in Unreal Engine's physics and collision systems, including collision channels, trace queries, collision events, physics bodies, and the Chaos physics engine.

---

## Step 1: Read Project Context

Read `.agents/ue-project-context.md` to confirm:
- UE version (Chaos is the default physics backend from UE 5.0; PhysX was deprecated)
- Which modules need `"PhysicsCore"` and `"Engine"` in their `Build.cs`
- Whether the project uses skeletal meshes with physics assets, or primarily static mesh collision
- Dedicated server targets (affects whether physics simulation should run server-side)

---

## Step 2: Identify the Need

Ask which area applies if not stated:
1. **Collision setup** — channels, profiles, responses on components
2. **Trace queries** — line traces, sweeps, overlap queries for gameplay logic
3. **Collision events** — OnComponentHit, OnBeginOverlap, OnEndOverlap delegates
4. **Physics simulation** — rigid body sim, forces, impulses, damping, constraints
5. **Physical materials** — friction, restitution, surface type detection

---

## Collision Channels & Profiles

### ECollisionChannel — built-in channels

```cpp
ECC_WorldStatic, ECC_WorldDynamic, ECC_Pawn, ECC_PhysicsBody,
ECC_Vehicle, ECC_Destructible               // object channels (what an object IS)
ECC_Visibility, ECC_Camera                  // trace channels (used for queries)
// Custom: ECC_GameTraceChannel1..ECC_GameTraceChannel18
```

**Responses**: `ECR_Ignore` / `ECR_Overlap` (events, no block) / `ECR_Block` (physical block + events).

**Built-in profiles**: `BlockAll`, `BlockAllDynamic`, `OverlapAll`, `OverlapAllDynamic`, `Pawn`, `PhysicsActor`, `NoCollision`.

### Setting Collision in C++

```cpp
MyMesh->SetCollisionProfileName(TEXT("BlockAll"));        // preferred — sets all at once
MyMesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
// ECollisionEnabled: NoCollision | QueryOnly | PhysicsOnly | QueryAndPhysics
MyMesh->SetCollisionObjectType(ECC_PhysicsBody);
MyMesh->SetCollisionResponseToAllChannels(ECR_Block);
MyMesh->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
MyMesh->SetCollisionResponseToChannel(ECC_Camera, ECR_Ignore);
```

### Object Type Channels vs Trace Channels

**Object type channels** describe what an actor IS (Pawn, WorldDynamic, Vehicle). Every component has exactly one object type. **Trace channels** are used for queries — they define what a trace is LOOKING FOR (Visibility, Camera, Weapon). This distinction determines which query function to use: `ByObjectType` matches the target's object type channel; `ByChannel` uses the querier's trace channel and checks responses. Most gameplay traces use trace channels (`ECC_Visibility`, custom `Weapon`); overlap queries for "find all pawns" use object type (`ECC_Pawn`).

### Custom Channels — DefaultEngine.ini

```ini
[/Script/Engine.CollisionProfile]
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel1,DefaultResponse=ECR_Block,bTraceType=True,bStaticObject=False,Name="Weapon")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel2,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="Interactable")
+Profiles=(Name="Interactable",CollisionEnabled=QueryAndPhysics,ObjectTypeName="Interactable",CustomResponses=((Channel="Weapon",Response=ECR_Ignore),(Channel="Visibility",Response=ECR_Block)))
```

`bTraceType=True` = trace channel; `bTraceType=False` = object type channel. They use separate query functions.

See `references/collision-channel-setup.md` for full profile examples.

---

## Trace Queries

### FCollisionQueryParams

```cpp
FCollisionQueryParams Params;
Params.TraceTag                = TEXT("WeaponTrace"); // for profiling/debug
Params.bTraceComplex           = false;  // false=simple hull (fast); true=per-poly (expensive)
Params.bReturnPhysicalMaterial = true;   // populates Hit.PhysMaterial
Params.bReturnFaceIndex        = false;  // expensive, only when needed
Params.AddIgnoredActor(this);
Params.AddIgnoredComponent(MyComp);
```

### World-Level Trace Functions (C++) — from `WorldCollision.h` via `UWorld`

```cpp
FHitResult Hit;
// By trace channel
GetWorld()->LineTraceSingleByChannel(Hit, Start, End, ECC_Visibility, Params);
GetWorld()->LineTraceMultiByChannel(Hits, Start, End, ECC_Visibility, Params);
// By object type
FCollisionObjectQueryParams ObjParams(ECC_PhysicsBody);
ObjParams.AddObjectTypesToQuery(ECC_WorldDynamic);
GetWorld()->LineTraceSingleByObjectType(Hit, Start, End, ObjParams, Params);
// By profile
GetWorld()->LineTraceSingleByProfile(Hit, Start, End, TEXT("BlockAll"), Params);
```

### Sweep Queries — FCollisionShape (from `CollisionShape.h`)

```cpp
FCollisionShape Sphere  = FCollisionShape::MakeSphere(30.f);
FCollisionShape Box     = FCollisionShape::MakeBox(FVector(50.f, 50.f, 50.f));
FCollisionShape Capsule = FCollisionShape::MakeCapsule(34.f, 88.f); // radius, half-height

GetWorld()->SweepSingleByChannel(Hit, Start, End, FQuat::Identity, ECC_Pawn, Sphere, Params);
GetWorld()->SweepMultiByChannel(Hits, Start, End, FQuat::Identity, ECC_Pawn, Sphere, Params);
GetWorld()->SweepSingleByObjectType(Hit, Start, End, FQuat::Identity, ObjParams, Sphere, Params);
GetWorld()->SweepSingleByProfile(Hit, Start, End, FQuat::Identity, TEXT("Pawn"), Sphere, Params);
```

### Overlap Queries

```cpp
TArray<FOverlapResult> Overlaps;
GetWorld()->OverlapMultiByObjectType(Overlaps, Center, FQuat::Identity,
    FCollisionObjectQueryParams(ECC_Pawn), FCollisionShape::MakeSphere(500.f), Params);
for (const FOverlapResult& R : Overlaps) { AActor* A = R.GetActor(); }

// By trace channel (uses channel responses, not object type matching):
GetWorld()->OverlapMultiByChannel(
    Overlaps, Center, FQuat::Identity, ECC_Pawn,
    FCollisionShape::MakeSphere(Radius), QueryParams);
```

### FHitResult — Key Fields

```cpp
Hit.bBlockingHit;          // true if blocking
Hit.ImpactPoint;           // world space contact point
Hit.ImpactNormal;          // surface normal
Hit.Distance;              // from Start to impact
Hit.BoneName;              // skeletal mesh bone
Hit.GetActor();
Hit.GetComponent();
// Physical material (requires bReturnPhysicalMaterial=true):
if (UPhysicalMaterial* M = Hit.PhysMaterial.Get())
    EPhysicalSurface S = UPhysicalMaterial::DetermineSurfaceType(M);
```

### Blueprint-Layer Traces (UKismetSystemLibrary)

```cpp
#include "Kismet/KismetSystemLibrary.h"
TArray<AActor*> Ignore = { this };
// LineTrace with debug draw (ETraceTypeQuery maps to ECollisionChannel)
UKismetSystemLibrary::LineTraceSingle(this, Start, End,
    ETraceTypeQuery::TraceTypeQuery1, false, Ignore, EDrawDebugTrace::ForDuration, Hit, true);
// SphereTrace
UKismetSystemLibrary::SphereTraceSingle(this, Start, End, 50.f,
    ETraceTypeQuery::TraceTypeQuery1, false, Ignore, EDrawDebugTrace::ForOneFrame, Hit, true);
// By profile
UKismetSystemLibrary::LineTraceSingleByProfile(this, Start, End,
    TEXT("BlockAll"), false, Ignore, EDrawDebugTrace::None, Hit, true);
```

### Async Traces

```cpp
FTraceHandle Handle = GetWorld()->AsyncLineTraceByChannel(
    EAsyncTraceType::Single, Start, End, ECC_Visibility, Params);
// Read next frame:
FTraceDatum Datum;
if (GetWorld()->QueryTraceData(Handle, Datum) && Datum.OutHits.Num() > 0)
    FHitResult& Hit = Datum.OutHits[0];
```

### Debug Visualization

```cpp
#if ENABLE_DRAW_DEBUG
DrawDebugLine(GetWorld(), Start, End, FColor::Red, false, 2.f);
DrawDebugSphere(GetWorld(), HitResult.ImpactPoint, 10.f, 12, FColor::Green, false, 2.f);
#endif
```

`DrawDebugLine` / `DrawDebugSphere` are from `DrawDebugHelpers.h`. Wrap in `ENABLE_DRAW_DEBUG` so they compile out in shipping builds. The bool param is `bPersistentLines`; the float param is `LifeTime` in seconds.

See `references/trace-patterns.md` for full gameplay patterns (hitscan, melee sweep, AoE, ground detection, async sensors).

---

## Collision Events

Delegate declarations from `PrimitiveComponent.h`:
- `OnComponentHit` — `(HitComp, OtherActor, OtherComp, NormalImpulse, FHitResult)` — physics collision
- `OnComponentBeginOverlap` — `(OverlappedComp, OtherActor, OtherComp, OtherBodyIndex, bFromSweep, SweepResult)`
- `OnComponentEndOverlap` — `(OverlappedComp, OtherActor, OtherComp, OtherBodyIndex)`

```cpp
// Hit events (physics collision)
MyMesh->SetNotifyRigidBodyCollision(true);  // "Simulation Generates Hit Events"
MyMesh->OnComponentHit.AddDynamic(this, &AMyActor::OnHit);

UFUNCTION()
void AMyActor::OnHit(UPrimitiveComponent* HitComp, AActor* OtherActor,
                      UPrimitiveComponent* OtherComp, FVector NormalImpulse, const FHitResult& Hit) {}

// Overlap events — SetGenerateOverlapEvents(true) REQUIRED on BOTH components
MyMesh->SetGenerateOverlapEvents(true);
MyMesh->OnComponentBeginOverlap.AddDynamic(this, &AMyActor::OnBeginOverlap);
MyMesh->OnComponentEndOverlap.AddDynamic(this, &AMyActor::OnEndOverlap);

UFUNCTION()
void AMyActor::OnBeginOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
    UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult) {}

UFUNCTION()
void AMyActor::OnEndOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
    UPrimitiveComponent* OtherComp, int32 OtherBodyIndex) {}
```

**Requirements:** Hit: `QueryAndPhysics`, `ECR_Block` on both, `SetNotifyRigidBodyCollision(true)`. Overlap: `ECR_Overlap` on both, `SetGenerateOverlapEvents(true)` on both.

---

## Physics Bodies

```cpp
// Enable simulation (PrimitiveComponent.h / BodyInstanceCore.h)
MyMesh->SetSimulatePhysics(true);
MyMesh->SetEnableGravity(true);
MyMesh->SetMassOverrideInKg(NAME_None, 50.f, true); // 50 kg
MyMesh->SetLinearDamping(0.1f);
MyMesh->SetAngularDamping(0.05f);
float Mass = MyMesh->GetMass();

// Forces and impulses
MyMesh->AddImpulse(FVector(0,0,1000), NAME_None, false);       // bVelChange=true ignores mass
MyMesh->AddImpulseAtLocation(FVector(500,0,0), HitPoint);      // adds torque
MyMesh->AddForce(FVector(0,0,9800), NAME_None, false);          // continuous (per tick)
MyMesh->AddRadialImpulse(Center, 500.f, 2000.f, RIF_Linear, false);
MyMesh->SetPhysicsLinearVelocity(FVector(0,0,300));             // use sparingly
```

**FBodyInstanceCore key flags** (set via UPROPERTY/editor): `bSimulatePhysics`, `bOverrideMass`, `bEnableGravity`, `bAutoWeld`, `bStartAwake`, `bGenerateWakeEvents`, `bUpdateKinematicFromSimulation`.

**Collision complexity** (`BodySetupEnums.h`): `CTF_UseDefault`, `CTF_UseSimpleAndComplex`, `CTF_UseSimpleAsComplex`, `CTF_UseComplexAsSimple` (expensive, static only for physics).

### Physics Constraints

```cpp
UPhysicsConstraintComponent* C = NewObject<UPhysicsConstraintComponent>(this);
C->SetupAttachment(RootComponent);
C->SetConstrainedComponents(MeshA, NAME_None, MeshB, NAME_None);
C->SetAngularSwing1Limit(EAngularConstraintMotion::ACM_Limited, 45.f);
C->SetAngularTwistLimit(EAngularConstraintMotion::ACM_Free, 0.f);
C->SetLinearXLimit(ELinearConstraintMotion::LCM_Locked, 0.f);
C->RegisterComponent();
```

**Named constraint presets** (set via `ConstraintProfile` or editor Preset dropdown):

| Preset | Angular Limits | Linear Limits |
|---|---|---|
| Fixed | All locked | All locked |
| Hinge | One axis free | All locked |
| Prismatic | All locked | One axis free |
| Ball-and-Socket | All free | All locked |

---

## Physical Materials (UPhysicalMaterial)

From `PhysicalMaterials/PhysicalMaterial.h`:

```cpp
float Friction;       // kinetic (0 = frictionless)
float StaticFriction; // before sliding starts
float Restitution;    // 0 (no bounce) to 1 (elastic)
float Density;        // g/cm^3 — used to compute mass from shape volume
EPhysicalSurface SurfaceType; // SurfaceType_Default, SurfaceType1..SurfaceType62
// FrictionCombineMode / RestitutionCombineMode: Average, Min, Multiply, Max

// Runtime override
MyMesh->SetPhysMaterialOverride(MyPhysMaterial);

// Detect surface from trace (requires bReturnPhysicalMaterial=true)
if (UPhysicalMaterial* M = Hit.PhysMaterial.Get())
{
    EPhysicalSurface S = UPhysicalMaterial::DetermineSurfaceType(M);
    switch (S) { case SurfaceType1: /* Metal */ break; }
}
```

---

## Chaos Physics (UE5)

UE5 uses **Chaos** by default (PhysX removed). Key architecture:
- `FChaosScene` (`ChaosScene.h`) owns the solver: `StartFrame()`, `SetUpForFrame()`, `EndFrame()`.
- Physics runs on a dedicated thread; game thread reads results at sync points.
- **Substepping**: enabled per Project Settings > Physics (`MaxSubsteps`, `MaxSubstepDeltaTime`). Enable when small/fast objects tunnel through thin geometry — substepping divides the physics tick into smaller increments so collisions are not missed.
- **Async physics**: runs simulation on a separate thread with one-frame latency. Enable via `UPhysicsSettings::bTickPhysicsAsync`. Use `UAsyncPhysicsInputComponent` on components that need physics-thread input callbacks.

Key `UPhysicsSettingsCore` fields (`PhysicsSettingsCore.h`):
```cpp
float DefaultGravityZ;         // -980 cm/s^2 default
float BounceThresholdVelocity; // min velocity to bounce
float MaxAngularVelocity;      // rad/s cap
float MaxDepenetrationVelocity;
float ContactOffsetMultiplier; // contact shell size
FChaosSolverConfiguration SolverOptions;
```

**EPhysicalSurface**: 62 configurable slots (`SurfaceType1..SurfaceType62`) mapped in Project Settings > Physics > Physical Surface.

**Geometry Collections (Chaos Destructibles)**: use `UGeometryCollectionComponent`. Fracture thresholds driven by `FPhysicalMaterialStrength` (TensileStrength, CompressionStrength, ShearStrength) and `FPhysicalMaterialDamageModifier` (DamageThresholdMultiplier) on `UPhysicalMaterial`.

---

### Cloth Simulation

```cpp
// Cloth uses UClothingAssetBase attached to USkeletalMeshComponent
// Enable in Mesh asset: Clothing → Add Clothing Data
// C++ access:
USkeletalMeshComponent* Mesh = GetMesh();
if (UClothingSimulationInteractor* Cloth = Mesh->GetClothingSimulationInteractor())
{
    Cloth->PhysicsAssetUpdated();             // re-sync after physics asset change
    Cloth->SetAnimDriveSpringStiffness(10.f); // blend anim ↔ cloth
}
```

### Field System

Field System actors apply forces, strain, and anchors to Chaos destruction and cloth:

```cpp
// Place AFieldSystemActor in level, add field nodes:
// URadialFalloff — distance-based falloff
// URadialVector — directional force from center
// UUniformVector — constant directional force
// UBoxFalloff — box-shaped field region

// Trigger destruction at runtime:
AFieldSystemActor* FieldActor = GetWorld()->SpawnActor<AFieldSystemActor>();
URadialFalloff* Falloff = NewObject<URadialFalloff>(FieldActor);
Falloff->SetRadialFalloff(1000000.f, 0.8f, 1.f, 0.f, 500.f, FVector::ZeroVector, EFieldFalloffType::Field_Falloff_Linear);
UFieldSystemMetaDataFilter* Meta = NewObject<UFieldSystemMetaDataFilter>(FieldActor);
Meta->SetMetaDataFilterType(EFieldFilterType::Field_Filter_All, EFieldObjectType::Field_Object_All, EFieldPositionType::Field_Position_CenterOfMass);
FieldActor->GetFieldSystemComponent()->ApplyPhysicsField(true, EFieldPhysicsType::Field_ExternalClusterStrain, Meta, Falloff);
```

---

## Common Mistakes & Anti-Patterns

**Wrong collision responses**: Overlap events require `ECR_Overlap` AND `bGenerateOverlapEvents=true` on BOTH components.

**Traces every Tick on many actors**: Use async traces or throttle to 5–10 Hz with a timer.

**QueryOnly vs PhysicsOnly confusion**: `QueryOnly` = traces only, no physics forces. `PhysicsOnly` = forces only, traces skip it. Use `QueryAndPhysics` for both.

**Complex collision in traces**: `bTraceComplex=true` is 4–10x more expensive. Default `false`; only enable for precise terrain interaction.

**Missing `SetNotifyRigidBodyCollision`**: `OnComponentHit` will never fire without it — this flag ("Simulation Generates Hit Events") is separate from collision response.

**Sweep vs overlap**: Sweep = shape moving along a path (movement, projectile). Overlap = shape at fixed point (AoE, proximity). Don't substitute one for the other.

**Physics on dedicated servers**: Disable skeletal ragdolls with `bSimulateSkeletalMeshOnDedicatedServer=false` unless server accuracy is required.

### Multiplayer & Replicated Actor Collision

In multiplayer, physics simulation runs on the server. Collision events (`OnComponentHit`, `OnBeginOverlap`) fire on the server only by default — clients do not receive these events unless you replicate them explicitly via RPCs. Clients see physics-simulated actor positions via `FRepMovement` (the replicated transform + velocity struct behind `bReplicateMovement`). Setting `bReplicateMovement = true` on an actor syncs its transform and linear/angular velocity; the underlying physics state itself is not replicated. For client-predicted physics (e.g., projectiles), simulate locally on the client and reconcile with server authority on correction. Cosmetic-only physics — ragdolls, debris, environmental props — can simulate on clients independently without server involvement, since visual fidelity matters more than authority.

---

## Required Module Dependencies

```csharp
// Build.cs
PublicDependencyModuleNames.AddRange(new string[] {
    "Core", "CoreUObject",
    "Engine",      // UPrimitiveComponent, FHitResult, UWorld trace API
    "PhysicsCore", // UPhysicalMaterial, FCollisionShape, FBodyInstanceCore
});
```

---

## Related Skills

- `ue-actor-component-architecture` — `UPrimitiveComponent` lifecycle, attachment, registration
- `ue-ai-navigation` — trace-based sensing and navmesh overlap queries
- `ue-gameplay-abilities` — targeting systems built on trace and overlap queries
- `ue-cpp-foundations` — delegate binding syntax and UFUNCTION requirements
