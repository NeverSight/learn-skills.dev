---
name: ue-mass-entity
description: "Use this skill when working with Mass Entity, MassEntity, Mass AI, MassProcessor, MassFragment, MassTag, MassObserver, MassSpawner, MassCrowd, Mass ECS, entity archetype, ForEachEntityChunk, FMassEntityQuery, FMassEntityManager, ISM crowd, or large-scale entity simulation in Unreal Engine. See references/mass-entity-patterns.md for processor and observer templates. See references/mass-fragment-reference.md for built-in fragment types."
metadata:
  version: 1.0.0
---

# UE Mass Entity Framework

You are an expert in Unreal Engine's Mass Entity framework -- an archetype-based Entity Component System (ECS) designed for high-performance simulation of thousands of entities using cache-friendly data layouts and parallel processing.

## Context Check

Before proceeding, read `.agents/ue-project-context.md` to determine:
- Whether the MassEntity plugin is enabled (and MassAI, MassCrowd, MassGameplay if needed)
- The target entity count and performance budget
- Whether MassCrowd lane navigation or ZoneGraph is in use
- Existing processors, fragments, traits, and entity config assets

## Information Gathering

Ask the developer:
1. What kind of entities are being simulated? (crowds, projectiles, traffic, wildlife, custom)
2. What data does each entity carry? (position, velocity, health, custom state)
3. Are entities visualized? If so, what LOD strategy? (ISM, skeletal, actor promotion)
4. Is this multiplayer? If so, which entities replicate?
5. How many entities at peak? (hundreds vs. tens of thousands)

---

## ECS Concepts

Mass Entity uses an archetype ECS model where entity composition determines memory layout:

| Concept | Class Base | Purpose |
|---------|-----------|---------|
| Entity | `FMassEntityHandle` | 8-byte identity handle (Index + SerialNumber) |
| Fragment | `FMassFragment` | Per-entity mutable data (position, velocity, health) |
| Tag | `FMassTag` | Zero-size boolean marker for filtering |
| Shared Fragment | `FMassSharedFragment` | Per-archetype mutable data |
| Const Shared Fragment | `FMassConstSharedFragment` | Per-archetype immutable data (mesh params) |
| Chunk Fragment | `FMassChunkFragment` | Per-memory-chunk data (custom chunk-level state) |
| Archetype | `FMassArchetypeHandle` | Unique combination of fragment/tag types |

**Why archetypes matter:** Entities with identical fragment/tag composition share the same archetype. All fragments of the same type within a chunk are stored contiguously, enabling cache-friendly iteration over thousands of entities per frame.

---

## Fragment and Tag Definitions

All types require `USTRUCT()` with `GENERATED_BODY()`:

```cpp
// Per-entity mutable data
USTRUCT()
struct FHealthFragment : public FMassFragment
{
    GENERATED_BODY()
    float Current = 100.f;
    float Max = 100.f;
};

// Zero-size marker — no data members
USTRUCT()
struct FDeadTag : public FMassTag
{
    GENERATED_BODY()
};

// Shared across all entities in an archetype (mutable)
USTRUCT()
struct FTeamSharedFragment : public FMassSharedFragment
{
    GENERATED_BODY()
    int32 TeamID = 0;
};
```

**Chunk fragments** (`FMassChunkFragment`) store per-memory-chunk state shared across all entities in a chunk. Note: `FMassRepresentationLODFragment` inherits from `FMassFragment` (per-entity), not `FMassChunkFragment`. **Const shared fragments** (`FMassConstSharedFragment`) are immutable after archetype creation -- use for configuration data like `FMassRepresentationParameters`. See `references/mass-fragment-reference.md` for built-in types.

---

## FMassEntityManager

The entity manager is NOT a `UObject` -- it is a struct (`TSharedFromThis<FMassEntityManager>`, `FGCObject`). Access it through `UMassEntitySubsystem` (a `UWorldSubsystem`):

```cpp
UMassEntitySubsystem* MassSubsystem = GetWorld()->GetSubsystem<UMassEntitySubsystem>();
FMassEntityManager& EntityManager = MassSubsystem->GetMutableEntityManager();
// const ref: MassSubsystem->GetEntityManager()
```

### Entity Lifecycle

```cpp
// One-shot creation
FMassEntityHandle Entity = EntityManager.CreateEntity(ArchetypeHandle);

// With shared fragments
FMassArchetypeSharedFragmentValues SharedValues;
FMassEntityHandle Entity = EntityManager.CreateEntity(ArchetypeHandle, SharedValues);

// Two-phase (reserve then build)
FMassEntityHandle Handle = EntityManager.ReserveEntity();
EntityManager.BuildEntity(Handle, ArchetypeHandle);

// Batch creation (thousands at once)
// BatchCreateEntities returns TSharedRef<FEntityCreationContext> — retain it until
// observer processors should fire (dropping it early suppresses observer execution).
TArray<FMassEntityHandle> Entities;
TSharedRef<FEntityCreationContext> CreationContext =
    EntityManager.BatchCreateEntities(ArchetypeHandle, 5000, Entities);

// Destruction
EntityManager.DestroyEntity(Handle);
EntityManager.BatchDestroyEntities(EntityArray);
```

### Validity Checks

`FMassEntityHandle::IsSet()` (aliased as `IsValid()`) only checks non-zero Index/SerialNumber -- it does NOT verify the entity exists. Always use the entity manager:

```cpp
EntityManager.IsEntityValid(Handle)   // entity exists
EntityManager.IsEntityBuilt(Handle)   // fully constructed
EntityManager.IsEntityActive(Handle)  // active in simulation
```

### Direct Fragment/Tag Mutations (Outside Processors)

```cpp
EntityManager.AddFragmentToEntity(Handle, FHealthFragment::StaticStruct());
EntityManager.RemoveFragmentFromEntity(Handle, FHealthFragment::StaticStruct());
EntityManager.AddTagToEntity(Handle, FDeadTag::StaticStruct());
EntityManager.RemoveTagFromEntity(Handle, FDeadTag::StaticStruct());
EntityManager.SwapTagsForEntity(Handle, FOldTag::StaticStruct(), FNewTag::StaticStruct());
```

---

## UMassProcessor

Processors iterate over entities matching a query each frame. Subclass `UMassProcessor` (abstract), override `ConfigureQueries()` and `Execute()`:

```cpp
UCLASS()
class UMyMovementProcessor : public UMassProcessor
{
    GENERATED_BODY()
public:
    UMyMovementProcessor();
protected:
    virtual void ConfigureQueries(const TSharedRef<FMassEntityManager>& EntityManager) override;
    virtual void Execute(FMassEntityManager& EntityManager,
                         FMassExecutionContext& Context) override;
private:
    FMassEntityQuery MovementQuery;
};
```

### Constructor Configuration

```cpp
UMyMovementProcessor::UMyMovementProcessor()
{
    ProcessingPhase = EMassProcessingPhase::PrePhysics;
    ExecutionFlags = static_cast<int32>(
        EProcessorExecutionFlags::Server |
        EProcessorExecutionFlags::Standalone);
    ExecutionOrder.ExecuteInGroup = UE::Mass::ProcessorGroupNames::Movement;
    ExecutionOrder.ExecuteAfter.Add(TEXT("UMassApplyVelocityProcessor"));
    bRequiresGameThreadExecution = false; // true if accessing UObjects
}
```

**`EMassProcessingPhase`:** `PrePhysics`, `StartPhysics`, `DuringPhysics`, `EndPhysics`, `PostPhysics`, `FrameEnd`

**`EProcessorExecutionFlags`:** `None`(0), `Standalone`(1), `Server`(2), `Client`(4), `Editor`(8), `AllNetModes`(7 = Standalone|Server|Client)

**Execution ordering:** `ExecutionOrder.ExecuteInGroup`, `ExecuteAfter`, `ExecuteBefore` control processor scheduling relative to named groups and other processors.

---

## FMassEntityQuery

Queries define which entities a processor operates on. Configure in `ConfigureQueries()`, then call `RegisterQuery()`:

```cpp
void UMyMovementProcessor::ConfigureQueries(const TSharedRef<FMassEntityManager>& EntityManager)
{
    MovementQuery.AddRequirement<FTransformFragment>(
        EMassFragmentAccess::ReadWrite, EMassFragmentPresence::All);
    MovementQuery.AddRequirement<FMassVelocityFragment>(
        EMassFragmentAccess::ReadOnly, EMassFragmentPresence::All);
    MovementQuery.AddRequirement<FHealthFragment>(
        EMassFragmentAccess::ReadOnly, EMassFragmentPresence::Optional);
    MovementQuery.AddTagRequirement<FDeadTag>(EMassFragmentPresence::None);
    MovementQuery.AddSharedRequirement<FTeamSharedFragment>(
        EMassFragmentAccess::ReadOnly, EMassFragmentPresence::All);
    MovementQuery.AddConstSharedRequirement<FMassRepresentationParameters>(
        EMassFragmentPresence::All);
    MovementQuery.AddRequirement<FMassRepresentationLODFragment>(
        EMassFragmentAccess::ReadWrite, EMassFragmentPresence::Optional);
    MovementQuery.AddSubsystemRequirement<UMassRepresentationSubsystem>(
        EMassFragmentAccess::ReadWrite);
    RegisterQuery(MovementQuery);
}
```

| `EMassFragmentAccess` | Usage |
|----------------------|-------|
| `None` | No access (filter only) |
| `ReadOnly` | `GetFragmentView<T>()` -- `TConstArrayView` |
| `ReadWrite` | `GetMutableFragmentView<T>()` -- `TArrayView` |

| `EMassFragmentPresence` | Meaning |
|------------------------|---------|
| `All` | Entity must have this fragment |
| `Any` | At least one `Any`-marked fragment must exist |
| `None` | Entity must NOT have this fragment |
| `Optional` | Access if present, skip if absent |

### Fragment-Based Chunk Filtering

```cpp
// FMassRepresentationLODFragment is a per-entity fragment, not a chunk fragment.
// Filter using a regular fragment view within the iteration lambda.
MovementQuery.SetChunkFilter([](const FMassExecutionContext& Context) -> bool {
    // Chunk filters operate on chunk-level data; use per-entity access inside ForEachEntityChunk.
    return true;
});
```

---

## FMassExecutionContext and Iteration

Inside `ForEachEntityChunk`, the context provides typed views into chunk data:

```cpp
void UMyMovementProcessor::Execute(FMassEntityManager& EntityManager,
                                   FMassExecutionContext& Context)
{
    MovementQuery.ForEachEntityChunk(Context,
        [this](FMassExecutionContext& Context)
    {
        const int32 NumEntities = Context.GetNumEntities();
        TArrayView<FTransformFragment> Transforms =
            Context.GetMutableFragmentView<FTransformFragment>();
        TConstArrayView<FMassVelocityFragment> Velocities =
            Context.GetFragmentView<FMassVelocityFragment>();
        TConstArrayView<FMassEntityHandle> Entities = Context.GetEntities();
        const float DeltaTime = Context.GetDeltaTimeSeconds();

        for (int32 i = 0; i < NumEntities; ++i)
        {
            Transforms[i].GetMutableTransform().AddToTranslation(
                Velocities[i].Value * DeltaTime);
        }
    });
}
```

**Parallel execution:** `MovementQuery.ParallelForEachEntityChunk(Context, Lambda)` for thread-safe processors.

**Subsystem access:** `Context.GetMutableSubsystem<T>()` / `Context.GetSubsystem<T>()` for subsystems declared via `AddSubsystemRequirement`.

**Shared/chunk access:** `Context.GetMutableSharedFragment<T>()`, `Context.GetConstSharedFragment<T>()`, `Context.GetChunkFragment<T>()`.

---

## FMassCommandBuffer (Deferred Mutations)

**CRITICAL:** Inside `ForEachEntityChunk`, never call entity manager mutations directly. Structural changes during iteration invalidate archetype memory layouts, causing undefined behavior. Use `Context.Defer()`:

```cpp
MovementQuery.ForEachEntityChunk(Context,
    [](FMassExecutionContext& Context)
{
    auto Transforms = Context.GetMutableFragmentView<FTransformFragment>();
    auto Entities = Context.GetEntities();
    for (int32 i = 0; i < Context.GetNumEntities(); ++i)
    {
        if (Transforms[i].GetTransform().GetLocation().Z < -1000.f)
        {
            Context.Defer().AddTag<FDeadTag>(Entities[i]);
            Context.Defer().RemoveFragment<FHealthFragment>(Entities[i]);
        }
    }
});
```

Deferred command execution order: **Create -> Add -> Remove -> ChangeComposition -> Set -> Destroy**. This guarantees fragments exist before being written, and entities exist before being modified.

`PushCommand<T>(Command)` pushes a typed deferred command. Note: `PushCommand` does NOT accept a lambda. For custom deferred logic, use `PushUniqueCommand(TUniquePtr<FMassBatchedCommand>&&)` with a subclass of `FMassBatchedCommand`. See `references/mass-entity-patterns.md` for patterns.

---

## UMassObserverProcessor

Observers react to structural changes -- when a fragment or tag is added to or removed from an entity. They fire automatically:

```cpp
UCLASS()
class UHealthAddedObserver : public UMassObserverProcessor
{
    GENERATED_BODY()
public:
    UHealthAddedObserver()
    {
        ObservedType = FHealthFragment::StaticStruct();
        ObservedOperations = EMassObservedOperationFlags::AddElement;
    }
protected:
    virtual void ConfigureQueries(const TSharedRef<FMassEntityManager>& EntityManager) override;
    virtual void Execute(FMassEntityManager& EntityManager,
                         FMassExecutionContext& Context) override;
};
```

The observer `Execute` runs only for entities that just had the observed type added/removed. Use observers for initialization, cleanup, and state-change responses instead of per-frame polling.

---

## FMassEntityView

For single-entity access outside processor iteration, use `FMassEntityView`. It is transient -- never store across frames because archetype memory can relocate:

```cpp
if (EntityManager.IsEntityValid(Handle))
{
    FMassEntityView View(EntityManager, Handle);
    if (View.GetFragmentDataPtr<FHealthFragment>() != nullptr)
    {
        FHealthFragment& Health = View.GetFragmentData<FHealthFragment>();
        Health.Current -= Damage;
    }
    bool bDead = View.HasTag<FDeadTag>();
}
```

---

## Mass Spawner and Config Assets

`UMassEntityConfigAsset` defines entity templates via traits. Add traits like `UMassAssortedFragmentsTrait` (custom fragments), `UMassVisualizationTrait` (ISM visualization), or `UMassReplicationTrait` (networking).

Custom traits subclass `UMassEntityTraitBase` and override `BuildTemplate(FMassEntityTemplateBuildContext&, const UWorld&)` to add fragments and configure archetypes. `ValidateTemplate()` provides editor-time validation.

`AMassSpawner` is a world actor that references entity config assets and controls spawn count, timing, and spatial distribution. See `references/mass-entity-patterns.md` for trait implementation templates.

---

## Common Fragments

| Fragment | Type | Purpose |
|----------|------|---------|
| `FTransformFragment` | Fragment | Entity world transform |
| `FMassVelocityFragment` | Fragment | Linear velocity |
| `FMassForceFragment` | Fragment | Applied force |
| `FAgentRadiusFragment` | Fragment | Agent collision radius |
| `FMassMoveTargetFragment` | Fragment | Navigation move target |
| `FMassRepresentationFragment` | Fragment | Current visual representation state |
| `FMassRepresentationLODFragment` | Fragment | Per-entity LOD level and visibility state |
| `FMassRepresentationParameters` | Const Shared | Representation type per LOD, update rate config |
| `FMassMovementParameters` | Const Shared | Max speed, acceleration |

See `references/mass-fragment-reference.md` for complete field details and trait types.

---

## Representation (ISM Visualization)

Mass Entity uses Instanced Static Meshes for rendering thousands of entities without per-entity actors:

| `EMassRepresentationType` | Usage |
|--------------------------|-------|
| `StaticMeshInstance` | ISM for mid/far entities |
| `HighResSpawnedActor` | Full actor for close-up (high LOD) |
| `LowResSpawnedActor` | Reduced actor for medium LOD |
| `None` | No visual representation |

| `EMassLOD` | Detail Level |
|------------|-------------|
| `High` | Full detail, actor-based |
| `Medium` | Reduced detail |
| `Low` | Minimal (ISM only) |
| `Off` | Not rendered |

`UMassRepresentationSubsystem` manages ISM instances. Use `UMassVisualizationTrait` on entity configs to set meshes and LOD distances. Force game-thread for representation processors: `TMassSharedFragmentTraits<T>::GameThreadOnly = true`.

---

## MassCrowd

`UMassCrowdSubsystem` provides lane-based navigation using ZoneGraph for pedestrian crowd simulation. Located in `Engine/Plugins/AI/MassCrowd/` (not Runtime).

Key features: lane state management, waiting slot allocation, density tracking, and avoidance. Thread-safe for parallel processors: `TMassExternalSubsystemTraits<UMassCrowdSubsystem>::GameThreadOnly = false`.

Entities use `FMassMoveTargetFragment` for lane-following targets. ZoneGraph defines navigation lanes as connected graphs with automatic density management.

---

## StateTree Integration

Mass Entity processors can trigger State Tree evaluations for entity AI. State Trees provide hierarchical decision-making for Mass entities as an alternative to per-entity behavior trees (prohibitively expensive at scale). For State Tree architecture and task patterns, see `ue-state-trees`.

---

## Common Mistakes

**Direct mutations inside ForEachEntityChunk:**

```cpp
// WRONG: direct mutation during iteration — undefined behavior
Query.ForEachEntityChunk(Context,
    [&EntityManager](FMassExecutionContext& Context) {
    EntityManager.AddFragmentToEntity(Context.GetEntities()[0],
        FHealthFragment::StaticStruct()); // CRASH
});
// RIGHT: use deferred commands
Query.ForEachEntityChunk(Context,
    [](FMassExecutionContext& Context) {
    Context.Defer().AddFragment<FHealthFragment>(Context.GetEntities()[0]);
});
```

**Storing FMassEntityView across frames:** Entity views are transient. Archetype memory may relocate between frames, invalidating stored views. Create a fresh `FMassEntityView` each time.

**Using IsSet/IsValid for existence:** `Handle.IsSet()` only checks non-zero fields. A destroyed entity's handle still returns true. Use `EntityManager.IsEntityValid(Handle)`.

**Missing RegisterQuery:** Forgetting `RegisterQuery(MyQuery)` in `ConfigureQueries()` silently skips the query. Every query used in `Execute` must be registered.

**UObject access without game-thread flag:** Accessing `UObject` properties from a parallel processor causes races. Set `bRequiresGameThreadExecution = true` or declare dependencies via `AddSubsystemRequirement`.

**Fragment access mismatch:** `ReadOnly` access + `GetMutableFragmentView<T>()` triggers an assertion. Match access mode to view type.

---

## Reference Files

- `references/mass-entity-patterns.md` -- Processor, observer, trait, and deferred command code templates
- `references/mass-fragment-reference.md` -- Built-in fragment types, shared fragments, and trait classes

## Related Skills

- `ue-ai-navigation` -- NavMesh pathfinding and AI perception for Mass agents
- `ue-procedural-generation` -- PCG and ISM patterns relevant to Mass representation
- `ue-gameplay-framework` -- GameMode/GameState interaction with Mass simulation
- `ue-actor-component-architecture` -- Actor-entity bridging via MassAgentComponent
- `ue-async-threading` -- Parallel execution patterns and thread safety
- `ue-cpp-foundations` -- USTRUCT, UCLASS, subsystem patterns
