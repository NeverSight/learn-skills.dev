---
name: setting-up-shortcuts
description: "Set up customizable keyboard shortcuts for PySide6 apps with TOML config and platform-specific defaults."
---

# Setting Up Keyboard Shortcuts

Reusable keyboard shortcuts system for PySide6 applications. Provides platform-specific defaults, TOML configuration, and Qt integration.

Copy reusable code from `coding_rules_python/reusable/shortcuts/` and tests from `coding_rules_python/reusable_tests/`.

See also: `reusable/shortcuts/README.md` for full API reference.

---

## When to Use

- PySide6 desktop apps that need **customizable keyboard shortcuts**
- Apps targeting **multiple platforms** (Linux, Windows, macOS)
- Apps where users should be able to **edit shortcuts via config file**

---

## Quick Start

### 1. Define Shortcuts

```python
# src/myapp/config.py
from shared.shortcuts import ActionShortcut

DEFAULT_SHORTCUTS = (
    ActionShortcut("new_file", "New File", "Ctrl+N", "Ctrl+N", "Cmd+N"),
    ActionShortcut("save", "Save", "Ctrl+S", "Ctrl+S", "Cmd+S"),
    ActionShortcut("quit", "Quit", "Ctrl+Q", "Ctrl+Q", "Cmd+Q"),
    ActionShortcut("search", "Search", "Ctrl+F"),  # Same on all platforms
)
```

### 2. Initialize Manager

```python
from shared.shortcuts import ShortcutManager
from pathlib import Path
import platformdirs

manager = ShortcutManager(
    config_dir=Path(platformdirs.user_config_dir("myapp")),
    app_name="myapp",
    default_shortcuts=DEFAULT_SHORTCUTS,
)
```

### 3. Use in Qt

```python
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.shortcut_manager = manager
        self.shortcut_manager.load()
        self._setup_menu()

    def _setup_menu(self):
        file_menu = self.menuBar().addMenu("&File")

        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence(self.shortcut_manager.get_shortcut("save")))
        save_action.triggered.connect(self._save)
        file_menu.addAction(save_action)
```

---

## Key Concepts

### ActionShortcut

Immutable definition of a keyboard shortcut with platform-specific defaults:

```python
ActionShortcut(
    action_id="save",           # Unique ID (snake_case)
    display_name="Save",        # Human-readable name for UI
    default_linux="Ctrl+S",     # Linux default
    default_windows="Ctrl+S",   # Windows default (falls back to Linux if empty)
    default_macos="Cmd+S",      # macOS default (falls back to Linux if empty)
)
```

### Key Sequence Format

Uses Qt's `QKeySequence` string format:

- **Modifiers:** `Ctrl`, `Shift`, `Alt`, `Meta`
- **Special keys:** `Return` (NOT `Enter`), `Backspace`, `Delete`, `Tab`, `Escape`, `Space`, `F1`-`F35`
- **Navigation:** `Left`, `Right`, `Up`, `Down`, `Home`, `End`, `PageUp`, `PageDown`
- **Combine with `+`:** `Ctrl+Shift+S`, `Alt+Left`

**Important:** Always use `"Return"` for the Enter key, NOT `"Enter"` (which maps to numpad Enter on some platforms).

### TOML Config File

Auto-created at `<config_dir>/<app_name>_shortcuts.toml`:

```toml
# Edit keyboard shortcuts using Qt QKeySequence string format.
# MODIFIERS: Ctrl, Shift, Alt, Meta (use '+' to combine)
# SPECIAL KEYS: Return (Enter key), Backspace, Delete, Tab, Escape, Space, F1-F35

[shortcuts]
new_file = "Ctrl+N"
save = "Ctrl+S"
quit = "Ctrl+Q"
search = ""        # Empty string disables the shortcut
```

---

## Dependencies

```toml
[project]
dependencies = [
    "pyside6>=6.10.1",
    "rusty-results>=1.1.1",
    "tomli>=2.2.1",
    "tomli-w>=1.2.0",
]
```

---

## Files to Copy

From `coding_rules_python/reusable/`:
- `shortcuts/__init__.py` — public API exports
- `shortcuts/shortcuts.py` — `ActionShortcut`, `ShortcutConfig`, `ShortcutManager`
- `shortcuts/README.md` — full API reference

From `coding_rules_python/reusable_tests/` → copy into your `tests/`:
- `test_shortcuts_base.py` — generic tests for `ActionShortcut`, `ShortcutConfig`, validation
- `test_shortcuts_manager.py` — generic tests for `ShortcutManager`

Update import paths after copying (e.g., `reusable.shortcuts` → `shared.shortcuts`, `reusable.shortcuts.shortcuts` → `shared.shortcuts.shortcuts` in monkeypatch paths).

---

## Testing

The reusable tests cover all generic behavior. For app-specific tests:

```python
# tests/test_my_shortcuts.py
from reusable_tests.test_shortcuts_base import (
    TestActionShortcut,
    TestShortcutConfig,
    TestShortcutConfigSave,
    TestValidateKeySequence,
)

# Inherit generic tests — they run automatically
class TestMyActionShortcut(TestActionShortcut):
    pass

# Add app-specific tests
class TestMyAppShortcuts:
    def test_default_shortcuts_are_valid(self):
        from myapp.config import DEFAULT_SHORTCUTS
        for shortcut in DEFAULT_SHORTCUTS:
            assert shortcut.action_id
            assert shortcut.display_name
```
