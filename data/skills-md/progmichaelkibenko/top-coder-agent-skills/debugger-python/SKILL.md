---
name: debugger-python
description: Debug Python applications at runtime using DAP breakpoints and variable inspection. Use when the user reports a runtime bug in Python, a silent failure, unexpected variable values, incorrect data flow, or when print-debugging is insufficient. Also use proactively when you encounter a bug you cannot diagnose from static analysis alone.
---

# Debugger (Python)

**Why:** Runtime bugs -- silent failures, wrong variable values, incorrect data flow through complex logic -- cannot always be diagnosed from code alone. This skill gives you a real debugger (breakpoints, variable inspection, expression evaluation) instead of scattering `print()` calls and guessing. You use the Debug Adapter Protocol (DAP) via `debugpy` to pause execution and inspect actual state.

**Hard constraints:** Requires the `top-coder-ai-skills-debugger` Python package. `debugpy` is pulled in by it. All commands go through `scripts/debug.py`. Never leave a debug session running after you are done -- always call `stop`.

---

## Setup (before first use)

**Install the package** in the environment used to run the script (globally or in the project):

- **Global (recommended for skills):**  
  `pip install top-coder-ai-skills-debugger`  
  or for the current user only: `pip install --user top-coder-ai-skills-debugger`

- **Project (if using uv):**  
  `uv add top-coder-ai-skills-debugger`

- **Project (if using Poetry):**  
  `poetry add top-coder-ai-skills-debugger`

**One-command setup:** From the project root (or the directory containing `scripts/`), run `python scripts/init.py`. It installs `top-coder-ai-skills-debugger` with pip if missing, or reports that it is already installed.

**Check that it works:** Run `python scripts/debug.py` with no arguments. If you see "top-coder-ai-skills-debugger is not installed", run `python scripts/init.py` or one of the install commands above, then retry. The debug script checks for the package and exits with a clear message when it is missing.

---

## When to use

- **Runtime errors:** A function returns the wrong result and you cannot see why from the source.
- **Silent failures:** Data is not saved, a callback never fires, but there is no crash or traceback.
- **Unexpected values:** A variable is `None`, an empty list, or the wrong type when it should not be.
- **Complex data flow:** Values pass through multiple functions/classes and you need to see where they go wrong.
- **Async / threading bugs:** Coroutines or threads produce unexpected interleaving.
- **Static analysis is not enough:** You have read the code but cannot determine the root cause.

Do **not** use for: syntax errors, import errors, or type errors that the linter or type checker already catches.

---

## Available commands

All commands run via `python scripts/debug.py <action> [args]`. If the script reports that `top-coder-ai-skills-debugger` is not installed, run the install command from **Setup** above, then retry.

| Command | Usage | Description |
|---------|-------|-------------|
| **start** | `start <file.py>` | Launch the Python debugger for the given file. |
| **breakpoint** | `breakpoint <file.py> <line>` | Set a breakpoint at a specific file and line. |
| **continue** | `continue` | Resume execution until the next breakpoint or termination. |
| **step** | `step` | Step over the current line. |
| **evaluate** | `evaluate <expression>` | Evaluate an expression in the current scope (e.g. `evaluate len(items)`). |
| **stack** | `stack` | Print the current call stack. |
| **variables** | `variables` | Print all local variables in the current frame. |
| **probe** | `probe <file.py>:<line>` | One-shot: run to the line, dump all variables and stack, then stop. |
| **stop** | `stop` | End the debug session and clean up. |

---

## Workflows

### Interactive debugging (multi-turn)

Use when you need to set multiple breakpoints, step through code, and inspect different variables across turns.

```
1. start app.py
2. breakpoint app.py 22
3. continue                     # runs until line 22
4. evaluate some_variable       # inspect the value
5. step                         # step to next line
6. variables                    # dump all locals
7. stop                         # always clean up
```

### One-shot probe (single turn)

Use when you have a hypothesis about a specific line and want to see all state at that point in one go.

```
1. probe app.py:22              # runs to line 22, dumps everything, stops
```

The probe returns: source context (with `>>>` marking the line), full stack trace, and all local variables. This is usually enough to confirm or reject a hypothesis.

---

## Code contrast

### Anti-pattern: Guess-and-print

```python
# Scattered print() calls that you must add, run, read, and remove.
def process_orders(orders: list[dict]) -> float:
    total = 0.0
    print(f"DEBUG orders: {orders}")           # added for debugging
    for order in orders:
        subtotal = order["quantity"] * order["price"]
        print(f"DEBUG subtotal: {subtotal}")   # added for debugging
        total += subtotal
    print(f"DEBUG total: {total}")             # added for debugging
    return total
# Problems: pollutes code, must remember to clean up, cannot inspect
# complex objects deeply or step through logic interactively.
```

### Top-coder pattern: Probe at the suspect line

```
$ python scripts/debug.py probe app.py:8

Stopped (breakpoint) at app.py:8
     5 | def process_orders(orders: list[dict]) -> float:
     6 |     total = 0.0
     7 |     for order in orders:
  >>>  8 |         subtotal = order["quantity"] * order["price"]
     9 |         total += subtotal
    10 |     return total

--- Stack Trace ---
#0   process_orders                 (app.py:8)
#1   main                           (app.py:25)

--- Local Variables ---
  total: float = 0.0
  order: dict = {'item': 'Widget', 'quantity': '3', 'price': 9.99}
  orders: list = [{'item': 'Widget', 'quantity': '3', 'price': 9.99}, ...]

# Immediately see: quantity is a string '3', not int 3.
# '3' * 9.99 gives '9.999.999.99' (string repetition), not 29.97.
# Fix the bug, no print() cleanup needed.
```

---

## Prerequisites

1. **Python 3.11+** must be on PATH.
2. **debugpy**: `pip install debugpy`
3. **top-coder-ai-skills-debugger** Python package: `pip install -e packages/debugger-core` or `uv sync` (from the repo root).

---

## Tips

- **Probe first.** Start with a one-shot probe at the suspicious line. If that gives enough info, you are done.
- **Breakpoint before continue.** Always set at least one breakpoint before calling `continue`, or execution will run to completion without stopping.
- **Always stop.** Call `stop` when finished. Do not leave zombie debug processes.
- **Evaluate rich expressions.** `evaluate` accepts any valid Python expression -- e.g. `evaluate [o['quantity'] for o in orders]`, `evaluate type(result).__name__`.
- **Generators and iterators.** Evaluate `list(gen)` to materialise a generator for inspection (note: this consumes it).
- **Check the stack.** If you are unsure how the code reached a point, use `stack` to see the full call chain.
- **`justMyCode` is on by default.** The debugger skips library internals. If you need to step into a dependency, modify the launch args in the adapter.
