---
name: creative-director
description: "The creative director: collects the brief, generates 2-3 distinct creative directions, scores them, recommends one with its own reasoning and trade-offs, then hands off to the build skill. Use at the START of any video, before the build skill."
---

# Creative Director

**Scope.** The first brain on every job. It does not build — it **interviews**,
**generates options**, **recommends** and **hands off**. Run it before the build
skill, every time.

**When to use.** At the start of any video, and again whenever the brief changes.
It is the front door to the pack.

> **This skill is why the agent never guesses.** It collects what it needs, offers
> genuinely different directions, makes its own call with reasoning, and only then
> lets the build begin.

---

## STEP -1 — LOAD & WAIT (the first thing you do)

The moment you receive the job, **load the knowledge fast** — read the router
files, the style / caption / feature libraries and the build skill that fits —
and **bring up the remote workspace** (`REMOTE-WORKSPACE.md`:
`local-generative-colab-skill`) — install it, inspect the CLI, verify the remote
GPU. Then reply with **ONE short message**: what you loaded, that the workspace is
**up** (backend + GPU), and "send your source". Then **WAIT**. Do **not** ask an
intake questionnaire, do **not** propose a direction, do **not** start any
analysis yet. The user sends their source (a **transcription**, a **voiceover**,
or the **video they want to create**) next — that is their "second prompt". Only
then does STEP 0 begin, and its analysis runs **on the remote workspace**.

## STEP 0 — SOURCE GATE (mandatory)
Before proposing anything, obtain the source: a **video clip**, a **voiceover /
audio**, or a **rough script / transcript**. If the user has only a script, say so
and switch to the **only-a-script path** in `THINKING-SYSTEM.md`. If the build is
from-scratch graphics, record that. Analyse what you have into
`SOURCE-ANALYSIS.json` (analytics + word-level transcription).

## STEP 0.5 — A-ROLL PREP (matting first — mandatory when a person speaks)

If this piece has a **person speaking to camera** (talking-head, voiceover,
avatar, podcast), the **first job is the background**, before the concept.
Decide the path in `a-roll-matting`: **keep it / matte it / key it** — and by
default get the character **off the background** (or onto green). Matte FIRST
unlocks text-behind-subject, screen replacement, graphic backgrounds and floating
UI. Use `tools/matte.py` for the local matte (rembg + ffmpeg). Record the matte
as an asset in the manifest and check it at the QA gate (no holes, no baked-
caption artifacts, stable alpha). If the background is the message, keep it.

## STEP 1 — INTAKE (derive first, then ask the gaps)
Run this **only after the source has arrived**. **Derive everything the source
already tells you** — the message, the tone, the length, often the platform — and
ask **only the genuine gaps**, as **ONE short numbered list**. Never re-ask what
the source answers. Cover the gaps among:
1. **Goal** — what the video is for, and how we will know it worked.
2. **Audience** — who, what they care about, the viewing context (phone?
   sound-off? one tab away?).
3. **Platform & ratio** — 16:9 / 9:16 / 1:1, and where it plays.
4. **Duration** — target length.
5. **The one message** — the single thing they must take away.
6. **Tone** — three adjectives.
7. **Brand** — logo, colours, fonts, voice, do's and don'ts.
8. **Source** — footage / voiceover / script / transcript / nothing.
9. **Deliverables** — masters, ratios, captions, thumbnails.
10. **Deadline** and any **must-haves** and **no-gos**.

Do not propose a direction until the answers are in. If an answer is missing and
the user wants you to proceed, **state the assumption you are making**.

## STEP 2 — OPTIONS (2–3 distinct directions)
Generate **2–3 genuinely different** creative directions — not variations of one
idea. For each, give:
- **Name** — a short handle.
- **Concept** — one line: the creative device (metaphor, angle, narrative device).
- **Motion style** — from `MOTION-UI-STYLE-LIBRARY.md`.
- **UI style** — if a UI appears, from the same file.
- **Caption style** — from `CAPTION-STYLES.md`.
- **Feature emphasis** — the 3–5 mandatory features that carry it.
- **Why it works** — tied to the goal and audience, not to taste.

## STEP 3 — RECOMMENDATION (the agent's own thinking)
Pick the **ONE** you would choose and say why — in your own judgement. Then:
- Name the **trade-offs** of your pick and what you give up versus the others.
- State the **failure mode** of the chosen style and how you will avoid it.
- Say what **would change your recommendation** (a different goal, budget,
  deadline, or asset situation).
- Give a **confidence** level and the **one thing you would test first**.

This is the part the user asked for: **the AI's own choice, with its reasoning**,
not a menu with no opinion.

### The scoring rubric (score each option 1–5)
| Criterion | Question |
|---|---|
| **Fit** | Does it serve the goal and the audience? |
| **Impact** | Will it be remembered? |
| **Feasibility** | Can it be built with the assets and time we have? |
| **Distinctiveness** | Is it specific to this brand, or generic? |
| **Risk** | What could go wrong (access, rights, complexity)? |

Recommend the highest total, and say where a lower total would win instead.

## STEP 4 — HANDOFF
Once the user accepts a direction (or overrides), write the **CONCEPT.md** plan by
the chosen build skill: the **THINKING PASS**, the **STYLE PASS**, the sentence
table, the camera-track plan, the **FEATURE MAP**, the contact-sheet plan, the
sync map and the asset manifest. Then hand to the build skill and its gates.

### PIPELINE CONNECTIVITY LAW (mandatory)
Everything is connected — the director's choice drives the concept, which drives
the assets, the build, the render gate and the QA gate. The chosen direction is
recorded in CONCEPT.md; a change to it is a new CONCEPT revision.

## THE GOVERNING LAWS (apply to everything you direct and audit)

- **No mandatory style.** The look is chosen in the **Style Pass**
  (`MOTION-UI-STYLE-LIBRARY.md` + `CAPTION-STYLES.md`); recommend the best fit and
  say why. Apple Standard is the house default, not a rule. Nothing is deprecated.
- **Camera Law** — one camera wrapper only · one move at a time · every zoom has a
  reason (READ / EMPHASIZE / REVEAL / FOLLOW / BREATHE) · never cut while zoomed ·
  motion blur only during fast motion.
- **Sentence Law** — every narration sentence gets its own visual event, bound to
  its stressed word (+/-100 ms).
- **Caption system** — one declared style from `CAPTION-STYLES.md`; styled,
  transparent-background (alpha) and chroma-key captions as needed.
- **Feature catalogue** — `ADVANCED-FEATURE-USE-CASES.md`; mandatory where the
  concept needs it.

## The gates (do not skip)
- **RENDER GATE** — contact-sheet variants (V1/V2/V3); present them and ask
  "Did you like any of these, or shall I generate more variants?"; write the pick
  back into CONCEPT.md.
- **QA GATE** — run `edit-qa-validator` / `tools/qa_check.py`; audit, AI-re-think
  the gaps, revalidate; write `EDIT-QA.md`. Deliver only when it passes.

## Hard limits
The look is **Apple Standard** unless a preset or named documentary style is
requested. Never invent facts, prices, stats or testimonials. Never include
voiceover or video clips in `ASSETS-PROMPT.md`. Label every recreation, animation
and composite. Ask for assets; asking is expected, never a failure.

## Output shape (what the user gets)
1. Which build skill you will use.
2. Your intake questions (one list).
3. *(after answers)* the 2–3 options.
4. Your recommendation + reasoning + trade-offs + confidence.
5. The CONCEPT.md plan and the asset zip.
6. The contact-sheet variants and the ask.
7. The QA report and the final deliverable.
