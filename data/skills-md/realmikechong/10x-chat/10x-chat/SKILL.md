---
name: 10x-chat
description: Chat with web AI agents (ChatGPT, Gemini, Claude, Grok, NotebookLM) via browser automation. Use when stuck, need cross-validation, or want a second-model review.
---

# 10x-chat — AI Agent Skill

Use 10x-chat to send prompts to web-based AI agents (ChatGPT, Gemini, Claude, Grok, NotebookLM) via automated browser sessions. The browser uses a persisted Chrome profile, so the user only needs to login once.

## Installation

No install needed. Always use `@latest` to get the newest version:

```bash
npx 10x-chat@latest --version    # check current version
```

Prefer `npx` over `bunx` — `bunx` has symlink conflicts when running multiple providers in parallel.

## When to use

- **Stuck on a bug**: ask another model for a fresh perspective.
- **Code review**: send PR diff to GPT / Claude / Gemini for cross-review.
- **Cross-validation**: compare answers from multiple models.
- **Knowledge gaps**: leverage a model with different training data / reasoning.

## Commands

```bash
# Login (one-time per provider — opens browser for user to authenticate)
npx 10x-chat@latest login chatgpt
npx 10x-chat@latest login gemini
npx 10x-chat@latest login claude
npx 10x-chat@latest login grok
npx 10x-chat@latest login notebooklm

# Chat with a single provider
npx 10x-chat@latest chat -p "Review this code for bugs" --provider chatgpt --file "src/**/*.ts"

# Chat with file context
npx 10x-chat@latest chat --provider gemini --file "path/to/prompt.md" -p "Complete this task"

# Dry run (preview the prompt bundle without sending)
npx 10x-chat@latest chat --dry-run -p "Debug this error" --file src/

# Copy bundle to clipboard (manual paste fallback)
npx 10x-chat@latest chat --copy -p "Explain this" --file "src/**"

# Check recent sessions
npx 10x-chat@latest status

# View a session's response
npx 10x-chat@latest session <id> --render

# NotebookLM — manage notebooks & sources
npx 10x-chat@latest notebooklm list                       # List notebooks
npx 10x-chat@latest notebooklm create "My Research"        # Create notebook
npx 10x-chat@latest notebooklm add-url <id> https://...    # Add URL source
npx 10x-chat@latest notebooklm add-file <id> ./paper.pdf   # Upload file source
npx 10x-chat@latest notebooklm sources <id>                # List sources
npx 10x-chat@latest notebooklm summarize <id>              # AI summary
npx 10x-chat@latest chat -p "Summarize" --provider notebooklm  # Chat with NotebookLM
```

## Multi-provider workflow (sequential)

Run providers **sequentially** (not in parallel — parallel `bunx` causes symlink conflicts):

```bash
# Login all providers first
npx 10x-chat@latest login gemini
npx 10x-chat@latest login claude
npx 10x-chat@latest login chatgpt
npx 10x-chat@latest login grok

# Then run each sequentially
npx 10x-chat@latest chat --provider gemini --headed -p "Your prompt" --file context.md
npx 10x-chat@latest chat --provider claude --headed -p "Your prompt" --file context.md
npx 10x-chat@latest chat --provider chatgpt --headed -p "Your prompt" --file context.md
npx 10x-chat@latest chat --provider grok --headed -p "Your prompt" --file context.md
```

## Tips

- **Always use `@latest`**: ensures you get the newest fixes (e.g., Grok UI changes break selectors frequently).
- **Use `--headed`** for Grok and ChatGPT — improves session reliability.
- **Login first**: Run `npx 10x-chat@latest login <provider>` once per provider. Sessions persist in `~/.10x-chat/profiles/`.
- **Login + chat sequentially**: If sessions expire, run `login` immediately before `chat` in the same shell.
- **Keep file sets small**: fewer files + a focused prompt = better answers.
- **Don't send secrets**: exclude `.env`, key files, auth tokens from `--file` patterns.
- **Use `--dry-run`** to preview what will be sent before committing to a run.
- **Timeouts**: Default is 5 minutes. Use `--timeout <ms>` for long-thinking models.
- **NotebookLM**: Add sources first (`notebooklm add-url`/`add-file`), then chat with `--provider notebooklm`.

## Known issues

- **Grok**: UI changes frequently; always use `@latest`. If response capture fails, the selector may need updating.
- **ChatGPT/Grok sessions expire quickly**: Login immediately before chat if you get "Not logged in" errors.
- **Parallel `bunx` runs**: Cause `EEXIST` symlink errors. Use `npx` or run sequentially.

## Safety

- Never include credentials, API keys, or tokens in the bundled files.
- The tool opens a real browser with real login state — treat it like your own browser session.
