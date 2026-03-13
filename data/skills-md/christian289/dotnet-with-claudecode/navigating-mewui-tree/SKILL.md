---
name: navigating-mewui-tree
description: "Traverses and manipulates the MewUI visual tree. Use when understanding element hierarchy, finding parent/child elements, implementing IVisualTreeHost, or working with element lifecycle."
---

## Element Hierarchy

```
Element (base)
└─ UIElement (input, visibility, focus)
   └─ FrameworkElement (sizing, margin, alignment)
      ├─ Panel (multi-child: StackPanel, Grid, Canvas, DockPanel)
      ├─ Control (themed elements: Button, Label, TextBox)
      │  ├─ ContentControl (single child: Window)
      │  └─ Border (decorator)
      └─ ...
```

---

## Parent-Child Relationships

```csharp
// Every element has one parent
Element? parent = element.Parent;

// Multi-child (Panel)
panel.Add(child);       // Sets child.Parent = panel
panel.Remove(child);    // Sets child.Parent = null
panel.Children;         // IReadOnlyList<Element>

// Single-child (ContentControl, Border)
contentControl.Content = child;  // Element? type, sets child.Parent
border.Child = child;            // UIElement? type
```

---

## Tree Traversal

```csharp
// Find visual root (usually Window)
Element? root = element.FindVisualRoot();

// Check ancestry
bool isChild = element.IsDescendantOf(ancestor);
bool isParent = element.IsAncestorOf(descendant);  // Also available

// Find ancestor of type
static T? FindAncestor<T>(Element element) where T : Element
{
    for (var cur = element.Parent; cur != null; cur = cur.Parent)
        if (cur is T match) return match;
    return null;
}
```

Note: `VisualTree.Visit()` exists but is `internal` - use FindVisualRoot/IsDescendantOf for external code.

---

## IVisualTreeHost (Internal)

Interface for elements with children (internal API):

```csharp
internal interface IVisualTreeHost
{
    void VisitChildren(Action<Element> visitor);
}

// Panel implementation
void IVisualTreeHost.VisitChildren(Action<Element> visitor)
{
    foreach (var child in _children)
        visitor(child);
}

// ContentControl implementation
void IVisualTreeHost.VisitChildren(Action<Element> visitor)
{
    if (Content != null) visitor(Content);
}
```

---

## Visual Root Lifecycle

```csharp
// Called when element joins/leaves tree
protected virtual void OnVisualRootChanged(Element? oldRoot, Element? newRoot)
{
    // newRoot == null: removed from tree
    // newRoot is Window: added to tree
}
```

---

## Coordinate Transforms

```csharp
// Transform to ancestor
var transform = element.TransformToAncestor(ancestor);

// Translate point between elements
Point translated = element.TranslatePoint(localPoint, otherElement);

// Mouse position - use MouseEventArgs.Position property
protected override void OnMouseMove(MouseEventArgs e)
{
    Point pos = e.Position;  // Position relative to this element
}
```

---

**Hit testing**: See [hit-testing.md](hit-testing.md)
