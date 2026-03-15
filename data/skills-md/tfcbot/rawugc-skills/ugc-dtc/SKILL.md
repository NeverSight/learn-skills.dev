---
name: ugc-dtc
description: >-
  UGC video format templates for DTC (direct-to-consumer) brands. Contains 15
  TikTok-native, lofi video formats with shot-by-shot structure and AI video
  generation prompts. Use when the user wants to create DTC UGC content —
  unboxings, product rituals, honest reviews, or lifestyle integrations.
requires:
  env:
    - RAWUGC_API_KEY
compatibility: >-
  Use alongside the rawugc-api skill for API endpoint knowledge.
  Requires RAWUGC_API_KEY.
homepage: https://github.com/tfcbot/rawugc-skills
source: https://github.com/tfcbot/rawugc-skills
---

# DTC UGC Video Formats

15 lofi, TikTok-native video formats for DTC brands. Raw, authentic, easy to produce. No hard CTAs — these feel like real people sharing products that genuinely became part of their life.

## How to Use These Formats

1. Identify the user's goal (product launch, unboxing experience, repeat purchase story, brand loyalty content).
2. Select the format below that best matches.
3. Use the **Prompt Template** to compose the `prompt` field for `POST /videos/generate`. Replace `[BRACKETED]` placeholders with details from the user.
4. Default to `aspectRatio: "portrait"` (9:16) and `nFrames: "10"` unless the format specifies otherwise.
5. Keep the tone casual, genuine, unscripted. These should feel like someone who genuinely bought this with their own money.

---

## Formats

### 1. Unboxing Moment

**Vibe**: Opening the package — tissue paper, first touch, genuine reaction to the experience.

**Structure**:
- 0-3s: Package on table, hands pulling at tape/opening the box
- 3-6s: Tissue paper unwrapped, first reveal of product inside
- 6-8s: Picking up [PRODUCT], turning it over, feeling the quality
- 8-10s: Genuine reaction — nodding, impressed by packaging and product

**Prompt Template**:
> A person sitting at a table, opening a delivery package from [BRAND]. They pull at the tape, open the box, unwrap tissue paper. [PRODUCT] is revealed inside — they pick it up, turning it over in their hands, examining the packaging and quality. Their reaction is genuine — pleasantly surprised, impressed. The unboxing experience matters and this one delivers. Kitchen or living room table, natural light, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 2. My Honest Take

**Vibe**: Stream of consciousness review — product in hand, talking to camera, no script.

**Structure**:
- 0-3s: Holding [PRODUCT], casual setting, talking directly to camera
- 3-6s: Walking through what they like — pointing at details, demonstrating
- 6-8s: One thing they'd note — honest but not negative, balanced
- 8-10s: Overall verdict — genuine nod, "yeah I'd recommend this"

**Prompt Template**:
> A person holding [PRODUCT] from [BRAND], talking casually to camera like they're telling a friend about it. They point out what they love — [POSITIVE DETAILS, e.g. the texture, the design, how it works]. They mention one honest observation — [HONEST NOTE, e.g. "wish it came in more colors" or "took a day to get used to"]. Final verdict is genuine approval. Unscripted, stream-of-consciousness energy. Casual setting, natural light, selfie angle, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 3. Kitchen Counter Demo

**Vibe**: Product in its natural habitat — casual use while cooking, eating, or prepping.

**Structure**:
- 0-3s: Kitchen scene, counter with everyday items, [PRODUCT] among them
- 3-6s: Using [PRODUCT] casually as part of a routine — cooking, eating, prepping
- 6-8s: Close-up of the product in use — functional, easy, integrated
- 8-10s: Back to the scene — product sits naturally in the kitchen, belongs there

**Prompt Template**:
> A kitchen scene. [PRODUCT] from [BRAND] sits on the counter among other everyday items. A person uses it casually — [USE CASE, e.g. adding it to their morning coffee, using it while cooking, grabbing it during meal prep]. Close-up of the product in action. It's not the star of the scene — it just belongs there, integrated into daily life. Warm kitchen lighting, lived-in counter, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 4. The Ritual Spot

**Vibe**: Showing where the product lives in your home — its permanent spot, part of the furniture now.

**Structure**:
- 0-3s: Camera on a specific spot — kitchen counter, bathroom shelf, desk corner
- 3-6s: [PRODUCT] sitting there naturally among everyday items
- 6-8s: Hand reaches in and uses/interacts with it casually
- 8-10s: Puts it back in its spot — it lives here, part of the daily landscape

**Prompt Template**:
> Camera on a specific spot in the home — [LOCATION, e.g. kitchen counter corner, bathroom shelf, desk edge]. [PRODUCT] from [BRAND] sitting there naturally among everyday items — [SURROUNDING ITEMS]. It just lives there. A hand reaches in, grabs it, [INTERACTION, e.g. uses it, pours some, applies a bit]. Sets it back in its spot — part of the daily landscape. [ROOM], natural light, vertical video, permanent fixture energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 5. The Restock

**Vibe**: "Ran out, had to reorder" — showing empty next to the fresh replacement.

**Structure**:
- 0-3s: Holding up the empty/almost-empty product — squeezing the last drops
- 3-5s: Setting empty next to brand new replacement
- 5-8s: Opening the new one — fresh, full, satisfying
- 8-10s: First use of the restock, relieved "I was running low" energy

**Prompt Template**:
> A person holding up a nearly empty [PRODUCT] from [BRAND] — squeezing out the very last bit. They set the empty one down and reveal a brand new replacement next to it. They open the fresh one — full, clean, satisfying. First use from the restock. The message is clear: this product gets used up and repurchased. Not a first-time buy — a repeat. Natural setting, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 6. The Repurchase Moment

**Vibe**: Showing the new one arriving right as the old one runs out — timing, loyalty, routine.

**Structure**:
- 0-3s: Nearly empty [PRODUCT] on counter, clearly well-used
- 3-6s: Hand places the fresh replacement right next to the old one
- 6-8s: Side-by-side comparison — the battle-worn original and the pristine new one
- 8-10s: Tossing the old one, sliding the new one into its spot — the cycle continues

**Prompt Template**:
> A nearly empty [PRODUCT] from [BRAND] on the counter, clearly well-loved and almost done. A hand places the fresh replacement right next to it — pristine packaging, full product. Side-by-side moment — the battle-worn original and the brand new one. Tossing the old one, sliding the new [PRODUCT] into its spot — the cycle continues. [ROOM], natural light, vertical video, loyalty loop energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 7. Morning Ritual

**Vibe**: Product integrated into a calm morning routine — not the star, just part of the scene.

**Structure**:
- 0-3s: Waking up, soft morning light, stretching
- 3-6s: Moving through morning routine — coffee, [PRODUCT] used casually
- 6-8s: [PRODUCT] in use — brief, natural, not highlighted
- 8-10s: Heading out or settling into the day, morning routine complete

**Prompt Template**:
> A calm morning routine. Person wakes up in soft morning light, stretches, heads to the kitchen. They go through their routine — making coffee, [USING PRODUCT from BRAND] as a natural part of the flow. The product isn't the focus — it's just there, integrated. The morning is the vibe: peaceful, intentional, real. The product earns its place by being useful, not by being the center of attention. Warm morning light, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 8. The Smell Test

**Vibe**: Opening the product and smelling it — genuine sensory reaction, face tells the whole story.

**Structure**:
- 0-3s: Holding [PRODUCT], unopened, looking at it with curiosity
- 3-6s: Opening it — first peek inside, leaning in to smell
- 6-8s: Face reaction — eyes close, slight smile, inhaling deeper
- 8-10s: Nodding approvingly, holding it up — the scent is everything

**Prompt Template**:
> Holding [PRODUCT] from [BRAND], looking at it with curiosity. Opening it — [OPENING ACTION, e.g. pulling out the bottle, unscrewing the cap, unwrapping]. Leaning in for the first smell. Face reaction — eyes close, slight smile, inhaling deeper. Nodding approvingly, holding it up — the scent is everything. Clean surface, natural light, vertical video, sensory discovery energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 9. Counter Flat-Lay

**Vibe**: Overhead shot of [PRODUCT] in its natural habitat — styled but real, the everyday aesthetic.

**Structure**:
- 0-3s: Overhead shot of a counter/surface with everyday items
- 3-6s: [PRODUCT] sits naturally in the arrangement, not centered but present
- 6-8s: Hand enters frame, adjusts [PRODUCT] slightly toward center
- 8-10s: Final overhead — the curated but lived-in flat-lay

**Prompt Template**:
> Overhead shot of a [SURFACE, e.g. bathroom counter, kitchen counter, desk] — [SURROUNDING ITEMS, e.g. a hand towel, a small ceramic dish, a plant cutting]. [PRODUCT] from [BRAND] sits naturally in the arrangement, fitting the aesthetic. A hand enters frame and nudges [PRODUCT] slightly toward center. Final overhead — the curated but lived-in surface. [ROOM], natural overhead light, vertical video, everyday aesthetic energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 10. The Texture Moment

**Vibe**: Close-up of the product's material/texture/finish — tactile, sensory, satisfying detail.

**Structure**:
- 0-3s: Product sitting on a surface, camera close
- 3-6s: Hands pick it up, fingers explore the surface — texture, finish, weight
- 6-8s: Turning it slowly in hands, close-up of material detail
- 8-10s: Setting it down gently, satisfied with the quality

**Prompt Template**:
> [PRODUCT] from [BRAND] sitting on a [SURFACE, e.g. wooden desk, marble counter, clean table], camera close. Hands pick it up, fingers running across the surface — feeling the [TEXTURE DETAILS, e.g. texture, the slim profile, the weight]. Turning it slowly, close-up of [MATERIAL DETAILS, e.g. the stitching, the edge paint, the embossed logo]. Setting it down gently — satisfied with the quality. [ROOM], natural light, vertical video, tactile quality check energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 11. One Week Later

**Vibe**: Follow-up after first impression — "here's what I actually think now."

**Structure**:
- 0-3s: Face to camera — "so it's been a week since I got [PRODUCT]…"
- 3-6s: Showing the product with signs of actual use — it's been lived with
- 6-8s: Honest update — what held up, what they noticed with more use
- 8-10s: Updated verdict — more informed, still genuine

**Prompt Template**:
> One-week follow-up. A person talking to camera — "it's been a week since I started using [PRODUCT] from [BRAND]." They show the product with visible signs of real use. They share their updated take — [FOLLOW-UP NOTES, e.g. "the texture grew on me," "it actually lasts longer than I thought," "I use it every day now"]. The verdict is more informed than a first impression. Honest, not performative. Same setting as their "first impression" video, natural light, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 12. Why I Switched

**Vibe**: Casual story about leaving an old brand for this one — no drama, just honest.

**Structure**:
- 0-3s: Mentioning old product/brand — maybe showing the old one briefly
- 3-6s: Explaining the switch — what wasn't working, what they wanted
- 6-8s: [PRODUCT] enters — "and then I found this"
- 8-10s: Using it, satisfied — the switch was worth it

**Prompt Template**:
> A person casually explaining why they switched to [PRODUCT] from [BRAND]. They briefly reference their old product — [OLD PRODUCT/BRAND] — and what wasn't working. "I wanted something that [NEED]." They hold up [PRODUCT] — this was the answer. They use it, showing satisfaction. The switch is presented as a natural evolution, not brand-bashing. Genuine, balanced, trustworthy. Casual setting, selfie angle, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 13. The Shelf Moment

**Vibe**: Product on a styled shelf among other objects — it belongs in this curated world.

**Structure**:
- 0-3s: Camera on a styled shelf — books, a candle, small objects
- 3-6s: [PRODUCT] sits among them, looking intentional
- 6-8s: Camera slowly pushes in toward [PRODUCT], centering it
- 8-10s: Hand reaches in and picks it up for use — it's decorative AND functional

**Prompt Template**:
> Camera on a styled shelf — [SHELF ITEMS, e.g. art books stacked horizontally, a small succulent, a framed photo]. [PRODUCT] from [BRAND] sits among them, looking intentional — decorative object and functional product. Camera slowly pushes in toward [PRODUCT]. A hand reaches in and [INTERACTION, e.g. picks it up, adjusts it, turns it on]. [ROOM LIGHT DESCRIPTION], vertical video, curated shelf energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 14. The Thing I Keep Recommending

**Vibe**: "Every time someone asks me, I say this" — organic word-of-mouth energy.

**Structure**:
- 0-3s: Face to camera — "so people keep asking me about…"
- 3-6s: Holding up [PRODUCT], genuine enthusiasm about recommending it
- 6-8s: Quick demo or showing key feature that makes it worth recommending
- 8-10s: "If you're looking for [CATEGORY], this is it" energy, authentic

**Prompt Template**:
> A person talking to camera — "every time someone asks me for a [CATEGORY] recommendation, I say the same thing." They hold up [PRODUCT] from [BRAND] with genuine enthusiasm. They quickly show [KEY FEATURE or DEMO] — the reason it's their go-to recommendation. The energy is authentic word-of-mouth, like texting a friend a product link. Not sponsored energy — organic evangelist energy. Casual setting, selfie angle, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 15. The "Just One Thing" Buy

**Vibe**: Talking to camera about buying just this one thing — disciplined, intentional purchase.

**Structure**:
- 0-3s: Face to camera, holding [PRODUCT] — "I told myself just one thing this month"
- 3-6s: Holding it up, showing it off — "and this was it"
- 6-8s: Explaining why this was the pick — genuine, thoughtful reasoning
- 8-10s: Setting it on the counter with finality — money well spent

**Prompt Template**:
> A person face to camera, holding [PRODUCT] from [BRAND] — "I told myself just one thing this month." Holding it up, showing it off — "and this was it." Explaining why — [REASONING, e.g. replaces something old, non-toxic, aesthetically perfect, solves a real problem]. Setting it on the counter with finality — money well spent. [ROOM], natural light, vertical video, intentional purchase energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`
