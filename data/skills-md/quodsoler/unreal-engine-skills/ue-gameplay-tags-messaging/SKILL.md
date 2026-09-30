---
name: ue-gameplay-tags-messaging
description: "Use when defining, querying or replicating Gameplay Tags, or wiring decoupled event messaging between gameplay systems in C++. Also use when the user mentions 'FGameplayTag', 'FGameplayTagContainer', 'FGameplayTagQuery', 'UE_DEFINE_GAMEPLAY_TAG', 'native gameplay tag', 'DefaultGameplayTags.ini', 'GameplayTagList', 'tag redirect', 'MatchesTag', 'HasTagExact', 'RequestGameplayTag', 'UGameplayTagsManager', 'Categories meta', 'tag picker', 'gameplay message', 'message bus', 'event bus' or 'AsyncMessageSystem'. For abilities, effects and cues that consume tags, see ue-gameplay-abilities; for wire cost and RPCs, see ue-networking-replication."
metadata:
  version: "2.0.0"
  engine: "5.8"
---

# UE Gameplay Tags and Messaging

Target engine: **UE 5.8**. APIs below are verified against the 5.8 headers; older forms are listed under "Deprecated — do not use".

Gameplay Tags are a built-in runtime module, not a plugin: add `"GameplayTags"` to `PublicDependencyModuleNames` in your `Build.cs` and include `GameplayTagContainer.h` / `NativeGameplayTags.h` / `GameplayTagsManager.h`. This skill owns tag definition (native and ini), `FGameplayTag`, `FGameplayTagContainer`, `FGameplayTagQuery`, `UGameplayTagsManager`, editor filtering, and decoupled gameplay messaging — including the `AsyncMessageSystem` plugin (Experimental in 5.8).

## Context

Read `.agents/ue-project-context.md` if it exists (module names, conventions, enabled plugins, GAS/networking setup). Do not stop if it is missing.

Identify the area from the request and the codebase. Ask only when two plausible readings would produce different code.

| Request is about… | Go to |
|---|---|
| Declaring tags in C++, native tag macros, module setup | [Native Tag Definitions](#native-tag-definitions) |
| Declaring tags in `.ini`, data tables, renaming a tag | [Ini and Data Table Tag Sources](#ini-and-data-table-tag-sources) |
| Testing a tag, container membership, parent vs exact | [Matching Semantics](#matching-semantics) |
| Multi-tag conditions, AND/OR/NOT, designer-authored rules | [Tag Queries](#tag-queries) |
| Actors exposing tags, gates and states built from tags | [Tag-Driven Design](#tag-driven-design) |
| Sending tags over the network, tag cost, hot paths | [Replication and Performance](#replication-and-performance) |
| Broadcasting events between systems without hard references | [Decoupled Messaging](#decoupled-messaging) |
| Tag pickers, `Categories` filtering, per-team tag files | [Editor UX and Filtering](#editor-ux-and-filtering) |

## Tag Sources

A tag must be registered before it can be requested. Four sources feed the one global dictionary held by `UGameplayTagsManager`:

| Source | Where | Use for |
|---|---|---|
| Native | `UE_DEFINE_GAMEPLAY_TAG*` in a module `.cpp` | Tags C++ compares against by name |
| Default ini | `Config/DefaultGameplayTags.ini`, `+GameplayTagList=` | Tags authored by designers |
| Extra ini | `Config/Tags/*.ini` and plugin config dirs | Per-team or per-plugin tag lists |
| Data table | `UDataTable` of `FGameplayTagTableRow` listed in `GameplayTagTableList` | Bulk import from a spreadsheet |

`EGameplayTagSourceType` (`Native`, `DefaultTagList`, `TagList`, `RestrictedTagList`, `DataTable`, `Invalid`) names these in the editor. Tags are hierarchical: registering `MyGame.State.Stunned` implicitly registers `MyGame.State` and `MyGame`.

## Native Tag Definitions

Declare in a public header, define in exactly one `.cpp` of the same module. The macros `static_assert` that they are used from a `.cpp`.

```cpp
// MyGameplayTags.h
#pragma once

#include "NativeGameplayTags.h"

MYGAME_API UE_DECLARE_GAMEPLAY_TAG_EXTERN(TAG_MyGame_State_Stunned);
MYGAME_API UE_DECLARE_GAMEPLAY_TAG_EXTERN(TAG_MyGame_Damage_Fire);
MYGAME_API UE_DECLARE_GAMEPLAY_TAG_EXTERN(TAG_MyGame_Message_ScoreChanged);
```

```cpp
// MyGameplayTags.cpp
#include "MyGameplayTags.h"

UE_DEFINE_GAMEPLAY_TAG_COMMENT(TAG_MyGame_State_Stunned, "MyGame.State.Stunned", "Character cannot act");
UE_DEFINE_GAMEPLAY_TAG_COMMENT(TAG_MyGame_Damage_Fire, "MyGame.Damage.Fire", "Fire damage channel");
UE_DEFINE_GAMEPLAY_TAG_COMMENT(TAG_MyGame_Message_ScoreChanged, "MyGame.Message.ScoreChanged", "Score changed broadcast");
```

| Macro | Parameters | Effect |
|---|---|---|
| `UE_DECLARE_GAMEPLAY_TAG_EXTERN` | `(TagName)` | `extern FNativeGameplayTag TagName;` — goes in the header, prefixed with your `_API` macro |
| `UE_DEFINE_GAMEPLAY_TAG` | `(TagName, Tag)` | Defines the variable with an empty dev comment |
| `UE_DEFINE_GAMEPLAY_TAG_COMMENT` | `(TagName, Tag, Comment)` | Same plus a developer comment shown in the editor |
| `UE_DEFINE_GAMEPLAY_TAG_STATIC` | `(TagName, Tag)` | `static` — visible only inside that one `.cpp`, with no matching declaration in a header |

`Tag` and `Comment` are bare string literals: the macro wraps `Comment` in `TEXT()` itself. Writing `TEXT("…")` there does not compile.

`FNativeGameplayTag` registers on static construction and unregisters when the module unloads, so tags from a plugin disappear cleanly with the plugin. It converts implicitly to `FGameplayTag` and also exposes `GetTag()`:

```cpp
const FGameplayTag Stunned = TAG_MyGame_State_Stunned.GetTag();
if (OwnedTags.HasTag(TAG_MyGame_State_Stunned))
{
    return;
}
```

**One definition rule:** exactly one `UE_DEFINE_GAMEPLAY_TAG` (or `_COMMENT` / `_STATIC`) per tag variable per binary. Two modules defining the same tag string is fine (the manager reference-counts registrations), but two definitions of the same *variable* is a link error, and a definition in a header breaks every translation unit that includes it.

To register a tag whose name is only known at runtime, call the manager directly:

```cpp
const FGameplayTag Runtime = UGameplayTagsManager::Get().AddNativeGameplayTag(
    FName(TEXT("MyGame.Generated.Slot01")), TEXT("Generated at startup"));
```

`AddNativeGameplayTag` after startup invalidates fast replication (see [Replication and Performance](#replication-and-performance)). Register from `CallOrRegister_OnAddNativeTagsDelegate`, and run code that *consumes* tags from `CallOrRegister_OnDoneAddingNativeTagsDelegate`:

```cpp
// MyGameModule.cpp — FDelegateHandle NativeTagsHandle; is a member of FMyGameModule.
#include "MyGameModule.h"
#include "GameplayTagsManager.h"

void FMyGameModule::StartupModule()
{
    NativeTagsHandle = UGameplayTagsManager::CallOrRegister_OnDoneAddingNativeTagsDelegate(
        FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FMyGameModule::OnTagsReady));
}

void FMyGameModule::ShutdownModule()
{
    UGameplayTagsManager::UnregisterNativeTagDelegate(NativeTagsHandle);
}
```

If registration already finished, `CallOrRegister_OnDoneAddingNativeTagsDelegate` runs the delegate immediately and `CallOrRegister_OnAddNativeTagsDelegate` runs it at the end of the current module load (`GameplayTagsManager.h:419-427`), so there is no ordering hazard in calling them late.

## Ini and Data Table Tag Sources

`UGameplayTagsSettings` is `UCLASS(config=GameplayTags, defaultconfig)` deriving from `UGameplayTagsList`, so Project Settings → Gameplay Tags writes `Config/DefaultGameplayTags.ini`:

```ini
[/Script/GameplayTags.GameplayTagsSettings]
ImportTagsFromConfig=True
FastReplication=False
NumBitsForContainerSize=6
NetIndexFirstBitSegment=16
+GameplayTagList=(Tag="MyGame.State.Stunned",DevComment="Character cannot act")
+GameplayTagList=(Tag="MyGame.Damage.Fire",DevComment="Fire damage channel")
+GameplayTagTableList=/Game/Data/DT_MyGameTags.DT_MyGameTags
+GameplayTagRedirects=(OldTagName="MyGame.State.Stun",NewTagName="MyGame.State.Stunned")
```

| Key | Type | Meaning |
|---|---|---|
| `ImportTagsFromConfig` | `bool` | Master switch for ini-defined tags; read back through `UGameplayTagsManager::ShouldImportTagsFromINI()` |
| `GameplayTagList` | `TArray<FGameplayTagTableRow>` | `Tag` (`FName`) plus `DevComment` (`FString`) |
| `GameplayTagTableList` | `TArray<FSoftObjectPath>` | Data tables of `FGameplayTagTableRow`, loaded by `LoadGameplayTagTables` |
| `GameplayTagRedirects` | `TArray<FGameplayTagRedirect>` | `OldTagName` → `NewTagName`; inherited from `UGameplayTagsList` |
| `CategoryRemapping` | `TArray<FGameplayTagCategoryRemap>` | Remaps an engine `Categories` filter onto project categories |
| `RestrictedConfigFiles` | `TArray<FRestrictedConfigInfo>` | Top-level tags only a named owner may edit |
| `InvalidTagCharacters` | `FString` | Characters rejected in tag names, beyond newline and friends |

Extra ini sources live in `Config/Tags/` (added automatically) and in any directory passed to `UGameplayTagsManager::Get().AddTagIniSearchPath(RootDir)`; `RemoveTagIniSearchPath` takes them away again. A Game Feature plugin's config directory is registered this way, which is why its tags appear only while the plugin is active.

**Renaming a tag requires a redirect.** `FGameplayTagRedirect` is `{ OldTagName, NewTagName }`; `FGameplayTagRedirectors::Get().RedirectTag(OldName, OutTag)` is what serialization uses (engine-internal: the class is not exported). Without a redirect, every asset that referenced the old name silently loads an invalid tag.

Full ini and data-table details are in [gameplay-tag-reference.md](references/gameplay-tag-reference.md).

## Matching Semantics

`FGameplayTag` is one `FName`. A container keeps the explicitly added tags plus a transient expanded parent list, so parent-aware checks are array lookups, not string parsing.

| Call | Receiver | Semantics | `{"A.1"}` vs `A` |
|---|---|---|---|
| `MatchesTag(TagToCheck)` | `FGameplayTag` | This tag or any parent equals `TagToCheck` | `A.1.MatchesTag(A)` → true; `A.MatchesTag(A.1)` → false |
| `MatchesTagExact(TagToCheck)` | `FGameplayTag` | Names equal | `A.1.MatchesTagExact(A)` → false |
| `MatchesAny(ContainerToCheck)` | `FGameplayTag` | Parent-expanded match against any tag in the container | `A.1.MatchesAny({A,B})` → true |
| `MatchesAnyExact(ContainerToCheck)` | `FGameplayTag` | Container explicitly holds this tag | `A.1.MatchesAnyExact({A,B})` → false |
| `HasTag(TagToCheck)` | `FGameplayTagContainer` | Explicit or parent list contains it | `{A.1}.HasTag(A)` → true |
| `HasTagExact(TagToCheck)` | `FGameplayTagContainer` | Explicit list only | `{A.1}.HasTagExact(A)` → false |
| `HasAny` / `HasAnyExact` | `FGameplayTagContainer` | At least one; **false for an empty argument** | `{A.1}.HasAny({A,B})` → true |
| `HasAll` / `HasAllExact` | `FGameplayTagContainer` | All; **true for an empty argument** | `{A.1,B.1}.HasAll({A,B})` → true |
| `Filter(OtherContainer)` | `FGameplayTagContainer` | New container of tags matching any tag in `OtherContainer`, parents expanded | `{A.1,C}.Filter({A})` → `{A.1}` |
| `FilterExact(OtherContainer)` | `FGameplayTagContainer` | True intersection, exact names | `{A.1,C}.FilterExact({A})` → `{}` |

The empty-argument asymmetry is deliberate: "any of nothing" is false, "all of nothing" is true. Gates written as `RequiredTags.IsEmpty() || Owned.HasAll(RequiredTags)` are redundant.

```cpp
FGameplayTagContainer MakeStateTags(const FGameplayTagContainer& ExtraTags)
{
    FGameplayTagContainer Owned;
    Owned.AddTag(TAG_MyGame_State_Stunned);    // checks uniqueness and refills parents
    Owned.AddTagFast(TAG_MyGame_Damage_Fire);  // no uniqueness check — only when the tag is known to be new
    Owned.AppendTags(ExtraTags);
    Owned.RemoveTag(TAG_MyGame_State_Stunned);

    if (!Owned.IsEmpty())
    {
        UE_LOG(LogMyGame, Log, TEXT("%d tags, first %s, last %s: %s"),
            Owned.Num(), *Owned.First().ToString(), *Owned.Last().ToString(), *Owned.ToStringSimple());
    }

    return Owned;
}
```

Parent navigation: `FGameplayTag::RequestDirectParent()` returns `x` for `x.y`, `FGameplayTag::GetGameplayTagParents()` returns a container holding the tag plus every parent, and `FGameplayTagContainer::GetGameplayTagParents()` does the same for a whole container. `ParseParentTags(TArray<FGameplayTag>&)` does it without touching the manager.

`AddTagFast` skips the `Contains` check but still fills parents; use it when building a container from data you already know is unique, never in place of `AddTag` on user input.

## Tag Queries

`FGameplayTagQuery` is a compiled token stream — cheap to evaluate, expensive to build. Build it once, store it, evaluate it many times.

```cpp
// MyBurnRule.cpp
#include "GameplayTagContainer.h"
#include "MyGameplayTags.h"

bool ShouldBurn(const FGameplayTagContainer& OwnedTags)
{
    FGameplayTagContainer Elements;
    Elements.AddTag(TAG_MyGame_Damage_Fire);

    // (any element tag) AND NOT Stunned
    FGameplayTagQuery ComplexQuery = FGameplayTagQuery::BuildQuery(
        FGameplayTagQueryExpression()
            .AllExprMatch()
            .AddExpr(FGameplayTagQueryExpression().AnyTagsMatch().AddTags(Elements))
            .AddExpr(FGameplayTagQueryExpression().NoTagsMatch().AddTag(TAG_MyGame_State_Stunned)));

    return ComplexQuery.Matches(OwnedTags);
}
```

The shortcut form covers the common cases without an expression tree:

```cpp
FGameplayTagContainer Blocking;
Blocking.AddTag(TAG_MyGame_State_Stunned);
const FGameplayTagQuery BlockedQuery = FGameplayTagQuery::MakeQuery_MatchAnyTags(Blocking);
```

Shortcuts on `FGameplayTagQuery`: `MakeQuery_MatchAnyTags`, `MakeQuery_MatchAllTags`, `MakeQuery_MatchNoTags`, `MakeQuery_ExactMatchAnyTags`, `MakeQuery_ExactMatchAllTags`, `MakeQuery_MatchTag`. Expression verbs on `FGameplayTagQueryExpression`: `AnyTagsMatch`, `AllTagsMatch`, `NoTagsMatch`, `AnyTagsExactMatch`, `AllTagsExactMatch`, `AnyExprMatch`, `AllExprMatch`, `NoExprMatch`, fed by `AddTag`, `AddTags` and `AddExpr`.

Evaluate from either side — `Query.Matches(Container)` or `Container.MatchesQuery(Query)`. Both call the same evaluator.

Expose a query as a `UPROPERTY` and designers get the query editor with no extra work:

```cpp
UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Gating")
FGameplayTagQuery ActivationQuery;
```

`ReplaceTagsFast(Tags)` and `ReplaceTagFast(Tag)` swap the tag dictionary of a cached query without rebuilding the token stream; the new container must be the same size.

## Tag-Driven Design

Anything that owns tags should expose them through `IGameplayTagAssetInterface` so unrelated systems can ask without casting:

```cpp
// MyTaggedActor.h
#pragma once

#include "GameFramework/Actor.h"
#include "GameplayTagAssetInterface.h"
#include "GameplayTagContainer.h"
#include "MyTaggedActor.generated.h"

UCLASS()
class MYGAME_API AMyTaggedActor : public AActor, public IGameplayTagAssetInterface
{
    GENERATED_BODY()

public:
    virtual void GetOwnedGameplayTags(FGameplayTagContainer& TagContainer) const override;

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Tags", meta = (Categories = "MyGame.State"))
    FGameplayTagContainer OwnedTags;
};
```

```cpp
// MyTaggedActor.cpp
#include "MyTaggedActor.h"

void AMyTaggedActor::GetOwnedGameplayTags(FGameplayTagContainer& TagContainer) const
{
    TagContainer.AppendTags(OwnedTags);
}
```

`HasMatchingGameplayTag`, `HasAllMatchingGameplayTags` and `HasAnyMatchingGameplayTags` come from the interface for free — they call your `GetOwnedGameplayTags`. From Blueprint the equivalents are `UBlueprintGameplayTagLibrary::DoesTagAssetInterfaceHaveTag`, `HasAnyMatchingGameplayTags` and `GetOwnedGameplayTags`.

**Counted tags:** an `FGameplayTagContainer` is a set, so two sources granting `Stunned` and one removing it leaves nothing. When several sources can grant the same tag, use `FGameplayTagCountContainer` (`GameplayEffectTypes.h:1102`, in the `GameplayAbilities` plugin; it is what an ASC uses for owned tags). `UpdateTagCount(Tag, +1/-1, EGameplayTagReplicationState::None)` adjusts the count (the single-tag overload has no default for the third argument; `UpdateTagCount(Container, Delta)` takes two), `GetTagCount(Tag)` includes child tags (A.B and A.C added make `GetTagCount(A) == 2`), `GetExplicitTagCount` does not, `GetExplicitGameplayTags()` returns the current set for `GetOwnedGameplayTags`, and `RegisterGameplayTagEvent(Tag, EGameplayTagEventType::NewOrRemoved | AnyCountChange)` returns an `FOnGameplayEffectTagCountChanged` (`void(const FGameplayTag, int32 NewCount)`) to bind. With GAS in the project, use the ASC's loose tags instead of owning one.

Design rules that hold up:

- **Tags name states and categories, not objects.** `MyGame.State.Stunned` and `MyGame.Damage.Fire` are good; `MyGame.Actor.Goblin03` is a class reference wearing a tag.
- **Depth is the query.** Keep the hierarchy shallow enough that `HasTag(MyGame.Damage)` is a meaningful question.
- **Author the gate, not the branch.** Expose `FGameplayTagContainer` or `FGameplayTagQuery` properties and let data decide, instead of `if (Tag == SpecificTag)` chains.
- **Never store a tag as `FName` or `FString` on a gameplay type.** Store `FGameplayTag`; it validates, redirects and replicates.

## Replication and Performance

An `FGameplayTag` is a single `FName` — copy it freely, pass it by value. Cost lives in registration and in serialization.

| Concern | Rule |
|---|---|
| Lookup | `RequestGameplayTag` walks a map every call. Resolve once into a native tag or a member, never per tick or per hit |
| Container build-up | `AddTag` refills the parent array each call; `AddTagFast` skips the uniqueness check; `FGameplayTagContainer::CreateFromArray` builds parents once for a whole array |
| Wire format | `FGameplayTag::NetSerialize` and `FGameplayTagContainer::NetSerialize` are registered via `TStructOpsTypeTraits` — a replicated tag property already uses them |
| `FastReplication=True` | Replicates tags by net index instead of name. Client and server dictionaries must be identical, so it breaks if a plugin adds tags on only one side |
| `bDynamicReplication=True` | Per-connection index assignment; slightly more expensive than `FastReplication` but tolerates differing dictionaries. Ignored when `FastReplication` is on |
| `NetIndexFirstBitSegment` | Bits in the first index segment; tags listed in `CommonlyReplicatedTags` get the low indices and fit in one segment |
| `NumBitsForContainerSize` | Bits used for a replicated container's element count — size it to your real containers |

`UGameplayTagsManager::Get().DoneAddingNativeTags()` flushes native registration; after it, adding more tags is unsafe with fast replication because the net index table has already been built and hashed (`GetNetworkGameplayTagNodeIndexHash`).

For the wire cost of the properties that carry these containers, and for push-model replication, see `ue-networking-replication`.

## Decoupled Messaging

Pick the lightest mechanism that fits:

| Need | Use |
|---|---|
| A few known listeners inside one game | A dynamic multicast delegate on a `UGameInstanceSubsystem` or `UWorldSubsystem` |
| Tag-addressed, hierarchical, cross-thread, typed payloads | `AsyncMessageSystem` plugin (Experimental in 5.8) |
| Ability activation and GAS-side events | `SendGameplayEventToActor` / `RegisterGameplayTagEvent`, owned by `ue-gameplay-abilities` |

A dynamic multicast delegate on a subsystem is often enough, and it costs nothing extra:

```cpp
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FMyScoreChanged, AActor*, Scorer, int32, NewScore);

UPROPERTY(BlueprintAssignable, Category = "Score")
FMyScoreChanged OnScoreChanged;
```

Reach for `AsyncMessageSystem` when listeners must be addressed by tag hierarchy or must run off the game thread. Enable the plugin in the `.uproject` and add `"AsyncMessageSystem"` to `PublicDependencyModuleNames`; it already depends on `GameplayTags`. The recipe, verbatim signatures, binding options and endpoints are in [gameplay-messaging.md](references/gameplay-messaging.md).

```cpp
// MyScorePayload.h
#pragma once

#include "StructUtils/InstancedStruct.h"
#include "MyScorePayload.generated.h"

USTRUCT()
struct FMyScorePayload
{
    GENERATED_BODY()

    UPROPERTY()
    int32 NewScore = 0;
};
```

```cpp
// MyScoreComponent.cpp — queue side
#include "AsyncMessageWorldSubsystem.h"
#include "AsyncMessageSystemBase.h"
#include "MyGameplayTags.h"
#include "MyScorePayload.h"

void UMyScoreComponent::BroadcastScore(int32 NewScore)
{
    TSharedPtr<FAsyncMessageSystemBase> Sys = UAsyncMessageWorldSubsystem::GetSharedMessageSystem(GetWorld());
    if (!Sys.IsValid())
    {
        return;
    }

    FMyScorePayload Payload;
    Payload.NewScore = NewScore;
    Sys->QueueMessageForBroadcast(FAsyncMessageId(TAG_MyGame_Message_ScoreChanged.GetTag()),
        FInstancedStruct::Make<FMyScorePayload>(Payload));
}
```

**Not in the engine:** `UGameplayMessageSubsystem` and its `GameplayMessageRouter` are Lyra sample code, copied into the Lyra project, not shipped in `Engine/`. Do not `#include "GameFramework/GameplayMessageSubsystem.h"` — it does not resolve. Port the Lyra files into your own module, or use `AsyncMessageSystem`.

## Editor UX and Filtering

`meta = (Categories = "…")` restricts a tag picker to one subtree. The metadata keys are `Categories` and `GameplayTagFilter`, declared in `namespace GameplayTagsManager` in `ObjectMacros.h`:

```cpp
UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Damage", meta = (Categories = "MyGame.Damage"))
FGameplayTag DamageType;

UFUNCTION(BlueprintCallable, Category = "Damage")
void ApplyElement(UPARAM(meta = (GameplayTagFilter = "MyGame.Damage")) FGameplayTag Element);
```

`UGameplayTagsManager::GetCategoriesMetaFromField` reads `Categories` first and falls back to `GameplayTagFilter`; `GetCategoriesMetaFromFunction(Func, ParamName)` is what resolves the filter for a Blueprint pin. Both accept a comma-separated list of roots.

`FGameplayTagCategoryRemap` (`BaseCategory` → `RemapCategories`) in `UGameplayTagsSettings` redirects an engine-side filter such as a Mover or GAS `Categories` value onto your own subtree, so engine properties show your tags. `UGameplayTagsDeveloperSettings` (`config=EditorPerProjectUserSettings`) holds the per-user `FavoriteTagSource` and `DeveloperConfigName` used when adding a new tag from the picker. `IGameplayTagsModule::OnGameplayTagTreeChanged` and `OnTagSettingsChanged` let editor tooling refresh when the dictionary changes.

## Deprecated — do not use

| Do not emit | Use in 5.8 | Source |
|---|---|---|
| `UGameplayTagsManager::OnLastChanceToAddNativeTags()` | `CallOrRegister_OnAddNativeTagsDelegate`, or `AddNativeGameplayTag` directly | `UE_DEPRECATED(5.8)` in `GameplayTagsManager.h:415` |
| `CallOrRegister_OnDoneAddingNativeTags` | `CallOrRegister_OnDoneAddingNativeTagsDelegate` | Name never existed; `GameplayTagsManager.h:429` |
| `UGameplayTagsManager::GetSingleTagContainer(Tag)` | `FindTagNode(Tag)` or `FGameplayTag::GetSingleTagContainer()` | `UE_DEPRECATED(5.4)` in `GameplayTagsManager.h:472` |
| `FGameplayTagContainer::AddParentsForTag` | `ParseParentTags` or `UGameplayTagsManager::ExtractParentTags` | `UE_DEPRECATED(5.4)` in `GameplayTagContainer.h:615` |
| `UGameplayTagsManager::ShouldClearInvalidTags()` | Nothing — invalid tags are never cleared | `UE_DEPRECATED(5.5)` in `GameplayTagsManager.h:594` |
| `ClearInvalidTags` ini key | Remove it | `UE_DEPRECATED(5.5)` in `GameplayTagsSettings.h:115` |
| `+GameplayTagRedirects` under `[/Script/Engine.Engine]` | Same key under `[/Script/GameplayTags.GameplayTagsSettings]` | "deprecated location" error, `GameplayTagRedirectors.cpp:26-56` |
| `EGameplayTagMatchType::Explicit` / `IncludeParentTags` | The `Exact` suffix on each call (`HasTagExact`, `MatchesTagExact`) | Enum does not exist in 5.8 |
| `Container.HasTag(Tag, MatchTypeA, MatchTypeB)` | `HasTag(Tag)` or `HasTagExact(Tag)` | One-argument forms only, `GameplayTagContainer.h:299,316` |
| `Container.MatchesAll(Other)` | `HasAll(Other)` / `HasAllExact(Other)` | No such member; `GameplayTagContainer.h:379,402` |
| `Container.Matches(Query)` | `Container.MatchesQuery(Query)` or `Query.Matches(Container)` | `GameplayTagContainer.h:464,803` |
| `MakeQuery_MatchAnyTagsExact` | `MakeQuery_ExactMatchAnyTags` | `GameplayTagContainer.h:857` |
| `DEFINE_GAMEPLAY_TAG` / `DECLARE_GAMEPLAY_TAG_EXTERN` (no `UE_`) | `UE_DEFINE_GAMEPLAY_TAG` / `UE_DECLARE_GAMEPLAY_TAG_EXTERN` | `NativeGameplayTags.h:31,41` |
| `IGameplayTagsModule::Get().GetGameplayTagsManager()` | `UGameplayTagsManager::Get()` | Module exposes only the two change delegates, `GameplayTagsModule.h:47-50` |
| `UGameplayMessageSubsystem` (Lyra sample, not engine) | A subsystem delegate, or `AsyncMessageSystem` | Not present anywhere under `Engine/Source` or `Engine/Plugins` |

## Common Mistakes

**Requesting a tag before the manager has it:** `RequestGameplayTag(FName("MyGame.X"))` during static init or early module startup ensures and returns an empty tag. Use a native tag variable, or defer the lookup into `CallOrRegister_OnDoneAddingNativeTagsDelegate`.

**Two definitions of the same native tag:** `UE_DEFINE_GAMEPLAY_TAG` in a header, or the same variable defined in two `.cpp` files, is a duplicate-symbol link error. Declare once with `UE_DECLARE_GAMEPLAY_TAG_EXTERN` in the header, define once in a `.cpp`. Use `UE_DEFINE_GAMEPLAY_TAG_STATIC` when the tag is file-local.

**`MatchesTag` where exactness was meant:** `Owned.HasTag(TAG_MyGame_Damage_Fire)` is true for a container holding `MyGame.Damage.Fire.Napalm`, and `DamageType.MatchesTag(FireTag)` is true for any fire subtype. When you need the leaf and only the leaf, use `HasTagExact` / `MatchesTagExact`.

**Hard-coded tag strings in gameplay code:** `RequestGameplayTag(FName("MyGame.State.Stunned"))` sprinkled through a class survives a rename with no compile error and no redirect. One native tag, referenced everywhere.

**Module dependency:** `Engine.Build.cs` lists `"GameplayTags"` as a *public* dependency, so any module that depends on `Engine` already compiles and links tag code without it. Add `"GameplayTags"` explicitly anyway (public if tag types appear in your public headers, private otherwise) so the dependency survives if `Engine` is ever dropped and IWYU tools see it. Modules that do not depend on `Engine` (rare) do need it.

**Renaming an ini tag without a redirect:** every asset referencing the old name loads an invalid tag and `WarnOnInvalidTags` at most logs it. Add `+GameplayTagRedirects=(OldTagName="Old",NewTagName="New")` in the same commit as the rename.

**Calling `AddNativeGameplayTag` late with `FastReplication=True`:** the net index table is already built, so client and server disagree. Register during module startup, or use `bDynamicReplication` instead.

**Building an `FGameplayTagQuery` per frame:** `BuildQuery` emits a token stream. Build it in the constructor or `BeginPlay`, store it, and call `Matches` in the hot path.

**Expecting a Lyra message router:** `#include "GameFramework/GameplayMessageSubsystem.h"` does not resolve in a clean project — that subsystem ships with the Lyra sample, not the engine. Use a subsystem delegate or the `AsyncMessageSystem` plugin.

## Related Skills

- `ue-gameplay-abilities` — GAS-side tag usage: ability activation gates, granted tags, `RegisterGameplayTagEvent` and gameplay events
- `ue-state-trees` — State Tree conditions and tasks that evaluate tag containers and queries
- `ue-game-features` — plugin-scoped tag ini sources and the activation lifecycle that registers them
- `ue-ai-navigation` — Smart Object and behaviour tag filtering
- `ue-cpp-foundations` — `UPROPERTY`/`UFUNCTION` specifiers, delegates, subsystems that host messaging
- `ue-networking-replication` — replicating tag properties, push model, RPC cost
- `ue-data-assets-tables` — `UDataTable` assets used as a tag source and for tag-keyed data
