---
name: nightmareui
description: "Build settings pages and debug FFXIV Dalamud plugins using NightmareUI or NightmareUI.OtterGuiWrapper. Use when a plugin already depends on either library or the user asks to add one. Compose NuiBuilder sections and Nui controls, manage button tabs and NightmareUIState, add WorldSelector world pickers or Censor name masking, persist and navigate configuration trees with ConfigFileSystem, GenericFileSystem, and FileSystemSelector, or repair ECommons/OtterGui submodule integration. Covers NuiTools.ButtonTabs and wrapper-specific APIs. These internal-use libraries may break between pins."
license: "MIT; bundled upstream files retain their own licenses, listed in references/NOTICE.md."
---

# NightmareUI and NightmareUI.OtterGuiWrapper

The bundle pins NightmareUI `aae510d` and NightmareUI.OtterGuiWrapper `371b1f9`, both still the head of upstream `main` on 2026-11-13. Their consumers use ECommons and stock Dalamud bindings; the tree-selector wrapper also depends on the Limiana OtterGui fork. Upstream's internal-use notice describes API stability, so match the consumer's pinned revision.

## Workflow

1. Inspect the plugin project and submodules. Determine whether it needs basic NightmareUI widgets or the optional OtterGui wrapper.
2. Check the sibling submodule directories at the solution root against the project references, which use relative paths. Read the matching guide in the task table before changing setup or UI code.
3. Locate a type in `references/all-public-members.txt` or `references/all-internal-members.txt`, then inspect its bundled source under `references/NightmareUI/` or `references/NightmareUI.OtterGuiWrapper/`.
4. Initialize ECommons before constructing or drawing dependent UI. Preserve each helper's documented state and callback timing.
5. Build the solution. On missing-project or type errors, check the directory layout, recursive submodule initialization, ECommons package/project selection, and SDK compatibility; fix the relevant mismatch and rebuild.
6. In an available client, verify the settings page or selector renders, persists the intended config, and survives reload. Test tab state and filtering when those paths changed. Inspect `/xllog` for draw exceptions and state separately when runtime verification was unavailable.

## Minimal settings page

Initialize ECommons once with `ECommonsMain.Init(pluginInterface, this)` (`using ECommons;`), retaining any existing module arguments. NightmareUI has no global `Init`. Reuse the plugin's window system and draw subscription so the override has an active ImGui window; stop its UI callbacks before the owning plugin calls `ECommonsMain.Dispose()`.

This window edits a mutable field and saves only when the checkbox changes:

```csharp
using System;
using Dalamud.Interface.Windowing;
using NightmareUI.PrimaryUI;

public sealed class NightmareSettingsWindow : Window
{
    private bool enabled;
    private readonly Action<bool> save;
    private readonly NuiBuilder settings;

    public NightmareSettingsWindow(bool initialEnabled, Action<bool> save)
        : base("Settings###NightmareSettings")
    {
        enabled = initialEnabled;
        this.save = save;
        settings = new NuiBuilder()
            .Section("Settings")
            .Checkbox("Enabled", () => ref enabled);
    }

    public override void Draw()
    {
        var previous = enabled;
        settings.Draw();
        if (enabled != previous)
            save(enabled);
    }
}
```

Pass the persisted flag and a callback that updates the plugin's configuration and calls `pluginInterface.SavePluginConfig(config)`, where `config` implements `IPluginConfiguration`. The builder's ref callback requires a mutable field; an auto-property cannot replace `enabled`. Retain this window instance between frames.

At the consumer checkout root, initialize declared dependencies:

```sh
git submodule update --init --recursive
```

Then run this from the directory containing the consumer plugin's `.csproj` (not a library submodule):

```sh
dotnet build -c Debug
```

Inspect failures using workflow step 5 before retrying.

## Common tasks

| Task | Read |
|---|---|
| Fluent settings page, NuiBuilder callbacks | [NuiBuilder](references/guide-2-nightmareui-public-surface.md#2-nightmareui-public-surface) and [worked examples](references/guide-4-worked-examples.md#4-worked-examples) |
| Nui controls and rendering behavior | [Public surface](references/guide-2-nightmareui-public-surface.md#2-nightmareui-public-surface) |
| Tab bar, state, world picker, censor | [Public surface](references/guide-2-nightmareui-public-surface.md#2-nightmareui-public-surface), then the corresponding source file |
| ConfigFileSystem or selector subclass | [OtterGui wrapper](references/topic-otterguiwrapper.md) |
| Missing projects or conflicting dependencies | [Setup](references/guide-1-adding-it-to-a-plugin.md#1-adding-it-to-a-plugin) and [pitfalls](references/guide-5-pitfalls.md#5-pitfalls) |

A similarly named ECommons or stock ImGui helper is not a drop-in replacement without checking its signature and behavior. The wrapper simplifies OtterGui's full filesystem API; use its own topic before copying an upstream selector example.

[The technical guide](references/guide.md) includes consumer evidence. Examples have source verification only. [NOTICE.md](references/NOTICE.md) records credits, licenses, and the wrapper's inherited-code provenance question.
