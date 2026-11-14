---
name: neo-python
description: >
  Use this skill when writing, reviewing, debugging, or architecting Python 3.10+
  code, including type hints, structural pattern matching, dataclasses, async/task
  groups, packaging-aware project structure, testability, and maintainability.
compatibility: "Supports Python 3.10 to 3.14. Requires a Python project structure (pyproject.toml, requirements.txt, or venv)."
metadata:
  version: "1.0.0"
  category: "Core"
---

# Python 3.10+ Expert Skill

## Trigger On
- The user asks to write, debug, review, or refactor Python code.
- Working in a repository containing `*.py`, `pyproject.toml`, `requirements.txt`, `Pipfile`, or `poetry.lock`.
- Requires asynchronous programming (`asyncio`), type hinting, or modern Python feature recommendations.
- The project needs setup for testing frameworks (`pytest`) or static analysis tools (`ruff`, `mypy`).

## Workflow
1. **Perceive:**
   - Inspect the project root to identify package management tools: `pyproject.toml` (Poetry/PDM/Ruff), `requirements.txt` (pip), or `environment.yml` (Conda).
   - Probe for Python version requirements (ensure compatibility with 3.10+ minimum).
   - Identify the application type: Web API (FastAPI, Flask, Django), Data Science (Pandas, PyTorch), or CLI tools.
2. **Reason:**
   - Evaluate if the current code follows modern Python (3.10+) idioms (e.g., `match/case`, `|` union types).
   - Decide if type checking (MyPy/Pyright) or auto-formatting (Ruff/Black) needs to be introduced.
   - Recommend appropriate architectural patterns based on project scale.
3. **Act:**
   - Write Python code with complete Type Hints, prioritizing the `X | Y` syntax.
   - Prefer modern language features: `match` statements (3.10+), `TaskGroup` (3.11+), and new generic syntax (3.12+).
   - Ensure code passes static analysis and unit tests.

## Coding Standards
- **Type Hinting:** Strongly recommended for all function signatures. Use 3.10+ union syntax like `list[int | str]`.
- **PEP 8 Compliance:** Follow official style guidelines. Recommended to use `ruff` as a linter and formatter for consistency.
- **Async Processing:** Use 3.11+ `asyncio.TaskGroup` to manage concurrent tasks.
- **Error Handling:** Use specific exception types and leverage 3.11+ `ExceptionGroup` and `except*` syntax.

## Tooling Recommendations
- **Linter / Formatter:** `ruff` (high performance and highly integrated).
- **Type Checker:** `mypy` or `pyright`.
- **Testing:** `pytest` with `pytest-asyncio` or `pytest-cov`.
- **Package Management:** `Poetry` or `uv` to ensure dependency locking and environment consistency.

## Deliver
- **Code Quality Report:** Identify parts that do not comply with 3.10+ modern syntax or PEP 8.
- **Best Practice Recommendations:** Provide specific refactoring suggestions, such as converting complex logic into `match/case` structures.
- **Validated Code:** Provide Python source code accompanied by test cases and passed type checks.

## Validate
- Code must run in a Python 3.10+ environment.
- Functions should have Docstrings (following Google or NumPy styles).
- Complex logic should include unit tests.
- All public APIs should have complete type hints.

## Documentation
### Official References
- [Python 3 Official Documentation](https://docs.python.org/3/)
### Internal References
- [Modern Python syntax evolution (3.10-3.14) and PEP 8 naming conventions](reference/coding-style.md)
- [Recommended modern Python 3.10 - 3.14 development patterns and best practices](reference/patterns.md)
- [Outdated Python practices to avoid, common pitfalls, and security traps](reference/anti-patterns.md)
- [Intelligent detection and management of Python project virtual environments and dependency tools](../neo-python-manager/SKILL.md)
