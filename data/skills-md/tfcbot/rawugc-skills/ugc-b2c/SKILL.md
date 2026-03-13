---
name: ugc-b2c
description: >-
  UGC video format templates for general B2C products. Contains 15 TikTok-native,
  lofi video formats with shot-by-shot structure and AI video generation prompts.
  Use when the user wants to create B2C UGC content — product demos, honest reviews,
  lifestyle integrations, or comparison content for any consumer product.
requires:
  env:
    - RAWUGC_API_KEY
compatibility: >-
  Use alongside the rawugc-api skill for API endpoint knowledge.
  Requires RAWUGC_API_KEY.
homepage: https://github.com/tfcbot/rawugc-skills
source: https://github.com/tfcbot/rawugc-skills
---

# B2C UGC Video Formats

15 lofi, TikTok-native video formats for general B2C products. Raw, authentic, easy to produce. No hard CTAs — these work for any consumer product and feel like real people sharing things they genuinely use.

## How to Use These Formats

1. Identify the user's goal (product launch, social proof, comparison, lifestyle integration).
2. Select the format below that best matches.
3. Use the **Prompt Template** to compose the `prompt` field for `POST /videos/generate`. Replace `[BRACKETED]` placeholders with details from the user.
4. Default to `aspectRatio: "portrait"` (9:16) and `nFrames: "10"` unless the format specifies otherwise.
5. Keep the tone casual, genuine, unscripted. These should feel like someone sharing a real find with their group chat.

---

## Formats

### 1. Just Got This

**Vibe**: Immediate reaction to receiving or buying something — raw excitement, no prep.

**Structure**:
- 0-3s: Holding or unwrapping [PRODUCT], barely contained excitement
- 3-6s: First look — turning it over, examining quality and details
- 6-8s: First use or try — genuine "oh wow" moment
- 8-10s: Looking at camera, nodding — this was a good purchase

**Prompt Template**:
> A person just received [PRODUCT] from [BRAND]. They're holding it for the first time — excitement barely contained. They turn it over, examining the [DETAILS — e.g. build quality, design, packaging]. They use it for the first time — [FIRST USE ACTION]. Genuine impressed reaction. They look at the camera and nod — this was worth it. Unscripted, immediate, real. Living room or kitchen table, natural light, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 2. The Desk Companion

**Vibe**: Product sitting on your desk while you work — it's just always there, part of the setup.

**Structure**:
- 0-3s: Desk setup shot — keyboard, monitor, and [PRODUCT] sitting naturally in the scene
- 3-6s: Person working, hand casually reaches for [PRODUCT], uses it briefly
- 6-8s: Sets it back down, continues working — seamless, not a disruption
- 8-10s: Wide shot of the desk — [PRODUCT] belongs in this workspace

**Prompt Template**:
> A clean desk setup — keyboard, monitor, and [PRODUCT] from [BRAND] sitting naturally in the scene. A person working, hand casually reaches for [PRODUCT], [BRIEF USE — e.g. takes a sip, checks a reading, adjusts a setting]. Sets it back down without looking, continues working — completely seamless. Wide shot of the desk — [PRODUCT] belongs in this workspace. Home office, natural light, vertical video, desk companion energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 3. The First Touch

**Vibe**: First time holding/touching the product — genuine tactile discovery, quality check.

**Structure**:
- 0-3s: [PRODUCT] in packaging or on a surface, hands approaching
- 3-6s: Picking it up for the first time, feeling the weight, the texture, the build
- 6-8s: Turning it over in hands, examining details — impressed nod
- 8-10s: Setting it down with care — first impression locked in, it's quality

**Prompt Template**:
> First-touch discovery of [PRODUCT] from [BRAND]. [PRODUCT] sitting on a surface or in packaging. Hands approach and pick it up for the first time — feeling the weight, the texture, the build quality. Turning it over, examining [DETAILS — e.g. the finish, the hardware, the craftsmanship]. An impressed nod — the build quality is undeniable. Setting it down with care — first impression locked in. Natural light, vertical video, first-touch discovery energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 4. Hack I Found

**Vibe**: Unexpected way to use the product — "wait, try this."

**Structure**:
- 0-3s: Holding [PRODUCT], mischievous "I found something" expression
- 3-6s: Demonstrating the unexpected use or hack
- 6-8s: The hack working — satisfying result
- 8-10s: "You're welcome" energy, proud of the discovery

**Prompt Template**:
> Product hack video. A person holding [PRODUCT] from [BRAND] with a "watch this" expression. They demonstrate [UNEXPECTED USE/HACK — e.g. a secondary function, a creative way to use it, a tip that isn't obvious]. The hack works beautifully — satisfying result. They look at the camera with proud, "you're welcome" energy. The product is more versatile than people think. Close-up demonstration, natural light, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 5. Honest Pros and Cons

**Vibe**: Talking to camera, listing what you love and what's mid — full transparency.

**Structure**:
- 0-3s: "Okay here's my honest take on [PRODUCT]" — holding it up
- 3-6s: Pros — counting on fingers, genuine enthusiasm
- 6-8s: Cons — fair, minor, balanced
- 8-10s: Overall verdict — "pros way outweigh" authentic conclusion

**Prompt Template**:
> Honest pros and cons review. A person holding [PRODUCT] from [BRAND], talking directly to camera. Pros: [PROS — e.g. "the quality is insane," "it does exactly what it says," "the design is clean"]. Cons: [CONS — e.g. "wish it came in black," "took a couple days to ship," "slightly bigger than I expected"]. The cons are real but minor — the pros clearly outweigh. Transparent, trustworthy, balanced. Casual setting, selfie angle, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 6. The One Detail

**Vibe**: Zeroing in on one specific design detail that makes the product special — the little thing.

**Structure**:
- 0-3s: [PRODUCT] in frame, camera at normal distance
- 3-6s: Camera pushes in close to one specific detail — a button, a hinge, a finish
- 6-8s: Finger points at or interacts with the detail — "this right here"
- 8-10s: Pull back to full product — but now you can't unsee that detail

**Prompt Template**:
> Design-detail obsession video. [PRODUCT] from [BRAND] in frame at normal distance. Camera pushes in close to [SPECIFIC DETAIL — e.g. a clasp, a button, a hinge, a texture, a finish]. A finger points at or interacts with the detail — "this right here" energy. Pull back to the full product — but now the detail is all you notice. Natural light, vertical video, design-detail obsession energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 7. The Sound It Makes

**Vibe**: ASMR focus on satisfying product sounds — clicks, zips, pours, snaps.

**Structure**:
- 0-3s: Close-up of [PRODUCT], anticipation
- 3-6s: The satisfying sound — [CLICK, ZIP, SNAP, POUR, WHIR]
- 6-8s: Repeat from different angle — same satisfying sound
- 8-10s: Final interaction, the sound is the hook

**Prompt Template**:
> ASMR product video focused on the sounds [PRODUCT] from [BRAND] makes. Close-up: [THE SOUND — e.g. the satisfying click of the lid, the zip of the case, the pour of the liquid, the snap of it locking in place]. The camera captures it from multiple angles — the sound is crisp, satisfying, oddly addictive. No talking, just the product's natural sounds. Extreme close-up, quiet room, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 8. Would I Rebuy

**Vibe**: Holding product after months of use — "here's my verdict after actually living with it."

**Structure**:
- 0-3s: Holding [PRODUCT] — it has signs of real use (wear, half-empty, etc.)
- 3-6s: Reflecting on months of use — what held up, what they love
- 6-8s: The verdict moment — "would I buy this again?"
- 8-10s: Confident yes (or honest qualification) — genuine conclusion

**Prompt Template**:
> Long-term review. A person holding [PRODUCT] from [BRAND] that's clearly been used — [SIGNS OF USE, e.g. some wear, half-empty, well-loved]. They talk about life with the product over [TIME PERIOD]. "Would I rebuy?" The verdict: [VERDICT — e.g. "absolutely, already have a backup," "yes, but I'd get the larger size next time"]. Genuine, informed by actual use, not first impressions. The trust comes from time with the product. Natural setting, selfie angle, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 9. The Friend Text

**Vibe**: Talking to camera about texting a friend to recommend this — word-of-mouth moment.

**Structure**:
- 0-3s: Face to camera, holding [PRODUCT] and phone — "I literally just texted my friend about this"
- 3-6s: Holding product up, explaining what makes it worth recommending
- 6-8s: Gesturing at phone — "she's already ordering one"
- 8-10s: Satisfied expression, holding product — the genuine recommendation

**Prompt Template**:
> Word-of-mouth recommendation video. A person face to camera, holding [PRODUCT] from [BRAND] in one hand and phone in the other — "I literally just texted my friend about this." Holding [PRODUCT] up, explaining what makes it worth recommending — [KEY SELLING POINTS]. Gesturing at phone — "she's already ordering one." Satisfied expression, holding [PRODUCT] — the genuine word-of-mouth moment. [SETTING], natural light, vertical video, recommendation energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 10. Car Review

**Vibe**: Reviewing the product in your car — popular TikTok setting, casual drive-thru energy.

**Structure**:
- 0-3s: Sitting in parked car, holding [PRODUCT], car lighting
- 3-6s: Talking through the product — showing it, demonstrating features
- 6-8s: Using it in the car context — it works anywhere
- 8-10s: Casual verdict, tossing it on the passenger seat — approved

**Prompt Template**:
> Car review. A person sitting in their parked car, holding [PRODUCT] from [BRAND]. The car provides natural framing — window light, dashboard visible. They show the product, talk through [KEY FEATURES/IMPRESSIONS]. They use or demonstrate it — [CAR DEMO]. They casually toss it on the passenger seat — it's coming with them. The car setting adds intimacy and authenticity — classic TikTok review energy. Car interior, natural daylight through windows, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 11. The Thing That Fixed

**Vibe**: "I had this problem, this product fixed it" — simple storytime, genuine.

**Structure**:
- 0-3s: Describing the problem — relatable frustration, talking to camera
- 3-6s: "Then I found this" — introducing [PRODUCT]
- 6-8s: Showing how it solved the problem — demo or explanation
- 8-10s: Life after the fix — relief, satisfaction, problem gone

**Prompt Template**:
> Problem-solution storytime. A person talking to camera about [PROBLEM — e.g. a daily frustration, something that was broken, an unmet need]. Relatable, genuine frustration. "Then I found [PRODUCT] from [BRAND]." They show how it solved the problem — [SOLUTION DEMO]. The relief is visible. Life is better now, the problem is handled. Simple, effective storytelling. Casual setting, selfie angle, natural light, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 12. The Restock Click

**Vibe**: The moment you rebuy without hesitation — loyalty confirmed, no research needed.

**Structure**:
- 0-3s: Person holding nearly-empty/well-used [PRODUCT]
- 3-6s: Glancing at it, immediate decision — "yep, reordering"
- 6-8s: Casually tapping on phone to reorder, no browsing, no comparing
- 8-10s: Setting old product down, satisfied nod — loyalty is automatic

**Prompt Template**:
> Rebuy-without-thinking video. A person holding their well-used [PRODUCT] from [BRAND] — [SIGNS OF USE — e.g. nearly empty, well-worn, clearly loved]. Glancing at it with an immediate decision — "yep, getting another." Casually tapping their phone to reorder, no browsing alternatives, no comparing — they know what they want. Setting it down with a satisfied nod — the loyalty is automatic. [SETTING], natural light, vertical video, rebuy-without-thinking energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 13. Gift Guide Energy

**Vibe**: "If you don't know what to get someone, this" — effortless recommendation.

**Structure**:
- 0-3s: "If you need a gift for [PERSON TYPE]…" — face to camera
- 3-6s: Holding up [PRODUCT], showing it off — it's a crowd-pleaser
- 6-8s: Quick demo of why it works as a gift — universal appeal
- 8-10s: "Trust me, they'll love it" — confident recommendation

**Prompt Template**:
> Gift guide content. A person talking to camera — "if you need a gift for [PERSON TYPE — e.g. your partner, a friend who has everything, your mom], get them this." They hold up [PRODUCT] from [BRAND], showing it off. Quick demo of why it's a great gift — [GIFT APPEAL, e.g. "it's useful but also looks premium," "everyone who sees it asks about it," "it's the kind of thing you wouldn't buy yourself"]. Confident recommendation energy. Casual setting, holiday or everyday vibe, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 14. The Nightstand Essential

**Vibe**: Product on the nightstand — the last thing you see at night or first thing in the morning.

**Structure**:
- 0-3s: Nightstand scene — lamp, book, phone, and [PRODUCT]
- 3-6s: Hand reaches for [PRODUCT], uses it briefly
- 6-8s: Sets it back on the nightstand, it stays within arm's reach
- 8-10s: Settling into bed or getting up — [PRODUCT] is bookending the day

**Prompt Template**:
> Nightstand essential video. A nightstand scene — lamp, book, phone, and [PRODUCT] from [BRAND]. A hand reaches for [PRODUCT], [BRIEF USE — e.g. picks it up, opens it, checks it, uses it]. A moment of use, comfortable and settled. Sets it back on the nightstand within arm's reach. Settling into bed or getting up — [PRODUCT] is bookending the day. Bedroom, warm lamp light, vertical video, nightstand essential energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 15. The Aesthetic

**Vibe**: Product styled beautifully in its environment — no talking, vibes only.

**Structure**:
- 0-3s: [PRODUCT] in a beautifully styled setting — morning light, clean surface
- 3-6s: Slow pan or close-up, capturing texture, color, design details
- 6-8s: A hand enters frame, interacts gently — picks it up or adjusts it
- 8-10s: Final hero shot, product looking its best, pure visual vibes

**Prompt Template**:
> Pure aesthetic product video. [PRODUCT] from [BRAND] styled in a beautiful setting — [ENVIRONMENT, e.g. marble countertop with morning light, minimal desk with a plant, cozy bedside table]. Slow pan capturing the details — [DESIGN DETAILS, e.g. texture, color, form factor]. A hand gently enters frame and interacts with the product — picking it up, turning it slightly. Final hero shot. No talking, no text, just vibes. The product speaks for itself visually. Soft, warm lighting, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`
