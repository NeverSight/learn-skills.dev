---
name: openhands-api
description: Use the OpenHands REST API (V0) to create and manage agent conversations programmatically. Includes minimal Python and TypeScript clients under scripts/.
triggers:
- openhands-api-v0
- openhands-cloud-v0
- oh-cloud-v0
---

This skill provides a minimal, easy-to-copy OpenHands API client for starting and monitoring conversations.

It is intentionally small and focused:

- Defaults to OpenHands Cloud (`https://app.all-hands.dev`).
- Targets the **legacy V0 REST API routes** implemented in `OpenHands/OpenHands` under `openhands/server/routes/`.
- Implements only a few core endpoints so an AI agent can quickly adapt/extend it.

## Quick start (Python)

```python
from scripts.openhands_api import OpenHandsAPI

api = OpenHandsAPI(api_key="...")  # or set OPENHANDS_API_KEY

conv = api.create_conversation(
    initial_user_msg="Please audit this repo for flaky tests and open a PR fixing them.",
    repository="owner/repo",
    selected_branch="main",
)
conversation_id = conv["conversation_id"]

final = api.poll_until_terminal(conversation_id, timeout_s=1800, poll_interval_s=30)
print(final["status"], final.get("url"))
```

## Quick start (TypeScript)

```ts
import { OpenHandsAPI } from "./scripts/openhands_api";

const api = new OpenHandsAPI({ apiKey: process.env.OPENHANDS_API_KEY! });

const conv = await api.createConversation({
  initialUserMsg: "Run dependency upgrades and open a PR.",
  repository: "owner/repo",
  selectedBranch: "main",
});

const final = await api.pollUntilTerminal(conv.conversation_id, {
  timeoutMs: 30 * 60_000,
  pollIntervalMs: 30_000,
});

console.log(final.status, final.url);
```

## Example (modeled after enyst/playground#105)

The following example shows a simple automation pattern:

1. Start a conversation with a prompt template
2. Print the conversation URL for humans
3. Optionally poll until completion

```bash
export OPENHANDS_API_KEY="..."
python skills/openhands_api/scripts/openhands_api.py \
  new-conversation \
  --prompt-file skills/openhands_api/references/example_prompt.md \
  --repo owner/repo \
  --branch main \
  --poll
```

## Notes for AI agents extending this client

- The server expects a Bearer token (`Authorization: Bearer <OPENHANDS_API_KEY>`).
- The most important endpoint is `POST /api/conversations`.
- If you need streaming/logs, the V0 server exposes `GET /api/conversations/{conversation_id}/events`.
- If you need the full event history in one call, use `GET /api/conversations/{conversation_id}/trajectory`.

See also:
- `skills/openhands_api/references/README.md` (API docs pointers)
- `skills/openhands_api/scripts/openhands_api.py` and `skills/openhands_api/scripts/openhands_api.ts`
