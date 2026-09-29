---
name: flux-3-product-ads
description: Use when building a finished product ad from FLUX 3 - shot design, voiceover, action-to-word sync, evidence-gated copy, deterministic assembly, and QC gates that catch clipped audio, floating products, off-model plates, and reports that claim a pass the build did not give.
metadata:
  author: Black Forest Labs
  version: "1.3.0"
  tags: flux, flux-3, bfl, product-ad, commercial, voiceover, assembly, copy, editing, qc
---

# FLUX 3 product ads

A finished spot is two jobs, not one. FLUX 3 generates picture and voice. A
deterministic pass cuts, times, captions and masters them. Keep the boundary
sharp: the model handles what only a model can, and everything a computer can
compute exactly stays out of the model's hands.

Route facts this skill depends on live in `flux-3-generate`. Read it first for
`/v1/flux-3-video`, polling and download behaviour. Continuation behaviour, including
what a `v2v` link actually returns, lives in `flux-3-keyframes-continuation`.

Everything here has been run at 12, 30 and 60 seconds. Where a rule only holds at one
length, it says so. **Assume nothing written for a three-shot ten-second spot
generalises without being re-tested at length**: on the run that produced this
revision, two pieces of timing logic that were correct at 10 seconds turned out to
have a silent correctness bug and a complexity bug that only appear in a longer read.

## Shape of the work

1. Design shots that survive generation.
2. Generate picture plates and VO in the same round.
3. Screen VO by machine, then listen.
4. Derive timing from the audio.
5. Assemble deterministically.
6. Gate on measurements, including the failures that look like passes.

## 1. Shot design

Three cuts carry a 10-second spot: **reveal, proof, payoff**. Reveal establishes the
object, proof shows it doing the one thing the copy claims, payoff lands the brand.

Longer spots need more beats and more plates. A plate yields roughly 4 to 5 seconds
of usable middle once a dissolve is allowed for, so **shot count is length divided by
about 4.5, rounded up**, and a shortfall does not degrade gracefully: it fails the
build outright with no legal cut placement. Measured: 12s took 3 plates, 30s took 6,
60s took 11. A 60-second spot planned with 9 plates could not be cut at all.

At 30 seconds and beyond, reveal/proof/payoff no longer fills the time. What worked:
hook on the material, the object whole, a detail, the mechanism, a state change, what
the product does for you, brand. The structure that matters is that each beat earns
its own shot, not that it has three parts.

**Anchor motion at its endpoints.** A generated clip is trustworthy at its first and
last frame and inventive in between. Motion whose midpoint is implied by its endpoints
survives; motion that requires the model to invent geometry does not.

Works: a highlight travelling across a surface, a collar rotating through a short arc
and stopping, a handle rising and stopping, a lid parting slightly.

Two shots that *appear* to work and do not: **a hand drawing an ink line across
paper**, and **a phone descending into frame and landing on a product**. Both were
predicted to fail as "travel" and "an object entering the frame". Both arrived
looking correct, passed every signal gate, went into masters, and were rejected on
sight. The pen's ink ran ahead of the tip while the paper slid underneath; the
"phone" was a featureless slab as wide as the pad it landed on. Arrival is not
correctness, and this is the trap: the failure mode of a *nearly* achievable shot
is a plate that is wrong in the object rather than broken in the signal, which is
invisible to every measurement. See the semantic gate in section 6.

Fails: multiple revolutions, and rotation of two bodies at once. A crank asked for 2
to 3 full revolutions rotated to about 180 degrees, then deformed and vanished as the
arm occluded itself. A knurled collar asked to spin two revolutions *while* the head
it sits on tilted produced no motion at all: an inert clip where neither action
happened.

The predictor is not travel and not occlusion. It is **whether the model must invent
geometry it has never seen**. A hand crossing frame is a rigid body with a known
silhouette. A descending phone is a rigid body. A crank going around 720 degrees has
to render its own far side, and that is where it dies. Design against invented
geometry, not against movement.

**A quarter-turn is not a safe fallback for a rotation shot, it is an invisible one.**
The safe version of the failed collar shot technically succeeded and was still
unusable, because a small rotation of a knurled ring at macro reads as nothing
happening. When a rotation shot fails, the shot that replaces it should be **light
moving across a static object**, which is the most reliable motion in the system and
the one that consistently looks alive.

**When an object must arrive in frame, generate it leaving and reverse the clip.**
This is the highest-leverage trick in the section, because it converts an
invention problem into a translation problem. Three attempts at the same shot, one
variable:

| Attempt | Approach | Result |
|---|---|---|
| 1 | describe a descending phone; keyframe contains no phone | slab as wide as the pad |
| 2 | describe the phone in far more detail (two-thirds pad diameter, 8mm thick, dark glass front, metal rails, rounded corners, explicit no-warp instruction); same phone-less keyframe | still a slab, now tilted and overhanging the pad |
| 3 | keyframe already contains a correctly proportioned phone; generate the phone *lifting away*; `ffmpeg -vf reverse` in post | correct phone, correct scale, constant through the move |

Prompt detail did not fix invention. Removing the invention did. If the object is
in the keyframe, the model only has to move something it can already see, and
scale cannot drift because it was never chosen by the model. Cost: one filter.

Two things to watch. Author any lighting change in the direction that reads
correctly *after* reversing, and check the source still's camera height against its
neighbours, since a still shot for a different purpose may not cut with them.

**Reversing moves the action to the other end of the clip, and any timing you
already derived is now wrong.** This is the cost the trick hides, and it surfaces
as a sync failure in a spot that was passing before. The lift plate peaked at
5.79s of a 6.04s clip, a quarter-second before the end. Reversed, that same peak
sits at 0.17s. Nothing else changed: same duration, same frame count, same file
size class.

That matters because a plate can only be slipped *later* into its segment, never
earlier than its own first frame. So the reachable window for an action collapses
to roughly `[peak - segment_slack, peak]`, and an action at 0.17s can only ever
land in the first fraction of a second of its segment. The anchor word chosen for
the pre-reverse plate, several seconds in, became permanently unreachable, and the
build reported it correctly as a clamp:

```
slip : shot 3 in=0.00s -> action 14.32s vs word 15.62s (-1.30s)
       CLAMPED (reachable 13.00-14.32s, word at 15.62s)
```

The trap is that this looks like drift. The plates were byte-identical to the run
that passed, the VO was untouched, and the durations matched to the sample, so
every "did something move?" check comes back clean while the numbers disagree with
a note written a day earlier. The thing that moved was inside the file.

Two rules follow. **Re-derive anchors after any post step that changes where the
action sits in the clip**, reversing above all, and treat a reversal as a new plate
rather than an edit of the old one. And **when a reversed plate needs an early
action, anchor it to an early word**: a landing that peaks in the first frames
belongs on the first word of its line, not the word that named the motion when the
clip ran forwards.

**Test the prediction rather than trusting it.** Give a risky shot two prompts in the
same brief, a `hard_prompt` and a safe `prompt`, generate both, keep both. One extra
job per risky shot is what keeps this section honest as the model improves, and it is
how the two "impossible" shots above were found.

**Name the grounding in every prompt.** Say the product's contact shadow and its
reflection explicitly. A product can hold identity and motion perfectly and still look
pasted onto the frame because nothing defended its shadow. This passes identity checks
and reads as fake instantly to a human.

**Camera lock is advisory.** "Locked camera, no push-in, no pan, no zoom" still permits
parallax and drift. Design shots that tolerate a little movement rather than expecting
the prompt to forbid it.

## 1b. Reference stills come first, and the model gets a vote

Every plate inherits its still, because `i2v` treats the keyframe as literal. A still
that is wrong in a way you can live with poisons every clip generated from it, so the
reference pack has to be right before any video job runs.

**When the product is real, the pack is derived from the photograph, not written from
scratch.** This is the easier path and it skips the entire failure class below, because
no invariant paragraph has to describe the object well enough for a model to build it.
Take the supplied photo as the canonical still, then generate each remaining angle from
it with FLUX 2 `input_image` identity carry, seeded so the pack is reproducible. Write
the invariants anyway, by reading them off the photograph: they are what the identity
and semantic gates check against later. On a run built this way from one real product
photo, three generated angles held every named feature and no still needed regenerating.

Two things this does not buy you. The still is faithful and the *video* still drifts,
so the interior-frame and identity checks below apply unchanged. And a real photo is
usually a catalogue shot on seamless white, which gives you no set to cut to: every
plate looks like the same photo unless the shots differ in framing and scale, so design
the pack for genuinely different crops.

Expect the model to overrule the spec, and read it as information. On a three-product
run, two products came back with the model quietly substituting its own design: a
light channel specified as unlit rendered lit in every frame, and a lamp specified
with a two-segment elbow arm rendered as a single post with a yoke-mounted head in all
seven angles.

Both refusals were **coherent**: one alternative design, held consistently across every
angle. That is the signal. A model that disagrees at random gives you noise; a model
that disagrees identically seven times is telling you the invariant paragraph
describes something it cannot build. **Rewrite the spec to match what it reliably
builds, then regenerate.** Fighting a coherent refusal costs jobs and loses.

Regenerate a still when the error is one the video stage will amplify: stray text on a
prop, a wordmark in the wrong place, an object overhanging its base.

**Check identity across the pack, not one still at a time.** A pack can be clean
plate by plate and still be incoherent, because "is this a good photo of a lamp?"
is a different question from "is every one of these the same lamp?" On the lamp
above, the pack mixed two incompatible designs across its angles; each still looked
fine alone, and every plate generated from them inherited whichever design its
keyframe happened to carry. Pick one still as canonical, then compare each of the
others to it on **named, falsifiable features** rather than overall impression:

```
base:   shallow domed profile curving in one arc, vs a flat cylindrical puck
        with a vertical side wall
post:   smooth and unbroken from base to head, vs a collar, ring, knurling
        or joint partway up
head:   plain green cylinder roughly twice as long as wide, vs short/fat
        or a knurled metal barrel
ring:   exactly one knurled ring, at the FRONT of the head encircling the
        lens, vs any knurling on the post or base
```

Each feature names the correct form *and* the wrong one it gets confused with,
which is what makes a verdict checkable. Run the same comparison over the finished
plates too, at least twice per feature, and fold unanimously as with the semantic
gate in section 6. On a 14-plate run this returned 13 consistent and one off-model,
where a thin gold bezel had changed the head's proportions. The plate it flagged
had passed every signal gate. Its hard-motion twin, generated as the safe/risky
pair described above, was clean and already on disk, so the fix cost nothing.

This is worth doing before generation and again after, because the two runs answer
different questions: the first stops a poisoned pack, the second catches the plate
that drifted anyway.

**Never let a failed step's stale output become the next step's input.** When a
chained link failed, the runner picked up the previous day's file of the same name
and fed it to the following link, which then succeeded and produced a plausible
clip built on the wrong material. A failure that leaves the old file in place is
indistinguishable, to the next step, from a success. Check that a chain input is
newer than the run that is consuming it, or write links to run-scoped names so a
missing file is missing rather than stale.

## 2. Generate picture and VO together

Finished product ads carry voiceover. Budget it in the first generation round,
never bolt it on after picture lock: the VO determines the length of the spot,
so generating it last means re-cutting everything.

For voiceover generation, music beds, audio layering, speakability checks, and
deterministic audio finishing, use `flux-3-audio-dialogue`. This skill covers
ad-specific timing and assembly: how the VO sets spot length, how paragraphs
join at designed pauses, and how the mastered stem feeds the cut pipeline.

Get VO from audio-only jobs: a voice-booth scene whose picture is discarded and
whose audio is harvested. Generate at least two scripts against two speaker
profiles, because takes are not interchangeable and you want a real choice.

Do not use native picture audio in a finished spot. Generate picture silent.

**`duration` is a tempo control, not a length estimate.** The clip comes back at
exactly the length you ask for and the read stretches to fill it. The same 27-word
script, same speaker, asked for three lengths:

| asked | returned | words/sec |
| --- | --- | --- |
| 11s | 11.01s | 2.45 |
| 14s | 14.00s | 2.11 |
| 18s | 18.02s | 1.50 |

The script was delivered completely and correctly every time. Only the pace changed,
and at 18s it does not pad with silence, it drags. So pick the speaking rate you want
and derive the length: `duration = words / rate`, with roughly 2.1 to 2.5 words per
second reading unhurried and confident. Do not pad the estimate for "room to breathe";
that slows the delivery instead of adding a pause.

**One audio job caps at 20 seconds, about 45 words at a good pace.** A 30-second spot
needs around 75 words and a 60-second spot around 150, so any longer read is generated
**one paragraph per job** and joined in post at a designed pause. This is also better
writing, because ads pause. Trim each paragraph to its own speech before joining;
stacking booth room tone produces an audible seam.

**Generate a music bed the same way** whenever the spot runs past about 20 seconds.
Silence between paragraphs that is fine at 10 seconds sounds broken at 60. A bed is an
audio-only job with no speech in the prompt, looped with a crossfade to length, and
ducked under the voice with a sidechain compressor keyed off the VO. Attenuate the bed
first and let the duck shape an already-quiet bed: a bed loud enough to need heavy
ducking pumps audibly on every phrase.

## 3. Screen VO by machine, then listen

Transcribe each take and compute word error rate against the script. This
catches dropped and mangled lines cheaply.

**Invented brand names need phonetic matching, not exact matching.** ASR has
never seen your product name and will spell it plausibly wrong: "Ferrolane"
came back as "Feraline", "Feralaine" and "Fairlane". An exact-token check
rejected every correct take. Score brand names by phonetic similarity over a
sliding window and treat a close match as evidence the name was spoken.

Machine screening cannot approve a take. Pronunciation, cadence and synthetic
artefacts need a human ear. Mark every invented name unverified until someone
listens.

**Derive the brand tokens from the brief, not from a table.** A screening step with
the product names hardcoded works for exactly the products it was written against,
which is not a reusable skill. Derive them: first word of the product name is the
brand, and a letter-plus-digits token is the model code.

Model codes need digit-word folding in both directions. "P2" transcribes as "P two"
about half the time, and an unfolded comparison charges a correct take a word error it
did not earn.

**Watch for a tail at true digital silence.** One take in six ended at -91 dB in its
final 0.35 seconds: not room tone, an empty buffer, where the other five sat between
-30 and -40 dB. The clipped-tail gate looks for speech that is still loud at the end,
which is the opposite failure and passes this happily. A booth take with no room tone
at its tail will not match its neighbours' noise floor across a paragraph join.

## 4. Derive timing from the audio

The VO is the master clock. Everything else is measured from it.

**Find the end of speech by energy, not by word timestamp.** A transcriber's
final word timestamp marks where a word stops being intelligible, not where its
energy reaches the noise floor. On a real stem the transcriber reported the last
word ending at 9.76s while audible decay continued to about 9.9s. Trimming
there clipped the final word off the master, and every duration and loudness
gate still passed.

Detect silence at a true noise floor instead, and **count only silence that
runs to end of file**. Taking the last silence region is a second, subtler bug:
on that same stem the final gap sat *before* the last word, so trusting it cut
the master even shorter than the timestamp did.

**Measure the noise floor per take; a fixed threshold finds nothing.** These
booth takes do not share a floor. One measured -33.2 dB, so a -45 dB
`silencedetect` threshold returned zero silence regions on a read with four
audible pauses in it, and every pause-based cut placement had nothing to work
with. Read the floor with `astats` and set the threshold a few dB above it: at
floor+6 dB that same take resolved four clean sentence pauses, while floor+4 dB
fragmented them into six and floor+8 dB began eating quiet consonants. Derive
the number, and record which floor produced the cuts you shipped.

**Place cuts in measured gaps.** Candidates are pause centres, best first:
sentence pauses at a deep floor, then word gaps at a shallower one. Never cut
mid-word. If no placement fits, fail loudly and say why: the fix is a longer
plate, another shot or a shorter read, not a cut inside a word.

Score placements on gap quality **minus** pacing imbalance. Gap quality alone
picks the single best-hidden cut in the read and cheerfully produces a 1.6
second opening shot against a 4.9 second middle.

**Search by dynamic programming, not by scanning combinations.** Both inputs to the
combinatorial blow-up scale with spot length: a longer read offers more candidate
pauses and needs more cuts.

| spot | candidates | cuts | combinations |
| --- | --- | --- | --- |
| 12s, 3 shots | 29 | 2 | 406 |
| 30s, 6 shots | 69 | 5 | 11,238,513 |
| 60s, 9 shots | 90 | 8 | 77,515,521,435 |

A brute-force scan is fine at 10 seconds, slow at 30 and does not return at 60, where
it fails by hanging: the worst failure mode, because it looks like slowness. Every
term in the score is a sum over segments or over chosen cuts divided by a constant, so
the score decomposes per segment and the optimum builds left to right in
O(shots x candidates squared).

A faster search that picks different cuts is a regression, not an optimisation. Assert
the fast search returns what the brute force returns on cases small enough to scan,
comparing ties by score rather than by list identity.

Every segment must fit the plate it comes from. Check it. A hand-measured cut
once demanded a 5.72s segment from a 5.04s plate.

**Slip each plate so its action lands on the word that names it.** This is the
single highest-leverage edit decision available, and taking the segment from the
middle of the plate throws it away.

Measure where the action is: `signalstats` YDIF gives a per-frame luma delta,
which smoothed over five frames is a usable proxy for when the thing happens.
Skip four frames at each end, or the decode boundary and the fade read as peaks.
Then declare, per shot, which spoken word the action is *about*, and choose the
in-point so the two coincide.

Measured on a real pair of spots before this existed: the shell finished opening
1.70s after the voice said "opens flat", the collar clicked 2.33s after "one
honest click", the handle rose 1.00s before its word. A viewer cannot articulate
that, but it is the difference between an ad and footage with narration on top.

Fold the anchor into the cut search too. A cut that hides beautifully but leaves
a shot no room to slip is worse than a slightly more visible one that lets the
picture and the voice say the same thing at once.

Gate the result. If an action lands more than ~0.6s from its word, fail. When
the plate physically cannot reach the word, say so with the reachable window:
the fix is regenerating with the action earlier or re-anchoring to a word the
plate can actually hit, and both are honest. Silently absorbing the miss is not.

**Choose the anchor word after measuring the plate, not while writing the script.**
Picking an evocative noun and hoping the plate can reach it missed on three shots out
of nine across two spots. Generated plates put their action early far more often than
a writer expects: one peaked 0.21s in, against an anchor word at 0.84s, so the
reachable window had closed before the word was spoken. The reachable window is
computable before you commit to a word, so compute it.

Re-anchoring is often the better edit on merit anyway. A macro of an engraved wordmark
re-anchored from "looked" to the brand name is both reachable and truer to what the
shot shows.

**Regenerating to move an action is a new plate, and it needs the semantic gate
again.** Faced with a clamp, the obvious fix is to re-prompt the shot with the
action early. It worked on the timing and broke the depiction: asked for a lever
that pivots down in the first half second and then holds, the regenerated clip
had the lever start horizontal, rise, and settle back down, so its measured peak
at 0.92s was the *raise* rather than the close. Every number improved and the
clip showed the wrong thing. The plate that shipped was the original, re-anchored
from "switch" to "water", which landed the close 0.05s off its word and reads
truer besides, since the lever closing is what holds the water. Try the
re-anchor before the regeneration: it costs no jobs, and a plate already through
the gate is worth more than a fresh one that has not been looked at.

**Resolve anchors monotonically.** Take each anchor's earliest occurrence *after* the
previous anchor's, because shots advance through the read and so must their words. A
first-match lookup is correct only while no word repeats, which is an accident of short
scripts: a 30-second read said "light" twice, ten seconds apart, and the closing shot
anchored to the first one and reported a 10.18s miss no slip could satisfy.

**Not every shot has an anchor, and inventing one is worse than omitting it.** When a
shot's motion is a light drift rather than a discrete event, there is no word it is
*about*. Long spots have more of these. Leave the anchor null and take the segment from
the plate's middle.

**Order the shots to follow the script, and treat shot order as a timing lever.**
A shot can only be anchored to a word inside its own segment, so a plate whose
action names a word late in the read cannot sit early in the cut. A macro of the
lever was clamped 1.8s from "switch" in segment two and reachable in segment
three, and swapping it with the wide payoff shot fixed the anchor without
regenerating anything. Reordering is free, so try it before re-prompting: the
constraint is which segment a word falls in, not the plate.

Take a segment from the middle of its plate only when no anchor applies.
Generated clips are weakest in their first frames, where the image settles, and
in their last.

## 5. Assemble deterministically

No model call happens after generation. Same inputs, same master.

Drive it from a manifest that carries **content only**: which plates, which VO,
what the copy says. Cut points, spot length, loudness target and end-card
treatment are all derived from the media at build time. A per-product number in
a config file is a number someone has to re-measure by hand for the next
product.

**Decide the end card from measured luminance.** Sample the region the text will
occupy and add a scrim only when it is too bright for white copy. White text
over a light sand-coloured case was nearly unreadable while identical text on a
dark set needed nothing. Measuring separates those cases without a flag.

If you need a scrim, run the gradient to the frame edge. A floating band has two
visible edges to hide; an edge-anchored gradient has one.

**Target loudness the material can reach.** These stems are peak-limited, not
level-limited: one measured -21.3 LUFS integrated with true peak already at
-4.2 dBTP. Reaching -14 LUFS demands about +7 dB, which drives true peak well
past the ceiling, so the normaliser clamps and lands short no matter what you
ask for. Compression recovered 0.4 LU and damaged the approved read.

Use the normaliser's own first-pass report of what it can deliver under the
peak ceiling, and gate against that. Do not derive the ceiling from a single
transient sample peak, which is far too pessimistic. And do not lower a target
until a gate turns green; that is not a pass, it is a hidden failure.

## 6. Gate on measurements

Duration, resolution, frame rate, audio presence, loudness and true peak are
table stakes. They are also insufficient. Add the gates that catch failures
which look like passes:

- **Clipped tail.** Measure energy in the final quarter-second before the
  closing fade. Still-loud speech there means the master ends mid-word.
- **Black frames in the body.** A dropped plate or a bad transition offset
  shows as black that every other gate passes. Exclude the intended closing
  fade.
- **Grounding.** Crop and magnify the product base mid-shot. A missing contact
  shadow survives identity and motion checks.
- **Interior frames.** Sample at several points, not just first and last.
  Geometry decays in the middle, which is exactly where a first-versus-last
  comparison cannot see.

**Validate a gate against a known-bad file.** A gate that has never failed is a
guess. Hard-cut a master mid-word and confirm the gate fails it: on real
material the intact file measured -91 dB in that window and the broken one -34
dB, so a -30 dB threshold would have passed the broken file. Threshold chosen by
inspection, then confirmed against the control.

**A master with no ending cannot be gated for a clipped one.** Where the read
finishes flush against end of file, the intact master measured -15.3 dB in its
final quarter-second and a deliberately hard-cut copy measured -13.8 dB. Those
are 1.4 dB apart, so no threshold separates them and the gate is decorative. The
fix is not a cleverer threshold, it is giving the spot a real ending: pad the
tail and fade, after which the same measurement read -inf against -13.8 dB for
the control. A finished ad wants that fade anyway, which is why this hid: the
missing ending was a creative defect and it disabled a gate on the way past.

### Signal gates cannot see meaning. Add a semantic gate.

Every gate above measures signal properties, and every one of them will pass a
plate that depicts the wrong thing. Two measured cases from one run:

- A pen "drawing a line" where the ink ran ahead of the tip, with blank paper
  visible between the tip and the end of the line. The paper slid; the pen
  barely moved.
- A phone "landing on a charging pad" that was a featureless grey slab as wide
  as the pad's full diameter. It arrived cleanly, which is precisely why the
  action-sync gate liked it.

Both passed duration, resolution, frame rate, loudness, true peak, black-frame
and sync gates, shipped into masters, and were rejected on sight by the first
human who watched them. The gates were not wrong; they answer *is this file
broken?* Nothing asked *is this the thing we said it was?*

The fix is a separate gate that samples labelled frames, tiles them into a
contact sheet, and puts a vision model in front of **falsifiable assertions**
taken from the brief. Rules that make it worth trusting:

- **Write assertions that a wrong depiction makes false.** "The clip looks
  good" is unusable. "All visible ink is behind or at the pen tip, and there is
  never a gap between the tip and the end of the drawn line" is a gate.
- **Require frame citations.** The judge must name which frames decided each
  verdict, or the verdict cannot be checked.
- **Run every sheet at least twice and fold harshly.** Only unanimous PASS
  passes. Any FAIL blocks, and round-to-round disagreement blocks as UNSTABLE. A
  judge that cannot reproduce its own answer has not checked anything, and this
  is not hypothetical: on a known-bad plate, two of five assertions returned
  opposite verdicts across two rounds of the same sheet. Majority-vote or
  single-round judging would have been a coin flip.
- **Give every product plate the universal four for free:** contact shadow
  present, geometry and materials constant across frames, no garbled or
  duplicated text, no dead or corrupted frames. Then the brief author writes the
  per-shot claims that would be lies if the plate came back wrong.
- **A pass here is evidence, not proof.** It does not retire the human watch. It
  stops obvious wrongness reaching the human, which is what buys back review
  capacity.

**The assertion set is the attack surface, not the judge.** The most expensive
mistake in this run was not a wrong verdict. It was a *right* verdict on an
incomplete question. A retry plate showed a convincing phone whose width really
was narrower than the pad's diameter, so the width assertion passed honestly, and
the plate went green while the phone came to rest tilted across the rim,
overhanging both sides. Nothing in the set asked whether it landed flat or fitted
inside the footprint. Every individual verdict was defensible and the gate still
shipped a wrong plate.

A false PASS from a thin assertion set is more dangerous than having no semantic
gate at all, because it arrives with frame citations attached. Two habits fix it:

- **Assert the resting state, not just the motion.** Where the object ends up
  (flat, inside the footprint, in contact) is the part a viewer reads as wrong,
  and it is the part a motion-focused assertion set forgets.
- **When a plate is rejected by eye, find which assertion should have caught it
  before writing a new prompt.** If none would have, the hole is in the set. Two
  of the four blocks in this run cited the defect precisely; one blocked on an
  unstable split about something else while the real defect went unasked. Right
  answer for the wrong reason is not coverage, and it fails silently the moment
  the accident stops happening.

**An assertion can be false by construction, and it will look rigorous.** "The
phone keeps a constant size and shape as it moves" blocked a *correct* plate. A
rigid body rotating from near-vertical to flat must foreshorten, so no true clip
could ever satisfy that sentence, and the judge's stated reason was an accurate
reading of the frames. Assert physical plausibility (edges straight, corners
square, no independent drooping) and say explicitly that perspective change is
expected. Test any assertion you rewrite against the known-bad material in the
same run: if the rewrite stops failing the bad plates, it was a weakening, not a
correction.

**Rewriting an assertion after seeing a verdict you dislike is how a gate dies.**
It is sometimes correct, as above. The discipline that keeps it honest is
mechanical: keep known-good and known-bad plates as fixtures, and re-run both
sides after every assertion edit. The bad plates must still fail for the same
stated reason. This is also why the loop is trustworthy when it works: a retry
that passes assertions **left untouched since the failure** is real evidence, and
one that passes only after the sentence moved is not.

**Inspect the gate's own evidence once, by eye, before trusting its verdicts.**
The first version of this tool built its contact sheet by feeding six separate
inputs to ffmpeg's `tile` filter. `tile` consumes successive frames of a *single*
stream, so it tiled the first frame, left the rest black, exited 0, and wrote a
plausible JPEG. The judge was shown one frame, asked about motion across six, and
answered anyway. Nothing in the exit code said so. A QC tool that fails silently
is worse than no QC tool, because it manufactures confidence.

**Never weaken a gate to get a green run.** Fix the material or state the
failure. Watch for the softer version of this: when a check fires, the tempting
move is to trim whatever number it complained about until it stops. A collision
warning got answered by shortening callout holds to 0.5s, which cleared the
overlap and left the claims too brief to read. The gate went green and the ad
got worse. If a fix makes the check pass by making the work worse, it is not a
fix, and the gate is measuring the wrong thing.

**A warning nobody acts on is a bug in the gate.** "Callout outlives its shot"
sat at warning level while a render shipped with a label surviving across a cut,
pointing at a feature no longer on screen. If a condition means the output is
wrong, it is an error.

**The QC file has to agree with the console, or the file is the one people will
believe.** The builder printed `FAILURES PRESENT` and exited non-zero for a spot
with two sync failures, then wrote `"pass": true` into `master-qc.json` for that
same spot. The sync check flipped the local verdict but the persisted record was
assembled from the *signal* gates' pass flag, which knows nothing about sync.
Anything reading the artifact instead of watching stdout saw a green spot. Write
the composite verdict, and write the failures alongside it so the record can be
audited without re-running the build.

**A per-item run must not erase the record of the items it did not build.** The
same file was rebuilt from an empty dict every invocation, so `--only kestrel`
silently deleted stonewell's entry. The file then described one spot while looking
like it described the project, which is the more dangerous state: an incomplete
record that reads as complete. Merge into what is already there, stamp each entry
with the time it was built, and say plainly which entries came from an earlier run.

Both of these are the same failure as the contact-sheet bug above, arriving by a
different route: the check ran correctly and the report lied about it. When a gate
and its artifact can disagree, test that they don't, by failing something on
purpose and reading the file rather than the terminal.

## Copy

On-screen copy invents claims faster than picture does, because writing a
plausible spec costs nothing.

**Require evidence for every line, and name which kind.** *Seen* means it is
visible in the plate the label points at. *Spec* means it is part of the
reference design. *Said* means the approved VO says it. A line with no evidence
does not ship.

Two labels failed this on real work: "TWO-STAGE LOCK" and "COLD-FORGED". Both
name mechanisms and processes that were never designed, generated or spoken.
They read as confident specifications and were simply invented, which in a piece
demonstrating a pipeline is worse than vague copy.

**Put the proof in the noun or the number.** "38 litres" beats "generous
capacity". Name the material and the part: *stainless body*, *walnut sleeve*,
*charcoal zip band*. Outcome adjectives (smooth, precise, effortless, honest)
assert something the plate cannot show, so they need the VO behind them or they
go.

**Name the part the way a person would.** "Telescoping stem" is nobody's word
for a handle.

## Editing

Three identical dissolves is not an edit, it is a default. It says the same
thing about every pair of shots when the relationships differ.

Keep the vocabulary small and give each treatment a job: a **hard cut** between
two views of the same object, where continuity is obvious and confidence is the
point; a short **dissolve** for a change of scale or subject; a two-frame
**flash** into the payoff, where the edit should feel like arrival. Sample the
flash colour from the plate's own highlights. White on a warm set looks like a
blown frame.

**Give the camera a move that finishes.** A push that runs at constant speed for
the whole shot reads as software. Ease it, arrive early, then hold: the hold is
what makes a move look intended.

**Add the imperfections generation leaves out.** Generated plates are optically
dead. Sub-pixel seeded noise on the transform (two octaves, roughly a pixel at
960px) reads as a rig rather than a weld, and light grain dithers the smooth
gradients that band after H.264. Both should be invisible and only missed when
absent. Seed them, so rebuilds stay byte-identical.

## Renderer choice

ffmpeg is enough for cuts, dissolves, captions, scrims, fades, loudness and
muxing, and it is already installed everywhere.

Remotion is worth it when the end card grows into real design: layout, web
fonts, data-driven variants, many sizes. It is React, so a gradient is one
CSS declaration rather than a generated alpha ramp overlaid at a computed
offset, and the studio gives you a scrubbable preview.

Two things to know before choosing it. Licensing: Remotion is free for
individuals and companies up to three people, and a company of four or more
needs a paid Company License. Audio: the browser plays a stem as it is, with no
loudness normalisation, so an unmastered take renders at its raw level. Master
audio with ffmpeg first and hand Remotion a finished stem.

Both renderers can consume the same derived timing. Keep the measurement in one
place and let the renderer be a choice rather than a rewrite. Matching them
exactly takes care: text placement differs because a caption filter positions
the glyph box while CSS includes the font's ascent leading, and a cross-dissolve
must start *at* the cut rather than finish there.

## Reference

`references/pipeline.md` is a reference design and implementation blueprint:
manifest schema, derived-timing export, both renderers, and the QC gate list
with the measured thresholds and negative control. The modules it describes are
not shipped in this repo; an agent builds them from the contracts there.
