---
name: commit
description: Use when the user asks to commit changes, create a commit, or save work to git
---

Create a new commit for all of our uncommitted changes

## Step 0: Determine Reasoning
Before committing, identify WHY these changes were needed. The commit body MUST include a short reason.

- If the user explicitly stated a reason (e.g., "commit my changes, I fixed the login bug"), use that.
- If this skill was invoked by another skill/command and the reason is clear from context, use that.
- If the reason is NOT clear from the conversation context, use AskUserQuestion to ask: "Why were these changes needed? (This will be included in the commit message)"

## Step 1: Review Current State
Run: `git status && git diff HEAD && git status --porcelain`
This shows all uncommitted changes (modified, untracked, and staged files)

## Step 1.5: Secret / Credential Scan
Before staging anything, scan the diff output from Step 1 for explicit secrets or credentials.

**Two complementary checks — BOTH must pass:**

### Check A: Value-pattern scan
Look for values that look like secrets regardless of what field they are in:
- API keys with known prefixes (e.g., `sk-...`, `AIza...`, `AKIA...`, `ghp_...`, `xoxb-...`)
- Private keys or certificates (e.g., `-----BEGIN RSA PRIVATE KEY-----`)
- Hard-coded connection strings with credentials (e.g., `postgresql://user:pass@host`)
- Any high-entropy string (20+ random chars) assigned to a variable named key, secret, token, password, credential, or similar

### Check B: Field-name scan (catches low-entropy keys like `org-agentic-kb`)
Scan for any non-placeholder value assigned to an authentication-related field name, regardless of the value's format or length. Flag any of these patterns:

```
"X-API-Key": "<anything that is not a placeholder>"
"Authorization": "..."
api_key: ...
apiKey: ...
token: ...
password: ...
secret: ...
credential: ...
```

In JSON, YAML, .env, config files, or any headers block (e.g., MCP `mcp.json`, CI configs).

**A value is safe (not flagged) only if it is clearly a placeholder:**
- Wrapped in angle brackets: `<your-key-here>`
- Prefixed with `PLACEHOLDER_`, `YOUR_`, `MY_`, `EXAMPLE_`
- An empty string: `""`
- A well-known dummy: `"changeme"`, `"test-key"` (flag these too — they suggest a real value is expected)

**If any suspected secret is found:**
1. DO NOT stage or commit anything.
2. Alert the user with the exact file path, line number, and the suspicious value (mask the middle characters, e.g., `org-ag...kb`).
3. Ask the user to confirm whether it is a real secret and how to proceed before continuing.
4. STOP — do not proceed to Step 2 until the user responds.

**Only continue to Step 2 if no secrets were found, or the user has confirmed the flagged values are safe.**

## Step 2: Stage ALL Changes
CRITICAL: You MUST run `git add .` to stage ALL files including:
- Modified files
- Untracked files
- Untracked directories

DO NOT selectively stage files with `git add <specific-file>` unless explicitly instructed.
The default behavior is to commit everything.

Run: `git add .`

## Step 3: Create Commit
Add an atomic commit message with conventional commit format:
- Type: "feat", "fix", "docs", "chore", "refactor", "test", etc.
- Scope (optional): component or area affected
- Description: brief summary (50 chars or less, imperative mood)
- Body (REQUIRED): must include a short reason explaining WHY these changes were needed
- Footer: Include "Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

Run: `git commit -m "$(cat <<'EOF'
type(scope): description

Why: <short reason these changes were needed>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"`
