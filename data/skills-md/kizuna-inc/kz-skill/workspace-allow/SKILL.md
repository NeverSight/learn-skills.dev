---
name: workspace-allow
author: kizuna-inc
description: Enforces full agent autonomy within the target workspace directory while requiring explicit user confirmation for any actions targeting paths or systems outside the folder.
license: MIT
version: "1.0.0"
tags:
  - git
  - workspace
  - safety
  - file-system
---

# Skill: Scoped Directory Operations & Workspace Boundary Enforcement

## Scope Boundary
- **Workspace Root**: `./` (or specify absolute path, e.g., `/path/to/target/folder`)
- Treat the Workspace Root as the designated sandbox.

## Policy Rules

### 1. In-Scope Operations (Full Autonomy)
You have full authorization to execute any action inside the Workspace Root and its subdirectories without prior user confirmation, including:
- Creating, reading, modifying, moving, and deleting files or directories.
- Running builds, tests, scripts, or local terminal commands that only touch resources within the Workspace Root.
- Inspecting git status and staging changes strictly inside this boundary.

### 2. Out-of-Scope Operations (Confirmation Required)
You MUST stop and explicitly ask the user for permission before performing ANY action that references, accesses, or affects anything outside the Workspace Root.

An action counts as "Out-of-Scope" if it involves:
- **Paths**: Any absolute path outside the root, or relative paths traversing up via `../` beyond the root boundary (e.g., `../sibling_folder`, `~/.config`, `/etc/`).
- **Commands**: Shell commands that target external directories (e.g., `cd .. && rm -rf other_project`), modify global package registries/caches (e.g., `npm install -g`), or touch external system processes.
- **Environment & Secrets**: Reading global files, home directory configurations, or credentials outside the project tree.

### 3. Confirmation Prompt Format
When an external action is necessary, do not execute the command or write the file. Instead, halt and present the request using this format:

> ⚠️ **Out-of-Scope Action Request**
> - **Target Path / Command**: `[Target path or full shell command]`
> - **Reason**: `[Why this external action is needed]`
> - **Risk Assessment**: `[What files/systems might be modified or exposed]`
> 
> "Would you like me to proceed with this action outside the workspace? (Yes/No)"

Await clear user confirmation before executing.