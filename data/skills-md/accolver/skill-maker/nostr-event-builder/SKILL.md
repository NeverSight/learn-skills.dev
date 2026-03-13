---
name: nostr-event-builder
description: Use when constructing Nostr events from natural language descriptions, building kind-specific tag structures, implementing NIP-10 threading for kind:1 replies, creating NIP-22 comments on non-note content, or generating correct event JSON with proper e/p/a tag markers and serialization format.
---

# Nostr Event Builder

## Overview

Construct correct Nostr event structures from natural language descriptions.
This skill handles the non-obvious parts: choosing the right kind, building
proper tag arrays with correct markers, enforcing NIP-10 vs NIP-22 threading
rules, and producing valid event JSON ready for signing.

## When to Use

- Developer describes what they want to publish on Nostr
- Building reply threads (NIP-10 kind:1 replies)
- Commenting on non-note content (NIP-22 kind:1111 comments)
- Creating or updating user profiles (kind:0 metadata)
- Constructing any Nostr event and unsure about tag structure
- Debugging malformed events (wrong markers, missing tags)

**Do NOT use when:**

- Implementing relay WebSocket logic (that's relay protocol, not event building)
- Working with NIP-19 encoding/decoding (bech32 concerns, not event structure)
- Building subscription filters (REQ messages, not EVENT messages)

## Workflow

### 1. Identify the Event Kind

Ask: "What is the developer trying to publish?"

| Intent                        | Kind  | Category    | Key NIP |
| ----------------------------- | ----- | ----------- | ------- |
| Post a short text note        | 1     | Regular     | NIP-10  |
| Reply to a kind:1 note        | 1     | Regular     | NIP-10  |
| Comment on non-kind:1 content | 1111  | Regular     | NIP-22  |
| Set/update user profile       | 0     | Replaceable | NIP-01  |
| Update follow list            | 3     | Replaceable | NIP-02  |
| Delete events                 | 5     | Regular     | NIP-09  |
| Repost a note                 | 6     | Regular     | NIP-18  |
| React to an event             | 7     | Regular     | NIP-25  |
| Publish a long-form article   | 30023 | Addressable | NIP-23  |

See [references/event-kinds.md](references/event-kinds.md) for full
kind-to-structure mapping.

**Critical routing rule:**

```
Is the target a kind:1 note?
  YES → Use kind:1 reply with NIP-10 e-tag markers
  NO  → Use kind:1111 comment with NIP-22 uppercase/lowercase tags
```

### 2. Build the Tag Array

Tags are the hardest part. Follow the tag guide for your kind:

**For kind:1 replies (NIP-10):**

Direct reply to root (no intermediate replies):

```json
{
  "kind": 1,
  "tags": [
    ["e", "<root-event-id>", "<relay-url>", "root", "<root-author-pubkey>"],
    ["p", "<root-author-pubkey>"]
  ],
  "content": "Your reply text"
}
```

Reply to a reply in a thread:

```json
{
  "kind": 1,
  "tags": [
    ["e", "<root-event-id>", "<relay-url>", "root", "<root-author-pubkey>"],
    [
      "e",
      "<parent-event-id>",
      "<relay-url>",
      "reply",
      "<parent-author-pubkey>"
    ],
    ["p", "<root-author-pubkey>"],
    ["p", "<parent-author-pubkey>"]
  ],
  "content": "Your reply text"
}
```

**For kind:1111 comments (NIP-22):**

Top-level comment on a regular event:

```json
{
  "kind": 1111,
  "tags": [
    ["E", "<root-event-id>", "<relay-url>", "<root-author-pubkey>"],
    ["K", "<root-event-kind>"],
    ["P", "<root-author-pubkey>", "<relay-url>"],
    ["e", "<root-event-id>", "<relay-url>", "<root-author-pubkey>"],
    ["k", "<root-event-kind>"],
    ["p", "<root-author-pubkey>", "<relay-url>"]
  ],
  "content": "Your comment text"
}
```

Top-level comment on an addressable event (kind 30000-39999):

```json
{
  "kind": 1111,
  "tags": [
    ["A", "<kind>:<pubkey>:<d-tag>", "<relay-url>"],
    ["K", "<root-event-kind>"],
    ["P", "<root-author-pubkey>", "<relay-url>"],
    ["a", "<kind>:<pubkey>:<d-tag>", "<relay-url>"],
    ["e", "<event-id>", "<relay-url>"],
    ["k", "<root-event-kind>"],
    ["p", "<root-author-pubkey>", "<relay-url>"]
  ],
  "content": "Your comment text"
}
```

Comment on a URL or external identifier:

```json
{
  "kind": 1111,
  "tags": [
    ["I", "<url-or-identifier>"],
    ["K", "<identifier-type>"],
    ["i", "<url-or-identifier>"],
    ["k", "<identifier-type>"]
  ],
  "content": "Your comment text"
}
```

Reply to an existing comment:

```json
{
  "kind": 1111,
  "tags": [
    ["E", "<original-root-event-id>", "<relay-url>", "<root-author-pubkey>"],
    ["K", "<original-root-kind>"],
    ["P", "<root-author-pubkey>"],
    [
      "e",
      "<parent-comment-id>",
      "<relay-url>",
      "<parent-comment-author-pubkey>"
    ],
    ["k", "1111"],
    ["p", "<parent-comment-author-pubkey>"]
  ],
  "content": "Your reply to the comment"
}
```

See [references/tag-guide.md](references/tag-guide.md) for complete tag
semantics.

### 3. Set the Content Field

Content format depends on the kind:

| Kind  | Content Format                                                   |
| ----- | ---------------------------------------------------------------- |
| 0     | Stringified JSON: `{"name":"...","about":"...","picture":"..."}` |
| 1     | Plaintext (no markdown, no HTML)                                 |
| 5     | Optional deletion reason text                                    |
| 6     | Stringified JSON of the reposted event                           |
| 7     | `+` (like), `-` (dislike), or emoji                              |
| 1111  | Plaintext comment                                                |
| 30023 | Markdown-formatted article body                                  |

### 4. Construct the Complete Event

Assemble the unsigned event object:

```json
{
  "pubkey": "<32-bytes-lowercase-hex-public-key>",
  "created_at": "<unix-timestamp-seconds>",
  "kind": "<integer>",
  "tags": [["..."]],
  "content": "<string>"
}
```

The `id` is computed as SHA-256 of the serialized form:

```json
[0, "<pubkey>", <created_at>, <kind>, <tags>, "<content>"]
```

Serialization rules:

- UTF-8 encoding, no whitespace/formatting
- Escape in content: `\n`, `\"`, `\\`, `\r`, `\t`, `\b`, `\f`
- All other characters verbatim

The `sig` is a Schnorr signature (secp256k1) of the `id`.

### 5. Validate Before Signing

Checklist before the event is ready:

- [ ] `kind` is correct for the intent
- [ ] All required tags present for this kind
- [ ] `e` tags have correct markers (`root`/`reply` for kind:1)
- [ ] `p` tags include ALL participants in the thread
- [ ] NIP-10 kind:1 replies only target other kind:1 events
- [ ] NIP-22 kind:1111 comments do NOT target kind:1 events
- [ ] `K` and `k` tags present for kind:1111 comments
- [ ] Uppercase tags (E/A/I/K/P) point to root scope in kind:1111
- [ ] Lowercase tags (e/a/i/k/p) point to parent item in kind:1111
- [ ] `content` format matches the kind's requirements
- [ ] `created_at` is a Unix timestamp in seconds (not milliseconds)
- [ ] All hex values are 32-byte lowercase

## Common Mistakes

| Mistake                                             | Why It Breaks                                                | Fix                                                                |
| --------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------ |
| Using kind:1 to reply to a kind:30023 article       | NIP-10 kind:1 replies MUST only reply to other kind:1 events | Use kind:1111 (NIP-22 comment) for non-kind:1 targets              |
| Using kind:1111 to reply to a kind:1 note           | NIP-22 comments MUST NOT reply to kind:1                     | Use kind:1 with NIP-10 e-tag markers                               |
| Missing `root` marker on e tags in kind:1           | Clients can't reconstruct the thread tree                    | Always use marked e tags: `["e", "<id>", "<relay>", "root"]`       |
| Only one e tag with `reply` marker (no `root`)      | Direct replies to root need `root` marker, not `reply`       | Single e tag = use `root` marker only                              |
| Missing p tags for thread participants              | Users don't get notified of replies                          | Include p tags for ALL pubkeys in the thread                       |
| Lowercase e/k/p tags for root scope in kind:1111    | Root scope MUST use uppercase E/K/P tags                     | Uppercase = root scope, lowercase = parent item                    |
| Missing K or k tags in kind:1111                    | Both are REQUIRED by NIP-22                                  | Always include `["K", "<root-kind>"]` and `["k", "<parent-kind>"]` |
| `created_at` in milliseconds                        | Nostr uses seconds, not milliseconds                         | Use `Math.floor(Date.now() / 1000)`                                |
| Content as object instead of string for kind:0      | Content must be stringified JSON                             | Use `JSON.stringify({name: "...", ...})`                           |
| Missing `d` tag on addressable events (30000-39999) | Relay can't address the event properly                       | Always include `["d", "<identifier>"]`                             |
| Positional e tags without markers                   | Deprecated; creates ambiguity in thread reconstruction       | Always use marked e tags with `root`/`reply`                       |

## Kind Category Quick Reference

| Range                 | Category    | Behavior                          |
| --------------------- | ----------- | --------------------------------- |
| 1000-9999, 4-44, 1, 2 | Regular     | Stored by relays, all kept        |
| 10000-19999, 0, 3     | Replaceable | Latest per pubkey+kind kept       |
| 20000-29999           | Ephemeral   | Not stored by relays              |
| 30000-39999           | Addressable | Latest per pubkey+kind+d-tag kept |

## Example: Complete Event Construction

**User says:** "I want to reply to my friend's note in an existing thread"

**Step 1 — Identify kind:** Replying to a kind:1 note → use kind:1 (NIP-10)

**Step 2 — Determine thread position:** This is a reply to a reply (not the
root), so we need both `root` and `reply` e tags.

**Step 3 — Build the event:**

```json
{
  "pubkey": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
  "created_at": 1709827200,
  "kind": 1,
  "tags": [
    ["e", "aaa111...", "wss://relay.example.com", "root", "f7234bd4..."],
    ["e", "bbb222...", "wss://relay.example.com", "reply", "93ef2eba..."],
    ["p", "f7234bd4...", "wss://relay.example.com"],
    ["p", "93ef2eba...", "wss://relay.example.com"]
  ],
  "content": "Great point! I totally agree with this take."
}
```

**Step 4 — Validate:** Root e tag has `root` marker ✓, reply e tag has `reply`
marker ✓, p tags include both the root author and the parent author ✓, content
is plaintext ✓.
