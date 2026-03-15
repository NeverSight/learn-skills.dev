---
name: video-generator
description: Generate AI videos using Google VEO 3.1 or OpenAI Sora. Two providers for different strengths - VEO for native audio, Sora for visual quality and longer clips.
tier: full-setup
setup_time: 15-20 min
requires: Gemini API key and/or OpenAI API key
---

# Video Generator

Generate professional short-form videos using Google VEO 3.1 (with native audio) or OpenAI Sora (high visual quality, up to 12s).

## Prerequisites & Setup

### API Keys

You need at least one. Both gives you maximum flexibility.

**VEO (Google):**
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

```bash
export GEMINI_API_KEY=your_gemini_key_here
```

**Sora (OpenAI):**
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the generated key

```bash
export OPENAI_API_KEY=your_openai_key_here
```

### Install Dependencies

```bash
pip install google-genai requests
```

### Available Models

| Provider | Model | CLI `--model` | Best For |
|----------|-------|---------------|----------|
| **VEO** | Veo 3.1 Standard | `standard` (default) | Quality, audio fidelity, final assets |
| **VEO** | Veo 3.1 Fast | `fast` | Drafts, iteration, quick previews |
| **Sora** | Sora 2 | `sora-2` (default) | Visual quality, creative motion |
| **Sora** | Sora 2 Pro | `sora-2-pro` | Highest Sora quality, slower |

### When to Use Which

| Need | Use |
|------|-----|
| Native synchronized audio (dialogue, SFX) | **VEO** - Sora has no audio |
| Longer clips (12 seconds) | **Sora** - VEO maxes at 8s |
| Higher visual fidelity / artistic styles | **Sora** - stronger on visual aesthetics |
| Fast iteration / drafts | **VEO Fast** - quickest turnaround |
| 4K resolution | **VEO** - Sora uses fixed sizes |
| Negative prompts (exclude elements) | **VEO** - Sora doesn't support them |

### Video Parameters

| Parameter | VEO Options | Sora Options | Default |
|-----------|-------------|--------------|---------|
| **Duration** | 4, 6, or 8 seconds | 4, 8, or 12 seconds | 8s |
| **Resolution** | 720p, 1080p, 4K | Fixed (from aspect ratio) | 720p |
| **Aspect Ratio** | 16:9, 9:16 | 16:9 -> 1280x720, 9:16 -> 720x1280 | 16:9 |
| **Count** | 1-4 variations | 1-4 variations | 1 |
| **Negative Prompt** | Supported | Not supported (ignored) | none |

### Approximate Cost

| Provider | Model | Cost |
|----------|-------|------|
| VEO | Standard | ~$0.025-0.05 per video |
| VEO | Fast | ~$0.01-0.025 per video |
| Sora | sora-2 | ~$0.10 per second of video |
| Sora | sora-2-pro | ~$0.20 per second of video |

### Latency

Video generation is async - expect 11 seconds to 6 minutes depending on server load and provider. The script polls automatically and saves when ready.

---

## Workflow Overview

1. **Define the Concept** - What story does the video tell in 4-12 seconds?
2. **Storyboard the Shot** - Camera, motion, subject, environment
3. **Add Audio Direction** - Dialogue, sound effects, ambient sound (VEO only)
4. **Generate Video** - Run via API
5. **Iterate** - Adjust prompt based on results

## Prompt Rules

1. **150-300 characters is the sweet spot.** Under 100 = generic. Over 400 = the model drops elements unpredictably.
2. **One shot = one action.** Don't pack multiple scene changes or style shifts into one prompt. One camera move + one subject action.
3. **Describe what you want, not what you don't want.** Use the `--negative` flag for exclusions (VEO only), not the main prompt.
4. **Treat audio as a separate layer.** Write audio cues in their own sentences, not mixed into visual descriptions. (VEO only - Sora has no audio.)
5. **Use colon syntax for dialogue.** `A man says: "Hello!"` prevents subtitle artifacts. (VEO only.)
6. **Keep dialogue under 7 words per line.** Longer speech causes lip-sync drift. (VEO only.)
7. **Start simple, then layer.** Begin with a basic prompt, evaluate, then add one variable at a time.
8. **Slow camera movements win.** Fast pans and spins break output. Use tight framing for perceived speed.

---

## Storyboarding the Shot

Structure your prompt with cinematic language. Both VEO and Sora respond well to film terminology:

### Camera Language

| Term | Effect |
|------|--------|
| **Wide shot** | Shows full environment, establishes context |
| **Close-up** | Tight on a subject, emphasizes detail |
| **Tracking shot** | Camera follows subject movement |
| **Dolly in/out** | Camera moves toward or away from subject |
| **Static shot** | Locked camera, subject moves within frame |
| **Slow pan** | Camera rotates horizontally across scene |
| **Overhead / bird's eye** | Looking straight down |
| **Low angle** | Looking up at subject, adds drama |

### Motion Description

Be explicit about what moves and how:

| Don't | Do |
|-------|-----|
| "A dog in a park" | "A golden retriever runs toward camera through tall grass, ears bouncing" |
| "City at night" | "Camera slowly dollies through a neon-lit Tokyo alley as rain puddles reflect signs" |
| "Ocean" | "A single wave forms, curls, and crashes onto wet sand in slow motion" |

### Lighting & Atmosphere

| Term | Mood |
|------|------|
| Golden hour | Warm, nostalgic, cinematic |
| Overcast | Soft, even, contemplative |
| Neon / artificial | Urban, energetic, modern |
| Candlelight | Intimate, quiet |
| Hard shadows | Dramatic, high contrast |

---

## Audio Direction (VEO Only)

VEO 3.1 generates synchronized audio natively. This is a major differentiator.

### Three Types of Audio Cues

**1. Dialogue** - Use colon syntax before quotes:
```
A barista says: "Here you go!" as she slides a latte across the counter.
```
Keep lines under 7 words for clean lip-sync. One sentence max per 8-second clip.

**2. Sound Effects** - Describe specific sounds:
```
The sound of a match striking, then a candle flame flickering to life.
```

**3. Ambient Sound** - Set the sonic environment:
```
Birds chirping in the background, distant traffic hum, morning atmosphere.
```

---

## Prompt Structure (5-Element Priority)

Structure prompts in this order - you don't need all five every time:

1. **Shot Specification** - camera work, framing, movement
2. **Setting & Atmosphere** - location, time, weather, lighting
3. **Subject & Action** - who/what, described in beats
4. **Audio Layer** - dialogue, SFX, ambient (VEO only)
5. **Style/Grade** - artistic treatment, lens, color

```
[Shot type + camera movement]. [Setting and lighting]. [Subject doing action].
[Audio: what you hear]. [Style/grade].
```

### Example Prompts

**Podcast promo (VEO, 16:9):**
```
A close-up tracking shot of a vintage microphone in a warmly lit podcast studio.
Steam rises slowly from a coffee mug beside it. Morning sunlight filters through
blinds, casting soft stripes across the desk. The sound of a quiet room - a clock
ticking, the faint hum of equipment. Cinematic, intimate, inviting.
```

**Social teaser - vertical (Sora, 9:16):**
```
A hand reaches into frame and opens a leather-bound journal on a wooden desk.
The pages flutter briefly before settling on a page covered in handwritten notes.
A pen is set down beside the book. Warm overhead lighting, shallow depth of field.
Shot on 16mm film, natural grain.
```

**Product reveal (either provider, 16:9):**
```
Camera slowly orbits a pair of wireless headphones placed on a dark marble surface.
Dramatic studio lighting with a single warm key light from the left. The headphones
cast a sharp shadow. Premium, minimal, modern.
```

---

## Running the Script

```bash
# VEO: Basic generation (8s, 720p, 16:9)
python scripts/generate_video.py "Your prompt here"

# VEO: Fast draft for iteration
python scripts/generate_video.py "Your prompt here" --model fast

# VEO: High quality vertical video for social
python scripts/generate_video.py "Your prompt" --aspect 9:16 --resolution 1080p

# VEO: Multiple variations to choose from
python scripts/generate_video.py "Your prompt" --count 2 --output ./videos

# VEO: Short clip with specific settings
python scripts/generate_video.py "Your prompt" --duration 4 --resolution 4k --name "hero-clip"

# VEO: Exclude unwanted elements
python scripts/generate_video.py "Your prompt" --negative "text overlays, watermarks, blurry"

# Sora: Basic generation
python scripts/generate_video.py "A cat on a windowsill, warm light" --provider sora

# Sora: 12-second clip (longer than VEO allows)
python scripts/generate_video.py "A dog running through a meadow" --provider sora --duration 12

# Sora: Pro model, vertical
python scripts/generate_video.py "Latte art being poured" --provider sora --model sora-2-pro --aspect 9:16

# Sora: Multiple variations
python scripts/generate_video.py "Ocean waves at sunset" --provider sora --count 2 --output ./videos
```

**Options:**

| Flag | Values | Default | Notes |
|------|--------|---------|-------|
| `--provider` | `veo`, `sora` | `veo` | VEO for audio, Sora for visual quality |
| `--model` | VEO: `standard`, `fast` / Sora: `sora-2`, `sora-2-pro` | `standard` / `sora-2` | Provider-specific models |
| `--aspect` | `16:9`, `9:16` | `16:9` | Vertical for Reels/TikTok/Shorts |
| `--resolution` | `720p`, `1080p`, `4k` | `720p` | VEO only (ignored by Sora) |
| `--duration` | VEO: `4`, `6`, `8` / Sora: `4`, `8`, `12` | `8` | Sora supports 12s |
| `--negative` | text | none | VEO only (ignored by Sora) |
| `--count` | `1`-`4` | `1` | Generate variations |
| `--output` | path | `.` | Save directory |
| `--name` | text | none | Filename prefix |

**Output:** MP4 files with timestamp-based filenames.

---

## Iteration Strategy

1. Start with `--model fast` (VEO) or `--duration 4` (Sora) for quick drafts
2. Refine the prompt through 2-3 fast iterations
3. Switch to full quality/duration for the final take
4. Generate 2 variations of the final prompt and pick the best

After reviewing generated video:

- **Motion wrong?** Be more explicit about direction, speed, and sequence
- **Audio off?** (VEO) Add or refine audio cues
- **Too much happening?** Simplify. One clear action per clip works best
- **Style drift?** Add a negative prompt (VEO) or adjust style descriptors
- **Wrong mood?** Adjust lighting and atmosphere descriptors

---

## Negative Prompt Guide (VEO Only)

Use `--negative` to steer away from common problems:

| Problem | Negative Prompt |
|---------|-----------------|
| Text/watermarks appearing | "text, watermarks, logos, subtitles" |
| Uncanny faces | "distorted faces, morphing features" |
| Jittery motion | "jerky motion, flickering, stuttering" |
| Over-saturated look | "oversaturated, HDR, neon colors" |
| Stock footage feel | "generic, corporate, stock footage aesthetic" |

---

## Prompting Principles

### Think in Shots, Not Scenes

8 seconds is one shot. Don't try to cram a narrative arc - describe a single continuous moment.

| Don't | Do |
|-------|-----|
| "A chef makes a meal from scratch and serves it" | "A chef's hands julienne carrots on a wooden cutting board, knife moving rhythmically" |
| "A day at the beach from sunrise to sunset" | "Waves gently lap at bare feet on sand, golden hour light, camera at ground level" |

### Be Specific About Motion

Vague motion descriptions produce vague results. Describe *what moves*, *how fast*, and *in which direction*.

### Layer Your Audio (VEO)

Don't just describe one sound - create a soundscape:
```
The crackling of a vinyl record playing soft jazz,
a distant car horn outside the window,
the quiet clink of an ice cube in a glass.
```

### Use Negative Prompts Proactively (VEO)

Always include `--negative "text, watermarks"` at minimum. The model occasionally generates unwanted text overlays.

---

## Use Cases

### Social Media (9:16, 4-8s)

Short, punchy, loop-friendly. Favor close-ups and strong motion.

```bash
# VEO with audio
python scripts/generate_video.py "Close-up of coffee being poured into a ceramic mug, steam rising, warm morning light. The sound of liquid pouring and a soft sigh." \
  --aspect 9:16 --duration 4 --resolution 1080p

# Sora for visual quality
python scripts/generate_video.py "Close-up of coffee being poured into a ceramic mug, steam rising, warm morning light. Photorealistic, shallow depth of field." \
  --provider sora --aspect 9:16 --duration 4
```

### Podcast/Newsletter Headers (16:9, 8s)

Ambient, atmospheric. Favor wide shots and subtle motion.

```bash
python scripts/generate_video.py "A vintage radio on a wooden shelf, dial slowly turning. Warm tungsten light. Soft static transitioning into faint music." \
  --resolution 1080p --name "podcast-header"
```

### Product/Brand (16:9, 6-8s)

Clean, controlled, premium feel. Studio lighting, slow orbits.

```bash
python scripts/generate_video.py "Camera slowly orbits a leather notebook on a dark wood desk. Single warm key light. The sound of pages turning gently." \
  --resolution 4k --duration 6 --negative "text, watermarks, busy background"
```

### Extended Clips (Sora, 12s)

For content that needs more breathing room.

```bash
python scripts/generate_video.py "A woman walks through an autumn forest path, leaves falling around her. Golden hour light filters through the canopy. Cinematic, contemplative." \
  --provider sora --duration 12 --name "autumn-walk"
```

---

## Multi-Clip Consistency

When generating multiple clips for a project:

### Lock Your Constants

Create a consistency block and repeat it verbatim across all prompts:

```
CHARACTER: A woman in her thirties with short silver hair and a black turtleneck
PALETTE: amber, cream, walnut brown, deep olive
LIGHTING: Soft key light from camera right, warm tungsten
STYLE: Cinematic, shallow depth of field, warm film grain
NEGATIVE: no subtitles, no on-screen text, no watermarks
```

### Consistency Checklist

- [ ] Same character description, word for word
- [ ] Same palette anchors (3-5 named colors)
- [ ] Same lighting direction and quality
- [ ] Same aspect ratio and resolution
- [ ] Same style/grade language
- [ ] Same provider for all clips in a sequence
