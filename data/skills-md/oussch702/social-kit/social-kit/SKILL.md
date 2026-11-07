---
name: social-kit
description: Make on-brand social media images from a brand file and plain text, rendered with headless Chrome. Use for a LinkedIn carousel (document post, PDF plus PNG slides), Instagram highlight covers, Instagram story templates, a LinkedIn profile banner, an Open Graph (OG) share image, a quote card or testimonial card, or any social media design that should match a brand's logo, colours and fonts.
---

# social-kit

social-kit turns `brand.json` (logo, colours, fonts) and `spec.json` (the words) into finished PNGs, plus a PDF for each LinkedIn carousel. It needs Node 22+ and a local Chrome, Chromium or Edge. There is nothing to install.

The CLI is `bin/social-kit.mjs` at the root of this plugin, two folders above this file. Below, `social-kit` means `node <plugin root>/bin/social-kit.mjs`.

## 1. Gather the brand

Ask for, or find in the user's project:

- Brand name and website (shown in footers).
- Logo as SVG or PNG. A square mark works best; a wide wordmark works with `"showName": false`.
- Colours as hex: `bg` (page), `ink` (text), `muted` (small grey text), `accent` (bullets, highlight fills) and `accentInk` (an accent shade dark enough for text on `bg`).
- Fonts: a display face for headlines, a body face, and an italic serif for *emphasis*. Local `.woff2`, `.woff`, `.ttf` or `.otf` files. If the user has none, keep the bundled defaults.

Run `social-kit init <folder>` to get a working `brand.json`, `spec.json`, logo and fonts, then edit them. Check that `ink` on `bg` is readable; `social-kit check` warns below 4.5:1.

## 2. Write the spec

Only include the assets the user asked for. Wrap a word or two of each headline in `*asterisks*` to set it in the italic serif; one emphasis per headline is enough.

```json
{
  "brand": "./brand.json",
  "carousel": { "url": "example.com/guide", "slides": [
    { "type": "cover", "kicker": "Guide · 2026", "title": "The headline with *one emphasis*" },
    { "type": "rows", "title": "Five plans", "rows": [["Basic", "$49", "250 minutes a month"]] },
    { "type": "statement", "title": "One idea per slide", "body": "A sentence or two." },
    { "type": "math", "kicker": "300 calls a month", "lines": [["Plan", "$150.00"]], "total": ["Your bill", "$712.50"] },
    { "type": "checklist", "title": "Before you buy", "items": ["Step one", "Step two"] },
    { "type": "cards", "title": "Two options", "cards": [["Name", "$0.07 a minute", "One line on why"]] },
    { "type": "cta", "title": "The full guide, *free*" }
  ] },
  "stories": [
    { "type": "stat", "kicker": "Client result", "number": "4.4M", "line": "views in *90 days*", "footnote": "Source or detail" },
    { "type": "quote", "quote": "Exact words of the client.", "name": "Name", "role": "Role, Company" },
    { "type": "list", "title": "How it *works*", "items": ["One", "Two", "Three"] },
    { "type": "cta", "title": "Want one?", "link": "example.com", "hint": "Tap the link in our bio." }
  ],
  "highlights": ["star", "quote", { "icon": "zap", "style": "accent" }],
  "banner": { "kicker": "What you do", "title": "The promise in *one line*", "chips": ["Proof one", "Proof two"], "url": "example.com" },
  "og": { "kicker": "Guide · 2026", "title": "Page title, *short*" },
  "quote": { "quote": "Exact words.", "name": "Name", "role": "Role, Company" }
}
```

Content rules that keep slides readable:

- One idea per slide. Headlines under about 10 words. Checklists 3 to 6 items, tables up to 6 rows, cards up to 3.
- Never invent numbers, quotes or client names. Use what the user gives you, and say where a figure comes from in a `note` or `footnote`.
- Highlight icons: `social-kit icons` lists them, or use `{ "svg": "./icon.svg" }`. Styles: `ink`, `accent`, `light`.

Run `social-kit check spec.json` and fix every message it prints.

## 3. Render

```
social-kit render spec.json --out out/
```

Headlines shrink automatically to fit. The command prints a `note` when text had to be scaled down and lists any page that still overflows (exit code 2).

## 4. Look before you deliver

Rendering is not the end. Open `out/contact-sheet.png` (it is written on every render; `social-kit contact-sheet out/` rebuilds it) and look at every tile, then open any doubtful PNG at full size. Check for:

- Text cut off, overlapping the logo or footer, or running past the edge.
- A headline that shrank to a much smaller size than its neighbours (shorten it instead).
- Orphans: one word alone on the last line of a headline.
- Stories: nothing important in the top 250px or bottom 330px.
- Banner: nothing important in the left 420px, where the profile photo sits.

Fix the words in `spec.json`, render again, and look again. Only hand over the files when every page looks deliberate. Tell the user where the PDF (for a LinkedIn document post) and the PNGs are.
