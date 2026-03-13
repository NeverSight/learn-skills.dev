---
name: log-to-post
description: "Log what you built (text, images, commits, branches); get LinkedIn, X, Reddit, and standup copy in one go. Stores structured daily logs (logs/YYYY-MM-DD.md) and generates platform-ready drafts (posts/). Use when the user wants to log this, log my day, turn my log into a post, post ideas from my logs, standup from my logs, or drafts for LinkedIn / X / Reddit. Use this skill whenever the user mentions logging their day, turning notes or chat into posts, standup notes, or generating LinkedIn/X/Reddit from dev activity, even if they don't name the skill. Messages that start with \"Log: \" (with a space) are log requests: log the rest of the message."
---

# Log-to-Post

Log what you built (text, images, commits, branches); get LinkedIn, X, Reddit, and standup copy in one go. One base path holds `logs/` and `posts/` by day.

## Base path (first run or unknown)

- If the base path for logs and posts is not known, ask once: *"Where should I store your logs and posts? (e.g. `~/dev-log` or `./log-to-post`)"*
- Persist the choice by creating a marker file at that path: `.log-to-post` with a single line `basePath: .` (or the chosen path). On later runs, if `logs/` and `posts/` exist under a candidate path, or `.log-to-post` exists, use that as the base path without asking again.
- Under the base path ensure two folders exist: `logs/` and `posts/`.

## Log structure and format

- One file per day: `logs/YYYY-MM-DD.md`.
- Each log entry in the file must follow the structure in [references/log-format.md](references/log-format.md): entry type, content, optional links/tags.
- Entry types: `started` | `running` | `blocked` | `discovered` | `shipped` | `learning`.

## Collecting from different inputs

1. **"Log: " prefix**  
   If the user's message starts with `Log: ` (capital L, colon, space), treat the rest of the message as content to log. Strip the prefix, parse into one or more log entries, infer entry type from context, and append to today's log file. No need to ask for confirmation—just log it.

2. **Free text / agent chat**  
   Parse the user message or pasted conversation into one or more log entries. Infer entry type from context (e.g. "shipped", "discovered", "blocked"). Append to today's log file (`logs/YYYY-MM-DD.md`) using the format in references/log-format.md.

3. **Images**  
   Describe or transcribe the image content in one or two sentences, assign an entry type, and append as a log entry to today's file. Infer entry type from the image when possible (e.g. screenshot of terminal/code → `shipped` or `discovered`, diagram or doc → `learning`). Only ask the user for type when it's ambiguous.

4. **Git commits**  
   Run `git log` (e.g. `git log -n 20 --oneline` or with `--format=...`) in the repo the user indicates. For each relevant commit, include the branch name when available (e.g. `git log` with `%(refname:short)` or `git branch --show-current` for the repo). Write a short log entry (e.g. type `shipped` or `discovered`) with optional `branch` and `repo` in the entry metadata, and append to today's log file. Optionally include commit link in `links`.

5. **Multiple entries in one go**  
   When the user dumps several items (bullets, paragraphs, or a list), create one log entry per item and append all to the same day file.

## Writing logs

- Read existing `logs/YYYY-MM-DD.md` if present; append new entries without duplicating. Use the same heading/entry format as in references.
- If the file does not exist, create it with a short date heading and then the new entries.

## Generating post ideas and drafts

- When the user asks for "post ideas", "drafts", "standup from my logs", or "turn my log into posts":
  1. Resolve base path. List available log files (e.g. under `logs/*.md`) and show a short summary: *"You have logs for [list dates]. Use all, a date range, or only certain entry types (e.g. shipped + discovered)? Default: today + last 2 days if you don't specify."* Only after the user confirms or accepts the default, proceed.
  2. Read the content from the chosen `logs/YYYY-MM-DD.md` file(s). Aggregate the entry contents (and optional project name) into a single text block.
  3. Use the content philosophy and platform rules in [references/prompts-and-platforms.md](references/prompts-and-platforms.md) to generate. Each output format uses a distinct style per that reference. Produce:
     - One draft per format (LinkedIn, X, Reddit, Standup), or
     - A single "post ideas" section with 2–3 bullet ideas and then one draft per format if the user wants full drafts.
  4. Write output under `posts/`:
     - Either one file per day: `posts/YYYY-MM-DD.md` containing all formats (LinkedIn, X, Reddit, Standup) with clear headings, or
     - One file per platform per day: `posts/YYYY-MM-DD-linkedin.md`, `posts/YYYY-MM-DD-twitter.md`, `posts/YYYY-MM-DD-reddit.md`, `posts/YYYY-MM-DD-standup.md`.
  5. Prefer the single-file-per-day format unless the user asks for separate files per platform.

## Checklist for "log this" requests

- [ ] Resolve base path (ask or infer from `.log-to-post` / existing `logs/`).
- [ ] Ensure `logs/` and `posts/` exist.
- [ ] Parse input (text / image / git) into entries with type and content.
- [ ] Append to `logs/YYYY-MM-DD.md` using the reference format.

## Checklist for "generate posts" requests

- [ ] Resolve base path. Prompt user on which logs/dates/themes (or use default: today + last 2 days); then read and aggregate only the chosen set.
- [ ] Read and aggregate log content from the chosen file(s).
- [ ] Generate drafts using references/prompts-and-platforms.md (one per format: LinkedIn, X, Reddit, Standup).
- [ ] Write to `posts/YYYY-MM-DD.md` (or per-platform files if requested).

## Additional resources

- [references/log-format.md](references/log-format.md) — Log entry format and fields. Read when collecting or writing log entries (any input type or appending to logs).
- [references/prompts-and-platforms.md](references/prompts-and-platforms.md) — Content philosophy and platform rules. Read when generating post ideas or drafts (LinkedIn, X, Reddit, Standup).
