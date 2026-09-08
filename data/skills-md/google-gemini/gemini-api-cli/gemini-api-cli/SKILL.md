---
name: gemini-api-cli
description: Guide for using the Gemini API CLI tool. Use when you need to interact with the Gemini API via the command line, manage agents, or generate media (images, audio).
---

# Gemini API CLI Skill

This skill provides guidance on using the `gemini-api` command-line interface.

## Overview

The `gemini-api` CLI allows you to:
- Run prompts against various Gemini models.
- Manage the full lifecycle of Gemini Agents.
- Generate and edit media (images, audio, TTS).

## References

For detailed usage and examples, see the following references:

- **Normal Model Calls**: See [references/model_calls.md](references/model_calls.md) for text generation, multi-turn conversations, and tool usage.
- **Agents (Lifecycle)**: See [references/agents.md](references/agents.md) for creating, testing, and managing agents.
- **Agent Calls**: See [references/agent_calls.md](references/agent_calls.md) for invoking antigravity-preview-05-2026 and Deep Research agents.
- **Genmedia**: See [references/genmedia.md](references/genmedia.md) for image generation, image editing, and text-to-speech.

## Basic Usage

The primary command is `gemini-api run`.

```bash
gemini-api run "Hello, who are you?"
```

Always ensure your `GEMINI_API_KEY` environment variable is set.

## Global Flags & Features

The CLI supports several flags that are useful for debugging and automation:

### Dry Run (`--dry-run`)
Prints the equivalent `curl` command and exits without making an API call. Useful for verifying what request would be sent.
```bash
gemini-api run "Hello" --dry-run
```

### Help (`--help`)
Displays usage information and available flags for any command.
```bash
gemini-api --help
gemini-api run --help
```

### JSON Output (`--json`)
Outputs raw SSE events as JSONL (one event per line), useful for machine parsing.
```bash
gemini-api run "Hello" --json
```

### Verbose (`--verbose` / `-v`)
Outputs complete JSON step objects line-by-line as they finish. Recommended for programmatic parsing by calling agents.
```bash
gemini-api run "Hello" --verbose
```
