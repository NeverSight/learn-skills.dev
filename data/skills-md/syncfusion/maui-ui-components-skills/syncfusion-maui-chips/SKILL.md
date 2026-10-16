---
name: syncfusion-maui-chips
description: Implements Syncfusion .NET MAUI Chips (SfChip or SfChipGroup). Use when working with chips, tags, tag controls, selection chips, input chips, or filter chips in .NET MAUI applications. Covers chip types, chip customization, chip events, chip selection, chip groups, remove chips, close button chips, and chip data binding.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Implementing .NET MAUI Chips

The Syncfusion .NET MAUI Chips control provides versatile and feature-rich components (`SfChip` and `SfChipGroup`) for displaying information in compact, interactive layouts. Chips enable users to view, select, filter, or trigger actions through visually appealing and customizable UI elements.

## When to Use This Skill

Use this skill when the user needs to:

- **Display categorical data** as compact, interactive chips (tags, labels, categories)
- **Implement selection interfaces** with single or multi-select chip groups
- **Create input chips** that can be dynamically added or removed by users
- **Build filter interfaces** with multi-selection indicators for data filtering
- **Add action chips** that execute commands when clicked
- **Customize chip appearance** with colors, borders, icons, fonts, and images
- **Handle chip interactions** through selection events, click handlers, or removal events
- **Bind chip data** from collections using ItemsSource and DisplayMemberPath

## Component Overview

**SfChip:** Individual chip component with text, icon, close button, and customization options.

**SfChipGroup:** Container that manages multiple chips with support for:
- Four chip types: Input, Choice, Filter, Action
- Data binding with ItemsSource
- Selection modes and visual states
- Layout customization (FlexLayout, StackLayout, etc.)
- Event handling for selection and removal

**Key Capabilities:**
- Dynamic chip creation and removal
- Single and multi-selection modes
- Visual selection indicators
- Icon and background image support
- Comprehensive styling options
- MVVM command support
- Event-driven interactions

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

When the user needs to:
- Install and configure Syncfusion .NET MAUI Chips package
- Register the Syncfusion Core handler in MauiProgram.cs
- Create first SfChip or SfChipGroup
- Set up chip layouts (FlexLayout, StackLayout)
- Understand basic chip setup and configuration
- See a minimal working example

### Chip Types and Selection Modes
📄 **Read:** [references/chip-types.md](references/chip-types.md)

When the user needs to:
- Understand the four chip types: Input, Choice, Filter, Action
- Implement Input chips with dynamic add/remove functionality
- Create Choice chips with single selection (ChoiceMode: Single, SingleOrNone)
- Build Filter chips with multi-selection and selection indicators
- Use Action chips with command execution
- Configure visual states for selected/normal states
- Choose the appropriate chip type for their use case

### Customization and Styling
📄 **Read:** [references/customization.md](references/customization.md)

When the user needs to:
- Customize individual SfChip appearance
  - Show/hide close button and selection indicator
  - Change colors (background, text, border, close button, selection indicator)
  - Modify border properties (stroke thickness, corner radius)
  - Style text (font size, family, attributes, color, alignment)
  - Configure icons (show, source, size, alignment)
  - Add background images
- Customize SfChipGroup styling
  - Set chip and selected chip colors
  - Configure border and padding
  - Adjust item height and text size
  - Style selection indicators
- Implement commands for MVVM pattern
- Apply consistent theming across chip groups

### Populating Data
📄 **Read:** [references/populating-data.md](references/populating-data.md)

When the user needs to:
- Bind business objects to chips using ItemsSource
- Use DisplayMemberPath to specify the text property
- Use ImageMemberPath to bind icon images
- Create model and ViewModel classes for chip data
- Populate chips with SfChip items directly using Items collection
- Add InputView for dynamic chip creation
- Implement data binding best practices
- Handle AOT publishing considerations with [Preserve] attribute

### Events and Interactions
📄 **Read:** [references/events.md](references/events.md)

When the user needs to:
- Handle SelectionChanging event (cancellable, before selection)
- Handle SelectionChanged event (after selection completes)
- Respond to ChipClicked events
- Handle ItemRemoved events for Input type chips
- Capture CloseButtonClicked events
- Understand event arguments and properties
- Know which events are supported for each chip type

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

When the user needs to:
- Apply font icons to chips (custom icon fonts)
- Use DataTemplateSelector for custom chip templates
- Implement Liquid Glass visual effects
- Programmatically control selection with IsSelected property
- Handle AOT publishing requirements
- Apply platform-specific customizations

