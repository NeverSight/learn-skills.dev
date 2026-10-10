---
name: defold-project-build
description: Builds the project using the running Defold editor, returns build errors, and launches the game if build succeeds.
---

# Build Defold Project via Editor HTTP API

Build and run a Defold project by sending HTTP requests to the running Defold editor.

## Prerequisites

- The Defold editor must be running with the project open.

## Reading the Editor Port

The editor writes its HTTP port to `.internal/editor.port` in the project root. Read this file to get the port number.

**Windows (PowerShell):**
```powershell
$port = Get-Content .internal/editor.port
```

**Linux/macOS:**
```bash
port=$(cat .internal/editor.port)
```

If the file does not exist, the editor is not running or the project is not open.

## Building the Project

Send a POST request to the `/command/build` endpoint.

**Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:$port/command/build" -Method Post
```

**Linux/macOS:**
```bash
curl -X POST "http://127.0.0.1:$port/command/build" --silent
```

The response is JSON with two fields:
- `success` (boolean) — whether the build succeeded.
- `issues` (array) — list of build issues (empty on success).

If `success` is `true`, the build succeeded and the editor launches the game automatically.

If `success` is `false`, each entry in `issues` contains:

| Field | Description |
|-------|-------------|
| `severity` | `"error"` or `"warning"` |
| `message` | Human-readable description |
| `resource` | Absolute project path (e.g. `/main/logo.script`) |
| `range.start.line` | Start line (0-based) |
| `range.start.character` | Start column (0-based) |
| `range.end.line` | End line (0-based) |
| `range.end.character` | End column (0-based) |

## Checking Console Output

After a successful build and launch, read runtime logs from the editor console:

**Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:$port/console" -Method Get
```

**Linux/macOS:**
```bash
curl "http://127.0.0.1:$port/console" --silent
```

## Workflow

1. Read the port from `.internal/editor.port`.
2. POST to `/command/build`.
3. If the build fails, report all issues with file paths, line numbers, and messages.
4. If the build succeeds, the game launches automatically. Check `/console` for runtime logs if needed.

## Troubleshooting

- **Connection refused** — the editor is not running or the port file is stale. Restart the editor and try again.

## Example: Successful Build Response

```json
{
  "success": true,
  "issues": []
}
```

## Example: Failed Build Response

```json
{
  "success": false,
  "issues": [
    {
      "severity": "error",
      "message": "go.property declaration should be a top-level statement",
      "resource": "/main/logo.script",
      "range": {
        "start": { "line": 3, "character": 4 },
        "end": { "line": 3, "character": 35 }
      }
    }
  ]
}
```
