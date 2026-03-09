---
name: confluence-page-viewer
description: Read Confluence page content using the confluence CLI. Use when given a Confluence page URL to fetch and display page information.
agent: Explore
argument-hint: Confluence page URL [OUT_DIR] (e.g. https://envato.atlassian.net/wiki/spaces/MS/pages/... ./out)
allowed-tools: Read, Bash, Write, Edit
context: fork
---

# Confluence Page Viewer

Fetch and display Confluence page content using `npx confluence-cli`.

## Arguments
- `$ARGUMENTS[0]` — Confluence page URL
- `$ARGUMENTS[1]` — (optional) Output directory for persisting the page content. Defaults to `.implement-assets/confluence`

When invoked by the orchestrator (e.g. `implement`), `$ARGUMENTS[1]` is provided. When used standalone, it defaults to `.implement-assets/confluence`.

## System Requirements
- Node.js and npm/npx available
- `confluence-cli` package (https://github.com/pchuri/confluence-cli) — invoked via `npx confluence-cli` to avoid asdf Node.js version conflicts

## Execution

1. **Pre-flight check**: Run `npx confluence-cli --help` to verify the CLI works — if it fails, follow error handling in [references/rules.md](references/rules.md). Do NOT continue until the CLI is available. Auth errors are caught when the actual command runs.
2. Validate `$ARGUMENTS[0]` against [references/rules.md](references/rules.md)
3. Run `npx confluence-cli read $ARGUMENTS[0]` via Bash
4. Format the output per [references/output-format.md](references/output-format.md)
5. **Save output**: Run `mkdir -p $ARGUMENTS[1]` via Bash, then save the full formatted output to `$ARGUMENTS[1]/output.md` using the Write tool. This ensures the complete output is persisted for the orchestrator to read.

<tags>
   <mode>think</mode>
   <custom>yes</custom>
</tags>
