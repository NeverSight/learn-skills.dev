---
name: flux-3-archival-formats
description: Use when a FLUX 3 video needs a period or archival look. Covers naming a recording format instead of a mood, per-format artifacts, and templates.
metadata:
  author: Black Forest Labs
  version: "1.0.0"
  tags: flux, flux-3, bfl, text-to-video, archival, format, style
---

# FLUX 3 Archival Formats

A period look is requested by naming the machine that recorded it, not the feeling it
should produce. "Vintage," "nostalgic," and "retro" are adjectives: nothing in the output
can confirm or refute them. A recording format is hardware with named physical artifacts,
so a reviewer can check the frame for each one and say whether the request landed.

Use this for a single standalone shot, or for a montage that must read as one era. Route
supplied stills or clips to `flux-3-keyframes-continuation`, and shot craft that has
nothing to do with period to `flux-3-cinematic-inserts`.

## Format artifacts

Each row is a checklist. Name the format and the era together, then request the artifacts
explicitly; a reviewer confirms the look by finding them in the frame.

| Format | Era | Artifacts to request and verify |
| --- | --- | --- |
| Super 8 | 1970s | Rounded film-gate corners, heavy warm grain, blooming highlights, dust and hair in the gate, occasional splice jump, slight gate weave |
| VHS camcorder | 1980s | 4:3 pillarbox, chroma bleed, horizontal scan lines, magenta head-switching band along the bottom of frame, tracking-error flicker, washed-out low-contrast color |
| 16mm documentary | 1960s | Muted green-leaning stock, handheld weave, visible print wear and scratches, shallow depth from a fast prime |
| Hi8 | late 1990s | Video-sharp image, barrel distortion, mild color noise in shadows, timecode-era consumer framing |

Hi8 separates least from a modern digital look, because its era is the least stylistically
distinct. Expect a weaker result there and lean on the other three when the brief allows a
choice.

## Name the degradation, not only the format

A format label alone is not enough. A bare request for "1980s VHS" returns a sharp,
modern-looking image wearing period colors: the model reads the era as a color grade. Low
fidelity has to be requested as fidelity, in the prompt, alongside the format name.

Three phrases carry most of the weight:

1. **Reduced resolution**: "soft, visibly low-resolution tape image," not just "VHS."
2. **Tape artifacts**: scan lines, chroma bleed, head-switching band, tracking flicker.
3. **Bright-source behavior**: "soft hazy bloom around the sun." A sharp anamorphic lens
   flare is one of the strongest signals of a modern synthetic image, and models reach for
   it by default.

## Templates

Replace the bracketed fields; leave the format language intact.

```text
Super 8 home-movie footage from the 1970s. [SUBJECT AND ACTION] in [SETTING], warm
afternoon light. Heavy warm-toned film grain, rounded film-gate corners, blooming
highlights, dust and hair visible in the gate, slight gate weave, occasional splice jump.
Handheld, softly focused, saturated faded film color.
```

```text
1980s VHS camcorder footage, soft and visibly low-resolution, 4:3 pillarboxed.
[SUBJECT AND ACTION] in [SETTING]. Heavy chroma bleed, horizontal scan lines, a magenta
head-switching band along the bottom of frame, tracking-error flicker, washed-out
low-contrast color. Bright sources bloom as a soft haze rather than a sharp flare.
```

```text
16mm documentary footage from the 1960s. [SUBJECT AND ACTION] in [SETTING]. Muted
green-leaning film stock, handheld weave, visible print wear and vertical scratches,
shallow depth of field from a fast prime, available light only.
```

```text
Late-1990s Hi8 camcorder footage. [SUBJECT AND ACTION] in [SETTING]. Video-sharp but
noisy image, barrel distortion at the frame edges, color noise in the shadows, flat
consumer-camcorder exposure.
```

## Prove a style word works: run a control probe

Before committing a style vocabulary, test that it changes the output at all. Hold one
subject constant, generate it once per candidate format, and generate **one control with
no format language whatsoever**. If the formats do not separate from the control and from
each other, the vocabulary is inert and the wording is doing nothing.

The result to look for is an artifact the prompt did not ask for. In one probe on a fixed
subject, a VHS request produced an unprompted head-switching band: a physical tape
artifact, not a color grade, which is evidence the model holds a real representation of
the format. The clean control came back bright, sharp, and modern, resembling none of the
four. Use this probe for any new style claim before it ships in a guide.

## Montage

Hold one format constant across every shot. Mixing Super 8 grain into one clip and VHS
scan lines into the next reads as an error rather than a style, and artifacts from two
formats inside a single clip are physically contradictory. Vary subject, light, and time of
day instead; the format is the thing tying the sequence together.

## Review

A shot passes when the named artifacts for its format are present in the frame, no
artifact from a second format appears, bright sources bloom rather than flare, and the
image does not read as a sharp modern capture wearing period colors. Reject and reprompt
rather than accepting a clip that only fails the fidelity test; that failure is the most
common one and the easiest to talk yourself out of seeing.

Period home-movie subjects carry a content risk worth stating: childhood scenes such as
bath time or a pool jump can render a child unclothed. Discard the render, exclude the
file, and record why, rather than reviewing it further.

Reference: [docs.bfl.ai](https://docs.bfl.ai)
