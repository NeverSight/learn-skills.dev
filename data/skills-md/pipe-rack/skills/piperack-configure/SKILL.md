---
name: piperack-configure
description: Configure Piperack for a project. Use when the user wants to set up Piperack, create a piperack.toml file, or needs help configuring processes.
---

# Piperack Configuration

## Overview

This skill helps you configure [Piperack](https://github.com/carlos/piperack) for a project by generating a `piperack.toml` file. Piperack is a process manager that runs multiple commands in parallel (similar to Foreman or Goreman) with a TUI.

## Workflow

1.  **Analyze the Project**: Inspect the current directory to identify the project type and required processes.
    *   Look for `package.json` (Node.js scripts).
    *   Look for `Cargo.toml` (Rust binaries).
    *   Look for `docker-compose.yml` (Docker services).
    *   Look for `Procfile` (Heroku/Foreman definitions).
    *   Look for `Makefile`.
    *   Look for `go.mod`.
    *   Look for `requirements.txt` or `pyproject.toml`.

2.  **Determine Processes**: Based on the analysis, determine which processes should be run.
    *   **Frontend**: `npm start`, `yarn dev`, etc.
    *   **Backend**: `cargo run`, `go run`, `python app.py`, etc.
    *   **Database**: `docker-compose up db`, etc.
    *   **Worker**: background jobs.

3.  **Draft Configuration**: Create a `piperack.toml` content.
    *   Use the `assets/piperack.toml` template as a starting point.
    *   Add a `[[process]]` block for each identified service.
    *   Use `references/configuration.md` to ensure correct syntax and available options (e.g., `ready_check`, `depends_on`, `watch`).

4.  **Propose and Write**: Present the proposed configuration to the user.
    *   If the user approves, write the file to `piperack.toml`.

## Best Practices

*   **Colors**: Assign different colors to different processes to make the TUI readable.
*   **Ready Checks**: If a service depends on another (e.g., API depends on DB), add a `ready_check` to the dependency (e.g., `{ tcp = 5432 }`) and `depends_on` to the dependent service.
*   **Watch Mode**: Suggest enabling `watch` for development servers that don't have built-in hot reloading.

## Reference

*   **Configuration**: See [references/configuration.md](references/configuration.md) for detailed documentation on all available options in `piperack.toml`.