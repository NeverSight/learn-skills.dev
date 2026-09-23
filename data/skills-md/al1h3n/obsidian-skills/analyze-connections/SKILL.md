---
name: analyze-connections
description: Find missing links between Obsidian notes and write linked copies to "AI System/" without touching originals. Scans a given folder path, turns plain-text mentions of other note titles/aliases into [[wikilinks]], adds a Related section for notes sharing tags. Use whenever user asks to link notes, find connections, build backlinks, connect or wire up a vault or folder, improve the graph, or when a loop maintains vault links, even if they never say "analyze".
---

# analyze-connections

Add missing `[[links]]` between notes. Originals stay untouched. Linked copies go to `AI System/`.

## Style

Drop: filler (just/really/basically/actually/simply), pleasantries (sure/certainly/of course/happy to), hedging. Fragments OK. Short synonyms (big not extensive, fix not "implement a solution for"). No tool-call narration, no decorative tables/emoji, no dumping long raw error logs unless asked quote shortest decisive line. Standard well-known tech acronyms OK (DB/API/HTTP); never invent new abbreviations (cfg/impl/req/res/fn) tokenizer split them same as full word: zero token saved, reader still decode. Full word cheaper AND clearer. No causal arrows (→) either own token, save nothing. Technical terms exact. Code blocks unchanged. Errors quoted exact.

## Hard rules

- Never edit, move, rename, delete existing vault files.
- Write only inside `<vault>/AI System/`. Create folder if missing. Files there are AI-owned, overwrite OK.
- Output mirrors original relative path: `Projects/x.md` becomes `AI System/Projects/x.md`.
- Write a copy only when it has at least one change. No identical copies.
- Skip `AI System/`, `.obsidian/`, `.trash/` everywhere.
- Wrong link costs more than missed link: user must review each. Unsure means skip.
- Loop run (no user to answer): never block. Path missing means stop and report.

## Inputs

- vault: absolute root path (has `.obsidian/`). Default: current dir if it has `.obsidian/`.
- path: folder to scan, relative to vault. Required. Missing and user present: ask. Missing and no user: stop, report `path missing`.
- since: only notes modified in last N days. Default: all notes in path.
- cap: max notes per run. Default 100, newest first. Report leftover count.

## Steps

1. Index whole vault, not just path (links may point outside scope):
   `find "$V" -type f -name '*.md' -not -path '*/.obsidian/*' -not -path '*/.trash/*' -not -path '*/AI System/*'`
   Title = filename without `.md`. Aliases = `aliases:` list in frontmatter. Read frontmatter only: `sed -n '2,/^---$/p' "$f"`.
   Map lowercase title/alias to note. Same key hits two notes: ambiguous, drop key.
   Drop keys shorter than 4 chars, generic words (index, notes, todo, inbox, home, readme, untitled, daily), date-only titles.
2. Candidates: for each key, `grep -rilw -- "key" "$V/<path>"` (skip AI System). Read only notes with hits. Do not read whole scope.
3. Per note, add inline links:
   - Match case-insensitive, whole word. Longest key first.
   - First mention only, per target, per note.
   - Skip: frontmatter, fenced code, inline code, existing `[[...]]` and `[...](...)`, URLs, heading lines, tags.
   - No self-link. Skip target already linked anywhere in note.
   - Matched text equals title: `[[Title]]`. Otherwise `[[Title|matched text]]`.
   - Max 10 new links per note.
4. Related section. Add target when note and target share 2 or more tags (frontmatter `tags` or inline `#tag`) and target not yet linked. Ignore tags on over 25% of notes.
   - Append under `## Related` at end. Section exists: add lines inside, no duplicates. Else create.
   - Format `- [[Target]]`. Max 5.
5. Write changed notes to `AI System/<relative path>`. Content byte-identical to original except inserted links. Keep line endings and frontmatter as is.
6. Report.

## Report

```
Changed N of M notes, +L links. Leftover: K.
Projects/x.md: +3
Ideas/y.md: +1
```

Max 10 file lines, then `+N more`. Nothing changed: `No missing links found in <path>.`
