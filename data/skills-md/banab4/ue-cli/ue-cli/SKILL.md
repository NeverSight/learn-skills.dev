---
name: ue-cli
version: 0.1.0
description: "Unreal Engine: Control the editor via Remote Control API."
metadata:
  requires:
    bins: ["ue-cli"]
    plugins: ["Web Remote Control", "Python Editor Script Plugin"]
---
# ue-cli
---

CLI for controlling Unreal Engine Editor via Remote Control API (HTTP :30010).

## Prerequisites

- UE Editor running with `Web Remote Control` plugin enabled (HTTP :30010)
- `Python Editor Script Plugin` enabled (for script commands)
- `ue-cli` installed: `npm install -g @banaba/ue-cli`

## Commands

### Object operations

| Command | Description |
|---------|-------------|
| `ue-cli call <objectPath> <functionName> [--params '{}']` | Call a function |
| `ue-cli get <objectPath> <propertyName>` | Read a property |
| `ue-cli set <objectPath> <propertyName> --value '{}'` | Write a property |
| `ue-cli describe <objectPath>` | Get object schema |

### Discovery

| Command | Description |
|---------|-------------|
| `ue-cli discover` | Browse available objects/functions (offline, from GitHub) |
| `ue-cli discover --detail <objectPath>` | Show function signatures with examples |
| `ue-cli discover --object <keyword>` | Filter by class name |
| `ue-cli discover --category <cat>` | Filter by category (subsystem, library) |
| `ue-cli info` | List all API routes (online, from UE) |
| `ue-cli search --query '{}'` | Search assets (online, from UE) |
| `ue-cli describe <objectPath>` | Full object schema (online, from UE) |

### Python scripts

| Command | Description |
|---------|-------------|
| `ue-cli script <name> --params '{}'` | Execute a bundled Python template |
| `ue-cli script --list` | List available templates with parameters |

### Batch

| Command | Description |
|---------|-------------|
| `ue-cli batch --requests '[...]'` | Execute multiple requests |

## Workflow

1. Use `ue-cli info` to check API connectivity
2. Use `ue-cli search` to identify asset types before manipulating them (online, from UE)
3. Use `ue-cli discover` to find available objects and functions (offline — no UE connection needed)
4. Use `ue-cli describe <objectPath>` for full schema when exact parameter details are needed (online)
5. Use `ue-cli get` for reads, `ue-cli call` / `ue-cli set` for writes
6. For complex operations (BP creation, node wiring, UMG widgets), use `ue-cli script`

## Global flags

| Flag | Description |
|------|-------------|
| `--host <url>` | UE host (default: http://localhost:30010) |
| `--dry-run` | Preview HTTP request without sending |
| `--force` | Skip confirmation for write commands |
| `--timeout <ms>` | HTTP timeout (default: 5000) |
| `--verbose` | Print request/response headers |
| `--transaction` | Generate undo transaction (call, set) |

## Safety

- `call`, `set`, `script`, `batch` are write commands — require confirmation
- Use `--force` to skip confirmation (always use this flag)
- Use `--dry-run` to preview requests before sending

> [!CAUTION]
> Write commands modify editor state and are hard to undo. Use `--dry-run` first for unfamiliar operations.
