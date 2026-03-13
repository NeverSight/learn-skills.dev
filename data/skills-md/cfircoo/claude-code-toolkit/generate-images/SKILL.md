---
name: generate-images
description: Generate and edit images using Nano Banana (Google Gemini image generation). Use whenever Claude Code needs to create new images, edit existing images, generate icons, diagrams, mockups, or any visual content.
---

<essential_principles>

This skill generates images using the Nano Banana model via `~/.claude/scripts/generate_image.py`.

**Always use this skill when the user asks to:**
- Generate, create, or make an image
- Create icons, logos, banners, or visual assets
- Edit, modify, or transform an existing image
- Generate mockups, diagrams, or illustrations
- Create any visual content

**Prerequisites:**
- `GEMINI_API_KEY` must be set in `~/.claude/settings.json` under `env`
- Script: `~/.claude/scripts/generate_image.py` (runs via `uv run`)

**Reference images:** Users can store named images in `~/.claude/images/` for use as editing sources. Filenames describe the content (e.g., `myself.jpg`, `company-logo.png`, `office.jpg`).

</essential_principles>

<process>

<step name="1_check_api_key">
Before generating, verify the API key is available:

```bash
uv run ~/.claude/scripts/generate_image.py --check-key
```

If `API_KEY_MISSING`: inform the user they need to set `GEMINI_API_KEY` in `~/.claude/settings.json` or get one at https://aistudio.google.com/apikey
</step>

<step name="2_match_reference_images">
Check if the user's request refers to a known reference image.

**List available reference images:**
```bash
ls ~/.claude/images/ 2>/dev/null
```

**Matching rules:**
- Match user mentions to filenames (without extension). Examples:
  - "add a hat to **myself**" → look for `myself.jpg`, `myself.png`, etc.
  - "put **my dog** in a park" → look for `my-dog.jpg`, `dog.jpg`, etc.
  - "update the **company logo**" → look for `company-logo.png`, `logo.png`, etc.
- Match is case-insensitive, try with and without hyphens/underscores
- If a match is found, use `--edit` mode with the matched file as source
- If no match and the user clearly references a personal image, ask them to place it in `~/.claude/images/`

**Also check the current project** for relevant images if the user references project assets:
- Look in `assets/`, `images/`, `public/`, `static/`, or project root
</step>

<step name="3_determine_output_path">
Choose an appropriate output path based on context:

- If user specifies a path, use it
- If editing a reference image, save to the current project (not back to `~/.claude/images/`)
- If inside a project, use a sensible location (e.g., `assets/`, `images/`, `public/`, or project root)
- Default filename: descriptive kebab-case with `.png` extension (e.g., `hero-banner.png`, `app-icon.png`)
</step>

<step name="4_craft_prompt">
Write an effective image prompt. Good prompts include:

- **Subject**: What to generate (e.g., "a minimalist logo of a rocket")
- **Style**: Visual style (e.g., "flat design", "photorealistic", "watercolor", "pixel art")
- **Details**: Specific attributes (colors, lighting, composition, mood)
- **Quality**: Resolution hints (e.g., "high detail", "4K quality", "professional")

Example prompt structure: `[Subject], [style], [details], [quality]`
</step>

<step name="5_generate">
Run the generation script:

**Text-to-image (new image):**
```bash
uv run ~/.claude/scripts/generate_image.py "prompt here" --output path/to/output.png
```

**Image editing with reference image:**
```bash
uv run ~/.claude/scripts/generate_image.py "editing instructions" --edit ~/.claude/images/myself.jpg --output path/to/output.png
```

**Image editing with project image:**
```bash
uv run ~/.claude/scripts/generate_image.py "editing instructions" --edit path/to/source.png --output path/to/output.png
```

**Options:**
- `--output PATH` - Output file path (default: `generated_image.png`)
- `--edit IMAGE` - Source image for editing mode
- `--json` - Output metadata as JSON
</step>

<step name="6_verify">
After generation:

1. Read the output image using the Read tool to verify it was created and looks correct
2. Report the file path and size to the user
3. If the result doesn't match expectations, refine the prompt and regenerate
</step>

</process>

<prompt_examples>

**Icon/Logo:**
"A minimalist app icon for a task management tool, flat design, blue and white color scheme, clean geometric shapes, centered composition, professional quality"

**Banner/Hero:**
"Wide panoramic banner for a tech blog, abstract gradient background in purple and teal, modern typography space on the left, subtle geometric patterns, professional web design"

**Edit with reference image:**
User says: "add a clown hat to myself"
→ Match `myself.jpg` in `~/.claude/images/`
→ Run: `uv run ~/.claude/scripts/generate_image.py "Add a colorful clown hat to the person in this photo" --edit ~/.claude/images/myself.jpg --output clown-hat-myself.png`

**Edit with reference image:**
User says: "put my dog on a beach"
→ Match `dog.jpg` or `my-dog.jpg` in `~/.claude/images/`
→ Run: `uv run ~/.claude/scripts/generate_image.py "Place the dog on a tropical beach with waves and sunset" --edit ~/.claude/images/dog.jpg --output dog-on-beach.png`

</prompt_examples>

<success_criteria>
Image generation is complete when:

- API key check passes
- Reference images matched when applicable
- Image is saved to the specified output path
- Output image has been visually verified via Read tool
- User is informed of the file location
</success_criteria>
