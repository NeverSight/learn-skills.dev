---
name: image-to-video
description: Generate AI video from static images using Kling 3.0, Hailuo, Luma Ray3, Runway Gen-4.5, and 8 other tools. Covers free vs paid tools, prompt writing (motion-only), camera control, and face stability. Use when user asks to animate an image, create AI video, or convert photo to video.
---

# Image-to-Video AI Generation — Skill Reference

> **Version:** 1.0.0 | **Updated:** 2026-03-02 | **Category:** Content & Video

---

## Table of Contents

1. [Tool Comparison Matrix](#1-tool-comparison-matrix)
2. [Detailed Tool Profiles](#2-detailed-tool-profiles)
3. [Universal Prompt Best Practices](#3-universal-prompt-best-practices)
4. [Camera Movement Reference](#4-camera-movement-reference)
5. [Subject Animation Guide](#5-subject-animation-guide)
6. [Consistency & Stability](#6-consistency--stability)
7. [Avoiding Distortion & Common Mistakes](#7-avoiding-distortion--common-mistakes)
8. [Text & Logo Preservation](#8-text--logo-preservation)
9. [Thumbnail-to-Video Specific Guide](#9-thumbnail-to-video-specific-guide)
10. [Prompt Templates](#10-prompt-templates)

---

## 1. Tool Comparison Matrix

| Tool | Best Model (Mar 2026) | Max Length | I2V | Free Tier | Max Resolution | Native Audio | Best For |
|------|----------------------|------------|-----|-----------|----------------|-------------|----------|
| **Runway** | Gen-4.5 | 10s | Yes | 125 one-time credits (~25s Gen-4 Turbo) | 4K (upscale) | No | Cinematic consistency, character ref |
| **Kling** | Kling 3.0 / 2.6 Pro | 15s (3.0) / 10s (2.6) | Yes | 66 daily credits (360-540p, watermark) | 1080p (Master) | Yes (2.6+) | Motion control, product detail, fashion |
| **Pika** | Pika 2.5 | 10s | Yes | 80 monthly credits (480p, watermark) | 1080p+ (paid) | No | Creative effects (Pikaswaps, Pikadditions) |
| **Luma** | Ray3 / Ray3 Modify | 20s (720p+) | Yes | 30 gens/month (draft res, watermark) | 1080p | No | Long clips, start+end frame, cinematic |
| **Sora** | Sora 2 / Sora 2 Pro | 25s | Yes | None (Plus $20/mo minimum) | 1080p (Pro: 1792x1024) | Yes | Narrative scenes, physics, dialogue |
| **Vidu** | Vidu Q3 | 16s | Yes | 3 videos/month (720p, watermark) | 4K (Q3 Pro) | Yes (native) | Multi-shot sequences, synced audio |
| **Hailuo/MiniMax** | Hailuo 2.3 | 10s | Yes | Daily bonus credits (720p, watermark) | 1080p (paid) | Yes (2.6+) | Speed, social content, A/B testing |
| **Google Veo** | Veo 3.1 | 8s | Yes (Ingredients) | Limited (Gemini free: older model) | 4K (3840x2160) | Yes | 4K output, film language, camera control |
| **Adobe Firefly** | Firefly Video | 5s | Yes | Limited credits (with CC sub) | 2K native (up to 8K upscale) | No | Commercial-safe (IP indemnity), integration with CC |
| **Seedance** | Seedance 2.0 (ByteDance) | 15s | Yes | Free credits on signup | 1080p | Yes (native) | Multimodal input, fast generation |
| **WAN** | WAN 2.6 / 2.1 | 10s | Yes | Open source (run locally) | 1080p | No | Open source, self-hosted, general-purpose |

---

## 2. Detailed Tool Profiles

### Runway (Gen-4 / Gen-4.5)

**Current Models:**
- **Gen-4.5** (latest, Jan 2026): State-of-the-art motion quality, prompt adherence, visual fidelity. Variable durations 2-10s.
- **Gen-4 Turbo**: Fast, economical (5 credits/sec vs Gen-4.5 at 25 credits/sec). Good for iteration.
- **Gen-4**: Mid-tier (12 credits/sec). Balanced quality/cost.

**Image-to-Video Specifics:**
- Upload a reference image + text prompt describing motion
- Choose duration (5 or 10 seconds) and aspect ratio
- Enable "Fixed Seed" for reproducible motion
- Reference images maintain character appearance, clothing, features across scenes
- Strong spatial understanding — objects/backgrounds stay coherent during camera movement

**Pricing:**
- Free: 125 one-time credits (~25s of Gen-4 Turbo, ~5s of Gen-4.5)
- Standard: $12-15/mo (625 credits)
- Pro: $28-35/mo (2,250 credits)
- Unlimited: $76-95/mo (2,250 fast + unlimited relaxed)

**Prompt Best Practices (Runway-Specific):**
- Focus prompts EXCLUSIVELY on motion — do NOT re-describe what is in the image
- Start simple, iterate by adding detail
- Use camera terms: pan, tilt, dolly, orbit, zoom, truck, pedestal, crane, rack focus, crash zoom
- Structure: "The camera [motion] as [subject action]"
- Abstract/conceptual language causes unpredictable results — be specific and physical
- Re-describing image elements in detail can reduce motion or cause artifacts

**Sources:** [Runway Pricing](https://runwayml.com/pricing) | [Gen-4 Research](https://runwayml.com/research/introducing-runway-gen-4) | [Gen-4.5 Research](https://runwayml.com/research/introducing-runway-gen-4.5)

---

### Kling AI (Kling 3.0 / 2.6 Pro)

**Current Models:**
- **Kling 3.0** (latest): Scene-aware generation, character/prop consistency, native audio, 3-15s clips
- **Kling 2.6 Pro**: Built-in English and Chinese audio, stronger prompt control, cinematic realism
- **Kling 2.6 Motion Control**: Upload a motion reference video to guide character movement
- Variants: Turbo (fast), Pro (balanced), Master (highest quality)

**Image-to-Video Specifics:**
- Upload image as subject + describe movement in prompt
- Motion Control mode: image + reference video for precise motion transfer
- Preserves edges, logos, and fabric details (great for product/fashion)

**Pricing:**
- Free: 66 daily credits (resets every 24h, no rollover). 360-540p, watermarked, non-commercial
- Paid plans: $6.99-180/mo depending on tier

**Prompt Best Practices (Kling-Specific):**
- For I2V: describe ONLY what should move/change + camera behavior. The image IS the scene.
- Keep ONE main action ("hero action"). Hint at secondary motion only.
- For Motion Control: do NOT describe motion in prompt (the reference video defines it). Use prompt for environment/look only.
- Use terms like "slow push-in", "drone follow", "lateral track"
- Describe pace with words like "glides smoothly" or "jerks to a halt"
- Ensure character limbs are visible in source image (hidden limbs cause hallucination/extra fingers)
- Leave "breathing room" around subject for movement
- Match aspect ratios between image and motion reference

**Sources:** [Kling AI](https://klingai.com/global/) | [Kling 3.0 Guide](https://invideo.io/blog/kling-3-0-complete-guide/) | [Kling 2.6 Motion Control](https://fal.ai/learn/devs/kling-video-2-6-motion-control-prompt-guide)

---

### Pika Labs (Pika 2.5)

**Current Models:**
- **Pika 2.5** (latest): Sharper, smoother cinematic clips. Upgraded engine.
- **Pikaformance**: Talking face model for lifelike voice-to-face performances
- **AI Selves**: Personalized AI avatar creation

**Key Features:**
- **Pikaframes**: Turn 2-5 images into smooth transition video with realistic movement
- **Pikaswaps**: Replace objects in video (e.g., dog -> robot) with preserved lighting/motion
- **Pikadditions**: Insert new characters/objects into footage
- Scene Ingredients: Upload your own characters/objects for consistency

**Pricing:**
- Free: 80 monthly credits. 480p only, watermarked, non-commercial
- Paid: Unlocks all resolutions, removes watermark, commercial use

**Prompt Best Practices (Pika-Specific):**
- Great for creative/stylized transformations rather than photorealistic
- Use Pikaframes for multi-image storytelling
- Specify lighting and physics behavior for realistic material interactions
- Best for short creative social clips and effects-heavy content

**Sources:** [Pika Pricing](https://pika.art/pricing) | [Pika 2.5 Release](https://pikartai.com/pika-2-5/)

---

### Luma Dream Machine (Ray3)

**Current Models:**
- **Ray3**: Primary generation model. Supports 5-20s video depending on resolution.
- **Ray3 Modify**: Modify existing footage with character reference images
- **Ray3.14**: Draft resolution model (available on free tier)

**Image-to-Video Specifics:**
- Upload still image, animate with natural motion and cinematic camera action
- Start+End frame feature: provide first and last frame, AI generates the transition
- Adds subtle camera pans, zooms, perspective shifts automatically

**Pricing:**
- Free: $0/mo. 30 gens/month. Draft resolution (Ray3.14), 720p images, watermarked, personal only
- Lite: $9.99/mo. 3,200 credits. 1080p images, watermarked, non-commercial
- Plus: $29.99/mo. 10,000 credits. No watermark, commercial rights
- Unlimited: $94.99/mo. 10,000 fast + unlimited relaxed

**Video Duration by Resolution:**
- 540p SDR: 5s (160 credits), 10s (320 credits)
- 720p SDR: 5-20s
- 1080p SDR: up to 20s

**Sources:** [Luma Pricing](https://lumalabs.ai/pricing) | [Dream Machine](https://lumalabs.ai/dream-machine) | [Ray3 Info](https://lumalabs.ai/ray)

---

### OpenAI Sora (Sora 2)

**Current Models:**
- **Sora 2**: Text-to-video and image-to-video with synchronized audio
- **Sora 2 Pro**: Higher resolution (1792x1024) and better quality

**Image-to-Video Specifics:**
- Start with a still image and expand it into motion
- Physically accurate, realistic, controllable
- Can insert people into any Sora-generated environment with accurate appearance and voice
- Native dialogue and sound effects generation

**Pricing:**
- NO free tier (as of Jan 10, 2026)
- ChatGPT Plus ($20/mo): Unlimited 480p video generation
- ChatGPT Pro ($200/mo): Higher quality, priority access
- API: $0.10/sec (720p), $0.30/sec (720p Pro), $0.50/sec (1024p Pro)

**Prompt Best Practices (Sora-Specific):**
- Rewards prompts describing INTENT and MOOD, not just motion
- Use director-style framing and gradual motion introduction
- Structure prompts in distinct sections: what happens, visual style, audio elements
- Be explicit about sound (dialogue, foley, music, mood)
- Specify character positioning, framing, emotional states, gestures
- Describe physics: "gentle collision" vs "violent crash", "heavy object slides" vs "light feather floats"
- Support 15-25 second clips. Describe pacing progression.
- Specify 24fps for cinematic feel

**Sources:** [Sora 2 Guide](https://wavespeed.ai/blog/posts/openai-sora-2-complete-guide-2026/) | [Sora Announcement](https://openai.com/index/sora-2/)

---

### Vidu (Vidu Q3)

**Current Models:**
- **Vidu Q3** (latest): Native audio+video in one pass, up to 16s, 2K resolution, multi-shot "Smart Cuts"
- **Vidu Q2**: Previous gen. Natural motion, film-like camera effects.
- **Reference-to-Video 2.0**: Character/subject consistency across generations

**Key Features:**
- First AI model to generate multi-shot, edited-style sequences with synced audio from a single prompt
- "Smart Cuts" for automatic multi-shot sequences
- Audio: BGM + SFX synced to scene rhythm
- Up to 4K in Q3 Pro via API

**Pricing:**
- Free: 3 videos/month. 720p, watermarked
- Paid plans available on vidu.com

**Sources:** [Vidu](https://www.vidu.com/) | [Vidu Q3 Guide](https://www.nemovideo.com/blog/what-is-vidu-q3) | [Vidu Q3 on WaveSpeed](https://wavespeed.ai/blog/posts/introducing-vidu-q3-image-to-video-pro-on-wavespeedai/)

---

### Hailuo / MiniMax (Hailuo 2.3)

**Current Models:**
- **Hailuo 2.3** (latest): Improved physical actions, stylization, character micro-expressions, anime support
- **Hailuo 02**: Standard and Fast variants. 768p and 1080p, up to 10s
- **Media Agent**: Multi-modal creation with minimal manual editing

**Pricing:**
- Free: $0/mo. Daily bonus credits. 720p, watermarked. Peak-hour wait times.
- Standard: $9.99/mo. 1,000 credits, fast-track, no watermark, up to 5 tasks
- Unlimited: $94.99/mo. Unlimited credits

**Prompt Best Practices (Hailuo-Specific):**
- Works best with clean images and modest motion requests
- Great for rapid A/B testing and short-form social content
- Strong anime/stylized content support in 2.3

**Sources:** [Hailuo AI](https://hailuoai.video/) | [MiniMax Hailuo 2.3](https://www.minimax.io/news/minimax-hailuo-23)

---

### Google Veo (Veo 3.1)

**Current Models:**
- **Veo 3.1**: 4K output (3840x2160), vertical video (9:16), "Ingredients to Video" (up to 4 reference images)
- **Veo 3 Standard**: Older model available to some free users
- **Veo 3 Fast**: Lower-cost option

**Key Features:**
- FIRST mainstream AI model with true 4K output
- "Ingredients to Video": Accept up to 4 reference images per generation
- Character identity consistency across scene changes
- Native vertical video for YouTube Shorts / TikTok / Reels
- Built-in audio generation

**Pricing:**
- Free (Gemini): 100 monthly AI credits for Flow/Whisk. May get Veo 3 Standard (not 3.1)
- Pro ($19.99/mo): Limited Veo 3.1 access
- Ultra ($124.99/3mo or ~$42/mo): 25,000 monthly credits, full Veo 3.1
- API: Veo 2 at $0.35-0.50/sec

**Prompt Best Practices (Veo-Specific):**
- Excels with film language — reference shot types and pacing
- Separate subject stability from camera motion in prompts
- Input images should be 720p+ with 16:9 or 9:16 aspect ratio
- Prompts referencing specific shot types produce more controlled results

**Sources:** [Veo 3.1 4K Update](https://wavespeed.ai/blog/posts/google-veo-3-1-4k-update-brings-professional-grade-ai-video-generation/) | [Veo 3.1 Blog](https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/) | [Google DeepMind Veo](https://deepmind.google/models/veo/)

---

### Adobe Firefly Video

**Current Model:** Firefly Video (Feb 2026)

**Key Features:**
- 5s clips per generation
- Native 2K resolution (up to 8K with Upscale)
- **IP indemnity** — commercially safe, trained on licensed content
- QuickCut: Upload b-roll or generate footage, auto-create structured first cut
- Deep integration with Premiere Pro, After Effects, Creative Cloud

**Pricing:**
- Firefly Standard: $9.99/mo (2,000 premium credits). ~20 videos at 100 credits/5s clip
- Firefly Pro: $19.99/mo (4,000 premium credits)
- Firefly Premium: $199.99/mo (50,000 premium credits)
- Jan-Mar 2026 promo: Unlimited generations on paid plans

**Best For:** Enterprise/agency use where IP indemnity matters. Integration with existing Adobe workflows.

**Sources:** [Adobe Firefly Pricing](https://www.adobe.com/products/firefly/plans.html) | [Firefly Blog](https://blog.adobe.com/en/publish/2026/02/02/create-unlimited-generations-adobe-firefly-all-in-one-creative-ai-studio)

---

### Seedance 2.0 (ByteDance)

**Current Model:** Seedance 2.0

**Key Features:**
- Unified multimodal audio-video joint generation (text, image, audio, video inputs)
- 4-15s video length
- 1080p resolution
- 30% faster than Seedance 1.0
- Native audio generation (BGM + SFX)

**Pricing:**
- Free credits on signup (check-in daily for more)

**Sources:** [Seedance 2.0](https://seed.bytedance.com/en/seedance2_0) | [Seedance on fal.ai](https://fal.ai/seedance-2.0)

---

### WAN 2.6 / 2.1 (Open Source)

**Current Models:**
- **WAN 2.6**: Latest release
- **WAN 2.1**: Widely available, open-source on Hugging Face

**Key Features:**
- Open source — run locally, no credits needed
- 1.3B and 14B parameter variants
- Text AND image generation in video (Chinese + English)
- Realistic physics simulation
- Great general-purpose all-rounder

**Pricing:** Free (open source). Hardware costs only.

**Best For:** Self-hosted workflows, privacy-sensitive projects, unlimited generation without credits

**Sources:** [WAN GitHub](https://github.com/Wan-Video/Wan2.1) | [WAN on HuggingFace](https://huggingface.co/Wan-AI/Wan2.1-T2V-14B)

---

## 3. Universal Prompt Best Practices

### The Golden Rules

1. **Separate identity from motion.** The image defines WHO/WHAT. The prompt defines HOW it MOVES.
2. **Do NOT re-describe the image.** This causes reduced motion or visual artifacts.
3. **Start simple, iterate.** Begin with one action, one camera move. Add complexity after testing.
4. **Be physically specific, not conceptual.** "Camera slowly pushes in" > "dramatic emphasis"
5. **3-4 descriptive elements per component is the sweet spot.** More adjectives past this degrades quality.

### Prompt Structure Formula

```
[Camera movement], [pace/speed], [subject action], [environmental motion/details]
```

**Example:**
```
Slow push-in, steady cinematic pace, the developer's fingers type on the glowing keyboard,
holographic UI panels float and pulse with soft blue light around the workspace
```

### The 8-Point Shot Grammar (Advanced)

For consistent cinematic outputs, cover these 8 elements:

| Element | What to Specify | Example |
|---------|----------------|---------|
| 1. Subject | Who/what is the focus | "A developer at a desk" |
| 2. Emotion/Mood | Tone of the scene | "focused, intense concentration" |
| 3. Optics/Framing | Shot type and lens | "medium close-up, 35mm lens" |
| 4. Motion | Camera + subject movement | "slow dolly in, subtle typing motion" |
| 5. Lighting | Light source and quality | "cool monitor glow, purple ambient neon" |
| 6. Style | Visual aesthetic | "cinematic, dark moody, tech noir" |
| 7. Audio (if supported) | Sound design | "mechanical keyboard clicks, ambient hum" |
| 8. Continuity | What stays constant | "face remains still, same expression" |

---

## 4. Camera Movement Reference

### Movement Types with Prompt Keywords

| Movement | Description | Prompt Keywords | Best For |
|----------|------------|-----------------|----------|
| **Static/Locked** | Camera stays still, subject moves | "static shot", "locked camera", "fixed frame" | Subtle expressions, product focus |
| **Pan** | Horizontal swivel from fixed point | "pan left", "pan right", "slow pan", "sweeping pan" | Revealing landscapes, following action |
| **Tilt** | Vertical angle up/down from fixed point | "tilt up", "tilt down", "slow tilt", "dramatic tilt" | Height emphasis, outfit reveal |
| **Push-in/Dolly In** | Camera moves toward subject | "push in", "dolly in", "slow push-in", "intimate push" | Building tension, product detail |
| **Pull-back/Dolly Out** | Camera moves away from subject | "pull back", "dolly out", "reveal pull-back" | Context reveal, scene endings |
| **Truck** | Camera moves parallel to subject | "truck left", "truck right", "lateral movement" | Walking scenes, shelf scanning |
| **Pedestal** | Camera moves vertically (elevator-like) | "pedestal up", "pedestal down", "rising reveal" | Revealing hidden elements |
| **Tracking** | Camera follows moving subject | "tracking shot", "follow shot", "match pace" | Action sequences, character walk |
| **Orbit/Arc** | Camera circles around subject | "orbit clockwise", "orbit counterclockwise", "arc around", "slow orbit" | Hero shots, product showcase, dramatic |
| **Crane/Boom** | Sweeping vertical + horizontal move | "crane up", "crane shot", "boom up", "sweeping crane" | Epic establishing shots, crowd reveals |
| **Rack Focus** | Focus shifts between planes | "rack focus", "shift focus", "focus pull" | Attention redirection |
| **Crash Zoom** | Very fast dramatic zoom | "crash zoom", "snap zoom", "whip zoom" | Action beats, comedy, emphasis |
| **Zoom** | Lens zooms in/out (not physical move) | "zoom in", "zoom out", "slow zoom" | Drawing attention, reveal |
| **Handheld** | Slight natural shake | "handheld", "shaky cam", "documentary style" | Realism, urgency, immediacy |
| **FPV/First-Person** | Camera IS the subject | "FPV", "first person view", "POV shot" | Immersive, gaming content |

### Combining Movements

You can combine camera movements for complex shots:
```
"Slow dolly in while panning slightly right, the camera rises gently"
"Crane up and orbit counterclockwise, revealing the full workspace"
"Tracking shot following the subject with a slight handheld shake"
```

### Speed/Pace Modifiers

| Modifier | Effect | Keywords |
|----------|--------|----------|
| Very slow | Dreamy, contemplative | "very slow", "glacial pace", "barely moving" |
| Slow | Cinematic, elegant | "slow", "steady", "gentle", "smooth" |
| Medium | Natural, documentary | "natural pace", "moderate speed" |
| Fast | Energetic, dynamic | "fast", "dynamic", "brisk", "energetic" |
| Whip | Sudden, dramatic | "whip", "snap", "lightning fast", "sudden" |

---

## 5. Subject Animation Guide

### Subtle vs. Dramatic Motion Spectrum

| Level | Description | Keywords | Use Case |
|-------|------------|----------|----------|
| **Minimal** | Almost imperceptible | "barely perceptible movement", "very subtle", "still with micro-motion" | Thumbnails, portrait-style |
| **Subtle** | Natural idle motion | "gentle sway", "subtle breathing", "slight movement", "soft idle" | Professional headshots, calm scenes |
| **Moderate** | Clear but controlled | "natural movement", "smooth gesture", "controlled action" | Product demos, presentations |
| **Dynamic** | Active, energetic | "active movement", "energetic", "fluid motion" | Action scenes, sports |
| **Dramatic** | Maximum motion | "explosive motion", "dramatic action", "intense movement" | Music videos, trailers |

### Animating Specific Elements

**Hair/Clothing:**
```
"hair gently moves as if from a light breeze"
"coat fabric ripples softly"
"scarf billows in the wind"
```

**Eyes/Face (CAREFUL — most distortion-prone):**
```
"eyes blink naturally"
"subtle smile forms"
"gaze shifts to the right"
```
WARNING: Keep facial animation minimal to avoid distortion. "Natural blinking" and "subtle expression" are safest.

**Hands/Typing:**
```
"fingers move across keyboard with natural rhythm"
"hands gesture subtly while speaking"
"subtle finger movement on the trackpad"
```

**Environment/Background:**
```
"particles float gently in the air"
"screen content scrolls slowly"
"ambient light pulses softly"
"clouds drift across the sky"
```

---

## 6. Consistency & Stability

### Keeping the Subject Stable

1. **Identity locks in prompt:** "same face, same outfit, same hairstyle, consistent proportions"
2. **Fixed Seed** (Runway): Enable for reproducible motion across iterations
3. **Reference images** (Runway Gen-4+, Veo 3.1): Upload character reference for cross-scene consistency
4. **Minimize facial motion:** Faces drift the most. Keep face expressions subtle.
5. **Foreground priority:** Place main character in foreground, blur secondary faces
6. **One subject focus:** Multiple moving subjects = more drift. Focus on ONE.

### Maintaining Visual Coherence

- Use the SAME image for multi-clip generation (don't switch source images)
- Save and reuse exact style parameters across batches (colors, aesthetic, motion quality)
- Keep lighting description consistent: "cool blue monitor glow" in every prompt
- Specify what should NOT change: "the background remains static" or "the desk stays perfectly still"

### Cross-Scene Consistency

- **Runway Gen-4+**: Upload character reference image for appearance matching
- **Veo 3.1 Ingredients**: Up to 4 reference images per generation
- **Kling Motion Control**: Character image + motion reference video
- **Pika Scene Ingredients**: Upload characters/objects for consistency

---

## 7. Avoiding Distortion & Common Mistakes

### Top 10 Distortion Causes and Fixes

| Cause | Symptom | Fix |
|-------|---------|-----|
| Re-describing image content in prompt | Reduced motion, visual artifacts | Prompt should ONLY describe motion, not the scene |
| Too many actions at once | Chaotic, incoherent motion | ONE hero action + hint secondary motion |
| Abstract/conceptual language | Unpredictable results | Use specific physical descriptions |
| Hidden limbs in source image | Extra fingers, hallucinated hands | Ensure all limbs visible in source |
| Wide-angle lens in source | Perspective distortion during motion | Use neutral focal length (35-85mm framing) |
| Too many adjectives | Quality degradation | 3-4 descriptive elements per component max |
| Mismatched aspect ratios | Stretching, cropping artifacts | Match source image to output aspect ratio |
| Excessive facial animation | Face warping, identity drift | Keep face motion minimal ("subtle", "natural blink") |
| Low-resolution source image | Blurry, unstable output | Use 720p+ source images minimum |
| Contradictory instructions | Confused model output | Review prompt for conflicts |

### Negative Prompt Keywords (where supported)

Place critical exclusions first (models weight earlier terms more):
```
"blurry, low resolution, distorted, warped face, extra fingers, glitchy text,
unnatural movements, chaotic cuts, morphing features, flickering"
```

### Quality Safeguards

- **Source image quality matters most.** The cleaner the keyframe, the less the model invents.
- Generate the source image with a good image model first (FLUX, Seedream 4.5, Midjourney)
- Iterate ONE variable at a time when fixing issues (motion strength, camera move, style complexity)
- Use preview/draft resolution first, then upscale the winner

---

## 8. Text & Logo Preservation

### The Core Problem

AI video models struggle with text and logos. They frequently warp, blur, or morph text during motion. This is a fundamental limitation of current diffusion models.

### Mitigation Strategies

1. **Minimize motion near text areas:**
   ```
   "the text/logo remains perfectly stationary in the frame"
   "camera movement avoids the text area"
   "text stays sharp and readable throughout"
   ```

2. **Use static camera for text-heavy areas:**
   If text must be visible, keep the camera locked and animate only non-text elements.

3. **Specify high contrast text:**
   ```
   "bold high-contrast text", "clear sans-serif text", "readable block letters"
   ```

4. **Post-production approach (recommended for important text):**
   - Generate the video WITHOUT text
   - Overlay text/logos in video editing (Premiere, After Effects, CapCut)
   - This guarantees readability

5. **Kling 2.6 for logos:** Best at preserving edges and logos in product shots.

6. **Short duration helps:** Text stays more stable in 3-5s clips than 10s+.

---

## 9. Thumbnail-to-Video Specific Guide

### For Tech/Coding Thumbnails (Dark bg, neon, workspace, developer)

This section is specifically designed for thumbnails with: dark backgrounds, purple/teal neon lighting, desk/workspace scenes, MacBook/monitors, developer character, floating UI elements, holographic panels.

### Best Camera Movements for Desk/Workspace Scenes

**Recommended (in order of effectiveness):**

1. **Slow Push-In** (BEST for thumbnails):
   ```
   "Slow push-in toward the developer's workspace, steady cinematic pace,
   ambient particles float gently, monitor screens glow softly"
   ```
   Why: Creates focus, minimal distortion, keeps face stable.

2. **Subtle Orbit** (dramatic, good for hero shots):
   ```
   "Very slow orbit clockwise around the developer at the desk,
   neon reflections shift on the monitor surface, floating UI elements rotate gently"
   ```
   Why: Adds depth and drama without disrupting the subject.

3. **Static + Ambient Motion** (safest for face stability):
   ```
   "Static locked camera, the developer sits motionless at the desk,
   holographic panels pulse with soft light, particles drift upward,
   screen content scrolls slowly"
   ```
   Why: Zero face distortion. All motion is environmental.

4. **Gentle Pedestal Up** (reveal shot):
   ```
   "Slow pedestal up from the keyboard level, rising to reveal the developer's face
   and floating holographic displays, purple ambient light pulses"
   ```

5. **Dolly Back + Reveal**:
   ```
   "Slow dolly backward revealing the full workspace setup,
   multiple monitors glow, floating code snippets hover in the air"
   ```

### Animating Floating UI Elements

```
"Translucent holographic panels float around the workspace, slowly rotating and pulsing"
"Code snippets hover in mid-air with a soft cyan glow, gently bobbing up and down"
"Floating UI windows orbit the developer, each displaying different data visualizations"
"Semi-transparent screens drift slowly, reflecting purple and blue neon light"
"Holographic interface elements materialize one by one around the desk"
```

**Key descriptors for floating elements:**
- "translucent", "semi-transparent", "glassmorphic"
- "floating", "hovering", "drifting", "orbiting"
- "pulsing", "glowing", "flickering softly"
- "materializing", "fading in", "dissolving"

### Making Holographic Panels Glow/Pulse

```
"Holographic panels emit a soft pulsating blue-purple glow"
"Screens pulse rhythmically with cyan light, intensity rising and falling"
"Neon edges of the floating panels flicker with electric energy"
"Warm glow radiates from the holographic displays, casting colored light on the developer's face"
"Panels glow brighter momentarily before dimming back, creating a breathing light effect"
```

**Light behavior keywords:**
- "pulsating", "breathing light", "rhythmic glow"
- "flickering", "shimmering", "radiating"
- "casting colored light", "reflecting off surfaces"
- "intensity rising and falling", "soft oscillation"

### Adding Subtle Typing/Screen Activity

```
"Fingers move naturally across the backlit keyboard, screen content scrolls upward"
"Subtle typing motion, code appearing on the main monitor line by line"
"The MacBook screen displays scrolling code with a soft green-on-black terminal"
"Cursor blinks on the screen, new lines of code appear gradually"
"Multiple monitors show different live data — one scrolling code, one showing metrics"
```

### Keeping the Person's Face Stable with Ambient Motion

**This is the #1 challenge. Here is the priority order:**

1. **Face = STATIC, Everything else = MOVING:**
   ```
   "The developer sits perfectly still, face unchanged, steady gaze at the screen.
   Around him, holographic panels pulse with light, particles float upward,
   keyboard keys glow softly, ambient neon light shifts between purple and blue"
   ```

2. **Minimal face motion only:**
   ```
   "The developer blinks naturally, otherwise perfectly still.
   Ambient environment has floating particles, pulsing lights, and drifting UI elements"
   ```

3. **Identity locks:**
   Always include: "same face throughout, consistent facial features, no face morphing"

4. **Camera choice matters:**
   - Static camera = most stable face
   - Slow push-in = face stays stable (camera moves, not face)
   - Orbit = face can drift (use with caution)
   - Any motion toward/around face = highest risk

5. **Tool selection for face stability:**
   - **Best:** Kling (Motion Control with locked face), Luma (start+end frame)
   - **Good:** Runway Gen-4.5 (character reference), Veo 3.1 (identity consistency)
   - **Risky:** Sora (longer clips = more drift), Pika (creative focus, less stability)

---

## 10. Prompt Templates

### Template 1: Thumbnail-to-Video (Tech Workspace)

```
Slow push-in, smooth cinematic pace. A developer sits at a dark workspace,
face perfectly still with natural subtle blinking. Holographic UI panels float
around the desk, pulsing with soft [purple/blue/cyan] neon light. Particles
drift gently upward. The MacBook screen displays scrolling code. Ambient
lighting shifts subtly between [purple and teal]. The background remains
perfectly static while floating elements orbit slowly.
```

### Template 2: Product Showcase (Orbit)

```
Slow orbit clockwise around [product], smooth cinematic pace. The [product]
sits on a dark reflective surface. Ambient particles float in the air.
Soft studio lighting highlights edges and details. The background is
[dark/gradient]. Camera completes a quarter rotation over [5-10] seconds.
```

### Template 3: Hero Shot (Person)

```
Static locked camera, [duration] seconds. [Person description] stands/sits
in [environment]. Face remains perfectly still. Hair moves gently from a
subtle breeze. Atmospheric particles float in the background. Volumetric
light rays stream through [window/source]. The mood is [cinematic/dramatic/calm].
```

### Template 4: Code/Tech Demo

```
[Camera movement], steady pace. Close-up of a MacBook Pro screen showing
[code editor/terminal/dashboard]. Code scrolls upward naturally. The cursor
blinks. Ambient keyboard glow pulses softly. Shallow depth of field blurs
the background workspace. [Monitor reflections shift/bokeh lights drift].
```

### Template 5: Dramatic Reveal

```
Slow crane up from [starting point], sweeping reveal. Rising from [desk level/
ground level] to reveal [full scene/workspace/city]. Atmospheric fog drifts
through the scene. [Neon/ambient] lights illuminate the environment.
The scale of the scene becomes apparent as the camera rises.
```

---

## Schema

### Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| source_image | Image (720p+ recommended) | Yes | The still image to animate |
| prompt | String | Yes | Motion description (camera + subject + environment) |
| tool | Enum | Yes | Which AI tool to use |
| duration | Integer (3-25s) | No | Target video length |
| aspect_ratio | Enum (16:9, 9:16, 1:1, 4:3) | No | Output aspect ratio |
| resolution | Enum (480p-4K) | No | Output resolution (tool-dependent) |
| motion_reference | Video | No | Motion reference video (Kling Motion Control only) |

### Outputs

| Parameter | Type | Description |
|-----------|------|-------------|
| video | MP4 | Generated video file |
| duration | Integer | Actual video length in seconds |
| resolution | String | Output resolution |
| credits_used | Integer | Credits consumed |

### Composable With

| Skill | How |
|-------|-----|
| `thumbnail-generator` | Generate thumbnail image -> animate with this skill |
| `nano-banana-images` | Generate source image -> animate |
| `video-edit` | Post-process: trim, add text overlay, music |
| `pan-3d-transition` | Combine I2V clips with 3D transitions |
| `title-variants` | Generate titles -> overlay on video |
| `recreate-thumbnails` | Face-swap source image -> animate |

---

## Tool Selection Decision Tree

```
Need 4K output?
  -> Google Veo 3.1 or Vidu Q3 Pro

Need face stability (thumbnail/portrait)?
  -> Kling Motion Control (best) or Static camera on any tool

Need native audio?
  -> Sora 2, Vidu Q3, Seedance 2.0, Kling 2.6+, or Veo 3.1

Need free / no budget?
  -> Kling free (66 daily credits) or Hailuo free (daily bonus)
  -> WAN 2.1 (open source, run locally)

Need commercial IP safety?
  -> Adobe Firefly (IP indemnity)

Need creative effects (swaps, additions)?
  -> Pika 2.5 (Pikaswaps, Pikadditions, Pikaframes)

Need longest output?
  -> Sora 2 (25s) or Luma Ray3 (20s) or Vidu Q3 (16s)

Need product/fashion detail?
  -> Kling 2.6 Pro (preserves edges, logos, fabric)

Need fast iteration?
  -> Hailuo 2.3 (speed) or Runway Gen-4 Turbo (cheap credits)

Need multi-shot sequences?
  -> Vidu Q3 (Smart Cuts) or Veo 3.1 (Ingredients)

Need open source / self-hosted?
  -> WAN 2.1/2.6 (GitHub, HuggingFace)
```

---

## Quick Reference Card

### Top 5 Motion Keywords That Work Across All Tools

1. "slow push-in" / "dolly in"
2. "gentle orbit" / "arc around"
3. "static shot with ambient motion"
4. "tracking shot following"
5. "slow pan left/right"

### Top 5 Stability Keywords

1. "face remains perfectly still"
2. "same face throughout, consistent features"
3. "background stays static"
4. "subtle natural motion only"
5. "locked camera, environmental motion only"

### Top 5 Atmosphere Keywords (for tech thumbnails)

1. "holographic panels pulse with [color] light"
2. "particles float gently upward"
3. "neon ambient glow shifts between [colors]"
4. "translucent UI elements drift slowly"
5. "volumetric light rays, atmospheric haze"

---

*Last updated: 2026-03-02 | Research covers tools available as of early March 2026*
