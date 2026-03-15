---
name: nostr-dvms
description: Build Nostr Data Vending Machine (DVM) services and clients using NIP-90. Use when implementing AI/compute service providers (kinds 5000-5999 job requests, 6000-6999 job results, kind 7000 feedback), creating DVM job request clients with payment handling, chaining DVM jobs, handling encrypted DVM params, or publishing NIP-89 service provider discovery events for DVMs.
---

# Nostr Data Vending Machines (NIP-90)

## Overview

Build AI and compute services on Nostr using the Data Vending Machine protocol.
DVMs follow a simple pattern: customers publish job requests (kind 5000-5999),
service providers process them and return results (kind 6000-6999), with
optional feedback events (kind 7000) for status updates and payment negotiation.

## When to Use

- Building a DVM service provider that processes job requests
- Creating a client that publishes DVM job requests and handles results
- Implementing payment flows for DVM services (bid, amount, bolt11)
- Chaining multiple DVM jobs (output of one feeds into another)
- Adding encrypted parameters to DVM requests for privacy
- Publishing NIP-89 handler announcements for DVM discoverability
- Handling DVM feedback states (processing, payment-required, error, partial)

**Do NOT use when:**

- Building general Nostr events (use nostr-event-builder)
- Implementing relay WebSocket logic
- Working with Lightning payments outside the DVM context

## Workflow

### 1. Determine Your Role

Ask: "Am I building a service provider, a client, or both?"

| Role             | Publishes              | Subscribes To        |
| ---------------- | ---------------------- | -------------------- |
| Service Provider | kind:6xxx results      | kind:5xxx requests   |
|                  | kind:7000 feedback     | kind:5 cancellations |
|                  | kind:31990 NIP-89 info |                      |
| Customer/Client  | kind:5xxx requests     | kind:6xxx results    |
|                  | kind:5 cancellations   | kind:7000 feedback   |

### 2. Choose the Job Kind

Each DVM operation has a specific kind number. The result kind is always request
kind + 1000.

| Request Kind | Result Kind | Description                      |
| ------------ | ----------- | -------------------------------- |
| 5000         | 6000        | Text extraction                  |
| 5001         | 6001        | Summarization                    |
| 5002         | 6002        | Translation                      |
| 5003         | 6003        | Text generation                  |
| 5005         | 6005        | Content discovery/recommendation |
| 5050         | 6050        | Text-to-speech                   |
| 5100         | 6100        | Image generation                 |
| 5250         | 6250        | Event publishing                 |

See [references/dvm-kinds.md](references/dvm-kinds.md) for the full registry.

### 3. Build the Job Request (Customer Side)

Construct a kind 5000-5999 event:

```json
{
  "kind": 5001,
  "content": "",
  "tags": [
    ["i", "<data>", "<input-type>", "<relay>", "<marker>"],
    ["output", "<mime-type>"],
    ["relays", "wss://relay.example.com"],
    ["bid", "<msat-amount>"],
    ["t", "<topic-tag>"],
    ["p", "<preferred-service-provider-pubkey>"]
  ]
}
```

**Input types** — the second element of the `i` tag:

| Type    | Meaning                                     | Example                                       |
| ------- | ------------------------------------------- | --------------------------------------------- |
| `text`  | Raw text data, no resolution needed         | `["i", "Hello world", "text"]`                |
| `url`   | URL to fetch content from                   | `["i", "https://example.com/doc.pdf", "url"]` |
| `event` | Reference to a Nostr event by ID            | `["i", "<event-id>", "event", "wss://relay"]` |
| `job`   | Output of a previous DVM job (for chaining) | `["i", "<job-event-id>", "job"]`              |

**Optional tags:**

- `output` — requested MIME type for the result (e.g., `text/plain`)
- `param` — key/value parameters: `["param", "lang", "es"]`
- `bid` — max millisats the customer will pay
- `relays` — where service providers should publish responses
- `p` — preferred service provider pubkey (others MAY still respond)
- `t` — topic tags for categorization

### 4. Handle Job Feedback (Kind 7000)

Service providers send feedback events to communicate status:

```json
{
  "kind": 7000,
  "content": "",
  "tags": [
    ["status", "<status>", "<extra-info>"],
    ["amount", "<msat>", "<bolt11>"],
    ["e", "<job-request-id>", "<relay-hint>"],
    ["p", "<customer-pubkey>"]
  ]
}
```

**Status values:**

| Status             | Meaning                                           | Action Required          |
| ------------------ | ------------------------------------------------- | ------------------------ |
| `payment-required` | SP requires payment before continuing             | Customer must pay        |
| `processing`       | SP is actively working on the job                 | Wait for result          |
| `error`            | SP could not process the job                      | Check extra-info for why |
| `success`          | SP completed the job                              | Result incoming          |
| `partial`          | SP has partial results (content may have samples) | More results coming      |

**Critical:** `payment-required` is a hard gate — the SP will NOT proceed until
paid. Other statuses are informational.

The `content` field MAY contain partial results (e.g., a sample of processed
output) for any feedback status.

### 5. Publish Job Results (Service Provider Side)

Result kind = request kind + 1000 (e.g., 5001 → 6001):

```json
{
  "kind": 6001,
  "content": "<result-payload>",
  "tags": [
    ["request", "<stringified-original-job-request-event>"],
    ["e", "<job-request-id>", "<relay-hint>"],
    ["i", "<original-input-data>"],
    ["p", "<customer-pubkey>"],
    ["amount", "<msat>", "<optional-bolt11>"]
  ]
}
```

**Required tags:**

- `request` — the FULL original job request event as a stringified JSON string
- `e` — references the job request event ID
- `p` — the customer's pubkey (so they can find the result)

**Important:** The `request` tag value is the entire job request event
serialized as a JSON string, not just the event ID.

### 6. Handle Payments

The payment model is flexible by design:

1. **Customer bids:** Include `["bid", "<msat>"]` in the request
2. **SP quotes:** Include `["amount", "<msat>", "<bolt11>"]` in feedback/result
3. **Customer pays:** Either pay the bolt11 invoice OR zap the result event

```
Customer                    Service Provider
   |                              |
   |-- kind:5001 (bid: 5000) ---->|
   |                              |
   |<-- kind:7000 ----------------|  status: payment-required
   |    amount: 3000, bolt11:...  |
   |                              |
   |-- pay bolt11 or zap -------->|
   |                              |
   |<-- kind:7000 ----------------|  status: processing
   |                              |
   |<-- kind:6001 ----------------|  result + amount tag
```

SPs MUST use `payment-required` feedback to block until paid. They SHOULD NOT
silently wait for payment without signaling.

### 7. Implement Job Chaining

Chain jobs by using the `job` input type — the output of one job becomes the
input of the next:

```json
{
  "kind": 5001,
  "content": "",
  "tags": [
    ["i", "<translation-job-event-id>", "job"],
    ["param", "lang", "en"]
  ]
}
```

The service provider for job #2 watches for the result of job #1, then processes
it. Payment timing is at the SP's discretion — they may wait for the customer to
zap job #1's result before starting job #2.

**Chaining example — translate then summarize:**

```
Step 1: Publish kind:5002 (translation)
  ["i", "https://article.com/post", "url"]
  ["param", "lang", "en"]

Step 2: Publish kind:5001 (summarization)
  ["i", "<step-1-event-id>", "job"]
```

### 8. Add Encrypted Parameters (Optional)

For privacy, encrypt `i` and `param` tags using NIP-04 with the service
provider's pubkey:

1. Collect all `i` and `param` tags into a JSON array
2. Encrypt with NIP-04 (customer's private key + SP's public key)
3. Put encrypted payload in `content` field
4. Add `["encrypted"]` tag and `["p", "<sp-pubkey>"]` tag
5. Remove plaintext `i` and `param` tags from the event

```json
{
  "kind": 5001,
  "content": "<nip04-encrypted-payload>",
  "tags": [
    ["p", "<service-provider-pubkey>"],
    ["encrypted"],
    ["output", "text/plain"],
    ["relays", "wss://relay.example.com"]
  ]
}
```

The SP decrypts the content to recover the input parameters. If the request was
encrypted, the result MUST also be encrypted and tagged `["encrypted"]`.

### 9. Publish Service Provider Discovery (NIP-89)

Advertise DVM capabilities with a kind:31990 handler announcement:

```json
{
  "kind": 31990,
  "content": "{\"name\":\"My Summarizer DVM\",\"about\":\"AI-powered text summarization\"}",
  "tags": [
    ["d", "<unique-identifier>"],
    ["k", "5001"],
    ["t", "summarization"],
    ["t", "ai"]
  ]
}
```

- `k` tag: the job request kind this DVM handles (e.g., `5001`)
- `t` tags: topic tags for discoverability
- `content`: JSON with `name` and `about` fields (like kind:0 metadata)

### 10. Handle Cancellation

Customers cancel jobs by publishing a kind:5 deletion request:

```json
{
  "kind": 5,
  "tags": [
    ["e", "<job-request-event-id>"],
    ["k", "5001"]
  ],
  "content": "No longer needed"
}
```

Service providers SHOULD monitor for kind:5 events tagging their active jobs and
stop processing if a cancellation is received.

## Checklist

- [ ] Job request uses correct kind (5000-5999) for the operation type
- [ ] Input `i` tags use valid input-type (`text`, `url`, `event`, `job`)
- [ ] Job result kind = request kind + 1000
- [ ] Result includes `request` tag with full stringified job request event
- [ ] Result includes `e` tag referencing the job request event ID
- [ ] Result includes `p` tag with customer's pubkey
- [ ] Feedback events use kind:7000 with valid status values
- [ ] `payment-required` feedback includes `amount` tag with bolt11
- [ ] Encrypted requests have `["encrypted"]` tag and encrypted content
- [ ] Encrypted results also use `["encrypted"]` tag
- [ ] Job chains use `["i", "<event-id>", "job"]` input type
- [ ] NIP-89 discovery uses kind:31990 with `k` tag for supported job kind
- [ ] Cancellation uses kind:5 with `e` tag referencing the job request

## Example: Complete Summarization DVM Service Provider

**Scenario:** Build a service provider that handles kind:5001 summarization
requests.

### Subscribe to job requests

```typescript
const sub = relay.subscribe([{ kinds: [5001] }]);
```

### Process a request

```typescript
async function handleJobRequest(event: NostrEvent) {
  const customerPubkey = event.pubkey;
  const jobId = event.id;

  // 1. Send processing feedback
  await publishEvent({
    kind: 7000,
    content: "",
    tags: [
      ["status", "processing", "Starting summarization"],
      ["e", jobId, "wss://relay.example.com"],
      ["p", customerPubkey],
    ],
  });

  // 2. Extract input data
  const inputTag = event.tags.find((t) => t[0] === "i");
  const inputType = inputTag[2]; // "text", "url", "event", "job"
  let inputData: string;

  if (inputType === "text") {
    inputData = inputTag[1];
  } else if (inputType === "url") {
    inputData = await fetch(inputTag[1]).then((r) => r.text());
  } else if (inputType === "event") {
    inputData = await fetchNostrEvent(inputTag[1], inputTag[3]);
  }

  // 3. Process the job
  const summary = await summarize(inputData);

  // 4. Publish result (kind = 5001 + 1000 = 6001)
  await publishEvent({
    kind: 6001,
    content: summary,
    tags: [
      ["request", JSON.stringify(event)],
      ["e", jobId, "wss://relay.example.com"],
      ["i", inputTag[1], inputTag[2]],
      ["p", customerPubkey],
      ["amount", "1000", generateBolt11(1000)],
    ],
  });
}
```

## Common Mistakes

| Mistake                                               | Why It Breaks                                         | Fix                                                        |
| ----------------------------------------------------- | ----------------------------------------------------- | ---------------------------------------------------------- |
| Result kind doesn't match request kind + 1000         | Clients can't correlate results to requests           | kind:5001 → kind:6001, always add 1000                     |
| Missing `request` tag in result                       | Clients can't verify the result matches their request | Include full stringified job request event                 |
| `request` tag contains event ID instead of full event | Spec requires the complete event JSON as a string     | Use `JSON.stringify(originalEvent)`                        |
| Using `payment-required` without `amount` tag         | Customer has no way to pay                            | Always include `["amount", "<msat>", "<bolt11>"]`          |
| Forgetting `p` tag in result/feedback                 | Customer can't find the result via subscription       | Always tag the customer's pubkey                           |
| Encrypting request but not result                     | Leaks the output even though input was private        | If request has `["encrypted"]`, result must too            |
| Using wrong input-type in `i` tag                     | SP can't resolve the input data                       | `text`=raw, `url`=fetch, `event`=nostr lookup, `job`=chain |
| Chaining with `event` type instead of `job`           | SP treats it as a static event, not a job output      | Use `["i", "<id>", "job"]` for chaining                    |
| Not monitoring for kind:5 cancellations               | Wastes compute on cancelled jobs                      | Subscribe to kind:5 events tagging active jobs             |
| NIP-89 announcement missing `k` tag                   | Clients can't discover which kinds the DVM supports   | Include `["k", "5001"]` for each supported kind            |

## Key Principles

1. **Result kind = request kind + 1000** — This is the fundamental mapping.
   kind:5001 always produces kind:6001. No exceptions.

2. **The `request` tag carries the full event** — Not just the ID. The entire
   original job request event must be stringified and included so clients can
   verify the result matches their request without additional lookups.

3. **Payment is flexible, signaling is not** — SPs can choose when to require
   payment, but they MUST use `payment-required` feedback to signal it. Silent
   blocking creates a broken UX.

4. **Encrypted in = encrypted out** — If the job request uses encrypted params,
   the result MUST also be encrypted. Partial encryption leaks data.

5. **Job chaining uses the `job` input type** — Not `event`. The `job` type
   tells the SP to wait for and use the output of a previous DVM job, not just
   read a static event.
