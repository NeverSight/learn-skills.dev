---
name: "python-dev-environment"
description: "Expertise skill for Chapter 14.1 — The Development Environment. Contains verified facts about uv, pyright, ruff, pytest, and Git as a unified discipline stack. All data grounded from official documentation (Feb 2026)."
category: "expertise"
chapter: "14.1"
version: "1.0"
grounded_date: "2026-02-20"
---

# Python Development Environment Expertise Skill

**Purpose**: Provides verified, grounded reference data for writing Chapter 14.1 lessons. Every command, version number, and config option below was extracted from official documentation on 2026-02-20.

**Usage**: Content-implementer subagents MUST reference this skill when writing Ch 14.1 lessons. Never invent commands or config options — use only what is documented here.

---

## 1. uv — Package Manager & Project Orchestrator

**Version**: 0.10.4 (released February 17, 2026)
**Written in**: Rust
**Maker**: Astral (same company as ruff)
**Source**: [docs.astral.sh/uv](https://docs.astral.sh/uv/)

### Installation Commands

```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```bash
# macOS / Linux (curl)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# macOS (Homebrew)
brew install uv
```

```powershell
# Windows (WinGet)
winget install --id=astral-sh.uv -e
```

### `uv init` — Project Scaffolding

```bash
uv init smartnotes          # Create new project in subdirectory
uv init                     # Initialize in current directory
uv init --lib <name>        # Library project
uv init --package <name>    # Packaged application (src layout)
```

**Files created by `uv init smartnotes`:**

```
smartnotes/
├── .gitignore
├── .python-version          # Contains: 3.12 (or detected version)
├── README.md
├── main.py
└── pyproject.toml
```

**Default `main.py`:**

```python
def main():
    print("Hello from smartnotes!")


if __name__ == "__main__":
    main()
```

**Default `pyproject.toml`:**

```toml
[project]
name = "smartnotes"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.11"
dependencies = []
```

**Additional files created on first `uv run` or `uv sync`:**

- `.venv/` — virtual environment (not version-controlled)
- `uv.lock` — cross-platform lockfile with exact versions (should be committed)

### `uv add` — Dependency Management

```bash
uv add requests                    # Add runtime dependency
uv add 'requests>=2.28,<3'        # With version constraint
uv add --dev pytest                # Add dev dependency
uv add --dev pytest pyright ruff   # Multiple dev deps at once
uv remove requests                 # Remove a dependency
```

**What `uv add` does (three steps in one):**

1. Updates `pyproject.toml`
2. Updates `uv.lock` (lockfile)
3. Syncs the `.venv` environment

**Result in pyproject.toml after `uv add --dev pytest pyright ruff`:**

```toml
[dependency-groups]
dev = ["pytest>=9.0.2", "pyright>=1.1.408", "ruff>=0.15.2"]
```

### `uv run` — Execute in Project Environment

```bash
uv run main.py                     # Run a Python file
uv run pytest                      # Run an installed tool
uv run python -c "print('hi')"    # Run inline Python
```

**What happens on `uv run`:**

1. Verifies `uv.lock` is up-to-date with `pyproject.toml`
2. Verifies `.venv` is up-to-date with `uv.lock`
3. Installs/syncs missing dependencies automatically
4. Runs the command inside the project's virtual environment

**No manual venv activation required.** Students never need `source .venv/bin/activate`.

### Why uv Over pip

| Dimension | pip | uv |
|-----------|-----|-----|
| Speed | Baseline | 10-100x faster (Rust, parallel downloads, global cache) |
| Scope | Package install only | All-in-one: Python install, venvs, deps, scripts, builds |
| Virtual envs | Separate `python -m venv` step | Creates `.venv` automatically |
| Lockfile | None (needs pip-tools) | `uv.lock` generated automatically |
| Python versions | Need pyenv separately | Built-in: `uv python install 3.12` |
| Uninstall cleanup | Leaves orphaned transitive deps | Removes transitive deps on uninstall |
| Disk usage | Separate copies per venv | Global cache, up to 40% disk savings |
| Replaces | Just pip | pip, pip-tools, pipx, poetry, pyenv, virtualenv |

**Axiom Callback**: uv = Axiom I (Shell as Orchestrator). One command replaces an entire ecosystem.

---

## 2. pyright — Static Type Checker

**Version**: 1.1.408 (released January 8, 2026)
**Written in**: TypeScript (runs via Node.js; pip wrapper handles this transparently)
**Maker**: Microsoft
**Source**: [github.com/microsoft/pyright](https://github.com/microsoft/pyright)

### Installation

```bash
uv add --dev pyright               # Recommended via uv
```

### Configuration in `pyproject.toml`

```toml
[tool.pyright]
include = ["src"]
exclude = ["**/__pycache__"]
typeCheckingMode = "strict"
pythonVersion = "3.12"
```

**Also supports `pyrightconfig.json`** (takes precedence if both exist):

```json
{
  "include": ["src"],
  "typeCheckingMode": "strict",
  "pythonVersion": "3.12"
}
```

### Type Checking Modes

| Mode | Description |
|------|-------------|
| `"off"` | All type-checking disabled; syntax errors still reported |
| `"basic"` | Minimal rule set |
| `"standard"` | **Default (CLI).** Moderate coverage |
| `"strict"` | Most rules enabled; requires complete type annotations |

### Running Pyright

```bash
uv run pyright                     # Check entire project
uv run pyright src/main.py         # Check specific file
```

**Clean output:**

```
0 errors, 0 warnings, 0 informations
```

**Error output:**

```
/path/to/file.py:10:5 - error: Type of parameter "name" is unknown (reportUnknownParameterType)
1 error, 0 warnings, 0 informations
```

### What Strict Mode Catches (28 Additional Rules)

Strict mode enables 28 rules that are `"none"` in standard but `"error"` in strict:

**Missing annotations:**
- `reportMissingParameterType` — parameters without type hints
- `reportMissingTypeArgument` — generic classes without type args
- `reportUnknownParameterType` — parameter type resolves to Unknown
- `reportUnknownVariableType` — variable type resolves to Unknown
- `reportUnknownArgumentType` — argument type resolves to Unknown
- `reportUnknownMemberType` — member access resolves to Unknown
- `reportUnknownLambdaType` — lambda parameters Unknown

**Code quality:**
- `reportUnusedImport` — imported symbols not referenced
- `reportUnusedVariable` — local variables not referenced
- `reportUnusedFunction` — functions not referenced
- `reportUnusedClass` — classes not referenced
- `reportDuplicateImport` — duplicate imports
- `reportPrivateUsage` — accessing private members
- `reportConstantRedefinition` — redefining Final variables
- `reportDeprecated` — deprecated features

**Type safety:**
- `reportUntypedBaseClass` — base class without types
- `reportUntypedFunctionDecorator` — untyped decorators
- `reportUntypedClassDecorator` — untyped class decorators
- `reportUntypedNamedTuple` — NamedTuple without types
- `reportMatchNotExhaustive` — incomplete match
- `reportUnnecessaryCast` — unnecessary casts
- `reportUnnecessaryComparison` — always-true/false comparisons
- `reportUnnecessaryContains` — unnecessary `in` checks
- `reportUnnecessaryIsInstance` — unnecessary isinstance
- `reportIncompleteStub`, `reportInconsistentConstructor`, `reportInvalidStubStatement`, `reportTypeCommentUsage`

### Before/After Example (for Ch 14.1)

```python
# BEFORE: Passes standard, FAILS strict
def greet(name):
    return f"Hello, {name}"

# AFTER: Passes strict
def greet(name: str) -> str:
    return f"Hello, {name}"
```

**Axiom Callback**: pyright = Axiom V (Types Are Guardrails). The compiler catches bugs before runtime.

---

## 3. ruff — Linter & Formatter

**Version**: 0.15.2 (released February 19, 2026)
**Written in**: Rust
**Maker**: Astral (same company as uv)
**Source**: [docs.astral.sh/ruff](https://docs.astral.sh/ruff/)

### Installation

```bash
uv add --dev ruff                  # Add as dev dependency
```

### Running Ruff

```bash
# Linting
uv run ruff check .               # Lint all Python files
uv run ruff check --fix .         # Lint and auto-fix

# Formatting
uv run ruff format .              # Format all Python files
uv run ruff format --check .      # Check without modifying
```

### Configuration in `pyproject.toml`

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # Pyflakes (unused imports, undefined names)
    "I",    # isort (import sorting)
    "UP",   # pyupgrade (modernize syntax)
    "B",    # flake8-bugbear (common bugs)
    "SIM",  # flake8-simplify (simplifiable code)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Key Rule Categories (for Teaching)

| Prefix | Name | What It Catches |
|--------|------|-----------------|
| **F** | Pyflakes | Undefined names, unused imports, unused variables |
| **E** | pycodestyle (errors) | PEP 8 style violations (indentation, whitespace) |
| **W** | pycodestyle (warnings) | PEP 8 warnings |
| **I** | isort | Import sorting order |
| **UP** | pyupgrade | Old syntax that can be modernized |
| **B** | flake8-bugbear | Common programming mistakes |
| **SIM** | flake8-simplify | Code that can be simplified |
| **N** | pep8-naming | Naming conventions (CamelCase, snake_case) |
| **S** | flake8-bandit | Security vulnerabilities |
| **T20** | flake8-print | Print statements left in code |

**Default enabled rules**: `E4`, `E7`, `E9`, and `F` (minimal safe set).
**Total rules**: 800+ built-in.
**Suppress inline**: `# noqa: F841` on a line.

### What Ruff Replaces

Ruff is a single binary replacing: Flake8 (+ dozens of plugins), Black, isort, pydocstyle, pyupgrade, autoflake. Speed: 10-100x faster than these tools individually.

**Ruff format** is a drop-in Black replacement (>99.9% identical formatting).

**Axiom Callback**: ruff = Axiom IX (Verification is a Pipeline). Automated quality checks in your CI.

---

## 4. pytest — Testing Framework

**Version**: 9.0.2 (released December 6, 2025)
**Requires**: Python >= 3.10
**Source**: [docs.pytest.org](https://docs.pytest.org/en/stable/)

### Installation

```bash
uv add --dev pytest                # Add as dev dependency
```

### Test Discovery Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Files | `test_*.py` or `*_test.py` | `test_calculator.py` |
| Functions | `test_*` prefix | `def test_addition():` |
| Classes | `Test*` prefix (no `__init__`) | `class TestCalculator:` |
| Methods | `test_*` inside `Test*` classes | `def test_add(self):` |

### Minimal Test File

```python
# test_example.py
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4
```

Key: pytest uses plain `assert` — no special assertion methods needed.

### Running Tests

```bash
uv run pytest                      # Run all discovered tests
uv run pytest -v                   # Verbose (one line per test)
uv run pytest -q                   # Quiet (minimal output)
uv run pytest test_example.py      # Run specific file
uv run pytest -k "test_answer"     # Run matching keyword
```

### Output Format

**Default (dots):**

```
test_example.py .                                                [100%]
========================== 1 passed in 0.12s ===========================
```

**Verbose (`-v`):**

```
test_example.py::test_answer PASSED                              [100%]
========================== 1 passed in 0.12s ===========================
```

**Output characters:**

| Character | Meaning |
|-----------|---------|
| `.` | Passed |
| `F` | Failed |
| `E` | Error (exception in setup/teardown) |
| `s` | Skipped |
| `x` | Expected failure (xfail) |

### Configuration in `pyproject.toml`

```toml
[tool.pytest.ini_options]
addopts = "-ra -q"
testpaths = ["tests"]
```

**Axiom Callback**: pytest = Axiom VII (Tests Are the Specification). Tests define what "correct" means.

---

## 5. Git — Version Control

**Note**: Git is not a Python-specific tool and doesn't need version-grounding the same way. The chapter references Git as the fifth discipline tool.

### Key Git Commands for SmartNotes

```bash
git init                           # Initialize repo (uv init creates .gitignore)
git add .                          # Stage all changes
git commit -m "message"            # Commit with message
git log --oneline                  # View history
git diff                           # See uncommitted changes
```

**Axiom Callback**: Git = Axiom VIII (Version Control is Memory). Every change tracked, reversible.

---

## 6. The Unified `pyproject.toml` (SmartNotes After Full Setup)

After running all setup commands, the SmartNotes `pyproject.toml` looks like:

```toml
[project]
name = "smartnotes"
version = "0.1.0"
description = "A personal note-taking assistant"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = ["pytest>=9.0.2", "pyright>=1.1.408", "ruff>=0.15.2"]

[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.pytest.ini_options]
addopts = "-ra -q"
testpaths = ["tests"]
```

**Teaching point**: One file configures ALL four tools. This is the power of `pyproject.toml` as the single source of truth for a Python project.

---

## 7. Platform-Specific Notes

### Windows

- uv install: PowerShell command (see Section 1)
- Paths use `\` but uv handles this transparently
- `.venv\Scripts\activate` (if manual activation needed, but `uv run` avoids this)

### macOS

- uv install: curl or Homebrew
- `.venv/bin/activate` (if manual activation needed)

### Linux

- uv install: curl
- Same as macOS for venv paths

**Key teaching point**: `uv run` works identically on all platforms. Students never need to know activation differences.

---

## 8. Chapter 14 Tone Reference (Condensed)

### Characters

- **James**: Junior dev, 3 weeks into first job, e-commerce platform team. Learner surrogate. Makes understandable mistakes. Never mocked. Growth narrative.
- **Emma**: Senior engineer, 4 years at company. Mentor. Teaches through showing, not lecturing. Delivers quotable one-liners. Calm, slightly dry. Declarative sentences.

### Lesson Opening Pattern

1. Bridge sentence from previous lesson
2. James hits a crisis (specific time, specific number, visceral detail)
3. He discovers tools/code are inadequate (shown as code block)
4. Emma arrives, delivers one-line diagnosis
5. Emma fixes it

### Lesson Section Flow

1. Title → Narrative opening (4-6 paragraphs)
2. "The Problem Without This Tool" → pain point
3. "The Tool Defined" → blockquote + table + image
4. "From Axiom to Practice" → connects to Ch 14 axiom
5. "Practical Application" → code examples, configs
6. "Anti-Patterns" → narrative + table (3-4 columns)
7. "Try With AI" → exactly 3 prompts with `**What you're learning:**`
8. "Key Takeaways" → numbered list, 4-6 items
9. "Looking Ahead" → bridge to next lesson

### YAML Frontmatter Template

```yaml
---
sidebar_position: N
title: "Lesson Title"
description: "One sentence"
keywords: ["keyword1", "keyword2"]
chapter: 14.1
lesson: N
duration_minutes: 20-25

skills:
  - name: "Skill Name"
    proficiency_level: "A2|B1"
    category: "Conceptual|Technical|Applied"
    bloom_level: "Understand|Apply"
    digcomp_area: "Computational Thinking|Problem Solving"
    measurable_at_this_level: "Student can..."

learning_objectives:
  - objective: "Full sentence"
    proficiency_level: "A2|B1"
    bloom_level: "Apply|Understand"
    assessment_method: "Full sentence"

cognitive_load:
  new_concepts: 5-7
  assessment: "Justification sentence"

differentiation:
  extension_for_advanced: "Advanced activity"
  remedial_for_struggling: "Simplified approach"
---
```

### Code Style

- Use ` ```python static ` tag for Python blocks
- BAD code first with `# BAD:` comments, GOOD code follows
- Inline comments explain intent, not syntax
- Never two code blocks back-to-back without prose

### Voice

- Third-person narrator for narrative sections
- "You" for instructional sections (Practical Application, Try With AI)
- Declarative, confident. No hedging, no exclamation marks.
- Tables as primary analytical device.

---

## 9. Axiom Callbacks (Ch 14.1 → Ch 14 Mapping)

| Tool | Axiom | Connection |
|------|-------|------------|
| uv | I — Shell as Orchestrator | One command orchestrates entire ecosystem |
| pyproject.toml | II — Knowledge is Markdown | Project config as single source of truth |
| pyright | V — Types Are Guardrails | Compiler catches bugs before runtime |
| ruff | IX — Verification is a Pipeline | Automated lint/format in CI |
| pytest | VII — Tests Are the Specification | Tests define "correct" behavior |
| Git | VIII — Version Control is Memory | Every change tracked and reversible |

---

## 10. Confidence Assessment

| Data Point | Status | Source |
|-----------|--------|--------|
| uv v0.10.4, commands, config | VERIFIED | docs.astral.sh/uv, PyPI, GitHub |
| pyright v1.1.408, strict rules | VERIFIED | github.com/microsoft/pyright, PyPI |
| ruff v0.15.2, rules, config | VERIFIED | docs.astral.sh/ruff, PyPI, GitHub |
| pytest v9.0.2, conventions | VERIFIED | docs.pytest.org, PyPI, changelog |
| `requires-python` default | NOTE | Shows `>=3.11` in docs but varies by detected Python |
| Platform install differences | VERIFIED | Official docs for each tool |
| Ch 14 tone and structure | VERIFIED | Read from actual lesson files |
