---
name: motion-plan
description: Turn a script or timestamped transcript into a shot-by-shot motion plan — which lines earn an on-screen visual, which stay bare A-roll rest, what each visual must show, and how long it holds. Use BEFORE designing or animating anything in Remotion, HyperFrames, or After Effects. Triggers on "plan this edit", "what should be on screen", "storyboard this script", "beat map", "where do the animations go", or any request to animate a video that arrives without a shot list.
---

# motion-plan

You are the editor deciding **what the viewer sees and when**. Design and animation come later and are downstream of this document. Skipping this step is why AI edits look like decorated transcripts instead of edited videos.

**Hard rule: never generate a visual for a line you have not classified.** Decorating every sentence is the single loudest slop signal — it flattens emphasis, exhausts the viewer, and makes the piece read as automated.

## Input

One of:
- A script with beats, or
- A timestamped transcript (JSON/SRT/VTT with word- or phrase-level times), or
- A cut video + its transcript.

Timestamps are not optional for a real edit. Without them you cannot compute durations, and every visual will be the same length — a tell. If you only have a script, say so and produce the plan with **relative beat weights** instead of seconds, flagging that timings need a pass after the audio exists.

## Step 1 — Segment into beats

A beat is one complete idea, usually one to three sentences. Do not segment on sentence boundaries mechanically; segment where the *idea* turns. Record for each beat: index, start, end, duration, verbatim text.

## Step 2 — Classify every beat

For each beat, ask one question: **is this line load-bearing for understanding or for retention?**

Mark `VISUAL` when the beat matches a trigger. Mark `REST` otherwise. Rest is a deliberate choice, not a gap.

### Triggers (a beat needs a visual if it is one of these)

**Opening section** — higher density, because you are buying attention you have not earned yet:
1. **Claim or concept** — a new idea named for the first time.
2. **Number or stat** — any figure, percentage, price, count, or date.
3. **Chapter / section transition** — the structural spine.
4. **Promise or open loop** — "by the end of this you'll…", "and the crazy part is…".
5. **Autobiographical proof** — a specific personal fact used as credibility.

**Body section** — lower density:
1. **New information** — something the viewer did not have thirty seconds ago.
2. **Number or stat** — same as above; numbers always animate.
3. **Re-stimulation** — the first beat after a long dry stretch (>15s without a visual), even if it is not otherwise remarkable. Its job is to reset attention.
4. **Proof** — evidence, example, screenshot, receipt, result.

### Rest triggers (a beat must stay bare)

- Time jumps and scene changes in a story ("nearly twenty years later…") — the pause *is* the transition.
- Emotional or conclusive lines where the speaker's face carries the meaning.
- The opening statement of a piece, when the goal is speaker-to-viewer connection.
- Immediately after a dense visual sequence — the eye needs a floor.
- Anything you cannot state a clear *purpose* for. If the visual would only be decoration, it is REST.

## Step 3 — Set density and check it

Compute visuals per minute and compare against the target for the format:

| Format | Opening | Body |
|---|---|---|
| Long-form talking head (8–15 min) | 4–10 / min | ~2 / min |
| Short-form vertical (30–90s) | animate the value lines only; expect **6–10 visuals total**, with 2–4 REST beats interleaved | — |
| Documentary / explainer VO | 3–6 / min throughout; VO has no face to rest on, so rest is a held frame, not a cut to nothing | — |

If your plan is outside these bands, fix the plan — do not rationalize it. Over-density is the common failure.

**Rest ratio floor: at least 20% of runtime must be REST.** A plan with no rest is a broken plan.

## Step 4 — Recurring elements

Identify anything that appears more than once — chapter titles, a section counter, a recurring product mark, a repeated framing device. **Reuse one design for all instances.** Same layout, same motion, different content. Recurrence is how a viewer builds a mental map of the structure; re-inventing it each time destroys that and reads as inconsistency.

Name the recurring element once in the plan and reference it by name in every beat that uses it.

## Step 5 — Write the shot for each VISUAL beat

For each, specify:

- **Subject** — the one thing the frame is about. One subject. If you write two, split the beat or drop one.
- **Archetype** — pick from `motion-design` (overlay / full-frame UI / illustrated / dimensional / typographic). Do not invent per-beat looks.
- **On-screen copy** — the exact words. Usually 3–8 words, pulled or compressed from the line. **Never the full sentence** — captions already carry the sentence; the super carries the emphasis.
- **Accent word** — the single word that gets special treatment. Exactly one per frame.
- **Duration** — see below.
- **Entry / exit** — how it arrives and leaves, in one clause.
- **Why** — one clause naming which trigger fired. If you cannot write this, the beat is REST.

### Duration rules

- A visual **covers its line**. It enters on or just before the first word and leaves within ~0.4s of the last.
- **Floor 1.8s.** Anything shorter reads as a flicker and cannot be parsed.
- **Ceiling ~7s** for a single static composition. Past that, the frame must evolve — a second element enters, the camera continues moving, or it transitions to a paired shot.
- **Vary them.** If your durations cluster within ±0.3s of each other, the edit will feel metronomic no matter how good the individual frames are. Deliberately mix short (2s) punctuation against longer (5–6s) hero beats.

## Step 6 — Output

Emit a markdown table plus a short preamble. Nothing else — no prose walkthrough.

```markdown
## Plan: <title>
Runtime <M:SS> · <N> visuals · <N> rest · density <x>/min · rest ratio <y>%
Recurring: <name> — <one-line description>, used at beats <indices>

| # | In | Out | Dur | Type | Subject | On-screen copy | Accent | Motion | Why |
|---|----|-----|-----|------|---------|----------------|--------|--------|-----|
| 1 | 0:00 | 0:04 | 4.0 | REST | — | — | — | — | opening connection |
| 2 | 0:04 | 0:09 | 5.2 | illustrated | person alone at desk, night | obsession compounds | obsession | push-in 1.08→1.00 | claim |
```

Then a one-paragraph **pacing note**: where the density spikes, where the floor is, and any beat you were unsure about. Flag unsure beats explicitly — do not silently guess.

## Handoff

The plan is the contract. `motion-design` reads Subject + Archetype + copy and produces frames. `motion-animate` reads Duration + Motion and produces timing. Neither may add a visual that is not in this plan, or change a REST beat to a VISUAL, without saying so.
