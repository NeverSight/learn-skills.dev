---
name: writing-python-code
description: "Core Python standards: basedpyright strict typing, Result-based error handling, async patterns, security, code style. Use when writing or editing any Python code."
---

# Writing Python Code

All Python code follows the pit-of-success philosophy: strict types, Result-based error handling, modern tooling.

---

## Type System

### basedpyright Configuration

```toml
[tool.basedpyright]
pythonVersion = "3.14"
typeCheckingMode = "strict"
reportAny = "error"
reportImplicitStringConcatenation = "none"
reportUnusedCallResult = "none"
reportUnnecessaryIsInstance = "none"
```

Additional strict options (for medium-big projects):

```toml
reportExplicitAny = "error"
reportUnnecessaryTypeIgnoreComment = "error"
reportMissingModuleSource = "error"
reportPrivateUsage = "error"
reportOptionalMemberAccess = "error"
reportOptionalCall = "error"
reportAttributeAccessIssue = "error"
```

### Banned Patterns

| Banned | Use Instead |
|--------|-------------|
| `Any` | `object` for top type, `Protocol` for duck typing |
| `typing.cast()` | `isinstance`, `TypeIs`, pattern matching |
| `# type: ignore` without rationale | `# type: ignore[specific-code]  # rationale: <reason>` |
| Raw `dict` in business logic | `msgspec.Struct`, `dataclass`, or `TypedDict` |
| Implicit return types | Explicit annotation on every function |

### Type Patterns

**External data** → `msgspec.Struct`:

```python
import msgspec

class UserConfig(msgspec.Struct):
    name: str
    port: int
    debug: bool = False

# JSON → typed object (validates at decode time)
config = msgspec.json.decode(raw_bytes, type=UserConfig)

# Dict/YAML → typed object
config = msgspec.convert(raw_dict, type=UserConfig)
```

`TypedDict` is still valid when dict compatibility is needed (e.g., `**unpacking`, APIs expecting dicts).

**Domain objects** → `dataclass`:

```python
@dataclass(slots=True)
class Profile:
    name: str
    version: str
    active: bool = True
```

**Duck typing** → `Protocol`:

```python
class Renderable(Protocol):
    def render(self) -> str: ...
```

**Constants** → `Final`:

```python
MAX_RETRIES: Final = 3
CONFIG_PATH: Final[Path] = Path("~/.config/app")
```

### Handling `Any` at Library Boundaries

**0. Typed deserialization (for external data):**

`msgspec.json.decode(data, type=MyStruct)` eliminates `Any` for JSON/API responses — the return type is `MyStruct`, not `Any`. Use this before reaching for wrappers when the boundary is data deserialization.

**1. Typed wrappers (preferred for library APIs):**

```python
class WhisperModelWrapper:
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

Enforce wrapper usage via ruff:

```toml
[tool.ruff.lint.flake8-tidy-imports.banned-api]
"faster_whisper" = { msg = "Use src/wrappers/whisper_wrapper instead" }
```

**2. Type stubs** in `src/stubs/`:

```python
# src/stubs/some_library.pyi
def some_function(arg: str) -> list[int]: ...
```

Configure: `stubPath = "src/stubs"` in basedpyright config.

**3. Inline type narrowing** for one-off cases:

```python
raw_value = untyped_lib.get_value()  # returns Any
assert isinstance(raw_value, str)    # narrows to str
```

### TypeIs Guards

> **Note:** `TypeIs` guards are unnecessary for `msgspec`-decoded data (already fully typed). Use them for narrowing in-memory objects of unknown type.

```python
from typing import TypeIs, TypedDict, Required

class ValidResponse(TypedDict):
    status: Required[str]
    data: Required[dict[str, object]]

def is_valid_response(obj: object) -> TypeIs[ValidResponse]:
    return (
        isinstance(obj, dict)
        and isinstance(obj.get("status"), str)
        and isinstance(obj.get("data"), dict)
    )

def process(response: object) -> Result[str, str]:
    if not is_valid_response(response):
        return Err("Invalid response format")
    return Ok(response["data"]["key"])  # type-safe access
```

### Pattern Matching for Type Safety

```python
@dataclass
class Success:
    value: str

@dataclass
class Failure:
    error: str
    code: int

type Outcome = Success | Failure

def handle(outcome: Outcome) -> str:
    match outcome:
        case Success(value=v):
            return f"OK: {v}"
        case Failure(error=e, code=c):
            return f"Error {c}: {e}"
```

### `# type: ignore` Policy

Every `# type: ignore` must have a specific error code and rationale:

```python
# BAD
result = some_call()  # type: ignore

# GOOD
result = some_call()  # type: ignore[no-any-return]  # rationale: lib returns Any, validated below
assert isinstance(result, ExpectedType)
```

### TYPE_CHECKING Guard

For imports that cause circular dependencies or are only needed for annotations:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.managers.audio_manager import AudioManager

class TranscriptionService:
    def __init__(self, audio: "AudioManager") -> None: ...
```

---

## Error Handling

Errors are values, not exceptions. Use `Result[T, E]` from `rusty-results` for expected failures.

### Decision Table

| Situation | Use |
|-----------|-----|
| File not found, network error, invalid input | `Result[T, E]` |
| User provided bad data | `Result[T, E]` |
| Third-party library raised | Catch at boundary → `Result[T, E]` |
| Invariant violated (should never happen) | `raise` exception |
| Invalid program state (bug) | `raise` exception |

### Pattern

```python
from rusty_results import Result, Ok, Err

def load_config(path: Path) -> Result[Config, str]:
    if not path.exists():
        return Err(f"Config not found: {path}")
    try:
        data = json.loads(path.read_text())
        return Ok(Config(**data))
    except (json.JSONDecodeError, OSError) as e:
        return Err(f"Failed to load: {e}")
```

### Rules

1. **Early returns** — handle error first, keep success path linear:
   ```python
   result = load_data(path)
   if result.is_err:
       return Err(f"Cannot proceed: {result.unwrap_err()}")
   data = result.unwrap()
   ```

2. **Three error boundaries:**
   - Library: catch third-party exceptions → Result
   - Component: each subsystem returns Result to caller
   - Global: UI/CLI top-level catches everything, shows user message

3. **Never swallow errors** — no `except: pass`, no ignored Results. Every `Result[T, E]` must be checked — at minimum log the error + show toast/alert in GUI or print to CLI.

4. **Cleanup on failure** — if multi-step operation fails midway, clean up partial state

5. **Custom error types** for complex domains:
   ```python
   @dataclass
   class ConfigError:
       path: Path
       reason: str
       line: int | None = None
   ```

6. Handle received error values gracefully: show UI warning, or log, or do early return or propagate with context

### Async Task Boundaries

Any coroutine launched via `asyncio.ensure_future()` or `create_task()` is a **fire-and-forget boundary**. If an exception escapes, nobody retrieves it and the UI gets stuck in an intermediate state (e.g. "processing" forever).

**Mandatory pattern:** wrap the entire coroutine body in `try/except Exception` as a safety net:

```python
async def _do_work(self, path: Path) -> None:
    try:
        await self._do_work_inner(path)
    except Exception as exc:
        logger.exception("Unexpected error for %s", path)
        self._set_error_state(path, f"Unexpected error: {exc}")
```

The inner method handles expected errors (Result checks, specific exceptions). The outer method guarantees the UI always transitions to a terminal state.

### CLI Error Boundary

```python
def main() -> int:
    result = run_app()
    if result.is_err:
        typer.echo(f"Error: {result.unwrap_err()}", err=True)
        return 1
    return 0
```

---

## Async Patterns

### When to Use

| Use async | Don't use async |
|-----------|-----------------|
| File I/O | Pure data transformations |
| Network requests | Simple calculations |
| Subprocess execution | In-memory operations |
| Operations >100ms | Quick lookups |
| Parallel I/O operations | Sequential pure logic |

### HTTP Requests

```python
async def fetch_data(url: str) -> Result[bytes, str]:
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=30.0)
            resp.raise_for_status()
            return Ok(resp.content)
    except httpx.HTTPError as e:
        return Err(f"HTTP error: {e}")
```

### Subprocess Execution

```python
async def run_command(args: list[str]) -> Result[str, str]:
    try:
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            return Err(f"Command failed: {stderr.decode()}")
        return Ok(stdout.decode())
    except FileNotFoundError:
        return Err(f"Command not found: {args[0]}")
```

### Concurrent Operations

```python
async def fetch_all(urls: list[str]) -> list[Result[bytes, str]]:
    return await asyncio.gather(*(fetch_data(url) for url in urls))
```

### Timeouts

```python
async def fetch_with_timeout(url: str) -> Result[bytes, str]:
    try:
        async with asyncio.timeout(10):
            return await fetch_data(url)
    except TimeoutError:
        return Err(f"Timeout fetching {url}")
```

### Async Rules

1. **Never** call `subprocess.run()`, `time.sleep()`, or synchronous HTTP in async context
2. **Never** use `shell=True` in subprocess calls
3. **Always** use `asyncio.create_subprocess_exec()` for subprocesses
4. **Always** use `async with` for resource management (HTTP clients, file handles)
5. **Never** mix sync and async in the same call chain
6. **Always** handle `TimeoutError` for operations that may hang

---

## Code Style

| Rule | Value |
|------|-------|
| Line length | 120 |
| Indentation | 4 spaces |
| Quotes | Double quotes (single only to avoid escaping) |
| Import order | stdlib → third-party → local (auto-sorted by ruff) |

### Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Modules, functions, variables | `snake_case` | `load_config`, `user_name` |
| Classes, TypedDicts | `PascalCase` | `ProfileManager`, `UserConfig` |
| Constants | `UPPER_SNAKE` | `MAX_RETRIES`, `DEFAULT_PORT` |
| Private | `_prefix` | `_internal_state` |

### Documentation

Google-style docstrings on public APIs. Comments explain **why**, not **what**.

---

## Preconditions & Validation

Validate at subsystem entry points. Fail fast. Check permissions, external deps, config validity, complex input arguments or other data or value ranges before proceeding with business logic.

---

## Architecture

```
Presentation (Qt GUI / CLI / API)
        |
        v
Domain (Managers, Models, Business Rules)
        |
        v
Utilities (Helpers, Wrappers, Common)
```

- Dependencies flow **downward only**
- UI is a **plugin** — adding CLI, GUI, or API should not change business logic
- Domain never imports from presentation

---

## Security

- **No `shell=True`** in subprocess calls
- **Validate paths** (symlink-aware):
  ```python
  def is_safe_path(path: Path, base: Path) -> bool:
      try:
          resolved = path.resolve(strict=True)
          return resolved.is_relative_to(base.resolve(strict=True))
      except (OSError, ValueError):
          return False
  ```
- **No hardcoded secrets** — use environment variables or dotenv
- **Input validation** at system boundaries
- **Never interpolate user input** into subprocess commands
- **Cleanup on failure** — if multi-step operation fails midway, clean up partial state

---

## Performance

- Clear code first, optimize only with profiling data
- `__slots__` on frequently instantiated dataclasses
- Batch I/O operations (don't read files one by one in a loop)
- Lazy loading for expensive resources (load on first use, not import time)
- Concurrent I/O with `asyncio.gather()`

---

## Logging

```python
import colorlog

def get_logger(name: str) -> logging.Logger:
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(name)s: %(message)s"
    ))
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
```

Usage: `logger = get_logger(__name__)`

---

## Jinja2 Templating

Use when generating text output (HTML, configs, reports, markdown):

---

## Tooling

| Tool | Purpose |
|------|---------|
| `uv` | Package management, script execution |
| `basedpyright` | Type checking (strict) |
| `ruff` | Lint + format |
| `pytest` | Testing |
| `rusty-results` | Result[T, E] pattern |
| `typer` | CLI framework (preferred) |
| `argparse` | CLI only for stdlib-only scripts |
| `PySide6` | GUI (no system deps) |
| `httpx` | HTTP (async) |
| `msgspec` | External data validation + parsing |
| `Jinja2` | Text output generation |

**Run `uv run poe lint_full` continuously**, not just at the end.

---

## Git Conventions

Commit format: `<type>(<scope>): <subject>`

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

Pre-commit: `uv run poe lint_full` passes, tests pass, public APIs have docstrings.
