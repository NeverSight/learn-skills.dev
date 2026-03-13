---
name: ue-testing-debugging
description: Use when writing automation tests, functional tests, or any test in Unreal Engine. Also use when the user asks about "UE_LOG", logging, log categories, assertion, check, ensure, verify, DrawDebug, debug draw, console command, profiling, Unreal Insights, stat commands, or debugging techniques. See ue-module-build-system for test module setup, and ue-cpp-foundations for general C++ logging patterns.
metadata:
  version: 1.0.0
---

# UE Testing & Debugging

You are an expert in testing, debugging, and profiling Unreal Engine C++ projects.

## Context

Read `.agents/ue-project-context.md` for engine version, existing log categories, test infrastructure (automation modules, test maps), and project-specific conventions before providing guidance.

## Before You Start

Ask which area the user needs help with if unclear:
- **Automation tests** — unit/integration tests using IMPLEMENT_SIMPLE_AUTOMATION_TEST
- **Functional tests** — actor-based AFunctionalTest in maps
- **Logging** — UE_LOG, custom categories, verbosity filtering
- **Assertions** — check, ensure, verify and when to use each
- **Debug drawing** — DrawDebug helpers for runtime visualization
- **Console commands** — UFUNCTION(Exec), FAutoConsoleCommand, CVars
- **Profiling** — Unreal Insights, stat commands, SCOPE_CYCLE_COUNTER

---
## Automation Framework

Automation tests live in a dedicated module (e.g., `MyGameTests`) that depends on `"AutomationController"`. Include the module in the editor target via `ExtraModuleNames` and conditionally in the game target via `if (bWithAutomationTests)`.

### Simple Tests

```cpp
// Source/MyGameTests/Private/MyFeature.spec.cpp
#include "Misc/AutomationTest.h"
// Must specify one application context flag AND exactly one filter flag
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FMyInventoryTest, "MyGame.Inventory.AddItem",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FMyInventoryTest::RunTest(const FString& Parameters)
{
    UInventoryComponent* Inv = NewObject<UInventoryComponent>();
    Inv->AddItem(FName("Sword"), 1);
    TestEqual(TEXT("Item count after add"), Inv->GetItemCount(FName("Sword")), 1);
    TestTrue(TEXT("Has sword"), Inv->HasItem(FName("Sword")));
    TestFalse(TEXT("No axe"),   Inv->HasItem(FName("Axe")));
    TestNotNull(TEXT("Inv valid"), Inv);
    return true;
}
```

### Complex / Parameterized Tests

`IMPLEMENT_COMPLEX_AUTOMATION_TEST` requires overriding `GetTests()` to populate the parameter list, and `RunTest(Parameters)` receives each entry in turn.

```cpp
IMPLEMENT_COMPLEX_AUTOMATION_TEST(FMyAssetLoadTest, "MyGame.Assets.LoadByPath",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

void FMyAssetLoadTest::GetTests(TArray<FString>& OutBeautifiedNames,
                                 TArray<FString>& OutTestCommands) const
{
    OutBeautifiedNames.Add(TEXT("Sword"));  OutTestCommands.Add(TEXT("/Game/Items/BP_Sword"));
    OutBeautifiedNames.Add(TEXT("Shield")); OutTestCommands.Add(TEXT("/Game/Items/BP_Shield"));
}

bool FMyAssetLoadTest::RunTest(const FString& Parameters)
{
    UObject* Asset = StaticLoadObject(UObject::StaticClass(), nullptr, *Parameters);
    if (!TestNotNull(TEXT("Asset loaded"), Asset)) { return false; }
    TestTrue(TEXT("Is DataAsset"), Asset->IsA<UPrimaryDataAsset>());
    return true;
}
```

### Test Assertion Methods

```cpp
// Equality — overloaded for int32, int64, float, double, FVector, FRotator,
//            FTransform, FColor, FLinearColor, FString, FStringView, FText, FName
TestEqual(TEXT("Label"), Actual, Expected);
TestEqual(TEXT("Float approx"), ActualF, ExpectedF, 0.001f);   // tolerance overload

// Boolean
TestTrue(TEXT("Label"), bCondition);
TestFalse(TEXT("Label"), bCondition);

// Pointer / validity
TestNotNull(TEXT("Label"), Ptr);          // fails if Ptr == nullptr
TestNull(TEXT("Label"), Ptr);             // fails if Ptr != nullptr
TestValid(TEXT("Label"), WeakPtr);        // IsValid() check on TWeakObjectPtr etc.

// Custom failure messages
AddError(FString::Printf(TEXT("Unexpected damage %d"), Damage));
AddWarning(TEXT("Deprecated path hit"));

// Add error and bail — returns false from RunTest if condition fails
UE_RETURN_ON_ERROR(Ptr != nullptr, TEXT("Ptr must not be null"));
```

### Test Flags Reference

| Flag | Meaning |
|---|---|
| `EditorContext` | Runs in the editor process |
| `ClientContext` | Runs in game client |
| `ServerContext` | Runs on dedicated server |
| `SmokeFilter` | Fast; runs on every CI check-in |
| `ProductFilter` | Project/game-level tests |

---
## Latent Commands (Async Testing)

Use latent commands when the test must wait for an async operation. `Update()` returns `true` when done, `false` to retry next frame.

```cpp
DEFINE_LATENT_AUTOMATION_COMMAND_ONE_PARAMETER(FWaitSecondsCommand, float, Duration);
bool FWaitSecondsCommand::Update() { return GetCurrentRunTime() >= Duration; }

// Enqueue inside RunTest; commands drain sequentially after RunTest returns
ADD_LATENT_AUTOMATION_COMMAND(FWaitSecondsCommand(2.0f));
```

See `references/automation-test-patterns.md` for delegate-wait, timeout, and post-async assertion patterns.

---
## Functional Tests

`AFunctionalTest` is a `UCLASS` actor placed in a test map. Override `StartTest()` and call `FinishTest()` when done.

```cpp
// MyFunctionalTest.h
UCLASS()
class MYGAMETESTS_API AMyFunctionalTest : public AFunctionalTest
{
    GENERATED_BODY()
public:
    virtual void StartTest() override;
private:
    UFUNCTION() void OnTimerExpired();
    FTimerHandle TimerHandle;
};

// MyFunctionalTest.cpp
void AMyFunctionalTest::StartTest()
{
    Super::StartTest();
    GetWorldTimerManager().SetTimer(TimerHandle, this,
        &AMyFunctionalTest::OnTimerExpired, 1.0f, false);
}

void AMyFunctionalTest::OnTimerExpired()
{
    bool bPassed = /* verify world state */ true;
    FinishTest(bPassed ? EFunctionalTestResult::Succeeded
                       : EFunctionalTestResult::Failed,
               TEXT("Timer-based check"));
}
```

Place actors in `Maps/Test_MyFeature.umap`. Run via `RunAutomationTest "MyGame.Functional.MyFeature"` or the Session Frontend.

### TimeLimit

```cpp
// Timeout — auto-fail if test exceeds time limit
void AMyFunctionalTest::PrepareTest()
{
    Super::PrepareTest();
    TimeLimit = 10.0f;  // seconds; 0 = no timeout (default)
}
```

---
## Logging

### Declaring and Defining a Category

```cpp
// MyModule.h  — visible across the module
DECLARE_LOG_CATEGORY_EXTERN(LogMyModule, Log, All);
//                           ^Name       ^Default  ^CompileTime max

// MyModule.cpp
DEFINE_LOG_CATEGORY(LogMyModule);

// Single-file static category (no extern needed)
DEFINE_LOG_CATEGORY_STATIC(LogMyHelper, Warning, All);
```

### UE_LOG Usage

```cpp
// UE_LOG(CategoryName, Verbosity, Format, ...)
UE_LOG(LogMyModule, Log,        TEXT("Player spawned: %s"), *PlayerName);
UE_LOG(LogMyModule, Warning,    TEXT("Inventory full, dropping item %s"), *ItemName);
UE_LOG(LogMyModule, Error,      TEXT("Failed to load asset at %s"), *AssetPath);
UE_LOG(LogMyModule, Verbose,    TEXT("Tick called, dt=%.4f"), DeltaTime);
UE_LOG(LogMyModule, Fatal,      TEXT("Unrecoverable save corruption")); // crashes

// Conditional log — condition evaluated only if category/verbosity is active
UE_CLOG(Health <= 0.f, LogMyModule, Warning, TEXT("Actor %s has zero health"), *GetName());
```

### Verbosity Levels (highest to lowest severity)

| Level | When to use |
|---|---|
| `Fatal` | Crash-worthy unrecoverable errors |
| `Error` | Operation failed, needs developer attention |
| `Warning` | Unexpected but recoverable condition |
| `Display` | User-visible output (always shown) |
| `Log` | Standard development info |
| `Verbose` | Detailed per-frame or per-call info |
| `VeryVerbose` | Trace-level; very high frequency |

### Structured Logging (UE 5.2+)

```cpp
#include "Logging/StructuredLog.h"
// Named fields — order does not matter; extra fields beyond the format string are allowed
UE_LOGFMT(LogMyModule, Warning,
    "Loading '{Name}' failed with error {Error}",
    ("Name", AssetName), ("Error", ErrorCode), ("Flags", LoadFlags));
```

### Runtime Log Filtering

```
# Command line: set a category to Verbose at startup
-LogCmds="LogMyModule Verbose, LogAI Warning"

# Console at runtime
Log LogMyModule Verbose
Log LogAI Warning
Log reset          # restore defaults
```

---
## Assertions

Assertions are defined in `Misc/AssertionMacros.h`. Understand the build-configuration behaviour before choosing one.

### check / checkf

```cpp
// Active in Debug, Development, Test. REMOVED in Shipping (expression not evaluated).
check(Ptr != nullptr);
checkf(Index >= 0 && Index < Array.Num(),
       TEXT("Index %d out of range [0,%d)"), Index, Array.Num());

// Debug-only (DO_GUARD_SLOW — only Debug builds)
checkSlow(ExpensiveValidationFn());

// Marks unreachable code paths
checkNoEntry();

// Marks code that must only execute once
checkNoReentry();
```

### ensure / ensureMsgf

```cpp
// Non-fatal. Logs callstack and submits crash report. Execution continues.
// Fires only ONCE per call site per session (subsequent failures are silent).
if (ensure(Component != nullptr))
{
    Component->DoWork();  // safe to call here
}

// With a message
ensureMsgf(Health > 0.f, TEXT("Actor %s has non-positive health %.1f"),
           *GetName(), Health);

// Always fires (not just once per session)
ensureAlways(bInitialized);
ensureAlwaysMsgf(bInitialized, TEXT("System not initialized before use"));
```

### verify / verifyf

```cpp
// Expression ALWAYS evaluated (even in Shipping), but only halts in non-Shipping.
// Use when expression has side effects you always need.
verify(Manager->Init());
verifyf(Count++ < MaxCount, TEXT("Exceeded max count %d"), MaxCount);
```

### Decision Guide

| Situation | Macro |
|---|---|
| Class invariant, programmer error | `check` / `checkf` |
| Recoverable condition, want to continue | `ensure` / `ensureMsgf` |
| Expression has side effects always needed | `verify` / `verifyf` |
| Debug-build heavy validation | `checkSlow` |
| User-facing input validation | **none** — use explicit if/return |

---
## Debug Drawing

Debug draw functions from `DrawDebugHelpers.h` render geometry directly in the world viewport during PIE or standalone builds. They are stripped by `#if ENABLE_DRAW_DEBUG` in Shipping.

```cpp
#include "DrawDebugHelpers.h"

// Duration > 0 = seconds visible; bPersistentLines = true for permanent.
// Duration 0 or -1 both show for one frame.
UWorld* World = GetWorld();
DrawDebugLine(World, StartLoc, EndLoc, FColor::Red, false, 2.0f, 0, 2.0f);
DrawDebugSphere(World, Center, Radius, 12, FColor::Green, false, 2.0f);
DrawDebugBox(World, Center, Extent, FColor::Blue, false, 2.0f);
DrawDebugCapsule(World, Center, HalfHeight, Radius,
                 FQuat::Identity, FColor::Yellow, false, 2.0f);
DrawDebugPoint(World, Location, 8.0f, FColor::White, false, 2.0f);
DrawDebugDirectionalArrow(World, Start, End, 40.0f, FColor::Cyan, false, 2.0f);
DrawDebugString(World, Location, TEXT("Label"), nullptr,
                FColor::White, 2.0f, true);

// Clear all persistent debug geometry
FlushPersistentDebugLines(World);

// Guard persistent draws for shipping: #if ENABLE_DRAW_DEBUG ... #endif
// UKismetSystemLibrary::DrawDebugSphere (and siblings) auto-gate behind ENABLE_DRAW_DEBUG
```

---
## Console Commands

### Exec Functions

```cpp
// AMyPlayerController.h
UFUNCTION(Exec)
void ToggleGodMode();

// AMyPlayerController.cpp
void AMyPlayerController::ToggleGodMode()
{
    bGodMode = !bGodMode;
    UE_LOG(LogMyModule, Display, TEXT("GodMode: %s"), bGodMode ? TEXT("ON") : TEXT("OFF"));
}
```

Exec functions work when typed in the console (~) if on a `PlayerController`, `Pawn`, `HUD`, `GameMode`, `GameState`, `CheatManager`, or `GameInstance`.

### FAutoConsoleCommand and CVars

```cpp
// Registers at static init; no world context needed
static FAutoConsoleCommand GDumpStatsCmd(
    TEXT("MyGame.DumpStats"), TEXT("Dump gameplay stats"),
    FConsoleCommandDelegate::CreateLambda([]()
    {
        UE_LOG(LogMyModule, Display, TEXT("=== GameStats ==="));
    }));

// With world + args (PIE-safe; prefer this for gameplay commands)
static FAutoConsoleCommandWithWorldAndArgs GSpawnItemCmd(
    TEXT("MyGame.SpawnItem"), TEXT("Usage: MyGame.SpawnItem <Name>"),
    FConsoleCommandWithWorldAndArgsDelegate::CreateLambda(
        [](const TArray<FString>& Args, UWorld* World) { /* spawn */ }));

// CVar — declare in .cpp to avoid ODR issues
static TAutoConsoleVariable<float> CVarDamageScale(
    TEXT("MyGame.DamageScale"), 1.0f,
    TEXT("Scales all outgoing damage."), ECVF_Cheat);
float Scale = CVarDamageScale.GetValueOnGameThread();

// Attach CVar to an existing variable
float GDrawDistance = 5000.0f;
static FAutoConsoleVariableRef CVarDrawDistance(
    TEXT("MyGame.DrawDistance"), GDrawDistance,
    TEXT("Draw distance for gameplay objects"), ECVF_Default);
```

### Runtime Command Registration

```cpp
// Runtime registration — call from StartupModule, Initialize, or BeginPlay
IConsoleCommand* Cmd = IConsoleManager::Get().RegisterConsoleCommand(
    TEXT("MyGame.ReloadConfig"),
    TEXT("Reloads runtime config"),
    FConsoleCommandDelegate::CreateUObject(this, &UMySubsystem::ReloadConfig));
// Unregister when the owning object is destroyed:
IConsoleManager::Get().UnregisterConsoleObject(Cmd);
```

Unlike `FAutoConsoleCommand` (static init registration), `RegisterConsoleCommand` registers at runtime and returns a handle for explicit cleanup.

---
## Custom Stat Groups & Profiling Markers

```cpp
// Declare in a .cpp — feeds stat commands and Unreal Insights
DECLARE_STATS_GROUP(TEXT("MyGame"), STATGROUP_MyGame, STATCAT_Advanced);
DECLARE_CYCLE_STAT(TEXT("MySystem Tick"), STAT_MySystemTick, STATGROUP_MyGame);
DECLARE_CYCLE_STAT(TEXT("PathFind"),      STAT_PathFind,     STATGROUP_MyGame);

void UMySystem::Tick(float DeltaTime) { SCOPE_CYCLE_COUNTER(STAT_MySystemTick); }
FPath UMySystem::FindPath(...)        { SCOPE_CYCLE_COUNTER(STAT_PathFind); }

// Named events — colored blocks in Insights, no stat overhead
#include "HAL/PlatformMisc.h"
void UMySystem::HeavyOperation() { SCOPED_NAMED_EVENT(MyHeavyOp, FColor::Orange); }

// CSV profiling — lightweight always-on telemetry written to Saved/Profiling/CSVStats/
#include "ProfilingDebugging/CsvProfiler.h"
CSV_DEFINE_CATEGORY(MyGame, true);
void UMySystem::Tick(float DeltaTime) { CSV_SCOPED_TIMING_STAT(MyGame, SystemTick); }
```

---
## Debugging Techniques

### Visual Logger

```cpp
#include "VisualLogger/VisualLogger.h"
// Window > Visual Logger shows a timeline of shapes and log events per actor
UE_VLOG_SPHERE(this, LogMyModule, Verbose, GetActorLocation(), 50.0f, FColor::Green, TEXT("Patrol point"));
UE_VLOG_SEGMENT(this, LogMyModule, Log, From, To, FColor::Red, TEXT("Path"));
UE_VLOG(this, LogMyModule, Log, TEXT("State: %s"), *StateName);
```

### Gameplay Debugger

Press `'` (apostrophe) in PIE to open the Gameplay Debugger. It shows AI, EQS, Ability System, and custom categories. Register a custom category in module startup:

```cpp
IGameplayDebugger::Get().RegisterCategory("MySystem",
    IGameplayDebugger::FOnGetCategory::CreateStatic(&FMyDebugCategory::MakeInstance),
    EGameplayDebuggerCategoryState::EnabledInGame);
```

### IDE Breakpoint Debugging

Attach Visual Studio or Rider to the running `UnrealEditor` process (Debug > Attach to Process). Use `DebugGame` or `Debug` configuration for full symbol resolution -- `Development` strips many symbols.

```cpp
// Break on assertion failures -- set breakpoints on these functions:
// FDebug::AssertFailed       (check/checkf)
// FDebug::EnsureFailed       (ensure/ensureMsgf)
// FDebug::OptionallyLogFormattedEnsureMessageReturningFalse

// Conditional breakpoint example (VS/Rider):
// Condition: Actor->GetName().Contains(TEXT("Enemy"))
// Hit count: break on 5th hit
```

For `check()` and `ensure()` failures, set breakpoints on the handler functions above -- they fire before crash/log, letting you inspect the call stack.

### Crash Analysis

- Minidumps land in `Saved/Crashes/`. Open with `UnrealEditor-Win64-DebugGame` PDB in WinDbg or Rider.
- `FDebug::DumpStackTraceToLog(ELogVerbosity::Error)` prints the current callstack to the log.
- `ensure` submits a callstack to the Crash Reporter without crashing the process.

**Network**: `-NetTrace` for replication capture, `stat net` for live bandwidth, `net.ListActorChannels` for actor channels.

**Key profiling commands**: `stat startfile`/`stat stopfile` (.uestats capture for Insights), `stat gpu`/`ProfileGPU` (GPU timing), `stat memoryplatform`/`memreport -full` (memory), `-trace=cpu,gpu,frame,memory` (Insights launch args). See `references/profiling-commands.md`.

---

## Common Mistakes

**check() in shipping** — `check()` expressions are compiled out of Shipping builds. Never put required logic inside a check expression; use `verify()` if the expression must always evaluate.

**ensure fires only once** — After the first ensure failure at a call site, subsequent calls at that site are silent. Use `ensureAlways` if you need every failure reported.

**DrawDebug in shipping** — DrawDebug calls do not exist in Shipping without `ENABLE_DRAW_DEBUG`. Wrap persistent draws with `#if ENABLE_DRAW_DEBUG`.

**Missing log category** — Defining `UE_LOG` with a category not visible in the current translation unit causes a linker error. Include the header that declares the category.

**Automation test without a filter flag** — Every `IMPLEMENT_SIMPLE_AUTOMATION_TEST` must have exactly one filter flag (Smoke, Engine, Product, Perf, Stress, or Negative). Missing it is a compile-time `static_assert` failure.

**Latent command after `return true`** — Latent commands are enqueued before the function returns. Do not enqueue them after the `return true;` statement.

**Log spam in multiplayer** — Identical log calls fire from both server and each client. Prefix messages with `GetWorld()->GetNetMode()` or use `UE_CLOG(HasAuthority(), ...)` to reduce noise.

---

## Related Skills

- `ue-cpp-foundations` — UE macro system, delegates, FString, UE_LOG basics
- `ue-module-build-system` — setting up a dedicated test module and target inclusion
- `ue-actor-component-architecture` — AFunctionalTest placement and world interaction

---
## References

- `references/automation-test-patterns.md` — test setup patterns, latent commands, common scenarios
- `references/profiling-commands.md` — stat commands, Insights capture, analysis workflow
