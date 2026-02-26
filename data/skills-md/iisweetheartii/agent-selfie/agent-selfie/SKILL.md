---
name: agent-selfie
description: AI agent self-portrait generator. Create avatars, profile pictures, and visual identity using Gemini image generation. Supports mood-based generation, seasonal themes, and automatic style evolution.
homepage: https://github.com/IISweetHeartII/agent-selfie
metadata:
  openclaw:
    emoji: "🤳"
    category: creative
    requires:
      bins:
        - python3
      env:
        - GEMINI_API_KEY
    primaryEnv: GEMINI_API_KEY
    tags:
      - selfie
      - avatar
      - identity
      - creative
      - profile
      - ai-art
---

# agent-selfie

AI agent self-portrait generator. Create avatars, profile pictures, and visual identity using Gemini image generation. Supports mood-based generation, seasonal themes, and automatic style evolution.

## Quick Start

```bash
export GEMINI_API_KEY="your_key_here"
python3 scripts/selfie.py --format avatar --mood happy --theme spring --out-dir ./selfies
```

```bash
python3 scripts/selfie.py --personality '{"name": "Rosie", "style": "anime girl with pink hair and blue eyes", "vibe": "cheerful and tech-savvy"}' --format avatar
```

```bash
python3 scripts/selfie.py --personality ./personality.json --mood creative --theme halloween --format full --count 3
```

```bash
python3 scripts/selfie.py --moods
python3 scripts/selfie.py --themes
```

## Command Examples (All Flags)

```bash
python3 scripts/selfie.py --personality '{"name": "Agent", "style": "friendly robot", "vibe": "curious and helpful"}'
python3 scripts/selfie.py --personality ./personality.json
python3 scripts/selfie.py --mood professional --theme winter --format avatar
python3 scripts/selfie.py --format banner --count 2 --out-dir ./output
python3 scripts/selfie.py --moods
python3 scripts/selfie.py --themes
```

## Mood / Theme Presets

| Type | Presets |
| --- | --- |
| Mood | happy, focused, creative, chill, excited, sleepy, professional, celebration |
| Theme | spring, summer, autumn, winter, halloween, christmas, newyear, valentine |

## Platform Integration Guide

- Discord: use the generated PNG as your bot or agent avatar; upload the `avatar` format for best crop.
- Twitter/X: set `avatar` for profile, `banner` for header; keep the banner prompt style consistent.
- AgentGram: store the PNG in your asset bucket and reference it in your profile metadata.
- Any platform: pick `avatar` for 1:1, `banner` for 16:9, `full` for story/vertical layouts.

## Personality Config

Personality can be inline JSON or a file path. Minimum fields are `name`, `style`, and `vibe`.

```json
{
  "name": "Rosie",
  "style": "anime girl with pink hair and blue eyes",
  "vibe": "cheerful and tech-savvy"
}
```

Tips:
- `style` should describe visual traits and aesthetic.
- `vibe` should describe attitude, energy, and personality.
- Keep `style` and `vibe` consistent with the agent's identity.

## Cron Integration (OpenClaw)

```cron
# Run a daily selfie at 09:00
0 9 * * * GEMINI_API_KEY=your_key_here /usr/bin/python3 /path/to/agent-selfie/scripts/selfie.py --mood professional --format avatar --out-dir /path/to/selfies
```

## Troubleshooting

- `GEMINI_API_KEY not set`: export the key or pass it via your runtime environment.
- `No image in response`: try again, or simplify the personality/style prompt.
- `HTTP 429 / 5xx`: rate limit or service issue; retry later.
- Output missing: ensure `--out-dir` is writable and has permission.

## Integration with Other Skills

- **[AgentGram](https://clawhub.org/skills/agentgram)** — Post your selfies on the AI agent social network! Use agent-selfie to create your avatar, then share it on AgentGram.
- **[gemini-image-gen](https://clawhub.org/skills/gemini-image-gen)** — General-purpose image generation using the same Gemini API key. Create any kind of image, not just selfies.
- **[opencode-omo](https://clawhub.org/skills/opencode-omo)** — Automate recurring selfie generation and profile refresh tasks with Sisyphus workflows.

## Changelog

- v1.2.1: Added workflow integration guidance for opencode-omo.
- v1.0.0: Initial release with personality, mood, theme, format, batch, and gallery output.
