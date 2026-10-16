---
name: syncfusion-maui-date-time-slider
description: Implements Syncfusion .NET MAUI DateTime Slider (SfDateTimeSlider) for date range selection. Use when working with DateTime Slider, date range selection, date picker slider, or temporal value selection UI in MAUI applications. This skill covers installation, configuration, track customization, labels, ticks, dividers, tooltips, thumb styling, intervals, and discrete selection.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Implementing .NET MAUI Date Time Slider

The Syncfusion .NET MAUI DateTime Slider (SfDateTimeSlider) is a highly interactive UI control for selecting a single DateTime value from a range of date/time values. It provides rich customization options for labels, ticks, tooltips, track, thumb, and dividers, making it ideal for temporal data selection in MAUI applications.

## When to Use This Skill

Use this skill when user need to:
- **Implement date selection** with a slider interface in .NET MAUI applications
- **Create time pickers** or datetime range selectors with visual feedback
- **Build temporal UI controls** for selecting dates, times, or datetime values
- **Customize slider appearance** including track colors, thumb styling, labels, ticks, and tooltips
- **Handle datetime value changes** through events and commands in MVVM patterns
- **Enable discrete selection** with specific date/time steps (daily, monthly, yearly, hourly)
- **Support RTL and accessibility** with WCAG-compliant datetime sliders
- **Add modern glass effects** with the Liquid Glass Effect (.NET 10+)

This skill is essential when working with temporal data selection, calendar-based inputs, date range filtering, time scheduling interfaces, or any scenario requiring intuitive datetime value selection in .NET MAUI.

## Component Overview

**Key Features:**
- **DateTime Support**: Select DateTime values with flexible range configuration
- **Dual Orientation**: Horizontal and vertical slider orientations
- **Rich Labeling**: Customizable date format labels with active/inactive states
- **Ticks & Dividers**: Visual indicators for major/minor intervals
- **Interactive Tooltip**: Shows selected value during interaction
- **Discrete Mode**: Step-based selection with configurable intervals
- **Visual Customization**: Full control over colors, sizes, fonts, and styles
- **Events & Commands**: Value change tracking and MVVM command support
- **Visual State Manager**: Support for enabled/disabled states
- **Liquid Glass Effect**: Modern translucent design (.NET 10, iOS/macOS 26)

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

**When to read:** First-time implementation, installation, or basic setup.

**Topics covered:**
- Installation of Syncfusion.Maui.Sliders NuGet package
- Handler registration with ConfigureSyncfusionCore
- Basic DateTime Slider implementation (XAML and C#)
- Setting Minimum, Maximum, and Value properties
- Orientation configuration (Horizontal/Vertical)
- Inverse slider direction with IsInversed
- Platform-specific setup (Visual Studio, VS Code, JetBrains Rider)

### Track Configuration
📄 **Read:** [references/track-customization.md](references/track-customization.md)

**When to read:** Customizing track appearance, colors, or dimensions.

**Topics covered:**
- Minimum, Maximum, and Value property details
- Active and inactive track colors (ActiveFill, InactiveFill)
- Track height customization (ActiveSize, InactiveSize)
- Track extent for extending track edges
- TrackStyle class and properties
- Disabled track states with Visual State Manager

### Labels and Formatting
📄 **Read:** [references/labels.md](references/labels.md)

**When to read:** Displaying formatted date labels or customizing label appearance.

**Topics covered:**
- ShowLabels property to enable labels
- DateFormat property for custom date/time formats
- Label placement options (OnTicks, BetweenTicks)
- Edge label placement (Default, Inside)
- Label style customization (colors, fonts, sizes)
- Active and inactive label styling
- Label offset adjustment
- LabelCreated event for custom label text
- Disabled label states

### Ticks and Dividers
📄 **Read:** [references/ticks-and-dividers.md](references/ticks-and-dividers.md)

**When to read:** Adding visual interval indicators or customizing tick/divider appearance.

**Topics covered:**
- ShowTicks property for major ticks
- MinorTicksPerInterval for minor tick indicators
- Major and minor tick styling (colors, sizes)
- Tick offset configuration
- ShowDividers property for divider marks
- Divider styling (radius, colors, stroke)
- Active and inactive tick/divider customization
- Disabled states with Visual State Manager

### Thumb and Overlay Customization
📄 **Read:** [references/thumb-and-overlay.md](references/thumb-and-overlay.md)

**When to read:** Customizing the draggable thumb or its interactive overlay.

**Topics covered:**
- Thumb definition and purpose
- Thumb size with Radius property
- Thumb colors (Fill, Stroke, StrokeThickness)
- ThumbStyle class properties
- Thumb overlay definition and behavior
- Overlay size and color customization
- ThumbOverlayStyle properties
- Disabled thumb states with Visual State Manager

### Tooltip Configuration
📄 **Read:** [references/tooltip.md](references/tooltip.md)

**When to read:** Displaying tooltips during interaction or customizing tooltip appearance.

**Topics covered:**
- Enabling tooltip with SliderTooltip
- ShowAlways property for persistent tooltips
- Tooltip styling (Fill, Stroke, StrokeThickness)
- Tooltip text customization (TextColor, FontSize, FontFamily)
- Padding and Position properties
- DateFormat for tooltip date display
- TooltipLabelCreated event for custom tooltip text

### Intervals and Value Selection
📄 **Read:** [references/intervals-and-selection.md](references/intervals-and-selection.md)

**When to read:** Configuring date intervals, discrete selection, or deferred updates.

**Topics covered:**
- Interval property for label/tick/divider spacing
- IntervalType enumeration (Years, Months, Days, Hours, Minutes, Seconds)
- Auto interval calculation
- StepDuration for discrete selection mode
- EnableDeferredUpdate and DeferredUpdateDelay
- Different interval type examples with DateFormat

### Events and Commands
📄 **Read:** [references/events-and-commands.md](references/events-and-commands.md)

**When to read:** Handling value changes, implementing MVVM commands, or customizing labels/tooltips dynamically.

**Topics covered:**
- ValueChangeStart, ValueChanging, ValueChanged, ValueChangeEnd events
- Event handler implementation
- LabelCreated event for dynamic label customization
- TooltipLabelCreated event for tooltip text formatting
- DragStartedCommand and DragCompletedCommand
- Command parameters for MVVM binding
- Liquid Glass Effect (EnableLiquidGlassEffect property)

