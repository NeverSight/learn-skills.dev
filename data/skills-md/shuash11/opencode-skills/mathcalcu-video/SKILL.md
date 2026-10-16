---
name: mathcalcu-video
description: Build promotional/tutorial videos for MathCalcu Flutter app. Uses PIL for frame generation, mcp-video for video assembly and post-processing.
---

# MathCalcu Video Skill (mcp-video edition)

## Overview
Creates promotional and tutorial videos for the MathCalcu Flutter calculus solver app. PIL/Pillow generates frames, mcp-video compiles them into video and handles audio, transitions, and quality gates.

## Key Files
- **App project:** `C:\projects\mathcalcu` (Flutter)
- **Real logo:** `C:\projects\mathcalcu\assets\images\app_icon.png`
- **Tutorial scripts:** `C:\projects\mathcalcu\tutorial\build_video_v*.py`
- **Narration audio:** `C:\projects\mathcalcu\tutorial\narration\*.mp3`
- **Official script:** `C:\Users\joashua\Downloads\MathCalcu_VideoPromo_Script.md`
- **Output:** `C:\Users\joashua\Downloads\mathcalcu_tutorial.mp4`

## ElevenLabs API
- Key in: `C:\Users\joashua\video-use\.env`
- Voice ID: `hpp4J3VqNfWAUOO0d1Us`

## The 9 Segments
1. Hook — "Tomorrow: MATH EXAM" → stress → "MATHCALCU HAS ENTERED THE CHAT"
2. App Introduction — 8 modules, benefits, "Built by BSCS students"
3. Derivatives Tutorial — Step-by-step demo, rapid demo, rules list
4. Quiz Break #1 — 2 derivative questions with countdown
5. Limits Tutorial — 4 methods, substitution/factoring/infinity demos
6. Analytic Geometry — Circles, Distance, Slope, Inequalities
7. Quiz Break #2 — 2 questions + bonus challenge
8. Fun Facts — 6 cards (Flutter, LaTeX, Descartes, Newton/Leibniz)
9. CTA/Outro — Logo, GitHub link, "Math doesn't have to be hard"

## Colors/Theme (from real logo)
- Background: dark navy (12,12,28)
- Primary: cyan (0,220,255)
- Accent: purple (120,80,255)
- Cards: (28,28,60)
- Fun accents: CORAL, LIME, GOLD, SKY, MAGENTA, MINT

## Workflow (PIL + mcp-video)

### 1. Generate frames (PIL)
PIL/Pillow generates each segment's frames as PNG sequences. Use 15 FPS for faster rendering. Build segments incrementally.

### 2. Compile frames to video (mcp-video)
```bash
python -m mcp_video create-from-images frames/segment_%04d.png -o segment_1.mp4 --fps 15
```

Or via Python:
```python
from mcp_video import Client
editor = Client()
editor.create_from_images("frames/segment_%04d.png", output_path="segment_1.mp4", fps=15)
```

### 3. Add narration (mcp-video)
```bash
python -m mcp_video add-audio segment_1.mp4 tutorial/narration/segment_1.mp3 -o segment_1.mp4 --replace
```

### 4. Merge segments (mcp-video)
```bash
python -m mcp_video merge segment_1.mp4 segment_2.mp4 segment_3.mp4 -o final_compilation.mp4
```

Or use the `edit` tool with a JSON timeline.

### 5. Add subtitles / overlays (mcp-video, optional)
```bash
python -m mcp_video subtitles final_compilation.mp4 subtitles.srt -o final.mp4
python -m mcp_video watermark final.mp4 app_icon.png -o final.mp4 --position bottom-right
```

### 6. Quality check (mcp-video)
```bash
python -m mcp_video video-quality-check final.mp4
python -m mcp_video video-release-checkpoint final.mp4
```

### 7. Copy final output
```bash
copy final.mp4 C:\Users\joashua\Downloads\mathcalcu_tutorial.mp4
```

## mcp-video Enhancement Options

| Step | mcp-video tool | Purpose |
|------|---------------|---------|
| Frame compilation | `create-from-images` | PNG sequence → video |
| Audio sync | `add-audio` | Mux narration |
| Segment assembly | `merge` or `edit` | Combine segments |
| Subtitles | `subtitles` / `subtitles_styled` | Caption overlays |
| Logo watermark | `watermark` | Branding |
| Text overlays | `add-text` / `text-animated` | Lower thirds |
| Audio normalize | `normalize-audio` | Consistent loudness |
| Quality gate | `quality-check` / `release-checkpoint` | Pre-release verification |
| Platform variants | `repurpose` | Shorts/Reels cuts |

## Important Notes
- Use 15 FPS for faster rendering
- Build segments incrementally, don't rebuild everything
- Real logo is at `assets/images/app_icon.png`
- Student character shirt color = CYAN (brand color)
- mcp-video is configured as an MCP server in opencode.json; use either MCP tools or CLI commands
- Run `mcp-video doctor` to verify dependencies
