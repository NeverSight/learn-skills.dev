---
name: open-skill-learn
description: Saves what the user teaches - a lesson, preference, convention, glossary term or project fact - as a note in their local knowledge, scoped to a role, project or skill, so future work and routing use it; also forgets notes, exports them, and handles starter-knowledge updates after a release. Use when the user says "remember", "from now on", "note that", "always", "never again", "don't do X again", "forget", "ghi nhớ", "bài học", "từ giờ", when they correct how you worked, when an incident teaches something, or when they ask to export notes or review seed updates.
---

# Open Skill Learn

A correction the user makes once should not have to be made again next week. This skill keeps such lessons as small local files that `open-skill route` attaches to future chains.

`open-skill` means the CLI; if it is not on PATH use `uvx --from git+https://github.com/VoKhoiNhon/open-skill-standard@v0.6.0 open-skill`.

## Save

One fact per note, written so it still makes sense months later. Record corrections and approaches the user confirmed, with the reason when it matters.

```bash
open-skill learn "<one fact>" --applies-to <scopes> --type lesson|preference|pitfall|glossary|project-fact
```

Scopes tell the router when the note applies; combine as needed, comma separated:
`skill:<id>` (for example `skill:bmad-method/bmad-build`), `role:<role-id>`, `project:<absolute path>`, `phase:<phase>`, or `role:*` for everything.

Saving the same text again updates the existing note instead of duplicating it. Don't save what the repository or chat history already records; a copy goes stale when the source changes. The CLI refuses text that looks like a secret, token, email or phone number; keep credentials and personal data out of notes entirely.

## Forget, review, move

- `ls ~/.open-skill/knowledge/` lists notes; each is a plain Markdown file the user can edit.
- `open-skill forget <note-id>` deletes one; delete notes that turned out to be wrong.
- `open-skill export <file.zip>` copies profile and notes to another machine (usage history stays local).
- `open-skill scan --memory` imports Claude Code memory files as notes, read-only.

## After an update

Updating skills or the CLI never changes the notes folder. When the CLI reports that it upgraded the user's data, or `open-skill status` lists seed updates to review, tell the user in one line and offer:

- `open-skill upgrade --dry-run`, then `open-skill upgrade` — back up, migrate, sync starter knowledge.
- `open-skill seeds diff` — upstream rewrote a seed the user had edited; `seeds accept <id>` takes upstream's wording (after a backup), `seeds keep <id>` keeps theirs.
- `open-skill upgrade --rollback` — undo the last upgrade.

Let the user decide on seed updates; their edited wording is theirs.

## First use

If `~/.open-skill/profile.yaml` does not exist, suggest `open-skill init --role <role>[=weight]`; it saves the user's roles and seeds starter notes for them.
