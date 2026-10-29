---
name: Influencer
slug: influencer
version: 1.0.0
description: Create, manage, and scale AI-generated virtual influencers with consistent characters, multi-platform content, and monetization workflows.
homepage: https://clawic.com/skills/influencer
metadata:
  clawdbot:
    emoji: ⭐
    displayName: Influencer
---

## Workspace Structure

Each influencer lives in a dedicated folder:
```
~/influencers/
├── {persona-slug}/
│   ├── identity.md        # Name, niche, voice, personality
│   ├── reference/         # Base images for consistency
│   │   ├── face-ref-1.png
│   │   └── style-guide.md
│   ├── content/
│   │   ├── photos/        # Generated images by date
│   │   └── videos/        # Generated videos by date
│   ├── captions.md        # Caption templates, hashtags
│   ├── schedule.md        # Posting schedule
│   └── analytics.md       # Performance tracking
└── tools.md               # Configured generation tools
```

---

## Quick Reference

| Task | Load |
|------|------|
| Create new persona (identity, niche, aesthetics) | `persona.md` |
| Generate consistent photos | `image-gen.md` |
| Generate videos (talking head, lifestyle) | `video-gen.md` |
| Voice and audio (TTS, voice cloning) | `voice.md` |
| Content strategy and captions | `content.md` |
| Platform optimization (IG, TikTok, YT) | `platforms.md` |
| Monetization (brand deals, affiliates) | `monetization.md` |
| Legal and disclosure requirements | `compliance.md` |

---

## Persona Creation Checklist

Before generating any content:
- [ ] Define niche (fitness, lifestyle, tech, fashion, etc.)
- [ ] Create identity document (name, age, location, backstory)
- [ ] Generate 5-10 reference images for face consistency
- [ ] Define visual style (lighting, colors, settings)
- [ ] Create voice profile (if using TTS/videos)
- [ ] Draft personality guidelines for captions

---

## Character Consistency Rules

Maintaining the same face/body across all content is CRITICAL.

**For photos:**
1. Generate base reference set first (5-10 images, multiple angles)
2. Use IP-Adapter or InstantID for every generation
3. Same seed + similar prompt structure = more consistency
4. Quality check EVERY image before posting

**For videos:**
1. Use face-swap on real footage OR
2. Generate with character LoRA if trained OR
3. Talking head tools (HeyGen, D-ID) with reference image

---

## Content Generation Flow

1. **Plan** — Check schedule.md for what's needed today
2. **Generate** — Use appropriate tool (see image-gen.md or video-gen.md)
3. **Review** — Verify character consistency, quality
4. **Caption** — Write engaging copy matching persona voice
5. **Schedule** — Queue for optimal posting time
6. **Track** — Log in analytics.md after posting

---

## Common Patterns

| User says | Agent does |
|-----------|------------|
| "Create new influencer" | Run persona creation flow, set up workspace |
| "Generate photos for today" | Check schedule, generate with consistency refs |
| "Make a TikTok video" | Generate 9:16 video with talking head or lifestyle footage |
| "Write captions for these" | Draft captions matching persona voice + niche hashtags |
| "How is she performing?" | Summarize analytics.md, suggest improvements |
| "Add brand deal content" | Generate sponsored content with disclosure |

---

## Tool Configuration

Store active tools in `~/influencers/tools.md`:

```markdown
## Active Tools
- Image: Nano Banana Pro (Gemini)
- Video: Kling / Runway
- Voice: ElevenLabs (voice_id: xxx)
- Lip Sync: HeyGen
```

Update when switching providers. All generation scripts read from here.
