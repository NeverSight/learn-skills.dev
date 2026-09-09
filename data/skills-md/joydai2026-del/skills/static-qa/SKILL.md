---
name: static-qa
description: >-
  Automated vision-QA gate for AI-generated ad STILLS before a human looks: a context-free multimodal reviewer scores the actual pixels PASS or REGEN against a 10-dimension rubric. Use when writing "QA this image", "static QA", "check the still", "is this image good", "regen-loop the image", "QA the storyboard stills", "QA the comp". The video counterpart is vid-qa; the human brand-safety gate is FINAL.
---

# Static QA (image vision gate)

The automated vision gate for AI-generated ad STILLS. `static-ad` makes the image; this checks the actual pixels against a written rubric before a human looks, and before a still becomes a video keyframe you pay to animate. The video counterpart is `vid-qa` (it calls this skill on sampled frames, then adds the time-only layers).

**Core principle (the reason this skill exists): the maker cannot judge their own output objectively.** The model that made the image cannot see it. The person who prompted it is biased toward seeing what they intended. "It looks fine to me" and "the file exists, exit code 0" both pass while the hand has six fingers, the Chinese renders as empty tofu boxes, the disclosure label is missing, or the headline sits under the platform UI. So a **fresh, context-free reviewer** that never saw the generation prompt checks what is actually on the canvas. This is the visual version of the owner's "critical audit: act as if someone else did it."

**Two laws sit above everything** (from the pipeline): generate wide, gate hard at one place; and **files-exist is never QA, watch the pixels.** A green codex/exit only means a file got written, not that it looks right.

**Every platform number, aspect ratio, safe-zone, and disclosure rule here drifts fast.** Re-verify the current platform doc at use time (`/last30days` or official docs). The thresholds are heuristics, not constants.

---

## Part 1. When it runs

Two fire points, both cheaper than the alternative:

1. **On storyboard / keyframe STILLS, before you pay to animate.** The single highest-leverage moment. A broken hand or garbled headline costs ~$0.02 to catch on a still and 22 to 270 credits to catch after the video is rendered. Never animate a failing still. (This is the gate `vid-ad` and the format directors call before motion.)
2. **On a finished static ad, after generation, before the human gate.** So the human reviews a clean, pre-screened image instead of being the first filter.

**Both fire points apply BEFORE EVERY handoff to a human, every time, including after any re-roll** (a re-roll is a new image; it gets the full gate, not a glance). And **after any change, re-check the WHOLE affected set, not just the changed still**: a re-rolled still drifts (wardrobe, props, color, denomination) against its neighbors, so cross-shot consistency is re-judged across the full batch every time.

It does NOT replace the human Stage-3 brand-safety gate. It runs upstream of it.

---

## Part 2. The static-image gate

### Inputs the reviewer gets
- the **brief** (subject, action, framing / shot-size, count, the single message);
- the **approved product / reference image(s)** (the real SKU, the brand kit) so identity and fidelity are judged against ground truth, not a vibe;
- the **expected strings** (headline, CTA, disclosure / AI-generated label) as literal text to diff against;
- the **brand kit** (palette, logo rules, tone);
- the **target channel + aspect ratio + action-safe region** (where the platform UI covers the frame, especially 9:16 bottom-third);
- the **candidate image(s)**.

### The reviewer is a freshly spawned, context-free Agent
Use the `Agent` tool (general-purpose / multimodal), NOT yourself inside the generation conversation, and NOT the agent that generated the image. Its ONLY inputs are the list above, so it reads what is actually there. **No new API key is needed** (Claude vision via a spawned Agent). Batch ~4 to 8 images per reviewer so it can also compare them for cross-shot consistency and catch the batch-clone tell.

### The 10-dimension ad rubric
Each dimension scored **1 = clean / 2 = minor / 3 = blocking**, with a one-line reason. Dimensions tagged **[HUMAN-CONFIRM if 2 to 3]** route to a human even on "minor" because MLLMs are measurably weakest there (Part 5).

1. **brand_logo**: brand marks correct, OR correctly ABSENT where required. (Example: a Gold Cash note must show NO brand name / wordmark anywhere; the model loves to print it.) No competitor logos, no real trademarked logos, no real celebrities.
2. **product_fidelity**: product shape, color, proportion match the real SKU; no impossible geometry; not "more vibrant than reality" (reads fake and is a claim risk).
3. **text_legibility**: every on-image word spelled right and not warped; **CJK not rendered as tofu boxes** (□□□); OCR the frame and diff against the expected strings. Bilingual-critical: PIL/codex can silently drop a CJK font and the exit code stays green. Use a CJK-capable font (**STHeiti Medium** `/System/Library/Fonts/STHeiti Medium.ttc`, or **Hiragino Sans**); **`PingFang.ttc` often fails to load in PIL and silently falls back to tofu** with a green exit. Verify the glyphs actually RENDERED (OCR-diff the rendered frame), never trust exit-0; if CJK text keeps failing, burn it in as a deterministic overlay on a clean plate.
4. **claim_compliance**: no fake testimonial / receipt / balance / merchant name / official seal / certification badge; required **AI-generated + disclosure label present**; claims stay inside the allowed lane (no "guaranteed", "tax-free", implied returns for a regulated product). **[HUMAN-CONFIRM if 2 to 3]**
5. **hands**: correct finger count; no fused / extra / melted / six-finger hands; plausible grip. (Hands are the #1 generated-image failure.) **[HUMAN-CONFIRM if 2 to 3]**
6. **faces_anatomy**: faces and eyes coherent (no melted / asymmetric / dead eyes, no extra teeth); body logic holds; no extra / missing / fused limbs, no impossible joints. **[HUMAN-CONFIRM if 2 to 3]**
7. **scene_physics**: lighting, shadow direction, and reflections consistent; no floating or fused objects; background geometry sane (no warped shelves, no impossible perspective).
8. **prompt_adherence**: shows what the brief asked (subject, action, framing / shot-size, count). Flags "looks fine but is the WRONG shot".
9. **brand_fit_slop**: on palette and tone, has a point of view, NOT generic "AI stock" slop (the 2026 anti-slop brand risk).
10. **channel_safe_area**: headline, product, CTA, and disclosure all sit inside the target aspect-ratio action-safe region (especially 9:16, where the platform UI eats the bottom third and right rail).

### The copy-paste judge prompt
```
You are a context-free ad-creative QA reviewer. You did NOT make these images and have no
stake in passing them. Be strict, not generous. A real customer and a regulator will see this.

INPUTS:
- Brief: <subject, action, framing, count, single message>
- Reference / product image(s): attached (the REAL SKU + brand kit)
- Expected on-image strings (must appear, spelled exactly): <headline> | <CTA> | <disclosure / "AI-generated">
- Brand rules: <palette, logo present-or-absent rule, tone>
- Channel + aspect: <e.g. 9:16 TikTok; action-safe = avoid bottom 30% and right rail>
- Candidate image(s): attached

For EACH image, REASON step by step through all 10 dimensions (what you actually see vs what is
required), THEN output JSON ONLY (no prose after the JSON). Score each 1=clean, 2=minor, 3=blocking.
OCR every visible word and diff it against the expected strings; CJK as boxes/garbage = text_legibility 3.

Output, per image:
{
  "image": "<id>",
  "scores": { "brand_logo":1-3,"product_fidelity":1-3,"text_legibility":1-3,"claim_compliance":1-3,
              "hands":1-3,"faces_anatomy":1-3,"scene_physics":1-3,"prompt_adherence":1-3,
              "brand_fit_slop":1-3,"channel_safe_area":1-3 },
  "blocking": [<every dimension scored 3>],
  "verdict": "PASS" | "REGEN",
  "regen_guidance": "<negative-prompt + anchor deltas that fix each blocking item>",
  "needs_human": <true if any of claim_compliance / hands / faces_anatomy scored >= 2>
}

VERDICT RULE: "PASS" ONLY if no dimension scored 3 AND needs_human is false. Otherwise "REGEN".
Do not be generous. When unsure between two scores, pick the higher (worse) one.
```

### The reviewer's output format
```
<image-id>: VERDICT(PASS / REGEN)   needs_human: yes|no
  brand_logo: ok|<issue>   product_fidelity: ok|<issue>   text_legibility: ok|<issue>
  claim_compliance: ok|<issue>   hands: ok|<issue>   faces_anatomy: ok|<issue>
  scene_physics: ok|<issue>   prompt_adherence: ok|<issue>   brand_fit_slop: ok|<issue>   channel_safe_area: ok|<issue>
  -> action: regen | keep | human-confirm  (one line why)

SUMMARY
  image-id | verdict | needs_human | top blocking issue

REGEN LIST (de-duplicated)
  - <image-id(s)>: <single fix + the negative-prompt deltas>
```

---

## Part 2.5. Deterministic anchor-element measurement (the maker's pre-check the vision reviewer CANNOT do)

The 10-dimension vision rubric is necessary but **not sufficient when the design has a REQUIRED exact-position or exact-size element**, a coin that must sit at dead-center, a logo pinned to a fixed corner, a fixed-size badge, a security strip at a fixed width. An MLLM reviewer grades "the gold looks centered" leniently: it cannot tell 2% off from 8% off, and it will **silently PASS an element that is half-size or missing entirely**. So the MAKER measures it in PIXELS, deterministically, BEFORE the vision gate and before any human sees it.

**This exists because fake-QA is a recurring failure.** Gold Cash 2026-07-04: claimed the center gold "passed" on 7 banknotes without measuring; 4 of them actually had the gold **missing, off-center, or half-size**. the owner: *"为什么你还会犯这样的错误？...apparently you didn't use it to verify."* "Looks centered" is not a measurement. Paste the numbers, or it did not happen.

**Recipe (proven, stdlib + numpy):**
1. **Isolate the element by color.** For a warm gold bead: `mask = (R>170) & (G>110) & (G<210) & (B<150) & (R>B+55) & (R>=G)`. (Pick the color rule that fits the element; a navy logo, a red seal each get their own.)
2. **Window to the region it must live in**, exclude margins, holographic strips, text bands, and any other area that shares the color (e.g. a bottom multilingual gold band, an iridescent left strip). A full-frame centroid gets dragged off by that noise; a central-band window (`x∈[0.28,0.72]W, y∈[0.10,0.72]H`) isolates the real element.
3. **Measure**: blob centroid → **offset % from the target point**; bounding-box `w×h` → **size vs a reference element** (another approved note in the set); **pixel count** → a floor.
4. **Assert, per element**: offset ≤ threshold (**≤2%** for dead-center); size within **0.85 to 1.15×** the reference; pixel-count ≥ a floor (this line alone catches "element missing entirely" and "half-size", the two the vision judge waves through).

**Rule:** the maker runs this and **pastes the measured numbers into the QA report** (`center=(x,y) off=(±a%,±b%) size=w×h`). On fail, **fix by regenerating or precision-i2i, never by stamping a composite** (a stamped/haloed element reads fake and the owner rejects it, Gold Cash method lock), then re-measure. This is deterministic (Part 2's "watch the pixels" floor); it complements, does not replace, the vision rubric, which still owns anatomy/text/slop/compliance.

**Also add a vision dimension when the design imitates a real artifact.** If the still is meant to read as a real thing (a real-currency feel, a real product photo, a real document), score the **material/authenticity realism** (intaglio line-work, cotton-linen fibre, believable wear), not just defect-freedom, "no defects" and "looks like the real thing" are two different bars (Gold Cash B-side "真美元质感" check).

---

## Part 3. Regen discipline

A REGEN is never a blind re-roll (re-rolling the same prompt re-rolls the same odds).

- **Carry explicit anchors**: `full head in frame`, `five fingers, one thumb`, `hands resting flat`, `single subject`.
- **Carry targeted NEGATIVE prompts** for exactly what failed: `extra fingers, fused hands, six fingers, garbled text, warped letters, tofu boxes, two people, melted face, dead eyes, brand name printed on product`.
- **Cap the loop at 3 rounds**, then escalate to a human. A model that cannot hold the requirement (cannot keep hands clean, cannot render the CJK headline) needs a method change (different model, deterministic text overlay, a cutaway that hides the hand), not a 4th seed.
- **Judge with a DIFFERENT model family than the generator** (generate gpt-image, judge Claude/Gemini). A model grades its own output too leniently.
- **Final copy is a deterministic overlay, never model typography.** If `text_legibility` keeps failing, burn the headline/CTA/legal in as a Pillow/SVG overlay on a clean plate.

---

## Part 4. The artifact it emits

Save `static_qa.json` alongside the image:
```json
{ "asset":"<path>", "stage":"still", "channel":"<e.g. 9:16-tiktok>",
  "scores":{"<dimension>":1-3}, "blocking":["<dims scored 3>"],
  "verdict":"PASS"|"REGEN", "needs_human":true|false, "regen_round":0,
  "reviewer":"claude-vision (spawned agent)" , "notes":"<one line>" }
```

### Optional unattended mode
For a hands-off batch, an AutoMV-style programmatic judge sends each image to a vision API (e.g. Gemini) and returns strict JSON `{verdict, score 1-5, reason}`: score >=4 auto-pass, ==3 auto-regen (cap 3), <=2 escalate. Needs a vision API key; keep the same safeguards (strict JSON, different model family, 3-round cap, claim/hands/faces still human-confirmed). The default is the no-key spawned Agent.

---

## Part 5. Calibration + honesty (do not over-trust the judge)

- **Force strictness:** "output JSON only", "do not be generous", "when unsure, pick the worse score". A generous judge manufactures false PASSes.
- **Validate the judge before you trust it.** On a sample, eyeball the images yourself and compare; if it misses defects you can see, tighten the prompt or change the model.
- **MLLMs are measurably WEAKEST at anatomical accuracy** (hands, faces, eyes). Those ALWAYS route to human-confirm on a 2 or 3, never auto-pass.
- **The human Stage-3 brand-safety gate remains the FINAL authority.** This skill reaches "visually pre-screened against the rubric" only. Ties to the owner's global rule 3.13 (Visual Render Gate) and the `/ai-done` bar.
- **"Files exist" and "exit 0" are never QA.** Watch the pixels, every time. End every pass with an explicit "Still needs human approval" line.

---

## Part 6. Handoffs

- **`static-ad`** calls this on every generated image before a human looks.
- **`vid-ad`** and the format directors call this on STORYBOARD STILLS before paying to animate.
- **`vid-qa`** calls this rubric on each SAMPLED VIDEO FRAME, then adds its time-only layers on top.
- The **`claim_compliance`** dimension pre-screens only; the FINAL compliance call defers to the **`legal-compliance-checker`** / **`brand-safety-gate`** + the human Stage-3 gate.
- Reviewers are **fresh, context-free Agents spawned in PARALLEL** (one batch per still-set), per the owner's parallelization rule.

---

## Provenance
Ported from the `vision-qa` methodology (context-free fresh reviewer; PASS/FAIL/WARN per-dimension rubric with one-line reasons + a de-duped regen list) and re-cast for ad creative (a 10-dimension AD rubric: brand-absence, claim/disclosure compliance, channel safe-area, anti-slop). Aligned with 2026 best-practice research on the generate -> vision-judge -> regenerate loop (cap the loop; different model family for the judge; watch pixels not exit codes). No content from the source project is reproduced. Re-verify every platform spec, safe-zone, and disclosure rule at use time.

## Addendum (2026-07-05, C「无声的交易」keyframes)

- **Body completeness vs furniture (new watch item).** A person behind a TRANSPARENT counter rendered with no lower body ("没腿") passes casual review; verify furniture occlusion is physically consistent, an opaque base that plausibly hides the body, or visible legs. Fix side: prompt a solid-base counter.
- **Scene-partner consistency check.** Every close-up/insert in a multi-person scene must match the approved WIDE's cast (gender, wardrobe, skin tone). Flag any frame whose implied person contradicts the scene wide (a two-women scene rendered a MALE receiver and a male foreground back, twice, from text-only prompts).
- **Gate placement (the owner standing rule).** Full strictness on the FIRST keyframe batch, before the first human round. A dead/timed-out QA agent is RE-RUN, never skipped, this session's dead agent's missed findings all resurfaced later at the owner's cost. See memory front-load-strict-qa-to-first-generations.
