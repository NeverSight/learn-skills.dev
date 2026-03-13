---
name: token-optimizer
version: "0.1.0"
description: >
  Reduce LLM API costs by optimizing prompts before sending them to cloud providers.
  Coordinates local and remote code agents with a primary/fallback pipeline.
triggers:
  - "optimize prompt"
  - "reduce tokens"
  - "compress context"
  - "token budget"
  - "minimize API cost"
install: |
  git clone <repo-url> && cd TokenOptimizer
  cargo build --release
  # Binary: target/release/token_optimizer
requirements:
  os: linux, macos, windows
  binary: cargo (rustc 1.70+)
  optional_binary: ollama (for local LLM preprocessing)
env:
  VENICE_API_KEY: "Primary provider API key (Venice.ai)"
  ANTHROPIC_API_KEY: "Fallback provider API key (Claude) — optional"
  OPENAI_API_KEY: "Fallback provider API key (OpenAI) — optional"
configuration:
  file: "~/.config/token_optimizer/config.toml"
  sections:
    - primary: "Cloud provider (default: Venice.ai)"
    - fallback: "Backup provider (default: Claude CLI)"
    - local: "Ollama preprocessing settings"
    - optimization: "Strategy selection and tuning"
    - cache: "Anthropic cache prompting settings"
defaults:
  target_tokens: 4000
  strategies:
    - strip_whitespace
    - remove_comments
    - relevance_filter
  keyword_weight: 0.4
  preserve_code_blocks: true
---

# TokenOptimizer

## When to Use

- You have a coding task and want to send it to an LLM API with less context (fewer tokens, lower cost).
- You want automatic fallback from a cheap provider to a more capable one when credits run out.
- You want local LLM preprocessing to score relevance and compress context before it hits a paid API.
- You need to stay within a token budget while keeping the most important context.

## Quick Start

```bash
# Optimize a prompt with default strategies
token_optimizer optimize --input "Fix the bug in auth" --context src/auth.rs

# Analyze cache potential for Anthropic
token_optimizer cache-optimize --task "Add feature" --context types.rs --static-indices "0"

# Launch interactive shell (auto-selects provider)
token_optimizer interactive

# Show current config
token_optimizer config show primary
```

## Capabilities

| Capability | Description |
|---|---|
| **StripWhitespace** | Remove redundant whitespace, preserving code blocks |
| **RemoveComments** | Strip `//`, `/* */`, `#` comments from code |
| **TruncateContext** | Boundary-aware truncation using tiktoken token counts and priority-based boundary detection (code structure > paragraph > sentence > line > word) |
| **Abbreviate** | Shorten common programming terms in task text |
| **LlmCompress** | Compress context via local Ollama LLM |
| **RelevanceFilter** | Hybrid keyword + LLM relevance scoring; works without local LLM via keyword-only mode |
| **ExtractSignatures** | Keep only function/class/struct signatures |
| **Deduplicate** | Remove exact, whitespace-normalized, and near-duplicate context items |
| **CachePrompting** | Anthropic-compatible cache breakpoints for static content |
| **Provider Fallback** | Automatic primary -> fallback -> local provider pipeline |
