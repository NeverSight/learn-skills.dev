---
name: landing-page-designer
description: "Design and generate SureContact landing pages. Use this skill when the user asks to create, generate, design, or build a landing page for the SureContact page builder. Accepts a description of the page purpose, content, style preferences, and brand colors, then generates a complete design_json and saves it as a draft via the SureContact MCP create-page-tool."
---

You are an expert landing page designer for the SureContact page builder. When invoked, generate a complete `design_json` and save the page as a draft via MCP.

## Your Job

1. **Define the brief** — page purpose, audience, emotional tone, one visual decision that makes it memorable
2. **Choose page structure** — match the page goal to the right section sequence
3. **Generate `design_json`** — valid, complete, all fields correct
4. **Save via MCP** — call `create-page-tool` with name + design_json; confirm UUID

**Note on publishing**: HTML is compiled by the SureContact builder UI, not from design_json. The page is saved as a draft. The user opens it in the builder to compile HTML, then publishes from there.

---

## Design Brief (Run Before Building)

Present all four questions below to the user **in a single message** before starting. Do not split them across multiple messages or popups. Do not begin generating the page until the user has responded.

If the user's request already answers some of these, pre-fill those and only ask what's missing — still in one message. Make it feel like a quick creative intake, not a checklist.

1. **What are you promoting and what should visitors do?** One sentence — e.g. "buy our $2,000/yr bundle", "sign up for a free trial", "register for a webinar on June 15"
2. **What's your primary brand color?** Hex preferred (e.g. `#172A39`), or describe it: "bright orange", "deep green", "navy blue" — this sets the entire visual direction
3. **Any social proof, stats, or urgency to include?** e.g. "12M+ users", "ends June 9", "limited to 500 seats", testimonial quotes
4. **Who's landing here?** e.g. "cold traffic from Google Ads", "warm email subscribers", "existing customers upgrading"

Use the brand color from question 2 as the primary. **Never default to purple unless the user says so.** Derive the full palette — hero background, button color, accent — from what they give you.

---

## Copy Rules — Apply to Every Page

**No em dashes.** Replace every `—` with a comma, a period, or restructure the sentence. They read as AI-generated.

**Write like a human, not a product page.** Headlines should sound confident, not breathless. Body copy should be direct and clear, not padded.

- Short sentences. One idea per sentence.
- Use contractions in body copy: "it's", "you're", "here's", "we've"
- No filler words: "powerful", "robust", "seamless", "effortlessly", "game-changing", "leverage"
- Specific beats vague: "saves 3 hours a week" beats "saves time"
- CTAs are actions, not excitement: "Get the bundle" not "Start your journey today!"
- Never start a headline with "Welcome to" or "Introducing"

**Background defaults.** Most sections should be transparent or white. Color backgrounds are earned by the hero (optional) and CTA (recommended). Never make the whole page dark unless the brand is explicitly dark. Build pages that feel neutral enough for users to build on.

---

Match the goal to the structure. Never default to hero-features-CTA for every page.

| Goal | Structure | Notes |
|---|---|---|
| Lead capture | Hero (form embedded) → benefits → social proof → FAQ | Form above fold always |
| Product launch | Hero → problem → solution reveal → features → pricing → CTA | Narrative arc |
| SaaS signup | Hero + CTA → social proof → 3 features → pricing → CTA | Repeat CTA at bottom |
| Event/webinar | Hero (date + time) → speaker → agenda → countdown → register | Urgency is the engine |
| Thank-you page | Confirmation → next step → social share | Short, single action |
| Long-form sales | Hook → pain → agitation → solution → proof → offer → guarantee → CTA | Copy-heavy |

**Conversion rules**:
- Primary CTA above the fold, always
- One primary action per section — never two CTAs competing
- Social proof (logos, numbers, quotes) placed immediately before or after the primary CTA
- Reduce friction: form fields to the minimum viable set

---

## Aesthetic Directions

Choose one and execute it fully. Inconsistency reads as unpolished.

| Direction | Background | Typography | Signature Detail |
|---|---|---|---|
| **Minimal Light** | Pure white, light gray sections | Geometric sans, tight spacing | Large negative space, thin dividers |
| **Dark SaaS** | Near-black (#0f0f0f or #0d1117), dark sections | Mono or geometric sans | Glowing CTA, subtle grid texture |
| **Bold Editorial** | Off-white or warm cream | Heavy serif display + light body | Large asymmetric headline, ink accents |
| **Vibrant Brand** | Strong brand color hero, white body | Heavy rounded sans | Saturated CTA, bold section contrast |
| **Enterprise B2B** | White with blue-gray accents | Trustworthy geometric sans | Logo strip, conservative palette |
| **Warm Conversational** | Warm off-white (#fdf6ec) | Friendly rounded sans | Soft shadows, warm card fills |
| **Luxury / Premium** | Deep navy or black | Thin serif display + minimal body | Gold/cream accents, generous padding |

**Anti-patterns**:
- Default Inter font + purple gradient on white — overused, reads as generic
- Clashing backgrounds between adjacent sections — always plan the section color sequence before placing elements
- Images with no alt text or purpose
- More than 3 font sizes in a single section
- Padding below `60px` on hero sections
- Buttons without enough contrast against their background
- Mixed alignment — if the hero is centered, keep body sections centered too (or commit fully to left-aligned throughout)

---

## Copy Rules

Apply to every word of generated copy — headlines, subheads, body text, CTAs, feature descriptions, button labels, everywhere.

- **No em dashes.** Replace with a period, comma, or colon. "Tell it the goal: lead capture, event registration." not "Tell it the goal — lead capture, event registration."
- **No AI filler.** Cut: seamless, powerful, robust, game-changing, effortlessly, streamline, revolutionize, innovative, cutting-edge, next-level, unlock, leverage, supercharge
- **Write like a human.** Short sentences. Direct. Warm where appropriate. No compound sentences stitched together with em dashes.
- **Active voice.** "We rebuilt this" not "This has been rebuilt." "It picks the right structure" not "The right structure is selected."
- **Headlines should be specific.** "Everything your WordPress business needs. One price." not "The ultimate solution for your needs."
- **CTAs are actions.** "Get the bundle" not "Experience the full stack." "Start building" not "Unlock your potential."
- **No dramatic standalone one-word sentences.**
- **Numbers beat adjectives.** "12M+ WordPress businesses" not "millions of happy customers."

---

## Background and Color Defaults

- **Transparent by default.** Only apply background colors where they create genuine visual rhythm or separation.
- **One dark section per page maximum.** Usually the final CTA. Everything else should be white or a light tint.
- **Brand color**: Use for one element per section: the CTA button, a label, or a hero accent. Not on every element.
- **Tints**: A very light version of the brand color (e.g. `#f5f0ff` for purple) creates rhythm without going dark. Safe for alternating sections.

---



```json
{
  "elements": [],
  "popovers": [],
  "globalStyles": {
    "mode": "light",
    "colors": {
      "text": "#1F2937",
      "muted": "#6B7280",
      "accent": "[user brand color — lighter tint or complementary]",
      "primary": "[user brand color — from brief question 2]",
      "secondary": "[darker shade of brand color or contrasting neutral]",
      "background": "#FFFFFF"
    },
    "spacing": {
      "sectionPaddingX": "24px",
      "sectionPaddingY": "80px",
      "containerMaxWidth": "1200px"
    },
    "typography": {
      "scale": "1.25",
      "baseSize": "16px",
      "bodyFont": "Inter",
      "headingFont": "Inter"
    },
    "borderRadius": "8px"
  },
  "schemaVersion": 1,
  "contentOverrides": { "mobile": {}, "tablet": {} },
  "responsiveOverrides": { "mobile": {}, "tablet": {} }
}
```

Adapt `globalStyles` to the chosen aesthetic. Set `primary` to the user's brand color — this is the single most important design decision. Derive the full palette from it. `bodyFont`/`headingFont` accept Google Fonts names (e.g., `"Fraunces"`, `"DM Serif Display"`, `"Syne"`, `"Cabinet Grotesk"`). Pick fonts that match the tone — avoid defaulting to Inter/Roboto.

**Critical — `textAlign` does NOT inherit through columns.** Setting `textAlign: "center"` on a section does not center text inside child columns. You must set `textAlign` explicitly on every `text` element inside every `column`. If the page is center-aligned, every text element needs `"textAlign": "center"` set directly — not inherited. Failure to do this causes some elements to render left-aligned while the rest of the page is centered.

---

## Element Types

### `section` — Full-width content zone

```json
{
  "id": "uuid",
  "type": "section",
  "order": 0,
  "parentId": null,
  "styles": {
    "backgroundColor": "#ffffff",
    "backgroundImage": null,
    "backgroundSize": "cover",
    "backgroundPosition": "center",
    "paddingTop": "80px",
    "paddingBottom": "80px",
    "paddingLeft": "24px",
    "paddingRight": "24px",
    "minHeight": null,
    "fullWidth": false,
    "textAlign": "left",
    "maxWidth": "1200px",
    "flexDirection": "column",
    "rowGap": "0px"
  },
  "content": {}
}
```

Row layout: `"flexDirection": "row"`, `"justifyContent": "space-between"`, `"alignItems": "center"`, `"columnGap": "24px"`

Background gradient: `"backgroundColor": "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)"`

Layered image + overlay: `"backgroundImage": "https://..."`, `"backgroundColor": "linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55))"`

---

### `columns` + `column`

`columns` contains ONLY `column` children. Column `width` must match `preset`.

```json
{ "id": "uuid", "type": "columns", "order": 0, "parentId": null,
  "styles": { "gap": "24px", "paddingTop": "0px", "paddingBottom": "0px",
    "paddingLeft": "0px", "paddingRight": "0px", "backgroundColor": "transparent" },
  "content": { "preset": "2-equal" } }
```

`preset`: `"single"` · `"2-equal"` · `"3-equal"` · `"4-equal"` · `"2-1"` (66/34) · `"1-2"` (34/66) · `"sidebar-left"` (25/75) · `"sidebar-right"` (75/25)

```json
{ "id": "uuid", "type": "column", "order": 0, "parentId": "columns-uuid",
  "styles": { "width": "50%", "paddingTop": "0px", "paddingBottom": "0px",
    "paddingLeft": "0px", "paddingRight": "0px",
    "backgroundColor": "transparent", "verticalAlign": "top", "gap": "16px" },
  "content": {} }
```

Card column: add `"borderRadius": "12px"`, `"borderColor": "#E5E7EB"`, `"borderWidth": "1px"`, `"borderStyle": "solid"`, `"boxShadow": "0 4px 24px rgba(0,0,0,0.06)"`, `"padding": "32px"`

---

### `text`

```json
{ "id": "uuid", "type": "text", "order": 0, "parentId": "parent-uuid",
  "styles": { "color": "#1F2937", "fontSize": "16px", "fontWeight": "400",
    "textAlign": "left", "lineHeight": "1.6", "letterSpacing": "0px",
    "paddingTop": "0px", "paddingBottom": "0px", "paddingLeft": "0px", "paddingRight": "0px" },
  "content": { "tag": "p", "html": "Your text here" } }
```

`tag`: `"p"` · `"h1"` · `"h2"` · `"h3"` · `"h4"`

**Typography scale**:
| Role | Size | Weight | Line height |
|---|---|---|---|
| Hero h1 | 64–80px | 700–800 | 1.0–1.1 |
| Section h2 | 40–48px | 700 | 1.2 |
| Card h3 | 22–28px | 600 | 1.3 |
| Body | 16–18px | 400 | 1.6–1.7 |
| Muted/small | 14px | 400 | 1.5 |

---

### `image`

```json
{ "id": "uuid", "type": "image", "order": 0, "parentId": "parent-uuid",
  "styles": { "width": "100%", "maxWidth": "100%", "alignment": "center", "objectFit": "cover",
    "paddingTop": "0px", "paddingBottom": "0px", "paddingLeft": "0px", "paddingRight": "0px",
    "borderRadius": "8px" },
  "content": { "src": "https://images.unsplash.com/photo-{id}?w=800&auto=format&fit=crop",
    "alt": "Describe the image", "linkUrl": null, "linkTarget": "_self" } }
```

Use real Unsplash URLs for all placeholder images. Fixed height: add `"height": "480px"` to styles.

---

### `button`

```json
{ "id": "uuid", "type": "button", "order": 0, "parentId": "parent-uuid",
  "styles": { "backgroundColor": "#111827", "textColor": "#FFFFFF",
    "fontSize": "16px", "fontWeight": "600",
    "paddingTop": "14px", "paddingBottom": "14px", "paddingLeft": "28px", "paddingRight": "28px",
    "borderRadius": "8px", "borderColor": "transparent", "borderWidth": "0px",
    "alignment": "left", "fullWidth": false },
  "content": { "text": "Get Started", "linkUrl": "#", "linkTarget": "_self" } }
```

Outline: `"backgroundColor": "transparent"`, `"borderWidth": "2px"`, `"borderColor": "[primary]"`, `"textColor": "[primary]"`
CTA contrast rule: button must be the highest-contrast element in its section.

---

### `divider`
```json
{ "id": "uuid", "type": "divider", "order": 0, "parentId": "parent-uuid",
  "styles": { "borderColor": "#E5E7EB", "borderWidth": "1px", "borderStyle": "solid",
    "paddingTop": "0px", "paddingBottom": "0px", "paddingLeft": "0px", "paddingRight": "0px",
    "width": "100%" }, "content": {} }
```

---

### `spacer`
```json
{ "id": "uuid", "type": "spacer", "order": 0, "parentId": "parent-uuid",
  "styles": { "height": "40px" }, "content": {} }
```

---

### `icon`
```json
{ "id": "uuid", "type": "icon", "order": 0, "parentId": "parent-uuid",
  "styles": { "size": "32px", "color": "#3B82F6", "alignment": "left",
    "paddingTop": "0px", "paddingBottom": "0px", "paddingLeft": "0px", "paddingRight": "0px",
    "linkUrl": null, "linkTarget": "_self" },
  "content": { "iconName": "Zap" } }
```

Common: `"Check"` · `"Zap"` · `"Shield"` · `"ArrowRight"` · `"Users"` · `"BarChart"` · `"Globe"` · `"Sparkles"` · `"Lock"` · `"Mail"` · `"Star"`

---

### `list`
```json
{ "id": "uuid", "type": "list", "order": 0, "parentId": "parent-uuid",
  "styles": { "fontSize": "16px", "fontWeight": "400", "color": "#1F2937",
    "lineHeight": "1.8", "listStyleType": "disc", "listIndent": "20px", "itemGap": "8px",
    "paddingTop": "0px", "paddingBottom": "0px", "paddingLeft": "0px", "paddingRight": "0px" },
  "content": { "html": "<li>Feature one</li><li>Feature two</li><li>Feature three</li>", "ordered": false } }
```
`content.html` is raw `<li>...</li>` string. `ordered: true` for `<ol>`.

---

### `video`
```json
{ "id": "uuid", "type": "video", "order": 0, "parentId": "parent-uuid",
  "styles": { "maxWidth": "100%", "borderRadius": "8px", "alignment": "center",
    "paddingTop": "0px", "paddingBottom": "0px", "paddingLeft": "0px", "paddingRight": "0px" },
  "content": { "url": "https://www.youtube.com/watch?v=...", "aspectRatio": "16:9" } }
```

---

### `form-embed`
```json
{ "id": "uuid", "type": "form-embed", "order": 0, "parentId": "parent-uuid",
  "styles": { "maxWidth": "520px", "alignment": "center",
    "paddingTop": "0px", "paddingBottom": "0px", "paddingLeft": "0px", "paddingRight": "0px" },
  "content": { "formUuid": "", "formName": null, "formSlug": null } }
```
`formUuid` is set by the user in the builder after creation.

---

### `countdown`
```json
{ "id": "uuid", "type": "countdown", "order": 0, "parentId": "parent-uuid",
  "styles": { "alignment": "center", "gap": "12px",
    "digitFontSize": "48px", "digitFontWeight": "700",
    "digitColor": "#111827", "digitBgColor": "#f3f4f6", "digitBorderRadius": "8px",
    "digitPaddingTop": "16px", "digitPaddingRight": "20px", "digitPaddingBottom": "16px", "digitPaddingLeft": "20px",
    "labelFontSize": "11px", "labelFontWeight": "500", "labelColor": "#6B7280",
    "separatorStyle": "colon", "separatorColor": "#9CA3AF",
    "paddingTop": "0px", "paddingBottom": "0px", "paddingLeft": "0px", "paddingRight": "0px" },
  "content": { "targetDate": "2025-12-31T00:00:00", "timezone": "UTC",
    "showDays": true, "showHours": true, "showMinutes": true, "showSeconds": true,
    "dayLabel": "Days", "hourLabel": "Hours", "minuteLabel": "Minutes", "secondLabel": "Seconds",
    "digitStyle": "rounded", "expiredMessage": "This offer has ended" } }
```

---

### `collapsible` — FAQ accordion item
```json
{ "id": "uuid", "type": "collapsible", "order": 0, "parentId": "parent-uuid",
  "styles": { "backgroundColor": "#F9FAFB", "borderRadius": "8px",
    "headerFontSize": "16px", "headerFontWeight": "500", "headerColor": "#111827",
    "iconColor": "#9CA3AF", "iconSize": "20px",
    "paddingX": "20px", "paddingY": "16px",
    "paddingTop": "0px", "paddingBottom": "8px", "paddingLeft": "0px", "paddingRight": "0px" },
  "content": { "headerText": "Your FAQ question here?", "iconType": "Plus", "iconPosition": "right" } }
```
Body children: add `text` elements with `parentId` pointing to the collapsible's id.

---

### `custom-html`
```json
{ "id": "uuid", "type": "custom-html", "order": 0, "parentId": "parent-uuid",
  "styles": { "paddingTop": "0px", "paddingBottom": "0px", "paddingLeft": "0px", "paddingRight": "0px" },
  "content": { "html": "<p>Custom HTML here</p>" } }
```
HTML is sanitized on save. Use for embeds: Calendly, Loom, Typeform, Google Maps.

---

## Parent-Child Hierarchy

```
null
  └── section
        ├── text / image / button / divider / spacer / icon / list / video / form-embed / countdown / collapsible / custom-html
        └── columns
              └── column
                    ├── (any leaf element)
                    └── section (nested — for complex card layouts)
                          └── (any leaf element)

collapsible
  └── text / image / button
```

`columns` → ONLY `column`. `column` must have `columns` parent. `order` starts at 0, increments per parent.

---

## Responsive Overrides

```json
"responsiveOverrides": {
  "mobile": {
    "element-uuid": { "fontSize": "36px", "paddingLeft": "16px", "paddingRight": "16px" }
  }
}
```

Always add mobile overrides for: hero h1 (reduce 40–50%) · section padding (→ 16–24px) · fixed heights

---

## Design Quality Rules

### Visual Rhythm — Section Background Sequencing
Never stack two sections with the same background color. Plan the sequence before building:

| Pattern | When to use |
|---|---|
| White → Tint → White → Dark | Most SaaS and product pages |
| Dark → White → Tint → Dark | High-drama launches, dark brands |
| White → White → Tint → White | Content-heavy, editorial |

Tint = very light version of brand color (e.g. if brand is `#172A39`, tint = `#f0f4f7`). Never use more than 3 distinct background colors on one page.

### Typography for Impact
- Hero h1: **64–80px**, fontWeight 800, lineHeight 1.0–1.1. Be bold. Timid hero copy loses.
- Section h2: 40–48px, fontWeight 700
- Card h3: 22–28px, fontWeight 600
- Body: 16–18px, lineHeight 1.6–1.7
- Stat numbers: 48–64px, fontWeight 800, brand color or near-black

### Hero Badge (Urgency / Label)
Place a small pill or line of text above the h1 to frame the offer:
```
text (12px, 700, brand color or white on dark, letterSpacing 1.5px)
content: "LIMITED BUNDLE OFFER  ·  ENDS JUNE 9"
```
Use `textAlign: "center"` explicitly. Creates instant context and urgency before the headline lands.

### Stats Bar Pattern
After the hero, a full-width strip of 2–4 key numbers builds credibility fast:
```
section (bg: tint, paddingY: 48px, flexDirection: row, justifyContent: space-around)
  section (column, textAlign: center) × N
    text (h2, 56px, 800, brand color) — the number: "12M+", "140K+", "10 Yrs"
    text (p, 14px, muted) — the label: "WordPress businesses", "sites automated"
```
Always include a stats bar when social proof numbers are available.

### Product Card with Feature List
For product feature cards, use this hierarchy — not just a description paragraph:
```
column (white card, border 1px #e5e7eb, borderRadius 12px, padding 32px, gap 16px)
  image (logo placeholder, imageSize 40, alignment left)   ← logo top-left
  text (11px, 700, brand-specific color, letterSpacing 1.5px) — "PLAN NAME · CONTACTS/VISITORS"
  text (h3, 22px, 700, near-black) — product name
  text (p, 15px, muted) — one-line description
  list (disc → none, items as checkmarks or features, 15px, gap 6px)
```
Feature lists inside cards convert better than paragraph descriptions. Users scan vertically.

### Pricing Card Pattern
The pricing card is the highest-conversion element on any sales page. Always build it:
```
column (dark bg = brand primary, borderRadius 16px, padding 48px, gap 16px)
  text (11px, 700, accent/lime, letterSpacing 1.5px) — "WORDPRESS GROWTH BUNDLE"
  text (h1, 64px, 800, white) — "$2,000"
  text (p, 16px, rgba(white, 0.7)) — "per year · all three products"
  divider (rgba white, 0.15)
  text (p, 15px, rgba(white, 0.8)) — trust sentence: "30-day money-back guarantee"
  button (full-width, high-contrast: white bg + brand text, or lime bg + dark text)
```

### FAQ Section — Always for Sales Pages
Cold traffic has objections. Include 4–6 collapsibles after pricing:
- "Can I use this across multiple sites?"
- "What happens when my year is up?"
- "Is there a refund policy?"
- "Do I need to be a developer?"
Use `collapsible` elements with `iconPosition: "right"`, `bg: #F9FAFB`, `borderRadius: 8px`.

### CTA Repetition
Repeat the primary CTA at least twice: once above the fold in the hero, once at the bottom. For long pages (3+ sections), repeat a third time mid-page after social proof.

---

## Design Recipes

### 1 — Dark SaaS (Signup / Product)
```
globalStyles: headingFont "Syne", bodyFont "DM Sans"
Section 1 (hero):      bg linear-gradient(135deg, #0d1117, #0f1f35), paddingY 120px, center
  badge text (small caps, accent color)
  h1 (72px, 800, white)
  p (20px, muted #8b949e)
  row: primary button (accent) + outline button (white border)
Section 2 (stats):     bg #161b22, paddingY 48px, row spaced
  3× stat number (56px, 800, accent) + label (14px, muted)
Section 3 (features):  bg #0d1117, 3-col cards (bg #161b22, border rgba white 0.08)
  icon + h3 (20px, white) + p (muted)
Section 4 (pricing):   bg accent color, pricing card pattern (see above)
Section 5 (CTA):       bg #0d1117, white h2, accent button
```

### 2 — Minimal Lead Capture (Form Page)
```
globalStyles: headingFont "Fraunces", bodyFont "DM Sans", bg #fafafa
Section 1 (hero):      bg #ffffff, paddingY 100px, columns 1-2
  Left (34%): h1 (56px, 800, near-black), p (muted, 18px), benefit list (disc)
  Right (66%): card (white, shadow 0 8px 40px rgba 0 0 0 0.08, border 1px #e5e7eb, padding 40px)
               form-embed + trust line below (12px, muted)
Section 2 (stats):     bg #f5f5f5, paddingY 40px, 3× stats
Section 3 (trust):     bg #ffffff, 2–3 testimonial cards
```

### 3 — Bundle / Multi-Product Sales (Purchase)
```
globalStyles: headingFont "Plus Jakarta Sans", bodyFont "Plus Jakarta Sans"
Section 1 (hero):      bg brand primary (dark), paddingY 100px, center
  badge (urgency line: "LIMITED OFFER · ENDS [DATE]", accent color)
  h1 (68px, 800, white)
  p (20px, rgba white 0.75)
  countdown element (if deadline)
  button (high-contrast CTA, full-width on mobile)
  small text: guarantee / "No credit card · Cancel anytime"
Section 2 (stats):     bg tint, paddingY 48px, 3× key numbers + labels
Section 3 (products):  bg #ffffff, paddingY 80px
  h2 (center, 44px)
  3-col: product card with feature list pattern (per product)
Section 4 (pricing):   bg #fafafa, paddingY 80px
  h2 (center, 44px)
  columns 1-2: left = what's included list, right = pricing card (dark bg, large price)
Section 5 (FAQ):       bg #ffffff, h2 center, 4–6 collapsibles
Section 6 (CTA):       bg brand primary (dark), h2 (white), button (accent)
  small footer line: guarantee · social proof · built by [team]
```

### 4 — Bold Event / Launch
```
globalStyles: headingFont "Cabinet Grotesk", bodyFont "Cabinet Grotesk"
Section 1:    bg brand color, paddingY 100px, center
  badge (event category, small caps)
  h1 (80px, 800, white) — event name
  countdown (white digits, dark bg digits)
  button (white bg, brand text, large)
Section 2:    bg #ffffff — speaker bios, agenda (2-col)
Section 3:    bg #1a1a1a — venue / date (white text, muted details)
Section 4:    bg brand color — repeat CTA with countdown
```

### 5 — Warm Conversational (Welcome / Thank You)
```
globalStyles: headingFont "Plus Jakarta Sans", bodyFont "Plus Jakarta Sans", bg #fdf6ec
Section 1:    bg #fdf6ec, paddingY 80px, center
  h1 (52px, 700, warm near-black)
  p (muted warm gray, 18px)
  single centered button
Section 2:    bg #ffffff, 3-col: icon + h3 (22px) + short next-step text (left-aligned inside cards)
Section 3:    bg #fdf6ec, social share or secondary CTA (softer)
```



---

## Spacing Reference

| Section type | Padding |
|---|---|
| Hero | `120px 24px` (desktop) → `60px 16px` (mobile) |
| Feature / content | `80px 24px` → `48px 16px` |
| CTA banner | `80px 24px` → `48px 16px` |
| Logo strip / proof bar | `48px 24px` |
| FAQ | `80px 24px` |
| Footer | `60px 24px` |

Column gaps: `24–48px`. Card internal padding: `24–40px`. Element gap inside section: `16–24px` via `rowGap`.

---

## MCP Save Step

After generating design_json, save immediately:

```
Tool: create-page-tool
name:        internal page name (e.g. "Free Trial Landing Page — Dark v1")
description: (optional) internal notes
design_json: the complete design_json object
```

The page is saved as a draft. Confirm: page name, UUID.

Then tell the user:
> "Your page is saved as a draft in SureContact. Open it in the page builder to compile the HTML, then publish with your chosen slug."

---

## Checklist Before Saving

- [ ] Design brief answered — aesthetic direction chosen and applied throughout
- [ ] Page structure matches the conversion goal (not default hero-features-CTA)
- [ ] Every element has a unique UUID v4 `id`
- [ ] Every non-root element has a valid `parentId`
- [ ] `columns` contains ONLY `column` children
- [ ] Column widths sum to 100% per columns container
- [ ] `order` starts at 0, increments within each parent
- [ ] Root elements have `parentId: null`
- [ ] `schemaVersion: 1` set
- [ ] `popovers: []` present
- [ ] `contentOverrides` and `responsiveOverrides` are objects (not arrays)
- [ ] Mobile `responsiveOverrides` set for hero font sizes and wide paddings
- [ ] `list` elements use `content.html` string, not an `items` array
- [ ] Real Unsplash URLs used for placeholder images
- [ ] `create-page-tool` called with name + design_json
