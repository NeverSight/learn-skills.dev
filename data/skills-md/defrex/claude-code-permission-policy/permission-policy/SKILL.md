---
name: permission-policy
description: Install or update the AI permission policy for auto-approving safe tool invocations.
allowed-tools: Bash(ls *), Bash(mkdir *), Bash(which *), Bash(chmod *), Read, Write, Edit, Glob
---

Set up the Claude Code permission hook that uses Haiku to auto-approve safe tool invocations based on a per-repo permission policy.

**Authentication**: The hook automatically reuses your Claude Code login (OAuth).

## Steps

### Step 1 — Check runtime availability

1. Run `which bun` to check if the Bun runtime is available.
2. If `bun` is found, continue to Step 2. The hook command will be: `bun .claude/skills/permission-policy/permission-policy.ts`
3. If `bun` is NOT found:
   a. Tell the user: "The permission-policy hook is written in TypeScript for the Bun runtime, but `bun` was not found on your system."
   b. Ask the user which option they'd prefer:
      - **Install Bun** — They can install it from https://bun.sh and re-run `/permission-policy`
      - **Port to Node.js** — You'll rewrite the hook as a standalone `.mjs` script (no dependencies)
      - **Port to Python** — You'll rewrite the hook as a standalone `.py` script (no dependencies)
      - **Port to another language** — They can specify their preferred language/runtime
   c. If the user chooses to port:
      - Read the original TypeScript source from `.claude/skills/permission-policy/permission-policy.ts`
      - Rewrite it in the chosen language, preserving all behavior: stdin JSON parsing, permission policy loading, `claude -p` subprocess call, JSON output, logging, and fail-open error handling
      - Write the ported script to `.claude/hooks/permission-policy.{ext}` in the current project root (e.g. `.mjs`, `.py`, etc.)
      - Make the file executable (`chmod +x`)
      - Use this as the hook command for Step 4 instead of the default bun command (e.g. `node .claude/hooks/permission-policy.mjs` or `python3 .claude/hooks/permission-policy.py`)
      - Add `.claude/hooks/` to `.gitignore` (in Step 3)
   d. If the user chooses to install Bun, stop here and tell them to re-run `/permission-policy` after installing.

### Step 2 — Create repo permission policy

1. Check if `.claude/PERMISSION_POLICY.md` exists in the current project root.
2. If it already exists, tell the user: "Permission policy already exists at `.claude/PERMISSION_POLICY.md` — skipping. Edit it to customize."
3. If it doesn't exist, copy the contents of `.claude/skills/permission-policy/PERMISSION_POLICY_TEMPLATE.md` to `.claude/PERMISSION_POLICY.md` in the current project root.
4. Tell the user to customize the policy for their project.

### Step 3 — Gitignore log file (and hooks if ported)

1. Check if `.claude/logs/` is already covered by a `.gitignore` entry in the current project root (e.g. `.claude/logs/` or `.claude/logs`).
2. If not, append `.claude/logs/` on a new line to the project root `.gitignore` (create the file if it doesn't exist).
3. If the hook was ported in Step 1, also ensure `.claude/hooks/` is in `.gitignore`.
4. Tell the user what was added to `.gitignore`.

### Step 4 — Configure hook in settings

1. Read `.claude/settings.json` in the current project root (or treat as `{}` if it doesn't exist).
2. Determine the hook command:
   - If bun is available (default): `bun .claude/skills/permission-policy/permission-policy.ts`
   - If ported in Step 1, use the appropriate command (e.g. `node .claude/hooks/permission-policy.mjs` or `python3 .claude/hooks/permission-policy.py`)
3. Merge the following hook configuration, preserving all existing settings:

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "Bash|Read|Write|Edit|Glob|Grep|WebFetch|WebSearch",
        "hooks": [
          {
            "type": "command",
            "command": "<hook command from above>",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

4. If there's already a `PermissionRequest` hook entry whose matcher includes `"Bash"`, replace it. Otherwise, add a new entry.
5. Write the updated settings back.

### Step 5 — Summary

1. Tell the user about `.claude/PERMISSION_POLICY.md` — explain that this is where they control what gets auto-approved, denied outright, or deferred to the human. Read the policy file and provide a brief summary of what it currently allows, denies, and asks about.
2. Tell the user about the log file at `.claude/logs/permission-policy.log`. Encourage them to run `tail -f .claude/logs/permission-policy.log` in a separate terminal if they want to follow the decisions being made in real time.
