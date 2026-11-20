---
name: stitch-extract-design-md
version: "2.0"
last_updated: 2026-09-08
tags: [stitch, design-system, frontend, tokens, audit]
description: "Extract a Stitch-compatible DESIGN.md from frontend source code, stylesheets, Tailwind config, theme files, and component patterns."
license: "Apache-2.0"
---
# Stitch Extract DESIGN.md From Source

This skill is a catalog-normalized import from `https://github.com/google-labs-code/stitch-skills` at commit `7b53207b94e62911777d53d4238b5f8c88c2b519`, source path `plugins/stitch-design/skills/extract-design-md`. The upstream control file was corrected for this workspace: the verified Stitch MCP surface here is design-system oriented, so screen lookup, screen generation, and screen editing tools must be used only when the current host explicitly exposes them.

## When to Use This Skill

- Use when source code should reveal the visual system before a Stitch upload or generation workflow.
- The task involves Google Stitch project IDs, `.stitch/` artifacts, DESIGN.md files, Stitch exports, or Stitch-specific validation.
- The broader `stitch-design` router points here as the narrowest workflow.

## Workflow

1. Detect the framework and read the closest file under `references/`: React/Tailwind, Vue, Svelte, Angular, or plain CSS.
2. Read theme config, global CSS, font imports, layout roots, representative components, and state styles.
3. Extract actual colors, fonts, spacing, radii, shadows, variants, and responsive rules.
4. Name tokens semantically and keep exact values next to descriptive labels.
5. Write `.stitch/DESIGN.md` using atmosphere, palette, typography, components, layout, and generation notes.
6. Hand off to `stitch-manage-design-system` when the user wants upload.

## Local Assets

- `examples/`, `resources/`, `references/`, or `reference/` are upstream support material when present. Treat `SKILL.md` as the source of truth if a support file mentions an unavailable MCP tool.
- `scripts/` are optional helpers. On Windows, prefer PowerShell or Node equivalents unless Git Bash or WSL is actually available.
- Keep generated `.stitch/` files out of commits unless the user explicitly wants them as durable examples.

## Corrected Stitch MCP Surface

Verified in this workspace on 2026-06-15: `create_project`, `upload_design_md`, `create_design_system_from_design_md`, `list_design_systems`, and `apply_design_system`. This 2026-07-29 source refresh did not re-verify a broader live MCP surface. Do not claim `list_projects`, `list_screens`, `get_project`, `get_screen`, `generate_screen_from_text`, `edit_screens`, or `generate_variants` were used unless the current host exposes those exact tools in the active tool list.

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/stitch-extract-design-md` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: Stitch MCP

- Fallback prompt: "Use the Stitch Extract DESIGN.md From Source skill without MCP. Follow the documented local or manual fallback, show the selected tool surface, and report the verification evidence."
- Use local `.stitch/` artifacts, exported HTML or screenshots, bundled scripts, and the Stitch web UI when the host does not expose the needed Stitch MCP operation.
- Do not claim screen lookup, generation, editing, or variant MCP calls unless those tools are present in the active host tool list.
- Do not claim an MCP operation was used when the active host does not expose it.

<!-- MCP:END -->

## Anti-Patterns

- Claiming a Stitch screen-generation, screen-editing, or screen-retrieval MCP call succeeded when the active host does not expose that tool.
- Uploading files, screenshots, HTML, markdown, or design assets to Stitch without user-approved destination and artifact details.
- Reading, printing, storing, or committing Stitch API keys, MCP config secrets, cookies, or credential-bearing files.
- Treating generated design or code as final without local render, syntax, or artifact verification.
- Collapsing this workflow into a broader frontend/design skill when Stitch-specific files, project IDs, or design-system assets matter.

## Verification Protocol

Before claiming this skill was applied successfully:

1. Pass/fail: Every color and typography claim is traceable to source or marked as inference.
2. Pass/fail: Framework guidance was selected correctly.
3. Pass/fail: The DESIGN.md translates technical values into semantic design language.
4. Pass/fail: No fabricated brand claims, metrics, or unsupported implementation details were introduced.
5. Pressure-test scenario: Repeat the workflow with Stitch MCP screen tools unavailable and confirm the fallback path remains honest and actionable.
6. Success metric: The user can identify the exact artifact, project/design-system target, and verification evidence without relying on unstated MCP behavior.

## Related Skills

- [stitch-design-md](../stitch-design-md/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [stitch-manage-design-system](../stitch-manage-design-system/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [frontend-design](../frontend-design/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
