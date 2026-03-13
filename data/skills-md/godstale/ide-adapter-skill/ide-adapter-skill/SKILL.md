---
name: ide-adapter-skill
description: >
  IDEAS (IDE Adapter Skill) - Connect to the IDE Adapter VS Code extension via WebSocket
  to use VS Code features from CLI. Use this skill when the user asks to: search/replace
  text in a codebase, find symbol definitions or references, get diagnostics/errors/warnings,
  list document symbols, search files by name, view git commit history, compare file versions
  (diff), roll back files to a previous git commit, or access VS Code local save history
  (snapshots between commits).
  Triggers: "find all usages of", "go to definition", "show errors in", "git history of",
  "diff current vs HEAD", "roll back to commit", "local history", "find files named",
  "IDEAS", "IDE Adapter".
  Requires: IDE Adapter extension running in VS Code (default port 7200).
---

# IDEAS - IDE Adapter Skill

Connect to the IDE Adapter VS Code extension WebSocket server and use VS Code's language
intelligence, git history, and file system features from Claude Code.

> **Abbreviation**: IDEAS (IDE Adapter Skill) - pronounced "ideas"

## Prerequisites

1. **IDE Adapter extension** must be running in VS Code
2. **Python dependency**: `pip install websocket-client`

## Settings Auto-Detection

The script automatically reads port and token from `.vscode/settings.json` in the current
directory or any parent directory. **No need to pass `--port` or `--token` manually** as long
as the script is run from inside (or below) the workspace directory.

```json
// .vscode/settings.json
{
  "idea.server.port": 7200,
  "idea.server.authToken": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

If explicit values are provided via `--port` / `--token`, those take priority over the file.

## Workflow

### Step 1: Run the client script

```bash
python <skill-dir>/scripts/idea_client.py --topic <topic> --params '<json>'
```

The script: auto-loads settings -> connect -> handshake -> request -> print JSON -> exit.

### Step 2: Parse the response

**Success**: response has `result` key
**Error**: response has `error` key with `code` and `message`

See [references/protocol.md](references/protocol.md) for all result shapes.

---

## Windows (Git Bash) - Required Workarounds

Two issues occur when running `idea_client.py` directly in Git Bash on Windows:

### Issue 1: Path expansion of `/app/vscode/...`

Git Bash expands `/app/vscode/...` to `C:/Program Files/Git/app/vscode/...`, breaking the topic.

**Fix**: Use `MSYS_NO_PATHCONV=1` prefix OR call via Python subprocess (recommended).

### Issue 2: cp949 encoding error

Python's stdout on Korean Windows defaults to cp949, causing `UnicodeEncodeError` when the
response contains non-cp949 characters (e.g., em dash `-` in commit messages).

**Fix**: The script now calls `sys.stdout.reconfigure(encoding="utf-8")` automatically.
However, if running via subprocess from another Python script, pass `encoding='utf-8'`.

### Recommended call pattern on Windows

Always call via Python subprocess to avoid both issues at once:

```python
import subprocess, sys, os

SCRIPT = "C:/Users/<user>/.claude/skills/ide-adapter-skill/scripts/idea_client.py"
env = {**os.environ, "PYTHONIOENCODING": "utf-8"}

result = subprocess.run(
    [sys.executable, SCRIPT, "--topic", "/app/vscode/fs/findFiles",
     "--params", '{"query": "App", "include": "**/*.tsx"}'],
    capture_output=True, text=True, encoding="utf-8", env=env,
    cwd="<workspace-path>"   # ensures .vscode/settings.json is found
)
print(result.stdout)
```

Setting `cwd` to the workspace root ensures `settings.json` is found for auto-detection.

---

## Quick Reference: Common Tasks

### Find files by name
```python
--topic /app/vscode/fs/findFiles --params '{"query": "App", "include": "**/*.tsx"}'
```

### Search text in workspace
```python
--topic /app/vscode/edit/find --params '{"pattern": "IHandler", "include": "**/*.ts"}'
```

### Get diagnostics (errors/warnings)
```python
--topic /app/vscode/diag/list --params '{"filePath": "src/extension.ts", "severity": "error"}'
```

### Find symbol definition (line/character are 0-indexed)
```python
--topic /app/vscode/nav/definition --params '{"filePath": "/abs/path/file.ts", "line": 10, "character": 5}'
```

### Git history of a file
```python
--topic /app/vscode/history/list --params '{"filePath": "src/extension.ts", "maxCount": 10}'
```

### Diff working tree vs HEAD
```python
--topic /app/vscode/history/diff --params '{"filePath": "src/extension.ts", "fromIndex": 0, "toIndex": 1}'
```

### Roll back to a commit (toIndex=1=HEAD, toIndex=2=HEAD~1)
```python
--topic /app/vscode/history/rollback --params '{"filePath": "src/extension.ts", "toIndex": 2}'
```

### VS Code local save history
```python
--topic /app/vscode/localhistory/list --params '{"filePath": "src/extension.ts"}'
```

---

## Full Protocol Reference

See [references/protocol.md](references/protocol.md) for all topics, params, result shapes,
error codes, and index semantics for git history.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `CONNECTION_FAILED` | IDE Adapter not running or wrong port. Check VS Code status bar. |
| `UNAUTHORIZED` | `authToken` missing from `.vscode/settings.json` or wrong value. |
| `UNKNOWN_TOPIC` with `C:/Program Files/Git/...` prefix | Git Bash path expansion. Use subprocess pattern above. |
| `UnicodeEncodeError: cp949` | Update to latest `idea_client.py` (auto-fixes via `reconfigure`). |
| `ModuleNotFoundError: websocket` | Run `pip install websocket-client` |
| `INVALID_REQUEST` | Check required params. `filePath` must be absolute for nav/definition/references. |
| `HANDLER_ERROR` | VS Code internal error. File may not exist or git repo unavailable. |
