---
name: ue-blueprint-cpp-interop
description: "Use when exposing C++ to Blueprint or calling Blueprint from C++: UFUNCTION(BlueprintCallable), BlueprintPure, BlueprintImplementableEvent, BlueprintNativeEvent, _Implementation, UBlueprintFunctionLibrary, WorldContext, DefaultToSelf, ExpandEnumAsExecs, DeterminesOutputType, latent nodes, FPendingLatentAction, FLatentActionInfo, UBlueprintAsyncActionBase, BlueprintAssignable, UINTERFACE, Execute_, TScriptInterface, UENUM(BlueprintType), CallInEditor, FindFunction, ProcessEvent. Also use when the user mentions 'expose to Blueprint', 'custom Blueprint node', 'async Blueprint node' or 'meta specifier'. For reflection and container basics, see ue-cpp-foundations; for details customization, see ue-editor-tools."
metadata:
  version: "2.0.0"
  engine: "5.8"
---

# UE Blueprint / C++ Interop

Target engine: **UE 5.8**. APIs below are verified against the 5.8 headers; older forms are listed under "Deprecated — do not use".

This skill covers the boundary between native code and the Blueprint VM: which `UFUNCTION`/`UPROPERTY` specifiers and `meta=` keys produce which node shapes, function libraries, latent and async nodes, Blueprint-implementable interfaces, and how C++ calls back into a Blueprint graph. Everything here lives in `Core`, `CoreUObject` and `Engine` (`PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine" });`); Project Settings pages also need `DeveloperSettings`. The authority for every specifier is `Runtime/CoreUObject/Public/UObject/ObjectMacros.h` — anything not declared in its `UC`, `UI`, `UF`, `UP`, `US` or `UM` enumerations is not a specifier.

## Context

Read `.agents/ue-project-context.md` if it exists (module names, conventions, enabled plugins, GAS/networking setup). Do not stop if it is missing.

Identify the area from the request and the codebase. Ask only when two plausible readings would produce different code.

| Request is about… | Go to |
|---|---|
| Making a C++ function callable or overridable in Blueprint | [UFUNCTION Exposure](#ufunction-exposure) |
| Making data visible or editable in Blueprint, getters/setters | [UPROPERTY Exposure](#uproperty-exposure) |
| Static helpers, `WorldContext`, `DefaultToSelf` | [Function Libraries](#function-libraries) |
| A node with an exec pin that finishes later (Delay-style) | [Latent Nodes](#latent-nodes) |
| A node with several output exec pins that fire on events | [Async Action Nodes](#async-action-nodes) |
| Interfaces Blueprint can implement, `Execute_`, `TScriptInterface` | [Blueprint Interfaces](#blueprint-interfaces) |
| `UENUM`, `USTRUCT`, containers as Blueprint types | [Enums and Structs in Blueprint](#enums-and-structs-in-blueprint) |
| `BlueprintAssignable` events, binding Blueprint to a C++ delegate | [Delegates and Events](#delegates-and-events) |
| Running Blueprint logic from native code, Blueprint classes | [Calling Blueprint from Native Code](#calling-blueprint-from-native-code) |
| Subsystems, `UDeveloperSettings`, `Exec` commands | [Subsystems and Settings in Blueprint](#subsystems-and-settings-in-blueprint) |
| A button in the Details panel, editor-only actions | [Editor-Callable Functions](#editor-callable-functions) |

## UFUNCTION Exposure

| Specifier | Node shape | C++ body |
|---|---|---|
| `BlueprintCallable` | Exec pins in and out | Yours |
| `BlueprintPure` | No exec pins; implies `BlueprintCallable` | Yours, side-effect free |
| `BlueprintImplementableEvent` | Event the Blueprint implements | **None** — UHT generates the thunk |
| `BlueprintNativeEvent` | Event the Blueprint may override | `Name_Implementation` only |
| `BlueprintGetter` / `BlueprintSetter` | Hidden; reached through the property | Yours |
| `BlueprintAuthorityOnly` | Blueprint calls are skipped without network authority (direct C++ calls still run) | Yours |
| `BlueprintCosmetic` | Blueprint calls are skipped on a dedicated server (direct C++ calls still run) | Yours |
| `BlueprintInternalUseOnly` | Not offered in the palette; only generated nodes call it | Yours |
| `CallInEditor` | Button on the Details panel | Yours |
| `Exec` | Console command | Yours |

`Category="A\|B"` builds a nested palette category. The node-shaping `meta=` keys — `DisplayName`, `ToolTip`, `Keywords`, `CompactNodeTitle`, `AdvancedDisplay`, `ReturnDisplayName`, `HidePin`, `DeterminesOutputType`, `DynamicOutputParam`, `ArrayParm`, `ExpandEnumAsExecs`, `WorldContext`, `UnsafeDuringActorConstruction`, `DevelopmentOnly`, `BlueprintThreadSafe` and the rest — are tabled with header citations in [references/blueprint-meta-specifiers.md](references/blueprint-meta-specifiers.md#ufunction-meta-keys).

```cpp
// MyActor.h
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MyActor.generated.h"

UCLASS(Blueprintable)
class MYGAME_API AMyActor : public AActor
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintCallable, Category="MyGame|Combat", meta=(Keywords="damage hurt"))
    void ApplyDamage(float Amount);

    UFUNCTION(BlueprintPure, Category="MyGame|Combat", meta=(CompactNodeTitle="HP", ReturnDisplayName="Health"))
    float GetHealth() const;

    /** Blueprint supplies the whole body; C++ never defines this. */
    UFUNCTION(BlueprintImplementableEvent, Category="MyGame|Combat")
    void OnDamaged(float Amount);

    /** C++ supplies the default in OnDied_Implementation; Blueprint may override it. */
    UFUNCTION(BlueprintNativeEvent, Category="MyGame|Combat")
    void OnDied();
    virtual void OnDied_Implementation();

    UFUNCTION(BlueprintCallable, BlueprintAuthorityOnly, Category="MyGame|Combat")
    void ResetOnServer() { Health = MaxHealth; }     // Blueprint calls skipped on clients

    UFUNCTION(BlueprintCallable, BlueprintCosmetic, Category="MyGame|FX")
    void PlayHitFlash() {}                           // Blueprint calls skipped on a dedicated server

    UFUNCTION(CallInEditor, Category="MyGame|Tools")
    void SnapToGround() {}                           // button in the Details panel

private:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="MyGame|Combat", meta=(AllowPrivateAccess="true", ClampMin="0.0"))
    float Health = 100.f;

    float MaxHealth = 100.f;
};
```

```cpp
// MyActor.cpp
#include "MyActor.h"

void AMyActor::ApplyDamage(float Amount)
{
    Health = FMath::Max(0.f, Health - Amount);
    OnDamaged(Amount);                  // runs the Blueprint graph
    if (Health <= 0.f) { OnDied(); }    // runs the BP override if any, else OnDied_Implementation
}

float AMyActor::GetHealth() const { return Health; }
void AMyActor::OnDied_Implementation() {}            // the C++ default, overridable in Blueprint
```

Raise an event by its plain name (`OnDied()`), never `OnDied_Implementation()` — the plain name is the generated thunk that dispatches to Blueprint. A subclass overrides `virtual void OnDied_Implementation() override;` and chains with `Super::OnDied_Implementation();`, never `Super::OnDied();`.

### Parameters and pins

| C++ parameter | Blueprint pin |
|---|---|
| `float Amount` | Input |
| `const FVector& Base` | Input, passed by reference |
| `FVector& Out` | **Output** pin, not an input |
| `UPARAM(ref) FVector& InOut` | By-reference input that is also an output |
| `UPARAM(DisplayName="Event") FMyReadySignature Callback` | Input renamed on the node |

A bare `T&` gets the `OutParm` flag from UHT; `UPARAM(ref)` adds `ReferenceParm` so the pin stays an input. `meta=(AutoCreateRefTerm="Offset")` gives a reference input an inline literal when nothing is connected.

## UPROPERTY Exposure

| Specifier | Effect in Blueprint |
|---|---|
| `BlueprintReadWrite` | Get and Set nodes |
| `BlueprintReadOnly` | Get node only |
| `BlueprintGetter=Fn` | Get routes through `UFUNCTION(BlueprintGetter)` |
| `BlueprintSetter=Fn` | Set routes through `UFUNCTION(BlueprintSetter)`; implies `BlueprintReadWrite` |
| `BlueprintAssignable` | Bind Event node (multicast dynamic delegates only) |
| `BlueprintCallable` | Broadcast node (multicast dynamic delegates only) |
| `BlueprintAuthorityOnly` | Delegate accepts only `BlueprintAuthorityOnly` events |

`BlueprintReadWrite`/`BlueprintReadOnly` on a `private` member is a UHT **error** ("BlueprintReadWrite should not be used on private members") unless the property carries `meta=(AllowPrivateAccess="true")`. An editor-only property cannot be a Blueprint-exposed struct member. Editor `meta=` keys (`ClampMin`/`ClampMax`, `UIMin`/`UIMax`, `EditCondition`, `EditConditionHides`, `InlineEditConditionToggle`, `TitleProperty`, `ShowOnlyInnerProperties`, `MultiLine`, `GetOptions`, `AllowedClasses`, `MustImplement`, `Categories`, `Bitmask`/`BitmaskEnum`, `ExposeOnSpawn`): [references/blueprint-meta-specifiers.md](references/blueprint-meta-specifiers.md#uproperty-meta-keys).

| C++ member type | Blueprint pin |
|---|---|
| `double` / `float` | Real |
| `TObjectPtr<UStaticMesh>` | Object reference |
| `TSubclassOf<AActor>` | Class (filtered by `meta=(MustImplement=…)`, `AllowedClasses`, `BlueprintBaseOnly`) |
| `TSoftObjectPtr<T>` / `TSoftClassPtr<T>` | Soft reference; Blueprint resolves or loads on demand |
| `FInstancedStruct` | Struct pin whose concrete type is chosen in the editor |
| `TScriptInterface<IMyInteractable>` | Interface reference |
| `FMyHealthChangedSignature` (multicast dynamic) | Bind Event / Broadcast nodes via `BlueprintAssignable` |
| `FTimerHandle` | `USTRUCT(BlueprintType)` handle passed straight through |

A worked component showing `ExposeOnSpawn`, `EditCondition`/`EditConditionHides`, `InlineEditConditionToggle`, `MustImplement` and a `BlueprintGetter`/`BlueprintSetter` pair: [references/blueprint-meta-specifiers.md](references/blueprint-meta-specifiers.md#a-worked-property-example).

**Floats and doubles.** Both `float` and `double` properties show as a Blueprint *Real* pin (`UEdGraphSchema_K2` maps `FFloatProperty` and `FDoubleProperty` to `PC_Real` with sub-category `PC_Float`/`PC_Double`), and Blueprint-authored variables are doubles. Declare `double` for scalars that flow through Blueprint math so no narrowing conversion is inserted; keep `float` only where the engine type is already float.

## Function Libraries

`UBlueprintFunctionLibrary` (`Kismet/BlueprintFunctionLibrary.h`) is `UCLASS(Abstract)` and every member is `static`. `GetWorld()` returns null on its CDO, so take `const UObject* WorldContextObject`, tag it `meta=(WorldContext="WorldContextObject")` and resolve with `GEngine->GetWorldFromContextObject(WorldContextObject, EGetWorldErrorMode::LogAndReturnNull)`; `meta=(DefaultToSelf="Param")` pre-wires a pin to the calling object.

```cpp
// MyBlueprintLibrary.h
#pragma once
#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "Templates/SubclassOf.h"
#include "MyBlueprintLibrary.generated.h"

class AActor;

UENUM(BlueprintType)
enum class EMyConsumeResult : uint8
{
    Consumed,
    NotEnough
};

UCLASS()
class MYGAME_API UMyBlueprintLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()
public:
    /** WorldContextObject is hidden on the node and filled in by the graph. */
    UFUNCTION(BlueprintCallable, Category="MyGame|Utility", meta=(WorldContext="WorldContextObject"))
    static int32 CountPawns(const UObject* WorldContextObject);

    /** The return pin takes the type plugged into ActorClass, so Blueprint needs no cast. */
    UFUNCTION(BlueprintPure, Category="MyGame|Utility", meta=(DefaultToSelf="Target", DeterminesOutputType="ActorClass"))
    static AActor* FindAttachedActorOfClass(AActor* Target, TSubclassOf<AActor> ActorClass);

    /** One input enum becomes one output exec pin per enumerator. */
    UFUNCTION(BlueprintCallable, Category="MyGame|Utility", meta=(ExpandEnumAsExecs="Result"))
    static void TryConsume(int32 Available, int32 Amount, EMyConsumeResult& Result);
};
```

The matching `.cpp`: [references/blueprint-node-patterns.md](references/blueprint-node-patterns.md#function-library-implementation). `ExpandEnumAsExecs` accepts exactly one input parameter (UHT errors on a second); name `ReturnValue` to expand the return value, and use `ExpandBoolAsExecs` for a bool. Wildcard array nodes use `meta=(ArrayParm="Items", ArrayTypeDependentParams="Item")`.

## Latent Nodes

A latent node holds one exec pin pending across frames. It needs `meta=(Latent, LatentInfo="LatentInfo", WorldContext="WorldContextObject")` and a trailing `FLatentActionInfo` parameter, plus an `FPendingLatentAction` subclass registered with the world's `FLatentActionManager`. `UKismetSystemLibrary::Delay` and `FDelayAction` (`Engine/Public/DelayAction.h`) are the engine reference.

```cpp
// MyLatentLibrary.h — declaration
UFUNCTION(BlueprintCallable, Category="MyGame|Flow", meta=(Latent, LatentInfo="LatentInfo", WorldContext="WorldContextObject", Duration="1.0"))
static void WaitSeconds(const UObject* WorldContextObject, float Duration, FLatentActionInfo LatentInfo);
```

```cpp
// MyLatentLibrary.cpp — the UUID guard is mandatory
void UMyLatentLibrary::WaitSeconds(const UObject* WorldContextObject, float Duration, FLatentActionInfo LatentInfo)
{
    if (UWorld* World = GEngine->GetWorldFromContextObject(WorldContextObject, EGetWorldErrorMode::LogAndReturnNull))
    {
        FLatentActionManager& Manager = World->GetLatentActionManager();
        if (Manager.FindExistingAction<FMyWaitAction>(LatentInfo.CallbackTarget, LatentInfo.UUID) == nullptr)
        {
            Manager.AddNewAction(LatentInfo.CallbackTarget, LatentInfo.UUID, new FMyWaitAction(Duration, LatentInfo));
        }
    }
}
```

Without the `FindExistingAction` guard, re-entering the node stacks a second action on the same UUID and the exec pin fires more than once. The action subclass overrides `UpdateOperation(FLatentResponse& Response)` and finishes with `Response.FinishAndTriggerIf(bDone, ExecutionFunction, OutputLink, CallbackTarget)`, copying `ExecutionFunction`, `Linkage` and `CallbackTarget` out of the `FLatentActionInfo` in its constructor; it also overrides `NotifyObjectDestroyed()`, `NotifyActionAborted()` and, under `WITH_EDITOR`, `GetDescription() const`. `FLatentResponse` additionally offers `DoneIf(bool)` and `TriggerLink(ExecutionFunction, LinkID, CallbackTarget)` for several exit links. Complete subclass and the rest of the `FLatentActionManager` API: [references/blueprint-node-patterns.md](references/blueprint-node-patterns.md#latent-actions).

## Async Action Nodes

`UBlueprintAsyncActionBase` (`Kismet/BlueprintAsyncActionBase.h`) produces a node with one exec input and one output exec pin per `BlueprintAssignable` delegate. The static factory must carry `meta=(BlueprintInternalUseOnly="true")` so only the generated node can call it.

```cpp
// MyWaitForHealthAction.h
#pragma once
#include "CoreMinimal.h"
#include "Kismet/BlueprintAsyncActionBase.h"
#include "MyWaitForHealthAction.generated.h"

class UMyStatsComponent;

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FMyHealthThresholdSignature, double, Health);

UCLASS()
class MYGAME_API UMyWaitForHealthAction : public UBlueprintAsyncActionBase
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintCallable, Category="MyGame|Async", meta=(BlueprintInternalUseOnly="true", WorldContext="WorldContextObject", DisplayName="Wait For Health Below"))
    static UMyWaitForHealthAction* WaitForHealthBelow(UObject* WorldContextObject, UMyStatsComponent* Stats, double Threshold);

    virtual void Activate() override;

    UPROPERTY(BlueprintAssignable)
    FMyHealthThresholdSignature OnReached;      // one output exec pin

    UPROPERTY(BlueprintAssignable)
    FMyHealthThresholdSignature OnFailed;       // a second output exec pin

private:
    UFUNCTION()
    void HandleHealthChanged(double NewHealth);   // AddDynamic targets must be UFUNCTIONs

    UPROPERTY()
    TObjectPtr<UMyStatsComponent> TrackedStats;

    double ThresholdValue = 0.0;
};
```

The factory does `NewObject<UMyWaitForHealthAction>()`, stores its inputs, calls `RegisterWithGameInstance(WorldContextObject)` and returns the action; the node then binds the delegates and calls `Activate()`, where the work starts. Each completion path broadcasts once and calls `SetReadyToDestroy()`. An unregistered action lives only for the frame it was created on (`RF_StrongRefOnFrame`), so a delegate firing later finds it collected. The engine ensures when more than `bp.MaxAsyncActionCount` (default 10000) actions are alive at once.

`UCancellableAsyncAction` (`Engine/CancellableAsyncAction.h`, `UCLASS(Abstract, BlueprintType, meta=(ExposedAsyncProxy=AsyncAction))`) adds `Cancel()`, `IsActive() const` and `ShouldBroadcastDelegates() const` so the node hands the object back for later cancelling; guard every broadcast with `ShouldBroadcastDelegates()`. Full `Activate`/`Cancel` implementations: [references/blueprint-node-patterns.md](references/blueprint-node-patterns.md#async-actions).

## Blueprint Interfaces

`UINTERFACE`'s own specifiers (`UI::`) are `MinimalAPI`, `Blueprintable`, `NotBlueprintable` and `ConversionRoot` plus `meta=`; UHT's shared `BlueprintType` is also accepted, and engine interfaces use it so the interface is usable as a Blueprint variable type. Blueprint can implement `BlueprintImplementableEvent` and `BlueprintNativeEvent` members; a plain `virtual` C++ method is invisible to Blueprint.

```cpp
// MyInteractable.h
#pragma once
#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "MyInteractable.generated.h"

class AActor;

UINTERFACE(Blueprintable, BlueprintType, MinimalAPI)
class UMyInteractable : public UInterface
{
    GENERATED_BODY()
};

class MYGAME_API IMyInteractable
{
    GENERATED_BODY()
public:
    /** Blueprint-only implementations are allowed; C++ implementers write Interact_Implementation. */
    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category="MyGame|Interaction")
    bool Interact(AActor* Interactor);
    virtual bool Interact_Implementation(AActor* Interactor);

    virtual float GetInteractRange() const { return 200.f; }   // native-only: invisible to Blueprint
};
```

```cpp
// Calling an interface that may be implemented in C++ or in Blueprint
bool MyTryInteract(UObject* Target, AActor* Interactor)
{
    return Target && Target->Implements<UMyInteractable>()
        && IMyInteractable::Execute_Interact(Target, Interactor);
}
```

| Form | C++ implementers | Blueprint implementers |
|---|---|---|
| `IMyInteractable::Execute_Interact(Obj, …)` | Yes | Yes — always use this |
| `Obj->Implements<UMyInteractable>()` | Yes | Yes |
| `Obj->GetClass()->ImplementsInterface(UMyInteractable::StaticClass())` | Yes | Yes |
| `Cast<IMyInteractable>(Obj)` then a direct call | Yes | **No** — the cast returns null |
| `TScriptInterface<IMyInteractable>` member | Yes | Interface pointer is null; still call through `Execute_` |

`TScriptInterface<T>` (`UObject/ScriptInterface.h`) stores the object and the interface pointer together and is documented as useful for native interfaces only. Declare `UPROPERTY(EditAnywhere, BlueprintReadWrite) TScriptInterface<IMyInteractable> Target;` so designers get a filtered picker, and still dispatch with `Execute_`.

## Enums and Structs in Blueprint

```cpp
// MyTypes.h
#pragma once
#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "MyTypes.generated.h"

UENUM(BlueprintType)
enum class EMyWeaponState : uint8      // BlueprintType enums must be uint8-based
{
    Idle,
    Firing      UMETA(DisplayName="Firing Weapon"),
    Reloading,
    MAX         UMETA(Hidden)
};

USTRUCT(BlueprintType)
struct MYGAME_API FMyWeaponStats
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Weapon")
    double BaseDamage = 10.0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Weapon")
    TArray<FName> Tags;                // container of a Blueprint-supported type

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Weapon")
    TMap<FName, double> Modifiers;     // key and value must both be Blueprint-supported
};

USTRUCT(BlueprintType)
struct MYGAME_API FMyWeaponRow : public FTableRowBase   // data table row type
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Weapon")
    FMyWeaponStats Stats;
};
```

- `UENUM(BlueprintType)` requires `enum class : uint8`; UHT rejects any other base ("Invalid BlueprintType enum base - currently only uint8 supported"). `UMETA(DisplayName="…")` renames an enumerator and `UMETA(Hidden)` hides it from pickers.
- `USTRUCT(BlueprintType)` gives Make and Break nodes. Structs cannot hold `UFUNCTION`s — put struct helpers in a function library.
- **No nested containers.** `TArray`, `TSet` and `TMap` clear their own "can be a container key/value" capability in UHT, so `TArray<TArray<int32>>` and `TMap<FName, TArray<int32>>` do not compile. Wrap the inner container in a `USTRUCT`.
- A container is Blueprint-exposable only when its element type — and for `TMap` its key type — is itself Blueprint-supported.
- `FTableRowBase` (`Engine/DataTable.h`) is `USTRUCT(BlueprintInternalUseOnly)`; derive row structs from it and mark the derived struct `BlueprintType`. Table loading and row lookup: `ue-data-assets-tables`.
- `FInstancedStruct` (`StructUtils/InstancedStruct.h`) is `USTRUCT(BlueprintType)` and gives Blueprint a single pin whose concrete struct type is chosen in the editor; `TInstancedStruct<FMyBase>` is the typed C++ wrapper.

## Delegates and Events

Only **dynamic** delegates cross the Blueprint boundary. Declaration macros and native binding rules: `ue-cpp-foundations`.

- `UPROPERTY(BlueprintAssignable)` on a multicast dynamic delegate gives Blueprint a Bind Event node; adding `BlueprintCallable` also gives it a Broadcast node. Both are legal only on multicast dynamic delegates.
- Delegate parameters need names — they become the pin names on the event node.
- Any C++ handler bound with `AddDynamic` must be a `UFUNCTION()`; otherwise the name lookup fails at runtime and the handler never runs.
- A single dynamic delegate (`DECLARE_DYNAMIC_DELEGATE`, `DECLARE_DYNAMIC_DELEGATE_OneParam`, …) works as a `UFUNCTION` parameter, which is how async nodes take a one-shot callback: `UPARAM(DisplayName="Event") FMyReadySignature Callback`.
- Native (non-dynamic) delegates cannot be exposed at all; wrap them in a dynamic delegate or an async action.

## Calling Blueprint from Native Code

| Need | Use |
|---|---|
| A hook the designer fills in | `UFUNCTION(BlueprintImplementableEvent)`, called by its plain name |
| A hook with a C++ default | `UFUNCTION(BlueprintNativeEvent)`, called by its plain name |
| Fire an event many graphs listen to | `UPROPERTY(BlueprintAssignable)` multicast, `Broadcast(...)` |
| Call a function that exists only in a Blueprint asset | `FindFunction` + `ProcessEvent` |
| Read defaults off a Blueprint class | `TSubclassOf<T>::GetDefaultObject()`, `UClass::GetDefaultObject<T>()` |

```cpp
// The params struct must match the function's parameter list exactly, in declaration order.
struct FMyOnScoredParams
{
    int32 Points;
    FString Reason;
};

void MyNotifyScored(UObject* Target, int32 Points)
{
    if (!Target) { return; }

    if (UFunction* Func = Target->FindFunction(FName(TEXT("OnScored"))))
    {
        checkf(Func->ParmsSize == sizeof(FMyOnScoredParams), TEXT("OnScored signature changed"));
        FMyOnScoredParams Params;
        Params.Points = Points;
        Params.Reason = TEXT("Kill");
        Target->ProcessEvent(Func, &Params);
    }
}
```

`FindFunction` returns null when the Blueprint was renamed or recompiled away, so always branch on it (`FindFunctionChecked` asserts instead). Prefer a `BlueprintImplementableEvent` declaration whenever C++ owns the contract — it is type-checked at compile time.

```cpp
// SpawnClassPath is a UPROPERTY(EditDefaultsOnly) TSoftClassPtr<AMyActor> set to BP_MyThing
void MyInspectSpawnClass(const TSoftClassPtr<AMyActor>& SpawnClassPath)
{
    if (UClass* LoadedClass = SpawnClassPath.LoadSynchronous())
    {
        const AMyActor* Defaults = LoadedClass->GetDefaultObject<AMyActor>();
        const bool bIsBlueprintClass = Cast<UBlueprintGeneratedClass>(LoadedClass) != nullptr;   // UClass hides IsA (Class.h:4853)
        UE_LOG(LogMyGame, Log, TEXT("Default health %.1f, Blueprint class %d"), Defaults->GetHealth(), bIsBlueprintClass ? 1 : 0);
    }
}
```

`LoadSynchronous` blocks the game thread; for streamed loads use the Asset Manager (`ue-data-assets-tables`). `UBlueprintGeneratedClass` (`Engine/BlueprintGeneratedClass.h`) is the runtime `UClass` a compiled Blueprint produces — test for it when native and Blueprint classes must be handled differently.

## Subsystems and Settings in Blueprint

- Every `UGameInstanceSubsystem`, `UWorldSubsystem`, `ULocalPlayerSubsystem` and `UEngineSubsystem` subclass automatically gets a `Get <Subsystem>` node (`UK2Node_GetSubsystem`); its `BlueprintCallable` members then appear on that object. No extra specifier is needed. Subsystem lifetimes and native accessors: `ue-cpp-foundations`.
- `UDeveloperSettings` (`Engine/DeveloperSettings.h`, module `DeveloperSettings`) auto-registers a Project Settings page. Declare it `UCLASS(Config=Game, DefaultConfig, meta=(DisplayName="My Game"))`, mark fields `UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category=…)`, and add a `UFUNCTION(BlueprintPure)` static accessor returning `GetDefault<UMyGameSettings>()` — Blueprint has no node for `GetDefault`. `GetContainerName()`, `GetCategoryName()` and `GetSectionName()` are overridable to move the page.
- `UFUNCTION(Exec)` declares a console command; the console routes to PlayerInput, PlayerController, Pawn, HUD, GameMode, CheatManager, GameState, PlayerCameraManager and GameInstance. `meta=(DevelopmentOnly)` compiles a `BlueprintCallable` out of Shipping, as `UKismetSystemLibrary::PrintString` does.

## Editor-Callable Functions

`CallInEditor` — see `AMyActor::SnapToGround` above — is a `UFUNCTION` specifier, not a `meta=` key, and the function takes no parameters. It runs against the editor world, so guard anything that assumes PIE. Details customizations, editor utility widgets and asset actions: `ue-editor-tools`.

## Deprecated — do not use

| Do not emit | Use in 5.8 | Source |
|---|---|---|
| `meta=(HideAssetPicker)` | `meta=(HidePinAssetPicker)` | `UE_DEPRECATED(5.6)` in `UObject/ObjectMacros.h:1673` |
| `Delegate.ProcessMulticastDelegate<UObject>(Params)` | `Delegate.ProcessDelegate<UObject>(Params)` | `UE_DEPRECATED(5.8)` in `UObject/ScriptDelegates.h:1462` |
| `SomeClass->ClassDefaultObject` | `GetDefault<T>()`, `UClass::GetDefaultObject<T>()` | `UE_DEPRECATED(5.6)` in `UObject/Class.h:4045` |
| `GENERATED_UCLASS_BODY()`, `GENERATED_IINTERFACE_BODY()` | `GENERATED_BODY()` | Legacy aliases in `UObject/ObjectMacros.h:802-805` |
| `Cast<IMyInterface>(Obj)->Foo()` on a Blueprint implementer | `IMyInterface::Execute_Foo(Obj, …)` | Blueprint implementers have no `IMyInterface` pointer (`UObject/ScriptInterface.h:135`) |
| `Obj->Foo_Implementation()` to raise a `BlueprintNativeEvent` | `Obj->Foo()` | The plain name is the generated dispatch thunk (`UObject/ObjectMacros.h:997`) |
| A C++ body for a `BlueprintImplementableEvent` | Declare it and stop | UHT generates the body (`UObject/ObjectMacros.h:992`) |
| `UPROPERTY(BlueprintReadWrite)` on a private member | Add `meta=(AllowPrivateAccess="true")`, or make it protected | UHT error "BlueprintReadWrite should not be used on private members" |
| `UENUM(BlueprintType) enum class EMyState : uint32` | `enum class EMyState : uint8` | UHT error "Invalid BlueprintType enum base - currently only uint8 supported" |
| `TArray<TArray<T>>` or `TMap<K, TArray<V>>` in a `UPROPERTY` | Wrap the inner container in a `USTRUCT` | `TArray`/`TMap` clear `CanBeContainerValue`/`CanBeContainerKey` in UHT |
| `AddNewAction` without a `FindExistingAction` guard | Check `LatentInfo.UUID` first | `Engine/LatentActionManager.h:121,143` |
| `NewObject<UMyAsyncAction>()` returned without registering | `RegisterWithGameInstance(WorldContextObject)` | `Kismet/BlueprintAsyncActionBase.h:37` |

## Common Mistakes

**`BlueprintNativeEvent` without `_Implementation`, or a C++ body for a `BlueprintImplementableEvent`:** the first is an unresolved external, the second a duplicate symbol (UHT already emitted one). A native event needs `virtual void Foo_Implementation(...)` defined; an implementable event needs no definition at all.

**`BlueprintPure` with side effects:** the compiler prunes unused pure nodes and re-evaluates the rest at each consumer, so the side effect runs an unpredictable number of times. Use `BlueprintCallable`.

**A non-const reference parameter that was meant as an input:**
```cpp
static void Scale(FVector& Value, double Factor);                 // WRONG: Value becomes an output pin
static void Scale(UPARAM(ref) FVector& Value, double Factor);     // RIGHT: by-reference input
static void Scale(const FVector& Value, double Factor);           // RIGHT: plain input
```

**A library function that needs the world but declares no `WorldContext`:** `GetWorld()` returns null on a `UBlueprintFunctionLibrary` CDO. Take `const UObject* WorldContextObject`, tag it `meta=(WorldContext="WorldContextObject")` and resolve with `GEngine->GetWorldFromContextObject(WorldContextObject, EGetWorldErrorMode::LogAndReturnNull)`.

**`BlueprintReadWrite` on a private member:** a UHT error, not a warning. Add `meta=(AllowPrivateAccess="true")`.

**Nested containers in a `UPROPERTY`:** UHT rejects `TArray<TArray<T>>` and `TMap<K, TArray<V>>`. Wrap the inner container in a `USTRUCT(BlueprintType)`.

**A latent action added without the UUID guard:** re-entering the node stacks duplicate actions and the completion pin fires once per copy. Check `FindExistingAction<FMyWaitAction>(LatentInfo.CallbackTarget, LatentInfo.UUID)` first.

**An async action collected mid-flight:** an action that never calls `RegisterWithGameInstance` lives only for the frame it was created on, so a delegate firing later never reaches it. Register in the factory and call `SetReadyToDestroy()` exactly once when finished.

**`Cast<IMyInterface>(Obj)` on a Blueprint implementer:** returns null and the call is silently skipped. Test with `Obj->Implements<UMyInterface>()` and dispatch with `IMyInterface::Execute_Foo(Obj, …)`.

**A static async factory without `meta=(BlueprintInternalUseOnly="true")`:** Blueprint offers both the proxy node and a bare call to the factory, and the bare call returns an object nothing ever activates.

## Related Skills

- `ue-cpp-foundations` — `UCLASS`/`UPROPERTY`/`UFUNCTION` fundamentals, containers, delegates, subsystem lifetimes, GC
- `ue-actor-component-architecture` — Actor and component lifecycle, spawning, `BlueprintSpawnableComponent`
- `ue-gameplay-framework` — GameMode, PlayerController, damage, the classes Blueprint most often extends
- `ue-editor-tools` — details customization, editor utility widgets, asset actions, editor subsystems
- `ue-async-threading` — `AsyncTask`, `UE::Tasks`, timers and thread safety behind an async node
- `ue-data-assets-tables` — `UDataAsset`, DataTable rows, soft references and Asset Manager loading
- `ue-ui-umg-slate` — `UUserWidget` C++ bases, `BindWidget`, exposing widget data to Blueprint
