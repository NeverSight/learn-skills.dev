---
name: syncfusion-blazor-sunburst-chart
description: >-
  Implement and customize the Syncfusion Blazor Sunburst Chart (SfSunburstChart)
  component, which renders hierarchical data as concentric rings of segments to
  create a multi-level pie chart. Use this skill whenever the user needs to build,
  configure, data-bind, theme, animate, label, add legends, highlight or select
  segments, enable drill-down with breadcrumbs, show tooltips, wire up events,
  print, export, or ensure accessibility for the Syncfusion Blazor Sunburst Chart.
  Trigger it for any mention of Sunburst Chart, multi-level pie, hierarchical
  ring chart, or SfSunburstChart in a Blazor Server, Blazor WebAssembly, or
  Blazor Web App (.NET 8/9/10 interactivity) context, even when the user just
  asks for "a chart that shows hierarchy" or "a pie with rings".
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization"
---

# Syncfusion Blazor Sunburst Chart

The `SfSunburstChart` renders hierarchical data as concentric rings of segments — a visual sometimes described as a multi-level pie chart or radial treemap. Each ring represents a level in the hierarchy inferred from a flat `DataSource`, and each segment represents a node in that hierarchy. The component is ideal for displaying population breakdowns, organizational workforces, file-system usage, sales by region, or any data with a parent-child structure that fits a parent → child traversal.

This skill guides you through setup across all Blazor hosting models, data binding from a flat collection, appearance and geometry, interactive features (highlight, selection, drill-down, tooltip, legend), events, printing/exporting, and accessibility.

## Table of Contents
- [When to Use This Skill](#when-to-use-this-skill)
- [Documentation and Navigation Guide](#documentation-and-navigation-guide)
  - [Getting Started](#getting-started)
  - [Getting Started — Blazor Web App](#getting-started--blazor-web-app)
  - [Getting Started — Standalone WebAssembly](#getting-started--standalone-webassembly)
  - [Working with Data](#working-with-data)
  - [Appearance](#appearance)
  - [Dimensions](#dimensions)
  - [Animation](#animation)
  - [Data Label](#data-label)
  - [Legend](#legend)
  - [Highlight](#highlight)
  - [Selection](#selection)
  - [Drill-Down](#drill-down)
  - [Tooltip](#tooltip)
  - [Events](#events)
  - [Print and Export](#print-and-export)
  - [Accessibility](#accessibility)
- [Quick Start](#quick-start)
- [Common Patterns](#common-patterns)
  - [Enable legend, tooltip, and data labels together](#enable-legend-tooltip-and-data-labels-together)
  - [Enable drill-down with breadcrumbs](#enable-drill-down-with-breadcrumbs)
  - [Full interactive dashboard (palette + legend + data labels + drill-down + tooltip)](#full-interactive-dashboard-palette--legend--data-labels--drill-down--tooltip)
- [Key Props Reference](#key-props-reference)
- [See also](#see-also)

## When to Use This Skill

- Add a Sunburst Chart to a Blazor Server, WebAssembly, or Web App project.
- Bind hierarchical data using `IdMemberPath`, `ParentIdMemberPath`, `LabelMemberPath`, and `ValueMemberPath`.
- Customize theme, palette, background, border, margin, radius, inner radius, start/end angles, title, and subtitle.
- Size the chart to fit a container, fixed pixels, or percentages.
- Enable and style data labels, legend, highlight, selection, drill-down with breadcrumbs, and tooltips.
- Subscribe to drill, click, selection, legend, data-label, segment, tooltip, loaded, and export events.
- Print the chart or export it as PNG, JPEG, SVG, PDF, XLSX, or CSV.
- Meet WCAG 2.2 AA, Section 508, screen reader, keyboard, and ARIA accessibility requirements.

Package: `Syncfusion.Blazor.Charts` NuGet. Platform: Blazor (.NET 8/9/10).

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Create a Blazor Server App, install the NuGet package, and add `_Imports.razor` namespaces.
- Register `AddSyncfusionBlazor()` in `Program.cs`.
- Add the script reference and first chart example.

### Getting Started — Blazor Web App
📄 **Read:** [references/getting-started-web-app.md](references/getting-started-web-app.md)
- Create a Blazor Web App (Server/WebAssembly/Auto interactivity).
- Install the package in the `.Client` project for WASM/Auto render modes.
- Register services, add the script reference, and render the first chart.

### Getting Started — Standalone WebAssembly
📄 **Read:** [references/getting-started-wasm.md](references/getting-started-wasm.md)
- Create a standalone Blazor WebAssembly app.
- Install the package, register the service, add the script to `index.html`.
- Render the first chart.

### Working with Data
📄 **Read:** [references/working-with-data.md](references/working-with-data.md)
- Bind a flat collection via `DataSource` and the four member paths.
- Required member paths and the hierarchy-inference rules.
- Hierarchy validation: missing/duplicate IDs, cycles, unresolvable parents, multiple roots, and depth limits.
- Reflection binding with `nameof`, numeric values and culture, and data updates.

### Appearance
📄 **Read:** [references/appearance.md](references/appearance.md)
- Built-in themes via `Theme`, custom color palette via `Palette`, and `Background`.
- Chart border using `SunburstChartBorder`, chart margin using `SunburstChartMargin`.
- Ring geometry: `Radius`, `InnerRadius`, `StartAngle`, `EndAngle`.
- Title and subtitle via `SunburstTitleSettings` and `SunburstSubtitleSettings`.

### Dimensions
📄 **Read:** [references/dimensions.md](references/dimensions.md)
- Size the chart to fit a container with CSS, fixed pixels, or percentage values.
- `Width` and `Height` defaults (`100%` each).

### Animation
📄 **Read:** [references/animation.md](references/animation.md)
- `EnableAnimation` (default `true`) toggles the entrance animation.
- `AnimationType` chooses `Rotation` (default) or `FadeIn`.
- Disabling animation for performance and large datasets.

### Data Label
📄 **Read:** [references/data-label.md](references/data-label.md)
- Enable labels via `SunburstDataLabelSettings.Visible`.
- `OverflowMode` (Trim, Hide, None) and `RotationMode` (Angle, Normal).
- Customize text style with `SunburstDataLabelTextStyle`.

### Legend
📄 **Read:** [references/legend.md](references/legend.md)
- Enable and position the legend via `SunburstLegendSettings`.
- `Position` (Top, Bottom, Left, Right), `ToggleVisibility`, and accessibility properties.
- Customize appearance with `SunburstLegendTextStyle` and `SunburstLegendBorder`.

### Highlight
📄 **Read:** [references/highlight.md](references/highlight.md)
- Enable hover highlighting via `SunburstHighlightSettings`.
- `Mode` (Single, Parent, Child, All), `Color`, and `Opacity`.
- Tooltip-driven highlighting with `SunburstTooltipSettings.EnableHighlight`.

### Selection
📄 **Read:** [references/selection.md](references/selection.md)
- Enable segment selection via `SunburstSelectionSettings`.
- `Mode` (Single [default], Parent, Child, All), `Color`, and `Opacity`.
- Selection clears on re-click and drill navigation.

### Drill-Down
📄 **Read:** [references/drill-down.md](references/drill-down.md)
- `SunburstDrillSettings.Enable` activates drill-down (double-click, double-tap, or Enter).
- Breadcrumb position belongs to `SunburstDrillSettings` (`BreadcrumbHorizontalAlignment`, `BreadcrumbVerticalAlignment`); appearance and accessibility belong to the nested `SunburstBreadcrumbSettings` child component.

### Tooltip
📄 **Read:** [references/tooltip.md](references/tooltip.md)
- `SunburstTooltipSettings.Enable` displays label and value.
- `Format`, `HeaderText`, `EnableHighlight`, `ShowHeaderLine`, `Opacity`, `Fill`.
- Customize text style and border.

### Events
📄 **Read:** [references/events.md](references/events.md)
- Drills: `DrillDownStarting`/`DrillUpStarting` (cancelable), `DrillDownCompleted`/`DrillUpCompleted`.
- Interactions: `PointClick`, `SelectionChanged`, `LegendClick`.
- Rendering: `LegendItemRendering`, `DataLabelRendering`, `SegmentRendering`, `TooltipRendering`.
- Lifecycle and export: `Loaded`, `PrintCompleted`, `Exporting`, `ExportCompleted`.
- `Action<>` vs `EventCallback<>` semantics.

### Print and Export
📄 **Read:** [references/print-export.md](references/print-export.md)
- Print via `PrintAsync`.
- Export via `ExportAsync` to PNG, JPEG, SVG, PDF (with orientation), XLSX, or CSV.
- `AllowDownload` and `IsBase64` parameters.

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 AA, Section 508, screen reader, keyboard, and ARIA support.
- WAI-ARIA roles and attributes for segments, levels, breadcrumbs, and legend.
- Keyboard navigation table (Tab, arrows, Home, End, Enter, Space).

## Quick Start

```cshtml
@using Syncfusion.Blazor.Charts

<SfSunburstChart TItem="NodeDetails"
                 Title="Population by Region"
                 DataSource="@DataSource"
                 IdMemberPath="@nameof(NodeDetails.Id)"
                 ParentIdMemberPath="@nameof(NodeDetails.ParentId)"
                 ValueMemberPath="@nameof(NodeDetails.Value)"
                 LabelMemberPath="@nameof(NodeDetails.Name)"
                 Width="100%"
                 Height="450px">
</SfSunburstChart>

@code {
    public class NodeDetails
    {
        public string Id { get; set; } = string.Empty;
        public string? ParentId { get; set; }
        public string Name { get; set; } = string.Empty;
        public double Value { get; set; }
    }

    public List<NodeDetails> DataSource = new()
    {
        new NodeDetails { Id = "USA", ParentId = null, Name = "USA" },
        new NodeDetails { Id = "USA-Electronics", ParentId = "USA", Name = "Electronics", Value = 35 },
        new NodeDetails { Id = "India", ParentId = null, Name = "India" },
        new NodeDetails { Id = "India-Electronics", ParentId = "India", Name = "Electronics", Value = 30 },
        new NodeDetails { Id = "Germany", ParentId = null, Name = "Germany" },
        new NodeDetails { Id = "Germany-Electronics", ParentId = "Germany", Name = "Electronics", Value = 20 }
    };
}
```

## Common Patterns

### Enable legend, tooltip, and data labels together

```cshtml
<SfSunburstChart TItem="RegionData"
                 DataSource="@Regions"
                 IdMemberPath="@nameof(RegionData.Id)"
                 ParentIdMemberPath="@nameof(RegionData.ParentId)"
                 LabelMemberPath="@nameof(RegionData.Label)"
                 ValueMemberPath="@nameof(RegionData.Population)"
                 Width="100%" Height="600px">
    <SunburstLegendSettings Visible="true" Position="SunburstLegendPosition.Bottom" />
    <SunburstTooltipSettings Enable="true" />
    <SunburstDataLabelSettings Visible="true" />
</SfSunburstChart>
```

### Enable drill-down with breadcrumbs

```cshtml
<SfSunburstChart TItem="RegionData"
                 DataSource="@Regions"
                 IdMemberPath="@nameof(RegionData.Id)"
                 ParentIdMemberPath="@nameof(RegionData.ParentId)"
                 LabelMemberPath="@nameof(RegionData.Label)"
                 ValueMemberPath="@nameof(RegionData.Population)"
                 Width="100%" Height="600px">
    <SunburstDrillSettings Enable="true" ShowBreadcrumbs="true" />
</SfSunburstChart>
```

### Full interactive dashboard (palette + legend + data labels + drill-down + tooltip)

A common real-world request combines custom colors, an interactive legend, readable data labels, drill-down navigation, and a highlighted tooltip. Set the breadcrumb alignment to `Bottom` and `Center` when the user wants breadcrumbs below the chart rather than at the top (the default is `Top`/`Left`).

```cshtml
<SfSunburstChart TItem="NodeDetails"
                 Title="Global Workforce Distribution"
                 DataSource="@WorkforceData"
                 Palette="@BrandPalette"
                 IdMemberPath="@nameof(NodeDetails.Id)"
                 ParentIdMemberPath="@nameof(NodeDetails.ParentId)"
                 LabelMemberPath="@nameof(NodeDetails.Name)"
                 ValueMemberPath="@nameof(NodeDetails.HeadCount)"
                 Width="90%" Height="600px">
    <SunburstLegendSettings Visible="true"
                            Position="SunburstLegendPosition.Top"
                            ToggleVisibility="true" />
    <SunburstDataLabelSettings Visible="true"
                               OverflowMode="SunburstLabelOverflowMode.Hide"
                               RotationMode="SunburstLabelRotationMode.Normal" />
    <SunburstDrillSettings Enable="true"
                           ShowBreadcrumbs="true"
                           BreadcrumbHorizontalAlignment="BreadcrumbHorizontalAlignment.Center"
                           BreadcrumbVerticalAlignment="BreadcrumbVerticalAlignment.Bottom">
        <SunburstBreadcrumbSettings FontWeight="600"
                                     Separator=">"
                                     SeparatorColor="#9E9E9E" />
    </SunburstDrillSettings>
    <SunburstTooltipSettings Enable="true"
                             HeaderText="Workforce Detail"
                             EnableHighlight="true" />
</SfSunburstChart>
```

## Key Props Reference

| Property | Component | Purpose |
|----------|-----------|---------|
| `DataSource` | `SfSunburstChart` | Flat `IEnumerable<TItem>` providing the rows |
| `IdMemberPath` | `SfSunburstChart` | Property name for each row's stable ID (required) |
| `ParentIdMemberPath` | `SfSunburstChart` | Property name for each row's parent ID (required) |
| `LabelMemberPath` | `SfSunburstChart` | Property name for each segment's label text (required) |
| `ValueMemberPath` | `SfSunburstChart` | Numeric property for each segment's value (required) |
| `Theme` | `SfSunburstChart` | Built-in theme (`Theme.Bootstrap5`, `Fluent`, etc.) |
| `Palette` | `SfSunburstChart` | Custom color array for root-level segments |
| `Radius` / `InnerRadius` | `SfSunburstChart` | Ring geometry ratios (0-1) |
| `StartAngle` / `EndAngle` | `SfSunburstChart` | Angular span in degrees |
| `EnableAnimation` | `SfSunburstChart` | Toggle entrance animation (default `true`) |
| `AnimationType` | `SfSunburstChart` | `Rotation` (default) or `FadeIn` |
| `Title` / `Subtitle` | `SfSunburstChart` | Chart heading and optional secondary line |

## See also

- Syncfusion Blazor Charts NuGet package: `Syncfusion.Blazor.Charts`
- [Getting Started — Blazor Server App](references/getting-started.md)
- [Getting Started — Blazor Web App](references/getting-started-web-app.md)
- [Getting Started — Standalone WebAssembly](references/getting-started-wasm.md)
- [Working with Data](references/working-with-data.md)
- [Appearance](references/appearance.md)
