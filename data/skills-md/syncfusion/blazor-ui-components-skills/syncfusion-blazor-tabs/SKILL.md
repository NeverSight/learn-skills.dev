---
name: syncfusion-blazor-tabs
description: Implement Syncfusion Blazor Tab component for tabbed navigation interfaces. Use this skill whenever the user needs to create tab navigation, organize content into tabs, handle tab selection, manage tab items, configure tab orientation, customize tab appearance, implement responsive tab modes, or build any tabbed interface in Blazor applications.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Navigation"
---

# Implementing Syncfusion Blazor Tabs Component

## When to Use This Skill

Use the Syncfusion Blazor Tabs component when you need to:
- Organize content into multiple sections with tab-based navigation
- Create tabbed interfaces for content organization and switching
- Handle programmatic and user-driven tab selection
- Dynamically add, remove, or manage tab items
- Implement vertical or horizontal tab layouts
- Build responsive tab interfaces that adapt to different screen sizes
- Create nested tab structures for hierarchical content organization
- Customize tab appearance, styling, and animations
- Implement multi-step wizards with conditional navigation
- Enable drag-and-drop for tab reordering
- Persist tab state across page refreshes

## Component Overview

The Syncfusion Blazor Tabs component (`SfTab`) provides a flexible, accessible, and feature-rich tabbed navigation interface with support for:
- Multiple tab items with customizable headers and content
- Dynamic tab management (add/remove items programmatically)
- Multiple header placements (Top, Bottom, Left, Right)
- Responsive overflow modes (Scrollable, Popup)
- Two-way binding with `SelectedItem` property
- Comprehensive event system for user interactions
- Content rendering modes (Dynamic, On-Demand, Initial)
- Rich templating with `ContentTemplate` and `HeaderTemplate`
- Animation support with multiple effects
- State persistence through browser cookies
- Full keyboard and screen reader accessibility
- Drag-and-drop support for tab reordering

### Key Components
- **SfTab**: Main container component managing all tabs
- **TabItems**: Collection container for tab items
- **TabItem**: Individual tab with header and content
- **TabHeader**: Header configuration for tab title, icons, and positioning
- **TabEvents**: Event handlers for tab interactions
- **TabAnimationSettings**: Animation configuration for tab transitions
- **ContentTemplate**: Template for rendering complex content
- **HeaderTemplate**: Template for custom header rendering

---

## Installation and Setup

### Prerequisites
- .NET 6.0 or higher
- Blazor WebAssembly or Blazor Server application

### NuGet Package Installation

```csharp
// Install via Package Manager Console
Install-Package Syncfusion.Blazor.Navigations
Install-Package Syncfusion.Blazor.Themes
```

Or via .NET CLI:
```bash
dotnet add package Syncfusion.Blazor.Navigations
dotnet add package Syncfusion.Blazor.Themes
```

### Register Syncfusion Blazor Service

In **Program.cs**:
```csharp
using Syncfusion.Blazor;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.Services.AddSyncfusionBlazor();
await builder.Build().RunAsync();
```

### Add Namespaces

In **_Imports.razor**:
```csharp
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Navigations
```

### Add Theme and Script References

In **index.html** (in `<head>` section):
```html
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
<script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js" type="text/javascript"></script>
```

---

## Basic Implementation

### Minimal Blazor Tabs Component Setup

```razor
@using Syncfusion.Blazor.Navigations

<SfTab>
    <TabItems>
        <TabItem>
            <ChildContent>
                <TabHeader Text="Tab 1"></TabHeader>
            </ChildContent>
            <ContentTemplate>
                <div>Content for Tab 1</div>
            </ContentTemplate>
        </TabItem>
        <TabItem>
            <ChildContent>
                <TabHeader Text="Tab 2"></TabHeader>
            </ChildContent>
            <ContentTemplate>
                <div>Content for Tab 2</div>
            </ContentTemplate>
        </TabItem>
        <TabItem>
            <ChildContent>
                <TabHeader Text="Tab 3"></TabHeader>
            </ChildContent>
            <ContentTemplate>
                <div>Content for Tab 3</div>
            </ContentTemplate>
        </TabItem>
    </TabItems>
</SfTab>
```

---

## Core API Reference

### SfTab Component Properties

| Property | Type | Default | Description | Example |
|----------|------|---------|-------------|---------|
| `AllowDragAndDrop` | bool | false | Enables drag-and-drop reordering of tabs | `AllowDragAndDrop="true"` |
| `CssClass` | string | null | CSS class applied to the Tab container | `CssClass="e-fill"` |
| `DragArea` | string | null | Sets the area to move the draggable element; dragging is restricted outside this area | `DragArea="body"` |
| `EnablePersistence` | bool | false | Enables state persistence in browser cookies | `EnablePersistence="true"` |
| `Height` | string | null | Height of the Tab component | `Height="250px"` |
| `HeaderPlacement` | HeaderPosition | Top | Position of tab headers (Top, Bottom, Left, Right) | `HeaderPlacement="HeaderPosition.Left"` |
| `ID` | string | null | Unique identifier for the component (required for persistence) | `ID="myTabs"` |
| `LoadOn` | ContentLoad | Dynamic | Content rendering mode (Dynamic, Demand, Init) | `LoadOn="ContentLoad.Demand"` |
| `OverflowMode` | OverflowMode | Scrollable | Behavior for overflowed tabs (Scrollable, Popup) | `OverflowMode="OverflowMode.Popup"` |
| `ReorderActiveTab` | bool | true | Reorders active tab when clicking from popup | `ReorderActiveTab="false"` |
| `ScrollStep` | int | 0 | Number of pixels to scroll when clicking navigation arrows | `ScrollStep="150"` |
| `SelectedItem` | int | 0 | Index of currently selected tab (supports two-way binding) | `@bind-SelectedItem="tabIndex"` |
| `ShowCloseButton` | bool | false | Shows close button on tab headers | `ShowCloseButton="true"` |
| `SwipeMode` | TabSwipeMode | TabSwipeMode.Touch \| TabSwipeMode.Mouse | Enables swipe gestures for tab navigation | `SwipeMode="TabSwipeMode.Touch"` |
| `Width` | string | null | Width of the Tab component | `Width="500px"` |
| `Locale` | string | "en-US" | Sets the locale for localization support | `Locale="fr-FR"` |
| `ShouldReinitialize` | bool | false | Gets or sets a value that indicates whether to re-initialize the tab content on every TabItem initialization | `ShouldReinitialize="true"` |

#### Property Examples

**Setting HeaderPlacement to create vertical tabs:**
```razor
<SfTab HeaderPlacement="HeaderPosition.Left" Height="250px" Width="500px">
    <TabItems>
        <!-- Tab items -->
    </TabItems>
</SfTab>
```

**Enabling drag-and-drop for tab reordering:**
```razor
<SfTab AllowDragAndDrop="true">
    <TabItems>
        <!-- Tab items -->
    </TabItems>
</SfTab>
```

**Restricting drag area with DragArea property:**
```razor
<div id="dragContainer" style="border: 2px solid blue; padding: 10px;">
    <SfTab AllowDragAndDrop="true" DragArea="#dragContainer">
        <TabItems>
            <TabItem>
                <ChildContent>
                    <TabHeader Text="Tab 1"></TabHeader>
                </ChildContent>
                <ContentTemplate>Tab 1 content</ContentTemplate>
            </TabItem>
            <TabItem>
                <ChildContent>
                    <TabHeader Text="Tab 2"></TabHeader>
                </ChildContent>
                <ContentTemplate>Tab 2 content</ContentTemplate>
            </TabItem>
            <TabItem>
                <ChildContent>
                    <TabHeader Text="Tab 3"></TabHeader>
                </ChildContent>
                <ContentTemplate>Tab 3 content</ContentTemplate>
            </TabItem>
        </TabItems>
    </SfTab>
</div>
```

**Two-way binding with SelectedItem:**
```razor
<SfNumericTextBox @bind-Value="SelectedTabIndex" Min="0" Max="4"></SfNumericTextBox>

<SfTab @bind-SelectedItem="SelectedTabIndex">
    <TabItems>
        <!-- Tab items -->
    </TabItems>
</SfTab>

@code {
    private int SelectedTabIndex = 0;
}
```

**Enabling state persistence:**
```razor
<SfTab ID="PersistentTabs" EnablePersistence="true">
    <TabItems>
        <!-- Tab items -->
    </TabItems>
</SfTab>
```

**Customizing scroll step for scrollable mode:**
```razor
<SfTab Width="400px" OverflowMode="OverflowMode.Scrollable" ScrollStep="150">
    <TabItems>
        <!-- Tab items -->
    </TabItems>
</SfTab>
```

**Disabling swipe gestures:**
```razor
<SfTab SwipeMode="~TabSwipeMode.Touch & ~TabSwipeMode.Mouse">
    <TabItems>
        <!-- Tab items -->
    </TabItems>
</SfTab>
```

**Setting locale for localization:**
```razor
<SfTab Locale="fr-FR">
    <TabItems>
        <TabItem Content="Onglet 1">
            <ChildContent>
                <TabHeader Text="Tab 1"></TabHeader>
            </ChildContent>
        </TabItem>
    </TabItems>
</SfTab>
```

**Using ShouldReinitialize to re-initialize tab content on every TabItem initialization:**
```razor
@using Syncfusion.Blazor.Navigations
@using Syncfusion.Blazor.Buttons

<SfButton @onclick="ToggleReinitialize">Toggle Re-initialization</SfButton>
<p>Re-initialize: @shouldReinitialize</p>

<SfTab ShouldReinitialize="@shouldReinitialize">
    <TabItems>
        <TabItem>
            <ChildContent>
                <TabHeader Text="Tab 1"></TabHeader>
            </ChildContent>
            <ContentTemplate>
                <div>
                    <p>Content loaded at: @DateTime.Now.ToString("HH:mm:ss.fff")</p>
                    <p>This content reloads every time ShouldReinitialize is triggered</p>
                </div>
            </ContentTemplate>
        </TabItem>
        <TabItem>
            <ChildContent>
                <TabHeader Text="Tab 2"></TabHeader>
            </ChildContent>
            <ContentTemplate>
                <div>
                    <p>Content loaded at: @DateTime.Now.ToString("HH:mm:ss.fff")</p>
                    <p>This content reloads every time ShouldReinitialize is triggered</p>
                </div>
            </ContentTemplate>
        </TabItem>
    </TabItems>
</SfTab>

@code {
    private bool shouldReinitialize = false;

    private async Task ToggleReinitialize()
    {
        shouldReinitialize = !shouldReinitialize;
        await Task.Delay(500);
        shouldReinitialize = !shouldReinitialize;
    }
}
```

---

### TabItems Collection Properties

| Property | Type | Default | Description | Example |
|----------|------|---------|-------------|---------|
| `Items` | List<TabItem> | Empty | Gets or sets the list of tab items to be rendered in the tab panel | `Items="@tabItems"` |

#### TabItems Property Examples

**Using Items property to bind tab items from a list:**
```razor
@using Syncfusion.Blazor.Navigations

<SfButton @onclick="AddTab">Add Tab</SfButton>
<SfButton @onclick="RemoveTab">Remove Tab</SfButton>

<SfTab>
    <TabItems Items="@TabItems">
    </TabItems>
</SfTab>

@code {
    private List<TabItem> TabItems = new List<TabItem>();

    protected override void OnInitialized()
    {
        TabItems = new List<TabItem>
        {
            new TabItem
            {
                Header = new TabHeader { Text = "HTML" },
                Content = "HTML is the standard markup language"
            },
            new TabItem
            {
                Header = new TabHeader { Text = "CSS" },
                Content = "CSS is used for styling web pages"
            },
            new TabItem
            {
                Header = new TabHeader { Text = "JavaScript" },
                Content = "JavaScript is a programming language"
            }
        };
    }

    private void AddTab()
    {
        TabItems.Add(new TabItem
        {
            Header = new TabHeader { Text = $"New Tab {TabItems.Count + 1}" },
            Content = "New tab content"
        });
    }

    private void RemoveTab()
    {
        if (TabItems.Count > 0)
            TabItems.RemoveAt(TabItems.Count - 1);
    }
}
```

---

### TabItem Component Properties

| Property | Type | Default | Description | Example |
|----------|------|---------|-------------|---------|
| `Content` | string | null | Simple string content for the tab | `Content="Tab content text"` |
| `ContentTemplate` | RenderFragment | null | Template for rendering complex content | `<ContentTemplate>...</ContentTemplate>` |
| `Disabled` | bool | false | Disables the tab item and prevents selection | `Disabled="true"` |
| `HeaderTemplate` | RenderFragment | null | Template for custom header rendering | `<HeaderTemplate>...</HeaderTemplate>` |
| `TabIndex` | int | -1 | Tab order for keyboard navigation | `TabIndex="0"` |
| `Visible` | bool | true | Shows or hides the tab item | `Visible="true"` |

#### Property Examples

**Disabling specific tab items:**
```razor
<SfTab>
    <TabItems>
        <TabItem Content="Available tab">
            <ChildContent>
                <TabHeader Text="Tab 1"></TabHeader>
            </ChildContent>
        </TabItem>
        <TabItem Disabled="true" Content="Unavailable tab">
            <ChildContent>
                <TabHeader Text="Tab 2 (Disabled)"></TabHeader>
            </ChildContent>
        </TabItem>
    </TabItems>
</SfTab>
```

**Toggling tab visibility:**
```razor
<SfButton @onclick="ToggleVisibility">Toggle Tab Visibility</SfButton>

<SfTab>
    <TabItems>
        <TabItem Visible="@isTabVisible" Content="Visible/Hidden Tab">
            <ChildContent>
                <TabHeader Text="Toggle Tab"></TabHeader>
            </ChildContent>
        </TabItem>
    </TabItems>
</SfTab>

@code {
    private bool isTabVisible = true;

    private void ToggleVisibility()
    {
        isTabVisible = !isTabVisible;
    }
}
```

**Enabling Tab key navigation:**
```razor
<SfTab>
    <TabItems>
        <TabItem TabIndex="0">
            <ChildContent>
                <TabHeader Text="Tab 1"></TabHeader>
            </ChildContent>
            <ContentTemplate>Content 1</ContentTemplate>
        </TabItem>
        <TabItem TabIndex="0">
            <ChildContent>
                <TabHeader Text="Tab 2"></TabHeader>
            </ChildContent>
            <ContentTemplate>Content 2</ContentTemplate>
        </TabItem>
    </TabItems>
</SfTab>
```

---

### TabHeader Component Properties

| Property | Type | Default | Description | Example |
|----------|------|---------|-------------|---------|
| `IconCss` | string | null | CSS class for tab header icon | `IconCss="e-twitter"` |
| `IconPosition` | IconPosition | Left | Icon position relative to text (Left, Right, Top, Bottom) | `IconPosition="IconPosition.Top"` |
| `Text` | string | null | Header text display | `Text="Tab Title"` |

#### Property Examples

**Adding icons to tab headers:**
```razor
<SfTab>
    <TabItems>
        <TabItem>
            <ChildContent>
                <TabHeader Text="Twitter" IconCss="e-twitter" IconPosition="IconPosition.Left"></TabHeader>
            </ChildContent>
            <ContentTemplate>Twitter content...</ContentTemplate>
        </TabItem>
        <TabItem>
            <ChildContent>
                <TabHeader Text="Facebook" IconCss="e-facebook" IconPosition="IconPosition.Top"></TabHeader>
            </ChildContent>
            <ContentTemplate>Facebook content...</ContentTemplate>
        </TabItem>
    </TabItems>
</SfTab>
```

---

### Methods

| Method | Parameters | Return Type | Description | Example |
|--------|-----------|------------|-------------|---------|
| `AddTab` | `List<TabItem> items, int index` | Task | Adds new tab items at specified index | `await Tab.AddTab(newItems, 1)` |
| `EnableTabAsync` | `int index, bool enable` | Task | Enables or disables a tab item | `await Tab.EnableTabAsync(0, false)` |
| `RemoveTab` | `int index` | void | Removes tab item at specified index | `Tab.RemoveTab(0)` |
| `Select` | `int index` | void | Selects a tab by index (non-async) | `Tab.Select(1)` |
| `SelectAsync` | `int index` | Task | Asynchronously selects a tab by index | `await Tab.SelectAsync(1)` |

#### Method Examples

**Dynamically adding tabs:**
```razor
<SfButton @onclick="AddNewTab">Add Tab</SfButton>

<SfTab @ref="TabControl">
    <TabItems>
        <!-- Initial tabs -->
    </TabItems>
</SfTab>

@code {
    private SfTab TabControl;

    private async Task AddNewTab()
    {
        var newTab = new TabItem
        {
            Header = new TabHeader { Text = "New Tab" },
            Content = "New tab content"
        };

        await TabControl.AddTab(new List<TabItem> { newTab }, TabControl.Items.Count);
    }
}
```

**Removing tabs:**
```razor
<SfButton @onclick="RemoveFirstTab">Remove First Tab</SfButton>

<SfTab @ref="TabControl">
    <TabItems>
        <!-- tabs -->
    </TabItems>
</SfTab>

@code {
    private SfTab TabControl;

    private void RemoveFirstTab()
    {
        if (TabControl.Items.Count > 0)
        {
            TabControl.RemoveTab(0);
        }
    }
}
```

**Programmatically selecting tabs:**
```razor
<SfButton @onclick="SelectTab">Select Tab 2</SfButton>

<SfTab @ref="TabControl">
    <TabItems>
        <!-- tabs -->
    </TabItems>
</SfTab>

@code {
    private SfTab TabControl;

    private async Task SelectTab()
    {
        await TabControl.SelectAsync(1);
    }
}
```

**Enabling/disabling tabs conditionally:**
```razor
<SfButton @onclick="DisableSecondTab">Disable Tab 2</SfButton>

<SfTab @ref="TabControl" ID="ConditionTab">
    <TabItems>
        <!-- tabs -->
    </TabItems>
</SfTab>

@code {
    private SfTab TabControl;

    private async Task DisableSecondTab()
    {
        await TabControl.EnableTabAsync(1, false);
    }
}
```

---

### Events and Event Arguments

| Event | Handler Type | EventArgs | Description | Fires When |
|-------|-------------|-----------|-------------|-----------|
| `Created` | EventCallback | CreatedEventArgs | Fires after component is created and rendered | Component initialization completes |
| `Dragged` | EventCallback | DragEventArgs | Fires when drag-drop action completes | Tab item drop action completes |
| `OnDragStart` | EventCallback | DragStartEventArgs | Fires before tab drag starts | User initiates drag on tab |
| `Selecting` | EventCallback | SelectingEventArgs | Fires before tab selection changes | User clicks or Select() is called |
| `Selected` | EventCallback | SelectEventArgs | Fires after tab selection changes | New tab becomes active |

#### Event Arguments

**SelectingEventArgs:**
- `Cancel` (bool): Set to true to prevent tab selection
- `PreviousIndex` (int): Index of previously selected tab
- `Index` (int): Index of tab being selected

**SelectEventArgs:**
- `Index` (int): Index of newly selected tab
- `PreviousIndex` (int): Index of previously selected tab
- `IsInteracted` (bool): true if user clicked; false if programmatically selected

**DragStartEventArgs:**
- `Cancel` (bool): Set to true to prevent drag operation
- `DraggedItem` (TabItem): The tab item being dragged
- `Event` (MouseEventArgs): Browser mouse event details

**DragEventArgs:**
- `DraggedItem` (TabItem): The tab item that was dragged
- `DropIndex` (int): New position index after drop
- `Event` (MouseEventArgs): Browser mouse event details

#### Event Examples

**Detecting user interaction vs programmatic selection:**
```razor
@using Syncfusion.Blazor.Navigations

<div>Last action: @lastAction</div>

<SfTab @bind-SelectedItem="SelectedTab">
    <TabEvents Selected="OnSelected"></TabEvents>
    <TabItems>
        <TabItem Content="Tab 1 content">
            <ChildContent>
                <TabHeader Text="Tab 1"></TabHeader>
            </ChildContent>
        </TabItem>
        <TabItem Content="Tab 2 content">
            <ChildContent>
                <TabHeader Text="Tab 2"></TabHeader>
            </ChildContent>
        </TabItem>
    </TabItems>
</SfTab>

@code {
    private int SelectedTab = 0;
    private string lastAction = "None";

    private void OnSelected(SelectEventArgs args)
    {
        if (args.IsInteracted)
        {
            lastAction = $"User clicked Tab {args.Index + 1}";
        }
        else
        {
            lastAction = $"Tab {args.Index + 1} selected programmatically";
        }
    }
}
```

**Preventing tab selection with validation:**
```razor
<SfTab @ref="TabControl">
    <TabEvents Selecting="OnSelecting"></TabEvents>
    <TabItems>
        <TabItem Content="Form content">
            <ChildContent>
                <TabHeader Text="Form"></TabHeader>
            </ChildContent>
        </TabItem>
        <TabItem Content="Confirmation">
            <ChildContent>
                <TabHeader Text="Confirm"></TabHeader>
            </ChildContent>
        </TabItem>
    </TabItems>
</SfTab>

@code {
    private SfTab TabControl;

    private void OnSelecting(SelectingEventArgs args)
    {
        // Prevent moving to confirmation tab if form is invalid
        if (args.Index == 1 && !isFormValid)
        {
            args.Cancel = true;
        }
    }

    private bool isFormValid = false;
}
```

**Handling drag and drop events:**
```razor
<SfTab AllowDragAndDrop="true">
    <TabEvents OnDragStart="OnDragStart" Dragged="OnDragged"></TabEvents>
    <TabItems>
        <!-- Tab items -->
    </TabItems>
</SfTab>

@code {
    private void OnDragStart(DragStartEventArgs args)
    {
        Console.WriteLine($"Dragging tab: {args.DraggedItem.Header?.Text}");
    }

    private void OnDragged(DragEventArgs args)
    {
        Console.WriteLine($"Tab dropped at position: {args.DropIndex}");
    }
}
```

---

## Feature Implementations

This section provides focused examples for key features. For complete property examples, see the **Core API Reference** section above.

### Nested Tabs

```razor
<SfTab>
    <TabItems>
        <TabItem>
            <ChildContent>
                <TabHeader Text="USA"></TabHeader>
            </ChildContent>
            <ContentTemplate>
                <SfTab>
                    <TabItems>
                        <TabItem Content="New York description">
                            <ChildContent>
                                <TabHeader Text="New York"></TabHeader>
                            </ChildContent>
                        </TabItem>
                        <TabItem Content="Los Angeles description">
                            <ChildContent>
                                <TabHeader Text="Los Angeles"></TabHeader>
                            </ChildContent>
                        </TabItem>
                    </TabItems>
                </SfTab>
            </ContentTemplate>
        </TabItem>
        <TabItem>
            <ChildContent>
                <TabHeader Text="France"></TabHeader>
            </ChildContent>
            <ContentTemplate>
                <SfTab>
                    <TabItems>
                        <TabItem Content="Paris description">
                            <ChildContent>
                                <TabHeader Text="Paris"></TabHeader>
                            </ChildContent>
                        </TabItem>
                        <TabItem Content="Marseille description">
                            <ChildContent>
                                <TabHeader Text="Marseille"></TabHeader>
                            </ChildContent>
                        </TabItem>
                    </TabItems>
                </SfTab>
            </ContentTemplate>
        </TabItem>
    </TabItems>
</SfTab>
```

### Animation Configuration

```razor
@using Syncfusion.Blazor.Navigations

<SfTab>
    <TabAnimationSettings>
        <TabAnimationPrevious Effect="AnimationEffect.SlideLeftIn" Duration="500"></TabAnimationPrevious>
        <TabAnimationNext Effect="AnimationEffect.SlideRightIn" Duration="500"></TabAnimationNext>
    </TabAnimationSettings>
    <TabItems>
        <TabItem Content="Tab 1 content">
            <ChildContent>
                <TabHeader Text="Tab 1"></TabHeader>
            </ChildContent>
        </TabItem>
        <TabItem Content="Tab 2 content">
            <ChildContent>
                <TabHeader Text="Tab 2"></TabHeader>
            </ChildContent>
        </TabItem>
    </TabItems>
</SfTab>
```

Available animation effects: `SlideLeftIn`, `SlideRightIn`, `FadeIn`, `FadeOut`, `FadeZoomIn`, `FadeZoomOut`, `ZoomIn`, `ZoomOut`, `None`

### Dynamic Tab Management

```razor
@using Syncfusion.Blazor.Navigations
@using Syncfusion.Blazor.Buttons

<SfButton @onclick="AddItemClick">Add Tab</SfButton>
<SfButton @onclick="RemoveItemClick">Remove Tab</SfButton>

<SfTab @ref="Tab" ShowCloseButton="true">
    <TabItems>
        @foreach (var item in TabItems)
        {
            <TabItem>
                <ChildContent>
                    <TabHeader Text="@item.Title"></TabHeader>
                </ChildContent>
                <ContentTemplate>
                    <div>@item.Content</div>
                </ContentTemplate>
            </TabItem>
        }
    </TabItems>
</SfTab>

@code {
    private SfTab Tab;
    private List<TabItemData> TabItems = new List<TabItemData>();

    protected override void OnInitialized()
    {
        TabItems = new List<TabItemData>
        {
            new TabItemData { Title = "ASP.NET", Content = "ASP.NET is a web framework..." },
            new TabItemData { Title = "ASP.NET MVC", Content = "ASP.NET MVC implements the MVC pattern..." }
        };
    }

    private void AddItemClick()
    {
        TabItems.Add(new TabItemData { Title = "New Tab", Content = "New content..." });
    }

    private void RemoveItemClick()
    {
        if (TabItems.Count > 0) TabItems.RemoveAt(0);
    }

    public class TabItemData
    {
        public string Title { get; set; }
        public string Content { get; set; }
    }
}
```

---

## Documentation Reference Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Prerequisites and system requirements
- NuGet package installation (Syncfusion.Blazor.Navigations, Syncfusion.Blazor.Themes)
- Namespace imports in _Imports.razor
- Service registration in Program.cs
- Theme and script references in index.html
- Basic tab component setup with TabItems and TabHeader
- Rendering tab items with headers and content
- Two-way binding with SelectedItem
- ContentTemplate for rendering custom content

### Tab Selection and Navigation
📄 **Read:** [references/tab-selection-and-navigation.md](references/tab-selection-and-navigation.md)
- SelectedItem property binding and two-way binding patterns
- Select() method for synchronous tab selection
- SelectAsync() method for asynchronous tab selection
- Detecting user interaction vs programmatic selection
- Selected event handler implementation
- Selecting event handler for validation and prevention
- Managing and monitoring current tab selection state
- Event arguments (Index, PreviousIndex, IsInteracted)

### Tab Item Management
📄 **Read:** [references/tab-item-management.md](references/tab-item-management.md)
- Dynamic tab addition using AddTab() method
- Tab removal using RemoveTab() method
- Conditional rendering with foreach loops
- ShowCloseButton for user-driven tab removal
- Disabled property for preventing tab selection
- Visible property for conditional tab display
- TabIndex property for keyboard navigation
- Programmatic tab enabling/disabling with EnableTabAsync()

### Orientation and Header Placement
📄 **Read:** [references/orientation-and-header-placement.md](references/orientation-and-header-placement.md)
- HeaderPlacement property (Top, Bottom, Left, Right positions)
- Horizontal vs vertical tab layouts configuration
- OverflowMode configurations (Scrollable, Popup)
- ReorderActiveTab behavior in popup mode
- Navigation arrow scroll behavior
- ScrollStep customization for scroll distance
- Tab wrapping and overflow handling
- Responsive header placement strategies

### Content Rendering Modes
📄 **Read:** [references/content-render-modes.md](references/content-render-modes.md)
- LoadOn property options (Dynamic, Demand, Init)
- Dynamic rendering for performance optimization
- On-Demand rendering for state persistence
- Initial rendering for full component access
- ContentTemplate usage for complex content
- Performance comparison between rendering modes
- Memory and performance optimization strategies
- Content template conditional rendering

### Animations
📄 **Read:** [references/animations.md](references/animations.md)
- TabAnimationSettings configuration
- TabAnimationPrevious effect for backward navigation
- TabAnimationNext effect for forward navigation
- Available animation effects (SlideLeftIn, SlideRightIn, FadeIn, FadeOut, FadeZoomIn, FadeZoomOut, ZoomIn, ZoomOut, None)
- Duration configuration for animation timing
- Custom animation selection and timing
- Disabling animations for better performance
- Animation effect combinations

### Styling and Theming
📄 **Read:** [references/styling-and-theming.md](references/styling-and-theming.md)
- CssClass property for custom styling
- Header style classes (e-fill, e-background, e-accent)
- Icon positioning with IconPosition property (Left, Right, Top, Bottom)
- IconCss for tab header icons
- Tab header text styling and customization
- Theme integration and application
- Custom CSS class application to tab containers
- Responsive styling strategies

### Accessibility and Localization
📄 **Read:** [references/accessibility-and-localization.md](references/accessibility-and-localization.md)
- Keyboard navigation support (Tab, Shift+Tab, Arrow keys)
- TabIndex property for keyboard navigation order
- Screen reader accessibility support
- ARIA attributes for accessible components
- Locale property for localization support
- RTL (Right-to-Left) language support
- Multi-language tab content
- Blazor Localization integration
- Syncfusion localization resources

### Advanced Features and Customization
📄 **Read:** [references/advanced-features-and-customization.md](references/advanced-features-and-customization.md)
- AllowDragAndDrop for tab reordering functionality
- Drag-and-drop event handlers (OnDragStart, Dragged)
- State persistence with EnablePersistence property
- ID property requirement for persistence
- Browser cookie storage configuration
- ShouldReinitialize property for content re-initialization
- SwipeMode for touch and mouse gesture control
- HeaderTemplate and ContentTemplate for custom rendering
- Nested tab structures and hierarchical organization
- Multi-step wizard patterns with tabs
- Form validation across tab steps
- TabItem properties (Visible, Disabled, Content)

---

## Integration Checklist

Before finalizing your tab implementation:

- [ ] **Setup Complete**
  - [ ] `Syncfusion.Blazor.Navigations` NuGet package installed
  - [ ] `Syncfusion.Blazor.Themes` NuGet package installed
  - [ ] Syncfusion service registered in Program.cs
  - [ ] Namespaces imported in _Imports.razor
  - [ ] Theme stylesheet added to index.html
  - [ ] Script reference added to index.html

- [ ] **Component Configuration**
  - [ ] HeaderPlacement chosen (Top/Bottom/Left/Right)
  - [ ] OverflowMode selected (Scrollable/Popup)
  - [ ] Width and Height properties set if needed
  - [ ] LoadOn property configured for content rendering
  - [ ] CssClass applied for desired header style

- [ ] **Tab Items Configured**
  - [ ] Tab headers properly labeled
  - [ ] Content populated (either Content property or ContentTemplate)
  - [ ] Disabled and Visible states managed
  - [ ] TabIndex set for keyboard navigation if needed
  - [ ] Close buttons enabled if dynamic removal needed

- [ ] **Features Implemented**
  - [ ] Tab selection handled (SelectedItem or event handlers)
  - [ ] Event handlers implemented if needed (Selected, Selecting)
  - [ ] Methods called appropriately (AddTab, RemoveTab, SelectAsync)
  - [ ] Animation settings configured if desired
  - [ ] State persistence enabled if required (with ID property)
  - [ ] Drag-and-drop enabled if tab reordering needed

- [ ] **Testing and Validation**
  - [ ] Keyboard navigation tested (Tab, Shift+Tab, Arrow keys)
  - [ ] Accessibility verified with screen readers
  - [ ] Responsive behavior tested on different screen sizes
  - [ ] Event handling works correctly
  - [ ] Dynamic tab operations function properly
  - [ ] State persistence works across page refreshes
  - [ ] Custom styling applied correctly

- [ ] **Performance and Optimization**
  - [ ] LoadOn property optimized for content volume
  - [ ] ScrollStep adjusted for user experience
  - [ ] Animation effects appropriate for use case
  - [ ] Complex components lazy-loaded if needed

- [ ] **Documentation and Maintenance**
  - [ ] Component usage documented in project
  - [ ] Configuration parameters clearly marked
  - [ ] Event handlers properly commented
  - [ ] Future maintenance considerations noted

---

**Next Steps:**

1. Review the specific reference guide for your use case from the Documentation Reference Guide section
2. Choose your implementation pattern based on your requirements
3. Implement and test in your Blazor application
4. Customize styling, animations, and behavior as needed
5. Verify accessibility and responsiveness
6. Deploy with confidence

---

**Related Resources:**

- [Syncfusion Blazor Documentation](https://blazor.syncfusion.com/documentation/introduction/)
- [Syncfusion Blazor Tabs Component](https://www.syncfusion.com/blazor-components/blazor-tabs)
- [Syncfusion GitHub Examples](https://github.com/SyncfusionExamples/)
