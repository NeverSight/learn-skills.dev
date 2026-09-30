---
name: computer
description: Computer connector for exposing local services to remote sandboxes via
  authenticated ngrok tunnels. Use when user mentions "computer use", "tunnel",
  "ngrok", "expose local", or needs to bridge local services to a sandbox.
---

## Environment Variables

- `COMPUTER_CONNECTOR_BRIDGE_TOKEN` — Authentication token for the ngrok bridge
- `COMPUTER_CONNECTOR_DOMAIN` — Tunnel domain for routing traffic
