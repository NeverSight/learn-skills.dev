---
name: powershell
description: >
  PowerShell best practices for scripts used in FieldWorks (dev scripts & CI helpers).
  Use when writing or modifying PowerShell scripts in scripts/ or Build/Agent/.
allowed-tools: "Read,Bash(pwsh:*)"
version: "1.0.0"
---

# PowerShell Development Skill

Conventions and safety patterns for PowerShell scripts in `scripts/` and CI.

## Style and Linting

- Use `pwsh`/PowerShell Core syntax where possible and `Set-StrictMode -Version Latest`.
- Use `Write-Host` sparingly; prefer `Write-Output` and `Write-Error` for correct streams.
- Use `-ErrorAction Stop` in helper functions when errors should abort execution.
- **No Unicode icons or emojis** in output messages (e.g., `✓`, `✗`, `⚠`, `🔧`). Use plain ASCII text like `[OK]`, `[FAIL]`, `[WARN]`, `ERROR:` instead. Unicode causes encoding issues in CI logs.

## Security

- Avoid embedding secrets in scripts; read from env vars and prefer platform secret stores.
- Do not commit credential tokens in any scripts or docs.

## Testing and Execution

- Use `pwsh -NoProfile -ExecutionPolicy Bypass -File` in CI wrappers.
- Add small smoke test steps to validate paths and required tools are present.

## Auto-Approval Patterns

**CRITICAL**: Agent terminal security blocks complex commands. The following require manual approval:
- Pipes (`|`)
- Semicolons (`;`) or `&&`
- Redirection (`2>&1`)

**ALWAYS use `scripts/Agent/` wrapper scripts for these operations.** Do not attempt raw commands.

See [terminal.instructions.md](../../instructions/terminal.instructions.md) for the complete transformation table.

## Examples

```powershell
# Good: simple commands auto-approve
.\build.ps1
git status

# Good: use wrapper scripts (ALWAYS for git with pipes)
.\scripts\Agent\Git-Search.ps1 -Action show -Ref "release/9.3" -Path "file.h" -HeadLines 20
.\scripts\Agent\Git-Search.ps1 -Action log -HeadLines 20
.\scripts\Agent\Read-FileContent.ps1 -Path "file.cs" -HeadLines 50 -LineNumbers

# BAD: these require manual approval - NEVER USE
# git log --oneline | head -20
# Get-Content file.cs | Select-Object -First 50
```
