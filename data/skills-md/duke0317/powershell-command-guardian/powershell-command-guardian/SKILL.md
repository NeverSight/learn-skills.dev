---
name: powershell-command-guardian
description: Review, diagnose, and rewrite Windows PowerShell 5.1 and PowerShell 7+ commands for version compatibility, quoting, paths, encoding, native executable arguments, error propagation, and destructive-operation safety. Use when a user asks to convert shell commands to PowerShell, fix a PowerShell command or error, check whether a command is safe on Windows, or make a script work across PowerShell versions.
---

# PowerShell Command Guardian

Review PowerShell commands before execution. Preserve intent and semantics; do not perform blind text substitution.

## Workflow

1. Determine target environment from explicit context:
   - Windows PowerShell 5.1 (`powershell.exe`) or PowerShell 7+ (`pwsh`)
   - interactive shell, script, CI runner, WSL, Git Bash, or container
   - PowerShell cmdlets versus native executables
   - working directory and path dialect
2. If version or host changes the correct answer materially, ask for it. When execution cannot pause, provide clearly labeled 5.1 and 7+ variants.
3. Audit command using checks below.
4. Rewrite only broken or unsafe parts. Preserve failure behavior, data flow, quoting, interpolation, and command order.
5. Explain concrete findings. Do not claim a command is perfectly safe or guaranteed to run without testing it in target environment.

## Audit checks

### Version compatibility

- Reject PowerShell 7-only syntax in a 5.1 target, including `&&`, `||`, `??`, ternary expressions, pipeline chain operators, and `ForEach-Object -Parallel`.
- Prefer `$PSVersionTable.PSVersion` when runtime inspection is available.
- Do not silently default unknown environments to 5.1 when that could change behavior. State uncertainty or provide both variants.
- Add `-UseBasicParsing` to `Invoke-WebRequest` only for Windows PowerShell 5.1 compatibility. Do not add it to PowerShell 7 commands.

### Encoding

- Separate console encoding, native-process pipe encoding, and file encoding. They are different settings.
- Do not present `[Console]::OutputEncoding` as a fix for file encoding.
- In Windows PowerShell 5.1, remember that `Out-File` and redirection operators normally write UTF-16LE. `-Encoding utf8` writes UTF-8 with BOM.
- In PowerShell 7+, text output cmdlets normally use `utf8NoBOM`; still specify `-Encoding` when a consumer requires an exact format.
- For UTF-8 without BOM in Windows PowerShell 5.1, use a suitable .NET API such as `[IO.File]::WriteAllText($path, $text, [Text.UTF8Encoding]::new($false))`.
- Warn before rewriting a file when encoding, newline style, or final newline may change.

### Paths and quoting

- Keep URLs and URI paths unchanged.
- Do not replace every `/` with `\`. PowerShell, .NET APIs, native tools, WSL, Git Bash, and containers interpret paths differently.
- Quote paths containing spaces or PowerShell metacharacters.
- Use single quotes for literal strings. Use double quotes only when interpolation or escape processing is intended.
- Preserve provider paths, UNC paths, extended-length paths, registry paths, and wildcard behavior.
- Convert `/mnt/c/...`, `/c/...`, and container paths only after identifying their source environment and intended Windows destination.

### Command semantics

- Do not mechanically map Unix commands to similarly named cmdlets. Compare semantics first.
- Preserve conditional execution. In PowerShell 5.1, translate `cmd1 && cmd2` using explicit success checks appropriate to cmdlets or native processes; do not replace it with `;`.
- Distinguish `$?`, `$LASTEXITCODE`, terminating errors, and non-terminating errors.
- Preserve stdout, stderr, pipeline object types, glob expansion, environment-variable lifetime, and exit codes when relevant.
- Prefer splatting, arrays, or natural PowerShell line breaks over fragile backtick continuation.
- For native executables, account for PowerShell version-specific argument passing and the executable's own parser.

### Destructive operations

- Treat deletion, overwrite, permission, registry, service, process, disk, firewall, package, and remote-execution commands as high risk.
- Show resolved target and scope before proposing a destructive command.
- Prefer `-LiteralPath` when wildcards are not intended.
- Do not add `-Force`, recursion, elevation, or confirmation suppression unless required by user intent.
- Require explicit confirmation before execution when an operation is irreversible or affects data outside stated scope.

## Output

Use compact Markdown:

````markdown
### Findings
- [severity] Concrete problem and consequence.

### Corrected command
```powershell
# corrected command
```

### Assumptions
- Target: PowerShell 7 on Windows 11.
````

Omit empty sections. If original command is already valid, say so and avoid cosmetic rewriting.

## Examples

Input:

```text
Convert `test -d /mnt/d/data/cache && echo ready` from WSL to Windows PowerShell 5.1.
```

Output approach:

```powershell
if (Test-Path -LiteralPath 'D:\data\cache' -PathType Container) {
    Write-Output 'ready'
}
```

Explain that `/mnt/d/...` was interpreted as a WSL path and that the conditional behavior was preserved without using PowerShell 7 pipeline-chain syntax.

Input:

```text
Write Chinese JSON as UTF-8 without BOM in Windows PowerShell 5.1.
```

Output approach:

```powershell
$json = $data | ConvertTo-Json -Depth 10
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($path, $json, $utf8NoBom)
```

Explain that console output encoding does not control `WriteAllText` file encoding.
