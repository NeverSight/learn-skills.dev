---
name: rimsearcher
description: "RimWorld mod development: runtime Def data queries, C# decompilation and source investigation, Harmony patching, API migration, and mechanic research. Uses rimsearcher for Def truth and DecompilerServer for decompiled source evidence."
---

## 1. Project Entry

1. Read `.rimsearcher/README.md` at the project root first. If missing or incomplete, follow [references/setup.md](references/setup.md) to initialize the environment.
2. On first interaction in a session, run `<cli_path> check update` to check for newer releases (ignore failures; upgrades require user authorization following [references/update.md](references/update.md)).

## 2. Tools & Primary Source of Truth

Plan investigation timing and tool combinations autonomously without rigid procedures:

- **rimsearcher CLI** (Runtime Def Data): Located at `<project_root>/.rimsearcher/rimsearcher.exe`.
  > **All syntax, arguments, exit codes, and option details strictly treat `<cli_path> --help` and `<cli_path> <command> --help` as the primary source of truth.**
- **DecompilerServer MCP** (C# Source Decompilation): Inspects game and mod assemblies, examining real source code and IL opcodes.
- **Data-to-Code Bridge**: `classes[]` and polymorphic `$type` extracted via `get <defName> --brief` serve as the standard class name sources to query DecompilerServer.

## 3. Evidence Standards

- **Querying Defs**: Avoid reading local raw XML; always use the CLI (unapplied patches, overrides, and load-order merges produce misleading data).
- **Inspecting Code**: Never guess APIs; always use DecompilerServer. Method signatures, private fields, and algorithms must trace to real source code.
- **Mark Uncertainties**: When the evidence chain is incomplete, label findings `[UNVERIFIED]` and never fabricate conclusions.
