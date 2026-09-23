---
name: analog-occultism
description: >-
  Use this skill to create subject-neutral images and videos in an analog occultism
  / industrial CRT noir aesthetic: near-monochrome archival technical atmosphere,
  severe low-key lighting, tactile signal degradation, industrial geometry, and
  quiet unresolved tension. Use for portraits, products, environments, interfaces,
  diagrams, abstract forms, stills, and motion. Do not use for colorful cyberpunk,
  vaporwave, glossy advertising, conventional horror, or clean digital renders.
license: MIT
compatibility: >-
  Compatible with image-generation and video-generation tools. Video workflows
  may require a configured video backend and FFmpeg for frame-level verification.
metadata:
  tags: analog-occultism, industrial-crt-noir, archival, retro-futurist, image-generation, video-generation
  source: user-provided aesthetic brief
---

# Analog Occultism / Industrial CRT Noir

Apply a cross-media visual language, not a subject, character, brand, or story. The
creative premise is: **advanced systems seen through an obsolete recording medium**.
The result should feel like a mysterious technical artifact recovered from a
forgotten research archive: intelligent, secretive, uncanny, severe, tactile, and
quietly beautiful.

## Core Workflow

1. **Identify the subject and its essential identity.** Preserve the subject's
   recognizable structure, but treat it as evidence, artifact, specimen, icon, or
   component of a larger system rather than a casual commercial presentation.
2. **Choose one dominant practical source.** Prefer a screen, projector, narrow
   overhead fixture, hard backlight, small industrial light, or source just outside
   frame. Let it reveal selected surfaces while most of the space falls into black.
3. **Build the frame around depth and obstruction.** Use a square, portrait, or tight
   crop by default; central or slightly off-center placement; tunnel perspective,
   receding grids, corridors, cables, grilles, foreground obstruction, and a single
   luminous rectangle or focal object.
4. **Apply the shared visual grammar.** Use near-monochrome tonality, crushed blacks,
   blown ivory highlights, sparse midtones, tactile age, geometric framing, and
   controlled imperfection. Color is absent or limited to a subtle cold green,
   blue-gray, desaturated amber, or signal-error cast.
5. **Choose the capture layer explicitly.** There are two related but different looks:
   **CRT-display view** shows an image on a square monochrome tube; **analog-camera
   documentary view** shows a real-world object or scene recorded by a period analog
   video camera. Do not let the second collapse into the first. For documentary view,
   state that the subject is physically present in a real location and that the camera
   is photographing it directly, with practical lens behavior, imperfect focus,
   exposure, depth of field, reflections, and incidental set detail. The CRT or signal
   is the camera and recording chain, not the subject's entire reality.
6. **Make the recording medium the subject of the image.** The result must read as
   a low-fidelity monochrome CRT capture or a photograph of one, not a clean digital
   scene with scanline overlays. Start from a small, soft, interlaced raster: visible
   scanline structure, phosphor bloom, coarse noise, sync wobble, barrel distortion,
   clipped whites, crushed blacks, ghosting, focus falloff, dust, scratches, and
   uneven exposure. Let detail disappear. Signal damage should reduce fidelity while
   preserving the essential subject.
7. **Add signal treatment as physical evidence, not decoration.** Use restrained CRT
   scanlines, interlacing, film grain, dust, scratches, halation, phosphor bloom,
   soft focus, edge smearing, vignette, slight barrel distortion, ghosting, minor
   chromatic misregistration, and uneven exposure. Keep the subject legible.
7. **Check the result against the consistency rules.** Reject outputs that become
   bright, evenly exposed, colorful, glossy, busy, generic glitch art, or polished CGI.

## Prompt Pattern

Use the subject-neutral shorthand, then add only the details the specific asset needs:

```text
[SUBJECT] shown as a low-fidelity monochrome CRT screen capture, rendered as analog
occultism / industrial CRT noir: visibly soft interlaced raster, coarse phosphor
structure, horizontal scanlines, sync wobble, barrel distortion, ghosting, uneven
tracking, crushed blacks, clipped ivory highlights, one luminous practical source,
claustrophobic geometry, archival technical atmosphere, tactile signal degradation,
quiet unresolved tension, controlled imperfection. It must look like an old recording
of a CRT, not a clean digital image with a scanline filter.

The recording defects are structural and unavoidable: low-resolution broadcast image,
soft focus, horizontal line structure, phosphor persistence trails, unstable vertical
hold, slight horizontal tearing, uneven brightness across the tube, black crush hiding
fine detail, white blooming around the screen, dirty glass, dust, and imperfect analog
capture. Do not render a sharp modern digital photograph and then add cosmetic lines.
```

Describe concrete objects, spatial relationships, and the information the viewer must
understand. Do not rely on mood words alone. If typography is necessary, use original
archival-technical labels, all-caps system annotations, monospaced text, framed
emblems, diagrams, readouts, indexes, or specimen-card structures. Keep text sparse;
models may render small annotations imperfectly.

For detailed still-image prompt blocks, reference-based generation, and negative
prompt guidance, read `references/image-prompting.md`. If a user supplies a visual
reference, use the actual reference in the image tool; a text description is not a
substitute for the pixels.

## Video Direction

Preserve the same visual grammar across time. Motion should be slow, deliberate,
mechanical, and slightly uncanny:

- slow push-ins or pull-backs, mechanical tracking, and subtle lateral drift;
- focus breathing, screen flicker, small exposure shifts, servo-like camera motion;
- long pauses, sparse cuts, gradual reveals, and loops that return unresolved;
- camera behavior suggesting an automated observer or a machine becoming aware.

Describe motion as a restrained physical event, not as a collection of effects. Keep
one dominant light source stable enough to anchor the shot, then allow small changes
in flicker, exposure, focus, dust, or tracking. Use image-to-video when the opening
composition matters, keyframes when a transformation or style continuity matters,
and continuation when extending an established shot. Do not turn scanlines or
jitter into frenetic glitch animation.

Before any video generation, load the configured video backend's prompting guide. For
FLUX 3 workflows, use the `video-generation` skill and its required prompting guide,
then verify a bounded sample of rendered frames with FFmpeg and visual inspection.
Read `references/video-prompting.md` for shot templates and continuity rules.

## Shared Consistency Rules

Each asset should contain most of these ten signals:

1. near-monochrome tonality;
2. one dominant luminous source;
3. severe black-and-white contrast;
4. strong negative space;
5. tactile analog or archival texture;
6. geometric or industrial framing;
7. hidden technical depth;
8. quiet, unresolved tension;
9. controlled imperfection;
10. a discovered artifact quality rather than fresh manufacture.

The subject can change. The visual grammar cannot.

## Avoid

- **Screen-capture fidelity:** when the brief calls for CRT or recovered footage, name
  the raster defects explicitly: low resolution, soft focus, visible scanlines,
  interlacing, phosphor persistence, sync wobble, tracking errors, barrel distortion,
  clipped whites, crushed blacks, ghost trails, and dropped detail. A clean image with
  a decorative scanline overlay is a failure, not a pass.

Do not default to colorful cyberpunk, vaporwave, broad RGB neon, teal-and-orange
cinema grading, clean SaaS minimalism, glossy product advertising, high-key studio
photography, generic hacker imagery, excessive digital corruption, random interface
clutter, cartoon horror, jump scares, gore, conventional horror iconography, or
perfectly polished CGI. Do not use nostalgic retro props merely as decoration.
Effects must never become more noticeable than the subject.

## Reference and QA Boundaries

- Use reference images to preserve identity, composition, or a visual anchor, but do
  not promise pixel-exact style transfer from an edit model.
- For people and creatures, inspect anatomy before judging style. Clearly visible
  hands, limbs, cables, straps, and connected objects must have plausible geometry.
- For typography and diagrams, verify every visible label, relationship, arrow, and
  hierarchy. Never invent technical data because the aesthetic suggests annotations.
- For video, inspect sampled frames rather than trusting generation metadata. Confirm
  the dominant light, subject identity, motion restraint, and absence of accidental
  color or digital corruption. Sampling proves only the sampled times.
- After one or two materially different failed generations, stop and report the
  model limitation or change the shot. Do not hide a failed subject behind more
  darkness or degradation.

## When Not to Use

Use another aesthetic skill for a named brand's locked visual identity, a specific
site's cover rules, colorful cyberdelic work, or a production video workflow that
needs backend-specific operation rather than aesthetic direction. This skill defines
visual language; it does not replace `image-gen-reference`, `video-generation`, or
`ffmpeg` for their respective operational procedures.

## Completion

The skill is complete when the still or shot preserves the subject, expresses the
shared visual grammar, passes the relevant image or frame-level checks, and has an
explicit note of any unresolved model limitation or sampling boundary.
