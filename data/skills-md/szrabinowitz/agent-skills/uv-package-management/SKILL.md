---
name: uv-package-management
description: Teaches the agent how to manage Python projects, standalone scripts, and dependencies using the uv package manager.
---
# UV Quickstart Guide for Coding Agents

This guide outlines the standard operating procedures for managing Python projects, scripts, and dependencies using `uv`. 

**🚨 CRITICAL RULE: Never use the bare `python` command.** Barely ever should you run `python file.py` or `python -c`. Always use `uv run` to ensure you are executing within the correct, managed environment. If you are stuck or forget a command's syntax, always use `uv --help` or `uv <command> --help`.

---

## 1. Project Management (Permanent)
When managing a standard Python project, prefer `uv`'s built-in project management over traditional `pip` workflows.

* **Create a new project:** `uv init`
* **Add a dependency:** `uv add <package>`
* **Remove a dependency:** `uv remove <package>`
* **Resync dependencies:** `uv sync` *(Use this to clean up the environment or after manually modifying `pyproject.toml`)*.

## 2. Temporary Scripts & Debugging
Do not pollute the global environment or the permanent project files with temporary debugging dependencies.

* **Run a script with temporary dependencies:** `uv run --with pack1,pack2 file.py`
* **Run a quick Python command:** `uv run python -c "print('hello')"`
* **Run a quick Python command with a temporary dependency:** `uv run --with requests python -c "import requests; print(requests.get('https://example.com').status_code)"`

## 3. Standalone Scripts (Permanent for User)
When creating a single-file script for the user that needs to reliably run on its own across different machines, embed the dependency metadata directly into the script.

* **Add inline dependencies to a script:** `uv add --script myscript.py pack1,pack2`
    *(This modifies the script file to include standard inline metadata).*
* **Execute the script:** Once dependencies are added, simply run `uv run myscript.py`. `uv` will automatically read the file, create an isolated environment, and include those dependencies on the fly.

## 4. Python Execution & Version Control
* **Specify a Python version:** Pass the `--python` flag to `uv run`. 
    `uv run --python 3.14 file.py`
* **Run binaries installed in the project:** Use `uv run` to execute tools installed within the project's environment. 
    `uv run uvicorn main:app`

## 5. Global Tools & CLIs
Use `uv`'s tool management for CLIs that operate independently of the current virtual environment.

* **Run an interactive CLI temporarily (run-once):** `uvx <tool-name>`
* **Install a tool permanently:** `uv tool install <tool-name>`
* **Upgrade installed tools:** `uv tool upgrade <tool-name>` (or `uv tool upgrade --all`)

## 6. Temporary Testing via Pip
While `uv add` is strictly for permanent project management, `uv pip install` serves a great role in temporary experimentation. 

* **Test a dependency temporarily:** If you are inside a `uv` project and run `uv pip install <package>`, it will install the package into the current environment *without* adding it to `pyproject.toml`. 
* **Wipe temporary dependencies:** Because it wasn't permanently added, simply running `uv sync` later will remove the experimental package and return the environment to its official state.
* **Create a standard venv manually:** `uv venv` (if you explicitly need a raw virtual environment outside of standard project management).
