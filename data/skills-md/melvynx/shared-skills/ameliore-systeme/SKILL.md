---
name: ameliore-systeme
description: >-
  Makes Claude Code improve itself from your own history. Reads every Claude
  Code session of the last days saved on your computer
  (~/.claude/projects/**/*.jsonl), then reports what Claude keeps getting
  wrong, the corrections you repeat, the skills you should create and the
  tasks you redo every day that could be automated, and writes the skill or
  automation you pick. Use when the user types /ameliore-systeme, asks
  "qu'est-ce que je fais mal", "quels skills je devrais créer", or wants
  Claude to learn from past sessions.
argument-hint: "[jours, 7 par défaut]"
disable-model-invocation: true
---

# ameliore-systeme

Every Claude Code conversation is saved on the user's computer, one `.jsonl` file per session in
`~/.claude/projects/<folder>/`. That history shows what Claude got wrong, what the user had to say
twice and the work they redo every day. This skill reads it and turns it into fixes.

What the user typed after `/ameliore-systeme`: `$ARGUMENTS` (a number = how many days to read, default 7).

Answer in the language the user writes in (French by default).

## 1. Read the history

Run the digest script of this skill folder. It only reads, and writes one Markdown file:

```bash
node <this skill folder>/scripts/digest.mjs --days <N> --out /tmp/ameliore-digest.md
```

Then read `/tmp/ameliore-digest.md` in full. Each session has its folder, its date, its title, the
slash commands used, the tool errors and every message the user typed. Never open the raw `.jsonl`
files one by one: they hold the whole conversation and fill the context. Open one only to check a
precise point, with `grep`.

If the digest is cut (`tronqué`), run it again with fewer days.

## 2. The report

Write the report in chat, with these 4 sections. Every point quotes the history: a date, a folder and
the user's own words. Never a generic tip that the history does not show.

1. **Ce que Claude fait mal**: the mistakes that come back (the user says « non », « pas ça »,
   « je t'ai déjà dit », redoes the same request, stops Claude). For each one: how many times, 2 quotes,
   and the fix: one rule to add to `CLAUDE.md` (written out, ready to paste).
2. **Ce que tu répètes**: instructions the user gives in many sessions (a style, a tool, a check).
   Each one becomes a `CLAUDE.md` rule or a skill.
3. **Les skills à créer**: workflows of several steps done again and again. For each one: its name,
   what it would do in 3 lines, the sessions it comes from.
4. **Les tâches répétées à automatiser**: the tasks that come back every day or every week (same
   folder, same kind of request). For each one: the dates and folders where it appears, the time it
   takes today (number of messages and tools in those sessions) and the automation that would do it:
   a skill, a script, a scheduled task or a hook.

End with the top 3 changes, ranked by time saved, and ask which one to build.

## 3. Build what the user picks

- A `CLAUDE.md` rule: show the exact lines, then add them to `~/.claude/CLAUDE.md` (every project) or
  the project's `CLAUDE.md` (one project) on the user's yes. Never remove a line already there.
- A skill: write `~/.claude/skills/<name>/SKILL.md` (frontmatter `name` and `description` with the
  phrases that should trigger it, then the steps taken from the sessions). Show it before saving.
  Tell the user to type `/<name>` to use it.
- An automation: write the script or the scheduled task, run it once, show the result.

Never delete or edit a session file. Never send the history anywhere: everything stays on the computer.

## Notes

- Run it once or twice a week: each report only reads the days asked.
- The digest keeps only what the user typed, not Claude's answers, so it stays small. Tool errors are
  counted per session, which shows where Claude struggled.
