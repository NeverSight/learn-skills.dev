---
name: summarize
description: Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).
homepage: https://summarize.sh
metadata: {"clawdbot":{"emoji":"🧾","requires":{"bins":["summarize"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/summarize","bins":["summarize"],"label":"Install summarize (brew)"}]}}
---

# Summarize

Fast CLI to summarize URLs, local files, and YouTube links.

## Quick start

```bash
summarize "https://example.com" --model google/gemini-3-flash-preview
summarize "/path/to/file.pdf" --model google/gemini-3-flash-preview
summarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto
```

## OpenCode Zen (FREE models!)

Use OpenCode Zen for free summarization with GLM 4.7:

```bash
# Set env vars for OpenCode Zen
export OPENAI_BASE_URL="https://opencode.ai/zen/v1"
export OPENAI_API_KEY="<your-zen-api-key>"  # Get from https://opencode.ai/auth

# Summarize with free GLM 4.7
summarize "https://example.com" --model openai/glm-4.7-free
```

### Free models on OpenCode Zen:
| Model | Model ID |
|-------|----------|
| GLM 4.7 | `glm-4.7-free` |
| Big Pickle | `big-pickle` |
| Grok Code Fast 1 | `grok-code` |
| MiniMax M2.1 | `minimax-m2.1-free` |
| GPT 5 Nano | `gpt-5-nano` |

### When using summarize with OpenCode Zen:
```bash
OPENAI_BASE_URL="https://opencode.ai/zen/v1" OPENAI_API_KEY="$OPENCODE_ZEN_KEY" summarize "URL" --model openai/glm-4.7-free
```

## Model + keys

Set the API key for your chosen provider:
- OpenAI: `OPENAI_API_KEY`
- Anthropic: `ANTHROPIC_API_KEY`
- xAI: `XAI_API_KEY`
- Google: `GEMINI_API_KEY` (aliases: `GOOGLE_GENERATIVE_AI_API_KEY`, `GOOGLE_API_KEY`)

Default model is `google/gemini-3-flash-preview` if none is set.

## Useful flags

- `--length short|medium|long|xl|xxl|<chars>`
- `--max-output-tokens <count>`
- `--extract-only` (URLs only)
- `--json` (machine readable)
- `--firecrawl auto|off|always` (fallback extraction)
- `--youtube auto` (Apify fallback if `APIFY_API_TOKEN` set)

## Config

Optional config file: `~/.summarize/config.json`

```json
{ "model": "openai/gpt-5.2" }
```

For OpenCode Zen default:
```json
{
  "model": "openai/big-pickle",
  "baseUrl": "https://opencode.ai/zen/v1"
}
```

Optional services:
- `FIRECRAWL_API_KEY` for blocked sites
- `APIFY_API_TOKEN` for YouTube fallback
