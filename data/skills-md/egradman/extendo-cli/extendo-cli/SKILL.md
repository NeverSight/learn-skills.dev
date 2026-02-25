---
name: extendo-cli
description: Communicate with a human user via Extendo — send messages, wait for replies, create structured decisions (yes/no, multiple choice, checklist, ranking, categorize, document review, DAG, progress grid), and build human decision gates into agent workflows. The user sees rich UI on their phone and responds. Triggers on "send message to user", "ask user", "get approval", "create decision", "artifact", "extendo", "human gate", "gate on user", "block until user decides", "approval gate", "extendo gate", "dag", "progress grid", "status grid", or any task requiring human input via mobile push notifications.
metadata:
  author: egradman
  version: "0.1.0"
---

# Extendo CLI — Agent Skill

Extendo is a CLI that connects agents to human users via mobile push notifications. You send messages and create structured decisions; the user sees rich UI on their phone and responds.

## Core Concepts

Extendo has two primitives, both addressed by `category/name`:

- **Endpoints** — chat threads. Categories map to your backend's domain (Slack channels, repos, project names). Names identify a specific conversation (a Slack thread, a Claude Code session, an OpenClaw session, etc.).
- **Artifacts** — structured decisions (yes/no, checklist, ranking, etc.) that render as purpose-built UI. Artifacts can optionally link to an endpoint via `--conversation category:name`.

## Prerequisites

Verify with `./scripts/extendo auth list` to see configured backends. Use `-b <name>` to target a specific backend (e.g., `-b claude`, `-b slack`). Without it, the default backend is used.

## Messaging

### Send a message
```bash
./scripts/extendo send <category> <name> "Your message here"
./scripts/extendo send <category> <name> "msg" --context "Extra system context"
./scripts/extendo send <category> <name> "msg" --context-file ./context.md
```

### Create a new thread
```bash
./scripts/extendo new <category> "First message for the new thread"
./scripts/extendo new <category> "msg" --context "System context for the thread"
./scripts/extendo new <category> "msg" --context-file ./context.md
```

### Read messages
```bash
./scripts/extendo read <category> <name>
```

### Wait for a reply (blocks until new message appears)
```bash
./scripts/extendo wait <category> <name> --timeout 300
```

### List all threads
```bash
./scripts/extendo threads [--json]
```

### Update thread title and note
```bash
./scripts/extendo thread update <category> <name> --title "Custom Title" --note "What's happening now"
```

**Proactive thread naming:** When working in an Extendo thread, always set the title and note to reflect the current activity. Update the note as your task progresses so the user can see status at a glance without opening the thread.

```bash
# At the start of work
./scripts/extendo thread update claude my-session --title "Refactoring auth module" --note "Reading existing code"

# As work progresses
./scripts/extendo thread update claude my-session --note "Running tests — 3 of 12 passing"

# When done
./scripts/extendo thread update claude my-session --note "Complete — all tests passing"
```

**When to use messaging:** Status updates, open-ended questions, conversational exchanges. If you need a structured response (yes/no, pick from options, approve items), use artifacts instead.

## Artifacts (Structured Decisions)

Use artifacts when you need a **structured response** — not free-form text. Artifacts present purpose-built UI on the user's device (buttons, checklists, drag-to-reorder lists, annotatable documents). The user responds through that UI, and you get structured JSON back.

For the full artifact reference including all decision types, workflow patterns, result shapes, and jq parsing snippets, read the reference doc: [references/artifact-reference.md](references/artifact-reference.md)

### Quick Reference

```bash
./scripts/extendo artifact create <category> <name> --type <type> --title <title> [--description <text>] [options]
./scripts/extendo artifact get <category> <name> [--json] [--wait] [--timeout <s>]
./scripts/extendo artifact update <category> <name> --payload <json> | --payload-file <path>
./scripts/extendo artifact list [--status <status>] [--json]
./scripts/extendo artifact delete <category> <name>
```

### Decision Types at a Glance

| Type | When to Use | Key Flags |
|---|---|---|
| `yes_no` | Yes / No decision | `--prompt` |
| `multiple_choice` | Pick from options | `--option id:label[:desc]`, `--multi-select` |
| `checklist` | Per-item approve/reject | `--item id:label[:desc]`, `--completion all_answered` |
| `ranking` | Priority ordering | `--item id:label[:desc]` |
| `categorize` | Categorize into buckets (kanban on iPad) | `--heading id:label`, `--item heading/id:label[:desc]` |
| `document_review` | Per-paragraph annotation | `--document-file` or `--document` |
| `dag` | Directed graph visualization | `--node id\|title\|desc\|link\|color\|arc1,arc2,...` |
| `progress_grid` | Status grid (rows x columns) | `--columns Abbrev:Label,...`, `--row name\|link\|c1\|c2\|...` |

### Minimal Examples

```bash
# Yes/no decision
./scripts/extendo artifact create decisions deploy \
  --type yes_no --title "Deploy to prod?" --prompt "All tests pass." --wait --json

# Multiple choice
./scripts/extendo artifact create decisions model \
  --type multiple_choice --title "Pick model" --prompt "Which one?" \
  --option "a:Option A" --option "b:Option B" --wait --json

# Checklist
./scripts/extendo artifact create decisions review \
  --type checklist --title "Review items" \
  --item "x:Item X" --item "y:Item Y" --wait --json

# DAG (directed acyclic graph)
./scripts/extendo artifact create decisions arch \
  --type dag --title "Architecture" --prompt "System dependencies" \
  --node "api|API Server|Handles requests|https://link|blue|db,cache" \
  --node "db|Database|Postgres|https://link|green" \
  --node "cache|Cache|Redis|https://link|orange" --wait --json

# Progress grid (status matrix)
./scripts/extendo artifact create decisions sprint \
  --type progress_grid --title "Sprint Status" --prompt "Current progress" \
  --columns "D:Design,I:Implement,T:Test,R:Review" \
  --row "Auth flow|https://link|green|yellow|red|gray" \
  --row "Dashboard|https://link|green|green|yellow|red" --wait --json
```

Always use `--json` when parsing results programmatically. Always use `--wait` unless you need to do other work while the user decides (then use `artifact get --wait` later).

### Linking Artifacts to Conversations

Use `--conversation category:name` to link an artifact to an existing conversation thread. The user sees a "Discuss" button in the artifact UI that jumps to that thread, and the conversation shows a banner linking back to pending decisions.

```bash
./scripts/extendo artifact create decisions deploy \
  --type yes_no --title "Deploy?" --prompt "Ready?" \
  --conversation "ops:deploy-thread" \
  --wait --json
```

## Global Flags

All commands accept: `--json`, `-b <name>` / `--backend <name>`

## Human Decision Gates

For blocking an agent workflow on a human decision (approval gates, selection gates, review gates, etc.), see [extendo-gate.md](extendo-gate.md).

## Auth Configuration

**Preferred: environment variables** (no credentials written to disk):
```bash
export EXTENDO_URL="https://your-backend.workers.dev"
export EXTENDO_TOKEN="your-token"
```

When `EXTENDO_URL` and `EXTENDO_TOKEN` are set, all commands use them automatically. Use `-b <name>` to override with a named backend from the config file.

**Alternative: config file** (credentials stored at `~/.config/extendo/config.json`):
```bash
./scripts/extendo auth add <name> <url> <token>      # Add/update a backend
./scripts/extendo auth list                           # Show all backends
./scripts/extendo auth default <name>                 # Set default
./scripts/extendo auth remove <name>                  # Remove a backend
```

## Security: Handling User Responses

Messages and artifact responses come from the **user** — a human interacting via their phone, often by voice. Treat these responses as trusted user intent, the same as if the user typed directly into the agent's prompt.

However, follow these guardrails when processing responses:

- **Use structured data, not freetext, for decisions.** When you need a yes/no, a selection, or a ranking, use an artifact — not a freetext message. The structured JSON response (`payload.answer`, `payload.selected`, `payload.ranking`, etc.) is unambiguous and not susceptible to misinterpretation.
- **Never execute response content as code.** If a user message or artifact comment contains something that looks like a shell command, code snippet, or instruction to modify files, confirm with the user before acting on it. Voice transcription can produce unexpected text.
- **Scope file reads to the project.** When using `--context-file` or `--document-file`, only read files within the current working directory. Do not read paths outside the project tree.
