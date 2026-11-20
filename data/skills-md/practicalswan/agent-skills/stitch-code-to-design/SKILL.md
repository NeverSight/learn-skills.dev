---
name: stitch-code-to-design
version: "2.0"
last_updated: 2026-09-08
tags: [stitch, design, frontend, html, migration]
description: "Convert an existing frontend into Stitch-ready design assets by extracting static HTML, writing DESIGN.md, creating the design system, and uploading approved files."
license: "Apache-2.0"
---
# Code to Design

Transform your existing frontend code (React + Vite, Next.js, Angular, Vue, etc.) into a Stitch Design so you can iterate and improve it using Stitch.

This skill orchestrates three other skills in sequence:
1. `extract-static-html`: Extract a single self-contained HTML file from your build output or running dev server (e.g., Vite dev server or Angular CLI `ng serve`).
2. `extract-design-md`: Analyze the source code (including Angular `angular.json`, external `.html` templates, theme files, and components) to create a design system (DESIGN.md).
3. `upload-to-stitch`: Upload that HTML file and the design system to your Stitch project.

## Workflow

Follow these steps to convert your existing code.

### Prerequisites

- A running local dev server (e.g. `npm run dev`, `ng serve`) OR a built web application directory containing `index.html` and assets.
- Target Stitch `projectId` (use `list_projects` if unknown).

### Steps

#### 1. Extract Self-Contained HTML

Delegate to the `extract-static-html` skill to generate a standalone HTML file.
Read [stitch-extract-static-html/SKILL.md](../stitch-extract-static-html/SKILL.md) for detailed instructions and script usage.

Expected output: A single file like `/path/to/extracted/standalone.html`.

#### 2. Verify HTML (Optional — User-Driven)

After extraction, inform the user of the output file path so they can manually
verify in a browser if desired. **Do not block on verification** — proceed
directly to Step 3.

If the user reports issues after reviewing, fix them before continuing.

#### 3. Extract Design System (File)

Delegate to the `extract-design-md` skill to analyze the project's source files
(components, stylesheets, theme configs) and produce a design system. Read
[stitch-extract-design-md/SKILL.md](../stitch-extract-design-md/SKILL.md) for the
full analysis workflow.

Write `.stitch/DESIGN.md` following the `extract-design-md` skill's output
structure.

#### 4. Upload DESIGN.md and Create Design System in Stitch

Delegate to the `manage-design-system` skill to upload the `DESIGN.md` and
create the design system in Stitch. Read
[stitch-manage-design-system/SKILL.md](../stitch-manage-design-system/SKILL.md) for
the full workflow (upload script usage, `create_design_system_from_design_md`
call, and required schemas). Pass
`--generated-by 'stitch::code-to-design'` when uploading.

#### 5. Upload HTML to Stitch

Use the same `upload-to-stitch` skill's script to upload the extracted HTML file.
Read [stitch-upload-to-stitch/SKILL.md](../stitch-upload-to-stitch/SKILL.md) for detailed instructions and script usage.

You will need:
- The path to the standalone HTML file generated in Step 1.
- Your Stitch API Key (same key used in Step 4).
- The target `projectId`.
- The `--generated-by` argument set to `'stitch::extract-static-html'`.
- The `--title` argument set to the **route path** of the page (e.g., `'/dashboard'`, `'/settings/profile'`, `'/inbox'`) so that the screen name/title in Stitch clearly identifies its route in the application.

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/stitch-code-to-design` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: Stitch MCP

- Fallback prompt: "Use the Code to Design skill without MCP. Follow the documented local or manual fallback, show the selected tool surface, and report the verification evidence."
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

1. Pass/fail: `.stitch/DESIGN.md` exists and summarizes real source tokens.
2. Pass/fail: The static HTML opens locally enough to inspect core layout and images.
3. Pass/fail: Stitch design-system creation was MCP-verified or the fallback evidence is recorded.
4. Pass/fail: No API key, token, cookie, or credential-bearing config was copied into durable files.
5. Pressure-test scenario: Repeat the workflow with Stitch MCP screen tools unavailable and confirm the fallback path remains honest and actionable.
6. Success metric: The user can identify the exact artifact, project/design-system target, and verification evidence without relying on unstated MCP behavior.

## Related Skills

- [stitch-extract-static-html](../stitch-extract-static-html/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [stitch-extract-design-md](../stitch-extract-design-md/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [stitch-manage-design-system](../stitch-manage-design-system/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [stitch-upload-to-stitch](../stitch-upload-to-stitch/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
