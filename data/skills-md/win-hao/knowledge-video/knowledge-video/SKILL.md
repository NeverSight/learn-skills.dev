---
name: knowledge-video
description: "Turn one topic into a knowledge explainer video that is easy to follow, good to look at and makes people want to watch to the end (on-screen text over music, the kind that took off under Douyin's #Vibe知识大赏), rendered with HyperFrames. Gives a path that works (research → copy → images → look and storyboard → render) and small tools for music editing, beat timing, sound effects and self-checks; the design is yours to make for each topic. Use it whenever someone wants a knowledge, science, history or how-it-works video — 'make a video explaining X', 'turn the history of X into a short video', 'explainer video', '做一条知识视频', '科普视频', 'Vibe知识大赏' — even if they don't name this skill. For a single short animation or just a new look, use code-video instead."
---

# Knowledge video

Turn one topic into a knowledge video people want to watch to the end. What follows is a path that works, not a fixed procedure: merge, skip or reorder steps, and design the writing, the look and the motion for this topic yourself.

Talk to the user in their language; file names below are defaults.

## The rough path

1. **Research** → `article.md`: find sources and write a sourced article. First see what shape the topic has (timeline, chain of causes, concept, comparison, myths, one story), then decide which points to cover. The user decides how many: offer two or three options by the music's length and recommend one
2. **Copy** → `script.md`: rewrite the article as a video people scroll to
3. **Images** → `images.md` or `image-prompts.md`: real images, or prompts for AI illustrations (assume you can't call an image API; the user runs their own tool)
4. **Look and storyboard** → `looks/`, `storyboard.md`: show the user a few directions, then storyboard to the music
5. **Render** → `opening-preview.mp4` → `final.mp4`: a short opening first, the full video once it's right

By default, show the user each step's result before moving on: a wrong direction is most expensive after rendering. If they say "go all the way", keep going and note what you chose and why in `storyboard.md`.

## Each step: fill in a prompt, then follow it

Per Anthropic's [prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), keep background, requirements and checks in separate XML tags, with a reason for each line: separated parts don't blur together, and knowing why lets the model generalize to what isn't written. You fill the tags yourself, from this topic and what the user has said.

- **Brief** `prompts/brief.md`: filled once at the start, updated after each step. Just one `<context>`: the topic, the audience, the takeaway, length, orientation, music, what the user likes and dislikes, what earlier steps settled, where the files are
- **This step's prompt** `prompts/<step>.md`, four tags:
  - `<role>`: which role does this step and what that role cares about most. Roles differ by step; pick one for this step, e.g. research is a knowledge editor (cares most about sources), copy is a screenwriter (cares most about whether viewers swipe away), images is a picture editor or illustrator, the look is an art director, the storyboard is a storyboard artist, the composition is a motion designer (cares most about what each movement explains)
  - `<task>`: what this step produces and where it goes
  - `<style>`: recommended approaches, each with a reason; **recommendations, not rules**: pick from the examples in `references/` or design something new for this topic; follow the user where they've said what they want, and note what they don't want here too
  - `<check>`: what to verify, item by item, before the step counts as done; include the "Must hold" items

  Write `<role>`, `<task>` and `<check>` every step; leave out `<style>` where it isn't needed (research and rendering usually). Infer what the user hasn't said from the topic, and ask about what you're unsure of in the report. Show the filled prompt with the step's output; if the user edits it, redo the step from the edited version

**Who follows it**: steps that need back-and-forth with the user (how many points, which look) you do yourself. Large self-contained steps (research, finding images or writing image prompts, writing the composition and rendering) go to a subagent: give it only the brief, this step's prompt and the file paths, so its context is clean and holds only what this step needs. It doesn't know what you and the user discussed, so both must be complete. When it's done, read its output and run the self-check before showing the user. Without subagents, follow the prompt yourself.

## Must hold

- **Facts are sourced**: every year, name, number and quote traces to a reliable source (papers, institutions, archives, the person's own words), linked in `article.md`; drop what you can't source, label estimates, say whose account a second-hand claim is. Every line on screen, including the opening question and the ending, matches `article.md`
- **Assets are usable**: images, music, sound effects and fonts are licensed for this (check the file page); credits go in `credits.md`
- **No AI-drawn faces of real people**; if the video uses AI illustrations, turn on the platform's "AI-generated content" label
- **The picture depends only on time**: seed any randomness so a frame renders the same every time (HyperFrames needs this)
- Before delivering, watch the whole thing yourself: text visible, readable in time and understandable (no skipped steps in the reasoning; any suspense pays off later), years and numbers match the article, sound and picture in sync

## Tools at hand

HyperFrames for the picture (`npx hyperframes init / docs / check / snapshot / render`); if its skills are installed, follow them for compositions. Small tools in `scripts/`, use them or not:

| Script | What it does |
|---|---|
| `beats.py` | tempo, beats, bar lines and per-bar loudness changes of the music |
| `music_loops.py`, `cut_music.py` | find bars that repeat or cut seamlessly, build the new music from a bar list |
| `timing.py` | lay each screen of the copy onto the beat grid, pin key screens to given bars |
| `sfx.py` | download Kenney's CC0 foley, mix sound-effect cues into one track |
| `qa.py` | contact sheets of every screen and frames around key beats |

## What earlier videos left behind

References, not rules. Design for this topic first; look here when unsure or when you hit the same problem:

- `references/example-ai-history.md`: the first tested run, each step's output and timing
- `references/example-fish-and-bears-paw.md`: the night-sky particle look of *Information Theory*, revised three times (motion too flat → copy hard to follow)
- `references/prompt-examples.md`: two filled prompts from a tested video, to see how detailed they get
- `references/notes.md`: observations on copy and pacing, including how to make a chain of reasoning land
- `references/images.md`: checking licenses, writing prompts, generating in layers
- `references/visuals.md`: dense collage, night-sky particles, timeline moments, photo cards, fitting UI onto generated screens, what to draw in code
- `references/sound.md`: music edits, sound effects, loudness
- `references/pitfalls.md`: check first when a render fails or the picture is off
