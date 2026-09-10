---
name: antdv
description: >
  Use when the user's task involves antdv-next — writing antdv-next components,
  debugging antdv-next issues, querying antdv-next props/events/slot/tokens/demos, migrating between
  antdv-next versions, or analyzing antdv-next usage in a project. Triggers on antdv-next-related
  code, imports from 'antdv-next', or explicit antdv-next questions.
allowed-tools:
  - Bash(antdv *)
  - Bash(antdv bug*)
  - Bash(antdv bug-cli*)
  - Bash(npm install -g @antdv-next/cli*)
  - Bash(which antdv)
---

# Ant Design CLI

You can visit `@antdv-next/cli` - a local cli tool that contains metadata about the current, latest version of antdv-next. Use it to query component knowledge, analyze projects, and guide migrations. All data is offline and does not require a network.
## Setup

Before first use, check if the CLI is installed. If not, install it automatically:

```bash
which antdv || npm install -g @antdv-next/cli
```

After running any command, if the output contains an "Update available" notice, run `antdv upgrade` to update before continuing.


**Always use `--format json` for structured output you can parse programmatically.**

## Scenarios

### 1. Writing antd component code

Before writing any antd component code, look up its API first — don't rely on memory.

```bash
# Check what props are available
antdv info Button --format json

# Get a working demo as starting point
antdv demo Button basic --format json

# Check semantic classNames/styles for custom styling
antdv semantic Button --format json

# Check component-level design tokens for theming
antdv token Button --format json

# Get the overall design language (design.md): colors, typography, spacing, radius + principles
antdv design.md --format json
```

**Workflow:** `antdv info` → understand props/event/slot → `antdv demo` → grab a working example → write code.

### 2. Looking up full documentation

When you need comprehensive component docs (not just props):

```bash
antdv doc Table --format json        # full markdown docs for Table
antdv doc Table --lang zh            # Chinese docs
```

### 3. Debugging antd issues

When code isn't working as expected or the user reports an antdv bug:

```bash
# Collect full environment snapshot (system, deps, browsers, build tools)
antdv env --format json

# Check if the prop exists for the user's antd version
antdv info Select --version 5.12.0 --format json

# Check if the prop is deprecated
antdv lint ./src/components/MyForm.tsx --format json

# Diagnose project-level configuration issues
antdv doctor --format json
```

**Workflow:** `antdv env` → capture full environment → `antdv doctor` → check configuration → `antdv info --ver X` → verify API against the user's exact version → `antdv lint` → find deprecated or incorrect usage.

### 4. Analyzing project antd usage

When the user wants to understand how antd is used in their project:

```bash
# Scan component usage statistics
antdv usage ./src --format json

# Filter to a specific component
antdv usage ./src --filter Form --format json

# Lint for best practice violations
antdv lint ./src --format json

# Check only specific rule categories
antdv lint ./src --only deprecated --format json
antdv lint ./src --only a11y --format json
antdv lint ./src --only performance --format json
```

### 5. Comparing component APIs between versions

When the user asks what component APIs changed between versions:

```bash
# Compare props, events, slots, and methods for all components
antdv changelog 1.2.2 1.5.2 --format json

# Limit the comparison to one component
antdv changelog 1.2.2 1.5.2 Select --format json
```

### 6. Exploring available components

When the user is choosing which component to use:

```bash
# List all components with categories
antdv list --format json

# List components for a specific antd version
antdv list --version 5.0.0 --format json
```

### 7. Collecting environment info

When you need to understand the project's antdv-next setup, or prepare info for a bug report:

```bash
# Full environment snapshot (text — paste into GitHub Issues)
antdv env

# Structured JSON for programmatic use
anvtd env --format json

# Scan a specific project directory
antdv env ./my-project --format json
```

Collects: OS, Node, package managers (npm/pnpm/yarn/bun/utoo), npm registry, browsers, core deps (antdv-next/vue/dayjs), all `@antdv-next/*` packages, and build tools (vite/typescript/etc.).

### 8. Reporting antd bugs

When the user asks you to report an antdv bug:

```bash
# Step 0: Collect environment info for reference (optional — antd bug already embeds basic env)
# Use the output to cross-check versions or attach extra details to the bug report
antdv env --format json

# Step 1: Preview for user review
antdv bug --title "DatePicker crashes when selecting date" \
  --reproduction "https://codesandbox.io/s/xxx" \
  --steps "1. Open DatePicker 2. Click a date" \
  --expected "Date is selected" \
  --actual "Component crashes with error" \
  --format json

# Step 2: Show to user, ask for confirmation

# Step 3: Submit after user confirms
antdv bug --title "DatePicker crashes when selecting date" \
  --reproduction "https://codesandbox.io/s/xxx" \
  --steps "1. Open DatePicker 2. Click a date" \
  --expected "Date is selected" \
  --actual "Component crashes with error" \
  --submit
```

### 9. Reporting CLI issues

When the user asks you to report a CLI bug, or explicitly requests help filing one:

```bash
# Preview the bug report for the user
antdv bug-cli --title "antdv info Button returns wrong props for v1.5.1" \
  --description "When querying Button info for version 1.5.1, the output includes props that don't exist in that version" \
  --steps "1. Run: antdv info Button --ver 1.5.1 --format json" \
  --expected "Props matching antdv-next 1.5.0 Button API" \
  --actual "Props include 'classes' which was added in 1.5.1" \
  --format json
```

Show the report to the user and confirm before submitting:

```bash
antdv bug-cli --title "antdv info Button returns wrong props for v1.5.1" \
  --description "..." \
  --steps "..." \
  --expected "..." \
  --actual "..." \
  --submit
```

**Opt-out:** If the environment variable `ANTDV_NO_AUTO_REPORT=1` is set, skip all bug-reporting suggestions entirely — do not suggest `antdv bug` or `antdv bug-cli` unless the user directly asks.

### 10. Upgrading the CLI

When the user wants to update `@antdv-next/cli` to the latest version, or when an "Update available" notice appears:

```bash
# Upgrade to the latest version (auto-detects package manager)
antdv upgrade
```

The command detects which package manager installed the CLI (npm, yarn, pnpm, bun) and runs the appropriate upgrade command. If detection fails, it suggests the manual command.

### 11. Using as MCP server

If working in an IDE that supports MCP (Claude Desktop, Cursor, etc.), the CLI can also run as an MCP server, exposing all knowledge-query tools directly:

```json
{
  "mcpServers": {
    "antdv": {
      "command": "antdv",
      "args": ["mcp", "--version", "1.5.0"]
    }
  }
}
```

This provides 8 tools (`antdv_list`, `antdv_info`, `antdv_doc`, `antdv_demo`, `antdv_token`, `antdv_design_md`, `antdv_semantic`) and 2 prompts (`antdv-expert`, `antdv-page-generator`) via MCP protocol.

## Global Flags

| Flag                | Purpose                                                                    |
|---------------------|----------------------------------------------------------------------------|
| `--format <format>` | Output format: `json`, `text`, or `markdown` (agents should prefer `json`) |
| `--ver`             | Target a specific antd version (e.g. `1.5.0`)                              |
| `--detail`          | Include extra fields (description, since, deprecated, FAQ)                 |
| `-V, --version`     | Print CLI version and exit                                                 |

## Key Rules

1. **Always query before writing** — Don't guess antd APIs from memory. Run `antdv info` first.
2. **Match the user's version** — Knowledge queries (`list/info/doc/demo/token/semantic/changelog`) support antdv-next v1.x.
3. **Use `--format json`** — Every command supports it. Parse the JSON output rather than regex-matching text output.
4. **Check before suggesting migration** — Run `antdv changelog <v1> <v2>` and `antdv migrate` before advising on version upgrades.
5. **Lint after changes** — After writing or modifying antd code, run `antdv lint` on the changed files to catch deprecated or problematic usage.
6. **Report antdv-next bugs** — When the user asks to report an antd bug, use `antdv bug`. Always preview first, get user confirmation, then submit.
7. **Report CLI issues** — When the user asks about a CLI problem, use `antdv bug-cli` to help them file a report. Always preview first, get user confirmation, then submit.
