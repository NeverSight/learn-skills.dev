---
name: turnitin0
description: >-
  Use when the user wants Turnitin AI detection, similarity/plagiarism checking,
  or AI text humanization via turnitin0.com — including /turnitin0, uploading
  .docx/.pdf/.txt, paying for checks, downloading reports, or reducing AI scores.
---

# Turnitin0 Skill

Codex / Claude Code / Cursor skill for **Turnitin0** ([turnitin0.com](https://www.turnitin0.com)): Turnitin AI detection + similarity reports, and AI text humanization.

Turnitin0 is **not** affiliated with Turnitin, LLC. Reports match what instructors see in institutional systems.

## Dual entry (important)

This repo has **two valid skill roots** (same commands):

| Entry | Path | Used by |
|-------|------|---------|
| **A. Package** | `skills/turnitin0/` | Cursor plugin, Codex/Claude preferred install |
| **B. Repo root** | repository root (this file) | Codex when installing the whole repo / `--path .` |

Canonical implementation (JWT `config.json`, `downloads/`, real Python) lives under **`skills/turnitin0/`**. Repo-root `scripts/*.py` forward there.

Prefer entry A when possible. From either root:

```bash
python scripts/login.py
```

## When to use

- User asks for `/turnitin0`, Turnitin check, AI detection, similarity/plagiarism report
- User asks to humanize / reduce AI score on academic text
- User provides **text**, an **attachment**, or an **explicit file path** from the runtime

## Hard rules

1. **Only read file paths the runtime already provided** (attachments / user-given paths). Do not scan the disk or home directory for files.
2. **Never put JWT in a browser URL.** Login uses `?r=` (16-digit code). Pay uses `?c=` (`pay_code`). Never `?t=`.
3. Auth is the site JWT in `config.json` (under `skills/turnitin0/`) → `Authorization: Bearer <token>`. Do not invent OAuth/PayPal in the skill.
4. Prefer running the Python scripts below; do not reimplement API calls ad hoc unless debugging.

## Setup

- Python 3.10+ (stdlib only; no pip install required)
- Working directory: **repo root** or **`skills/turnitin0/`**

```bash
python scripts/login.py
```

## Workflow

```text
login → upload (text|file) → pay/ready (pay.py if needed) → create task → poll → download to downloads/
```

### 1) Login

```bash
python scripts/login.py
# force re-login:
python scripts/login.py --force
```

Opens `https://www.turnitin0.com/skill_login?r=<16 digits>`. User signs in with Google. Token is saved to `skills/turnitin0/config.json` (gitignored).

### 2) Turnitin check (similarity + AI)

```bash
# text
python scripts/turnitin_check.py --text "Your essay text here..." --title "essay"

# file (.docx / .pdf / .txt) — path MUST be runtime-provided
python scripts/turnitin_check.py --file "/absolute/path/to/paper.docx"
```

Usually finishes in 5–10 minutes (skill waits up to **1 hour**). Saves AI + similarity reports under `skills/turnitin0/downloads/`.

### 3) Humanize

```bash
python scripts/humanize.py --text "Your essay text here..." --title "essay"
python scripts/humanize.py --file "/absolute/path/to/paper.docx"
# optional: pass AI report from a prior check
python scripts/humanize.py --file "/path/paper.docx" --ai-report-id 123
```

Accepts `.docx` / `.txt`. Result document lands in `skills/turnitin0/downloads/` (skill waits up to **2 hours**).

### 4) Pay (usually automatic)

Scripts call this when balance is insufficient. Login and pay browser pairing each time out after **5 minutes**.

```bash
python scripts/pay.py --document-id 123 --type turnitin_check
python scripts/pay.py --document-id 123 --type humanizer
```

Opens `https://www.turnitin0.com/skill_pay?c=<pay_code>` only — **never** `?t=<jwt>`.

### 5) Manual download

```bash
python scripts/download.py --report-id 456
python scripts/download.py --document-id 789
```

## Pricing (site billing; confirm via `/api/me`)

**Turnitin check** (per check packs, 100-day validity): $2.50 / $4.50(2) / $10(5) / $17.50(10)

**Humanizer**: PAYG $0.80 / 500 words (round up); prepaid packs 10k/30k/100k words do not expire. Prepaid balance first, then PAYG.

## Agent checklist

Copy and track:

```
- [ ] Ensure login (`python scripts/login.py` if needed)
- [ ] Confirm input is text OR an explicit runtime file path
- [ ] Run turnitin_check.py OR humanize.py
- [ ] If browser opens for pay, tell user to complete PayPal
- [ ] Wait for script to finish; report local paths under skills/turnitin0/downloads/
```

## Layout

```text
# Entry B — repo root (this SKILL.md)
SKILL.md
scripts/                 # thin forwards → skills/turnitin0/scripts
config.example.json      # mirror

# Entry A — canonical package
skills/turnitin0/
  SKILL.md
  config.example.json
  config.json            # local only — JWT
  downloads/
  scripts/               # real implementation
```

## Errors

- `402` / `payment_required` → pay flow (`?c=`), then retry task
- Invalid token → `python scripts/login.py --force`
- Upload rejected → check file type/size/English word-count rules on the site
