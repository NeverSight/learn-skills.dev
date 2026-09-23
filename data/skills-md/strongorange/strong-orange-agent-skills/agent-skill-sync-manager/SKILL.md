---
name: agent-skill-sync-manager
description: Syncs Agent Skills between the local working source (~/.agents/skills), agent runtime folders, and the team/personal publish repos, and audits the personal repo for company content. Use only when the user explicitly asks to register, sync, publish, or push skills.
disable-model-invocation: true
---

# Agent Skill Sync Manager

Read `config.local.yml` in this skill folder first: repo paths, personal remote, usage log, sensitive patterns. If it is missing, copy `config.example.yml`, ask the user for the values, and save it.

## Layout

- Working source: `~/.agents/skills/<skill>`. Edit skills here.
- Codex and Cursor read `~/.agents/skills` directly. Only Claude Code needs a link: `~/.claude/skills/<skill>` -> `../../.agents/skills/<skill>`.
- Installing from a publish repo: `npx skills add <owner/repo> -g -a claude-code codex cursor -s <skill> -y` produces exactly this layout.
- Publish repos keep `skills/<skill>/` and a README skill list that must match the folder.

## Where a skill may go

Resolve the source with `readlink -f` first, then check top to bottom. The first matching row wins.

| Skill | Destination |
|---|---|
| Third-party: a `~/.agents/.skill-lock.json` entry whose source is not one of the publish repos, a link to someone else's repo, or a bundled `.system` skill | Nowhere. Reinstall from its source instead |
| Source lives in a company repo | Team repo only, unless the user approves a personal copy. If it is tracked in a company product repo, change it there by PR |
| Only works with company infra or vault | Team repo only |
| Anything else | Personal repo |

A personal skill that only mentions company paths as examples can still go to the personal repo: publish a copy with generic placeholders, keep the local source as is, and add the skill to `generic_copies` in config.

## Full audit

Use when the personal repo has not been synced for a while.

1. Compare every `skills/<skill>` in the repo with its resolved source (`diff -rq -x config.local.yml -x __pycache__`). List working-source skills missing from the repo.
2. Decide per skill: update, add, or remove. For a skill in `generic_copies`, read the diff: a change only in the placeholder spots is expected, anything else is a real update to port by hand.
3. Copy without `config.local.yml` and `__pycache__`.
4. Run `scripts/scan-sensitive.sh <repo> --history`. It must print `clean` before any commit.
5. Sync the README list with `skills/`, following the README's existing order and style. Commit per change type in the repo's existing message style (`git log -5`). Push only when the user asked.

## Gotchas

- The personal remote must use the SSH host alias from config. Plain `github.com` authenticates with the company key. Check `git config user.email` in the repo too.
- Copying a whole skill folder drags in `config.local.yml` (personal emails, company paths) and `__pycache__`. The repo `.gitignore` must cover both. A committed `config.local.yml` is a leak by itself.
- Scanning HEAD is not enough. Earlier commits already leaked content and company author emails, so always scan with `--history`.
- `.gitignore` does not untrack files committed earlier. The scan reports them as "tracked but gitignored"; remove them with `git rm --cached`.
- The usage log covers Claude Code only, and only since it was created. Zero hits does not prove a skill is unused in Codex or Cursor, so ask before deleting. A skill name in Codex session logs is the injected skill list, not usage.
- A second copy or link under `~/.codex/skills` or `~/.cursor/skills` makes Codex list the skill twice. During a repo sync, report such runtime drift and leave fixing it to a separate request.
- Codex `~/.codex/config.toml` enables or disables skills by exact `SKILL.md` path (`[[skills.config]]`). Moving or unlinking a skill silently re-enables it under the new path, so rewrite those paths too. A disabled skill cannot be called even explicitly.
- Publish copies that were made generic differ from the local source on purpose. A hash mismatch on those is expected.
- If sensitive content already reached a pushed commit, follow [references/history-purge.md](references/history-purge.md). It is the only case that allows force push.
