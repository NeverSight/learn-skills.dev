---
name: syncfusion-maui-slider
description: Implements Syncfusion .NET MAUI Slider (SfSlider) control. Use when working with sliders, numeric value selection, or interactive value controls. This skill covers installation, track configuration, labels with formatting, ticks and dividers, tooltips, thumb customization, discrete selection with StepSize, deferred updates, and LiquidGlass effect.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Implementing .NET MAUI Slider

The Syncfusion .NET MAUI Slider (SfSlider) is a highly interactive UI control that enables users to select a single value from a defined range. It offers a rich set of customization features, including track styling, labels, ticks, dividers, and tooltips, allowing developers to create intuitive and visually engaging slider experiences.

## When to Use This Skill

Use this skill when the user needs to:

- Implement a numeric slider control in .NET MAUI applications
- Allow users to select a single value from a range (e.g., volume, brightness, price)
- Configure slider track, thumb, labels, ticks, dividers, or tooltips
- Handle slider value changes through events or commands
- Create discrete sliders with step values
- Customize slider appearance with colors, sizes, and styles
- Enable advanced features like deferred updates or liquid glass effects
- Migrate from Xamarin.Forms RangeSlider to .NET MAUI Slider
- Implement sliders in both horizontal and vertical orientations

The Syncfusion .NET MAUI Slider (SfSlider) is a highly interactive UI control for selecting a single numeric value from a range, with rich features including customizable track, labels, ticks, dividers, tooltips, and responsive interactions.

## Component Overview

The **SfSlider** is the numeric slider control for .NET MAUI that allows users to select a single value by dragging a thumb along a track. It provides:

- **Numeric Support**: Select values from numeric ranges with configurable minimum and maximum
- **Visual Elements**: Track, thumb, overlay, labels, ticks, dividers, and tooltips
- **Orientation**: Both horizontal and vertical layout support
- **Interaction**: Smooth dragging with events and commands for value changes
- **Discrete Mode**: Step-based value selection for specific increments
- **Customization**: Extensive styling options for all visual components
- **Advanced Features**: Deferred updates, liquid glass effect, and Visual State Manager support

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installing Syncfusion.Maui.Sliders NuGet package
- Registering handler with ConfigureSyncfusionCore
- Creating basic slider in XAML and C#
- Setup for Visual Studio, VS Code, and JetBrains Rider
- Orientation (horizontal/vertical)
- IsInversed property for reversed sliders

### Track and Value Configuration
📄 **Read:** [references/track-and-values.md](references/track-and-values.md)
- Minimum and Maximum properties
- Value property and data binding
- Track customization with TrackStyle
- ActiveFill and InactiveFill colors
- ActiveSize and InactiveSize for track thickness
- Track height and custom styling

### Labels and Formatting
📄 **Read:** [references/labels-and-formatting.md](references/labels-and-formatting.md)
- ShowLabels property to display labels
- Interval configuration (manual and auto)
- NumberFormat for label formatting (prefix/suffix)
- LabelCreated event for custom label text
- SliderLabelCreatedEventArgs (Text, Style properties)
- Label styling (color, font, family, offset)

### Ticks and Dividers
📄 **Read:** [references/ticks-and-dividers.md](references/ticks-and-dividers.md)
- ShowTicks property for major ticks
- MinorTicksPerInterval for minor ticks
- Tick size, length, and styling
- ShowDividers property for track markers
- Divider radius, fill, and stroke customization
- ActiveRadius, InactiveRadius, ActiveFill, InactiveFill
- ActiveStroke, InactiveStroke, ActiveStrokeThickness, InactiveStrokeThickness
- Visual State Manager for disabled dividers

### Tooltip
📄 **Read:** [references/tooltip.md](references/tooltip.md)
- Enabling tooltip with SliderTooltip
- ShowAlways property for persistent tooltips
- Tooltip.NumberFormat for value formatting
- TooltipLabelCreated event for custom tooltip text
- SliderTooltipLabelCreatedEventArgs (Text, TextColor, FontSize, FontFamily, FontAttributes)
- Tooltip positioning and styling

### Thumb, Selection, and Overlay
📄 **Read:** [references/thumb-selection-overlay.md](references/thumb-selection-overlay.md)
- Thumb customization with ThumbStyle
- Thumb Radius, Fill, Stroke, and StrokeThickness
- ThumbOverlay properties with ThumbOverlayStyle
- Overlay radius and color configuration
- Selection track styling
- Visual State Manager for disabled thumb states
- Complete styling examples

### Events, Commands, and Interaction
📄 **Read:** [references/events-and-commands.md](references/events-and-commands.md)
- ValueChangeStart event (thumb press)
- ValueChanging event with SliderValueChangingEventArgs (during drag)
- ValueChanged event with SliderValueChangedEventArgs (drag complete)
- ValueChangeEnd event (thumb release)
- DragStartedCommand and DragStartedCommandParameter
- DragCompletedCommand and DragCompletedCommandParameter
- Command binding with ViewModel and ICommand
- Event handler patterns

### Advanced Features and Migration
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- StepSize for discrete value selection
- EnableDeferredUpdate and DeferredUpdateDelay
- IsEnabled property for disabled state
- EnableLiquidGlassEffect (modern translucent design for .NET 10+)
- LiquidGlass prerequisites (iOS 26, macOS 26)
- Visual State Manager (VSM) for state-based styling
- Custom theming and styling patterns
- Migration from Xamarin.Forms SfRangeSlider
- Property mapping (Xamarin → MAUI)

