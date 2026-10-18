---
name: accelerate-python-resolvers
description: Make Chalk Python resolvers statically accelerable. Use when the user asks to accelerate resolvers, fix static-acceleration diagnostics, check why a resolver "can't be accelerated", or speed up Python feature pipelines in a Chalk project (a repo with chalk.yaml/chalk.yml).
---

# Accelerate Chalk Python resolvers

Chalk's static accelerator translates Python resolver functions into native
columnar expressions via symbolic execution of the function's bytecode.
Accelerated resolvers run orders of magnitude faster than interpreted Python.
A resolver can only be accelerated when every operation it performs can be
proven safe and is supported by the accelerator.

This skill drives a feedback loop against the Chalk static accelerator
service: get diagnostics, rewrite the offending resolvers, repeat until clean.

## The loop

1. From anywhere inside the Chalk project (the directory tree containing
   `chalk.yaml` or `chalk.yml`), run:

   ```sh
   python "${CLAUDE_PLUGIN_ROOT}/bin/accelerator-diagnostics.py"
   ```

   Use the same Python environment the project uses (it must be able to
   `import chalk`). If the project uses a venv, activate it first or invoke
   the venv's `python` explicitly.

2. Read the diagnostics. Each line is `file:line: severity: message` and the
   message explains exactly which operation blocked acceleration, e.g.:

   - `'int.__add__(int)' is only supported for non-null values; guard this
     'option<int>' argument against None` — a nullable input (annotated
     `int | None` / `Optional[int]` on the feature class) flows into an
     operation that requires a non-null value.
   - `reference to possibly-unbound name 'uuid'` — the resolver uses an
     import or helper the accelerator cannot capture (an unsupported
     library), or a local variable that is not assigned on every path.

3. Rewrite the resolver to remove the failure point (see recipes below).
   Preserve the resolver's signature, output feature, and Python semantics —
   the accelerated version must compute the same values the Python version
   would.

4. Re-run the script. Repeat until it prints
   `All resolvers are statically accelerable.` and exits 0.

## Rewrite recipes

### Nullable input used where a non-null value is required

The most common diagnostic. A feature annotated `int | None` may be None at
runtime; operations like `+`, `-`, `*`, comparisons, and most method calls
require proven-non-null operands. Add an explicit guard so the symbolic
executor can narrow the type:

```python
@online
def get_score(a: User.maybe_null_input) -> User.score:
    if a is None:
        return 0          # pick a semantically sensible default
    return a + 2          # `a` is now provably non-null
```

Both `if a is None: return <default>` early-returns and
`x = 0 if a is None else a` conditional expressions work. If no sensible
default exists, ask the user what the None case should produce — do not
invent business logic silently.

### Unsupported library or helper

The accelerator supports a fixed set of builtins and modules (including
`math`, `statistics`, `re`, `hashlib`, `datetime`, `json`, common `str` /
`list` / `dict` / `set` methods, `numpy`, `pandas`, and protobuf message
access). A reference to anything else (e.g. `uuid`, `requests`-adjacent
helpers, custom classes) fails with a "possibly-unbound name" or
"Unsupported" diagnostic.

Fixes, in order of preference:

1. Re-express the logic with supported operations (e.g. replace
   `uuid.uuid5(...)` with a supported `hashlib` digest if the user agrees the
   semantics are acceptable).
2. Inline small pure helpers into the resolver body, or make sure helpers are
   module-level functions the accelerator can capture.
3. If the dependency is essential, leave the resolver un-accelerated and tell
   the user why; do not fake the behavior.

### Possibly-unbound local variable

If a variable is only assigned inside a conditional or loop, assign a default
before the conditional so every path binds it.

## Configuration

- `CHALK_ACCELERATOR_HOST` — accelerator service host. Defaults to
  `https://accelerator.chalk.ai` (the service Chalk runs on your behalf).
  Pass `--host http://127.0.0.1:8780` or set the env var to use a
  locally-running server.
- `CHALK_ACCELERATOR_TOKEN` — optional bearer token for the hosted service.

## Notes

- The script exports the whole project (`python -m chalk.cli export`), so
  syntax errors or import failures anywhere in the project fail the check
  before diagnostics run; fix those first (exit code 2).
- Diagnostics cover every resolver in the project. If the user asked about
  one resolver, fix that one and leave unrelated diagnostics alone unless
  asked.
- A clean run means every resolver either accelerates fully or was explicitly
  marked never-accelerate by its author.
