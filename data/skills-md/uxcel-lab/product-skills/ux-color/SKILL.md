---
name: ux-color
description: Design or critique a product's color palette and system — base hue, harmony, neutrals, semantic colors, tonal scales, and tokens. Applies the always-true core and gates context-dependent decisions (dark mode, brand expressiveness, accessibility trade-offs). Trigger when creating a color palette, choosing UI colors, building a color system, setting up color tokens, or reviewing a palette for issues.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Color Palette & System Skill


## How this skill behaves (read first)

This is a **generative** skill. Color has two opposite default failure modes: **arbitrary** (pick a nice blue, no system, fails contrast) and **garish** (apply every emotional/cultural association and standout trick → the over-colored "Willy Wonka" palette `aesthetics` warns about). So this skill gates:

1. **Establish brand, audience, and market** — these drive the *one* set of hue/emotion/culture choices worth making.
2. **Apply the always-true core** — a restrained, role-based, tokenized, accessible palette holds for any product.
3. **Make the expressive choices deliberately** — surface base-hue/emotion/saturation/dark-mode as gated decisions, not defaults.

Then **hand off to the audits**: `accessibility` owns contrast ratios and color-blindness; `aesthetics` owns harmony and balance.

---

## Step 0 — Establish context before choosing colors

- **Brand & industry** — existing brand colors/guidelines? Industry conventions (finance → trust/navy; kids → playful)? Check competitors for the field's visual language.
- **Audience & market** — who, and **where** — color meaning is culture-dependent (see the emotion reference caveat).
- **Personality** — premium/refined vs. playful/energetic? This drives saturation and neutrals more than hue.
- **Modes** — light only, or dark mode too?

State assumptions if proceeding without answers.

---

## The always-apply core (true for any palette/system)

- **Build on a harmony scheme, then refine.** Start from a base color and a scheme — **monochromatic/analogous** (safe, low-contrast) or **complementary** (high-contrast, soften with tints/transitional tones) — then adjust saturation/brightness for interest.
- **Neutral-dominant, accent-sparing — the 60-30-10 rule.** ~60% primary/neutral surface, ~30% secondary, ~10% accent reserved for elements that must stand out (CTAs). Primary/secondary stay relatively neutral for readability.
- **Define color by role, not just hue.** A system needs: **primary / secondary / tertiary** accents (with on-color pairs), **neutral/surface** tones, and **functional/semantic** colors (success, warning, error, info).
- **Keep functional colors distinct from brand.** If the brand color is a bright red near the error red, define a separate error family so users don't confuse branding with feedback.
- **Build tonal scales + tokens.** Generate consistent tints/shades from each base; expose them as named **variables/tokens** (functional or numeric naming) so one change propagates and the system stays consistent.
- **Never rely on color alone**, and **check every text/icon/surface pair for contrast** — defer the actual ratios and color-blindness checks to the `accessibility` audit, but the palette must be built to pass them.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0. **Stacking many saturated hues/associations is the failure mode.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Base hue / emotional tone** | Match hue to the feeling the brand wants (see reference) | Picking a hue for taste alone, or chasing every association | One intentional base aligned to brand + industry |
| **Harmony scheme** | Complementary for vivid/high-energy; analogous/mono for calm/refined | Complementary at full chroma (too intense) | Analogous/mono as the safe default; complementary softened with neutrals |
| **Saturation / vibrancy** | High saturation for playful/energetic brands | Premium/enterprise (use restrained, desaturated tones) | Match to personality; neutral anchor for any bold accent |
| **Cultural adaptation** | Global product / specific markets (color meaning differs) | Single-market where convention is settled | Validate key hues against target markets |
| **Number of accents** | One clear accent; a second only if it earns a role | Many competing accent colors (garish, no focal point) | One accent + functional colors; everything else neutral |
| **Dark mode** | Product needs/expects it | Bolting it on by simple inversion | Design semantic colors for both modes (below) |

### Color → emotion (the gated menu — use sparingly, context decides)
Yellow: happy/warm · Orange: energetic/enthusiastic · Red: stimulating/urgent/passionate (also alarm) · Blue: calming + trustworthy (navy → finance/tech trust) · Green: grounded/natural/success · Purple: creative/spiritual/premium · Pink: soft/nurturing (mind shifting gender connotations) · Brown/earth tones: stable/grounded. **Caveat:** these are Western-leaning and context-dependent — the *same* hue means different things by culture and surrounding colors. Pick one intentional association; don't paint with all of them.

### Dark mode notes
Define **semantic** colors (purpose, not literal hue) so they adapt across modes; don't just invert light mode. Maintain contrast in **both** modes, signal elevation with **lighter surfaces** (not just shadow) in dark mode, and test in real lighting conditions.

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After defining or revising the palette, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **none are Tier A; `accessibility` and `aesthetics` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — contrast ratios for every text/icon/surface pair (light **and** dark mode), and color-blindness safety (don't encode status by red/green alone). The palette must be built to pass this.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — harmony and balance: is it neutral-dominant with a clear accent, or has it tipped into the over-colored, no-focal-point "Willy Wonka" zone?

If accessibility fails a pair or aesthetics flags garishness, return to the 60-30-10 / one-accent core.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Pick a nice color with no system | Define roles: primary/secondary/tertiary + neutrals + functional |
| Equal amounts of several bright colors | 60-30-10: neutral-dominant, one ~10% accent |
| Apply every color-emotion association | One intentional association tied to brand + market |
| Full-chroma complementary clash | Soften with tints/neutrals; analogous/mono as the safe base |
| Brand red ≈ error red | Separate functional color families from brand |
| Hardcode hex everywhere | Tonal scales exposed as named tokens/variables |
| Encode status by color alone | Color + icon/label (→ accessibility) |
| Invert light mode for "dark mode" | Semantic colors designed for both modes; elevation via lighter surfaces |
| Ship without contrast checks | Hand off to accessibility (ratios + color-blindness) and aesthetics |

---

## Source lessons (Uxcel)

- [How to Create a Color Palette](https://uxcel.com/lessons/creating-a-color-palette-208)
- [Intro to Color Theory](https://uxcel.com/lessons/color-wheel-i-156)
- [Color in Design Systems](https://uxcel.com/lessons/color-systems-439)
- [How Color Affects Mood & Emotion](https://uxcel.com/lessons/how-does-color-affect-emotion-926)
- [Color Systems & Dark Mode](https://uxcel.com/lessons/color-systems-dark-mode-518)
