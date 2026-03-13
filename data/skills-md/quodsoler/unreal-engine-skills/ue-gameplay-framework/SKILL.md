---
name: ue-gameplay-framework
description: "Use this skill when working with Unreal Engine's gameplay framework classes: GameMode, GameState, PlayerController, PlayerState, Pawn, Character, or GameInstance. Also use when the user mentions 'gameplay framework', 'game rules', 'player management', 'match flow', or 'player spawning'. See references/framework-class-map.md for the full authority/presence matrix. For networking/replication, see ue-networking-replication. For input setup, see ue-input-system."
metadata:
  version: 1.0.0
---

# UE Gameplay Framework

You are an expert in Unreal Engine's gameplay framework architecture.

## Context Check

Read `.agents/ue-project-context.md` before proceeding. The game type (single player, co-op, competitive multiplayer, dedicated vs listen server) determines which classes to subclass and which replication patterns apply. Resolve: single-player or multiplayer? Dedicated or listen server? What are you implementing?

---

## Class Responsibility Map

Each class exists on specific machines for specific reasons. Getting this wrong is the primary source of multiplayer bugs.

### AGameModeBase / AGameMode — Server Only

**Exists on:** Server and standalone only. Never instantiated on clients.

**Why server-only:** GameMode is the authoritative referee. It decides who joins, when the match starts, where players spawn, and what the win conditions are. Client execution would allow cheating via local state manipulation.

**AGameMode adds** the full match-state machine (`EnteringMap` → `WaitingToStart` → `InProgress` → `WaitingPostMatch` → `LeavingMap`; `Aborted` on failure) with `ReadyToStartMatch` and `ReadyToEndMatch` hooks. Use `AGameModeBase` for lobby/simple games, `AGameMode` for match flow.

**Key API from source (GameModeBase.h):**
```cpp
// Class assignments — set in constructor
TSubclassOf<APawn>             DefaultPawnClass;
TSubclassOf<AGameStateBase>    GameStateClass;
TSubclassOf<APlayerController> PlayerControllerClass;
TSubclassOf<APlayerState>      PlayerStateClass;
TSubclassOf<AHUD>              HUDClass;
uint32                         bUseSeamlessTravel : 1;

// Server startup and player join lifecycle (server only)
virtual void InitGame(const FString& MapName, const FString& Options, FString& ErrorMessage);
virtual void PreLogin(const FString& Options, const FString& Address,
    const FUniqueNetIdRepl& UniqueId, FString& ErrorMessage);
virtual APlayerController* Login(UPlayer* NewPlayer, ENetRole InRemoteRole,
    const FString& Portal, const FString& Options,
    const FUniqueNetIdRepl& UniqueId, FString& ErrorMessage);
virtual void PostLogin(APlayerController* NewPlayer);   // first safe point for RPCs (DispatchPostLogin deprecated 5.6 — override PostLogin directly)
virtual void Logout(AController* Exiting);
virtual void HandleStartingNewPlayer(APlayerController* NewPlayer);

// Spawn pipeline
virtual AActor* FindPlayerStart(AController* Player, const FString& IncomingName = TEXT(""));
virtual void    RestartPlayer(AController* NewPlayer);
virtual APawn*  SpawnDefaultPawnFor(AController* NewPlayer, AActor* StartSpot);

// Travel
virtual void ProcessServerTravel(const FString& URL, bool bAbsolute = false);
virtual void GetSeamlessTravelActorList(bool bToTransition, TArray<AActor*>& ActorList);
```

---

### AGameStateBase / AGameState — Server + All Clients

**Exists on:** Everywhere. Fully replicated.

**Why everywhere:** Clients cannot read GameMode (it does not exist on them). Any global data clients need — scores, match timer, phase — belongs in GameState. `PlayerArray` exposes all connected `APlayerState` instances to every machine.

**Key API from source (GameStateBase.h):**
```cpp
// All PlayerStates, always replicated
UPROPERTY(Transient, BlueprintReadOnly)
TArray<TObjectPtr<APlayerState>> PlayerArray;

// The GameMode class (not instance) replicated to clients
UPROPERTY(Transient, BlueprintReadOnly, ReplicatedUsing=OnRep_GameModeClass)
TSubclassOf<AGameModeBase> GameModeClass;

// Server-authoritative clock, automatically synced
virtual double GetServerWorldTimeSeconds() const;
virtual bool   HasBegunPlay() const;
virtual bool   HasMatchStarted() const;
virtual bool   HasMatchEnded() const;
```

**Custom replicated match data:**
```cpp
UCLASS()
class AMyGameState : public AGameStateBase
{
    GENERATED_BODY()
public:
    UPROPERTY(Replicated, BlueprintReadOnly) int32 TeamAScore;
    UPROPERTY(Replicated, BlueprintReadOnly) int32 TeamBScore;
    UPROPERTY(ReplicatedUsing=OnRep_MatchTimer) float MatchTimeRemaining;

    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;
};

void AMyGameState::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME(AMyGameState, TeamAScore);
    DOREPLIFETIME(AMyGameState, TeamBScore);
    DOREPLIFETIME(AMyGameState, MatchTimeRemaining);
}
```

---

### APlayerController — Server (all) + Owning Client (own only)

**Exists on:** Server holds one per connected player. Each client holds only its own. Remote clients do not see other players' PlayerControllers.

**Why this split:** The PlayerController bridges one human to the server. Both ends run it for client-side prediction and server validation. A client has no reason to know another player's input state.

**Key API from source (PlayerController.h):**
```cpp
TObjectPtr<APlayerCameraManager> PlayerCameraManager;  // camera, local only
TObjectPtr<APawn>                AcknowledgedPawn;      // server-confirmed possession
TObjectPtr<AHUD>                 MyHUD;                 // local only

uint32 bShowMouseCursor : 1;
uint32 bEnableStreamingSource : 1;  // drives World Partition loading for this viewport

void SetInputMode(const FInputModeDataBase& InData); // FInputModeGameOnly, UIOnly, GameAndUI
virtual void PlayerTick(float DeltaTime);            // only ticked locally
virtual void SetupInputComponent() override;
```

**`SetupInputComponent` on PlayerController** is for non-pawn input: spectator actions, UI shortcuts, or global keybinds that persist across possession changes. For pawn-specific input, override `APawn::SetupPlayerInputComponent()` instead — see `ue-input-system`.

**Enhanced Input setup:**
```cpp
void AMyPlayerController::BeginPlay()
{
    Super::BeginPlay();
    if (IsLocalController())
    {
        if (auto* Sub = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(GetLocalPlayer()))
            Sub->AddMappingContext(DefaultMappingContext, 0);
        SetInputMode(FInputModeGameOnly());
    }
}
```

**RPC patterns:**
```cpp
UFUNCTION(Server, Reliable, WithValidation) void ServerRequestRespawn();   // client → server
UFUNCTION(Client, Reliable)                void ClientNotifyMatchStart();  // server → client
```

**Possess/UnPossess (server-authority required):**
```cpp
// Take control of a new pawn — must run on server
PlayerController->Possess(NewPawn);
// Release the currently possessed pawn
PlayerController->UnPossess();
```

**Listen-server dual-role:** On a listen server, the host's PlayerController is both `ROLE_Authority` and locally controlled. Guard dual-role logic with `IsLocalController()` checks. This is a common source of bugs where code assumes authority implies non-local (i.e., code written for dedicated servers runs incorrectly on a listen server host).

**ClientTravel — connect this client to a different server:**
```cpp
PlayerController->ClientTravel(TEXT("127.0.0.1:7777"), TRAVEL_Absolute);
```

**ServerTravel — move all players to a new map (called from GameMode, server only):**
```cpp
GetWorld()->ServerTravel(TEXT("/Game/Maps/NewMap?listen"));
```

---

### AController — Shared Base

`AController` is the base class for both `APlayerController` and `AAIController`. It owns the pawn possession interface (`Possess`, `UnPossess`, `GetPawn`) and the rotation used to drive pawn orientation (`ControlRotation`). Subclass `APlayerController` for human players and `AAIController` for AI.

---

### APlayerState — Server + All Clients (Always Relevant)

**Exists on:** Server and all clients. Marked always-relevant so it replicates to everyone regardless of distance.

**Why always relevant:** Scoreboards, team displays, and player lists need to show data for every player, not just nearby ones. PlayerState survives pawn death — when a pawn is destroyed and respawned, the PlayerController keeps its PlayerState, preserving accumulated stats.

```cpp
UCLASS()
class AMyPlayerState : public APlayerState
{
    GENERATED_BODY()
public:
    UPROPERTY(Replicated, BlueprintReadOnly) int32 Kills;
    UPROPERTY(Replicated, BlueprintReadOnly) int32 Deaths;
    UPROPERTY(ReplicatedUsing=OnRep_Team)   uint8 TeamIndex;
};

// Access patterns
APlayerState* PS = MyPawn->GetPlayerState();
APlayerState* PS = MyPC->PlayerState;
for (APlayerState* PS : GetGameState<AGameStateBase>()->PlayerArray) { /* all players */ }
```

---

### APawn — Server + All Clients (Replicated)

**Exists on:** Server (authority) and all clients (simulated or autonomous proxy). Minimal base — no mesh, no collision component, no movement component.

**Use APawn when:** entity is not a humanoid (vehicle, turret, drone), you need a completely custom movement component, or you need zero-overhead baseline.

```cpp
// Minimal subclass pattern
virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;
virtual void PossessedBy(AController* NewController) override;
virtual void UnPossessed() override;
```

`ADefaultPawn` is the engine's built-in pawn with floating movement (no gravity) and a sphere collision root. It is used as the `DefaultPawnClass` placeholder when no custom pawn is assigned.

---

### ACharacter — Server + All Clients (Replicated with Prediction)

**Exists on:** Server (authority) and all clients. The locally controlled instance runs client-side prediction; simulated proxies interpolate from server updates.

**Why ACharacter:** Walking humanoids need capsule collision, gravity, jump, crouch, and movement prediction. ACharacter bundles all of this with built-in networked prediction via `UCharacterMovementComponent`.

**Component layout from source (Character.h):**
```cpp
// Private, access via getters
TObjectPtr<UCapsuleComponent>          CapsuleComponent;    // GetCapsuleComponent() — root
TObjectPtr<USkeletalMeshComponent>     Mesh;                // GetMesh()
TObjectPtr<UCharacterMovementComponent> CharacterMovement;  // GetCharacterMovement()
TObjectPtr<UArrowComponent>            ArrowComponent;      // GetArrowComponent() — editor-only direction indicator
```

**Constructor configuration:**
```cpp
AMyCharacter::AMyCharacter()
{
    GetCapsuleComponent()->SetCapsuleHalfHeight(96.f);
    GetCapsuleComponent()->SetCapsuleRadius(42.f);
    GetMesh()->SetRelativeLocation(FVector(0.f, 0.f, -97.f));
    GetMesh()->SetRelativeRotation(FRotator(0.f, -90.f, 0.f));

    GetCharacterMovement()->MaxWalkSpeed = 600.f;
    GetCharacterMovement()->JumpZVelocity = 700.f;
    GetCharacterMovement()->GravityScale = 1.75f;
    GetCharacterMovement()->AirControl = 0.35f;
    GetCharacterMovement()->NavAgentProps.bCanCrouch = true;
}
```

**Key ACharacter API from source:**
```cpp
// Jump — from Character.h
virtual void Jump();          // set bPressedJump, triggers on next tick
virtual void StopJumping();   // clear bPressedJump
bool CanJump() const;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Replicated) float JumpMaxHoldTime; // variable height
UPROPERTY(EditAnywhere, BlueprintReadWrite, Replicated) int32 JumpMaxCount;    // double jump

virtual void LaunchCharacter(FVector LaunchVelocity, bool bXYOverride, bool bZOverride);

// Crouch
void Crouch(bool bClientSimulation = false);   // requests crouch via CharacterMovementComponent
void UnCrouch(bool bClientSimulation = false);
UPROPERTY(BlueprintReadOnly, ReplicatedUsing=OnRep_IsCrouched) uint8 bIsCrouched : 1;

// Movement mode
// MOVE_Walking, MOVE_Falling, MOVE_Swimming, MOVE_Flying, MOVE_Custom
GetCharacterMovement()->SetMovementMode(MOVE_Flying);
```

**Custom movement modes:** Set `MOVE_Custom` then override `PhysCustom(float deltaTime, int32 Iterations)` in your `UCharacterMovementComponent` subclass. The `CustomMovementMode` byte lets you distinguish multiple custom modes within the same `PhysCustom` dispatch.

```cpp
// Custom movement mode: override in CMC subclass
void UMyCharacterMovement::PhysCustom(float DeltaTime, int32 Iterations)
{
    if (CustomMovementMode == (uint8)ECustomMovement::Flying)
    {
        // Custom flying physics here
        Velocity.Z += GetGravityZ() * DeltaTime;
    }
    Super::PhysCustom(DeltaTime, Iterations);
}
// Activate: CharMoveComp->SetMovementMode(MOVE_Custom, (uint8)ECustomMovement::Flying);
```

**Movement replication:** Client sends `ServerMovePacked`, server validates and replies via `ClientMoveResponsePacked`. This is automatic — do not call these RPCs manually.

---

### UGameInstance — Process Lifetime Singleton

**Exists on:** One per process. Survives ALL level loads.

**Why:** On level travel, every actor (including GameMode, GameState, PlayerController, PlayerState) is destroyed. GameInstance is never destroyed. It holds session handles, save game references, analytics state, and any data that must span the entire application lifetime.

```cpp
// Lifecycle overrides
virtual void Init() override;      // called once at startup; subsystem init, save-game loading
virtual void OnStart() override;   // called when the instance is ready, after Init
virtual void Shutdown() override;  // called on application exit

// Access from actor or component
UMyGameInstance* GI = GetWorld()->GetGameInstance<UMyGameInstance>();

// Subsystems (also survive level travel)
UMySubsystem* Sub = GetGameInstance()->GetSubsystem<UMySubsystem>();
```

### Session Management (Online Subsystem)

```cpp
// Access the Online Subsystem session interface from GameInstance
IOnlineSubsystem* OSS = IOnlineSubsystem::Get();
IOnlineSessionPtr Sessions = OSS ? OSS->GetSessionInterface() : nullptr;
if (!Sessions.IsValid()) return;

// Create session (host)
FOnlineSessionSettings Settings;
Settings.bIsLANMatch = false;
Settings.NumPublicConnections = 4;
Settings.bShouldAdvertise = true;
Sessions->OnCreateSessionCompleteDelegates.AddUObject(
    this, &UMyGameInstance::OnCreateSessionComplete);
Sessions->CreateSession(0, NAME_GameSession, Settings);

// Find sessions (client)
TSharedRef<FOnlineSessionSearch> Search = MakeShared<FOnlineSessionSearch>();
Sessions->OnFindSessionsCompleteDelegates.AddUObject(
    this, &UMyGameInstance::OnFindSessionsComplete);
Sessions->FindSessions(0, Search);

// Join a found session
Sessions->OnJoinSessionCompleteDelegates.AddUObject(
    this, &UMyGameInstance::OnJoinSessionComplete);
Sessions->JoinSession(0, NAME_GameSession, Search->SearchResults[0]);
```

The Online Subsystem abstracts platform-specific backends (Steam, EOS, Null for testing). Add `"OnlineSubsystem"` and `"OnlineSubsystemUtils"` to your Build.cs dependencies. After joining, retrieve the connect string with `GetResolvedConnectString` and call `ClientTravel`.

---

## GameMode: Registration and Spawn Pipeline

```cpp
AMyGameMode::AMyGameMode()
{
    DefaultPawnClass      = AMyCharacter::StaticClass();
    PlayerControllerClass = AMyPlayerController::StaticClass();
    GameStateClass        = AMyGameState::StaticClass();
    PlayerStateClass      = AMyPlayerState::StaticClass();
    HUDClass              = AMyHUD::StaticClass();
    bUseSeamlessTravel    = true;
}
```

**Join sequence (server only):**
```
InitGame()            → called before any player joins; use for map-specific rules init
PreLogin()            → reject here (server full, banned)
Login()               → create PlayerController, assign UniqueId
PostLogin()           → first safe point for server→client RPCs; assign teams here
HandleStartingNewPlayer() → triggers RestartPlayer()
RestartPlayer()       → FindPlayerStart() → SpawnDefaultPawnFor() → Possess()
```

**Match state (AGameMode only):**
```cpp
bool AMyGameMode::ReadyToStartMatch_Implementation()
{
    return GetNumPlayers() >= MinPlayersToStart;
}
bool AMyGameMode::ReadyToEndMatch_Implementation()
{
    return GetGameState<AMyGameState>()->TeamAScore >= ScoreLimit;
}
```

---

## Travel Patterns

| Pattern | Clients disconnect? | GameMode/GameState survive? | Use when |
|---|---|---|---|
| Non-seamless (`ServerTravel`) | Yes, reconnect | No, recreated | Map change with clean slate |
| Seamless (`bUseSeamlessTravel=true`) | No | No, recreated | Lobby→game, round change |

**Seamless travel survival:**
- Always: `UGameInstance`, `APlayerController`, `APlayerState`
- Never: `AGameMode`, `AGameState`, level actors
- Optional: actors you add in `GetSeamlessTravelActorList()`

---

## Common Mistakes

**GameMode on client (null crash):**
```cpp
// WRONG
GetWorld()->GetAuthGameMode<AMyGameMode>()->EndMatch(); // nullptr on client
// RIGHT
if (HasAuthority()) { if (auto* GM = GetWorld()->GetAuthGameMode<AMyGameMode>()) GM->EndMatch(); }
```

**Wrong class for data:**
```
Score visible to all clients  → APlayerState, NOT APlayerController
Match timer on clients        → AGameState replicated property, NOT AGameMode
Data surviving level travel   → UGameInstance, NOT AGameState
Input binding                 → PlayerController or Pawn::SetupPlayerInputComponent, NOT ACharacter body
```

**AcknowledgedPawn vs GetPawn:**
`GetPawn()` on a PlayerController may return a pawn before the server confirms possession. Use `AcknowledgedPawn` when you need the server-confirmed pawn.

**Dedicated server guard:**
```cpp
if (GetNetMode() != NM_DedicatedServer)
{
    // HUD, camera, audio — never run these on dedicated server
}
```

**PIE multi-player:** In PIE with multiple players, each has its own PlayerController but all share the same GameMode instance. Test multiplayer logic with PIE > Number of Players set to 2 or more.

---

## Related Skills

- `ue-actor-component-architecture` — actor lifecycle, component tick, attachment
- `ue-networking-replication` — DOREPLIFETIME conditions, RPC patterns, push model
- `ue-input-system` — Enhanced Input mapping contexts and input actions
