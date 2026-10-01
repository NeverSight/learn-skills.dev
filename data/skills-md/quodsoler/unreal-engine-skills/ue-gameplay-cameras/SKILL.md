---
name: ue-gameplay-cameras
description: "Use when building or fixing Unreal Engine cameras — spring-arm third-person rigs, first-person cameras, view-target blends, camera shakes, camera modifiers, cine cameras, or the Gameplay Camera System plugin. Also use when the user mentions 'APlayerCameraManager', 'USpringArmComponent', 'TargetArmLength', 'bUsePawnControlRotation', 'SetViewTargetWithBlend', 'UpdateViewTarget', 'CalcCamera', 'UCameraModifier', 'camera shake', 'UCameraShakeBase', 'FMinimalViewInfo', 'UGameplayCameraComponent', 'camera rig', 'camera director' or 'ShowDebug Camera'. For Sequencer shots, see ue-sequencer-cinematics; for the classes that own the camera, see ue-gameplay-framework; for input, see ue-input-system."
metadata:
  version: "2.0.0"
  engine: "5.8"
---

# UE Gameplay Cameras

Target engine: **UE 5.8**. APIs below are verified against the 5.8 headers; older forms are listed under "Deprecated — do not use".

Two camera stacks ship in 5.8. The classic stack lives in the `Engine` module (`Classes/Camera`, `Classes/GameFramework/SpringArmComponent.h`) with shake patterns in the `EngineCameras` plugin and film-style cameras in `CinematicCamera`; the data-driven Gameplay Camera System lives in the `GameplayCameras` plugin (Experimental in 5.8, but enabled by default). Build.cs needs `"Core"`, `"CoreUObject"`, `"Engine"`, plus `"CinematicCamera"` for cine cameras, `"EngineCameras"` for shake patterns, and `"GameplayCameras"` for the plugin.

## Context

Read `.agents/ue-project-context.md` if it exists (module names, conventions, enabled plugins, GAS/networking setup). Do not stop if it is missing.

Identify the area from the request and the codebase. Ask only when two plausible readings would produce different code.

| Request is about… | Go to |
|---|---|
| Choosing between the two stacks | [Classic Stack or Gameplay Camera System](#classic-stack-or-gameplay-camera-system) |
| Who computes the final view each frame | [How the Classic Pipeline Runs](#how-the-classic-pipeline-runs) |
| Third-person boom, camera lag, collision probe | [Third-Person Spring Arm Camera](#third-person-spring-arm-camera) |
| First-person camera, eye height, view rotation | [First-Person Camera](#first-person-camera) |
| Switching cameras, blending between actors | [View Targets and Blending](#view-targets-and-blending) |
| Pitch clamps, FOV, fades, custom camera logic | [Custom APlayerCameraManager](#custom-aplayercameramanager) |
| Persistent post-effects on the camera (lean, recoil, lock-on) | [Camera Modifiers](#camera-modifiers) |
| Explosions, hits, world-space rumble | [Camera Shakes](#camera-shakes) |
| Focal length, aperture, focus, rails and cranes | [Cinematic Cameras](#cinematic-cameras) |
| Camera assets, rigs, directors, blends, control rotation | [Gameplay Camera System](#gameplay-camera-system) |
| Writing a new camera node and evaluator | [Custom Camera Node in C++](#custom-camera-node-in-c) |
| Nothing renders, wrong camera, jitter | [Debugging Cameras](#debugging-cameras) |

Full classic API surface (post-process on cameras, `FMinimalViewInfo` fields, shake pattern catalogue, cine camera settings): [references/classic-camera-stack.md](references/classic-camera-stack.md). Node/director/service catalogue, camera variables, evaluation contexts and CVars: [references/gameplay-camera-system.md](references/gameplay-camera-system.md).

## Classic Stack or Gameplay Camera System

| Need | Classic stack | Gameplay Camera System |
|---|---|---|
| Ship-today stability | Yes — production API | Plugin is Experimental in 5.8 (`IsExperimentalVersion` in `GameplayCameras.uplugin`), API still moving |
| Enabled out of the box | Always (Engine module) | Yes — `"EnabledByDefault": true` |
| One camera per pawn, small number of modes | Best fit | Overkill |
| Many camera modes with authored blends and transitions | Hand-rolled state machine in `UpdateViewTarget` | Built in: camera rigs + transitions + blend stack |
| Designers author cameras without C++ | Blueprint subclasses only | Camera assets, rig graphs, State Tree directors |
| Per-mode post-process, framing, collision push | Write it yourself | Shipped camera nodes |
| Camera shakes | `UCameraShakeBase` + patterns | `UCameraShakeAsset` + shake camera nodes |

Mixing is supported: `AGameplayCamerasPlayerCameraManager` is an `APlayerCameraManager` subclass, so classic view targets, fades and modifiers still work while the plugin runs the evaluation.

## How the Classic Pipeline Runs

1. `APlayerController` holds `PlayerCameraManager` (spawned by `virtual void SpawnPlayerCameraManager()` from `TSubclassOf<APlayerCameraManager> PlayerCameraManagerClass`).
2. `APlayerCameraManager::UpdateCamera(float DeltaTime)` → `DoUpdateCamera(float DeltaTime)` → `UpdateViewTarget(FTViewTarget& OutVT, float DeltaTime)`.
3. `UpdateViewTarget` fills `OutVT.POV` (an `FMinimalViewInfo`). An `ACameraActor` target uses its camera component directly; any other target gets `Target->CalcCamera` (`PlayerCameraManager.cpp:354`), whose base `AActor` implementation uses the first active camera component when `bFindCameraComponentWhenViewTarget` is true, else the actor's eyes viewpoint (`Actor.cpp:3688-3706`).
4. `ApplyCameraModifiers(float DeltaTime, FMinimalViewInfo& InOutPOV)` runs every `UCameraModifier` in `ModifierList` by `Priority` (0 = highest).
5. The result is cached; `GetCameraLocation()`, `GetCameraRotation()` and `GetCameraCacheView()` read it, and `APlayerController::GetPlayerViewPoint(FVector& out_Location, FRotator& out_Rotation)` returns it.

`bAutoManageActiveCameraTarget` on `APlayerController` (default true) makes possession call `virtual void AutoManageActiveCameraTarget(AActor* SuggestedTarget)`, which is why a freshly possessed pawn becomes the view target with no code.

## Third-Person Spring Arm Camera

```cpp
// MyCharacter.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "MyCharacter.generated.h"

class UCameraComponent;
class USpringArmComponent;

UCLASS()
class MYGAME_API AMyCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AMyCharacter();

private:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
    TObjectPtr<USpringArmComponent> CameraBoom;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
    TObjectPtr<UCameraComponent> FollowCamera;
};

// MyCharacter.cpp - also include Camera/CameraComponent.h,
// GameFramework/SpringArmComponent.h and GameFramework/CharacterMovementComponent.h
#include "MyCharacter.h"

AMyCharacter::AMyCharacter()
{
    bUseControllerRotationPitch = false;
    bUseControllerRotationYaw   = false;
    bUseControllerRotationRoll  = false;

    GetCharacterMovement()->bOrientRotationToMovement = true;
    GetCharacterMovement()->RotationRate = FRotator(0.f, 500.f, 0.f);

    CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
    CameraBoom->SetupAttachment(RootComponent);
    CameraBoom->TargetArmLength = 400.f;
    CameraBoom->bUsePawnControlRotation = true;
    CameraBoom->bInheritPitch = true;
    CameraBoom->bInheritYaw = true;
    CameraBoom->bInheritRoll = false;
    CameraBoom->SocketOffset = FVector(0.f, 60.f, 0.f);
    CameraBoom->TargetOffset = FVector(0.f, 0.f, 50.f);
    CameraBoom->bDoCollisionTest = true;
    CameraBoom->ProbeChannel = ECC_Camera;
    CameraBoom->ProbeSize = 12.f;
    CameraBoom->bEnableCameraLag = true;
    CameraBoom->CameraLagSpeed = 10.f;
    CameraBoom->CameraLagMaxDistance = 100.f;

    FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
    FollowCamera->SetupAttachment(CameraBoom, USpringArmComponent::SocketName);
    FollowCamera->bUsePawnControlRotation = false;
    FollowCamera->FieldOfView = 90.f;
}
```

`SocketOffset` is applied in the boom's rotated space (side offsets follow the camera); `TargetOffset` is applied in world space (height offsets stay vertical). `bUsePawnControlRotation` belongs on exactly one of boom or camera — putting it on both double-applies the control rotation. Read the rotation the boom inherits (parent or control rotation) with `FRotator GetTargetRotation() const`, and test whether the collision probe pulled the arm in with `bool IsCollisionFixApplied() const`.

## First-Person Camera

Attach the `UCameraComponent` directly to the mesh or capsule, set `bUsePawnControlRotation = true` on the camera, and leave `bUseControllerRotationYaw = true` on the pawn so the body turns with the view.

```cpp
// MyFirstPersonCharacter.h - inside the class body
UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
TObjectPtr<UCameraComponent> FirstPersonCamera;

// MyFirstPersonCharacter.cpp - also include Camera/CameraComponent.h and Components/CapsuleComponent.h
AMyFirstPersonCharacter::AMyFirstPersonCharacter()
{
    bUseControllerRotationYaw = true;

    FirstPersonCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FirstPersonCamera"));
    FirstPersonCamera->SetupAttachment(GetCapsuleComponent());
    FirstPersonCamera->SetRelativeLocation(FVector(0.f, 0.f, BaseEyeHeight));
    FirstPersonCamera->bUsePawnControlRotation = true;
    FirstPersonCamera->bEnableFirstPersonFieldOfView = true;
    FirstPersonCamera->bEnableFirstPersonScale = true;
    FirstPersonCamera->FirstPersonFieldOfView = 70.f;
    FirstPersonCamera->FirstPersonScale = 0.6f;
}
```

`FirstPersonFieldOfView` and `FirstPersonScale` only affect primitives tagged as first person, and both need their `bEnable*` flag set. `APawn::BaseEyeHeight` feeds `virtual FVector GetPawnViewLocation() const`; override `virtual void RecalculateBaseEyeHeight()` for crouch. `virtual FRotator GetViewRotation() const` is the aim rotation used by the spring arm and by AI perception. To compute the view yourself, override `AActor::CalcCamera` and do not call `Super` — your override always runs for a non-`ACameraActor` view target; the camera-component lookup lives in the base implementation (`Actor.cpp:3690`). Set `bFindCameraComponentWhenViewTarget = false` only when you do call `Super` and want it to skip the component.

```cpp
// MyViewTargetActor.cpp - declare the override in the class body, include Camera/CameraTypes.h
void AMyViewTargetActor::CalcCamera(float DeltaTime, struct FMinimalViewInfo& OutResult)
{
    OutResult.Location = GetActorLocation() + FVector(0.f, 0.f, 150.f);
    OutResult.Rotation = GetActorRotation();
    OutResult.FOV = 75.f;
}
```

## View Targets and Blending

```cpp
// Inside a method of a MyGame class that has a PlayerController - include GameFramework/PlayerController.h
void AMyPlayerController::FocusOnActor(AActor* NewTarget)
{
    SetViewTargetWithBlend(NewTarget, 0.75f, VTBlend_EaseInOut, 2.f, false);
}
```

`virtual void SetViewTargetWithBlend(class AActor* NewViewTarget, float BlendTime = 0, enum EViewTargetBlendFunction BlendFunc = VTBlend_Linear, float BlendExp = 0, bool bLockOutgoing = false)` is the call to reach for. `EViewTargetBlendFunction` values: `VTBlend_Linear`, `VTBlend_Cubic`, `VTBlend_EaseIn`, `VTBlend_EaseOut`, `VTBlend_EaseInOut`, `VTBlend_PreBlended`. `BlendExp` only matters for the three ease functions. `bLockOutgoing` freezes the old target's POV for the rest of the blend — use it when you are about to teleport or destroy it.

The manager-level form is `virtual void SetViewTarget(class AActor* NewViewTarget, FViewTargetTransitionParams TransitionParams = FViewTargetTransitionParams())`, where `FViewTargetTransitionParams` carries `BlendTime`, `BlendFunction`, `BlendExp` and `bLockOutgoing`. During a blend the manager holds `ViewTarget` and `PendingViewTarget` (both `FTViewTarget`, each with `Target` and `POV`) and counts down `BlendTimeToGo`; `OnBlendComplete()` fires when the pending target is promoted.

`SetViewTarget` and `SetViewTargetWithBlend` act on the calling machine's camera manager only — they do not replicate. To change one client's view from the server, call the client RPC `UFUNCTION(Reliable, Client) void ClientSetViewTarget(class AActor* A, struct FViewTargetTransitionParams TransitionParams = FViewTargetTransitionParams())`.

## Custom APlayerCameraManager

```cpp
// MyCameraManager.h
#pragma once

#include "CoreMinimal.h"
#include "Camera/PlayerCameraManager.h"
#include "MyCameraManager.generated.h"

UCLASS()
class MYGAME_API AMyCameraManager : public APlayerCameraManager
{
    GENERATED_BODY()

public:
    AMyCameraManager(const FObjectInitializer& ObjectInitializer);

protected:
    virtual void UpdateViewTarget(FTViewTarget& OutVT, float DeltaTime) override;

    UPROPERTY(EditDefaultsOnly, Category = "Aim")
    float AimFieldOfView = 55.f;
    UPROPERTY(BlueprintReadWrite, Category = "Aim")
    bool bIsAiming = false;
};

// MyCameraManager.cpp
#include "MyCameraManager.h"

AMyCameraManager::AMyCameraManager(const FObjectInitializer& ObjectInitializer)
    : Super(ObjectInitializer)
{
    ViewPitchMin = -70.f;
    ViewPitchMax = 55.f;
    DefaultFOV = 90.f;
}

void AMyCameraManager::UpdateViewTarget(FTViewTarget& OutVT, float DeltaTime)
{
    Super::UpdateViewTarget(OutVT, DeltaTime);

    if (bIsAiming)
    {
        OutVT.POV.FOV = AimFieldOfView;
    }
}
```

Register it with `PlayerCameraManagerClass = AMyCameraManager::StaticClass();` in the `APlayerController` constructor. Other hooks worth knowing: `virtual void InitializeFor(class APlayerController* PC)`, `virtual void ProcessViewRotation(float DeltaTime, FRotator& OutViewRotation, FRotator& OutDeltaRot)`, and the clamp helpers `LimitViewPitch`, `LimitViewYaw`, `LimitViewRoll`.

Fades run off the manager: `virtual void StartCameraFade(float FromAlpha, float ToAlpha, float Duration, FLinearColor Color, bool bShouldFadeAudio = false, bool bHoldWhenFinished = false)`, `virtual void StopCameraFade()`, and `virtual void SetManualCameraFade(float InFadeAmount, FLinearColor Color, bool bInFadeAudio)` when you drive the alpha yourself. `APlayerController::ClientSetCameraFade` is the replicated wrapper.

## Camera Modifiers

A modifier is a stateful object that post-processes the computed POV every frame — lean, recoil, breathing, lock-on nudges.

```cpp
// MyCameraModifier.h
#pragma once

#include "CoreMinimal.h"
#include "Camera/CameraModifier.h"
#include "MyCameraModifier.generated.h"

UCLASS()
class MYGAME_API UMyCameraModifier : public UCameraModifier
{
    GENERATED_BODY()

public:
    UMyCameraModifier(const FObjectInitializer& ObjectInitializer);

    virtual bool ModifyCamera(float DeltaTime, struct FMinimalViewInfo& InOutPOV) override;

    UPROPERTY(EditDefaultsOnly, Category = "Lean")
    float LeanRollDegrees = 8.f;
};

// MyCameraModifier.cpp
#include "MyCameraModifier.h"
#include "Camera/CameraTypes.h"   // FMinimalViewInfo is only forward-declared by CameraModifier.h

UMyCameraModifier::UMyCameraModifier(const FObjectInitializer& ObjectInitializer)
    : Super(ObjectInitializer)
{
    Priority = 10;
    AlphaInTime = 0.2f;
    AlphaOutTime = 0.3f;
}

bool UMyCameraModifier::ModifyCamera(float DeltaTime, struct FMinimalViewInfo& InOutPOV)
{
    Super::ModifyCamera(DeltaTime, InOutPOV);

    InOutPOV.Rotation.Roll += LeanRollDegrees * Alpha;
    return false;
}
```

Return `true` only to stop lower-priority modifiers from running. `Alpha` is driven by `virtual void UpdateAlpha(float DeltaTime)` from `AlphaInTime`/`AlphaOutTime`; `virtual float GetTargetAlpha()` decides the destination. Toggle with `virtual void EnableModifier()`, `virtual void DisableModifier(bool bImmediate = false)` and `virtual void ToggleModifier()`; `virtual bool IsDisabled() const` reports state.

Add modifiers declaratively through `TArray<TSubclassOf<UCameraModifier>> DefaultModifiers` on the manager, or at runtime with `virtual UCameraModifier* AddNewCameraModifier(TSubclassOf<UCameraModifier> ModifierClass)`, which instantiates, registers and returns it. `virtual UCameraModifier* FindCameraModifierByClass(TSubclassOf<UCameraModifier> ModifierClass)` retrieves one later; `virtual bool RemoveCameraModifier(UCameraModifier* ModifierToRemove)` drops it. `virtual bool ProcessViewRotation(class AActor* ViewTarget, float DeltaTime, FRotator& OutViewRotation, FRotator& OutDeltaRot)` lets a modifier alter the player's aim before the POV is built.

## Camera Shakes

`UCameraShakeBase` is a thin container; the motion lives in its `RootShakePattern` (a `UCameraShakePattern`). In C++ you subclass a pattern — usually `USimpleCameraShakePattern`, which already supplies `Duration`, `BlendInTime` and `BlendOutTime` — and override `virtual void UpdateShakePatternImpl(const FCameraShakePatternUpdateParams& Params, FCameraShakePatternUpdateResult& OutResult)`, writing into `OutResult.Location`, `OutResult.Rotation` and `OutResult.FOV`; advance the inherited `State` with `State.Update(Params.DeltaTime)` and scale by the weight it returns, or the shake never finishes. Full worked example: [references/classic-camera-stack.md](references/classic-camera-stack.md). The other pattern hooks, all on `UCameraShakePattern`, are `GetShakePatternInfoImpl(FCameraShakeInfo& OutInfo) const`, `StartShakePatternImpl(const FCameraShakePatternStartParams& Params)`, `ScrubShakePatternImpl(const FCameraShakePatternScrubParams& Params, FCameraShakePatternUpdateResult& OutResult)`, `IsFinishedImpl() const`, `StopShakePatternImpl(const FCameraShakePatternStopParams& Params)` and `TeardownShakePatternImpl()`.

Shipped patterns (module `"EngineCameras"`): `UPerlinNoiseCameraShakePattern`, `UWaveOscillatorCameraShakePattern`, `UCompositeCameraShakePattern`, plus `ULegacyCameraShakePattern` behind `ULegacyCameraShake`. `USequenceCameraShakePattern` drives a shake from a `UCameraAnimationSequence` and lives in the `TemplateSequence` plugin. `UDefaultCameraShakeBase` is a `UCameraShakeBase` whose root pattern defaults to Perlin noise — the usual Blueprint starting point. Playing a shake:

| Call | Where | Use for |
|---|---|---|
| `APlayerCameraManager::StartCameraShake(TSubclassOf<UCameraShakeBase> ShakeClass, float Scale=1.f, ECameraShakePlaySpace PlaySpace = ECameraShakePlaySpace::CameraLocal, FRotator UserPlaySpaceRot = FRotator::ZeroRotator)` | local | direct, local player only |
| `APlayerController::ClientStartCameraShake(TSubclassOf<class UCameraShakeBase> Shake, float Scale = 1.f, ECameraShakePlaySpace PlaySpace = ECameraShakePlaySpace::CameraLocal, FRotator UserPlaySpaceRot = FRotator::ZeroRotator)` | server → one client | server-driven feedback |
| `UGameplayStatics::PlayWorldCameraShake(const UObject* WorldContextObject, TSubclassOf<class UCameraShakeBase> Shake, FVector Epicenter, float InnerRadius, float OuterRadius, float Falloff = 1.f, bool bOrientShakeTowardsEpicenter = false)` | local, radial | explosions |
| `UCameraShakeSourceComponent::StartCameraShake(TSubclassOf<UCameraShakeBase> InCameraShake, float Scale=1.f, ECameraShakePlaySpace PlaySpace = ECameraShakePlaySpace::CameraLocal, FRotator UserPlaySpaceRot = FRotator::ZeroRotator)` | local, attenuated | a rumbling machine that keeps shaking |

Stop with `APlayerController::ClientStopCameraShake(TSubclassOf<class UCameraShakeBase> Shake, bool bImmediately = true)`, `APlayerCameraManager::StopAllCameraShakes(bool bImmediately = true)` or `StopAllCameraShakesFromSource(UCameraShakeSourceComponent* SourceComponent, bool bImmediately = true)`. `ECameraShakePlaySpace` is `CameraLocal`, `World` or `UserDefined`. `UCameraShakeSourceComponent` carries `Attenuation` (`ECameraShakeAttenuation`), `InnerAttenuationRadius`, `OuterAttenuationRadius`, `CameraShake` and `bAutoStart`; `ACameraShakeSourceActor` is the placeable wrapper.

Shakes are applied by `UCameraModifier_CameraShake`, which the manager creates by default; `virtual UCameraShakeBase* AddCameraShake(TSubclassOf<UCameraShakeBase> NewShake, const FAddCameraShakeParams& Params)` is the low-level entry when you need `FAddCameraShakeParams::DurationOverride` or a custom initializer.

## Cinematic Cameras

`UCineCameraComponent` extends `UCameraComponent` with physical-camera settings: `Filmback` (`FCameraFilmbackSettings`), `LensSettings` (`FCameraLensSettings`), `FocusSettings` (`FCameraFocusSettings`), `CurrentFocalLength`, `CurrentAperture`, `CurrentFocusDistance` and `CurrentHorizontalFOV`. Drive it through the setters (`SetFilmback`, `SetLensSettings`, `SetFocusSettings`, `void SetCurrentFocalLength(float InFocalLength)`, `void SetCurrentAperture(const float NewCurrentAperture)`) so derived values recompute. `ACineCameraActor` adds `LookatTrackingSettings` (`FCameraLookatTrackingSettings`). `ACameraRig_Rail` exposes `CurrentPositionOnRail` (0–1 along its spline) and `bLockOrientationToRail`; `ACameraRig_Crane` exposes `CranePitch`, `CraneYaw`, `CraneArmLength`, `bLockMountPitch` and `bLockMountYaw`. Attach a camera actor to either and animate the exposed floats. Sequencer ownership: camera cuts, spawnables, `ULevelSequencePlayer` and take recording belong to `ue-sequencer-cinematics`. This skill covers the camera objects themselves.

## Gameplay Camera System

The `GameplayCameras` plugin (Experimental in 5.8) is enabled by default. A `UCameraAsset` holds a `UCameraDirector` plus enter/exit transitions; the director picks which `UCameraRigAsset` runs each frame; a rig is a tree of `UCameraNode` objects rooted at `RootNode`; the running system blends rigs on a blend stack and outputs an `FMinimalViewInfo`. Put a `UGameplayCameraComponent` on the pawn and point it at a camera asset:

```cpp
// MyGameplayCameraCharacter.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "MyGameplayCameraCharacter.generated.h"

class UGameplayCameraComponent;

UCLASS()
class MYGAME_API AMyGameplayCameraCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AMyGameplayCameraCharacter();

    virtual void BeginPlay() override;

private:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
    TObjectPtr<UGameplayCameraComponent> GameplayCamera;
};

// MyGameplayCameraCharacter.cpp - also include GameFramework/GameplayCameraComponent.h
#include "MyGameplayCameraCharacter.h"

AMyGameplayCameraCharacter::AMyGameplayCameraCharacter()
{
    GameplayCamera = CreateDefaultSubobject<UGameplayCameraComponent>(TEXT("GameplayCamera"));
    GameplayCamera->SetupAttachment(RootComponent);
}

void AMyGameplayCameraCharacter::BeginPlay()
{
    Super::BeginPlay();

    if (APlayerController* PC = Cast<APlayerController>(GetController()))
    {
        if (PC->IsLocalController())
        {
            GameplayCamera->ActivateCameraForPlayerController(PC, true);
        }
    }
}
```

Set the asset on `FCameraAssetReference CameraReference` (the property that replaced the old direct `UCameraAsset` pointer). The activation API lives on `UGameplayCameraComponentBase`: `void ActivateCameraForPlayerIndex(int32 PlayerIndex, bool bSetAsViewTarget = true)`, `void ActivateCameraForPlayerController(APlayerController* PlayerController, bool bSetAsViewTarget = true)`, and `Deactivate()` inherited from `UActorComponent`. Useful state: `bRunStandaloneCameraSystem`, `bSetControlRotationWhenViewTarget`, `DefaultPlayer`, `FRotator GetEvaluatedCameraRotation() const` and `UCineCameraComponent* GetOutputCameraComponent() const` — the output is a cine camera, so lens and focus settings come for free.

| Class | Role |
|---|---|
| `UGameplayCameraComponent` / `AGameplayCameraActor` | runs a `UCameraAsset` in its own evaluation context |
| `UGameplayCameraRigComponent` / `AGameplayCameraRigActor` | runs a single `UCameraRigAsset` without authoring a camera asset |
| `UGameplayCameraSystemComponent` / `AGameplayCameraSystemActor` | hosts the camera system itself; `ActivateCameraSystemForPlayerController(APlayerController*)`, `DeactivateCameraSystem(AActor* NextViewTarget = nullptr)`, `bSetPlayerControllerRotation` |
| `AGameplayCamerasPlayerCameraManager` | `APlayerCameraManager` subclass that runs the system; `ActivateGameplayCamera`, plus Blueprint-only (not exported, link error from C++) `StealPlayerController` / `ReleasePlayerController` |
| `UGameplayControlRotationComponent` | keeps the player's control rotation in sync with the camera; `AxisActions`, `AutoActivateForPlayer`; its `ActivateControlRotationManagementFor*` functions are not exported — Blueprint only (`GameplayControlRotationComponent.h:40-53`) |

Camera directors that ship in 5.8: `USingleCameraDirector` (one `CameraRig`), `UBlueprintCameraDirector` (runs a `UBlueprintCameraDirectorEvaluator` subclass — implement `RunCameraDirector` and call `ActivateCameraRig`), `UStateTreeCameraDirector` (a `FStateTreeReference` built with `UCameraDirectorStateTreeSchema`), and `UPriorityQueueCameraDirector`.

Runtime rig control, without touching the director, is on the component and on the camera manager: `FCameraRigInstanceID ActivatePersistentBaseCameraRig(UCameraRigAsset* CameraRig)` (plus `Global` and `Visual` variants), `void DeactivateCameraRig(FCameraRigInstanceID InstanceID, bool bImmediately = false)`, `FCameraRigInstanceID StartGlobalCameraModifierRig(const UCameraRigAsset* CameraRig, int32 OrderKey = 0)` / `StartVisualCameraModifierRig` / `void StopCameraModifierRig(FCameraRigInstanceID InstanceID, bool bImmediately = false)`. Shakes use `FCameraShakeInstanceID StartCameraShakeAsset(const UCameraShakeAsset* CameraShake, float ShakeScale = 1.f, ECameraShakePlaySpace PlaySpace = ECameraShakePlaySpace::CameraLocal, FRotator UserPlaySpaceRotation = FRotator::ZeroRotator)` and `bool StopCameraShakeAsset(FCameraShakeInstanceID InInstanceID, bool bImmediately = false)`. Node, variable, transition and service catalogues: [references/gameplay-camera-system.md](references/gameplay-camera-system.md).

## Custom Camera Node in C++

A node is a `UCameraNode` (data, editable in the rig graph) paired with an `FCameraNodeEvaluator` (runtime, allocated in the evaluator storage). The node overrides `OnBuildEvaluator` and returns `Builder.BuildEvaluator<FMyEvaluator>()`. The evaluator must use `UE_DECLARE_CAMERA_NODE_EVALUATOR` in the class and `UE_DEFINE_CAMERA_NODE_EVALUATOR` in the .cpp — they register its RTTI type ID, without which evaluator casts (`CastThis`, `CastThisChecked`) and type lookups fail (`GetCameraNodeAs` is a plain `UObject` `Cast` of the node and does not depend on them). Expose tunables as camera parameters (`FVector3dCameraParameter` and friends) so designers can bind them to camera variables, read them through a `TCameraParameterReader<T>` initialised in `OnInitialize`, and write the result through the `FCameraPose` setters in `OnRun`. Keep `ECameraNodeEvaluatorFlags` minimal — evaluators start at `Default` (parameter updates, serialization and operations), so clear the ones you do not use with `SetNodeEvaluatorFlags`.

Worked shoulder-offset node and the full hook lists for both classes: [references/gameplay-camera-system.md](references/gameplay-camera-system.md#writing-a-camera-node).

## Debugging Cameras

| Symptom | Check |
|---|---|
| Wrong actor on screen | `ShowDebug Camera` — prints the camera manager state including the view target |
| Nothing visible after possession | `bAutoManageActiveCameraTarget`, or a `SetViewTarget` call that never ran |
| `CalcCamera` override ignored | target is an `ACameraActor`, a Blueprint `BlueprintUpdateCamera` returned true, or the override calls `Super::CalcCamera` (which picks the camera component) |
| Camera clipped into geometry | `bDoCollisionTest`, `ProbeChannel`, `ProbeSize` on the boom |
| Blend snapped instead of easing | `BlendTime` is 0, or `BlendFunc` is `VTBlend_PreBlended` |
| Pitch runs past vertical | `ViewPitchMin` / `ViewPitchMax` on the camera manager |
| Gameplay Cameras shows nothing | `GameplayCameras.Debug.Enable 1`, then `GameplayCameras.Debug.Categories nodetree` |

Gameplay Cameras CVars worth knowing: `GameplayCameras.Debug.Enable`, `GameplayCameras.Debug.Categories` (`nodetree`, `directortree`, `blendstacks`, `services`, `posestats`, `viewfinder`), `GameplayCameras.Debug.SystemID`, `GameplayCameras.Debug.Trace`, `GameplayCameras.Debug.NodeTree.Filter`, `GameplayCameras.Debug.BlendStacks.Filter`. Project settings live on `UGameplayCamerasSettings` (`bAutoBuildInPIE`, `DefaultViewRotationMode`). A dedicated server renders nothing, so shakes, fades and post-process work there is wasted — drive them from client RPCs, or guard with `if (GetNetMode() != NM_DedicatedServer)`.

## Deprecated — do not use

| Do not emit | Use in 5.8 | Source |
|---|---|---|
| `#include "Camera/CameraShake.h"` | `#include "Shakes/LegacyCameraShake.h"` | `UE_DEPRECATED_HEADER(5.5)` in `EngineCameras/Legacy/Camera/CameraShake.h:9` |
| `#include "Shakes/MatineeCameraShake.h"` / `UMatineeCameraShake` | `ULegacyCameraShake` | `UE_DEPRECATED_HEADER(5.5)` in `EngineCameras/Public/Shakes/MatineeCameraShake.h:9` |
| `UCameraAnim`, `UCameraAnimInst`, `PlayCameraAnim` | `UCameraAnimationSequence` + `UEngineCamerasSubsystem::PlayCameraAnimation` | no `UCameraAnim` class exists in the 5.8 headers |
| `FCameraRigParameterOverrides` and the `F*CameraRigParameterOverride` structs | `FInstancedPropertyBag` parameter overrides on `FCameraRigAssetReference` | `UE_DEPRECATED(5.7)` in `GameplayCameras/Public/Core/CameraRigAssetReference.h:26-43` |
| `UCameraRigProxyTable` | `FCameraRigProxyRedirectTable` | `UE_DEPRECATED(5.6)` in `GameplayCameras/Public/Core/CameraRigProxyRedirectTable.h:69` |
| `FBlueprintCameraDirectorEvaluationParams` / `ActivateParams` / `DeactivateParams` as carriers | parameters passed directly to `RunCameraDirector` / `ActivateCameraDirector` / `DeactivateCameraDirector` | `UE_DEPRECATED(5.6)` in `GameplayCameras/Public/Directors/BlueprintCameraDirector.h:18,32,42` |
| `UActivateCameraRigFunctions::ActivatePersistentBaseCameraRig(WorldContext, PC, Rig)` | the same-named method on the gameplay camera component or camera manager | `DeprecatedFunction` in `GameplayCameras/Public/GameFramework/ActivateCameraRigFunctions.h:32` |
| `UGameplayCameraComponent::DeactivateCamera(bImmediately)` | `Deactivate()` | `DeprecatedFunction` in `GameplayCameras/Public/GameFramework/GameplayCameraComponentBase.h:212` |
| `UGameplayCameraComponent::Camera` (raw `UCameraAsset` pointer) | `CameraReference` (`FCameraAssetReference`) | `Camera_DEPRECATED` in `GameplayCameras/Public/GameFramework/GameplayCameraComponent.h:71` |
| `USimpleBlendCameraNode::SetBlendTime` meaning "current" | `SetDefaultBlendTime` | `UE_DEPRECATED(5.7)` in `GameplayCameras/Public/Nodes/Blends/SimpleBlendCameraNode.h:29` |
| `UCineCameraComponent::FilmbackSettings` | `Filmback` | `FilmbackSettings_DEPRECATED` in `CinematicCamera/Public/CineCameraComponent.h:34` |
| Calling `APawn::CalcCamera` as if the pawn had its own version | the inherited `AActor::CalcCamera` virtual (a pawn subclass overrides it normally), or a camera component | `APawn` does not declare `CalcCamera` in 5.8 |

## Common Mistakes

**`bUsePawnControlRotation` on both boom and camera:** the control rotation is applied twice, so the camera counter-rotates during mouse look. Set it on the spring arm for third person, on the camera for first person, never both.

**Calling `Super::CalcCamera` in a custom override:** the base `AActor::CalcCamera` returns the first active camera component's view when `bFindCameraComponentWhenViewTarget` is true (`Actor.cpp:3690-3702`), overwriting your POV. Skip `Super`, or clear the flag.

**Overriding `UpdateViewTarget` without calling `Super::`:** the base fills `OutVT.POV` from the target's camera component or `CalcCamera`. Skip it and you get a zeroed POV at the world origin.

**Getting `ModifyCamera` wrong:** override `virtual bool ModifyCamera(float DeltaTime, struct FMinimalViewInfo& InOutPOV)`, not the `FVector`/`FRotator` overload that bridges to Blueprint, and return `false` — `true` means "I am the last modifier" and silently kills every lower-priority modifier, including the shake modifier.

**Calling `StartCameraShake` on the server:** the server has its own camera manager, so the shake plays where nobody sees it. Use the client RPC `ClientStartCameraShake` from the server, or `UGameplayStatics::PlayWorldCameraShake` on the machine that renders.

**Forgetting the Build.cs modules:** `UPerlinNoiseCameraShakePattern` and `ULegacyCameraShake` need `"EngineCameras"`, `UCineCameraComponent` needs `"CinematicCamera"`, and everything under `UE::Cameras` needs `"GameplayCameras"`. Missing modules produce link errors, not compile errors.

**Writing a camera node evaluator without the RTTI macros:** `UE_DECLARE_CAMERA_NODE_EVALUATOR` in the class body and `UE_DEFINE_CAMERA_NODE_EVALUATOR` at file scope are both required; without them the evaluator reports its base class's type ID, so evaluator casts and type lookups fail at runtime.

**Subclassing `UCameraShakeBase` and overriding nothing:** the base class has no motion of its own. Set a `RootShakePattern` (via `ChangeRootShakePattern<T>()` in the constructor, or in the asset) or subclass `UDefaultCameraShakeBase`.

**Treating the Gameplay Camera System as final API:** the plugin is Experimental in 5.8. Isolate it behind your own wrapper component if you need to survive engine upgrades.

## Related Skills

- `ue-gameplay-framework` — `APlayerController`, `APawn`, possession and the view-target owner
- `ue-actor-component-architecture` — component attachment, sockets, tick order, `CreateDefaultSubobject`
- `ue-input-system` — Enhanced Input actions and axes that feed control rotation and camera input nodes
- `ue-sequencer-cinematics` — Level Sequences, camera cuts, spawnable cameras, take recording
- `ue-character-movement` — `bOrientRotationToMovement`, `RotationRate`, crouch and eye-height changes
- `ue-ui-umg-slate` — viewport-space UI, reticles and letterboxing that sit on top of the camera
- `ue-state-trees` — State Trees, the schema behind `UStateTreeCameraDirector`
