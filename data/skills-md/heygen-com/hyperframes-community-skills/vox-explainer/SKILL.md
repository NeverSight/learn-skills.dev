---
name: vox-explainer
description: "Create a 60–90 second, collage-style HyperFrames explainer from a hiding-in-plain-sight topic or supplied documents and links. Use for requests such as 'make a plain-sight explainer', 'Vox-style history of X', 'why is X everywhere?', or 'turn this document into an explainer'. Covers topic or source routing, research, script, static design approval, voiceover timing, motion continuity, build, and numeric quality gates."
---

# Plain-Sight Explainer (Gateway Workflow)

Build against the HyperFrames composition contract (clips, `data-*` timing,
and the `#root` schema). Install the upstream HyperFrames skills with
`npx skills add heygen-com/hyperframes`, or scaffold with
`npx hyperframes init`, and read the generated project documentation first.

Make a 60–90s explainer about something the viewer sees daily but has never
looked at. The film manufactures recognition first, then pays it off with a
causal history. Grammar measured from Vox's Cooper Black film; motion from the
same frame-by-frame calibration process.

This is a Vox-inspired design vocabulary, not an affiliation or endorsement.
Do not use Vox logos or imply that Vox produced the result.

## Trust boundary and requirements

- Require Node.js 22 or newer for the bundled seam scripts. When they start a
  preview server, `npx` may download the exact HyperFrames version pinned in
  `scripts/seam-gate.mjs` from the npm registry.
- Read only the files and URLs the user supplies. Source mode may fetch public
  citations and public-domain or openly licensed assets from declared sources.
  Never send private documents, credentials, or private URLs to another
  service.
- Ask before using any TTS or transcription API. State the provider, data sent,
  required credential, and possible cost before the call.
- Write project source, downloaded assets, audio, contact sheets, and renders
  only inside the user's chosen project directory. Do not publish or upload the
  result automatically.
- The seam verifier starts a local preview server and an isolated Chrome
  profile. Its `--url` and `--comp-url` inputs accept localhost only. A preview
  may still load remote assets declared by the user's composition.

## Reference map

Read only the references needed for the current stage:

- Topic selection: [plain-sight-topics.md](references/plain-sight-topics.md)
- Script and captions: [plain-sight-script.md](references/plain-sight-script.md)
- Layout and assets: [vox-collage-layout.md](references/vox-collage-layout.md)
- Text and highlights: [vox-text-overlays.md](references/vox-text-overlays.md)
- Collage motion: [vox-collage-motion.md](references/vox-collage-motion.md)
- Motion law and seam gate: [motion-continuity.md](references/motion-continuity.md)
- Transition catalog and code: [velocity-matched-transitions.md](references/velocity-matched-transitions.md)
  and [velocity-matched-transitions-gsap.md](references/velocity-matched-transitions-gsap.md)
- Multi-stage element motion: [animation-overlap.md](references/animation-overlap.md)
- Render-safe seam mechanics: [render-safe-seams.md](references/render-safe-seams.md)
- Seam ledger and script usage: [seam-gate.md](references/seam-gate.md)

## Pipeline (run in order; each gate blocks the next)

1. **Entry router — two modes, one gate.** Read
   [plain-sight-topics.md](references/plain-sight-topics.md).
   - **Topic mode** (the user names a subject, or asks for ideas): the
     four-part filter governs IDEATION and tie-breaking only. If a
     user-chosen topic fails it, name which part fails and what the film
     loses, offer passing alternatives — then build the film they asked for
     if they confirm. The filter never refuses a chosen subject.
   - **Source mode** (the user supplies material — documents: a memo,
     strategy doc, report, paper, deck, transcript, PDF, or a folder of them;
     or links: an article, docs page, repo, announcement): the filter does
     not apply at all. After confirming the allowed network scope, read every
     supplied file, fetch every supplied URL, and follow at most one public
     citation hop when needed for a claim. When a citation is dead or truncated
     (common in exported PDFs), do not guess the source — verify the claim
     independently on the open web before it becomes a receipt, or cut it.
     Then run the storyline mine. Person+date and PD-archive requirements are
     waived; the mechanism beat is not. The audience is the
     source's INTENDED audience, not "any viewer" — the FAMILIAR beat
     calibrates to what they see daily. The VO never mentions the source —
     see [plain-sight-script.md](references/plain-sight-script.md).

   **The storyline mine (source mode).** The source is ore, not an
   outline — never film it section by section. Extract five things:
   - **The on-ramp** — the recognition the intended audience already has, in
     the source's own world (a habit, a number they see weekly, a thing on
     their screen right now).
   - **The tension** — the sharpest claim in the source that contradicts what
     that audience assumes.
   - **The turn** — the DIG's landing point: a person+date when the source
     has one, otherwise the decision, number, or moment the story pivots on.
   - **The mechanism** — the one claim the viewer can verify on screen
     unaided. If the source only asserts, BUILD the demonstration (two-panel
     compare, dots redistributed two ways, before/after at equal scale).
   - **The receipts** — real artifacts from the source plus the open web
     (charts, screenshots, filings, on-screen attributed quotes). Real-assets
     rule still holds.

   Map those onto the structural spine; beats the source can't fill honestly
   get cut, not faked. Multiple sources — or ONE source carrying
   several candidate storylines — mine each, then pick ONE spine: a film
   gets one storyline; everything else demotes to receipts. Deliver the
   beat map for approval before drafting script.
2. **Script** — read [plain-sight-script.md](references/plain-sight-script.md).
   Draft VO + beat map. GATE: every line passes the deletion test;
   opener/closer rules hold. If ghost-writing for a specific person, their
   voice skill outranks this one.
3. **Design pass** — read
   [vox-collage-layout.md](references/vox-collage-layout.md). Build a contact
   sheet (one frame per beat, 960×540 tiles, HTML → headless-Chrome screenshot)
   from REAL assets. Deliver the sheet BEFORE building any comp. Iterate here
   — it is 10x cheaper than comp notes.

   **LOOK GATE — check before delivering the sheet.** Use this collage grammar
   without implying Vox affiliation. Verify, don't assume:
   - Palette is the measured set — ink #1a1a1a, yellow #FFE619, process blue
     #66CFFF, specimen blue #58BCEC, greys #F2F2F2 / #8d9399, ground #fbfaf8.
     Treat bright blues as fills and accents. Use #3E87A8 or darker for small
     text on white, and pass the renderer's contrast checks.
   - Headlines are Archivo Black.
   - Every frame is a named recipe from the layout reference (evidence stack,
     zoom-isolation, two-panel compare, specimen grid, lower-third, newsprint
     layering, circle reveal). Label each frame with its recipe on the sheet.
   - The yellow circle appears as the recurring visual carrier.

   **The trap:** when the source document belongs to a company with its own
   design system — or the project folder already holds a brand capture,
   `frame.md`, or an earlier build in that brand — the pull is to inherit
   those tokens. Do not. `brand-faithful` is a DIFFERENT workflow for
   product-launch films. A brand skin here is an explicit user decision, never
   a default. Ask; don't substitute.
4. **VO** — record or TTS. The TTS input file is a PRONUNCIATION script:
   numbers written out ("eighteen thirty-nine"), names spelled as spoken.
   Transcribe the result for word timestamps — audio is the clock; every cut,
   pop, and highlight keys to a word time. A replacement VO = a full retime.
   Captions transcribe the PERFORMED read verbatim, not the script doc.
   TTS playbook: `npx hyperframes tts` first; if its bundled speech
   stack fails (old Python, espeakng-loader abort), install espeak-ng and
   call the Kokoro model directly with the CLI's cached model files. Use a
   TTS API only after the user approves its provider, data sharing, credentials,
   and cost. Then transcribe whatever produced the audio; the
   timestamps are the clock regardless of the engine.
5. **Build** — one HyperFrames comp, one clip group per beat, quiet caption
   rail (suppress cues wherever promoted on-screen text carries the words).
   Read [vox-text-overlays.md](references/vox-text-overlays.md) and
   [vox-collage-motion.md](references/vox-collage-motion.md) before writing timelines.
6. **QC gates (all numeric, all mandatory)**
   - lint/check: 0 errors.
   - Dead-time sweep: MAD every consecutive frame pair of the RENDER; any
     still run >3s is a planning bug — add a staged reveal, not wobble.
   - Seam measurement: for any zoom-isolation cut, render the last pre-swap
     and first post-swap frames, detect the carrier in both, verify centers
     within ~30px and sizes within ~10%. Fix by measuring, not eyeballing.
   - Event-density: per beat, largest gap between authored timeline events
     ≤3.0s (the motion reference explains why the MAD sweep cannot see
     creep-only holds).
   - Composition integrity: audit the final keyframe sheet against the layout
     reference's hard rules, item by item, logged.
   - Keyframe sheet: screenshot one frame per beat; look at it.

## Technique floor (anti-slideshow gate — declare at beat-map time)

Passing the defect gates does not make a film. A build that resolves every
beat to cards, side-by-sides, and lower-third text passes lint, seams, and
dead-time and still reads as a slideshow — the collage idiom lives in
techniques a cautious agent will never volunteer. So techniques are DECLARED
in the beat map, not improvised at build time: every beat names its layout
recipe AND its motion treatment from the motion reference's catalog, and the
film's distribution must clear this floor:

- ≥1 zoom-isolation swap — the camera pushes INTO a photograph, isolates the
  carrier, and cuts through it (numerically aligned per the motion reference).
- ≥1 inverse zoom-through arrival, spent on a payoff beat.
- ≥2 drive-pasts or scale traversals that exit at/through frame-fill.
- ≥1 background-dropped cutout (subject lifted off its plate) doing motion a
  flat card cannot — docking into a grid, riding a drive-past, anchoring an
  iso swap.
- ≥1 newsprint layering moment; the circle reveal (the brand carrier).
- CAPS: static-card / side-by-side layouts ≤ one third of beats; no two
  consecutive beats share the same layout recipe or the same treatment.
- When a photograph with interior depth is on frame, the camera enters it
  rather than drifting over the card row — flat drift over cards is the
  slideshow tell. Entering is governed by the zoom-in contract below.

**The zoom-in contract.** Pushing into a photograph promises the viewer the
payoff is INSIDE the image. Exactly two legal continuations:
1. **Background dropout** — the subject lifts off its plate and becomes the
   carrier (iso swap, dock, drive-past);
2. **Full-frame hold + callouts** — the image holds at/near full-bleed while
   annotations draw ON it (labels, arrows, attention windows).
A push into a photo that then cuts to an unrelated composition is banned —
that is a transition wearing a technique's clothes. If neither payoff serves
the beat, do not enter the photo.

Contract boundaries (what counts as "entering"): a sustained push whose
origin sits inside the image and that reaches near-full-bleed. Seam-scale
zooms (~0.2s whole-scene mechanics) and sub-10% camera creeps are different
categories and are not entries. An element driving AT the camera is the
mirror of an entry and obeys the same contract (it must already be a
dropped-out carrier, never a flat card flying at the lens). A traversal may
exit through frame-fill only into the same image or into the beat its own
motion caused — never into an unrelated composition.

QC: the beat map logs the treatment distribution table; the final keyframe
audit verifies each declared treatment actually appears on screen (the seam
verifier already measures the zoom-isolation numerically). A film that
cannot clear the floor honestly is a planning bug: re-plan the beats, do not
pad with decoration. When the floor's minimums and the zoom-in contract
conflict, the contract wins and the technique is cut — a missing technique is
a smaller defect than an unmotivated one.

## Structural spine (weights of a 60s cut)

This weighted spine is authoritative. THE FAMILY (see the script reference) is
the back half of FAMILIAR — more instances of the recognition, not a new beat.
THE ARTIFACT BEAT sits between STORY and MECHANISM in the script reference's
spine too; when the two references seem to disagree, this list wins. In source
mode, spine beats the source cannot fill honestly (SECOND WIND, the person in
DIG) are CUT and their weight redistributed — the cut-don't-fake rule outranks
the spine's completeness.

FAMILIAR 15% → DIG (person + date named) 5% → STORY 15% → THE ARTIFACT BEAT
10% → MECHANISM the viewer verifies on screen 20% → SECOND WIND (a technology
removes a constraint) 15% → THESIS in the yellow circle 10% → CLOSE mirrors
the open 10%.

## Non-negotiables inherited from the motion layer

- [motion-continuity.md](references/motion-continuity.md) governs seams. Make
  hard-looking swaps land inside a verified continuation seam; a literal
  static-to-static cut is not exempt from the seam gate.
- Real assets only — PD archives (Wikimedia Commons API, LOC), flagged
  recreations when a scan is missing. Recreating artifacts with shapes reads
  as slop.
- Highlights always animate on per the text-overlay reference.
- Elements step at 12fps over smooth eases; camera moves stay smooth
  per the collage-motion reference.
