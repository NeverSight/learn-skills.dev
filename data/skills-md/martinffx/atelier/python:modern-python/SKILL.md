---
name: python:modern-python
description: Modern Python language features and typing patterns. Use when writing type hints, using generics, implementing pattern matching, working with async/await, or leveraging Python 3.10+ features.
user-invocable: false
---

# Modern Python Features

Modern Python 3.10+ language features, type hints, and patterns.

## Type Hints

### Basic Types

```python
def greet(name: str) -> str:
    return f"Hello {name}"

age: int = 25
prices: list[float] = [9.99, 19.99]
mapping: dict[str, int] = {"a": 1}
```

### Union Types (Python 3.10+)

```python
# Modern syntax
def process(value: int | str) -> bool:
    ...

# Optional
def get_user(id: int) -> User | None:
    ...

# Multiple types
Result = int | str | bool
```

### Generic Types

```python
from typing import TypeVar, Generic

T = TypeVar("T")

class Repository(Generic[T]):
    def get(self, id: int) -> T | None:
        ...

    def save(self, entity: T) -> T:
        ...

user_repo = Repository[User]()
```

### Protocol (Structural Typing)

```python
from typing import Protocol

class Drawable(Protocol):
    """Structural type - any class with draw()"""
    def draw(self) -> None:
        ...

def render(obj: Drawable) -> None:
    """Works with any object that has draw()"""
    obj.draw()
```

## Pattern Matching (Python 3.10+)

### Basic Matching

```python
def handle_command(command: str):
    match command:
        case "start":
            start_process()
        case "stop":
            stop_process()
        case "status":
            return get_status()
        case _:
            raise ValueError("Unknown command")
```

### Matching with Values

```python
def handle_http_status(status: int):
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500 | 502 | 503:
            return "Server Error"
        case _:
            return "Unknown"
```

### Structural Pattern Matching

```python
def process_point(point):
    match point:
        case (0, 0):
            return "Origin"
        case (x, 0):
            return f"On X-axis at {x}"
        case (0, y):
            return f"On Y-axis at {y}"
        case (x, y):
            return f"At ({x}, {y})"
```

## Async/Await

### Async Functions

```python
async def fetch_data(url: str) -> dict:
    """Async function"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Call async function
data = await fetch_data("https://api.example.com")
```

### Concurrent Execution

```python
import asyncio

async def process_all(urls: list[str]):
    """Process multiple URLs concurrently"""
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results
```

### Async Context Managers

```python
class AsyncDatabase:
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args):
        await self.disconnect()

async with AsyncDatabase() as db:
    await db.query(...)
```

## Dataclasses and attrs

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5
```

## Walrus Operator

```python
# Assign and use in one expression
if (n := len(items)) > 10:
    print(f"Too many items: {n}")

# In comprehensions
results = [y for x in items if (y := process(x)) is not None]
```

## Modern String Formatting

```python
name = "Alice"
age = 30

# f-strings
message = f"Hello {name}, you are {age} years old"

# f-strings with expressions
message = f"In 5 years you'll be {age + 5}"

# Debug f-strings (Python 3.8+)
print(f"{name=}")  # name='Alice'
```

See references/ for advanced typing, async patterns, and pattern matching.
