---
name: bg-jobs
description: >
  Run and manage background jobs from the terminal. Use this skill when the user wants
  to execute long-running commands in the background, track job status, read job output,
  or manage multiple concurrent processes. Provides job ID tracking, status monitoring,
  and output capture for background tasks.
---

# Background Jobs Skill

Run and manage background jobs from the terminal, with live runtime details and persisted exit metadata.

## Installation Check

```bash
bg --help
```

If not installed:
```bash
uv tool install agentcli-helpers
```

## Usage

`bg` runs commands in your platform shell. On Windows it prefers PowerShell 7, then Windows PowerShell, then `cmd.exe`, launches jobs without a visible console window when PowerShell is available, and expects shell syntax that matches the shell you expect.

### Run a Background Job
```bash
bg run "python long_script.py"
# Returns: abc123 (job ID)
```

```powershell
bg run "python --version"
```

### List All Jobs
```bash
bg list
bg list --json
```

`bg list` shows live job details including status, PID, start time, elapsed runtime, memory usage, and command.

### Check Job Status
```bash
bg status abc123
```

`bg status <id>` refreshes the job before printing JSON. Running jobs may include `elapsed_seconds`, `memory_bytes`, and `cpu_percent`. Finished jobs can also include `finished_at` and `exit_code`.

### Read Job Output
```bash
bg read abc123   # stdout only
bg logs abc123   # stdout + stderr
```

### Remove Job
```bash
bg rm abc123
```

## Workflow Pattern

```bash
# Bash / zsh
JOB_ID=$(bg run "python train_model.py")
bg status $JOB_ID
bg read $JOB_ID
```

```powershell
# PowerShell
$jobId = bg run "python train_model.py"
bg status $jobId
bg read $jobId
```

## Job Storage

Jobs keep runtime state in your OS temp directory under `agentcli_bgjobs/<id>/`:
- `meta.json` - Job metadata (`cmd`, `pid`, `status`, `started_at`, optional `finished_at`, optional `exit_code`, and live runtime fields)
- `stdout.txt` - Standard output
- `stderr.txt` - Standard error

Windows note:
- PowerShell syntax works by default when `pwsh` or `powershell` is available
- Windows background jobs are started hidden, so there is no extra console window to close
- Use explicit `cmd.exe /d /c "..."` if you need cmd-specific syntax

## Status Values

- `running` - Process is still active
- `completed` - Process finished
- `failed` - Process exited with error

## Examples

```bash
# Download large file
bg run "curl -O https://example.com/large_file.zip"

# Run tests in background
bg run "pytest tests/ -v"

# Start a server
bg run "python -m http.server 8000"

# Check one job as JSON
bg status abc123

# Check all running jobs
bg list

# Read merged logs
bg logs abc123
```

```powershell
# Native PowerShell command
bg run "Get-Process | Sort-Object CPU -Descending | Select-Object -First 5"

# Force cmd syntax when needed
bg run "cmd.exe /d /c dir"
```
