---
name: nostr-social-graph
description: Build and traverse Nostr social graphs including follow lists (kind:3, NIP-02), relay list metadata (kind:10002, NIP-65), the outbox model for relay-aware event fetching, mute lists (kind:10000), and NIP-51 lists with public and private encrypted items. Use when implementing follow/unfollow, building feeds from followed users, discovering user relays, implementing the outbox model, creating mute or bookmark lists, or working with any NIP-51 list kind.
---

# Nostr Social Graph

## Overview

Build and traverse Nostr social graphs: follow lists, relay discovery, the
outbox model, and NIP-51 lists. This skill handles the non-obvious parts —
correct tag structures for each list kind, the outbox model's read/write relay
routing, private list item encryption, and efficient graph traversal patterns.

## When to Use

- Building follow/unfollow functionality (kind:3)
- Implementing a feed that fetches posts from followed users
- Discovering where a user publishes or reads (kind:10002)
- Implementing the outbox model for relay-aware fetching
- Creating mute lists, bookmark lists, or pin lists (NIP-51)
- Building lists with private encrypted entries
- Traversing the social graph (follows-of-follows, Web of Trust)
- Working with follow sets (kind:30000) or relay sets (kind:30002)

**Do NOT use when:**

- Building individual events like notes or replies (use nostr-event-builder)
- Implementing relay WebSocket protocol logic
- Working with NIP-19 encoding/decoding
- Building subscription filters (REQ messages)

## Workflow

### 1. Identify the List Kind

Ask: "What social graph data is the developer working with?"

| Intent                      | Kind  | Category    | NIP    |
| --------------------------- | ----- | ----------- | ------ |
| Follow/unfollow users       | 3     | Replaceable | NIP-02 |
| Mute users, words, hashtags | 10000 | Replaceable | NIP-51 |
| Pin notes to profile        | 10001 | Replaceable | NIP-51 |
| Advertise read/write relays | 10002 | Replaceable | NIP-65 |
| Bookmark events             | 10003 | Replaceable | NIP-51 |
| Set DM relay preferences    | 10050 | Replaceable | NIP-51 |
| Categorized follow groups   | 30000 | Addressable | NIP-51 |
| User-defined relay groups   | 30002 | Addressable | NIP-51 |

See [references/list-kinds.md](references/list-kinds.md) for all list kinds with
full tag structures.

### 2. Build the Event Structure

#### Follow List (Kind:3)

```json
{
  "kind": 3,
  "tags": [
    ["p", "<pubkey-hex>", "<relay-url>", "<petname>"],
    ["p", "<pubkey-hex>", "<relay-url>"],
    ["p", "<pubkey-hex>"]
  ],
  "content": ""
}
```

Rules:

- **Replaceable**: only the latest kind:3 per pubkey is kept
- Each `p` tag = one followed pubkey
- Relay URL and petname are optional (can be empty string or omitted)
- `content` is empty (historically held relay prefs, now use kind:10002)
- **Append new follows to the end** for chronological ordering
- **Publish the complete list** every time — new event replaces the old one

#### Relay List Metadata (Kind:10002)

```json
{
  "kind": 10002,
  "tags": [
    ["r", "wss://relay.example.com"],
    ["r", "wss://write-only.example.com", "write"],
    ["r", "wss://read-only.example.com", "read"]
  ],
  "content": ""
}
```

Rules:

- **Replaceable**: only the latest kind:10002 per pubkey is kept
- `r` tags with relay URLs
- No marker = both read AND write
- `"read"` marker = read only
- `"write"` marker = write only
- **Keep small**: guide users to 2-4 relays per category
- Spread this event widely for discoverability

#### Mute List (Kind:10000)

```json
{
  "kind": 10000,
  "tags": [
    ["p", "<pubkey-hex>"],
    ["t", "hashtag-to-mute"],
    ["word", "lowercase-word"],
    ["e", "<thread-event-id>"]
  ],
  "content": "<encrypted-private-items-or-empty>"
}
```

Rules:

- Public items go in `tags`
- Private items go in `content` as encrypted JSON
- Supports `p` (pubkeys), `t` (hashtags), `word` (strings), `e` (threads)
- Words should be lowercase for case-insensitive matching

### 3. Handle Private List Items (NIP-51 Encryption)

Any NIP-51 list can have private items. Public items live in `tags`, private
items are encrypted in `content`.

**Encryption process:**

```typescript
// Private items use the same tag structure as public items
const privateItems = [
  ["p", "07caba282f76441955b695551c3c5c742e5b9202a3784780f8086fdcdc1da3a9"],
  ["word", "nsfw"],
];

// Encrypt with NIP-44 using the author's own key pair
// The shared key is computed from author's pubkey + privkey
const encrypted = nip44.encrypt(
  JSON.stringify(privateItems),
  conversationKey(authorPrivkey, authorPubkey),
);

event.content = encrypted;
```

**Decryption and backward compatibility:**

```typescript
function decryptPrivateItems(event, authorPrivkey) {
  if (!event.content || event.content === "") return [];

  // Detect NIP-04 vs NIP-44 by checking for "iv" in ciphertext
  if (event.content.includes("?iv=")) {
    // Legacy NIP-04 format
    return JSON.parse(
      nip04.decrypt(authorPrivkey, authorPubkey, event.content),
    );
  } else {
    // Current NIP-44 format
    return JSON.parse(nip44.decrypt(
      conversationKey(authorPrivkey, authorPubkey),
      event.content,
    ));
  }
}
```

### 4. Implement the Outbox Model

The outbox model is the correct way to route event fetching across relays. See
[references/outbox-model.md](references/outbox-model.md) for the full
explanation.

**Core rules:**

| Action                               | Which relays to use            |
| ------------------------------------ | ------------------------------ |
| Fetch events FROM a user             | That user's WRITE relays       |
| Fetch events ABOUT a user (mentions) | That user's READ relays        |
| Publish your own event               | Your WRITE relays              |
| Notify tagged users                  | Each tagged user's READ relays |
| Spread your kind:10002               | As many relays as viable       |

**Implementation pattern:**

```typescript
async function buildFeedSubscriptions(myFollows: string[]) {
  // Step 1: Fetch kind:10002 for each followed user
  const relayLists = await fetchRelayLists(myFollows);

  // Step 2: Group follows by their WRITE relays
  const relayToUsers = new Map<string, string[]>();
  for (const [pubkey, relays] of relayLists) {
    const writeRelays = getWriteRelays(relays); // "write" or no marker
    for (const relay of writeRelays) {
      if (!relayToUsers.has(relay)) relayToUsers.set(relay, []);
      relayToUsers.get(relay)!.push(pubkey);
    }
  }

  // Step 3: Subscribe to each relay for its relevant users
  for (const [relay, users] of relayToUsers) {
    subscribe(relay, { kinds: [1], authors: users });
  }
}

function getWriteRelays(tags: string[][]): string[] {
  return tags
    .filter((t) => t[0] === "r" && (t.length === 2 || t[2] === "write"))
    .map((t) => t[1]);
}

function getReadRelays(tags: string[][]): string[] {
  return tags
    .filter((t) => t[0] === "r" && (t.length === 2 || t[2] === "read"))
    .map((t) => t[1]);
}
```

### 5. Traverse the Social Graph

**Follows-of-follows (2-hop):**

```typescript
async function getFollowsOfFollows(pubkey: string) {
  // 1. Get direct follows
  const myFollowList = await fetchKind3(pubkey);
  const directFollows = myFollowList.tags
    .filter((t) => t[0] === "p")
    .map((t) => t[1]);

  // 2. Fetch kind:3 for each direct follow
  const secondHop = await Promise.all(
    directFollows.map((pk) => fetchKind3(pk)),
  );

  // 3. Aggregate and rank by frequency
  const scores = new Map<string, number>();
  for (const followList of secondHop) {
    for (const tag of followList.tags.filter((t) => t[0] === "p")) {
      const pk = tag[1];
      if (pk !== pubkey && !directFollows.includes(pk)) {
        scores.set(pk, (scores.get(pk) || 0) + 1);
      }
    }
  }

  return [...scores.entries()].sort((a, b) => b[1] - a[1]);
}
```

**Web of Trust scoring:**

```typescript
function wotScore(
  target: string,
  myFollows: string[],
  followLists: Map<string, string[]>,
): number {
  let score = 0;
  for (const follow of myFollows) {
    const theirFollows = followLists.get(follow) || [];
    if (theirFollows.includes(target)) score++;
  }
  return score; // Higher = more trusted
}
```

### 6. Validate Before Publishing

- [ ] Kind is correct for the list type
- [ ] All tag types are valid for this kind (see list-kinds reference)
- [ ] For kind:3: every entry is a `p` tag with valid 32-byte hex pubkey
- [ ] For kind:10002: every entry is an `r` tag with valid `wss://` URL
- [ ] For kind:10002: markers are only `"read"` or `"write"` (or omitted)
- [ ] For kind:10000: `word` tags use lowercase strings
- [ ] Private items are encrypted with NIP-44 (not NIP-04 for new events)
- [ ] The complete list is published (not just additions/removals)
- [ ] `content` is empty string when no private items exist
- [ ] `created_at` is Unix timestamp in seconds

## Common Mistakes

| Mistake                                              | Why It Breaks                                                                  | Fix                                                                  |
| ---------------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| Publishing only new follows instead of the full list | Kind:3 is replaceable — new event replaces old, so partial list = lost follows | Always publish the complete follow list                              |
| Using kind:3 content for relay preferences           | Deprecated; clients ignore it                                                  | Use kind:10002 for relay list metadata                               |
| Treating unmarked `r` tags as write-only             | No marker means BOTH read and write                                            | `["r", "wss://..."]` = read + write                                  |
| Fetching from a user's READ relays for their posts   | READ relays are where they expect mentions, not where they publish             | Use WRITE relays to fetch a user's own events                        |
| Broadcasting to all known relays                     | Wastes bandwidth, defeats the outbox model                                     | Use targeted relay routing per the outbox model                      |
| Using NIP-04 for new private list items              | NIP-04 is deprecated for this purpose                                          | Use NIP-44 encryption for new events                                 |
| Forgetting to spread kind:10002 widely               | Others can't discover your relays                                              | Publish kind:10002 to well-known indexer relays                      |
| Uppercase words in mute list `word` tags             | Matching should be case-insensitive                                            | Always store words as lowercase                                      |
| Missing relay URL normalization                      | Duplicate relay entries with different formatting                              | Normalize URLs (lowercase host, remove default port, trailing slash) |

## Quick Reference

| Operation      | Kind  | Key Tags                                 | Content                 |
| -------------- | ----- | ---------------------------------------- | ----------------------- |
| Follow user    | 3     | `["p", "<hex>", "<relay>", "<petname>"]` | `""`                    |
| Set relays     | 10002 | `["r", "<url>", "<read\|write>"]`        | `""`                    |
| Mute user/word | 10000 | `["p", "<hex>"]`, `["word", "<str>"]`    | encrypted private items |
| Pin note       | 10001 | `["e", "<event-id>"]`                    | `""`                    |
| Bookmark       | 10003 | `["e", "<id>"]`, `["a", "<coord>"]`      | encrypted private items |
| DM relays      | 10050 | `["relay", "<url>"]`                     | `""`                    |
| Follow set     | 30000 | `["d", "<id>"]`, `["p", "<hex>"]`        | encrypted private items |
| Relay set      | 30002 | `["d", "<id>"]`, `["relay", "<url>"]`    | encrypted private items |

## Key Principles

1. **Replaceable means complete** — Kind:3, 10000, 10001, 10002, 10003 are
   replaceable events. Every publish must contain the FULL list, not just
   changes. The new event completely replaces the old one.

2. **Outbox model is not optional** — Fetching events without consulting
   kind:10002 relay lists leads to missed content and wasted connections. Always
   resolve a user's write relays before fetching their events.

3. **Private items use NIP-44** — New encrypted list content MUST use NIP-44.
   When reading, detect NIP-04 legacy format by checking for `?iv=` in the
   ciphertext and handle both.

4. **Relay lists should be small** — Guide users to 2-4 relays per category
   (read/write). Large relay lists defeat the purpose of targeted routing and
   increase load on the network.

5. **Graph traversal requires relay awareness** — You can't just fetch kind:3
   from one relay. Use the outbox model to find each user's kind:3 on their
   write relays, then use those follow lists to discover the next hop.
