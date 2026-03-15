---
name: python-venv
description: Manage project-local Python virtual environments with venv.
---

# Skill: Python3 Virtual Environments (venv)

## Purpose
Manage project-local Python 3 virtual environments under `.venv` with clear, repeatable steps.

## When to use
- Any task in a Python project, including running scripts, tests, or tools
- Repos containing `pyproject.toml`, `requirements.txt`, `setup.py`, `setup.cfg`, `Pipfile`, `poetry.lock`, or `*.py`
- Setting up a fresh Python environment
- Installing or updating dependencies
- Exporting or locking dependencies
- Repairing or recreating a broken environment

## Activation guidance
- If a task involves executing Python code or tooling, ensure `.venv` exists and is activated first.
- If `.venv` is missing, create it and install dependencies before running the task.

## Default conventions
- Environment path: `.venv`
- Python interpreter: `python3`
- Dependency file: `requirements.txt`

## Core commands

Create a new environment:

```bash
python3 -m venv .venv
```

Activate (macOS/Linux):

```bash
source .venv/bin/activate
```

Activate (Windows PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Deactivate:

```bash
deactivate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Freeze dependencies:

```bash
python -m pip freeze > requirements.txt
```

Remove and recreate:

```bash
rm -rf .venv
python3 -m venv .venv
```

## Notes
- Always activate the environment before installing or running Python commands.
- Use `python -m pip` to ensure pip targets the active environment.
- Prefer project-local `.venv` over global installs.
- If `python3` is missing, make sure the user is aware.
- Always attempt to upgrade pip before installing dependencies.
