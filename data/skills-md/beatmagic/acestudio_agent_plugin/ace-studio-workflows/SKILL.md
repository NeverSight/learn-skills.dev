---
name: ace-studio-workflows
description: "Recommended end-to-end workflows in ACE Studio — the order to run features in, which feature to reach for at each step, and where the work has to leave Studio for an external tool. Covers generating a whole song and aligning the project to it, reworking a song from an imported audio file (beat alignment, stem splitting, transcription back to MIDI), and turning a finished project into printable sheet music. Load whenever the user's request spans more than one step, or says things like 'write me a song', 'I have this audio and I want to…', or 'I need a score for this'. Pair with `ace-studio-features` for what each feature does."
---

# ACE Studio workflows

# Song generation

When the user wants a whole song generated, use **Inspire Me**.

## 1. Generate

See `ace-studio-features` for what Inspire Me takes and what it costs.

## 2. Align the project tempo to the result

Do this before any editing — an unaligned project makes every later edit fight
the grid. Which way you go depends on what else is on the timeline, because
**applying a tempo replaces the project's tempo and meter wholesale and moves
existing content.**

- **The generated audio is the only thing on the timeline.** Nothing can be
  disturbed, so apply its tempo to the project directly.

- **The timeline already has other content.** Ask the user first: confirm which
  version of the music they are keeping, and that it is the one the tempo should
  follow. Then apply that one's tempo. Everything already on the timeline will
  shift, so say so before you do it.

## 3. Offer to keep going

Ask whether they want to edit the song. If they do, the first workflow below is
the route in — split it into stems and transcribe the parts they want to change.

---

# Edit a song from audio

When the user hands over a complete piece of music and wants to edit it, work
through it like this.

## 1. Align the project to the audio

Imported audio triggers beat analysis automatically. Apply that analysis so the
project tempo matches the audio's tempo — the operation also snaps the audio's
first downbeat forward to the nearest bar line, which shifts the audio later.

Tell the user the audio will move before you apply, and remember the whole apply
replaces the project's tempo and meter wholesale.

## 2. Split the music into stems

Use the Stem Splitter. Pick the mode from what the user actually needs — see
`ace-studio-features` for what each mode separates and what it costs.

## 3. Turn the melodic stems into MIDI

### 3.1 The lead vocal

Use the built-in Vocal to MIDI. It gives you the melody **and** the lyrics, which
is why it beats a generic transcriber here. It needs a monophonic vocal.

### 3.2 The other instrument stems — Basic Pitch, outside Studio

There is no instrument transcriber on ACE Studio's surface. Use
[Basic Pitch](https://github.com/spotify/basic-pitch), which runs locally and
free, then bring the MIDI back in.

**The stems live on tracks, and Basic Pitch reads files** — so the chain is:
export each stem track as audio → run Basic Pitch on the file → import the
resulting MIDI onto a track.

**Setting it up.** Check for a working environment first; do not install over the
user's existing one. Basic Pitch wants an older interpreter than the newest
system Python, so give it its own virtual environment — Python 3.11 is a
compatible starting point:

```
python3.11 -m venv work/transcribe-env
work/transcribe-env/bin/python -m pip install basic-pitch librosa pretty_midi mido
```

On Windows the interpreter is `work/transcribe-env/Scripts/python.exe`.

```
basic-pitch <output-dir> <stem.wav>
```

**Basic Pitch is a candidate generator, not a transcription.** It is built for
single-instrument material, which is exactly what a stem is — but the output
still needs cleaning before it is worth importing. Running it several times and
getting the same answer is not evidence; it is the same model twice.

### 3.3 Clean the MIDI before importing

Remove what the recogniser invented:

- **Harmonic stacking** — phantom notes an octave or a fifth above the real one.
- **Ultra-short noise notes** and **tail fragments** left by decay.
- **Duplicate onsets** on the same pitch at the same moment.

Keep what is musical: ornaments, syncopation, and rests are content, not noise.
**Judge against the actual tempo and phrasing — do not delete every short note
with one fixed millisecond threshold**, or you will flatten the performance.

Then check per instrument:

- **Bass.** Octave errors are the common failure, and slides come back as dense
  runs of semitones. Cross-check the root against the kick and the chord changes.
  Keep it monophonic by default: bleed from guitar or keys must not become bass
  chords.
- **Guitar.** Distorted guitar transcribes badly. Check short phrases against the
  spectrogram, the onsets, and the chord underneath.
- **Keys.** Sustain pedal and tail resonance come back as masses of held notes —
  do not transcribe them literally. Reconstruct the two-hand division from the
  bass and the harmony.
- **Drums. Do not use Basic Pitch.** It is a pitch model; percussion is out of
  scope for it.

### 3.4 Load sound sources

Load a suitable sound source onto whichever tracks the user wants to edit. See
`ace-studio-features` for choosing between AI Instruments and plugins.

---

# Export the project as sheet music

When the user wants a printable score of what is in the project.

## 1. Get the notes out of Studio

Export MIDI. It writes on the calling thread, so the file is on disk the moment
the command returns — there is nothing to wait on. It carries every track that
holds notes: voice, instrument, generic MIDI and chord tracks.

**Audio tracks carry no notes, so they will simply be absent from the score.**
Check the project for them before you export — a bass or guitar that only exists
as audio will vanish silently, and the user will not see it missing until they
read the page.

To bring one in, run it through the transcription path from the first workflow:
if it is a mixed audio track, split it into stems first; then export the audio,
run Basic Pitch on the file, clean the result, and import it back as a MIDI
track. For an audio track that is a **lead vocal**, use Vocal to MIDI instead —
it brings the lyrics with it, which is what the score wants under the vocal
line. Once the material is on note-carrying tracks, export MIDI again.

Ask the user before doing this: transcription is an estimate, and they may
prefer a score of only the parts they actually authored.

**Know what MIDI drops.** Lyrics, syllables, vocal parameters and articulations
have nowhere to live in a MIDI file. If the score needs lyrics under the vocal
line, export the vocal separately as UfData — which carries them, but only for
voice tracks — or plan to type them into the notation program.

There is **no MusicXML export** on this surface, so MIDI is the way across.

## 2. Notate it in MuseScore

MuseScore Studio is the free notation and export tool for this. Find the
executable rather than assuming a path: check `PATH`, the executable path of a
running process, the usual OS install directories, or ask the user. On Windows
the file is usually `MuseScore4.exe` — **do not assume it is on the C: drive.**

Import the MIDI, build the score, and save a native `.mscz`. Export PDF and MIDI
**from that `.mscz`**, so all three files come from one source:

```
<musescore> -o work/score.pdf work/score.mscz
<musescore> -o work/score.mid work/score.mscz
```

`-o` picks the format from the target extension. **Do not pass `-F`** — it clears
the user's settings — and do not reach for `--force` to paper over a score that
will not open.

## 3. Clean up what MIDI import produces

A MIDI import is a starting point, not a score. Expect to fix:

- **Note durations and rests.** A performance MIDI has notes that end slightly
  early or late; notation needs real durations, ties and rests.
- **Enharmonics and key.** MIDI carries pitch numbers, not spellings, so the key
  signature and accidentals need setting by hand.
- **Voice and staff assignment.** Keyboard parts arrive as one stream and need
  splitting across two staves; a percussion track may import as piano.
- **Tempo map.** Confirm the imported tempo and meter match the project,
  especially if beat analysis was applied earlier.

## 4. Verify before you hand it over

Do not report a score as finished on the basis that the files exist.

1. Reopen the final `.mscz` in MuseScore and confirm it is editable.
2. Parse the exported MIDI (`mido` or `pretty_midi`): check the tempo map, that
   notes are present, the voice mapping, and the durations. Look for octave
   shifts, drums exported as piano, and empty tracks. **A non-empty file with a
   valid header proves only that it is a MIDI file.**
3. Render **every** page of the PDF to an image (`pdftoppm -png -r 120 …`) and
   check each one for clefs, beams, ties, rhythm and layout. Spot-checking a
   couple of pages is not the final check.
4. If you edit the `.mscz` after exporting, re-export both PDF and MIDI from it.

Fix problems in the source score and re-check whatever the fix touched. Handle
routine issues yourself; do not ask the user about every spacing adjustment.

Describe the result honestly: say what you verified and what you did not. Call it
a playable arrangement unless you actually have evidence for note-level fidelity.
