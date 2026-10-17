---
name: awesome-design-md
description: 73 brand DESIGN.md files from real websites. Drop one into your project to generate consistent, brand-quality UI. Use when building UI that should match a specific design language, when a user references a brand's visual style, or when you need design tokens (colors, typography, spacing, rounded) for production-quality UI generation.
---

# Awesome DESIGN.md

DESIGN.md is a plain-text design system document that AI agents read to generate consistent UI. This skill provides 12 pre-analyzed brand design systems you can reference or drop into a project root.

## How to Use

### Quick Reference
When a user wants UI matching a brand's style, read the corresponding `.md` file from `design-md/` and apply its tokens:

```
design-md/claude.md    — Warm canvas, serif display, coral CTAs
design-md/vercel.md    — Black/white precision, Geist font
design-md/linear.app.md — Ultra-minimal, purple accent
design-md/stripe.md    — Purple gradients, weight-300 elegance
design-md/figma.md     — Vibrant multi-color, playful professional
design-md/framer.md    — Bold black/blue, motion-first
design-md/notion.md    — Warm minimalism, serif headings
design-md/cursor.md    — Sleek dark interface, gradient accents
design-md/spotify.md   — Dark UI, vibrant green accent
design-md/nike.md      — Bold typography, sport energy
design-md/apple.md     — Clean minimalism, SF Pro, spacious
design-md/tesla.md     — Stark futuristic, red accent
```

### Drop into Project
For persistent design guidance, copy a DESIGN.md to the project root:
```bash
cp ~/.claude/skills/awesome-design-md/design-md/<brand>.md ./DESIGN.md
```

### Apply Tokens
Each DESIGN.md contains structured tokens:
- **colors**: primary, ink, body, muted, canvas, surface, accent
- **typography**: display, title, body, caption, code scales
- **spacing**: section, component, inner scales
- **rounded**: xs, sm, md, lg, xl, full
- **shadows**: subtle, medium, prominent
- **motion**: duration, easing curves

### Full Collection
73 total DESIGN.md files available at https://github.com/VoltAgent/awesome-design-md
Download additional brands with:
```bash
gh api repos/VoltAgent/awesome-design-md/contents/design-md/<brand>/DESIGN.md --jq '.content' | base64 -d > <brand>.md
```

Available brands: airbnb, airtable, apple, binance, bmw, bugatti, cal, claude, clay, clickhouse, cohere, coinbase, composio, cursor, dell-1996, elevenlabs, expo, ferrari, figma, framer, hashicorp, hp, ibm, intercom, kraken, lamborghini, linear.app, lovable, mastercard, meta, minimax, mintlify, miro, mistral.ai, mongodb, nike, nintendo-2001, notion, nvidia, ollama, opencode.ai, pinterest, playstation, posthog, raycast, renault, replicate, resend, revolut, runwayml, sanity, sentry, shopify, slack, spacex, spotify, starbucks, stripe, supabase, superhuman, tesla, theverge, together.ai, uber, vercel, vodafone, voltagent, warp, webflow, wise, x.ai, zapier

## Design Language Categories

| Category | Brands |
|----------|--------|
| AI & LLM | claude, cohere, elevenlabs, minimax, mistral.ai, ollama, replicate, voltagent, x.ai |
| Developer Tools | cursor, expo, raycast, vercel, warp |
| Productivity | cal, intercom, linear.app, notion, zapier |
| Fintech | binance, coinbase, kraken, mastercard, revolut, stripe, wise |
| Design & Creative | figma, framer, miro, webflow |
| Automotive | bmw, bugatti, ferrari, lamborghini, renault, tesla |
| Consumer | airbnb, apple, nike, nvidia, pinterest, shopify, slack, spotify, starbucks, uber |

## Integration with Other Skills

- **ui-ux-pro-max** — Use DESIGN.md tokens with ui-ux-pro-max style/palette search
- **frontend-design-direction** — Pick a design direction, then apply matching DESIGN.md tokens
- **motion-ui** — Pair motion patterns with DESIGN.md spacing/timing tokens
- **design-system** — Use DESIGN.md tokens as the foundation for token architecture
