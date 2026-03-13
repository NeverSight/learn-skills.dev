---
name: setting-up-python-projects
description: "Bootstrap new Python projects: directory structure, pyproject.toml, pre-commit, uv sync. Use when creating a new project from scratch."
---

# Setting Up Python Projects

New projects start with the full safety net configured. Templates are in the repo: <https://github.com/quick-brown-foxxx/coding_rules_python/tree/master/templates>`.

Make sure to read repo's readme.

---

## Project Layout

```
project/
├── src/appname/
│   ├── __init__.py           # __version__ = "0.1.0"
│   ├── __main__.py           # Entry point
│   ├── constants.py          # Shared constants
│   ├── core/                 # Business logic
│   │   ├── models.py         # Data types (dataclasses)
│   │   ├── manager.py        # Business operations
│   │   └── exceptions.py     # Custom exception hierarchy
│   ├── cli/                  # CLI interface
│   │   ├── commands.py       # Command implementations
│   │   ├── parser.py         # Argument parsing
│   │   └── output.py         # Formatted output helpers
│   ├── ui/                   # Qt GUI (if applicable)
│   │   ├── main_window.py
│   │   ├── dialogs/
│   │   └── widgets/
│   ├── utils/                # Stateless utilities
│   │   ├── paths.py
│   │   └── logging.py
│   ├── wrappers/             # Third-party lib wrappers
│   │   └── some_wrapper.py
│   └── stubs/                # Type stubs for untyped libs
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── fixtures/
│   └── conftest.py
├── scripts/                  # Dev utilities
│   ├── bootstrap.py          # Setup script
│   └── check_type_ignore.py
├── docs/
│   ├── coding_rules.md       # Copy from rules/coding_rules.md
│   └── PHILOSOPHY.md          # Copy from PHILOSOPHY.md
├── shared/                   # Cross-cutting (copy from coding_rules_python/reusable/)
│   ├── logging/              # Logging + colored output (if needed)
│   └── shortcuts/            # Keyboard shortcuts (if PySide6 app)
├── AGENTS.md                 # Copy from templates/AGENTS.md, customize
├── CLAUDE.md                 # Symlink → AGENTS.md
├── pyproject.toml            # Copy from templates/pyproject.toml, customize
├── .pre-commit-config.yaml   # Copy from templates/pre-commit-config.yaml
├── .gitignore                # Copy from templates/gitignore
└── .vscode/
    ├── settings.json         # Copy from templates/vscode_settings.json
    └── extensions.json       # Copy from templates/vscode_extensions.json
```

---

## Setup Checklist

1. **Create directory structure:**
   ```
   mkdir -p src/APPNAME tests/unit tests/integration tests/fixtures scripts docs .vscode
   ```

2. **Copy template and reference files:**
   - `templates/pyproject.toml` → `pyproject.toml` (update `[project]` section)
   - `templates/AGENTS.md` → `AGENTS.md` (fill TODO sections)
   - `templates/pre-commit-config.yaml` → `.pre-commit-config.yaml`
   - `templates/gitignore` → `.gitignore`
   - `templates/vscode_settings.json` → `.vscode/settings.json`
   - `templates/vscode_extensions.json` → `.vscode/extensions.json`
   - `rules/coding_rules.md` → `docs/coding_rules.md`
   - `PHILOSOPHY.md` → `docs/PHILOSOPHY.md`
   - Create symlink: `ln -s AGENTS.md CLAUDE.md`

3. **Copy reusable code (if needed):**
   - From `coding_rules_python/reusable/` copy modules you need into `shared/`
   - `logging/` — colored logging, file rotating logs, CLI output (see `setting-up-logging` skill)
   - `shortcuts/` — keyboard shortcuts for PySide6 apps (see `setting-up-shortcuts` skill)
   - Also copy matching tests from `coding_rules_python/reusable_tests/` into your `tests/` (e.g., `test_shortcuts_base.py`, `test_shortcuts_manager.py`)
   - Update import paths after copying (`reusable.` → `shared.` or your package path, `reusable_tests.` → your test package)

4. **Create entry points:**
   ```python
   # src/APPNAME/__init__.py
   __version__ = "0.1.0"

   # src/APPNAME/__main__.py
   import sys

   def main() -> int:
       if len(sys.argv) > 1:
           return cli_main()  # CLI mode
       return gui_main()      # GUI mode (if applicable)

   if __name__ == "__main__":
       sys.exit(main())
   ```

5. **Create initial test:**
   ```python
   # tests/test_main.py
   from APPNAME.__main__ import main

   def test_main_runs(capsys: pytest.CaptureFixture[str]) -> None:
       assert main() == 0
   ```

6. **Initialize environment:**
   ```bash
   git init
   uv sync --all-extras --group dev
   uv run pre-commit install
   uv run poe lint_full
   uv run poe test
   ```

7. **Verify everything works:**
   - `uv run poe app` runs the application
   - `uv run poe lint_full` passes with 0 errors
   - `uv run poe test` passes

---

## Bootstrap Script

```python
# scripts/bootstrap.py
"""Set up development environment."""
import subprocess

def main() -> None:
    subprocess.run(["uv", "sync", "--all-extras", "--group", "dev"], check=True)
    subprocess.run(["uv", "run", "pre-commit", "install"], check=True)
    print("Development environment ready.")

if __name__ == "__main__":
    main()
```

---

## Adapt to Tech Stack & Domain

After scaffolding, **adapt everything to the specific project**. The templates are a starting point, not a straitjacket. `docs/PHILOSOPHY.md` is the only ruling constant — everything else bends to fit the project's tech stack, domain, and constraints.

### What to adapt

| Area | How to adapt |
|------|--------------|
| **Directory layout** | Add/remove/rename directories to match the domain. Not every project needs `cli/`, `ui/`, `wrappers/`, `shared/`. A data pipeline might need `pipelines/`, `schemas/`, `extractors/`. A web service might need `routes/`, `middleware/`, `repositories/`. |
| **Dependencies** | Add domain-specific libraries. Remove unused template defaults. Research current best-in-class libraries for the domain (e.g. SQLAlchemy vs raw asyncpg, Pydantic vs attrs). |
| **pyproject.toml** | Adjust ruff rules, pytest markers, basedpyright overrides for the domain. Some domains need relaxed rules (e.g. data science may need broader `type: ignore` for numpy interop). |
| **AGENTS.md** | Fill TODO sections with project-specific architecture, key decisions, domain vocabulary, and workflows. This is the agent's primary orientation document — make it specific. |
| **coding_rules.md** | Extend or override rules for the domain. Add domain-specific conventions (e.g. database migration rules, API versioning policy, data validation requirements). |
| **Test structure** | Adjust to match what matters. A CLI tool needs heavy e2e tests. A library needs heavy unit tests. A web service needs API integration tests. |
| **CI/CD** | Add domain-appropriate checks (e.g. migration consistency, API schema validation, container builds). |

### Research before building

When setting up a project in an unfamiliar domain or with unfamiliar libraries:

1. **Research the domain's conventions** — look up how well-maintained projects in the same space are structured
2. **Check library compatibility** — verify libraries work together and with basedpyright strict mode (some libraries have poor type stubs; plan wrappers early)
3. **Identify domain-specific tooling** — some domains have their own linters, formatters, or validation tools that complement the base toolchain
4. **Check for basedpyright known issues** — some libraries (numpy, pandas, SQLAlchemy) need specific configuration or stub packages to work cleanly in strict mode

### Quick customization checklist

- [ ] Directory layout matches the domain, not the generic template
- [ ] Dependencies are domain-appropriate (researched, not guessed)
- [ ] AGENTS.md describes *this* project, not a generic Python project
- [ ] coding_rules.md has domain-specific additions if needed
- [ ] Test structure reflects what matters most for this project
- [ ] basedpyright config accounts for domain-specific library quirks
