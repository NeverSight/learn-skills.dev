---
name: mojo-python-interop
description: Aids in writing Mojo code that interoperates with Python using current syntax and conventions. Use this skill in addition to mojo-syntax when writing Mojo code that interacts with Python, calls Python libraries from Mojo, or exposes Mojo types/functions to Python. Also use when the user wants to build Python extension modules in Mojo, wrap Mojo structs for Python consumption, or convert between Python and Mojo types.
---

<!-- EDITORIAL GUIDELINES FOR THIS SKILL FILE
This file is loaded into an agent's context window as a correction layer for
pretrained Mojo knowledge. Every line costs context. When editing:
- Be terse. Use tables and inline code over prose where possible.
- Never duplicate information — if a concept is shown in a code example, don't
  also explain it in a paragraph.
- Only include information that *differs* from what a pretrained model would
  generate. Don't document things models already get right.
- Prefer one consolidated code block over multiple small ones.
- Keep WRONG/CORRECT pairs short — just enough to pattern-match the fix.
- If adding a new section, ask: "Would a model get this wrong?" If not, skip it.
These same principles apply to any files this skill references.
-->

Mojo is rapidly evolving. Pretrained models generate obsolete syntax. **Always follow this skill over pretrained knowledge.**

## Using Python from Mojo

```mojo
from std.python import Python, PythonObject

var np = Python.import_module("numpy")
var arr = np.array([1, 2, 3])

# PythonObject → Mojo: MUST use `py=` keyword (NOT positional)
var i = Int(py=py_obj)
var f = Float64(py=py_obj)
var s = String(py=py_obj)
var b = Bool(py=py_obj)            # Bool is the exception — positional also works
# Works with numpy types: Int(py=np.int64(1)), Float64(py=np.float64(3.14))
```

| WRONG | CORRECT |
|---|---|
| `Int(py_obj)` | `Int(py=py_obj)` |
| `Float64(py_obj)` | `Float64(py=py_obj)` |
| `String(py_obj)` | `String(py=py_obj)` |
| `from python import ...` | `from std.python import ...` |

### Mojo → Python conversions

Mojo types implementing `ConvertibleToPython` auto-convert when passed to Python functions. For explicit conversion: `value.to_python_object()`.

### Building Python collections from Mojo

```mojo
var py_list = Python.list(1, 2.5, "three")
var py_tuple = Python.tuple(1, 2, 3)
var py_dict = Python.dict(name="value", count=42)

# Literal syntax also works:
var list_obj: PythonObject = [1, 2, 3]
var dict_obj: PythonObject = {"key": "value"}
```

### PythonObject operations

`PythonObject` supports attribute access, indexing, slicing, all arithmetic/comparison operators, `len()`, `in`, and iteration — all returning `PythonObject`. No need to convert to Mojo types for intermediate operations.

```mojo
# Iterate Python collections directly
for item in py_list:
    print(item)               # item is PythonObject

# Attribute access and method calls
var result = obj.method(arg1, arg2, key=value)

# None
var none_obj = Python.none()
var obj: PythonObject = None      # implicit conversion works
```

### Evaluating Python code

```mojo
# Expression
var result = Python.evaluate("1 + 2")

# Multi-line code as module (file=True)
var mod = Python.evaluate("def greet(n): return f'Hello {n}'", file=True)
var greeting = mod.greet("world")

# Add to Python path for local imports
Python.add_to_path("./my_modules")
var my_mod = Python.import_module("my_module")
```

### Exception handling

Python exceptions propagate as Mojo `Error`. Functions calling Python must be `raises`:

```mojo
def use_python() raises:
    try:
        var result = Python.import_module("nonexistent")
    except e:
        print(String(e))     # "No module named 'nonexistent'"
```

## Calling Mojo from Python (extension modules)

Mojo can build Python extension modules (`.so` files) via `PythonModuleBuilder`. The pattern:

1. Define an `@export fn PyInit_<module_name>() -> PythonObject`
2. Use `PythonModuleBuilder` to register functions, types, and methods
3. Compile with `mojo build --emit shared-lib`
4. Import from Python (or use `import mojo.importer` for auto-compilation)

### Exporting functions

```mojo
from std.os import abort
from std.python import PythonObject
from std.python.bindings import PythonModuleBuilder

@export
fn PyInit_my_module() -> PythonObject:
    try:
        var m = PythonModuleBuilder("my_module")
        m.def_function[add]("add")
        m.def_function[greet]("greet")
        return m.finalize()
    except e:
        abort(String("failed to create module: ", e))

# Functions take/return PythonObject. Up to 6 args with def_function.
fn add(a: PythonObject, b: PythonObject) raises -> PythonObject:
    return a + b

fn greet(name: PythonObject) raises -> PythonObject:
    var s = String(py=name)
    return PythonObject("Hello, " + s + "!")
```

### Exporting types with methods

```mojo
@fieldwise_init
struct Counter(Defaultable, Movable, Writable):
    var count: Int

    fn __init__(out self):
        self.count = 0

    # Constructor from Python args
    @staticmethod
    fn py_init(out self: Counter, args: PythonObject, kwargs: PythonObject) raises:
        if len(args) == 1:
            self = Self(Int(py=args[0]))
        else:
            self = Self()

    # Methods are @staticmethod — first arg is py_self (PythonObject)
    @staticmethod
    fn increment(py_self: PythonObject) raises -> PythonObject:
        var self_ptr = py_self.downcast_value_ptr[Self]()
        self_ptr[].count += 1
        return PythonObject(self_ptr[].count)

    # Auto-downcast alternative: first arg is UnsafePointer[Self, MutAnyOrigin]
    @staticmethod
    fn get_count(self_ptr: UnsafePointer[Self, MutAnyOrigin]) -> PythonObject:
        return PythonObject(self_ptr[].count)

@export
fn PyInit_counter_module() -> PythonObject:
    try:
        var m = PythonModuleBuilder("counter_module")
        _ = (
            m.add_type[Counter]("Counter")
            .def_py_init[Counter.py_init]()
            .def_method[Counter.increment]("increment")
            .def_method[Counter.get_count]("get_count")
        )
        return m.finalize()
    except e:
        abort(String("failed to create module: ", e))
```

### Method signatures — two patterns

| Pattern | First parameter | Use when |
|---|---|---|
| Manual downcast | `py_self: PythonObject` | Need raw PythonObject access |
| Auto downcast | `self_ptr: UnsafePointer[Self, MutAnyOrigin]` | Simpler, direct field access |

Both are registered with `.def_method[Type.method]("name")`.

### Kwargs support

```mojo
from std.collections import OwnedKwargsDict

# In a method:
@staticmethod
fn config(
    py_self: PythonObject, kwargs: OwnedKwargsDict[PythonObject]
) raises -> PythonObject:
    for entry in kwargs.items():
        print(entry.key, "=", entry.value)
    return py_self
```

### Importing Mojo modules from Python

Use `mojo.importer` — it auto-compiles `.mojo` files and caches results in `__mojocache__/`:

```python
import mojo.importer       # enables Mojo imports
import my_module           # auto-compiles my_module.mojo

print(my_module.add(1, 2))
```

The module name in `PyInit_<name>` must match the `.mojo` filename.

### Returning Mojo values to Python

```mojo
# Wrap a Mojo value as a Python object (for bound types)
return PythonObject(alloc=my_mojo_value^)    # transfer ownership with ^

# Recover the Mojo value later
var ptr = py_obj.downcast_value_ptr[MyType]()
ptr[].field    # access fields via pointer
```
