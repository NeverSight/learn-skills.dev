---
name: tesseract-audio
description: Audio processing of all kinds - edit and mix multi-track recorded audio, compose & arrange music using DAW features (synthesizers, sequencers, drum kits, etc.), and even add spatial audio effects. Insert tracks, audio clips, MIDI clips and instruments, tempo, audio effects and automation, then measure the mix and render it to WAV. Use for songs, beats, sound design and music production; dialogue, podcast, sound-effect and video mixdowns; and binaural audio/spatial audio effects to match 3d placement.
---

# Compose, mix and spatialize audio with Tesseract

Do in Tesseract everything Tesseract can do, and keep the result native and editable. When it cannot do something, say so, propose the closest native approach, and use another tool only if the user asks for it.

The CLI may send basic usage telemetry for some commands. You can provide optional attribution via `TESSERACT_SKILL=tesseract-audio` and the [other attribution variables](references/telemetry.md). Respect the CLI's telemetry opt-out setting; never enable telemetry on the user's behalf.

## Start

1. Resolve this skill's root from the directory containing this `SKILL.md`. Read [CLI installation](references/installation.md) and check the required Tesseract version once per session. Save `tsrct project schema` to a file and search it to see every DAW action, instrument, effect, option and preset; it is too large to print whole. Read [local operation](references/local-operation.md) and [native authoring](references/native-authoring.md).
2. Establish which of the three areas below the request needs (often more than one), the deliverable and its length, any delivery loudness spec, and the supplied recordings, samples, stems or MIDI.
3. Read the DAW references in order: [tracks and audio clips](references/daw-tracks.md), [mixer and effects](references/daw-mixer.md), [MIDI, instruments and tempo](references/daw-midi.md) and [automation](references/daw-automation.md). Their examples build one song. Look up each action's exact fields in `tsrct project schema`, and the document's in `project schema --document`, before writing them; do not invent fields, enum spellings or effect types. Apply small batches with `project apply` and stop at a rejected batch. Keep every element native and editable.

## Audio processing and mixing: dialogue, podcasts, sound effects and video sound

- Import recordings with `project import-asset --kind audio` ([media import](references/media-import.md)). Put them on audio tracks for a multitrack session, or keep the Audio and Video layers an edit already has: tracks, Audio layers and Video layers all have mixer channels.
- Set gain first, with headroom on every source, then EQ and dynamics per source, shared processing on a track, and a limiter on the master.
- Balance with each owner's `volume` until you automate it: volume keys replace the static `volume`. To rebalance a track, clip or master whose volume is automated, set its `trimDb` with `updateFxMixerChannel` and leave the keys alone; do not rescale or rewrite them ([mixer](references/daw-mixer.md#channel-controls)).
- For dialogue, follow [speech cleanup](references/speech-cleanup.md). For sound under picture, follow [sound design](references/sound-design.md) and [audio and timing](references/audio-and-timing.md). Duck music under speech with a compressor on the music's track keyed by the dialogue ([sidechain](references/daw-mixer.md#sidechain)).

## Music production: songs, beats, jingles and beds

Tesseract supports all music production tasks that one could ostensibly accomplish using professional audio 
editing software such as Logic pro or Ableton.

- Set the tempo, time signatures and key, and plan the sections in bars. Create one track per part. To write parts or visuals in time with a supplied song, loop or stem, first detect its tempo, beats and first downbeat with `tsrct detect-tempo` and set them, as described in [sync to the music's tempo](references/sound-design.md#sync-to-the-musics-tempo).
- Give each MIDI track an instrument: an oscillator synth, with FM between its oscillators for bells, metallic tones and growls; a sampler playing imported samples, with zones by key, or one recording played across the keyboard at its own length; or a `drums` kit, whose pads each put a synthesized or sampled drum on a key, with optional choke groups. Recorded samples make drums, breaks, vocals and acoustic instruments sound far better than synthesized ones: find, prepare and load them.
- For finding and importing samples, check [sampling guidelines](references/sampling.md). Use this to build drum kits and midi instruments.
- Write MIDI clips and loop short patterns instead of copying notes. Use per-note bends for scoops and drops.
- Once your notes cover the whole piece, and before you add accents, effects or automation, run the [composition review](references/composition-review.md), which follows the [critic review](references/critic-review.md): two independent critics, a composer and a specialist in the brief's genre, score the notes, and you revise until both rate them at least 8.5/10, for at most three review rounds.
- Add risers, impacts and other accents as audio clips; the [sound helper](references/audio-and-timing.md#select-or-make-a-local-accent) makes them. Use clip fades and crossfades, and automation for builds, filter sweeps and drops.
- Balance the parts with each track's `volume`, and once a track's volume is automated, with its `trimDb`: the keys keep the build's shape and the trim moves the whole track by exactly its dB.
- Add a supplied `.mid` with `tsrct project import-midi --project <doc> --file <song.mid> --instrument <instrument.json>`, where the JSON file holds the instrument record its parts play (channel-10 parts play the General MIDI drum kit). Write MIDI out with `tsrct project export-midi --project <doc> --output <song.mid>` when asked.
- End the master chain with a limiter; the `master-bus-glue` preset is a starting point. Clips lengthen the document to cover them, but effect tails and instrument releases do not: extend the document's `duration` to let the ending ring out.

## Spatial audio: binaural sound effects

- For spatial audio ("3D" or "8D" audio), add a `binaural` effect as the last effect in a source's chain and leave that owner's pan at the centre. Set its azimuth, elevation and distance, and automate them to move the source. For fast passes, also set `doppler` so the pitch bends as the source comes and goes. The [mixer](references/daw-mixer.md) and [automation](references/daw-automation.md) references describe both.
- Place individual sources rather than the whole mix, and keep the bass and the main voice ahead unless the brief asks otherwise. To match objects in a 3D scene, follow [spatial audio](references/sound-design.md#spatial-audio-for-headphones).

## Review and deliver

1. Review with [audio review](references/audio-review.md): render the mix, stems, loudness report and spectrogram with `export-audio`, fix every failed check and render again. Then read and follow the [critic review](references/critic-review.md): two independent critics, a music critic and a mix engineer for music (a producer with a podcast producer for spoken audio, or with an immersive audio engineer for binaural work), score the measurements, and you revise between rounds until both rate it at least 8.5/10, for at most three review rounds. Tell the user the review plan, each round's scores and feedback, and the final score. Neither you nor the critics can listen: say which qualities still need a listener.
2. Deliver the editable `.tsrct` with the final WAV from `export-audio` (or an MP4 from `export` when the piece has picture), its report, and the measured integrated loudness and true peak: for an MP4, `export --json`'s `encodedAudio`, as [measure and check the final delivery](references/audio-and-timing.md#measure-and-check-the-final-delivery) describes. Keep checkpoints and review renders lean as described in [storage](references/local-operation.md#storage), and hand off as described in [review and delivery](references/review-and-delivery.md#handoff).
