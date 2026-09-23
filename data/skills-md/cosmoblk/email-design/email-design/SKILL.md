---
name: email-design
description: >
  Design distinctive, on-brand emails — newsletters, campaigns, welcome series,
  promo, post-purchase, win-back, transactional, announcements. Use when the
  user wants to draft, write, compose, design, redesign, critique, polish, or
  improve an email; or send a campaign / blast / broadcast through any ESP
  (Nitrosend, Klaviyo, Mailchimp, ActiveCampaign, etc.). Produces a structured
  design brief and translates it into the sending tool's section format. Bakes
  in anti-slop principles: own a colour, restrained palettes, real imagery
  with sourced or prompted image slots, distinctive voice, no category-reflex
  aesthetics, no orphan whitespace, single column ≤600px, mobile-first, real
  footers (verified mission only, plus socials + address + unsubscribe). Asks at most three
  questions to fill brand gaps; otherwise infers from connected ESP account
  settings or a project brand file. Self-contained — no other skills required.
  Skip for pure strategy, deliverability, copy-only, or platform-selection
  questions.
license: MIT
user-invocable: true
metadata:
  author: george-hartley
  version: "1.0"
---

# Email Design Skill

Distinctive, on-brand emails. Produces a structured brief, then hands it to the connected sending tool. Self-contained.

## When to use

Triggered for:

- "draft / write / compose / design / build an email" (newsletter, campaign, blast, broadcast, announcement, welcome, win-back, post-purchase, abandoned cart, promo, transactional)
- "make this email less generic / less plain / more on brand"
- "redesign / critique / polish this email"
- "send a campaign through Nitrosend / Klaviyo / etc."

Skip for:

- Strategy-only ("what frequency should I send at?")
- Deliverability-only ("why am I in spam?")
- Platform selection ("Klaviyo vs Mailchimp?")
- Copywriting in isolation, no design

## The flow (five steps)

1. **Context check** — pull brand state from the connected ESP and project files. No questions yet.
2. **Ask up to three questions** — only the highest-leverage gaps. Bundle into one message.
3. **Pick an archetype, write the brief.** Commit before composing.
4. **Resolve image slots** — fetch from brand site, brand assets, or prompt the user.
5. **Translate the brief into the sending tool's format** and run a dry-run preview before approval.

---

## Step 1 — Context check (silent)

Pull what is already known. **Do not ask the user yet.**

If Nitrosend MCP tools are available (`nitro_*`):

- Read the `nitro://account` resource for brand fields (company name, brand colour, logo, fonts, physical address, voice document if present).
- Call `nitro_get_status` for onboarding state and any obvious gaps.
- Call `nitro_query({ entity: "templates", limit: 3 })` to see prior design language. Look at the actual sections, colours, typography, and tone.

If the connected ESP is something else, look for the equivalent — most ESPs expose a brand or settings endpoint. If the ESP is unknown, fall back to project files: `BRAND.md`, `email-brand.md`, `PRODUCT.md`, or a top-level `README.md` for tone clues.

Build a brand profile in your head with these fields, marking each as `known`, `inferable`, or `missing`:

- Company name, from-name, from-email, mission/tagline
- Primary brand colour (hex), secondary if any
- Logo URL
- Voice descriptors (e.g. founder-personal, editorial, cheeky, technical, premium-restrained)
- Footer essentials: physical address, social handles, unsubscribe handler

If three or more fields are `missing`, you can ask. Otherwise default to inferred values and note them in the brief.

---

## Step 2 — Up to three questions (only if needed)

Hard cap: **three questions, in one message, as a numbered list**. If more fields are missing, fill with sensible defaults and note them in the brief — do not interrogate.

Priority order — pick the top three that are missing and matter for *this specific email*:

1. **Email purpose** — what does this specific email need to do? (Drive a click? Tell a story? Confirm an action? Re-engage a lapsed user? Tease a launch?) Almost always worth asking on first email of a session.
2. **Tone register** — editorial, bold-mono, minimal-lux, founder-letter, punk/character, or lookbook? Ask only if voice is unclear from prior templates.
3. **Primary brand colour** — hex preferred. Ask only if missing AND no logo to extract from.
4. **Mission line** — one sentence on why the company exists (not what it sells). Ask only if footer-critical and absent.
5. **Socials + physical address** — handles + one mailing address for footer / CAN-SPAM. Ask only if footer would otherwise be incomplete.

If the user has already answered these earlier in the session, do not re-ask.

---

## Step 3 — Pick an archetype, then write the brief

Anti-slop wins. Commit to an archetype before drafting. The most common failure mode is defaulting to "minimal-lux" because it feels safe — it is the right answer maybe 30% of the time. For the rest, pick deliberately.

### Archetypes

| Archetype | When | Hallmarks | Reference brands |
|---|---|---|---|
| **Editorial** | Newsletters, brand stories, long-form | Serif heads, full-bleed photo, generous leading, single column, voice-rich | Patagonia, Tracksmith, Lucy Folk |
| **Bold mono** | Promo, launches, statements | One saturated colour drenches the surface, big punchy type, minimal copy | Absolut, Liquid Death, Fly By Jing |
| **Minimal lux** | Premium, transactional, restraint as positioning | Tinted neutrals, narrow width 472–520px, one accent, lots of breath, never discount-led | Stripe, Aesop, Apple, MoMA |
| **Founder letter** | Welcome, win-back, milestones, reply-driver | Plain-text feel, first-person, short paragraphs, signed off, no template chrome | Ugmonk, Superhuman, Tracksmith CEO |
| **Punk / character** | Brand voice carriers, retention | Heavy personality, mascot or character, irreverent copy, custom imagery | Frank Body, Duolingo, Liquor Loot, Chubbies |
| **Lookbook** | Product, fashion, food, paint, anything where the product *is* the design | Editorial photo > copy, gallery layout, full-bleed hero | Dior, Clare Paint, Starbucks seasonal |

### Shared visual laws

Apply to every archetype. Implementation should match the aesthetic — bold needs committed; minimal needs precision.

#### Colour

- Pick a strategy *before* picking colours:
  - **Restrained** — tinted neutrals + one accent ≤10% of the surface. Default for transactional and minimal-lux only.
  - **Committed** — one saturated colour carries 30–60% of the surface. Default for brand-identity emails.
  - **Drenched** — the surface IS the colour. For heroes and statement emails.
- Never pure `#000` or `#fff`. Tint every neutral toward the brand hue.
- High chroma at extreme lightness looks garish; pull saturation back as you approach black or white.
- **Category-reflex check.** If someone could guess the palette from the category alone — fintech → navy + gold, wellness → white + sage, AI → black + neon, ecommerce → millennial pink + cream — rework it. Training-data reflexes make emails forgettable.

#### Typography

- One typeface family per email. Add a second only with a clear functional reason.
- Body 14–16px. Headline 22–34px. Hierarchy ratio ≥1.25 between steps.
- Cap line length 50–65 characters.
- No gradient text. No `background-clip: text`. Emphasis through weight or size, not effects.

#### Layout

- Single column. Width 472–600px. Wider feels desktopy and breaks on mobile.
- Vary spacing for rhythm. Same padding everywhere reads as wireframe.
- Cards are the lazy answer. Use only when truly the best affordance. Nested cards are always wrong.
- Touch targets ≥44×44px.

#### Whitespace (this is where most AI-drafted emails fail)

The default LLM behaviour is to over-pad — every section gets generous top *and* bottom padding, plus standalone spacer rows. The result is a moonscape. Counteract:

- **No orphan spacers.** Two `spacer` sections in a row, ever, is wrong. Collapse.
- **Asymmetric padding.** Most sections: `padding_top: 0, padding_bottom: 32`. Let the next section's top padding (or its lack) own the rhythm.
- **Hero hugs.** Hero image sits flush to header (≤8px gap), generous space *below* the hero, not both sides.
- **End rule.** Final content section before footer: `padding_bottom: 32–48px`, never more. Footer has its own top padding.
- **Never:** two consecutive empty paragraphs, double `<br>` between blocks, margin AND padding on the same side, an empty `text` section used as a spacer.

This applies regardless of platform whitespace-trimming passes — belt and braces.

#### Imagery

- Real photography or commissioned illustration only. No stock, no AI slop, no flat geometric shapes as decoration.
- Hero must serve a purpose: product, person, place, or moment. Decoration is not enough.
- Each image ≤200KB; total payload ≤800KB.
- Alt text on every image. Treat as fallback for the ~33% who block images.
- Dark mode: transparent PNGs for logos and icons; off-white (not pure white) backgrounds.

#### Copy

- Inverted pyramid. Lead with the answer.
- Short paragraphs. Every word earns its place.
- No restated headings. No intro paragraphs that repeat the subject.
- No em dashes (—) or en dashes (–) in body. Use commas, colons, semicolons, periods, parentheses. No `--`.
- One CTA above the fold. A second CTA at the bottom is fine. More than two is dilution.
- Subject ≤45 chars. Preheader ≤90 chars. Both must add information; never restate the subject.

### The brief (structured)

Write the brief as JSON before composing sections. This is what feeds the sending tool. Treat it as the contract.

```json
{
  "name": "Campaign or template name",
  "subject": "subject line ≤45 chars",
  "preheader": "preheader ≤90 chars adding new info",
  "archetype": "editorial | bold-mono | minimal-lux | founder-letter | punk-character | lookbook",
  "color_strategy": "restrained | committed | drenched",
  "primary_color": "#hex",
  "secondary_color": "#hex or null",
  "voice_descriptors": ["e.g. founder-personal", "wry", "concrete"],
  "structure": [
    { "kind": "header",         "logo": true, "padding": "compact" },
    { "kind": "hero",           "image_slot": "<slot-id>" },
    { "kind": "headline",       "content": "..." },
    { "kind": "body",           "content": "..." },
    { "kind": "cta",            "label": "...", "url": "..." },
    { "kind": "secondary_body", "content": "..." },
    { "kind": "footer" }
  ],
  "image_slots": [
    {
      "slot_id": "hero",
      "purpose": "what it must convey",
      "candidate_url": "<url-from-brand-site or null>",
      "user_prompt": "<text to show user if no candidate>"
    }
  ],
  "footer": {
    "mission_line": "exact verified copy from brand fields or brand site, or null — never invent",
    "socials": [{ "name": "instagram", "url": "..." }],
    "physical_address": "one line",
    "unsubscribe": "{{unsubscribe_url}}"
  },
  "anti_slop_checks": ["no category-reflex palette", "real imagery", "distinctive voice"]
}
```

---

## Step 4 — Resolve image slots

Each `image_slot` must end with a real candidate URL or an explicit prompt to the user. Sources, in priority order:

1. **Already-uploaded brand assets.** If Nitrosend is connected: `nitro_query({ entity: "media" })`. Use what's there before fetching anything new.
2. **Brand site.** Fetch `https://<brand-domain>/` with WebFetch and look for:
   - `<meta property="og:image">`
   - hero image on the homepage (look for `<section class="hero"> img`, `<header> img`, `[data-hero] img`, banner-y filenames)
   - `/press`, `/about`, or `/blog` page imagery for portraits and lifestyle
   - Prefer images ≥1200px on the long edge.
3. **Brand social profiles.** Instagram or X profile images for portraits and lifestyle moments.
4. **Prompt the user — once.** Concrete description, options included: *"For the hero I'm picturing [X]. Got an image for that, or want me to leave a placeholder so you can drop one in via the media uploader?"*

Never fabricate or AI-generate a stock-style image. A clearly-marked placeholder is better than visual slop.

If you uploaded a new image and the brand uses Nitrosend: `nitro_ingest_image({ url: "...", purpose: "hero" })`.

---

## Step 5 — Translate the brief and hand off

Map the brief's `structure` array to the sending tool's section types. For Nitrosend `nitro_compose_campaign`:

| Brief kind | Nitrosend section | Notes |
|---|---|---|
| header | omit if logo lives in `theme.logo_url`; otherwise `image` | Logo height 32–48px |
| hero | `image` | Full-width, no side padding, set `link_url` only if it's clickable |
| headline | `text` with `<h1>` or `<h2>` markup | Don't add a separate spacer above; let the next section's top padding handle rhythm |
| body | `text` | Short paragraphs |
| cta | `button` | Single CTA, full-width on mobile |
| secondary_body | `text` | Optional |
| divider | `divider` | Once per email max |
| footer | `footer` | Auto-rendered if account footer is configured; otherwise build explicitly |

### Whitespace overrides on the call

Override the platform's default padding when composing. Do this even if the platform has a whitespace-trimming pass.

```json
{
  "type": "image",
  "props": {
    "src": "...",
    "alt": "...",
    "padding_top": 0,
    "padding_bottom": 24
  }
}
```

Default rule per section: `padding_top: 0, padding_bottom: 32`. Override only with reason.

### Footer — the part most AI emails get wrong

A great footer, in this order:

1. **Mission line.** One sentence. *Why* the company exists, not what it sells. ("Made for runners. Made in Boston." beats "Premium athletic apparel since 2014.") **Do not guess or invent this.** Pull verbatim from one of: the connected ESP's brand fields (Nitrosend: `company_description` on the brand, also visible in the Brand settings), or the brand's homepage / about page (hero subhead, footer tagline, "we believe…" copy). If neither yields an exact, verified line, **omit the mission line entirely** — a missing mission is better than a fabricated one.
2. **Social icons.** 3–5 max. Real handles, real URLs. 24–32px icons.
3. **Physical address.** Required for CAN-SPAM. Single line.
4. **Unsubscribe link.** Visible, not microscopic. The word "unsubscribe", not a buried "preferences" euphemism. Required for CAN-SPAM and Gmail/Yahoo bulk-sender rules.
5. **Optional:** tagline, contact email, "you're getting this because…" reason.

Visual: smaller type (12–13px), tinted neutral text at 60–70% of body contrast, generous internal padding, no extra spacer above.

### The handoff

Always run a dry-run first and always show the preview URL before the user approves a real send. Ask if they want a test email.

```
nitro_compose_campaign({
  name: brief.name,
  subject: brief.subject,
  preheader: brief.preheader,
  sections: <translated from brief.structure with explicit padding>,
  theme: {
    brand_color: brief.primary_color,
    bg_color: ...,
    text_color: ...,
    font_body: ...,
    font_heading: ...,
    logo_url: ...
  },
  audience: { audience_type: "lists", contact_list_ids: [...] },
  dry_run: true
})
```

Then surface the preview URL from the response. Only proceed to a real send after the user confirms.

### Offer a test send

After the dry-run preview, before any real send, ask:

> *"Want me to send you a test email first? I can send to [from_email from account] or another address — let me know."*

Default the recipient to the account's `from_email` or the saved test recipients, but accept any address the user names. If they say yes, send via the platform's test endpoint and surface the result.

For Nitrosend:

```
nitro_send_test_message({
  template_id: <id from compose response>,
  email: "<recipient>"
})
```

For other ESPs, use the equivalent (`POST /v1/my/templates/{id}/send_test` on the Nitrosend REST API; analogous endpoints elsewhere). After the test lands, ask if any final tweaks are needed before the real send.

---

## Pre-handoff checklist

Run this mentally before composing. If three or more fail, redraft.

- [ ] Subject ≤45 chars, adds information
- [ ] Preheader ≤90 chars, doesn't restate subject
- [ ] One archetype, applied consistently
- [ ] Colour strategy committed (not "neutrals + accent" by reflex unless minimal-lux)
- [ ] No category-reflex palette
- [ ] At least one real image, sourced or explicitly prompted
- [ ] Single CTA above the fold; ≤2 total
- [ ] Footer has socials + physical address + unsubscribe (mission line only if verified — never invented)
- [ ] No double spacers, no `<br><br>`, no margin+padding combos
- [ ] No em dashes in body
- [ ] Single column ≤600px; touch targets ≥44px
- [ ] Voice is recognisable as the brand, not a template
- [ ] Offered a test send to the user before any real send

## Pushback patterns

When the user wants to iterate:

- **"Make it bolder"** → escalate colour strategy (restrained → committed → drenched), increase type contrast, shrink line lengths, swap to bold-mono or punk-character archetype.
- **"Make it quieter"** → de-escalate colour, increase whitespace selectively (not uniformly — that's the moonscape failure mode), strip secondary CTAs, swap to minimal-lux or editorial.
- **"Add personality"** → swap to founder-letter or punk-character; rewrite copy first-person; add one unexpected element (handwritten asset, mascot, ridiculous subject line).
- **"Too plain"** → almost always means the archetype is wrong. If you defaulted to minimal-lux, ask once whether they want bold-mono or lookbook instead.
- **"Looks like AI made it"** → category-reflex palette, stock-feeling imagery, or no voice. Diagnose which one and fix only that.

## Examples

### Brief — SaaS welcome email (founder-letter)

```json
{
  "name": "Welcome 1 — Founder Hello",
  "subject": "you're in",
  "preheader": "a quick note from the founder, plus what to expect this week",
  "archetype": "founder-letter",
  "color_strategy": "restrained",
  "primary_color": "#1f2933",
  "voice_descriptors": ["first-person", "concrete", "warm", "no marketing fluff"],
  "structure": [
    { "kind": "header", "logo": true, "padding": "compact" },
    { "kind": "headline", "content": "Hey, I'm [name]." },
    { "kind": "body", "content": "Three short paragraphs. What we built, why we built it, what to do this week." },
    { "kind": "cta", "label": "Reply with one thing you're trying to do", "url": "mailto:..." },
    { "kind": "footer" }
  ],
  "image_slots": [],
  "footer": {
    "mission_line": "Building [thing] so [who] can [outcome].",
    "socials": [{ "name": "linkedin", "url": "..." }],
    "physical_address": "...",
    "unsubscribe": "{{unsubscribe_url}}"
  },
  "anti_slop_checks": ["plain-text feel keeps it personal", "no stock imagery", "single CTA is a reply, not a click"]
}
```

### Brief — D2C product launch (bold-mono, drenched)

```json
{
  "name": "Launch — Nitro Blue Drop",
  "subject": "blue.",
  "preheader": "the new colorway. limited run. tomorrow 9am.",
  "archetype": "bold-mono",
  "color_strategy": "drenched",
  "primary_color": "#1d4ed8",
  "voice_descriptors": ["punchy", "confident", "few words"],
  "structure": [
    { "kind": "hero", "image_slot": "hero" },
    { "kind": "headline", "content": "Blue." },
    { "kind": "body", "content": "Limited to 200. 9am tomorrow." },
    { "kind": "cta", "label": "Set a reminder", "url": "..." },
    { "kind": "footer" }
  ],
  "image_slots": [
    {
      "slot_id": "hero",
      "purpose": "Single product shot on solid background. Same blue as primary_color. No text overlay.",
      "candidate_url": "https://brand.com/og-image.jpg",
      "user_prompt": "Got the product photo of the blue colorway? Drop the URL or upload via the media uploader."
    }
  ],
  "footer": {
    "mission_line": "Made for runners. Made in [city].",
    "socials": [
      { "name": "instagram", "url": "..." },
      { "name": "tiktok", "url": "..." }
    ],
    "physical_address": "...",
    "unsubscribe": "{{unsubscribe_url}}"
  },
  "anti_slop_checks": ["committed to one colour", "real product photo, not stock", "no double-padding"]
}
```

### Brief — Editorial newsletter (Patagonia-style)

```json
{
  "name": "Newsletter — Running gear for winter's worst",
  "subject": "running gear for winter's worst",
  "preheader": "what we wear when it's brutal out there",
  "archetype": "editorial",
  "color_strategy": "committed",
  "primary_color": "#0a3d2e",
  "voice_descriptors": ["earnest", "specific", "outdoorsy", "sells the weather, not the product"],
  "structure": [
    { "kind": "header", "logo": true, "padding": "compact" },
    { "kind": "hero", "image_slot": "winter-trail" },
    { "kind": "headline", "content": "When the weather wins, you don't." },
    { "kind": "body", "content": "Short essay — 120 words on running in horizontal sleet. No product names yet." },
    { "kind": "cta", "label": "See the kit", "url": "..." },
    { "kind": "secondary_body", "content": "Three pieces, briefly. Photo above each, not in a grid card." },
    { "kind": "footer" }
  ],
  "image_slots": [
    {
      "slot_id": "winter-trail",
      "purpose": "Editorial landscape — runner small in frame, weather doing the talking. No product close-ups in the hero.",
      "candidate_url": null,
      "user_prompt": "Have a winter trail / weather shot? Or shall I leave a placeholder?"
    }
  ],
  "footer": {
    "mission_line": "We're in business to save our home planet.",
    "socials": [{ "name": "instagram", "url": "..." }],
    "physical_address": "...",
    "unsubscribe": "{{unsubscribe_url}}"
  },
  "anti_slop_checks": ["no category-reflex green-and-brown palette", "hero sells the moment, not the product", "voice carries the email, not the design chrome"]
}
```
