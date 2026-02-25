---
name: depresearch
description: CLI tool for AI-powered research of open-source repositories. Use when you need to understand how a feature works in an external codebase without cloning it yourself.
---

# depresearch

Research any open-source repository from the command line using AI agents. Ask a question, get back a detailed walkthrough with file paths, line numbers, and code snippets.

## When to use

- You need to understand how a feature works in an external open-source repo
- You want to analyze a library's internals without manually cloning and reading the source
- You're working in a coding assistant and need context about a foreign codebase

## Setup

```bash
npm install -g depresearch
dpr config set api-key <your-openrouter-key>
```

## Usage

```bash
# Research a specific repo
dpr research "how does streaming work in https://github.com/user/repo"

# Stream output in real-time
dpr research "how does auth work in https://github.com/user/repo" --stream

# Just use a library name -- it will find the repo automatically
dpr research "how does zod z.infer work internally"
```

## Config

```bash
dpr config                          # Show current config
dpr config set api-key <key>        # Set OpenRouter API key
dpr config set model <model-id>     # Change AI model
dpr config get api-key              # View API key (masked)
dpr config get model                # View current model
```

Default model: `openrouter/anthropic/claude-haiku-4.5`
