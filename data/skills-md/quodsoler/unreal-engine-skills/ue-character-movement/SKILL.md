---
name: ue-character-movement
description: "Use this skill when working with character movement, CharacterMovementComponent, CMC, movement modes, walking, falling, swimming, flying, custom movement, network prediction, FSavedMove, root motion, floor detection, step-up, or character physics. Also use for 'PhysWalking', 'PhysCustom', 'LaunchCharacter', 'WalkableFloor', or 'movement replication'. See references/ for CMC extension patterns and movement pipeline details."
metadata:
  version: 1.0.0
---

# UE Character Movement

You are an expert in Unreal Engine's `UCharacterMovementComponent` (CMC), the core system that drives character locomotion, floor detection, network prediction, and root motion integration. You understand the full Phys* pipeline, custom movement mode implementation, and the `FSavedMove_Character` prediction architecture.

## Context Check

Read `.agents/ue-project-context.md` to determine:
- Whether the project uses `ACharacter` or a custom pawn with its own movement
- The UE version (UE 5.4+ adds `GravityDirection` support, UE 5.5 changes `DoJump` signature)
- Whether multiplayer is involved (affects prediction pipeline complexity)
- Any existing CMC subclass or custom movement modes already in use

## Information Gathering

Ask the developer:
1. Are you extending `UCharacterMovementComponent` or configuring the default one?
2. Do you need custom movement modes (wall-running, climbing, dashing)?
3. Is this multiplayer? If so, do custom abilities need network prediction?
4. Are you integrating root motion from animations or gameplay code?
5. Do you need custom gravity directions (UE 5.4+)?

---

## CMC Architecture

`UCharacterMovementComponent` sits at the end of a four-level class hierarchy:

```
UMovementComponent
  -> UNavMovementComponent
    -> UPawnMovementComponent
      -> UCharacterMovementComponent
```

CMC also implements `IRVOAvoidanceInterface` and `INetworkPredictionInterface`. It is declared `UCLASS(MinimalAPI)`.

CMC lives as a default subobject on `ACharacter`, created in the constructor. `ACharacter` provides the capsule, skeletal mesh, and high-level actions (`Jump`, `Crouch`, `LaunchCharacter`), while CMC handles the actual physics simulation, floor detection, and network prediction.

### Movement Modes

CMC dispatches movement logic through `EMovementMode`:

| Mode | Value | Description |
|------|-------|-------------|
| `MOVE_None` | 0 | No movement processing |
| `MOVE_Walking` | 1 | Ground movement with floor detection and step-up |
| `MOVE_NavWalking` | 2 | Walking driven by navmesh projection |
| `MOVE_Falling` | 3 | Airborne — gravity, air control, landing detection |
| `MOVE_Swimming` | 4 | Fluid movement with buoyancy |
| `MOVE_Flying` | 5 | Free 3D movement, no gravity |
| `MOVE_Custom` | 6 | User-defined; dispatches to `PhysCustom` with a `uint8` sub-mode |
| `MOVE_MAX` | 7 | Sentinel value |

Change modes with `SetMovementMode(EMovementMode, uint8 CustomMode = 0)`. The CMC calls `OnMovementModeChanged(PreviousMode, PreviousCustomMode)` after every transition, which is the correct place to handle enter/exit logic for custom modes.

---

## Phys* Movement Pipeline

Every tick, CMC processes movement through a strict pipeline. Understanding this flow is essential for writing correct custom movement or debugging unexpected behavior.

`PerformMovement(float DeltaTime)` is the main entry point (protected). It calls `StartNewPhysics()`, which dispatches to the appropriate `Phys*` function based on the current `EMovementMode`. Each `Phys*` function is `protected virtual`:

- `PhysWalking(float deltaTime, int32 Iterations)` — ground movement
- `PhysNavWalking(float deltaTime, int32 Iterations)` — navmesh-projected walking
- `PhysFalling(float deltaTime, int32 Iterations)` — airborne/gravity
- `PhysSwimming(float deltaTime, int32 Iterations)` — fluid movement
- `PhysFlying(float deltaTime, int32 Iterations)` — free flight
- `PhysCustom(float deltaTime, int32 Iterations)` — your code here

Inside each `Phys*` function, two core methods do the heavy lifting:

**`CalcVelocity`** computes the velocity for this frame:
```cpp
// BlueprintCallable
void CalcVelocity(float DeltaTime, float Friction, bool bFluid, float BrakingDeceleration);
```

**`SafeMoveUpdatedComponent`** moves the capsule and resolves penetration:
```cpp
virtual bool SafeMoveUpdatedComponent(
    const FVector& Delta,
    const FQuat& NewRotation,
    bool bSweep,
    FHitResult& OutHit,
    ETeleportType Teleport = ETeleportType::None
);
```

It wraps `MoveUpdatedComponent` and automatically handles depenetration if the move results in an overlap. Always prefer `SafeMoveUpdatedComponent` over `MoveUpdatedComponent` in custom Phys* functions.

When a sweep hits a surface, `SlideAlongSurface` projects movement along it. When hits occur in a corner (two blocking surfaces), CMC calls `TwoWallAdjust` (virtual on `UMovementComponent`) to compute a safe movement direction that avoids both walls. During `PhysWalking`, `ComputeGroundMovementDelta` (virtual) adjusts the velocity delta to follow the floor slope — it projects horizontal input onto the floor plane so the character walks along inclines rather than into them.

See `references/movement-pipeline.md` for the full flow diagram and per-mode breakdown.

---

## Floor Detection

CMC's walking mode relies on continuous floor detection to determine whether the character is grounded.

### FFindFloorResult

```cpp
struct FFindFloorResult
{
    uint32 bBlockingHit : 1;    // Sweep hit something
    uint32 bWalkableFloor : 1;  // Hit surface passes walkability test
    uint32 bLineTrace : 1;      // Result came from line trace (not sweep)
    float FloorDist;             // Distance from capsule bottom to floor
    float LineDist;              // Distance from line trace
    FHitResult HitResult;        // Full hit result data

    bool IsWalkableFloor() const { return bBlockingHit && bWalkableFloor; }
};
```

### Floor Detection Methods

`FindFloor` is the primary method:
```cpp
void FindFloor(
    const FVector& CapsuleLocation,
    FFindFloorResult& OutFloorResult,
    bool bCanUseCachedLocation,
    const FHitResult* DownwardSweepResult = nullptr
);
```

It delegates to `ComputeFloorDist()`, which performs a downward capsule sweep followed by a line trace. The sweep finds the floor surface, and the line trace validates walkability at the exact contact point.

### Walkable Floor Angle

Two linked properties control what counts as "walkable":

- `WalkableFloorAngle` (default 44.765 degrees) — the maximum surface angle in degrees
- `WalkableFloorZ` — the corresponding Z component of the surface normal (auto-calculated from the angle)

Set the angle, not the Z value directly. `SetWalkableFloorAngle()` updates both.

---

## Custom Movement Modes

`MOVE_Custom` with a `uint8` sub-mode is the standard way to add new movement types. This gives you up to 256 custom modes while reusing CMC's full network prediction pipeline.

### Implementation Steps

1. Define custom mode constants:
```cpp
UENUM(BlueprintType)
enum class ECustomMovementMode : uint8
{
    WallRun = 0,
    Climb   = 1,
    Dash    = 2
};
```

2. Override `PhysCustom` in your CMC subclass:
```cpp
virtual void PhysCustom(float deltaTime, int32 Iterations) override;
```

3. Enter the mode using `SetMovementMode`:
```cpp
SetMovementMode(MOVE_Custom, static_cast<uint8>(ECustomMovementMode::WallRun));
```

4. Handle transitions in `OnMovementModeChanged`:
```cpp
virtual void OnMovementModeChanged(EMovementMode PrevMode, uint8 PrevCustomMode) override;
```

Inside `PhysCustom`, dispatch on `CustomMovementMode` and implement your simulation. Call `CalcVelocity` for acceleration, `SafeMoveUpdatedComponent` for capsule movement, and `SetMovementMode` when transitioning out.

See `references/cmc-extension-patterns.md` for a complete wall-run implementation.

---

## Network Prediction

CMC uses a client-side prediction and server reconciliation model. The client runs movement locally, saves inputs, sends them to the server, and corrects if the server disagrees. This is why custom movement must integrate with the prediction pipeline to work in multiplayer.

### FSavedMove_Character

Each client tick generates a saved move that records the input state:

Key fields: `bPressedJump`, `bWantsToCrouch`, `StartLocation`, `StartVelocity`, `SavedLocation`, `Acceleration`, `MaxSpeed`.

Key virtuals to override for custom data:
- `Clear()` — reset your custom fields
- `SetMoveFor(ACharacter*, float, FVector const&, FNetworkPredictionData_Client_Character&)` — capture your custom state from the CMC before the move executes
- `PrepMoveFor(ACharacter*)` — restore your custom state before replaying a move
- `GetCompressedFlags() const` — pack custom booleans into the `uint8` flags
- `CanCombineWith(const FSavedMovePtr&, ACharacter*, float)` — return `true` only if two moves are identical (enables bandwidth optimization)
- `PostUpdate(ACharacter*, EPostUpdateMode)` — called after the move executes
- `IsImportantMove(const FSavedMovePtr&)` — prevent combining if this move carries significant state

### CompressedFlags

The `uint8` returned by `GetCompressedFlags` has a fixed layout:

| Flag | Value | Purpose |
|------|-------|---------|
| `FLAG_JumpPressed` | `0x01` | Jump input |
| `FLAG_WantsToCrouch` | `0x02` | Crouch input |
| `FLAG_Reserved_1` | `0x04` | Engine reserved |
| `FLAG_Reserved_2` | `0x08` | Engine reserved |
| `FLAG_Custom_0` | `0x10` | Your custom flag |
| `FLAG_Custom_1` | `0x20` | Your custom flag |
| `FLAG_Custom_2` | `0x40` | Your custom flag |
| `FLAG_Custom_3` | `0x80` | Your custom flag |

You get four custom bits. For more complex state, use `FCharacterNetworkMoveData`.

### FNetworkPredictionData_Client_Character

Override `AllocateNewMove()` to return your custom `FSavedMove` subclass:

```cpp
class FMyNetworkPredictionData : public FNetworkPredictionData_Client_Character
{
public:
    FMyNetworkPredictionData(const UCharacterMovementComponent& ClientMovement)
        : FNetworkPredictionData_Client_Character(ClientMovement) {}

    virtual FSavedMovePtr AllocateNewMove() override;
};
```

The CMC exposes this via `GetPredictionData_Client()`, which you override to lazy-init your custom prediction data class.

### Modern Packed RPCs

UE5 uses packed move RPCs on `ACharacter`:
- `ServerMovePacked(FCharacterServerMovePackedBits)` — client to server
- `ClientMoveResponsePacked(FCharacterMoveResponsePackedBits)` — server to client

The old RPCs (`ServerMove`, `ServerMoveDual`, `ClientAdjustPosition`) are `DEPRECATED_CHARACTER_MOVEMENT_RPC`. For custom network data beyond CompressedFlags, derive `FCharacterNetworkMoveData` (override `ClientFillNetworkMoveData`, `Serialize`), derive `FCharacterNetworkMoveDataContainer`, and call `SetNetworkMoveDataContainer()` in your CMC constructor.

See `references/cmc-extension-patterns.md` for full FSavedMove and network data implementation templates.

---

## Root Motion

Root motion allows animations or gameplay code to drive character movement directly. CMC integrates root motion through `FRootMotionSource` and its subclasses.

### FRootMotionSource

Base class fields:
- `Priority` — higher priority sources override lower
- `LocalID` — unique ID returned by `ApplyRootMotionSource`
- `InstanceName` — `FName` for retrieval and removal
- `Duration` — total time in seconds; **negative Duration means infinite** (runs until explicitly removed)
- `AccumulateMode` — `Override` (replaces other sources) or `Additive` (stacks)

### Subclasses

| Class | Key Parameters | Use Case |
|-------|---------------|----------|
| `FRootMotionSource_ConstantForce` | `Force`, `StrengthOverTime` | Knockback, wind |
| `FRootMotionSource_RadialForce` | `Location`, `Radius`, `Strength` | Explosions, vortex |
| `FRootMotionSource_MoveToForce` | `StartLocation`, `TargetLocation` | Dash to fixed point |
| `FRootMotionSource_MoveToDynamicForce` | `SetTargetLocation()` | Homing dash |
| `FRootMotionSource_JumpForce` | `Rotation`, `Distance`, `Height` | Targeted jump arc |

### CMC Methods

```cpp
// Returns uint16 LocalID for tracking
uint16 ApplyRootMotionSource(TSharedPtr<FRootMotionSource> Source);

// Retrieve by InstanceName
TSharedPtr<FRootMotionSource> GetRootMotionSource(FName InstanceName);

// Remove by InstanceName
void RemoveRootMotionSource(FName InstanceName);
```

Apply a constant knockback:
```cpp
auto Knockback = MakeShared<FRootMotionSource_ConstantForce>();
Knockback->InstanceName = TEXT("Knockback");
Knockback->Duration = 0.3f;
Knockback->Force = KnockbackDirection * KnockbackStrength;
Knockback->AccumulateMode = ERootMotionAccumulateMode::Override;
CMC->ApplyRootMotionSource(Knockback);
```

---

## Key Properties

| Property | Default | Description |
|----------|---------|-------------|
| `MaxWalkSpeed` | 600 | Maximum ground speed |
| `MaxAcceleration` | — | Rate of speed change |
| `GravityScale` | 1.0 | Multiplier on world gravity |
| `JumpZVelocity` | — | Initial vertical velocity on jump |
| `AirControl` | — | Lateral control while falling (0-1) |
| `GroundFriction` | — | Friction on ground surfaces |
| `BrakingDecelerationWalking` | — | Deceleration when no input on ground |
| `MaxStepHeight` | — | Maximum height of obstacles to step over |
| `WalkableFloorAngle` | 44.765 | Max walkable surface angle in degrees |
| `MaxWalkSpeedCrouched` | — | Speed while crouching |
| `MaxSwimSpeed` | — | Maximum speed in water |
| `MaxFlySpeed` | — | Maximum speed when flying |
| `MaxCustomMovementSpeed` | — | Speed cap for custom modes |
| `bOrientRotationToMovement` | — | Rotate character toward movement direction |
| `bUseControllerDesiredRotation` | — | Smoothly rotate toward controller rotation |
| `NetworkSmoothingMode` | — | Simulated proxy interpolation mode |
| `MaxSimulationTimeStep` | — | Cap on sub-step delta for stability |
| `MaxSimulationIterations` | — | Max physics iterations per frame |
| `bUseRVOAvoidance` | false | Enable RVO (reciprocal velocity obstacle) avoidance |
| `AvoidanceGroup` | — | `FNavAvoidanceMask` — group membership for avoidance filtering |
| `AvoidanceWeight` | — | float — higher weight yields right-of-way to other agents |

### Rotation

`bOrientRotationToMovement` and `bUseControllerDesiredRotation` are mutually exclusive in practice. The first rotates the character toward its velocity direction (third-person), the second smoothly rotates toward where the controller is facing (strafing shooter). Set one, not both.

### Gravity Direction (UE 5.4+)

```cpp
virtual void SetGravityDirection(const FVector& GravityDir);
FVector GetGravityDirection() const;
bool HasCustomGravity() const;
// Transform helpers (fields are protected — access via accessors)
FQuat GetWorldToGravityTransform() const;
FQuat GetGravityToWorldTransform() const;
```

Custom gravity reorients the entire movement simulation. Walking, falling, and floor detection all respect the gravity direction when `HasCustomGravity()` returns `true`.

---

## ACharacter API

`ACharacter` provides high-level movement actions that delegate to CMC:

### Jump

```cpp
void Jump();           // Sets bPressedJump, CMC handles velocity
void StopJumping();    // Clears jump input
bool CanJump() const;  // Checks CanJumpInternal
```

Properties: `bPressedJump`, `JumpMaxHoldTime`, `JumpMaxCount`, `JumpCurrentCount`.

`DoJump(bool bReplayingMoves, float DeltaTime)` is the internal method called by CMC to apply the jump velocity. In UE 5.5+ it takes two parameters; the old `DoJump(bool)` is deprecated.

### Crouch

```cpp
void Crouch(bool bClientSimulation = false);
void UnCrouch(bool bClientSimulation = false);
```

`bIsCrouched` is the replicated state. CMC handles capsule resizing and checks for clearance before uncrouching. Note: `CrouchedHalfHeight` on CMC is deprecated as of UE 5.0 — use `SetCrouchedHalfHeight()` / `GetCrouchedHalfHeight()` on the CMC instead.

### LaunchCharacter

```cpp
void LaunchCharacter(FVector LaunchVelocity, bool bXYOverride, bool bZOverride);
```

When `bXYOverride` is `true`, replaces XY velocity entirely. When `false`, adds to existing velocity. Same logic for `bZOverride` on the Z axis. Automatically transitions to `MOVE_Falling`.

### Landed

```cpp
virtual void Landed(const FHitResult& Hit);
```

Called when the character lands after falling. Override this for landing effects, damage, or animation triggers.

### Accessors

```cpp
UCharacterMovementComponent* GetCharacterMovement() const;
UCapsuleComponent* GetCapsuleComponent() const;
USkeletalMeshComponent* GetMesh() const;
```

---

## Common Mistakes

**Modifying velocity directly instead of using CalcVelocity:**
```cpp
// WRONG: Bypasses friction, braking, and acceleration curves
Velocity = GetLastInputVector() * MaxWalkSpeed;

// RIGHT: Let CMC handle physics
CalcVelocity(DeltaTime, GroundFriction, false, BrakingDecelerationWalking);
```

**Forgetting to call Super in PhysCustom:**
```cpp
// WRONG: Skips base class bookkeeping
void UMyCMC::PhysCustom(float DT, int32 Iter)
{
    MyCustomLogic(DT, Iter);
}

// RIGHT: Call Super first (base PhysCustom is empty but future-proofs)
void UMyCMC::PhysCustom(float DT, int32 Iter)
{
    Super::PhysCustom(DT, Iter);
    MyCustomLogic(DT, Iter);
}
```

**Not saving custom state in FSavedMove:**
Custom movement flags that are not captured in `SetMoveFor` and restored in `PrepMoveFor` will be lost during server correction replays, causing desyncs.

**Using MoveUpdatedComponent instead of SafeMoveUpdatedComponent:**
`MoveUpdatedComponent` does not resolve penetration. In custom Phys* functions, always use `SafeMoveUpdatedComponent` to prevent the character from getting stuck inside geometry.

**Setting both rotation flags:**
`bOrientRotationToMovement` and `bUseControllerDesiredRotation` conflict. The character oscillates between two desired rotations each frame. Pick one based on your camera style.

**Using deprecated old-style RPCs:**
`ServerMove`, `ServerMoveDual`, `ClientAdjustPosition` are `DEPRECATED_CHARACTER_MOVEMENT_RPC`. Use the packed RPC pipeline and `FCharacterNetworkMoveData` for custom data.

---

## Reference Files

- `references/cmc-extension-patterns.md` — Complete CMC subclass templates: custom FSavedMove, prediction data, GetPredictionData_Client, wall-run PhysCustom, and custom network move data
- `references/movement-pipeline.md` — Phys* flow diagrams, floor detection chain, step-up logic, PhysWalking/PhysFalling breakdowns, and root motion replication flow

## Related Skills

- `ue-networking-replication` — Replication fundamentals, RPCs, net roles; CMC prediction builds on this
- `ue-animation-system` — Root motion from AnimMontage, animation-driven movement
- `ue-physics-collision` — Sweep queries, collision channels used by CMC floor detection
- `ue-gameplay-abilities` — GAS abilities that trigger movement modes or root motion
- `ue-ai-navigation` — NavMesh integration, MOVE_NavWalking, RVO avoidance
- `ue-input-system` — Enhanced Input feeding movement input to CMC
- `ue-actor-component-architecture` — Component subobject patterns for CMC subclasses
