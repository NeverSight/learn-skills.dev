---
name: ue-input-system
description: "Use this skill when implementing player input with Unreal Engine's Enhanced Input system. Also use when the user mentions 'Enhanced Input', 'input', 'input action', 'InputAction', 'mapping context', 'InputMappingContext', 'input binding', 'key binding', 'input trigger', 'input modifier', 'gamepad', or 'keyboard'. Covers ETriggerEvent, built-in triggers (Hold, Tap, Pulse, ChordAction, Combo), built-in modifiers (DeadZone, Scalar, Negate, SwizzleAxis), and custom trigger/modifier authoring. See references/input-action-reference.md for the full catalogue. For UI input modes, see ue-ui-umg-slate."
metadata:
  version: 1.0.0
---

# UE Enhanced Input System

You are an expert in Unreal Engine's Enhanced Input system.

## Context Check

Read `.agents/ue-project-context.md` before proceeding. Confirm:

- `EnhancedInput` plugin is listed as enabled
- Target platforms (affects which modifiers are needed per platform)
- Whether CommonUI is in use (it manages input mode switching automatically)
- Whether the project still uses legacy input (migration may be needed)

## Information Gathering

Ask the developer: what actions are needed and their value types (Bool/Axis1D/Axis2D/Axis3D), which platforms, any complex input requirements (hold-to-charge, double-tap, combos, chord shortcuts), and whether multiple input modes are required (gameplay vs UI vs vehicle).

---

## Enhanced Input Setup

### Plugin and Module

`.uproject`: add `{ "Name": "EnhancedInput", "Enabled": true }` to Plugins.

`Build.cs`: add `"EnhancedInput"` to `PublicDependencyModuleNames`.

`DefaultInput.ini`:
```ini
[/Script/Engine.InputSettings]
DefaultPlayerInputClass=/Script/EnhancedInput.EnhancedPlayerInput
DefaultInputComponentClass=/Script/EnhancedInput.EnhancedInputComponent
```

### UInputAction Asset

`UInputAction : UDataAsset`. Create one per logical player action. Key properties (from `InputAction.h`):

```cpp
EInputActionValueType ValueType = EInputActionValueType::Boolean;
// Boolean | Axis1D (float) | Axis2D (FVector2D) | Axis3D (FVector)

EInputActionAccumulationBehavior AccumulationBehavior
    = EInputActionAccumulationBehavior::TakeHighestAbsoluteValue;
// TakeHighestAbsoluteValue — highest magnitude wins across all mappings to this action
// Cumulative — all mapping values sum (W + S cancel each other for WASD)

bool bConsumeInput = true;  // blocks lower-priority Enhanced Input mappings to same keys

TArray<TObjectPtr<UInputTrigger>> Triggers;   // applied AFTER per-mapping triggers
TArray<TObjectPtr<UInputModifier>> Modifiers; // applied AFTER per-mapping modifiers
```

### UInputMappingContext Asset

`UInputMappingContext : UDataAsset`. Maps physical keys to actions.

- `DefaultKeyMappings.Mappings` — `TArray<FEnhancedActionKeyMapping>` of key-to-action entries
- `MappingProfileOverrides` — per-profile key overrides for player remapping support
- `RegistrationTrackingMode`: `Untracked` (default, first Remove wins) or `CountRegistrations` (IMC stays until Remove called N times, safe when multiple systems share it)

---

## Binding Actions in C++

### SetupPlayerInputComponent

```cpp
// MyCharacter.h — declare assets and handlers
UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
TObjectPtr<UInputMappingContext> DefaultMappingContext;
UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
TObjectPtr<UInputAction> MoveAction;
UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
TObjectPtr<UInputAction> JumpAction;

void Move(const FInputActionValue& Value);
void StartJump();
void StopJump();
```

```cpp
// MyCharacter.cpp
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"

void AMyCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);
    UEnhancedInputComponent* EIC = Cast<UEnhancedInputComponent>(PlayerInputComponent);
    if (!EIC) { return; }

    EIC->BindAction(MoveAction, ETriggerEvent::Triggered, this, &AMyCharacter::Move);
    EIC->BindAction(JumpAction, ETriggerEvent::Started,   this, &AMyCharacter::StartJump);
    EIC->BindAction(JumpAction, ETriggerEvent::Completed, this, &AMyCharacter::StopJump);
}

void AMyCharacter::BeginPlay()
{
    Super::BeginPlay();
    if (APlayerController* PC = Cast<APlayerController>(GetController()))
    {
        if (auto* Sub = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(
                PC->GetLocalPlayer()))
        {
            Sub->AddMappingContext(DefaultMappingContext, 0); // priority 0 = lowest
        }
    }
}
```

### Callback Signatures

`BindAction` accepts four delegate signatures:

```cpp
// No params — press/release without value needed
void AMyCharacter::StartJump() { Jump(); }

// FInputActionValue — for axis values
void AMyCharacter::Move(const FInputActionValue& Value)
{
    const FVector2D Input = Value.Get<FVector2D>();
    AddMovementInput(GetActorForwardVector(), Input.Y);
    AddMovementInput(GetActorRightVector(),   Input.X);
}

// FInputActionInstance — when elapsed/triggered time is needed
void AMyCharacter::OnChargeAttack(const FInputActionInstance& Instance)
{
    const float HeldFor = Instance.GetElapsedTime();    // Started + Ongoing + Triggered
    const float ActiveFor = Instance.GetTriggeredTime(); // Triggered only
}

// Lambda variant
EIC->BindActionValueLambda(InteractAction, ETriggerEvent::Triggered,
    [this](const FInputActionValue& Value) { TryInteract(); });
```

Storing and removing a binding:
```cpp
FEnhancedInputActionEventBinding& B =
    EIC->BindAction(DebugAction, ETriggerEvent::Started, this, &AMyCharacter::DebugToggle);
uint32 Handle = B.GetHandle();
// ...
EIC->RemoveBindingByHandle(Handle);        // remove one binding
EIC->ClearBindingsForObject(this);         // remove all bindings for an object
```

---

## Trigger Events (ETriggerEvent)

Bitmask enum from `InputTriggers.h`:

| Event | State Transition | Use for |
|---|---|---|
| `Started` | None -> Ongoing/Triggered | First frame of input; press-once actions |
| `Triggered` | *->Triggered, Triggered->Triggered | Every active frame; continuous movement |
| `Ongoing` | Ongoing->Ongoing | Held but not yet triggered (charge build-up) |
| `Canceled` | Ongoing->None | Released before trigger threshold |
| `Completed` | Triggered->None | Input released after triggering; stop continuous actions |

Note: `Completed` does not fire if any trigger on the same action reports `Ongoing` that frame.

---

## Built-in Triggers

Full parameter listings in `references/input-action-reference.md`.

| Class | Name | Behavior |
|---|---|---|
| `UInputTriggerDown` | Down | Every frame input exceeds threshold (implicit default) |
| `UInputTriggerPressed` | Pressed | Once on first actuation; holding does not repeat |
| `UInputTriggerReleased` | Released | Once when input drops below threshold after actuation |
| `UInputTriggerHold` | Hold | After `HoldTimeThreshold` s; `bIsOneShot=false` repeats every frame |
| `UInputTriggerHoldAndRelease` | Hold And Release | On release after holding `HoldTimeThreshold` s |
| `UInputTriggerTap` | Tap | Released within `TapReleaseTimeThreshold` s |
| `UInputTriggerRepeatedTap` | Repeated Tap | N taps within `RepeatDelay` (`NumberOfTapsWhichTriggerRepeat=2` for double-tap) |
| `UInputTriggerPulse` | Pulse | Repeatedly at `Interval` s while held; optional `TriggerLimit` |
| `UInputTriggerChordAction` | Chorded Action | Only fires while `ChordAction` is active (Implicit type; auto-blocks solo key) |
| `UInputTriggerCombo` | Combo (Beta) | All `ComboActions` completed in order within `TimeToPressKey` windows |

Trigger type rules for multi-trigger evaluation: `Explicit` (default, at least one must fire), `Implicit` (all must fire), `Blocker` (blocks everything if active).

---

## Built-in Modifiers

Applied in array order. Mapping-level modifiers run before action-level modifiers.

| Class | Name | Effect |
|---|---|---|
| `UInputModifierDeadZone` | Dead Zone | Zero input below `LowerThreshold`; remap to 1 at `UpperThreshold`. Types: Axial, Radial, UnscaledRadial |
| `UInputModifierScalar` | Scalar | Multiply per axis by `FVector Scalar` |
| `UInputModifierScaleByDeltaTime` | Scale By Delta Time | Multiply by frame DeltaTime |
| `UInputModifierNegate` | Negate | Invert selected axes (`bX`, `bY`, `bZ`) |
| `UInputModifierSwizzleAxis` | Swizzle Input Axis Values | Reorder axes; `YXZ` (default) swaps X/Y — maps 1D key onto Y of Axis2D action |
| `UInputModifierSmooth` | Smooth | Rolling average over recent samples |
| `UInputModifierSmoothDelta` | Smooth Delta | Smoothed normalized delta; configurable interpolation (`Lerp`, `Interp_To`, ease curves) |
| `UInputModifierResponseCurveExponential` | Response Curve - Exponential | `sign(x)*|x|^CurveExponent` per axis |
| `UInputModifierResponseCurveUser` | Response Curve - User Defined | Separate `UCurveFloat` per axis |
| `UInputModifierFOVScaling` | FOV Scaling | Scale by camera FOV for consistent angular speed across zoom levels |
| `UInputModifierToWorldSpace` | To World Space | 2D axis -> world space (up/down = world X, left/right = world Y) |

**WASD -> Axis2D recipe** (`AccumulationBehavior = Cumulative`):
- `W`: `SwizzleAxis(YXZ)` → Y=+1
- `S`: `SwizzleAxis(YXZ)` + `Negate(bY)` → Y=-1
- `D`: none → X=+1
- `A`: `Negate(bX)` → X=-1

**Gamepad stick**: `DeadZone(Radial, LowerThreshold=0.2)` per stick mapping.

**Mouse look**: `[Scalar(0.4,0.4,1), Smooth, FOVScaling]` per mapping.

---

## Mapping Context Priority

```cpp
// Higher integer = higher priority; wins key conflicts
Subsystem->AddMappingContext(GameplayIMC, 0);
Subsystem->AddMappingContext(VehicleIMC,  1);

// FModifyContextOptions — prevent ghost inputs on switch
FModifyContextOptions Opts;
Opts.bIgnoreAllPressedKeysUntilRelease = true;
Subsystem->AddMappingContext(UIIMC, 2, Opts);

// Remove on mode exit
Subsystem->RemoveMappingContext(VehicleIMC);
```

When `bConsumeInput = true` on a `UInputAction` (the default), a higher-priority context that maps the same physical key will consume it, blocking all lower-priority bindings to that key from firing. This is intentional: use priority layering and `bConsumeInput` together to prevent input conflicts between modes (e.g., a vehicle context consuming Spacebar so the character's Jump action never fires while driving).

### Split-Screen / Multiple Local Players

In split-screen, each local player has their own `UEnhancedInputLocalPlayerSubsystem`. Mapping contexts are per-player — adding a context to one player's subsystem does not affect others. To target a specific player, retrieve their subsystem directly from their `ULocalPlayer`:

```cpp
// Access subsystem for a specific local player (e.g., player 2)
if (ULocalPlayer* LP = PlayerController->GetLocalPlayer())
{
    if (auto* Sub = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(LP))
    {
        Sub->AddMappingContext(PlayerTwoIMC, 0);
    }
}
```

---

## Custom Triggers

Subclass `UInputTrigger`; override `UpdateState_Implementation` returning `ETriggerState::None / Ongoing / Triggered`:

```cpp
UCLASS(EditInlineNew, meta=(DisplayName="Double Click"))
class MYGAME_API UDoubleClickTrigger : public UInputTrigger
{
    GENERATED_BODY()
public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Trigger Settings")
    float DoubleClickThreshold = 0.3f;
protected:
    virtual ETriggerType GetTriggerType_Implementation() const override
        { return ETriggerType::Explicit; }
    virtual ETriggerState UpdateState_Implementation(
        const UEnhancedPlayerInput* PlayerInput, FInputActionValue ModifiedValue, float DeltaTime) override;
private:
    float LastPressTime = 0.f;
    bool bWasActuated = false;
};

ETriggerState UDoubleClickTrigger::UpdateState_Implementation(
    const UEnhancedPlayerInput* PlayerInput, FInputActionValue ModifiedValue, float DeltaTime)
{
    const bool bActuated = IsActuated(ModifiedValue); // helper: magnitude >= ActuationThreshold
    const float Now = PlayerInput->GetWorld()->GetTimeSeconds();
    if (bActuated && !bWasActuated)
    {
        if ((Now - LastPressTime) <= DoubleClickThreshold)
            { LastPressTime = 0.f; bWasActuated = bActuated; return ETriggerState::Triggered; }
        LastPressTime = Now;
    }
    bWasActuated = bActuated;
    return ETriggerState::None;
}
```

`UInputTriggerTimedBase` provides `HeldDuration` and `CalculateHeldDuration` for time-based triggers.

---

## Custom Modifiers

Subclass `UInputModifier`; override `ModifyRaw_Implementation`:

```cpp
UCLASS(EditInlineNew, meta=(DisplayName="Clamp Magnitude"))
class MYGAME_API UClampMagnitudeModifier : public UInputModifier
{
    GENERATED_BODY()
public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category=Settings)
    float MaxMagnitude = 1.0f;
protected:
    virtual FInputActionValue ModifyRaw_Implementation(
        const UEnhancedPlayerInput* PlayerInput, FInputActionValue CurrentValue, float DeltaTime) override
    {
        FVector V = CurrentValue.Get<FVector>();
        if (V.SizeSquared() > MaxMagnitude * MaxMagnitude)
            V = V.GetSafeNormal() * MaxMagnitude;
        return FInputActionValue(CurrentValue.GetValueType(), V);
    }
};
```

---

## Common Mistakes

- **Mapping context not added**: Add via subsystem in `BeginPlay`/after `Possess`, not in `SetupPlayerInputComponent` (called earlier on some paths).
- **Legacy binding on UEnhancedInputComponent**: `BindAction(FName,...)` and `BindAxis` are `= delete`. Compile error. Set `DefaultInputComponentClass` in `DefaultInput.ini`.
- **Triggered for a button press**: `Triggered` fires every active frame. Use `Started` for press-once, `Completed` for release.
- **Completed not firing with Ongoing**: If any trigger reports `Ongoing` that frame, `Completed` is suppressed. Use separate actions for clean press/release events.
- **No dead zone on gamepad sticks**: Sticks produce non-zero resting values. Always add `DeadZone(Radial)` per stick mapping.
- **Missing SwizzleAxis for WASD-to-2D**: Keyboard produces 1D. Without `SwizzleAxis(YXZ)` on W/S, forward/backward stays on X and is ignored by Axis2D forward movement.
- **Replicating input actions**: Input is client-local. Replicate results (movement, ability activation), not trigger events.
- **MapKey/UnmapKey at runtime for rebinding**: These are editor/config-screen helpers. Use subsystem player mappable key APIs or swap contexts instead.
- **Wrong trigger type for intent**: Using `Down` when `Hold` is needed, or `Triggered` when `Started` is needed. Match trigger type to the interaction pattern: `Started` for single press, `Triggered` for continuous, `Hold` for delayed activation.

---

## Legacy Input Migration

To migrate from the legacy input system to Enhanced Input: search for `InputComponent->BindAction` and `InputComponent->BindAxis` calls and replace each with `UEnhancedInputComponent::BindAction`. Create a `UInputAction` data asset for every old action name, choosing the appropriate `ValueType` (Boolean for buttons, Axis1D for single-axis, Axis2D for stick/WASD). Create a `UInputMappingContext` asset and add key mappings corresponding to the old `DefaultInput.ini` `ActionMappings`/`AxisMappings` entries. Set `DefaultInputComponentClass` in `DefaultInput.ini` and enable the EnhancedInput plugin.

## UI Input Mode

Without CommonUI, manage input modes manually via `APlayerController::SetInputMode()`:
```cpp
PC->SetInputMode(FInputModeUIOnly());          // cursor captured by UI, no game input
PC->SetInputMode(FInputModeGameAndUI());       // both UI and game receive input
PC->SetInputMode(FInputModeGameOnly());        // full game input, UI events suppressed
```
CommonUI automates input routing through `UCommonActivatableWidget` stacks and eliminates most manual `SetInputMode` calls — see `ue-ui-umg-slate`.

---

## Related Skills

- `ue-gameplay-framework` — PlayerController input lifecycle, `Possess`/`UnPossess`, `SetupPlayerInputComponent`
- `ue-ui-umg-slate` — `SetInputMode(FInputModeUIOnly())`/`FInputModeGameAndUI()`, cursor visibility, CommonUI `UCommonActivatableWidget` stacks
- `ue-gameplay-abilities` — binding Enhanced Input actions to GAS ability activation via input ID tags
