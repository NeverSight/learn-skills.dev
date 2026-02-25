---
name: textual-widget-development
description: |
  Designs and implements custom Textual widgets with composition, styling, and lifecycle management. Use when creating reusable widget components, composing widgets from built-in components, implementing widget lifecycle (on_mount, on_unmount), handling widget state, and testing widgets. Covers custom widgets extending Static, Container, and building complex widget hierarchies.
allowed-tools: Read, Write, Edit, Bash
---

# Textual Widget Development

## Purpose
Build reusable, composable Textual widgets that follow functional principles, proper lifecycle management, and type safety. Widgets are the fundamental building blocks of Textual applications.

## Quick Start

```python
from textual.app import ComposeResult
from textual.widgets import Static, Container
from textual.containers import Vertical

class SimpleWidget(Static):
    """A simple reusable widget."""

    DEFAULT_CSS = """
    SimpleWidget {
        height: auto;
        border: solid $primary;
        padding: 1;
    }
    """

    def __init__(self, title: str, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._title = title

    def render(self) -> str:
        """Render widget content."""
        return f"Title: {self._title}"

# Use in app:
class MyApp(App):
    def compose(self) -> ComposeResult:
        yield SimpleWidget("Hello")
```

## Instructions

### Step 1: Choose Widget Base Class

Select appropriate base class based on widget purpose:

```python
from textual.widgets import Static, Container, Input, Button
from textual.containers import Vertical, Horizontal, Container as GenericContainer

# For custom content/display - Simple widgets
class StatusWidget(Static):
    """Displays status information."""
    pass

# For layout/composition - Container widgets
class DashboardWidget(Container):
    """Composes multiple child widgets."""
    pass

# Built-in widgets (ready to use)
# - Static: Display text/rich content
# - Input: Text input field
# - Button: Clickable button
# - Label: Static label
# - Select: Dropdown selector
# - DataTable: Tabular data
# - Tree: Hierarchical data
```

**Guidelines:**
- Use `Static` for display-only content
- Use `Container` when you need to compose child widgets
- Use built-in widgets first before creating custom ones
- Create custom widgets only when built-in options don't fit

### Step 2: Define Widget Initialization and Configuration

Implement `__init__` with proper type hints and parent class initialization:

```python
from typing import ClassVar
from textual.app import ComposeResult
from textual.widgets import Static

class ConfigurableWidget(Static):
    """Widget with configurable parameters."""

    DEFAULT_CSS = """
    ConfigurableWidget {
        height: auto;
        border: solid $primary;
        padding: 1;
    }

    ConfigurableWidget .header {
        background: $boost;
        text-style: bold;
    }
    """

    # Class constants
    BORDER_COLOR: ClassVar[str] = "$primary"

    def __init__(
        self,
        title: str,
        content: str = "",
        *,
        name: str | None = None,
        id: str | None = None,  # noqa: A002
        classes: str | None = None,
        variant: str = "default",
    ) -> None:
        """Initialize widget.

        Args:
            title: Widget title.
            content: Initial content.
            name: Widget name.
            id: Widget ID for querying.
            classes: CSS classes to apply.
            variant: Visual variant (default, compact, etc).

        Always pass **kwargs to parent:
            super().__init__(name=name, id=id, classes=classes)
        """
        super().__init__(name=name, id=id, classes=classes)
        self._title = title
        self._content = content
        self._variant = variant
```

**Important Rules:**
- Always call `super().__init__()` with name, id, classes
- Store configuration in instance variables (prefix with `_`)
- Use type hints for all parameters
- Document all parameters with docstrings
- Use keyword-only arguments (after `*`) for optional parameters

### Step 3: Implement Widget Composition

For complex widgets that contain child widgets:

```python
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Button, Label

class CompositeWidget(Vertical):
    """Widget that composes multiple child widgets."""

    DEFAULT_CSS = """
    CompositeWidget {
        height: auto;
        border: solid $primary;
    }

    CompositeWidget .header {
        height: 3;
        background: $boost;
        text-style: bold;
    }

    CompositeWidget .content {
        height: 1fr;
        overflow: auto;
    }

    CompositeWidget .footer {
        height: auto;
        border-top: solid $primary;
    }
    """

    def __init__(self, title: str, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._title = title
        self._items: list[str] = []

    def compose(self) -> ComposeResult:
        """Compose child widgets.

        Yields:
            Child widgets in order they should appear.
        """
        # Header
        yield Static(f"Title: {self._title}", classes="header")

        # Content area with items
        yield Vertical(
            Static(
                "Content area" if not self._items else "\n".join(self._items),
                id="content-area",
            ),
            classes="content",
        )

        # Footer with buttons
        yield Horizontal(
            Button("Add", id="btn-add", variant="primary"),
            Button("Remove", id="btn-remove"),
            classes="footer",
        )

    async def on_mount(self) -> None:
        """Initialize after composition."""
        # Can now query child widgets
        content = self.query_one("#content-area", Static)
        content.update("Initialized")

    async def add_item(self, item: str) -> None:
        """Add item to widget."""
        self._items.append(item)
        content = self.query_one("#content-area", Static)
        content.update("\n".join(self._items))
```

**Composition Pattern:**
- Override `compose()` to yield child widgets
- Use containers (Vertical, Horizontal) for layout
- Use `on_mount()` after children are mounted
- Query children by ID using `self.query_one()`

### Step 4: Implement Widget Rendering

For display widgets using `render()`:

```python
from rich.console import Console
from rich.table import Table
from rich.text import Text
from textual.widgets import Static

class RichWidget(Static):
    """Widget that renders Rich objects."""

    def __init__(self, data: dict, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._data = data

    def render(self) -> str | Text | Table:
        """Render widget content as Rich object.

        Returns:
            str, Text, or Rich-renderable object.
            Textual converts to displayable content.
        """
        # Simple text
        return f"Data: {self._data}"

        # Rich Text with styling
        text = Text()
        text.append("Status: ", style="bold")
        text.append(self._data.get("status", "unknown"), style="green")
        return text

        # Rich Table
        table = Table(title="Data")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="magenta")
        for key, value in self._data.items():
            table.add_row(key, str(value))
        return table
```

**Rendering Methods:**
1. `render()` - Return displayable content
2. `update(content)` - Update rendered content
3. `refresh()` - Force re-render

### Step 5: Add Widget Lifecycle Methods

Implement lifecycle hooks for initialization and cleanup:

```python
class LifecycleWidget(Static):
    """Widget with full lifecycle implementation."""

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._initialized = False

    async def on_mount(self) -> None:
        """Called when widget is mounted to DOM.

        Use for:
        - Initializing state
        - Starting background tasks
        - Loading data
        - Querying sibling widgets
        """
        self._initialized = True
        self.update("Widget mounted and ready")

        # Start background task
        self.app.run_worker(self._background_work())

    async def _background_work(self) -> None:
        """Background async work."""
        import asyncio
        while self._initialized:
            await asyncio.sleep(1)
            self.refresh()

    def on_unmount(self) -> None:
        """Called when widget is removed from DOM.

        Use for:
        - Cleanup
        - Stopping background tasks
        - Closing connections
        """
        self._initialized = False
```

**Lifecycle Events:**
- `on_mount()` - After widget mounted and can query children
- `on_unmount()` - After widget removed, before destruction
- `on_focus()` - Widget gained focus
- `on_blur()` - Widget lost focus

### Step 6: Implement Widget Actions and Messages

Add interactivity through actions and custom messages:

```python
from textual.message import Message
from textual import on
from textual.widgets import Button

class ItemWidget(Static):
    """Widget that posts custom messages."""

    class ItemClicked(Message):
        """Posted when item is clicked."""

        def __init__(self, item_id: str) -> None:
            super().__init__()
            self.item_id = item_id

    def __init__(self, item_id: str, label: str, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._item_id = item_id
        self._label = label

    def render(self) -> str:
        return f"[{self._item_id}] {self._label}"

    def on_click(self) -> None:
        """Handle click event."""
        # Post message that parent can handle
        self.post_message(self.ItemClicked(self._item_id))

# Parent widget handling custom messages
class ItemList(Vertical):
    """Widget that handles ItemWidget messages."""

    @on(ItemWidget.ItemClicked)
    async def on_item_clicked(self, message: ItemWidget.ItemClicked) -> None:
        """Handle item click message."""
        print(f"Item clicked: {message.item_id}")
        self.notify(f"Selected: {message.item_id}")
```

**Message Pattern:**
1. Define custom Message subclass
2. Post message with `self.post_message()`
3. Parent handles with `@on(MessageType)` decorator
4. Messages bubble up the widget tree

### Step 7: Add CSS Styling

Define DEFAULT_CSS for widget styling:

```python
class StyledWidget(Static):
    """Widget with comprehensive CSS styling."""

    DEFAULT_CSS = """
    StyledWidget {
        width: 100%;
        height: auto;
        border: solid $primary;
        padding: 1 2;
        background: $surface;
    }

    StyledWidget .header {
        width: 100%;
        height: 3;
        background: $boost;
        text-style: bold;
        content-align: center middle;
        color: $text;
    }

    StyledWidget .content {
        width: 1fr;
        height: 1fr;
        padding: 1;
        overflow: auto;
    }

    StyledWidget .status-active {
        color: $success;
        text-style: bold;
    }

    StyledWidget .status-inactive {
        color: $error;
        text-style: dim;
    }

    StyledWidget:focus {
        border: double $primary;
    }

    StyledWidget:disabled {
        opacity: 0.5;
    }
    """

    def render(self) -> str:
        return "Styled Widget"
```

**CSS Best Practices:**
- Use CSS variables ($primary, $success, etc.) for consistency
- Keep DEFAULT_CSS in the widget file
- Use classes for variants
- Use pseudo-classes (:focus, :hover, :disabled)
- Use width/height in fr (fraction) or auto

## Examples

### Basic Widget Examples

See above instructions for two fundamental widget examples:
1. Custom Status Display Widget (rendering with Rich)
2. Reusable Data Table Widget (composition pattern)

**For advanced widget patterns**, see [references/advanced-patterns.md](references/advanced-patterns.md):
- Complex container widgets with multiple child types
- Dynamic widget mounting/unmounting
- Lazy loading patterns
- Advanced reactive patterns with watchers
- Custom message bubbling
- Performance optimization (virtual scrolling, debouncing)
- Comprehensive testing patterns

## Requirements
- Textual >= 0.45.0
- Python 3.9+ for type hints
- Rich (installed with Textual for rendering)

## Common Patterns

### Creating Reusable Containers

```python
def create_section(title: str, content: Static) -> Container:
    """Factory function for creating sections."""
    return Container(
        Static(title, classes="section-header"),
        content,
        classes="section",
    )
```

### Lazy Widget Mounting

```python
async def lazy_mount_children(self) -> None:
    """Mount child widgets gradually."""
    for i, item in enumerate(self._items):
        await container.mount(self._create_item_widget(item))
        if i % 10 == 0:
            await asyncio.sleep(0)  # Yield to event loop
```

## See Also
- [textual-app-lifecycle.md](../textual-app-lifecycle) - App initialization and lifecycle
- [textual-event-messages.md](../textual-event-messages) - Event and message handling
- [textual-layout-styling.md](../textual-layout-styling) - CSS styling and layout
