---
name: ue-data-assets-tables
description: "Use when working with DataAsset, DataTable, soft reference, hard reference, TSoftObjectPtr, async loading, Asset Manager, StreamableManager, or game data structures in Unreal Engine. See references/asset-loading-patterns.md for async loading and StreamableManager patterns. See references/data-driven-design.md for data-driven gameplay architecture. For serialization, see ue-serialization-savegames. For C++ foundations, see ue-cpp-foundations."
metadata:
  version: 1.0.0
---

# UE Data Assets and Tables

You are an expert in Unreal Engine's data management and asset loading systems.

---

## Context

Read `.agents/ue-project-context.md` for project-specific data patterns, module layout, plugin dependencies, and any custom AssetManager subclass or DataAsset conventions the project has established.

---

## Information Gathering

Before generating code or advice, ask:

1. What kind of data is being stored? (item stats, level config, ability definitions, NPC data, etc.)
2. Is this data authored by designers in spreadsheets, or configured directly in the editor?
3. What are the loading requirements — always in memory, loaded per-level, streamed on demand?
4. Is memory budget a concern? How many instances are expected?
5. Does the project already use a custom `UAssetManager` subclass?

---

## Core Framework

### DataAssets vs DataTables — Choosing the Right Tool

| Concern | DataAsset | DataTable |
|---|---|---|
| Structure | C++ class with typed UPROPERTY fields | Row struct, all rows same shape |
| Designer workflow | Editor-authored instances, picker UI | Spreadsheet import (CSV/JSON) |
| Hierarchy / inheritance | Yes, via Blueprint subclasses | No |
| Asset Manager integration | Yes (`UPrimaryDataAsset`) | Not directly |
| Bulk lookup by row name | No | Yes (`FindRow`) |
| Best for | Per-item config objects | Large flat tables (loot, dialogue, XP curves) |

---

## DataAssets

### UDataAsset — Simple Configuration Objects

`UDataAsset` (declared in `Engine/DataAsset.h`) is the base class. Assets are only loaded when directly referenced or explicitly loaded. Subclass it with typed UPROPERTY fields:

```cpp
UCLASS(BlueprintType)
class MYGAME_API UMyItemData : public UDataAsset
{
    GENERATED_BODY()
public:
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Item") FText DisplayName;
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Item") float BaseDamage = 10.f;
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Item") TSoftObjectPtr<UStaticMesh> Mesh;
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Item") TSoftClassPtr<AActor> SpawnClass;
};
```

In the editor: right-click in Content Browser > Miscellaneous > Data Asset, select `UMyItemData`.

### UPrimaryDataAsset — Asset Manager Integration

`UPrimaryDataAsset` overrides `GetPrimaryAssetId()` so the Asset Manager can track, scan, and load it. The Primary Asset Type is derived from the first native class in the hierarchy.

```cpp
// PrimaryAssetType == native class name; PrimaryAssetName == asset name.
UCLASS(BlueprintType)
class MYGAME_API UWeaponDefinition : public UPrimaryDataAsset
{
    GENERATED_BODY()
public:
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Weapon")
    FText WeaponName;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Weapon")
    float FireRate = 1.f;

    // meta = (AssetBundles = "X") groups soft refs for selective AM loading.
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Weapon",
              meta = (AssetBundles = "UI"))
    TSoftObjectPtr<UTexture2D> Icon;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Weapon",
              meta = (AssetBundles = "Game"))
    TSoftObjectPtr<USkeletalMesh> WorldMesh;
};
```

---

## DataTables

### Defining a Row Struct

`FTableRowBase` is declared in `Engine/DataTable.h`. Every row struct must inherit it and use `USTRUCT(BlueprintType)`.

```cpp
// ItemTableRow.h
#pragma once
#include "Engine/DataTable.h"
#include "ItemTableRow.generated.h"

USTRUCT(BlueprintType)
struct FItemTableRow : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FText DisplayName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxStack = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Weight = 0.5f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TSoftObjectPtr<UStaticMesh> PreviewMesh;

    // Called after CSV/JSON import. Override for custom fixups.
    virtual void OnPostDataImport(const UDataTable* InDataTable,
                                  const FName InRowName,
                                  TArray<FString>& OutCollectedImportProblems) override;
};
```

In the editor: right-click > Miscellaneous > Data Table, assign `FItemTableRow` as the row struct.

### Querying DataTables at Runtime

```cpp
UPROPERTY(EditDefaultsOnly, Category = "Data")
TObjectPtr<UDataTable> ItemTable;

// FindRow<T>: returns nullptr if row not found or type mismatch.
const FItemTableRow* Row = ItemTable->FindRow<FItemTableRow>(
    RowName, TEXT("LookupItem"));

// GetAllRows<T>: fills array with pointers to all rows.
TArray<FItemTableRow*> AllRows;
ItemTable->GetAllRows<FItemTableRow>(TEXT("GetAllItems"), AllRows);

// ForeachRow: iterate with row name keys.
ItemTable->ForeachRow<FItemTableRow>(
    TEXT("ForeachRow"),
    [](const FName& Key, const FItemTableRow& Value)
    {
        UE_LOG(LogTemp, Log, TEXT("Row %s: weight=%.2f"), *Key.ToString(), Value.Weight);
    });
```

### Runtime Modification and Row Handles

```cpp
// AddRow/RemoveRow do not persist to disk.
FItemTableRow NewRow;
NewRow.DisplayName = FText::FromString(TEXT("Runtime Sword"));
ItemTable->AddRow(FName(TEXT("RuntimeSword")), NewRow);
ItemTable->RemoveRow(FName(TEXT("ObsoleteItem")));

// Import from CSV at runtime (RowStruct must be set beforehand).
TArray<FString> Problems = ItemTable->CreateTableFromCSVString(CsvContent);

// Import from JSON at runtime. JSON format uses "RowName" as key with struct fields as properties.
TArray<FString> JsonProblems = ItemTable->CreateTableFromJSONString(JsonContent);

// Export to CSV/JSON strings (WITH_EDITOR only — unavailable in cooked/shipping builds):
FString CsvOut  = ItemTable->GetTableAsCSV();
FString JsonOut = ItemTable->GetTableAsJSON();

// FDataTableRowHandle: a UPROPERTY-friendly typed row reference.
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Config")
FDataTableRowHandle StartingWeaponHandle;

const FItemTableRow* Row = StartingWeaponHandle.GetRow<FItemTableRow>(
    TEXT("StartingWeapon lookup"));
```

---

## Asset References

### Hard References

```cpp
// Hard ref: loaded when the referencing asset loads. Causes the mesh/material
// to be in memory as long as this object is alive.
UPROPERTY(EditDefaultsOnly, Category = "Art")
TObjectPtr<UStaticMesh> Mesh;          // UE5 TObjectPtr preferred over raw ptr
```

Use hard references only for assets that are always needed while this object exists (e.g., a character's skeleton).

### Soft References

Soft references store a path string. The asset is NOT loaded until explicitly resolved.

```cpp
// TSoftObjectPtr<T>: soft ref to an asset instance.
UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Art")
TSoftObjectPtr<UStaticMesh> MeshSoft;

// TSoftClassPtr<T>: soft ref to a class (blueprint subclasses especially).
UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Spawning")
TSoftClassPtr<AActor> SpawnableSoft;

// FSoftObjectPath: untyped path, useful for generic systems.
FSoftObjectPath MeshPath = MeshSoft.ToSoftObjectPath();
```

#### Synchronous Resolution (avoid on game thread for large assets)

```cpp
UStaticMesh* Mesh = MeshSoft.LoadSynchronous();   // Blocks until loaded.

// FSoftObjectPath::TryLoad — returns nullptr if not on disk, does not assert.
UObject* Loaded = MeshPath.TryLoad();
```

#### Checking State Without Loading

```cpp
if (MeshSoft.IsNull())    { /* no path set */ }
if (MeshSoft.IsValid())   { /* path set AND asset is loaded in memory */ }
if (MeshSoft.IsPending()) { /* path set, async load started, not complete */ }

UStaticMesh* MeshPtr = MeshSoft.Get(); // Returns nullptr if not loaded.
```

---

## Async Loading

### FStreamableManager

`FStreamableManager` is declared in `Engine/StreamableManager.h`. Access it via `UAssetManager::GetStreamableManager()`.

```cpp
FStreamableManager& SM = UAssetManager::GetStreamableManager();
```

#### RequestAsyncLoad — Single Asset

```cpp
void AMyActor::LoadWeaponMeshAsync()
{
    FStreamableManager& SM = UAssetManager::GetStreamableManager();

    StreamableHandle = SM.RequestAsyncLoad(
        WeaponMeshSoft.ToSoftObjectPath(),
        FStreamableDelegate::CreateUObject(this, &AMyActor::OnWeaponMeshLoaded));
}

void AMyActor::OnWeaponMeshLoaded()
{
    if (StreamableHandle.IsValid() && StreamableHandle->HasLoadCompleted())
    {
        UStaticMesh* Mesh = WeaponMeshSoft.Get();
        if (Mesh)
        {
            MeshComponent->SetStaticMesh(Mesh);
        }
    }
}

// Member:
TSharedPtr<FStreamableHandle> StreamableHandle;
```

#### RequestAsyncLoad — Multiple Assets

```cpp
// All paths fire one callback when every asset is loaded.
TArray<FSoftObjectPath> PathsToLoad = {
    IconSoft.ToSoftObjectPath(), MeshSoft.ToSoftObjectPath() };
StreamableHandle = SM.RequestAsyncLoad(
    PathsToLoad,
    FStreamableDelegate::CreateLambda([this]()
    {
        // Both guaranteed loaded; IconSoft.Get() and MeshSoft.Get() are valid.
    }));
```

#### FStreamableHandle State and Control

```cpp
Handle->HasLoadCompleted();   // true when all assets finished.
Handle->IsLoadingInProgress();// true while still loading.
Handle->WasCanceled();        // true if CancelHandle() was called.
Handle->GetLoadProgress();    // 0.0 to 1.0.
Handle->WaitUntilComplete();  // blocks game thread — use only on loading screens.
Handle->ReleaseHandle();      // allow GC of loaded assets.
```

Priority: pass higher values to `RequestAsyncLoad` for urgent loads (default is 0).
Use `AsyncLoadHighPriority` (100) from `StreamableManager.h` for gameplay-critical assets.

`FStreamableManager` also provides `RequestSyncLoad()` for synchronous loading when the asset is needed immediately (e.g., during initialization). Prefer async for gameplay to avoid stalling the game thread.

---

## Asset Manager

### Setup — DefaultGame.ini

```ini
[/Script/Engine.AssetManagerSettings]
+PrimaryAssetTypesToScan=(PrimaryAssetType="WeaponDefinition",
    AssetBaseClass=/Script/MyGame.WeaponDefinition,
    bHasBlueprintClasses=False,
    bIsEditorOnly=False,
    Directories=((Path="/Game/Data/Weapons")),
    Rules=(Priority=1,bApplyRecursively=True))
```

### Custom AssetManager Subclass

Subclass `UAssetManager`, override `StartInitialLoading()` for startup logic, register in `DefaultEngine.ini`:

```ini
[/Script/Engine.Engine]
AssetManagerClassName=/Script/MyGame.UMyAssetManager
```

### Loading Primary Assets

```cpp
UAssetManager& AM = UAssetManager::Get();

// List all registered IDs of a type.
TArray<FPrimaryAssetId> WeaponIds;
AM.GetPrimaryAssetIdList(FPrimaryAssetType(TEXT("WeaponDefinition")), WeaponIds);

// Load a single primary asset asynchronously.
FPrimaryAssetId WeaponId(TEXT("WeaponDefinition"), TEXT("DA_Sword"));
TSharedPtr<FStreamableHandle> Handle = AM.LoadPrimaryAsset(
    WeaponId,
    TArray<FName>{ TEXT("Game") },  // load "Game" bundle (world mesh, etc.)
    FStreamableDelegate::CreateLambda([WeaponId]()
    {
        UWeaponDefinition* Def = UAssetManager::Get()
            .GetPrimaryAssetObject<UWeaponDefinition>(WeaponId);
        // Use Def...
    }));

// Load all assets of a type.
TSharedPtr<FStreamableHandle> AllHandle = AM.LoadPrimaryAssetsWithType(
    FPrimaryAssetType(TEXT("WeaponDefinition")),
    TArray<FName>{ TEXT("UI") });   // e.g., load only icons.

// Unload when no longer needed.
AM.UnloadPrimaryAsset(WeaponId);
```

### Asset Bundles

Bundles group soft references for selective loading. Decorate UPROPERTY fields with `meta = (AssetBundles = "BundleName")`. The Asset Manager will load only the requested bundle's assets.

```cpp
// "UI" bundle: loaded in menus for icon display.
UPROPERTY(EditDefaultsOnly, meta = (AssetBundles = "UI"))
TSoftObjectPtr<UTexture2D> Icon;

// "Game" bundle: loaded when entering gameplay.
UPROPERTY(EditDefaultsOnly, meta = (AssetBundles = "Game"))
TSoftObjectPtr<USkeletalMesh> WorldMesh;

// Transition from UI to Game bundle:
AM.ChangeBundleStateForPrimaryAssets(
    { WeaponId },
    { TEXT("Game") },   // AddBundles
    { TEXT("UI") });    // RemoveBundles
```

---

## Asset Registry

`IAssetRegistry` allows querying asset metadata without loading assets. Access it via `IAssetRegistry::GetChecked()` or `FAssetRegistryModule::GetRegistry()`.

```cpp
#include "AssetRegistry/AssetRegistryModule.h"
#include "AssetRegistry/IAssetRegistry.h"

IAssetRegistry& AR = IAssetRegistry::GetChecked();

// Get all assets of a class in a path.
TArray<FAssetData> AssetDataList;
AR.GetAssetsByPath(FName(TEXT("/Game/Data/Weapons")), AssetDataList, /*bRecursive=*/true);

// Get all assets of a specific class.
AR.GetAssetsByClass(
    FTopLevelAssetPath(TEXT("/Script/MyGame"), TEXT("WeaponDefinition")),
    AssetDataList,
    /*bSearchSubClasses=*/true);

// FAssetData is lightweight — no asset load occurs.
for (const FAssetData& Data : AssetDataList)
{
    FString AssetName = Data.AssetName.ToString();
    FSoftObjectPath Path = Data.GetSoftObjectPath();

    // Read asset registry tags without loading.
    FString TagValue;
    Data.GetTagValue(FName(TEXT("WeaponType")), TagValue);
}

// Query by tag values.
TMultiMap<FName, FString> TagFilter;
TagFilter.Add(TEXT("WeaponType"), TEXT("Melee"));
AR.GetAssetsByTagValues(TagFilter, AssetDataList);
```

### Making Properties Searchable

```cpp
UPROPERTY(EditDefaultsOnly, AssetRegistrySearchable)
FName WeaponType;
```

---

## Common Mistakes and Anti-Patterns

### Hard Referencing Everything

```cpp
// BAD: This UPROPERTY loads ALL 50 particle effects when this data asset loads.
UPROPERTY(EditDefaultsOnly)
TObjectPtr<UParticleSystem> HitEffect;

// GOOD: Soft reference — only load when the gameplay effect actually triggers.
UPROPERTY(EditDefaultsOnly)
TSoftObjectPtr<UParticleSystem> HitEffect;
```

### Loading on the Game Thread

```cpp
// BAD: LoadSynchronous on a large skeletal mesh stalls the render thread.
USkeletalMesh* Mesh = MeshSoft.LoadSynchronous();

// GOOD: Async load, apply result in callback.
UAssetManager::GetStreamableManager().RequestAsyncLoad(
    MeshSoft.ToSoftObjectPath(),
    FStreamableDelegate::CreateUObject(this, &AMyActor::OnMeshLoaded));
```

### Forgetting to Keep the Handle Alive

```cpp
// BAD: Handle is a local — destroyed when function returns, assets may be unloaded.
void LoadStuff()
{
    TSharedPtr<FStreamableHandle> Handle = SM.RequestAsyncLoad(...);
} // Handle destroyed here!

// GOOD: Store handle as a member until assets are no longer needed.
TSharedPtr<FStreamableHandle> LoadHandle; // member variable
```

### Not Registering Primary Asset Types

If a `UPrimaryDataAsset` subclass is not listed under `PrimaryAssetTypesToScan` in `DefaultGame.ini`, `GetPrimaryAssetIdList` returns nothing and `LoadPrimaryAsset` silently fails.

### Circular Soft Reference Resolution

Resolving a soft reference that itself holds soft references that point back creates load cycles. Use Asset Bundles to break cycles — load only the bundle that is needed for the current state.

### DataTable Column Changes with Existing Data

Adding a column to an existing DataTable struct invalidates serialized row data unless `bPreserveExistingValues` is set on the table or you re-import. Removing a column causes all existing rows to lose that data. Always back up DataTable assets before struct changes in production.

---

## Edge Cases

- **Cooked vs uncooked paths**: In uncooked builds, paths use `/Game/`. Cooked paths differ — do not hard-code paths; use `FSoftObjectPath` from UPROPERTY references.
- **Asset Manager and cook**: Assets not reachable through Primary Asset scanning rules or hard references will be excluded from the cook. Use `PrimaryAssetRules` or explicit asset labels to ensure inclusion.
- **Hot reload**: `UDataAsset` changes during PIE (Play In Editor) may not reflect until the asset is fully reloaded. Use `PostLoad` or `PostEditChangeProperty` for editor-time updates.
- **Memory budgets**: Track loaded assets by type via `UAssetManager::GetPrimaryAssetObjectList`. Use `ChangeBundleStateForPrimaryAssets` to swap between UI and Game bundles as scenes change.
- **`bStripFromClientBuilds`**: Set this on `UDataTable` instances that contain server-only data (e.g., loot tables with drop rates) to prevent distribution to clients.

---

## Related Skills

- `ue-cpp-foundations` — UPROPERTY specifiers, USTRUCT, UObject lifecycle
- `ue-serialization-savegames` — saving and loading soft object references across sessions
- `ue-module-build-system` — adding `AssetRegistry`, `Engine` module dependencies to Build.cs
