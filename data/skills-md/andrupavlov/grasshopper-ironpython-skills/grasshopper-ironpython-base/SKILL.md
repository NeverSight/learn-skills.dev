---
name: grasshopper-ironpython-base
description: Write IronPython 2.7 scripts for Rhino Grasshopper components. Covers syntax constraints, Rhino.Geometry and Grasshopper APIs, DataTree operations, sc.sticky state, error handling, and component structure. Use when creating or editing .py files in the Gh/ directory, writing Grasshopper Python nodes, or working with Rhino geometry.
rhino_version: "7"
---

# Grasshopper IronPython 2.7

> **Target platform:** Rhinoceros 7 + Grasshopper 1 with the built-in IronPython 2.7 interpreter.
> All API signatures, return types, and method names in this skill are verified against the
> [RhinoCommon 7.x SDK](https://developer.rhino3d.com/api/rhinocommon/?version=7.x).
> Rhino 8 ships with **both** IronPython 2.7 (legacy) and CPython 3 — if you are targeting Rhino 8
> CPython, many constraints in the Hard Constraints section do not apply.

## Hard Constraints (IronPython 2.7)

These will cause **runtime errors** — never use them:

| Forbidden                               | Use instead                                  |
| --------------------------------------- | -------------------------------------------- |
| `f"text {var}"`                         | `"text {}".format(var)` or `"text %s" % var` |
| `:=` (walrus)                           | separate assignment                          |
| Type hints `def fn(x: int) -> str:`     | `def fn(x):` with docstring                  |
| `pathlib`                               | `os.path`                                    |
| `dataclasses`                           | plain `class Foo(object):`                   |
| `enum.Enum`                             | module-level constants                       |
| `dict / list comprehension` with walrus | standard comprehension                       |
| `yield from`                            | explicit loop with `yield`                   |
| `nonlocal`                              | mutable container workaround                 |
| `super()` without args                  | `super(ClassName, self)`                     |
| `{**d1, **d2}` dict merge               | `d = dict(d1); d.update(d2)`                 |

Additional notes:
- `print()` works but is **not** for primary output — use GH output params
- `xrange()` is available (use instead of `range()` for large iterations)
- Use `(object)` as base class: `class Foo(object):`
- String `.format()` uses positional `{0}`, `{1}` or auto `{}`
- File I/O: always `open(path, 'rb')` / `open(path, 'wb')` with `.encode('utf-8')` / `.decode('utf-8')`

## Component File Structure

Every `.py` script follows this order:

```python
"""
GH Python (IronPython)
Description: <what this component does>

Inputs:
    param_name : Type — description
    ...

Outputs:
    param_name : Type — description
    ...
"""

import Rhino.Geometry as rg
import Grasshopper as gh
import System
# ... other imports ...

ghenv.Component.Message = "ComponentName v0.01"

# CONSTANTS
TOLERANCE = 0.01
STICKY_KEY = "component_data"

# CLASSES (if needed)
class MyProcessor(object):
    """Docstring"""
    def __init__(self):
        pass

# MAIN FUNCTIONS (above helpers)
def process_data(input_data):
    """Docstring"""
    pass

# HELPER FUNCTIONS
def validate_input(data):
    """Docstring"""
    pass

# GRASSHOPPER ENTRY POINT
try:
    # Main logic
    result = process_data(my_input)
    ok = True
except Exception as e:
    ok = False
    error = str(e)
```

### Header docstring rules

- **Must use triple-quoted `""" ... """`** — only multi-line strings provide docstrings
- This text becomes the **tooltip** visible when hovering over the IronPython node in Grasshopper
- Always list Inputs and Outputs with types

### Component naming

- Component name in `ghenv.Component.Message` **must match the file name** or main function
- Format: `"<ComponentName> v<Version>"`
- **Every git change must increment the version number**

### Optional per-input descriptions

```python
ghenv.Component.Params.Input[0].Description = "input param description"
ghenv.Component.Params.Output[0].Description = "output param description"
```

## Available Imports

```python
import Rhino.Geometry as rg          # geometry kernel
import Grasshopper as gh             # GH data trees, params
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path
import Grasshopper.Kernel as ghk     # runtime messages
import System                        # .NET base types
import System.IO as SIO              # .NET file I/O
import scriptcontext as sc           # Rhino doc context, sc.sticky
import rhinoscriptsyntax as rs       # helper shortcuts
import json                          # built-in
import os, math, re                  # standard lib
```

## DataTree Operations

**API note:** The official Grasshopper SDK exposes **BranchCount**, **Branch(i)**, **Path(i)**, **Branches** (list of branches), and **Paths** (list of GH_Path) on `DataTree<T>`. **`PathCount` is not a standard property** — always prefer `BranchCount`. When writing defensive code, use `hasattr` checks rather than `or`-chaining (which treats a count of 0 as falsy):

```python
if hasattr(tree, "BranchCount"):
    n = tree.BranchCount
elif hasattr(tree, "Branches"):
    n = len(tree.Branches)
else:
    n = 0
```

Two import styles are used in the project (both valid):

```python
# Style 1 (via gh alias — matches CodeStyleGuide)
import Grasshopper as gh
import System
tree = gh.DataTree[System.Object]()
path = gh.Kernel.Data.GH_Path(0)

# Style 2 (direct import — common in project code)
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path
tree = DataTree[object]()
path = GH_Path(0)
```

### List of lists → DataTree

```python
def list_to_tree(list_of_lists):
    """Converts nested lists into Grasshopper data tree"""
    tree = gh.DataTree[System.Object]()
    for i, lst in enumerate(list_of_lists):
        path = gh.Kernel.Data.GH_Path(i)
        tree.AddRange(lst, path)
    return tree
```

### DataTree → flat list (robust)

```python
def tree_to_list(data_tree):
    """
    Converts a Grasshopper data tree into a flat list

    Args:
        data_tree: Grasshopper data tree (DataTree)

    Returns:
        list: Flat list of all elements from the tree
    """
    if data_tree is None:
        return []

    result_list = []

    if hasattr(data_tree, 'Branches'):
        for branch in data_tree.Branches:
            for item in branch:
                result_list.append(item)
    else:
        if hasattr(data_tree, '__iter__') and not isinstance(data_tree, str):
            for item in data_tree:
                result_list.append(item)
        else:
            result_list.append(data_tree)

    return result_list
```

### DataTree → list of lists

```python
def tree_to_list_of_lists(data_tree):
    """Converts GH DataTree into nested lists"""
    if data_tree is None:
        return []
    result = []
    for branch in data_tree.Branches:
        result.append(list(branch))
    return result
```

### Typed DataTree creation

```python
tree = gh.DataTree[rg.Point3d]()
tree = gh.DataTree[System.String]()
tree = gh.DataTree[System.Double]()
tree = gh.DataTree[rg.Brep]()
tree = gh.DataTree[System.Object]()  # mixed types
```

### Iterate by Paths and use EnsurePath (output trees)

When the tree has **Paths** and **Branch(path)**, you can iterate by path and keep the same path structure in output trees. Use **EnsurePath(path)** so the output tree has the branch before adding items:

```python
# Input tree with .Paths and .Branch(path) API
for path in input_tree.Paths:
    branch = input_tree.Branch(path)
    out_tree.EnsurePath(path)   # create branch in output if missing
    for item in branch:
        out_tree.Add(processed(item), path)
```

Use this when you need path identity (e.g. one output branch per input branch). When only **Branches** is available, use `for i, branch in enumerate(tree.Branches)` and `GH_Path(i)` for outputs.

**Optional:** If you need a default when an input is not wired, use `ghenv.Component.Params.Input[i].SourceCount == 0` ([GH API](https://mcneel.github.io/grasshopper-api-docs/api/grasshopper/html/P_Grasshopper_Kernel_GH_Param_1_SourceCount.htm)).

## sc.sticky State Persistence

```python
import scriptcontext as sc

comp_guid = str(ghenv.Component.InstanceGuid)
STICKY_KEY = "my_data_" + comp_guid

# Write
sc.sticky[STICKY_KEY] = my_data

# Read with default
cached = sc.sticky.get(STICKY_KEY, None)

# Check
if STICKY_KEY in sc.sticky:
    pass
```

## Error Reporting

```python
# Runtime message (appears on component)
import Grasshopper.Kernel as ghk

ghenv.Component.AddRuntimeMessage(
    ghk.GH_RuntimeMessageLevel.Warning,
    "Something went wrong: {}".format(msg)
)

# Levels: Warning, Error, Remark

# Component status message (bottom of component)
ghenv.Component.Message = "MyComponent v0.01 - OK"

# Force recompute
ghenv.Component.ExpireSolution(True)
```

## Common Geometry Patterns

For detailed Rhino.Geometry API patterns, see [reference.md](reference.md).

## Style Rules

1. **snake_case** for functions, **UPPER_SNAKE_CASE** for constants, **PascalCase** for classes
2. Every function has a docstring (short one-liner or detailed with Args/Returns)
3. No magic numbers — extract to named constants with meaningful prefixes (`TOLERANCE`, `STICKY_KEY`)
4. Component name in `ghenv.Component.Message` **must match file name** — increment version on every git change
5. Classes use `(object)` base class
6. Main functions above helpers; classes above functions (after imports + constants)
7. Initialize global output variables immediately after `ghenv.Component.Message`
8. Standard import abbreviations: `rg`, `gh`, `sc`, `rs`

## Anti-Patterns

- **Never** use `try: ... except: pass` silently — at least log to debug
- **Never** use bare `except:` for flow control — catch specific exceptions when possible
- **Never** use `print()` as primary output — use GH output params
- **Never** hardcode file paths — use `os.path.join()`, `System.IO.Path`
- **Never** assume input list order matches between different GH params without verifying length

## Additional Resources

- For Rhino.Geometry API patterns and .NET interop, see [reference.md](reference.md)
- For complete component templates and real examples, see [examples.md](examples.md)
