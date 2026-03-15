---
name: ue-state-trees
description: "Use this skill when working with State Tree, StateTree, UStateTree, state machine, StateTreeTask, StateTreeCondition, StateTreeEvaluator, StateTreeSchema, AI State Tree, Mass StateTree, FStateTreeExecutionContext, or data-driven state logic in Unreal Engine. See references/state-tree-patterns.md for task/condition/evaluator templates and references/state-tree-mass-integration.md for Mass Entity integration."
metadata:
  version: 1.0.0
---

# UE State Trees

You are an expert in Unreal Engine's State Tree system for building flexible, data-driven state machines.

## Context Check

Read `.agents/ue-project-context.md` to determine:
- Whether `StateTreeModule` and `GameplayStateTreeModule` plugins are enabled
- If Mass Entity integration is needed (`MassEntity`, `MassAIBehavior` plugins)
- Existing AI frameworks — behavior trees, custom FSMs to migrate from
- Schema types in use and any custom schemas

## Information Gathering

Before implementing, clarify:
1. What is the use case? (AI behavior, game logic, UI state, entity processing)
2. What scale? (single actor with `UStateTreeComponent` vs thousands of Mass entities)
3. How complex? (simple linear FSM vs hierarchical states with linked subtrees)
4. Are there existing behavior trees to migrate from?
5. What external data do tasks need? (actor references, subsystems, world state)

---

## StateTree Architecture

A State Tree is a hierarchical finite state machine authored as a `UStateTree` data asset:

```
UStateTree (UDataAsset)
  ├── UStateTreeSchema         ← defines allowed context/external data
  ├── States[]                 ← hierarchical state tree
  │     ├── Tasks[]            ← work performed while state is active
  │     ├── Transitions[]      ← rules for leaving this state
  │     └── Conditions[]       ← gates on transitions
  ├── Evaluators[]             ← global data providers (tick before transitions)
  └── Parameters               ← FInstancedPropertyBag default inputs
```

**Runtime flow per tick:** 1) Evaluators tick, 2) Transitions checked from active leaf up to root, 3) If transition fires: ExitState on old tasks then EnterState on new, 4) Active tasks tick.

**Key classes:**

| Class | Role |
|-------|------|
| `UStateTree` | Data asset — call `IsReadyToRun()` before execution |
| `FStateTreeExecutionContext` | Per-tick context — constructed each frame, NOT persisted |
| `FStateTreeInstanceData` | Persistent runtime state — survives across ticks |
| `UStateTreeComponent` | Actor component that manages tree lifecycle |
| `EStateTreeRunStatus` | `Running`, `Stopped`, `Succeeded`, `Failed`, `Unset` |

**Build.cs modules**: `StateTreeModule`, `GameplayStateTreeModule`

The execution context is constructed per-tick from persistent instance data:
```cpp
FStateTreeInstanceData InstanceData;  // persists across frames
// Each tick:
FStateTreeExecutionContext Context(Owner, *StateTree, InstanceData);
Context.Tick(DeltaTime);
```

This separates mutable state (`FStateTreeInstanceData`) from stateless execution logic, making State Trees safe for parallel evaluation in Mass Entity scenarios.

---

## Schema System

Schemas define what context data a State Tree can access, constraining valid tasks and conditions. This prevents authoring errors at edit time rather than runtime.

| Schema | Context Provided | Use Case |
|--------|-----------------|----------|
| `UStateTreeComponentSchema` | Actor + BrainComponent | General actor logic |
| `UStateTreeAIComponentSchema` | Above + `AIControllerClass` | AI behavior |
| `UMassStateTreeSchema` | Mass entity context | Mass Entity processing |

`UStateTreeComponentSchema` exposes `ContextActorClass` (`TSubclassOf<AActor>`) so the editor knows which components are available for property binding. `UStateTreeAIComponentSchema` extends it with `AIControllerClass` (`TSubclassOf<AAIController>`).

### Custom Schemas

Subclass `UStateTreeSchema` for project-specific trees:

```cpp
UCLASS()
class UMyGameSchema : public UStateTreeSchema
{
    GENERATED_BODY()
public:
    virtual bool IsStructAllowed(const UScriptStruct* InStruct) const override;
    virtual bool IsExternalItemAllowed(const UStruct& InStruct) const override;
    virtual TConstArrayView<FStateTreeExternalDataDesc> GetContextDataDescs() const override;

#if WITH_EDITOR
    virtual bool AllowEvaluators() const override { return true; }
    virtual bool AllowMultipleTasks() const override { return true; }
    virtual bool AllowGlobalParameters() const override { return true; }
#endif // WITH_EDITOR
};
```

Override `GetContextDataDescs()` to declare context objects (actor refs, subsystems). The editor uses this to validate property bindings.

---

## Tasks

Tasks are the primary work units in a state. They are USTRUCTs (not UObjects), making them lightweight and cache-friendly.

### FStateTreeTaskBase API

Key virtuals (all `const` — tasks are immutable at runtime):

| Virtual | Returns | Called When |
|---------|---------|-------------|
| `EnterState(Context, Transition)` | `EStateTreeRunStatus` (default: Running) | State becomes active |
| `ExitState(Context, Transition)` | `void` | State is exited |
| `Tick(Context, DeltaTime)` | `EStateTreeRunStatus` (default: Running) | Each frame (if `bShouldCallTick`) |
| `StateCompleted(Context, Status, CompletedStates)` | `void` | Child state completes (REVERSE order) |
| `TriggerTransitions(Context)` | `void` | Only if `bShouldAffectTransitions` |

### Behavioral Flags

| Flag | Default | Purpose |
|------|---------|---------|
| `bShouldStateChangeOnReselect` | `true` | Exit+Enter when transitioning to same state |
| `bShouldCallTick` | `true` | Enable per-frame Tick calls |
| `bShouldCallTickOnlyOnEvents` | `false` | Tick only when events are pending |
| `bShouldCopyBoundPropertiesOnTick` | `true` | Refresh property bindings each tick |
| `bShouldAffectTransitions` | `false` | Enable `TriggerTransitions` calls |

Set `bShouldCallTick = false` for fire-and-forget tasks that only need `EnterState`/`ExitState`.

### Instance Data Pattern

Tasks are `const` at runtime — mutable per-instance state lives in a separate struct via the `typedef FInstanceDataType` pattern:

```cpp
USTRUCT()
struct FMyTaskInstanceData
{
    GENERATED_BODY()
    float ElapsedTime = 0.f;
};

USTRUCT(meta=(DisplayName="My Custom Task"))
struct FMyTask : public FStateTreeTaskBase
{
    GENERATED_BODY()
    typedef FMyTaskInstanceData FInstanceDataType;  // required — framework allocates storage

    virtual EStateTreeRunStatus EnterState(FStateTreeExecutionContext& Context,
        const FStateTreeTransitionResult& Transition) const override
    {
        FInstanceDataType& Data = Context.GetInstanceData(*this);
        Data.ElapsedTime = 0.f;
        return EStateTreeRunStatus::Running;
    }

    virtual EStateTreeRunStatus Tick(FStateTreeExecutionContext& Context,
        float DeltaTime) const override
    {
        FInstanceDataType& Data = Context.GetInstanceData(*this);
        Data.ElapsedTime += DeltaTime;
        return Data.ElapsedTime >= Duration
            ? EStateTreeRunStatus::Succeeded : EStateTreeRunStatus::Running;
    }

    UPROPERTY(EditAnywhere, Category = "Parameter")
    float Duration = 2.0f;
};
```

See `references/state-tree-patterns.md` for complete task, condition, and evaluator templates.

### Multiple Tasks Per State

When `AllowMultipleTasks()` is true, a state runs several tasks simultaneously. Any task returning `Failed` fails the state immediately; all must return `Succeeded` for the state to succeed.

---

## Conditions

Conditions gate transitions — evaluated to determine whether a transition should fire.

```cpp
USTRUCT(meta=(Hidden))
struct FStateTreeConditionBase : public FStateTreeNodeBase
{
    virtual bool TestCondition(FStateTreeExecutionContext& Context) const;  // default: false
    EStateTreeExpressionOperand Operand = EStateTreeExpressionOperand::And;
    int8 DeltaIndent = 0;  // indent level for logical grouping
    EStateTreeConditionEvaluationMode EvaluationMode = EStateTreeConditionEvaluationMode::Evaluated;
};
```

**Operands:** `And` (both must be true), `Or` (either), `Copy` (hidden/internal). `DeltaIndent` creates logical grouping — conditions at the same indent level are evaluated together, enabling `(A AND B) OR (C AND D)` without nesting.

**Built-in conditions:** `FStateTreeCompareIntCondition`, `FStateTreeCompareFloatCondition`, `FStateTreeCompareEnumCondition`, `FGameplayTagMatchCondition`, `FStateTreeObjectIsValidCondition`, `FStateTreeCompareDistanceCondition`. Bind inputs via property bindings.

---

## Evaluators

Evaluators run globally (not per-state) and execute **before** transitions and task ticks each frame. They inject external world data into the tree via property bindings, decoupling tasks from direct world queries.

```cpp
USTRUCT(meta=(Hidden))
struct FStateTreeEvaluatorBase : public FStateTreeNodeBase
{
    virtual void TreeStart(FStateTreeExecutionContext& Context) const;
    virtual void TreeStop(FStateTreeExecutionContext& Context) const;
    virtual void Tick(FStateTreeExecutionContext& Context, float DeltaTime) const;
    // Note: DeltaTime is 0 during preselection
};
```

Evaluators use the same `FInstanceDataType` typedef pattern as tasks. Their instance data properties can be bound to task/condition inputs in the editor: Evaluator populates data, tasks/conditions read it.

**When to use evaluators vs external data:** Evaluators for data that changes every frame (nearest enemy, world time). External data handles for stable references (owning actor, subsystem).

---

## Transitions

Transitions define how and when states change. Each state has an ordered list evaluated top-to-bottom — the first matching transition fires.

### Trigger Types

`EStateTreeTransitionTrigger` is a bitmask (`ENUM_CLASS_FLAGS`, supports bitwise OR):

| Trigger | Value | Fires When |
|---------|-------|------------|
| `OnStateSucceeded` | 1 | Active state returns Succeeded |
| `OnStateFailed` | 2 | Active state returns Failed |
| `OnStateCompleted` | 3 | Either Succeeded or Failed (1\|2) |
| `OnTick` | 4 | Every frame (gate with conditions) |
| `OnEvent` | 8 | Matching event in the queue |
| `OnDelegate` | 16 | Bound delegate fires |

### Priorities and Properties

`EStateTreeTransitionPriority`: `Low`, `Normal`, `Medium`, `High`, `Critical`. Higher-priority transitions on child states evaluate before lower-priority ones on parents.

| Property | Default | Purpose |
|----------|---------|---------|
| `bConsumeEventOnSelect` | `true` | Remove event from queue when transition fires |
| `bTransitionEnabled` | `true` | Disable without removing |
| `bReactivateTargetState` | `false` | Force Exit+Enter even if target is current state |

**Targets:** GotoState (specific named state), NextState (next sibling), Succeeded/Failed (complete parent with that status), or tree-root Succeeded/Failed to complete the entire tree.

---

## State Types and Selection

### State Types

| Type | Purpose |
|------|---------|
| `State` | Normal state with tasks, conditions, transitions |
| `Group` | Container for child states — no tasks of its own |
| `Linked` | References another state within the same tree |
| `LinkedAsset` | References a state in a different `UStateTree` asset |
| `Subtree` | Embeds another `UStateTree` as a child |

`LinkedAsset` is useful for sharing common behavior patterns (patrol, investigate, flee) across AI archetypes.

### Selection Behavior

`EStateTreeStateSelectionBehavior` controls how child states are chosen on entry:

| Behavior | Effect |
|----------|--------|
| `TryEnterState` | Enter this state directly |
| `TrySelectChildrenInOrder` | Try children top-to-bottom, first valid wins |
| `TrySelectChildrenAtRandom` | Random child selection |
| `TrySelectChildrenWithHighestUtility` | Utility-based selection (highest score) |
| `TrySelectChildrenAtRandomWeightedByUtility` | Weighted random by utility score |
| `TryFollowTransitions` | Follow transition chain |

`FStateTreeActiveStates::MaxStates = 8` — maximum depth of active state hierarchy. Stay within this limit.

---

## Events

State Trees use a GameplayTag-based event system for decoupled communication.

`FStateTreeEvent` contains: `FGameplayTag Tag`, `FInstancedStruct Payload` (optional typed data), `FName Origin` (optional sender name for debugging).

```cpp
// From outside via UStateTreeComponent
TreeComp->SendStateTreeEvent(FGameplayTag::RequestGameplayTag("AI.Alert"));

// With payload
FMyAlertData AlertData;
AlertData.ThreatLevel = 5;
TreeComp->SendStateTreeEvent(
    FGameplayTag::RequestGameplayTag("AI.Alert"),
    FConstStructView::Make(AlertData), TEXT("PerceptionSystem"));

// From inside a task via execution context
Context.SendEvent(Tag, FConstStructView::Make(ResultData), TEXT("MyTask"));
```

`FStateTreeEventQueue` holds up to `MaxActiveEvents = 64` events per tick. Events are processed during transition evaluation. Use `bConsumeEventOnSelect = true` (default) to prevent one event triggering multiple transitions.

---

## External Data

External data provides typed references to objects outside the tree (actors, components, subsystems) without going through evaluators.

```cpp
// Declare handles in your task/condition/evaluator struct
TStateTreeExternalDataHandle<FMyActorContext, EStateTreeExternalDataRequirement::Required> ActorHandle;
TStateTreeExternalDataHandle<FMySubsystemContext, EStateTreeExternalDataRequirement::Optional> SubsystemHandle;

// Link in the Link override
virtual bool Link(FStateTreeLinker& Linker) override
{
    Linker.LinkExternalData(ActorHandle);
    Linker.LinkExternalData(SubsystemHandle);
    return true;
}

// Access at runtime
auto& ActorCtx = Context.GetExternalData(ActorHandle);       // Required — reference
auto* SubsystemCtx = Context.GetExternalDataPtr(SubsystemHandle);  // Optional — pointer
```

The schema's `CollectExternalData` populates these handles at tree start, validating at link time rather than runtime.

---

## UStateTreeComponent

`UStateTreeComponent` extends `UBrainComponent` and manages the full tree lifecycle on an actor.

```cpp
void SetStateTree(UStateTree* NewStateTree);
void SetStateTreeReference(FStateTreeReference NewStateTreeRef);
void SendStateTreeEvent(const FStateTreeEvent& Event);
void SendStateTreeEvent(FGameplayTag Tag, FConstStructView Payload, FName Origin);
EStateTreeRunStatus GetStateTreeRunStatus() const;
// Delegate — fires when run status changes
FStateTreeRunStatusChanged OnStateTreeRunStatusChanged;  // BlueprintAssignable
bool bStartLogicAutomatically = true;  // EditAnywhere
```

### FStateTreeReference

`FStateTreeReference` wraps a `UStateTree*` with parameter overrides:
```cpp
FStateTreeReference TreeRef;
TreeRef.SetStateTree(MyStateTreeAsset);
TreeRef.SyncParameters();
TreeRef.GetParameters().SetValueFloat(TEXT("AggroRange"), 1500.f);
```

`FStateTreeReferenceOverrides` swaps tree references at runtime by tag:
```cpp
Overrides.AddOverride(Tag_CombatVariant, CombatTreeRef);
Overrides.RemoveOverride(Tag_CombatVariant);
```

Subclass `UStateTreeComponent` to customize context via `SetContextRequirements(FStateTreeExecutionContext&, bool bLogErrors)` and `CollectExternalData(...)`.

---

## AI Integration

`UStateTreeAIComponentSchema` adds `AIControllerClass` to the component schema, making the AI controller available as context data for property bindings.

```cpp
AMyAIController::AMyAIController()
{
    StateTreeComp = CreateDefaultSubobject<UStateTreeComponent>(TEXT("StateTree"));
    StateTreeComp->bStartLogicAutomatically = true;
}
```

Assign the `UStateTree` asset in the controller defaults. Set the schema's `ContextActorClass` to your Pawn class so the editor can bind to its components.

### State Tree vs Behavior Tree

| Aspect | State Tree | Behavior Tree |
|--------|-----------|---------------|
| Structure | Hierarchical FSM with transitions | Tree of composites, decorators, tasks |
| Data flow | Evaluators + property bindings (typed) | Blackboard (string-keyed, loosely typed) |
| Conditions | First-class on transitions | Decorators on tree nodes |
| Mass Entity | Native via `UMassStateTreeSchema` | No Mass support |
| Best for | Data-driven FSMs, Mass entities, flat logic | Deep decision hierarchies, complex aborts |

Prefer State Trees for new AI needing Mass Entity scaling or data-driven transitions. Keep Behavior Trees for deeply nested decision logic with complex abort/decorator patterns.

---

## Mass Entity Integration

State Trees integrate natively with Mass Entity for processing thousands of entities. See `references/state-tree-mass-integration.md` for complete setup.

Key concepts:
- `UMassStateTreeSchema` constrains trees to Mass-compatible node types (`FMassStateTreeTaskBase`, etc.)
- `UMassStateTreeSubsystem` manages pooled instance data (`AllocateInstanceData`/`FreeInstanceData`)
- `UMassStateTreeProcessor` evaluates trees per entity each frame
- `FMassStateTreeExecutionContext` wraps execution context with `SetEntity`/`GetEntity`
- Mass-specific tasks override `GetDependencies(UE::MassBehavior::FStateTreeDependencyBuilder&)` to declare fragment read/write requirements

For Mass Entity architecture details, see `ue-mass-entity`.

---

## Common Mistakes

**Persisting FStateTreeExecutionContext across frames:**
```cpp
// WRONG — context is per-tick, NOT persistent
FStateTreeExecutionContext* SavedContext;  // dangling after tick

// RIGHT — reconstruct each tick from persistent instance data
FStateTreeExecutionContext Context(Owner, *StateTree, InstanceData);
Context.Tick(DeltaTime);
```

**Mutating task struct directly instead of using instance data:**
```cpp
// WRONG — task structs are const at runtime
virtual EStateTreeRunStatus Tick(...) const override {
    Timer += DeltaTime;  // compile error — 'this' is const
}

// RIGHT — use FInstanceDataType typedef
typedef FMyInstanceData FInstanceDataType;
virtual EStateTreeRunStatus Tick(...) const override {
    auto& Data = Context.GetInstanceData(*this);
    Data.Timer += DeltaTime;
}
```

**Conditions with side effects:** `TestCondition` may be called multiple times per frame during transition evaluation. Never modify state in conditions — they must be pure functions.

**Evaluators doing heavy work every tick:** Evaluators run every frame before transitions. Cache results in instance data and only refresh when inputs change.

**Exceeding MaxStates depth:** `FStateTreeActiveStates::MaxStates = 8`. Deeply nested hierarchies silently fail. Flatten with linked states or subtrees.

**Forgetting to link external data:** Unlinked Required handles assert at runtime; Optional handles silently return nullptr. Always link all declared handles in `Link()`.

**Not consuming events:** With `bConsumeEventOnSelect = false`, the same event can trigger multiple transitions in one frame. Leave default `true` unless broadcast behavior is intended.

---

## Related Skills

- `ue-ai-navigation` — Behavior tree patterns, AI controller setup, perception system
- `ue-mass-entity` — Mass Entity architecture, processors, fragments, traits
- `ue-gameplay-abilities` — Ability-driven state transitions, GAS integration
- `ue-gameplay-framework` — Game state machines, controller/pawn lifecycle
- `ue-actor-component-architecture` — Component setup for `UStateTreeComponent`
- `ue-cpp-foundations` — USTRUCT patterns, delegates, subsystem access
