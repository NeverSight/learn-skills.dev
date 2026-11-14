---
name: veo-flow-prompting
description: Use when writing or fixing prompts for Google Flow video generation - Veo 3.1 or Gemini Omni Flash - including multi-clip scripts, dialogue clips, silent clips, the @me avatar, on-screen text, and clips that keep getting blocked by the content filter. Encodes the verified prompt anatomy, the per-clip complexity budget, and the failure modes that cost real credits.
---

# Veo 3.1 / Gemini Omni Flash prompting

Field-tested rules for Google Flow (`labs.google/fx/tools/flow`). Full source-cited
background: [`docs/google-flow-veo-playbook.md`](../../docs/google-flow-veo-playbook.md).
UI map and credit costs: [`docs/flow-ui-map.md`](../../docs/flow-ui-map.md).
Filters and policy: [`docs/content-filters-and-policy.md`](../../docs/content-filters-and-policy.md).

Claim tags used throughout: `[FACT]` = stated by a Google primary source ·
`[ESTIMATE]` = practitioner guidance · `[UNVERIFIED]` / `[CONTESTED]` = confirm
in-product before relying on it. Never invent model behaviour; if you are unsure,
tag it.

> **Which model is which.** "Omni Flash" is **Gemini Omni Flash**, Google's any-input
> (text/image/audio/video) → video model with native audio. It is not a Gemini text
> LLM and there is no product called "Veo 3 Flash". **Veo 3.1** (Lite / Fast / Quality)
> is the cinematic model. Both are selectable in Flow's model dropdown. `[FACT]`

---

## 1. The per-clip prompt block

Field order, every clip: **LOOK → CAMERA → ACTION → FIDELITY → DIALOGUE → AUDIO →
EXCLUSIONS** (+ optional POST NOTE).

Google's own five-part formula for Veo 3.1 is
`[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]` `[FACT]`.
The block above is that formula plus the three lines production keeps needing
(fidelity, audio direction, exclusions).

```
LOOK:       <subject + wardrobe + setting + light, restated in full>
CAMERA:     <exactly ONE move>
ACTION:     <max 2 beats>
FIDELITY:   Keep natural, realistic body proportions. Do not slim or idealize.
DIALOGUE:   He says, "<one or two short lines, in quotes, attributed>"
AUDIO:      Ambient noise: <...>. SFX: <...>.
EXCLUSIONS: a clean frame with no subtitles, no captions, no on-screen text,
            no lower-thirds, no logos, no watermark.
```

**Every clip prompt must be self-contained.** The generator never sees your other
clips. Repeat wardrobe, setting and identity in *every* clip. A "base card" at the
top of your script document is human reference only — it is not merged into anything.

**Complexity budget per clip** (production-learned; overloaded clips render wrong):

- Max **2 action beats**. More than that → split into two clips.
- Exactly **one camera move** `[FACT]`. Vague or contradictory camera cues make the
  model default to near-static. For a locked frame, say
  `static shot, camera completely still` `[ESTIMATE]` — omitting the camera line does
  *not* give you a locked frame.
- **No invisible micro-props** (pressure sensors, hidden latches). Imply them through
  timing instead: *"the moment it leaves the cushion, the alarm sounds"*.
- **State changes only at the very end of the clip** — never a mid-clip lighting
  transition inside the LOOK line.
- In close-ups keep **one character in focus**; others soft-blurred or off-screen with
  off-screen dialogue.

**Length:** ~100–200 words per prompt `[ESTIMATE]`. Beats of 4–8s. Omni Flash goes to
10s; Veo 3.1 caps at 8s. 1080p/4K require an 8s clip; Extend caps at 720p `[FACT]`.

**Lens to feel:** 16mm expands space · 35mm natural · 50mm intimate · 85mm compresses
for intensity · wide-angle for establishers `[ESTIMATE]`.

**Timestamp prompting** packs several shots into one generation `[FACT]`:

```
[00:00-00:03] Medium close-up, slow push-in: <shot>.
[00:03-00:07] Static medium shot: <shot>.
[00:07-00:10] Slight low angle, locked frame: <shot>.
```

**Anchor performance to words:** *"firm flipping gesture on 'flip that'"* works;
"expressive gestures" does not.

---

## 2. Dialogue, language and silence

- Write **directions in English** (best visual control) and **dialogue in the target
  language**. This pattern is production-verified.
- Non-English dialogue **must keep its accents** — `nao → não`, `e → é`,
  `missao → missão`. Accents drive pronunciation; never ASCII-strip a dialogue line.
  Spell numbers out in words.
- Speech is **attributed to a named speaker**, and kept to 1–2 short lines per clip.
  **On quotation marks the sources conflict** `[CONTESTED]`: Google's Veo prompt guide
  shows quoted dialogue (`A woman says, "We have to leave now."`), while separate Google
  guidance says to use a colon after the speaker's action and **avoid quotation marks**,
  because quotes push the model toward rendering the text on screen. Field testing sided
  with the colon form, and it composes with the caption bug below — so **default to**
  `Man says: Bom dia!` and keep the quoted form as a fallback if speech fails to trigger
  at all. Full detail: [`dialogue-and-voice`](../dialogue-and-voice/SKILL.md).
- **No ellipsis and no mid-sentence periods** in a dialogue line — they stop the voice
  and the lip-sync dead. Use commas; punctuate only at the very end.
- **Name the language on every spoken line** (and every background murmur). Omitting it
  causes audio failures and random-language output.
- **Regional accent control:** tag every line, e.g.
  `DIALOGUE (PT-BR, carioca accent - coda "S" softened to "sh"): "..."`.
  Accent adherence is unstable `[UNVERIFIED]`; fallback is to record or TTS in post.
- **Silent clip recipe:** no quoted speech, no speech cues at all, *positively* specify
  the ambient audio, then add `no dialogue, no speech, silent`. Speech cues are the
  primary trigger for both spoken audio **and** burned-in captions `[FACT]`. Flow also
  has an explicit toggle: View Settings → **Return silent videos: On**.
  **Never mention the mouth, lips or speaking in a silent clip** — "his mouth opens
  slightly as if about to speak" reliably generates actual speech. Emotion goes through
  eyebrows, jaw and eyes.
- Audio is **always generated** and there is no mute flag `[FACT]` — so direct it per
  clip. If only one clip should carry crowd noise, say so and keep the others quiet.

---

## 3. The gotchas that cost credits

- **Burned-in junk captions.** Veo burns garbled subtitles into clips even when told
  not to `[FACT]`. Google's documented mechanism is negative prompting written as
  *positive description* — describe the clean frame you want, not "no X". End every
  clip with the EXCLUSIONS tail above. It is effective but **not foolproof**; inspect
  every render.
- **On-screen text is garbled**, including short words and accented words. Generate the
  plate clean and add real text in post, or use Flow's **Type Overlays** tool. Same for
  end cards.
- **Branded real locations** get approximated. Describe them generically
  (*"a grand white Belle Époque beachfront hotel"*), optionally add a reference photo
  of the place, and never ask for the brand name or logo on screen — exclude it.
- **SynthID watermark is always on, no opt-out** `[FACT]`. Label your output as
  AI-generated where the platform requires it.
- **PG / stylized action renders better and avoids refusals**: no explicit weapons, no
  blood, no real explosions. Alarms, chases and heists are fine.
- **Aspect ratio:** 9:16 for Reels/Shorts, 16:9 for YouTube/TV. If the UI already sets
  the ratio, do **not** also write "Vertical 9:16" in the prompt text.
- **Credits are spent per generation, and there are no free re-rolls** for successful
  generations `[FACT]`. Validate identity with one cheap, calm close-up before
  committing to a whole sequence. (You are not charged for *failed* generations
  `[FACT]` — but see the NPOV note below: a filtered generation in Flow's UI has been
  observed to charge anyway.)

---

## 4. When the content filter blocks you

Flow returns a single generic message — *"This prompt might violate our policy about
generating harmful content"* — for completely different underlying causes. Do not
guess which one you hit. Full detail, including how to read the real reason out of the
API response, is in
[`docs/content-filters-and-policy.md`](../../docs/content-filters-and-policy.md).

The one finding that changes how you write prompts:

> **NPOV — the news framing itself is the trigger, not the faces.**
> Verified by inspecting the generation-status API: a blocked generation returns
> `failureReasons: ["NPOV"]` (Neutral Point Of View). Framing a clip as a **news
> broadcast** — anchor, newsroom, "delivering the news", and even a *news-coded set*
> (channel logo wall, world map panel, anchor desk) — fails, no matter how neutral the
> content. The **same real events told as a casual story or anecdote pass**, with the
> same people, the same dry wit and the same facts.

The fix: generate *"two people sharing absurd stories to camera, dry deadpan amusement;
not a news broadcast"* over a **generic** modern studio, and composite the newscast look
(logo, chyrons, ident) 100% in post. The model sees storytelling; the audience sees a
newscast.

Related: naming a real celebrity in dialogue may trip a separate **prominent-people**
filter. Prefer the no-name variant by default (*"a famous player"*, *"a European
airport"*) so you never gamble credits on it.

---

## 5. Before you deliver a multi-clip script

Run the continuity protocol and produce a regeneration ledger — both live in
[`skills/multiclip-continuity`](../multiclip-continuity/SKILL.md). Skipping this is the
single most expensive mistake in multi-clip work: props teleport, wardrobe changes
between clips, and characters act on facts they were never told.

Identity, avatars, reference photos and consent:
[`skills/identity-and-likeness`](../identity-and-likeness/SKILL.md).

---

## 6. Honesty rules

- Big claims in a script are framed as **vision** ("what if…"), not fact.
- A statistic needs a source in hand before it appears as fact in a script.
- Mark every unconfirmed model behaviour `[UNVERIFIED]` or `[CONTESTED]` and say so
  out loud — model behaviour and pricing move fast, and a stale "fact" in a prompt
  playbook burns real money.
