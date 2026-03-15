---
name: using-mewui-layout
description: "Arranges UI elements using MewUI layout panels. Use when building UI layouts with StackPanel, Grid, Canvas, DockPanel, WrapPanel, or creating custom panels."
---

## Panel Quick Reference

| Panel | Use Case |
|-------|----------|
| `StackPanel` | Vertical/horizontal lists |
| `Grid` | Row/column layouts |
| `Canvas` | Absolute positioning |
| `DockPanel` | Edge docking (toolbars, status bars) |
| `WrapPanel` | Flow with wrapping |

---

## StackPanel

```csharp
new StackPanel()
    .Orientation(Orientation.Vertical)  // or .Horizontal(), .Vertical()
    .Spacing(8)
    .Children(
        new Label().Text("First"),
        new Label().Text("Second"),
        new Button().Content("Action")
    )
```

---

## Grid

```csharp
new Grid()
    .Rows("Auto,*,Auto")      // Auto, Star(*), Pixel(100)
    .Columns("200,*")
    .Spacing(8)               // Note: single Spacing property for both rows and columns
    .Children(
        new Label().Text("Header").Row(0).ColumnSpan(2),
        new ListBox().Row(1).Column(0),
        new ContentControl().Row(1).Column(1),
        new Button().Content("OK").Row(2).Column(1)
    )

// Convenience: .GridPosition(row, column) or .GridPosition(row, col, rowSpan, colSpan)
```

**Row/Column definitions:** `"Auto"` (content), `"*"` (proportional), `"2*"` (2x proportional), `"100"` (pixels)

---

## Canvas

```csharp
new Canvas()
    .Children(
        new Rectangle().CanvasLeft(10).CanvasTop(10).Width(50).Height(50),
        new Rectangle().CanvasRight(10).CanvasBottom(10).Width(50).Height(50)
    )

// Convenience: .CanvasPosition(left, top)
```

**Rules:** Left > Right, Top > Bottom. Both set = stretch.

---

## DockPanel

```csharp
new DockPanel()
    .LastChildFill(true)
    .Children(
        new Menu().DockTo(Dock.Top),        // Note: .DockTo() not .Dock()
        new StatusBar().DockTo(Dock.Bottom),
        new TreeView().DockTo(Dock.Left).Width(200),
        new ContentArea()  // Fills remaining space
    )

// Convenience methods: .DockTop(), .DockBottom(), .DockLeft(), .DockRight()
```

---

## WrapPanel

```csharp
new WrapPanel()
    .Orientation(Orientation.Horizontal)
    .Spacing(8)               // Note: single Spacing property for all gaps
    .ItemWidth(100).ItemHeight(100)  // Optional fixed size
    .Children(tag1, tag2, tag3, tag4)
```

---

## Alignment & Sizing

```csharp
element
    .Width(200).Height(100)
    .MinWidth(50).MaxWidth(500)
    .Margin(8)                    // All sides
    .Margin(8, 4)                 // H, V
    .Margin(8, 4, 8, 4)           // L, T, R, B
    .HorizontalAlignment(HorizontalAlignment.Center)
    .VerticalAlignment(VerticalAlignment.Stretch)
```

---

**Custom panels**: See [custom-panel.md](custom-panel.md)
**Attached properties**: See [attached-properties.md](attached-properties.md)
