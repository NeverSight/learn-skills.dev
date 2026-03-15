---
name: ue-serialization-savegames
description: "Use when implementing save/load systems, player progress persistence, or data serialization in Unreal Engine. Triggers on: save game, USaveGame, FArchive, serialization, SaveGameToSlot, config, persist data, save file, load game. See references/save-system-architecture.md for full slot management and multi-user patterns."
metadata:
  version: 1.0.0
---

# UE Serialization & Save Games

You are an expert in Unreal Engine's serialization and save game systems. You implement save/load pipelines using `USaveGame`, `FArchive`, config files, and versioning so player progress persists correctly across sessions and game updates.

---

## Step 1: Read Project Context

Read `.agents/ue-project-context.md` before giving any recommendations. You need:
- Engine version (UE 5.0+ has `ULocalPlayerSaveGame`; earlier versions differ)
- Module names (the save system lives in a specific module)
- Target platforms (console vs. PC save paths and user indices differ)
- Whether multiplayer is in scope (server-authoritative vs. client-local saves)

If the file does not exist, ask the user to run `/ue-project-context` first.

---

## Step 2: Gather Requirements

Ask before writing code:
1. **Save complexity**: Simple key/value data, or complex world state with hundreds of objects?
2. **Data types**: Primitives, nested structs, asset references (soft vs. hard)?
3. **Versioning needs**: Live game with future patches? Old saves must keep working?
4. **Multiple save slots**: How many? Does each player/user get their own?
5. **Async requirement**: Can save/load stall the game thread, or must it be background?

---

## Step 3: USaveGame Subclass

`USaveGame` is an abstract `UObject` from `GameFramework/SaveGame.h`. Subclass it and mark fields with `UPROPERTY(SaveGame)` for automatic tagged serialization by `UGameplayStatics`.

```cpp
// MyGameSaveGame.h
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "MyGameSaveGame.generated.h"

USTRUCT(BlueprintType)
struct FInventoryItemData
{
    GENERATED_BODY() // Required — missing GENERATED_BODY() breaks struct serialization silently

    UPROPERTY(SaveGame) FName  ItemID;
    UPROPERTY(SaveGame) int32  Quantity = 0;
    UPROPERTY(SaveGame) bool   bIsEquipped = false;
};

UCLASS(BlueprintType)
class MYGAME_API UMyGameSaveGame : public USaveGame
{
    GENERATED_BODY()
public:
    UPROPERTY(SaveGame) int32   SaveVersion = 0;      // Always include a version field
    UPROPERTY(SaveGame) float   PlayerHealth = 100.f;
    UPROPERTY(SaveGame) int32   PlayerLevel = 1;
    UPROPERTY(SaveGame) FVector LastCheckpointLocation = FVector::ZeroVector;
    UPROPERTY(SaveGame) FString PlayerDisplayName;
    UPROPERTY(SaveGame) float   TotalPlayTimeSeconds = 0.f;
    UPROPERTY(SaveGame) TArray<FInventoryItemData>   InventoryItems;
    UPROPERTY(SaveGame) TMap<FName, int32>            AbilityLevels;
    // TSet<FName> is also supported in UPROPERTY(SaveGame) fields and serializes/deserializes automatically.

    // Asset references: FSoftObjectPath stores a string path — safe across saves
    // Never use raw UObject* or hard TObjectPtr<> to content assets in save data
    UPROPERTY(SaveGame) FSoftObjectPath LastEquippedWeaponPath;
};
```

### Saving and Loading

```cpp
#include "Kismet/GameplayStatics.h"

static const FString SlotName  = TEXT("MainSave");
static constexpr int32 UserIdx = 0; // Always 0 on PC; use GetPlatformUserIndex() on console

// Create the object first, populate its fields, then save
UMySaveGame* SaveGame = Cast<UMySaveGame>(UGameplayStatics::CreateSaveGameObject(UMySaveGame::StaticClass()));
SaveGame->PlayerHealth = 75.f;
// Then pass SaveGame to SaveGameToSlot / AsyncSaveGameToSlot below

// Sync save (blocks game thread — avoid in gameplay)
bool bSaved = UGameplayStatics::SaveGameToSlot(SaveData, SlotName, UserIdx);

// Async save (preferred — does not block)
FAsyncSaveGameToSlotDelegate OnSaved;
OnSaved.BindUObject(this, &USaveManager::OnAsyncSaveComplete);
UGameplayStatics::AsyncSaveGameToSlot(SaveData, SlotName, UserIdx, OnSaved);

// Load
if (UGameplayStatics::DoesSaveGameExist(SlotName, UserIdx))
{
    UMyGameSaveGame* Save = Cast<UMyGameSaveGame>(
        UGameplayStatics::LoadGameFromSlot(SlotName, UserIdx));
}

// Async load
FAsyncLoadGameFromSlotDelegate OnLoaded;
OnLoaded.BindUObject(this, &USaveManager::OnAsyncLoadComplete);
UGameplayStatics::AsyncLoadGameFromSlot(SlotName, UserIdx, OnLoaded);

// Delete
UGameplayStatics::DeleteGameInSlot(SlotName, UserIdx);
```

---

## Step 4: ULocalPlayerSaveGame (UE 5.0+)

`ULocalPlayerSaveGame` ties a save to a specific local player, tracks versioning via `GetLatestDataVersion()`, and provides `HandlePostLoad()` for migrations.

```cpp
UCLASS()
class MYGAME_API UMyLocalPlayerSave : public ULocalPlayerSaveGame
{
    GENERATED_BODY()
public:
    virtual int32 GetLatestDataVersion() const override { return 3; }
    virtual void  HandlePostLoad() override;

    UPROPERTY(SaveGame) TMap<FName, int32> UnlockedAbilities;
};

void UMyLocalPlayerSave::HandlePostLoad()
{
    Super::HandlePostLoad();
    const int32 Ver = GetSavedDataVersion(); // version when last saved

    if (Ver < 2) { UnlockedAbilities.Add(TEXT("Dash"), 1); }
    // Ver < 3 migrations go here
}
```

```cpp
// Load or create (sync)
UMyLocalPlayerSave* Save = ULocalPlayerSaveGame::LoadOrCreateSaveGameForLocalPlayer(
    UMyLocalPlayerSave::StaticClass(), PlayerController, TEXT("PlayerSlot0"));

// Load or create (async)
ULocalPlayerSaveGame::AsyncLoadOrCreateSaveGameForLocalPlayer(
    UMyLocalPlayerSave::StaticClass(), PlayerController, TEXT("PlayerSlot0"),
    FOnLocalPlayerSaveGameLoadedNative::CreateUObject(this, &AMyPC::OnSaveLoaded));

// Save back
Save->AsyncSaveGameToSlotForLocalPlayer(); // async (preferred)
Save->SaveGameToSlotForLocalPlayer();      // sync
```

---

## Step 5: FArchive and Custom Serialization

`FArchive` (from `Serialization/Archive.h`) is the base for all UE serialization. Key API:

```cpp
Ar.IsLoading()    // true when deserializing — same operator<< handles both directions
Ar.IsSaving()     // true when serializing to output
Ar.IsError()      // true after any read/write failure — always check before continuing
Ar.Tell()         // current position (int64); -1 if not seekable
Ar.CustomVer(Key) // returns the registered version number for a FGuid key
```

### FMemoryWriter and FMemoryReader

`FMemoryWriter`/`FMemoryReader` (from `Serialization/MemoryWriter.h` / `MemoryReader.h`) serialize to/from `TArray<uint8>`:

```cpp
// Serialize to bytes
TArray<uint8> OutBytes;
FMemoryWriter Writer(OutBytes, /*bIsPersistent=*/true);
int32 Version = 2;
Writer << Version;          // Serialize version header first — always
Writer << SomeData;
checkf(!Writer.IsError(), TEXT("Serialization failed"));

// Deserialize from bytes
FMemoryReader Reader(OutBytes, /*bIsPersistent=*/true);
int32 LoadedVersion = 0;
Reader << LoadedVersion;
if (LoadedVersion < 1 || Reader.IsError()) { /* corrupt data */ return; }
Reader << SomeData;
```

### FBufferArchive

`FBufferArchive` (from `Serialization/BufferArchive.h`) combines `FMemoryWriter` + `TArray<uint8>` — the object *is* the output buffer:

```cpp
FBufferArchive Buffer(/*bIsPersistent=*/true);
int32 Magic = 0x53415645; // 'SAVE'
Buffer << Magic;
Buffer << MyStruct;        // requires operator<< overload
TArray<uint8> Bytes = MoveTemp(Buffer); // FBufferArchive IS a TArray<uint8>
```

### Custom operator<< for Structs

Define `operator<<` to make a struct serializable via any `FArchive` (required when passing it to `FBufferArchive`, `FMemoryWriter`, etc.):

```cpp
FArchive& operator<<(FArchive& Ar, FMyCustomData& Data)
{
    Ar << Data.Name << Data.Value << Data.Timestamp;
    return Ar;
}
```

### Compressed Archives

For large saves, use `FArchiveSaveCompressedProxy` / `FArchiveLoadCompressedProxy` (from `Serialization/ArchiveSaveCompressedProxy.h`):

```cpp
// Compress
TArray<uint8> Compressed;
FArchiveSaveCompressedProxy Comp(Compressed, NAME_Zlib);
Comp.Serialize(RawData.GetData(), RawData.Num());
Comp.Flush();

// Decompress
FArchiveLoadCompressedProxy Decomp(Compressed, NAME_Zlib);
TArray<uint8> Raw;
Raw.SetNum(KnownUncompressedSize);
Decomp.Serialize(Raw.GetData(), Raw.Num());
```

### Custom Serialize() on UObject

Override `Serialize(FArchive& Ar)` for precise binary layout control:

```cpp
void UMyObject::Serialize(FArchive& Ar)
{
    Super::Serialize(Ar); // always call Super first
    Ar << BinaryField;
    Ar << UniqueRunID;
    if (Ar.IsLoading() && Ar.IsError()) { /* handle corruption */ }
}
```

---

## Step 6: Versioning

### Integer Versioning in USaveGame

```cpp
namespace ESaveVersion
{
    enum Type : int32
    {
        Initial          = 0,
        AddedInventory   = 1,
        SoftRefForWeapon = 2,
        VersionPlusOne,
        Latest = VersionPlusOne - 1
    };
}

void USaveManager::RunMigrations(UMyGameSaveGame* Save)
{
    if (Save->SaveVersion == ESaveVersion::Latest) { return; }

    if (Save->SaveVersion < ESaveVersion::AddedInventory)
        Save->InventoryItems.Reset();

    if (Save->SaveVersion < ESaveVersion::SoftRefForWeapon)
    { /* convert old FName field to FSoftObjectPath */ }

    Save->SaveVersion = ESaveVersion::Latest; // stamp after migration
}
```

### FCustomVersionRegistration (FArchive-based saves)

```cpp
// Declare version enum + GUID (generate once with FGuid::NewGuid(), then hardcode)
struct FMySaveVersion
{
    enum Type { Initial = 0, AddedQuestData = 1, VersionPlusOne, Latest = VersionPlusOne - 1 };
    static const FGuid GUID;
};
const FGuid FMySaveVersion::GUID(0xA1B2C3D4, 0xE5F60718, 0x293A4B5C, 0x6D7E8F90);

// Register globally (module startup or static):
FCustomVersionRegistration GReg(FMySaveVersion::GUID, FMySaveVersion::Latest, TEXT("MySave"));

// In Serialize():
Ar.UsingCustomVersion(FMySaveVersion::GUID);
const int32 Ver = Ar.CustomVer(FMySaveVersion::GUID);
Ar << CoreData;
if (Ver >= FMySaveVersion::AddedQuestData)
    Ar << QuestData;
else if (Ar.IsLoading())
    QuestData.Reset(); // Initialize missing data on old saves
```

### Struct Field Migration

When a struct field is renamed or its type changes, override `Serialize()` on the struct to migrate old data:

```cpp
void FMyStruct::Serialize(FArchive& Ar)
{
    Ar.UsingCustomVersion(FMySaveVersion::GUID);
    if (Ar.CustomVer(FMySaveVersion::GUID) < FMySaveVersion::RenamedHealthToHP)
    {
        float OldHealth;
        Ar << OldHealth;
        HP = OldHealth; // Migrate old field name to new
    }
    else
    {
        Ar << HP;
    }
}
```

---

## Step 7: Config Files

### UGameUserSettings (user preferences)

```cpp
UCLASS()
class MYGAME_API UMyGameUserSettings : public UGameUserSettings
{
    GENERATED_BODY()
public:
    UPROPERTY(Config, BlueprintReadWrite, Category="Game")
    float MasterVolume = 1.0f;

    UPROPERTY(Config, BlueprintReadWrite, Category="Game")
    bool bSubtitlesEnabled = true;

    void ApplyAndSave() { ApplySettings(false); SaveSettings(); }
};
// Register in DefaultEngine.ini:
// [/Script/Engine.Engine]
// GameUserSettingsClassName=/Script/MyGame.MyGameUserSettings
```

### UDeveloperSettings (project settings)

```cpp
UCLASS(Config=Game, DefaultConfig, meta=(DisplayName="My Game Settings"))
class MYGAME_API UMyProjectSettings : public UDeveloperSettings
{
    GENERATED_BODY()
public:
    UPROPERTY(Config, EditAnywhere, Category="Save") int32 MaxSaveSlots = 5;
    UPROPERTY(Config, EditAnywhere, Category="Save") bool  bEnableAutoSave = true;
    UPROPERTY(Config, EditAnywhere, Category="Save") float AutoSaveIntervalSeconds = 300.f;
    static const UMyProjectSettings* Get() { return GetDefault<UMyProjectSettings>(); }
};
```

### GConfig Direct Access

```cpp
#include "Misc/ConfigCacheIni.h"

FString Value;
GConfig->GetString(TEXT("/Script/MyGame.MyConfig"), TEXT("Key"), Value, GGameIni);
GConfig->SetString(TEXT("/Script/MyGame.MyConfig"), TEXT("Key"), TEXT("Val"), GGameIni);
GConfig->Flush(/*bRemoveFromCache=*/false, GGameIni);

MyObject->SaveConfig();  // writes UPROPERTY(Config) fields to .ini
MyObject->LoadConfig();  // reloads from .ini
```

**INI section naming**: Section `[/Script/ModuleName.ClassName]` maps to the CDO. `SaveConfig()` writes from the object to INI; `LoadConfig()` reads INI into the object and is called automatically for the CDO at startup. Custom section names require overriding `OverrideConfigSection(FString& SectionName)`.

---

## Cloud Save Integration

```cpp
// Platform save systems (Steam, EOS, console) provide ISaveGameSystem
// Access via IPlatformFeaturesModule:
ISaveGameSystem* SaveSystem = IPlatformFeaturesModule::Get().GetSaveGameSystem();
if (SaveSystem && SaveSystem->DoesSaveSystemSupportMultipleUsers())
{
    // Platform handles cloud sync — use UGameplayStatics normally
    // Steam: auto-syncs Saved/SaveGames/ via Steam Cloud if configured in Steamworks
    // EOS: use IOnlineSubsystem → IOnlineTitleFileInterface for explicit cloud read/write
}

// Cross-platform pattern: serialize to TArray<uint8>, then write via platform API
TArray<uint8> SaveData;
FMemoryWriter Ar(SaveData);
SaveObject->Serialize(Ar);
// Upload SaveData via platform SDK

// Steam Cloud — write save slot directly via Steamworks API
ISteamRemoteStorage* SteamStorage = SteamRemoteStorage();
if (SteamStorage && SteamStorage->IsCloudEnabledForApp())
{
    SteamStorage->FileWrite("SaveSlot1.sav", SaveData.GetData(), SaveData.Num());
}
// Read back: SteamStorage->FileRead("SaveSlot1.sav", Buffer, Size)
```

## Save Data Encryption

```cpp
// Use FAES for symmetric encryption of save data
#include "Misc/AES.h"
// Build a zero-padded 32-byte FAESKey from a string.
// Do NOT use Key.Left(32): if the string is shorter than 32 chars it silently
// produces a truncated key, corrupting every encrypt/decrypt call.
static FAESKey MakeAESKey(const FString& KeyString)
{
    FAESKey AESKey;
    FMemory::Memzero(AESKey.Key, FAESKey::KeySize);
    const FTCHARToUTF8 Utf8(*KeyString);
    FMemory::Memcpy(AESKey.Key, Utf8.Get(), FMath::Min(Utf8.Length(), FAESKey::KeySize));
    return AESKey;
}

void EncryptSaveData(TArray<uint8>& Data, const FString& KeyString)
{
    int32 PaddedSize = Align(Data.Num(), FAES::AESBlockSize);
    Data.SetNumZeroed(PaddedSize);
    FAES::EncryptData(Data.GetData(), PaddedSize, MakeAESKey(KeyString));
}

void DecryptSaveData(TArray<uint8>& Data, const FString& KeyString)
{
    FAES::DecryptData(Data.GetData(), Data.Num(), MakeAESKey(KeyString));
}
```

**Why encrypt**: Prevents casual save editing for competitive/economy-sensitive games. Not foolproof — determined players can still extract keys from the binary. Combine with server-side validation for authoritative saves.

---

## Step 8: Common Mistakes

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Saving raw `UObject*` or `AActor*` | Pointers invalid between sessions | Save `FSoftObjectPath` or a stable unique ID |
| No version field | Adding/removing fields corrupts old saves silently | Always include `int32 SaveVersion`; run migrations on load |
| `SaveGameToSlot` on game thread per frame | Blocks rendering, causes hitches | Use `AsyncSaveGameToSlot` |
| `USTRUCT` without `GENERATED_BODY()` in a saved field | Silent serialization failure | Add `GENERATED_BODY()` to all saved structs |
| Ignoring `Ar.IsError()` | Reads past corrupted data, applies garbage | Check after every block; abort immediately if set |
| Overlapping async saves | Second save starts before first completes | Guard with `bSaveInProgress` flag or `IsSaveInProgress()` |
| Hardcoded save file paths | Breaks on consoles and different platforms | Use `UGameplayStatics` APIs; `FPaths::ProjectSavedDir()` only for debug |

**PIE vs. Packaged / platform paths**: In PIE, saves go to `<Project>/Saved/SaveGames/`. Packaged Windows builds write to `%LocalAppData%/<ProjectName>/Saved/SaveGames/`. Console platforms use title storage APIs. `UGameplayStatics::SaveGameToSlot` abstracts all of this through the platform's `ISaveGameSystem` — never hardcode OS paths; use `FPaths::ProjectSavedDir()` only for debug logging.

---

## Advanced Edge Cases

**Corruption recovery**: When `Ar.IsError()` returns true mid-read or magic/version checks fail, discard the corrupt data and fall back to a fresh save. Optionally maintain a backup slot (write to `Slot_Backup` before overwriting `Slot_Primary`) so players never lose all progress:

```cpp
USaveGame* LoadedSave = UGameplayStatics::LoadGameFromSlot(PrimarySlot, 0);
if (!LoadedSave)
    LoadedSave = UGameplayStatics::LoadGameFromSlot(BackupSlot, 0);
if (!LoadedSave)
    LoadedSave = UGameplayStatics::CreateSaveGameObject(UMySaveGame::StaticClass());
```

**Large saves — chunked approach**: Split world state across multiple slots by subsystem (e.g., `Save_World_00`, `Save_Inventory`, `Save_Quests`). Load each with `AsyncLoadGameFromSlot` in parallel. This prevents single-file bottlenecks and lets you load only what's needed for the current level.

**Multiplayer save ownership**: Shared world state (quests, economy, enemy state) belongs to server-authoritative saves — the server's `AGameMode` writes these; clients send state changes via RPCs, never write shared saves directly. Per-player preferences (keybinds, UI layout) remain client-local via `ULocalPlayerSaveGame`. This split prevents desync and cheating.

---

## Module Dependencies (Build.cs)

```csharp
PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine" });
// For UDeveloperSettings:
PublicDependencyModuleNames.Add("DeveloperSettings");
```

---

## Related Skills

- `ue-cpp-foundations` — UPROPERTY, USTRUCT, UObject lifetime
- `ue-data-assets-tables` — FSoftObjectPath patterns for asset references in saves
- `ue-gameplay-framework` — GameInstance as save manager host; GameMode auto-save integration

## Reference Files

- `references/save-system-architecture.md` — Full slot manager subsystem, metadata bank, multi-user patterns, and migration pipeline
