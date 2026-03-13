---
name: ue-animation-system
description: "Use this skill when working with Unreal Engine animation: AnimInstance, montage playback, blend space, state machine, anim notify, IK, AnimGraph, skeletal mesh, or linked anim graphs. See references/anim-notify-reference.md for notify patterns and references/locomotion-setup.md for locomotion setup. For montage integration with GAS, see ue-gameplay-abilities."
metadata:
  version: 1.0.0
---

# UE Animation System

You are an expert in Unreal Engine's animation system.

## Context Check

Read `.agents/ue-project-context.md` first. Note which plugins are enabled
(Control Rig, Motion Matching, Full Body IK), whether GAS is in use, and the
skeleton/character hierarchy.

## Information to Gather

1. What animation need? (locomotion, ability, cinematic, IK, procedural)
2. C++ only, Blueprint only, or mixed?
3. Does the character use `ACharacter` with an existing `USkeletalMeshComponent`?
4. Is GAS active? (affects montage replication)
5. Multiplayer? (determines replication strategy)
6. Does the project use modular linked anim layers?

---

## Architecture

```
ACharacter / AActor
  └── USkeletalMeshComponent
        └── UAnimInstance subclass
              ├── NativeInitializeAnimation()           [setup, game thread]
              ├── NativeUpdateAnimation(float dt)       [game thread]
              ├── NativeThreadSafeUpdateAnimation(dt)   [worker thread]
              ├── FAnimInstanceProxy                    [worker thread eval]
              └── Montage API / Linked Layers
```

Animation updates run in two phases. Game thread: `NativeUpdateAnimation` —
safe to read gameplay state. Worker thread: blend tree evaluation. Write all
shared state as `UPROPERTY() Transient` members in `NativeUpdateAnimation`;
read those cached values in `NativeThreadSafeUpdateAnimation`.

---

## AnimInstance

### Subclass Pattern

```cpp
// MyAnimInstance.h
UCLASS()
class MYGAME_API UMyAnimInstance : public UAnimInstance
{
    GENERATED_BODY()

    virtual void NativeInitializeAnimation() override;
    virtual void NativeUpdateAnimation(float DeltaSeconds) override;
    virtual void NativeThreadSafeUpdateAnimation(float DeltaSeconds) override;

protected:
    UPROPERTY(Transient) TObjectPtr<ACharacter> OwningCharacter;
    UPROPERTY(Transient) TObjectPtr<UCharacterMovementComponent> MovementComp;

    UPROPERTY(Transient, BlueprintReadOnly, Category="Locomotion")
    float Speed = 0.f;

    UPROPERTY(Transient, BlueprintReadOnly, Category="Locomotion")
    float Direction = 0.f;

    UPROPERTY(Transient, BlueprintReadOnly, Category="Locomotion")
    bool bIsInAir = false;
};
```

```cpp
// MyAnimInstance.cpp
void UMyAnimInstance::NativeInitializeAnimation()
{
    Super::NativeInitializeAnimation(); // ALWAYS call super
    OwningCharacter = Cast<ACharacter>(TryGetPawnOwner());
    if (OwningCharacter)
        MovementComp = OwningCharacter->GetCharacterMovement();
}

void UMyAnimInstance::NativeUpdateAnimation(float DeltaSeconds)
{
    Super::NativeUpdateAnimation(DeltaSeconds);
    if (!OwningCharacter || !MovementComp) return;

    const FVector Velocity = MovementComp->Velocity;
    Speed    = Velocity.Size2D();
    bIsInAir = MovementComp->IsFalling();

    if (Speed > 3.f)
    {
        const FRotator ActorRot    = OwningCharacter->GetActorRotation();
        const FRotator VelocityRot = Velocity.ToOrientationRotator();
        Direction = UKismetMathLibrary::NormalizedDeltaRotator(
            VelocityRot, ActorRot).Yaw;
    }
}

void UMyAnimInstance::NativeThreadSafeUpdateAnimation(float DeltaSeconds)
{
    Super::NativeThreadSafeUpdateAnimation(DeltaSeconds);
    // Only read UPROPERTY members written in NativeUpdateAnimation above.
    // Do NOT call any UObject functions not marked BlueprintThreadSafe.
}
```

### FAnimInstanceProxy — Thread-Safe Access

Heavy animation logic can run on worker threads via
`NativeThreadSafeUpdateAnimation`. Access shared data through the proxy:

```cpp
void UMyAnimInstance::NativeThreadSafeUpdateAnimation(float DeltaSeconds)
{
    FMyAnimInstanceProxy& Proxy = GetProxyOnAnyThread<FMyAnimInstanceProxy>();
    Proxy.Speed = Proxy.Velocity.Size();
    Proxy.bIsFalling = Proxy.MovementMode == EMovementMode::MOVE_Falling;
}
```

```cpp
// FAnimInstanceProxy declaration — worker thread data container
USTRUCT()
struct FMyAnimInstanceProxy : public FAnimInstanceProxy
{
    GENERATED_BODY()
    FMyAnimInstanceProxy() = default;
    explicit FMyAnimInstanceProxy(UAnimInstance* Instance) : FAnimInstanceProxy(Instance) {}

    float Speed = 0.f;
    FVector Velocity = FVector::ZeroVector;
    TEnumAsByte<EMovementMode> MovementMode = MOVE_None;

    virtual void PreUpdate(UAnimInstance* AnimInstance, float DeltaSeconds) override;
    virtual void Update(float DeltaSeconds) override;
};

// In UMyAnimInstance: override CreateAnimInstanceProxy to return your proxy
virtual FAnimInstanceProxy* CreateAnimInstanceProxy() override
{ return new FMyAnimInstanceProxy(this); }
```

The engine copies data between game thread and worker thread at safe sync points.

---

## Montages

Source: `AnimMontage.h`, `AnimInstance.h`

Key API (`UAnimInstance`):
```cpp
float Montage_Play(UAnimMontage*, float PlayRate=1.f,
    EMontagePlayReturnType=MontageLength, float StartAt=0.f, bool bStopAll=true);
void  Montage_Stop(float BlendOut, const UAnimMontage* Montage=nullptr);
void  Montage_Pause(const UAnimMontage* Montage=nullptr);
void  Montage_Resume(const UAnimMontage* Montage);
void  Montage_JumpToSection(FName Section, const UAnimMontage* Montage=nullptr);
void  Montage_SetNextSection(FName From, FName To, const UAnimMontage* Montage=nullptr);
bool  Montage_IsActive(const UAnimMontage*) const;
bool  Montage_IsPlaying(const UAnimMontage*) const;
FName Montage_GetCurrentSection(const UAnimMontage* Montage=nullptr) const;
float Montage_GetPosition(const UAnimMontage*) const;
```

### Playing + Delegate Pattern

```cpp
void UMyComponent::PlayAttackMontage(UAnimMontage* Montage)
{
    UAnimInstance* AnimInst = GetMesh()->GetAnimInstance();
    if (!AnimInst || !Montage) return;

    // Play FIRST — Montage_SetEndDelegate calls GetActiveInstanceForMontage()
    // internally, which returns nullptr until Montage_Play creates the instance.
    if (AnimInst->Montage_Play(Montage) <= 0.f) return;

    FOnMontageEnded EndDelegate;
    EndDelegate.BindUObject(this, &UMyComponent::OnAttackEnded);
    AnimInst->Montage_SetEndDelegate(EndDelegate, Montage);

    FOnMontageBlendingOutStarted BlendOutDelegate;
    BlendOutDelegate.BindUObject(this, &UMyComponent::OnAttackBlendingOut);
    AnimInst->Montage_SetBlendingOutDelegate(BlendOutDelegate, Montage);
}

void UMyComponent::OnAttackEnded(UAnimMontage* Montage, bool bInterrupted) { }
void UMyComponent::OnAttackBlendingOut(UAnimMontage* Montage, bool bInterrupted) { }
```

### Dynamic Slot Montage

```cpp
UAnimMontage* DynMontage = AnimInst->PlaySlotAnimationAsDynamicMontage(
    SomeSequence, FName("UpperBody"), 0.25f, 0.25f, 1.f, 1);
```

### Multiplayer Replication

- **With GAS**: use `UAbilitySystemComponent::PlayMontage()` — GAS handles
  replication via `FGameplayAbilityRepAnimMontage`.
- **Without GAS**: replicate a montage pointer or a custom rep struct; server
  calls `Montage_Play`, clients play on `OnRep_`.
- Never call `Montage_Play` independently on all net roles without sync.

### GAS Integration — PlayMontageAndWait

```cpp
// GAS ability task — PlayMontageAndWait (requires GameplayAbilities module)
UAbilityTask_PlayMontageAndWait* Task =
    UAbilityTask_PlayMontageAndWait::CreatePlayMontageAndWaitProxy(
        this, NAME_None, AttackMontage, 1.f);
Task->OnCompleted.AddDynamic(this, &UMyAbility::OnMontageCompleted);
Task->OnInterrupted.AddDynamic(this, &UMyAbility::OnMontageInterrupted);
Task->ReadyForActivation();  // must call to start the task
```

---

## Blend Spaces

Blend spaces are data assets sampled in the AnimGraph. Drive them by setting
`UPROPERTY` members on the AnimInstance that the AnimGraph reads.

- **1D** (`UBlendSpace1D`): single axis, typically Speed (0–600).
  Use `FInterpolationParameter` with `InterpolationType=SpringDamper`,
  `InterpolationTime=0.15`, `DampingRatio=1.0`.
- **2D** (`UBlendSpace`): two axes — Direction (-180 to 180) and Speed (0–600).
  Cardinal direction samples at each speed tier.
- **Aim Offset** (`UAimOffsetBlendSpace`): additive blend space for Yaw/Pitch
  aiming, placed after the base locomotion pose in the AnimGraph.

See `references/locomotion-setup.md` for complete axis configuration and
sample placement.

---

## State Machines

State machines live in the AnimGraph. Bind native C++ logic to transition rules
and state entry/exit without Blueprint:

```cpp
// In NativeInitializeAnimation()
AddNativeTransitionBinding(
    FName("LocomotionSM"), FName("Idle"), FName("Walk/Run"),
    FCanTakeTransition::CreateUObject(this, &UMyAnimInstance::CanStartMoving),
    FName("IdleToMoving"));

AddNativeStateEntryBinding(
    FName("LocomotionSM"), FName("Land"),
    FOnGraphStateChanged::CreateUObject(this, &UMyAnimInstance::OnLandEntered));
```

Query state machine at runtime:
```cpp
const FAnimNode_StateMachine* SM =
    GetStateMachineInstanceFromName(FName("LocomotionSM"));
float RunWeight = GetInstanceStateWeight(
    GetStateMachineIndex(FName("LocomotionSM")), SM->GetCurrentState());
```

### Conduit Nodes

Conduits evaluate a single boolean rule and fan out to multiple destination
states — replacing duplicated transition logic. Add a Conduit in the AnimGraph
editor; its `CanEnterTransition` runs once and all outgoing transitions share
the result. Use conduits when three or more states need the same entry condition
(e.g., "is grounded?"). For simple A-to-B transitions, a direct rule is clearer.

---

## Anim Notifies

Source: `AnimNotify.h`, `AnimNotifyState.h`

### UAnimNotify — Point-in-Time

```cpp
UCLASS(meta=(DisplayName="Footstep"))
class MYGAME_API UFootstepNotify : public UAnimNotify
{
    GENERATED_BODY()
public:
    // Always override the UE5 3-argument signature
    virtual void Notify(USkeletalMeshComponent* MeshComp,
        UAnimSequenceBase* Animation,
        const FAnimNotifyEventReference& EventReference) override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Footstep")
    FName FootSocket = FName("foot_l");
};
```

### UAnimNotifyState — Duration (Begin/Tick/End)

```cpp
UCLASS(meta=(DisplayName="Weapon Collision Window"))
class MYGAME_API UWeaponCollisionState : public UAnimNotifyState
{
    GENERATED_BODY()
public:
    virtual void NotifyBegin(USkeletalMeshComponent*, UAnimSequenceBase*,
        float TotalDuration, const FAnimNotifyEventReference&) override;
    virtual void NotifyEnd(USkeletalMeshComponent*, UAnimSequenceBase*,
        const FAnimNotifyEventReference&) override;
};
```

### BranchingPoint (Synchronous)

Set `bIsNativeBranchingPoint = true` in the constructor. Override
`BranchingPointNotify()` instead of `Notify()`. Fires synchronously during
`Montage_Advance` — use for section jumps and precise timeline control. All
other notifies are queued (fire after tick completes, safe for VFX/SFX).

### Named Notify Delegate

```cpp
AnimInst->OnPlayMontageNotifyBegin.AddDynamic(
    this, &UMyComponent::HandleNotifyBegin);

void UMyComponent::HandleNotifyBegin(FName NotifyName,
    const FBranchingPointNotifyPayload& Payload)
{
    if (NotifyName == FName("EnableHitbox")) ActivateHitDetection();
}
```

See `references/anim-notify-reference.md` for built-in notify catalog and more
custom patterns.

---

## IK and Procedural

### Foot IK with Line Traces (NativeUpdateAnimation — game thread)

```cpp
FVector UMyAnimInstance::GetFootTarget(FName SocketName) const
{
    const FVector Foot = GetOwningComponent()->GetSocketLocation(SocketName);
    FHitResult Hit;
    FCollisionQueryParams P(SCENE_QUERY_STAT(FootIK), true);
    P.AddIgnoredActor(OwningCharacter);
    if (GetWorld()->LineTraceSingleByChannel(
            Hit, Foot + FVector(0,0,50), Foot - FVector(0,0,75),
            ECC_Visibility, P))
        return Hit.ImpactPoint;
    return Foot;
}
```

Feed results into a Control Rig asset (UE5 recommended) or a
**Two Bone IK** skeletal control node in the AnimGraph.

**Skeletal control nodes** (AnimGraph):

| Node | Purpose |
|---|---|
| Two Bone IK | Two-joint IK (arm, leg) — effector + joint target |
| FABRIK | Multi-bone chain IK — tip bone + effector |
| Look At | Single bone tracks target location with clamp |
| Copy Bone | Copies transform components between bones |
| Spline IK | Bones follow a spline curve (spine, tail) |

### Layered Blend Per Bone (Upper/Lower Split)

In the AnimGraph:
1. Connect state machine output to **Base Pose**.
2. Connect `UpperBody` slot output to **Blend Poses 0**.
3. Layer Setup: Bone=`spine_01`, Depth=0, MeshPoseBlendFactor=1.0.

Attack montages use the `UpperBody` slot; locomotion plays uninterrupted below.

### Aim Offset

```cpp
// In NativeUpdateAnimation:
const FRotator Delta = UKismetMathLibrary::NormalizedDeltaRotator(
    OwningCharacter->GetBaseAimRotation(),
    OwningCharacter->GetActorRotation());
AimYaw   = FMath::Clamp(Delta.Yaw,   -90.f, 90.f);
AimPitch = FMath::Clamp(Delta.Pitch, -90.f, 90.f);
```

Place an Aim Offset node after the base pose in the AnimGraph, feeding
`AimYaw` and `AimPitch`.

---

## Linked Anim Graphs and Layers

Source: `AnimNode_LinkedAnimGraph.h`, `AnimNode_LinkedAnimLayer.h`

### Linked Anim Layer (Recommended)

1. Create a `UAnimLayerInterface` Blueprint with layer function signatures.
2. Main AnimInstance has **Linked Anim Layer** nodes referencing the interface.
3. Separate AnimInstance subclasses implement the interface per mode.
4. Swap at runtime:

```cpp
// Switch locomotion implementation
AnimInst->LinkAnimClassLayers(UClimbingLocomotionLayer::StaticClass());
// Reset all layers to defaults:
AnimInst->LinkAnimClassLayers(nullptr);
// Retrieve a linked instance:
UAnimInstance* Layer =
    AnimInst->GetLinkedAnimLayerInstanceByClass(UClimbingLocomotionLayer::StaticClass());
```

### Linked Anim Graph (by Tag)

```cpp
AnimInst->LinkAnimGraphByTag(FName("CombatGraph"), UMyCombatAnimInstance::StaticClass());
UAnimInstance* Sub = AnimInst->GetLinkedAnimGraphInstanceByTag(FName("CombatGraph"));
```

### Notify Propagation

```cpp
AnimInst->SetReceiveNotifiesFromLinkedInstances(true);
AnimInst->SetPropagateNotifiesToLinkedInstances(true);
// UE5.2+: let linked layers share main instance montage evaluation:
// AnimInst->SetUseMainInstanceMontageEvaluationData(true);
```

---

## Root Motion

```cpp
// Options: NoRootMotionExtraction, IgnoreRootMotion,
//          RootMotionFromMontagesOnly, RootMotionFromEverything
RootMotionMode = ERootMotionMode::RootMotionFromMontagesOnly;

// Per-montage disable
FAnimMontageInstance* Inst = AnimInst->GetActiveInstanceForMontage(Montage);
if (Inst) { Inst->PushDisableRootMotion(); /* ... */ Inst->PopDisableRootMotion(); }
```

For networked root motion, set the movement component's smoothing mode to
`ENetworkSmoothingMode::Exponential` and enable
`bAllowPhysicsRotationDuringAnimRootMotion` if rotation comes from animation.
The server runs root motion authoritatively; clients predict and correct via
`FRootMotionMovementParams`.

---

## Common Mistakes

| Anti-Pattern | Fix |
|---|---|
| Reading gameplay state in `NativeThreadSafeUpdateAnimation` | Cache values as `UPROPERTY Transient` in `NativeUpdateAnimation` (game thread) |
| Polling `Montage_IsActive` in a loop | Bind `FOnMontageEnded` delegate before calling `Montage_Play` |
| Two montages sharing the same slot group | Use distinct slot names (`UpperBody`, `LowerBody`) or `bStopAllMontages=false` |
| Skipping `Super::NativeInitializeAnimation()` | Always call super — it initializes the proxy and skeleton |
| Calling non-thread-safe UObject methods in thread-safe update | Only read primitive `UPROPERTY` copies; never call `GetOwningActor()` from worker thread |

---

## Build.cs

```csharp
PublicDependencyModuleNames.AddRange(new string[] {
    "Core", "CoreUObject", "Engine", "AnimGraphRuntime"
});
// Optional:
PrivateDependencyModuleNames.Add("ControlRig");        // Control Rig IK
PrivateDependencyModuleNames.Add("GameplayAbilities"); // GAS montage tasks
```

---

## Related Skills

- `ue-gameplay-abilities` — `PlayMontageAndWait` task, GAS montage replication.
- `ue-actor-component-architecture` — SkeletalMeshComponent setup, Character
  hierarchy, component tick ordering.
- `ue-cpp-foundations` — delegate binding, `UPROPERTY` specifiers, `TWeakObjectPtr`.

## Reference Files

- `references/anim-notify-reference.md` — built-in notify catalog and custom
  notify implementation patterns.
- `references/locomotion-setup.md` — complete locomotion blend space and state
  machine configuration guide.
