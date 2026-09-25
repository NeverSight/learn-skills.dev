---
name: scenario-storyboards
description: "Use when a story must unfold across a sequence of Scenario images: a comic page or strip, manga or webtoon panels, a children's storybook, a film, game, or ad storyboard, animatic pre-viz frames, or any shot list where the same characters and world must persist from panel to panel and dialogue must stay legible. Keywords: storyboard, comic, panel, sequential art, storybook, shot list, pre-viz, animatic, scene to scene, character consistency."
license: MIT
---

# Scenario Storyboards and Comics

## Overview

Asked for a comic page, an agent prompts one model for "a page with six panels" and gets a page it cannot fix: uneven panel geometry, a hero whose face changes between cells, dialogue rendered as garble. The unit of generation is the panel, never the page. Script first, lock the cast, one `model_run` per panel anchored to the same references, letter in post, assemble the page last. Connection and the core loop: see the `scenario` skill. Character lock: `scenario-consistency`. Per-model image contracts: `scenario-image`. Lettering: `scenario-text-overlay`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Stage             | Do                                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Script         | A beat table before any generation: per panel, the shot size and angle, the action, the setting, the dialogue                               |
| 2. Cast and style | One approved hero image per character plus a style pick (`search` with `query="comic"` surfaces style LoRAs); write each baseline           |
| 3. Panels         | One `model_run` per panel: byte-identical baselines plus that panel's clause, references wired per the schema                               |
| 4. Review         | `jobs_wait`, then check identity panel over panel before lettering                                                                          |
| 5. Letter         | Dialogue, captions, and sound effects as `scenario-text-overlay` cards composited onto text-free art                                        |
| 6. Assemble       | Page layout and contact sheets: layer composition in `scenario-video-assembly` (Image Studio), or the grid tool in `scenario-image-editing` |

Label the panels the way a shot list does, in that order: number, shot size, angle, lens or camera move, then the action with each character's frame side and facing. Arrange them as coverage rather than a row of pictures: open on a master that establishes the geography, hold one side of the axis so screen direction never flips, climb the size ladder as tension rises, and punctuate with an insert or a reaction.

A storyboard headed for animation stops at stage 4. Approved panels become first frames for image-to-video (`scenario-video`), one clip per shot, when each shot stands on its own. When the movement itself has to carry across the cuts, animating panels independently resets the performance at every one: that sequence belongs in the `scenario-seedance-storyboard` skill, which chains each shot's exit pose to the next shot's entry.

## Worked example: a six-panel comic page

1. Script the page as a table: panel, shot size and angle, lens or camera move, action, dialogue and captions. The action column holds only what a camera sees: a thought, a smell, or backstory renders as nothing, so it becomes visible evidence or a caption. Dialogue and captions are written down here, never prompted into the art.
2. Cast lock: generate or upload the hero and iterate until approved; unattended, the script's own character description stands in for the approval, so take the candidate that matches it and continue. `asset_display` the hero and write its baseline enumeration (geometry, costume, palette by name or hex) per `scenario-consistency`.
3. Style: `search` with `target="models"`, `query="comic"`, `public=true`; the public catalog carried comic-style LoRA hits at authoring time. Confirm the pick with the user (unattended, take it from the task instructions, else the first result in returned order), then `model_schema_get` it for the reference field's name, cap, and cardinality. No reference field that fits the cast? Capabilities may advertise adapters the schema never exposes; the schema wins. Keep the pick for hero generation and `recommend` a reference-capable model for the panels, restating the style line in every prompt.
4. Six `model_run` calls. Each prompt is the style line, the character baseline, and the setting line (location, time of day), all byte-identical across the panels that share them, plus that panel's clause (shot, action), plus "clean art, no lettering, no speech bubbles". A dropped setting line breaks continuity the same way a dropped baseline breaks identity. Wire the hero reference as the schema says: an array only under `array: true`. A batch-count field repeats one prompt, so it cannot carry per-panel clauses.
5. `jobs_wait` on the six jobs, re-calling with `pending_job_ids`. Review each panel against the hero; fix drift by tightening that panel's enumeration and re-running from the baseline, never by chaining from a neighboring panel.
6. Letter with `scenario-text-overlay`, composite the cards as layers, assemble the page, then file panels and page in a collection (`scenario-asset-analysis`).

## Common mistakes

- Generating a page in one run: panels from a single prompt cannot be regenerated one at a time, so one bad panel costs the whole page.
- Prompting dialogue: generated lettering drifts and garbles; keep the art text-free and letter in post.
- Chaining panel to panel: feeding panel three panel two's output compounds drift; anchor every panel to the same approved hero.
- Writing "same character as before": there is no memory between calls; restate the full baseline every time.
- Carrying a lasting change (a new costume from panel four on) as a per-panel clause against the old hero: the reference pulls the old costume back. Generate a second hero from the first with the change described, approve it, rewrite the baseline, and anchor the later panels to it.
- Animating unapproved panels: image money is cheap, video money is not; gate the expensive stage the way `scenario-video-ads` prices its board first.
- Merged characters: with several heroes in one panel, state each reference's role in the prompt, check the schema's reference cap fits the cast before planning the scene, and keep extras generic and unnamed; only cast that must stay recognizable gets a baseline and a slot.
- Abandoning a moderation-blocked action beat: providers can reject a weapon or fight panel (`moderation_blocked`); soften that panel's clause, de-emphasizing the weapon, and re-run from the baseline.
