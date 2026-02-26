---
name: python-guidelines
description: When dealing with python code, these guidelines must always be followed.
---

# Python Guidelines

## Logging

When calling a logger by for example calling logger.infog(...) or logger.debug(...) etc..
always use lazy string formatting when interpolating variables for performance.

Bad example. Must avoid:

```python
logging.error(f"Python version: {sys.version}")
```

Good example, use Lazy formatting

```python
logging.error("Python version: %s", sys.version)
```
