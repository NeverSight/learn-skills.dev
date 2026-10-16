---
name: syncfusion-maui-range-selector
description: Implements the Syncfusion .NET MAUI Range Selector (SfRangeSelector) component. Use when working with range selection with embedded charts, numeric range input, RangeStart/RangeEnd, track customization, or thumb styling in .NET MAUI. Covers tooltip configuration, label formatting, ticks/dividers, selection modes, events, and embedding SfCartesianChart inside a range control.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Implementing .NET MAUI Range Selector

The Syncfusion `SfRangeSelector` is a .NET MAUI control that lets users select a numeric range by dragging thumbs over a track. It uniquely supports embedding any content (typically a chart) inside the selector, making it ideal for filtering chart data by range.

## When to Use This Skill

Use this skill when the user needs to:

- **Set up SfRangeSelector** from scratch in a MAUI app
- **Embed chart content** (`SfCartesianChart` or other views) inside the range selector for interactive data filtering
- **Customize track appearance** — colors, height, and extent
- **Configure intervals, ticks, labels, and dividers** for the range scale
- **Style thumb and overlay** — size, colors, stroke
- **Configure tooltips** — show always, styling, custom text
- **Implement selection modes** — discrete, interval selection, drag behaviors
- **Handle events** — ValueChanged, ValueChanging, LabelCreated
- **Use MVVM commands** — DragStartedCommand, DragCompletedCommand
- **Customize labels** — placement, edge placement, styling, offset
- **Style ticks and dividers** — colors, sizes, strokes
- **Add visual regions** — active/inactive region colors and strokes
- **Invert range selector direction** with IsInversed
- **Format displayed labels** with prefix/suffix via `NumberFormat`
- **Enable Liquid Glass effect** for modern translucent design
- **Bind RangeStart/RangeEnd to a ViewModel** for MVVM data binding

## Component Overview

The **SfRangeSelector** is a .NET MAUI control for selecting a numeric range by dragging dual thumbs over a track. It uniquely supports embedding any content (typically a chart) inside the selector, making it ideal for interactive data filtering.

**Package**: `Syncfusion.Maui.Sliders`  
**Namespace**: `Syncfusion.Maui.Sliders`  
**Control**: `SfRangeSelector`

**Key Capabilities:**
- **Embedded Content**: Any .NET MAUI view (e.g., `SfCartesianChart`) rendered inside the selector
- **Dual Thumbs**: Drag to define start and end values with full track styling
- **Interval Controls**: Labels, ticks, minor ticks, and dividers at configurable intervals
- **Selection Modes**: Discrete steps, interval snapping, and drag behavior options
- **Rich Customization**: Track colors, thumb styles, tooltip, label/tick/divider styling
- **Region Support**: Active/inactive region customization
- **MVVM Ready**: Events, commands, and two-way data binding support
- **Liquid Glass Effect**: Modern translucent design for iOS/macOS 26+

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet installation (`Syncfusion.Maui.Sliders`)
- Handler registration in `MauiProgram.cs`
- Minimal XAML and C# setup
- Adding chart content via the `Content` property
- Namespace imports

### Interval Configuration
📄 **Read:** [references/interval-configuration.md](references/interval-configuration.md)
- Setting `Interval`, `Minimum`, `Maximum`
- Auto-interval calculation when `Interval = 0`
- Showing ticks with `ShowTicks` + `MinorTicksPerInterval`
- Showing dividers with `ShowDividers`
- How interval affects labels and ticks rendering

### Display Features
📄 **Read:** [references/display-features.md](references/display-features.md)
- Enabling labels with `ShowLabels`
- Enabling ticks and minor ticks
- Formatting labels with `NumberFormat` (prefix/suffix)
- Inverting the selector with `IsInversed`
- Configuring `RangeStart` and `RangeEnd`

### Content and Chart Integration
📄 **Read:** [references/content-and-integration.md](references/content-and-integration.md)
- How the `Content` property works
- Embedding `SfCartesianChart` with hidden axes
- ViewModel + `ItemsSource` binding pattern
- `SplineAreaSeries` setup inside a range selector
- Tips for using other chart types

### Track Customization
📄 **Read:** [references/track-customization.md](references/track-customization.md)
- Minimum and Maximum properties
- RangeStart and RangeEnd values
- Track colors (ActiveFill, InactiveFill)
- Track height (ActiveSize, InactiveSize)
- Track extent (extending track edges)
- TrackStyle property and complete styling

### Labels Customization
📄 **Read:** [references/labels-customization.md](references/labels-customization.md)
- ShowLabels property
- NumberFormat for prefix/suffix ($, %, etc.)
- LabelsPlacement (OnTicks vs BetweenTicks)
- EdgeLabelsPlacement (Default vs Inside)
- LabelStyle (colors, fonts, sizes for active/inactive)
- Label offset customization
- Custom label text via LabelCreated event

### Ticks and Dividers
📄 **Read:** [references/ticks-and-dividers.md](references/ticks-and-dividers.md)
- ShowTicks and major ticks configuration
- MinorTicksPerInterval for minor ticks
- MajorTickStyle (colors, sizes, offset)
- MinorTickStyle (colors, sizes, offset)
- ShowDividers property
- DividerStyle (radius, colors, stroke, stroke thickness)
- Complete tick and divider styling examples

### Selection Modes
📄 **Read:** [references/selection-modes.md](references/selection-modes.md)
- Discrete selection with StepSize
- EnableIntervalSelection property
- DragBehavior options (OnThumb, BetweenThumbs, Both)
- EnableDeferredUpdate for performance
- DeferredUpdateDelay configuration
- Selection behavior comparisons

### Tooltip Configuration
📄 **Read:** [references/tooltip-configuration.md](references/tooltip-configuration.md)
- Enabling tooltip with SliderTooltip
- ShowAlways property for persistent tooltips
- Tooltip styling (Fill, Stroke, StrokeThickness)
- Text styling (TextColor, FontSize, FontFamily, FontAttributes)
- Padding and Position properties
- NumberFormat for tooltip text
- Custom tooltip text via TooltipLabelCreated event

### Thumb and Styling
📄 **Read:** [references/thumb-and-styling.md](references/thumb-and-styling.md)
- ThumbStyle properties (Radius, Fill, Stroke, StrokeThickness)
- OverlapStroke for overlapping thumbs
- ThumbOverlayStyle (Radius, Fill)
- Visual regions (ActiveRegionFill, InactiveRegionFill, strokes)
- Complete styling patterns
- EnableLiquidGlassEffect for modern translucent design
- Platform requirements for Liquid Glass

### Events and Commands
📄 **Read:** [references/events-and-commands.md](references/events-and-commands.md)
- Value change events (ValueChangeStart, ValueChanging, ValueChanged, ValueChangeEnd)
- LabelCreated event for custom label text
- TooltipLabelCreated event for custom tooltip text
- DragStartedCommand and DragCompletedCommand
- Command parameters
- MVVM pattern implementation
- Complete event handling examples

