---
name: geo-multimodal-tagger
description: Generate AI-optimized Alt Text, file names, captions, and Schema markup for images, videos, and audio assets. Improves AI discoverability on Google Lens, ChatGPT Vision, and Perplexity. Use whenever the user mentions optimizing images for AI, writing Alt Text, generating video Schema, tagging assets for AI discoverability, or making images visible in ChatGPT Vision and Google Lens.
---

# Multimodal Asset Tagger

> Methodology by **GEOly AI** (geoly.ai) — every image and video is a citation opportunity AI can either read or miss.

Generate optimized metadata for images, videos, and audio files for AI platforms.

## Quick Start

```bash
python scripts/optimize_asset.py --type image --description "dashboard showing metrics" --output optimized.md
```

## Why Multimodal Matters

AI platforms increasingly read visual content:

| Platform | Visual Capability | Citation Type |
|----------|-------------------|---------------|
| Google Lens | Image search | Direct image citation |
| ChatGPT Vision | Image understanding | Contextual reference |
| Perplexity | Video transcripts | Transcript citations |
| Gemini | Native image processing | Multimodal answers |

## Image Optimization

### Alt Text Formula

```
[Descriptive subject] + [Brand if relevant] + [Context/use case]
```

**Examples:**

❌ `alt="image1.jpg"`  
❌ `alt="product photo"`  
✅ `alt="GEOly AI dashboard showing AIGVR score trend over 30 days"`  
✅ `alt="Brand visibility comparison chart across ChatGPT and Perplexity — GEOly AI"`

### Filename Formula

```
[primary-keyword]-[secondary-keyword]-[brand]-[descriptor].jpg
```

**Examples:**

❌ `IMG_3847.jpg`  
✅ `geo-brand-visibility-dashboard-geoly-ai.png`  
✅ `aigvr-score-chart-ai-search-monitoring.jpg`

### ImageObject Schema

```json
{
  "@context": "https://schema.org",
  "@type": "ImageObject",
  "name": "AIGVR Score Dashboard",
  "description": "Dashboard showing brand visibility scores across AI platforms",
  "contentUrl": "https://example.com/images/dashboard.jpg",
  "author": {
    "@type": "Organization",
    "name": "GEOly AI"
  },
  "keywords": "AIGVR, brand visibility, AI search, dashboard"
}
```

## Video Optimization

### Checklist

- [ ] Title contains primary keyword
- [ ] Description: first 150 chars = keyword + brand
- [ ] Transcript/captions attached (SRT/VTT)
- [ ] Chapters/timestamps for long videos
- [ ] Thumbnail: keyword-rich filename
- [ ] VideoObject Schema added

### VideoObject Schema

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "How to Optimize for AI Search",
  "description": "Complete guide to GEO strategies...",
  "thumbnailUrl": "https://example.com/thumbs/geo-guide.jpg",
  "uploadDate": "2024-01-15",
  "duration": "PT12M30S",
  "contentUrl": "https://example.com/videos/geo-guide.mp4"
}
```

## Audio/Podcast Optimization

- Descriptive episode titles (not "Episode 47")
- 150+ word descriptions, keyword-rich
- Full transcript as page content
- Guest names and topics as entities

## Asset Optimization Tool

```bash
python scripts/optimize_asset.py \
  --type [image|video|audio] \
  --description "Asset description" \
  --brand "BrandName" \
  --keywords "keyword1,keyword2"
```

**Output:**
- Optimized Alt Text
- Recommended filename
- Schema markup
- Discoverability score (Before/After)

## Scoring

| Factor | Weight | Best Practice |
|--------|--------|---------------|
| Descriptiveness | 30% | Specific, detailed |
| Keyword presence | 25% | Natural inclusion |
| Brand mention | 20% | When relevant |
| Context | 15% | Use case clear |
| Length | 10% | 100-150 chars for Alt |

**Discoverability Score**: 0-10
- 8-10: Excellent
- 6-7: Good
- 4-5: Fair
- <4: Poor