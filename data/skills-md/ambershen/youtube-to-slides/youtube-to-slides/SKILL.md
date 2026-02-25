---
name: youtube-to-slides
description: >
  Convert a YouTube video into infographic slides. Extracts transcript, segments
  into sections, summarizes, and generates stylized infographic images using Gemini AI.
  7 styles: davinci, magazine, comic, geek, chalkboard, collage, newspaper. Use when user wants slide summaries from YouTube.
argument-hint: "<youtube-url> [--style davinci|magazine|comic|geek|chalkboard|collage|newspaper] [--max-sections N]"
allowed-tools: Bash, Read, Write, Glob
context: fork
---

# youtube-to-slides

Convert YouTube videos into beautiful infographic slide decks.

## Natural Language Examples

Users can invoke this skill with natural language. Here are examples of what they might say and how to handle each:

**Setup and troubleshooting:**
- "Set up youtube-to-slides" → Run `setup.sh`
- "Check if youtube-to-slides is ready" → Run `check-env.sh`
- "I need to configure my API keys" → Guide to `.env` setup
- "It's not working" → Run `check-env.sh`, read diagnostics, consult `references/TROUBLESHOOTING.md`

**Generate slides:**
- "Generate slides from https://youtu.be/VIDEO_ID"
- "Convert this YouTube video to slides: https://youtube.com/watch?v=VIDEO_ID"
- "Make infographic slides from https://youtu.be/VIDEO_ID in comic style"
- "Create 5 magazine-style slides from https://youtu.be/VIDEO_ID"
- "Turn this video into slides https://youtu.be/VIDEO_ID --style geek"

**Choose a style:**
- "Use the davinci style" → `--style davinci`
- "Make it look like a magazine" → `--style magazine`
- "Comic book style please" → `--style comic`
- "Geek / bulletin board style" → `--style geek`
- "Chalkboard style" → `--style chalkboard`
- "Collage / dreamcore style" → `--style collage`
- "Newspaper style" → `--style newspaper`

**Control slide count:**
- "Just give me 4 slides" → `--max-sections 4`
- "Make as many slides as needed" → `--max-sections 0`

**Preview without generating images:**
- "Do a dry run first"
- "Just show me the prompts, don't generate images yet"

## Argument Parsing

Parse `$ARGUMENTS` to extract:

- **url** (required) — YouTube video URL. Supports formats: `https://youtu.be/ID`, `https://www.youtube.com/watch?v=ID`, `https://youtube.com/watch?v=ID`
- **--style** (optional, default: `davinci`) — One of: `davinci`, `magazine`, `comic`, `geek`, `chalkboard`, `collage`, `newspaper`
- **--max-sections** (optional, default: `8`) — Maximum number of slide sections to generate. Use `0` for unlimited.
- **--dry-run** (optional) — Show prompts without generating images
- **--ar** (optional, default: `16:9`) — Aspect ratio: `16:9`, `4:3`, or `1:1`

If no URL is provided, ask the user for one. If the URL looks invalid (not a YouTube URL), tell the user and ask for a valid one.

For style guidance, read `references/STYLES.md` in this skill directory.

## Execution Steps

### Step 1: Pre-flight Check

Run the environment check script:

```bash
bash "$SKILL_DIR/scripts/check-env.sh"
```

- If it exits 0, proceed to Step 2.
- If it exits non-zero, read its output for diagnostics:
  - **Missing virtual environment or package** — Run the setup script:
    ```bash
    bash "$SKILL_DIR/scripts/setup.sh"
    ```
    Then re-run `check-env.sh` to confirm.
  - **Missing API keys** — Tell the user:
    1. Copy the example env file: `cp "$SKILL_DIR/.env.example" "$SKILL_DIR/.env"`
    2. Add their Gemini API key (get one free at https://aistudio.google.com/apikey)
    3. Add their YouTube Data API key (get one at https://console.cloud.google.com/apis/credentials — enable YouTube Data API v3 first)
    4. See `references/TROUBLESHOOTING.md` for detailed setup steps.
  - After fixing, re-run `check-env.sh` to confirm everything passes.

If the user just asks to "set up" or "install" the skill, run both `setup.sh` and `check-env.sh`, then report the result.

### Step 2: Run the Pipeline

Build the command from parsed arguments and run:

```bash
bash "$SKILL_DIR/scripts/run.sh" "<url>" --style <style> --max-sections <max_sections> --ar <ar>
```

Add `--dry-run` flag if requested.

**This takes 3-5 minutes for a full run.** Inform the user that generation is in progress and what style/settings are being used.

### Step 3: Present Results

After successful completion:

1. Determine the video ID from the URL (the 11-character ID, e.g. `twzLDx9iers` from `https://youtu.be/twzLDx9iers`)
2. Read `output/<video_id>/metadata.json` to get the list of generated slides
3. Present a summary to the user:
   - Video title and channel
   - Style used
   - Number of slides generated
   - List each slide with its title and file path
4. Show the user how to open the slides:
   ```bash
   open output/<video_id>/
   ```

### Error Handling

If the pipeline fails, check output for common errors and consult `references/TROUBLESHOOTING.md`:

- **429 Rate Limit** — Gemini rate limit hit. The tool has built-in retry logic. If it still fails, suggest waiting 60 seconds and retrying.
- **No transcript available** — The video may not have captions. Inform the user.
- **Invalid URL** — Ask the user for a valid YouTube URL.
- **API key errors** — Guide user to set up their `.env` file with valid keys.

## Variable Reference

- `$SKILL_DIR` — Absolute path to this skill's directory (`skills/youtube-to-slides/`)
- `$ARGUMENTS` — Raw argument string passed by the user
