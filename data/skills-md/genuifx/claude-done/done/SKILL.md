---
name: done
description: "Save a session summary to ~/.claude-done/ when wrapping up. Use when the user says /done, 'wrap up', 'save session notes', 'summarize this session', or wants to record what was accomplished."
---

# Done

Save a structured summary of the current session to `~/.claude-done/` for future reference.

## Workflow

### Step 1: Gather Metadata

Run these commands to collect metadata:

```bash
date +%Y-%m-%d
```

```bash
git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "no-branch"
```

The session ID is available from the current conversation context — use the full session ID.
The current working directory is the project path — use it for the Project field.

### Step 2: Review the Conversation

Write the summary in the user's preferred language (match the language used in the system prompt or the language the user has been communicating in during this session).

Meticulously review the entire conversation, tracing the full arc of discussion, and identify:

- The main goal and what was accomplished
- Key decisions made and their reasoning
- Alternatives explored and why they were rejected
- Problems encountered during the session and how they were resolved
- Important questions raised (both resolved and unresolved)
- Files that were changed and why
- Logical next steps and follow-ups

### Step 3: Generate Title

Create a 3-5 word kebab-case title summarizing the session (e.g., `fix-token-refresh-logic`, `add-user-auth-flow`).

### Step 4: Write the Summary File

Create the output directory and write the file:

```bash
mkdir -p ~/.claude-done
```

**Filename format:** `{YYYY-MM-DD}_{branch}_{sessionId-full}_{kebab-case-title}.md`

- Replace `/` in branch names with `-`
- Example: `2026-02-18_feat-auth_a1b2c3d4_fix-token-refresh.md`

**File content template:**

```markdown
# {Natural Language Title}

**Date:** YYYY-MM-DD
**Branch:** branch-name
**Project:** /path/to/project
**Session:** full-session-id

## Summary
2-4 sentences describing the goal and outcome of this session.

## Key Decisions
- Decision and brief reasoning
- Alternatives considered and why they were rejected

## What Changed
- `file/path` — what changed and why

## Problems & Solutions
- Problem encountered — how it was resolved

## Questions Raised
- Important questions discussed, with answers if resolved
- Unresolved questions flagged for future sessions

## Next Steps
- [ ] Follow-up task
```

Omit any section that has no content. Do not include empty sections.

### Step 5: Sync to Notion (best-effort)

After saving the local file, attempt to sync the summary to Notion as a child page using the Python script bundled with this skill.

#### 5a: Read config

Check if `~/.claude-done/config.json` exists:

```bash
cat ~/.claude-done/config.json 2>/dev/null
```

- If config has both `notion_token` and `notion_page_id` → go to **5c**
- If config has `"notion_sync": false` → skip sync entirely, proceed to Step 6 silently
- If config doesn't exist or is missing token/page_id → go to **5b**

#### 5b: First-time setup

Ask the user:

"Notion sync is not configured yet. Would you like to sync session summaries to Notion?

1. **Yes** — I'll guide you through setup
2. **Skip** — don't sync to Notion"

**Option 1 (Setup):**

Guide the user through these steps:

1. Go to https://www.notion.so/profile/integrations and create an Internal Integration. Copy the token (starts with `ntn_` or `secret_`).
2. In Notion, open the page where you want summaries saved. Click "..." → "Connect to" → select the integration you just created.
3. Copy the page URL (e.g., `https://www.notion.so/My-Page-abc123def456...`).

Ask the user to provide:
- The integration token
- The Notion page URL or page ID

Extract the page_id from the URL: it's the 32-character hex string at the end (after the last `-`, ignoring any `?` query params). Format it with hyphens as `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.

Write the config:

```bash
cat > ~/.claude-done/config.json << 'EOF'
{
  "notion_token": "<token>",
  "notion_page_id": "<page-id>"
}
EOF
```

**Option 2 (Skip):**

Write config so future `/done` runs won't ask again:

```bash
cat > ~/.claude-done/config.json << 'EOF'
{
  "notion_sync": false
}
EOF
```

Proceed to Step 6.

#### 5c: Run sync script

Determine the path to the sync script relative to this SKILL.md file. The script is at `skills/done/scripts/sync_notion.py` in the plugin directory.

```bash
python3 <plugin-dir>/skills/done/scripts/sync_notion.py --title "{YYYY-MM-DD} {Natural Language Title}" --file <path-to-saved-summary.md>
```

- On success, the script prints the Notion page URL — capture it for Step 6.
- On failure, note the error but do NOT let it block the workflow. The local file is already saved.

### Step 6: Confirm

After writing the file, tell the user:
- The filename and a one-line summary of what was saved
- Notion sync status: **synced** (with link) / **skipped** / **failed** (with brief reason)
