---
name: autocad-agent
description: "Automate AutoCAD drafting and CAD workflows through doc-driven execution: discover installed AutoCAD/Core Console/API access, retrieve official/local command and API documentation, generate AutoLISP, scripts, .NET guidance, DXF transformations, or command sequences, validate drawings, diagnose blockers, and search trusted Autodesk forums when needed. Use when Codex is asked to create, modify, batch process, debug, or explain AutoCAD drawings, DWG/DXF files, layers, blocks, dimensions, plotting, standards checks, or CAD automation."
---

# AutoCAD Agent

## Overview

Use this skill to convert AutoCAD drafting requests into reproducible scripts/macros, drawing transformations, plots, and validation notes. Prefer documented AutoCAD command-line, AutoLISP, Core Console, DXF, and API workflows over manual clicking.

## Workflow

1. Frame the CAD task: identify file format, units, layers, blocks, styles, dimensions, plotting requirements, standards, and validation criteria.
2. Discover access: check AutoCAD installation, platform, Core Console availability, AutoLISP support, and relevant APIs.
3. Retrieve docs first: use official command/API docs, local help, command names, and file format references before generating scripts.
4. Generate reproducible automation: create `.scr`, `.lsp`, DXF transforms, or API code that can be rerun.
5. Run or guide execution: use Core Console or script execution when available; otherwise provide exact UI steps for unavoidable UI-only actions.
6. Diagnose and unblock: use `references/blocker-remediation.md` for missing commands, unsupported platform features, file locks, plot devices, fonts, and permissions.
7. Search forums when needed: use `references/community-troubleshooting.md` after official docs and local diagnostics are insufficient.
8. Report artifacts: list generated scripts, DWG/DXF/PDF outputs, logs, and assumptions.

## Resources

- `references/software-notes.md`: AutoCAD-specific automation surfaces and artifacts.
- `references/blocker-remediation.md`: legitimate ways to resolve installation, platform, font, plot, permission, and API blockers.
- `references/community-troubleshooting.md`: trusted forum search process.

Never overwrite original drawings without making a copy. Preserve units, layers, coordinates, and object handles where possible.
