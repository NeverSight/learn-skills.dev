---
name: avalonia
description: Use when working with Avalonia UI framework — building, styling, binding, animating, or deploying Avalonia apps with .NET.
---

# Avalonia UI

## Overview
Avalonia is a cross-platform .NET UI framework using XAML (`.axaml`), with its own Skia-based rendering engine, supporting Windows, macOS, Linux, iOS, Android, and WASM.

**Supported versions:** 11.3 (legacy), 12.0, **12.1 (current stable, 12.1.4)**. Default for new projects: latest 12.1.x on `net10.0`.

**Rule 1 — version first:** Before writing or reviewing code, detect the project's Avalonia version (`Avalonia` `PackageReference` in `*.csproj` / `Directory.Packages.props`). Many APIs differ between 11.x and 12.x (clipboard, drag-drop, Android lifetime, `Watermark`, window decorations, compiled-binding default). Load `avalonia-versions` when unsure whether a feature exists in that version, or when migrating/upgrading.

**Rule 2:** Always load the matching subskill before writing or reviewing Avalonia code. Subskills mark version-specific content as **(12.0+)**, **(12.1+)** or **(11.x)**; unlabelled content works in all supported versions.

**Rule 3 — documentation lookup:** Prefer available MCP documentation tools before browsing: use an Avalonia-specific documentation provider first, then a general library-documentation provider such as Context7. Identify suitable tools by their descriptions and capabilities, not a fixed server alias. Follow the official documentation links when suitable MCP tools are unavailable or their results are incomplete, unrelated, or do not establish the target version. Verify version-specific behavior against matching documentation, tagged source, and the project's Avalonia packages. MCP providers are optional; keep the official links as sources and fallback.

**Bundled references:** Resolve each route relative to this skill's directory: `avalonia-xaml` means `avalonia-xaml/SKILL.md`, and `avalonia-pro-max/motion` means `avalonia-pro-max/motion/SKILL.md`. Read the matching file even when the host exposes only the `avalonia` entrypoint. Resolve that file's supporting links and scripts relative to its own directory.

## Routing Table

| Task | Load subskill |
|---|---|
| Which version? Feature availability, 11→12 migration, 12.0→12.1 upgrade | `avalonia-versions` |
| XAML markup, .axaml files, namespaces, code-behind | `avalonia-xaml` |
| Panels, Grid, StackPanel, alignment, margins | `avalonia-layout` |
| Styles, control themes, selectors, pseudoclasses, themes | `avalonia-styling` |
| `{Binding}`, compiled bindings, converters, validation | `avalonia-data-binding` |
| DataTemplate, ItemTemplate, template selection | `avalonia-data-templates` |
| MVVM pattern, INotifyPropertyChanged, ICommand, CommunityToolkit | `avalonia-mvvm` |
| Built-in controls (Button, TextBox, GroupBox, TableView, DataGrid, pages, etc.) | `avalonia-controls` |
| Custom UserControl, TemplatedControl, drawing controls | `avalonia-custom-controls` |
| Brushes, transforms, animations, transitions | `avalonia-graphics-animation` |
| Pointer, keyboard, gestures, drag-and-drop | `avalonia-input-interaction` |
| StyledProperty, DirectProperty, AttachedProperty | `avalonia-property-system` |
| Routed events, bubbling, tunneling | `avalonia-events` |
| Clipboard, file dialogs, notifications, storage | `avalonia-services` |
| App structure, resource dictionaries, app lifetime | `avalonia-app-development` |
| Headless testing, UI automation | `avalonia-testing` |
| Packaging for macOS/Windows/Linux/WASM | `avalonia-deployment` |
| Migrating from WPF | `avalonia-wpf-migration` |
| UI thread, `Dispatcher`, async/await, background work, timers | `avalonia-threading` |
| Android/iOS app concerns: lifetimes, safe areas, soft keyboard, back button, haptics | `avalonia-mobile` |
| Composition API, direct Skia/OpenGL, `NativeControlHost`, embedding Avalonia in WinForms/WPF/WinUI | `avalonia-interop-rendering` |
| Slow UI, profiling, DevTools, virtualization, startup time, trimming, NativeAOT | `avalonia-performance` |
| **Designing/polishing UI for visual quality, picking themes, building a design system, motion, accessibility, layout patterns, icons, pre-ship review** | `avalonia-pro-max` |

## Notable Community Packages

A curated short-list of the most commonly needed community packages:

| Need | Package |
|---|---|
| Message box dialogs | `MsgBox.Avalonia` |
| Hot reload during dev | `HotAvalonia` |
| SVG images | `Svg.Skia` |
| Animated GIFs | `AvaloniaGif` |
| Charts | `LiveChartsCore.SkiaSharpView.Avalonia` or `ScottPlot.Avalonia` |
| Code editor control | `AvaloniaEdit` |
| Docking layout | `Dock.Avalonia` |
| Behaviors (DataTrigger replacement) | `Avalonia.Xaml.Behaviors` |
| Node editor | `NodifyAvalonia` (GitHub: BAndysc) |
| Material theme | `Material.Avalonia` |
| Fluent/WinUI controls | `FluentAvalonia` |
| Rich dialog service | `HanumanInstitute.MvvmDialogs.Avalonia` |
| VLC media player | `LibVLCSharp.Avalonia` |
| PDF viewer | `MuPDFCore` |
| Deployment packaging | PupNet Deploy (GitHub: kuiperzone/PupNet-Deploy) |

Full community list: https://github.com/AvaloniaCommunity/awesome-avalonia
