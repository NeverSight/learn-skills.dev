---
name: neo-python-manager
description: >
  Use this skill when the user asks how to install, add, remove, update, or run
  Python dependencies; choose between uv, Poetry, venv, or pip; create/sync a virtual
  environment; or diagnose Python package manager setup from pyproject.toml, lock
  files, or requirements.txt.
compatibility: "Supports any Python project containing pyproject.toml, requirements.txt, uv.lock, or poetry.lock."
metadata:
  version: "1.1.0"
  category: "Environment"
---

# Python Environment Manager Skill

## Trigger On
- The user asks "How do I install a package?" or "Which package manager is this project using?".
- The user requests to add, remove, or update Python dependencies.
- Need to initialize a virtual environment or execute a Python script but unsure whether to use `uv run`, `poetry run`, or `python`.
- The project lacks explicit environment configuration and needs recommendations for suitable tools.

## Workflow
1. **Perceive:**
   - Scan the project root for characteristic files: `uv.lock`, `poetry.lock`, `pyproject.toml`, `requirements.txt`.
   - Check the system environment to test if tools are installed: execute `uv --version` or `poetry --version`.
2. **Reason:**
   - Determine the tool the project should use based on characteristic files (Priority: `uv` > `Poetry` > `pip`).
   - **Check tool availability**: If the project is determined to use `uv` but it's not installed, or if the user wants to switch to `uv/Poetry` but the environment is not ready, mark it as "Pending Installation".
3. **Act:**
   - **Tool Installation Suggestion**: If the tool is not installed, **must ask the user first**: "Detected that the project uses [Tool Name], but it is not installed in your environment. Would you like me to provide the installation command and assist with the installation?"
   - **Output Commands**: Provide the correct operation commands for the identified management tool.
   - **Execute Changes**: If the user agrees to installation or dependency changes, provide CLI commands for user confirmation.

## Tooling Commands Reference

### 1. uv (Recommended: Ultra-fast Tool)
- **Detection Criteria:** `uv.lock` exists.
- **Installation (Unix/macOS):** `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Installation (Windows):** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **Common Commands:**
  - `uv add <package>` (Add package)
  - `uv sync` (Sync environment)
  - `uv run <script.py>` (Run script)

### 2. Poetry
- **Detection Criteria:** `poetry.lock` exists or `[tool.poetry]` in `pyproject.toml`.
- **Installation (Cross-platform):** `curl -sSL https://install.python-poetry.org | python3 -`
- **Common Commands:**
  - `poetry add <package>` (Add package)
  - `poetry install` (Install dependencies)
  - `poetry run python <script.py>` (Run script)

### 3. venv + pip (Legacy Standard)
- **Detection Criteria:** Only `requirements.txt` or `.venv` exists.
- **Common Commands:**
  - `pip install <package>`
  - `pip install -r requirements.txt`

## Deliver
- **Environment Detection Report:** Inform the current environment status (e.g., uv installed, poetry.lock detected).
- **Installation and Operation Guidance:** If tools are missing, proactively ask for installation consent and provide the correct syntax.
- **Environment Consistency Check:** Ensure provided commands perfectly match the project's existing lock files.

## Validate
- Never execute installation commands directly without asking the user.
- Installation commands must distinguish between operating systems (macOS/Linux vs Windows).
