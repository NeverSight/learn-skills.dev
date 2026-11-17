---
name: dayz-lookup
description: Answer a question about the DayZ engine or Enforce Script API from source — a class, method, widget property, event, callback, config class, or engine behaviour. Reports what each source contributed, with file paths.
when_to_use: Before writing code against an unfamiliar DayZ symbol, and whenever an answer about engine behaviour has to be verified rather than recalled.
context: fork
background: false
allowed-tools: Read, Grep, Glob
---

# DayZ lookup

Answer from **ground truth**, never from recall. Three sources, searched in order, each one narrowing the next.

## 1. Project docs — `.claude/references/`

Skip this stage if the directory does not exist.

Read `.claude/references/INDEX.md`, then grep it for the queried symbols. This is where a project documents its own APIs, custom widgets, and internal classes — symbols no vanilla source knows about. Carry forward the symbols that still need vanilla coverage.

## 2. Plugin reference — `references/` (beside this file)

Start at `references/INDEX.md` and follow the nested `INDEX.md` files down: `DayZ/Configs/` for config classes, `DayZ/Scripts/ai/` for creature and AI systems, `DayZ/Scripts/api/1_Core` … `5_Mission` for the scripting API by layer.

Grep the narrowed subdirectory for the symbols, read what matches, and form a preliminary answer. Name the specific classes, methods, and properties in it that stage 3 has to verify.

## 3. Vanilla scripts — the `P:` drive

DayZ ships its scripts unpacked so modders can read them; this is their intended use. They are the ground truth, and the docs above are derived material that can be stale.

| Path | Holds |
|------|-------|
| `P:/scripts/1_core/proto/enwidgets.c` | widget class hierarchy, proto native widget methods, `WidgetFlags`, `ScriptedWidgetEventHandler` |
| `P:/scripts/1_core/proto/` | other proto declarations — entities, math, containers |
| `P:/scripts/3_game/gameplay.c` | `Mission`, `Hud`, and the widget classes declared in script |
| `P:/scripts/3_game/tools/uimanager.c`, `uiscriptedmenu.c` | UI runtime and menu lifecycle |
| `P:/scripts/3_game/constants.c` | `MENU_*`, `IDC_*` |
| `P:/scripts/3_game/tools/tools.c` | `CALL_CATEGORY_*` |
| `P:/scripts/2_gamelib/`, `4_world/`, `5_mission/` | the rest of the engine and game scripts |
| `P:/gui/layouts/`, `looknfeel/`, `imagesets/`, `fonts/` | vanilla UI assets — property names, slot names, file conventions |

Some extractors put each module's files one folder deeper (`P:/scripts/1_core/DayZ/proto/enwidgets.c`); when a path above misses, glob for the file name under `P:/scripts/`.

Search for the named symbols from stage 2, not for the topic. Verify, supplement, or correct the preliminary answer.

If the `P:` drive is absent, say so in Caveats and answer from stages 1 and 2 — a documented answer flagged as unverified beats a guess.

## Budget

**Five files read in total, across all three stages.** A precise answer from two files beats a vague one from fifteen. Stop as soon as the question is answered; the budget is a ceiling, not a target.

## Precedence

Vanilla scripts beat project docs, which beat the plugin reference. Where two sources disagree about the same symbol, take the higher one and put the disagreement in Caveats — a stale doc is a finding the caller needs.

## Report

- **Answer** — the response to the question, in your own words.
- **Sources** — one line per file actually used, tagged `project` / `plugin` / `vanilla`, saying what it contributed. Paths must be exact, so the caller can check without redoing the search.
- **Confidence** — high, medium, or low. Mark anything inferred rather than read.
- **Caveats** — version-specific behaviour, edge cases, and any source disagreement.

Report what the API **is**; the caller writes the code. Where a symbol cannot be found, say it was not found — that is an answer, and a plausible invention is not.
