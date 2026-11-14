---
name: git-diff-explain
description: Use when user asks what changed, requests a diff summary, or says "explain my changes". Scans uncommitted changes (staged and unstaged) and produces a one-sentence summary of what was modified.
allowed-tools: [Bash]
---

Execute the following steps:
1. Check if current directory is a valid git repository
2. Get all uncommitted changes (staged and unstaged) in one command
3. Analyze the changes and provide exactly one sentence summarizing what changed
4. Only output more than one sentence for critical errors (not a git repo, etc.)

Rules:
- Output exactly one sentence unless there's a critical error
- Be concise but descriptive about the nature of changes
- Include number of files affected if relevant
- Mention the type of changes (additions, modifications, deletions)
