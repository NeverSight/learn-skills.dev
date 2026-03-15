---
name: securityclaw-skill
description: Security-first skill auditing and quarantine for OpenClaw skills. Use when installing new skills, reviewing skills from unknown sources, scanning skills for prompt injection/exfiltration/supply-chain risks, or when a bot suspects a skill is malicious. Guides static + optional sandbox checks, quarantines suspicious skills, and produces an owner-action checklist (Delete / Report / Allow / Scan all).
---

# SecurityClaw (Skill Scanner)

## Install auto-scan service (recommended)

Install directly from public GitHub repo via npm:

```bash
npx github:mallen-lbx/SecurityClaw install
```

Run installer:

```bash
python3 scripts/install_securityclaw.py --skills-dir ~/.openclaw/skills --notify-config ~/.openclaw/securityclaw-notify.json
```

What installer does:

- macOS: installs `launchd` agent for continuous watch scanning
- Linux: installs `systemd --user` service for continuous watch scanning

Linux behavior when `systemd` is missing:

- warns during installation
- prints a concrete install command for detected package manager
- offers to run install command automatically

## Use the scanner script

Run the scanner (read-only by default):

```bash
python3 scripts/securityclaw_scan.py --skills-dir ~/.openclaw/skills
```

Quarantine anything suspicious (moves folders, no deletion):

```bash
python3 scripts/securityclaw_scan.py --skills-dir ~/.openclaw/skills --quarantine-dir ~/.openclaw/skills-quarantine --quarantine
```

Use an allowlist for known-safe exceptions (skill + hash + rules):

```bash
python3 scripts/securityclaw_scan.py --skills-dir ~/.openclaw/skills --allowlist ~/.openclaw/securityclaw-allowlist.json
```

Reports are saved by default to:

- `~/.openclaw/SecurityClaw_Scans`
- file format: `Security_Scan-(MM)-(DD)-(YYYY)-(scan number)` (example: `Security_Scan-02-06-2026-001.json`)
- when quarantine candidates exist, an ELI5 summary is also written: `Security_Scan-...-ELI5.md`

The scanner also prints a user-facing summary with severity counts, top findings, confidence indicators, and the owner action menu.

If quarantine candidates are found, the Markdown report includes a dedicated proof section with **4 concrete findings per quarantined skill**.
The scanner tells the user where the ELI5 summary file was written.

## Notifications

Configure notifications at `~/.openclaw/securityclaw-notify.json` (see `references/notification.example.json`).

Then run:

```bash
python3 scripts/securityclaw_scan.py --skills-dir ~/.openclaw/skills --notify-config ~/.openclaw/securityclaw-notify.json --notify-on quarantine
```

Supported channels:

- `telegram` (bot token + chat ID)
- `webhook` (POST JSON payload)
- `stdout` (local terminal output)

## Auto-scan new skills

Run watch mode to automatically scan when a skill is added or changed:

```bash
python3 scripts/securityclaw_scan.py --skills-dir ~/.openclaw/skills --watch --watch-scan-on-start
```

How it works:

- keeps a hash snapshot at `~/.openclaw/SecurityClaw_Scans/watch-state.json`
- polls `~/.openclaw/skills` on an interval (`--watch-interval`, default 30s)
- triggers a new scan when new/changed skills are detected
- in watch mode, report files are created only when findings require review/quarantine
- when a **new skill** is scanned, notifications are always sent

## Scan log

SecurityClaw appends every scan (manual and auto) to a monthly log file:

- directory: `~/.openclaw/SecurityClaw_Scans/Scan_Logs`
- file: `<Month>.log` (example: `April.log`)
- line format per scan: `scan completed 04-06-26 12:00:00`

## What to do when findings exist

If the report recommends `quarantine` for any skill:

1) **Do not execute** the skill.
2) **Quarantine** the skill folder.
3) **Notify the owner** with:
   - skill name
   - top reasons + file/line locations
   - recommended action
4) Await owner instruction:
   - **Delete**: remove quarantined skill
   - **Report**: prepare public report / IOCs (no secrets)
   - **Allow**: add allowlist entry and restore
   - **Scan all**: deep scan everything

## Optional: sandbox/dynamic checks (advanced)

Dynamic checks are optional and should run only after owner approval.

- Prefer running unknown code with:
  - no network egress
  - read-only filesystem except a temp workspace
  - no access to OpenClaw config/secrets

See `references/sandboxing.md`.

## Files

- `scripts/securityclaw_scan.py` — main scanner + quarantine
- `scripts/install_securityclaw.py` — cross-platform scheduler installer (launchd/systemd)
- `references/rules.md` — rule catalog (what we flag and why)
- `references/sandboxing.md` — safe sandbox strategy + what to avoid
- `references/allowlist.example.json` — allowlist template (skill/hash/rule suppression)
- `references/notification.example.json` — notification channels template
