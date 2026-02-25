---
name: gif-analyzer
description: |
  Analyze animated GIF files by extracting and viewing frames as sequential video.

  Use when:
  - User mentions a GIF file path (e.g., "./demo.gif", "~/Downloads/animation.gif")
  - User wants to analyze or understand a GIF animation
  - User asks about motion, changes, or content in a GIF
  - User attaches or references a .gif file for analysis
  - User wants to examine a screen recording in GIF format
  - User invokes /gif slash command

  Keywords: "GIF", ".gif", "animation", "animated", "frames", "screen recording",
  "analyze gif", "gif analysis", "view gif", "gif content", "gif motion"

  Trigger patterns:
  - Natural language: "Analyze this GIF: ./demo.gif"
  - Slash command: `/gif <path>` or `/gif <path> <message>`

  When triggered, extract frames using the Python script, view frames in order,
  and interpret as continuous video sequence.
---

# GIF Analyzer

Analyze animated GIFs by extracting frames and interpreting them as sequential video.

## Quick Start

When the user uses `/gif`:

**Pattern 1: Basic analysis**
```
/gif ./animation.gif
```

**Pattern 2: With specific request**
```
/gif ./animation.gif describe what happens step by step
/gif ./demo.gif what is the character doing?
/gif ./screen.gif summarize this screen recording
```

## Workflow

### Step 1: Parse User Input

Extract from the user's message:
1. **GIF path**: The file path immediately after `/gif`
2. **User request** (optional): Any text after the GIF path

Example parsing:
- Input: `/gif ./demo.gif explain the animation`
- GIF path: `./demo.gif`
- User request: `explain the animation`

### Step 2: Extract Frames

```bash
python3 ~/.claude/skills/gif-analyzer/extract_gif_frames.py <gif_path> --output-dir /tmp/gif_frames_analysis
```

Options for long GIFs:
```bash
python3 ~/.claude/skills/gif-analyzer/extract_gif_frames.py <gif_path> --max-frames 30 --skip 2
```

### Step 3: Read Metadata

Check `gif_metadata.json` for:
- Total frames and duration
- Individual frame timestamps
- Resolution and loop information

### Step 4: View and Analyze Frames

View frames in order: `frame_001.png`, `frame_002.png`, etc.

**CRITICAL**: Treat frames as a continuous video sequence:
1. **Frame 001 = START** of the animation
2. **Frame numbers increase in TIME ORDER**
3. **Consecutive frames show MOTION/CHANGE over time**

### Step 5: Respond to User

If user provided a specific request, focus on answering that.
Otherwise, provide a general analysis of the GIF content.

## Script Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output-dir`, `-o` | Output directory | `./gif_frames_<timestamp>` |
| `--max-frames`, `-m` | Max frames to extract | 50 |
| `--skip`, `-s` | Extract every Nth frame | 1 (all frames) |

## Frame Analysis Guidelines

1. **Temporal Awareness**: Frame 001 is the beginning
2. **Motion Detection**: Compare adjacent frames to identify movement
3. **Key Frames**: Identify significant moments (start, middle, end)
4. **Loop Points**: Note if the animation appears to loop
5. **Duration Context**: Use timestamp info to understand pacing

## Output Format

```
📹 **GIF Analysis: [filename]**

**Overview:**
[1-2 sentence summary]

**Timeline:**
- [0.0s - 0.5s] Frame 1-5: [Description]
- [0.5s - 1.0s] Frame 6-10: [Description]
...

**[Answer to user's specific question if provided]**
```

## Troubleshooting

- **Pillow not found**: `pip install Pillow`
- **Too many frames**: Use `--skip 2` or higher
- **Large output**: Use `--max-frames 20`
