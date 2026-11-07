---
name: aiediting
description: Workshop that builds your own video-editing skills. Interviews you about a format (stream, lesson, vertical or your own), looks at frames of your footage, assembles a design system with you, edits a trial clip until you say yes, and installs a self-contained format skill that edits every next video the same way. Or, if you say «без вопросов», takes one message and a recording and returns the finished video and the installed skill. Also refines a format skill you already have. Starts only on /aiediting.
disable-model-invocation: true
argument-hint: "[new|refine] format name or path to a source video"
metadata:
  version: "0.1.0"
---

# AIEditing

AIEditing is a **workshop**. It exists to create a format skill — `монтаж-<the person's word>` — or to
refine one that exists. It interviews the person, looks at frames of their own footage, builds a design
system with them, edits **one trial piece** of their source to show, reworks it until they say «да», and
then builds and installs the format skill globally. From then on the format skill does the editing; the
workshop is not needed again until something should change. A person who asks for no questions gets all
of this from one message: the finished video first, the skill installed with it.

**What the workshop never does** — in every phase, whatever is asked: it never publishes, uploads or
sends anything, never voices, never generates video, music or images. Its only edit is the trial piece,
shown on the dashboard and kept in the workshop folder; without questions, the built skill edits the whole
recording into its issue folder instead. The same holds for every format skill it builds:
«смонтируй <путь>» → a folder with the video, `.srt` and a short report. Nothing else.

## Reading this skill

This file is the order and the rules that never lose. Each phase's rules are in its own file, **read
when that phase starts and not before** — one at a time; a file opened early stays in the context for
the rest of the session.

| Stage id | Read | Produces |
|---|---|---|
| `start` | `phases/start.md` | the dashboard open; «новый» or «доработка» chosen |
| `formats` | `phases/formats.md` | one draft profile per format, listed or the person's own |
| `sources` | `phases/sources.md` | 1–3 sources, their frames and layout on the dashboard |
| `interview` | `phases/interview.md` + `prompts/question-round.md` | the profile answered, round by round |
| `design` | `phases/design.md` | `design/` of the skill, chosen variants |
| `trial` | `phases/trial.md` | a trial clip the person said «да» to; every remark in the profile |
| `build` | `phases/build.md` | `монтаж-<слово>` built, its tools installed on «да», installed globally |
| — | `phases/refine.md` — instead of formats and sources, when refining | |
| — | `phases/resume.md` — instead of start, when `.aiediting-work/state.js` is unfinished | |
| — | `phases/no-questions.md` — instead of all of them, when the person asked not to be asked | a finished video and the skill installed |

**Their words choose the path.** The person asked not to be asked (the signal is at the top of that file)
→ `phases/start.md`, §1, then `phases/no-questions.md`, in place of every phase but the ones it names.
Everything below that says «asked» or «да» reads there as that phase says; the limits on publishing,
generating, paying and keys do not move.

After a compaction re-read `.aiediting-work/state.js`, the draft `profile.json` of the format in work,
and the file of the current phase. Nothing else. With `noQuestions` in `state.js` that is
`phases/no-questions.md`, its `решения.md`, and the method of the step you are in.

## The words the person sees

Instructions here are English; the person is spoken to **in their language** — Russian unless they write
in another one. One word per stage, on the dashboard and in the chat: Старт · Форматы · Исходники ·
Интервью · Дизайн · Пробный монтаж · Сборка. The thing being made is «скилл формата» or «скилл
монтажа», named `монтаж-<слово>` with the person's own word.

## The tool

Every event is one call: `python "<skillDir>/tools/ae.py" <command>` — `init`, `no-questions`, `stage`, `ask`,
`answered`, `formats`, `profile`, `frames`, `layout`, `design-example`, `samples`, `choose`, `trial`,
`verdict`, `build-skill`, `install-skill`, `list-skills`, `backup-skill`, `restore-skill`, `doctor`,
`finish`. The command list with arguments is at the top of `tools/ae.py`. `phases/start.md` says how to
find `<skillDir>`. You never edit `state.js` or the dashboard by hand. Where there is no `python`, as on
many Macs, use `python3`; where it is the Microsoft Store stub on Windows, use `py -3`.

## Rules that never lose

1. **A key is never asked for, echoed or written.** Which recogniser, whether an account exists — yes.
   The key itself — never: the person puts it into their environment or `.env` by the variable name.
2. **A fact about the person is never invented** — the output folder, the brand glossary, the music
   library: asked, or left as a visible gap in the profile.
3. **Nothing is installed without «да».** `doctor --install <id> --yes` only after the person agreed to that
   tool, by its pin from `catalog/tools.json`. Only tools the interview chose; heavy ones (the whisper
   model) are offered with their size. Steps marked `not_built` in `catalog/steps.json` are not offered.
   Asking for no questions is that «да» for the chosen steps' tools, and each is named at the end.
4. **Examples are always on the person's own video.** No source of the needed kind → ask for one; without
   it the question is asked in words, without an example.
5. **Every remark on the format goes into the profile** (`ae.py profile taste`), and only AIEditing changes a profile —
   a format skill writes remarks into its report and suggests «запусти AIEditing — доработка».
6. **The previous version is kept.** Installing over a skill moves the old one to the reserve;
   `restore-skill` brings it back in one command.
7. **The format skill holds only what was chosen** — steps, tools and design; nothing «на всякий случай».

## Files

```
.aiediting-work/                 in the folder where the workshop was started
├── state.js  dashboard.html  index.html  serve.pid  serve.log
├── frames of the person's sources: `ae.py frames` prints their paths
└── монтаж-<слово>/
    ├── profile.json             the draft profile — data only, no keys
    ├── design/                  tokens, fonts, samples/ (chosen variants)
    ├── variants/<element>/      design variants shown side by side
    └── trials/01/ …             trial pieces, вопросы.json / ответы.json, out/
overlay-kit/                     in this skill: the method and tools of the `graphics` step, copied into formats that use it
~/.agents/skills/монтаж-<слово>/ the installed format skill; pointer in ~/.claude/skills/
~/.agents/skills/.aiediting-backups/  previous versions
```

## Updating AIEditing

Never mid-session. «Обнови AIEditing» → `npx skills update aiediting -g`, then a new session. Format
skills are separate folders with their own copy of the runtime: updating or removing AIEditing never
breaks them; a refinement rebuilds them on the new version.
