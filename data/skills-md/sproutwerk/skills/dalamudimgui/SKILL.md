---
name: dalamudimgui
description: "Build FFXIV Dalamud plugin windows, migrate ImGuiNET code, manage drawing lifetimes, and debug ImGui interfaces. Use with Dalamud.Bindings.ImGui, API 13+ migration, ImU8String overloads, WindowSystem, Window, ImRaii scopes, fonts, textures, tables and clipping, SeString rendering, notifications, drag-drop, file dialogs, ImPlot, or ImGuizmo. Covers the stock Dalamud UI layer; Luna and ImSharp use a separate API."
license: "MIT; bundled upstream files retain their own licenses, listed in references/NOTICE.md."
compatibility: "Pinned reference: Dalamud 43b3411 (2026-11-10, released as 15.0.4.0), API 15, .NET 10, C# 14, Dear ImGui 1.88 docking. Match the target SDK and binding generation before copying signatures."
---

# Dalamud ImGui

Match the plugin's SDK and bindings to the [bundled revision record](references/guide.md) before copying signatures. Stock `Dalamud.Bindings.ImGui` and legacy `ImGuiNET` examples can have incompatible overloads and types; use the [migration reference](references/topic-migration.md) when porting code. Some helpers and one scope fix are newer than Dalamud 15.0.3.5; [changes since 15.0.3.5](references/guide.md#changes-since-dalamud-15035) lists them for plugins that target an older runtime.

## Workflow

1. Identify the plugin's SDK/API level and UI library. Check existing imports before choosing stock Dalamud, OtterGui, ECommons helpers, or ImSharp.
2. Read the matching topic below and verify overloads in `references/src/`. The [bindings reference](references/topic-bindings.md) explains signature lookup, UTF-8 arguments, and pointer overloads.
3. Draw through the plugin's `IUiBuilder.Draw` callback or existing `WindowSystem`. Match event subscription with teardown, and keep ImGui calls inside an active draw context.
4. Balance scope lifetimes. Use the correct `ImRaii` implementation for the imported namespace; its conditions and disposal behavior can differ from similarly named libraries.
5. Build against the target SDK. For an overload error, check UTF-8/string handling, `ref` versus pointer arguments, enum names, and `ImTextureID` before adding casts.
6. In an available client, reload and test the window open/close path, UI scale, repeated draws, and unload. Inspect `/xllog` for stack imbalance or disposed-resource errors. Correct the failing lifetime or overload and repeat the affected check. Report when in-game verification was unavailable.

## A draw callback

For an existing plugin, merge this callback into its UI lifecycle. Subscribe `pi.UiBuilder.Draw += Draw` during initialization and unsubscribe `pi.UiBuilder.Draw -= Draw` during disposal, where `pi` is the injected `IDalamudPluginInterface`.

```csharp
using Dalamud.Bindings.ImGui;

private bool isOpen = true;

private void Draw()
{
    if (!isOpen)
        return;

    var visible = ImGui.Begin("Example###ExamplePluginMain"u8, ref isOpen);
    try
    {
        if (visible)
            ImGui.TextUnformatted("Ready"u8);
    }
    finally
    {
        ImGui.End();
    }
}
```

`End()` is required even when `Begin()` returns false. For a plugin using `WindowSystem`, put the controls in `Window.Draw()` and let the system own `Begin`/`End`; see the [window example](references/guide-windowsystem-and-window.md). Build with `dotnet build` from the plugin project, then perform the reload and teardown checks above.

## Drawing constraints

- Keep allocations, file access, and network requests out of per-frame drawing. Cache derived data and load textures through the documented provider.
- Preserve texture and font ownership rules. A borrowed wrapper or atlas-managed handle must not be disposed as if the plugin owned it.
- Use scaled dimensions with `ImGuiHelpers.GlobalScale` where the API expects them; avoid scaling a value twice.
- Give repeated controls distinct IDs. Large collections need clipping or the table helpers rather than drawing every row.
- Dispose windows, font handles, owned texture wrappers, and subscribed callbacks according to their documented lifetime.

## Task routing

| Task | Read |
|---|---|
| ImGuiNET migration, bindings, UTF-8, enums | [Migration](references/topic-migration.md), [bindings](references/topic-bindings.md) |
| Window setup, events, scopes | [Windows](references/topic-windows.md), [ImRaii](references/topic-imraii.md) |
| Scaling, buttons, helper widgets | [Helpers and components](references/topic-helpers-components.md) |
| Fonts or FontAwesome | [Fonts](references/topic-fonts.md) |
| Game icons, image loading, ownership | [Textures](references/topic-textures.md) |
| Tables and list clipping | [Tables](references/topic-tables.md) |
| Rich text | [SeString](references/topic-sestring.md) |
| Notifications, dialogs, drag-drop | [Notifications](references/topic-notifications.md), [file dialog](references/topic-file-dialog.md), [drag-drop](references/topic-drag-drop.md) |
| Style, colors, plots, gizmos | [Colors and style](references/topic-colors-style.md), [ImPlot and ImGuizmo](references/topic-implot-imguizmo.md) |

For additional examples, read [drawing events](references/guide-iuibuilder-hooking-up-drawing.md), [scope usage](references/guide-imraii.md), or [binding pitfalls](references/guide-pitfalls.md). [The technical guide](references/guide.md) indexes the remaining examples. [NOTICE.md](references/NOTICE.md) identifies the licenses of Dalamud, its bindings, and copied documentation. Source-derived examples are not evidence of a successful in-game test.
