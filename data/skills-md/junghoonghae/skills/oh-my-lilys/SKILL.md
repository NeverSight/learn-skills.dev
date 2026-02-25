---
name: oh-my-lilys
description: CLI tool for lilys.ai - Summarize YouTube, PDF, websites, and audio. Use when user wants to: (1) Summarize content from URLs, (2) List digest sessions, (3) Generate/fetch AI reports with different note types, (4) Manage authentication. Triggers: "summarize URL", "generate report", "get sessions", "lilys", "YouTube summary".
---

# oh-my-lilys

CLI tool for lilys.ai to summarize YouTube, PDF, websites, and audio directly from your terminal.

## Installation

```bash
npm install -g oh-my-lilys
```

For auto-auth, install playwright-cli:

```bash
npm install -g playwright-cli
```

## Commands

| Command   | Description                                    |
| --------- | ---------------------------------------------- |
| auth      | Authenticate with lilys.ai (auto or token)     |
| summarize | Summarize a URL (YouTube, PDF, audio, website) |
| sessions  | List digest sessions                           |
| report    | Get report for a session                       |
| lang      | Get/set AI result language                     |
| upgrade   | Check for updates                              |
| doctor    | Diagnose and fix issues                        |
| whoami    | Check authentication status                    |

## Report Options

| Option              | Description                        |
| ------------------- | ---------------------------------- |
| --note-type <type>  | Generate specific note type        |
| --watch             | Watch for report completion (poll) |
| --timeout <seconds> | Watch timeout (default: 120)       |
| --export markdown   | Export as markdown file            |

## Note Types

`detailed`, `key_points`, `easy`, `script`, `animation`, `infographic`, `background`, `deep_dive`

## Authentication

```bash
# Auto-detect from browser (recommended)
lilys auth

# Manual with token
lilys auth <token>
```

Browser profile stored at `~/.lilys-chrome-profile`.

## Examples

```bash
lilys auth
lilys summarize https://youtube.com/watch?v=abc123
lilys sessions
lilys report 8260019
lilys report 8260019 --note-type detailed --watch --timeout 180
lilys report 8260019 --export markdown
lilys lang ko
```

## Error Handling

- **Auth errors**: Auto-detected (401/403/invalid_token), prompts re-authentication
- **Note generation timeout**: 504 errors don't fail, generation continues in background
- **Watch mode**: Polls every 3 seconds until ready or timeout

## Disclaimer

This tool reverse-engineers the lilys.ai API. Use at your own risk.
