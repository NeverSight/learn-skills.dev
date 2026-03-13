---
name: ue-ai-navigation
description: "Use this skill when implementing AI, AIController, behavior tree, blackboard, AI perception, NavMesh, EQS, navigation, pathfinding, State Tree, or Smart Objects in Unreal Engine. See references/behavior-tree-patterns.md for BT patterns and references/eqs-reference.md for EQS configuration. For AI ability use, see ue-gameplay-abilities."
metadata:
  version: 1.0.0
---

# UE AI and Navigation

You are an expert in Unreal Engine's AI and navigation systems.

## Context

Read `.agents/ue-project-context.md` for project AI plugins, subsystem configs, enabled modules (AIModule, NavigationSystem, GameplayStateTreeModule, SmartObjectsModule), and existing AI frameworks.

## Information Gathering

Before implementing, clarify: AI complexity, navigation needs (ground/fly/swim, dynamic obstacles, streaming), perception senses required, Behavior Tree vs. State Tree preference, multiplayer authority model, and agent count for budget planning.

---

## AI Architecture

```
APawn
  └── AAIController (server-only in multiplayer)
        ├── UBehaviorTreeComponent  (UBrainComponent subclass)
        │     └── UBehaviorTree asset → UBlackboardData
        ├── UBlackboardComponent    (AI knowledge store)
        ├── UAIPerceptionComponent  (sight, hearing, damage)
        └── UPathFollowingComponent (NavMesh path execution)
```

**Build.cs modules**: `AIModule`, `NavigationSystem`, `GameplayTasks`

---

## AIController

```cpp
// MyAIController.h
UCLASS()
class AMyAIController : public AAIController
{
    GENERATED_BODY()
public:
    AMyAIController();
    UPROPERTY(EditDefaultsOnly, Category = AI)
    TObjectPtr<UBehaviorTree> BehaviorTreeAsset;
protected:
    virtual void OnPossess(APawn* InPawn) override;
    UFUNCTION()
    void OnTargetPerceptionUpdated(AActor* Actor, FAIStimulus Stimulus);
};

// MyAIController.cpp
AMyAIController::AMyAIController()
{
    bStartAILogicOnPossess = true;
    bStopAILogicOnUnposses = true;
    // PerceptionComponent declared in AAIController; configure senses here or in BP defaults
}

void AMyAIController::OnPossess(APawn* InPawn)
{
    Super::OnPossess(InPawn);
    if (BehaviorTreeAsset)
        RunBehaviorTree(BehaviorTreeAsset); // calls UseBlackboard internally
    if (UAIPerceptionComponent* PC = GetAIPerceptionComponent())
        PC->OnTargetPerceptionUpdated.AddDynamic(this, &AMyAIController::OnTargetPerceptionUpdated);
}
```

### Key AAIController API

```cpp
// Navigation
EPathFollowingRequestResult::Type MoveToActor(AActor* Goal, float AcceptanceRadius = -1,
    bool bStopOnOverlap = true, bool bUsePathfinding = true, bool bCanStrafe = true,
    TSubclassOf<UNavigationQueryFilter> FilterClass = {}, bool bAllowPartialPath = true);

EPathFollowingRequestResult::Type MoveToLocation(const FVector& Dest, float AcceptanceRadius = -1,
    bool bStopOnOverlap = true, bool bUsePathfinding = true,
    bool bProjectDestinationToNavigation = false, bool bCanStrafe = true,
    TSubclassOf<UNavigationQueryFilter> FilterClass = {}, bool bAllowPartialPath = true);

void StopMovement();
bool HasPartialPath() const;
EPathFollowingStatus::Type GetMoveStatus() const;

// Focus
void SetFocus(AActor* NewFocus, EAIFocusPriority::Type Priority = EAIFocusPriority::Gameplay);
void SetFocalPoint(FVector NewFocus, EAIFocusPriority::Type Priority = EAIFocusPriority::Gameplay);
void ClearFocus(EAIFocusPriority::Type Priority);

// Brain / Blackboard
bool RunBehaviorTree(UBehaviorTree* BTAsset);
bool UseBlackboard(UBlackboardData* BlackboardAsset, UBlackboardComponent*& BlackboardComponent);
UBlackboardComponent* GetBlackboardComponent();

// Team (IGenericTeamAgentInterface)
void SetGenericTeamId(const FGenericTeamId& NewTeamID);

// Delegate: FAIMoveCompletedSignature ReceiveMoveCompleted (RequestID, Result)
```

**On Pawn**: `AIControllerClass = AMyAIController::StaticClass(); AutoPossessAI = EAutoPossessAI::PlacedInWorldOrSpawned;`

---

## Blackboard

| Type | Get | Set |
|------|-----|-----|
| Object | `GetValueAsObject` | `SetValueAsObject` |
| Vector | `GetValueAsVector` | `SetValueAsVector` |
| Bool | `GetValueAsBool` | `SetValueAsBool` |
| Float | `GetValueAsFloat` | `SetValueAsFloat` |
| Int | `GetValueAsInt` | `SetValueAsInt` |
| Enum | `GetValueAsEnum` | `SetValueAsEnum` |
| Name | `GetValueAsName` | `SetValueAsName` |
| Rotator | `GetValueAsRotator` | `SetValueAsRotator` |
| String | `GetValueAsString` | `SetValueAsString` |
| Class | `GetValueAsClass` | `SetValueAsClass` |

```cpp
UBlackboardComponent* BB = GetBlackboardComponent();
BB->SetValueAsObject(TEXT("TargetActor"), SomeActor);
BB->SetValueAsVector(TEXT("LastKnownLocation"), Location);
BB->ClearValue(TEXT("TargetActor"));
bool bSet = BB->IsVectorValueSet(TEXT("PatrolLocation"));

// Observer (called when key changes)
FBlackboard::FKey KeyID = BB->GetKeyID(TEXT("TargetActor"));
FDelegateHandle H = BB->RegisterObserver(KeyID, this,
    FOnBlackboardChangeNotification::CreateUObject(this, &AMyAIController::OnBBKeyChanged));
BB->UnregisterObserver(KeyID, H);

// High-perf cached accessor (avoids repeated name lookups):
FBBKeyCachedAccessor<UBlackboardKeyType_Bool> BBInCombat;
// Init: BBInCombat = FBBKeyCachedAccessor<...>(*BBComp, KeyID);
// Use: bool b = BBInCombat.Get(); BBInCombat.SetValue(*BB, true);
```

Mark keys **Instance Synced** to share values across all AI using the same `UBlackboardData` (squad-wide alerts via `UAISystem` propagation).

---

## Behavior Tree Nodes

### Custom Task

```cpp
UCLASS()
class UMyBTTask_Attack : public UBTTaskNode
{
    GENERATED_BODY()
public:
    UMyBTTask_Attack() { NodeName = TEXT("Attack"); INIT_TASK_NODE_NOTIFY_FLAGS(); }
    UPROPERTY(EditAnywhere) FBlackboardKeySelector TargetKey;
protected:
    virtual EBTNodeResult::Type ExecuteTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory) override;
    virtual void TickTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory, float DeltaSeconds) override;
    virtual EBTNodeResult::Type AbortTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory) override;
};

EBTNodeResult::Type UMyBTTask_Attack::ExecuteTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
{
    AActor* Target = Cast<AActor>(
        OwnerComp.GetBlackboardComponent()->GetValueAsObject(TargetKey.SelectedKeyName));
    if (!IsValid(Target)) return EBTNodeResult::Failed;
    // Start async work → return InProgress; call FinishLatentTask() when done
    return EBTNodeResult::InProgress;
}

void UMyBTTask_Attack::TickTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory, float DeltaSeconds)
{
    FinishLatentTask(OwnerComp, EBTNodeResult::Succeeded); // or Failed
}

EBTNodeResult::Type UMyBTTask_Attack::AbortTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
{
    return EBTNodeResult::Aborted; // cleanup; or InProgress + FinishLatentAbort()
}
```

### Custom Decorator

```cpp
UCLASS()
class UMyBTDecorator_CanSee : public UBTDecorator
{
    GENERATED_BODY()
public:
    UMyBTDecorator_CanSee()
    {
        INIT_DECORATOR_NODE_NOTIFY_FLAGS();
        bAllowAbortLowerPri = true; bAllowAbortChildNodes = true;
        FlowAbortMode = EBTFlowAbortMode::Both;
    }
    UPROPERTY(EditAnywhere) FBlackboardKeySelector TargetKey;
protected:
    virtual bool CalculateRawConditionValue(
        UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory) const override
    {
        AActor* Target = Cast<AActor>(
            OwnerComp.GetBlackboardComponent()->GetValueAsObject(TargetKey.SelectedKeyName));
        return IsValid(Target) && OwnerComp.GetAIOwner()->LineOfSightTo(Target);
    }
};
```

### Custom Service

```cpp
UCLASS()
class UMyBTService_UpdateTarget : public UBTService
{
    GENERATED_BODY()
public:
    UMyBTService_UpdateTarget() { Interval = 0.5f; RandomDeviation = 0.1f; INIT_SERVICE_NODE_NOTIFY_FLAGS(); }
protected:
    virtual void TickNode(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory, float DeltaSeconds) override
    {
        TArray<AActor*> Hostiles;
        OwnerComp.GetAIOwner()->GetAIPerceptionComponent()->GetPerceivedHostileActors(Hostiles);
        AActor* Best = nullptr; float BestDist = FLT_MAX;
        FVector MyLoc = OwnerComp.GetAIOwner()->GetPawn()->GetActorLocation();
        for (AActor* A : Hostiles)
        {
            float D = FVector::Dist(MyLoc, A->GetActorLocation());
            if (D < BestDist) { BestDist = D; Best = A; }
        }
        OwnerComp.GetBlackboardComponent()->SetValueAsObject(TEXT("TargetActor"), Best);
    }
};
```

### Built-in Nodes (reference)

**Tasks**: `BTTask_MoveTo`, `BTTask_MoveDirectlyToward`, `BTTask_Wait`, `BTTask_WaitBlackboardTime`, `BTTask_RunEQSQuery`, `BTTask_PlayAnimation`, `BTTask_MakeNoise`, `BTTask_RotateToFaceBBEntry`, `BTTask_RunBehavior`, `BTTask_RunBehaviorDynamic`, `BTTask_FinishWithResult`

**Decorators**: `BTDecorator_Blackboard`, `BTDecorator_CompareBBEntries`, `BTDecorator_Cooldown`, `BTDecorator_TagCooldown`, `BTDecorator_Loop`, `BTDecorator_TimeLimit`, `BTDecorator_DoesPathExist`, `BTDecorator_IsAtLocation`, `BTDecorator_CheckGameplayTagsOnActor`, `BTDecorator_ForceSuccess`

**Composites**: `Selector` (first success), `Sequence` (first failure), `SimpleParallel` (main task + background subtree; main task drives completion). UE does not ship a general-purpose Parallel node — `SimpleParallel` is the built-in option. For true parallel execution of N branches, implement a custom `UBTCompositeNode` or chain multiple `SimpleParallel` nodes.

---

## AI Perception

```cpp
// In AIController constructor:
#include "Perception/AISenseConfig_Sight.h"
#include "Perception/AISenseConfig_Hearing.h"
#include "Perception/AISenseConfig_Damage.h"

UAIPerceptionComponent* AIP = CreateDefaultSubobject<UAIPerceptionComponent>(TEXT("AIPerception"));
SetPerceptionComponent(*AIP);

UAISenseConfig_Sight* Sight = CreateDefaultSubobject<UAISenseConfig_Sight>(TEXT("Sight"));
Sight->SightRadius = 2000.f;
Sight->LoseSightRadius = 2500.f;
Sight->PeripheralVisionAngleDegrees = 60.f;
Sight->AutoSuccessRangeFromLastSeenLocation = 400.f;
Sight->DetectionByAffiliation.bDetectEnemies = true;
AIP->ConfigureSense(*Sight);
AIP->SetDominantSense(Sight->GetSenseImplementation());

UAISenseConfig_Hearing* Hearing = CreateDefaultSubobject<UAISenseConfig_Hearing>(TEXT("Hearing"));
Hearing->HearingRange = 3000.f;
Hearing->DetectionByAffiliation.bDetectEnemies = true;
Hearing->DetectionByAffiliation.bDetectNeutrals = true;
AIP->ConfigureSense(*Hearing);
```

```cpp
// Perception handler:
void AMyAIController::OnTargetPerceptionUpdated(AActor* Actor, FAIStimulus Stimulus)
{
    UBlackboardComponent* BB = GetBlackboardComponent();
    if (Stimulus.WasSuccessfullySensed())
    {
        BB->SetValueAsObject(TEXT("TargetActor"), Actor);
        BB->SetValueAsVector(TEXT("LastKnownLocation"), Stimulus.StimulusLocation);
    }
    else
    {
        // Lost target — keep last known location for investigation
        BB->SetValueAsVector(TEXT("LastKnownLocation"), Stimulus.StimulusLocation);
    }
}

// Report noise manually (e.g., gunshot):
UAISense_Hearing::ReportNoiseEvent(GetWorld(), Location, Loudness, Instigator, MaxRange, Tag);

// Report damage:
UAISense_Damage::ReportDamageEvent(GetWorld(), DamagedActor, Instigator, Amount, EventLoc, HitLoc);
```

```cpp
// On perceived actors — add UAIPerceptionStimuliSourceComponent:
#include "Perception/AIPerceptionStimuliSourceComponent.h"
UAIPerceptionStimuliSourceComponent* Source =
    CreateDefaultSubobject<UAIPerceptionStimuliSourceComponent>(TEXT("StimuliSource"));
Source->bAutoRegister = true;
Source->RegisterForSense(TSubclassOf<UAISense>(UAISense_Sight::StaticClass()));
Source->RegisterForSense(TSubclassOf<UAISense>(UAISense_Hearing::StaticClass()));
```

```cpp
// Query perception state:
UAIPerceptionComponent* PC = GetAIPerceptionComponent();
TArray<AActor*> Visible; PC->GetCurrentlyPerceivedActors(UAISense_Sight::StaticClass(), Visible);
TArray<AActor*> Hostiles; PC->GetPerceivedHostileActors(Hostiles);
bool bCanSee = PC->HasActiveStimulus(*Target, UAISense::GetSenseID<UAISense_Sight>());
PC->ForgetActor(Target);
PC->ForgetAll();
// Per-actor delegate (shown above):
// OnTargetPerceptionUpdated — fires once per actor whose perception state changed
// Batch delegate — fires once per frame with all updated actors:
// OnPerceptionUpdated — signature: void(const TArray<AActor*>& UpdatedActors)
// Also: OnTargetPerceptionForgotten, OnTargetPerceptionInfoUpdated
```

Additional sense configs: `UAISenseConfig_Touch` (fires on physical contact with perceived actor), `UAISense_Team` (propagates enemy awareness across teammates via `IGenericTeamAgentInterface`), `UAISense_Prediction` (predicts future location — call `UAISense_Prediction::RequestPawnPredictionEvent`).

---

## Navigation System

```cpp
#include "NavigationSystem.h"
UNavigationSystemV1* NavSys = UNavigationSystemV1::GetCurrent(GetWorld());

// Random reachable point
FNavLocation ResultLoc;
bool bOk = NavSys->GetRandomReachablePointInRadius(Origin, Radius, ResultLoc);

// Project onto NavMesh
FNavLocation Projected;
NavSys->ProjectPointToNavigation(WorldLoc, Projected, FVector(500, 500, 500));

// Sync path query
FPathFindingQuery Query; Query.StartLocation = Start; Query.EndLocation = End;
FPathFindingResult Result = NavSys->FindPathSync(Query);
if (Result.IsSuccessful()) { TArray<FNavPathPoint>& Pts = Result.Path->GetPathPoints(); }

// Async path query
FNavAgentProperties NavAgent = GetPawn()->GetNavAgentPropertiesRef();
NavSys->FindPathAsync(NavAgent, Query,
    FNavPathQueryDelegate::CreateUObject(this, &AMyAI::OnPathFound));

// Dynamic obstacle on actor:
#include "NavModifierComponent.h"
UNavModifierComponent* Mod = CreateDefaultSubobject<UNavModifierComponent>(TEXT("NavMod"));
Mod->AreaClass = UNavArea_Obstacle::StaticClass();

// Custom nav filter (prefer certain areas):
UCLASS() class UMyNavFilter : public UNavigationQueryFilter { ... };
MoveToActor(Target, -1.f, true, true, true, UMyNavFilter::StaticClass());

// Runtime NavMesh rebuild (after procedural generation):
NavSys->Build();

// Access RecastNavMesh for agent config (mirrors Project Settings > Navigation)
ARecastNavMesh* RNM = Cast<ARecastNavMesh>(NavSys->GetDefaultNavDataInstance());
// Key properties: AgentRadius, AgentHeight, AgentMaxStepHeight, AgentMaxSlope
// ANavMeshBoundsVolume must exist in level — without it, no tiles generate.
// For streaming/open-world: use UNavigationInvokerComponent on AI pawns instead.
```

**Off-mesh links**: Use `ANavLinkProxy` in-level, or implement `INavLinkCustomInterface` for traversal callbacks.

---

## EQS (Environment Query System)

```cpp
#include "EnvironmentQuery/EnvQueryManager.h"

UPROPERTY(EditDefaultsOnly) TObjectPtr<UEnvQuery> FindCoverQuery;

void AMyAIController::RunCoverQuery()
{
    FEnvQueryRequest Request(FindCoverQuery, this);
    Request.Execute(EEnvQueryRunMode::SingleResult,
        FQueryFinishedSignature::CreateUObject(this, &AMyAIController::OnCoverDone));
}

void AMyAIController::OnCoverDone(TSharedPtr<FEnvQueryResult> Result)
{
    if (Result.IsValid() && Result->IsSuccessful())
        GetBlackboardComponent()->SetValueAsVector(TEXT("CoverLocation"),
            Result->GetItemAsLocation(0));
}
```

**Run modes**: `SingleResult` (cheapest), `RandomBest5Pct`, `RandomBest25Pct`, `AllMatching`

**BTTask_RunEQSQuery**: set `EQSRequest.QueryTemplate`, `BlackboardKey`, `RunMode`. Async lifecycle managed via `FBTEnvQueryTaskMemory.RequestID`.

**Custom context** (resolve BB actor for use in tests):

```cpp
UCLASS()
class UEnvQueryContext_Enemy : public UEnvQueryContext
{
    GENERATED_BODY()
    virtual void ProvideContext(FEnvQueryInstance& QI, FEnvQueryContextData& CD) const override
    {
        AAIController* C = Cast<AAIController>(Cast<APawn>(QI.Owner.Get())->GetController());
        AActor* Enemy = Cast<AActor>(C->GetBlackboardComponent()->GetValueAsObject(TEXT("TargetActor")));
        if (IsValid(Enemy)) UEnvQueryItemType_Actor::SetContextHelper(CD, Enemy);
    }
};
```

See `references/eqs-reference.md` for generator and test configurations.

---

## State Trees (UE 5.1+)

Use State Trees for simpler state machines, designer-friendly workflows, and Smart Object integration. Use Behavior Trees for complex reactive combat with priority-based interrupts.

```cpp
// Build.cs: "GameplayStateTreeModule"
#include "Components/StateTreeComponent.h"

UCLASS()
class AMyNPC : public ACharacter
{
    GENERATED_BODY()
    UPROPERTY(VisibleAnywhere) TObjectPtr<UStateTreeComponent> StateTreeComp;
};
AMyNPC::AMyNPC() { StateTreeComp = CreateDefaultSubobject<UStateTreeComponent>(TEXT("StateTree")); }
void AMyNPC::BeginPlay() { Super::BeginPlay(); StateTreeComp->StartLogic(); }
```

State Tree tasks use `FStateTreeTaskBase` + `FInstanceDataType`. Override `EnterState`, `Tick`, `ExitState`.

State Tree **evaluators** (`FStateTreeEvaluatorBase`) run persistently across all active states — use them for shared context data (nearest enemy, threat level) that multiple states read, analogous to BT services.

---

## Smart Objects

Add `USmartObjectComponent` to world actors (set `SmartObjectDefinition`). AI interacts via `USmartObjectSubsystem`:

```cpp
// Build.cs: "SmartObjectsModule"
#include "SmartObjectSubsystem.h"
USmartObjectSubsystem* SOS = USmartObjectSubsystem::GetCurrent(GetWorld());
FSmartObjectRequestFilter Filter;
FSmartObjectRequest Req(FBox(Origin, Origin).ExpandBy(500.f), Filter);
FSmartObjectRequestResult Res = SOS->FindSmartObject(Req);
if (Res.IsValid())
{
    FSmartObjectClaimHandle Handle = SOS->MarkSlotAsClaimed(Res.SlotHandle, ESmartObjectClaimPriority::Normal);
    // ... use slot, then:
    SOS->MarkSlotAsFree(Handle);
}
```

---

## Common Mistakes

**Polling instead of event-driven**: Do not check per-frame in `TickTask` if a `BTDecorator_Blackboard` observer abort or `WaitForMessage` achieves the same result.

**Overcomplicated BTs**: Flatten needless nesting. Use services for periodic knowledge updates at `Interval >= 0.5s`. Gate expensive EQS with `BTDecorator_Cooldown`.

**NavMesh gaps**: Always place `ANavMeshBoundsVolume`. For streaming/procedural levels, call `NavSys->Build()` after generation or use `UNavigationInvokerComponent` on AI pawns.

**Server vs client**: `AAIController` only exists on the server. Replicate AI state via Pawn replicated properties, not through the controller. BT Blackboard is not replicated.

**Large worlds**: Use hierarchical NavMesh (RecastNavMesh actor settings). Set EQS max parallel queries per frame in Project Settings > AI > EQS.

---

## Edge Cases

- **Flying/swimming**: Set `FNavAgentProperties::bCanFly`/`bCanSwim`; assign a `UNavArea` subclass with matching `SupportedAgents` flags. Custom `UNavArea` subclasses define traversal cost and area flags — create one per movement domain (e.g., `UNavArea_Water` with high cost for ground agents, zero for swimmers). Apply via NavModifierVolumes or NavMesh generation settings.
- **Dedicated server**: Sight perception uses collision traces, not rendering — works fine. Guard non-server code with `HasAuthority()`.
- **AI with GAS**: BT tasks request ability activation; abilities manage their own latent logic.

---

## Related Skills

- `ue-actor-component-architecture` — component setup patterns for AI
- `ue-gameplay-framework` — GameMode AI spawning, controller/pawn relationships
- `ue-cpp-foundations` — delegates, subsystems, UObject patterns
- `ue-gameplay-abilities` — GAS + AI integration

## Reference Files

- `references/behavior-tree-patterns.md` — patrol, combat, flee, investigate, squad BT patterns
- `references/eqs-reference.md` — generator and test configurations for spatial queries
