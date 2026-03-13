---
name: ue-module-build-system
description: Use when working with Build.cs, Target.cs, module creation, plugin setup, or build errors in Unreal Engine — including "unresolved external symbol," "cannot open include file," IWYU violations, missing API macros, or dependency configuration. See also ue-cpp-foundations for UObject macro patterns.
metadata:
  version: 1.0.0
---

# UE Module & Build System

You are an expert in Unreal Engine's module and build system. You understand Unreal Build Tool (UBT), ModuleRules, TargetRules, the .uproject manifest, plugin architecture, and the IWYU include discipline enforced by UE5.

## Before Starting

Read `.agents/ue-project-context.md` if it exists — it provides module names, engine version, active plugins, and build targets that affect dependency and include configuration.

Ask which situation applies:
1. Configuring dependencies in an existing Build.cs
2. Creating a new module from scratch
3. Creating a new plugin
4. Resolving a build error (linker, include, or IWYU)
5. Setting up Target.cs for a new build target

---

## Build.cs Anatomy

Every UE module has a `ModuleName.Build.cs` file next to its `Public/` and `Private/` directories.

```csharp
// Source/MyModule/MyModule.Build.cs
using UnrealBuildTool;

public class MyModule : ModuleRules
{
    public MyModule(ReadOnlyTargetRules Target) : base(Target)
    {
        // PCH settings — use IWYU in UE5
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        // Enable strict IWYU (recommended for new modules in UE5)
        bEnforceIWYU = true;

        // Types accessible to modules that depend on MyModule
        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core",
            "CoreUObject",
            "Engine",
        });

        // Types used only internally (not re-exported in public headers)
        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "Slate",
            "SlateCore",
        });

        // Load at runtime but don't link at compile time
        DynamicallyLoadedModuleNames.Add("OnlineSubsystem");
    }
}
```

### Public vs Private Dependencies

| Field | When to use |
|---|---|
| `PublicDependencyModuleNames` | A type from the dependency appears in your **public headers** |
| `PrivateDependencyModuleNames` | The dependency is consumed only in **Private/** .cpp files |

A common mistake: putting everything in `PublicDependencyModuleNames`. This bloats transitive include paths for every downstream module. Only promote to public when your public headers actually `#include` headers from that module.

### Include Paths

```csharp
// Expose extra paths to modules that depend on you
PublicIncludePaths.Add(Path.Combine(ModuleDirectory, "Public/Interfaces"));

// Expose extra paths only to this module's own source
PrivateIncludePaths.Add(Path.Combine(ModuleDirectory, "Private/Helpers"));
```

UBT automatically adds `Public/` and `Private/` — you rarely need to set these manually unless you have nested subdirectory headers you want to import without path prefixes.

### API Export Macro

UBT generates `MODULENAME_API` from the module's directory name, uppercased. Any class, function, or variable that must be visible across DLL boundaries needs this macro:

```cpp
// Public/MyClass.h
#pragma once
#include "CoreMinimal.h"

class MYMODULE_API FMyClass
{
public:
    void DoSomething();
};

// Standalone exported function
MYMODULE_API void MyFreeFunction();
```

Missing `MYMODULE_API` on a class that another module references causes "unresolved external symbol" linker errors.

### PCH and IWYU

```csharp
// UE5 recommended — each file includes exactly what it uses
PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
bEnforceIWYU = true;

// Legacy — one monolithic PCH (avoid for new modules)
PCHUsage = PCHUsageMode.UseSharedPCHs;
```

With IWYU, every `.cpp` file includes its own `.h` first, then only what it directly uses:

```cpp
// Private/MyClass.cpp
#include "MyClass.h"       // own header first
#include "Engine/Actor.h"  // only includes this file directly uses
```

### Compiler Flags

```csharp
// C++ exceptions — disable unless third-party code requires them
bEnableExceptions = false;

// Runtime type information — disable unless using dynamic_cast
bUseRTTI = false;

// Third-party static libraries shipped with the engine
AddEngineThirdPartyPrivateStaticDependencies(Target, "zlib", "OpenSSL");
```

---

## Target.cs

Located at `Source/ProjectName.Target.cs` (and `Source/ProjectNameEditor.Target.cs`).

```csharp
// Source/MyGame.Target.cs
using UnrealBuildTool;
using System.Collections.Generic;

public class MyGameTarget : TargetRules
{
    public MyGameTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;

        // All game modules that UBT should compile
        ExtraModuleNames.AddRange(new string[] { "MyGame", "MyGameUtilities" });
    }
}

// Source/MyGameEditor.Target.cs
public class MyGameEditorTarget : TargetRules
{
    public MyGameEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.AddRange(new string[] { "MyGame", "MyGameEditor" });
    }
}
```

### Target Types

| TargetType | Use for |
|---|---|
| `Game` | Standalone game executable |
| `Editor` | Editor build (includes editor-only modules) |
| `Client` | Networked client without server logic |
| `Server` | Dedicated server (no renderer) |
| `Program` | Standalone non-game tool |

**Build configurations**: `Debug` (full symbols, no optimization), `DebugGame` (engine optimized, game debug), `Development` (default; balanced), `Test` (like shipping but with console/stats), `Shipping` (final release, strips all debug).

---

## .uproject File

```json
{
    "FileVersion": 3,
    "EngineAssociation": "5.4",
    "Category": "",
    "Description": "",
    "Modules": [
        {
            "Name": "MyGame",
            "Type": "Runtime",
            "LoadingPhase": "Default"
        },
        {
            "Name": "MyGameEditor",
            "Type": "Editor",
            "LoadingPhase": "Default"
        }
    ],
    "Plugins": [
        {
            "Name": "ModelingToolsEditorMode",
            "Enabled": true
        },
        {
            "Name": "MyPlugin",
            "Enabled": true
        }
    ]
}
```

### Module Types

| Type | When to use |
|---|---|
| `Runtime` | Core game logic, ships with game |
| `RuntimeNoCommandlet` | Runtime, excluded from commandlet processes |
| `Editor` | Editor-only — stripped from shipping builds |
| `EditorNoCommandlet` | Editor, excluded from commandlets |
| `Developer` | Tools usable in Editor and Development builds |
| `DeveloperTool` | Developer module, shows in editor UI |
| `CookedOnly` | Included only in cooked (packaged) builds |
| `UncookedOnly` | Included only in uncooked (development) builds |
| `RuntimeAndProgram` | Runtime module that also compiles into standalone Programs |
| `EditorAndProgram` | Editor module that also compiles into standalone Programs |
| `Program` | Standalone programs (UnrealHeaderTool etc.) |

### Loading Phases

| Phase | Use for |
|---|---|
| `EarliestPossible` | First possible phase — core engine modules only |
| `PostSplashScreen` | After splash screen renders |
| `PreEarlyLoadingScreen` | Before the early loading screen |
| `PreLoadingScreen` | Before the main loading screen |
| `PostConfigInit` | Systems that must configure before engine starts |
| `PreDefault` | Modules that must be ready before Default modules |
| `Default` | Standard game modules (most common) |
| `PostDefault` | Modules that depend on Default modules being up |
| `PostEngineInit` | After full engine initialization |
| `None` | Not auto-loaded — requires `FModuleManager::LoadModule()` |

---

## Creating a New Module

### Directory Structure

```
Source/
  MyModule/
    Public/
      MyModule.h          (optional module interface header)
      MyClass.h
    Private/
      MyModule.cpp        (module registration)
      MyClass.cpp
    MyModule.Build.cs
```

### Module Interface

```cpp
// Public/MyModule.h
#pragma once
#include "Modules/ModuleManager.h"

class IMyModule : public IModuleInterface
{
public:
    static IMyModule& Get()
    {
        return FModuleManager::LoadModuleChecked<IMyModule>("MyModule");
    }

    static bool IsAvailable()
    {
        return FModuleManager::Get().IsModuleLoaded("MyModule");
    }
};
```

```cpp
// Private/MyModule.cpp
#include "MyModule.h"

class FMyModule : public IMyModule
{
public:
    virtual void StartupModule() override
    {
        // Initialize subsystems, register delegates, etc.
    }

    virtual void ShutdownModule() override
    {
        // Unregister delegates, clean up
    }
};

// Use IMPLEMENT_MODULE for non-gameplay modules
IMPLEMENT_MODULE(FMyModule, MyModule)

// Use IMPLEMENT_GAME_MODULE for modules containing UObject/gameplay code
// IMPLEMENT_GAME_MODULE(FMyModule, MyModule)

// Use IMPLEMENT_PRIMARY_GAME_MODULE for the main game module
// IMPLEMENT_PRIMARY_GAME_MODULE(FMyModule, MyGame, "MyGame")
```

The `IMPLEMENT_MODULE` macro (defined in `Modules/ModuleManager.h`) registers the module's initializer function. In DLL builds it registers a static `FModuleInitializerEntry` that maps the module name to its factory function. In monolithic builds it registers a static `FStaticallyLinkedModuleRegistrant`.

`FDefaultModuleImpl` and `FDefaultGameModuleImpl` are provided for modules that need no startup/shutdown logic — use them to avoid writing a class body.

### Add to .uproject

```json
{
    "Name": "MyModule",
    "Type": "Runtime",
    "LoadingPhase": "Default"
}
```

---

## Creating a Plugin

### Directory Structure

```
Plugins/
  MyPlugin/
    MyPlugin.uplugin
    Source/
      MyPlugin/
        Public/
          IMyPlugin.h
        Private/
          MyPlugin.cpp
        MyPlugin.Build.cs
      MyPluginEditor/           (optional editor-only module)
        Public/
        Private/
          MyPluginEditor.cpp
        MyPluginEditor.Build.cs
    Content/                    (optional, for content plugins)
    Resources/
      Icon128.png
```

### .uplugin File

```json
{
    "FileVersion": 3,
    "Version": 1,
    "VersionName": "1.0",
    "FriendlyName": "My Plugin",
    "Description": "Does something useful.",
    "Category": "Gameplay",
    "CreatedBy": "MyStudio",
    "CreatedByURL": "",
    "DocsURL": "",
    "MarketplaceURL": "",
    "CanContainContent": true,
    "IsBetaVersion": false,
    "IsExperimentalVersion": false,
    "Installed": false,
    "Modules": [
        {
            "Name": "MyPlugin",
            "Type": "Runtime",
            "LoadingPhase": "Default"
        },
        {
            "Name": "MyPluginEditor",
            "Type": "Editor",
            "LoadingPhase": "Default"
        }
    ]
}
```

### Plugin with Runtime + Editor Modules

The runtime module must not include editor-only headers. Gate editor code:

```cpp
// MyPlugin.Build.cs — runtime module
public class MyPlugin : ModuleRules
{
    public MyPlugin(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine" });

        // Editor-only dependency, only when compiling an editor build
        if (Target.bBuildEditor)
        {
            PrivateDependencyModuleNames.Add("UnrealEd");
        }
    }
}
```

```cpp
// MyPluginEditor.Build.cs — editor module
public class MyPluginEditor : ModuleRules
{
    public MyPluginEditor(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "UnrealEd" });
        PrivateDependencyModuleNames.Add("MyPlugin");
    }
}
```

### Engine vs Project Plugins

**Engine plugins** (`Engine/Plugins/`): available to all projects using that engine installation. Ship with Epic or marketplace installs. **Project plugins** (`YourProject/Plugins/`): project-specific, travel with the project. When both exist with the same name, the project plugin wins.

**Content-only plugins**: No `Source/` directory, no `Modules` array in `.uplugin`. Contains only `Content/` and `Resources/`. Set `"CanContainContent": true`. Used for distributing Blueprint libraries and asset packs without C++ compilation.

**Edge case -- launcher vs source builds**: Launcher (binary) installs only include pre-built engine module binaries. Adding a dependency on an engine module not in the pre-built set causes LNK1104. Source builds from GitHub expose all engine modules. Use `Target.LinkType` to conditionally include source-build-only dependencies.

---

## Resolving Build Errors

Most build errors fall into a few categories: **LNK2019** (missing dependency or missing `MODULENAME_API`), **C1083** (missing dependency or wrong include path under IWYU), **IWYU violations** (include every header each file directly uses), and **circular dependencies** (extract a shared interface module or use `DynamicallyLoadedModuleNames`). Guard editor-only code in runtime modules with `#if WITH_EDITOR` and `if (Target.bBuildEditor)` in Build.cs. See [references/common-build-errors.md](references/common-build-errors.md) for full error message lookup, causes, and fix patterns.

---

## Common Anti-Patterns

- **Putting everything in PublicDependencyModuleNames** — inflates transitive include paths for every downstream module. Only promote to public when your public headers require it.
- **Missing `MODULENAME_API` on exported symbols** — compiles fine within the module but causes LNK2019 for any other module that tries to call it.
- **Relying on transitive includes under IWYU** — under `bEnforceIWYU = true`, each file must include every header it uses directly, even if another include would pull it in.
- **Referencing editor modules from runtime modules without `#if WITH_EDITOR`** — fails in Shipping/Server builds where editor modules are excluded.
- **Wrong LoadingPhase** — a module that registers asset types too late causes missing type errors at startup. Use `PreDefault` or `PostConfigInit` when needed.
- **Not adding the module to .uproject** — UBT will not compile a module that isn't listed in `.uproject` or a `.uplugin`.

---

## Related Skills

- **ue-cpp-foundations** — UObject macros (UCLASS, UPROPERTY, UFUNCTION), reflection, and what must be in public headers for UHT to process

For detailed Build.cs field reference, see [references/build-cs-reference.md](references/build-cs-reference.md).
For error message lookup, see [references/common-build-errors.md](references/common-build-errors.md).
