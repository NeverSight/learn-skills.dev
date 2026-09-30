---
name: standup
description: "Generate the user's daily standup update from real activity: GitHub PRs and commits, unpushed local work across worktrees, and Claude/Codex/OpenCode session history. Use when the user says /standup, give me my standup, what did I do yesterday, or wants a status summary."
---

# Standup

Produce a short, spoken-ready standup update from real activity. Never invent items. A gathering script collects the raw material. The script only gathers. The summary is the skill's job.

## Step 0: Confirm the day scope

Propose the smart default, then ask the user to confirm. One question, three choices: today, previous workday, or both. Monday reaches back to Friday. A weekend run covers since Friday. Late-night work past midnight belongs to the standup that has not happened yet.

Translate the confirmed scope into explicit bounds. A single named day means that day's full cycle, 10:00 that day to 10:00 the next, so its late-night work stays attached.

## Step 1: Gather

Run `${CLAUDE_SKILL_DIR}/scripts/gather.py`. With no arguments it computes the default window from the current time and prints one JSON blob. Pass explicit bounds when the user confirmed a scope other than the default.

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/gather.py"
python3 "${CLAUDE_SKILL_DIR}/scripts/gather.py" --start 2026-09-05 --end 2026-09-06
python3 "${CLAUDE_SKILL_DIR}/scripts/gather.py" --start 2026-09-04
python3 "${CLAUDE_SKILL_DIR}/scripts/gather.py" --org myorg --repo-root /path/to/repo
```

A bare `YYYY-MM-DD` means 10:00 local that day. Use full ISO only for sub-day precision. `--org` overrides the auto-detected org from the git remote. `--repo-root` defaults to the current directory. The local scan covers that repo and all its git worktrees. `--no-github`, `--no-local`, and `--no-sessions` drop a source when asked. The `window` object in the output states exactly what was covered. Echo that range in the header.

Session history is best-effort across Claude, Codex, and OpenCode. Missing stores are skipped silently. Present stores never block the other sources.

## Step 2: Write the standup

Keep it short and flat. One ticket is one line. A whole standup reads aloud in well under a minute. Never list individual commits or SHAs. Never dump file lists. Never quote session prompts verbatim.

Collapse every commit, PR, and local change for the same ticket into a single line. Branch names and PR titles carry the ticket number.

Three buckets, in this order. Omit any empty bucket.

- **Done.** Merged PRs and pushed commits. Say what landed, not that a PR merged.
- **In progress.** Open PRs and unpushed local work such as uncommitted changes, unpushed commits, and stashes. Use sessions only to name a ticket that had real work but left no commit yet. Skip anything already covered above.
- **Reviewed.** Teammates' PRs the user reviewed. One line total when few.

## Output format

```text
Standup — <window.start_readable> to <window.end_readable>

Done
- <ticket>: <what landed> (#<pr>)

In progress
- <ticket>: <what is mid-way through>

Reviewed
- <teammate>'s <ticket> (#<pr>)
```

Write each line as a short phrase, not a sentence. Lead with the ticket or feature, then a few words on what it was. Merge small related items onto one line rather than spending a bullet each.

When any of `github.errors`, `github.error`, `local.errors`, or `sessions.errors` is present, or a source was skipped, add one short note at the end so the user knows the picture is partial. Otherwise say nothing about plumbing. When everything is empty, say so in one line and suggest checking the org or repo root.
