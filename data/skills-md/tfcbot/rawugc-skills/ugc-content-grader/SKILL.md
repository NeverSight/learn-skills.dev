---
name: ugc-content-grader
description: Score and grade short-form UGC video ideas for quality, complexity, and nativeness. Use when the user wants to evaluate, audit, or improve UGC video scripts, hooks, overlays, and shot lists for platforms like TikTok and Reels.
---

# UGC Content Grader

Procedural knowledge for auditing and scoring short-form UGC video ideas destined for AI generation (RawUGC / Sora / Veo). Apply these rubrics to every card in a kanban board or any batch of UGC scripts.

## When to Use

- User asks to "score", "grade", "audit", or "review" UGC ideas
- User asks to "improve" low-scoring content
- User adds new ideas and wants them evaluated
- User wants to check if content "sounds like an ad"

## Scores

Every idea receives three scores. All three must be present.

### 1. Quality Score (1–10)

Does the script make sense for the target audience and short-form platform?

| Range | Label | Meaning |
|-------|-------|---------|
| 8–10  | High  | Hook stops the scroll, overlay is tight, shot list is filmable, angle lands for the persona |
| 5–7   | Mid   | Decent but something is off — weak hook, overlay too long, angle mismatch |
| 1–4   | Low   | Doesn't work — confusing, wrong audience, wouldn't hold attention past 1 second |

See [reference.md](reference.md) for the full quality rubric.

### 2. Complexity Score (low / medium / high)

How likely is AI video generation to fail or produce artifacts?

| Level  | Meaning |
|--------|---------|
| low    | Static location, one person, no props requiring precision, no on-screen text/numbers, no walking |
| medium | One location change OR one precise prop interaction OR brief text on screen |
| high   | Screen content, multiple simultaneous props, walking while talking, specific readable text/numbers, two-phone setups |

**Target: low.** If an idea scores medium or high, rewrite the shot list to remove the offending elements. Common fixes in [reference.md](reference.md).

### 3. Native Score (1–10)

Does this feel like organic creator content or does it read like an ad?

**High = native/casual. Low = reads like an ad.**

| Range | Label  | Color | Meaning |
|-------|--------|-------|---------|
| 7–10  | Native | Green | Feels like a real person posting organically — storytime, pov, rant, hot take, meme format |
| 4–6   | Mid    | Orange | Mixed — decent hook but some ad structure leaking through |
| 1–3   | Adsy   | Red   | Reads like a marketing department wrote it — jargon, checklists, "link in bio", feature lists |

See [reference.md](reference.md) for the full native scoring rubric with red flags and green flags.

## CTA Rules

- **Ratio**: 1/3 of ideas should have a CTA. 2/3 should have NO CTA.
- **No "link in bio"** — ever. It screams ad.
- **Acceptable CTA format**: Comment-keyword style only (e.g. "comment SUNDAY and I'll send you the process")
- **No CTAs that sound like landing pages**: "try it free today", "see what it costs", "start your free trial" are all banned.
- When distributing CTAs across a batch, spread them evenly — don't cluster all CTAs in one funnel phase.

## Improvement Workflow

When content scores below threshold, rewrite it following these principles:

1. **Hook**: Rewrite as storytime, pov, hot take, or rant. First person. Emotional. Specific.
2. **Overlay**: Conversational, not formatted. No bullet points or checklists. Short — max 4 lines.
3. **Shot List**: Keep it to 3–4 simple shots. One static location. No complex choreography.
4. **Tone**: Gen-Z native — self-deprecating, unhinged, chaotic, conspiratorial, smug, confused. NOT: professional, motivational, coach-y, LinkedIn energy.

## Data Format

Scores are saved directly on each card object:

```json
{
  "qualityScore": 9,
  "complexityScore": "low",
  "nativeScore": 8
}
```

For the full rubric details, scoring examples, red/green flags, and rewrite patterns see [reference.md](reference.md).
