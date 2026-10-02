---
name: syncfusion-javascript-tab
description: This skill enables creating and customizing Syncfusion TypeScript Tab components, including tab navigation, tab headers, styling, responsive layouts, dynamic content loading, animations, and multi-panel organization.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Navigation Components"
---

# Implementing Syncfusion TypeScript Tab Component

The Syncfusion TypeScript Tab is a powerful content container that displays multiple contents in a specific space, one at a time. It supports rendering from JSON items or HTML elements, with extensive customization, animation, accessibility, and responsive design capabilities.

## When to Use This Skill

- **Basic Tab Setup**: Create simple tabbed interfaces with headers and content
- **Tab Selection & Navigation**: Handle programmatic and user-initiated tab selection
- **Customization**: Style headers, content, icons, and selected states
- **Responsive Design**: Implement adaptive tabs with scrollable or popup modes
- **Dynamic Content**: Load tab items dynamically or through data sources
- **Advanced Features**: Drag-and-drop reordering, nested tabs, collapsible tabs, wizards
- **User Experience**: Add animations, tooltips, keyboard navigation, accessibility
- **State Management**: Persist tab state across sessions

## Key Features

1. **Rendering**: Create tabs from JSON items collection or HTML elements
2. **Adaptive**: Responsive rendering with scrollable tabs and popup menus
3. **Customization**: Header icons, orientation, styling, and theming support
4. **Animation**: Built-in animation effects for tab transitions with `animation` property
5. **Accessibility**: WCAG compliance with keyboard navigation and ARIA attributes
6. **Drag & Drop**: Reorder tabs and transfer items between interfaces with `allowDragAndDrop`
7. **Dynamic Loading**: Control content loading with `loadOn` property (Demand, Dynamic, Init)
8. **State Persistence**: Restore selected tab state across user sessions using `enablePersistence`
9. **Security**: Built-in HTML sanitization with `enableHtmlSanitizer` to prevent XSS attacks
10. **Swipe Gestures**: Tab navigation via touch/mouse swipe with `swipeMode` property

## Complete Enumeration Reference

### HeaderPosition - Tab Header Placement

Controls where tab headers are positioned relative to content.

| Value | Placement | Use Case |
|-------|-----------|----------|
| `'Top'` | Headers above content (default) | Dashboard, forms, standard tabs |
| `'Bottom'` | Headers below content | Document viewers, bottom navigation |
| `'Left'` | Headers on left side | Admin panels, sidebar navigation |
| `'Right'` | Headers on right side | Specialized layouts |

```typescript
new Tab({ headerPlacement: 'Top', items: [...] });     // Default
new Tab({ headerPlacement: 'Left', items: [...] });    // Sidebar
new Tab({ headerPlacement: 'Bottom', items: [...] });  // Bottom
new Tab({ headerPlacement: 'Right', items: [...] });   // Right side
```

### HeightStyles - Content Height Adjust Modes

Controls how tab content height is calculated.

| Value | Behavior |  Usage |
|-------|----------|--------|
| `'None'` | Use explicit `height` property | Fixed containers |
| `'Auto'` | All tabs match tallest content | Equalizing heights |
| `'Content'` | Each tab matches its own content (default) | Variable-height content |
| `'Fill'` | Content fills parent container | Responsive fills |

```typescript
new Tab({ height: '400px', heightAdjustMode: 'None', items: [...] });
new Tab({ heightAdjustMode: 'Auto', items: [...] });
new Tab({ heightAdjustMode: 'Content', items: [...] });
new Tab({ height: '100%', heightAdjustMode: 'Fill', items: [...] });
```

### ContentLoad - Content Rendering Modes

Controls when tab content is loaded into the DOM.

| Value | Loading | DOM | When Used |
|-------|---------|-----|-----------|
| `'Demand'` (default) | On first selection | Persists | Many tabs, static content |
| `'Dynamic'` | On each selection | Only selected | Dynamic/live data |
| `'Init'` | All upfront | Always in DOM | Few tabs, small content |

```typescript
new Tab({ loadOn: 'Demand', items: [...] });    // Lazy load (default)
new Tab({ loadOn: 'Dynamic', items: [...] });   // Reload each time
new Tab({ loadOn: 'Init', items: [...] });      // Load all at init
```

### TabSwipeMode - Swipe Gesture Control

Controls which input methods trigger tab swiping.

| Value | Touch | Mouse | Desktop | Mobile |
|-------|-------|-------|---------|--------|
| `'Both'` (default) | ✅ | ✅ | All devices | All devices |
| `'Touch'` | ✅ | ❌ | Desktop only | Mobile users |
| `'Mouse'` | ❌ | ✅ | Desktop users | Mouse input only |
| `'None'` | ❌ | ❌ | Swiping disabled | Swiping disabled |

```typescript
new Tab({ swipeMode: 'Both', items: [...] });      // Both touch and mouse
new Tab({ swipeMode: 'Touch', items: [...] });     // Mobile touch only
new Tab({ swipeMode: 'Mouse', items: [...] });     // Desktop mouse only
new Tab({ swipeMode: 'None', items: [...] });      // Disabled swiping
```

---

### Core Documentation (Start Here)

1. **[Getting Started](references/getting-started.md)** ⭐ START HERE
   - Installation and setup
   - First Tab component
   - HTML structure and imports

2. **[Tab Structure and Content](references/tab-structure-and-content.md)**
   - Tab item structure
   - Headers and content
   - Tab selection

### API Reference & Properties

3. **[Complete API Properties Reference](references/api-properties-reference.md)** 📚 COMPREHENSIVE
   - All 24+ properties documented
   - Usage examples for each property
   - Property combinations and recommendations
   - Core, rendering, interaction, animation properties

4. **[Event Handling Reference](references/event-handling-reference.md)** 📚 COMPREHENSIVE
   - All 11 events documented
   - Event arguments (SelectEventArgs, SelectingEventArgs, DragEventArgs, etc.)
   - Event lifecycle and timing
   - Practical event patterns

5. **[Complete Methods Reference](references/methods-reference.md)** 📚 COMPREHENSIVE
   - All 18 methods documented with signatures and parameters
   - Tab management methods (addTab, removeTab, select)
   - Visibility and state control (hideTab, enableTab, disable)
   - Event management (addEventListener, removeEventListener)
   - Component lifecycle (destroy, refresh, refreshActiveTab)
   - Utility methods (getItemIndex, getRootElement, appendTo, dataBind)
   - Practical code examples for each method
   - Method interaction patterns and best practices

### Customization & Styling

6. **[Customization and Styling](references/customization-and-styling.md)**
   - CSS structure
   - Header and content styling
   - `showCloseButton` property
   - Built-in themes
   - Custom styling examples

### Content & Data

7. **[Data Binding and Dynamic Content](references/data-binding.md)**
   - Loading methods (JSON, AJAX, DataManager)
   - `loadOn` property (Demand, Dynamic, Init)
   - `addTab()` and `removeTab()` methods
   - POST requests and API integration
   - Content rendering modes

### Layout & Responsiveness

8. **[Content Orientation and Header Placement](references/content-orientation.md)**
   - `headerPlacement` (Top, Bottom, Left, Right)
   - Horizontal vs vertical layouts
   - Responsive design patterns
   - Sidebar navigation implementation

9. **[Responsive and Adaptive Modes](references/responsive-adaptive-modes.md)**
   - Scrollable mode
   - Popup/dropdown mode
   - Multi-row mode
   - `overflowMode` property

### Advanced & Features

10. **[Advanced Features](references/advanced-features.md)**
    - Drag and drop (`allowDragAndDrop`, `dragArea`)
    - `reorderActiveTab` property
    - Nested and collapsible tabs
    - Tab-based wizards
    - Icon and tooltip integration

11. **[Animation and Transitions](references/animation-effects.md)**
    - `animation` property (TabAnimationSettingsModel)
    - Effects: SlideLeftIn, SlideRightIn, FadeIn, ZoomIn, etc.
    - `swipeMode` property (Both, Touch, Mouse, None)
    - Custom animation timing

12. **[State Persistence](references/state-persistence.md)**
    - `enablePersistence` property
    - localStorage-based persistence
    - Multi-tab forms and dashboards
    - Advanced persistence patterns

### Accessibility & Internationalization

13. **[Accessibility and Localization](references/accessibility-and-localization.md)**
    - WCAG compliance and ARIA
    - Keyboard navigation
    - `enableRtl` property (RTL support)
    - `locale` property (i18n)

### Security

14. **[Security and HTML Sanitization](references/security-html-sanitization.md)** 🔒 IMPORTANT
    - `enableHtmlSanitizer` property
    - XSS prevention
    - User content protection
    - Security best practices

### Troubleshooting

15. **[Edge Cases and Troubleshooting](references/edge-cases-and-troubleshooting.md)**
    - Height and scroll management
    - Browser compatibility

---

## Quick Start

### Basic Tab with JSON Items

```typescript
import { Tab } from '@syncfusion/ej2-navigations';

let tabObj: Tab = new Tab({
    items: [
        {
            header: { 'text': 'Twitter' },
            content: 'Twitter is an online social networking service...'
        },
        {
            header: { 'text': 'Facebook' },
            content: 'Facebook is an online social networking service...'
        },
        {
            header: { 'text': 'WhatsApp' },
            content: 'WhatsApp Messenger is a proprietary cross-platform...'
        }
    ]
});

tabObj.appendTo('#element');
```

### HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Tab Example</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
<body>
    <div id="element"></div>
</body>
</html>
```

### CSS Setup

```css
@import '../../node_modules/@syncfusion/ej2-base/styles/fluent2.css';
@import '../../node_modules/@syncfusion/ej2-buttons/styles/fluent2.css';
@import '../../node_modules/@syncfusion/ej2-popups/styles/fluent2.css';
@import '../../node_modules/@syncfusion/ej2-navigations/styles/fluent2.css';
```

## Feature-Specific Usage Scenarios

### Tab Content Height Customization

Use the `heightAdjustMode` property to control how tab content height is adjusted:

```typescript
let tabObj: Tab = new Tab({
    heightAdjustMode: 'Auto',  // 'None', 'Auto', 'Content', 'Fill'
    height: '400px',  // Set container height when using 'None' or 'Auto'
    items: [
        { header: { 'text': 'Tab 1' }, content: 'Short content' },
        { header: { 'text': 'Tab 2' }, content: 'Much longer content with more text...' },
        { header: { 'text': 'Tab 3' }, content: 'Another tab with varying content length' }
    ]
});
tabObj.appendTo('#element');
```

**Height Modes:**
- **None**: Content height matches Tab container height (requires explicit height)
- **Auto**: All tabs adjust to match the tallest content
- **Content**: Each tab adjusts to its own content height (default)
- **Fill**: Tab content fills the parent element completely

### Show Close Button on Tabs

Enable users to close individual tabs by clicking a close button:

```typescript
let tabObj: Tab = new Tab({
    showCloseButton: true,
    items: [
        { header: { 'text': 'Home' }, content: 'Home content...' },
        { header: { 'text': 'Editor' }, content: 'Editor content...' },
        { header: { 'text': 'Settings' }, content: 'Settings content...' }
    ]
});
tabObj.appendTo('#element');

// Optionally handle close button clicks
tabObj.element.addEventListener('close', (e: any) => {
    console.log(`Closed tab at index: ${e.index}`);
});
```

### Reorder Active Tab in Popup Mode

Control how the active tab behaves when tabs overflow into a popup menu:

```typescript
let tabObj: Tab = new Tab({
    overflowMode: 'Popup',  // Enable popup mode for overflow tabs
    reorderActiveTab: false,  // Don't reorder active tab in popup (keep it highlighted)
    heightAdjustMode: 'Auto',
    items: [
        { header: { 'text': 'India' }, content: 'India content...' },
        { header: { 'text': 'Canada' }, content: 'Canada content...' },
        { header: { 'text': 'Australia' }, content: 'Australia content...' },
        // ... many more tabs that trigger popup mode
    ]
});
tabObj.appendTo('#element');
```

When `reorderActiveTab` is `true` (default), clicking a tab in the popup moves it to the main view. When `false`, the tab remains highlighted in the popup without being reordered to the main view.

### Load Tab Items Dynamically

Add tabs programmatically in response to user actions:

```typescript
let tabObj: Tab = new Tab({
    items: [
        { header: { 'text': 'Home' }, content: 'Home content' }
    ]
});
tabObj.appendTo('#element');

// Add new tab dynamically
document.getElementById('addTabBtn')?.addEventListener('click', () => {
    let newTabCount = tabObj.items.length;
    let newTab = {
        header: { 'text': `Tab ${newTabCount}` },
        content: `Content for tab ${newTabCount}`
    };
    tabObj.addTab([newTab]);  // Add at end
    // Or insert at specific position: tabObj.addTab([newTab], 1);
});

// Remove tab by index
document.getElementById('removeTabBtn')?.addEventListener('click', () => {
    if (tabObj.items.length > 1) {
        tabObj.removeTab(tabObj.items.length - 1);  // Remove last tab
    }
});
```

### State Persistence Across Page Refreshes

Automatically save and restore the selected tab:

```typescript
let tabObj: Tab = new Tab({
    enablePersistence: true,  // Enable localStorage-based persistence
    items: [
        { header: { 'text': 'Dashboard' }, content: 'Dashboard...' },
        { header: { 'text': 'Analytics' }, content: 'Analytics...' },
        { header: { 'text': 'Settings' }, content: 'Settings...' }
    ]
});
tabObj.appendTo('#element');

// When user returns to page, the previously selected tab is automatically restored
```

### Customize Selected Tab Appearance

Use CSS classes to override default styling for selected tabs:

```typescript
let tabObj: Tab = new Tab({
    cssClass: 'e-tab-custom-style',  // Add custom CSS class
    items: [...]
});
tabObj.appendTo('#element');
```

Then define custom CSS:

```css
.e-tab.e-tab-custom-style .e-tab-header .e-toolbar-item.e-active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-bottom: 3px solid #667eea;
}

.e-tab.e-tab-custom-style .e-tab-header .e-toolbar-item.e-active .e-tab-text {
    font-weight: 600;
    color: white;
}
```

### Load Content Through POST Requests

Fetch tab content from a server:

```typescript
import { Tab } from '@syncfusion/ej2-navigations';
import { Ajax } from '@syncfusion/ej2-base';

let ajax: Ajax = new Ajax('./api/tab-content', 'GET', true);

ajax.onSuccess = (data: string): void => {
    let tabObj: Tab = new Tab({
        items: [
            { header: { 'text': 'Home' }, content: 'Home content' },
            { header: { 'text': 'Remote Content' }, content: data }
        ]
    });
    tabObj.appendTo('#element');
};

ajax.send();

// Or using Fetch API
async function loadTabContent() {
    try {
        let response = await fetch('api/tab-data', { method: 'POST' });
        let data = await response.json();
        
        let tabObj = new Tab({
            items: data.tabs  // Server returns array of tab items
        });
        tabObj.appendTo('#element');
    } catch (error) {
        console.error('Failed to load tabs:', error);
    }
}

loadTabContent();
```

### Drag and Drop Between Tabs or External Sources

Enable users to move tab items within the same tab or to external components:

```typescript
let tabObj: Tab = new Tab({
    allowDragAndDrop: true,  // Enable drag-drop
    dragArea: '#dragContainer',  // Restrict drag area
    items: [...],
    dragged: (args) => {
        console.log(`Item moved from ${args.draggedIndex} to ${args.droppedIndex}`);
    }
});
tabObj.appendTo('#element');

// Transfer tabs between two Tab instances
let sourceTab: Tab = new Tab({
    allowDragAndDrop: true,
    dragArea: '#container',
    items: [{ header: { 'text': 'Source 1' }, content: 'Can be moved' }]
});
sourceTab.appendTo('#sourceTab');

let destTab: Tab = new Tab({
    allowDragAndDrop: true,
    dragArea: '#container',
    items: [{ header: { 'text': 'Dest 1' }, content: 'Receives items' }]
});
destTab.appendTo('#destTab');
```

### Content Rendering Modes

Control how and when tab content is loaded:

```typescript
// Mode 1: On-Demand (Lazy Loading) - Default
let tabObj: Tab = new Tab({
    // Content loaded only when tab is selected
    // Content persists in DOM once loaded
    items: [
        { header: { 'text': 'Tab 1' }, content: 'Content loaded on first select' }
    ]
});
tabObj.appendTo('#element');

// Mode 2: Dynamic - Only selected content in DOM
let dynamicTab: Tab = new Tab({
    loadOn: 'Dynamic',  // Content reloaded each time tab is selected
    items: []
});
dynamicTab.appendTo('#element');

// Mode 3: Initial - All content loaded upfront
let initialTab: Tab = new Tab({
    loadOn: 'Init',  // All tabs rendered on initialization
    items: []
});
initialTab.appendTo('#element');
```

## Common Patterns

### Pattern 1: Programmatic Tab Selection

```typescript
// Select a tab by index
tabObj.select(1);  // Select second tab

// Get currently selected tab index
let activeIndex = tabObj.selectedItem;

// Determine if selection was user interaction or programmatic
tabObj.selecting = (args) => {
    if (args.isInteracted) {
        console.log('User clicked tab');
    } else {
        console.log('Tab selected programmatically');
    }
};
```

### Pattern 2: Dynamic Tab Addition

```typescript
// Add new tab item dynamically
tabObj.addTab([
    {
        header: { 'text': 'New Tab' },
        content: 'New content here'
    }
], 2); // Insert at index 2
```

### Pattern 3: Responsive Tabs with Scrolling

```typescript
let tabObj: Tab = new Tab({
    items: [...], // your items
    heightAdjustMode: 'Auto',
    overflowMode: 'Scrollable'  // Enable scrollable mode
});
```

### Pattern 4: Tab with Icons

```typescript
let tabObj: Tab = new Tab({
    items: [
        {
            header: { 
                'text': 'Settings',
                'iconCss': 'e-icon-settings'  // Add icon class
            },
            content: 'Settings content...'
        }
    ]
});
```

## Key Props and Configuration

| Property | Type | Purpose | Common Values |
|----------|------|---------|----------------|
| `items` | Array | Tab items collection | Array of item objects |
| `selectedItem` | number | Active tab index | 0, 1, 2, ... |
| `heightAdjustMode` | string | Auto-adjust height | 'Auto', 'Content', 'Scroll' |
| `overflowMode` | string | Handle overflow tabs | 'Scrollable', 'Popup', 'MultiRow' |
| `animation` | object | Animation settings | { previous, next } |
| `headerPlacement` | string | Header placement | 'Top', 'Bottom', 'Left', 'Right' |
| `enableRtl` | boolean | RTL support | true, false |
| `allowDragAndDrop` | boolean | Enable drag-drop | true, false |
| `enablePersistence` | boolean | State persistence | true, false |

## Common Use Cases

1. **Multi-Panel Forms**: Organize form fields across multiple tabs with validation
2. **Documentation Sites**: Create tabbed code examples (TypeScript, JavaScript, HTML)
3. **Dashboard Layouts**: Organize dashboard widgets in tab sections
4. **Step-by-Step Wizards**: Create sequential workflows using tabs
5. **Content Organization**: Categorize and display large datasets
6. **Feature Toggles**: Show/hide related features in tab panels
7. **Admin Interfaces**: Organize settings and configuration options
8. **Mobile Navigation**: Responsive tab-based navigation for small screens

---

**Next Steps:**
- Read the appropriate reference file based on your use case
- Check the quick start example for basic setup
- Review common patterns for your specific scenario
- Refer to edge cases guide for troubleshooting
