---
name: bsocial
description: This skill should be used when the user asks to "post to BSocial", "like a post", "follow user", "send message", "on-chain social media", "BMAP", "BSocial protocol", "create on-chain post", "read BSocial posts", or needs social operations (posts, likes, follows, messages, reposts, friends) on BSV blockchain.
allowed-tools: "Bash(bun:*)"
---

# BSocial

Complete on-chain social protocol for BSV blockchain. Posts, likes, follows, messages, reposts, and friend requests using BitcoinSchema.org standards.

## When to Use

- Create social content (posts, replies, reposts)
- Social actions (likes, follows, friend requests)
- Real-time messaging (channels, direct messages)
- Query social data by address or transaction

## Create Operations

All create scripts require a funded WIF (Wallet Import Format) private key.

### Post

```bash
bun run skills/bsocial/scripts/create-post.ts <wif> "Post content" [options]

# Options:
#   --channel <name>    Post to a channel
#   --url <url>         Associate with URL
#   --tags <t1,t2>      Comma-separated tags
#   --dry-run           Build tx without broadcasting
```

### Reply

```bash
bun run skills/bsocial/scripts/create-reply.ts <wif> <txid> "Reply content" [--tags <t1,t2>]
```

### Like

```bash
bun run skills/bsocial/scripts/create-like.ts <wif> <txid>
```

### Follow

```bash
bun run skills/bsocial/scripts/create-follow.ts <wif> <bapId>
```

### Repost

```bash
bun run skills/bsocial/scripts/create-repost.ts <wif> <txid> [--context <type> --value <val>]
```

### Message

```bash
bun run skills/bsocial/scripts/create-message.ts <wif> "Message" [options]

# Options:
#   --channel <name>    Send to channel
#   --to <bapId>        Direct message to user
```

### Friend

```bash
bun run skills/bsocial/scripts/create-friend.ts <wif> <bapId>
```

## Read Operations

Query social data from the BMAP API.

### Posts

```bash
bun run skills/bsocial/scripts/read-posts.ts <address> [--limit 20] [--json]
```

### Likes

```bash
bun run skills/bsocial/scripts/read-likes.ts --address <addr>
bun run skills/bsocial/scripts/read-likes.ts --txid <txid>
```

### Follows

```bash
bun run skills/bsocial/scripts/read-follows.ts <address> [--limit 100] [--json]
```

### Messages

```bash
bun run skills/bsocial/scripts/read-messages.ts --channel <name>
bun run skills/bsocial/scripts/read-messages.ts --address <addr>
```

### Friends

```bash
bun run skills/bsocial/scripts/read-friends.ts <address> [--json]
```

## Protocol Stack

```
[B Protocol] | [MAP Protocol] | [AIP Protocol]
   content       metadata         signature
```

- **B Protocol**: Binary content storage (text, media)
- **MAP Protocol**: Metadata key-value pairs (app, type, context)
- **AIP Protocol**: Author signature for verification

## Context Types

| Context | Use Case |
|---------|----------|
| `tx` | Reply/like a transaction |
| `channel` | Post/message to named channel |
| `bapID` | Target specific identity |
| `url` | Associate with external URL |

## Dependencies

- `@bsv/sdk` - Transaction building
- `@bopen-io/templates` - BSocial protocol templates

## API

Base URL: `https://bmap-api-production.up.railway.app`

### REST Endpoints
| Endpoint | Description |
|----------|-------------|
| `/social/post/bap/{bapId}` | Posts by BAP ID |
| `/social/feed/{bapId}` | Feed for BAP ID |
| `/social/post/{txid}/like` | Likes for a post |
| `/social/bap/{bapId}/like` | Likes by user |
| `/social/friend/{bapId}` | Friends for BAP ID |
| `/social/@/{bapId}/messages` | Messages for user |
| `/social/channels/{channelId}/messages` | Channel messages |

### Query API (fallback)
- Query: `/q/{collection}/{base64Query}`
- SSE: `/s/{collection}/{base64Query}`

### Ingest
- POST `/ingest` with `{ rawTx: tx.toHex() }`

## Friend Encryption

Friend requests use Type42 key derivation with BRC-43 invoice numbers (`2-friend-{sha256(friendBapId)}`).

```typescript
import { BAP } from "bsv-bap";

const bap = new BAP({ rootPk: wif });
const identity = bap.getId(bap.listIds()[0]);

// Get encryption pubkey for friend request
const friendPubKey = identity.getEncryptionPublicKeyWithSeed(friendBapId);

// Encrypt private message for friend
const ciphertext = identity.encryptWithSeed("secret message", friendBapId);

// Decrypt message from friend
const plaintext = identity.decryptWithSeed(ciphertext, friendBapId);
```

A CLI is also available: `npm install -g bsv-bap` (see **`create-bap-identity`** skill).

## See Also

- `references/schemas.md` - Full schema reference
- [BitcoinSchema.org](https://bitcoinschema.org) - Protocol specs
