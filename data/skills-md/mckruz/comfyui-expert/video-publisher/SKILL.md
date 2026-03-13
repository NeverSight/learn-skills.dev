---
name: video-publisher
description: Publish assembled videos to YouTube and other platforms. Orchestrates existing youtube-uploader, youtube-strategy, and youtube-plan-new-video skills. Use when ready to publish or plan distribution for completed videos.
user-invocable: true
metadata: {"openclaw":{"emoji":"📤","os":["darwin","linux","win32"]}}
---

# Video Publisher

Thin orchestrator that routes publishing tasks to existing specialized skills.

## Publishing Workflow

```
PUBLISH REQUEST
    |
    |-- Need to plan content first?
    |   |-- youtube-research-video-topic → Research competitors and gaps
    |   |-- youtube-plan-new-video → Generate title, thumbnail, hook
    |   |-- youtube-strategy → Optimize for discovery
    |
    |-- Ready to upload?
    |   |-- Verify video file is ready (video-assembly checklist passed)
    |   |-- Generate metadata (title, description, tags)
    |   |-- youtube-uploader → Upload with metadata
    |
    |-- Post-publish?
    |   |-- youtube-studio → Monitor analytics
    |   |-- Track performance for future optimization
```

## Skill Delegation

### Content Planning

| Task | Delegate To | Input |
|------|-------------|-------|
| Research topic viability | `youtube-research-video-topic` | Topic/niche |
| Plan title + thumbnail + hook | `youtube-plan-new-video` | Research results |
| Optimize for YouTube algorithm | `youtube-strategy` | Content plan |

### Upload

| Task | Delegate To | Input |
|------|-------------|-------|
| Upload video file | `youtube-uploader` | Video file + metadata |
| Manage channel | `youtube-studio` | Channel operations |

### Analytics

| Task | Delegate To | Input |
|------|-------------|-------|
| View performance | `youtube-studio` | Video/channel ID |
| Analyze for improvements | `youtube-video-analyst` | Video URL |

## Metadata Generation

When preparing to publish, generate:

### Title
- Use `youtube-title` skill for optimization
- Keep under 60 characters
- Include primary keyword
- Create curiosity gap

### Description
```
{Hook paragraph - what viewer will learn/see}

{Detailed description with timestamps}

{Links to resources mentioned}

{Social links and subscribe CTA}

---
Tags: {comma-separated relevant tags}
```

### Tags
- Primary topic keyword
- Related keywords
- Tool/software names (ComfyUI, Stable Diffusion, etc.)
- Technique names
- "AI video generation", "AI art tutorial", etc.

### Thumbnail
- Use `youtube-thumbnail` skill (via youtube-plan-new-video)
- Character close-up or dramatic before/after
- Bold text overlay (3-5 words max)
- High contrast, readable at small size

## Platform-Specific Settings

### YouTube

| Setting | Recommended |
|---------|-------------|
| Resolution | 1920x1080 or 3840x2160 |
| Format | MP4 (H.264) |
| Frame rate | 24, 30, or 60 fps |
| Audio | AAC, 192kbps+ |
| Aspect ratio | 16:9 |
| Max file size | 256GB (12 hours) |

### YouTube Shorts

| Setting | Recommended |
|---------|-------------|
| Resolution | 1080x1920 (9:16) |
| Duration | 15-60 seconds |
| Format | MP4 (H.264) |

### Instagram Reels

| Setting | Recommended |
|---------|-------------|
| Resolution | 1080x1920 (9:16) |
| Duration | 15-90 seconds |
| Format | MP4 (H.264) |

### TikTok

| Setting | Recommended |
|---------|-------------|
| Resolution | 1080x1920 (9:16) |
| Duration | 15-180 seconds |
| Format | MP4 (H.264) |

## Pre-Publish Checklist

- [ ] Video passes quality check (video-assembly checklist)
- [ ] Title optimized for search + curiosity
- [ ] Description includes timestamps and links
- [ ] Tags are relevant and comprehensive
- [ ] Thumbnail is compelling and readable at small size
- [ ] Category and audience settings are correct
- [ ] Schedule time is optimal (check youtube-strategy)
- [ ] End screen and cards planned
- [ ] Subtitles/CC file ready (if applicable)

## Integration

This skill is the final step in the VideoAgent pipeline:
```
Research → Plan → Generate → Assemble → Publish
```

It bridges the ComfyUI production pipeline with the YouTube publishing pipeline.
