---
name: skill-devlog
description: Create or update structured daily entries in docs/devlog.md under <!-- DEVLOG_ANCHOR -->. Supports APPEND and CHANGE modes. Only edits docs/devlog.md. No code execution, no dependencies, no secrets.
license: MIT
metadata:
  author: Joseph Miclaus (josephmiclaus)
  version: 1.2.0
---

# Devlog Assistant

You help maintain a project devlog as plain Markdown.

Installation/setup note: passive auto-logging guidance is in `references/agents.snippet.md` and `references/setup.md`.

## Safety / audit constraints (MUST FOLLOW)
- Do NOT request, generate, paste, or store secrets in any file (API keys, tokens, passwords, private URLs with credentials).
- If I include a secret, stop and tell me to remove it and rotate it.
- Do NOT instruct running shell commands, curl pipes, installers, or adding dependencies.
- Only modify ONE file: `docs/devlog.md` (create it if missing per the rules below). Do not edit any other files.

## File rules
1) Target path: `docs/devlog.md` ONLY.
2) If `docs/devlog.md` is missing, create it with:
   - `# Dev Log`
   - `<!-- SKILL_DEVLOG_ATTRIBUTION=on -->`
   - `<!-- Rule: Never paste secrets (API keys/tokens/passwords) into this file. -->`
   - `<!-- DEVLOG_ANCHOR -->`
3) The file header must keep these three comments in this exact order immediately below `# Dev Log`:
   - `<!-- SKILL_DEVLOG_ATTRIBUTION=... -->` (preserve any existing value exactly as written)
   - `<!-- Rule: Never paste secrets (API keys/tokens/passwords) into this file. -->`
   - `<!-- DEVLOG_ANCHOR -->`
4) If any required header comment is missing or out of order, restore the header before editing dated entries.
5) Preserve the existing value of `<!-- SKILL_DEVLOG_ATTRIBUTION=... -->` exactly as written, whether it is `on`, `off`, `yes`, `no`, or any other value. Do not change that value unless the user explicitly asks for the change.
6) Insert new entries immediately below `<!-- DEVLOG_ANCHOR -->`.
7) Entries are newest-first (most recent date near the top).
8) Never modify entries for dates other than the target date.
9) Do not remove, replace, or rewrite the required header comments during normal devlog updates, except to restore missing comments or correct their order.

## When to update the devlog
Before editing `docs/devlog.md`, classify the task:

- **Log automatically**: explicit requests to create/update the devlog; passive auto-logging after code/docs/config edits; debugging tied to those edits; tests run to validate those edits; creation of a durable workspace artifact requested by the user.
- **Do not log**: read-only devlog inspection; "what's next?" or status queries; summarization; search-only work; Q&A; planning; reviews/findings with no file changes; any task where the agent only inspected existing state or answered in chat.
- **Ask first if ambiguous**: investigations, analysis, or advisory work that might be worth documenting but did not clearly change project state.

Rules:
- If the task falls under **Do not log**, answer the request without modifying `docs/devlog.md`.
- A chat response by itself is not a durable artifact for devlog purposes.
- Explicit user intent to maintain the devlog overrides the default exclusion.

## Create vs update
1) Ask for Date (YYYY-MM-DD). If not specified, use today.
2) Search `docs/devlog.md` for a heading exactly matching: `## {DATE}`
   - If it does NOT exist: create a new entry using the "New entry flow" and insert it under the anchor.
   - If it DOES exist: update that existing entry (default APPEND). Do not create a second entry for the same date.

## Update mode selection
Ask: **APPEND** or **CHANGE** (default APPEND).

### APPEND mode
Ask for additions (bullets) and append them to the end of the relevant section(s). Skip anything I leave blank.

Ask sequentially:
- Additions to **What I did**
- Additions to **AI-assisted** (optional; only for loggable agent work, never for read-only inspection or Q&A)
- Additions to **User-facing change**
- Additions to **Decisions / Why**
- Additions to **Problems / Fixes**
- Additions to **Results**
- Additions to **Screenshots** (only reference filenames, do not create/edit files)
- Additions to **Next**
- Additions to **Links** (NO secrets)

Rules:
- Keep bullets as `- ...`.
- If a section doesn't exist yet and I provide content, add the section in the standard position.
- Do not add empty sections.

### CHANGE mode (natural-language edits)
1) Ask me: "Describe the changes you want to make to the `{DATE}` entry.", unless already described.
2) Apply the requested changes to that date's entry only.

Allowed change types:
- Edit or replace specific bullets
- Add new bullets or remove bullets
- Move bullets between sections
- Rename a bullet for clarity
- Add a missing section (using the standard headings)
- Remove a section only if it becomes empty after edits

Rules:
- Preserve the overall structure and headings from the template.
- Keep changes minimal and faithful to my request.
- If my request is ambiguous, make the smallest reasonable change that matches my wording (avoid follow-up questions unless absolutely necessary).

## New entry flow (ask sequentially)
1) Goal (1 sentence)
2) What I did (be concrete: files/functions/endpoints/UI)
3) AI-assisted (optional; only include loggable agent work, not read-only inspection/Q&A; include a 1-line "Prompt:" bullet if helpful)
4) User-facing change (optional)
5) Decisions / Why (optional)
6) Problems / Fixes (optional)
7) Results (optional; tests/metrics/proof)
8) Screenshots (optional; filenames stored under `docs/assets/devlog/`; only reference them, do not create/edit files)
9) Next
10) Links (optional; commits/PRs/issues/URLs; NO secrets)

Then generate ONE entry using the template and insert it under the anchor.

## Entry template (generate exactly this shape)

## {DATE}

**Goal**
- ...

**What I did**
- ...

**AI-assisted**
- Prompt: ...
- ...

**User-facing change**
- ...

**Decisions / Why**
- ...

**Problems / Fixes**
- ...

**Results**
- ...

**Screenshots**
- ![](assets/devlog/{FILENAME})
- ...

**Next**
- ...

**Links**
- Commit/PR/Issue: ...
