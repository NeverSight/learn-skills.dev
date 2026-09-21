---
name: layer-audio
description: "Use when generating audio with Layer: sound effects for a game or trailer, music and background tracks, or speech and voice-over from text. Also when a sound effect comes back with unwanted ambience or reverb, when a music prompt needs structure or length control, or when choosing a voice and delivery for narration. Keywords: SFX, sound effect, foley, UI sound, music, soundtrack, loop, text to speech, TTS, voice over, narration."
license: MIT
---

# Layer Audio Generation

## Overview

Three distinct use cases with almost nothing in common: `sound_effects`, `music`, and
`text_to_speech`. Pick one, then write the prompt the way that discipline expects. The loop and the
spend gate are in the `layer` skill.

If a sibling skill named here is missing from your available skills, ask the user to install it
(`npx skills add layerai/skills --skill <name>`); unattended, proceed from tool schemas and flag the
gap.

## Sound effects

Describe the physical event, not the feeling. What object, made of what, doing what, at what scale,
in what space. "Heavy oak door, iron hinges, swinging open slowly with a low groan, then a dull thud
against stone" is a sound. "Scary door sound" is a mood board.

Three things decide whether a game-ready effect is usable:

- **The space.** Generated effects arrive with room ambience baked in unless you exclude it. For an
  asset the engine will place in its own reverb, ask for it dry, close-mic'd, and isolated. A wet
  effect cannot be made dry afterwards.
- **The length.** UI sounds are short, and a model given no length target produces a tail that has to
  be trimmed. State it.
- **One event per generation.** A footstep, a sword unsheathe, and an impact are three assets. Asking
  for a sequence yields one file you then have to cut apart.

For UI sound sets, generate each state separately and name the shared character once in every prompt,
so the confirm, cancel, and hover sounds read as one family.

## Music

Name genre, instrumentation, tempo, mood, and **function**. Function is the one people leave out and
the one that matters most: a menu loop, a combat layer, a boss intro, and a credits piece are written
differently even in the same style.

Say what the track should not do. Background music for a game should not have an arresting melodic
hook competing with dialogue, and stating "sparse, no lead melody, sits under voice" gets there
faster than three rerolls.

Where a model exposes structured fields (`lyrics`, `instrumental`, `speed`), use them instead of
describing the same thing in prose. `get_base_model` is the authority on which apply. For anything
that must loop, keep the arrangement steady rather than building to a climax that cannot rejoin its
own start.

## Speech

Filter for `text_to_speech`. Send the script clean, with real punctuation, since models take commas
and full stops as pacing. Spell out anything ambiguous: a number, an acronym, or an invented fantasy
name will otherwise be read the model's way, and "Aelthyr" needs a phonetic respelling if it must be
said consistently across a cast.

Direct the delivery separately from the words: pace, energy, age, accent, emotional register. Keep
one voice per character and reuse the same voice selection across the project, since a voice that
drifts between lines is more noticeable than one that is merely wrong.

Generate long narration in paragraph-sized chunks rather than one call. A single bad word in a
four-minute take costs the whole take.

## Worked example

"We need a sword-unsheathe effect for the inventory screen."

1. `list_base_models` with `filter.use_case: "sound_effects"`. Take the first result, then
   `get_base_model` for its length and format fields.
2. Prompt the event: "Single steel longsword drawn from a leather scabbard, fast, bright metallic
   ring with a short decay. Dry, close-mic'd, isolated, no room reverb, no ambience, no music. Under
   one second."
3. `estimate_forge_price`, then execute with `batch_size` high enough to choose from, since audio
   runs are cheap and the take-to-take variation is large.
4. Poll at `poll_interval_seconds`, then audition the results before delivering rather than passing
   on the first file.

## Common mistakes

- Describing the emotion of a sound instead of the physical event.
- Accepting baked-in reverb on an asset the engine will place in its own space.
- Asking for a sequence of events in one generation, then cutting the file apart by hand.
- Leaving length unstated on a UI sound.
- Omitting the function of a music cue, so a background loop arrives with a lead melody.
- Sending an unpunctuated script, or an invented name with no phonetic spelling.
- Generating four minutes of narration in one call.
