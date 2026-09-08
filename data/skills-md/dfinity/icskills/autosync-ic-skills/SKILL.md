---
name: autosync-ic-skills
description: One-time installer that makes a Claude Code project keep its Internet Computer skills up to date automatically. Sets up a SessionStart hook plus a sync script so .claude/skills/ always mirrors the latest skills published at skills.internetcomputer.org. Use when a user wants to install, bootstrap, or enable "always-latest" Internet Computer / IC / ICP / Motoko skills in a project, or pastes the link to this skill. This is a one-time setup action, not ongoing IC knowledge — after it runs, the installed hook keeps skills current on every session. Do NOT use for IC coding questions themselves — this only configures auto-updating skills.
license: Apache-2.0
metadata:
  title: Automatically Sync Latest IC Skills
  category: Infrastructure
---

# Set up self-updating Internet Computer skills

This skill installs a small amount of project configuration so that **every new
Claude Code session automatically downloads the latest Internet Computer skills**
into `.claude/skills/`, where Claude discovers and triggers them natively.

It is a **one-time installer**. After you complete the steps below, the user never
needs this link again — the installed `SessionStart` hook does the work from then on.

## What you will create

1. `.claude/sync-ic-skills.sh` — a **differential** sync script that mirrors the live
   skill index into `.claude/skills/`.
2. A `SessionStart` hook in `.claude/settings.json` that runs that script.
3. An immediate first run, so skills are present right away.

The script is a **differential mirror**. It fetches the discovery index once and
compares each skill's published `hash` against a stored manifest, re-downloading only
the skills that actually changed (and pruning ones removed upstream). Unchanged skills
are skipped with no per-file downloads, and the script writes nothing to stdout unless
something changed. If the server does not publish a `hash` for a skill, the script falls back to
re-downloading it every run, so it remains correct either way.

## Important: tell the user what to expect

Adding a hook means a shell script will run automatically at the start of future
sessions. Claude Code will ask the user to **review and trust** the new hook before
it activates — this is expected and correct. Let the user know:

> "I'm adding a `SessionStart` hook that runs `.claude/sync-ic-skills.sh`. Claude Code
> will ask you to approve/trust it before it runs automatically. After that, your IC
> skills stay current on every session."

Do **not** attempt to bypass that approval.

## Step 0 — Check prerequisites (`curl`, `jq`)

The sync script needs `curl` (virtually always present) and `jq` (often not).
Before writing anything, check for them:

```bash
command -v curl >/dev/null 2>&1 && echo "curl: ok" || echo "curl: MISSING"
command -v jq   >/dev/null 2>&1 && echo "jq: ok"   || echo "jq: MISSING"
```

- If `jq` is **missing**, offer to install it (ask the user before running an install
  command). Pick the right one for their platform:
  - macOS (Homebrew): `brew install jq`
  - Debian/Ubuntu: `sudo apt-get update && sudo apt-get install -y jq`
  - Fedora/RHEL: `sudo dnf install -y jq`
  - Alpine: `apk add jq`
  - Arch: `sudo pacman -S --noconfirm jq`
  - Windows (winget): `winget install jqlang.jq`
- If the user declines, still proceed — the script is written to degrade gracefully
  (it exits cleanly with a warning when `jq` is absent), and they can install `jq`
  later and the next session will sync.

## Step 1 — Download the sync script

The script is published as a file alongside this skill, so you fetch it verbatim rather
than transcribing it (this guarantees byte-exact content). Create the `.claude` directory
and download it:

```bash
mkdir -p .claude
curl -fsSL https://skills.internetcomputer.org/.well-known/skills/autosync-ic-skills/scripts/sync-ic-skills.sh \
  -o .claude/sync-ic-skills.sh
```

Do **not** hand-write or paraphrase the script — always fetch the published copy so the
sync logic stays correct as it is updated upstream.

**What the script does** (for the user's awareness):

- Fetches `https://skills.internetcomputer.org/.well-known/skills/index.json` once.
- For each skill, compares the published `hash` against `.claude/skills/.ic-managed.json`
  (a `{ "<skill>": "<hash>" }` manifest of skills it manages) and re-downloads only the
  skills whose hash changed or are new.
- Prunes skills it previously installed that are no longer in the index, and
  replaces a changed skill's whole directory via an atomic staging swap — so files
  renamed or removed upstream don't linger inside a skill, and an interrupted
  download leaves the existing copy intact.
- Writes nothing to stdout on a no-op sync. When something changed it prints one JSON
  object whose `systemMessage` carries the `added / updated / removed` summary — that
  string is what the user sees, because SessionStart hooks surface JSON fields rather
  than raw output. Its diagnostics (interrupted-sync recovery, unsafe skill names) go to
  stderr and so are not displayed.
- Degrades gracefully: exits cleanly (keeping cached skills) if the network is down or
  `jq` is missing, and falls back to re-downloading skills the server publishes no
  `hash` for.

## Step 2 — Register the SessionStart hook (idempotently)

Add a `SessionStart` hook to `.claude/settings.json` that runs the script.

- If `.claude/settings.json` does **not** exist, create it with the content below.
- If it **does** exist, **merge** — preserve all existing keys, hooks, and
  permissions. Only add the `SessionStart` entry, and **only if an equivalent
  `bash .claude/sync-ic-skills.sh` command is not already present** (do not create a
  duplicate). Parse the existing JSON, insert into the `hooks.SessionStart` array,
  and write it back; never blindly overwrite the file.

The entry to ensure is present:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "bash .claude/sync-ic-skills.sh" }
        ]
      }
    ]
  }
}
```

## Step 3 — Run it once now

Run the script immediately so the skills are available in this session without
waiting for the next session start:

```bash
bash .claude/sync-ic-skills.sh
```

## Step 4 — Verify and report

- Confirm `.claude/skills/` now contains skill directories (e.g. `writing-motoko`,
  `static-site`, `internet-identity`, …) each with a `SKILL.md`.
- Confirm `.claude/skills/.ic-managed.json` maps each synced skill name to its hash.
- Tell the user: how many skills were installed, that the `SessionStart` hook is in
  place, and that they'll be prompted to trust the hook before it auto-runs next
  session. From then on, their IC skills refresh automatically every session.

## Notes

- **Safe to re-run.** Re-invoking this skill or the script is idempotent: the hook is
  not duplicated, and only skills tracked in `.ic-managed.json` are ever pruned.
- **Differential by hash.** The script keys off the per-skill `hash` field in the
  discovery index, so a normal session that touches nothing downloads only `index.json`
  and exits silently. Skills are re-downloaded only when their hash changes. Migrating
  from an older version of this script (whose manifest was a bare name array) is handled
  automatically on the next run.
- **Optional mid-session refresh.** For very long-running sessions, the user can also
  run `bash .claude/sync-ic-skills.sh` manually, or schedule it (e.g. via `/loop` or a
  cron routine) — but the SessionStart hook covers the normal case.
