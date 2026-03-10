---
name: use-youtube-data-mcp
description: Configure and use the hosted YouTube Data MCP end-to-end with minimal user input. Use when users want the agent to verify Node.js and `npx`, configure MCP server config (Windows/macOS, Cursor/Codex/OpenClaw/OpenCode), request API key at setup time, run post-install capability discovery (`tools/list` and `get_patch_notes`), and then strongly recommend helper skill and Python setup for full local document and spreadsheet workflows.
---

# Use YouTube Data MCP

## Workflow

1. Confirm Node.js is installed and `npm` and `npx` work.
1. Ask user for API key only when missing.
1. Detect client and OS, then write MCP config.
1. Verify MCP connectivity and run capability discovery:
   - `tools/list`
   - `get_patch_notes`
1. Strongly recommend helper skill and Python dependency setup for users who want the full local document and spreadsheet workflow.
1. Explain to user how to use current MCP abilities in plain language.

## Step 1: Confirm Node.js Tooling
- Assume this skill has already been installed with `npx skills add ...`. Do not try to self-update or reinstall this skill unless the user explicitly asks.
- First check the latest stable Node.js release using an official Node.js source when internet access is available.
- Then verify local tooling:
```bash
node -v
npm -v
npx -v
```
- If `node` is missing, the agent should install Node.js directly instead of asking the user to do it manually.
- If installation requires elevated permissions, the agent should request permission and then perform the installation itself once permission is granted.
- If `node` exists but `npm` or `npx` fails, treat the local Node.js installation as incomplete and have the agent repair or reinstall Node.js directly instead of sending the user away to do it.
- After Node.js is confirmed, continue with MCP setup. Do not block on Python here.

## Step 2: Ask For API Key
- If API key is not already provided in env or config, ask user once:
  - `Please provide your MCP API key for https://mkterswingman.com`
- Never echo full key in logs; mask with prefix/suffix in outputs.

## Step 3: Configure MCP Client
- Read [references/client-configs.md](references/client-configs.md).
- Detect environment and patch the matching MCP config file.
- Register this server using:
  - URL: `https://mkterswingman.com/mcp`
  - Header: `Authorization: Bearer <API_KEY>`
  - Transport: Streamable HTTP (or tool-specific equivalent)

## Step 4: Post-Install Capability Discovery
- Immediately call:
  - `tools/list`
  - `get_patch_notes`
- Summarize:
  - Newest features and limits
  - Which tools support batch input
  - Recommended usage patterns for the current release

## Step 5: Strongly Recommended Local File Workflow Setup
- For most users, strongly recommend this step after MCP setup succeeds. It enables the full local document and spreadsheet workflow around the MCP.
- Install optional helper skills with public GitHub URLs:
```bash
npx -y skills add https://github.com/anthropics/skills/tree/main/skills/docx --yes
npx -y skills add https://github.com/anthropics/skills/tree/main/skills/xlsx --yes
npx -y skills add https://github.com/anthropics/skills/tree/main/skills/pptx --yes
```
- If the active agent requires explicit targets, add the same `--agent ... --global` options the user used for the main skill install.
- Explain that helper skill installation is separate from MCP setup. The YouTube Data MCP is already usable even before these helpers are installed, but most users will benefit from adding them.
- For Python-backed spreadsheet workflows, assume Python may be missing and verify the interpreter first:
```bash
python3 --version
```
- If `python3` is unavailable, also check:
```bash
python --version
```
- If neither `python3` nor `python` is available, ask the agent to search for the latest official Python installation method for the user's current OS before giving instructions.
- If Python is available but the spreadsheet stack is missing, ask the agent to search for the latest recommended install method for `pandas` and `openpyxl` on the user's current platform before giving instructions.

## Step 6: User Briefing Template
- Tell user:
  - Besides subtitle fetching, most tools support batch inputs.
  - User can paste multiple links directly in chat.
  - User can also provide Excel, CSV, and DOCX for link extraction after the strongly recommended helper setup.
  - Results can be written back to local DOCX or Excel after the strongly recommended helper setup.

## Notes
- Keep subtitle mode as single-video per request unless project rules change.
- If a client config path is uncertain, scan candidate config files and pick the one that already contains MCP settings first.
- After changing client config, remind user to restart the client if required.
- Do not assume Codex-specific directories exist. Use agent-neutral commands unless the user explicitly states a client-specific path.
