---
name: app-marketing-copy
description: "Write marketing copy and App Store / Google Play listings (ASO keywords, titles, subtitles, short+long descriptions, feature bullets, release notes), plus screenshot caption sets and text-to-image prompt templates for generating store screenshot backgrounds/promo visuals. Use when asked to: write/refresh app marketing copy, craft app store metadata, brainstorm taglines/value props, produce ad/landing/email copy, or generate prompts for screenshot/creative generation."
---

# App Marketing Copy

## Quick start

1) Ask for missing inputs (or infer from repo/product docs):
- App name + 1-sentence value prop
- Target user + primary job-to-be-done
- 3–7 key features + 1–3 differentiators
- Desired tone (and words to use/avoid)
- Platform(s): iOS App Store, Google Play, or both
- Screenshot count and theme (if needed)

2) Confirm deliverables:
- Store listing (iOS, Google Play)
- Marketing pack (landing hero, feature blurbs, CTAs, ads)
- Screenshot pack (caption copy + image-generation prompts)

3) Produce 2–3 variants per high-impact field, then recommend a “best pick” with 1-sentence rationale.

## Intake template (ask, then proceed)

- Audience: who + what they want
- Problem: what’s hard today
- Outcome: what “success” looks like
- Differentiators: why this vs alternatives
- Proof: numbers, reviews, awards, press (if any)
- Constraints: claims to avoid, legal/compliance notes, pricing mention policy
- Locale(s): default to US English unless told otherwise

## Outputs

### iOS App Store listing

- Provide: App Name options, Subtitle options, Promotional Text, Keyword set, Full Description, “What’s New” (release notes).
- Enforce field limits; if unsure, open `references/app-store-metadata.md` or run `scripts/check_app_store_limits.py`.

### Google Play listing

- Provide: Title options, Short Description options, Full Description, Feature bullets, Release notes.
- Enforce limits; see `references/app-store-metadata.md` or `scripts/check_app_store_limits.py`.

### Marketing copy pack

- Provide: 5–10 taglines, 3 hero sections (headline + subhead + CTA), 6 feature blurbs (1–2 sentences), 10 micro-CTAs, 10 ad hooks (short), 5 social posts.
- Keep claims supportable; avoid “#1 / best” unless proven.

### Screenshot pack (copy + prompts)

- Provide: 5–8 screenshot captions (2–5 words each) + optional sub-captions; include a narrative order (setup → value → proof → CTA).
- Provide: per-screenshot art direction + a prompt template for text-to-image generation (backgrounds/illustrations), tailored to the user’s tool.
- Use `references/screenshot-prompts.md` for prompt patterns and negative prompts.

## Quality checks (do before final)

- Character limits: validate with `scripts/check_app_store_limits.py` for store fields.
- Consistency: keep the same core value prop across title/subtitle/hero/screenshot 1.
- Compliance: avoid disallowed claims, competitor trademarks, and sensitive targeting; ask if regulated domain (health/finance/kids).
- Readability: short sentences, active voice, scannable bullets.

## Included resources

- `references/app-store-metadata.md`: field map + common limits + output skeletons.
- `references/screenshot-prompts.md`: prompt templates for backgrounds and promo visuals.
- `scripts/check_app_store_limits.py`: quick character-limit checker for iOS/Google Play fields (JSON in, table out).
