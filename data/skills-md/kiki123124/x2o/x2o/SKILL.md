---
name: x2o
description: |
  Export X (Twitter) bookmarks, classify them with AI, and generate an Obsidian knowledge vault.

  USE FOR:
  - Exporting X/Twitter bookmarks to local files
  - AI-powered bookmark classification and summarization
  - Generating Obsidian-compatible markdown knowledge bases
  - Batch processing bookmarks from JSON exports
  - Resolving t.co short URLs to real URLs
  - Fetching full content from X Notes (long-form tweets)
  - Reclassifying existing markdown vaults with a different AI

  TRIGGERS:
  - "导出书签", "export bookmarks", "X 书签", "x2o", "书签分类"
  - "twitter bookmarks", "obsidian vault from bookmarks"
  - "classify my bookmarks", "organize bookmarks"
version: 0.4.0
---

# x2o — X Bookmark Export + AI Classification

Export X (Twitter) bookmarks → AI classify → Obsidian knowledge vault. All local, no third-party servers.

### What's New (v0.4.0)
- Standalone reclassify: pick existing output folder, reclassify with different AI
- Reads markdown content directly (no X link dependency)
- t.co short URLs automatically resolved to real URLs
- X Notes (long-form tweets) full content extraction

## Usage

Run the CLI script via `npx tsx`:

```bash
npx tsx ~/.claude/skills/x2o/scripts/x2o.ts \
  --cookie "<X cookie string>" \
  --provider openai \
  --api-key "sk-..." \
  --output ~/x2o-output \
  --limit 100

# 也可以换成其他 provider：
# --provider claude  --api-key "sk-ant-..."
# --provider gemini  --api-key "..."
# --provider ollama  --model llama3.2   （本地 Ollama 不需要 api-key）
```

### Re-classify existing bookmarks (skip fetching):

If you already have an output folder that contains `bookmarks.json`, you can re-run AI classification without fetching again:

```bash
npx tsx ~/.claude/skills/x2o/scripts/x2o.ts \
  --input ~/x2o-output \
  --provider openai \
  --api-key "sk-..." \
  --output ~/x2o-output
```

### Rebuild from Markdown vault (only .md files) and re-classify:

```bash
npx tsx ~/.claude/skills/x2o/scripts/x2o.ts \
  --md-dir ~/x2o-output \
  --provider openai \
  --api-key "sk-..." \
  --output ~/x2o-output
```

> Notes:
> - Passing a directory to `--input/--reclassify/--md-dir` will first look for `<dir>/bookmarks.json`.
> - If not found, it will try to parse X URLs from `.md` files and reconstruct a minimal bookmarks list.

## Parameters

| Flag | Required | Description |
|------|----------|-------------|
| `--cookie` | Yes* | X browser cookie (must contain `ct0`) |
| `--input` | Yes* | Path to existing bookmarks JSON **or an output folder containing `bookmarks.json`** (alternative to cookie) |
| `--reclassify` | No | Alias of `--input` |
| `--md-dir` | No | Path to a Markdown vault folder (only `.md` files). If the folder has `bookmarks.json`, it will use that first. |
| `--provider` | No | AI provider (default: `openai`): `openai`, `claude`, `deepseek`, `gemini`, `ollama`, `groq`, `moonshot`, `qwen`, `zhipu`, `siliconflow`, `mistral`, `together`, `fireworks`, `xai`, `openrouter`, `cohere`, `deepinfra`, `perplexity` |
| `--api-key` | Yes** | API key for the chosen provider (not required for `ollama`, or when using `--fetch-only`) |
| `--output` | No | Output directory (default: `~/x2o-output`) |
| `--limit` | No | Max bookmarks to fetch (default: 800) |
| `--model` | No | Override default model for the provider |
| `--base-url` | No | Override API base URL |
| `--fetch-only` | No | Only fetch bookmarks, skip classification |

\* One of `--cookie` or `--input` is required
\** Not required for `ollama` (local)

## Workflow for Claude

When user wants to export bookmarks:

1. Ask for their X cookie (guide them: F12 → Network → find any request → copy Cookie header)
2. Ask which AI provider they want to use + API key
3. Run the script with appropriate parameters
4. Report results: how many bookmarks fetched, categories found, files generated
5. Optionally open the output in Obsidian: `open "obsidian://open?path=<output-dir>"`

## Supported AI Providers (18+)

OpenAI, Claude, DeepSeek, Gemini, Ollama, OpenRouter, Moonshot, Qwen, Zhipu GLM, SiliconFlow, Groq, Mistral, Together AI, Fireworks, Grok (xAI), Cohere, DeepInfra, Perplexity

## Source

GitHub: https://github.com/kiki123124/x2o
