---
name: messages
description: Use when sending requests or replies, subscribing to channels, or recovering queued and dead-lettered Tariboy messages.
---

# Tariboy Messages

**REQUIRED:** Use `cli-text` before passing text to this CLI. Keep the storage
rules below; quote transport separately. Resolve skill-local launchers relative
to this skill directory, not the current working directory.

This skill's `scripts/messages.sh` launcher lives inside this skill directory
and calls the identity-bound daemon through `TARIBOY_TOOLS_SOCKET`.
Execute the launcher when command execution is available. If it is unavailable,
return the exact command instead; never claim a message was sent or handled
unless the command succeeded.

Other agents, plugins, and external sources reach you over named channels.
Incoming messages arrive inline in the iteration prompt, batched per iteration,
and each carries its own ID. You must close every message you were handed:
unprocessed messages are redelivered in the next iteration. Act on each, then
close it with `scripts/messages.sh message processed <id> "<result>"`;
`scripts/messages.sh message reply <id> "<body>"` replies and closes it atomically.

- Notify: `scripts/messages.sh message send --channel <name> --text <body>`
- Request a reply: `scripts/messages.sh request --channel <name> --text <body> [--deadline 5m]`
- Inspect/recover: `scripts/messages.sh message ls [--all]`,
  `scripts/messages.sh message dlq`, `scripts/messages.sh message dlq requeue <id>`
- Subscribe: inspect `scripts/messages.sh sources`, then use
  `scripts/messages.sh channel subscribe`, `scripts/messages.sh channel ls`, or
  `scripts/messages.sh channel unsubscribe`.

Use matchers to narrow existing channel traffic. Use params only when a provider
must produce data for the subscription.
