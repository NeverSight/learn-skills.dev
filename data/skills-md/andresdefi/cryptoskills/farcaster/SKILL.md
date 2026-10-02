---
name: farcaster
description: "Onchain social protocol with Neynar API, Frames v2 Mini Apps, and transaction frames. Covers Snapchain architecture, FID registry on OP Mainnet, and Warpcast integration."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: Infrastructure
tags:
  - farcaster
  - neynar
  - frames
  - mini-apps
  - social
  - social-graph
  - warpcast
  - op-mainnet
  - snapchain
---

# Farcaster

Farcaster is a sufficiently decentralized social protocol. Users register onchain identities (FIDs) on OP Mainnet and publish social data (casts, reactions, links) as offchain messages to Snapchain, a purpose-built message ordering layer. Neynar provides the primary API infrastructure and, since January 2026, owns the Farcaster protocol itself. Frames v2 (Mini Apps) enable full-screen interactive web applications embedded inside Farcaster clients like Warpcast.

## What You Probably Got Wrong

- **Manifest `accountAssociation` domain MUST exactly match the FQDN where `/.well-known/farcaster.json` is hosted.** A mismatch causes silent failure -- the Mini App will not load, no error is surfaced to the developer, and Warpcast simply shows nothing. The domain in the signature payload must be byte-identical to the hosting domain (no trailing slash, no protocol prefix, no port unless non-standard).

- **Neynar webhooks MUST be verified via HMAC-SHA512 at write time.** Check the `X-Neynar-Signature` header against the raw request body. Never parse JSON before verification -- you must verify the raw bytes.

```typescript
import crypto from "node:crypto";
import type { IncomingHttpHeaders } from "node:http";

function verifyNeynarWebhook(
  rawBody: Buffer,
  headers: IncomingHttpHeaders,
  webhookSecret: string
): boolean {
  const signature = headers["x-neynar-signature"];
  if (typeof signature !== "string") return false;

  const hmac = crypto.createHmac("sha512", webhookSecret);
  hmac.update(rawBody);
  const computedSignature = hmac.digest("hex");

  return crypto.timingSafeEqual(
    Buffer.from(signature, "hex"),
    Buffer.from(computedSignature, "hex")
  );
}
```

- **Farcaster is NOT a blockchain.** It is a social protocol with an onchain registry (OP Mainnet) for identity and key management, plus an offchain message layer (Snapchain) for social data. Casts, reactions, and follows are never posted to any blockchain.

- **FIDs are onchain but casts are NOT.** Farcaster IDs (FIDs) live in the IdRegistry contract on OP Mainnet. Casts, reactions, and link messages are stored on Snapchain and are not onchain data.

- **Frames v2 is NOT Frames v1 -- completely different spec.** Frames v1 used static OG images with action buttons and server-side rendering. Frames v2 (Mini Apps) are full-screen interactive web applications loaded in an iframe with SDK access to wallet, user context, and notifications. Do not mix the two APIs.

- **Neynar is NOT just an API provider.** Neynar acquired Farcaster from Merkle Manufactory in January 2026. Neynar now owns and operates the protocol, the Snapchain infrastructure, and the primary API layer.

- **Frame images must be static.** Frame preview images (OG images shown in feed) cannot contain JavaScript. They are rendered as static images by the client. Interactive behavior only works inside the launched Mini App.

- **`@farcaster/frame-sdk` and `@farcaster/miniapp-sdk` are converging.** Both packages exist but `frame-sdk` is the current stable package for Frames v2. Check import paths -- functionality overlaps but the packages are not yet unified.

- **Farcaster timestamps use a custom epoch.** Timestamps are seconds since January 1, 2021 00:00:00 UTC (Farcaster epoch), not Unix epoch. To convert: `unixTimestamp = farcasterTimestamp + 1609459200`.

- **Cast text has a 1024 BYTE limit, not characters.** UTF-8 multibyte characters (emoji, CJK, accented characters) consume 2-4 bytes each. A 1024-character cast with emoji will exceed the limit.

- **Warpcast aggressively caches OG/frame images.** Changing content at the same URL will not update the preview in Warpcast feeds. Use cache-busting query parameters or new URLs when updating frame images.

## Critical Context

Neynar acquired Farcaster from Merkle Manufactory in January 2026. This means:

- Neynar operates the protocol, Snapchain validators, and the Hub network
- The Neynar API is the canonical way to interact with Farcaster
- Warpcast remains the primary client, now under Neynar's umbrella
- The open-source protocol spec and hub software remain MIT-licensed
- Third-party hubs can still run, but Neynar controls the reference implementation

## Protocol Architecture

### Snapchain

Snapchain replaced the Hub network in April 2025 as Farcaster's offchain message ordering layer.

| Property | Detail |
|----------|--------|
| Consensus | Malachite BFT (Tendermint-derived) |
| Throughput | 10,000+ messages per second |
| Sharding | Account-level -- each FID's messages are ordered independently |
| Finality | Sub-second for message acceptance |
| Data model | Append-only log of signed messages per FID |
| Validator set | Operated by Neynar (post-acquisition) |

Messages on Snapchain are CRDTs (Conflict-free Replicated Data Types). Each message type has merge rules that ensure consistency across nodes without coordination:

- **CastAdd** conflicts with a later **CastRemove** for the same hash -- remove wins
- **ReactionAdd** conflicts with **ReactionRemove** for the same target -- last-write-wins by timestamp
- **LinkAdd** conflicts with **LinkRemove** -- last-write-wins by timestamp

### Message Structure

Every Farcaster message is an Ed25519-signed protobuf:

```
MessageData {
  type: MessageType     // CAST_ADD, REACTION_ADD, LINK_ADD, etc.
  fid: uint64           // Farcaster ID of the author
  timestamp: uint32     // Farcaster epoch seconds
  network: Network      // MAINNET = 1
  body: MessageBody     // Type-specific payload
}

Message {
  data: MessageData
  hash: bytes           // Blake3 hash of serialized MessageData
  hash_scheme: BLAKE3
  signature: bytes      // Ed25519 signature over hash
  signature_scheme: ED25519
  signer: bytes         // Public key of the signer (app key)
}
```

## Onchain Registry (OP Mainnet)

Farcaster's onchain contracts manage identity, keys, and storage on OP Mainnet.

> **Last verified:** March 2026

| Contract | Address | Purpose |
|----------|---------|---------|
| IdRegistry | `0x00000000Fc6c5F01Fc30151999387Bb99A9f489b` | Maps FIDs to custody addresses |
| KeyRegistry | `0x00000000Fc1237824fb747aBDE0FF18990E59b7e` | Maps FIDs to Ed25519 app keys (signers) |
| StorageRegistry | `0x00000000FcCe7f938e7aE6D3c335bD6a1a7c593D` | Manages storage units per FID |
| IdGateway | `0x00000000Fc25870C6eD6b6c7E41Fb078b7656f69` | Permissioned FID registration entry point |
| KeyGateway | `0x00000000fC56947c7E7183f8Ca4B62398CaaDF0B` | Permissioned key addition entry point |
| Bundler | `0x00000000FC04c910A0b5feA33b03E0447ad0B0aA` | Batches register + addKey + rent in one tx |

```bash
# Verify IdRegistry is deployed on OP Mainnet
cast code 0x00000000Fc6c5F01Fc30151999387Bb99A9f489b --rpc-url https://mainnet.optimism.io

# Look up custody address for an FID
cast call 0x00000000Fc6c5F01Fc30151999387Bb99A9f489b \
  "custodyOf(uint256)(address)" 3 \
  --rpc-url https://mainnet.optimism.io
```

### Registration Flow

```
1. User calls IdGateway.register() or Bundler.register()
   -> IdRegistry assigns next sequential FID to custody address
       |
2. User (or Bundler) calls KeyGateway.add()
   -> KeyRegistry maps FID to an Ed25519 public key (app key / signer)
       |
3. User (or Bundler) calls StorageRegistry.rent()
   -> Allocates storage units (each unit = 5,000 casts, 2,500 reactions, 2,500 links)
       |
4. App key can now sign Farcaster messages on behalf of the FID
```

## Farcaster IDs (FIDs)

Every Farcaster user has an FID -- a sequentially assigned `uint256` stored in IdRegistry on OP Mainnet.

| Concept | Description |
|---------|-------------|
| FID | The user's numeric identity, immutable once assigned |
| Custody address | The Ethereum address that owns the FID -- can transfer ownership |
| App key (signer) | Ed25519 key pair registered in KeyRegistry -- signs messages |
| Recovery address | Can initiate FID recovery if custody address is compromised |

An FID can have multiple app keys. Each app (Warpcast, third-party client) registers its own app key via KeyGateway. The custody address can revoke any app key by calling KeyRegistry.remove().

## Neynar API v2

Neynar provides the primary API for reading and writing Farcaster data. Current SDK version: `@neynar/nodejs-sdk` v3.131.0.

### Setup

```bash
npm install @neynar/nodejs-sdk
```

```typescript
import { NeynarAPIClient, Configuration } from "@neynar/nodejs-sdk";

const config = new Configuration({
  apiKey: process.env.NEYNAR_API_KEY,
});

const neynar = new NeynarAPIClient(config);
```

### Fetch User by FID

```typescript
const { users } = await neynar.fetchBulkUsers({ fids: [3] });
const user = users[0];
console.log(user.username, user.display_name, user.follower_count);
```

### Publish a Cast

```typescript
const response = await neynar.publishCast({
  signerUuid: process.env.SIGNER_UUID,
  text: "Hello from Neynar SDK",
});
console.log(response.cast.hash);
```

### Fetch Feed

```typescript
const feed = await neynar.fetchFeed({
  feedType: "following",
  fid: 3,
  limit: 25,
});

for (const cast of feed.casts) {
  console.log(`@${cast.author.username}: ${cast.text}`);
}
```

### Search Users

```typescript
const result = await neynar.searchUser({ q: "vitalik", limit: 5 });
for (const user of result.result.users) {
  console.log(`FID ${user.fid}: @${user.username}`);
}
```

### Fetch Cast by Hash

```typescript
const { cast } = await neynar.lookupCastByHashOrWarpcastUrl({
  identifier: "0xfe90f9de682273e05b201629ad2338bdcd89b6be",
  type: "hash",
});
console.log(cast.text, cast.reactions.likes_count);
```

### Webhook Configuration

Create webhooks in the Neynar dashboard or via API. Webhooks fire on cast creation, reaction events, follow events, and more.

```typescript
import express from "express";
import crypto from "node:crypto";

const app = express();

// Raw body is required for signature verification
app.use("/webhook", express.raw({ type: "application/json" }));

app.post("/webhook", (req, res) => {
  const rawBody = req.body as Buffer;
  const signature = req.headers["x-neynar-signature"] as string;

  if (!signature) {
    res.status(401).json({ error: "Missing signature" });
    return;
  }

  const hmac = crypto.createHmac("sha512", process.env.NEYNAR_WEBHOOK_SECRET!);
  hmac.update(rawBody);
  const computed = hmac.digest("hex");

  const isValid = crypto.timingSafeEqual(
    Buffer.from(signature, "hex"),
    Buffer.from(computed, "hex")
  );

  if (!isValid) {
    res.status(401).json({ error: "Invalid signature" });
    return;
  }

  const event = JSON.parse(rawBody.toString("utf-8"));
  console.log("Verified webhook event:", event.type);

  res.status(200).json({ status: "ok" });
});

app.listen(3001, () => console.log("Webhook listener on :3001"));
```

## Frames v2 / Mini Apps

Frames v2 are full-screen interactive web applications embedded inside Farcaster clients. They replaced the static image + button model of Frames v1 with a rich SDK-powered experience.

### Manifest (`/.well-known/farcaster.json`)

Every Mini App must serve a manifest at `/.well-known/farcaster.json` on its domain:

```json
{
  "accountAssociation": {
    "header": "eyJmaWQiOjM...",
    "payload": "eyJkb21haW4iOiJleGFtcGxlLmNvbSJ9",
    "signature": "abc123..."
  },
  "frame": {
    "version": "1",
    "name": "My Mini App",
    "iconUrl": "https://example.com/icon.png",
    "homeUrl": "https://example.com/app",
    "splashImageUrl": "https://example.com/splash.png",
    "splashBackgroundColor": "#1a1a2e",
    "webhookUrl": "https://example.com/api/webhook"
  }
}
```

The `accountAssociation` proves that the FID owner controls the domain. The `payload` decoded is `{"domain":"example.com"}` -- this domain MUST match the FQDN hosting the manifest file.

### Meta Tags

Add these to your app's HTML `<head>` for Farcaster clients to discover the Mini App:

```html
<meta name="fc:frame" content='{"version":"next","imageUrl":"https://example.com/og.png","button":{"title":"Launch App","action":{"type":"launch_frame","name":"My App","url":"https://example.com/app","splashImageUrl":"https://example.com/splash.png","splashBackgroundColor":"#1a1a2e"}}}' />
```

### Frame SDK Setup

```bash
npm install @farcaster/frame-sdk
```

```typescript
import sdk from "@farcaster/frame-sdk";

async function initMiniApp() {
  const context = await sdk.context;

  // context.user contains the viewing user's FID, username, pfpUrl
  console.log(`User FID: ${context.user.fid}`);
  console.log(`Username: ${context.user.username}`);

  // Signal to the client that the app is ready to render
  sdk.actions.ready();
}

initMiniApp();
```

### SDK Actions

```typescript
// Open an external URL in the client's browser
sdk.actions.openUrl("https://example.com");

// Close the Mini App
sdk.actions.close();

// Compose a cast with prefilled text
sdk.actions.composeCast({
  text: "Check out this Mini App!",
  embeds: ["https://example.com/app"],
});

// Add a Mini App to the user's favorites (prompts confirmation)
sdk.actions.addFrame();
```

## Transaction Frames

Mini Apps can trigger onchain transactions through the embedded wallet provider. The SDK exposes an EIP-1193 provider that connects to the user's wallet in the Farcaster client.

### Wallet Provider Setup

```typescript
import sdk from "@farcaster/frame-sdk";
import { createWalletClient, custom, parseEther, type Address } from "viem";
import { base } from "viem/chains";

async function sendTransaction() {
  const context = await sdk.context;

  const provider = sdk.wallet.ethProvider;

  const walletClient = createWalletClient({
    chain: base,
    transport: custom(provider),
  });

  const [address] = await walletClient.requestAddresses();

  const hash = await walletClient.sendTransaction({
    account: address,
    to: "0xRecipient..." as Address,
    value: parseEther("0.001"),
  });

  return hash;
}
```

### With Wagmi Connector

For apps using wagmi, wrap the SDK's provider as a connector:

```typescript
import sdk from "@farcaster/frame-sdk";
import { createConfig, http, useConnect, useSendTransaction } from "wagmi";
import { base } from "wagmi/chains";
import { farcasterFrame } from "@farcaster/frame-wagmi-connector";

const config = createConfig({
  chains: [base],
  transports: {
    [base.id]: http(),
  },
  connectors: [farcasterFrame()],
});

// In your React component:
function MintButton() {
  const { connect, connectors } = useConnect();
  const { sendTransaction } = useSendTransaction();

  async function handleMint() {
    connect({ connector: connectors[0] });
    sendTransaction({
      to: "0xNFTContract..." as `0x${string}`,
      data: "0x...", // mint function calldata
      value: parseEther("0.01"),
    });
  }

  return <button onClick={handleMint}>Mint</button>;
}
```

## Warpcast Deep Links and Cast Intents

### Cast Intent URL

Open Warpcast's compose screen with prefilled content:

```
https://warpcast.com/~/compose?text=Hello%20Farcaster&embeds[]=https://example.com
```

| Parameter | Description |
|-----------|-------------|
| `text` | URL-encoded cast text |
| `embeds[]` | Up to 2 embed URLs |
| `channelKey` | Channel to post in (e.g., `farcaster`) |

### Deep Links

```
# Open a user's profile
https://warpcast.com/<username>

# Open a specific cast
https://warpcast.com/<username>/<cast-hash>

# Open a channel
https://warpcast.com/~/channel/<channel-id>

# Open direct cast composer
https://warpcast.com/~/inbox/create/<fid>
```

## Channels

Channels are topic-based feeds identified by a `parent_url`. A cast is posted to a channel by setting its `parent_url` to the channel's URL.

```typescript
// Post a cast to the "ethereum" channel
const response = await neynar.publishCast({
  signerUuid: process.env.SIGNER_UUID,
  text: "Pectra upgrade is live!",
  channelId: "ethereum",
});
```

### Channel Lookup

```typescript
const channel = await neynar.lookupChannel({ id: "farcaster" });
console.log(channel.channel.name, channel.channel.follower_count);
```

### Channel Feed

```typescript
const feed = await neynar.fetchFeed({
  feedType: "filter",
  filterType: "channel_id",
  channelId: "ethereum",
  limit: 25,
});
```

## Neynar API Pricing

> Current as of March 2026

| Plan | Monthly Credits | Price | Webhooks | Rate Limit |
|------|----------------|-------|----------|------------|
| Free | 100K | $0 | 1 | 5 req/s |
| Starter | 1M | $49/mo | 5 | 20 req/s |
| Growth | 10M | $249/mo | 25 | 50 req/s |
| Scale | 60M | $899/mo | 100 | 200 req/s |
| Enterprise | Custom | Custom | Unlimited | Custom |

Credit costs vary by endpoint. Read operations (user lookup, feed) cost 1-5 credits. Write operations (publish cast, react) cost 10-50 credits. Webhook deliveries are free but count against webhook limits.

## Hub / Snapchain Endpoints

Direct hub access for reading raw Farcaster data without the Neynar API abstraction.

| Provider | Endpoint | Auth |
|----------|----------|------|
| Neynar Hub API | `hub-api.neynar.com` | API key in `x-api-key` header |
| Self-hosted Hub | `localhost:2283` | None (local) |

### Hub HTTP API Examples

```bash
# Get casts by FID
curl -H "x-api-key: $NEYNAR_API_KEY" \
  "https://hub-api.neynar.com/v1/castsByFid?fid=3&pageSize=10"

# Get user data (display name, bio, pfp)
curl -H "x-api-key: $NEYNAR_API_KEY" \
  "https://hub-api.neynar.com/v1/userDataByFid?fid=3"

# Get reactions by FID
curl -H "x-api-key: $NEYNAR_API_KEY" \
  "https://hub-api.neynar.com/v1/reactionsByFid?fid=3&reactionType=1"
```

### Hub gRPC API

```bash
# Install hubble CLI
npm install -g @farcaster/hubble

# Query via gRPC
hubble --insecure -r hub-api.neynar.com:2283 getCastsByFid --fid 3
```

## Farcaster Epoch Conversion

```typescript
// Farcaster epoch: January 1, 2021 00:00:00 UTC
const FARCASTER_EPOCH = 1609459200;

function farcasterTimestampToUnix(farcasterTs: number): number {
  return farcasterTs + FARCASTER_EPOCH;
}

function unixToFarcasterTimestamp(unixTs: number): number {
  return unixTs - FARCASTER_EPOCH;
}

function farcasterTimestampToDate(farcasterTs: number): Date {
  return new Date((farcasterTs + FARCASTER_EPOCH) * 1000);
}
```

## Related Skills

- **viem** -- Used for onchain interactions with Farcaster registry contracts on OP Mainnet and for building transaction frames with the wallet provider
- **wagmi** -- React hooks for wallet connection in Mini Apps via the `@farcaster/frame-wagmi-connector`
- **x402** -- Payment protocol that can be integrated with Farcaster Mini Apps for paywalled content

## References

- [Farcaster Protocol Spec](https://github.com/farcasterxyz/protocol)
- [Farcaster Frames v2 Spec](https://docs.farcaster.xyz/developers/frames/v2/spec)
- [Neynar API Docs](https://docs.neynar.com)
- [Neynar Node.js SDK](https://github.com/neynar/nodejs-sdk)
- [`@farcaster/frame-sdk` (npm)](https://www.npmjs.com/package/@farcaster/frame-sdk)
- [Farcaster Contracts (GitHub)](https://github.com/farcasterxyz/contracts)
- [Warpcast](https://warpcast.com)
- [Farcaster IdRegistry (OP Mainnet)](https://optimistic.etherscan.io/address/0x00000000Fc6c5F01Fc30151999387Bb99A9f489b)
- [Snapchain Architecture](https://github.com/farcasterxyz/snapchain)
