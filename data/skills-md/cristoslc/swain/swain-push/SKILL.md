---
name: swain-push
description: Stage all changes, generate a descriptive commit message from the diff, commit, and push to the current branch's upstream.
user-invocable: true
allowed-tools: Bash, Read, Edit
metadata:
  short-description: Stage, commit, and push
  version: 1.0.0
  author: cristos
  license: MIT
---

Run through the following steps in order without pausing for confirmation unless a decision point is explicitly marked as requiring one.

Delegate this to a sub-agent so the main conversation thread stays clean. Include the full text of these instructions in the agent prompt, since sub-agents cannot read skill files directly.

## Step 1 — Survey the working tree

```bash
git --no-pager status
git --no-pager diff          # unstaged changes
git --no-pager diff --cached # already-staged changes
```

If the working tree is completely clean and there is nothing to push, report that and stop.

## Step 2 — Stage changes

Identify files that look like secrets (`.env`, `*.pem`, `*_rsa`, `credentials.*`, `secrets.*`). If any are present, warn the user and exclude them from staging.

**If there are 10 or fewer changed files** (excluding secrets), stage them individually:

```bash
git add file1 file2 ...
```

**If there are more than 10 changed files**, stage everything and then unstage secrets:

```bash
git add -A
git reset HEAD -- <secret-file-1> <secret-file-2> ...
```

## Step 3 — Generate a commit message

Read the staged diff (`git --no-pager diff --cached`) and write a commit message that:

- Opens with a **conventional-commit prefix** matching the dominant change type:
  - `feat` — new feature or capability
  - `fix` — bug fix
  - `docs` — documentation only
  - `chore` — tooling, deps, config with no behavior change
  - `refactor` — restructuring without behavior change
  - `test` — test additions or fixes
- Includes a concise imperative-mood subject line (≤ 72 chars).
- Adds a short body (2–5 lines) summarising *why*, not just *what*, when the diff is non-trivial.
- Appends a `Co-Authored-By` trailer identifying the model that generated the commit. Use the model name from your system prompt (e.g., `Claude Opus 4.6`, `Gemini 2.5 Pro`). If you can't determine the model name, use `AI Assistant` as a fallback.

Example shape:
```
feat(terraform): add Cloudflare DNS module for hub provisioning

Operators can now point DNS at Cloudflare without migrating their zone.
Module is activated by dns_provider=cloudflare and requires only
CLOUDFLARE_API_TOKEN — no other provider credentials are validated.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

## Step 4 — Commit

```bash
git --no-pager commit -m "$(cat <<'EOF'
<generated message here>
EOF
)"
```

Use a heredoc so multi-line messages survive the shell without escaping issues.

## Step 5 — Push (with rebase pull first)

First, check whether the current branch has an upstream tracking branch:

```bash
git --no-pager rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null
```

If there is no upstream, the push command later should use `git push -u origin HEAD` to set one.

Then pull and push:

```bash
git --no-pager pull --rebase
git push          # or: git push -u origin HEAD (if no upstream)
```

If `git pull --rebase` succeeds cleanly, continue to push.

If it surfaces conflicts, abort the rebase (`git rebase --abort`), show the user the conflicting files, and ask how they'd like to proceed.

## Step 6 — Verify

Run `git --no-pager status` and `git --no-pager log --oneline -3` to verify the push landed and show the user the final state. Do not prompt for confirmation — just report the result.
