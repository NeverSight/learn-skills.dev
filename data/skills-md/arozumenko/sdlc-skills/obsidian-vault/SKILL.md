---
name: obsidian-vault
description: Use when the user says 'save to vault', 'log this note', 'find my notes about X', 'what's in my inbox', 'open loops', or when filing an incoming signal (email/chat/memo) or updating people/project/meeting notes. Headless, file-system Obsidian vault operations, no Obsidian app needed.
license: Apache-2.0
compatibility: Requires Python 3.10+ (stdlib only). Vault path via $OBSIDIAN_VAULT_PATH. ripgrep recommended (falls back to grep).
metadata:
  authors:
    - Artem Rozumenko <artem_rozumenko@epam.com>
  version: "0.1.0"
---

# Obsidian Vault

Operate the user's Obsidian vault as a queryable second-brain — headlessly. The vault is plain markdown plus YAML frontmatter; the agent reads and writes files directly. Obsidian itself is for the *user* to browse the result later.

This skill is self-contained and stdlib-only. It pairs well with an agent-internal memory skill (e.g. the `memory` skill), but doesn't require one:

| Where | What goes here | Who reads it |
|---|---|---|
| Agent memory (if any) | Short-lived cognition, operational logs | The agent |
| `$OBSIDIAN_VAULT_PATH/` | User-facing knowledge base, signals, contacts | The user (in Obsidian); agent files into it |

If unsure where something belongs: short-lived agent thought → memory; user might want to read it later → vault.

The CLI is `scripts/vault.py`. Vault path comes from `$OBSIDIAN_VAULT_PATH` or `--vault`; the CLI exits with an error if neither is set. Output is human-readable on stdout; errors → stderr; non-zero exit on failure.

## Vault layout

The skill *enforces* this layout for any note it creates. Existing notes are not migrated.

```
<vault>/
  inbox/                    # raw, unprocessed signals — landing zone
  daily/YYYY-MM-DD.md       # user-facing daily note (append-only)
  people/                   # one note per contact — the leverage folder
  projects/                 # active projects
  researches/               # deep-dive notes, reading captures
  meetings/                 # synchronous events with attendees + outcomes
  decisions/                # decision log — "why did we do X"
  memories/                 # user-facing long-term memories
  mails/                    # processed email archive
  chats/                    # processed chat snippets (Telegram, Teams, Slack)
  plans/                    # plans, roadmaps, intent docs
  attachments/              # binaries (images, PDFs, audio)
  templates/                # frontmatter templates per note type
  open-loops.md             # active follow-ups (single flat file)
  open-loops-archive/
    YYYY-MM.md              # one file per month, closed loops
```

**Two hard rules:**

1. **Folder = type. Frontmatter = state.** PA filters by `status: inbox` *across* folders to find work. Folders never carry state. Don't invent `inbox/`-flavored subfolders inside other folders.
2. **Always wikilinks.** Use `[[people/anna-petrenko]]`, never `[Anna](./people/anna-petrenko.md)`. Free backlinks, rename-tracking, and the user gets a graph view.

## Frontmatter schema

Every note carries this baseline. Per-type extensions are listed below.

```yaml
---
type: signal | project | research | decision | meeting | person | plan | memory | mail | chat
status: inbox | active | done | archived
created: 2026-04-07
source: email | telegram | teams | manual | web | voice
people: [[people/anna-petrenko]]
projects: [[projects/q2-launch]]
tags: [urgent, finance]
processed_at: 2026-04-07T15:23:00
---
```

### Per-type extensions

| Type | Extra fields |
|---|---|
| `person` | `org`, `role`, `last_contact`, `topics`, `urgency` |
| `meeting` | `attendees` (list of `[[people/...]]`), `agenda`, `actions`, `duration_min` |
| `decision` | `alternatives`, `rationale`, `would_change_mind_if` |
| `project` | `started`, `target_date`, `blocker`, `next_action` |
| `mail` | `from`, `to`, `subject`, `received_at`, `thread_id` |
| `chat` | `channel`, `participants`, `received_at` |

Unknown fields are tolerated (warn-on-unknown, never blocking) — the user may extend the schema in Obsidian and the skill must not break their notes.

## Decision tree — where does an incoming signal go?

```
Is it a synchronous event (call, meeting)?           → meetings/
Is it an email?                                      → mails/
Is it a chat fragment (Telegram/Slack/Teams)?        → chats/
Is it a deep dive / web capture / reading note?     → researches/
Is it a plan / roadmap / intent doc?                 → plans/
Is it a decision the user wants to remember why?    → decisions/
Is it long-term knowledge for the user to reread?   → memories/
Is it a person mentioned 2+ times?                   → people/<slug>.md (autocreate)
Is it about an active project?                       → also wikilink to projects/<slug>
None of the above + user might care later?          → inbox/  (PA triages later)
None of the above + agent-internal only?             → memory log (NOT vault)
```

The wikilink convention means a single signal can be filed in *one* place and referenced from many. Don't duplicate notes — link them.

## CLI commands

All commands respect `--vault <path>` (overrides env) and `--role <name>` (defaults to the agent's role name).

### Filing & creation

```bash
# Move from inbox/ to its right home, fill frontmatter, set processed_at
vault.py file inbox/2026-04-07-anna-question.md --type chat --person anna-petrenko --project q2-launch

# Create a new note from template, opens for editing (or --content "...")
vault.py new project q2-launch --description "Q2 launch coordination"
vault.py new meeting 2026-04-07-team-sync --attendees anna-petrenko,bob
vault.py new decision use-postgres-not-sqlite --rationale "We need MVCC and JSONB"
```

### Querying

```bash
# Find notes by frontmatter facets — uses ripgrep, returns paths + summary
vault.py find --type meeting --since 30d
vault.py find --status inbox
vault.py find --person anna-petrenko --tag finance
vault.py find --project q2-launch --since 7d

# Get a single note's frontmatter + first paragraph
vault.py show people/anna-petrenko.md
```

### People

```bash
# Find or create a person note. --touch updates last_contact and bumps counter.
vault.py person anna-petrenko --touch
vault.py person "Anna Petrenko" --org "Acme" --role-field "CFO" --touch
```

People notes are autocreated **only on the second touch** to avoid noise from one-off mentions. The first touch records the person in `<vault>/.obsidian-vault/<role>/people-pending.md` (vault-local agent state, ignored by Obsidian); the second touch promotes it to a real `people/<slug>.md`.

### Open loops

```bash
vault.py loop add "Follow up with Anna re: contract by Tue"
vault.py loop list
vault.py loop done --id <id>        # cuts from open-loops.md → archive/YYYY-MM.md
```

`<id>` is a short hash printed by `loop add` and `loop list`. Closed loops archive into the **month they were closed** (not the month they were opened).

### Daily note

```bash
vault.py daily append "Spoke with Anna about Q2 launch — green light"
vault.py daily show                  # prints today's note
vault.py daily show --date 2026-04-06
```

**NEVER use the Write tool on daily notes.** They're append-only and shared between you and the user. Only `vault.py daily append` is safe.

### Linking

```bash
# Add wikilink from a → b, idempotent (safe to call repeatedly)
vault.py link meetings/2026-04-07-team-sync.md people/anna-petrenko.md
```

### Bases (Obsidian dashboards for the user)

```bash
# Copy starter .base files into the vault root (one-time, opt-in)
vault.py bases install

# What's available
vault.py bases list
```

Bases require Obsidian 1.9+. If the user is on an older version they're harmless YAML files that don't render — no error.

### Validation

```bash
# Lint all frontmatter against the schema; warn-only by default
vault.py validate
vault.py validate --strict           # exit 1 on any warning
vault.py validate --type meeting
```

`validate` reports unknown fields, missing required fields, and invalid date formats. **It is not blocking** — the user is allowed to evolve the schema. The skill must continue to function on notes that fail validation.

## Querying without Bases

Bases require Obsidian. For headless queries the skill uses `ripgrep` over frontmatter:

```bash
# All notes tagged urgent
rg -l '^tags:.*urgent' "$OBSIDIAN_VAULT_PATH"

# All notes with status: inbox
rg -l '^status: inbox' "$OBSIDIAN_VAULT_PATH"

# Backlinks to a person (substitute the wikilink target)
rg -l '\[\[people/anna-petrenko\]\]' "$OBSIDIAN_VAULT_PATH"
```

`vault.py find` wraps these patterns. Don't roll your own grep — use the CLI so the schema stays consistent.

## Conventions for content

- **Wikilinks** for everything internal: `[[people/anna]]`, `[[projects/q2-launch]]`, `[[decisions/use-postgres]]`.
- **Markdown links** only for external URLs: `[Acme press release](https://acme.example/news)`.
- **Callouts** for structured note sections (the user gets nice rendering, the agent gets greppable headers):
  ```markdown
  > [!info] Context
  > Anna asked about Q2 budget.

  > [!todo] Action
  > Reply by Tuesday with revised numbers.

  > [!quote] What she said
  > "We need to ship by end of May or push to Q3."
  ```
- **Block references** (`^block-id`) when the daily note needs to point back to a specific paragraph in a meeting note.
- **Headings** for navigation, not styling. One H1 per note (the title); H2 for sections.

## Sync conflicts

If the vault is on Obsidian Sync / iCloud / syncthing, you may see conflict files like `Note (Anna's iPhone).md`. The skill detects them and **refuses to operate on them** — they require human resolution. `vault.py validate` lists conflict files in its report.

## What NOT to do

- **Never overwrite a daily note.** Append only, via `vault.py daily append`.
- **Never duplicate a note across folders.** Link instead.
- **Never invent new top-level folders.** The schema is fixed; extend via tags or new note types.
- **Never store agent-internal state in the vault.** That belongs in `.agents/memory/`.
- **Never write a person note for a one-off mention.** Wait for the second touch.
- **Never use markdown links for internal references.** Wikilinks only.
- **Never operate on sync conflict files** (`*(.* iPhone)*.md`, `*conflict*.md`).
