---
name: gemini-review
description: "Local code review with Gemini CLI for pre-commit reviews. Use when user says review code, code review, check my changes, or review before commit."
allowed-tools: [mcp__acp__Read, mcp__acp__Bash]
compatibility: "Requires Gemini CLI installed and GEMINI_API_KEY in environment."
---

# ABOUTME: Local code review skill using Gemini CLI for pre-commit reviews
# ABOUTME: Supports staged, uncommitted, or branch diff with configurable prompts

# Gemini Review - Local Code Review

**MANDATORY: Always use `--model gemini-3.1-pro-preview`. No other model. No fallback. No substitution.**

## Trigger
Activate when user says: "gemini review", "review with gemini", "local review", or `/gemini-review`.

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--all` | Review all uncommitted changes | staged only |
| `--branch [base]` | Review current branch vs base | main |
| `--prompt <name>` | Use specific prompt template | default |
| `--extension` | Use Gemini's built-in `/code-review` | custom prompt |

## Execution Flow

### Step 1: Determine diff scope

```bash
# Default: staged changes
git diff --cached

# With --all: all uncommitted
git diff HEAD

# With --branch [base]: branch vs base (default base: main)
git diff main...HEAD
```

### Step 2: Check if there are changes to review

```bash
# Check if diff is empty
git diff --cached --quiet && echo "No staged changes" || echo "Has changes"
```

If no changes, inform user and suggest:
- `git add <files>` to stage changes
- `--all` flag for uncommitted changes
- `--branch` flag for branch review

### Step 3: Load prompt template

Prompt templates are in `~/.claude/skills/gemini-review/prompts/`:
- `default.md` - Concise review focused on bugs/security/performance
- `ci-style.md` - Detailed review matching CI pipeline style

### Step 4: Execute review

**Option A - Using built-in extension (with `--extension` flag):**
```bash
cd <project_root>
gemini --model gemini-3.1-pro-preview --yolo "/code-review"
```

**Option B - Using custom prompt (default):**
```bash
cd <project_root>

# Generate diff
DIFF=$(git diff --cached)

# Read prompt template
PROMPT=$(cat ~/.claude/skills/gemini-review/prompts/default.md)

# Invoke Gemini with prompt and diff
gemini --model gemini-3.1-pro-preview --yolo <<EOF
$PROMPT

## Code Changes to Review

\`\`\`diff
$DIFF
\`\`\`
EOF
```

### Step 5: Present results

Gemini's output will appear in the terminal. Summarize key findings for the user.

## Quality Notes

- Review the full diff carefully before sending to Gemini
- Summarize findings thoughtfully; do not just relay raw output
- Flag false positives rather than forwarding everything

## Important Notes

1. **Always run from project root** - Gemini needs project context
2. **Check for CLAUDE.md/GEMINI.md** - Include project guidelines in prompt if present
3. **Large diffs** - For very large diffs (>10000 lines), suggest `--branch` with specific files
4. **Exit codes** - Gemini CLI returns 0 on success, non-zero on error

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No staged changes" | Run `git add <files>` or use `--all` |
| "gemini: command not found" | Install Gemini CLI: see https://github.com/google-gemini/gemini-cli |
| API errors | Check `GEMINI_API_KEY` is set |
| Timeout on large diffs | Split into smaller reviews or use `--extension` |
