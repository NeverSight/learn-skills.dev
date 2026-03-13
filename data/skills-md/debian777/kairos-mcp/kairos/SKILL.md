---
name: kairos
description: >-
  Run KAIROS protocols. Use when the user invokes /k, /apply, or /search; the
  query is everything after the trigger word. Use when the user wants to run a
  protocol, execute a KAIROS workflow, or work in a KAIROS repo. For first-time
  install and server setup, use the kairos-install skill instead.
---

# kairos

**Protocol execution only.** For installing KAIROS (minimal Docker + .env and MCP config), use the **kairos-install** skill.

When the user wants to run a protocol (e.g. after /k, /apply, /search or when the context implies a KAIROS workflow):

1. Use the KAIROS tool `kairos_search` with the query: everything that comes after `/k`, `/apply`, or `/search` (or the user's stated goal).
2. Choose the protocol that matches the user request.
3. Follow the protocol to the letter: `kairos_begin` → `kairos_next` (until `next_action` directs to attest) → `kairos_attest`. Echo nonces and proof hashes from the server; never compute them yourself.
