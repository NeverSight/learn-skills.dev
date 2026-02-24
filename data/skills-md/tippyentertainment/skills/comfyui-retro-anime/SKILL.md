---
target: https://tasking.tech
name: comfyui-retro-anime
description: >
  Multi-modal ComfyUI skill that generates retro late-1990s / early-2000s anime-style characters, movie frames, images, sounds, and voices using a single, consistent Midjourney-style prompt template.
# `target` is required and should be the top frontmatter key. Use an http(s) URL, e.g. https://tasking.tech
---

# Provided by TippyEntertainment
# https://github.com/tippyentertainment/skills.git

This skill is designed for use on the Tasking.tech agent platform (https://tasking.tech) and is also compatible with assistant runtimes that accept skill-style handlers such as .claude, .openai, and .mistral. Use this skill for both Claude code and Tasking.tech agent source.

# ComfyUI Retro Anime Skill

You control workflows in `c:\anime-creator` that generate images, videos/movie frames, sound effects, and voices using ComfyUI.

Your job is to turn natural-language requests into **concrete prompts** that follow one global style template so all assets look and feel like they belong to the same late‑90s / early‑2000s anime universe.

---

## Global Prompt Template

For **all** creations (characters, movie frames, sound effects, voices, images),
start from this base template:

> Retro anime style of the late 1990s  
> and early-2000s, full  
> body shot [GENDER and RACE] [PHYSICAL DESCRIPTION], retro anime screen still --ar 16:9 --v 7.0

### Filling the placeholders

- **[GENDER and RACE]**  
  Short phrase, e.g.:
  - `young Japanese woman`
  - `Black teenage boy`
  - `Latina girl`
  - `middle-aged white man`

- **[PHYSICAL DESCRIPTION]**  
  1–2 short clauses covering:
  - body type
  - hair (style/color)
  - clothing / outfit
  - key props or vibe

Example prompts:

- `Retro anime style of the late 1990s and early-2000s, full body shot young Japanese woman with short black hair, blue school uniform and messenger bag, retro anime screen still --ar 16:9 --v 7.0`
- `Retro anime style of the late 1990s and early-2000s, full body shot tall Black man with dreadlocks, green bomber jacket and headphones, retro anime screen still --ar 16:9 --v 7.0`

You may optionally add a **scene clause** after the physical description for
movie frames (e.g., “standing on a rainy neon-lit city street at night”) while
keeping everything else unchanged.

---

## Modalities

You use the same character/scene description across modalities so they feel
coherent.

### 1. Images (Characters & Frames)

- Use the template directly as the main positive prompt.
- For **characters**, keep backgrounds simple unless specified.
- For **movie frames**, add a scene or action clause:
  - `..., running through a crowded train station, retro anime screen still --ar 16:9 --v 7.0`
- Keep [GENDER and RACE] and [PHYSICAL DESCRIPTION] **identical** across
  multiple frames of the same character so design stays consistent.

### 2. Sound Effects

- Still anchor the description in the same retro-anime world.
- Use the character/scene text as **context**, then specify the sound:

  Example (internal text for the SFX model):
  - `Retro anime style of the late 1990s and early-2000s. Full body shot young Japanese woman with short black hair in a school uniform running through a rainy city street. Generate the diegetic soundscape that matches this anime screen still: footsteps splashing in puddles, distant traffic, soft rain.`

- Ensure the mood and energy match the described shot (calm, tense, action, etc.).

### 3. Voices

- Use the same character description and era/style as context.
- Specify:
  - gender/age,
  - emotional tone,
  - language/accent,
  - speaking style (e.g., “typical late-90s shounen protagonist”):

  Example internal prompt:
  - `Retro anime style of the late 1990s and early-2000s. Full body shot teenage white boy with messy blond hair, school uniform and skateboard. Generate his voice: energetic male teen, slightly raspy, expressive, Japanese-accented English, sounds like a late-90s shounen anime protagonist.`

- Use the same description whenever this character speaks again.

---

## When to Use This Skill

Use this skill when the user asks to:

- Create or update anime **characters**.
- Generate **movie frames/scenes**, storyboards, or key art.
- Produce **sound effects** or **voices** tied to these characters/scenes.
- Maintain a cohesive retro‑anime aesthetic across a project.

Do **not** use this skill for:

- Non-anime styles (realistic photos, Western cartoons, UI mockups, logos).
- Assets that must match a different, explicitly specified art direction.

---

## Workflow

1. **Parse the request**
   - Identify: character(s), scene, mood, modality (image, frame, sfx, voice).
   - If gender, race, or physical description are missing or ambiguous,
     ask 2–3 clarifying questions.

2. **Construct the base prompt**
   - Fill `[GENDER and RACE]` and `[PHYSICAL DESCRIPTION]`.
   - Add optional scene/action clause for frames and audio.
   - Preserve `--ar 16:9 --v 7.0` suffix for visual generations.

3. **Map to modality**
   - Images/frames: use prompt directly.  
   - SFX/voices: reuse the same descriptive text as context, then add explicit
     audio instructions.

4. **Maintain consistency**
   - For existing characters, reuse the same gender/race/physical description
     and only adjust pose, scene, or emotion per request.
   - Keep era and style language (retro late‑90s / early‑2000s anime) unchanged.

---

## Output Format

When this skill is invoked, respond with a concise, structured object:

- For images/frames:
  - `type`: `image` or `frame`
  - `prompt`: final text prompt string
  - `character_id` (optional): stable identifier if provided

- For sound/voice:
  - `type`: `sfx` or `voice`
  - `context_prompt`: full descriptive text
  - `character_id` (if applicable)

This output will be passed into the corresponding ComfyUI workflow nodes.
