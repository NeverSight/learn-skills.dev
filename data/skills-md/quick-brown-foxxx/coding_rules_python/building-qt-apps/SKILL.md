---
name: building-qt-apps
description: "PySide6 desktop apps: Manager→Service→Wrapper architecture, qasync integration, signals, system tray, testing. Use when building or modifying Qt GUI applications."
---

# Building Qt Apps

Qt apps use PySide6 with qasync for async integration. Architecture follows Manager → Service → Wrapper layering. Never block the event loop.

---

## Why PySide6

- LGPL license (no additional restrictions)
- No extra system dependencies (ships with wheels)
- Same API as PyQt6, but freely redistributable

---

## Architecture: Manager → Service → Wrapper

```
UI Layer (MainWindow, Dialogs, TrayIcon)
    |  Qt signals/slots
    v
Manager Layer (AudioManager, TranscriptionManager)
    |  orchestrates, emits signals
    v
Service Layer (TranscriptionService, RecordingService)
    |  async operations
    v
Wrapper Layer (WhisperWrapper, SoundcardWrapper)
    |  typed interfaces to third-party libs
    v
Third-Party Libraries
```

### Manager Pattern

Managers coordinate operations and emit Qt signals:

```python
class TranscriptionManager(QObject):
    transcription_finished = Signal(str)
    transcription_error = Signal(str)
    model_changed = Signal(str)

    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self._service: TranscriptionService | None = None
        self._bridge = QAsyncSignalBridge()

    def transcribe(self, audio_data: np.ndarray) -> bool:
        if not self._service:
            self.transcription_error.emit("Service not initialized")
            return False

        self._bridge.run_async(
            self._service.transcribe(audio_data),
            on_success=self._on_finished,
            on_error=self._on_error,
        )
        return True

    def _on_finished(self, text: str) -> None:
        self.transcription_finished.emit(text)

    def _on_error(self, error: str) -> None:
        self.transcription_error.emit(error)
```

### Wrapper Pattern

Typed wrappers isolate untyped third-party APIs:

```python
class WhisperModelWrapper:
    """Typed wrapper for faster-whisper."""

    def __init__(self, model_size: str, device: str = "auto") -> None:
        from faster_whisper import WhisperModel as _WhisperModel
        self._model = _WhisperModel(model_size, device=device)

    def transcribe(self, audio: np.ndarray, language: str | None = None) -> TranscriptionResult:
        segments_gen, info = self._model.transcribe(audio, language=language)
        return TranscriptionResult(
            text="".join(s.text for s in segments_gen),
            language=str(info.language),
        )
```

---

## Async Integration with qasync (over QtAsyncio, which is still in technical preview)

### Setup

```python
import asyncio
import qasync
from PySide6.QtWidgets import QApplication

def main() -> int:
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        window = MainWindow()
        window.show()
        loop.run_forever()
    return 0
```

### QAsyncSignalBridge

Bridge async coroutines to Qt signals:

```python
class QAsyncSignalBridge(QObject):
    finished = Signal(object)
    error = Signal(str)

    def run_async(
        self,
        coro: Coroutine[object, None, T],
        on_success: Callable[[T], None] | None = None,
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        async def _wrapped() -> None:
            try:
                result = await coro
                if on_success:
                    on_success(result)
                else:
                    self.finished.emit(result)
            except Exception as e:
                if on_error:
                    on_error(str(e))
                else:
                    self.error.emit(str(e))

        loop = asyncio.get_event_loop()
        self._task = loop.create_task(_wrapped())
```

### ThreadPoolExecutor for Blocking Libraries

When a library only provides sync API:

```python
class AsyncRecorder(QObject):
    recording_completed = Signal(np.ndarray)

    def __init__(self) -> None:
        super().__init__()
        self._executor = ThreadPoolExecutor(max_workers=1)

    async def start_recording(self) -> None:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(self._executor, self._sync_record)
        self.recording_completed.emit(result)
```

---

## Key Rules

1. **PySide6** (LGPL, no system deps) over PyQt
2. **Never block event loop**: no `subprocess.run()`, no `time.sleep()`, no sync HTTP
3. **qasync** bridges asyncio and Qt event loops
4. **ThreadPoolExecutor** wraps blocking third-party APIs
5. **Typed wrappers** around untyped libraries, enforced via ruff `banned-api`
6. **Signals at class level**, not in `__init__`
7. **camelCase for Qt event handlers** (ignore ruff N802), **snake_case for our slots**

---

## Signal/Slot Conventions

- Define signals at class level (not in `__init__`)
- Connect signals in the component that owns the relationship
- Use typed signals: `Signal(str)`, `Signal(float)`, `Signal(object)`

```python
class AudioManager(QObject):
    volume_changed = Signal(float)
    recording_completed = Signal(np.ndarray)
    recording_failed = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._recorder = AsyncRecorder()
        self._recorder.recording_completed.connect(self.recording_completed)
```

---

## Naming Convention Exception

Qt event handlers use `camelCase` per Qt convention:

```toml
[tool.ruff.lint]
ignore = ["N802"]  # Qt event handlers use camelCase
```

```python
class CustomWidget(QWidget):
    def mousePressEvent(self, event: QMouseEvent) -> None:  # Qt convention
        ...

    def on_button_clicked(self) -> None:  # Our slots use snake_case
        ...
```

---

## Declarative Label → Callback Pattern

Whenever bootstrapping a fixed set of labeled actions — tray menus, button bars, context menus, toolbar items — avoid imperative `addAction`/`addButton` chains. Instead, declare all entries as data at the top of the setup method (where `self` is in scope for type-safe bound-method references) and drive the construction with a generic loop at the bottom.

`"SEPARATOR"` is a `Literal` sentinel: basedpyright rejects any other string in that position, so both the sentinel and the callbacks are fully type-checked.

```python
from typing import Callable, Final, Literal

_SEPARATOR: Final = "SEPARATOR"
_Entry = tuple[str, Callable[[], None]] | Literal["SEPARATOR"]

class ApplicationTrayIcon(QSystemTrayIcon):
    def __init__(self) -> None:
        super().__init__()
        self.setIcon(QIcon("icon.png"))
        self._setup_menu()

    def _setup_menu(self) -> None:
        entries: list[_Entry] = [
            ("Settings", self._open_settings),
            _SEPARATOR,
            ("Quit", QApplication.quit),
        ]

        menu = QMenu()
        for entry in entries:
            if entry is _SEPARATOR:
                menu.addSeparator()
            else:
                label, cb = entry
                menu.addAction(label, cb)
        self.setContextMenu(menu)

    def _open_settings(self) -> None: ...
```

`entries` is the single place to add, remove, or reorder items. The loop is generic boilerplate that never changes. Mistyping `self._poen_settings` is caught by basedpyright at check time — no runtime surprises. The same pattern applies to button bars, context menus, or any other label → callback mapping.

---

## Single Instance Enforcement

```python
class LockManager:
    def __init__(self, lock_path: Path) -> None:
        self._lock_path = lock_path

    def acquire(self) -> Result[None, str]:
        if self._lock_path.exists():
            pid = int(self._lock_path.read_text())
            if self._is_process_running(pid):
                return Err(f"Another instance running (PID {pid})")
            # Stale lock file
        self._lock_path.write_text(str(os.getpid()))
        return Ok(None)

    def release(self) -> None:
        self._lock_path.unlink(missing_ok=True)
```

---

## Keyboard Shortcuts

Customizable via TOML config:

```python
class ActionID(enum.Enum):
    NEW_PROFILE = "new_profile"
    START_PROFILE = "start_profile"

@dataclass
class ActionShortcut:
    id: str
    label: str
    default_key: str

DEFAULT_SHORTCUTS = (
    ActionShortcut(ActionID.NEW_PROFILE.value, "New Profile", "Ctrl+N"),
    ActionShortcut(ActionID.START_PROFILE.value, "Start Profile", "Return"),
)
```

User overrides stored in `~/.config/appname/shortcuts.toml`.

---

## Settings Management

Type-safe QSettings wrapper:

```python
class Settings:
    def __init__(self) -> None:
        self._settings = QSettings(APP_NAME, APP_NAME)
        self._init_defaults()

    def get_str(self, key: str, default: str = "") -> str:
        value = self._settings.value(key, default)
        return str(value) if value is not None else default

    def get_int(self, key: str, default: int = 0) -> int:
        value = self._settings.value(key, default)
        return int(value) if value is not None else default

    def set(self, key: str, value: str | int | bool) -> None:
        self._settings.setValue(key, value)
```

---

## Testing Qt Components

Use `pytest-qt`:

```python
def test_main_window_creates(qtbot: QtBot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.isVisible() is False  # Not shown until .show()

def test_button_click(qtbot: QtBot) -> None:
    widget = MyWidget()
    qtbot.addWidget(widget)
    with qtbot.waitSignal(widget.action_triggered, timeout=1000):
        qtbot.mouseClick(widget.button, Qt.LeftButton)
```

## Routing QML Logs to Python Logger

QML `console.log/info/warn/error` calls print to stderr by default with no structure or log levels. Install a custom Qt message handler before creating the QML engine to route them through Python's `logging` module.

### The Handler

```python
import logging
from PySide6.QtCore import QMessageLogContext, QtMsgType, qInstallMessageHandler

_qt_logger = logging.getLogger("qt.qml")

def _qt_message_handler(msg_type: QtMsgType, context: QMessageLogContext, message: str) -> None:
    file: str = context.file or ""
    line: int = context.line or 0
    location = f" ({file}:{line})" if file else ""
    log_message = f"{message}{location}"

    if msg_type == QtMsgType.QtDebugMsg:
        _qt_logger.debug(log_message)
    elif msg_type == QtMsgType.QtInfoMsg:
        _qt_logger.info(log_message)
    elif msg_type == QtMsgType.QtWarningMsg:
        _qt_logger.warning(log_message)
    else:  # QtCriticalMsg, QtFatalMsg
        _qt_logger.error(log_message)
```

### Install Before QML Engine

```python
qInstallMessageHandler(_qt_message_handler)
engine = QQmlApplicationEngine()
```

Order matters — install before `QQmlApplicationEngine()` so early QML load warnings are captured.

### QML Usage

```qml
Component.onCompleted: {
    console.info("Panel loaded, items: " + listModel.count)
    console.warn("Missing optional property")
    console.error("Failed to load resource")
}
```

### Gotcha: `console.log()` Is Silently Dropped

Qt maps `console.log()` to `QtDebugMsg`, which Qt's own message filtering suppresses **before** the handler is called. The handler never sees it.

| QML call | Qt type | Reaches handler | Recommendation |
|---|---|---|---|
| `console.log()` | `QtDebugMsg` | No | Don't use |
| `console.info()` | `QtInfoMsg` | Yes | Use for debug output |
| `console.warn()` | `QtWarningMsg` | Yes | Recoverable issues |
| `console.error()` | `QtCriticalMsg` | Yes | Errors |

**Always use `console.info()` instead of `console.log()`.**

The logger name `qt.qml` lets you filter or suppress QML messages independently:
```python
logging.getLogger("qt.qml").setLevel(logging.WARNING)  # silence info-level QML noise
```

See the `setting-up-logging` skill for colored stdout/file logging setup that works with this handler.

---

## Platform Integration -  File Dialogs (XDG Desktop Portals)

On Linux, file dialogs use XDG Desktop Portals for native system pickers (with favorites, bookmarks, etc.). The app sets `QT_QPA_PLATFORMTHEME=xdgdesktopportal` at startup if no platform theme is configured.

**Requirements:** `xdg-desktop-portal` + a desktop backend (`xdg-desktop-portal-kde`, `xdg-desktop-portal-gnome`, etc.).

**No code changes needed** — standard `QFileDialog` calls automatically use portals when the platform theme is set. In Flatpak environments, portals are used transparently without any configuration.
