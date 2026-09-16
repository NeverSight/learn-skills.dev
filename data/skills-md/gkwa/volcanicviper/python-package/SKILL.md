---
name: python-package
description: Scaffold a new Python package with pyproject.toml, hatchling build system, ruff linting, and --version support via importlib.metadata. Use when creating a new Python package, Python CLI tool, or Python project from scratch.
---

## Python Package Scaffold

Use this structure as the starting point for a new Python package. Update the description, dependencies, and dev dependencies based on context.

`src/<package>/__init__.py`:
```python
def main() -> None:
    print("Hello from <package>!")
```

`.python-version`:
```
3.13
```

`pyproject.toml`:
```toml
[project]
name = "<package>"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
authors = [
    { name = "Author Name", email = "author@example.com" }
]
requires-python = ">=3.13"
dependencies = []

[project.scripts]
<package> = "<package>:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
preview = true

[tool.ruff.lint]
select = ["F", "E", "W"]
extend-select = ["I"]
extend-safe-fixes = ["F401", "F841"]
```

## Show Version

Support `--version` using `importlib.metadata` so the version is not duplicated:

```python
import argparse
import importlib.metadata

parser = argparse.ArgumentParser(description="...")
parser.add_argument(
    "--version",
    action="version",
    version=f"%(prog)s {importlib.metadata.version('<package>')}"
)
```
