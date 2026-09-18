---
name: ace-studio-features
description: "What ACE Studio's features are and when to reach for each one — track types and what makes sound on them, audio effects, Vocal Synth and its voice library, AI Instruments, third-party instrument plugins, the generative kits (Inspire Me, Music Enhancer, Add A Layer), and the utilities (Stem Splitter, Voice Changer, Vocal to MIDI, Doubles, marker track, file import). Load whenever the user wants to create, change or understand anything in ACE Studio: adding a voice or instrument, choosing a singer, generating music, splitting stems, converting a vocal, or asking what a feature does. Pair with `ace-studio-workflows` for the order to do things in."
---

# ACE Studio features

# Tracks

### Track types

A track has no fixed type, and by default it is a blank track. It becomes what
you put on it — load a singing voice and it is a vocal track, load an instrument
and it is an instrument track. A project starts with a large pool of empty
tracks waiting to be filled.

| | Catalog | Driven by |
|---|---|---|
| Blank track | Blank | |
| Audio track | Audio | audio clip |
| Voice track | MIDI | MIDI + lyrics + vocal parameters |
| AI instrument track | MIDI | MIDI + articulations + instrument parameters |
| Plugin instrument track | MIDI | MIDI + MIDI CC |
| Master track | | |

- A MIDI track with no sound source is not silent — it falls back to a standard
  piano sample library. When the user says "it sounds like a piano", the answer
  is almost always that nothing is loaded, not that something broke.

- Every track except a blank track can host audio effects.

- **Unison Mode** belongs to voice tracks and AI instrument tracks only. It lets
  several voices or instruments load onto one track to produce a unison. Open
  the spread up when you want a wider stereo image.

### Audio effects

- ACE Studio ships basic effects, but prefer the third-party plugin effects the
  user has installed locally.

- Voice tracks and instrument tracks come with a basic effect chain already
  loaded. Add to it or strip it back as the work requires.

- **Room Effect** is a spatial effect that exists to serve Unison Mode: it
  models one acoustic space and places the unison speakers at different
  positions within it. Turn it on only when the track plays a background role.

- **To take an effect out of the chain, deactivate (disable) it — do not bypass
  it.** Bypass is for comparing a plugin in context, a listening call an agent
  does not make.

# Vocal Synth, AI Instruments, and instrument plugins

### Vocal Synth

Use Vocal Synth when the user wants to create a vocal. It is the sound source
that takes MIDI and lyrics, and synthesises a sung vocal through a chosen
speaker.

Recommended speakers:

| For | Speakers |
|---|---|
| Big pop vocals | Ember Rose, Rebecca, Bianca, Mangus |
| R&B, jazz | Jessica, Zalo |
| Lyrical, tender | Elirah, Emma |
| Epic, cinematic | Clara |

**Blend voice** creates a new voice by mixing several speakers. When the user
describes a voice they want, pick from the library first; reach for a blend only
if the library does not get there and they want something bespoke.

If the user wants their own voice, or a specific voice they supply, open the
voice library and point them at the **Cloning** tab to train it themselves. That
flow happens in a browser. Consult the wiki and walk them through it.

**Vocal Synth renders in the cloud, but there is a turbo mode** that moves most
of the model computation onto the local machine. Studio measures whether the
machine can support turbo mode the first time it launches: if the local compute
is enough it is on by default, and if the check fails it cannot be enabled.
Turbo mode turns on **pre-rendering** by default, so an edit triggers a render
immediately. With turbo mode and pre-rendering together, rendering is usually
finished before playback even starts.

- Without pre-rendering, rendering is triggered by playback.
- With pre-rendering, rendering is triggered by the edit.

### AI Instrument

When the user wants an acoustic instrument, prefer an AI Instrument — its
realism is far beyond a sample library.

AI Instruments do not render in real time, so each instrument type carries a
very small sample pack purely so MIDI input responds as you play. **That sample
is not what the model outputs.**

**String Section** is modelled on a string orchestra. Its speakers are Violins I,
Violins II, Violas, Celli and Basses. These support polyphony well, but keep the
written part idiomatic for the section it is on.

AI Instruments render in the cloud, with no turbo mode and no pre-rendering, so
rendering is always triggered by playback.

**Every other instrument is a solo instrument.** You can feed them polyphonic
material, but they do not behave the way a sample library does:

- Strings tolerate a little polyphony — but as one instrument bowing several
  strings, not as a section.
- Wind instruments cannot physically play polyphonically, so the model is forced
  to fake it. Do not do this.
- When a solo instrument needs several parts, split them across tracks instead.

Instruments named **Vintage** perform less well than the others.

**Articulations are marked on notes**, and each instrument type has its own set.
The default **smart mode** works out the articulation from the melody and applies
it in the synthesised result. Two articulations never appear under smart mode and
must be set explicitly:

- Pizzicato
- Mute

### Rendering — Vocal Synth and AI Instruments alike

Whatever triggers a render, **it only starts on a track that can currently be
heard.** A muted track makes no sound, and neither does any track while another
track is soloed — and a silent track never renders. If nothing is rendering,
check mute and solo before anything else.

During playback, a region that has not finished rendering blocks playback.

### Instrument plugins

ACE Studio supports third-party VST3 and AU instrument plugins.

When the user wants a particular sound:

- If it is an acoustic instrument, look through the AI Instrument list first.
- Then look through the user's own plugin list for something suitable.

**Once a plugin is loaded, it is fully drivable — parameters, whole state and
presets, and its own interface through Studio's built-in computer use.** See
`ace-studio-audio-plugins` for how to drive it, and for per-plugin recipes.

# Generative Kits

Every generative kit takes a prompt and produces audio. Generation takes **over a
minute**. There are three:

- **Inspire Me** — text to song. Use this when the user wants to generate a whole
  song outright.

- **Music Enhancer** — AI cover. Select a region of the timeline as the input
  context. Once the tool has uploaded the audio it returns the lyrics and style
  it recognised; edit either (or neither) to produce the cover. Three common uses:

  - **Style replacement.** Keep the lyrics, rewrite the style description, turn
    one finished piece of music into another.
  - **Finishing an idea.** Record a hum or write a melodic motif, then write the
    lyrics and style out in full to grow the motif into a complete demo.
  - **Refinement.** Keep the lyrics and style as they are and regenerate. The
    content usually shifts slightly, but it turns a rough demo into a polished one.

- **Add A Layer** — generation as splice. Select the region to generate into. The
  tool uploads the surrounding timeline content as reference audio and generates
  the specified sample from the prompt. The result fits what is already on the
  timeline — a bass line, a drum part, a lush string passage.

### How to prompt Add A Layer

**Choose custom mode.** Then write two short prompts, one per field:

- **Instrument** — the instrument and its timbre.
- **Styles** — the musical content: style, emotional colour, layering and
  dynamics, and the groove and physical feel of the playing.

Keep both short. **Do not describe rhythm or chords** — the surrounding audio is
uploaded as reference, so the model already has the harmony and the groove;
restating them adds nothing. And **do not pile up negative prompts**: this model
is built for synthesising a single timbre, so by default it does not need to be
told what to avoid.

# Utilities

### Stem Splitter

Four ways to split:

- **Vocal, instrumental.**

- **Vocal, drums, bass, piano, guitar, others.** Nothing is distinguished within a
  category — several guitar tracks may all land in the guitar stem — and some
  instruments end up in Others.

- **All detected stems.** Separation is not guaranteed to be complete; instruments
  of the same category often share a stem, and some land in FX or Others.

- **Customized.** Describe what to separate in a prompt. This suits non-musical
  audio better; on musical content the granularity is coarse — ask for hi-hat and
  you will likely get the whole drum kit. The operation produces two tracks: the
  separated target, and everything left over.

### Voice Changer

Converts a monophonic vocal on the timeline into a vocal or instrument audio in a
chosen timbre.

A set of preset **models** is included to cover a wide range of creative needs,
and the surface lists every model a conversion can use. When the user needs a
timbre outside it, guide them to train their own Voice Changer model.

Training input is usually a vocal, but in practice it also accepts instrument
audio with a clear timbre — which must also be monophonic.

### Vocal to MIDI

Recognises a sung vocal in audio as a MIDI clip with lyrics. Supports monophonic
vocals; it cannot correctly resolve stacked, multi-part vocals.

The V2 model can pull the lead vocal's lyrics and melody straight out of a
complete song, and holds up well against background noise.

**Expect some notes to come back at the wrong pitch, and fix them before the
clip is used.** A single note is not enough to judge — a drifting note and a
deliberate accidental look the same in isolation. Read the melody as a whole,
work out what key it is actually in, and correct the notes that fall outside it.

### Doubles

Vocal Synth tracks and AI Instrument tracks support doubles.

The result is two duplicated tracks whose notes carry a degree of random offset
from the originals. The two new tracks are panned left and right.

### Marker track

A marker track can be created at the top of the timeline to give the user
reference annotations against time — sections, lyrics, and so on.

### Tempo track

When the music changes tempo, draw tempo automation on the tempo track. Note
that **editing the tempo track overwrites globally.**

When the user wants the project tempo synced to imported audio, use the Apply
Tempo interface to apply the audio's tempo to the project. Note that this
operation **shifts the target audio later** so that the audio's first downbeat
lands on the nearest bar line.

### Importing files

Studio imports the common formats onto the timeline — MIDI, audio, MusicXML and
video among them. The surface's docs carry the full extension list.
