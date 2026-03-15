---
name: py-quality-setup
description: Configure ruff, mypy, and basedpyright for Python 3.13 projects. Use when setting up linters and type checkers in pyproject.toml and pyrightconfig.json.
status: stable
---

# Python Quality Tooling Setup

Configure comprehensive linting and type checking for Python 3.13 projects following Engineering Charter standards.

## Objectives

1. Configure ruff for linting and formatting
2. Configure mypy for strict type checking
3. Configure basedpyright for additional type analysis
4. Ensure all tools target Python 3.13 or later
5. Add tools to dev dependencies

## Required Tools

**Add to `[dependency-groups]` dev**: `"ruff"`, `"mypy"`, `"basedpyright"`, `"pytest"`, `"pytest-cov"`

- **ruff**: Fast linter and formatter (Rust-based, replaces black, isort, flake8)
- **mypy**: Standard Python type checker
- **basedpyright**: Enhanced Pyright fork with additional type analysis

## Required Configuration Files

### pyproject.toml (Canonical Reference)

This skill provides the **canonical pyproject.toml configuration** for all quality tools. Other skills reference this configuration.

Must include these sections:

```toml
[project]
requires-python = ">=3.13"

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
    "ruff>=0.8.0",
    "mypy>=1.0",
    "basedpyright>=1.0",
    "pre-commit>=3.0",
    # Analysis tools (add as needed for py-* skills):
    # "radon", "vulture", "pylint", "bandit", "lizard",
    # "mutmut", "wily", "xenon", "pyupgrade", "coverage",
]

[tool.ruff]
line-length = 100  # or 140 for larger projects
target-version = "py313"
src = ["src"]  # adjust to your source directory

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
]
ignore = []

[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
check_untyped_defs = true

# Add overrides for third-party packages without stubs
# [[tool.mypy.overrides]]
# module = "package_name"
# ignore_missing_imports = true

[tool.basedpyright]
pythonVersion = "3.13"
typeCheckingMode = "standard"  # or "recommended" for stricter
reportMissingTypeStubs = false
reportUnknownMemberType = false
reportUnknownArgumentType = false
reportUnknownVariableType = false
```

### pyrightconfig.json (optional, for multi-package projects)

A.When using `pyrightconfig.json` for multi-package projects, REMOVE the `tool.basedpyright` section from pyproject.toml

```json
{
  "include": ["src"],
  "exclude": ["**/node_modules", "**/__pycache__", "**/.*", "venv", ".venv"],
  "pythonVersion": "3.13",
  "typeCheckingMode": "recommended",
  "reportMissingImports": "error",
  "reportMissingTypeStubs": false,
  "reportUnknownMemberType": false,
  "reportUnknownVariableType": false,
  "reportUnknownArgumentType": false,
  "reportMissingParameterType": true,
  "reportUnusedVariable": true,
  "reportImplicitStringConcatenation": true,
  "reportUnnecessaryTypeIgnoreComment": true
}
```

## Setup Workflow

1. **Check existing configuration**
   - Read pyproject.toml
   - Check if dev dependencies exist
   - Verify Python version requirement

2. **Update or create configuration**
   - Add dev dependencies if missing
   - Add/update [tool.ruff] section
   - Add/update [tool.mypy] section
   - Add/update [tool.basedpyright] section
   - Create pyrightconfig.json if needed (multi-package projects)

3. **Install tools in venv**
   ```bash
   # Using uv (recommended):
   uv sync                      # Creates venv and installs dev group automatically

   # Or manually:
   uv venv
   source .venv/bin/activate
   uv sync --group dev

   # Fallback if uv not available:
   # python -m venv venv
   # source venv/bin/activate
   # pip install -e ".[dev]"
   ```

4. **Verify installation**
   ```bash
   which ruff mypy basedpyright
   ruff --version
   mypy --version
   basedpyright --version
   ```

5. **Run initial checks**
   ```bash
   ruff check .
   mypy .
   basedpyright .
   ```

6. **Configure Claude Code permissions**

   Write `.claude/settings.local.json` so all py-* skills can run without permission prompts. If the file already exists, merge new entries into the existing `allow` list without removing user entries.

   ```json
   {
     "permissions": {
       "allow": [
         "Bash(ruff *)",
         "Bash(mypy *)",
         "Bash(basedpyright *)",
         "Bash(pytest *)",
         "Bash(vulture *)",
         "Bash(pylint *)",
         "Bash(radon *)",
         "Bash(lizard *)",
         "Bash(wily *)",
         "Bash(bandit *)",
         "Bash(mutmut *)",
         "Bash(pyupgrade *)",
         "Bash(scc *)",
         "Bash(pre-commit *)",
         "Bash(uv *)",
         "Bash(pip *)",
         "Bash(python3 *)",
         "Bash(python *)",
         "Bash(source *)",
         "Bash(which *)",
         "Bash(mkdir *)",
         "Bash(chmod *)",
         "Bash(ls *)",
         "Bash(ln *)",
         "Bash(git add *)",
         "Bash(git diff *)",
         "Bash(git status *)",
         "Bash(git log *)",
         "Bash(git ls-files *)",
         "Bash(git checkout *)",
         "Bash(git branch *)",
         "Bash(git commit *)"
       ],
       "deny": []
     }
   }
   ```

   **Merge logic**: Read existing file, parse JSON, take union of `allow` lists, write back. Create `.claude/` directory if needed.

7. **Install Stop hook lint gate**

   Symlink the lint gate script so Claude Code runs the full lint suite (ruff, mypy, basedpyright) on modified files before returning to the user. If any linter reports errors, Claude is blocked from stopping and must fix them first.

   ```bash
   mkdir -p ~/.claude/hooks
   ln -sf ~/.claude/skills/py-git-hooks/lint-gate.py ~/.claude/hooks/lint-gate.py
   ```

   Configure the Stop hook in `~/.claude/settings.json` (merge into existing hooks if present):

   ```json
   {
     "hooks": {
       "Stop": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "python3 ~/.claude/hooks/lint-gate.py"
             }
           ]
         }
       ]
     }
   }
   ```

8. **Configure git hooks** (if requested)
   - Set up pre-commit hook to run linters
   - See py-git-hooks skill

## Tool-Specific Notes

### Ruff
- Fastest Python linter (Rust-based)
- Replaces: black, isort, flake8, and many plugins
- Auto-fix: `ruff check --fix .`
- Format: `ruff format .`

### Mypy
- Standard Python type checker
- Strict mode catches most type errors
- Use `# type: ignore[error-code]` sparingly
- Add overrides for packages without stubs

### Basedpyright
- Fork of Pyright with more features
- Catches some errors mypy misses
- More configurable than Pyright
- Works well alongside mypy

## Common Adjustments

**Monorepo/multi-package**:
- Use pyrightconfig.json with extraPaths
- Set namespace_packages = true in mypy

**Legacy codebase**:
- Start with less strict mypy (strict = false)
- Gradually enable strict checks
- Use mypy overrides per module

**Third-party packages without stubs**:
```toml
[[tool.mypy.overrides]]
module = "package_name"
ignore_missing_imports = true
```

## Verification Checklist

- [ ] pyproject.toml has requires-python = ">=3.13"
- [ ] dev dependencies include ruff, mypy, basedpyright
- [ ] [tool.ruff] configured with target-version = "py313"
- [ ] [tool.mypy] configured with python_version = "3.13"
- [ ] [tool.basedpyright] configured with pythonVersion = "3.13"
- [ ] All tools installed in venv
- [ ] ruff check passes (or only expected errors)
- [ ] mypy . passes (or only expected errors)
- [ ] basedpyright . passes (or only expected errors)
- [ ] `.claude/settings.local.json` exists with permissions for all quality tools
- [ ] `~/.claude/hooks/lint-gate.py` symlinked and Stop hook configured in `~/.claude/settings.json`

## Examples

**Example: New project setup**
```
1. Create venv: uv venv && source .venv/bin/activate
2. Create pyproject.toml with [project], [tool.ruff], [tool.mypy], [tool.basedpyright]
3. Install: uv pip install -e ".[dev]"
4. Verify: ruff --version && mypy --version && basedpyright --version
5. Run initial checks: ruff check . && mypy . && basedpyright .
6. Fix issues or add ignores for false positives
```

**Example: Add quality tools to existing project**
```
1. Activate venv: source .venv/bin/activate
2. Update pyproject.toml:
   - Add ruff, mypy, basedpyright to [project.optional-dependencies] dev
   - Add [tool.ruff], [tool.mypy], [tool.basedpyright] sections
3. Install: uv pip install -e ".[dev]"
4. Run checks: ruff check . (expect many errors initially)
5. Auto-fix: ruff check --fix . && ruff format .
6. Run type checkers: mypy . && basedpyright .
7. Add [[tool.mypy.overrides]] for third-party packages without stubs
8. Iterate until all checks pass
```

**Example: Legacy codebase gradual adoption**
```
1. Start with minimal ruff rules: select = ["E", "F"]
2. Start mypy non-strict: strict = false
3. Fix errors incrementally, expand rules over time
4. Add per-module mypy overrides for problematic modules
5. Eventually enable strict mode project-wide
```

## Related Skills

- **Foundation**: This skill is the foundation for all other skills
- **Next steps**: py-git-hooks (automate enforcement of configured tools)
- **See also**: py-modernize (for uv migration and syntax upgrades)
