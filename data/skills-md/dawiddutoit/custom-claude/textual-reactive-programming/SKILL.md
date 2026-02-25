---
name: textual-reactive-programming
description: |
  Builds reactive Textual widgets using computed properties, watchers, and reactive attributes. Use when implementing data-binding patterns, responding to state changes, computed properties, efficient updates based on attribute changes, and validation patterns. Covers reactive decorators, watch methods, and avoiding manual refresh patterns.
allowed-tools: Read, Write, Edit, Bash
---

# Textual Reactive Programming

## Purpose
Implement efficient, declarative data binding in Textual widgets using reactive attributes. This pattern eliminates manual refresh calls and ensures UI stays synchronized with state.

## Quick Start

```python
from textual.reactive import reactive
from textual.widgets import Static

class CounterWidget(Static):
    """Widget with reactive counter."""

    count = reactive(0)  # Reactive attribute initialized to 0

    def render(self) -> str:
        """Auto-called when count changes."""
        return f"Count: {self.count}"

    def increment(self) -> None:
        """Increment counter - triggers render()."""
        self.count += 1

# Usage:
widget = CounterWidget()
widget.increment()  # Automatically re-renders
```

## Instructions

### Step 1: Define Reactive Attributes

Declare reactive attributes using `reactive()`:

```python
from textual.reactive import reactive
from textual.widgets import Static
from typing import Literal

class ReactiveWidget(Static):
    """Widget with multiple reactive attributes."""

    # Basic reactive attribute
    status: reactive[str] = reactive("idle", init=False)

    # Reactive with initial value
    count: reactive[int] = reactive(0)

    # Reactive with complex type
    items: reactive[list[str]] = reactive(list, init=False)

    # Reactive with default name (attribute name used)
    message: reactive[str] = reactive("default message")

    # Reactive with type union
    state: reactive[Literal["on", "off"]] = reactive("off")

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        # Initialize reactive attributes in __init__
        # Only if init=False is set above
        # Otherwise they're initialized by reactive()
```

**Reactive Declaration Options:**
```python
reactive(
    default_value,              # Required: initial value
    init=False,                 # True: initialize in __init__, False: initialize here
    layout=False,               # True: trigger layout when changed
    recompose=False,            # True: call compose() when changed
)
```

**Important Rules:**
- Type hints are required: `attribute: reactive[Type]`
- `init=False` means initialize in `__init__`
- `init=True` (default) means initialize by reactive()
- Changing a reactive attribute triggers a watcher/refresh

### Step 2: Use Watch Methods

Watch methods automatically trigger when reactive attributes change:

```python
from textual.reactive import reactive
from textual.widgets import Static
from typing import Literal

class WatcherWidget(Static):
    """Widget demonstrating watch methods."""

    status: reactive[Literal["idle", "running", "error"]] = reactive("idle", init=False)
    count: reactive[int] = reactive(0)
    items: reactive[list[str]] = reactive(list, init=False)

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.status = "idle"
        self.items = []

    def watch_status(self, old_value: str, new_value: str) -> None:
        """Called when status changes.

        Args:
            old_value: Previous status.
            new_value: New status.
        """
        # Update UI based on status change
        print(f"Status changed: {old_value} -> {new_value}")
        self.refresh()  # Re-render widget

    def watch_count(self, old_value: int, new_value: int) -> None:
        """Called when count changes."""
        if new_value < 0:
            # Revert invalid change
            self.count = old_value
        else:
            # Count is valid
            self.refresh()

    def watch_items(self, old_value: list[str], new_value: list[str]) -> None:
        """Called when items list changes.

        Note: Called on replacement, not on list mutations.
        """
        print(f"Items changed: {len(old_value)} -> {len(new_value)} items")
        self.refresh()

    def add_item(self, item: str) -> None:
        """Add item (triggers watch_items)."""
        # Replace list to trigger watcher
        self.items = self.items + [item]  # Creates new list
        # NOT: self.items.append(item)  # This won't trigger watcher

    def increment(self) -> None:
        """Increment count (triggers watch_count)."""
        self.count += 1  # Triggers watch_count
```

**Watcher Pattern:**
- Method name: `watch_{attribute_name}`
- Signature: `watch_method(self, old_value: Type, new_value: Type) -> None`
- Called automatically when attribute changes
- Called BEFORE re-render
- Use for validation, side effects, cascading updates

### Step 3: Implement Computed Properties

Use computed attributes that derive from other reactive attributes:

```python
from textual.reactive import reactive, var
from textual.widgets import Static

class ComputedWidget(Static):
    """Widget with computed reactive attributes."""

    first_name: reactive[str] = reactive("John", init=False)
    last_name: reactive[str] = reactive("Doe", init=False)

    # Computed property (read-only)
    @property
    def full_name(self) -> str:
        """Derived from first_name and last_name."""
        return f"{self.first_name} {self.last_name}"

    # Alternative: Use var() for derived reactive attribute
    full_name_reactive: reactive[str] = reactive("John Doe")

    def watch_first_name(self, old_value: str, new_value: str) -> None:
        """Update computed attribute when first_name changes."""
        self.full_name_reactive = f"{new_value} {self.last_name}"
        self.refresh()

    def watch_last_name(self, old_value: str, new_value: str) -> None:
        """Update computed attribute when last_name changes."""
        self.full_name_reactive = f"{self.first_name} {new_value}"
        self.refresh()

    def render(self) -> str:
        return f"Full Name: {self.full_name}"
```

**Pattern:**
- Use `@property` for computed values derived from reactive attrs
- Watchers update derived attributes when dependencies change
- Re-render when computed attributes change

### Step 4: Handle Complex State Changes

Manage complex updates with multiple reactive attributes:

```python
from textual.reactive import reactive
from textual.widgets import Static
from dataclasses import dataclass

@dataclass(frozen=True)
class DataPoint:
    """Immutable data point."""
    value: float
    timestamp: str

class ComplexStateWidget(Static):
    """Widget managing complex reactive state."""

    # Multiple reactive attributes
    data: reactive[list[DataPoint]] = reactive(list, init=False)
    total: reactive[float] = reactive(0.0)
    average: reactive[float] = reactive(0.0)
    loading: reactive[bool] = reactive(False)
    error: reactive[str | None] = reactive(None)

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.data = []
        self.total = 0.0
        self.average = 0.0
        self.loading = False
        self.error = None

    def watch_data(self, old_value: list[DataPoint], new_value: list[DataPoint]) -> None:
        """Recalculate totals when data changes."""
        if not new_value:
            self.total = 0.0
            self.average = 0.0
            return

        # Update computed values
        self.total = sum(p.value for p in new_value)
        self.average = self.total / len(new_value)
        self.error = None

    async def load_data(self) -> None:
        """Load data with loading state."""
        try:
            self.loading = True
            self.error = None

            # Simulate async fetch
            import asyncio
            await asyncio.sleep(1)

            # Update data (triggers watch_data)
            self.data = [
                DataPoint(10.5, "2024-01-01"),
                DataPoint(20.3, "2024-01-02"),
                DataPoint(15.8, "2024-01-03"),
            ]
        except Exception as e:
            self.error = str(e)
            self.data = []
        finally:
            self.loading = False

    def render(self) -> str:
        """Render with state."""
        if self.loading:
            return "Loading..."

        if self.error:
            return f"Error: {self.error}"

        if not self.data:
            return "No data"

        return (
            f"Items: {len(self.data)}\n"
            f"Total: {self.total:.2f}\n"
            f"Average: {self.average:.2f}"
        )
```

**Pattern:**
- Organize related reactive attributes together
- Watch methods maintain invariants (total, average, etc.)
- Atomic updates: replace entire list/dict to trigger watchers
- Use frozen dataclasses for immutable data points

### Step 5: Implement Validation with Reactive Attributes

Use watchers to validate and enforce constraints:

```python
from textual.reactive import reactive
from textual.widgets import Input, Static

class ValidatingWidget(Static):
    """Widget with reactive validation."""

    value: reactive[str] = reactive("", init=False)
    is_valid: reactive[bool] = reactive(True)
    error_message: reactive[str] = reactive("")

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.value = ""
        self.is_valid = True
        self.error_message = ""

    def watch_value(self, old_value: str, new_value: str) -> None:
        """Validate value when it changes."""
        # Validate
        is_valid = self._validate(new_value)

        if is_valid:
            self.is_valid = True
            self.error_message = ""
        else:
            self.is_valid = False
            self.error_message = "Invalid value"

        self.refresh()

    def _validate(self, value: str) -> bool:
        """Validate value according to rules."""
        # Example: email validation
        return "@" in value and "." in value

    def render(self) -> str:
        """Render with validation status."""
        status = "✓" if self.is_valid else "✗"
        return f"{status} {self.value}\n{self.error_message}"
```

**Validation Pattern:**
- Watch method validates on change
- Update separate reactive attributes for validity
- Re-render to show status
- Use color changes via CSS for invalid state

## Examples

### Example 1: Agent Status Widget with Reactive Updates

```python
from textual.reactive import reactive
from textual.widgets import Static
from rich.text import Text
from typing import Literal

class AgentStatusWidget(Static):
    """Reactive agent status widget."""

    agent_id: reactive[str] = reactive("")
    status: reactive[Literal["idle", "running", "error"]] = reactive("idle", init=False)
    task_count: reactive[int] = reactive(0)
    error_message: reactive[str | None] = reactive(None)

    DEFAULT_CSS = """
    AgentStatusWidget {
        height: auto;
        border: solid $primary;
        padding: 1;
    }

    AgentStatusWidget .status-idle {
        color: $warning;
    }

    AgentStatusWidget .status-running {
        color: $success;
    }

    AgentStatusWidget .status-error {
        color: $error;
    }
    """

    def __init__(self, agent_id: str, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.agent_id = agent_id
        self.status = "idle"
        self.task_count = 0
        self.error_message = None

    def watch_status(self, old_value: str, new_value: str) -> None:
        """Update display when status changes."""
        self.refresh()

    def watch_task_count(self, old_value: int, new_value: int) -> None:
        """Track task count changes."""
        if new_value > old_value:
            # Task started
            if self.status == "idle":
                self.status = "running"
        elif new_value == 0:
            # All tasks completed
            if self.status == "running":
                self.status = "idle"

    def watch_error_message(self, old_value: str | None, new_value: str | None) -> None:
        """Update status when error occurs."""
        if new_value:
            self.status = "error"
        else:
            self.status = "idle"

    def render(self) -> Text:
        """Render reactive agent status."""
        text = Text()

        # Status indicator
        icon = self._get_icon()
        text.append(icon, style=f"status-{self.status}")
        text.append(" ")

        # Agent info
        text.append(self.agent_id, style="bold")
        text.append(f" ({self.status.upper()})")

        # Task count
        if self.task_count > 0:
            text.append(f" [{self.task_count} tasks]", style="dim")

        # Error
        if self.error_message:
            text.append("\n")
            text.append(f"Error: {self.error_message}", style="bold red")

        return text

    def _get_icon(self) -> str:
        """Get status icon."""
        return {
            "idle": "◐",
            "running": "●",
            "error": "✗",
        }.get(self.status, "?")

    async def update_task_count(self, count: int) -> None:
        """Update task count."""
        self.task_count = count

    async def set_error(self, error: str | None) -> None:
        """Set error state."""
        self.error_message = error
```

### Example 2: Form Widget with Reactive Validation

```python
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static, Input, Button

class FormWidget(Container):
    """Form with reactive validation."""

    email: reactive[str] = reactive("", init=False)
    password: reactive[str] = reactive("", init=False)
    is_valid: reactive[bool] = reactive(False)

    DEFAULT_CSS = """
    FormWidget {
        height: auto;
        border: solid $primary;
        padding: 1;
    }

    FormWidget .field {
        height: auto;
        margin: 0 0 1 0;
    }

    FormWidget .field-label {
        text-style: bold;
    }

    FormWidget .field-error {
        color: $error;
        text-style: dim;
    }

    FormWidget .submit-button {
        margin-top: 1;
    }
    """

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.email = ""
        self.password = ""
        self.is_valid = False

    def compose(self) -> ComposeResult:
        yield Static("Email", classes="field-label")
        yield Input(id="email-input", classes="field")
        yield Static("", id="email-error", classes="field-error")

        yield Static("Password", classes="field-label")
        yield Input(id="password-input", password=True, classes="field")
        yield Static("", id="password-error", classes="field-error")

        yield Button("Submit", id="submit", disabled=True, classes="submit-button")

    async def on_mount(self) -> None:
        """Set up input watchers."""
        email_input = self.query_one("#email-input", Input)
        password_input = self.query_one("#password-input", Input)

        email_input.on_change_handler = self._on_email_change
        password_input.on_change_handler = self._on_password_change

    async def _on_email_change(self, value: str) -> None:
        """Handle email input change."""
        self.email = value
        await self._validate_email()

    async def _on_password_change(self, value: str) -> None:
        """Handle password input change."""
        self.password = value
        await self._validate_password()

    def watch_email(self, old_value: str, new_value: str) -> None:
        """Validate email when changed."""
        self._check_form_valid()

    def watch_password(self, old_value: str, new_value: str) -> None:
        """Validate password when changed."""
        self._check_form_valid()

    async def _validate_email(self) -> None:
        """Validate email format."""
        error_widget = self.query_one("#email-error", Static)
        if not self.email or "@" not in self.email:
            error_widget.update("Invalid email")
        else:
            error_widget.update("")

    async def _validate_password(self) -> None:
        """Validate password strength."""
        error_widget = self.query_one("#password-error", Static)
        if len(self.password) < 8:
            error_widget.update("Password must be 8+ characters")
        else:
            error_widget.update("")

    def _check_form_valid(self) -> None:
        """Check if entire form is valid."""
        is_valid = (
            "@" in self.email
            and len(self.password) >= 8
        )
        self.is_valid = is_valid

        # Update submit button
        submit = self.query_one("#submit", Button)
        submit.disabled = not is_valid
```

## Requirements
- Textual >= 0.45.0
- Python 3.9+ with type hints

## Best Practices

**1. Prefer reactive attributes over manual refresh:**
```python
# ❌ WRONG - manual refresh
def set_status(self, status: str) -> None:
    self._status = status
    self.refresh()

# ✅ CORRECT - reactive attribute
status: reactive[str] = reactive("")

def watch_status(self, old_value: str, new_value: str) -> None:
    """Auto-refresh on change."""
    pass  # refresh() called automatically
```

**2. Use watchers for side effects:**
```python
def watch_count(self, old_value: int, new_value: int) -> None:
    """Handle side effects."""
    if new_value > 10:
        self.error = "Too many items"
    self.refresh()
```

**3. Replace collections to trigger watchers:**
```python
# ❌ WRONG - mutation doesn't trigger watcher
self.items.append(new_item)

# ✅ CORRECT - replacement triggers watcher
self.items = self.items + [new_item]
# OR
self.items = [*self.items, new_item]
```

## See Also
- [textual-widget-development.md](../textual-widget-development) - Widget structure and lifecycle
- [textual-event-messages.md](../textual-event-messages) - Custom messages and events
