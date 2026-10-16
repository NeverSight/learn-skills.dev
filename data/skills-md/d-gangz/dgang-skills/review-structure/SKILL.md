---
name: review-structure
description: >
  Audit a non-technical repo's folder structure for agent-navigability and propose a refactor plan.
  TRIGGER when user says "review structure", "audit folders", "audit my repo", "check organization",
  "is my repo agent-friendly", "clean up structure", or runs "/review-structure".
---

# Review Structure

You are auditing the user's repo so that **you** (Claude) can navigate it cold and operate inside it effectively. The user is non-technical — they don't search this repo, you do. Every principle below comes from how your own search tools actually work.

## How you search a repo

Internalize this before auditing — every principle downstream is a consequence of these mechanics.

- **`Read`** — load a known file by path. First move on entry: read root `CLAUDE.md` or `README.md`.
- **`Glob`** — pattern-match file paths. Case-sensitive, literal. e.g. `**/CLAUDE.md`, `clients/*/profile.md`.
- **`Grep`** — search file contents, usually scoped with `--glob`.
- **`Bash: ls / find`** — see directory shape, not content. e.g. `find . -type d -maxdepth 2`.
- **`CLAUDE.md` auto-loading**:
  - Ancestor `CLAUDE.md` files (root + dirs above cwd) load **at session start**.
  - Subdirectory `CLAUDE.md` files load **lazily, only when you `Read`/`Edit` a file in that subtree**. They do **not** fire on `Glob`, `Grep`, or `ls`.

The corollary: **a subdirectory `CLAUDE.md` cannot rescue bad names.** Naming carries navigation; `CLAUDE.md` only carries non-obvious context once you've already decided to open a file.

## Principles (the audit checklist)

1. **Self-describing names.** A cold reader (you) should infer content from the path alone. `data/` says nothing; `sales/pipeline.csv` says everything. Naming is your primary navigation aid because Glob/Grep see paths, not CLAUDE.md.
2. **Lowercase kebab-case** — `acme-corp/`, not `Acme Corp/` or `AcmeCorp/`. This is mechanical, not aesthetic: spaces break shell commands, casing breaks Glob patterns.
3. **Group by domain, not by file type.** Folders are business areas (`sales/`, `clients/`, `operations/`), not file kinds (`templates/`, `data/`, `scripts/`). Domain grouping lets you ignore irrelevant subtrees entirely; file-type grouping forces you to load everything.
4. **Sibling folders mirror each other's shape.** If every client folder has `profile.md`, `contacts.md`, `updates.md`, then `Glob clients/*/profile.md` pulls all profiles in one call. If shapes vary, you have to `Read` each folder to discover what's there.
5. **Shallow + wide over deep + narrow.** Three levels (root → domain → leaf) is comfortable. Five-deep generic nesting (`stuff/items/things/2024/q1/`) gets lost.
6. **Glossary for user-specific vocabulary.** Keep an `agent-docs/glossary.md` file (in an `agent-docs/` directory at the repo root, alongside other progressive-disclosure docs like `architecture.md`, `conventions.md`, etc.) for terms specific to the user's world that Claude can't infer — internal client codenames, industry acronyms, custom workflow names ("V2 brief", "the rolodex"), team shorthand. The root `CLAUDE.md` must include this self-perpetuating rule:

   > *"When the user uses a term you don't understand, check `agent-docs/glossary.md` first. If the term isn't there, ask the user to clarify, then add the definition there."*

   Why a separate file (not inline in `CLAUDE.md`): the glossary keeps growing as the user works; a dedicated file stays manageable and only loads when needed. Why the rule lives in root `CLAUDE.md`: that file auto-loads at session start, so Claude always knows where to check and how to maintain the glossary — even though the glossary itself is read lazily, only when an unfamiliar term appears. Why `agent-docs/`: the convention from the `claude-md` skill — all progressive-disclosure docs live there, keeping the root tidy.
7. **Root `CLAUDE.md` always.** It's the entry interface — what the repo is, how the domains connect, where to go for what.
8. **Subdirectory `CLAUDE.md`: default is none.** Only add one when the folder carries implicit context that names can't convey. Conditions that justify one:
   - **Behavioral rules that apply to every file in the subtree** — e.g. brand voice in `marketing/`, citation style in `research/`. Auto-loading the rule means Claude can't forget it when editing files inside.
   - **Per-instance context that varies** — e.g. each client folder has its own engagement history, contacts, recent decisions.
   - **Domain rules Claude can't infer from file names** — pricing logic, pipeline stages, judgment calls, things-to-watch-for.
   - **Naming conventions that operate inside the folder** — e.g. "files prefixed `draft-` are not yet reviewed."

   Skip when the folder's shape and names already explain themselves. An empty-restating `CLAUDE.md` is dead weight and trains Claude to skim past them.
9. **No orphaned business content.** Business files (proposals, client notes, pricing data, templates, scripts that operate on your data) belong inside a domain folder. Conventional root-level files — `README.md`, `CLAUDE.md`, `.gitignore`, `.env`, `package.json`, `pyproject.toml`, `LICENSE`, plus Claude-infrastructure dirs (`.claude/`, `agent-docs/`) and other hidden config dirs (`.github/`) — are expected at root and don't count as orphans.

## Teaching example

The same business, organized two ways:

**Wrong — grouped by file type:**

```
my-business/
├── CLAUDE.md
├── templates/
│   ├── proposal-template.md
│   ├── invoice-template.md
│   └── campaign-brief.md
├── data/
│   ├── client-list.csv
│   └── pipeline.csv
├── docs/
│   ├── sales-process.md
│   ├── brand-guidelines.md
│   └── pricing.md
└── scripts/
    ├── generate-invoice.py
    └── send-proposal.py
```

Asked to "draft a proposal for Acme Corp," you have to hunt across `templates/`, `docs/`, `data/`, and `scripts/` and load it all to figure out what's relevant. No domain boundaries. No place to put domain context that auto-loads when you open a sales file.

**Right — grouped by domain:**

Note: not every folder needs a `CLAUDE.md` — only the ones with implicit context that names can't carry (see Principle 8). Folders whose shape and names speak for themselves get none.

```
my-business/
├── CLAUDE.md                  ← what this repo is, how domains connect; rule: ask + add to agent-docs/glossary.md
├── agent-docs/
│   └── glossary.md            ← user-specific vocab, grows over time, read lazily
├── sales/
│   ├── CLAUDE.md              ← pricing rules, pipeline stages (domain rules Claude can't infer)
│   ├── templates/
│   ├── pipeline.csv
│   └── scripts/
├── clients/                   ← no CLAUDE.md: every client folder mirrors the same shape, Glob discovers it
│   ├── acme-corp/
│   │   ├── CLAUDE.md          ← per-client engagement context, contacts (varies per instance)
│   │   ├── profile.md
│   │   ├── contacts.md
│   │   └── updates.md
│   └── beta-inc/
│       ├── CLAUDE.md
│       ├── profile.md
│       ├── contacts.md
│       └── updates.md
├── operations/                ← no CLAUDE.md: `sops/` and `templates/` are self-explanatory
│   ├── sops/
│   └── templates/
└── marketing/
    ├── CLAUDE.md              ← brand voice (behavioral rule that applies to every file written here)
    ├── brand-voice.md
    └── templates/
```

Same task: read root `CLAUDE.md` → `sales/CLAUDE.md` → `clients/acme-corp/CLAUDE.md`. You never touch `operations/` or `marketing/`. Each domain `CLAUDE.md` auto-loads when you open files in its subtree, so domain rules ride along with the work — and folders without one stay out of the way.

## Workflow

1. **Map the repo.**
   ```bash
   ls
   find . -type d -maxdepth 3 -not -path '*/.*' -not -path '*/node_modules/*'
   ```
   Then `Glob **/CLAUDE.md` and `Read` the root `CLAUDE.md`.

2. **Clarify before auditing — one question at a time.** After mapping, you'll have inferences but also gaps. Fill them through `AskUserQuestion`. Ask **one** question, propose a recommended answer with a one-line reason, wait for the response before asking the next. Each answer informs the next question — never batch. The user is non-technical; foreign-looking folder names may be meaningful domain terms to them, and only they can tell you which.

   Common questions to walk in this order (skip any that are already obvious from the repo):
   1. **Domain confirmation** — "I see [list]. Are these your main business areas?" Recommend the inferred list with a one-line reason; let user correct, add, or merge.
   2. **Ambiguous folders** — for any folder whose purpose isn't clear from the name, ask what lives in it and whether it belongs inside one of the confirmed domains.
   3. **Sibling-shape intent** — when sibling folders look inconsistent (e.g. some clients have `profile.md`, others don't), ask whether they should mirror each other or whether the variation is intentional.
   4. **`CLAUDE.md` necessity** — for any subdirectory `CLAUDE.md` that just restates what names already say, ask whether there's implicit context worth keeping or whether it can be removed.
   5. **Glossary check** — list any terms you spotted in the repo or in the user's recent prompts that look user-specific and aren't in `agent-docs/glossary.md`. Ask: "Are these worth adding so a future session can look them up when they appear?" Recommend adding the obvious ones; let user accept, edit, or skip.

   Stop asking once you have what you need to audit confidently. Don't over-interview.

3. **Audit against the principles.** Walk the checklist. Note what's working and what isn't. Flag specifically:
   - Folders grouped by file type (templates/, docs/, data/, scripts/ at root)
   - Names with spaces, capitals, or that don't describe content
   - Sibling folders with inconsistent shapes
   - Subdirectory `CLAUDE.md` files that don't meet any of Principle 8's four conditions (dead weight — restates what names already say)
   - Domain folders missing a `CLAUDE.md` where Principle 8's conditions clearly apply (e.g. behavioral rules like brand voice, per-instance context that varies)
   - Missing `agent-docs/glossary.md`, or root `CLAUDE.md` doesn't include the "ask + add to glossary" rule
   - Loose business content at the root (not config/metadata files like `.gitignore`, `package.json`, etc.)
   - Generic nesting more than 3 levels deep

4. **Produce the report** (template below). Include a proposed before/after tree and a plain-English list of changes — no shell commands, the user is non-technical.

5. **Wait for explicit user confirmation before any file moves.** Even if the user invoked the skill, do not move files until they approve the specific plan. Then execute the moves yourself (you know the commands) and re-run step 1 to confirm.

## Output template

```
## Structure Audit

### What's working
- [Concrete patterns to keep]

### Issues
**Critical** (blocks navigation):
- [Issue] — at `path/` — [what to do]

**Warning** (slows navigation):
- [Issue] — at `path/` — [what to do]

**Suggestion** (polish):
- [Issue] — at `path/` — [what to do]

### Proposed structure

Before:
[ASCII tree of current shape]

After:
[ASCII tree of proposed shape]

### Changes I'll make
1. Rename `clients/Acme Corp` → `clients/acme-corp` (lowercase, no spaces — so my Glob/Grep tools can find it)
2. Move `templates/proposal-template.md` into `sales/templates/` (group by domain, not file type)
3. Remove `operations/CLAUDE.md` — its content just restates what the folder names already say

Confirm to execute? (yes / skip specific numbers / edit)
```

## When everything is good

If the audit finds no issues, say so plainly:

```
## Structure Audit

Your repo is agent-navigable.

- Domains are clear: [list inferred domains]
- Names are self-describing and lowercase kebab-case
- Sibling folders mirror each other's shape
- CLAUDE.md placement matches where implicit context exists
- `agent-docs/glossary.md` exists and `CLAUDE.md` includes the ask-and-add rule
- Nesting stays within 3 levels

No changes needed.
```
