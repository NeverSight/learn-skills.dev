---
name: safe-push
description: "Pre-push hygiene check for GitHub repositories. Scans for PII, secrets, and sensitive data before pushing. Audits commit messages, enforces repo-specific blocklists, and rate-limits pushes to avoid GitHub abuse detection. Use before any git push, especially to public repos."
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.2.0
  category: devops
  domain: git
  updated: 2026-05-08
  tested: 2026-05-08
  tested_with: "Claude Code v2.1"
---

# Safe Push

Pre-push hygiene check for GitHub repositories. Use when the user asks to push code, especially to public repos.

## Trigger

When the user says "push", "safe push", "push to GitHub", or runs `/safe-push`.

## Install

The skill loads patterns from `~/.claude/safe-push-blocklist`. Copy the bundled template and customize:

```bash
cp safe-push-blocklist.template ~/.claude/safe-push-blocklist
$EDITOR ~/.claude/safe-push-blocklist
```

The template includes commented-out examples for client names, hostnames, IP ranges, tracking IDs, and Slack token shapes. Replace them with values specific to your environment.

If the file is missing, the skill runs with a warning instead of erroring — but personal pattern checks are skipped, so creating it is strongly recommended.

## Procedure

### 1. Classify the repo

```bash
# Check if public repo
git remote -v
# Check for .public-repo marker
test -f .public-repo && echo "PUBLIC" || echo "private or unmarked"
```

If public (or pushing to a public remote): apply ALL checks below.
If private: apply only the PII scan (step 2).

### 2. PII and secrets scan

Load your personal pattern list from `~/.claude/safe-push-blocklist` and scan against it. The same patterns apply to diff content (step 2) AND commit messages (step 3) — both run from the same source of truth.

**Default mode** — scan the diff against the target branch:

```bash
# Load personal patterns (graceful fallback if file missing):
if [ -f ~/.claude/safe-push-blocklist ]; then
  PATTERNS=$(grep -v '^#' ~/.claude/safe-push-blocklist | grep -v '^$' | paste -sd '|' -)
else
  PATTERNS=""
  echo "WARNING: ~/.claude/safe-push-blocklist not found. Personal pattern checks skipped."
fi

git diff origin/main...HEAD
[ -n "$PATTERNS" ] && git diff origin/main...HEAD | grep -nE "$PATTERNS" \
  || echo "NO MATCHES IN DIFF"
```

**Full repo mode** (`/safe-push --full`) — scan ALL tracked files, not just the diff. Use this for baseline audits, first-time pushes of existing repos, or periodic hygiene checks:

```bash
git ls-files | xargs grep -n -E "$PATTERNS" \
  --include='*.md' --include='*.py' --include='*.js' --include='*.ts' \
  --include='*.html' --include='*.sh' --include='*.json' \
  --include='*.yml' --include='*.yaml'
```

Check for these categories (your `~/.claude/safe-push-blocklist` covers the regex-able ones):

- Client names or internal project codenames
- Personal infrastructure: hostnames, internal directory names, device IDs, hardware models, self-hosted service names
- Email addresses (personal or client), phone numbers, addresses
- API keys, tokens, secrets (AWS, GitHub, Slack, Telegram, generic)
- Private IP addresses, internal hostnames
- Private key material
- Slack tokens (`xoxb-`), Slack channel IDs
- Tracking IDs: GA4 (`G-XXXXXXXXXX`), GTM (`GTM-XXXXXXX`)

Edit `~/.claude/safe-push-blocklist` to maintain your personal patterns. Never hardcode real client names or infrastructure identifiers inside this skill file — the blocklist is the source of truth.

If anything is found:
- List each finding with file, line number, and what was detected
- Ask the user to fix before proceeding
- Do NOT push until resolved

### 3. Commit message audit

Review the FULL commit message — both subject (title) and body (description) — for every commit in the push range. Sensitive patterns can hide in either:

```bash
# Print the full message (subject + body) for every commit:
git log origin/main..HEAD --format="===%h %s===%n%b"

# Programmatically scan the full message text against the same
# blocklist used for diff content (graceful fallback if file missing):
if [ -f ~/.claude/safe-push-blocklist ]; then
  PATTERNS=$(grep -v '^#' ~/.claude/safe-push-blocklist | grep -v '^$' | paste -sd '|' -)
  git log origin/main..HEAD --format="%B" | grep -nE "$PATTERNS" \
    || echo "NO MATCHES IN MESSAGES"
else
  echo "WARNING: ~/.claude/safe-push-blocklist not found. Personal pattern checks skipped on commit messages."
fi
```

The same patterns from `~/.claude/safe-push-blocklist` that block diff content (step 2) ALSO block commit messages. Apply the full blocklist to BOTH title and body — not just the diff. For public repos, also flag:

- Personal info (email, phone, address) — categorical, not always pattern-matched
- Private repo names you own (e.g., upstream dev mirrors) — soft-warn, ask user before pushing
- Vague messages ("fix", "update", "wip") — suggest rewrites

If issues found, suggest interactive rebase to clean messages (with user approval).

### 4. Staggered push (rate limiting)

To avoid triggering GitHub bulk action / automation abuse detection:

- If pushing a single branch with < 50 commits: push normally
- If pushing multiple branches or > 50 commits:
  - Push one branch at a time
  - Wait 5 seconds between branch pushes
  - For very large pushes (100+ commits), break into batches of 50 and wait 10 seconds between batches
- If creating a new repo and pushing initial content with multiple branches:
  - Push main/default branch first
  - Wait 10 seconds
  - Push remaining branches one at a time with 5-second gaps
- NEVER use `git push --all` or `git push --mirror` to a public remote without staggering

```bash
# Example staggered multi-branch push
for branch in main develop feature/foo; do
  git push origin "$branch"
  sleep 5
done
```

### 5. Final confirmation

Before executing the push, present a summary:
- Repository: name and public/private status
- Branch(es) being pushed
- Number of commits
- **Full commit message preview** for every commit in the push range (both title and body) — even on amended commits and commits authored in this session
- Any warnings from steps 2-4
- Push strategy (direct or staggered)

Show the full commit messages with:

```bash
git log origin/main..HEAD --format="commit %h%n%n%s%n%n%b%n---"
```

The user must visually confirm each message before push. This catches:
- Amended commits where the original audit no longer applies
- Body content that wasn't surfaced in step 3 because of grep gaps
- Anything authored ad-hoc in this session that didn't go through a content review

Wait for explicit user confirmation before pushing.

### 6. Push and verify

After pushing:
```bash
git push origin <branch>
# Verify
git log origin/<branch> --oneline -5
```

Report success and the remote URL.

## Configuration files

- **`~/.claude/safe-push-blocklist`** — Your personal pattern blocklist. One regex per line; comments start with `#`. Loaded on every `/safe-push` invocation. Edit this file to add or remove patterns; never hardcode patterns in this skill file. See **Install** above for setup.
- **Repo-local `.pii-allowlist`** — One regex per line, matches are excluded from PII scan (used to allow false positives like example keys in docs).
- **Repo-local `.commit-msg-blocklist`** — Terms that should never appear in public commit messages for this specific repo.

## Notes

- This skill does NOT bypass the global pre-commit hook — they work together
- For projects with a public/private repo split (dev mirror → public release): always push to the dev repo first, sync via your sync script, then safe-push the public repo
- When in doubt, treat a repo as public
