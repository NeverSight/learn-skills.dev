---
name: ue-actor-component-architecture
description: "Use this skill when working with Actor and component design in Unreal Engine. Triggers on: Actor, component, BeginPlay, Tick, SpawnActor, lifecycle, CreateDefaultSubobject, composition, EndPlay, PostInitializeComponents, UActorComponent, USceneComponent, UINTERFACE, attachment, spawn, interface. See references/actor-lifecycle.md and references/component-types.md for detailed tables."
metadata:
  version: 1.0.0
---

# UE Actor-Component Architecture

You are an expert in Unreal Engine's Actor-Component architecture.

## Project Context

Before responding, read `.agents/ue-project-context.md` for the project's subsystem inventory, coding conventions, and any existing actor hierarchies or component patterns. This tells you which base classes are established and what naming conventions apply.

## Information Gathering

Clarify the developer's specific need before diving in:

- New actor from scratch, or adding behavior to an existing one?
- Logic-only (UActorComponent) or needs world position (USceneComponent)?
- Spawning requirement (deferred init, pooling, net-spawned)?
- Lifecycle bug (BeginPlay/Constructor confusion, component not initialized)?
- Cross-actor behavior via interfaces?

---

## Core Architecture Mental Model

Unreal's Actor-Component system is **composition over inheritance**. An `AActor` is a container that owns components. Behavior, rendering, collision, and logic are all expressed through `UActorComponent` subclasses.

```
UObject
  └── AActor                         (placeable/spawnable world entity)
        └── owns N x UActorComponent (reusable behavior units)
              └── USceneComponent    (adds transform + attachment)
                    └── UPrimitiveComponent (adds collision + rendering)
```

`AActor` is a full `UObject` — never `new`/`delete` an actor. Always use `SpawnActor` and `Destroy`.

---

## Actor Lifecycle

Full event order and safety rules are in `references/actor-lifecycle.md`. Key sequence:

```
Constructor                  → CreateDefaultSubobject, tick config, default values
PostActorCreated             → spawned actors only; before construction script
PostInitializeComponents     → all components initialized; world accessible
BeginPlay                    → game running; full logic OK; components BeginPlay fires here
Tick(DeltaTime)              → per-frame; each ticking component's TickComponent fires
EndPlay(EEndPlayReason)      → cleanup; ClearAllTimers; call Super
Destroyed                    → pre-GC; avoid complex logic
```

### Constructor vs BeginPlay

**Constructor** runs first on the **Class Default Object (CDO)** — an archetype used for default values. `GetWorld()` returns `nullptr` on the CDO. Never access the world or other actors in the constructor.

```cpp
// CORRECT — constructor-time only
AMyActor::AMyActor()
{
    MeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    SetRootComponent(MeshComp);
    PrimaryActorTick.bCanEverTick = true;
    PrimaryActorTick.TickInterval = 0.1f;
}

// CORRECT — world-dependent code belongs in BeginPlay
void AMyActor::BeginPlay()
{
    Super::BeginPlay(); // Required — always call Super
    GetWorld()->SpawnActor<AProjectile>(...);
}
```

### PostInitializeComponents

Called before BeginPlay; components are initialized; world exists. Use it to bind delegates to own components.

```cpp
void AMyCharacter::PostInitializeComponents()
{
    Super::PostInitializeComponents();
    HealthComponent->OnDeath.AddDynamic(this, &AMyCharacter::HandleDeath);
}
```

### EndPlay — reasons matter

| Reason | When |
|---|---|
| `Destroyed` | `Actor->Destroy()` called explicitly |
| `LevelTransition` | Map change |
| `EndPlayInEditor` | PIE session ended |
| `RemovedFromWorld` | Level streaming unloaded the sublevel |
| `Quit` | Application shutdown |

```cpp
void AMyActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    GetWorld()->GetTimerManager().ClearAllTimersForObject(this);
    Super::EndPlay(EndPlayReason);
}
```

### Network lifecycle note

**Replicated actors**: on clients, `BeginPlay` may fire before all replicated properties arrive. Use `OnRep_` callbacks for initialization that depends on replicated state. `PostNetReceive()` fires after each replication update (including the initial one); guard one-time setup inside it with a `bHasInitialized` flag. `PostNetInit` is not a standard `AActor` virtual and should not be used as a general init hook.

---

## Component System

### The three layers

| Class | Transform | Rendering/Collision | Use for |
|---|---|---|---|
| `UActorComponent` | No | No | Pure logic — health, inventory, AI data |
| `USceneComponent` | Yes | No | Transform anchors, grouping, pivot points |
| `UPrimitiveComponent` | Yes | Yes | Meshes, shapes, anything visible or collidable |

**Notable subclasses**: `UStaticMeshComponent`, `USkeletalMeshComponent`, shape primitives (`UCapsuleComponent`, `UBoxComponent`, `USphereComponent`), `UWidgetComponent` (3D UI in world space — requires `"UMG"` module), `USpringArmComponent` + `UCameraComponent`, `UChildActorComponent`. See `references/component-types.md`.

### Component creation

**In the constructor** (for default components that appear in the Details panel):

```cpp
AMyActor::AMyActor()
{
    // CreateDefaultSubobject registers the component as a subobject —
    // it is serialized with the actor and visible in Blueprint editors.
    MeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    SetRootComponent(MeshComp);

    ArrowComp = CreateDefaultSubobject<UArrowComponent>(TEXT("Arrow"));
    ArrowComp->SetupAttachment(MeshComp); // Parent set here; no world needed

    HealthComp = CreateDefaultSubobject<UHealthComponent>(TEXT("Health"));
    // Logic-only components need no attachment
}
```

**At runtime** (dynamic addition):

```cpp
void AMyActor::AddLight()
{
    // NewObject creates but does NOT register with the world
    UPointLightComponent* Light = NewObject<UPointLightComponent>(this,
        UPointLightComponent::StaticClass(), TEXT("DynamicLight"));

    Light->SetupAttachment(GetRootComponent());
    Light->RegisterComponent(); // Gives it world presence (render proxy, physics)
    Light->SetIntensity(5000.f);
}

void AMyActor::RemoveLight(UActorComponent* Comp)
{
    Comp->DestroyComponent(); // Unregisters and marks for GC
}

// UnregisterComponent() removes a component from the world without destroying it (reversible).
// DestroyComponent() marks it for GC — irreversible. Use Unregister when you may re-enable it later.
```

Why this distinction matters: constructor-created components are owned subobjects and participate in the actor's GC root. Runtime components via `NewObject` are not automatically serialized unless you add them to a `UPROPERTY` array.

### Attachment

```cpp
// Constructor (SetupAttachment — no world required)
SpringArmComp->SetupAttachment(RootComponent);
CameraComp->SetupAttachment(SpringArmComp);

// Runtime (AttachToComponent — world must exist)
WeaponMesh->AttachToComponent(
    CharMesh,
    FAttachmentTransformRules::SnapToTargetNotIncludingScale,
    TEXT("WeaponSocket")  // Named socket on the skeletal mesh
);

WeaponMesh->DetachFromComponent(FDetachmentTransformRules::KeepWorldTransform);
```

### Activation

```cpp
// In constructor — opt out of auto-activation for optional components
SoundComp->bAutoActivate = false;

// Runtime — Activate() checks ShouldActivate() internally
SoundComp->Activate();
SoundComp->Deactivate();
SoundComp->SetActive(true, /*bReset=*/false);
```

---

## Spawning

### Standard spawn

```cpp
FActorSpawnParameters Params;
Params.Owner = this;
Params.Instigator = GetInstigator();
Params.SpawnCollisionHandlingOverride =
    ESpawnActorCollisionHandlingMethod::AdjustIfPossibleButAlwaysSpawn;
Params.Name = FName("Enemy_Boss");  // deterministic name for replication (must be unique)

AEnemy* Enemy = GetWorld()->SpawnActor<AEnemy>(
    AEnemy::StaticClass(), Location, Rotation, Params);
```

### Deferred spawning — configure before BeginPlay

Use when the actor's `BeginPlay` reads data that must be set before it runs.

```cpp
AEnemy* Enemy = GetWorld()->SpawnActorDeferred<AEnemy>(
    AEnemy::StaticClass(), SpawnTransform, Owner, Instigator,
    ESpawnActorCollisionHandlingMethod::AlwaysSpawn);

if (Enemy)
{
    Enemy->SetEnemyData(EnemyDataAsset); // Set BEFORE BeginPlay
    Enemy->FinishSpawning(SpawnTransform);
    // FinishSpawning triggers PostInitializeComponents then BeginPlay
}
```

### Object pooling

For high-frequency actors (projectiles, shell casings), repeated `SpawnActor`/`Destroy` creates GC pressure. Pool them: pre-spawn, hide + disable collision to "return," re-enable to "reuse."

```cpp
AProjectile* AProjectilePool::Get()
{
    for (AProjectile* P : Pool)
    {
        // IsHidden() reflects the pool's "inactive" state set on return.
        // IsActive() exists only on UActorComponent, not on AActor.
        if (P->IsHidden())
        {
            P->SetActorHiddenInGame(false);
            P->SetActorEnableCollision(true);
            return P;
        }
    }
    AProjectile* New = GetWorld()->SpawnActor<AProjectile>(ProjectileClass, ...);
    Pool.Add(New);
    return New;
}
```

---

## Ticking

### Setup

```cpp
AMyActor::AMyActor()
{
    PrimaryActorTick.bCanEverTick = true;
    PrimaryActorTick.bStartWithTickEnabled = false; // Enable in BeginPlay
    PrimaryActorTick.TickInterval = 0.1f;           // ~10 Hz throttle
    PrimaryActorTick.TickGroup = TG_PostPhysics;    // After physics settles
}
```

Tick groups: `TG_PrePhysics` (default, input/movement) → `TG_DuringPhysics` (physics-coupled logic, runs during physics step) → `TG_PostPhysics` (camera, IK) → `TG_PostUpdateWork` (final reads).

**Component tick**: Set `PrimaryComponentTick.bCanEverTick = true` in the component constructor, with `PrimaryComponentTick.TickGroup` for ordering — same API as actor tick.

### Tick dependencies

```cpp
// ActorA ticks after ActorB completes
ActorA->AddTickPrerequisiteActor(ActorB);
ComponentA->AddTickPrerequisiteComponent(ComponentB);
```

### When NOT to tick

Tick has per-frame cost even when nothing changes. Prefer:

```cpp
// Delayed/repeating events → FTimerHandle
GetWorld()->GetTimerManager().SetTimer(TimerHandle, this,
    &AMyActor::OnTimerFired, 2.0f, /*bLoop=*/true);

// State changes → delegates / multicast delegates
HealthComp->OnDeath.AddDynamic(this, &AMyActor::HandleDeath);

// Collision events → OnComponentBeginOverlap / OnActorBeginOverlap
```

Only tick for true per-frame needs: smooth interpolation, physics sub-stepping, streaming queries.

---

## Interfaces (UINTERFACE Pattern)

Interfaces let unrelated actor types respond to the same message without coupling through inheritance. This replaces `Cast<ASpecificType>` scattered across your codebase.

### Declaration

```cpp
// IInteractable.h
UINTERFACE(MinimalAPI, Blueprintable)
class UInteractable : public UInterface { GENERATED_BODY() };

class MYGAME_API IInteractable
{
    GENERATED_BODY()
public:
    // BlueprintNativeEvent: C++ default + Blueprint can override
    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category="Interaction")
    void OnInteract(AActor* Instigator);
};
```

### Implementation

```cpp
// AChest.h
UCLASS()
class AChest : public AActor, public IInteractable
{
    GENERATED_BODY()
public:
    virtual void OnInteract_Implementation(AActor* Instigator) override;
};
```

### Calling through the interface

```cpp
// No cast needed — works on any actor or component
if (Target->Implements<UInteractable>())
{
    // Execute_ prefix required for Blueprint-callable interface functions
    IInteractable::Execute_OnInteract(Target, GetPawn());
}
```

**Interface vs component**: use an interface for a *capability declaration* ("this can be interacted with") especially when Blueprint classes need to implement it. Use a component when the behavior has its own state, needs ticking, or is reused identically by many actor types.

---

## Composition Patterns

### Favor components over deep inheritance

```cpp
// Wrong: inheritance hierarchy collapses under varied requirements
ACharacter → AHero → ASwordHero → AFireSwordHero

// Right: flat base + composed components
ABaseCharacter
  + UHealthComponent     (HP, damage, death event)
  + UInventoryComponent  (items, equipment)
  + UAbilityComponent    (skill execution)
  + UStatusComponent     (buffs/debuffs)
```

### Component-to-component communication

Components should not hold raw pointers to siblings. Query through the owner or use delegates:

```cpp
// Query approach
UHealthComponent* Health = GetOwner()->FindComponentByClass<UHealthComponent>();

// Delegate approach — total decoupling
HealthComp->OnDeath.AddDynamic(AbilityComp, &UAbilityComponent::OnOwnerDied);
```

### Data-driven composition

```cpp
// UEnemyData (UDataAsset) — varies per enemy type
// AEnemy reads configuration at BeginPlay or via SpawnActorDeferred

void AEnemy::Initialize(UEnemyData* Data)
{
    HealthComp->SetMaxHealth(Data->MaxHealth);

    for (TSubclassOf<UActorComponent> CompClass : Data->AdditionalComponents)
    {
        UActorComponent* Comp = NewObject<UActorComponent>(this, CompClass);
        Comp->RegisterComponent();
    }
}
```

---

## Common Mistakes and Anti-Patterns

### Inheritance abuse

```cpp
// Wrong — one class per variant
UCLASS() class AFireEnemy : public AEnemy { };
UCLASS() class AIceEnemy  : public AEnemy { };

// Right — one class, multiple DataAssets
// UEnemyData_Fire.uasset, UEnemyData_Ice.uasset → AEnemy reads at BeginPlay
```

### Tick polling instead of events

```cpp
// Wrong — checked every frame
void AMyActor::Tick(float DeltaTime)
{
    if (HealthComp->IsDead()) { HandleDeath(); }
}

// Right — event-driven, zero per-frame cost
void AMyActor::BeginPlay()
{
    Super::BeginPlay();
    HealthComp->OnDeath.AddDynamic(this, &AMyActor::HandleDeath);
    SetActorTickEnabled(false);
}
```

### Forgetting Super in lifecycle overrides

Every lifecycle override must call `Super::`. Skipping it breaks replication, GC, and Blueprint event forwarding.

```cpp
// Always
void AMyActor::BeginPlay()  { Super::BeginPlay(); ... }
void AMyActor::EndPlay(...) { ...; Super::EndPlay(EndPlayReason); }
void AMyActor::PostInitializeComponents() { Super::PostInitializeComponents(); ... }
```

### Storing raw actor pointers

```cpp
// Wrong — crashes when the actor is destroyed
AActor* CachedTarget;

// Right — use TWeakObjectPtr and check IsValid before use
TWeakObjectPtr<AActor> CachedTarget;
if (CachedTarget.IsValid()) { CachedTarget->DoSomething(); }
```

---

## Related Skills

- `ue-cpp-foundations` — UCLASS, UPROPERTY, UFUNCTION macros underpinning all patterns above
- `ue-gameplay-framework` — GameMode, PlayerController, Pawn layered on top of this system
- `ue-physics-collision` — UPrimitiveComponent channels, sweeps, overlap events

---

## Quick Reference

```
Constructor          CreateDefaultSubobject, SetRootComponent, tick config
PostInitialize       Bind delegates to own components; world accessible
BeginPlay            Full game logic; SpawnActor; timer setup
Tick                 Per-frame only; prefer timers/events
EndPlay              ClearAllTimers; Super required
Destroyed            Pre-GC; minimal logic

CreateDefaultSubobject<T>()          Constructor — owned, serialized, editable
NewObject<T>() + RegisterComponent() Runtime — dynamic, not auto-serialized
SetupAttachment()                    Constructor parent declaration
AttachToComponent()                  Runtime attachment with transform rules

SpawnActor<T>()                      Standard spawn
SpawnActorDeferred<T>() + Finish     Configure before BeginPlay fires
```
