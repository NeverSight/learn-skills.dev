---
name: gdrive-access
description: Access Google Drive via CLI with 1Password OAuth. Use when user wants to list files, download from Drive, sync folders, or mentions google drive access. TRIGGERS - google drive, gdrive, drive folder, download drive, sync drive, list drive files.
allowed-tools: Read, Bash, Grep, Glob, Write, AskUserQuestion
---

# Google Drive Access

List, download, and sync files from Google Drive programmatically via Claude Code CLI.

## MANDATORY PREFLIGHT (Execute Before Any Drive Operation)

**CRITICAL**: You MUST complete this preflight checklist before running any gdrive commands. Do NOT skip steps.

### Step 1: Check CLI Binary Exists

```bash
ls -la "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/gdrive-tools/skills/gdrive-access/scripts/gdrive" 2>/dev/null || echo "BINARY_NOT_FOUND"
```

**If BINARY_NOT_FOUND**: Build it first:

```bash
cd ~/.claude/plugins/marketplaces/cc-skills/plugins/gdrive-tools/skills/gdrive-access/scripts && bun install && bun run build
```

### Step 2: Check GDRIVE_OP_UUID Environment Variable

```bash
echo "GDRIVE_OP_UUID: ${GDRIVE_OP_UUID:-NOT_SET}"
```

**If NOT_SET**: You MUST run the Setup Flow below. Do NOT proceed to gdrive commands.

### Step 3: Verify 1Password Authentication

```bash
op account list 2>&1 | head -3
```

**If error or not signed in**: Inform user to run `op signin` first.

---

## Setup Flow (When GDRIVE_OP_UUID is NOT_SET)

Follow these steps IN ORDER. Use AskUserQuestion at decision points.

### Setup Step 1: Check 1Password CLI

```bash
command -v op && echo "OP_CLI_INSTALLED" || echo "OP_CLI_MISSING"
```

**If OP_CLI_MISSING**: Stop and inform user:

> 1Password CLI is required. Install with: `brew install 1password-cli`

### Setup Step 2: Discover Drive OAuth Items in 1Password

```bash
op item list --vault Employee --format json 2>/dev/null | jq -r '.[] | select(.title | test("drive|oauth|google"; "i")) | "\(.id)\t\(.title)"'
```

**Parse the output** and proceed based on results:

### Setup Step 3: User Selects OAuth Credentials

**If items found**, use AskUserQuestion with discovered items:

```
AskUserQuestion({
  questions: [{
    question: "Which 1Password item contains your Google Drive OAuth credentials?",
    header: "Drive OAuth",
    options: [
      // POPULATE FROM op item list RESULTS - example:
      { label: "Google Drive API (56peh...)", description: "OAuth client in Employee vault" },
      { label: "Gmail API - dental-quizzes (abc12...)", description: "Can also access Drive" },
    ],
    multiSelect: false
  }]
})
```

**If NO items found**, use AskUserQuestion to guide setup:

```
AskUserQuestion({
  questions: [{
    question: "No Google Drive OAuth credentials found in 1Password. How would you like to proceed?",
    header: "Setup",
    options: [
      { label: "Create new OAuth credentials (Recommended)", description: "I'll guide you through Google Cloud Console setup" },
      { label: "I have credentials elsewhere", description: "Help me add them to 1Password" },
      { label: "Skip for now", description: "I'll set this up later" }
    ],
    multiSelect: false
  }]
})
```

- If "Create new OAuth credentials": Read and present [references/gdrive-api-setup.md](./references/gdrive-api-setup.md)
- If "I have credentials elsewhere": Guide user to add to 1Password with required fields
- If "Skip for now": Inform user the skill won't work until configured

### Setup Step 4: Confirm mise Configuration

After user selects an item (with UUID), use AskUserQuestion:

```
AskUserQuestion({
  questions: [{
    question: "Add GDRIVE_OP_UUID to .mise.local.toml in current project?",
    header: "Configure",
    options: [
      { label: "Yes, add to .mise.local.toml (Recommended)", description: "Creates/updates gitignored config file" },
      { label: "Show me the config only", description: "I'll add it manually" }
    ],
    multiSelect: false
  }]
})
```

**If "Yes, add to .mise.local.toml"**:

1. Check if `.mise.local.toml` exists
2. If exists, append `GDRIVE_OP_UUID` to `[env]` section
3. If not exists, create with:

```toml
[env]
GDRIVE_OP_UUID = "<selected-uuid>"
```

1. Verify `.mise.local.toml` is in `.gitignore`

**If "Show me the config only"**: Output the TOML for user to add manually.

### Setup Step 5: Reload and Verify

```bash
mise trust 2>/dev/null || true
cd . && echo "GDRIVE_OP_UUID after reload: ${GDRIVE_OP_UUID:-NOT_SET}"
```

**If still NOT_SET**: Inform user to restart their shell or run `source ~/.zshrc`.

### Setup Step 6: Test Connection

```bash
GDRIVE_OP_UUID="${GDRIVE_OP_UUID}" $HOME/.claude/plugins/marketplaces/cc-skills/plugins/gdrive-tools/skills/gdrive-access/scripts/gdrive list 1wqqqvBmeUFYuwOOEQhzoChC7KzAk-mAS
```

**If OAuth prompt appears**: This is expected on first run. Browser will open for Google consent.

---

## Drive Commands (Only After Preflight Passes)

```bash
GDRIVE_CLI="$HOME/.claude/plugins/marketplaces/cc-skills/plugins/gdrive-tools/skills/gdrive-access/scripts/gdrive"

# List files in a folder
$GDRIVE_CLI list <folder_id>

# List with details (size, modified date)
$GDRIVE_CLI list <folder_id> --verbose

# Search for files
$GDRIVE_CLI search "name contains 'training'"

# Get file info
$GDRIVE_CLI info <file_id>

# Download a single file
$GDRIVE_CLI download <file_id> -o ./output.pdf

# Sync entire folder to local directory
$GDRIVE_CLI sync <folder_id> -o ./output_dir

# Sync with subfolders
$GDRIVE_CLI sync <folder_id> -o ./output_dir -r

# JSON output (for parsing)
$GDRIVE_CLI list <folder_id> --json
```

## Extracting Folder ID from URL

Google Drive folder URL:

```
https://drive.google.com/drive/folders/1wqqqvBmeUFYuwOOEQhzoChC7KzAk-mAS
                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                       This is the folder ID
```

## Drive Search Syntax

| Query                          | Description           |
| ------------------------------ | --------------------- |
| `name contains 'keyword'`      | Name contains keyword |
| `name = 'exact name'`          | Exact name match      |
| `mimeType = 'application/pdf'` | By file type          |
| `modifiedTime > '2026-01-01'`  | Modified after date   |
| `trashed = false`              | Not in trash          |
| `'<folderId>' in parents`      | In specific folder    |

Reference: <https://developers.google.com/drive/api/guides/search-files>

## Environment Variables

| Variable          | Required | Description                               |
| ----------------- | -------- | ----------------------------------------- |
| `GDRIVE_OP_UUID`  | Yes      | 1Password item UUID for OAuth credentials |
| `GDRIVE_OP_VAULT` | No       | 1Password vault (default: Employee)       |

## Token Storage

OAuth tokens stored at: `~/.claude/tools/gdrive-tokens/<uuid>.json`

- Central location (not in plugin, not in project)
- Organized by 1Password UUID (supports multi-account)
- Created with chmod 600

## Google Docs Export

Google Docs (Docs, Sheets, Slides) are automatically exported:

| Google Type  | Export Format |
| ------------ | ------------- |
| Document     | .docx         |
| Spreadsheet  | .xlsx         |
| Presentation | .pptx         |
| Drawing      | .png          |

## References

- [gdrive-api-setup.md](./references/gdrive-api-setup.md) - Google Cloud OAuth setup guide

## Post-Change Checklist

- [ ] YAML frontmatter valid (no colons in description)
- [ ] Trigger keywords current
- [ ] Path patterns use $HOME not hardcoded paths
- [ ] References exist and are linked
