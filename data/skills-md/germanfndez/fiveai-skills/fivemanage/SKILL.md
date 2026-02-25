---
name: fivemanage
description: Fivemanage SDK for FiveM — installation, screenshots (takeImage, takeServerImage, uploadImage), and centralized logs (Log, Info/Warn/Error). Use when integrating Fivemanage, capturing player screenshots, uploading images, or sending logs to the Fivemanage dashboard.
author: germanfndez
version: 1.0.0
mcp-server: projecthub
---

# Fivemanage SDK (FiveM)

Installation, images, and logs for the Fivemanage SDK on FiveM. Use this skill when integrating Fivemanage, capturing screenshots, or sending logs. Docs: https://docs.fivemanage.com/fivem-sdk/installation

## When to use

- User asks how to install or configure the Fivemanage SDK.
- Writing code that captures screenshots (client or server), uploads images, or sends logs to Fivemanage.
- Integrating `exports.fmsdk` in Lua or JavaScript resources.
- Questions about `takeImage`, `takeServerImage`, `uploadImage`, `Log`, `Info`, `Warn`, `Error`, or `config.json`.

## How to use

Read the rule that matches what you're doing:

- **rules/installation.md** — Prerequisites, download, extract to resources, server.cfg (ensure order, API keys).
- **rules/images.md** — Client `takeImage`; server `takeServerImage` and `uploadImage`; metadata (name, description, playerSource).
- **rules/logs.md** — `Log`, `Info`/`Warn`/`Error`, `LogMessage`; datasets; playerSource/targetSource; automatic event logging.
- **rules/configuration.md** — config.json, automatic events, presigned URLs, API keys reminder.
- **rules/reference-links.md** — Official docs and SDK download links.
