---
name: 1c-project-init
description: Initialize or enrich a 1C project with AI workspace skills, docs, templates. Use when user says "инициализируем проект", "init project", or asks to set up a 1C project.
argument-hint: [target-path]
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - AskUserQuestion
---

# /1c-project-init — Initialize or enrich 1C project

Source workspace: `YOUR_KIT_ROOT` (path where 1c-ai-development-kit is cloned)

## Mode detection

- `.claude/skills/` exists in target → **enrich** (sync missing/outdated skills & docs)
- No `.claude/skills/` → **new** (full init)

## Steps

### 1. Determine target path
- If argument provided → use it
- Otherwise → current working directory (`pwd`)

### 2. Run init script

```powershell
powershell.exe -NoProfile -File "YOUR_KIT_ROOT\.claude\skills\1c-project-init\scripts\init.ps1" -TargetPath "<target>" -Mode <new|enrich>
```

Script output lists what was copied/updated.

### 3. If mode = new — collect project info interactively

Ask user (AskUserQuestion):
1. Project name (for CLAUDE.md header)
2. 1C base name (e.g. `Minim_kg`, `Buh`)
3. Platform version: `8.3.24` / `8.3.25` / `8.3.27`
4. Web publication name (e.g. `minim`, `buh`) — for HTTP API and playwright
5. Project type: `extension` / `configuration` / `external-processor`
6. EDT project name (Latin, e.g. `MyProject_25`) — for edt-mcp reference

Platform → server mapping (all on CT107 / YOUR_EDT_SERVER):
- `8.3.24` → server `YOUR_EDT_SERVER:1641`, container `onec-server-24`, web port `8081`
- `8.3.25` → server `YOUR_EDT_SERVER:1541`, container `onec-server-25`, web port `8080`
- `8.3.27` → server `YOUR_EDT_SERVER:1741`, container `onec-server-27`, web port `8082`

### 4. Generate CLAUDE.md

Read template: `YOUR_KIT_ROOT\.claude\skills\1c-project-init\templates\CLAUDE.md.template`
Fill all placeholders:
- `{{PROJECT_NAME}}` — project name
- `{{PROJECT_DESCRIPTION}}` — brief description
- `{{V8_VERSION}}` — platform version (e.g. `8.3.25`)
- `{{SERVER}}` — `YOUR_EDT_SERVER`
- `{{PORT}}` — from platform map
- `{{SERVER_SUFFIX}}` — `24` / `25` / `27`
- `{{WEB_PORT}}` — from platform map
- `{{BASE_NAME}}` — 1C base name
- `{{PUBLICATION}}` — web publication name
- `{{EDT_PROJECT_NAME}}` — EDT project name

Write to `<target>/CLAUDE.md`.

### 5. Generate .mcp.json

Read template: `YOUR_KIT_ROOT\.claude\skills\1c-project-init\templates\mcp.json.template`
Replace `{{PROJECT_NAME}}` and `{{PUBLICATION}}` placeholders.
Write to `<target>/.mcp.json`.

### 6. Generate .v8-project.json if not exists

Use platform map to fill server/port automatically:

```json
{
  "v8path": "",
  "infobase": {
    "server": "YOUR_EDT_SERVER:<PORT>",
    "ref": "<BASE_NAME>",
    "user": "",
    "password": ""
  },
  "publication": "http://YOUR_EDT_SERVER:<WEB_PORT>/<PUBLICATION>"
}
```

### 7. Create openspec structure if mode = new

```
openspec/
  project.md        ← project context for AI
  changes/          ← active proposals
  specs/            ← feature specs
  archive/          ← done
```

### 8. Report

List what was created/updated. Remind user to configure:
- `v8path` in `.v8-project.json`
- MCP port in `.mcp.json` if using minimkg-enhanced
- Open project with `claude` in target directory

### 9. Register in EDT (optional)

Ask: "Зарегистрировать проект в EDT на CT107?"

If yes — determine mode:
- Project already has `src/` with 1C XML and `.project` file → mode=`project`
- Project has `src/` with 1C XML but no `.project` → mode=`xml`
- Only `.dt` available → mode=`dt`

Run:
```powershell
powershell.exe -NoProfile -File "YOUR_KIT_ROOT\.claude\skills\1c-project-init\scripts\edt-import.ps1" `
  -Mode <mode> -Source "<path-on-CT107>" -ProjectName "<EDT_PROJECT_NAME>" `
  -PlatformVersion "<V8_VERSION>" -ServerVersion "<SERVER_SUFFIX>"
```

For dt mode with extensions add `-WithExtensions`.
After import verify with `edt-mcp list_projects`.

**EDT project name rules:** Latin only, no Cyrillic, no spaces. Convention: `<ProjectName>_<ServerSuffix>` (e.g. `MyProject_25`).

## Enrich mode specifics

Compare skill files by content hash — copy only if workspace version is newer or file missing in target.
Always overwrite `.claude/docs/` (platform specs don't change per-project).
Never overwrite: `CLAUDE.md`, `.mcp.json`, `.v8-project.json`, `openspec/`.
