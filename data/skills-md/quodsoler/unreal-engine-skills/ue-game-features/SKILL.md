---
name: ue-game-features
description: "Use this skill when working with Game Feature plugins, modular gameplay, GameFeatureAction, GameFeatureData, GameFrameworkComponentManager, init state system, experience system, modular components, UPawnComponent, UControllerComponent, UGameStateComponent, UPlayerStateComponent, or Lyra-style modular architecture. See references/ for code templates and experience system patterns."
metadata:
  version: 1.0.0
---

# UE Game Features and Modular Gameplay

You are an expert in Unreal Engine's Game Features plugin system and modular gameplay architecture.

## Context Check

Read `.agents/ue-project-context.md` before proceeding. Determine:
- Whether the `GameFeatures` and `ModularGameplay` plugins are enabled
- Which actors register as component receivers (`AddReceiver`)
- Whether the project uses an init state system or experience-based loading
- Existing `UGameFeatureAction` subclasses or modular component base classes

## Information Gathering

Ask the developer:
1. Are you creating a new Game Feature plugin or extending an existing one?
2. What components or abilities should the feature inject into gameplay actors?
3. Does the feature need async loading or runtime activation/deactivation?
4. Is there an experience/game mode composition system (Lyra-style)?
5. Do components need ordered initialization across features?

---

## Game Feature Plugin Structure

A Game Feature plugin is a standard UE plugin with `Type` set to `"GameFeature"` in its `.uplugin` descriptor. This tells the engine to manage its lifecycle through the Game Features subsystem rather than loading it as a regular plugin.

### .uplugin Descriptor

```cpp
{
    "Type": "GameFeature",
    "BuiltInInitialFeatureState": "Active",  // or "Registered", "Installed"
    "Plugins": [
        { "Name": "GameFeatures", "Enabled": true },
        { "Name": "ModularGameplay", "Enabled": true }
    ]
}
```

`BuiltInInitialFeatureState` controls how far the plugin advances on startup. Use `"Active"` for always-on features, `"Registered"` for features activated by gameplay code, or `"Installed"` for downloadable content loaded on demand.

### UGameFeatureData

Each Game Feature plugin contains a `UGameFeatureData` primary data asset (extends `UPrimaryDataAsset`) that defines what the feature does:

```cpp
// From GameFeatureData.h
UPROPERTY(EditDefaultsOnly, Instanced, Category = "Game Feature | Actions")
TArray<TObjectPtr<UGameFeatureAction>> Actions;

UPROPERTY(EditAnywhere, Category = "Game Feature | Asset Manager")
TArray<FPrimaryAssetTypeInfo> PrimaryAssetTypesToScan;
```

`Actions` is the core — an instanced array of `UGameFeatureAction` subclasses that execute when the feature activates.

### Directory Convention

```
Plugins/GameFeatures/
├── ShooterCore/
│   ├── ShooterCore.uplugin          (Type: GameFeature)
│   ├── Content/
│   │   └── ShooterCore.uasset       (UGameFeatureData)
│   └── Source/ShooterCoreRuntime/
└── DeathmatchRules/
    ├── DeathmatchRules.uplugin
    └── Content/DeathmatchRules.uasset
```

---

## Plugin State Machine

Game Feature plugins transition through a well-defined state machine. Actions fire at specific transitions and runtime activation must target valid destination states.

### EGameFeaturePluginState Lifecycle

```
Uninitialized → Terminal → UnknownStatus → StatusKnown
    → Installed → Registered → Loaded → Active
```

Each major state has transition states between them (e.g., `Registering`, `Loading`, `Activating`). You target a destination state and the subsystem walks the chain.

### Destination States

| State | Description |
|-------|-------------|
| `Terminal` | Plugin removed from tracking entirely |
| `StatusKnown` | Availability confirmed (exists on disk or bundle) |
| `Installed` | Files on local storage, not yet registered |
| `Registered` | Assets registered with Asset Manager, actions notified |
| `Loaded` | Assets loaded into memory |
| `Active` | Actions fully activated, components injected |

URL protocols: `file:` for built-in disk plugins, `installbundle:` for downloadable features. Convert descriptor path to URL with `UGameFeaturesSubsystem::GetPluginURL_FileProtocol(Path)`.

---

## UGameFeatureAction

`UGameFeatureAction` (`UCLASS(MinimalAPI, DefaultToInstanced, EditInlineNew, Abstract)`) is the base class for all actions. `DefaultToInstanced` + `EditInlineNew` allow instances to be created inline within `UGameFeatureData`'s `Actions` array.

### Lifecycle Methods

```cpp
// Registration phase
virtual void OnGameFeatureRegistering();
virtual void OnGameFeatureUnregistering();

// Loading phase
virtual void OnGameFeatureLoading();
virtual void OnGameFeatureUnloading();

// Activation — primary override point
virtual void OnGameFeatureActivating(FGameFeatureActivatingContext& Context);
virtual void OnGameFeatureActivating();  // legacy no-arg fallback

// Post-activation confirmation
virtual void OnGameFeatureActivated();

// Deactivation — supports async via context
virtual void OnGameFeatureDeactivating(FGameFeatureDeactivatingContext& Context);
```

`OnGameFeatureActivating(Context)` is the primary override. The base calls the legacy no-arg version for backward compatibility.

### Async Deactivation

When deactivation requires async work, pause it via the context:

```cpp
void UMyAction::OnGameFeatureDeactivating(FGameFeatureDeactivatingContext& Context)
{
    FSimpleDelegate ResumeDelegate = Context.PauseDeactivationUntilComplete(
        TEXT("MyAction_AsyncCleanup"));
    // Start async work — MUST invoke ResumeDelegate when done or deactivation hangs
    AsyncTask(ENamedThreads::GameThread, [ResumeDelegate]()
    {
        // ... cleanup ...
        ResumeDelegate.ExecuteIfBound();
    });
}
```

See `references/game-feature-patterns.md` for complete custom action subclass templates.

---

## Built-in Actions

### UGameFeatureAction_AddComponents

`UCLASS(MinimalAPI, meta=(DisplayName="Add Components"), final)`. The most commonly used action — injects components into actors via `UGameFrameworkComponentManager`.

Configuration uses `FGameFeatureComponentEntry`:

```cpp
UPROPERTY(EditAnywhere) TSoftClassPtr<AActor> ActorClass;
UPROPERTY(EditAnywhere) TSoftClassPtr<UActorComponent> ComponentClass;
UPROPERTY(EditAnywhere) uint8 bClientComponent : 1;
UPROPERTY(EditAnywhere) uint8 bServerComponent : 1;
```

Internally stores `TSharedPtr<FComponentRequestHandle>` — RAII removes components when the handle drops (feature deactivates). Set both `bClientComponent` and `bServerComponent` for components needed everywhere, server-only for gameplay logic, client-only for cosmetic.

### Other Built-in Actions

| Action | Purpose |
|--------|---------|
| `UGameFeatureAction_AddCheats` | Register cheat manager extensions |
| `UGameFeatureAction_DataRegistry` | Register data registry sources |

---

## UGameFeaturesSubsystem

`UGameFeaturesSubsystem` (`UEngineSubsystem`) manages all Game Feature plugin lifecycles:

```cpp
UGameFeaturesSubsystem& GFS = UGameFeaturesSubsystem::Get();
```

### Runtime Activation and Deactivation

```cpp
FString PluginURL = UGameFeaturesSubsystem::GetPluginURL_FileProtocol(
    TEXT("/MyProject/Plugins/GameFeatures/MyFeature/MyFeature.uplugin"));

// Activate — callback receives const UE::GameFeatures::FResult&
GFS.LoadAndActivateGameFeaturePlugin(PluginURL,
    FGameFeaturePluginLoadComplete::CreateUObject(this, &UMyMgr::OnLoaded));

// Deactivate and unload
GFS.DeactivateGameFeaturePlugin(PluginURL);
GFS.UnloadGameFeaturePlugin(PluginURL, /*bKeepRegistered=*/ false);

// Or target a specific state:
GFS.ChangeGameFeatureTargetState(PluginURL, EGameFeatureTargetState::Registered,
    FGameFeaturePluginChangeStateComplete());
```

### Query and Observe

```cpp
bool bActive = GFS.IsGameFeaturePluginActive(PluginURL, /*bCheckForActivating=*/ false);
EGameFeaturePluginState State = GFS.GetPluginState(PluginURL);

// Global observer — implement IGameFeatureStateChangeObserver
GFS.AddObserver(MyObserver, UGameFeaturesSubsystem::EObserverPluginStateUpdateMode::CurrentAndFuture);
GFS.RemoveObserver(MyObserver);
```

`IGameFeatureStateChangeObserver` provides: `OnGameFeatureRegistering(Data, PluginName, URL)`, `OnGameFeatureActivating(Data, URL)`, `OnGameFeatureDeactivating(Data, Context, URL)`.

---

## Component Injection System

`UGameFrameworkComponentManager` (`UGameInstanceSubsystem`) is the runtime engine that injects components into actors. It is a **Game Instance subsystem** — not an engine subsystem:

```cpp
UGameFrameworkComponentManager* CompMgr =
    GetGameInstance()->GetSubsystem<UGameFrameworkComponentManager>();
```

### Actor Registration (Receivers)

Actors must register as receivers to accept injected components:

```cpp
void AMyCharacter::BeginPlay()
{
    Super::BeginPlay();
    UGameFrameworkComponentManager::AddGameFrameworkComponentReceiver(this);
}
void AMyCharacter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    UGameFrameworkComponentManager::RemoveGameFrameworkComponentReceiver(this);
    Super::EndPlay(EndPlayReason);
}
```

### Component Requests (RAII)

```cpp
TSharedPtr<FComponentRequestHandle> Handle = CompMgr->AddComponentRequest(
    TSoftClassPtr<AActor>(AMyCharacter::StaticClass()),
    UMyHealthComponent::StaticClass(),
    EGameFrameworkAddComponentFlags::AddUnique);
// Handle is RAII — destroying it removes the request and cleans up injected components
```

| Flag | Value | Behavior |
|------|-------|----------|
| `None` | 0 | Default, allows duplicates |
| `AddUnique` | 1 | Skip if same class already exists |
| `AddIfNotChild` | 2 | Skip if a child class already exists |
| `UseAutoGeneratedName` | 4 | Auto-generated name instead of class name |

### Extension Handlers and Events

```cpp
TSharedPtr<FComponentRequestHandle> ExtHandle = CompMgr->AddExtensionHandler(
    TSoftClassPtr<AActor>(AMyCharacter::StaticClass()),
    FExtensionHandlerDelegate::CreateUObject(this, &UMyAction::OnExtension));

void UMyAction::OnExtension(AActor* Actor, FName EventName)
{
    if (EventName == UGameFrameworkComponentManager::NAME_GameActorReady)
    { /* Actor fully initialized */ }
}
```

Standard event names: `NAME_ReceiverAdded`, `NAME_ReceiverRemoved`, `NAME_ExtensionAdded`, `NAME_ExtensionRemoved`, `NAME_GameActorReady`. Send custom events with `CompMgr->SendExtensionEvent(Actor, FName("MyEvent"))`.

---

## Init State System

The init state system solves ordered initialization across independently-loaded features. Without it, Component A might read from Component B before B exists — a common problem in modular architectures.

### Registering Init States

Define project-wide init states as `FGameplayTag` values in a fixed order:

```cpp
CompMgr->RegisterInitState(TAG_InitState_Spawning, false, FGameplayTag());
CompMgr->RegisterInitState(TAG_InitState_DataAvailable, false, TAG_InitState_Spawning);
CompMgr->RegisterInitState(TAG_InitState_DataInitialized, false, TAG_InitState_DataAvailable);
CompMgr->RegisterInitState(TAG_InitState_GameplayReady, false, TAG_InitState_DataInitialized);
```

### Changing and Observing Init State

```cpp
// Advance a feature's state
bool bChanged = CompMgr->ChangeFeatureInitState(
    MyActor, FName("MyComponent"), this, TAG_InitState_DataAvailable);

// Wait for another feature to reach a state
FDelegateHandle DH = CompMgr->RegisterAndCallForActorInitState(
    MyActor, FName("OtherComp"), TAG_InitState_DataInitialized,
    FActorInitStateChangedDelegate::CreateUObject(this, &UMyComp::OnOtherReady),
    /*bCallImmediately=*/ true);

// Check if all features reached a state
bool bAllReady = CompMgr->HaveAllFeaturesReachedInitState(
    MyActor, TAG_InitState_GameplayReady, /*ExcludingFeature=*/ NAME_None);
```

### IGameFrameworkInitStateInterface

Implement on components for structured init state progression:

```cpp
UCLASS()
class UMyModularComponent : public UPawnComponent,
    public IGameFrameworkInitStateInterface
{
    GENERATED_BODY()
public:
    virtual FName GetFeatureName() const override { return TEXT("MyFeature"); }
    virtual bool CanChangeInitState(UGameFrameworkComponentManager* Manager,
        FGameplayTag CurrentState, FGameplayTag DesiredState) const override;
    virtual void HandleChangeInitState(UGameFrameworkComponentManager* Manager,
        FGameplayTag CurrentState, FGameplayTag DesiredState) override;
    virtual void CheckDefaultInitialization() override;

    virtual void BeginPlay() override
    {
        Super::BeginPlay();
        RegisterInitStateFeature();
    }
    virtual void EndPlay(const EEndPlayReason::Type Reason) override
    {
        UnregisterInitStateFeature();
        Super::EndPlay(Reason);
    }
};
```

`ContinueInitStateChain(TArray<FGameplayTag>{State1, State2, State3})` attempts to advance through a sequence of states. Use this in `CheckDefaultInitialization` to auto-advance as far as possible.

---

## Modular Component Hierarchy

The `ModularGameplay` plugin provides typed base components for gameplay framework actors:

| Base Class | Parent | Typed Accessor |
|------------|--------|----------------|
| `UGameFrameworkComponent` | `UActorComponent` | None (generic base) |
| `UPawnComponent` | `UGameFrameworkComponent` | `GetPawn<T>()`, `GetPawnChecked<T>()` |
| `UControllerComponent` | `UGameFrameworkComponent` | `GetController<T>()`, `GetControllerChecked<T>()` |
| `UGameStateComponent` | `UGameFrameworkComponent` | `GetGameState<T>()`, `GetGameStateChecked<T>()` |
| `UPlayerStateComponent` | `UGameFrameworkComponent` | `GetPlayerState<T>()`, `GetPlayerStateChecked<T>()` |

Use these instead of raw `UActorComponent` for type-safe owner access and init state integration.

---

## Experience System Pattern

The experience system (pioneered by Lyra) composes game modes from Game Feature plugins at runtime. Instead of a monolithic GameMode, lightweight experience data assets list which features to activate.

### Core Flow

```
GameMode::InitGame()
  → Load UExperienceDefinition (from map or URL options)
    → For each feature: LoadAndActivateGameFeaturePlugin()
    → All loaded → OnExperienceLoaded broadcast
      → Components initialize, gameplay begins
```

A `UExperienceManagerComponent` on `AGameStateBase` orchestrates loading. Systems bind to its `OnExperienceLoaded` delegate rather than assuming features are available at `BeginPlay`.

See `references/experience-system.md` for the full pattern with code templates.

---

## Project Policies

`UGameFeaturesProjectPolicies` controls feature loading behavior. Override `IsPluginAllowed(PluginURL, OutReason)` to filter plugins, `GetGameFeatureLoadingMode(bLoadClientData, bLoadServerData)` for network filtering, and `InitGameFeatureManager()`/`ShutdownGameFeatureManager()` for custom lifecycle. Register via `DefaultGame.ini` under `GameFeaturesSubsystemSettings`.

See `references/game-feature-patterns.md` for the full policies subclass template.

---

## Common Mistakes

**Missing receiver registration:**
```cpp
// WRONG — components never injected, no error logged
void AMyCharacter::BeginPlay() { Super::BeginPlay(); }
// RIGHT
void AMyCharacter::BeginPlay()
{
    Super::BeginPlay();
    UGameFrameworkComponentManager::AddGameFrameworkComponentReceiver(this);
}
```

**Leaking FComponentRequestHandle:**
```cpp
// WRONG — handle destroyed immediately, component removed next frame
CompMgr->AddComponentRequest(ActorClass, CompClass, Flags);
// RIGHT — store for lifetime of injection
RequestHandle = CompMgr->AddComponentRequest(ActorClass, CompClass, Flags);
```

**Using BeginPlay for cross-component init:**
```cpp
// WRONG — modular components may not exist yet
void UMyComp::BeginPlay() { GetOwner()->FindComponentByClass<UOther>()->Configure(); }
// RIGHT — use init state system to wait for dependencies
void UMyComp::HandleChangeInitState(/*...*/, FGameplayTag DesiredState)
{
    if (DesiredState == TAG_InitState_DataInitialized)
        GetOwner()->FindComponentByClass<UOther>()->Configure();
}
```

**Forgetting PauseDeactivationUntilComplete delegate:** If you call `PauseDeactivationUntilComplete` but never invoke the returned delegate, plugin deactivation hangs indefinitely. Always invoke it, even on error paths.

**Wrong subsystem type for ComponentManager:**
```cpp
// WRONG — NOT an engine subsystem
GEngine->GetEngineSubsystem<UGameFrameworkComponentManager>();
// RIGHT — UGameInstanceSubsystem
GetGameInstance()->GetSubsystem<UGameFrameworkComponentManager>();
```

---

## Related Skills

- `ue-gameplay-framework` — GameMode, GameState, PlayerController, PlayerState lifecycle
- `ue-actor-component-architecture` — Component creation, attachment, tick management
- `ue-gameplay-abilities` — GAS integration with modular components
- `ue-data-assets-tables` — Primary data assets, Asset Manager scanning
- `ue-module-build-system` — Plugin structure, Build.cs dependencies
- `ue-world-level-streaming` — Level streaming, seamless travel interactions
