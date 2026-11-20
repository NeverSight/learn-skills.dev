---
name: spreadsheet-formula-helper
version: "2.0"
last_updated: 2026-09-08
tags: [spreadsheet, formula, helper, documents, automation]
description: "Write and debug spreadsheet formulas (Excel/Google Sheets), pivot tables, and array formulas; translate between dialects; use when users need working formulas with examples and edge-case checks."
---
# Spreadsheet Formula Helper

Produce reliable spreadsheet formulas with explanations.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Inputs to gather
- Platform (Excel/Sheets), locale (comma vs. semicolon separators), sample data layout (headers, ranges), expected outputs, and constraints (volatile functions allowed?).
- Provide small example rows and the desired result for them.

## Workflow
1) Restate the problem with explicit ranges and sheet names; propose a minimal sample to verify.
2) Draft formula(s); when dynamic arrays are available, prefer them over copy-down formulas.
3) Explain how it works and where to place it; include named ranges if helpful.
4) Edge cases: blank rows, mixed types, timezone/date quirks, duplicates; offer guardrails (e.g., `IFERROR`, `LET`, `LAMBDA`).
5) Variants: if porting between Excel and Sheets, provide both versions.

## Output
- Primary formula, short explanation, and a 2-3 row worked example showing inputs to outputs.
- Optional: quick troubleshooting checklist for common errors.

## MCP Fallback – Native Automation

When MCP is unavailable, use native automation: local spreadsheet formulas, `openpyxl` for workbook inspection, CSV fixtures for examples, and manual recalculation notes for functions the local engine cannot evaluate. Preserve locale separators, absolute references, dynamic arrays, and Excel-vs-Sheets differences before claiming success.

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/spreadsheet-formula-helper` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Spreadsheet Formula Helper skill without MCP. Rely on its local instructions, bundled resources, standard shell or editor tools, and direct verification. Show the evidence used before concluding."
- Do not claim an MCP operation was used when the active host does not expose it.
- Treat local files, tests, rendered outputs, logs, or screenshots as the fallback evidence path.

<!-- MCP:END -->

## Anti-Patterns

- Treating source content as already clean: Formatting automation will happily preserve broken or inconsistent input.
- Skipping an open-file verification pass: Documents and spreadsheets often fail in the destination app, not in the script output.
- Automating irreversible edits without checkpoints: A small mapping mistake can affect an entire workbook or document.

## Verification Protocol

Before claiming the `spreadsheet-formula-helper` workflow succeeded:

1. Pass/fail: The request matches this skill's documented activation boundary.
2. Pass/fail: Required inputs, dependencies, and safety checks were resolved or reported as blockers.
3. Pass/fail: The narrowest relevant workflow was completed without inventing unavailable tools or results.
4. Pass/fail: Output was checked with the most relevant local test, inspection, render, or source evidence.
5. Pressure test: Repeat the decision with the preferred integration unavailable and confirm the fallback remains safe and actionable.
6. Success metric: The result, evidence, and any unverified limitation are explicit enough for another agent to reproduce.

## Related Skills

- [documentation-authoring](../documentation-authoring/SKILL.md): Use it when the workflow also needs drafting structured technical or product documents.
- [notion-docs](../notion-docs/SKILL.md): Use it when the workflow also needs Notion page and database publishing workflows.
- [pdf](../pdf/SKILL.md): Use it when the workflow also needs PDF extraction, generation, and layout-aware review.
- [word-document](../word-document/SKILL.md): Use it when the workflow also needs Word document authoring and formatting workflows.
