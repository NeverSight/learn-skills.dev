---
name: textual-app-lifecycle
description: |
  Builds Textual applications with proper app lifecycle management, screen handling, and event loops. Use when creating Textual App subclasses, implementing on_mount/on_unmount handlers, managing application state, navigating between screens, and understanding app initialization flow. Includes patterns for graceful shutdown, configuration loading, and daemon/background task management.
allowed-tools: Read, Write, Edit, Bash
---

# Textual App Lifecycle

## Purpose
Understand and implement proper Textual application lifecycle patterns including initialization, mounting, screen management, background workers, and graceful shutdown. This is the foundation for building robust TUI applications.

## Quick Start

```python
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Static
from typing import ClassVar

class MyApp(App):
    """Minimal Textual application with proper lifecycle."""

    TITLE = "My Application"
    SUB_TITLE = "Powered by Textual"

    BINDINGS: ClassVar[list[Binding]] = [
        Binding("q", "quit", "Quit", show=True, priority=True),
        Binding("ctrl+c", "quit", "Quit", show=False, priority=True),
    ]

    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield Header(show_clock=True)
        yield Static("Welcome to Textual!", id="content")
        yield Footer()

    def on_mount(self) -> None:
        """Handle application mount event."""
        # Initialize application state, load configuration, etc.
        self.notify("Application started", severity="information")

    def action_quit(self) -> None:
        """Handle quit action with cleanup."""
        self.exit()

if __name__ == "__main__":
    app = MyApp()
    app.run()
```

## Instructions

### Step 1: Define App Class and Metadata

Create your App subclass with proper metadata and configuration:

```python
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from typing import ClassVar

class MyApp(App[None]):  # [T] is the return type for app.run()
    """Application description."""

    # Metadata
    TITLE = "Application Title"
    SUB_TITLE = "Optional subtitle"

    # Keyboard bindings
    BINDINGS: ClassVar[list[Binding | tuple]] = [
        Binding("q", "quit", "Quit", show=True, priority=True),
        Binding("ctrl+c", "quit", "Quit", show=False, priority=True),
        ("r", "refresh", "Refresh"),
    ]

    # CSS styling (inline or separate .css file)
    CSS = """
    Screen {
        background: $surface;
    }
    """

    # Theme selection
    THEME = "dracula"  # Built-in themes: nord, dracula, monokai, solarized-dark, etc.
```

### Step 2: Implement Application Composition

Define `compose()` to return all top-level widgets:

```python
def compose(self) -> ComposeResult:
    """Compose the application layout.

    Yields:
        Application components (Header, Footer, widgets, etc).

    Yields immediately - don't use async here.
    """
    yield Header(show_clock=True)  # Optional header with clock
    yield StaticContent()           # Your custom widgets
    yield Footer()                  # Optional footer with bindings
```

**Key Points:**
- `compose()` is synchronous - don't use `await`
- Widgets are yielded in order (they appear top-to-bottom)
- Use Container, Horizontal, Vertical for layout
- Containers support CSS Grid layout

### Step 3: Handle App Initialization (on_mount)

Implement `on_mount()` for initialization after all widgets are mounted:

```python
def on_mount(self) -> None:
    """Handle application mount event.

    Called after compose() completes and all widgets are mounted.
    Use for:
    - Loading configuration
    - Initializing state
    - Starting background workers
    - Setting up timers
    - Querying mounted widgets
    """
    # Load configuration
    try:
        self._config = self._load_config()
    except Exception as e:
        self.notify(f"Config error: {e}", severity="error")
        return

    # Query and configure widgets
    content = self.query_one("#content", Static)
    content.update("Initialized!")

    # Set up auto-refresh timer (runs every N seconds)
    self.set_interval(5.0, self._on_timer)

    # Start background worker
    self.run_worker(self._background_task())

async def _background_task(self) -> None:
    """Background async task that runs concurrently."""
    while True:
        # Do async work (I/O, network, etc.)
        await asyncio.sleep(1)
        self._update_ui()

def _on_timer(self) -> None:
    """Called by timer periodically."""
    # Synchronous callback - don't use await
    pass
```

**Important Rules:**
- `on_mount()` is synchronous
- Can use `self.query_one()` to access widgets (they're mounted now)
- Use `self.run_worker()` to start async tasks
- Use `self.set_interval()` for periodic tasks
- Use `self.notify()` to show toast messages

### Step 4: Implement Action Handlers

Actions are triggered by keybindings and can be async:

```python
def action_refresh(self) -> None:
    """Synchronous action handler."""
    self.run_worker(self._async_refresh())

async def _async_refresh(self) -> None:
    """Async action implementation."""
    try:
        # Do async work (fetch data, update UI)
        data = await self._fetch_data()
        await self._update_ui(data)
    except Exception as e:
        self.notify(f"Refresh failed: {e}", severity="error")

def action_quit(self) -> None:
    """Exit the application."""
    # Cleanup happens automatically
    self.exit()

def action_add_item(self) -> None:
    """Action with optional argument."""
    self.run_worker(self._show_dialog())
```

**Pattern:**
- Keybindings call action methods
- Actions can be sync or async
- For async work, use `self.run_worker()`
- Action methods are public (no leading underscore)

### Step 5: Handle Screen Navigation

Switch between screens for modal dialogs, multi-screen apps:

```python
class MyApp(App):
    def action_show_settings(self) -> None:
        """Push settings screen on top of current screen."""
        self.push_screen(SettingsScreen())

    def action_close_settings(self) -> None:
        """Pop settings screen and return to previous."""
        self.pop_screen()

class SettingsScreen(Screen):
    """Modal settings dialog."""

    def compose(self) -> ComposeResult:
        yield Static("Settings")

    def on_mount(self) -> None:
        """Initialize settings screen."""
        pass

    def action_save(self) -> None:
        """Save settings and close."""
        self.pop_screen()  # Return to previous screen

    def action_cancel(self) -> None:
        """Close without saving."""
        self.pop_screen()
```

**Screen Stack:**
- `push_screen()` adds screen on top (modal behavior)
- `pop_screen()` removes top screen
- `switch_screen()` replaces current screen
- Screens can return values using `pop_screen(result)`

### Step 6: Implement Graceful Shutdown

Cleanup resources on application exit:

```python
def on_unmount(self) -> None:
    """Handle application unmount/exit.

    Called after widgets are unmounted but before app exits.
    Use for cleanup: closing connections, saving state, etc.
    """
    # Save state
    if self._config:
        self._config.save()

    # Close connections
    if self._connection:
        self._connection.close()

    # Cancel background tasks
    # (Textual handles this automatically)

async def on_shutdown(self) -> None:
    """Called when application is shutting down.

    This is async - use for async cleanup.
    """
    # Close async connections
    if self._async_client:
        await self._async_client.close()
```

## Examples

### Example 1: Dashboard with Auto-Refresh and Notifications

```python
import asyncio
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Static, Container
from typing import ClassVar

class DashboardApp(App):
    """Dashboard that auto-refreshes data."""

    TITLE = "Agent Dashboard"
    BINDINGS: ClassVar[list[Binding]] = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._data: dict | None = None
        self._refresh_task_id: str | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("Loading...", id="status"),
            Static("", id="content"),
            Static("", id="footer-info"),
        )
        yield Footer()

    def on_mount(self) -> None:
        """Initialize dashboard on mount."""
        # Start auto-refresh (every 3 seconds)
        self.set_interval(3.0, self._silent_refresh)

        # Initial load with notification
        self.run_worker(self._refresh_with_notification())

    async def _refresh_with_notification(self) -> None:
        """Refresh and show notification."""
        try:
            self._data = await self._fetch_data()
            await self._update_display()
            self.notify("Dashboard refreshed", severity="information")
        except Exception as e:
            self.notify(f"Refresh error: {e}", severity="error")

    def _silent_refresh(self) -> None:
        """Auto-refresh without notification."""
        self.run_worker(self._refresh_async())

    async def _refresh_async(self) -> None:
        """Background refresh."""
        try:
            self._data = await self._fetch_data()
            await self._update_display()
        except Exception:
            pass  # Silent fail on background refresh

    async def _fetch_data(self) -> dict:
        """Simulate fetching data from remote."""
        await asyncio.sleep(0.5)  # Simulate network delay
        return {
            "status": "running",
            "agents": 3,
            "cpu": 45.2,
            "memory": 62.8,
        }

    async def _update_display(self) -> None:
        """Update display with current data."""
        if not self._data:
            return

        status = self.query_one("#status", Static)
        status.update(f"Status: {self._data['status']}")

        content = self.query_one("#content", Static)
        content.update(
            f"Agents: {self._data['agents']}\n"
            f"CPU: {self._data['cpu']:.1f}%\n"
            f"Memory: {self._data['memory']:.1f}%"
        )

    def action_refresh(self) -> None:
        """Manual refresh action."""
        self.run_worker(self._refresh_with_notification())

    def on_unmount(self) -> None:
        """Cleanup on exit."""
        # Textual automatically cancels timers and workers
        pass

if __name__ == "__main__":
    app = DashboardApp()
    app.run()
```

### Example 2: Multi-Screen Application with Modal Dialog

```python
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Input
from typing import ClassVar

class MainScreen(Screen):
    """Main application screen."""

    BINDINGS: ClassVar[list[Binding]] = [
        ("q", "quit", "Quit"),
        ("o", "open_dialog", "Open"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Main Screen", id="content")
        yield Footer()

    def action_open_dialog(self) -> None:
        """Open modal dialog."""
        self.app.push_screen(ModalDialog())

class ModalDialog(Screen):
    """Modal dialog example."""

    BINDINGS: ClassVar[list[Binding]] = [
        ("escape", "cancel", "Cancel"),
        ("enter", "confirm", "Confirm"),
    ]

    CSS = """
    ModalDialog {
        align: center middle;
    }

    ModalDialog > Container {
        width: 40;
        height: 10;
        border: solid $primary;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Container():
            yield Static("Dialog Title", id="dialog-title")
            yield Input("Enter something:", id="dialog-input")
            yield Button("OK", id="btn-ok")
            yield Button("Cancel", id="btn-cancel")

    def action_confirm(self) -> None:
        """Confirm and return data."""
        input_field = self.query_one("#dialog-input", Input)
        self.app.pop_screen(result=input_field.value)

    def action_cancel(self) -> None:
        """Cancel without returning data."""
        self.app.pop_screen()

class MultiScreenApp(App):
    """App with multiple screens."""

    def compose(self) -> ComposeResult:
        yield MainScreen()

if __name__ == "__main__":
    app = MultiScreenApp()
    app.run()
```

## Requirements
- Textual >= 0.45.0 (install with `pip install textual`)
- Python 3.9+ for type hints
- For syntax highlighting in TextArea: `pip install "textual[syntax]"`

## Common Pitfalls

**1. Calling async functions synchronously:**
```python
# ❌ WRONG - can't await in sync context
def on_mount(self) -> None:
    self._data = await self._fetch_data()  # Error!

# ✅ CORRECT - use run_worker
def on_mount(self) -> None:
    self.run_worker(self._load_data())
```

**2. Querying widgets before mount:**
```python
# ❌ WRONG - compose() runs before mount
def compose(self) -> ComposeResult:
    yield Static("Test")
    widget = self.query_one("#something")  # Fails!

# ✅ CORRECT - query in on_mount or later
def on_mount(self) -> None:
    widget = self.query_one("#something")  # Works!
```

**3. Forgetting to set interval ID:**
```python
# ❌ Can't cancel later
self.set_interval(5.0, callback)

# ✅ Save ID if you need to cancel
self._timer_id = self.set_interval(5.0, callback)
# Later: self.remove_timer(self._timer_id)
```

**4. Not handling async errors in workers:**
```python
# ❌ Errors are silent
def on_mount(self) -> None:
    self.run_worker(self._fetch_data())

# ✅ Handle errors
def on_mount(self) -> None:
    self.run_worker(self._safe_fetch())

async def _safe_fetch(self) -> None:
    try:
        await self._fetch_data()
    except Exception as e:
        self.notify(f"Error: {e}", severity="error")
```

## See Also
- [textual-event-messages.md](../textual-event-messages) - Event and message handling patterns
- [textual-widget-development.md](../textual-widget-development) - Creating custom widgets
- [textual-reactive-programming.md](../textual-reactive-programming) - Reactive attributes and watchers
