---
name: dark-tech
description: |
  Genre pack: dark, precise, developer-adjacent minimalism — the Linear/Vercel/Stripe-dark school. Near-black surfaces, one restrained accent, fine hairline borders, compact type, subtle glow only on the accent, dashboard-ready density. Use for developer tools, infra products, AI platforms, and technical audiences. Stack on the design-taste core skill.
triggers:
  - "dark tech"
  - "developer tools"
  - "linear style"
  - "dark mode"
  - "vercel style"
  - "infra product"
  - "ai platform"
  - "technical audience"
---

# dark-tech

> One identity: **a machine you can trust — precise, quiet, fast.**

## 1. PALETTE (Fixed)

- Ground: `#08090A` (near-black). Panels: `#0E0F11` and `#131417`. Hover surfaces: `#181A1D`.
- Ink text: `#F7F7F8` (primary), `#9CA3AD` (secondary), `#5C6370` (tertiary/muted).
- Borders: `rgba(255, 255, 255, 0.08)` hairlines. Stronger on interactive: `rgba(255, 255, 255, 0.16)`.
- Accent — exactly one: indigo `#5E6AD2`, violet `#7C7CF0`, or emerald-safe `#34D399` — selected by brand/meaning. Accent used for: links, the single primary button, active states, one data series.
- No gradients (flat surfaces only), no colored full-bleed backgrounds. Glow allowed ONLY on the accent: `box-shadow: 0 0 0 1px rgba(accent, .35), 0 0 24px rgba(accent, .25)` on the primary button.

## 2. TYPOGRAPHY (Fixed)

- **Display:** neutral grotesk with personality — Space Grotesk, or system sans at 500–600 weight. Sizes `clamp(2.2rem, 5vw, 4rem)`, tracking −0.03em, leading 1.05. Dark tech is restrained: powerful but not shouting.
- **Body:** 14–15px, `#9CA3AD` secondary for almost everything; pure `#F7F7F8` reserved for headings, key values, and interactive labels. Line-height 1.55.
- **Labels/metadata:** monospaced (`IBM Plex Mono` / `ui-monospace`), 11–12px, `#5C6370`, no letterspacing theatrics (0–0.02em). Version numbers, keys, statuses live here.
- UI density: 12–14px is normal. This is an instrument console, not a billboard.

## 3. COMPOSITION (Fixed)

- **Fine border discipline:** every panel, row, and table cell is separated by 1px `rgba(255,255,255,0.08)` borders. Inner fills are tonal (`#0E0F11` / `#131417`), never white cards on black.
- **Hero:** small caps mono kicker, medium-size headline (max 4rem), sub in secondary, CTA row — primary accent button + ghost button. Optional: a metrics strip or product panel below, bordered.
- **Data is the hero:** metrics, code blocks, terminal snippets, and status tables are aesthetic assets. A bordered panel with mono numbers beats a decorative illustration.
- **Radius: 6–10px** on panels (this is the ONE pack where a bit of radius is correct — machine parts), 4–6px on buttons. Shadows only at hover: `0 4px 20px rgba(0,0,0,0.5)`.
- Pricing: bordered rows or 3-panel grid; featured panel gets a 1px accent border + accent dot/check list.

## 4. CONTENT TREATMENT

- No emoji as icons. Draw icons: 1.5px stroke, rounded caps, 16–20px grid, `#9CA3AD` at rest, accent at active.
- No photography by default. Dark-tech surfaces are better empty: hairlines, mono labels, and metrics.
- Status language: `status: healthy`, `v2.4.1`, `99.99% SLA` — product authenticity beats marketing claims.
- CTA text: concrete ("Deploy now", "Run benchmark"), never "Get started today!!".

## 5. MOTION (Precise)

- Durations 120–240ms. Easing `cubic-bezier(0.4, 0, 0.2, 1)` (Material-style) or `ease-out` hovers.
- Hover: surface tone shift (`#0E0F11` → `#131417`) + border brighten. Border/glow transitions only, 150ms.
- One allowed flourish: a slow ambient status pulse on one accent element (like a "live" dot), 2–4s cycle, opacity only.
- Respect `prefers-reduced-motion`: everything off.

## 6. CHECKLIST (Fail the page if…)

- [ ] Any white or light background surfaces (main background must be near-black).
- [ ] More than one accent color in use.
- [ ] Any gradient fill.
- [ ] Headline above 4rem or in a display serif.
- [ ] Body text in pure white for normal paragraphs.
- [ ] Rounded corners above 10px on panels or above 6px on buttons.
- [ ] Emoji icons or bright marketing photography.
- [ ] Any section that could not exist in a developer tool.