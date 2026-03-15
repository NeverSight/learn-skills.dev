---
name: setting-up-logging
description: "Set up colored logging and stdout output for Python apps and CLI tools using colorlog."
---

# Setting Up Logging

Rotating file logging, colored stdout logging, and colored non-log output. Uses `colorlog` for prefix-only coloring (log prefix is colored, message text stays default).

Copy reusable code from `coding_rules_python/reusable/logging/`.

---

## Key Principle

**File logging is always on** — it's the durable record for post-mortem debugging. Stdout is lost on terminal close; file logs survive.

**Stdout logging** is for modes where no human reads stdout directly. When you launch a GUI app from terminal or run a server in a container, stdout logs are useful — they show real-time output during development and serve as container log transport (Docker/systemd capture stdout).

**CLI tools must NOT use stdout logging** — stdout is the user interface. Log lines mixed into stdout corrupt the output (imagine `mytool | grep something` with log lines). Use `write_info`/`write_error` for user-facing messages instead.

| Mode | File log | Stdout log | Non-log colored output |
|------|----------|------------|------------------------|
| **CLI tool** | Always | Never | `write_info`, `write_error` for user messages |
| **GUI app** | Always | Yes (dev convenience from terminal) | No (no terminal) |
| **Server (FastAPI)** | Always | Yes (container log transport) | No |

---

## When to Use

- **Every app** — `setup_file_logging()` in your entrypoint
- **GUI apps / servers** — also `setup_stdout_logging()` (stdout is not the user interface)
- **CLI tools** — `write_info`/`write_error` for user-facing messages (NOT stdout logging)
- **Suppressing noisy loggers** — `configure_logger_level("httpx", logging.WARNING)`

---

## Typical Patterns

### CLI tool — file logging + colored user output

```python
import logging
from pathlib import Path
from shared.logging import setup_file_logging, configure_logger_level, write_info, write_error

# File logs always on
setup_file_logging(
    log_dir=Path("~/.local/state/myapp/logs").expanduser(),
    app_name="myapp",
)
configure_logger_level("httpx", logging.WARNING)

# User-facing output via write_info/write_error (NOT stdout logging)
write_info("Processing 42 items...")
write_error("Connection failed")
```

### GUI app / server — file logging + stdout logging

```python
import logging
from pathlib import Path
from shared.logging import setup_file_logging, setup_stdout_logging, configure_logger_level

# File logs always on
setup_file_logging(
    log_dir=Path("~/.local/state/myapp/logs").expanduser(),
    app_name="myapp",
)
# Stdout logs for dev convenience (visible when launched from terminal / in containers)
setup_stdout_logging(level=logging.INFO)
configure_logger_level("httpx", logging.WARNING)
```

**Stdout output format (colored):**
```
<green>2025-12-19 00:01:35 [INFO] myapp.core:</green> Processing 42 items
<yellow>2025-12-19 00:01:36 [WARNING] myapp.core:</yellow> Slow response from API
```

**File output format (plain):**
```
2025-12-19 00:01:35 [INFO] myapp.core: Processing 42 items
2025-12-19 00:01:36 [WARNING] myapp.core: Slow response from API
```

**Color scheme (stdout only):**

| Level | Color |
|-------|-------|
| DEBUG | Cyan |
| INFO | Green |
| WARNING | Yellow |
| ERROR | Red |
| CRITICAL | Red on white |

---

## Non-Log Colored Output

For CLI tools — colored messages that are NOT log entries (status messages, results, prompts). This is how CLI tools communicate with the user instead of stdout logging:

```python
from shared.logging import write_info, write_success, write_warning, write_error

write_info("Starting download...")      # Green → stdout
write_success("Download complete!")     # Green → stdout
write_warning("Large file detected")   # Yellow → stdout
write_error("Failed to connect")       # Red → stderr
```

---

## Dependencies

```toml
[project]
dependencies = [
    "colorlog>=6.10.1",
]
```

---

## Files to Copy

Copy the entire `coding_rules_python/reusable/logging/` directory into your project's `shared/logging/`:
- `__init__.py` — public API re-exports
- `logger_setup.py` — `setup_stdout_logging()`, `setup_file_logging()`, `configure_logger_level()`
- `non_log_stdout_output.py` — `write_info()`, `write_success()`, `write_warning()`, `write_error()`
- `README.md` — references this skill

Update import paths after copying (e.g., `from shared.logging import ...`).

---

## QML Log Routing (PySide6)

QML `console.info/warn/error` can be routed through Python's `logging` module via a custom Qt message handler. This integrates QML output with your file and stdout logging setup. The handler logs under the `qt.qml` logger name, so you can filter it independently.

See the `building-qt-apps` skill for the full handler implementation and the `console.log()` gotcha (it's silently dropped by Qt).

---

## API Reference

### `setup_file_logging(log_dir, app_name="app", level=DEBUG, max_bytes=5MB, backup_count=3)`
Add RotatingFileHandler to root logger. Creates `<log_dir>/<app_name>.log`. Always use this — every app needs durable file logs.

### `setup_stdout_logging(level=logging.INFO)`
Add colored StreamHandler to root logger. For GUI apps and servers where stdout is not the user interface. Do NOT use for CLI tools.

### `configure_logger_level(logger_name, level, propagate=True)`
Set a specific logger's level. Use to suppress verbose third-party loggers.

### `write_info(message)` / `write_success(message)`
Green text to stdout.

### `write_warning(message)`
Yellow text to stdout.

### `write_error(message)`
Red text to stderr.
