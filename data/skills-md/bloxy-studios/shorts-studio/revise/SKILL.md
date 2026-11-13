---
name: revise
description: >-
  Apply natural-language changes to an existing short as typed operations on a new EditPlan version — trims/extensions, keep both speakers visible, speaker switches, calmer motion, caption style/emphasis/zone/word corrections, music level, voice cleanup — with targeted cache invalidation, a readable diff, and re-render + QA.
when_to_use: >-
  "end two seconds later", "keep both people visible from 0:12 to 0:18", "less motion", "make captions cleaner", "it says Artemus, should be Artemis", "music quieter", "move the captions up there"
argument-hint: "<project> --clip <id> <what to change>"
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio *) Bash(shorts-studio *) Read
effort: medium
license: MIT
compatibility: >-
  Needs the Shorts Studio engine (Claude Code plugin bloxy-studios/shorts-studio, or a clone of that repo) with Bun, Node >= 22 and FFmpeg; `shorts-studio doctor --setup` installs the rest project-locally.
---

# Revise an edit

Rules: `${CLAUDE_PLUGIN_ROOT}/references/rules.md` · CLI (all ops): `${CLAUDE_PLUGIN_ROOT}/references/cli.md`.
`ss` = `"${CLAUDE_PLUGIN_ROOT}/bin/shorts-studio"`. Input: `$ARGUMENTS`

## 0. Engine check

The commands below run the Shorts Studio engine. Installed as the Claude Code plugin it is already
present and `shorts-studio` is on the Bash PATH. If `shorts-studio doctor` is not found (for example,
this skill was added with `npx skills add`), ask the user before installing anything, then:
- Claude Code: `/plugin marketplace add bloxy-studios/shorts-studio` → `/plugin install shorts-studio@shorts-studio`.
- Other agents: `git clone --depth 1 https://github.com/bloxy-studios/shorts-studio ~/.shorts-studio/engine`
  and read every `${CLAUDE_PLUGIN_ROOT}` path below as `~/.shorts-studio/engine`.

Then run `shorts-studio doctor --setup` once (project-local runtime; never sudo or global installs).

## Steps

1. Map the request to ops (state the timebase: output time unless the user quotes source time):
   | Request | Op |
   | --- | --- |
   | end later/earlier, start earlier/later | `extend-end` / `trim-end` / `extend-start` / `trim-start` (`ms`) |
   | keep both people visible | `keep-both-visible` (`from`, `to`) |
   | switch to the other speaker here | `switch-speaker` (`at`) |
   | less motion / calmer | `reduce-motion` |
   | cleaner / different caption look | `caption-style` (`styleId`) — preview first if unsure (`preview` skill) |
   | highlight these words / fewer highlights | `caption-emphasis` (`keywords`, `onlyKeywords`, `mode`) |
   | wrong word in captions | `caption-correct` (`from`, `to`, `at`) — timing unchanged, correction recorded |
   | move captions | `caption-zone` (`from`, `to`, `y0`, `y1`, `reason`) |
   | music quieter/louder | `music-gain` (`db`) — voice untouched |
   | voice cleanup | `voice-chain` (`denoise`, `deess`, `compress`, `highpassHz`) |
   Luxury graphics changes are brief edits instead: update `luxury/graphics.json`, then `ss luxury plan`.
2. `ss revise <project> --clip <id> --reason "<user's words>" --op '{…}' [--op …]` → new plan version,
   diff, invalidated stages (unchanged stages reuse caches).
3. `ss render <project> --clip <id>` → QA. Inspect the changed region on real frames (`qa/cuts.jpg`, or extract frames).
4. The approved render is never overwritten (`approve` marks finals).

## Errors and limits

- Extending past the source, trimming the whole segment, or a word not in the captions → the op fails with the reason; ask/adjust.
- `keep-both-visible` needs two faces in the range (else say so and offer a stack/wide layout).

## Example

"Keep both of them visible from 1.3 to 4.3 and make the music 2 dB quieter" →
`ss revise p --clip clip-01 --reason "…" --op '{"op":"keep-both-visible","from":"0:01.3","to":"0:04.3"}' --op '{"op":"music-gain","db":-2}'` → `ss render p --clip clip-01`.

## Completion check

A new plan version exists with the user's reason in its changes; the re-render's QA has no new hard
failure; you looked at frames in the changed range and reported what changed (and what did not).
