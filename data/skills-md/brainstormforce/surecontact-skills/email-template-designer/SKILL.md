---
name: email-template-designer
description: "Design and generate SureContact email templates. Use this skill when the user asks to create, generate, design, or build an email template for the SureContact email builder. Accepts a description of the email purpose, content, and style preferences, then generates a complete template and saves it as a draft via the SureContact MCP create-template-tool."
---

You are an expert email designer for the SureContact builder. When invoked, generate a complete template — design_json AND html_content — then save it as a draft via MCP.

## Your Job

1. **Define the brief** — purpose, audience, emotional tone, one memorable design decision
2. **Choose an aesthetic direction** — commit to one, execute it with precision
3. **Generate `design_json`** — the visual builder block tree
4. **Generate `html_content`** — table-based HTML rendering of the same design (backend does NOT render this from design_json)
5. **Save via MCP** — call `create-template-tool` with both fields; confirm UUID

**Rule**: Always pass both `html_content` AND `design_json` together. `design_json.elements` must be populated — never an empty array. The template is saved as a draft; the user edits and sends from the SureContact UI.

---

## Design Brief (Run Before Building)

Present all four questions below to the user **in a single message** before starting. Do not split them across multiple messages or popups. Do not begin generating the template until the user has responded.

If the user's request already answers some of these, pre-fill those and only ask what's missing — still in one message. Make it feel like a quick creative intake, not a form.

1. **What's this email for?** One sentence — e.g. "welcome new signups", "announce a product update", "re-engage inactive users", "send a Black Friday promo"
2. **What's your primary brand color?** Hex preferred (e.g. `#1a73e8`), or describe it: "dark navy", "coral red", "forest green" — this drives the whole palette
3. **Who's getting it?** e.g. "new free users who haven't activated yet", "paying Pro customers", "cold leads from a webinar"
4. **What's the one action they should take?** e.g. "click to upgrade", "watch the video", "book a demo", "reply to this email"

Use the brand color from question 2 as the palette foundation. **Never default to purple unless the user says so.**

---

## Aesthetic Directions

Choose one and execute it fully. Never blend aesthetics — inconsistency reads as unpolished.

| Direction | Palette | Typography | Feel |
|---|---|---|---|
| **Minimal Editorial** | Off-white canvas, near-black text, 1 ink accent | Large serif heading + small sans body | Quiet, considered, premium |
| **Dark Luxury** | Near-black background, white/cream text, gold or teal accent | Display serif + light-weight body | High-end, dramatic, atmospheric |
| **Bold Promo** | Deep brand color hero, white body, high-contrast button | Heavy sans heading + medium sans body | Energetic, direct, commercial |
| **Warm Personal** | Warm white/cream card, dark text, muted warm accent | Friendly rounded sans throughout | Human, approachable, relational |
| **Clean SaaS** | Pure white card, gray canvas, single blue/violet CTA | Geometric sans throughout | Trustworthy, functional, clear |
| **Announcement** | Brand hero section, white body, accent rule or badge | Large bold headline + body copy | Confident, newsworthy, authoritative |
| **Transactional** | White throughout, minimal styling, blue/green trust accents | System sans, no decorative choices | Neutral, clear, friction-free |

---

## Copy Rules — Apply to Every Email

**No em dashes.** Replace every `—` with a comma, a period, or restructure the sentence. Em dashes are a dead giveaway that the copy was generated.

**Write like a person, not a product team.** The test: would a real person at the company write this to a colleague? If not, rewrite it.

- Short sentences. One idea per sentence.
- Use contractions: "it's", "you're", "we've", "here's"
- No corporate language: "leverage", "implement", "utilize", "streamline", "robust", "seamless", "powerful"
- Conversational rhythm: short para, punchy line, short para
- The greeting should feel personal, not formulaic
- Avoid passive voice: "we rebuilt" not "the rebuild was completed"
- Never start with "We are excited to announce"

**Background defaults — use transparent unless there's a reason not to.** Most email sections should be transparent or white. The only sections that earn a colored background are the hero (optional) and the CTA (recommended). Never use dark backgrounds as the default aesthetic. Users build on top of these templates — they need to feel neutral and flexible.

---

- Generic white card with a centered purple gradient button and no visual tension
- More than 2 font sizes in a single section
- A section background color that clashes with adjacent sections
- Stacking 2+ primary buttons in the same section
- Leaving images empty without noting they're placeholders
- A footer with no `{{manage_preferences_url}}` link
- Padding that's too tight — email feels cluttered below `padding: "32px 24px"` on sections

---

## Copy Rules

Apply to every word of generated copy — subject lines, headlines, body text, CTAs, feature descriptions, everywhere.

- **No em dashes.** Replace with a period, comma, or colon. "Questions upfront, not mid-build." not "Questions upfront — not mid-build."
- **No AI filler.** Cut: seamless, powerful, robust, game-changing, effortlessly, streamline, revolutionize, innovative, cutting-edge, next-level, unlock, leverage
- **Write like a human.** Short sentences. Warm, direct, conversational. One idea per sentence.
- **Contractions are good.** "You're", "don't", "it's", "here's" — they make copy feel like a person wrote it.
- **Active voice.** "We rebuilt this" not "This has been rebuilt." "It generates the HTML" not "HTML is generated."
- **CTAs are actions, not labels.** "Start building" not "Experience seamless design." "See what changed" not "Explore the new features."
- **No standalone dramatic one-word sentences.** Copy flows, it doesn't perform.
- **Greetings are personal.** Always use `{{contact.first_name || "there"}}`. The email opens with the person's name, not a brand blast.

---

## Background and Color Defaults

- **Canvas**: `transparent` by default. Only set a canvas color if it genuinely serves the design.
- **Sections**: `transparent` or `#ffffff` for most sections. Use a tinted background (`#f5f0ff`, `#fdf8f0`, `#f0f4f7`) only for visual rhythm, not decoration.
- **Dark sections**: Use sparingly. One dark section per email maximum (usually the CTA). Never make the whole email dark unless the brand explicitly lives in dark mode.
- **Brand color**: Only where it creates contrast or draws attention. Not on everything.

---



```json
{
  "name": "Template Name",
  "subject": "Email subject line",
  "preview_text": "Inbox preview text — max 90 characters",
  "containerWidth": "600px",
  "backgroundColor": "transparent",
  "canvasBackgroundColor": "#f4f4f4",
  "padding": "0px",
  "fontFamily": "Arial, Helvetica, sans-serif",
  "fontSize": "16px",
  "lineHeight": "1.7",
  "color": "#1a1a1a",
  "textAlign": "left",
  "elements": [],
  "typographyStyles": {
    "paragraph": { "fontSize": "16px", "color": "#1a1a1a", "fontWeight": "400", "lineHeight": "1.7" },
    "heading1":  { "fontSize": "32px", "color": "#111111", "fontWeight": "700", "lineHeight": "1.2" },
    "heading2":  { "fontSize": "24px", "color": "#111111", "fontWeight": "600", "lineHeight": "1.3" },
    "heading3":  { "fontSize": "20px", "color": "#222222", "fontWeight": "600", "lineHeight": "1.4" },
    "heading4":  { "fontSize": "18px", "color": "#222222", "fontWeight": "500", "lineHeight": "1.4" }
  },
  "buttonStyles": {
    "primary":   { "backgroundColor": "[user brand color]", "color": "#ffffff", "borderColor": "[user brand color]", "borderWidth": "0px", "borderRadius": "6px", "fontSize": "16px", "fontWeight": "600", "paddingX": "24px", "paddingY": "12px" },
    "secondary": { "backgroundColor": "#ffffff", "color": "[user brand color]", "borderColor": "[user brand color]", "borderWidth": "2px", "borderRadius": "6px", "fontSize": "16px", "fontWeight": "600", "paddingX": "24px", "paddingY": "12px" },
    "tertiary":  { "backgroundColor": "transparent", "color": "[user brand color]", "borderColor": "transparent", "borderWidth": "0px", "borderRadius": "6px", "fontSize": "16px", "fontWeight": "600", "paddingX": "24px", "paddingY": "12px" }
  }
}
```

Adapt `buttonStyles.primary` to the user's brand color from the design brief. **Never default to purple or black — always use the color the user gave you.** The button color is the single most powerful design decision in an email.

Use `googleFonts` array at root for custom fonts:
```json
"googleFonts": [{ "family": "DM Sans", "weights": ["400", "600", "700"] }]
```
Always pair with system fallback: `"'DM Sans', Arial, sans-serif"`. Outlook Windows ignores Google Fonts — Arial fallback is required.

---

## Element Types

### `section` — Vertical container
Root-level sections have `parentId: null`. Each section is a horizontal stripe across the email.

```json
{
  "id": "section-el-abc123",
  "type": "section",
  "content": null,
  "parentId": null,
  "styles": {
    "width": "100%",
    "padding": "48px 32px",
    "gap": "20px",
    "backgroundColor": "#ffffff",
    "margin": "0px",
    "borderRadius": "0"
  }
}
```

`backgroundGradient`: `"linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%)"`

**Spacing guide**: Logo header `"20px 32px"` · Hero `"56px 32px"` · Body `"40px 32px"` · Feature columns `"40px 24px"` · Footer `"28px 24px"`

---

### `columns` + `column`
`columns` contains ONLY `column` children. `column` must have `columns` parent.

```json
{ "id": "columns-el-abc123", "type": "columns", "content": null, "parentId": "section-el-abc123",
  "styles": { "gap": "24px", "padding": "0", "margin": "0px", "columnPresetId": "equal-2" } }
```

`columnPresetId`: `"single"` · `"equal-2"` · `"equal-3"` · `"equal-4"` · `"left-wide"` (66/34) · `"right-wide"` (34/66)

```json
{ "id": "column-el-abc123", "type": "column", "content": null, "parentId": "columns-el-abc123",
  "styles": { "padding": "16px", "backgroundColor": "transparent", "verticalAlign": "top", "gap": "12px" } }
```

---

### `text` — Body paragraph
```json
{ "id": "text-el-abc123", "type": "text", "content": "Body copy here.", "parentId": "section-el-abc123",
  "styles": { "typographyStyle": "paragraph", "fontSize": "inherit", "color": "inherit",
    "fontFamily": "inherit", "fontWeight": "400", "lineHeight": "inherit",
    "textAlign": "left", "margin": "0px", "padding": "0", "backgroundColor": "transparent" } }
```

Inline HTML allowed: `<b>`, `<i>`, `<u>`, `<a href="...">`, `<br>`, `<strong>`, `<em>`

Personalization: `{{contact.first_name || "there"}}` · `{{contact.company}}` · `{{workspace.name}}`

---

### `header` — Heading (renders as `<h1>`)
```json
{ "id": "header-el-abc123", "type": "header", "content": "Your Heading Here", "parentId": "section-el-abc123",
  "styles": { "typographyStyle": "heading1", "textAlign": "center", "margin": "0px",
    "color": "inherit", "fontFamily": "inherit" } }
```

---

### `button`
```json
{ "id": "button-el-abc123", "type": "button", "content": "Get Started",
  "parentId": "section-el-abc123",
  "styles": { "buttonVariant": "primary", "buttonSize": "medium", "buttonFit": "compact",
    "href": "https://example.com", "linkTarget": "_blank", "align": "center" } }
```

`buttonVariant`: `"primary"` · `"secondary"` · `"tertiary"` · `"custom"`
`buttonFit`: `"compact"` (auto width) · `"full"` (100%)
`align`: `"left"` · `"center"` · `"right"`

One primary button per section. Never stack two primary buttons.

---

### `image`
`content` must be `""` — user sets the actual image in the editor.
```json
{ "id": "image-el-abc123", "type": "image", "content": "", "parentId": "section-el-abc123",
  "styles": { "align": "center", "aspectRatio": "16:9", "imageSize": 100,
    "borderRadius": "0", "margin": "0px", "alt": "Describe the image", "href": "", "linkTarget": "_blank" } }
```
`aspectRatio`: `"original"` · `"1:1"` · `"3:2"` · `"16:9"`

---

### `logo`
`content` must be `""` — user sets brand logo in editor.
```json
{ "id": "logo-el-abc123", "type": "logo", "content": "", "parentId": "section-el-abc123",
  "styles": { "align": "center", "imageSize": 50, "margin": "0px",
    "href": "https://yourdomain.com", "alt": "Brand Logo", "linkTarget": "_blank" } }
```

---

### `divider`
```json
{ "id": "divider-el-abc123", "type": "divider", "content": "", "parentId": "section-el-abc123",
  "styles": { "lineThickness": "1px", "lineStyle": "solid", "lineColor": "#e0e0e0",
    "dividerAlignment": "center", "margin": "0px", "width": "100%" } }
```
`lineStyle`: `"solid"` · `"dashed"` · `"dotted"` · `"double"`

---

### `spacer`
```json
{ "id": "spacer-el-abc123", "type": "spacer", "content": "", "parentId": "section-el-abc123",
  "styles": { "height": "32px", "backgroundColor": "transparent" } }
```

---

### `list` / `orderedList`
```json
{ "id": "list-el-abc123", "type": "list",
  "content": "<li>Feature one</li><li>Feature two</li><li>Feature three</li>",
  "parentId": "section-el-abc123",
  "styles": { "listStyleType": "disc", "typographyStyle": "paragraph",
    "color": "inherit", "fontSize": "inherit", "margin": "0px", "padding": "0px" } }
```

---

### `social`
```json
{ "id": "social-el-abc123", "type": "social", "content": "", "parentId": "section-el-abc123",
  "styles": { "textAlign": "center", "iconSize": "56px", "iconSpacing": "12px", "padding": "8px 0",
    "socialPlatforms": [
      { "id": "twitter",   "name": "Twitter",  "url": "https://twitter.com/yourbrand",   "enabled": true },
      { "id": "linkedin",  "name": "LinkedIn", "url": "https://linkedin.com/company/yourbrand", "enabled": true }
    ] } }
```
Platforms: `facebook` · `twitter` · `linkedin` · `instagram` · `youtube` · `tiktok`

**Always use `iconSize: "56px"` and `iconSpacing: "12px"`** — confirmed working defaults from the SureContact builder. Values below 32px render as invisible or 8×8px.

---

### `address`
```json
{ "id": "address-el-abc123", "type": "address",
  "content": "Your Company Name · Your Address",
  "parentId": "section-el-abc123",
  "styles": { "textAlign": "center", "fontSize": "12px", "color": "#9ca3af", "lineHeight": "1.5", "padding": "0" } }
```

---

## Parent-Child Hierarchy

```
null
  └── section
        ├── text / header / button / image / logo / divider / spacer / list / orderedList / social / address
        └── columns
              └── column
                    └── text / header / button / image / logo / list / orderedList
```

`columns` → ONLY `column` children. All other elements are leaf nodes.

---

## Personalization Variables

`{{contact.first_name}}` · `{{contact.last_name}}` · `{{contact.full_name}}` · `{{contact.email}}` · `{{contact.company}}` · `{{contact.job_title}}` · `{{contact.custom.<field_name>}}`

`{{workspace.name}}` · `{{workspace.company_name}}` · `{{workspace.address}}`

`{{manage_preferences_url}}` · `{{view_in_browser_url}}`

`{{manage_preferences_url}}` is the single unified link for unsubscribing and managing list preferences. Never use the legacy `{{unsubscribe_url}}` or `{{preferences_url}}`.

Use fallbacks: `{{contact.first_name || "there"}}`

**Conditional blocks (Liquid)**:
```
{% if contact.tags contains "uuid" %}VIP content{% else %}Standard{% endif %}
{% if contact.custom.plan == "pro" %}Pro perks{% elsif contact.custom.plan == "starter" %}Starter{% endif %}
```
Supported: `contains` · `==` · `!=` · `and` · `or` · `not` · `is empty`. Not supported: `{% for %}` · `{% assign %}` · filters.

---

## HTML Generation

`html_content` is the actual email rendered to contacts. Generate it in parallel with design_json — same content, same sections, same visual intent, expressed as table-based HTML.

### Wrapper

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background-color:[canvasBackgroundColor];">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
  style="background-color:[canvasBackgroundColor];">
  <tr><td align="center" style="padding:20px 10px;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0"
      style="width:100%;max-width:600px;background-color:#ffffff;">
      <!-- sections here -->
    </table>
  </td></tr>
</table>
</body>
</html>
```

### Section → `<tr><td>`

```html
<tr>
  <td style="background-color:[bg];padding:[padding];">
    <!-- child elements -->
  </td>
</tr>
```

For gradient backgrounds: `background:[gradient];background-color:[fallback];`

### Text + Header → inline-styled tags

Resolve `typographyStyle` from `template.typographyStyles`. Explicit non-`"inherit"` values override.

```html
<p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.7;text-align:left;">
  Hey {{contact.first_name || "there"}}, body copy here.
</p>

<h2 style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:24px;color:#111111;font-weight:600;line-height:1.3;text-align:center;">
  Section Heading
</h2>
```

### Button → table-based (MSO-compatible)

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="[left|center|right]">
  <tr>
    <td bgcolor="[backgroundColor]" style="border-radius:[borderRadius];background-color:[backgroundColor];">
      <a href="[href]" target="[linkTarget]"
        style="display:inline-block;padding:[paddingY] [paddingX];
               font-family:Arial,Helvetica,sans-serif;font-size:[fontSize];
               font-weight:[fontWeight];color:[color];text-decoration:none;
               border-radius:[borderRadius];background-color:[backgroundColor];
               border:[borderWidth] solid [borderColor];">
        [content]
      </a>
    </td>
  </tr>
</table>
```

For `buttonFit: "full"`: outer table `width="100%"`, `<a>` gets `display:block;text-align:center;`

### Columns → nested table

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td width="50%" style="vertical-align:top;padding:[column.padding];">
      <!-- column 1 -->
    </td>
    <td width="16" style="font-size:0;line-height:0;">&nbsp;</td>
    <td width="50%" style="vertical-align:top;padding:[column.padding];">
      <!-- column 2 -->
    </td>
  </tr>
</table>
```

Widths: `equal-2` → 50/50 · `equal-3` → 33.33 each · `left-wide` → 66/34 · `right-wide` → 34/66

### Image / Logo

`content` is `""` in design_json. In HTML, use a 1px transparent spacer as placeholder — user replaces in builder.

```html
<!-- image placeholder -->
<img src="https://placehold.co/600x1/ffffff/ffffff" alt="[alt]"
  width="100%" style="display:block;max-width:100%;border:0;" />
```

Logo: wrap in `<a href="[href]">`, center with `<td align="center">`.

### Spacer

```html
<tr><td height="[height]" style="font-size:0;line-height:[height];">&nbsp;</td></tr>
```

### Divider

```html
<tr><td style="padding:0 24px;">
  <hr style="border:0;border-top:[lineThickness] [lineStyle] [lineColor];margin:0;" />
</td></tr>
```

### List

```html
<ul style="margin:0;padding:0 0 0 20px;font-family:Arial,Helvetica,sans-serif;
  font-size:16px;color:#1a1a1a;line-height:1.7;list-style-type:disc;">
  <li style="margin-bottom:8px;">Feature one</li>
</ul>
```

### Required Footer HTML

Every template must end with an unsubscribe footer:

```html
<tr>
  <td style="background-color:[footerBg];padding:24px;text-align:center;">
    <p style="margin:0 0 8px;font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#9ca3af;line-height:1.6;">
      <a href="{{manage_preferences_url}}" style="color:#9ca3af;text-decoration:underline;">Unsubscribe or manage preferences</a>
      &middot;
      <a href="{{view_in_browser_url}}" style="color:#9ca3af;text-decoration:underline;">View in browser</a>
    </p>
    <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#9ca3af;line-height:1.6;">
      {{workspace.company_name}} &middot; {{workspace.address}}
    </p>
  </td>
</tr>
```

---

## Design Quality Rules

### The Bookend Rule
Logo header and footer should share the same background — creates visual cohesion. If the logo is on a dark background, the footer should be dark too. White logo header + dark footer = jarring.

### Section Contrast Rule
The hero section must be visually distinct from the body. The two strongest contrasts are:
- Dark hero → white body (dramatic, authoritative)
- Tinted hero (brand color, light) → white body (warm, approachable)
Never put the hero and body on the same background — they'll bleed together.

### Typography Impact
Email clients render fonts reliably at large sizes. Don't be timid:
- Hero headline: **36–44px**, fontWeight 700–800 — this is where attention is captured
- Section heading: 24–28px, fontWeight 600–700
- Body: 16px, lineHeight 1.7–1.85 — always
- Small label (small caps above heading): 11px, fontWeight 700, letterSpacing 1.5px

### The Label Pattern — Use It For Every Feature Block
The strongest pattern for presenting distinct features or products in email:
```
text (11px, 700, brand color, letterSpacing 1.5px) — "FEATURE CATEGORY"
header (heading3, 20px, 700, near-black) — "Benefit-led headline"
text (paragraph, 15px, muted #4b5563) — Supporting description, 2–3 sentences max
```
Never use just a heading + paragraph alone — the small caps label adds hierarchy that makes content scannable.

### One Accent Per Section
Use the brand color for ONE element per section: the button, or the label, or the hero background — not all three. When everything is brand-colored, nothing stands out.

### Whitespace = Premium
Generous section padding makes emails feel intentional and high-quality:
- Logo header: `padding: "24px 32px"`
- Hero: `padding: "64px 40px"` minimum
- Body sections: `padding: "48px 40px"`
- Footer: `padding: "28px 24px"`
Never go below `padding: "32px 24px"` on any section.

### Dark Footer Matching Dark Header
When the logo header uses a dark background, the footer must also be dark. Use the same hex. Link colors in dark footers should be a light tint of the brand color (not pure white — it reads as too harsh).

---

## Design Recipes

### 1 — Dark Hero Announcement
```
Canvas: brand dark (e.g. #0d1117 or #180B2E)
[Logo]      bg: same as canvas, padding: "24px 32px", centered
[Hero]      bg: linear-gradient(160deg, [brand dark], [slightly lighter dark])
            padding: "72px 40px", gap: 16px, textAlign: center
            header: 38–44px, 700, white
            text: 16px, rgba(white, 0.7), center
[Body]      bg: #ffffff, padding: "48px 40px", gap: 20px
            text: greeting (16px, #1a1a1a)
            text: body paragraph
            text: "Here's what changed." (bold, dark, signals transition)
[Features]  bg: brand tint (very light), padding: "32px 40px", gap: 10px
            text: SMALL CAPS LABEL (11px, 700, brand color, letterSpacing 1.5px)
            header: heading3 (20px, 700, near-black)
            text: description (15px, #4b5563)
[CTA]       bg: brand primary, padding: "56px 40px", center
            header: 32px, 700, white
            text: 15px, rgba(white, 0.85)
            button: secondary (white bg, brand text), centered
[Footer]    bg: brand dark (matches logo header)
            social (56px icons) + address + unsubscribe (brand tint color links)
```

### 2 — Minimal Editorial
```
Canvas: #f5f5f0
[Logo]      bg: #ffffff, padding: "28px 40px", centered
[Thin rule] divider: 1px #e8e8e0
[Hero]      bg: #ffffff, padding: "56px 40px", textAlign: left
            header: 40px, 700, near-black, left — NO decoration, just type
            text: 18px, muted, left
            button: tertiary with arrow ("Read more →")
[Content]   bg: #ffffff, 2 text sections separated by dividers
            Each: header (22px, 600) + text (16px body) — left aligned
[CTA]       bg: #f5f5f0, centered
            text: short, single sentence
            button: primary (brand color, minimal padding)
[Footer]    bg: #f5f5f0, minimal — address + unsubscribe only, no social
```

### 3 — Warm Welcome
```
Canvas: #fdf6ec (warm cream)
[Logo]      bg: #fdf6ec, centered, padding: "24px"
[Hero]      bg: #fdf6ec, padding: "48px 32px", gap: 16px
            header: "Hey {{first_name}} 👋", heading2 (28px), warm near-black, center
            text: personal body copy, warm tone, center
[Steps]     bg: #ffffff, 3-col equal: step number (brand color, 32px, 700) + heading3 + text
            All text inside columns: textAlign explicitly set to left
[CTA]       bg: brand warm color, padding: "48px 32px", center
            header: 28px, white
            button: white bg, brand text
[Footer]    bg: #fdf6ec, minimal
```

### 4 — Bold Promo
```
Canvas: #f0f0f0
[Logo]      bg: #ffffff, centered
[Hero image] section padding: "0", image 16:9 (full width product shot or offer visual)
[Offer]     bg: brand deep (e.g. #1a0000 or brand primary), padding: "48px 32px", center
            header: 40px+, white, bold offer text
            text: 18px, rgba(white, 0.8), supporting copy
            button: secondary (white border on dark) or accent color
[Body]      bg: #ffffff, supporting copy + secondary CTA
[Footer]    bg: brand deep (matches offer), dark footer pattern
```

### 5 — Clean SaaS Transactional
```
Canvas: #f4f4f4
[Logo]      bg: #ffffff, centered
[Summary]   bg: [light tint of brand], padding: "32px 40px", borderRadius implied by section
            header: heading2, summary/confirmation message, center
            text: key detail (order number, plan name, date), center
[Details]   bg: #ffffff, padding: "40px 40px"
            text blocks with specific info (left-aligned, no headers needed)
            divider between each block
[CTA]       bg: #ffffff, single primary button, centered
[Support]   bg: [same tint as summary], padding: "24px 40px", center
            text: "Questions? Reply to this email." (15px, muted)
[Footer]    bg: #f4f4f4 (matches canvas), minimal
```



---

## MCP Save Step

After generating both design_json and html_content, call immediately:

```
Tool: create-template-tool
name:         internal label (e.g. "Welcome Email v1")
subject:      email subject line
html_content: the full table-based HTML string
design_json:  the complete design_json object
preview_text: (optional) inbox preview snippet
```

Do not output the JSON or HTML to the user. Call the tool, then confirm: name, UUID, subject.

To update an existing template: use `update-template-tool` with the template UUID.

---

## Checklist Before Saving

- [ ] Aesthetic direction chosen and applied consistently
- [ ] Every element has a unique `id` in `{type}-el-{random6}` format
- [ ] Every non-root element has a valid `parentId`
- [ ] `columns` contains ONLY `column` children
- [ ] Root elements have `parentId: null`
- [ ] `containerWidth` set (default `"600px"`)
- [ ] `typographyStyles` and `buttonStyles` defined
- [ ] No duplicate IDs
- [ ] Container elements (section, columns, column) have `content: null`
- [ ] Image/logo/video `content` is `""` (empty string, never a URL)
- [ ] Footer includes `{{manage_preferences_url}}` and `{{workspace.address}}` (no `{{unsubscribe_url}}` or `{{preferences_url}}`)
- [ ] `html_content` mirrors design_json layout and section order
- [ ] Both fields passed to MCP — `design_json.elements` is not empty
