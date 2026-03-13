---
name: ue-world-level-streaming
description: "Use this skill when working with World Partition, level streaming, level travel, OpenLevel, ServerTravel, data layer, world subsystem, level instance, sub-level, seamless travel, open world, or HLOD. See references/streaming-patterns.md for configuration patterns by game type."
metadata:
  version: 1.0.0
---

# UE World & Level Streaming

You are an expert in Unreal Engine's world management and level streaming systems.

---

## Context

Read `.agents/ue-project-context.md` before advising. Pay attention to:
- **Engine version** — World Partition is UE5 only; sub-level streaming works in both UE4 and UE5.
- **Build targets** — Dedicated server has no rendering-driven streaming; streaming must be server-safe.
- **World size** — Determines whether World Partition or manual sub-level streaming is appropriate.
- **Multiplayer** — Seamless travel requirements and per-player streaming radius.

---

## Information to Gather

Before recommending a streaming approach, confirm:

1. **World size and type**: Is this an open world (World Partition), a set of discrete levels, or a hub-and-spoke map?
2. **Multiplayer**: Are you running a dedicated server? Are per-player streaming radii needed?
3. **Streaming control**: Does gameplay code need to control load/unload explicitly, or should proximity drive it?
4. **Level travel**: Non-seamless (lobby flows), seamless (multiplayer round transitions), or no travel?
5. **Persistent data**: What must survive a level transition — player state, inventory, session state?

---

## World Partition (UE5)

### Enabling World Partition

Enable via the Level menu: **World -> World Partition -> Convert Level**. Once enabled, all actors in the level are managed by World Partition's grid. The level can no longer have traditional sub-levels. Use **One File Per Actor (OFPA)** for collaborative editing: each actor is saved as its own `.uasset` under `__ExternalActors__`.

### Runtime Data Layers

Data layers replace the old sub-level toggle pattern. A runtime data layer can be loaded/unloaded at runtime without traveling to a new map.

```cpp
// MyGameMode.cpp
#include "WorldPartition/DataLayer/DataLayerManager.h"

void AMyGameMode::ActivateDungeonDataLayer()
{
    UDataLayerManager* DLMgr = UDataLayerManager::GetDataLayerManager(GetWorld());
    if (!DLMgr) return;

    // Get by asset reference (set up in editor as a UDataLayerAsset)
    UDataLayerAsset* DungeonLayer = DungeonDataLayerAsset.LoadSynchronous();
    DLMgr->SetDataLayerRuntimeState(DungeonLayer, EDataLayerRuntimeState::Activated);
}

void AMyGameMode::DeactivateDungeonDataLayer()
{
    UDataLayerManager* DLMgr = UDataLayerManager::GetDataLayerManager(GetWorld());
    if (!DLMgr) return;

    UDataLayerAsset* DungeonLayer = DungeonDataLayerAsset.LoadSynchronous();
    DLMgr->SetDataLayerRuntimeState(DungeonLayer, EDataLayerRuntimeState::Unloaded);
}
```

**Data layer states:**
- `Unloaded` — not loaded, not visible.
- `Loaded` — loaded into memory, not visible (pre-warming).
- `Activated` — loaded and visible (fully active).

### Streaming Sources

Each player controller is a streaming source by default. For custom sources (cinematic cameras, AI directors), implement `IWorldPartitionStreamingSourceProvider`.

### HLOD

HLOD provides distant merged-mesh representations of World Partition cells. Configure HLOD layers in the World Partition editor; build before shipping via **Build -> Build World Partition HLODs**. Without HLOD, content beyond the streaming radius is simply absent.

### Converting Sub-Levels to World Partition

Use **Tools -> World Partition -> Convert Level**. Actors migrate into the persistent level under WP management. Audit cross-level references beforehand — hard references to converted actors become invalid.

### World Partition and Multiplayer

In a multiplayer session, each player controller acts as a streaming source with a configurable radius. The server streams based on server-side sources; clients receive visibility updates via `AServerStreamingLevelsVisibility`. On dedicated servers, rendering-based streaming does not apply — streaming is driven by server-side sources only.

Streaming radius is configured per-partition in the World Partition editor UI (`LoadingRange` on `URuntimePartition`), not via ini.

---

## Level Streaming (Manual Sub-Levels)

### ULevelStreaming State Machine

From `LevelStreaming.h`, the full state sequence is:

```
Removed -> Unloaded -> Loading -> LoadedNotVisible -> MakingVisible -> LoadedVisible -> MakingInvisible -> LoadedNotVisible
                                      |
                                 FailedToLoad   (check logs; level asset missing or corrupt)
```

Query state with:

```cpp
ULevelStreaming* StreamingLevel = /* ... */;
ELevelStreamingState State = StreamingLevel->GetLevelStreamingState();

switch (State)
{
    case ELevelStreamingState::Unloaded:         /* not in memory */ break;
    case ELevelStreamingState::Loading:          /* async load in progress */ break;
    case ELevelStreamingState::LoadedNotVisible: /* in memory, not rendered */ break;
    case ELevelStreamingState::MakingVisible:    /* adding to world */ break;
    case ELevelStreamingState::LoadedVisible:    /* fully active */ break;
    case ELevelStreamingState::MakingInvisible:  /* removing from rendering */ break;
    case ELevelStreamingState::FailedToLoad:     /* check logs */ break;
}
```

### UGameplayStatics: LoadStreamLevel / UnloadStreamLevel

For Blueprint-friendly async streaming with latent actions (from `GameplayStatics.h`):

```cpp
// MyActor.cpp — async load using FLatentActionInfo
#include "Kismet/GameplayStatics.h"

void AMyActor::StreamInRoom(FName LevelName)
{
    FLatentActionInfo LatentInfo;
    LatentInfo.CallbackTarget = this;
    LatentInfo.ExecutionFunction = FName("OnRoomLoaded");
    LatentInfo.Linkage = 0;
    LatentInfo.UUID = GetUniqueID();

    UGameplayStatics::LoadStreamLevel(
        this,           // WorldContextObject
        LevelName,      // e.g., FName("Room_01")
        true,           // bMakeVisibleAfterLoad
        false,          // bShouldBlockOnLoad — keep false for async
        LatentInfo
    );
}

UFUNCTION()
void AMyActor::OnRoomLoaded()
{
    // Room is now loaded and visible
}

void AMyActor::StreamOutRoom(FName LevelName)
{
    FLatentActionInfo LatentInfo;
    LatentInfo.CallbackTarget = this;
    LatentInfo.ExecutionFunction = FName("OnRoomUnloaded");
    LatentInfo.Linkage = 0;
    LatentInfo.UUID = GetUniqueID() + 1;

    UGameplayStatics::UnloadStreamLevel(
        this,
        LevelName,
        LatentInfo,
        false // bShouldBlockOnUnload
    );
}
```

For soft object pointers (preferred for packaging safety), use `LoadStreamLevelBySoftObjectPtr` with the same arguments.

### ULevelStreamingDynamic: Runtime Level Instances

Use `ULevelStreamingDynamic::LoadLevelInstance` to load the same level package multiple times at different transforms — for procedural dungeons, modular buildings, or instanced rooms (from `LevelStreamingDynamic.h`):

```cpp
#include "Engine/LevelStreamingDynamic.h"

void AMyDungeonGenerator::SpawnRoom(FVector Location, FRotator Rotation)
{
    bool bSuccess = false;
    ULevelStreamingDynamic* StreamingLevel = ULevelStreamingDynamic::LoadLevelInstance(
        this,                              // WorldContextObject
        TEXT("/Game/Levels/Room_Corridor"), // LongPackageName — full path
        Location,
        Rotation,
        bSuccess
    );

    if (bSuccess && StreamingLevel)
    {
        // Bind to delegate to know when visible
        StreamingLevel->OnLevelShown.AddDynamic(this, &AMyDungeonGenerator::OnRoomShown);
        StreamingLevel->OnLevelHidden.AddDynamic(this, &AMyDungeonGenerator::OnRoomHidden);

        LoadedRooms.Add(StreamingLevel);
    }
}

void AMyDungeonGenerator::UnloadRoom(ULevelStreamingDynamic* StreamingLevel)
{
    if (StreamingLevel)
    {
        StreamingLevel->SetShouldBeLoaded(false);
        StreamingLevel->SetShouldBeVisible(false);
        StreamingLevel->SetIsRequestingUnloadAndRemoval(true);
    }
}
```

For networking: use `OptionalLevelNameOverride` to give all clients and server the same package name for a given instance. Without this, names are auto-generated uniquely per process and will not match across connections.

```cpp
ULevelStreamingDynamic::FLoadLevelInstanceParams Params(
    GetWorld(),
    TEXT("/Game/Levels/Room_Corridor"),
    FTransform(Rotation, Location)
);
Params.OptionalLevelNameOverride = &InstanceName; // FString, same on server and clients
Params.bInitiallyVisible = true;

bool bSuccess = false;
ULevelStreamingDynamic* Level = ULevelStreamingDynamic::LoadLevelInstance(Params, bSuccess);
```

### OnLevelShown / OnLevelHidden Delegates

From `LevelStreaming.h` — four `BlueprintAssignable` delegates: `OnLevelLoaded`, `OnLevelUnloaded`, `OnLevelShown`, `OnLevelHidden`. Bind with `AddDynamic`:

```cpp
StreamingLevel->OnLevelShown.AddDynamic(this, &UMyManager::HandleLevelShown);
StreamingLevel->OnLevelLoaded.AddDynamic(this, &UMyManager::HandleLevelLoaded);
```

### Streaming Volumes

`ALevelStreamingVolume` automatically controls sub-level loading when the player camera is inside or outside the volume. From `LevelStreamingVolume.h`:

```cpp
// EStreamingVolumeUsage — set on the volume in editor
SVB_Loading                 // load but do not make visible
SVB_LoadingAndVisibility    // load and make visible (most common)
SVB_VisibilityBlockingOnLoad // force blocking load when entering
SVB_BlockingOnLoad          // block load of associated levels
SVB_LoadingNotVisible       // load, keep invisible (pre-warm)
```

Volumes are assigned to a sub-level via its `EditorStreamingVolumes` array. Disable volume-driven streaming for a level with `ULevelStreaming::bDisableDistanceStreaming = true` when you want code-only control.

### Manual Visibility Control

```cpp
// Get streaming level reference from world
const TArray<ULevelStreaming*>& Levels = GetWorld()->GetStreamingLevels();
for (ULevelStreaming* Level : Levels)
{
    if (Level->GetWorldAssetPackageFName() == FName("/Game/Levels/MySubLevel"))
    {
        Level->SetShouldBeLoaded(true);
        Level->SetShouldBeVisible(true);
        break;
    }
}
```

Force flush all streaming (blocks until complete — use sparingly):
```cpp
UGameplayStatics::FlushLevelStreaming(this);
```

---

## Level Instances

`ALevelInstance` places a level as a reusable chunk in the editor. Actors inside are editable as a unit. For runtime instancing, see `ULevelStreamingDynamic` above.

**Packed Level Actors** merge instance meshes into a single static mesh for performance. Enable via right-click on Level Instance → **Pack Level Actor**.

**Per-instance property overrides (UE5.1+):** Each placed `ALevelInstance` can override individual actor properties (materials, gameplay values) without modifying the source level. Configure overrides in the Details panel; overridden values bake into packed level data at cook time.

---

## Level Travel

### Non-Seamless: UGameplayStatics::OpenLevel

Destroys the current world and loads a new one; all clients disconnect. From `GameplayStatics.h`:

```cpp
UGameplayStatics::OpenLevel(this, FName("/Game/Maps/MainMenu"), true);
UGameplayStatics::OpenLevel(this, FName("/Game/Maps/GameLevel"), true, TEXT("?Difficulty=Hard"));
UGameplayStatics::OpenLevelBySoftObjectPtr(this, GameLevelAsset, true); // packaging-safe
```

### Server Travel (Multiplayer, Non-Seamless)

Initiated on the server; all connected clients follow (`World.h`):

```cpp
GetWorld()->ServerTravel(TEXT("/Game/Maps/Level02?listen"), /*bAbsolute=*/false);
```

### Seamless Travel

Seamless travel loads the destination map in the background via a transition (midpoint) map. Clients stay connected. From `World.h`:

```cpp
void UWorld::SeamlessTravel(const FString& InURL, bool bAbsolute);
bool UWorld::IsInSeamlessTravel() const;
void UWorld::SetSeamlessTravelMidpointPause(bool bNowPaused);
```

**Setup requirements:**

1. Set `bUseSeamlessTravel = true` on `AGameModeBase`:

```cpp
// bUseSeamlessTravel is already declared in AGameModeBase — do NOT redeclare it.
// Just set it in the constructor:

// MyGameMode.cpp constructor
bUseSeamlessTravel = true;
```

2. Set a transition map in `DefaultEngine.ini`:

```ini
[/Script/Engine.GameMapsSettings]
TransitionMap=/Game/Maps/Transition
```

3. Override `GetSeamlessTravelActorList` to control which actors persist:

```cpp
// GameMode — called on server side during transition
void AMyGameMode::GetSeamlessTravelActorList(bool bToTransition, TArray<AActor*>& ActorList)
{
    Super::GetSeamlessTravelActorList(bToTransition, ActorList);

    if (!bToTransition)
    {
        // bToTransition=false means we're moving TO the destination
        // Add actors that should survive (e.g., GameState, custom managers)
        ActorList.Add(MyPersistentManager);
    }
}

// GameMode — called after destination map is loaded
void AMyGameMode::PostSeamlessTravel()
{
    Super::PostSeamlessTravel();
    // Re-initialize any post-travel systems
}

// GameMode — handle re-possessing players after travel
void AMyGameMode::HandleSeamlessTravelPlayer(AController*& C)
{
    Super::HandleSeamlessTravelPlayer(C);
    // Restore player-specific state here
}
```

4. Trigger on server:

```cpp
// From GameMode, server-only
GetWorld()->ServerTravel(TEXT("/Game/Maps/Level02?listen"));
// Seamless travel is automatic because bUseSeamlessTravel is true
```

**Travel sequence:** current world -> transition map -> destination world. Use `SetSeamlessTravelMidpointPause(true)` to pause at midpoint for pre-loading.

### Client Travel

For client-initiated travel (join server, change options), call `APlayerController::ClientTravel(URL, ETravelType::TRAVEL_Absolute)` from the player controller.

---

## World Subsystems

`UWorldSubsystem` (from `Subsystems/WorldSubsystem.h`) is auto-instantiated once per `UWorld`. It is destroyed when the world is destroyed — including on level travel. It is the correct place for per-world singleton logic: streaming managers, zone trackers, world-state caches.

```cpp
// MyStreamingManager.h
UCLASS()
class MYGAME_API UMyStreamingManager : public UWorldSubsystem
{
    GENERATED_BODY()
public:
    virtual void PostInitialize() override;                          // after all subsystems init
    virtual void OnWorldBeginPlay(UWorld& InWorld) override;         // after all BeginPlay
    virtual void PreDeinitialize() override;                         // cleanup hook
    virtual bool ShouldCreateSubsystem(UObject* Outer) const override; // filter world type

    void RequestLoadZone(FName ZoneName);
    void RequestUnloadZone(FName ZoneName);
private:
    TMap<FName, TWeakObjectPtr<ULevelStreaming>> ActiveZones;
};
```

Access from anywhere with a world context:

```cpp
UMyStreamingManager* Manager = GetWorld()->GetSubsystem<UMyStreamingManager>();
if (Manager)
{
    Manager->RequestLoadZone(FName("Zone_A"));
}
```

### UTickableWorldSubsystem

For per-frame updates (distance checks, zone detection). Inherit from `UTickableWorldSubsystem`. Must call `Super::Initialize` and `Super::Deinitialize` to enable/disable ticking. Implement `GetStatId` returning a `RETURN_QUICK_DECLARE_CYCLE_STAT`.

---

## Persistent Data Across Level Transitions

| Mechanism | Lifetime | Use Case |
|---|---|---|
| `UGameInstance` | Entire application session | Cross-level player state, session config |
| `UGameInstanceSubsystem` | Entire application session | Services that outlive any world |
| Seamless travel actor list | Transition only | Actors that physically cross (GameState, managers) |
| `USaveGame` + `SaveGameToSlot` | Disk-persistent | Long-term saves, progression |
| `UWorldSubsystem` | Per world | World-scoped cache; push data to `UGameInstance` in `Deinitialize()` before travel clears it |

### GameInstance Pattern

Store cross-level data in `UGameInstance` properties (survives all level travel). Access from anywhere with a world context:

```cpp
UMyGameInstance* GI = GetGameInstance<UMyGameInstance>();
if (GI) GI->PlayerScore += 100;
```

---

## Common Mistakes and Anti-Patterns

**Loading everything at once.** Setting `bShouldBlockOnLoad = true` on many sub-levels causes hitches. Use async loading and the latent action pattern. Only block on load when the game is behind a loading screen.

**Streaming volume gaps.** Overlapping volumes cause spurious unload/reload cycles. Use `MinTimeBetweenVolumeUnloadRequests` on the streaming level to add a cooldown and prevent flickering.

**Broken seamless travel in multiplayer.** If `bUseSeamlessTravel` is true but no transition map is set, seamless travel silently falls back to non-seamless. Always set `TransitionMap` in `DefaultEngine.ini`.

**Cross-level hard references.** Hard object references (`UPROPERTY() UObject*`) between actors in different streaming levels cause the entire referenced level to stay loaded. Always use `TSoftObjectPtr` or `TSoftClassPtr` across level boundaries.

**Dynamic streaming level names not matching server and client.** When using `ULevelStreamingDynamic::LoadLevelInstance`, each process generates a unique name. In multiplayer, supply `OptionalLevelNameOverride` with the same name on server and all clients.

**World Partition on dedicated server.** The server does not use rendering-driven streaming. Streaming sources must be explicitly added server-side (e.g., player positions) or World Partition will not stream in actors correctly on the server.

**Modifying `StreamingLevels` directly.** Do not add to `UWorld::StreamingLevels` directly. Use `AddStreamingLevels`, `AddUniqueStreamingLevels`, and `RemoveStreamingLevels` (from `World.h`) which handle internal bookkeeping and `StreamingLevelsToConsider`.

**Forgetting to call `Super::Initialize` / `Super::Deinitialize` in `UTickableWorldSubsystem`.** These calls enable and disable ticking respectively. Skipping them results in a subsystem that never ticks or never stops ticking.

---

## Quick Reference: Key APIs

| API | Header | Notes |
|---|---|---|
| `UGameplayStatics::LoadStreamLevel` | `Kismet/GameplayStatics.h` | Async latent load of named sub-level |
| `UGameplayStatics::UnloadStreamLevel` | `Kismet/GameplayStatics.h` | Async latent unload |
| `UGameplayStatics::FlushLevelStreaming` | `Kismet/GameplayStatics.h` | Blocking flush — use behind loading screens |
| `UGameplayStatics::OpenLevel` | `Kismet/GameplayStatics.h` | Non-seamless level travel |
| `ULevelStreamingDynamic::LoadLevelInstance` | `Engine/LevelStreamingDynamic.h` | Runtime level instancing |
| `ULevelStreaming::GetLevelStreamingState` | `Engine/LevelStreaming.h` | Query current stream state |
| `ULevelStreaming::SetShouldBeLoaded` | `Engine/LevelStreaming.h` | Drive load state |
| `ULevelStreaming::SetShouldBeVisible` | `Engine/LevelStreaming.h` | Drive visibility |
| `ULevelStreaming::SetIsRequestingUnloadAndRemoval` | `Engine/LevelStreaming.h` | Remove level from world |
| `UWorld::ServerTravel` | `Engine/World.h` | Multiplayer level transition |
| `UWorld::SeamlessTravel` | `Engine/World.h` | Background seamless transition |
| `UWorld::GetStreamingLevels` | `Engine/World.h` | Iterate all streaming levels |
| `UDataLayerManager::SetDataLayerRuntimeState` | `WorldPartition/DataLayer/DataLayerManager.h` | World Partition data layer control (use `UDataLayerManager::GetDataLayerManager(World)`) |
| `UWorldSubsystem::OnWorldBeginPlay` | `Subsystems/WorldSubsystem.h` | Post-BeginPlay init hook |
| `AGameModeBase::GetSeamlessTravelActorList` | `GameFramework/GameModeBase.h` | Control actor persistence |

---

## Related Skills

- `ue-gameplay-framework` — GameMode travel callbacks, `PostSeamlessTravel`, actor persistence rules.
- `ue-data-assets-tables` — async asset loading patterns that complement level streaming.
- `ue-networking-replication` — net visibility transactions, server streaming authority.
- `ue-cpp-foundations` — subsystem patterns, `UGameInstance` lifetime.
