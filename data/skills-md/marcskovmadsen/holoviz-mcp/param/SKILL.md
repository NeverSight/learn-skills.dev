---
name: param
description: Use when building Python classes with validated, typed parameters using the Param library. Triggers include creating configuration classes, building reusable components with state, implementing reactive dependencies between parameters, adding type-safe attributes with bounds/constraints, creating testable parameterized classes, or when users mention param.Parameterized, @param.depends, or param.watch.
---

# Param: Declarative Parameters

Create typed, validated class attributes with reactive programming support.

## Hello World Example

```python
# DO always add this to ignore pyright Parameter type annotation warnings
# pyright: reportAssignmentType=false
import param

class Greeter(param.Parameterized):
    """A greeting generator with history tracking."""

    # DON'T use 'name' as parameter - it's reserved in Param
    # DO add type annotations, defaults, and doc strings
    target: str = param.String(default="World", doc="Name to greet")
    greeting: str = param.Selector(default="Hello", objects=["Hello", "Hi", "Hey"])
    count: int = param.Integer(default=1, bounds=(1, 10), doc="Repetitions")
    history: list = param.List(default=[], doc="Greeting history")

    # DO use @param.depends (watch=False) for computed values with no side effects
    @param.depends("target", "greeting", "count")
    def message(self) -> str:
        """Computed value - recalculates when dependencies change."""
        return " ".join([f"{self.greeting}, {self.target}!"] * self.count)

    # DO use @param.depends(watch=True) for side effects (state updates, I/O, etc.)
    @param.depends("target", watch=True)
    def _track_changes(self):
        """Side effect - automatically runs when target changes."""
        self.history = self.history + [self.target]


# Usage
greeter = Greeter(target="Alice")
print(greeter.message())      # "Hello, Alice!"

greeter.target = "Bob"
print(greeter.history)        # ["Bob"] - tracked the change

greeter.greeting = "Hi"
greeter.count = 2
print(greeter.message())      # "Hi, Bob! Hi, Bob!"
```

## param.Parameterized (Production) vs param.rx/bind (Exploration)

Use `param.Parameterized` for production code. Use `param.rx`/`param.bind` only for notebook exploration:

## Core Parameter Types

```python
import datetime
import param
import numpy as np
import pandas as pd

class AllParameterTypes(param.Parameterized):
    # Strings
    name: str = param.String(default="unnamed", doc="Item name")
    color: str = param.Color(default="#FF5733", doc="Hex color or named color")

    # Numbers
    count: int = param.Integer(default=10, bounds=(0, 1000))
    rate: float = param.Number(default=0.5, bounds=(0.0, 1.0), step=0.1)
    magnitude: float = param.Magnitude(default=0.5)  # Always 0.0-1.0

    # Boolean
    enabled: bool = param.Boolean(default=True)

    # Selectors
    mode: str = param.Selector(default="auto", objects=["auto", "manual", "hybrid"])
    tags: list = param.ListSelector(default=["a"], objects=["a", "b", "c"])

    # Collections
    items: list = param.List(default=[], item_type=str)
    config: dict = param.Dict(default={})
    data: np.ndarray = param.Array(default=np.array([]))
    df: pd.DataFrame = param.DataFrame(default=pd.DataFrame())

    # Dates
    date: datetime.date = param.CalendarDate(default=datetime.date.today())
    date_range: tuple = param.CalendarDateRange(default=None, doc="Optional date range")
    value_range: tuple = param.Range(default=(0, 10), bounds=(0, 100))

    # Files
    input_file: str = param.Filename(default=None, doc="Input file path")
    output_dir: str = param.Foldername(default=None, doc="Output directory")

    # Actions and Events
    submit: bool = param.Event(doc="Trigger processing")
    callback: callable = param.Callable(default=None, doc="Processing function")

    # Class instances
    nested: param.Parameterized = param.ClassSelector(class_=param.Parameterized, default=None)
```

## Parameter Metadata

```python
import param

class DocumentedModel(param.Parameterized):
    threshold = param.Number(
        default=0.5,
        bounds=(0, 1),           # Hard limits - enforced
        softbounds=(0.2, 0.8),   # Suggested range for UIs
        step=0.05,               # Increment hint for UIs
        doc="Classification threshold",
        label="Threshold (%)",   # Display name
        precedence=1,            # Order in UIs (lower = first)
        constant=False,          # If True, immutable after init
        readonly=False,          # If True, never settable by user
        allow_None=False,        # If True, None is valid
        instantiate=False,       # If True, deep copy default per instance
        per_instance=True,       # If True, separate Parameter object per instance
    )
```

### Dynamic Defaults with default_factory

```python
import uuid
import datetime
import param

class TrackedItem(param.Parameterized):
    id: str = param.String(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime.datetime = param.Date(default_factory=datetime.datetime.now)
```

## Dependencies with @param.depends

### watch=False: Declare Dependencies for External Frameworks

```python
import param

class DataView(param.Parameterized):
    source: str = param.Selector(default="A", objects=["A", "B", "C"])
    limit: int = param.Integer(default=10, bounds=(1, 100))

    @param.depends("source", "limit")
    def get_data(self) -> list:
        """Called by Panel/HoloViews when dependencies change."""
        return [f"{self.source}_{i}" for i in range(self.limit)]
```

### watch=True: Execute Side Effects Automatically

```python
import param

class CountrySelector(param.Parameterized):
    """Dependent parameters pattern - updates country list when continent changes."""

    _countries = {
        "Europe": ["France", "Germany", "Spain"],
        "Asia": ["China", "Japan", "India"],
        "Americas": ["USA", "Brazil", "Canada"],
    }

    continent: str = param.Selector(default="Europe", objects=["Europe", "Asia", "Americas"])
    country: str = param.Selector(default="France", objects=["France", "Germany", "Spain"])

    @param.depends("continent", watch=True, on_init=True)
    def _update_countries(self):
        """Automatically update country options when continent changes."""
        countries = self._countries[self.continent]
        self.param.country.objects = countries
        if self.country not in countries:
            self.country = countries[0]
```

### on_init=True: Run on Instantiation

Always use `on_init=True` when a watcher should run during `__init__`:

```python
@param.depends("config_path", watch=True, on_init=True)
def _load_config(self):
    """Load config on init AND when path changes."""
    if self.config_path:
        self.config = load_config(self.config_path)
```

## Watchers (Low-level API)

```python
import param

class WatcherExample(param.Parameterized):
    value: int = param.Integer(default=0)
    history: list = param.List(default=[])

    def __init__(self, **params):
        super().__init__(**params)
        # Watch with callback receiving Event objects
        self.param.watch(self._on_value_change, ["value"])

    def _on_value_change(self, event):
        """event.old, event.new, event.name, event.obj available."""
        self.history.append({"old": event.old, "new": event.new})


# Alternative: watch_values passes values as kwargs
model = WatcherExample()
model.param.watch_values(lambda value: print(f"Value: {value}"), ["value"])
```

## Event Parameter for Triggers

```python
import param

class Processor(param.Parameterized):
    data: list = param.List(default=[])
    process: bool = param.Event(doc="Click to process")
    result: str = param.String(default="")

    @param.depends("process", watch=True)
    def _on_process(self):
        """Triggered when process event fires."""
        self.result = f"Processed {len(self.data)} items"


processor = Processor(data=[1, 2, 3])
processor.process = True  # Triggers _on_process, then resets to False
print(processor.result)  # "Processed 3 items"
```

## Parameter References (allow_refs)

```python
import param

class Source(param.Parameterized):
    value: int = param.Integer(default=10)

class Consumer(param.Parameterized):
    # allow_refs=True lets this parameter reference another Parameter
    input_value: int = param.Integer(default=0, allow_refs=True)

source = Source()
consumer = Consumer(input_value=source.param.value)

print(consumer.input_value)  # 10
source.value = 20
print(consumer.input_value)  # 20 - automatically updated
```

## param.rx and param.bind (Exploration Only)

Use for notebooks and prototyping. Refactor to Parameterized for production:

```python
import param
from param import rx

# param.rx - reactive values
data = rx([1, 2, 3])
doubled = data.rx.pipe(lambda d: [x * 2 for x in d])  # [2, 4, 6]
data.rx.value = [10, 20]  # doubled becomes [20, 40]

# param.bind - bind function to parameters
class Config(param.Parameterized):
    x: int = param.Integer(default=5)
    y: int = param.Integer(default=10)

config = Config()
result = param.bind(lambda a, b: a * b, config.param.x, config.param.y)
print(result())  # 50
config.x = 7
print(result())  # 70
```

## Testing Parameterized Classes

```python
import pytest
import param

class Calculator(param.Parameterized):
    a: float = param.Number(default=0)
    b: float = param.Number(default=0)
    operation: str = param.Selector(default="add", objects=["add", "multiply"])

    @param.depends("a", "b", "operation")
    def result(self) -> float:
        return self.a + self.b if self.operation == "add" else self.a * self.b


def test_defaults():
    calc = Calculator()
    assert calc.a == 0 and calc.operation == "add"

def test_computed_values():
    assert Calculator(a=5, b=3).result() == 8
    assert Calculator(a=5, b=3, operation="multiply").result() == 15

def test_reactivity():
    calc = Calculator(a=2, b=3)
    assert calc.result() == 5
    calc.a = 10
    assert calc.result() == 13

def test_validation():
    with pytest.raises(ValueError):
        Calculator(a="not a number")
    with pytest.raises(ValueError):
        Calculator(operation="invalid")
```

## Best Practices

### DO

- Use Parameterized classes for production code
- Add type annotations for IDE support
- Add `# pyright: reportAssignmentType=false` at the top of files with type-annotated Parameters (Param's descriptors conflict with static type checkers)
- Write pytest tests for all reactive methods
- Use `watch=True` for side effects, `watch=False` for computed values
- Use `on_init=True` when watchers should run during initialization
- Use `doc` parameter for documentation
- Use `bounds` for numeric constraints

### DON'T

- Use `name` as a parameter name - it's reserved (use `title`, `label`, etc.)
- Use param.bind/rx for production code that needs testing
- Modify parameters inside their own `watch=True` callbacks (causes loops)
- Forget `on_init=True` when initialization logic depends on parameter values
- Use mutable defaults without `instantiate=True` or `default_factory`

## Common Patterns

### Configuration Object

```python
import param

class AppConfig(param.Parameterized):
    debug: bool = param.Boolean(default=False)
    log_level: str = param.Selector(default="INFO", objects=["DEBUG", "INFO", "WARNING", "ERROR"])
    max_workers: int = param.Integer(default=4, bounds=(1, 32))

config = AppConfig()
config.param.update(debug=True, log_level="DEBUG")  # Batch update, watchers called once
```

### Environment Variable Defaults

```python
import os
import param

env = os.environ.get

class AppSettings(param.Parameterized):
    database_url = param.String(default=env("DATABASE_URL", ""), doc="Database connection URL")
    secret_key = param.String(default=env("SECRET_KEY", ""), doc="Secret key for JWT tokens")
    debug = param.Boolean(default=env("DEBUG", "false").lower() == "true")
    allowed_hosts = param.List(default=env("ALLOWED_HOSTS", "localhost").split(","), item_type=str)

settings = AppSettings()
```

Note: Environment variables are read at class definition time. For dynamic reloading, read them in `__init__` or use `default_factory`.

### Batch Updates

```python
# Update multiple parameters atomically
with config.param.update(debug=True, log_level="DEBUG"):
    pass  # Changes applied, watchers called once at end

# Or without context manager
config.param.update(debug=True, log_level="DEBUG")
```
### Serialization

```python
import param

class User(param.Parameterized):
    age: int = param.Integer(default=0)
    email: str = param.String(default="")

user = User(age=25, email="test@example.com")
user.param.values()                    # {'name': 'User00001', 'age': 25, 'email': '...'}
user.param.values(onlychanged=True)    # {'age': 25, 'email': '...'}
json_str = user.param.serialize_parameters()
User.param.deserialize_parameters(json_str)  # Returns dict for constructor
```

## Pydantic Migration

Unlike Pydantic, Param does **not** auto-coerce types. Convert values explicitly:

```python
import param

class ParamUser(param.Parameterized):
    age: int = param.Integer()

ParamUser(age=25)    # Works
ParamUser(age="25")  # Raises ValueError - no coercion

# Convert when migrating from Pydantic
data = {"age": "25"}
ParamUser(age=int(data["age"]))
```

## Cross-Field Validation

Use `@param.depends(watch=True, on_init=True)` to validate across multiple parameters:

```python
import re

import param


class MinLengthString(param.String):
    """String with minimum length validation."""

    __slots__ = ["min_length"]

    def __init__(self, min_length=0, **params):
        self.min_length = min_length
        super().__init__(**params)

    def _validate_value(self, val, allow_None):
        super()._validate_value(val, allow_None)
        if val and len(val) < self.min_length:
            raise ValueError(f"Parameter {self.name!r} must be at least {self.min_length} characters.")


class EmailString(param.String):
    """String that must be a valid email format."""

    def _validate_value(self, val, allow_None):
        super()._validate_value(val, allow_None)
        if val and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", val):
            raise ValueError(f"Parameter {self.name!r} must be a valid email, not {val!r}.")


class UserRegistration(param.Parameterized):
    """User registration with cross-field validation."""

    username: str = MinLengthString(min_length=3, doc="Username (min 3 characters)")
    email: str = EmailString(doc="Email address")
    password: str = param.String(doc="Password")
    subscription_tier: str = param.Selector(default="free", objects=["free", "pro", "enterprise"])

    @param.depends("password", "subscription_tier", watch=True, on_init=True)
    def _validate_password(self):
        """Validate password complexity based on subscription tier."""
        if not self.password:
            return

        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters")

        if self.subscription_tier == "enterprise" and not re.search(r"[A-Z]", self.password):
            raise ValueError("Enterprise accounts require uppercase letters")


# Usage - validation runs on init and parameter changes
user = UserRegistration(
    username="alice", email="alice@example.com",
    password="SecurePass123", subscription_tier="enterprise",
)
UserRegistration(username="bob", password="lowercase", subscription_tier="enterprise")  # Raises ValueError
```

## Custom Parameter Types

Subclass and override `_validate_value` for reusable parameters with custom validation:

```python
import param

class EvenInteger(param.Integer):
    """Integer that must be even."""
    def _validate_value(self, val, allow_None):
        super()._validate_value(val, allow_None)  # Always call parent first
        if val is not None and val % 2 != 0:
            raise ValueError(f"EvenInteger parameter {self.name!r} must be even, not {val!r}.")

class PositiveNumber(param.Number):
    """Number that must be > 0."""
    def _validate_value(self, val, allow_None):
        super()._validate_value(val, allow_None)
        if val is not None and val <= 0:
            raise ValueError(f"PositiveNumber parameter {self.name!r} must be positive, not {val!r}.")

class GridConfig(param.Parameterized):
    rows: int = EvenInteger(default=4)
    spacing: float = PositiveNumber(default=1.0)

config = GridConfig(rows=6, spacing=2.5)
config.rows = 5     # Raises ValueError: must be even
config.spacing = -1  # Raises ValueError: must be positive
```

## Resources

- [Param Documentation](https://param.holoviz.org)
- [Param User Guide](https://param.holoviz.org/user_guide/index.html)
- [Parameter Types Reference](https://param.holoviz.org/user_guide/Parameter_Types.html)
- [Dependencies and Watchers](https://param.holoviz.org/user_guide/Dependencies_and_Watchers.html)
- [Specialized Parameter Types](https://param.holoviz.org/user_guide/Parameters.html#specialized-parameter-types)
