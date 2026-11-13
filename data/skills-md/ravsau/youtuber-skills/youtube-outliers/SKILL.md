---
name: youtube-outliers
description: "3x outlier videos in a niche, their format, and 3 adaptations. Use when picking the next video or asked what is working in a lane."
argument-hint: "[your niche] [optional: channels to study, your last 3 video titles]"
---

# YouTube Outliers

Input: a niche, and if given, channels to study and the creator's own recent titles.
Output: an outlier table, the formats behind them, and 3 adaptations ready to package.

## Steps

1. List 5-8 channels: direct niche, adjacent niche, one unrelated niche with the same audience age.
2. For each channel, take the last 20 videos and compute the average views. Flag any video at 3x or more.
3. Drop outliers caused by news events or collabs. Keep format-driven ones.
4. For each kept outlier, strip the topic and write the format as one sentence with blanks.
5. Write 3 adaptations that fill the blanks with the creator's niche, angle, and budget.
6. Rank them by fit, then hand the top one to youtube-packaging.

## Rules

- A format is a structure, never a topic. "[Tool A] vs [Tool B], tested for [N] days" is a format.
- Keep the tension of the original and shrink the spend to the creator's budget.
- Every adaptation must add something the original cannot: expertise, data, or access.
- If public view counts are unavailable, say so and ask for the creator's own numbers.
- Never list an outlier without its multiple.

## Output format

```markdown
## Outliers: [niche]

| Video | Channel | Views | Channel avg | Multiple | Format |
|-------|---------|-------|-------------|----------|--------|
| ... | ... | ... | ... | 4.2x | ... |

### Adaptations
1. **[title idea]** from [format]. Angle: ... Budget: ...
2. ...
3. ...

Top pick: #N. Why: one line.
```

## Example

Input: `local AI on Mac; channels: two hardware reviewers, one ML tutorial channel`

| Video | Channel | Views | Channel avg | Multiple | Format |
|-------|---------|-------|-------------|----------|--------|
| "I bought every M4 Mac to find the best one" | HardwareChannelA | 1.2M | 210K | 5.7x | Buy the full range, one task, one winner |
| "Llama runs on a Raspberry Pi. Here is how slow" | MLChannelB | 480K | 60K | 8.0x | Big model on the smallest box, show the pain |

### Adaptations
1. **Every Mac RAM tier runs the same coding agent. One wins.** from "full range, one task". Angle: agent latency, not benchmarks. Budget: borrow the machines.
2. **Claude Code on an 8GB Mac with a local model** from "smallest box, show the pain". Angle: what breaks first. Budget: zero.
3. **One 128GB Mac vs five cheap Minis for a team of agents** from "full range, one task". Angle: cost per agent. Budget: rental.

Top pick: #2. Cheapest to film and the pain is the thumbnail.

CRITICAL: never present a guessed view count as measured. Mark estimates.
