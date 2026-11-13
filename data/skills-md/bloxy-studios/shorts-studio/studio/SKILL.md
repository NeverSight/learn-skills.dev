---
name: studio
description: >-
  Shorts Studio router. Turns a YouTube link, a local recording, or an existing Shorts Studio project into the right editing workflow (clip a long video into shorts, finish a talking-head creator edit, apply the Luxury Tech preset, revise or export an edit, design a style). Use whenever the user wants vertical short-form video (Shorts, Reels, TikTok) made from footage, or mentions Shorts Studio.
when_to_use: >-
  "make shorts from this video", "clip this podcast", "turn my recording into a reel", "edit my camera + mic takes", "change the captions on my short", "export my clips", "what's the status of my shorts project".
argument-hint: "[youtube-url | file | folder | project] [what you want]"
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio *) Bash(shorts-studio *) Read
license: MIT
compatibility: >-
  Needs the Shorts Studio engine (Claude Code plugin bloxy-studios/shorts-studio, or a clone of that repo) with Bun, Node >= 22 and FFmpeg; `shorts-studio doctor --setup` installs the rest project-locally.
---

# Shorts Studio — router

Follow `${CLAUDE_PLUGIN_ROOT}/references/rules.md` (modes, questions, honesty, data handling).
CLI: `"${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio"`.

## 0. Engine check

The commands below run the Shorts Studio engine. Installed as the Claude Code plugin it is already
present and `shorts-studio` is on the Bash PATH. If `shorts-studio doctor` is not found (for example,
this skill was added with `npx skills add`), ask the user before installing anything, then:
- Claude Code: `/plugin marketplace add bloxy-studios/shorts-studio` → `/plugin install shorts-studio@shorts-studio`.
- Other agents: `git clone --depth 1 https://github.com/bloxy-studios/shorts-studio ~/.shorts-studio/engine`
  and read every `${CLAUDE_PLUGIN_ROOT}` path below as `~/.shorts-studio/engine`.

Then run `shorts-studio doctor --setup` once (project-local runtime; never sudo or global installs).

## 1. Resolve intent

| The user has… | …and wants | Skill |
| --- | --- | --- |
| a YouTube URL, long recording, podcast, folder of media | several short clips | `/shorts-studio:clip` |
| raw camera file(s) + a clean mic WAV of their own takes | one finished short | `/shorts-studio:creator-edit` |
| any source + "Luxury Tech" / white cards / premium style | the Luxury Tech look | `/shorts-studio:luxury-tech` |
| an existing project + a change ("give the punchline another half second") | a revision | `/shorts-studio:revise` |
| an existing project + "export / upload / deliver" | delivery packages | `/shorts-studio:export` |
| a style reference / brand rules | a reusable preset | `/shorts-studio:design` or `/shorts-studio:style-learning` |
| specific media + specific edits (trim, assemble, music) | a general edit | `/shorts-studio:edit` |
| an edit + caption wishes (style, highlights, wrong word, subtitles) | caption work | `/shorts-studio:captions` |
| an edit + framing complaints (wrong person, both in frame, too much motion) | reframing | `/shorts-studio:reframe` |
| an edit + sound wishes (music level, voice cleanup, SFX, stems) | audio work | `/shorts-studio:audio` |
| a Luxury/graphics edit + "change/add a visual" | graphics | `/shorts-studio:graphics` |
| "show me options first" | previews | `/shorts-studio:preview` |
| a rendered edit + "fix the issues / keep improving it" | brief refinement + bounded repair | directing loop in `references/rules.md` (`shorts-studio repair`) |
| setup problems | diagnosis | `/shorts-studio:doctor` |

If the request is ambiguous between two rows, ask one AskUserQuestion with those options.

## 2. Check state before acting

```bash
"${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio" doctor            # once per session if unsure
"${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio" project list
"${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio" project show <project> --json   # decisions already made
```

Reuse an existing project when the user refers to it; never re-ask decisions stored in
`project.json` (`decisions`). Infer the mode: explicit "do everything yourself" → autonomous;
"show me first" → director; otherwise guided.

## 3. Hand off

Invoke the chosen skill with the user's arguments. Stay in the main conversation for all
questions; worker agents return uncertainties to you.

## Completion check

You named the workflow you are running, its project directory, and the mode, and the
downstream skill's own completion check passed (or you reported what blocked it).

## Example

User: "Make three shorts from https://youtu.be/VIDEO_ID, clean podcast style."
→ intent = clip, preset = clean-podcast, count = 3, mode = guided → run `/shorts-studio:clip`.
