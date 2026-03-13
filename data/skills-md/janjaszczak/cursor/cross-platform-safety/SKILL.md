---
name: cross-platform-safety
description: Ensure commands and paths are safe across Windows + WSL + Docker (PowerShell vs bash, path translation, permissions). Use when instructions touch shell, filesystem, Docker, or OS-specific behavior.
compatibility: Intended for Windows + WSL2 + Docker environments; requires ability to detect platform or ask user.
allowed-tools: Bash(*) PowerShell(*) Read
metadata:
  intent: Only activate when OS boundaries matter; keep default answers OS-agnostic.
---

# cross-platform-safety

## Activation gate (anti-noise)
Activate if any of:
- The user mentions Windows/WSL/PowerShell/Docker explicitly.
- You must provide shell commands that could differ by OS.
- Paths/permissions/volumes/networking are involved.

## Procedure
1. Determine execution context:
   - Where the command will run (Windows host? WSL? container?).
2. Provide OS-specific variants ONLY if needed:
   - Prefer a single canonical path + “Windows note” if small delta.
3. Guardrails:
   - Avoid reserved PowerShell variables and quoting pitfalls.
   - Avoid whitespace path breakage; use explicit quoting.
4. Validate critical commands with “dry read” steps (e.g., `pwd`, `whoami`, `ls`).

## Output
- “Run in: <context>” + exact command(s) + 1–2 quick verification commands.
