---
name: powershell-style-guide
description: "Style, review, and refactoring standards for PowerShell scripting. Trigger when `.ps1`, `.psm1`, `.psd1` files, or CI workflow blocks with `shell: pwsh` or `shell: powershell` are created, modified, or reviewed and PowerShell-specific quality controls (error handling, parameter validation, readability, operational safety) must be enforced. Do not use for Bash, generic POSIX `sh`, or language-specific application style rules. In multi-language pull requests, run together with other applicable `*-style-guide` skills."
---

# PowerShell Style Guide

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

Use this skill to write and review PowerShell scripts that are predictable, secure, and maintainable for local automation and CI.

## Trigger And Co-activation Reference

- If available, use `references/trigger-matrix.md` for canonical co-activation rules.
- If available, resolve style-guide activation from changed files with `python3 scripts/resolve_style_guides.py <changed-path>...`.
- If available, validate trigger matrix consistency with `python3 scripts/validate_trigger_matrix_sync.py`.

## Quality Gate Command Reference

- If available, use `references/quality-gate-command-matrix.md` for CI check-only and local autofix mapping.

## Quick Start Snippets

### Script skeleton with strict mode and fail-fast behavior

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Failure {
    param(
        [string]$Message,
        [System.Exception]$Exception
    )

    Write-Error "$Message`n$($Exception.Message)"
}

try {
    # Main logic
    Write-Host 'Script started'
}
catch {
    Write-Failure -Message 'Unhandled failure' -Exception $_.Exception
    exit 1
}
```

### Required environment variable check

```powershell
$apiToken = $env:API_TOKEN
if ([string]::IsNullOrWhiteSpace($apiToken)) {
    throw 'API_TOKEN is required.'
}
```

### Parameter validation and approved verbs

```powershell
function Get-ReleaseArtifact {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [string]$ArtifactId,

        [ValidateSet('dev', 'staging', 'prod')]
        [string]$Environment = 'dev'
    )

    # Implementation
    "artifact=$ArtifactId env=$Environment"
}
```

### Bounded retry with backoff

```powershell
function Invoke-WithRetry {
    param(
        [Parameter(Mandatory)]
        [scriptblock]$Operation,
        [int]$MaxAttempts = 5,
        [int]$DelaySeconds = 2
    )

    for ($attempt = 1; $attempt -le $MaxAttempts; $attempt++) {
        try {
            return & $Operation
        }
        catch {
            if ($attempt -eq $MaxAttempts) { throw }
            Start-Sleep -Seconds $DelaySeconds
        }
    }
}
```

### Safe external command invocation

```powershell
$arguments = @(
    '--fail'
    '--silent'
    '--show-error'
    '--header'; "Authorization: Bearer $env:API_TOKEN"
    'https://example.com/health'
)

& curl @arguments
```

## Structure And Readability

1. Use approved PowerShell verb-noun naming (`Get-`, `Set-`, `Invoke-`, `Test-`).
2. Prefer functions with explicit parameters over global mutable state.
3. Keep scripts orchestration-focused and move reusable logic to functions/modules.
4. Replace magic numbers with named constants including units.
5. Add short comments only where intent is non-obvious.

## Parameters, Types, And Data Handling

1. Use `[CmdletBinding()]` for advanced functions where appropriate.
2. Validate input with `ValidateNotNullOrEmpty`, `ValidateSet`, or explicit checks.
3. Use typed parameters/returns for non-trivial data.
4. Avoid implicit string parsing when structured objects are available.
5. Prefer splatting for complex command arguments.

## Error Handling And Control Flow

1. Set `$ErrorActionPreference = 'Stop'` for fail-fast scripts.
2. Use `try/catch/finally` for boundary error handling and cleanup.
3. Throw specific, actionable errors.
4. Do not suppress failures without explicit rationale.
5. Return non-zero exit codes for automation-visible failures.

## Security And Operational Safety

1. Treat all external input as untrusted.
2. Avoid command injection by separating command and arguments.
3. Never print secrets; redact sensitive values in logs.
4. Use least privilege and avoid unnecessary elevation.
5. Validate file paths and destructive command targets.

## Performance And Scalability

1. Prefer pipeline/object operations over repeated text parsing when feasible.
2. Avoid unnecessary process spawning in loops.
3. Use streaming (`Get-Content -ReadCount`, pipeline) for large inputs.
4. Use bounded retries with explicit constants.

## Testing And Verification

1. Add Pester tests for critical behavior and failure paths.
2. Cover edge cases: missing env vars, invalid parameters, timeout, transient errors.
3. Document manual verification where environment dependencies exist.
4. Validate idempotency for repeatable automation scripts.

### Minimal Pester example

```powershell
Describe 'Get-ReleaseArtifact' {
    It 'throws when ArtifactId is empty' {
        { Get-ReleaseArtifact -ArtifactId '' } | Should -Throw
    }
}
```

## CI Required Quality Gates (check-only)

1. Run `Invoke-ScriptAnalyzer` in check mode with fail-on-issue policy.
2. Run formatting/lint check (`Invoke-Formatter -Check` or repository equivalent).
3. Run `Invoke-Pester`.
4. Reject changes that rely on implicit failures or silent fallbacks.

## Optional Autofix Commands (local)

1. Run `Invoke-Formatter` (or repository formatter autofix command).
2. Apply safe `Invoke-ScriptAnalyzer -Fix` results, then rerun checks.
