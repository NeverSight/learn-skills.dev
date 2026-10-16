---
name: syncfusion-maui-time-picker
description: Implements Syncfusion .NET MAUI TimePicker (SfTimePicker) control. Use when implementing time selection, time picker controls, or time input UI in .NET MAUI. This skill covers installation, configuration, time formats (14 predefined formats), picker modes (Dialog/RelativeDialog), intervals, time restrictions, looping, events, and customization.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Implementing Syncfusion .NET MAUI TimePicker

The Syncfusion .NET MAUI TimePicker (SfTimePicker) is a powerful control that allows users to select time values through an intuitive scrollable interface. It supports multiple time formats, customizable intervals, dialog modes, time restrictions, and extensive styling options.

## When to Use This Skill

Use this skill when you need to:
- Implement time selection in .NET MAUI applications
- Add SfTimePicker controls to XAML or C# code
- Configure time formats (12/24 hour, with/without seconds, milliseconds)
- Set up dialog or positioned picker modes
- Define hour/minute/second intervals for time selection
- Restrict selectable times (business hours, appointment slots, blocked times)
- Handle time selection events or use MVVM commands
- Customize picker appearance (header, footer, selection view, text display)
- Implement accessible or localized time pickers
- Troubleshoot TimePicker configuration or behavior issues

## Component Overview

The SfTimePicker provides:
- **14 predefined time formats** supporting 12/24-hour formats with hours, minutes, seconds, and milliseconds
- **Three picker modes**: Default (inline), Dialog (popup), and RelativeDialog (positioned popup)
- **Time intervals** for hours, minutes, seconds, and milliseconds
- **Time restrictions** including minimum/maximum time and blackout times
- **Looping support** for seamless navigation between first and last items
- **Rich event system** with selection changes, dialog lifecycle, and footer button events
- **MVVM support** through commands (SelectionChangedCommand, AcceptCommand, DeclineCommand)
- **Extensive customization** for header, footer, column headers, selection view, and text display modes
- **Accessibility** and localization support for global applications

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

**When to read:** Setting up TimePicker for the first time, installation, basic implementation.

**Coverage:**
- NuGet package installation (Syncfusion.Maui.Picker)
- Handler registration (ConfigureSyncfusionCore in MauiProgram.cs)
- Basic SfTimePicker initialization (XAML and C#)
- Setting header and footer views
- Configuring height and width
- Using SelectedTime property
- Clear selection support

### Time Formatting
📄 **Read:** [references/formatting.md](references/formatting.md)

**When to read:** Configuring how time is displayed (12/24 hour, including/excluding seconds, milliseconds).

**Coverage:**
- Format property overview
- 14 predefined time formats:
  - `H_mm`, `H_mm_ss` (24-hour without leading zero)
  - `HH_mm`, `HH_mm_ss`, `HH_mm_ss_fff` (24-hour with leading zero)
  - `h_mm_tt`, `h_mm_ss_tt` (12-hour without leading zero + AM/PM)
  - `hh_mm_tt`, `hh_mm_ss_tt`, `hh_mm_ss_fff_tt`, `hh_tt` (12-hour with leading zero + AM/PM)
  - `mm_ss`, `mm_ss_fff`, `ss_fff` (minute/second combinations)
  - `Default` (culture-based format)
- Format usage examples and switching between formats

### Picker Modes and Display
📄 **Read:** [references/picker-modes.md](references/picker-modes.md)

**When to read:** Configuring how the picker is displayed (inline, popup dialog, positioned dialog).

**Coverage:**
- Mode property (Default, Dialog, RelativeDialog)
- Dialog mode configuration
- IsOpen property for programmatic picker control
- RelativeDialog mode for positioned popups
- RelativePosition options (8 alignment positions):
  - AlignTop, AlignBottom, AlignToLeftOf, AlignToRightOf
  - AlignTopLeft, AlignTopRight, AlignBottomLeft, AlignBottomRight
- RelativeView property for positioning relative to specific controls
- Custom popup size (PopupWidth, PopupHeight properties)
- Code examples for each mode

### Time Intervals and Looping
📄 **Read:** [references/time-intervals-looping.md](references/time-intervals-looping.md)

**When to read:** Setting intervals between time values or enabling continuous looping.

**Coverage:**
- HourInterval property (e.g., show every 2 hours)
- MinuteInterval property (e.g., show every 5, 10, 15 minutes)
- SecondInterval property (e.g., show every 10 seconds)
- MilliSecondInterval property for precise time selection
- EnableLooping property for seamless first ↔ last item navigation
- Combining intervals with different time formats
- Practical scenarios (appointment booking, time tracking)

### Time Restrictions
📄 **Read:** [references/time-restrictions.md](references/time-restrictions.md)

**When to read:** Limiting selectable times (business hours, min/max ranges, blocked times).

**Coverage:**
- MinimumTime property to set earliest selectable time
- MaximumTime property to set latest selectable time
- BlackoutTimes collection to disable specific times
- Time range validation rules
- Use cases (business hours: 9 AM - 5 PM, appointment slots, blocked lunch hours)
- Combining restrictions with formats and intervals

### Events and Commands
📄 **Read:** [references/events-commands.md](references/events-commands.md)

**When to read:** Handling time selection changes, dialog lifecycle, or using MVVM commands.

**Coverage:**
- SelectionChanged event
  - TimePickerSelectionChangedEventArgs with NewValue and OldValue
  - IsSelectionImmediate behavior (immediate vs deferred selection)
- Dialog mode events:
  - Opened event (when picker opens)
  - Closing event with CancelEventArgs (can cancel closing)
  - Closed event (after picker closes)
- Footer view events:
  - OkButtonClicked event
  - CancelButtonClicked event
- MVVM Commands:
  - SelectionChangedCommand
  - AcceptCommand (OK button)
  - DeclineCommand (Cancel button)
- Event usage patterns and best practices

### Customization and Styling
📄 **Read:** [references/customization.md](references/customization.md)

**When to read:** Customizing picker appearance (colors, fonts, header/footer, visual effects).

**Coverage:**
- Header view customization
  - Text, Height, Background, TextStyle properties
- Footer view customization
  - OkButtonText, CancelButtonText
  - ShowOkButton, Height, Background, TextStyle
- Column header view customization
  - Text, Height, TextStyle per column
- Selection view customization
  - Background, Stroke, StrokeThickness, CornerRadius, TextStyle
- TextDisplayMode options:
  - Default, Fade, Shrink, FadeAndShrink
- Liquid glass effect for modern UI
- Item text styling
- Complete customization examples

### Accessibility and Localization
📄 **Read:** [references/accessibility-localization.md](references/accessibility-localization.md)

**When to read:** Implementing accessible controls or supporting multiple languages/cultures.

**Coverage:**
- WCAG compliance features
- Screen reader support
- Keyboard navigation
- Semantic properties for accessibility
- Localization configuration
- Culture-specific time formatting
- RTL (right-to-left) language support
- Multi-language implementation examples

