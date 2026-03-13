---
name: ue-networking-replication
description: "Use this skill when working on multiplayer networking, replication, RPC calls, net role logic, server/client authority, prediction, or synchronizing game state. Also use when the user mentions 'DOREPLIFETIME', 'dedicated server', 'replicated', or 'net role'. See references/replication-patterns.md for common patterns and references/rpc-decision-guide.md for RPC type selection. For GAS networking, see ue-gameplay-abilities."
metadata:
  version: 1.0.0
---

# UE Networking & Replication

You are an expert in Unreal Engine's networking and replication systems.

## Context Check

Read `.agents/ue-project-context.md` for this project's multiplayer configuration.
Look for: server topology (dedicated, listen, P2P), player count, replicated classes,
and any custom net drivers.

If the context file is absent, ask:
1. Server topology? (dedicated, listen, P2P)
2. Maximum player count per session?
3. Which actors or components need to replicate data?
4. Are you using Gameplay Ability System (GAS)?

---

## Net Roles and Authority

UE uses a server-authoritative model: the server is the source of truth for game state.
Clients predict locally and reconcile with server corrections.

Every actor on every machine has a local role and a remote role (`ENetRole`).

```
ROLE_Authority       — owns and can modify this actor (server for replicated actors)
ROLE_AutonomousProxy — client copy of the locally controlled pawn
ROLE_SimulatedProxy  — client copy of another player's actor; engine interpolates state
ROLE_None            — not replicated
```

From `Actor.h`:
```cpp
ENetRole GetLocalRole() const { return Role; }   // role on current machine
ENetRole GetRemoteRole() const;                   // role the other end sees
bool HasAuthority() const { return (GetLocalRole() == ROLE_Authority); }
```

Net modes: `NM_Standalone`, `NM_DedicatedServer`, `NM_ListenServer`, `NM_Client`.

**Role matrix for a replicated Pawn:**

| Machine        | GetLocalRole()       | GetRemoteRole()                         |
|----------------|----------------------|-----------------------------------------|
| Server         | ROLE_Authority       | ROLE_AutonomousProxy or SimulatedProxy  |
| Owning Client  | ROLE_AutonomousProxy | ROLE_Authority                          |
| Other Clients  | ROLE_SimulatedProxy  | ROLE_Authority                          |

**Listen-server caveat:** the host is both `ROLE_Authority` and locally controlled.
Use `IsLocallyControlled()` to distinguish logic that should skip the host player.

---

## UNetDriver

`UNetDriver` is the core transport class responsible for managing all network connections and
packet delivery for a world. It owns the list of `UNetConnection` objects and drives the
replication tick. Access it via `UWorld::GetNetDriver()`.

```cpp
UNetDriver* Driver = GetWorld()->GetNetDriver();
// Driver->ClientConnections  — all connected clients (server-side)
// Driver->ServerConnection   — connection to server (client-side)
```

For most gameplay code you never interact with `UNetDriver` directly; it is relevant when
writing custom net drivers, profiling connection state, or debugging packet loss.

---

## Property Replication

### Actor Setup

```cpp
AMyActor::AMyActor()
{
    bReplicates = true;             // AActor::SetReplicates() also available at runtime
    SetReplicateMovement(true);     // replicates FRepMovement (location/rotation/velocity)
    SetNetUpdateFrequency(10.f);    // checks per second
    SetMinNetUpdateFrequency(2.f);  // floor when nothing changes
    NetPriority = 1.0f;            // higher = preferred when bandwidth is saturated
}
```

From `Actor.h`: `SetReplicates`, `SetReplicateMovement`, `SetNetUpdateFrequency`,
`SetMinNetUpdateFrequency`, and `SetNetCullDistanceSquared` are all `ENGINE_API`.

**FRepMovement:** when `bReplicateMovement = true`, the engine serializes position,
velocity, and rotation into an `FRepMovement` struct (declared in `Actor.h`) and
sends it to simulated proxies. `UCharacterMovementComponent` bypasses this with its
own prediction-based replication; it writes compressed moves via `FSavedMove_Character`
and reconciles them server-side, so `SetReplicateMovement(false)` is the correct
default for characters using CMC.

### Declaring Properties

```cpp
UPROPERTY(Replicated)
int32 Health;

UPROPERTY(ReplicatedUsing = OnRep_State)
EMyState State;

UFUNCTION()
void OnRep_State(EMyState PreviousState); // old value passed as optional parameter
```

### GetLifetimeReplicatedProps

```cpp
// MyActor.cpp
#include "Net/UnrealNetwork.h"

void AMyActor::GetLifetimeReplicatedProps(
    TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps); // NEVER omit this
    DOREPLIFETIME(AMyActor, Health);
    DOREPLIFETIME_CONDITION(AMyActor, State,        COND_OwnerOnly);
    DOREPLIFETIME_CONDITION(AMyActor, SimData,      COND_SimulatedOnly);
    DOREPLIFETIME_CONDITION(AMyActor, InitData,     COND_InitialOnly);
    DOREPLIFETIME_CONDITION(AMyActor, PublicData,   COND_SkipOwner);
}
```

**Conditions:** `COND_None` (all), `COND_OwnerOnly`, `COND_SkipOwner`,
`COND_SimulatedOnly`, `COND_AutonomousOnly`, `COND_InitialOnly`, `COND_Custom`.

Use `COND_OwnerOnly` for private player data (inventory, currency).
Use `COND_InitialOnly` for immutable spawn data (team, character class).

**Initial replication burst**: When a client first joins or an actor first becomes relevant, ALL replicated properties send at once regardless of conditions (`COND_InitialOnly` fires exactly once here). This burst can saturate the actor channel — keep initial state compact and use `COND_InitialOnly` for spawn-time-only data to reduce ongoing bandwidth.

### FRepLayout (Internal)

`FRepLayout` is an internal engine struct that describes which properties of a class are
replicated and how. It handles delta compression (only changed properties are sent) and
evaluates `DOREPLIFETIME_CONDITION` filters per-connection. Developers rarely interact
with `FRepLayout` directly, but knowing it exists helps when debugging why a property is
or is not replicating: the layout is built once per class and cached, so dynamic changes
to conditions require `DOREPLIFETIME_WITH_PARAMS_FAST` or `bIsPushBased` patterns rather
than modifying the struct at runtime.

### Large Arrays: FFastArraySerializer

Plain `TArray` sends the full array on any change. Use `FFastArraySerializer` for
delta-only replication. See `references/replication-patterns.md` Pattern 3 for
a complete inventory implementation.

### Custom Struct Serialization

Implement `NetSerialize` on a `USTRUCT` and add `TStructOpsTypeTraits` with
`WithNetSerializer = true` to control binary layout manually. Use
`FVector_NetQuantize10` (0.1 cm precision) instead of raw `FVector` to halve
position bandwidth.

---

## Remote Procedure Calls (RPCs)

See `references/rpc-decision-guide.md` for the full decision flowchart.

```cpp
// Client calls → server executes. WithValidation is required for state changes.
UFUNCTION(Server, Reliable, WithValidation)
void ServerFireWeapon(FVector_NetQuantize Origin, FVector_NetQuantizeNormal Dir);

// Server calls → owning client executes. No WithValidation needed.
UFUNCTION(Client, Reliable)
void ClientShowKillConfirm();

// Server calls → server + all clients execute.
UFUNCTION(NetMulticast, Unreliable)
void MulticastPlayHitEffect(FVector ImpactPoint);
```

Implementations always end in `_Implementation`. Server RPCs with validation also
need `_Validate` (return `false` to kick the client).

**Reliable** — guaranteed delivery; use for state-changing actions (purchase, spawn,
possession). **Unreliable** — fire-and-forget; use for high-frequency cosmetics.

Real examples from `PlayerController.h`:
```cpp
UFUNCTION(unreliable, server, WithValidation) void ServerSetSpectatorLocation(...);
UFUNCTION(reliable,   server, WithValidation) void ServerAcknowledgePossession(APawn* P);
UFUNCTION(Reliable,   Client)                 void ClientReceiveLocalizedMessage(...);
UFUNCTION(Client,     Unreliable)             void ClientAckTimeDilation(float, int32);
```

**RPC ownership:** Server RPCs must be called on an actor whose ownership chain
leads to the calling client's `APlayerController`. Client RPCs must be called on
an actor owned by a player with a `NetConnection`. Calls on unowned actors are
silently dropped.

**RPC Parameter Rules**: Only net-addressable types are valid — basic types (`int32`,
`float`, `FString`, `FVector`), replicated `UObject*` pointers (arrive as `nullptr`
if not replicated), and `USTRUCT(BlueprintType)` structs. Non-replicated `UObject*`
pointers arrive as `nullptr`; pass an ID and look the object up on the remote side.
Large payloads (>1 KB) should use replicated properties instead of RPC parameters.
`TArray` and `TMap` parameters are supported but watch for bandwidth impact.

---

## Ownership and Relevancy

```cpp
// Server sets owner to control connection routing for RPCs and COND_OwnerOnly
Weapon->SetOwner(PlayerController);

// Relevancy flags (from Actor.h)
bAlwaysRelevant      = true;  // replicate to every connection
bOnlyRelevantToOwner = true;  // replicate only to the owning connection

// Override for custom logic (e.g., team-based relevancy)
virtual bool IsNetRelevantFor(const AActor* RealViewer, const AActor* ViewTarget,
                               const FVector& SrcLocation) const override;
```

Default relevancy culls actors beyond `NetCullDistanceSquared` from the client
viewpoint. `NetPriority` determines which actors win when bandwidth is saturated.

**Dormancy:** actors that rarely change can pause replication entirely.

```cpp
SetNetDormancy(DORM_DormantAll); // stop replication
FlushNetDormancy();              // send one update then return to dormant
```

**Re-relevancy**: When an actor moves outside `NetCullDistanceSquared` it stops replicating. When it returns to range, the engine treats it as a fresh relevancy event — sending another initial burst and firing all `OnRep_` callbacks with current server state. Design `OnRep_` functions to be idempotent (tolerate being called multiple times with the same value). Dormant actors (`DORM_DormantAll`) behave similarly when woken — they flush all dirty properties at once.

---

## Subobject Replication

### Modern API (UE 5.1+)

From `Actor.h`:
```cpp
ENGINE_API void AddReplicatedSubObject(UObject* SubObject,
                                       ELifetimeCondition NetCondition = COND_None);
ENGINE_API void RemoveReplicatedSubObject(UObject* SubObject);
ENGINE_API void AddActorComponentReplicatedSubObject(UActorComponent* OwnerComponent,
                                                     UObject* SubObject,
                                                     ELifetimeCondition NetCondition = COND_None);
```

Enable with `bReplicateUsingRegisteredSubObjectList = true` (now the default).
Call `AddReplicatedSubObject` on the server during `BeginPlay`; call
`RemoveReplicatedSubObject` in `EndPlay`.

### Legacy API

Override `ReplicateSubobjects` when `bReplicateUsingRegisteredSubObjectList = false`:

```cpp
bool AMyActor::ReplicateSubobjects(UActorChannel* Channel,
                                    FOutBunch* Bunch, FReplicationFlags* RepFlags)
{
    bool bWrote = Super::ReplicateSubobjects(Channel, Bunch, RepFlags);
    bWrote |= Channel->ReplicateSubobject(MySubObject, *Bunch, *RepFlags);
    return bWrote;
}
```

---

## Client-Side Prediction

Pattern (for non-movement systems without GAS):

```cpp
// 1. Client predicts immediately
void AMyCharacter::LocalPredictAbility(int32 AbilityId)
{
    if (IsLocallyControlled())
    {
        ApplyAbilityEffectLocal(AbilityId); // immediate visual/audio
        ServerActivateAbility(AbilityId);   // request server confirmation
    }
}

// 2. Server validates, broadcasts, or corrects
void AMyCharacter::ServerActivateAbility_Implementation(int32 AbilityId)
{
    if (CanActivateAbility(AbilityId))
    {
        ApplyAbilityEffectAuthority(AbilityId);
        MulticastAbilityActivated(AbilityId);
    }
    else
    {
        ClientCorrectionAbilityFailed(AbilityId); // roll back client prediction
    }
}
```

When the server rejects a prediction, smooth the visual correction to avoid jarring
snaps: interpolate the actor to the corrected position over 2-3 frames rather than
teleporting. `UCharacterMovementComponent` handles this automatically via
`NetworkSmoothingMode` (`Linear`, `Exponential`, or `Disabled`).

**CharacterMovementComponent** has full built-in prediction. Extend
`FSavedMove_Character` and override `PhysCustom` to support custom movement modes.

**Prediction eligibility**: Only `UCharacterMovementComponent` and GAS (`UAbilitySystemComponent` with `FPredictionKey`) have engine-managed prediction and rollback. Raw `UPROPERTY(Replicated)` properties have no built-in prediction — if you write them locally before the server confirms, the server's replicated value overwrites the client value with no rollback. For non-CMC/GAS state, use local-only variables for visual prediction and apply the authoritative value in `OnRep_`.

**GAS and FPredictionKey:** GAS uses `FPredictionKey` to link client-predicted actions
with server confirmations. The key is generated on the client (via
`FPredictionKey::CreateNewPredictionKey`), embedded in the Server RPC, and matched on the
server when applying `GameplayEffect`s or activating abilities. If the server determines
the prediction was invalid, every `GameplayEffect` and attribute change tagged with that
key is automatically rolled back on the client. You do not construct `FPredictionKey`
manually in most cases; `UAbilitySystemComponent::TryActivateAbility` manages the
lifecycle. Relevant when writing custom `UGameplayAbility` subclasses that need
scoped prediction windows (`FScopedPredictionWindow`). See `ue-gameplay-abilities`
for the full GAS networking details.

---

## Actor Replication Setup Checklist

```
[ ] bReplicates = true in constructor
[ ] SetNetUpdateFrequency / SetMinNetUpdateFrequency set appropriately
[ ] All UPROPERTY(Replicated) / UPROPERTY(ReplicatedUsing=...) declared
[ ] GetLifetimeReplicatedProps overridden; Super called first
[ ] DOREPLIFETIME / DOREPLIFETIME_CONDITION for each property
[ ] OnRep_ functions declared UFUNCTION() and implemented
[ ] Server RPCs have WithValidation; _Validate implemented
[ ] NetMulticast / Client RPCs guarded with HasAuthority() on call site
[ ] Subobjects registered via AddReplicatedSubObject or ReplicateSubobjects
[ ] SetOwner() called on server after spawning owned actors
[ ] DORM_DormantAll set on actors that rarely update
```

---

## Replication Graph

For large player counts (50+ connections), the default net driver relevancy checks become expensive. `UReplicationGraph` replaces per-connection per-actor relevancy with spatial and policy-based nodes.

```cpp
// Build.cs: "ReplicationGraph"
// Project: set ReplicationDriverClassName in DefaultEngine.ini
// [/Script/OnlineSubsystemUtils.IpNetDriver]
// ReplicationDriverClassName=/Script/MyGame.MyReplicationGraph

UCLASS()
class UMyReplicationGraph : public UReplicationGraph
{
    GENERATED_BODY()
public:
    virtual void InitGlobalActorClassSettings() override;
    virtual void InitGlobalGraphNodes() override;
    virtual void InitConnectionGraphNodes(UNetReplicationGraphConnection* RepGraphConnection) override;
};
```

Key node types: `UReplicationGraphNode_GridSpatialization2D` (spatial), `UReplicationGraphNode_AlwaysRelevant` (GameState, managers), `UReplicationGraphNode_AlwaysRelevant_ForConnection` (PlayerController, PlayerState, HUD), `UReplicationGraphNode_ActorList` (custom lists).

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Modifying state without `HasAuthority()` guard | Add `if (!HasAuthority()) return;` |
| Server RPC without `WithValidation` — client sends arbitrary values | Add `WithValidation`; validate in `_Validate` |
| Calling `Client`/`NetMulticast` from the client — silently dropped | Only call from server; guard with `HasAuthority()` |
| Plain `TArray` on replicated component — full array sent on every change | Use `FFastArraySerializer` |
| Omitting `Super::GetLifetimeReplicatedProps` — parent properties silently dropped | Always call `Super` first |
| Passing non-replicated `UObject*` in RPC params — arrives as `nullptr` | Pass an ID; look up object on remote side |
| Using `NetMulticast` for persistent state — late-joining clients miss it | Use `UPROPERTY(Replicated)` for state |
| Replicating cosmetic-only properties — increases bandwidth for data clients can compute locally | Only replicate gameplay-critical state; derive visuals client-side |

---

## APlayerController Replication Scope

`APlayerController` exists only on the server and the owning client — not on other
clients. Put data meant for all clients on `APawn` or `APlayerState`.

From `PlayerController.h`:
```cpp
// nullptr on local players (server-side); points to the network connection otherwise
UPROPERTY(DuplicateTransient)
TObjectPtr<UNetConnection> NetConnection;
```

**UNetConnection** represents a single client's network connection on the server. Each
connected client has exactly one `UNetConnection` owned by `UNetDriver`. Retrieve it
with `APlayerController::GetNetConnection()`. It is used for:
- Ownership checks: an actor's owning connection determines which client RPCs it can
  receive and which `COND_OwnerOnly` properties it sees.
- RPC routing: Server RPCs are only accepted from the actor's owning connection.
- Detecting disconnects: bind to `AGameModeBase::OnLogout` or check
  `NetConnection->GetConnectionState() == USOCK_Closed` (or `IsClosingOrClosed()`) rather than polling `NetConnection` directly.

Use `APlayerController` for connection-scoped Client RPCs (HUD updates, voice,
level streaming notifications). Use `APawn` or `APlayerState` for world-visible state.

---

## Related Skills

- `ue-gameplay-framework` — AGameMode (server-only), AGameState / APlayerState
  (replicated to all), APawn net roles
- `ue-gameplay-abilities` — GAS prediction keys, attribute set replication,
  GameplayEffect replication
- `ue-cpp-foundations` — UPROPERTY/UFUNCTION macros, module includes

## Reference Files

- `references/replication-patterns.md` — health, inventory (FFastArraySerializer),
  ability state, team data, subobject, dormancy, and custom relevancy patterns
- `references/rpc-decision-guide.md` — Server/Client/NetMulticast decision flowchart,
  Reliable vs Unreliable rules, ownership routing, and common RPC mistakes
