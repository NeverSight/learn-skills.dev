---
name: textual-test-patterns
description: |
  Testing recipes for specific Textual TUI scenarios. Provides "how do I test X?" patterns
  for common testing needs. Use when: testing keyboard shortcuts, screen transitions, focus
  management, reactive attributes, custom messages/events, CSS styling effects, data tables,
  scrolling, input validation, error/loading states, or background workers. Each pattern
  shows the complete test with proper async handling and assertions.

---

# Textual Test Patterns

Testing recipes for specific Textual scenarios. Each pattern shows complete, working test code.

## Pattern Index

| Scenario | Pattern |
|----------|---------|
| Keyboard shortcuts | [Test Keyboard Shortcuts](#test-keyboard-shortcuts) |
| Screen transitions | [Test Screen Transitions](#test-screen-transitions) |
| Focus management | [Test Focus Management](#test-focus-management) |
| Reactive attributes | [Test Reactive Attributes](#test-reactive-attributes) |
| Custom messages | [Test Custom Messages](#test-custom-messages) |
| CSS styling | [Test CSS Styling](#test-css-styling) |
| Data tables | [Test Data Tables](#test-data-tables) |
| Scrolling | [Test Scrolling](#test-scrolling) |
| Input validation | [Test Input Validation](#test-input-validation) |
| Error states | [Test Error States](#test-error-states) |
| Loading states | [Test Loading States](#test-loading-states) |
| Background workers | [Test Background Workers](#test-background-workers) |

## Test Keyboard Shortcuts

```python
async def test_keyboard_shortcuts():
    """Test keyboard binding triggers action."""
    class MyApp(App):
        BINDINGS = [("ctrl+s", "save", "Save")]
        saved = False

        def action_save(self) -> None:
            self.saved = True

    async with MyApp().run_test() as pilot:
        await pilot.press("ctrl+s")
        await pilot.pause()
        assert pilot.app.saved is True
```

## Test Screen Transitions

```python
from textual.screen import Screen

class MainScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

async def test_screen_navigation():
    """Test navigating between screens."""
    class MyApp(App):
        SCREENS = {"settings": SettingsScreen}

        def compose(self):
            yield Static("Main")

        def key_s(self):
            self.push_screen("settings")

    async with MyApp().run_test() as pilot:
        # Start on default screen
        assert not isinstance(pilot.app.screen, SettingsScreen)

        # Navigate to settings
        await pilot.press("s")
        await pilot.pause()
        assert isinstance(pilot.app.screen, SettingsScreen)

        # Navigate back
        await pilot.press("escape")
        await pilot.pause()
        assert not isinstance(pilot.app.screen, SettingsScreen)
```

## Test Focus Management

```python
from textual.widgets import Input

async def test_focus_order():
    """Test Tab moves focus through widgets."""
    class MyApp(App):
        def compose(self):
            yield Input(id="name")
            yield Input(id="email")
            yield Input(id="phone")

    async with MyApp().run_test() as pilot:
        name = pilot.app.query_one("#name", Input)
        email = pilot.app.query_one("#email", Input)

        # First input focused by default
        assert name.has_focus

        # Tab to next
        await pilot.press("tab")
        await pilot.pause()
        assert email.has_focus
        assert not name.has_focus

        # Shift+Tab back
        await pilot.press("shift+tab")
        await pilot.pause()
        assert name.has_focus
```

## Test Reactive Attributes

```python
from textual.reactive import reactive
from textual.widgets import Static

class StatusWidget(Static):
    status: reactive[str] = reactive("idle")

    def watch_status(self, new_status: str) -> None:
        self.add_class(f"status-{new_status}")
        self.remove_class(f"status-{self._previous_status}")
        self._previous_status = new_status

    def __init__(self):
        super().__init__()
        self._previous_status = "idle"

async def test_reactive_attribute():
    """Test reactive attribute triggers watcher."""
    class TestApp(App):
        def compose(self):
            yield StatusWidget(id="status")

    async with TestApp().run_test() as pilot:
        widget = pilot.app.query_one("#status", StatusWidget)

        assert widget.status == "idle"
        assert widget.has_class("status-idle")

        widget.status = "loading"
        await pilot.pause()

        assert widget.has_class("status-loading")
        assert not widget.has_class("status-idle")
```

## Test Custom Messages

```python
from textual.message import Message

class ItemSelected(Message):
    def __init__(self, item_id: str) -> None:
        super().__init__()
        self.item_id = item_id

async def test_custom_message():
    """Test custom message is received by handler."""
    class MyApp(App):
        selected_items: list[str] = []

        def compose(self):
            yield Static("Item", id="item")

        def on_item_selected(self, message: ItemSelected) -> None:
            self.selected_items.append(message.item_id)

    async with MyApp().run_test() as pilot:
        # Post message
        pilot.app.post_message(ItemSelected("item-1"))
        await pilot.pause()

        assert pilot.app.selected_items == ["item-1"]

        # Post another
        pilot.app.post_message(ItemSelected("item-2"))
        await pilot.pause()

        assert pilot.app.selected_items == ["item-1", "item-2"]
```

## Test CSS Styling

```python
from textual.color import Color

async def test_css_class_application():
    """Test CSS class changes styling."""
    class MyApp(App):
        CSS = """
        .error { background: red; }
        .success { background: green; }
        """

        def compose(self):
            yield Static("Status", id="status")

    async with MyApp().run_test() as pilot:
        status = pilot.app.query_one("#status")

        # Add error class
        status.add_class("error")
        await pilot.pause()
        assert status.has_class("error")

        # Switch to success
        status.remove_class("error")
        status.add_class("success")
        await pilot.pause()
        assert status.has_class("success")
        assert not status.has_class("error")
```

## Test Data Tables

```python
from textual.widgets import DataTable

async def test_data_table():
    """Test data table row selection."""
    class MyApp(App):
        def compose(self):
            yield DataTable(id="table")

        def on_mount(self):
            table = self.query_one("#table", DataTable)
            table.add_columns("Name", "Value")
            table.add_rows([
                ("Alice", "100"),
                ("Bob", "200"),
                ("Carol", "300"),
            ])

    async with MyApp().run_test() as pilot:
        table = pilot.app.query_one("#table", DataTable)

        assert table.row_count == 3

        # Navigate and select
        await pilot.click(DataTable)
        await pilot.press("down", "down")
        await pilot.pause()

        assert table.cursor_row == 2
```

## Test Scrolling

```python
from textual.containers import ScrollableContainer

async def test_scrolling():
    """Test scroll position changes."""
    class MyApp(App):
        def compose(self):
            with ScrollableContainer(id="container"):
                for i in range(100):
                    yield Static(f"Line {i}")

    async with MyApp().run_test(size=(80, 10)) as pilot:
        container = pilot.app.query_one("#container", ScrollableContainer)

        # Start at top
        assert container.scroll_y == 0

        # Scroll down
        await pilot.press("pagedown")
        await pilot.pause()
        assert container.scroll_y > 0

        # Scroll to end
        await pilot.press("end")
        await pilot.pause()
        assert container.scroll_y == container.max_scroll_y
```

## Test Input Validation

```python
from textual.widgets import Input
from textual.validation import Validator, ValidationResult

class EmailValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        if "@" in value and "." in value.split("@")[-1]:
            return self.success()
        return self.failure("Invalid email")

async def test_input_validation():
    """Test input field validates correctly."""
    class MyApp(App):
        def compose(self):
            yield Input(id="email", validators=[EmailValidator()])

    async with MyApp().run_test() as pilot:
        input_widget = pilot.app.query_one("#email", Input)

        # Invalid input
        await pilot.click(Input)
        await pilot.press(*"invalid")
        await pilot.pause()
        assert not input_widget.is_valid

        # Clear and enter valid
        input_widget.value = ""
        await pilot.press(*"user@example.com")
        await pilot.pause()
        assert input_widget.is_valid
```

## Test Error States

```python
async def test_error_display():
    """Test error message shows and dismisses."""
    class MyApp(App):
        def compose(self):
            yield Static("", id="error", classes="hidden")

        def show_error(self, msg: str):
            error = self.query_one("#error")
            error.update(msg)
            error.remove_class("hidden")

        def dismiss_error(self):
            self.query_one("#error").add_class("hidden")

    async with MyApp().run_test() as pilot:
        error = pilot.app.query_one("#error")

        # Initially hidden
        assert error.has_class("hidden")

        # Show error
        pilot.app.show_error("Something went wrong")
        await pilot.pause()
        assert not error.has_class("hidden")
        assert "Something went wrong" in error.renderable

        # Dismiss
        pilot.app.dismiss_error()
        await pilot.pause()
        assert error.has_class("hidden")
```

## Test Loading States

```python
async def test_loading_indicator():
    """Test loading state shows during async work."""
    class MyApp(App):
        loading = False

        def compose(self):
            yield Static("Ready", id="status")

        async def load_data(self):
            self.loading = True
            self.query_one("#status").update("Loading...")
            # Simulate async work
            await asyncio.sleep(0.1)
            self.loading = False
            self.query_one("#status").update("Loaded")

    async with MyApp().run_test() as pilot:
        status = pilot.app.query_one("#status")

        # Before loading
        assert "Ready" in status.renderable

        # Start loading (don't await)
        task = asyncio.create_task(pilot.app.load_data())
        await pilot.pause(0.05)

        # During loading
        assert pilot.app.loading is True

        # After loading
        await task
        await pilot.pause()
        assert pilot.app.loading is False
        assert "Loaded" in status.renderable
```

## Test Background Workers

```python
async def test_worker_completion():
    """Test background worker completes and updates state."""
    class MyApp(App):
        data = None

        def compose(self):
            yield Static("", id="result")

        @work
        async def fetch_data(self):
            await asyncio.sleep(0.1)
            self.data = {"items": [1, 2, 3]}
            self.query_one("#result").update(str(self.data))

    async with MyApp().run_test() as pilot:
        # Trigger worker
        pilot.app.fetch_data()

        # Wait for completion
        await pilot.app.workers.wait_for_complete()

        # Verify result
        assert pilot.app.data == {"items": [1, 2, 3]}
```

## Common Pitfalls

| Issue | Fix |
|-------|-----|
| Assertion before update | Add `await pilot.pause()` after interactions |
| Worker not complete | Use `await pilot.app.workers.wait_for_complete()` |
| Animation interference | Use `await pilot.wait_for_animation()` |
| Race condition | Increase pause duration or use explicit waits |

## See Also

- [textual-testing](../textual-testing) - Core Pilot API reference
- [textual-test-fixtures](../textual-test-fixtures) - Fixture patterns
- [textual-snapshot-testing](../textual-snapshot-testing) - Visual regression
