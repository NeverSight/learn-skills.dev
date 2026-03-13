---
name: ugc-lifestyle-broll
description: >-
  UGC lifestyle b-roll video templates for brands. Contains 20 TikTok-native,
  lofi b-roll formats with shot-by-shot structure and AI video generation prompts.
  Use when the user wants to create lifestyle b-roll content — aesthetic scene-setting,
  product-in-context shots, mood pieces, or ambient footage for ads and social.
requires:
  env:
    - RAWUGC_API_KEY
compatibility: >-
  Use alongside the rawugc-api skill for API endpoint knowledge.
  Requires RAWUGC_API_KEY.
homepage: https://github.com/tfcbot/rawugc-skills
source: https://github.com/tfcbot/rawugc-skills
---

# Lifestyle B-Roll UGC Video Formats

20 lofi, TikTok-native b-roll formats for lifestyle brands. Atmospheric, aesthetic, no dialogue. These are the filler clips that make ads feel cinematic and real — product woven naturally into everyday moments.

## How to Use These Formats

1. Identify the user's goal (ad filler, mood-setting, product placement, aesthetic content).
2. Select the format below that best matches.
3. Use the **Prompt Template** to compose the `prompt` field for `POST /videos/generate`. Replace `[BRACKETED]` placeholders with details from the user.
4. Default to `aspectRatio: "portrait"` (9:16) and `nFrames: "10"` unless the format specifies otherwise.
5. Keep the tone ambient, cinematic, and natural. No talking, no CTAs — pure vibes.

---

## Formats

### 1. Morning Light Pour

**Vibe**: Golden morning light streaming through a window onto a surface with product. Warm, still, cinematic.

**Structure**:
- 0-3s: Wide shot of a sunlit room, light pouring through curtains
- 3-6s: Slow pan to a surface (nightstand, counter) where [PRODUCT] sits in the light
- 6-8s: Close-up of light catching the product packaging, golden glow
- 8-10s: Pull back slightly, dust particles floating in the light beam

**Prompt Template**:
> Warm golden morning light streaming through sheer curtains into a clean, minimal room. The light falls across a [SURFACE — e.g. nightstand, bathroom counter, kitchen table] where [PRODUCT] sits naturally among everyday items. Slow, cinematic panning shot. The light catches the [PRODUCT MATERIAL — e.g. glass bottle, matte tube, jar] beautifully. Dust particles float in the sunbeam. No people, no movement except the light. Vertical video, warm tones, peaceful morning energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 2. Coffee Table Moment

**Vibe**: Product sitting on a coffee table while life happens softly in the background.

**Structure**:
- 0-3s: Low-angle shot of coffee table with [PRODUCT], mug, and a book/magazine
- 3-6s: Shallow depth of field — product sharp, background softly blurred
- 6-8s: A hand enters frame, picks up the mug, sips, sets it back down
- 8-10s: Product remains in frame, undisturbed — it belongs here

**Prompt Template**:
> Low-angle shot of a coffee table in a cozy living room. [PRODUCT] sits naturally next to a steaming mug of coffee and an open book. Shallow depth of field — [PRODUCT] is in sharp focus, the background softly blurred. A hand casually enters frame to pick up the mug and take a sip before setting it back. [PRODUCT] stays in frame the whole time, like it just lives there. Warm, lived-in, natural light from a nearby window. Vertical video, lofi aesthetic. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 3. Bag Dump

**Vibe**: Contents of a bag or purse spilled out — product is one of the essentials.

**Structure**:
- 0-3s: Overhead shot of a bag being tipped, contents tumbling out in slow motion
- 3-6s: Items settle — keys, phone, wallet, sunglasses, [PRODUCT]
- 6-8s: Camera slowly zooms in, [PRODUCT] centered among the everyday carry
- 8-10s: A hand reaches in and picks up [PRODUCT], pulling it out of frame

**Prompt Template**:
> Overhead flat-lay shot of the contents of a [BAG TYPE — e.g. tote bag, crossbody, backpack] spilled onto a clean surface. Keys, phone, wallet, sunglasses, lip balm, and [PRODUCT] are scattered naturally. The camera slowly pushes in toward [PRODUCT], centering it among the everyday essentials. A hand reaches in and picks it up. The vibe is "this goes everywhere with me." Clean surface, natural light, vertical video, satisfying overhead angle. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 4. Desk Drop

**Vibe**: Person sets [PRODUCT] down on their desk with a satisfying thud — it's arrived, it's here, hero moment.

**Structure**:
- 0-3s: Clean desk surface, slightly off-center framing, anticipation
- 3-6s: Hand enters frame from above, placing [PRODUCT] down with a deliberate, satisfying drop
- 6-8s: The product settles, camera holds — hero still moment
- 8-10s: Hand pulls away, [PRODUCT] owns the frame — the desk is its stage

**Prompt Template**:
> Clean desk surface with soft natural light. A hand enters the frame from above, placing [PRODUCT] down with a deliberate, satisfying drop. The [PRODUCT DESCRIPTION] settles on the wooden surface. The camera holds — hero still moment. The hand pulls away and [PRODUCT] owns the frame, the desk is its stage. Vertical video, natural light, satisfying product-drop energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 5. Vanity Top-Down

**Vibe**: Overhead shot of a curated vanity or desk setup with product arranged aesthetically.

**Structure**:
- 0-3s: Top-down static shot of a vanity/desk, products and accessories arranged
- 3-6s: A hand enters and rearranges items, nudging [PRODUCT] to center
- 6-8s: Hand exits, perfect flat-lay composition revealed
- 8-10s: Hold on the final arrangement, satisfying stillness

**Prompt Template**:
> Overhead flat-lay shot of a [SURFACE — e.g. marble vanity, wooden desk, bathroom shelf]. [PRODUCT] is arranged among complementary items — [ITEMS — e.g. a candle, dried flowers, jewelry, sunglasses]. A hand enters frame and subtly adjusts [PRODUCT] into the center of the composition. The hand exits, leaving a perfectly curated arrangement. Soft natural light, clean aesthetic, vertical video. Satisfying, organized, aspirational but real. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 6. Window Sill

**Vibe**: Product sitting on a windowsill with the world going by outside. Calm, contemplative.

**Structure**:
- 0-3s: Close-up of [PRODUCT] on a windowsill, soft focus on the view outside
- 3-6s: Rack focus from product to the scene outside (rain, cityscape, greenery)
- 6-8s: Rack focus back to the product, now sharply defined
- 8-10s: A droplet of condensation runs down the window beside it

**Prompt Template**:
> [PRODUCT] sitting on a windowsill with [OUTSIDE SCENE — e.g. rain streaking down the glass, a leafy street, city buildings, a garden]. The camera racks focus from the product to the scene outside and back again. Soft, contemplative, still. Natural light filters through the window, casting gentle shadows. A droplet of condensation catches the light. Vertical video, cinematic depth of field, peaceful ambient energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 7. Hands Close-Up

**Vibe**: Tight shot of hands interacting with the product — opening, holding, turning.

**Structure**:
- 0-3s: Clean hands picking up [PRODUCT] from a surface
- 3-5s: Turning it over slowly, examining the label
- 5-8s: Opening the cap/lid, satisfying click or twist
- 8-10s: Holding it still for a beat, product label facing camera

**Prompt Template**:
> Extreme close-up of clean, well-lit hands picking up [PRODUCT] from a [SURFACE]. They turn it over slowly, examining the label and packaging. The hands open the [CAP TYPE — e.g. twist cap, pump, flip lid] with a satisfying motion. They hold the product still, label facing the camera, for a lingering beat. Soft natural light, shallow depth of field, macro lens energy. No face visible, just hands and product. Vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 8. Towel and Steam

**Vibe**: Post-shower scene — steamy mirror, towel wrapped, product on the counter.

**Structure**:
- 0-3s: Steamy bathroom, mirror slightly fogged, warm diffused light
- 3-6s: A hand wipes a section of the mirror clear, revealing [PRODUCT] on the counter in the reflection
- 6-8s: Camera shifts to the actual product on the counter, water droplets on it
- 8-10s: A towel-wrapped arm reaches for the product

**Prompt Template**:
> A steamy bathroom after a hot shower. The mirror is slightly fogged. A hand wipes a clear streak across the mirror, revealing [PRODUCT] sitting on the counter in the reflection. The camera shifts to [PRODUCT] on the counter — small water droplets on the packaging from the steam. A towel-wrapped arm reaches for it. Warm, humid, intimate. Soft diffused light, vertical video, post-shower ritual energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 9. Bedside Table

**Vibe**: Nightstand scene — phone, lamp, product. The last thing you see before sleep.

**Structure**:
- 0-3s: Side-angle shot of a nightstand — lamp, phone charging, [PRODUCT]
- 3-6s: A hand sets down a phone on the nightstand, next to [PRODUCT]
- 6-8s: The lamp clicks off, room goes dim, product silhouetted
- 8-10s: Soft moonlight or ambient light catches the product's outline

**Prompt Template**:
> Side-angle shot of a cozy nightstand. A warm lamp glows beside a phone, a glass of water, and [PRODUCT]. A hand places the phone down face-first next to [PRODUCT]. The lamp clicks off — the room goes dim. Soft ambient light or moonlight catches the outline of [PRODUCT] on the nightstand. The vibe is end-of-day, winding down, peaceful. Vertical video, warm-to-cool lighting transition. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 10. Lap Blanket Cozy

**Vibe**: Product resting on a lap or blanket — intimate, cozy, personal scale.

**Structure**:
- 0-3s: Soft blanket draped over a lap on a couch, warm indoor lighting
- 3-6s: [PRODUCT] resting naturally on the blanket, surrounded by softness
- 6-8s: A hand gently picks it up, holds it briefly
- 8-10s: Sets it back down on the blanket — intimate, personal, cozy

**Prompt Template**:
> A soft blanket draped over a lap on a couch, warm indoor lighting. [PRODUCT] resting naturally on the blanket-covered lap. A hand gently picks it up, holds it briefly, examining it. Sets it back down on the blanket — intimate, personal, cozy. Vertical video, warm tones, comfort energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 11. Plant Shelf

**Vibe**: Product nestled among plants and greenery on a shelf — organic, natural aesthetic.

**Structure**:
- 0-3s: Wide shot of a shelf with plants, books, and [PRODUCT] arranged naturally
- 3-6s: Slow push-in toward [PRODUCT], greenery framing it
- 6-8s: Close-up of [PRODUCT] with a leaf slightly touching or draped over it
- 8-10s: Soft breeze moves the leaves gently, product stays still

**Prompt Template**:
> A curated shelf filled with potted plants, trailing vines, and a few minimal objects. [PRODUCT] sits among the greenery, looking like it naturally belongs there. The camera slowly pushes in toward [PRODUCT], framed by leaves and stems. A soft breeze gently moves the plants while [PRODUCT] stays perfectly still. Organic, earthy, natural aesthetic. Soft natural light, vertical video, botanical vibes. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 12. Linen and Texture

**Vibe**: Product lying on textured fabric — linen, cotton, knit. Tactile, sensory.

**Structure**:
- 0-3s: [PRODUCT] resting on rumpled linen sheets or a textured throw
- 3-6s: Camera slowly pans across the fabric texture toward the product
- 6-8s: Close-up of where the product meets the fabric — contrasting textures
- 8-10s: A hand gently runs across the fabric near the product

**Prompt Template**:
> [PRODUCT] resting on [FABRIC — e.g. rumpled white linen, a chunky knit throw, raw cotton]. The camera slowly pans across the fabric texture, approaching the product. Close-up of the contrast between the [FABRIC TEXTURE] and [PRODUCT MATERIAL — e.g. smooth glass, matte tube]. A hand gently runs across the fabric near the product, emphasizing the tactile quality. Soft, diffused natural light, vertical video, sensory and calming. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 13. Kitchen Counter

**Vibe**: Product on a kitchen counter during a morning routine — coffee brewing, toast popping.

**Structure**:
- 0-3s: Wide shot of a kitchen counter, morning light, coffee maker brewing in background
- 3-6s: [PRODUCT] sits among the morning scene — fruit bowl, mug, toast plate
- 6-8s: Steam rises from the coffee, product catches the warm light
- 8-10s: A hand grabs the mug, leaving [PRODUCT] in the scene as the morning continues

**Prompt Template**:
> A bright kitchen counter during a morning routine. Coffee is brewing in the background, steam rising. [PRODUCT] sits naturally on the counter among everyday items — a fruit bowl, a mug, a plate of toast. Warm morning light fills the scene. A hand reaches for the coffee mug, but [PRODUCT] stays in frame — part of the daily ritual. The vibe is easy, routine, real. Vertical video, warm tones, domestic comfort. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 14. Golden Hour Portrait

**Vibe**: Person holding product during golden hour — warm backlight, dreamy glow.

**Structure**:
- 0-3s: Silhouette or backlit shot of a person at golden hour
- 3-6s: They raise [PRODUCT] into the light, it glows warmly
- 6-8s: Close-up of [PRODUCT] catching the golden light, lens flare
- 8-10s: Pull back to show person and product against the sunset/golden sky

**Prompt Template**:
> A person standing outdoors during golden hour, warm backlight creating a dreamy glow around them. They raise [PRODUCT] into the light — it catches the golden rays beautifully. Close-up of [PRODUCT] glowing in the warm light, a subtle lens flare adding to the cinematic feel. Pull back to show the person holding [PRODUCT] against the [BACKGROUND — e.g. sunset sky, golden field, beach horizon]. Vertical video, warm golden tones, ethereal and aspirational. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 15. Rain Window

**Vibe**: Product on a surface near a rain-streaked window — moody, cozy, atmospheric.

**Structure**:
- 0-3s: Rain streaking down a window, soft focus, ambient sound energy
- 3-6s: Rack focus to [PRODUCT] sitting on the sill or nearby table
- 6-8s: Raindrops continue, product sharp in focus, reflections on its surface
- 8-10s: A warm light flickers on nearby (candle or lamp), adding warmth to the scene

**Prompt Template**:
> Rain streaking down a window, the outside world soft and blurred. The camera racks focus to [PRODUCT] sitting on the [SURFACE — e.g. windowsill, side table] nearby. Rain continues to pattern the glass, creating moving reflections on [PRODUCT]'s surface. A warm light — a candle or lamp — flickers on, adding a cozy glow to the moody scene. Vertical video, cinematic depth of field, rainy day atmosphere. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 16. Workout Cool-Down

**Vibe**: Post-workout scene — gym bag, water bottle, product. Active lifestyle context.

**Structure**:
- 0-3s: A gym bag open on a bench, water bottle and towel visible
- 3-6s: A hand pulls [PRODUCT] from the bag, sets it on the bench
- 6-8s: Person in workout clothes, slightly flushed, reaches for [PRODUCT]
- 8-10s: They use/hold the product, post-workout glow on their face

**Prompt Template**:
> A gym bag sits open on a bench. Inside: a water bottle, towel, earbuds, and [PRODUCT]. A hand pulls [PRODUCT] out and sets it on the bench. A person in workout clothes, slightly flushed with a post-exercise glow, reaches for [PRODUCT]. They hold it casually — it's part of their active routine. Natural gym or outdoor light, vertical video, healthy lifestyle energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 17. Sunset Drive

**Vibe**: Product in a car cupholder or dashboard during a golden hour drive.

**Structure**:
- 0-3s: Interior car shot, golden light flooding through the windshield
- 3-6s: [PRODUCT] sitting in the cupholder or on the passenger seat
- 6-8s: Shadows of trees or buildings flicker across the product as the car moves
- 8-10s: A hand reaches for the product at a red light, then pulls back

**Prompt Template**:
> Interior of a car during a golden hour drive. Warm light floods through the windshield, casting long shadows. [PRODUCT] sits in the [LOCATION — e.g. cupholder, passenger seat, center console]. Shadows of passing trees and buildings flicker across the product as the car moves. A hand reaches for [PRODUCT] at a stoplight, then pulls back as the light turns green. Cinematic, warm, in-motion. Vertical video, golden tones, road trip energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 18. Mirror Reflection

**Vibe**: Product seen through a mirror — bathroom, bedroom, or full-length. Layered composition.

**Structure**:
- 0-3s: Shot of a mirror reflecting a room, [PRODUCT] visible in the reflection
- 3-6s: Camera adjusts focus between the mirror surface and the reflection
- 6-8s: A person walks past in the background of the reflection, blurred
- 8-10s: Focus settles on [PRODUCT] in the mirror, sharp and centered

**Prompt Template**:
> A [MIRROR TYPE — e.g. round bathroom mirror, full-length bedroom mirror, vintage vanity mirror] reflecting a room. [PRODUCT] is visible in the reflection, sitting on a nearby surface. The camera plays with focus — shifting between the mirror's surface and the reflected scene. A person walks through the background of the reflection, softly blurred. Focus settles on [PRODUCT], sharp and centered in the mirror. Layered, artistic, vertical video, natural light. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 19. Picnic Spread

**Vibe**: Product at an outdoor picnic or park hang — blanket, snacks, sunshine.

**Structure**:
- 0-3s: Overhead shot of a picnic blanket with food, drinks, and [PRODUCT]
- 3-6s: Camera slowly lowers to a side angle, [PRODUCT] in the foreground
- 6-8s: A hand reaches for a snack, [PRODUCT] stays in frame
- 8-10s: Dappled sunlight through trees plays across the scene

**Prompt Template**:
> Overhead shot of a picnic blanket spread on grass. Fresh fruit, a baguette, drinks, and [PRODUCT] are arranged naturally on the blanket. The camera lowers to a side angle, placing [PRODUCT] in the foreground. A hand reaches for a piece of fruit while [PRODUCT] stays in focus. Dappled sunlight filters through tree leaves above, casting soft patterns across the scene. Outdoor, warm, carefree. Vertical video, natural light, summer energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 20. End-of-Day Unwind

**Vibe**: Product on a bathroom counter or tray at night — candle lit, warm tones, winding down.

**Structure**:
- 0-3s: A bathroom or vanity lit by candlelight, warm amber tones
- 3-6s: [PRODUCT] sits on a tray or counter alongside a candle and small plant
- 6-8s: A hand lights the candle (or it's already lit, flickering)
- 8-10s: The warm light dances across [PRODUCT]'s surface, intimate and still

**Prompt Template**:
> A bathroom counter or vanity tray at night, lit by warm candlelight. [PRODUCT] sits alongside a burning candle and [ACCENT ITEMS — e.g. a small succulent, a folded towel, a ring dish]. The candlelight flickers, casting dancing shadows and warm amber light across [PRODUCT]'s surface. Everything is still and quiet — the day is done. Intimate, warm, ritualistic. Vertical video, amber and shadow tones, nighttime wind-down energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`
