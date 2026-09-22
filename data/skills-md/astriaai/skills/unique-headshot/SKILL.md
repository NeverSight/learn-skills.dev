---
name: unique-headshot
description: Use when generating unique AI headshot/model faces without a reference tune. Creates diverse, realistic casting-style headshots with detailed facial trait descriptions.
allowed-tools: Bash(astria:*)
---

# Unique Headshot Generator

Generate realistic, unique face headshots for AI model creation. No reference tune needed — the prompt itself defines the face through detailed physical trait descriptions.

## Prompt Template

```
Close-up studio headshot of a [age]-year-old [ethnicity/heritage] [gender] with [skin_tone] skin, [skin_details], [eye_description], [nose_description], [face_structure], [unique_feature], [hair_description]. Bare shoulders, no clothing visible, no jewelry. [expression], looking at the camera. Clean white background #fff, [lighting], natural realistic skin detail, beauty headshot
```

## Slot Definitions

### Age
- Range: 18–35 for young models, 35–55 for mature
- Always specify exact age (e.g., "22-year-old")

### Ethnicity / Heritage
Describe a specific heritage because it guides realistic facial features — it is a
casting choice, never a default. Rules:
- **Derive it from what is asked or seen.** When the brief comes from a brand's own
  photos, read the heritage off the visible skin tone, hair and features. Never infer
  it from the brand's country, language, store name or currency: an Israeli shoe store,
  a French label or a Japanese marketplace does not make its models Israeli, French or
  Japanese.
- **No house default.** With no visual or written cue, spread a batch across regions
  (East Asia, South Asia, Southeast Asia, West/East/Southern Africa, North Africa and
  the Middle East, Northern/Southern/Eastern Europe, Latin America, Indigenous and
  mixed heritage) and never repeat a region within the batch.
- Single origin: "Nigerian", "Korean", "Irish", "Mexican", "Filipina", "Norwegian",
  "Egyptian", "Peruvian", "Punjabi", "Vietnamese"
- Hyphenated heritage: "Brazilian-Japanese", "Ghanaian-British", "Lebanese-Italian",
  "Maori-Polynesian", "Colombian-Korean", "Turkish-German", "Somali-Swedish"
- Regional descent: "of Eastern European descent", "of West African descent",
  "of Andean descent", "of Han Chinese descent"

### Skin
Always pair a **tone** with a **texture/detail**:
- **Tones**: porcelain, fair, light olive, olive-tan, warm golden-tan, cinnamon-brown, warm caramel, olive-bronze, coppery-bronze, warm umber, deep dark, dark mahogany, ebony
- **Undertones**: pink flush, cool blue-black undertone, warm golden undertone, cool undertone
- **Details** (pick 1-2): dense freckles across cheeks and nose, faint childhood freckles on nose bridge only, visible pores, natural sheen, light freckles, natural hyperpigmentation patchwork, scattered sun freckles, visible blue veins at temples, peach fuzz on jawline

### Eyes
Combine **shape**, **color**, and **distinguishing trait**:
- **Shapes**: almond-shaped, deep-set, round, wide-set, monolid, hooded, large expressive, doe eyes, heavy-lidded
- **Colors**: steel-blue, hazel, green-hazel, dark brown, dark walnut, amber, blue-grey, rose-tinted
- **Traits**: slight upward tilt at outer corners, thick lashes, heavily-lashed, barely-there pale lashes, set close together, spaced wide apart

### Nose
- narrow straight nose, petite button nose with flared nostrils, prominent Roman nose with defined bridge bump, aquiline nose, aquiline hooked nose, broad flat nose, long narrow nose turning slightly downward at tip, small upturned nose, strong nose, narrow bridge nose

### Face Structure
Combine **shape** with **defining bone structure**:
- **Shapes**: angular, heart-shaped tapering to pointed chin, round, narrow, oval, elongated
- **Bones**: sharp cheekbones casting slight shadows, high rounded forehead, strong square jaw, sharp defined jawline wider than forehead, prominent cheekbones, soft jawline, strong angular jawline, delicate pointed chin, small rounded chin

### Unique Features (pick 1-2 for distinctiveness)
These are critical for making each face unique:
- pronounced dimple on left cheek only
- faint scar across left eyebrow
- subtle beauty mark on cheek
- thick arched eyebrows that nearly meet
- asymmetric face with one slightly higher cheekbone
- slightly asymmetric smile
- a pronounced cupid's bow
- thin elegant neck / long neck / impossibly high forehead / elongated swan neck
- visible peach fuzz on jawline

### Hair
Always pulled back to keep face clear. Vary the style:
- sandy-blonde fine hair brushed back flat behind ears into a low knot
- black hair smoothed back into a neat low chignon
- dark curly hair tamed back into a tight bun
- dark espresso hair slicked back into a sleek low ponytail
- jet-black coarse hair pulled tightly into a high sculptural bun
- auburn red hair slicked back into a neat low chignon
- ash blonde hair brushed back behind ears
- straight black hair pulled back into a sleek tight ponytail
- glossy black hair swept back into a sleek twisted bun at the nape
- dark brown hair in a clean slicked-back low chignon
- dark hair slicked back into a tight oiled ballerina bun
- hair braided flat against scalp into a sleek gathered bun at nape
- hair in a severe slicked-back low knot

### Expression
- Poised neutral expression
- Gentle closed-mouth smile
- Calm direct gaze
- Natural relaxed expression
- Direct confident gaze
- Slight closed-mouth smile
- Composed knowing expression
- Soft parted lips, steady gaze
- Relaxed self-assured expression
- Quiet intensity, lips slightly pressed
- Unblinking confrontational stare
- Defiant half-squint

### Lighting
Vary lighting for natural diversity:
- soft ring light
- soft butterfly lighting
- soft diffused studio lighting
- soft even studio lighting
- flat diffused studio lighting
- even soft studio lighting

## Generation Rules

1. **No reference tunes** — these prompts generate entirely new faces (no `<faceid:...>` tokens)
2. **Always generate with Recraft 4.1 Pro**. Before generating, run `astria models` and resolve the current Recraft 4.1 Pro entry by its name/title (the catalog may expose a CLI name such as `recraft-4-1` or a display title such as `Recraft V4.1`). Never hard-code or infer a numeric tune ID, never use the composer default, and never silently substitute another model. Use the discovered model name for `astria generate`; in chat, use the discovered tune ID in `present_generation` — its detailed skin rendering suits beauty headshots
3. **Default parameters**: `--num-images 2 --aspect-ratio 1:1` (Recraft has no `--resolution` — that flag is Gemini-only)
4. **Never repeat the same ethnicity/heritage** in a batch, and never lean on one
   region across batches — check your last few prompts and move on
5. **Every prompt must have at least one unique distinguishing feature** (scar, dimple, beauty mark, asymmetry, etc.)
6. **Hair is always pulled back** — no hair framing or covering the face
7. **Fixed suffix**: `Bare shoulders, no clothing visible, no jewelry. [expression], looking at the camera. Clean white background #fff, [lighting], natural realistic skin detail, beauty headshot`
8. **No photographer references or magazine names** in the prompt — keep it clean and generic

## Batch Generation

When generating multiple unique headshots, maximize diversity:
- Vary ethnicity, skin tone, eye color, face shape, and unique features across the batch
- Alternate between single-origin and mixed-heritage backgrounds
- Mix age range (don't make them all the same age)
- Vary expressions and lighting setups
- Each face should be immediately distinguishable from the others

## Example Prompts

**Prompt 1:**
Close-up studio headshot of a 25-year-old Irish woman with cool-toned fair skin, dense freckles across cheeks and nose, deep-set hazel eyes, strong square jaw, auburn red hair slicked back into a neat low chignon. Bare shoulders, no clothing visible, no jewelry. Composed knowing expression, looking at the camera. Clean white background #fff, soft diffused studio lighting, natural realistic skin detail, beauty headshot

**Prompt 2:**
Close-up studio headshot of a 22-year-old Ethiopian woman with warm umber skin, large expressive round eyes, narrow bridge nose, defined cupid's bow, long neck, dark hair pulled into a smooth high ballerina bun. Bare shoulders, no clothing visible, no jewelry. Soft parted lips, steady gaze, looking at the camera. Clean white background #fff, even soft studio lighting, realistic skin texture with natural sheen, beauty headshot

**Prompt 3:**
Close-up studio headshot of a 27-year-old Mexican woman of Zapotec descent with warm caramel skin and visible pores, wide-set dark brown almond eyes with thick lashes, a strong straight nose, an oval face with high rounded cheekbones and a small rounded chin, a pronounced dimple on the left cheek only, glossy black hair swept back into a sleek twisted bun at the nape. Bare shoulders, no clothing visible, no jewelry. Poised neutral expression, looking at the camera. Clean white background #fff, soft ring light, natural realistic skin detail, beauty headshot

**Prompt 4:**
Close-up studio headshot of a 24-year-old Korean woman with pale milky skin, small monolid eyes, round face, soft jawline, subtle freckles on nose bridge, straight black hair pulled back into a sleek tight ponytail. Bare shoulders, no clothing visible, no jewelry. Slight closed-mouth smile, looking at the camera. Clean white background #fff, flat diffused studio lighting, realistic pore detail, natural skin, beauty headshot

**Prompt 5:**
Close-up studio headshot of a 31-year-old Norwegian man with cool-toned fair skin and light stubble, hooded blue-grey eyes with pale lashes, a prominent Roman nose with a defined bridge bump, an angular face with a strong square jaw, a faint scar across the left eyebrow, ash-blonde hair brushed back flat. Bare shoulders, no clothing visible, no jewelry. Calm direct gaze, looking at the camera. Clean white background #fff, soft butterfly lighting, natural realistic skin detail, beauty headshot
