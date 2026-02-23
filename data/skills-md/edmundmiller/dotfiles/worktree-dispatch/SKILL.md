---
name: worktree-dispatch
description: Delegate tasks to parallel worktree agents using worktrunk (wt). Use when asked to "spawn agents", "run in parallel", "delegate to worktrees", or split work across multiple Claude/OpenCode sessions.
---

Launch one or more tasks in new git worktrees using worktrunk (`wt`).

Tasks: $ARGUMENTS

## You are a dispatcher, not an implementer

**FORBIDDEN:** Do NOT read source files, edit code, or fix issues yourself. You
only write prompt files and run `wt switch` commands.

If tasks reference earlier conversation (e.g., "do option 2"), include all
relevant context in each prompt you write.

If tasks reference a markdown file (e.g., a plan or spec), re-read the file to
ensure you have the latest version before writing prompts.

For each task:

1. Generate a short, descriptive branch name (2-4 words, kebab-case)
2. Write a detailed implementation prompt to a temp file
3. Run `wt switch -c <branch-name> -x pi -- "$(cat <temp-file>)"` to create worktree + launch agent (pi is default)

The prompt should:

- Include the full task description
- Use RELATIVE paths only (never absolute paths, since each worktree has its own root)
- Be specific about what the agent should accomplish

## Skill delegation

If the user passes a skill reference (e.g., `/some-skill`), the prompt should
instruct the agent to use that skill instead of writing out manual
implementation steps.

**Skills can have flags.** If the user passes `/some-skill --flag`, pass the
flag through to the skill invocation in the prompt.

Example prompt:

```
[Task description here]

Use the skill: /skill-name [flags if any] [task description]
```

Do NOT write detailed implementation steps when a skill is specified - the skill
handles that.

## Flags

**`--merge`**: When passed, add instruction to merge when done:

```
...
When complete, run: wt merge
```

**`--claude`**: Use Claude instead of pi:

```bash
wt switch -c <branch> -x claude -- "prompt here"
```

**`--opencode`**: Use OpenCode instead of pi:

```bash
wt switch -c <branch> -x opencode -- "prompt here"
```

**`--bg`**: Run in background tmux session (for handoffs):

```bash
tmux new-session -d -s <branch> "wt switch -c <branch> -x claude -- 'prompt'"
```

## Workflow

Write ALL temp files first, THEN run all wt commands.

Step 1 - Write all prompt files (in parallel):

```bash
tmpfile=$(mktemp).md
cat > "$tmpfile" << 'EOF'
Implement feature X...
EOF
echo "$tmpfile"  # Note the path for step 2
```

Step 2 - After ALL files are written, run wt commands (in parallel):

```bash
wt switch -c feature-x -x pi -- "$(cat /tmp/tmp.abc123.md)"
wt switch -c feature-y -x pi -- "$(cat /tmp/tmp.def456.md)"
```

After creating the worktrees, inform the user which branches were created.

**Remember:** Your task is COMPLETE once worktrees are created. Do NOT implement
anything yourself.

## Quick Reference

```bash
# Create worktree + launch pi (default)
wt switch -c feature/auth -x pi -- "Implement OAuth flow"

# Create worktree + launch Claude
wt switch -c feature/auth -x claude -- "Implement OAuth flow"

# Create worktree + launch OpenCode
wt switch -c fix/bug-123 -x opencode -- "Fix the null pointer in auth.rs"

# Background session (handoff)
tmux new-session -d -s auth "wt switch -c feature/auth -x pi -- 'prompt'"

# Check status of all worktrees
wt list --full

# Merge completed work
wt merge
```
