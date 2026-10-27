---
name: daily-literature-digest
description: Set up, run, modify, or troubleshoot a personal AI literature digest automation that monitors Crossref, OpenAlex, and arXiv for new papers by user-provided research keywords, summarizes open metadata/abstracts, saves local Markdown or DOCX archives, and sends daily email digests through the Gmail connector. Use when the user asks for daily or weekly paper monitoring, publisher/arXiv alerts, research keyword digests, AI paper summary emails, Gmail literature updates, or a 09:00 recurring literature automation.
---

# Daily Literature Digest

## Overview

Use this skill to create a user's own daily literature digest. The bundled fetch script gathers open metadata and abstracts; Codex writes the AI interpretation, saves the archive, sends email through Gmail when connected, and creates the recurring automation.

Do not read paywalled full text or auto-login to university/publisher sites during the unattended daily run. Full-text follow-up is a separate explicit task after the user logs in themselves or provides PDFs.

## Setup Workflow

1. Confirm or infer the user's settings:
   - Recipient email for the digest.
   - Research keywords, grouped by theme when useful.
   - Language: ask if unclear; default to `zh-CN`.
   - Timezone: ask if unclear; otherwise use the user's local timezone.
   - Schedule time: default to `09:00`.
   - Sources: default to Elsevier, Springer Nature, Wiley, Taylor & Francis/Routledge, and arXiv.
2. Copy `scripts/daily_literature_digest.py` into the user's workspace, plus `scripts/markdown_to_docx.py` only when DOCX output is requested.
3. Create `daily-literature-digest.config.json` in the workspace:
   ```json
   {
     "recipient_email": "user@example.com",
     "crossref_mailto": "user@example.com",
     "language": "zh-CN",
     "timezone": "Europe/London",
     "schedule_time": "09:00",
     "output_dir": "daily-literature-digests",
     "keyword_groups": [
       {
         "label": "building energy",
         "terms": ["building energy", "building performance", "HVAC"]
       }
     ],
     "publishers": "use defaults",
     "include_arxiv": true,
     "rows": 20,
     "arxiv_rows": 25,
     "max_papers": 30
   }
   ```
   If using default publishers, omit the `publishers` key or replace it with the publisher objects in `references/default-config.md`; do not leave the string value in a real config.
4. Run a dry fetch:
   ```powershell
   python scripts\daily_literature_digest.py --config daily-literature-digest.config.json fetch --include-seen
   ```
5. Read the printed JSON file and write the digest:
   - Save full Markdown to `daily-literature-digests\YYYY-MM-DD.md`.
   - Summarize using only title, abstract, keywords, subject tags, DOI, journal, authors, publisher, and source metadata.
   - Mark arXiv items as preprints.
   - If there are no matches, still write a short no-results digest.
6. For no-abstract/title-only papers, write `daily-literature-digests\fulltext-inbox\to-download-YYYY-MM-DD.md` with DOI/URL and a note that no abstract/full text was read.
7. Check Gmail:
   - Call Gmail profile if Gmail tools are available.
   - If Gmail is connected, send a concise email body with the full local Markdown path.
   - If Gmail is unavailable, do not ask for SMTP credentials; tell the user to connect Gmail and record email status as `not-configured` or `failed`.
8. Mark success only after the Markdown archive exists:
   ```powershell
   python scripts\daily_literature_digest.py --config daily-literature-digest.config.json mark-success --data-file <JSON_PATH> --digest-file <DIGEST_PATH> --email-status <sent|failed|not-configured>
   ```
9. Create a Codex cron automation at the user's configured local time. For 09:00 daily:
   ```text
   FREQ=DAILY;BYHOUR=9;BYMINUTE=0;BYSECOND=0
   ```

## Summary Rules

- Treat matching as inclusive: one keyword term is enough to include a paper.
- Use priority for ranking, not for exclusion.
- For each paper include title, source/publisher, journal/preprint source, date, authors, DOI/URL, matched keywords, priority, research goal, method, main result, relevance to the user, and next action.
- If the abstract is missing, include the paper only as a title-level candidate and state clearly: `No abstract/full text was available; this is a title-level judgment only.`
- Do not infer research goal, method, or result for no-abstract papers.
- Mention Crossref, OpenAlex, or arXiv API errors in the digest and summarize successfully fetched results.

## Automation Prompt Requirements

The automation prompt must include:

- Exact workspace path and Python executable or `python` command that works in that workspace.
- Exact config path.
- Exact fetch command using `--config`.
- Recipient email, digest language, schedule time, timezone, and output directory.
- Instruction to summarize abstracts/open metadata only during the unattended run.
- Instruction to use Gmail connector if available.
- Instruction to call `mark-success` with `sent`, `failed`, or `not-configured`.
- A warning that local Codex automations may not run if the computer is asleep or the local runner is not active.

## Full-Text Follow-Up

When the user says they have logged in to ScienceDirect, a university library, or another publisher site:

- Do not ask for passwords.
- Use only the current active browser/session or PDFs the user downloaded into `daily-literature-digests\fulltext-inbox`.
- Process only the explicit batch/list the user asked about.
- Download/read accessible PDFs or article pages only when allowed by the active session.
- Summarize each full-text paper with topic, method, data/case, main results, limitations, and relevance.
- Save summaries to `daily-literature-digests\fulltext-summaries\YYYY-MM-DD-fulltext.md`.
- Do not create unattended daily publisher-download automation.

## References

- Read `references/default-config.md` when a user asks what defaults are used or wants a starter configuration.
- Use `scripts/markdown_to_docx.py` only when the user explicitly wants DOCX output.
