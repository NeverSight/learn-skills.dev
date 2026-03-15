---
name: ugc-fashion
description: >-
  UGC video format templates for fashion brands. Contains 20 TikTok-native,
  lofi video formats with shot-by-shot structure and AI video generation prompts.
  Use when the user wants to create fashion UGC content — OOTDs, try-on hauls,
  styling videos, or outfit showcases.
requires:
  env:
    - RAWUGC_API_KEY
compatibility: >-
  Use alongside the rawugc-api skill for API endpoint knowledge.
  Requires RAWUGC_API_KEY.
homepage: https://github.com/tfcbot/rawugc-skills
source: https://github.com/tfcbot/rawugc-skills
---

# Fashion UGC Video Formats

20 lofi, TikTok-native video formats for fashion brands. Raw, authentic, easy to produce. No hard CTAs — these feel like real people showing how they actually dress.

## How to Use These Formats

1. Identify the user's goal (new collection launch, styling inspiration, size-inclusive showcase, seasonal content).
2. Select the format below that best matches.
3. Use the **Prompt Template** to compose the `prompt` field for `POST /videos/generate`. Replace `[BRACKETED]` placeholders with details from the user.
4. Default to `aspectRatio: "portrait"` (9:16) and `nFrames: "10"` unless the format specifies otherwise.
5. Keep the tone casual, genuine, unscripted. These should feel like someone showing their friend what they're wearing.

---

## Formats

### 1. Mirror OOTD

**Vibe**: Classic mirror outfit check — simple spin, natural lighting, main character energy.

**Structure**:
- 0-3s: Standing in front of a full-length mirror, phone visible in reflection
- 3-6s: Slow reveal from feet up, showing the full outfit
- 6-8s: A casual spin or turn, showing the back and sides
- 8-10s: Final pose — confident, effortless, looking at the mirror

**Prompt Template**:
> A person standing in front of a full-length mirror taking an OOTD photo/video. They're wearing [OUTFIT DESCRIPTION — e.g. oversized blazer, wide-leg pants, and loafers]. The camera (phone in reflection) slowly captures the outfit from shoes up. They do a casual spin showing all angles. The vibe is confident but effortless — they know they look good. Natural bedroom/hallway lighting, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 2. Try-On in Real Time

**Vibe**: Getting dressed on camera — genuine first reaction to how it fits.

**Structure**:
- 0-3s: Holding up the piece on a hanger, showing it flat
- 3-6s: Putting it on — pulling over head, buttoning up, zipping
- 6-8s: First look in mirror or camera — genuine reaction to the fit
- 8-10s: Adjusting, smoothing, final satisfied expression

**Prompt Template**:
> A person holding up [GARMENT] on a hanger, showing it to the camera. They start putting it on — [DRESSING ACTION, e.g. pulling it over their head, buttoning it up, stepping into it]. First look at themselves — genuine surprise at how well it fits. They adjust and smooth the fabric, checking different angles. Real, unscripted reaction energy. Bedroom setting, natural light, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 3. Fabric Close-Up

**Vibe**: Extreme close-up of fabric texture, stitching, material quality — ASMR for fashion people.

**Structure**:
- 0-3s: Close-up of [PRODUCT] fabric — fingers running across the material
- 3-6s: Camera captures weave, texture, stitching detail
- 6-8s: Hand lifts the garment slightly to show drape and weight
- 8-10s: Pull back to show the full piece on a hanger or folded neatly

**Prompt Template**:
> Extreme close-up of [GARMENT from BRAND]. Fingers slowly run across the fabric, the [FABRIC DETAIL — e.g. fine knit, weave, grain] visible in detail. The camera captures the [TEXTURE DETAILS — e.g. weave, ribbed cuffs, clean stitching at the seams]. A hand lifts the garment slightly to show the [DRAPE/WEIGHT QUALITY — e.g. luxurious drape and weight]. Pull back to reveal the full piece [DISPLAY — e.g. folded neatly on a wooden surface, hanging on a wooden hanger]. Natural light, vertical video, tactile ASMR energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 4. Closet Dig

**Vibe**: Rummaging through closet, pulling out the piece — "found it" energy.

**Structure**:
- 0-3s: Hands pushing through hangers in a closet, searching
- 3-5s: Pulling out [GARMENT] — "this one" moment
- 5-8s: Holding it up, admiring it, maybe pressing it against body
- 8-10s: Walking toward mirror to try it on, excited energy

**Prompt Template**:
> A person rummaging through a full closet, pushing hangers aside, searching for something specific. They pull out [GARMENT] with a "found it" expression — holding it up, admiring it. They press it against their body in the mirror, head tilted, already styling it mentally. They head to try it on. The energy is getting-ready excitement, real closet chaos. Natural bedroom light, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 5. The Tag Check

**Vibe**: Checking the tag, showing the size, the brand — the small details that matter.

**Structure**:
- 0-3s: Person wearing [PRODUCT], hand reaches to the back/inside collar
- 3-6s: Pulling out the tag, showing it to camera — brand, size, material
- 6-8s: Letting the tag drop back, smoothing the fabric where they checked
- 8-10s: Quick adjustment of the piece, satisfied nod at mirror

**Prompt Template**:
> A person wearing [GARMENT from BRAND], hand reaching to the [TAG LOCATION — e.g. inside collar, back neckline]. They pull out the tag and show it to camera — the [BRAND] label, the size, the material blend. They let the tag drop back and smooth the fabric at the [AREA]. Quick adjustment of the [GARMENT] in the mirror, a satisfied nod — the details check out. [SETTING — e.g. bedroom mirror], natural light, vertical video, detail-oriented energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 6. Hanger Appeal

**Vibe**: Showing the piece on the hanger, examining it before putting it on — the anticipation.

**Structure**:
- 0-3s: [PRODUCT] on a hanger held up against a clean wall or closet door
- 3-6s: Turning the hanger slowly, showing front and back
- 6-8s: Close-up of details — buttons, zippers, labels, seams
- 8-10s: Pulling it off the hanger with intention — about to put it on

**Prompt Template**:
> [GARMENT from BRAND] on a [HANGER TYPE — e.g. wooden hanger, velvet hanger] held against a [BACKGROUND — e.g. white wall, closet door]. Slowly turning the hanger to show the front — [FRONT DETAILS — e.g. the structured silhouette, the buttons] — then the back. Close-up of the details: [CLOSE-UP DETAILS — e.g. the engraved buttons, the lined interior, the clean seams]. Pulling it off the hanger with intention, ready to wear. Natural light, vertical video, quiet anticipation energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 7. The Fold

**Vibe**: Satisfying folding or rolling technique — Marie Kondo energy for your favorite piece.

**Structure**:
- 0-3s: [PRODUCT] laid flat on a clean surface
- 3-6s: Hands begin a precise, satisfying fold — smooth movements
- 6-8s: The fold completes into a neat, compact shape
- 8-10s: Placing the folded piece into a drawer or stack — everything tidy

**Prompt Template**:
> [GARMENT from BRAND] laid flat on a [SURFACE — e.g. white bed, marble counter, clean table]. Hands begin a precise, satisfying fold — smoothing the [FABRIC TYPE] flat, [FOLD STEPS — e.g. folding in the legs, rolling from waistband down] into a compact shape. The fold completes into a neat, compact [SHAPE — e.g. rectangle, square]. Placing the folded [GARMENT] into a [DESTINATION — e.g. drawer alongside other perfectly folded pieces, neat stack] — everything tidy, Marie Kondo approved. Natural light, vertical video, satisfying organization energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 8. Thrift Flip Energy

**Vibe**: Taking a piece that looks basic on the hanger and styling it into a full look.

**Structure**:
- 0-3s: Holding up a plain/basic-looking garment — "trust me on this"
- 3-6s: Pairing it with unexpected pieces — layering, tucking, accessorizing
- 6-8s: The full styled look revealed — way better than expected
- 8-10s: Proud reveal, the transformation energy

**Prompt Template**:
> A person holding up [GARMENT] that looks plain and basic on the hanger — nothing special. They start styling it — [STYLING STEPS, e.g. tucking it into high-waisted pants, adding a belt, layering a jacket, rolling the sleeves]. Piece by piece, the outfit comes together. Final reveal — the look is unexpectedly fire. Proud expression, "told you" energy. Bedroom or closet setting, natural light, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 9. Color Match

**Vibe**: Holding the piece up to different items to show what it goes with — color palette moment.

**Structure**:
- 0-3s: Person holding [PRODUCT] up in front of them, looking at it
- 3-6s: Holding it next to other pieces from their closet — showing color combos
- 6-8s: Finding the perfect match, holding the two pieces together
- 8-10s: Satisfied expression, draping the combo over their arm

**Prompt Template**:
> A person standing at their open closet holding [GARMENT from BRAND] up in front of them. They hold it next to [ITEM 1 — e.g. a white tee] — nice. Then next to [ITEM 2 — e.g. a navy striped shirt] — even better. Then next to [ITEM 3 — e.g. dark denim] — perfect match. They hold the [GARMENT] and the [BEST MATCH] together with a satisfied expression, draping both over their arm. [SETTING — e.g. bedroom closet], natural light, vertical video, styling energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 10. Size Honest

**Vibe**: "I'm a size X and here's how this actually fits" — genuine, no filter.

**Structure**:
- 0-3s: Talking to camera, stating their size/measurements honestly
- 3-6s: Showing the garment — front, side, back angles
- 6-8s: Pointing out fit details — where it's snug, where it drapes
- 8-10s: Final honest verdict — genuine thumbs up or "runs a little big" energy

**Prompt Template**:
> A person talking to camera — "I'm a size [SIZE] and here's how [GARMENT] from [BRAND] actually fits." They turn to show front, side, and back views. They point out specifics — [FIT DETAILS, e.g. "the waist sits here," "it's a little loose in the shoulders," "perfect length"]. Honest, helpful, no filter. Their verdict is genuine. Good lighting to see the real fit and fabric. Natural setting, vertical video, selfie-to-mirror angles. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 11. Rain Day Fit

**Vibe**: Styled for the weather — practical but still cute, real conditions.

**Structure**:
- 0-3s: Looking out window at rain/overcast weather
- 3-6s: Getting dressed for it — layering, grabbing a jacket, choosing shoes
- 6-8s: Full outfit in mirror — weather-appropriate and stylish
- 8-10s: Walking out the door into the real weather, outfit holding up

**Prompt Template**:
> A rainy day outfit video. Person looks out the window at overcast skies, then starts getting dressed. They layer [OUTFIT — e.g. trench coat, knit sweater, waterproof boots from BRAND]. Mirror check — practical but cute. They step outside into real rain — the outfit works, they look good despite the weather. The message is: bad weather doesn't mean bad style. Natural overcast lighting, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 12. The Stretch Test

**Vibe**: Testing the stretch and movement of the fabric — pulling, bending, showing flexibility.

**Structure**:
- 0-3s: Close-up of [PRODUCT] on body, hands gripping the fabric
- 3-6s: Gentle stretch pull — showing the four-way stretch or give of the material
- 6-8s: Release — fabric snaps back perfectly, no distortion
- 8-10s: Smoothing the fabric with a satisfied hand pass — it holds up

**Prompt Template**:
> Close-up of [GARMENT from BRAND] on the [BODY AREA — e.g. leg, torso, arm], hands gripping the fabric at the [GRIP POINT — e.g. thigh, waist, sleeve]. A gentle stretch pull outward — showing the [STRETCH TYPE — e.g. four-way stretch, natural give] of the [MATERIAL]. Release — the fabric snaps back perfectly to shape, zero distortion. Smoothing the fabric with a satisfied hand pass — it holds up beautifully. Natural light, vertical video, quality-test energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 13. The Uniform

**Vibe**: "I wear this combo every week" — signature look showcase, consistency over trends.

**Structure**:
- 0-3s: Reaching for the same pieces in the closet — muscle memory
- 3-6s: Putting the combination together, well-practiced ease
- 6-8s: The uniform assembled — it just works, every time
- 8-10s: Confident walk out, this is their look and they own it

**Prompt Template**:
> A person reaching into their closet with zero hesitation — they know exactly what they're grabbing. [THE UNIFORM — e.g. white tee, black blazer, straight-leg jeans, and loafers from BRAND]. They get dressed with practiced ease, everything fitting perfectly. The combination is simple but intentional — this is their go-to, their signature. They walk out with quiet confidence. The vibe is consistency over trends. Natural light, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 14. The Hand Feel

**Vibe**: Running hands over the piece, feeling the quality — tactile, sensory, cozy.

**Structure**:
- 0-3s: [PRODUCT] draped over lap or across a surface
- 3-6s: Hands running slowly over the fabric — feeling the texture, the weight
- 6-8s: Bunching it slightly, showing the softness and recovery
- 8-10s: Holding it up to cheek or pressing it — pure comfort

**Prompt Template**:
> [GARMENT from BRAND] draped across a [SURFACE — e.g. lap on a couch, bed, chair arm]. Hands run slowly over the [FABRIC TYPE] — feeling the [TEXTURE QUALITY — e.g. incredible softness, the weight and drape]. Bunching it slightly to show how it [RECOVERY — e.g. springs back, no pilling, just pure softness]. Holding it up to cheek and pressing it in — pure cozy comfort. [SETTING — e.g. living room, bedroom], warm light, vertical video, sensory ASMR energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 15. Color Story

**Vibe**: Entire outfit in one color family — aesthetic broll, visual harmony.

**Structure**:
- 0-3s: First piece — in the color (e.g., all earth tones, all cream, all black)
- 3-6s: Adding matching pieces, same color palette throughout
- 6-8s: Full monochromatic or tonal outfit assembled
- 8-10s: Aesthetic broll — walking, posing, the color harmony is the star

**Prompt Template**:
> A monochromatic outfit video in [COLOR FAMILY — e.g. all cream, head-to-toe black, earth tones]. Piece by piece: [OUTFIT PIECES from BRAND] — all in the same tonal range. The full outfit assembled is visually harmonious, satisfying. Aesthetic broll shots — walking slowly, fabric catching the light, the color story is the hero. Clean backgrounds that complement the palette. Vertical video, soft golden light. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 16. Hand-Me-Up

**Vibe**: Styling a piece borrowed from a friend, partner, or parent — making it your own.

**Structure**:
- 0-3s: Holding up the borrowed piece — "stole this from my [person]"
- 3-6s: Putting it on, immediately making it work with their own style
- 6-8s: The borrowed piece looks completely different on them — elevated
- 8-10s: Confident result, the piece has a new life

**Prompt Template**:
> A person holding up [GARMENT] — something clearly borrowed. "Stole this from my [PERSON — e.g. dad, partner, roommate]" energy. They put it on and immediately make it their own — [STYLING, e.g. rolling the sleeves, belting it, pairing with heeled boots]. The oversized/borrowed piece looks completely elevated and intentional on them. New context, new outfit, same piece. Casual bedroom setting, natural light, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 17. Get Ready With Me Silent

**Vibe**: No talking, just getting dressed — music only, aesthetic cuts.

**Structure**:
- 0-3s: Laying out outfit pieces on bed, flat lay
- 3-6s: Getting dressed — pulling on each piece, close-ups of fabric
- 6-9s: Accessories going on — watch, jewelry, belt
- 9-12s: Final mirror look, adjusting, ready to go
- 12-15s: Walking out the door, complete look in motion

**Prompt Template**:
> A silent GRWM fashion video. No talking, just vibes. [OUTFIT PIECES from BRAND] laid out on a bed. The person gets dressed piece by piece — close-ups of fabric textures, buttons being done, sleeves being rolled. Accessories added — [ACCESSORIES]. Final mirror check, small adjustments. They walk out the door looking complete. The entire video is visual — music-video energy without words. Warm bedroom lighting, aesthetic cuts, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "15"`

---

### 18. In My X Era

**Vibe**: Leaning into a trend or aesthetic identity — "in my [aesthetic] era."

**Structure**:
- 0-3s: Text or face-to-camera declaring the era — "in my quiet luxury era" etc.
- 3-6s: Outfit that perfectly embodies the aesthetic
- 6-8s: Styled details — the specific touches that sell the vibe
- 8-10s: Full aesthetic moment — walking, posing, living the era

**Prompt Template**:
> "In my [ERA/AESTHETIC — e.g. quiet luxury, coastal grandmother, dark academia, clean girl] era" energy. A person wearing [OUTFIT from BRAND] that perfectly embodies the aesthetic. Close-ups of the styling details that sell it — [DETAILS, e.g. cashmere texture, specific shoes, particular accessories]. They're fully in the vibe — walking, posing, living it. The outfit isn't just clothes, it's a whole mood. Aesthetic-appropriate setting, vertical video, dreamy lighting. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 19. That Girl Outfit

**Vibe**: Aspirational but attainable everyday outfit — soft morning energy.

**Structure**:
- 0-3s: Morning setting — clean space, natural light pouring in
- 3-6s: Getting dressed in a put-together but effortless outfit
- 6-8s: Grabbing coffee, bag, heading out — "that girl" energy
- 8-10s: Walking out into the day, looking effortlessly assembled

**Prompt Template**:
> "That girl" morning routine outfit. A clean, bright space — morning light streaming in. The person gets dressed in [OUTFIT from BRAND] — [DESCRIPTION, e.g. matching set, clean sneakers, minimal jewelry]. Everything is intentional but not try-hard. They grab their coffee and tote bag, heading out the door with effortless "I have my life together" energy. Aspirational but attainable. Bright, clean aesthetic, morning light, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 20. The Hang

**Vibe**: Hanging the piece in its spot in the closet — it's earned its place.

**Structure**:
- 0-3s: Holding [PRODUCT] on a hanger, standing in front of open closet
- 3-6s: Finding the right spot on the rack, sliding hangers aside
- 6-8s: Placing it in its spot, adjusting the shoulders on the hanger
- 8-10s: Stepping back to see it in context — it belongs here

**Prompt Template**:
> Holding [GARMENT from BRAND] on a [HANGER TYPE — e.g. wooden hanger, velvet hanger], standing in front of an open closet. Finding the right spot on the rack — sliding hangers aside to make room. Placing the [GARMENT] in its spot, adjusting the shoulders perfectly on the hanger. Stepping back to see it in context among the other pieces — it belongs here, [WARDROBE ROLE — e.g. the anchor of the wardrobe, the statement piece]. [SETTING — e.g. bedroom closet], natural light, vertical video, wardrobe curation energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`
