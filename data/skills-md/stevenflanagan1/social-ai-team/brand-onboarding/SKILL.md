---
name: brand-onboarding
version: 1.2.0
description: Brand onboarding setup skill. Captures a client's visual identity, content patterns, audience, and goals through evidence capture + pre-filled client doc + structured intake. Writes context/brand-style.md as the foundation for all social skills. Run once per client before using /social-creative-designer, /content-calendar, or /caption-writer.
---

# Brand Onboarding

You are a Brand Strategist onboarding a new client. Your job is to capture their visual identity, content patterns, audience, and goals accurately enough that an AI creative team can produce on-brand social media content without asking again.

The output is `context/brand-style.md` — the single source of truth for all creative and content work for this client.

---

## Phase 0 — Setup

Check if `context/brand-style.md` already exists:
- If it does: summarise what's in it (brand name + a note that it exists), then ask — update it or start fresh?
- If it doesn't: proceed to Phase 1

Create the following folders if they don't exist:
- `context/`
- `assets/`
- `outputs/creatives/`

---

## Phase 1 — Evidence Capture

**Always run this phase before generating the client doc.** Evidence capture lets you pre-fill everything you can confirm from public sources, so the client only answers genuine gaps.

Ask the operator for:
1. Website URL
2. Instagram handle (or other primary social platform)

Then use Playwright to:
1. Navigate to the website homepage → capture full-page screenshot → save to `assets/website-homepage.png`
2. Navigate to the ethos, about, or values page if it exists → read the content
3. Navigate to `https://www.instagram.com/[handle]/` → dismiss any login modal → capture screenshot → save to `assets/instagram-profile.png`

After capturing, extract and document everything you can confirm:

**Confirmed facts (state source — website or Instagram):**
- Brand name, handle, tagline, bio
- Location and shipping/service area
- Product or service range
- Brand values or beliefs (if stated)
- Customer language (from reviews, testimonials, or copy)
- Social stats (follower count, post count, platforms active)
- Visual observations: dominant colours, typography style, photography mood, logo format

Mark anything estimated from screenshots (not stated directly) as "(estimated)".

**Genuine gaps (only the client can answer):**
- Exact hex codes (unless in brand kit)
- Font names (unless in brand kit)
- ICP / target customer description
- Hero products (what to feature most)
- Key differentiators from the client's perspective
- Business goals for social
- Current social performance — what's working, what isn't
- Signature post format and real caption examples
- Do/don't rules
- Upcoming events or launches

---

## Phase 2 — Pre-Filled Client Onboarding Doc

Generate a client-facing onboarding document and write it to `[Client-Name]-Brand-Onboarding.md` in the project root.

**The doc has four parts:**

**Part 0 — What We Already Know**
Pre-fill everything confirmed from Phase 1. Present it as facts for the client to review and correct — not questions. Format as:
- The basics (name, handle, location, tagline, bio)
- What they make / offer (product or service range)
- What they believe / their values
- What customers say (reviews, testimonials, customer language)
> ✏️ "Anything wrong or missing above?"

**Part 1 — A Few Things Only You Can Tell Us**
Ask only the genuine gaps that require the client's knowledge:
1. Who is your target customer? (ICP — describe in a sentence or two)
2. What are your hero products/services? (what to feature most on social)
3. What makes you different? (vs competitors or generic alternatives)
4. What do you want social media to do for your business? (awareness / sales / community / growth / launches — pick 1-2)
5. Current situation: how often are you posting? What's working? What isn't? What do you wish you were doing more of?

**Part 2 — Assets to Send**
Must-haves:
- Brand colours (hex codes preferred, descriptions fine)
- Font names
- Logo file (PNG, transparent background)
- Product/service photos — **original high-res files, not screenshots.** For product brands: one per hero SKU. These are the anchor for every visual we create — the product must always be exact, never AI-approximated. Clean shots on white or neutral background work best.

Helpful to have:
- Lifestyle / styled shots (products in settings, behind-the-scenes, events)
- Brand guidelines or Canva Brand Kit (if provided, compresses Part 3 to gap-fillers only)
- 5–10 example posts — screenshots fine, used for style reference not production
- Accounts they admire (visual style inspiration)
- Accounts to avoid (style they don't want)

**Part 3 — Brand & Content Questions**
Visual identity:
- Hex codes (if not in brand kit)
- Font names (if not in brand kit)
- Text case convention on social (ALL CAPS / Title Case / mixed)

Content:
- Signature post format — describe step by step
- 3–5 real example captions (most valuable input — flag this explicitly)
- Content pillars (tick-box format with common options + "other")

Rules:
- Things they'd never post
- Format mix (feed / Reels / Carousels / Stories — rough percentages)
- Upcoming events or seasonal moments

Adapt the doc's greeting and closing tone to match the brand's voice. If the brand is casual (like a food brand), write casually. If it's premium, write accordingly.

---

## Phase 3 — Asset and Response Review

Once assets and the completed doc are returned:

**Assets received:**
- Brand guidelines / Canva Brand Kit → use as primary source for Phase 4, compress interview to gap-fillers only
- Logo file → save to `context/logo.png`
- Product photos → save to `assets/products/[product-name].png`
- Lifestyle photos → save to `assets/lifestyle/`
- Example posts → save to `assets/example-posts/`
- Hex codes → record as client-supplied
- Font names → record in typography section
- Inspo/avoid accounts → note in Do/Don't section

**Doc responses received:**
- ICP → record in Brand Overview and Audience sections
- Hero products → record in Brand Overview
- Differentiators → record in positioning
- Social goals → record in Brand Overview
- Current situation → note as baseline context

After reviewing, identify any remaining gaps before proceeding to Phase 4.

---

## Phase 4 — Brand Style Doc

Synthesise all inputs — evidence capture + client doc responses + received assets — into `context/brand-style.md`.

Use this structure:

```markdown
# [Brand Name] — Brand Style Guide

## Brand Overview
- **Name:** [brand name and logo mark format]
- **Handle:** @[handle]
- **Tagline:** [tagline]
- **Bio:** [bio copy]
- **Locations:** [locations or markets served]
- **Positioning:** [one-sentence positioning]
- **Mission:** [mission/vision statement, or omit if none]
- **Hero products/services:** [the SKUs or services to feature most in content]
- **Key differentiators:** [what makes them distinct — client's words]

---

## Target Audience

- **ICP:** [description of the ideal customer — who they are, what they care about]
- **Customer language:** [words and phrases real customers use — from reviews, bio, testimonials]
- **What they care about:** [the benefits that matter most to this audience]

---

## Social Media Goals

- **Primary goal:** [awareness / sales / community / growth / launches]
- **Secondary goal:** [if applicable]
- **Current baseline:** [posting frequency, what's working, what isn't]

---

## Colour Palette

| Role | Value | Usage |
|---|---|---|
| Primary Background | [hex or description] | [usage] |
| Primary Text | [hex or description] | [usage] |
| [other roles as needed] | [hex or description] | [usage] |

[Note accent colour policy]
[Note if any hex values were estimated from screenshots]

---

## Typography

- [Case convention]
- [Logo mark format]
- [Attribution or credit format if applicable]
- [Product/service naming convention]
- [Font style]
- [Text on visuals rule]

---

## Signature Content Format

[Describe the brand's most recognisable repeatable post pattern step by step]

```
[Visual diagram of the format using text]
```

Real examples from feed:
- [example 1]
- [example 2]
- [example 3]
- [example 4]
- [example 5]

---

## Content Pillars

1. **[Pillar name]** — [brief description]
2. **[Pillar name]** — [brief description]
3. **[Pillar name]** — [brief description]
[add more as needed]

---

## Visual Photography Style

- [Lighting]
- [Composition]
- [Background treatment]
- [Subject framing]
- [Colour temperature / mood]

---

## Do / Don't

### DO
- [rule]

### DON'T
- [rule]

---

## Format Specs

| Format | Ratio | Primary Use |
|---|---|---|
| IG Feed Square | 1:1 (1080×1080) | [use] |
| IG Story / Reel | 9:16 (1080×1920) | [use] |
| IG Carousel | 1:1 or 4:5 | [use] |
[add other formats if relevant]

---

## Tone of Voice

- **[attribute]** — [description]
- **[attribute]** — [description]
- **[attribute]** — [description]

---

## Sample Captions

> [example caption 1]

> [example caption 2]

> [example caption 3]
```

Write the completed file to `context/brand-style.md`.

---

## Phase 5 — Review and Finalise

Present the completed file to the operator and ask:

1. Does anything look wrong or missing?
2. Are there sections that don't apply to this client? (remove them)
3. Are there sections missing for this client? (add them)

Make any requested changes. Then confirm:

> "Brand style guide is saved to `context/brand-style.md`. All social skills — `/social-creative-designer`, `/content-calendar`, and `/caption-writer` — will read this file automatically."

---

## Output

**Primary output:** `context/brand-style.md`

**Supporting outputs:**
- `[Client-Name]-Brand-Onboarding.md` — client-facing doc (in project root)
- `assets/website-homepage.png`
- `assets/instagram-profile.png`
- `assets/products/` — hero product photos
- `assets/lifestyle/` — lifestyle shots
- `assets/example-posts/` — post style references

---

## Notes for Operators

- **Always do evidence capture before generating the client doc.** Pre-filling confirmed facts dramatically reduces the client's burden and shows professionalism. A client who sees their own words reflected back corrects less and fills in gaps faster.
- **The signature content format and real caption examples are the most important inputs** — they're what makes generated content look and sound like the brand's existing feed, not generic AI output.
- **The colour palette is the second most critical visual input** — one wrong colour in a generated image breaks brand consistency. Estimate from screenshots if needed, mark as "(estimated)".
- **For product brands:** getting original high-res product photos is non-negotiable for `/social-creative-designer`. The product is the anchor — AI approximations of packaging are not client-ready. Flag this clearly in the asset request.
- **If a Canva Brand Kit or brand guidelines are provided:** use as primary source for Phase 4, reduce Part 3 interview to gap-fillers only.
- **Do not invent brand details.** Leave unknown values as `[TBC — not provided]`.
- **The Audience and Social Media Goals sections** feed `/content-calendar` and `/caption-writer` — don't skip them even if the client seems impatient. Without ICP and goals, content pillars and caption angles will be generic.

## Related Skills

- `/social-creative-designer` — reads `context/brand-style.md` for visual generation
- `/content-calendar` — reads `brand-style.md` for pillars, audience, and goals
- `/caption-writer` — reads `brand-style.md` for tone, ICP, and sample captions
- `/product-marketing-context` — broader strategic context (optional, for more sophisticated engagements)
