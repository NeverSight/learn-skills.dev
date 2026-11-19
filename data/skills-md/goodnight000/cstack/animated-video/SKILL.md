---
name: animated-video
description: >-
  Make animated videos in code with Remotion (React, SVG, three.js): explainers, character
  stories, motion graphics, kinetic typography, paper collage and animated infographics, in 2D or 3D, from a
  script or voiceover, in any aspect ratio. Use when asked to animate a script, make an
  animated video or Reel, or motion graphics. Not for editing camera footage (video-edit) or
  AI-generated clips (higgsfield-*).
---

# Animated video

Turn a brief into a finished animated video in which every image is made in code: drawn
procedurally, or built from approved sourced assets rendered deterministically. Footage from
image or video generators is a separate route (step 2). Read `~/.animated-video/profile.md` first
if it exists: the user's stated preferences come before the defaults here.

## What makes the film

**Be as inventive as the idea allows.** For every concept the film shows, look for the most
surprising picture that still makes it click. Wacky, impossible, funny or beautiful ideas are
welcome, and each is judged by one test: does the viewer understand the mechanism faster, or
remember it longer, than with the literal picture? The literal picture is the fallback that wins
only when nothing beats it. Accuracy checks an idea; a metaphor the narration grounds stays.

**The picture explains; the voice confirms.** With the sound off, a viewer learns each step from
what happens on screen: the mechanism is performed as cause and effect (cut, sent, hit, copied),
each line's idea visible by its word, with labels supporting the event rather than replacing it
([motion](references/review.md#motion)).

**Colour points the eye.** Decide what each colour means early: the thing the viewer follows
carries the accent and is the brightest, most saturated thing in frame, and a colour keeps its
meaning for the whole film. Give each other role its own colour and let everything that carries
no meaning stay quiet. To match a reference look, sample its colours from its frames and give
animators the numbers: lights, fog and grading drift a named colour toward grey.

**Design fresh for each brief.** Style packs, parts and past films are head starts. A past film
the user liked sets the bar for finish and pace, never the ideas, devices or look.

**Feedback narrows a picture, never the imagination.** When the user rejects an idea, write down
what was wrong with that idea (it confused, felt forced, looked cheap) and find a better one of
any kind. It becomes a rule about a whole category only when the user states it as one, and the
briefs you write for other agents carry only the rules the user stated.

**Ask with a recommendation,** so "yes" is a complete reply. Say once at the start that the skill
works best with the strongest available model at high effort.

## Scale the production to the piece

- **Short or simple:** one agent can carry it, checking stills. The brainstorm still goes to a
  fresh agent and the mute test still runs.
- **Longer, or many acts:** keep the pictures, concept and look with one agent until the user
  approves them, then parallelise the build as suits it. The board fixes each beat's idea;
  whoever animates owns how it moves and proposes a better picture when they see one. Keep one
  cue sheet for the whole film so the sound stays intentional. On long runs, send status with a
  still and the overall time left; have agents stamp status lines with the machine clock, since
  self-reported times can drift by hours.
- **A revision of a finished film:** ask which sections to rebuild, recommending the weakest;
  keep the rest and [splice](references/handoffs.md#splicing-new-parts-into-a-finished-film)
  the new parts in.
- **An insert for someone else's timeline** (an animated shot inside a camera edit, which
  video-edit owns): [inserts](references/handoffs.md#inserts-for-another-timeline). When
  it's unclear who owns the timeline, ask once.
- **A presenter on camera in the film:** [compositing](references/compositing.md) before those
  shots are planned.

## 1. Find the pictures and the concept

Pick the spine in [directing](references/direct.md): a story (someone who wants something) or an
explainer (how something works, why, what a number means). The pictures come from a fresh
brainstorm agent that sees no production rules, judged by a separate picker
([find the pictures](references/direct.md#find-the-pictures)); then concepts that genuinely
differ, your recommendation, and the chosen one as a timed beat sheet with each beat's picture. A
finished script settles the words, not the pictures. With the video-script skill installed,
check the narration against its checklist.

Get the user's approval of the concept and its pictures before building, short pieces included.

## 2. Lock the format and the style

- When the request names the format and style, confirm it in one line. Otherwise show styles that
  genuinely differ as style frames of the same beat ([styles](styles/README.md)) and get a pick;
  read the chosen style's pack when it has one.
- Ask about the route and its cost: made in code is free per shot and consistent; AI video costs
  per clip and drifts.
- Look up photos of the real objects, places and interfaces the film shows. If a real person
  appears, ask where their footage lives and pull frames from it.

## 3. Build the audio spine

Every beat times off the narration (without one, off the music bed, chosen first). Prefer the
user's recording; before it exists, build on
[stand-in word timings](references/remotion-pipeline.md#before-the-vo-exists), labelled.
`templates/remotion-film/align.py` gives word timestamps and a loudness envelope; derive every
cue from words with `cue("phrase")`, so a new VO re-times the film. Captions are hand-written
sense units checked against the transcript. Music and effects ship with the first cut: the
user's files, the asset library or samples on disk before synthesis
(`templates/parts/audio/designed.py`), and anything synthetic is labelled.

## 4. Skeleton and board

Copy `templates/remotion-film/`, wire acts, captions and audio, and render stills across the
timeline ([pipeline](references/remotion-pipeline.md)). Unverified facts stay out of the film.

Show the user a **key-frame board** before the full animation: a still per beat in the chosen
style, built in the real scene files so it grows into the finished shots. Approved stills don't
show whether anything happens between them; when meaning lives in motion, an **animatic** (rough
shapes performing the beats over the VO) shows it cheaply.

## 5. Build the assets and shots

Search the asset library first when it's installed. Recurring pieces hold at every scale the
story needs: drawn characters per [characters](references/characters.md);
[parts](templates/parts/README.md) has a globe, an iMessage iPhone, designed sounds, a realism kit
and a motion kit for dense three.js motion. Restyle what you take.

When several agents animate, give them one written look and bar, taken from the style pack and
the anchor frames (the reference film's frame for each beat, or the board). In every style, a
real object, interface, company or place is recognisably itself, and a stand-in gets the same
care. Derive each act's [sound events](references/remotion-pipeline.md#sound-events) from the
constants that draw it, so moving a beat moves its sound.

## 6. Review and deliver

Agents see frames, not playback: check motion as strips of consecutive frames
([temporal checks](references/review.md#temporal-checks)) and audio by measurement, and say what
was only measured. When you can't trust your own eye, have independent fresh agents judge
([review](references/review.md)); stop iterating when a round gains little or the top issue
needs the user.

Before the first full cut goes to the user, a fresh judge runs the
[mute test](references/review.md#mute-test) on it; fix what it can't follow. A rejected whole cut
restarts from the pictures ([restart](references/review.md#restart-after-a-rejected-cut)).

Render the final (`render.sh` normalises loudness; long films in chunks) and check the first
frame, the last second and the loudness. Report the path, open issues, skipped checks, sourced
images, and anything synthetic or invented. Commit each version in the project's git repo. With
the asset library installed, close its catalog.

On request, reflect with [the reflection protocol](references/reflection.md).
