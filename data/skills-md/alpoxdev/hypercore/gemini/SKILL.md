---
name: gemini
description: >-
  Use when the user wants to invoke Google Gemini CLI for reasoning tasks, research, and AI assistance.
  Trigger phrases: "use gemini", "ask gemini", "run gemini", "call gemini", "gemini cli", "Google AI",
  "Gemini reasoning", or when users request Google's AI models, research with web search, or want to
  continue a previous Gemini session.
---

# Gemini Skill

## Defaults

| Parameter | Default |
|-----------|---------|
| Model | `gemini-3.1-pro-preview` |
| Approval mode | `default` |
| Fallback chain | `gemini-3.1-pro-preview` → `gemini-2.5-pro` → `gemini-2.5-flash` |

Do NOT ask the user for model unless explicitly requested.

## CRITICAL: Headless Mode

**Always use `-p`/`--prompt`** in Claude Code. As of v0.29.0+, positional prompts open interactive mode.

```bash
# Correct
gemini -m gemini-3.1-pro-preview -p "your prompt here"

# Wrong — opens interactive terminal
gemini -m gemini-3.1-pro-preview "your prompt here"
```

## Running a Task

1. Select approval mode based on the task:
   - `default` (default): all tasks — prompts before edits
   - `auto_edit`: only when user explicitly requests file editing
   - `plan`: read-only, no file modifications
   - `yolo`: full auto-approval — ask user before using

2. Assemble and run the command:
   ```bash
   gemini -m gemini-3.1-pro-preview -p "your prompt here"
   ```

3. To resume a previous session:
   ```bash
   gemini -r latest -p "your follow-up prompt"
   gemini --list-sessions  # to see available sessions
   ```

4. After completion, use `AskUserQuestion` to confirm next steps or whether to resume.

5. When output includes warnings or partial results, summarize and ask how to adjust.

**Preview features note**: If OAuth free tier with `previewFeatures: true` in `~/.gemini/settings.json` causes 404 errors, set `"previewFeatures": false`. Fallback to `gemini-2.5-flash` automatically on 404.

## Critical Evaluation

Treat Gemini as a **colleague, not an authority**.

- **Trust your knowledge** when confident. Push back on incorrect claims directly.
- **Research disagreements** using WebSearch or docs before accepting Gemini's claims.
- **Remember knowledge cutoffs** — Gemini may not know about recent releases or API changes.
- Let the user decide when there's genuine ambiguity.

## Error Handling

- `command not found: gemini`: tell user to install Gemini CLI.
- Auth errors: run `gemini login`.
- 429 / rate limit: free tier is 60 req/min, 1000 req/day — wait or upgrade.
- 404 / model not found: retry with fallback model.
- 403 / access denied: disable `previewFeatures` or use `gemini-2.5-pro`.
- Session not found: run `gemini --list-sessions`.
