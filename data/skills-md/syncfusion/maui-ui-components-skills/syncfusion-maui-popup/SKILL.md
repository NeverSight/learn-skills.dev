---
name: syncfusion-maui-popup
description: Implements Syncfusion® .NET MAUI Popup (SfPopup) control for displaying alert messages, custom views, and modal dialogs. Use when working with popups, overlays, dialogs, modal windows, alert boxes, or confirmation dialogs in .NET MAUI applications. Covers positioning (center, absolute, relative to view), layout customization (header, footer, content templates), animations, and modal behavior.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Implementing .NET MAUI Popups

A comprehensive skill for implementing the Syncfusion .NET MAUI Popup (SfPopup) control to display alert messages, custom views, and modal dialogs with extensive positioning and customization options.

## When to Use This Skill

Use this skill when you need to:
- Display alert messages, confirmations, or notifications in .NET MAUI apps
- Show modal dialogs that require user interaction
- Create popups with custom headers, footers, and content
- Position popups at specific locations (center, absolute, relative to views)
- Display information overlays without navigating to new pages
- Implement tooltips, contextual menus, or flyout content
- Show loading indicators or progress dialogs
- Create full-screen modal experiences
- Display custom views (ListView, DataGrid, forms) in popups
- Handle accept/decline user actions with button callbacks

## Component Overview

**Syncfusion .NET MAUI Popup (SfPopup)** is a versatile layout control that displays customizable popups with:
- **Flexible Positioning**: Center, absolute coordinates, relative to any view, or full-screen
- **Customizable Layout**: Header, body, and footer with template support and custom styling.
- **Appearance Modes**: One-button or two-button footer layouts
- **Modal Support**: Prevent background interaction until popup is dismissed
- **Animations**: Built-in zoom, fade, and slide animations
- **Auto-sizing**: Automatically adjust to content dimensions
- **MVVM Support**: Full data binding and command support

> **Notice:** After Volume 3 2025 (Mid Sep 2025), feature enhancements for this control will no longer be available in the Syncfusion package. Please switch to the **Syncfusion Toolkit for .NET MAUI** for continued support.

## Documentation and Navigation Guide

### Getting Started and Installation
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation (`Syncfusion.Maui.Popup`)
- Handler registration in `MauiProgram.cs`
- Basic popup initialization (XAML and C#)
- Displaying and dismissing popups
- First popup implementation
- Native embedding (Android/iOS)

### Positioning Options
📄 **Read:** [references/positioning.md](references/positioning.md)
- Center positioning with `IsOpen` or `Show()`
- Absolute positioning at x, y coordinates
- Relative positioning to any view
- Absolute relative positioning with offsets
- Full-screen mode
- MVVM positioning patterns
- Auto-close with duration
- Position over action bar
- Returning results with `ShowAsync()`

### Layout Customizations
📄 **Read:** [references/layout-customization.md](references/layout-customization.md)
- Appearance modes (OneButton, TwoButton)
- Show/hide header, footer, close button
- Custom header templates
- Custom footer templates
- Custom content templates
- Header and footer height
- Button text customization
- Message property
- Disable overlay background

### Sizing and Animations
📄 **Read:** [references/sizing-and-animations.md](references/sizing-and-animations.md)
- Width and height configuration
- Auto-sizing modes (Height, Width, Both, None)
- Full-screen popup mode
- Animation types (Zoom, Fade, SlideOnLeft, SlideOnRight, SlideOnTop, SlideOnBottom)
- Animation duration and easing
- Custom animation effects

### Events and Modal Behavior
📄 **Read:** [references/events-and-modal.md](references/events-and-modal.md)
- Popup lifecycle events (Opening, Opened, Closing, Closed)
- Event arguments and cancellation
- Modal mode configuration
- Overlay interaction settings
- Close on overlay tap behavior
- Accept and decline button events

### Styling and Appearance

📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)

**When to read:** Customizing visual appearance of popup with styling header, footer, messages. Overlay and stroke customizations.

**Covers:**
- Header styling
- Footer styling
- Message/content styling
- Border customization
- Overlay background styling
- Blur effects
- Background styling
- Shadow effects
- Styling examples

---

### Advanced Integration and Examples
📄 **Read:** [references/advanced-integration.md](references/advanced-integration.md)
- Displaying ListView in popup
- DataGrid cell tap integration
- Switch control binding examples
- MVVM patterns with commands
- Localization support
- Liquid glass effect styling
- Migration from older versions
- Best practices and patterns

