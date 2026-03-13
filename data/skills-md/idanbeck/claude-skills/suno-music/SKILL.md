---
name: suno-music
description: Generate music using AI. Use when the user asks to create, generate, or make music, songs, audio, melodies, tracks, or beats. Supports custom lyrics, instrumental-only, and style tags.
allowed-tools: Bash, Read, Write
---

# Suno Music - AI Music Generation

Generate music using Suno AI's API.

## Setup (One-Time)

1. Sign in to [suno.ai](https://app.suno.ai/)
2. Open browser DevTools (F12) → Console tab
3. Run: `document.cookie`
4. Find the `__session=eyJ...` part (it's a long JWT token)
5. Export it: `export SUNO_COOKIE="__session=eyJ..."`

**Note:** The `__session` token expires after ~1 hour. You'll need to refresh it periodically.

## Usage

Run the generation script:

```bash
python3 ~/.claude/skills/suno-music/generate_music.py "your prompt here" [options]
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--custom` | Treat prompt as lyrics (not description) | False |
| `--tags` | Style/voice tags (e.g., "female voice, pop, upbeat") | None |
| `--title` | Song title | None |
| `--instrumental` | Generate instrumental only (no vocals) | False |
| `--output` | Output directory path | ./generated_music |
| `--model` | Model key (e.g., chirp-auk-turbo) | Default free model |

## Examples

### Generate from description

```bash
python3 ~/.claude/skills/suno-music/generate_music.py "an upbeat electronic track for a tech product demo"
```

### Custom lyrics with style

```bash
python3 ~/.claude/skills/suno-music/generate_music.py "[Verse 1]
Walking through the morning light
Everything feels just right" --custom --tags "indie folk, acoustic guitar, male voice" --title "Morning Light"
```

### Instrumental track

```bash
python3 ~/.claude/skills/suno-music/generate_music.py "epic orchestral trailer music with building tension" --instrumental
```

## Output

Songs are saved with format: `{timestamp}_{sanitized_title}_{n}.mp3`

Example: `20260106_morning_light_1.mp3`

Suno generates 2 variations per request by default.

## Credits

- Free tier: **50 credits/day** (renews daily)
- Each generation uses **10 credits** (5 per song × 2 variations)
- So you can generate **5 songs per day** on the free tier

Check remaining credits:
```bash
python3 ~/.claude/skills/suno-music/generate_music.py --credits
```

## Models

| Model | Key | Notes |
|-------|-----|-------|
| v4.5-all | chirp-auk-turbo | Best free model (default) |
| v5 | chirp-crow | Pro only, beta |
| v4.5+ | chirp-bluejay | Pro only |
| v4 | chirp-v4 | Pro only |

## Requirements

- Python 3.x
- `requests` library (usually pre-installed)
- `SUNO_COOKIE` environment variable with `__session` token

## Troubleshooting

**"API Error: 401"** - Token expired. Get a fresh `__session` token from the browser.

**"API Error: 402"** - Out of credits. Wait for daily refresh or upgrade.
