---
name: ue-mover
description: "Use when writing or debugging movement built on the Mover plugin: custom movement modes, layered moves, movement modifiers, instant effects, mode transitions, input production, or rollback networking for a Mover pawn. Also use when the user mentions 'Mover plugin', 'MoverComponent', 'CharacterMoverComponent', 'UBaseMovementMode', 'FLayeredMoveBase', 'FMoverSyncState', 'FMoverInputCmdContext', 'FProposedMove', 'ProduceInput', 'QueueNextMode', 'QueueLayeredMove', 'MovementModifier', 'InstantMovementEffect', 'ChaosMover', 'NetworkPrediction backend', or 'MoverExamples'. For UCharacterMovementComponent, see ue-character-movement; for replication mechanics, see ue-networking-replication."
metadata:
  version: "2.0.0"
  engine: "5.8"
---

# UE Mover

Target engine: **UE 5.8**. APIs below are verified against the 5.8 headers; older forms are listed under "Deprecated — do not use".

Mover is Epic's modular movement system, shipped as the `Mover` plugin (Experimental in 5.8 — APIs and data formats are subject to change). Movement is composed from data-driven objects — `UBaseMovementMode`, `FLayeredMoveBase`, `FMovementModifierBase`, `FInstantMovementEffect`, `UBaseMovementModeTransition` — hosted by `UMoverComponent` and driven by an external *backend liaison* rather than by `TickComponent`. Build.cs module names: `"Mover"` (plus `"ChaosMover"` for physics-driven movement, `"NetworkPrediction"` for the rollback backend, `"MoverMassIntegration"` for Mass). Public headers live under `Plugins/Experimental/Mover/Source/Mover/Public`. Log category is `LogMover`; console commands are prefixed `Mover.` and `mover.`.

## Context

Read `.agents/ue-project-context.md` if it exists (module names, conventions, enabled plugins, GAS/networking setup). Do not stop if it is missing.

Identify the area from the request and the codebase. Ask only when two plausible readings would produce different code.

| Request is about… | Go to |
|---|---|
| Choosing between CMC and Mover | [CMC vs Mover](#cmc-vs-mover) |
| Enabling plugins, Build.cs, project settings | [Setup](#setup) |
| Component, mode map, shared settings, what owns what | [Architecture](#architecture) |
| Where a simulation tick goes, substeps, mixing | [Tick Flow](#tick-flow) |
| Walk/climb/glide/zipline — a new movement type | [Movement Modes](#movement-modes) |
| Dash, launch, knockback, homing, root motion | [Layered Moves](#layered-moves) |
| Crouch, stance, settings swaps | [Movement Modifiers](#movement-modifiers) |
| Teleport, one-shot impulse, forced mode change | [Instant Movement Effects](#instant-movement-effects) |
| Automatic mode switching rules | [Transitions](#transitions) |
| Translating Enhanced Input into a Mover input cmd | [Input Production](#input-production) |
| Custom per-frame data, position, velocity, persistence | [Input and Sync State](#input-and-sync-state) |
| Backends, rollback, resimulation, what must replicate | [Backends and Networking](#backends-and-networking) |
| Reading velocity/mode, binding delegates, gameplay tags | [Reading State and Events](#reading-state-and-events) |
| Motion matching, trajectory, AI pathfollowing, Mass | [Integration Points](#integration-points) |

Full templates live in [mover-recipes.md](references/mover-recipes.md); the default movement set catalogue, data-model detail, utility libraries and debugging live in [mover-reference.md](references/mover-reference.md).

## CMC vs Mover

Mover is not a drop-in `UCharacterMovementComponent` replacement, and `UMoverComponent` does not require `ACharacter` — a `USceneComponent` root is the only hard requirement. This table matches the one in `ue-character-movement`.

| Situation | Use |
|---|---|
| Shipping title, any engine-supported platform | CMC |
| Existing `ACharacter` hierarchy, animation and AI already wired to CMC | CMC |
| Networked gameplay that must be stable today | CMC |
| Non-capsule, non-humanoid movers (vehicles, drones) that still want rollback networking | Mover |
| Movement composed from data-driven modes/modifiers instead of a `Phys*` subclass | Mover |
| Movement simulated on the physics thread with Chaos | Mover (`ChaosMover`) |
| Prototype that can absorb Experimental API churn | Mover |

Concept mapping: CMC movement modes → `UBaseMovementMode` objects; root motion sources → `FLayeredMoveBase`; `LaunchCharacter`/`TeleportTo` → `FInstantMovementEffect`; crouching → `FMovementModifierBase`; mode-change conditions scattered in `Phys*` → `UBaseMovementModeTransition`.

**Do not put both components on one pawn.** Unlike CMC, Mover state is not externally writable: there is no `Velocity` property to assign. Change motion only through modes, layered moves, modifiers and instant effects.

## Setup

Enable `Mover` (Experimental in 5.8). It pulls in `NetworkPrediction` (Beta in 5.8), `MotionWarping`, `PoseSearch`, `Water` and `ChaosVD`. Optional companions: `MoverExamples` (Experimental — sample maps and pawns), `ChaosMover` (Experimental — physics backend), `MoverAnimNext` (Experimental — UAF bridge), `MoverIntegrations` (Experimental — Mass).

```cs
// MyGame.Build.cs
PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "Mover", "GameplayTags" });
// Add "EnhancedInput" when the pawn binds input actions (the pawn recipe includes EnhancedInputComponent.h).
// Add "ChaosMover" only for physics-driven Mover actors.
// Add "MoverMassIntegration" only when driving Mover pawns from Mass.
```

Project Settings → Plugins → Network Prediction (`UNetworkPredictionSettingsObject`, `config=NetworkPrediction`), recommended starting point from the plugin README:

| Setting | Value | Why |
|---|---|---|
| `PreferredTickingPolicy` | `ENetworkPredictionTickingPolicy::Fixed` | Shared timeline, group rollback |
| `SimulatedProxyNetworkLOD` | `ENetworkLOD::Interpolated` | Other players' pawns forward-predict badly |
| `bEnableFixedTickSmoothing` | `true` | Fixed sim rate vs variable render rate |

With smoothing on, set the component's `SmoothingMode` to `EMoverSmoothingMode::VisualComponentOffset` (the default). Single-player: use `ENetworkPredictionTickingPolicy::Independent`, or drop Network Prediction entirely by setting `BackendClass` to `UMoverStandaloneLiaisonComponent`.

## Architecture

```
AActor (any APawn or AActor with a USceneComponent root)
 └─ UMoverComponent (UActorComponent, IMovementInterface)
     ├─ BackendClass            -> a UActorComponent implementing IMoverBackendLiaisonInterface
     ├─ MovementModes           : TMap<FName, TObjectPtr<UBaseMovementMode>>   (Instanced)
     ├─ StartingMovementMode    : FName
     ├─ Transitions             : TArray<TObjectPtr<UBaseMovementModeTransition>>  (global)
     ├─ PersistentSyncStateDataTypes : TArray<FMoverDataPersistence>
     ├─ InputProducer / InputProducers : objects implementing IMoverInputProducerInterface
     ├─ MovementMixer           : UMovementMixer
     └─ SharedSettings          : auto-built from each mode's SharedSettingsClasses
```

`UCharacterMoverComponent` subclasses `UMoverComponent` and adds character verbs: `Jump()`, `CanActorJump()`, `Crouch()`, `UnCrouch()`, `CanCrouch()`, `GetCrouchIntent()`, `IsCrouching()`, `IsFlying()`, `IsFalling()`, `IsAirborne()`, `IsOnGround()`, `IsSwimming()`, `IsSlopeSliding()`, and the `OnStanceChanged` delegate. Use it for humanoid pawns.

Modes never own gameplay state. A mode is a shared, `Instanced` `UObject` whose tuning lives in `UPROPERTY` fields and in shared settings objects (`IMovementSettingsInterface`, e.g. `UCommonLegacyMovementSettings`); everything that changes per frame belongs in `FMoverSyncState`.

```cpp
// Inside UMyClimbingMode::OnRegistered, after calling Super. Full class in mover-recipes.md.
const UCommonLegacyMovementSettings* Settings = GetMoverComponent()->FindSharedSettings<UCommonLegacyMovementSettings>();
```

## Tick Flow

The backend liaison drives three phases (`EMoverTickPhase::ProduceInput`, `SimulateMovement`, `ApplyState`):

1. **ProduceInput** — `UMoverComponent::ProduceInput(const int32 DeltaTimeMS, FMoverInputCmdContext* Cmd)` calls `IMoverInputProducerInterface::ProduceInput` on every entry of `InputProducers`, which `BeginPlay` fills with `InputProducer` (defaulting to the owner when it implements the interface) plus every owner component implementing it — the 5.8 `.cpp` never reads `bGatherInputFromAllInputProducerComponents`. Runs only on the controlling instance; it is *not* re-run during resimulation.
2. **SimulateMovement** — `OnPreSimulate(TimeStep, StartingData)` fires `OnPreSimulationTick`, then the simulation runs the substep loop:
   - queued instant effects apply;
   - each active `FLayeredMoveBase::GenerateMove` produces an `FProposedMove`;
   - unless a layered move fully overrides movement (`mover.perf.SkipGenerateMoveIfOverridden`), the active mode's `GenerateMove` runs;
   - `UMovementMixer::MixProposedMoves` combines them by `EMoveMixMode`;
   - `ProcessGeneratedMovement` (bind via `BindProcessGeneratedMovement`) gets the last word;
   - mode-owned `Transitions` then global `Transitions` are evaluated; the first hit calls `Trigger` and sets `FMovementModeTickEndState::NextModeName`, otherwise `UBaseMovementMode::SimulationTick` executes the move;
   - `FMovementModeTickEndState::RemainingMs` refunds time, producing another substep in the same frame.
   Then `OnPostSimulate(TimeStep, StartingData, EndingData)` fires `OnPostMovement` and `OnPostSimulationTick`.
3. **ApplyState** — the liaison calls `FinalizeFrame(SyncState, AuxState)` (or `FinalizeUnchangedFrame()`), which moves the actor and fires `OnPostFinalize`.

## Movement Modes

`UBaseMovementMode` is `UCLASS(MinimalAPI, Abstract, Blueprintable, BlueprintType, EditInlineNew, DefaultToInstanced)`. Override these, verbatim:

```cpp
virtual void OnRegistered(const FName ModeName, const FMoverSimContext& SimContext) override;
virtual void OnUnregistered(const FMoverSimContext& SimContext) override;
virtual void Activate(const FMoverEventContext& Context, FName PrevModeName, const FMoverSimContext& SimContext, const FMoverTickStartData& StartState, FMoverSyncState* OutSyncState, FMoverAuxStateContext* OutAuxState) override;
virtual void Deactivate(const FMoverEventContext& Context, FName NextModeName, const FMoverSimContext& SimContext) override;
virtual void GenerateMove_Implementation(const FMoverSimContext& SimContext, const FMoverTickStartData& StartState, const FMoverTimeStep& TimeStep, FProposedMove& OutProposedMove) const override;
virtual void SimulationTick_Implementation(const FSimulationTickParams& Params, FMoverTickEndData& OutputState) override;
```

`GenerateMove` is `const` and decides *what* motion is wanted; `SimulationTick` performs it (sweeps, floor checks) and writes the ending `FMoverDefaultSyncState`. Call `Super::` on `OnRegistered`, `OnUnregistered`, `Activate` and `Deactivate` — the base implementations manage owned transitions and fire the Blueprint events. Set `bSupportsAsync = true` only when `GenerateMove`/`SimulationTick` touch no scene components or other game-thread state.

Default set: `UWalkingMode`, `UFallingMode`, `UFlyingMode`, `USwimmingMode`, `UNavWalkingMode`, plus the async variants `UAsyncWalkingMode`, `UAsyncFallingMode`, `UAsyncFlyingMode`, `UAsyncNavWalkingMode` and the simplified `USimpleWalkingMode`, `USimpleFlyingMode`, `USimpleSpringWalkingMode`, `USmoothWalkingMode`. Default mode names are `DefaultModeNames::Walking`, `::Falling`, `::Flying`, `::Swimming`. Full catalogue in [mover-reference.md](references/mover-reference.md).

Register and switch at runtime:

```cpp
static void MyEnableClimbing(UMoverComponent& MoverComp)
{
    MoverComp.AddMovementModeFromClass(TEXT("Climbing"), UMyClimbingMode::StaticClass());
    MoverComp.QueueNextMode(TEXT("Climbing"), /*bShouldReenter=*/false);   // takes effect next sim frame
}

static void MyDisableClimbing(UMoverComponent& MoverComp)
{
    MoverComp.RemoveMovementMode(TEXT("Climbing"));
}
```

## Layered Moves

`FLayeredMoveBase` is temporary additive or overriding motion: it only proposes, the active mode executes. Shared fields: `MixMode` (`EMoveMixMode`), `Priority`, `DurationMs` (>0 timed, 0 single tick, <0 manual), `StartSimTimeMs`, `FinishVelocitySettings` (`FLayeredMoveFinishVelocitySettings`). Overrides, verbatim:

```cpp
virtual bool GenerateMove(const FMoverTickStartData& StartState, const FMoverTimeStep& TimeStep, const UMoverComponent* MoverComp, UMoverBlackboard* SimBlackboard, FProposedMove& OutProposedMove) override;
virtual bool IsFinished(double CurrentSimTimeMs) const override;
virtual FLayeredMoveBase* Clone() const override;
virtual void NetSerialize(FArchive& Ar) override;
virtual UScriptStruct* GetScriptStruct() const override;
virtual FString ToSimpleString() const override;
virtual void AddReferencedObjects(class FReferenceCollector& Collector) override;
```

`NetSerialize` must call `Super::NetSerialize(Ar)` first, then serialize your own fields — anything omitted will not survive a correction. Queueing stores your `TSharedPtr` as-is until a later simulation frame flushes it (it is cloned only when the sync state is copied), so fill it in completely first:

```cpp
static void MyQueueDash(UMoverComponent& MoverComp, const FVector& DashDirection)
{
    TSharedPtr<FLayeredMove_LinearVelocity> Dash = MakeShared<FLayeredMove_LinearVelocity>();
    Dash->Velocity = DashDirection.GetSafeNormal() * 2000.f;
    Dash->DurationMs = 200.f;
    Dash->MixMode = EMoveMixMode::OverrideVelocity;
    MoverComp.QueueLayeredMove(Dash);
}
```

Shipped moves: `FLayeredMove_LinearVelocity`, `FLayeredMove_JumpImpulseOverDuration`, `FLayeredMove_JumpTo`, `FLayeredMove_MoveTo`, `FLayeredMove_MoveToDynamic`, `FLayeredMove_RadialImpulse`, `FLayeredMove_MultiJump`, `FLayeredMove_Launch`, `FLayeredMove_AnimRootMotion`, `FLayeredMove_AnimRootMotion_SimDriven`.

A second, instanced form is in progress: stateless logic in `ULayeredMoveLogic` plus replicated data in `FLayeredMoveInstancedData`, activated with `FLayeredMoveActivationParams`. Register the logic class with `RegisterMove<T>()` / `K2_RegisterMove`, then `QueueLayeredMoveActivation(UMyMoveLogic::StaticClass())` or `QueueLayeredMoveActivationWithContext(Params)`. Prefer `FLayeredMoveBase` for new C++ work until the instanced path lands; both live side by side in `FMoverSyncState`.

## Movement Modifiers

`FMovementModifierBase` changes how the simulation behaves without proposing motion — stances, settings swaps, mode remaps. Overrides:

```cpp
virtual void OnStart(UMoverComponent* MoverComp, const FMoverTimeStep& TimeStep, const FMoverSyncState& SyncState, const FMoverAuxStateContext& AuxState) override;
virtual void OnEnd(UMoverComponent* MoverComp, const FMoverTimeStep& TimeStep, const FMoverSyncState& SyncState, const FMoverAuxStateContext& AuxState) override;
virtual void OnPreMovement(UMoverComponent* MoverComp, const FMoverTimeStep& TimeStep) override;
virtual void OnPostMovement(UMoverComponent* MoverComp, const FMoverTimeStep& TimeStep, const FMoverSyncState& SyncState, const FMoverAuxStateContext& AuxState) override;
virtual FMovementModifierBase* Clone() const override;
virtual void NetSerialize(FArchive& Ar) override;
virtual UScriptStruct* GetScriptStruct() const override;
virtual bool Matches(const FMovementModifierBase* Other) const override;
```

```cpp
static FMovementModifierHandle MyQueueStance(UMoverComponent& MoverComp)
{
    return MoverComp.QueueMovementModifier(MakeShared<FStanceModifier>());
}

static void MyCancelStance(UMoverComponent& MoverComp, const FMovementModifierHandle& Handle)
{
    if (MoverComp.IsModifierActiveOrQueued(Handle))
    {
        MoverComp.CancelModifierFromHandle(Handle);
    }
}
```

Mover assumes **one modifier of a given type at a time**; the default `Matches` compares type only. To allow several, override `Matches` using fields that `NetSerialize` also writes. `FStanceModifier` (with `EStanceMode` and `UStanceSettings`) is the shipped crouch implementation, driven by `UCharacterMoverComponent::Crouch()`.

## Instant Movement Effects

`FInstantMovementEffect` applies once, consuming no time, at the start or end of a substep. Override `virtual bool ApplyMovementEffect(FApplyMovementEffectParams& ApplyEffectParams, FMoverSyncState& OutputState) override;` and return true when you changed anything. Shipped: `FTeleportEffect`, `FAsyncTeleportEffect`, `FJumpImpulseEffect`, `FApplyVelocityEffect`.

```cpp
static void MyQueueTeleport(UMoverComponent& MoverComp, const FVector& Destination)
{
    TSharedPtr<FTeleportEffect> Teleport = MakeShared<FTeleportEffect>();
    Teleport->TargetLocation = Destination;
    MoverComp.QueueInstantMovementEffect(Teleport);
}
```

`ScheduleInstantMovementEffect` / `ScheduleLayeredMove` delay execution so every endpoint runs them on the same frame; they matter only for ChaosMover's networked physics path. Default to the `Queue*` forms.

## Transitions

`UBaseMovementModeTransition` decides mode changes from state. Override `virtual FTransitionEvalResult Evaluate_Implementation(const FSimulationTickParams& Params) const override;` (return `FTransitionEvalResult(NextModeName)` or `FTransitionEvalResult::NoTransition`) and `virtual void Trigger_Implementation(const FSimulationTickParams& Params) override;` for side effects. Put it in a mode's `Transitions` array for mode-scoped checks or the component's for global ones; `bAllowModeReentry` and `bFirstSubStepOnly` control re-entry and substep scope. Transitions are optional — `QueueNextMode`, `FProposedMove::PreferredMode` and `FMovementModeTickEndState::NextModeName` also change modes.

## Input Production

Mover does not read Enhanced Input. Cache input on the game thread, then translate it inside `ProduceInput`:

```cpp
// AMyMoverPawn : public APawn, public IMoverInputProducerInterface.
// CachedMoveInputIntent, bJumpHeld and bJumpPressedThisFrame are members filled by Enhanced Input handlers.
void AMyMoverPawn::ProduceInput_Implementation(int32 SimTimeMs, FMoverInputCmdContext& InputCmdResult)
{
    FCharacterDefaultInputs& CharacterInputs = InputCmdResult.InputCollection.FindOrAddMutableDataByType<FCharacterDefaultInputs>();
    CharacterInputs.ControlRotation = GetControlRotation();
    CharacterInputs.SetMoveInput(EMoveInputType::DirectionalIntent, CharacterInputs.ControlRotation.RotateVector(CachedMoveInputIntent));
    CharacterInputs.OrientationIntent = CharacterInputs.GetMoveInput().GetSafeNormal();
    CharacterInputs.bIsJumpPressed = bJumpHeld;
    CharacterInputs.bIsJumpJustPressed = bJumpPressedThisFrame;
    bJumpPressedThisFrame = false;
}
```

With fixed ticking, several render frames can feed one input cmd (or one frame can feed several ticks), so accumulate rather than sample. `FCharacterDefaultInputs` also carries `SuggestedMovementMode`, `MovementBase`/`MovementBaseBoneName`/`bUsingMovementBase`. `FMoverAIInputs` carries `RVOVelocityDelta` for AI. Full pawn in [mover-recipes.md](references/mover-recipes.md).

## Input and Sync State

Both the input cmd and the sync state are dynamic collections (`FMoverDataCollection`) of `FMoverDataStructBase`-derived structs, so custom data needs no component subclass.

| Type | Holds |
|---|---|
| `FMoverInputCmdContext` | `InputCollection` — authored by the owner each frame |
| `FMoverSyncState` | `MovementMode`, `LayeredMoves`, `LayeredMoveInstances`, `MovementModifiers`, `SyncStateCollection` |
| `FMoverAuxStateContext` | `AuxStateCollection` — rarely changing simulation input |
| `FMoverDefaultSyncState` | location, orientation, velocity, `AngularVelocityDegrees`, `MoveDirectionIntent`, movement base |
| `FMoverTickStartData` | `InputCmd`, `SyncState`, `AuxState` for the tick |
| `FMoverTickEndData` | `SyncState`, `AuxState`, `MovementEndState`, `MoveRecord` |
| `FProposedMove` | `PreferredMode`, `DirectionIntent`, `LinearVelocity`, `AngularVelocityDegrees`, `bHasDirIntent`, `MixMode` |
| `FMoverTimeStep` | `ServerFrame`, `BaseSimTimeMs`, `StepMs`, `bIsResimulating`, `bIsFirstResimFrame` |

`FMoverDefaultSyncState` is required on every Mover actor. Read through the world/base-space accessors — `GetLocation_WorldSpace()`, `GetVelocity_WorldSpace()`, `GetOrientation_WorldSpace()`, `GetAngularVelocityDegrees_WorldSpace()`, `GetTransform_WorldSpace()` — and write with `SetTransforms_WorldSpace(Location, Orient, Velocity, AngularVelocityDegrees, Base, BaseBone)`.

```cpp
void UMyClimbingMode::SimulationTick_Implementation(const FSimulationTickParams& Params, FMoverTickEndData& OutputState)
{
    const FMoverDefaultSyncState* StartingSyncState = Params.StartState.SyncState.SyncStateCollection.FindDataByType<FMoverDefaultSyncState>();
    check(StartingSyncState);

    FMyClimbState& OutClimb = OutputState.SyncState.SyncStateCollection.FindOrAddMutableDataByType<FMyClimbState>();
    OutClimb.SurfaceNormal = StartingSyncState->GetOrientation_WorldSpace().Vector();
}
```

Custom state structs must override `Clone`, `NetSerialize`, `GetScriptStruct`, `ToString`, `ShouldReconcile` and `Interpolate`. Anything that must survive a frame without being rewritten goes in `PersistentSyncStateDataTypes` as an `FMoverDataPersistence`.

`UMoverBlackboard` (`GetSimBlackboard()` / `GetSimBlackboard_Mutable()`) caches derived values *outside* the networked state — `CommonBlackboard::LastFloorResult`, `LastWaterResult`, `LastFoundDynamicMovementBase`, `TimeSinceSupported`. It is being replaced by the rollback-aware blackboard (`GetRollbackBlackboardExternal()`), so always treat a lookup as possibly missing and provide a fallback. `TryGet<T>` and `Set<T>` are type-strict: store and read the same type (a value written as `double` must be read as `double`).

## Backends and Networking

`IMoverBackendLiaisonInterface` (`Backends/MoverBackendLiaison.h`) is the contract: `GetCurrentSimTimeMs()`, `GetCurrentSimFrame()`, `IsAsync()`, `IsFixedDt()`, `ShouldResim()`, the pending/presentation sync-state accessors, and `OnSimulationRollback(NewSyncState, NewBaseTimeStep, PreRollbackTimeStep)`. Set the implementing component class on `UMoverComponent::BackendClass`.

| Backend | Use for | Notes |
|---|---|---|
| `UMoverNetworkPredictionLiaisonComponent` | networked or standalone play | Network Prediction (Beta in 5.8); fixed or independent ticking, rollback + resim |
| `UMoverStandaloneLiaisonComponent` | standalone, no physics-driven movement | no Network Prediction overhead |
| `UChaosMoverBackendComponent` | physics-driven pawns | ChaosMover (Experimental in 5.8); async, fixed dt, Chaos Networked Physics |

Network model: every endpoint simulates a shared timeline, clients running slightly ahead. Clients send only input cmds for a given sim frame; the server buffers them, simulates, and broadcasts state. Clients compare and decide whether to roll back and resimulate — `FMoverSyncState::ShouldReconcile` compares `MovementMode`, `SyncStateCollection` and `MovementModifiers`.

Consequences for your code:

- Everything the simulation reads next frame must be in the sync state (or aux state) and must `NetSerialize`. State cached on a mode object, a layered move that skips a field in `NetSerialize`, or blackboard data is not restored on rollback.
- `GenerateMove` / `SimulationTick` / `ApplyMovementEffect` re-run during resimulation. Keep them deterministic: no RNG without seeded state, no spawning, no one-shot audio or VFX. Use `FMoverTimeStep::bIsResimulating` and `FMoverEventContext::bIsCausedByRollback` to gate cosmetic work.
- `ProduceInput` does **not** re-run on resim, and runs only on the controlling instance — aim assist and lock-on belong there, movement logic does not.
- Simulated proxies: prefer `ENetworkLOD::Interpolated`; forward prediction of other players mispredicts on direction changes and jumps.
- Mover does not solve GAS/movement synchronisation; GAS still replicates independently.

For RPC rules, net roles, `DOREPLIFETIME` and push model, see `ue-networking-replication`.

## Reading State and Events

```cpp
static void MyReadMoverState(const UMoverComponent& MoverComp)
{
    const FMoverSyncState& SyncState = MoverComp.GetSyncState();
    const FName ModeName             = MoverComp.GetMovementModeName();
    const FVector Velocity           = MoverComp.GetVelocity();
    const FVector Intent             = MoverComp.GetMovementIntent();
    const FRotator TargetOrientation = MoverComp.GetTargetOrientation();
    const bool bGrounded             = MoverComp.HasGameplayTag(Mover_IsOnGround, /*bExactMatch=*/false);

    FHitResult FloorHit;
    const bool bHasFloor = MoverComp.TryGetFloorCheckHitResult(FloorHit);

    UE_LOG(LogMyGame, Verbose, TEXT("%s: mode %s, speed %.1f, grounded %d, floor %d, intent %s, facing %s"),
        *SyncState.MovementMode.ToString(), *ModeName.ToString(), Velocity.Size(),
        bGrounded ? 1 : 0, bHasFloor ? 1 : 0, *Intent.ToString(), *TargetOrientation.ToString());
}
```

Multicast delegates on `UMoverComponent`: `OnPreSimulationTick` (`FMover_OnPreSimTick`), `OnPostSimulationTick` (`FMover_OnPostSimTick`), `OnPostMovement` (`FMover_OnPostMovement`), `OnPostSimulationRollback` (`FMover_OnPostSimRollback`), `OnMovementModeChanged` (`FMover_OnMovementModeChanged`), `OnTeleportSucceeded`, `OnTeleportFailed`, `OnBasedMovementApplied`, `OnGameplayTagAdded`, `OnGameplayTagRemoved`, `OnMovementTransitionTriggered`, `OnPostFinalize`, plus the C++-only `OnPostSimEventReceived`. `UCharacterMoverComponent` adds `OnStanceChanged`.

Native tags declared in `MoverTypes.h`: `Mover_IsOnGround`, `Mover_IsInAir`, `Mover_IsFalling`, `Mover_IsFlying`, `Mover_IsSwimming`, `Mover_IsCrouching`, `Mover_IsNavWalking`, `Mover_AnimRootMotion`, `Mover_SkipAnimRootMotion`, `Mover_SkipVerticalAnimRootMotion`, `Mover_DisableLanding`. Add your own with `AddGameplayTag` / `RemoveGameplayTag`; query with `HasGameplayTag` or `GetGameplayTags()`.

## Integration Points

- **Animation** — `GetPredictedTrajectory(FMoverPredictTrajectoryParams)` returns `TArray<FTrajectorySampleInfo>` for motion matching. `FLayeredMove_AnimRootMotion` and `FLayeredMove_AnimRootMotion_SimDriven` drive root motion; `ConvertLocalRootMotionToWorld` plus `ProcessLocalRootMotionDelegate` / `ProcessWorldRootMotionDelegate` let Motion Warping hook in. `MoverAnimNext` (Experimental in 5.8) bridges to UAF. Montages and anim graph belong to `ue-animation-system`.
- **AI** — add `UNavMoverComponent` alongside the Mover component; it implements `INavMovementInterface` and `IRVOAvoidanceInterface`, and `ConsumeNavMovementData(OutIntent, OutVelocity)` feeds `ProduceInput`. `UNavWalkingMode` / `UAsyncNavWalkingMode` project onto the navmesh. Navmesh generation and queries belong to `ue-ai-navigation`.
- **Mass** — `MoverIntegrations` (Experimental in 5.8) supplies `UMoverMassAgentTrait`, `UMoverMassAgentOrientationSyncTrait` and `UMassMoverInputComponent` (an `IMoverInputProducerInterface` component). Entity/processor design belongs to `ue-mass-entity`.
- **Physics** — kinematic modes sweep with `UMovementUtils::TrySafeMoveUpdatedComponent` and `TryMoveToSlideAlongSurface`; impacts route through `HandleImpact(FMoverOnImpactParams&)`. ChaosMover instead drives a Chaos character-ground constraint on the physics thread. Channels, sweeps and responses belong to `ue-physics-collision`.

## Deprecated — do not use

| Do not emit | Use in 5.8 | Source |
|---|---|---|
| `UBaseMovementMode::OnActivate()` | `Activate()` | `UE_DEPRECATED(5.6)` in `MovementMode.h` |
| `UBaseMovementMode::OnDeactivate()` | `Deactivate()` | `UE_DEPRECATED(5.6)` in `MovementMode.h` |
| `UBaseMovementMode::OnGenerateMove()` | `GenerateMove_Implementation()` | `UE_DEPRECATED(5.6)` in `MovementMode.h` |
| `UBaseMovementMode::OnSimulationTick()` | `SimulationTick_Implementation()` | `UE_DEPRECATED(5.6)` in `MovementMode.h` |
| `UBaseMovementModeTransition::OnEvaluate()` | `Evaluate_Implementation()` | `UE_DEPRECATED(5.6)` in `MovementModeTransition.h` |
| `UBaseMovementModeTransition::OnTrigger()` | `Trigger_Implementation()` | `UE_DEPRECATED(5.6)` in `MovementModeTransition.h` |
| `UMoverComponent::GetFutureTrajectory()` | `GetPredictedTrajectory()` | `UE_DEPRECATED(5.5)` in `MoverComponent.h` |
| `UMoverComponent::HasValidCachedState()` | nothing — state is always valid now | `UE_DEPRECATED(5.6)` in `MoverComponent.h` |
| `UMoverComponent::HasValidCachedInputCmd()` | nothing — input cmd is always valid now | `UE_DEPRECATED(5.6)` in `MoverComponent.h` |
| `SetTransforms_WorldSpace(Loc, Orient, Velocity, Base, BaseBone)` | the overload taking `FVector WorldAngularVelocityDegrees` | `UE_DEPRECATED(5.7)` in `MoverDataModelTypes.h` |
| `UMovementUtils::ComputeAngularVelocity(FRotator, ...)` | `ComputeAngularVelocityDegrees()` | `UE_DEPRECATED(5.7)` in `MoveLibrary/MovementUtils.h` |
| `UMovementUtils::ApplyAngularVelocity(FRotator, FRotator, float)` | `ApplyAngularVelocityToRotator()` / `ApplyAngularVelocityToQuat()` | `UE_DEPRECATED(5.7)` in `MoveLibrary/MovementUtils.h` |
| `UMovementUtils::IsAngularVelocityZero(FRotator)` | angular velocity is an `FVector` — test it directly | `UE_DEPRECATED(5.7)` in `MoveLibrary/MovementUtils.h` |
| `UFloorQueryUtils::FindFloor` / `ComputeFloorDist` with loose float params | the overloads taking `FFloorCheckSettings` | `UE_DEPRECATED(5.8)` in `MoveLibrary/FloorQueryUtils.h` |
| `UAirMovementUtils::IsValidLandingSpot` / `TryMoveToFallAlongSurface` / `TestFallingMoveAlongHitSurface` with loose float params | the `FFloorCheckSettings` overloads | `UE_DEPRECATED(5.8)` in `MoveLibrary/AirMovementUtils.h` |
| `UGroundMovementUtils::TryMoveToStepUp` / `TestMoveToStepOver` with loose float params | the `FFloorCheckSettings` overloads | `UE_DEPRECATED(5.8)` in `MoveLibrary/GroundMovementUtils.h` |
| `EBlackboardPersistencePolicy::NextFrameOnly` | `EBlackboardPersistencePolicy::ThroughNextFrame` | `UE_DEPRECATED(5.8)` in `MoveLibrary/RollbackBlackboard.h` |

## Common Mistakes

**Storing per-frame state on the mode object:** a mode is a shared instanced `UObject`, not per-frame storage. A member written in `SimulationTick` is never rolled back, so it silently desyncs under latency. Put it in a `FMoverDataStructBase` inside `FMoverSyncState` and add the type to `PersistentSyncStateDataTypes`.

**Forgetting the backend:** `UMoverComponent` has no `TickComponent`-driven update. With no `BackendClass` set to a component implementing `IMoverBackendLiaisonInterface` — and, for the Network Prediction liaison, the `NetworkPrediction` plugin enabled — the actor simply never moves.

**Mixing CMC and Mover on one pawn:** two components fighting over the same root produces jitter and corrections. Pick one; `UMoverComponent` does not need `ACharacter`.

**Assuming CMC APIs exist:**
```cpp
// WRONG — no such members on UMoverComponent
MoverComp.Velocity = FVector(0.0, 0.0, 600.0);
MoverComp.SetMovementMode(MOVE_Flying);

// RIGHT
static void MyStartFlyingJump(UMoverComponent& MoverComp)
{
    TSharedPtr<FLayeredMove_JumpImpulseOverDuration> Jump = MakeShared<FLayeredMove_JumpImpulseOverDuration>();
    Jump->UpwardsSpeed = 600.f;
    MoverComp.QueueLayeredMove(Jump);
    MoverComp.QueueNextMode(DefaultModeNames::Flying);
}
```

**Omitting a field from `NetSerialize`:** a layered move or state struct that serializes only some of its fields replays with different values after a correction, producing rubber-banding that appears only under latency. Serialize everything the move reads, and call `Super::NetSerialize(Ar)` first.

**Queueing a move you then mutate:** `QueueLayeredMove`, `QueueMovementModifier` and `QueueInstantMovementEffect` keep your `TSharedPtr` in a queue that the simulation (possibly on another thread) flushes later, and the sync state clones it after that. Changes made afterwards race with the simulation and may or may not be seen — never touch the struct once queued.

**Expecting an immediate mode change:** `QueueNextMode` takes effect on the next simulation frame, not the calling frame. Read back with `GetNextMovementModeName()`, not `GetMovementModeName()`.

**Spawning or playing effects inside the simulation:** mode and layered-move code re-runs during resimulation. Gate cosmetic work on `!TimeStep.bIsResimulating`, or do it from `OnPostFinalize` / `OnMovementModeChanged`.

**Two modifiers of the same type:** Mover keeps only one per type because the default `Matches` compares the struct type. Override `Matches` with fields your `NetSerialize` also writes if you need several.

**Trusting the blackboard:** `UMoverBlackboard` entries are invalidated on rollback and on mode changes. Always handle `TryGet` returning false, and never read a value as a different type than it was stored with.

## Related Skills

- `ue-character-movement` — `UCharacterMovementComponent`, `ACharacter`, `FSavedMove_Character`; the system Mover is intended to succeed
- `ue-networking-replication` — net roles, RPCs, `DOREPLIFETIME`, push model, relevancy; the replication layer under the Mover backends
- `ue-animation-system` — montages, anim graph, root motion and motion matching fed by Mover trajectories
- `ue-ai-navigation` — navmesh generation, pathfollowing and avoidance behind `UNavMoverComponent` and `UNavWalkingMode`
- `ue-physics-collision` — collision channels, sweeps and Chaos bodies used by Mover sweeps and the ChaosMover backend
- `ue-gameplay-framework` — pawn, controller and possession wiring around a Mover actor
- `ue-input-system` — Enhanced Input actions and mappings that feed `ProduceInput`
- `ue-mass-entity` — Mass entities and processors behind the `MoverIntegrations` traits
