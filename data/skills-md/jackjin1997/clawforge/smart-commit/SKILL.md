---
name: smart-commit
description: "AI-powered git commit message generation. Uses LLM to summarize changes and create meaningful commit messages. Triggers when user wants to commit changes, amend/squash commits, or needs LLM to summarize changes for commit messages. Chinese triggers: 提交, 提交代码, 提交更改, 提交修改, 要提交, commit, 提交信息, git 提交, 生成提交信息."
user-invocable: true
---

# Smart Commit

AI-powered git commit message generation using LLM. Creates meaningful commit messages from code changes.

## Capabilities

1. **Amend Last Commit** - Summarize staged/unstaged changes and amend the last commit message
2. **Squash Commits** - Summarize last N commits and create a consolidated commit
3. **Interactive Commit** - Confirm files with user, then summarize and create new commit

## Quick Start

### For New Commit
```bash
# Show changed files and ask user confirmation
git status

# After confirmation, summarize changes with LLM
# Create commit with generated message
```

### For Amending
```bash
# Get diff of changes to amend
git diff --cached  # staged
git diff HEAD~1    # compared to last commit

# LLM summarizes, then
git commit --amend -m "new message"
```

### For Squashing
```bash
# Get last N commit messages and diffs
git log -n N --format="%H %s"

# LLM summarizes, then
git reset --soft HEAD~N
git commit -m "consolidated message"
```

## Workflow Decision Tree

```
User wants git commit help?
├─ "amend" or "修改"? → Amend workflow
├─ "squash" or "合并" + number? → Squash workflow
└─ New commit? → Interactive workflow
```

## Amend Workflow

1. Get changes: `git diff --cached` (staged) or `git diff HEAD~1` (all changes since last commit)
2. Send to LLM with prompt from `references/prompts.md` section "Amend Commit"
3. User reviews suggested message
4. `git commit --amend -m "message"`

## Squash Workflow

1. Get last N commits: `git log -n N --format="%H|%s|%an|%ad"`
2. Get combined diff: `git diff HEAD~N..HEAD`
3. Send to LLM with prompt from `references/prompts.md` section "Squash Commits"
4. User reviews suggested message
5. `git reset --soft HEAD~N && git commit -m "message"`

## Interactive Commit Workflow

1. Show `git status` to user
2. Ask user to confirm which files to include
3. Get diff for confirmed files
4. Send to LLM with prompt from `references/prompts.md` section "New Commit"
5. User reviews suggested message
6. `git add <files> && git commit -m "message"`

## LLM Prompts

See `references/prompts.md` for:
- New commit message generation
- Amend commit message generation
- Squash commit message generation

Each prompt includes:
- Git diff input format
- Output format requirements
- Style guidelines (conventional commits, etc.)
