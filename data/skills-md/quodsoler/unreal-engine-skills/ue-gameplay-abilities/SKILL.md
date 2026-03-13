---
name: ue-gameplay-abilities
description: "Use this skill when working with GAS, Gameplay Ability System, GameplayAbility, GameplayEffect, AttributeSet, GameplayTags, ability system, buffs, debuffs, cooldowns, or attribute modification. See references/ for detailed setup patterns, effect configuration, and ability task usage."
metadata:
  version: 1.0.0
---

# Gameplay Ability System (GAS)

You are an expert in Unreal Engine's Gameplay Ability System (GAS).

## Context Check

Before proceeding, read `.agents/ue-project-context.md` to determine:
- Whether the GameplayAbilities plugin is enabled
- Which actors own the AbilitySystemComponent (PlayerState vs Character)
- The replication mode in use (Minimal, Mixed, Full)
- Any existing AttributeSets or ability base classes

## Information Gathering

Ask the developer:
1. What type of abilities are needed? (active, passive, triggered, instant)
2. What attributes are required? (health, mana, stamina, custom stats)
3. Is this multiplayer? If so, which actors carry the ASC?
4. Are cooldowns and costs required, or is this a passive/trigger system?
5. Do abilities need prediction (local-only feedback before server confirms)?

---

## GAS Architecture Overview

GAS has three pillars that live on `UAbilitySystemComponent` (ASC):

| Pillar | Class | Purpose |
|--------|-------|---------|
| Abilities | `UGameplayAbility` | Logic for what happens when activated |
| Effects | `UGameplayEffect` | Data-driven stat mutations (instant, duration, infinite) |
| Attributes | `UAttributeSet` | Float properties representing character stats |

GameplayTags thread through all three as requirements, grants, and blockers.

---

## GAS Setup

### 1. Enable the Plugin

Enable `GameplayAbilities` in `.uproject` Plugins array, then in `[ProjectName].Build.cs`:
```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "GameplayAbilities", "GameplayTags", "GameplayTasks"
});
```

### 2. AbilitySystemComponent Ownership

**PlayerState (recommended for multiplayer):** ASC persists across respawns because PlayerState
is not destroyed on death. Use this for player characters in networked games.

**Character/Pawn:** Simpler. Use for AI characters or single-player games where persistence
across respawns is not required.

See `references/gas-setup-patterns.md` for full initialization sequences for both patterns.

### 3. IAbilitySystemInterface

Every actor that owns or exposes an ASC must implement `IAbilitySystemInterface`:

```cpp
#include "AbilitySystemInterface.h"

UCLASS()
class AMyCharacter : public ACharacter, public IAbilitySystemInterface
{
    GENERATED_BODY()
public:
    virtual UAbilitySystemComponent* GetAbilitySystemComponent() const override
        { return AbilitySystemComponent; }
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "GAS")
    TObjectPtr<UAbilitySystemComponent> AbilitySystemComponent;
};
```

### 4. Replication Modes

Set on the ASC after creation (server-side only):

```cpp
// In BeginPlay or PossessedBy on the server:
AbilitySystemComponent->SetReplicationMode(EGameplayEffectReplicationMode::Mixed);
```

| Mode | When to Use |
|------|-------------|
| `Minimal` | AI or non-player actors; no GE replication to simulated proxies |
| `Mixed` | Player-controlled characters (owner gets full info, others get minimal) |
| `Full` | Non-player games or debugging; all GEs replicate to all clients |

### 5. InitAbilityActorInfo

Must be called on both server and client after possession. Call in `PossessedBy` (server)
and `OnRep_PlayerState` (client): `ASC->InitAbilityActorInfo(OwnerActor, AvatarActor)`.
See `references/gas-setup-patterns.md` for full dual-path code with respawn handling.

---

## GameplayAbilities

### Subclass UGameplayAbility

```cpp
#include "Abilities/GameplayAbility.h"

UCLASS()
class UMyFireballAbility : public UGameplayAbility
{
    GENERATED_BODY()
public:
    UMyFireballAbility();
    virtual void ActivateAbility(const FGameplayAbilitySpecHandle Handle,
        const FGameplayAbilityActorInfo* ActorInfo,
        const FGameplayAbilityActivationInfo ActivationInfo,
        const FGameplayEventData* TriggerEventData) override;
    virtual void EndAbility(const FGameplayAbilitySpecHandle Handle,
        const FGameplayAbilityActorInfo* ActorInfo,
        const FGameplayAbilityActivationInfo ActivationInfo,
        bool bReplicateEndAbility, bool bWasCancelled) override;
    // Ability Tasks — async building blocks for latent abilities:
    // UAbilityTask_WaitTargetData    — waits for targeting (crosshair/AoE confirm)
    // UAbilityTask_WaitGameplayEvent — waits for a GameplayEvent tag (e.g., anim notify)
    // UAbilityTask_WaitDelay         — simple timer
    // UAbilityTask_PlayMontageAndWait — montage with callbacks (see ue-animation-system)
    // See references/ability-task-reference.md for full list and custom task pattern.
    // CancelAbility — called by CancelAbilitiesWithTag or ASC->CancelAbility(Handle)
    // Internally calls EndAbility with bWasCancelled=true. Override to add cleanup:
    virtual void CancelAbility(const FGameplayAbilitySpecHandle Handle,
        const FGameplayAbilityActorInfo* ActorInfo,
        const FGameplayAbilityActivationInfo ActivationInfo,
        bool bReplicateCancelAbility) override;
    // Custom activation guard — return false to block activation beyond tag checks
    virtual bool CanActivateAbility(const FGameplayAbilitySpecHandle Handle,
        const FGameplayAbilityActorInfo* ActorInfo, /*...*/) const override;
    // Must call Super first. Add custom checks (resource availability, cooldown state).
protected:
    UPROPERTY(EditDefaultsOnly, Category = "GAS")
    TSubclassOf<UGameplayEffect> DamageEffect;
};
```

### ActivateAbility Pattern

```cpp
void UMyFireballAbility::ActivateAbility(const FGameplayAbilitySpecHandle Handle,
    const FGameplayAbilityActorInfo* ActorInfo,
    const FGameplayAbilityActivationInfo ActivationInfo,
    const FGameplayEventData* TriggerEventData)
{
    // 1. Commit: validates and applies cost + cooldown
    if (!CommitAbility(Handle, ActorInfo, ActivationInfo))
    {
        EndAbility(Handle, ActorInfo, ActivationInfo, true, true);
        return;
    }
    // 2. Apply effect / spawn projectile / etc.
    FGameplayEffectSpecHandle Spec = MakeOutgoingGameplayEffectSpec(DamageEffect, GetAbilityLevel());
    FGameplayAbilityTargetDataHandle TargetData =
        UAbilitySystemBlueprintLibrary::AbilityTargetDataFromActor(
            ActorInfo->AvatarActor.Get());
    ApplyGameplayEffectSpecToTarget(Handle, ActorInfo, ActivationInfo, Spec, TargetData);
    // 3. End (instant abilities end immediately; latent abilities wait for tasks)
    EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
}
```

`CommitAbility` is shorthand for `CommitAbilityCost` + `CommitAbilityCooldown`. Call them
separately when needed -- e.g., commit cost without starting cooldown for a channeled ability,
or commit cooldown without cost for a free ability.

### Instancing and Net Execution Policy

Set in the ability constructor:

```cpp
UMyFireballAbility::UMyFireballAbility()
{
    // InstancedPerActor  - one instance per actor; cheapest for persistent abilities
    // InstancedPerExecution - new instance each activation; safe for concurrency
    // NonInstanced       - CDO runs the ability; no per-execution state
    InstancingPolicy = EGameplayAbilityInstancingPolicy::InstancedPerActor;

    // LocalPredicted  - client runs immediately, server validates (player abilities)
    // ServerOnly      - authority only, no prediction
    // LocalOnly       - local client only (UI, cosmetic)
    // ServerInitiated - server activates, clients run non-authoritative predicted copy
    NetExecutionPolicy = EGameplayAbilityNetExecutionPolicy::LocalPredicted;
}
```

### Granting and Activating Abilities

```cpp
// Grant (server/authority only):
FGameplayAbilitySpecHandle Handle = ASC->GiveAbility(
    FGameplayAbilitySpec(UMyFireballAbility::StaticClass(), 1 /*Level*/));

ASC->TryActivateAbility(Handle);                                       // by handle
ASC->TryActivateAbilityByClass(UMyFireballAbility::StaticClass());    // by class
ASC->TryActivateAbilitiesByTag(                                        // by tag
    FGameplayTagContainer(FGameplayTag::RequestGameplayTag("Ability.Skill.Fireball")));
```

### Ability Tags

Configure in the ability CDO constructor:

```cpp
// Tags this ability grants to its owner while active:
ActivationOwnedTags.AddTag(FGameplayTag::RequestGameplayTag("Ability.Active.Casting"));
// Tags that prevent this ability from activating:
ActivationBlockedTags.AddTag(FGameplayTag::RequestGameplayTag("State.Stunned"));
// Cancel other active abilities with these tags on activation:
CancelAbilitiesWithTag.AddTag(FGameplayTag::RequestGameplayTag("Ability.Active.Melee"));
```

---

## GameplayEffects

### Duration Policies

| Policy | Behavior |
|--------|----------|
| `Instant` | Executes once; modifies attribute base value permanently |
| `HasDuration` | Active for set duration; uses `DurationMagnitude` (seconds) |
| `Infinite` | Active until `RemoveActiveGameplayEffect` is called |

### Applying Effects

```cpp
FGameplayEffectContextHandle Ctx = ASC->MakeEffectContext();
FGameplayEffectSpecHandle Spec = ASC->MakeOutgoingSpec(UMyDamageEffect::StaticClass(), Level, Ctx);

// SetByCaller: inject runtime magnitude using a tag key
Spec.Data->SetSetByCallerMagnitude(
    FGameplayTag::RequestGameplayTag("SetByCaller.Damage"), 75.f);

ASC->ApplyGameplayEffectSpecToSelf(*Spec.Data.Get());         // self
ASC->ApplyGameplayEffectSpecToTarget(*Spec.Data.Get(), TargetASC); // target

ASC->RemoveActiveGameplayEffect(ActiveHandle);                // by handle
ASC->RemoveActiveGameplayEffectBySourceEffect(
    UMyDamageEffect::StaticClass(), nullptr);                  // by class
```

See `references/gameplay-effect-reference.md` for stacking (AggregateBySource/AggregateByTarget),
periodic effects (damage over time), `UGameplayEffectExecutionCalculation` (complex modifier logic),
conditional effects, and immunity.

---

## AttributeSet

### Define Attributes

```cpp
// MyHealthSet.h
#include "AttributeSet.h"
#include "AbilitySystemComponent.h"

// Convenience macro - define in your project headers
#define ATTRIBUTE_ACCESSORS(ClassName, PropertyName) \
    GAMEPLAYATTRIBUTE_PROPERTY_GETTER(ClassName, PropertyName) \
    GAMEPLAYATTRIBUTE_VALUE_GETTER(PropertyName) \
    GAMEPLAYATTRIBUTE_VALUE_SETTER(PropertyName) \
    GAMEPLAYATTRIBUTE_VALUE_INITTER(PropertyName)

UCLASS()
class UMyHealthSet : public UAttributeSet
{
    GENERATED_BODY()
public:
    UMyHealthSet();

    // Called BEFORE any modification - use for clamping current value
    virtual void PreAttributeChange(const FGameplayAttribute& Attribute, float& NewValue) override;

    // Called AFTER instant GE executes - react to changes (death, events)
    virtual void PostGameplayEffectExecute(const FGameplayEffectModCallbackData& Data) override;

    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;

    UPROPERTY(BlueprintReadOnly, ReplicatedUsing = OnRep_Health, Category = "Health")
    FGameplayAttributeData Health;
    ATTRIBUTE_ACCESSORS(UMyHealthSet, Health)

    UPROPERTY(BlueprintReadOnly, ReplicatedUsing = OnRep_MaxHealth, Category = "Health")
    FGameplayAttributeData MaxHealth;
    ATTRIBUTE_ACCESSORS(UMyHealthSet, MaxHealth)

protected:
    UFUNCTION()
    void OnRep_Health(const FGameplayAttributeData& OldHealth);

    UFUNCTION()
    void OnRep_MaxHealth(const FGameplayAttributeData& OldMaxHealth);
};
```

In the `.cpp`, implement replication and callbacks:

```cpp
void UMyHealthSet::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME_CONDITION_NOTIFY(UMyHealthSet, Health, COND_None, REPNOTIFY_Always);
    DOREPLIFETIME_CONDITION_NOTIFY(UMyHealthSet, MaxHealth, COND_None, REPNOTIFY_Always);
}

void UMyHealthSet::OnRep_Health(const FGameplayAttributeData& OldHealth)
{
    GAMEPLAYATTRIBUTE_REPNOTIFY(UMyHealthSet, Health, OldHealth);
}

// PreAttributeChange: clamp CURRENT value before any modification
void UMyHealthSet::PreAttributeChange(const FGameplayAttribute& Attribute, float& NewValue)
{
    Super::PreAttributeChange(Attribute, NewValue);
    if (Attribute == GetHealthAttribute())
        NewValue = FMath::Clamp(NewValue, 0.f, GetMaxHealth());
}

// PostGameplayEffectExecute: react AFTER instant GE modifies base value (damage, death)
void UMyHealthSet::PostGameplayEffectExecute(const FGameplayEffectModCallbackData& Data)
{
    Super::PostGameplayEffectExecute(Data);
    if (Data.EvaluatedData.Attribute == GetHealthAttribute())
    {
        SetHealth(FMath::Clamp(GetHealth(), 0.f, GetMaxHealth()));
        if (GetHealth() <= 0.f) { /* trigger death */ }
    }
}
```

### Register AttributeSet on ASC

```cpp
// In PlayerState or Character constructor:
// Option 1: CreateDefaultSubobject (auto-registered as subobject)
HealthSet = CreateDefaultSubobject<UMyHealthSet>(TEXT("HealthSet"));

// Option 2: Runtime (authority only) — create and register as subobject:
UMyHealthSet* NewSet = NewObject<UMyHealthSet>(this);
AbilitySystemComponent->AddSpawnedAttribute(NewSet);

// Read attribute value:
float CurrentHealth = AbilitySystemComponent->GetNumericAttribute(
    UMyHealthSet::GetHealthAttribute());
```

**Multiple AttributeSets**: An ASC can host multiple `UAttributeSet` subclasses (e.g.,
`UHealthSet` + `UOffenseSet`), each auto-discovered via subobject enumeration. Never register
two instances of the same class -- the second is silently ignored.

---

## GameplayTags

### Defining Tags

In `Config/DefaultGameplayTags.ini` or via native tags (preferred for code references):

```cpp
// MyGameplayTags.h
#include "NativeGameplayTags.h"
UE_DECLARE_GAMEPLAY_TAG_EXTERN(TAG_Ability_Fireball)
UE_DECLARE_GAMEPLAY_TAG_EXTERN(TAG_State_Stunned)

// MyGameplayTags.cpp
UE_DEFINE_GAMEPLAY_TAG_COMMENT(TAG_Ability_Fireball, "Ability.Skill.Fireball", "Fireball ability")
UE_DEFINE_GAMEPLAY_TAG_COMMENT(TAG_State_Stunned, "State.Stunned", "Actor is stunned")
```

### Tag Matching

`"A.1".MatchesTag("A") == true` (hierarchical); `MatchesTagExact` requires exact match.

```cpp
FGameplayTagContainer Tags;
Tags.HasTag(FireballTag);      // parent-aware match
Tags.HasTagExact(FireballTag); // exact only
Tags.HasAny(OtherContainer);
Tags.HasAll(OtherContainer);

// Query ASC:
ASC->HasMatchingGameplayTag(TAG_State_Stunned);
ASC->GetOwnedGameplayTags(); // FGameplayTagContainer

// Listen for changes:
ASC->RegisterGameplayTagEvent(TAG_State_Stunned, EGameplayTagEventType::NewOrRemoved)
    .AddUObject(this, &AMyCharacter::OnStunnedTagChanged);
```

### Loose Tags (Manual, No GE)

```cpp
ASC->AddLooseGameplayTag(TAG_State_Stunned);
ASC->RemoveLooseGameplayTag(TAG_State_Stunned);
// Loose tags are NOT replicated by default. To replicate a loose tag,
// pass EGameplayTagReplicationState::TagOnly as the third argument:
ASC->AddLooseGameplayTag(TAG_State_Buffed, 1, EGameplayTagReplicationState::TagOnly);
ASC->RemoveLooseGameplayTag(TAG_State_Buffed, 1, EGameplayTagReplicationState::TagOnly);
```

---

## GameplayCues

Cosmetic-only (particles, sounds, decals). Never affect gameplay state. Tag prefix: `GameplayCue.`

In the GE asset, add `FGameplayEffectCue` entries with `GameplayCueTags` and level range.

```cpp
// Burst (one-shot):
ASC->ExecuteGameplayCue(FGameplayTag::RequestGameplayTag("GameplayCue.Hit.Fire"),
    ASC->MakeEffectContext());

// Persistent (add/remove pair):
ASC->AddGameplayCue(FGameplayTag::RequestGameplayTag("GameplayCue.Buff.Speed"));
ASC->RemoveGameplayCue(FGameplayTag::RequestGameplayTag("GameplayCue.Buff.Speed"));

// Poll active state:
bool bActive = ASC->IsGameplayCueActive(FGameplayTag::RequestGameplayTag("GameplayCue.Buff.Speed"));
```

Cue Notify classes:
- `AGameplayCueNotify_Actor`: Persistent/looping. Overrides `OnActive`, `WhileActive`, `OnRemove`.
- `AGameplayCueNotify_Static`: Burst/one-shot. Overrides `OnExecute`.

Place cue notify assets in `/Game/GAS/GameplayCues/` for `UGameplayCueManager` auto-discovery.

---

## Common Mistakes and Anti-Patterns

**ASC ownership confusion:** Implement `IAbilitySystemInterface` on the class that *owns* the ASC
(PlayerState), not just on the Pawn. Otherwise `UAbilitySystemBlueprintLibrary` lookups fail.

**InitAbilityActorInfo only on server:** Clients need it too. Call in `OnRep_PlayerState` (client)
and `PossessedBy` (server). Skipping client-side init breaks attribute replication on the owning client.

**GEs applied before InitAbilityActorInfo:** The ASC is not ready; attributes are not registered.
Always complete init before granting abilities or applying effects.

**PreAttributeChange vs PostGameplayEffectExecute:** `PreAttributeChange` fires on every current-value
change (aggregator updates, buff adds/removes). Use it only to clamp. Use `PostGameplayEffectExecute`
to react to instant GE base-value execution (damage, death). Never send game events from `PreAttributeChange`.

**Forgetting CommitAbility:** Without it, the ability runs but consumes no mana and starts no cooldown.

**Loose tags not replicated:** `AddLooseGameplayTag` does not replicate by default. Pass
`EGameplayTagReplicationState::TagOnly` as the third argument to replicate the tag, or grant
via a GE for fully replicated effect-driven tags.

**Effect stacking overflow:** Stacks beyond `LimitCount` are silently rejected. Use `GetCurrentStackCount`
to inspect the current level before attempting further stack applications.

**GAS with AI:** AI has no PlayerState. Place the ASC on the AICharacter, call
`InitAbilityActorInfo(AICharacter, AICharacter)`, set replication mode to `Minimal`.

**Hot-joining**: Late-joining clients receive active effects via `FActiveGameplayEffectsContainer`
replication after `InitAbilityActorInfo`. Never apply startup GEs in `BeginPlay` unconditionally
-- server-only, or late joiners double-apply.

---

## Reference Files

- `references/gas-setup-patterns.md` — Full ASC ownership patterns and initialization sequences
  for PlayerState and Character owners, multiplayer and single-player
- `references/gameplay-effect-reference.md` — Effect configuration, stacking rules, modifier
  types, execution calculations, periodic effects, conditional effects
- `references/ability-task-reference.md` — Common built-in ability tasks and custom task patterns

## Related Skills

- `ue-actor-component-architecture` — Component setup and subobject registration
- `ue-networking-replication` — Replication modes, RPCs, prediction keys
- `ue-animation-system` — Montage ability tasks (PlayMontageAndWait)
- `ue-gameplay-framework` — PlayerState ownership pattern, Pawn/Controller lifecycle
- `ue-cpp-foundations` — Delegate binding, UPROPERTY macros, TSubclassOf patterns
