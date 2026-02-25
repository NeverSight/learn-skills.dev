---
name: textual-event-messages
description: |
  Handles keyboard, mouse, and custom events in Textual applications using messages and handlers. Use when implementing keyboard bindings, custom message passing, event bubbling, action dispatch, and inter-widget communication. Covers event handling patterns, message definitions, and routing.
allowed-tools: Read, Write, Edit, Bash
---

# Textual Event and Message Handling

## Purpose
Implement robust event handling and inter-widget communication in Textual using messages, keyboard bindings, and action dispatch. Messages enable loose coupling between components.

## Quick Start

```python
from textual.message import Message
from textual.app import App, ComposeResult
from textual.widgets import Button, Static
from textual import on

class ItemWidget(Static):
    """Widget that emits custom messages."""

    class ItemSelected(Message):
        """Posted when item is selected."""
        def __init__(self, item_id: str) -> None:
            super().__init__()
            self.item_id = item_id

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield ItemWidget()

    @on(ItemWidget.ItemSelected)
    def on_item_selected(self, message: ItemWidget.ItemSelected) -> None:
        """Handle item selection."""
        self.notify(f"Selected: {message.item_id}")
```

## Instructions

### Step 1: Define Custom Messages

Create message classes to communicate between widgets:

```python
from textual.message import Message
from dataclasses import dataclass

# Simple message without data
class DataRefreshed(Message):
    """Posted when data is refreshed."""
    pass

# Message with data
class ItemSelected(Message):
    """Posted when item is selected."""

    def __init__(self, item_id: str, index: int) -> None:
        """Initialize message.

        Args:
            item_id: Selected item ID.
            index: Index in list.
        """
        super().__init__()
        self.item_id = item_id
        self.index = index

# Message with complex data
@dataclass(frozen=True)
class SearchResult:
    """Result of search operation."""
    query: str
    items: list[str]
    total_count: int

class SearchCompleted(Message):
    """Posted when search completes."""

    def __init__(self, result: SearchResult) -> None:
        """Initialize with search result."""
        super().__init__()
        self.result = result
```

**Message Conventions:**
- Subclass `Message`
- Define immutable data in `__init__`
- Use descriptive PascalCase names
- Document the message purpose in docstring
- Use `frozen=True` for dataclasses to ensure immutability

### Step 2: Post and Handle Messages

Post messages from widgets and handle in parents:

```python
from textual import on
from textual.widgets import Static, ListView, ListItem
from textual.app import ComposeResult

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
        """Post message when clicked."""
        self.post_message(self.ItemClicked(self._item_id))

class ItemListWidget(Static):
    """Parent widget that handles item messages."""

    def compose(self) -> ComposeResult:
        yield ListView(id="item-list")

    async def on_mount(self) -> None:
        """Create items."""
        list_view = self.query_one("#item-list", ListView)
        for i, item_id in enumerate(["a", "b", "c"]):
            await list_view.append(ListItem(
                ItemWidget(item_id, f"Item {item_id}")
            ))

    @on(ItemWidget.ItemClicked)
    async def on_item_clicked(self, message: ItemWidget.ItemClicked) -> None:
        """Handle item click - called automatically."""
        self.notify(f"Clicked: {message.item_id}")

# Alternative handler without @on decorator
class AltListWidget(Static):
    """Using on_* method naming convention."""

    def on_item_widget_item_clicked(self, message: ItemWidget.ItemClicked) -> None:
        """Auto-routed handler.

        Convention: on_{widget_class_snake_case}_{message_class_snake_case}
        """
        self.notify(f"Clicked: {message.item_id}")
```

**Message Routing:**
1. Widget posts message: `self.post_message(MyMessage())`
2. Message bubbles up to parent widgets
3. Parent handles with `@on(MessageType)` or `on_*` method
4. First handler to handle the message stops propagation (can call `event.stop()`)

### Step 3: Implement Keyboard Event Handlers

Handle keyboard input directly:

```python
from textual.events import Key, Paste
from textual.widgets import Static

class KeyboardWidget(Static):
    """Widget handling keyboard events."""

    def on_key(self, event: Key) -> None:
        """Called when any key is pressed.

        Args:
            event: Key event with key name.
        """
        key_name = event.key
        # Common keys: "up", "down", "left", "right", "enter", "escape"
        # Letters: "a", "b", "ctrl+a", "shift+a"

        if key_name == "enter":
            self.handle_enter()
        elif key_name == "escape":
            self.handle_escape()
        elif key_name == "ctrl+c":
            self.app.exit()

    def handle_enter(self) -> None:
        """Handle Enter key."""
        self.update("Enter pressed")

    def handle_escape(self) -> None:
        """Handle Escape key."""
        self.update("Escape pressed")

    def on_paste(self, event: Paste) -> None:
        """Called when text is pasted.

        Args:
            event: Paste event with text.
        """
        self.update(f"Pasted: {event.text}")
```

**Key Event Handling:**
- `on_key()` called for keyboard events
- Common keys: arrow keys, enter, escape, tab, delete
- Modifier keys: "ctrl+key", "shift+key", "alt+key"
- Special: "home", "end", "page_up", "page_down", "F1"-"F12"

### Step 4: Add Keyboard Bindings and Actions

Bindings provide discoverable keyboard shortcuts tied to actions:

```python
from textual.app import App, ComposeResult
from textual.binding import Binding
from typing import ClassVar

class MyApp(App):
    """App with keyboard bindings."""

    BINDINGS: ClassVar[list[Binding]] = [
        # (key, action, description, show, priority)
        Binding("q", "quit", "Quit", show=True, priority=True),
        Binding("ctrl+c", "quit", "Quit", show=False, priority=True),
        Binding("r", "refresh", "Refresh"),
        Binding("n", "new_item", "New"),
        Binding("?", "show_help", "Help"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Content")
        yield Footer()  # Shows bindings

    def action_refresh(self) -> None:
        """Action handler for 'refresh' binding."""
        self.notify("Refreshed")

    def action_new_item(self) -> None:
        """Action handler for 'new_item' binding."""
        self.notify("Creating new item")

    async def action_show_help(self) -> None:
        """Action handlers can be async."""
        # Show help dialog
        pass
```

**Binding Conventions:**
- Binding key to action method name
- Action method: `action_{action_name}`
- Action methods can be sync or async
- Bindings shown in Footer if `show=True`
- `priority=True` for high-priority bindings (quit)
- Bindings override key event handlers when matched

### Step 5: Handle Mouse Events

React to mouse clicks and movements:

```python
from textual.events import MouseDown, MouseUp, MouseMove
from textual.widgets import Static

class MouseWidget(Static):
    """Widget handling mouse events."""

    def on_mouse_down(self, event: MouseDown) -> None:
        """Called when mouse button pressed.

        Args:
            event: MouseDown event with position and button.
        """
        x, y = event.x, event.y
        button = event.button  # 1: left, 2: middle, 3: right

        if button == 1:  # Left click
            self.handle_click(x, y)

    def on_mouse_up(self, event: MouseUp) -> None:
        """Called when mouse button released."""
        pass

    def on_mouse_move(self, event: MouseMove) -> None:
        """Called when mouse moves over widget."""
        x, y = event.x, event.y
        # Update display or state based on position

    def handle_click(self, x: int, y: int) -> None:
        """Handle click at position."""
        self.update(f"Clicked at ({x}, {y})")
```

**Mouse Events:**
- `on_mouse_down()` - Button pressed
- `on_mouse_up()` - Button released
- `on_mouse_move()` - Mouse moved
- `on_click()` - Single click (widget-specific)
- `on_double_click()` - Double click (widget-specific)

### Step 6: Control Event Flow

Stop event propagation and bubble events:

```python
from textual.events import Key
from textual.app import ComposeResult
from textual.widgets import Static, Container

class StopPropagationWidget(Static):
    """Widget that stops event propagation."""

    def on_key(self, event: Key) -> None:
        """Handle key and stop propagation."""
        if event.key == "enter":
            self.handle_enter()
            event.stop()  # Stop parent from handling
        # If not handled, event propagates to parent

    def handle_enter(self) -> None:
        """Handle enter key."""
        self.update("Handled locally")

class EventBubblingExample(Container):
    """Demonstrate event bubbling."""

    def compose(self) -> ComposeResult:
        yield StopPropagationWidget(id="inner")

    def on_key(self, event: Key) -> None:
        """Parent key handler."""
        # Called if child doesn't call event.stop()
        pass
```

**Event Control:**
- `event.stop()` - Stop propagation to parent
- `event.prevent_default()` - Prevent default behavior
- Messages bubble up automatically
- Key events can be stopped

## Examples

### Example 1: Agent Command Widget with Custom Messages

```python
from textual.message import Message
from textual.widgets import Static, Input, Button
from textual.containers import Container, Horizontal
from textual.app import ComposeResult
from textual import on

class CommandWidget(Container):
    """Widget for entering agent commands."""

    class CommandSubmitted(Message):
        """Posted when command is submitted."""

        def __init__(self, agent_id: str, command: str) -> None:
            super().__init__()
            self.agent_id = agent_id
            self.command = command

    class CommandCancelled(Message):
        """Posted when command is cancelled."""

        def __init__(self, agent_id: str) -> None:
            super().__init__()
            self.agent_id = agent_id

    def __init__(self, agent_id: str, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._agent_id = agent_id

    def compose(self) -> ComposeResult:
        """Compose command input widget."""
        with Horizontal():
            yield Input(
                placeholder="Enter command...",
                id="command-input",
            )
            yield Button("Send", id="btn-send", variant="primary")
            yield Button("Clear", id="btn-clear")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "btn-send":
            await self._submit_command()
        elif event.button.id == "btn-clear":
            await self._cancel_command()

    async def _submit_command(self) -> None:
        """Submit command to agent."""
        input_field = self.query_one("#command-input", Input)
        command = input_field.value.strip()

        if command:
            input_field.value = ""
            self.post_message(self.CommandSubmitted(self._agent_id, command))

    async def _cancel_command(self) -> None:
        """Cancel command entry."""
        input_field = self.query_one("#command-input", Input)
        input_field.value = ""
        self.post_message(self.CommandCancelled(self._agent_id))

# Parent handling messages
class AgentConsoleWidget(Static):
    """Console displaying agent commands and responses."""

    def compose(self) -> ComposeResult:
        yield Static("Agent Console", classes="header")
        yield Static("Ready", id="console-output")
        yield CommandWidget("agent-1", id="command-widget")

    @on(CommandWidget.CommandSubmitted)
    async def on_command_submitted(self, message: CommandWidget.CommandSubmitted) -> None:
        """Handle command submission."""
        output = self.query_one("#console-output", Static)
        output.update(f"Executing: {message.command}\n")
        self.notify(f"Command sent to {message.agent_id}")

    @on(CommandWidget.CommandCancelled)
    async def on_command_cancelled(self, message: CommandWidget.CommandCancelled) -> None:
        """Handle command cancellation."""
        output = self.query_one("#console-output", Static)
        output.update("Command cancelled\n")
```

### Example 2: Keyboard Navigation in List

```python
from textual.widgets import Static, ListView, ListItem
from textual.events import Key
from textual.app import ComposeResult

class NavigableListWidget(Static):
    """List with keyboard navigation."""

    DEFAULT_CSS = """
    NavigableListWidget {
        height: 100%;
    }

    NavigableListWidget ListView {
        height: 1fr;
    }

    NavigableListWidget .highlight {
        background: $boost;
    }
    """

    def compose(self) -> ComposeResult:
        yield ListView(id="item-list")

    async def on_mount(self) -> None:
        """Populate list."""
        list_view = self.query_one("#item-list", ListView)
        for i in range(10):
            await list_view.append(
                ListItem(Static(f"Item {i}"))
            )

    def on_key(self, event: Key) -> None:
        """Handle keyboard navigation."""
        list_view = self.query_one("#item-list", ListView)

        if event.key == "up":
            if list_view.index is not None and list_view.index > 0:
                list_view.index -= 1
                event.stop()

        elif event.key == "down":
            if list_view.index is not None and list_view.index < len(list_view.children) - 1:
                list_view.index += 1
                event.stop()

        elif event.key == "home":
            list_view.index = 0
            event.stop()

        elif event.key == "end":
            list_view.index = len(list_view.children) - 1
            event.stop()
```

## Requirements
- Textual >= 0.45.0
- Python 3.9+

## Common Patterns

### Modal Message Handling

```python
class ConfirmDialog(Screen):
    """Modal dialog that returns a choice."""

    def __init__(self, prompt: str, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._prompt = prompt

    def action_confirm(self) -> None:
        """Confirm and return True."""
        self.app.pop_screen(result=True)

    def action_cancel(self) -> None:
        """Cancel and return False."""
        self.app.pop_screen(result=False)

# Usage
async def show_confirm() -> bool:
    """Show confirmation dialog."""
    result = await self.app.push_screen_wait(
        ConfirmDialog("Are you sure?")
    )
    return result
```

### Event Debouncing

```python
import asyncio
from textual.widgets import Input

class DebouncedInput(Input):
    """Input with debounced on_change events."""

    class ValueChanged(Message):
        def __init__(self, value: str) -> None:
            super().__init__()
            self.value = value

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._debounce_timer: asyncio.Task | None = None

    async def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input change with debounce."""
        # Cancel previous timer
        if self._debounce_timer:
            self._debounce_timer.cancel()

        # Schedule new timer
        self._debounce_timer = asyncio.create_task(self._emit_change(event.value))

    async def _emit_change(self, value: str) -> None:
        """Emit change after delay."""
        await asyncio.sleep(0.5)  # 500ms debounce
        self.post_message(self.ValueChanged(value))
```

## See Also
- [textual-app-lifecycle.md](../textual-app-lifecycle) - Keyboard bindings and actions
- [textual-widget-development.md](../textual-widget-development) - Widget lifecycle
