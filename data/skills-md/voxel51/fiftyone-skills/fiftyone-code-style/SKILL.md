---
name: fiftyone-code-style
description: Writes Python code following FiftyOne's official conventions. Use when contributing to FiftyOne, developing plugins, or writing code that integrates with FiftyOne's codebase.
---

# FiftyOne Code Style

## Module Template

```python
"""
Module description.

| Copyright 2017-2026, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import logging
import os

import numpy as np

import eta.core.utils as etau

import fiftyone as fo
import fiftyone.core.fields as fof
import fiftyone.core.labels as fol
import fiftyone.core.utils as fou

logger = logging.getLogger(__name__)


def public_function(arg):
    """Public API function."""
    return _helper(arg)


def _helper(arg):
    """Private helper."""
    return arg
```


## Import Organization

Four groups, alphabetized within each, separated by blank lines:

| Group | Example |
|-------|---------|
| 1. Standard library | `import logging`, `import os` |
| 2. Third-party | `import numpy as np` |
| 3. eta packages | `import eta.core.utils as etau` |
| 4. FiftyOne | `import fiftyone.core.labels as fol` |

### FiftyOne Import Aliases

| Module | Alias |
|--------|-------|
| `fiftyone` | `fo` |
| `fiftyone.core.labels` | `fol` |
| `fiftyone.core.fields` | `fof` |
| `fiftyone.core.media` | `fom` |
| `fiftyone.core.storage` | `fos` |
| `fiftyone.core.utils` | `fou` |
| `fiftyone.utils.image` | `foui` |
| `fiftyone.utils.video` | `fouv` |

## Docstrings (Google-Style)

```python
def get_operator(operator_uri, enabled=True):
    """Gets the operator with the given URI.

    Args:
        operator_uri: the operator URI
        enabled (True): whether to include only enabled operators (True) or
            only disabled operators (False) or all operators ("all")

    Returns:
        an :class:`fiftyone.operators.Operator`

    Raises:
        ValueError: if the operator is not found
    """
```

**Key patterns:**
- Args with defaults: `param (default): description`
- Multi-line descriptions: indent continuation
- Cross-references: `:class:`fiftyone.module.Class``

## Lazy Imports

Use `fou.lazy_import()` for optional/heavy dependencies:

```python
o3d = fou.lazy_import("open3d", callback=lambda: fou.ensure_package("open3d"))

mask_utils = fou.lazy_import(
    "pycocotools.mask", callback=lambda: fou.ensure_import("pycocotools")
)
```

## Guard Patterns

Use `hasattr()` for optional attributes:

```python
if hasattr(label, "confidence"):
    if label.confidence is None or label.confidence < threshold:
        label = label.__class__()
```

## Error Handling

Use `logger.warning()` for non-fatal errors:

```python
try:
    result = process_data(data)
except Exception as e:
    logger.warning("Failed to process data: %s", e)
```

## Avoid Redundant Code

Before writing new functions, search for existing implementations:
- Local: search the FiftyOne source if available in the environment
- Remote: search `https://github.com/voxel51/fiftyone`
- Check `fiftyone/core/utils.py` and `fiftyone/utils/*` first

## Common Utilities

| Module | Functions |
|--------|-----------|
| `fou` | `lazy_import()`, `ensure_package()`, `extract_kwargs_for_class()` |
| `etau` | `guess_mime_type()`, `ensure_dir()`, `make_temp_dir()` |

## Quick Reference

| Pattern | Convention |
|---------|------------|
| Module structure | Docstring → imports → logger → public → private |
| Private functions | `_prefix` |
| Docstrings | Google-style with Args/Returns/Raises |
| Error handling | `logger.warning()` for non-fatal |
| Lazy imports | `fou.lazy_import()` for optional deps |
| Guard patterns | `hasattr()` checks |
| Import aliases | `fo`, `fol`, `fof`, `fom`, `fos`, `fou` |
