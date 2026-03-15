---
name: install-sandbox-psu
description: Installs PowerShell Universal in a sandboxed environment, allowing for isolated testing and development of custom components without affecting the global system configuration. This skill sets up a local instance of PowerShell Universal with minimal configuration, ideal for development and experimentation.
---

# install-sandbox-psu

Spins up a fully isolated PowerShell Universal (PSU) sandbox — either by downloading a pre-built release from the Devolutions CDN or by building and publishing a local .NET project. Each sandbox gets its own data directory, port, log paths, and generated relaunch/teardown scripts, so multiple sandboxes of the same version can run side-by-side without interfering.

## When to use

- Quickly test a released version of PSU without a system-wide install
- Run the current branch of a PSU source repo against a clean data directory
- Reproduce bugs in an isolated environment you can throw away
- Develop and test custom PSU components (pair with `custom-component-generate-psu`)

## Prerequisites

- PowerShell 7 (`pwsh`)
- Internet access

## Script

`.agents/skills/install-sandbox-psu/scripts/Install-PSU.ps1`

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `-PSUVersion` | `"latest"` | Version to install from CDN (e.g. `"2025.3.1.0"`). |
| `-SandboxId` | _(random 6-char hex)_ | A name to identify this sandbox. Reuse the same ID to restart against the same data directory and port. |
| `-Empty` | — | _(default parameter set)_ Start with an empty PSU repository — no configuration seeded. |
| `-ConfigurationDirectory` | _(none)_ | Path to a directory whose contents are copied into the PSU repository folder before the server starts. Mutually exclusive with `-GitRepo` and `-Empty`. |
| `-Git` | — | Use git to clone a repository. Use `GitRepo` to specify the URL. Uses the demo repo by default. |
| `-GitRepo` | `"https://github.com/Devolutions/powershell-universal-demo"` | Git repository URL to clone into the PSU repository folder before the server starts. Mutually exclusive with `-ConfigurationDirectory` and `-Empty`. |
| `-Teardown` | — | Stop the running server process and delete the entire sandbox folder. Requires `-SandboxId`. |
| `-List` | — | List all existing sandboxes under `$env:TEMP`, showing URL, SandboxId, source, creation time, and running status. |
| `-Features` | _(none)_ | Optional list of PSU features/plugins to enable. Supported values: `MCP`, `C#`, `YARP`. |
| `-DatabaseType` | `"SQLite"` | Database backend to use. Options: `SQLite`, `SQL` (SQL Server), `PostgreSQL`. |
| `-DatabaseConnectionString` | _(auto for SQLite)_ | Connection string for the selected database. When omitted with SQLite, defaults to a file in the sandbox data directory. |

## Sandbox layout

Each sandbox lives at `$env:TEMP\PSUSandbox-<version>-<sandboxId>\`:

```
PSUSandbox-2026.1.3.0-a3f9c2\
  psu\                  PSU binaries (extracted zip or dotnet publish output)
  data\
    repository\         PSU configuration repository
    psu.db              SQLite database
  logs\
    systemlog.txt
  agent\logs\
    log.txt
  Dashboard\            UniversalDashboard assets folder
  sandbox.json          Stored config for reproducible relaunches
  Start-Sandbox.ps1     Auto-generated relaunch script (no rebuild)
  Remove-Sandbox.ps1    Auto-generated teardown script
```

## Environment variables set

The following are set as process-scoped environment variables before launching the server, so the child process inherits them:

| Variable | Value |
|---|---|
| `Data__ConnectionString` | `Data Source=<root>\data\psu.db` |
| `Data__RepositoryPath` | `<root>\data\repository` |
| `SystemLogPath` | `<root>\logs\systemlog.txt` |
| `PsuAgentLogPath` | `<root>\agent\logs\log.txt` |
| `Kestrel__Endpoints__HTTP__Url` | `http://*:<port>` |
| `UniversalDashboard__AssetsFolder` | `<root>\Dashboard` |

Port is auto-selected from the unused range 5001–6000 on first run and stored in `sandbox.json` for all subsequent runs.

## Usage examples

### Install and run the latest CDN release (empty sandbox)

```powershell
pwsh .agents/skills/install-sandbox-psu/scripts/Install-PSU.ps1
```

### Seed from the default demo Git repo

```powershell
pwsh Install-PSU.ps1 -GitRepo
```

### Seed from a custom Git repo

```powershell
pwsh Install-PSU.ps1 -GitRepo https://github.com/myorg/my-psu-config -SandboxId myconfig
```

### Seed from a local configuration directory

```powershell
pwsh Install-PSU.ps1 -ConfigurationDirectory C:\myconfig -SandboxId myconfig
```

### Install a specific version

```powershell
pwsh Install-PSU.ps1 -PSUVersion 2025.3.1.0 -SandboxId testing
```

### List all sandboxes

```powershell
pwsh Install-PSU.ps1 -List
```

### Tear down a sandbox

```powershell
# Stops the process and deletes the entire folder
pwsh Install-PSU.ps1 -Teardown -SandboxId dev

# Or run the generated script directly
pwsh "$env:TEMP\PSUSandbox-local-dev\Remove-Sandbox.ps1"
```

If the teardown fails, don't force close any processes. Let the user know which locks are preventing cleanup so they can investigate or try again after a reboot.

## Expected output

On successful start:

```
==========================================
  PSU Sandbox Started
  Version    : 2026.1.3.0
  Source     : cdn:2026.1.3.0
  SandboxId  : a3f9c2
  URL        : http://localhost:5001
  Process ID : 12345
  Root       : C:\Users\...\Temp\PSUSandbox-2026.1.3.0-a3f9c2
  Relaunch   : ...\Start-Sandbox.ps1
  Teardown   : ...\Remove-Sandbox.ps1
==========================================
```

## Notes

- The CDN zip is cached in `$env:TEMP` and reused across sandbox instances of the same version — only the data directory is per-sandbox.
- `sandbox.json` stores the port and all paths. Re-running `Install-PSU.ps1` with the same `-SandboxId` reuses the existing port and data, making runs reproducible.
- The script is idempotent: running it twice with the same `-SandboxId` starts the server against the existing data without re-downloading or re-extracting.

