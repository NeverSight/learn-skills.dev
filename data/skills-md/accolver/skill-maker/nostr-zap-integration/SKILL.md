---
name: nostr-zap-integration
description: Implement Lightning Zaps (NIP-57) and Nutzaps (NIP-61) for Nostr applications. Use when building zap request construction (kind:9734), zap receipt validation (kind:9735), LNURL-pay flows, zap splits, Cashu/Nutzap sending (kind:9321), nutzap receiving configuration (kind:10019), or any payment integration between Nostr and Lightning/Cashu.
---

# Nostr Zap Integration

## Overview

Build correct Lightning Zap and Nutzap flows for Nostr applications. This skill
covers the full NIP-57 lifecycle (LNURL discovery, zap request construction,
invoice handling, zap receipt validation) and the NIP-61 Cashu alternative
(nutzap configuration, P2PK token minting, nutzap publishing and redemption).

## When to Use

- Implementing "zap" functionality in a Nostr client
- Constructing kind:9734 zap request events
- Validating kind:9735 zap receipt events
- Integrating LNURL-pay endpoints with Nostr
- Building zap split support for events with multiple `zap` tags
- Implementing NIP-61 Nutzaps (Cashu-based zaps)
- Setting up kind:10019 nutzap receiving configuration
- Constructing kind:9321 nutzap events with P2PK-locked tokens
- Debugging zap flows (missing tags, validation failures, amount mismatches)

**Do NOT use when:**

- Building general Lightning/LNURL wallets unrelated to Nostr
- Implementing relay WebSocket protocol logic
- Working with NIP-19 bech32 encoding (separate concern)
- Building Cashu wallets without Nostr integration

## Workflow

### 1. Determine the Payment Path

Ask: "Is this a Lightning Zap (NIP-57) or a Nutzap (NIP-61)?"

| Path           | When to Use                             | Key Kinds   |
| -------------- | --------------------------------------- | ----------- |
| Lightning Zap  | Recipient has lud16/lud06, LNURL server | 9734, 9735  |
| Nutzap (Cashu) | Recipient has kind:10019, trusted mints | 10019, 9321 |

If unsure, check the recipient's profile (kind:0) for `lud16`/`lud06` fields
(Lightning path) or query for their kind:10019 event (Nutzap path).

### 2. Lightning Zap Flow (NIP-57)

Follow the steps in [references/zap-flow.md](references/zap-flow.md) for the
complete implementation. Summary:

#### Step 2a: Discover the LNURL Endpoint

```typescript
// From lud16 (e.g., "bob@example.com")
const [name, domain] = lud16.split("@");
const url = `https://${domain}/.well-known/lnurlp/${name}`;
const res = await fetch(url);
const lnurlPayData = await res.json();

// Verify Nostr support
if (!lnurlPayData.allowsNostr || !lnurlPayData.nostrPubkey) {
  throw new Error("Recipient does not support Nostr zaps");
}
```

**Critical checks on the LNURL response:**

- `allowsNostr` MUST be `true`
- `nostrPubkey` MUST be a valid 32-byte hex public key
- Save `callback`, `minSendable`, `maxSendable` for later use

#### Step 2b: Construct the Zap Request (kind:9734)

```json
{
  "kind": 9734,
  "content": "Optional zap comment",
  "tags": [
    ["relays", "wss://relay1.example.com", "wss://relay2.example.com"],
    ["amount", "21000"],
    ["lnurl", "lnurl1dp68gurn8ghj7..."],
    ["p", "<recipient-pubkey-hex>"],
    ["e", "<event-id-hex>"],
    ["k", "<event-kind-string>"]
  ]
}
```

**Required tags:** `relays` (list of relay URLs), `p` (recipient pubkey).
**Recommended tags:** `amount` (millisats as string), `lnurl` (bech32-encoded).
**Optional tags:** `e` (event being zapped), `a` (addressable event coordinate),
`k` (kind of zapped event as string).

**Critical:** The zap request is NOT published to relays. It is sent to the
LNURL callback URL.

#### Step 2c: Send to Callback and Get Invoice

```typescript
const zapRequestEncoded = encodeURIComponent(JSON.stringify(signedZapRequest));
const url =
  `${callback}?amount=${amountMsats}&nostr=${zapRequestEncoded}&lnurl=${lnurlBech32}`;
const { pr: invoice } = await fetch(url).then((r) => r.json());
```

#### Step 2d: Pay the Invoice

Pass the bolt11 invoice to a Lightning wallet for payment. After payment, the
recipient's LNURL server creates and publishes the zap receipt (kind:9735).

#### Step 2e: Validate Zap Receipts

See [references/zap-flow.md](references/zap-flow.md) for full validation logic.
The three critical checks:

1. Receipt `pubkey` MUST match the recipient's LNURL `nostrPubkey`
2. Invoice amount in `bolt11` tag MUST match `amount` in the zap request
3. `SHA256(description)` SHOULD match the bolt11 description hash

### 3. Nutzap Flow (NIP-61)

Follow the steps in [references/nutzap-flow.md](references/nutzap-flow.md) for
the complete implementation. Summary:

#### Step 3a: Fetch Recipient's Nutzap Configuration (kind:10019)

```json
{
  "kind": 10019,
  "tags": [
    ["relay", "wss://relay1.example.com"],
    ["relay", "wss://relay2.example.com"],
    ["mint", "https://mint.example.com", "sat"],
    ["mint", "https://othermint.example.com", "usd", "sat"],
    ["pubkey", "<p2pk-pubkey-hex>"]
  ]
}
```

**Critical:** The `pubkey` tag value MUST NOT be the user's main Nostr pubkey.
It is a separate key used exclusively for P2PK locking.

#### Step 3b: Mint P2PK-Locked Tokens

1. Choose a mint from the recipient's `mint` tags
2. Mint or swap tokens P2PK-locked to the recipient's `pubkey` value
3. Prefix the pubkey with `"02"` for nostr-cashu compatibility
4. Include DLEQ proofs (NUT-12)

#### Step 3c: Publish the Nutzap (kind:9321)

```json
{
  "kind": 9321,
  "content": "Optional comment",
  "tags": [
    ["proof", "<cashu-proof-json>"],
    ["unit", "sat"],
    ["u", "https://mint.example.com"],
    ["e", "<zapped-event-id>", "<relay-hint>"],
    ["k", "<zapped-event-kind>"],
    ["p", "<recipient-nostr-pubkey>"]
  ]
}
```

Publish to the relays listed in the recipient's kind:10019 `relay` tags.

#### Step 3d: Receiving Nutzaps

Recipients query for kind:9321 events p-tagging them, filtered by trusted mint
URLs (`#u`). Upon receiving, swap the tokens into their wallet and publish a
kind:7376 redemption event.

### 4. Zap Splits

When an event has `zap` tags, distribute the zap across recipients:

```json
["zap", "<pubkey>", "<relay>", "<weight>"]
```

Weights are relative. Calculate percentages:

```typescript
const totalWeight = zapTags.reduce((sum, t) => sum + Number(t[3] || 0), 0);
for (const tag of zapTags) {
  const weight = Number(tag[3] || 0);
  const pct = weight / totalWeight;
  const recipientAmount = Math.floor(totalAmount * pct);
  // Create separate zap request for each recipient
}
```

Recipients without a weight value get weight 0 (no zap). If no weights are
present on any tag, divide equally.

## Checklist

- [ ] Identified payment path (Lightning vs Nutzap)
- [ ] For Lightning: LNURL endpoint discovered and verified (`allowsNostr`,
      `nostrPubkey`)
- [ ] For Lightning: Zap request (kind:9734) has required tags (`relays`, `p`)
- [ ] For Lightning: Zap request sent to callback URL, NOT published to relays
- [ ] For Lightning: Amount in millisats, within `minSendable`/`maxSendable`
- [ ] For Lightning: Zap receipt validation checks all three criteria
- [ ] For Nutzap: Recipient's kind:10019 fetched and parsed
- [ ] For Nutzap: Tokens minted at one of recipient's listed mints
- [ ] For Nutzap: P2PK pubkey prefixed with "02" and is NOT the main Nostr key
- [ ] For Nutzap: kind:9321 published to recipient's specified relays
- [ ] For splits: Weights calculated correctly, separate zap per recipient

## Common Mistakes

| Mistake                                  | Why It Breaks                                            | Fix                                                    |
| ---------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------ |
| Publishing kind:9734 to relays           | Zap requests are sent to LNURL callback, never published | Send via HTTP GET to callback URL                      |
| Amount in satoshis instead of millisats  | NIP-57 uses millisats (1 sat = 1000 msats)               | Multiply sats by 1000 for the `amount` tag             |
| Using recipient's Nostr pubkey for P2PK  | NIP-61 requires a SEPARATE key for P2PK locking          | Use the `pubkey` from kind:10019, never the main key   |
| Missing `relays` tag on zap request      | LNURL server won't know where to publish the receipt     | Always include at least one relay in `relays` tag      |
| Not validating receipt pubkey            | Fake zap receipts from wrong keys accepted               | Receipt pubkey MUST match LNURL `nostrPubkey`          |
| Sending nutzap to unlisted mint          | Recipient may never see it; tokens could be lost         | Only use mints from recipient's kind:10019 `mint` tags |
| Missing "02" prefix on P2PK pubkey       | Cashu P2PK expects compressed pubkey format              | Always prefix with "02" for nostr-cashu compat         |
| Not checking `allowsNostr` on LNURL      | Server may not support Nostr zaps at all                 | Verify `allowsNostr: true` before constructing zap     |
| Treating zap receipt as proof of payment | Receipts can be forged by rogue LNURL servers            | Trust the receipt author, not the receipt itself       |

## Quick Reference

| Operation     | Kind  | Key Tags                               | Published?            |
| ------------- | ----- | -------------------------------------- | --------------------- |
| Zap request   | 9734  | `relays`, `p`, `amount`, `lnurl`, `e`  | NO (HTTP only)        |
| Zap receipt   | 9735  | `p`, `P`, `bolt11`, `description`, `e` | YES (by LNURL server) |
| Nutzap config | 10019 | `relay`, `mint`, `pubkey`              | YES (replaceable)     |
| Nutzap send   | 9321  | `proof`, `u`, `unit`, `p`, `e`         | YES                   |
| Nutzap redeem | 7376  | `e` (9321 ref), `p` (sender)           | YES (encrypted)       |

## Key Principles

1. **Zap requests are HTTP-only** — Kind:9734 events are NEVER published to
   relays. They are signed, JSON-encoded, URI-encoded, and sent as a query
   parameter to the LNURL callback URL. This is the most common mistake.

2. **Validate the full chain** — A valid zap receipt requires matching the
   receipt pubkey to the LNURL `nostrPubkey`, matching the invoice amount to the
   request amount, and verifying the description hash. Skipping any check allows
   forged zaps.

3. **Nutzap keys are separate** — The P2PK pubkey in kind:10019 MUST be a
   different key from the user's main Nostr identity key. Using the same key
   would allow anyone to spend received tokens. Always prefix with "02".

4. **Amounts are in millisatoshis** — NIP-57 uses millisats everywhere (1 sat =
   1000 msats). The `amount` tag, `minSendable`, `maxSendable`, and invoice
   amounts are all in millisats.

5. **Trust boundaries matter** — Zap receipts are NOT cryptographic proofs of
   payment. They prove that a LNURL server claims payment was received. The
   trust is in the LNURL server operator, not in the protocol itself.
