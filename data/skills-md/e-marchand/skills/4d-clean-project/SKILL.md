---
name: 4d-clean-project
description: Clean a 4D project by removing generated files, caches, and system artifacts.
---

# 4D Project Cleaner

Remove generated files and caches from a 4D project.

## Usage

The script auto-detects the project root by finding the `.4DProject` file.

```bash
# From anywhere inside the project
python scripts/clean.py

# Or specify a path
python scripts/clean.py /path/to/4d-project
```

The script reports what was removed.

## What Gets Removed

| Item | Location | Description |
|------|----------|-------------|
| DerivedData/ | Recursive | Compilation cache |
| Libraries/ | Root | Runtime libraries |
| userPreferences.*/ | Root | User-specific settings |
| Project/Trash/ | Root | Deleted items |
| Logs/* | Root | Log file contents |
| .DS_Store | Recursive | macOS folder metadata |
| ehthumbs.db | Recursive | Windows thumbnail cache |
| Thumbs.db | Recursive | Windows thumbnail cache |