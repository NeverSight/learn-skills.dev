---
name: solidworks-mcp
description: >-
  Install and verify SolidWorks MCP for OpenAI Codex CLI on Windows. Connects
  Codex to SOLIDWORKS via COM for CAD automation (parts, sketches, extrude,
  assemblies). Supports SOLIDWORKS 2019+ with bundled patches. Use when
  installing SolidWorks MCP, configuring .codex/config.toml, connecting to
  SolidWorks, running $solidworks-mcp, or fixing COM/MCP errors.
---

# SolidWorks MCP — Codex Setup

Wire **alisamsam/Solidworks-MCP** into Codex via project `.codex/config.toml`.

## When to use

- First-time Codex + SolidWorks setup on Windows
- MCP tools missing or COM connection fails
- SOLIDWORKS 2019–2025 installed locally

## Quick install (agent runs)

From project root `C:\Users\ThinkPad\Desktop\codex`:

```powershell
powershell -ExecutionPolicy Bypass -File ".agents\skills\solidworks-mcp\scripts\install.ps1"
```

Custom MCP repo path:

```powershell
powershell -ExecutionPolicy Bypass -File ".agents\skills\solidworks-mcp\scripts\install.ps1" -InstallRoot "D:\Tools\Solidworks-MCP"
```

Then: **restart Codex session**, open SOLIDWORKS, run verify per [verify.md](verify.md).

## Agent checklist

```
- [ ] Python 3.10+ and git on PATH
- [ ] Run install.ps1 from Desktop\codex project root
- [ ] Confirm .codex/config.toml has [mcp_servers.solidworks]
- [ ] Run verify.ps1
- [ ] User restarts Codex (new session)
- [ ] User opens SOLIDWORKS before first MCP tool call
- [ ] Test: connect_solidworks + get_solidworks_info
```

## Default paths (this project)

| Item | Path |
|------|------|
| Codex project | `C:\Users\ThinkPad\Desktop\codex` |
| Project MCP config | `C:\Users\ThinkPad\Desktop\codex\.codex\config.toml` |
| MCP repo | `%USERPROFILE%\Projects\Solidworks-MCP` |
| This skill | `.agents\skills\solidworks-mcp\` |

## Invoke in Codex

Explicit:

```text
$solidworks-mcp 安装并验证 SolidWorks MCP 连接
```

Or natural language (implicit match):

```text
连接 SolidWorks，返回版本和已打开文档
```

## MCP tools available

`connect_solidworks`, `get_solidworks_info`, `create_new_part`, `draw_circle`, `extrude_sketch`, `open_document`, `execute_python`, … (22 tools). See [reference.md](reference.md).

## Feature tree fallback

On SOLIDWORKS 2019 / COM late-binding, `list_features`, `get_document_info`, or `list_open_documents` can return incomplete data or COM wrapper errors. If `list_features` only returns `Favorites`, use `execute_python` with `scripts/list_feature_tree_execute_python.py` and enumerate `FeatureByPositionReverse(index)`.

## FEA / Simulation

MCP = CAD only. For static, fatigue, motion → **$solidworks-simulation**

## SOLIDWORKS 2019

Upstream targets 2023–2025. Skill applies `patch-sw2019.ps1` (ProgID `.27`). Tested on `27.4.0`.

## Docs

- [install-windows.md](install-windows.md) — full install
- [verify.md](verify.md) — smoke tests
- [troubleshoot.md](troubleshoot.md) — errors
- [reference.md](reference.md) — API / tools
