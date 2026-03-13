---
name: ue-cpp-foundations
description: Use when writing Unreal Engine C++ code involving UPROPERTY, UFUNCTION, UCLASS, TArray, TMap, delegates, FString, garbage collection, or smart pointers. Also use when the user asks about "UE C++", USTRUCT, UENUM, FName, FText, TObjectPtr, TWeakObjectPtr, UObject lifetime, UE_LOG, or UE subsystems. For module build configuration, see ue-module-build-system. For Actor/Component architecture, see ue-actor-component-architecture.
metadata:
  version: 1.0.0
---

# UE C++ Foundations

You are an expert in Unreal Engine's C++ extensions and property system.

## Context

Read `.agents/ue-project-context.md` for engine version, coding conventions, and project-specific rules. Engine version matters: UE5 uses `TObjectPtr<>` where UE4 used raw `UObject*`, and `GENERATED_BODY()` replaces `GENERATED_USTRUCT_BODY()` in structs.

## Before You Start

Ask which area the user needs help with if unclear:
- **Macros & Reflection** — UCLASS, UPROPERTY, UFUNCTION, USTRUCT, UENUM
- **Containers** — TArray, TMap, TSet, TOptional
- **Delegates** — static, dynamic, multicast, binding patterns
- **Strings** — FName, FString, FText conversion and formatting
- **Memory & GC** — TObjectPtr, TWeakObjectPtr, TSharedPtr, GC roots
- **Logging** — UE_LOG, log categories, verbosity
- **Subsystems** — GameInstance, World, LocalPlayer subsystems

---

## UObject Macros & Reflection

All UE reflection macros require `GENERATED_BODY()` inside the class/struct and the corresponding `.generated.h` include.

### UCLASS()

| Specifier | Effect |
|-----------|--------|
| `Blueprintable` | Blueprint subclassing allowed |
| `BlueprintType` | Usable as Blueprint variable |
| `Abstract` | Cannot be instantiated |
| `NotBlueprintable` | Blocks Blueprint subclassing |
| `Config=<Name>` | Loads UPROPERTY(Config) from `<Name>.ini` |
| `Transient` | Not saved/serialized |
| `Within=<OuterClass>` | Outer must be of given type |

```cpp
UCLASS(Blueprintable, BlueprintType)
class MYGAME_API UMyDataObject : public UObject
{
    GENERATED_BODY()
public:
    UMyDataObject();
};
```

Full specifier list: [references/property-specifiers.md](references/property-specifiers.md).

### UPROPERTY()

```cpp
UCLASS(Blueprintable)
class MYGAME_API AMyCharacter : public ACharacter
{
    GENERATED_BODY()
public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Stats")
    float MaxHealth = 100.f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Stats")
    float CurrentHealth;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Config")
    int32 MaxLevel = 50;

    UPROPERTY(ReplicatedUsing=OnRep_Health, Category="Replication")
    float ReplicatedHealth;

    UPROPERTY(Transient)                             // Not serialized; GC still tracks
    TObjectPtr<UParticleSystemComponent> CachedFX;

    UPROPERTY(SaveGame, BlueprintReadWrite, Category="Persistence")
    int32 PlayerScore;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Stats",
              meta=(ClampMin="0.0", ClampMax="1.0"))
    float DamageMultiplier = 1.f;

    UFUNCTION()
    void OnRep_Health();

    virtual void GetLifetimeReplicatedProps(
        TArray<FLifetimeProperty>& OutLifetimeProps) const override;
};
```

### UFUNCTION()

```cpp
UFUNCTION(BlueprintCallable, Category="Actions")
void PerformAttack(float Damage);

UFUNCTION(BlueprintPure, Category="Queries")
float GetHealthPercent() const;

UFUNCTION(BlueprintNativeEvent, Category="Events")  // C++ provides _Implementation
void OnDamageTaken(float Amount);
virtual void OnDamageTaken_Implementation(float Amount);

UFUNCTION(BlueprintImplementableEvent, Category="Events")  // Blueprint must implement
void OnLevelUp(int32 NewLevel);

UFUNCTION(Server, Reliable, WithValidation)         // RPC: runs on server
void ServerFireWeapon(FVector Origin, FVector Direction);
void ServerFireWeapon_Implementation(FVector Origin, FVector Direction);
bool ServerFireWeapon_Validate(FVector Origin, FVector Direction);

UFUNCTION(Client, Reliable)                        // RPC: runs on owning client
void ClientShowDamageNumber(float Amount);
void ClientShowDamageNumber_Implementation(float Amount);

UFUNCTION(NetMulticast, Reliable)                   // RPC: runs on all
void MulticastPlayEffect(FVector Location);
void MulticastPlayEffect_Implementation(FVector Location);

UFUNCTION(Exec)                                    // Console command (~ in-game)
void DebugResetStats();                            // Works on PC, Pawn, HUD, GM, GI, CheatManager
```

### USTRUCT() and UENUM()

```cpp
// UE5: always GENERATED_BODY() — never GENERATED_USTRUCT_BODY()
USTRUCT(BlueprintType)
struct MYGAME_API FWeaponStats
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere, BlueprintReadWrite) float BaseDamage = 10.f;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) float FireRate   = 0.5f;
};

// DataTable row
USTRUCT(BlueprintType)
struct MYGAME_API FEnemyTableRow : public FTableRowBase
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FName EnemyID;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) TSoftClassPtr<AActor> SpawnClass;
};

UENUM(BlueprintType)
enum class EWeaponState : uint8
{
    Idle      UMETA(DisplayName="Idle"),
    Firing    UMETA(DisplayName="Firing"),
    Reloading UMETA(DisplayName="Reloading"),
};
```

---

## UE Containers

See [references/container-patterns.md](references/container-patterns.md) for full API and performance guide.

### TArray — Ordered Dynamic Array

```cpp
TArray<FString> Names;
Names.Add(TEXT("Alpha"));
Names.Emplace(TEXT("Beta"));       // Construct in-place (avoids copy)
Names.Reserve(100);                // Pre-allocate

FString First = Names[0];
bool bHas     = Names.Contains(TEXT("Alpha"));
int32 Idx     = Names.Find(TEXT("Beta"));  // INDEX_NONE if absent
FString* Ptr  = Names.FindByPredicate([](const FString& S){ return S.StartsWith(TEXT("A")); });

Names.Sort([](const FString& A, const FString& B){ return A.Len() < B.Len(); });
Names.Remove(TEXT("Alpha"));       // Order-preserving O(n)
Names.RemoveAtSwap(0);             // Fast O(1), destroys order

for (const FString& N : Names) { /* do NOT add/remove during ranged-for */ }
for (int32 i = Names.Num()-1; i >= 0; --i) { if (Names[i].IsEmpty()) Names.RemoveAt(i); }
```

### TMap — Hash Map

```cpp
TMap<FName, int32> ItemCounts;
ItemCounts.Add(FName("Sword"), 3);

int32& Ref  = ItemCounts.FindOrAdd(FName("Sword")); // Insert default if absent
int32* Ptr  = ItemCounts.Find(FName("Axe"));        // nullptr if absent
bool   bHas = ItemCounts.Contains(FName("Shield"));
ItemCounts.Remove(FName("Shield"));

for (const TPair<FName, int32>& Pair : ItemCounts) { /* ... */ }
```

### TSet — Hash Set

```cpp
TSet<FName> Tags;
Tags.Add(FName("Flying"));
bool bFlying          = Tags.Contains(FName("Flying"));
TSet<FName> Intersect = Tags.Intersect(OtherTags);
TSet<FName> Union     = Tags.Union(OtherTags);
```

### TOptional

```cpp
TOptional<float> MaybeHP;
if (MaybeHP.IsSet()) { float H = MaybeHP.GetValue(); }
float Safe = MaybeHP.Get(0.f);  // Default if not set
MaybeHP = 75.f;
MaybeHP.Reset();
```

### TVariant

```cpp
// Type-safe tagged union — avoids unsafe casts
TVariant<int32, float, FString> Value;
Value.Set<FString>(TEXT("Hello"));

if (Value.IsType<FString>())
{
    const FString& Str = Value.Get<FString>();
}

// Visit — use explicit overloads; LexToString(V) fails when V is FString.
Visit(TOverloaded{
    [](int32  V) { UE_LOG(LogTemp, Log, TEXT("%d"), V); },
    [](float  V) { UE_LOG(LogTemp, Log, TEXT("%f"), V); },
    [](const FString& V) { UE_LOG(LogTemp, Log, TEXT("%s"), *V); },
}, Value);
```

---

## Delegates

See [references/delegate-patterns.md](references/delegate-patterns.md) for all declaration macros and binding methods.

### Choosing the Right Type

| Type | Bindings | Blueprint | When to Use |
|------|----------|-----------|-------------|
| `DECLARE_DELEGATE` | 1 | No | Internal single-owner callback |
| `DECLARE_MULTICAST_DELEGATE` | N | No | Internal multi-listener events |
| `DECLARE_DYNAMIC_DELEGATE` | 1 | Yes | Blueprint-assignable single callback |
| `DECLARE_DYNAMIC_MULTICAST_DELEGATE` | N | Yes | Blueprint-bindable events (most common) |

### Declaration, Binding, Invocation

```cpp
// File scope (before UCLASS)
DECLARE_DELEGATE_OneParam(FOnItemPickedUp, AActor*);
DECLARE_MULTICAST_DELEGATE_TwoParams(FOnHealthChanged, float, float);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnHealthChangedDynamic, float, CurrentHealth, float, MaxHealth);

UCLASS()
class AMyActor : public AActor
{
    GENERATED_BODY()
public:
    UPROPERTY(BlueprintAssignable, Category="Events")
    FOnHealthChangedDynamic OnHealthChanged;   // Dynamic multicast in UPROPERTY
};

// Static single delegate
FOnItemPickedUp D;
D.BindUObject(this, &AMyCharacter::HandlePickup);
D.BindLambda([this](AActor* Item){ UE_LOG(LogTemp, Log, TEXT("%s"), *Item->GetName()); });
D.ExecuteIfBound(SomeActor);
// Multicast: add/broadcast/remove
FDelegateHandle H = HealthDelegate.AddUObject(this, &AMyHUD::OnHealthChanged);
HealthDelegate.Broadcast(75.f, 100.f);
HealthDelegate.Remove(H);
// Dynamic multicast
OnHealthChanged.AddDynamic(this, &AMyCharacter::HandleHealthChange);
OnHealthChanged.RemoveDynamic(this, &AMyCharacter::HandleHealthChange);
OnHealthChanged.Broadcast(75.f, 100.f);
```

---

## String Types

| Type | Use For | Comparison | Mutable |
|------|---------|-----------|---------|
| `FName` | Identifiers, asset names, tags | O(1) integer | No |
| `FString` | General-purpose strings, file paths | O(n) | Yes |
| `FText` | Player-visible display strings | — | No |

```cpp
// FName — global name table, case-insensitive O(1) compare
FName Tag("WeaponTag_Rifle");
FString S = Tag.ToString();
FName  N  = FName(*S);

// FString — heap string, Printf for formatting
FString Msg = FString::Printf(TEXT("HP: %.1f"), Health);
UE_LOG(LogTemp, Log, TEXT("%s"), *Msg);  // * dereferences to TCHAR*
int32 Num = FCString::Atoi(*FString("42"));

// FText — localized display text
// LOCTEXT requires a namespace defined in the same translation unit:
#define LOCTEXT_NAMESPACE "MyGame"
FText Label = LOCTEXT("Key", "Assault Rifle");
FText Fmt   = FText::Format(LOCTEXT("HP", "HP: {0}/{1}"),
                             FText::AsNumber(Cur), FText::AsNumber(Max));
#undef LOCTEXT_NAMESPACE  // Or: NSLOCTEXT("MyGame", "Key", "...") without a define
```

**Conversion:** `Name.ToString()` → FString, `FName(*Str)` ← FString, `FText::FromString(Str)`, `Text.ToString()`.

---

## Memory & Garbage Collection

UE's GC tracks every `UObject*` reachable from a root. Unreachable objects are destroyed.

```cpp
// UE5: TObjectPtr<> for UPROPERTY member UObject pointers
UPROPERTY()
TObjectPtr<UStaticMeshComponent> MeshComp;       // GC-tracked, lazy-load aware
// Without UPROPERTY — invisible to GC, pointer may dangle
UMyObject* UnsafePtr;  // BAD
// TWeakObjectPtr — non-owning, safe (becomes null after GC)
TWeakObjectPtr<AMyActor> WeakRef;
if (WeakRef.IsValid()) { WeakRef->DoSomething(); }
// TSharedPtr/TWeakPtr — for non-UObject plain C++ types ONLY
TSharedPtr<FMyData> Data = MakeShared<FMyData>();
TWeakPtr<FMyData>   Weak = Data;
if (TSharedPtr<FMyData> Pinned = Weak.Pin()) { Pinned->Process(); }
// NEVER use TSharedPtr for UObject-derived types
// GC root: AddToRoot (use sparingly)
UMyObject* Obj = NewObject<UMyObject>();
Obj->AddToRoot();
// ...
Obj->RemoveFromRoot();
// FGCObject: preferred for non-UObject C++ classes holding UObject refs
// UE 5.3+: use TObjectPtr<> — raw UObject* crashes with incremental GC.
class FMyManager : public FGCObject
{
public:
    virtual void AddReferencedObjects(FReferenceCollector& Collector) override
    {
        Collector.AddReferencedObject(ManagedObject);
    }
    virtual FString GetReferencerName() const override { return TEXT("FMyManager"); }
private:
    TObjectPtr<UMyObject> ManagedObject = nullptr;
};
```

---

## Logging

```cpp
// MyGameLog.h / .cpp
DECLARE_LOG_CATEGORY_EXTERN(LogMyGame, Log, All);
DEFINE_LOG_CATEGORY(LogMyGame);

// Single-file: DEFINE_LOG_CATEGORY_STATIC(LogLocal, Log, All);

UE_LOG(LogMyGame, Log,     TEXT("Loaded: %s"), *LevelName);
UE_LOG(LogMyGame, Warning, TEXT("HP low: %.1f"), Health);
UE_LOG(LogMyGame, Error,   TEXT("Spawn failed: %s"), *ClassName);
UE_CLOG(Health < 0.f, LogMyGame, Error, TEXT("Negative HP: %.1f"), Health);
```

| Verbosity | Visible | When |
|-----------|---------|------|
| `Fatal` | Always | Crash-level |
| `Error` | Always | Operation failed |
| `Warning` | Always | Unexpected but recoverable |
| `Log` | Non-shipping | Standard trace |
| `Verbose` | `-LogCmds` | Fine-grained trace |

---

## Subsystems

Auto-registered singletons — no manual `AddToRoot` needed.

| Subsystem | Owner | Persists Level Load | Per Player |
|-----------|-------|---------------------|------------|
| `UGameInstanceSubsystem` | `UGameInstance` | Yes | No |
| `UWorldSubsystem` | `UWorld` | No | No |
| `ULocalPlayerSubsystem` | `ULocalPlayer` | Yes | Yes |
| `UEngineSubsystem` | `UEngine` | Yes (whole session) | No |

```cpp
UCLASS()
class MYGAME_API UInventorySubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()
public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    UFUNCTION(BlueprintCallable) void AddItem(FName ItemID, int32 Count);
private:
    TMap<FName, int32> Inventory;
};

// Access — each subsystem type has a different accessor
UInventorySubsystem* Inv = GetGameInstance()->GetSubsystem<UInventorySubsystem>();
USpawnSubsystem*     Sp  = GetWorld()->GetSubsystem<USpawnSubsystem>();
UUIStateSubsystem*   UI  = GetLocalPlayer()->GetSubsystem<UUIStateSubsystem>();
UMyEngineSubsystem*  ES  = GEngine->GetEngineSubsystem<UMyEngineSubsystem>();
```

Subsystems have `Initialize()` and `Deinitialize()` -- override for setup/teardown. `UGameInstanceSubsystem` persists across map changes; `UWorldSubsystem` reinitializes per world. Call `GetSubsystem<T>()` via the owning context (`GetGameInstance()`, `GetWorld()`, `GetLocalPlayer()`).

---

## Replicated Properties

Both `UPROPERTY` specifier AND `GetLifetimeReplicatedProps` are required:

```cpp
UPROPERTY(ReplicatedUsing = OnRep_Health)
float Health;

UFUNCTION()
void OnRep_Health(); // Called on clients when server updates Health

void AMyActor::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutProps) const
{
    Super::GetLifetimeReplicatedProps(OutProps);
    DOREPLIFETIME_CONDITION(AMyActor, Health, COND_OwnerOnly);
    // COND_None, COND_OwnerOnly, COND_SkipOwner, COND_SimulatedOnly, COND_InitialOnly
}
```

---

## Conditional Compilation Guards

```cpp
#if WITH_EDITOR
// Editor-only properties — stripped from shipping builds
UPROPERTY(EditAnywhere, Category="Debug")
bool bShowDebugSpheres = false;

virtual void PostEditChangeProperty(FPropertyChangedEvent& E) override;
#endif

#if !UE_BUILD_SHIPPING
// Available in Development + Debug, stripped from Shipping
void DrawDebugInfo();
#endif
```

---

## Common Mistakes

**Raw UObject* member without UPROPERTY — dangling pointer:**
```cpp
UMyObject* Obj;  // BAD — GC invisible
UPROPERTY() TObjectPtr<UMyObject> Obj;  // GOOD
```

**Modify TArray during ranged-for — undefined behavior:**
```cpp
for (const AActor* A : Actors) { Actors.Remove(A); }  // CRASH
for (int32 i = Actors.Num()-1; i >= 0; --i) { if (ShouldRemove(Actors[i])) Actors.RemoveAt(i); }
```

**TSharedPtr on a UObject — GC + refcount conflict:**
```cpp
TSharedPtr<UMyObject> P = MakeShared<UMyObject>();  // BAD — leaks or double-free
UPROPERTY() TObjectPtr<UMyObject> P;                 // GOOD
```

**Missing GetLifetimeReplicatedProps:**
```cpp
void AMyActor::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME(AMyActor, ReplicatedHealth);
    DOREPLIFETIME_CONDITION(AMyActor, TeamScore, COND_OwnerOnly);
}
```

**GENERATED_USTRUCT_BODY() in UE5 structs — use GENERATED_BODY() instead.**

**AddDynamic with a non-UFUNCTION — compile error or crash at runtime.**

---

## Related Skills

- **ue-module-build-system** — Build.cs, module dependencies, include paths, PCH configuration
- **ue-actor-component-architecture** — AActor/UActorComponent lifecycle, spawning, tick groups, component setup
