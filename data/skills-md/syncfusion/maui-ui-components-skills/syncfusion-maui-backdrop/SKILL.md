---
name: syncfusion-maui-backdrop
description: Implements Syncfusion .NET MAUI Backdrop Page (SfBackdropPage) with back layer and front layer surfaces. Use when working with backdrop pages, SfBackdropPage, back layer, front layer, or reveal/conceal animations. Covers backdrop navigation patterns, header icons, corner shapes, reveal height, layer state events, and liquid glass effect.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Implementing Backdrop Pages (.NET MAUI)

The Syncfusion **SfBackdropPage** is a layered page with two surfaces:
- **Back Layer** — holds actionable/contextual content (navigation menus, filters)
- **Front Layer** — always visible, holds primary content; slides down to reveal the back layer

The back layer can be revealed/concealed via toolbar icon, touch/swipe, or programmatically.

## When to Use This Skill

Use this skill when the user needs to:

- **Implement menu-driven navigation** with a sliding front layer
- **Build filter or search panels** that slide in from behind primary content
- **Add reveal and conceal animations** to a layered page
- **Customize backdrop header icons**, corner shapes, or reveal height
- **Handle `BackLayerStateChanged` events** for state tracking
- **Apply the Liquid Glass Effect** to backdrop layers

## Component Overview
 
The **SfBackdropPage** control provides:
- **Two-Layer Architecture**: Back layer for contextual actions, front layer for primary content with spatial hierarchy
- **Multiple Reveal Methods**: Programmatic API, toolbar icon tap, and swipe/fling gestures
- **Adaptive Reveal Height**: Auto mode (fits content) or Fill mode (full screen expansion)
- **Customizable Front Layer**: Curved or flat edge shapes with independent corner radius control
- **Header Integration**: Seamless NavigationPage and FlyoutPage support with customizable icons and text
- **Smooth Animations**: Built-in Material Design motion for reveal/conceal transitions
- **State Tracking**: BackLayerStateChanged event with percentage-based reveal tracking
- **Modern Effects**: Liquid Glass Effect support for translucent designs (iOS/macOS 26+, .NET 10)

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation (`Syncfusion.Maui.Backdrop`)
- Handler registration in `MauiProgram.cs`
- `SfBackdropPage` initialization (XAML & C#)
- Adding `BackdropBackLayer` and `BackdropFrontLayer` content
- Programmatic, touch, and swipe reveal/conceal

### Header Configuration
📄 **Read:** [references/header-configuration.md](references/header-configuration.md)
- Wrapping in `NavigationPage` (required for header)
- Default icons in NavigationPage vs FlyoutPage
- Custom icon images (`OpenIconImageSource`, `CloseIconImageSource`)
- Custom icon text (`OpenText`, `CloseText`)

### Reveal Height & Corner Shape Customization
📄 **Read:** [references/reveal-and-corner-customization.md](references/reveal-and-corner-customization.md)
- `BackLayerRevealOption`: `Fill` vs `Auto`
- `RevealedHeight` on the front layer
- `EdgeShape`: `Curved` vs `Flat`
- `LeftCornerRadius` / `RightCornerRadius`

### Events
📄 **Read:** [references/events.md](references/events.md)
- `BackLayerStateChanged` event
- `BackLayerStateChangedEventArgs.Percentage`
- XAML and C# wiring patterns

### Liquid Glass Effect
📄 **Read:** [references/liquid-glass-effect.md](references/liquid-glass-effect.md)
- Enabling `EnableLiquidGlassEffect` on Front or Back Layer
- Transparent background setup for glass effect
- Platform requirements (iOS 26+, macOS 26+, .NET 10)

