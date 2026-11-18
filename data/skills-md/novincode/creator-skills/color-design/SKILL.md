---
name: color-design
description: Chooses and directs color for videos, thumbnails, animation and brand systems, covering palettes with roles, color scripts across a story, grading direction, contrast and accessibility. Use when the user needs a palette, color scheme, color grade or LUT direction, thumbnail colors, a color script, brand colors for a channel, or says colors look muddy, garish, inconsistent, flat or AI-generated.
license: MIT
metadata:
  version: "0.1.0"
  status: alpha
  category: production
  pack: creator-skills
---

# Color Design

Color is emotion and hierarchy at the speed of sight. People read value (light vs. dark) first, then saturation, then hue. Most color problems are value problems.

## The floor

1. **Value first.** Squint or convert to grayscale. If the subject doesn't separate from the background in grayscale, no hue will save it [C, standard in painting and design].
2. **Every color has a role.** Background, subject, accent, text, warning. A palette without roles is a mood board.
3. **One accent.** The most saturated color goes where the eye should land, and almost nowhere else.
4. **Color follows story.** Plan how color changes across the piece (a color script) instead of one look for everything.
5. **Contrast for text is a standard, not taste.** On-screen text aims for WCAG contrast of at least 4.5:1 against its background (3:1 for large text) [A, W3C WCAG 2.x].
6. **Don't rely on red vs. green alone.** Roughly 1 in 12 men and 1 in 200 women have color vision deficiency [A]. Pair color with value, shape or labels.
7. **Protect skin tones in grading.** Push the look in the shadows and highlights; keep skin natural unless the stylization is the point.
8. **Lock the palette in the bible** as hex values with roles.

## Palette building

1. Start from the story's emotion and the creator's identity, not a color wheel.
2. Pick the **dominant** (most area), **secondary**, and **accent**. A common split is about 60 / 30 / 10 [C].
3. Choose a harmony as a starting point, then adjust by eye:
   - **Complementary** (opposites): maximum pop; thumbnails, subject vs. background.
   - **Analogous** (neighbors): calm, cohesive; documentaries, mood pieces.
   - **Split-complementary:** pop with less tension.
   - **Triadic:** playful, energetic; kids' and comedy content (keep one dominant).
4. Check value separation in grayscale.
5. Check text contrast.
6. Write it down with roles.

## Color script

Borrowed from animation studios (Pixar's color scripts are the famous example): a strip of small frames showing the dominant color of each beat across the whole story.

```
HOOK        SETUP        ESCALATION       TURN            BUTTON
sepia gold  warm amber   sickly brown     near-black      cold gray + one brown accent
calm        nostalgic    oppressive       shock           aftermath
```

Use it to make color shifts deliberate and to brief `storyboarding` and `visual-prompting`.

## Emotion and color [C, culture-dependent]

Associations vary by culture and context, so treat these as starting points:
- Warm, saturated: energy, appetite, danger, nostalgia (when desaturated).
- Cool, desaturated: distance, calm, sadness, clinical.
- High contrast: drama, tension. Low contrast: dreamy, soft, foggy.
- A single saturated element in a desaturated frame: importance, the focal point.

## Thumbnails [C]

- Bright, saturated subject against a simpler or darker background.
- Avoid using the platform interface's own colors as your main contrast color.
- Test at phone size and in both light and dark platform themes.
- One color story across a channel's thumbnails helps recognition.

## Grading direction (for editors or AI prompts)

Describe grades in concrete terms: "lift shadows slightly toward blue, warm highlights, reduce saturation 15%, keep skin natural" rather than "moody cinematic look". Name a film stock or reference era when that's the target.

## Output

```markdown
## Color: <project>
| Role | Hex | Use |
|---|---|---|
| Background | #1E1A16 | 60% · scenes, cards |
| Secondary | #6B4A2B | 30% · molasses, props |
| Accent | #E8B04A | 10% · numbers, key words, focal point (8.8:1 on background) |
| Text | #F4EFE6 | on background: 15.1:1 |
Color script: <strip as above>
Grade: <concrete notes>
```

Report contrast ratios for every text/background pair you specify. Compute them, don't guess.
