---
name: youtube-thumbnail-analyzer
description: "Download and visually analyze YouTube thumbnails for any topic or channel using YouTube Data API v3. Downloads high-res thumbnails from top-performing videos, then provides AI-powered visual analysis of patterns, colors, text usage, faces, composition, and design trends. Use when users want to (1) Analyze what thumbnail styles work in a niche, (2) Download thumbnails from top videos for a topic, (3) Study competitor thumbnail strategies, (4) Get thumbnail design recommendations backed by data, (5) Understand visual patterns that drive clicks, (6) Compare thumbnail approaches across channels. Requires user's YouTube Data API v3 key."
---

# YouTube Thumbnail Analyzer

Download and visually analyze thumbnails from top-performing YouTube videos for any topic or channel.

## Usage

```
/youtube-thumbnail-analyzer "air fryer recipes"
/youtube-thumbnail-analyzer @ChannelHandle
/youtube-thumbnail-analyzer --topic "Python tutorial" --max 20
/youtube-thumbnail-analyzer @ChannelHandle --top 15
```

## Instructions

### Step 1: Parse Arguments

Input mode (one of):
- **Topic/keyword**: search YouTube for top videos on this topic
- **Channel** (`@handle`, URL, or ID): use this channel's top videos

Also:
- **--max N** (optional): number of thumbnails to download (default: 20, max: 50)
- **--scan-limit N** (optional, channel mode): cap uploads scanned (default: whole channel)

### Step 2: Get the API Key

Check Claude memory for a YouTube Data API v3 key. If not found, ask:
> "I need a YouTube Data API v3 key to fetch video data. You can get one from the Google Cloud Console. Please paste your key."

### Step 3: Run the Bundled Script

Run `scripts/fetch_thumbnails.py` — resolve the path relative to this skill's own directory:

```bash
# Topic search
YT_API_KEY=API_KEY python3 <skill-dir>/scripts/fetch_thumbnails.py --topic "TOPIC" --max 20

# Channel
YT_API_KEY=API_KEY python3 <skill-dir>/scripts/fetch_thumbnails.py --channel "@handle" --max 20
```

Dependencies: `pip3 install google-api-python-client requests`.

The script ranks videos by views, downloads the highest-resolution thumbnail available
(maxres → sd → hq → mq), and writes an `index.md` alongside the images.

### Step 4: Read the Data

```
reports/data/thumbnail-analysis-<slug>-<YYYY-MM-DD>.json
```

Thumbnails land in `reports/thumbnails/<slug>-<YYYY-MM-DD>/` with an `index.md` in
the same folder. The JSON's `videos[].thumbnail_path` gives each image's full path.

### Step 5: Visually Analyze the Thumbnails

This is the step that makes this skill unique — Claude can see images.

**Read each downloaded thumbnail** with the Read tool (it supports images). For each:

1. **Color scheme**: dominant colors, warm vs cool tones, brightness, contrast
2. **Text overlay**: present? how much? font size, position, color, ALL CAPS?
3. **Face/person**: face present? expression? close-up or full body? position?
4. **Composition**: rule of thirds? split screen? before/after? product-focused?
5. **Objects/props**: what objects are visible? food? tech? books?
6. **Background**: solid color? gradient? real location? blurred?
7. **Branding**: logo? consistent style across the channel?
8. **Emotion**: curiosity? excitement? shock?
9. **Clickbait signals**: arrows? circles? red X marks? exaggerated expressions?

Read thumbnails in batches of 5. Don't describe every thumbnail individually — focus on
identifying PATTERNS across all of them, and on what separates the top-viewed from the rest.

### Step 6: Write the Report

Write to the path the script printed: `reports/thumbnail-analysis-<slug>-<YYYY-MM-DD>.md`

```markdown
# Thumbnail Analysis Report: [Source]
*Analyzed [date] | [N] thumbnails from top-performing videos*

## Executive Summary
3-4 bullet points: Key visual patterns that drive clicks in this niche.

## Performance Context
| # | Title | Views | Engagement | Thumbnail File |
|---|-------|-------|------------|----------------|
[Top 10 videos with their metrics]

## Visual Pattern Analysis

### Color Schemes
- Dominant color palette across top thumbnails
- Warm vs cool color usage
- Brightness and contrast patterns
- Color combinations that correlate with high views

### Text Overlay Patterns
- % of thumbnails using text
- Average word count on thumbnail
- Font style patterns (bold, ALL CAPS, etc.)
- Text positioning (top, center, bottom)
- Text color against background
- What kind of text works (numbers, questions, statements)

### Face & Expression Patterns
- % of thumbnails featuring a face
- Common expressions (surprise, smile, serious, excited)
- Close-up vs medium shot vs full body
- Face position (center, left, right)
- Eye contact with viewer

### Composition Styles
- Most common layouts
- Use of before/after, split-screen, product focus
- Negative space usage
- Visual hierarchy

### Clickbait Elements
- Arrows, circles, and highlighting
- Red X or checkmarks
- Exaggerated reactions
- "vs" or comparison layouts

### Branding & Consistency
- Channels using consistent thumbnail style
- Logo/watermark usage
- Color brand consistency

## What Separates Top Performers
Analysis of what the highest-view thumbnails do differently from lower-view ones.

## Thumbnail Design Recommendations
5-8 specific, actionable recommendations:
1. **[Recommendation]** -- Backed by [data/observation]
...

## Thumbnail Templates
Based on patterns, suggest 3 thumbnail "formulas" that work in this niche:

### Template 1: [Name]
- Layout description
- Color scheme
- Text approach
- Example from data

### Template 2: [Name]
### Template 3: [Name]

## Quota Usage
| Operation | Calls | Units |
|-----------|-------|-------|
Use the `quota_used.breakdown` block from the JSON.
```

### Step 7: Report Completion

Tell the user the report path, the thumbnails folder, how many were downloaded, the
top 3 visual insights, the template recommendations, and the quota consumed.
Suggest opening `index.md` in Obsidian to see all thumbnails at once.

## Quota Estimate

| Mode | Operations | Total |
|------|-----------|-------|
| Topic (20 thumbnails) | 1 `search.list` + 1 `videos.list` + 1 `channels.list` | **~102** |
| Channel (500-video channel) | 1 `channels.list` + ~10 `playlistItems.list` + ~10 `videos.list` + 1 `channels.list` | **~22** |

Channel mode previously cost ~103 units via `search.list(channelId=..., order=viewCount)`,
which also only saw a partial slice of the channel; the uploads-playlist route ranks
across every upload for ~22. Thumbnail image downloads use img.youtube.com and cost 0 quota.
Daily default allowance is 10,000 units, resetting at midnight Pacific Time.
