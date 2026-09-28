---
name: hedera-consensus-service
description: "How to create topics, submit messages, and subscribe to real-time message streams on Hedera using the Hiero JavaScript SDK (@hiero-ledger/sdk). Use this skill whenever the user wants to work with Hedera Consensus Service (HCS), including topic creation, message submission, pub/sub messaging, mirror node subscriptions, chunked large messages, topic fees, or any consensus-related operation in JavaScript or TypeScript. Also trigger when users mention @hashgraph/sdk topic operations, event logging on Hedera, decentralized messaging, audit trails, or ordered message streams."
---

# Hedera Consensus Service (HCS) — JavaScript SDK

HCS provides a decentralized, ordered message log with consensus timestamps. It works like a pub/sub system: you create **topics**, **submit messages** to them, and **subscribe** to receive messages in real time via mirror nodes. Messages are immutable, ordered, and timestamped by network consensus — useful for audit trails, event logs, supply chain tracking, and decentralized communication.

## Setup

All imports come from `@hiero-ledger/sdk`. Two setup patterns:

### Client + setOperator (direct)
```js
import { Client, AccountId, PrivateKey } from "@hiero-ledger/sdk";

const client = Client.forName(process.env.HEDERA_NETWORK)
    .setOperator(
        AccountId.fromString(process.env.OPERATOR_ID),
        PrivateKey.fromStringECDSA(process.env.OPERATOR_KEY),
    );
```

### Wallet + LocalProvider (signer-based)
```js
import { Wallet, LocalProvider } from "@hiero-ledger/sdk";

const provider = new LocalProvider();
const wallet = new Wallet(process.env.OPERATOR_ID, process.env.OPERATOR_KEY, provider);
```

With the signer pattern, use `freezeWithSigner(wallet)`, `signWithSigner(wallet)`, `executeWithSigner(wallet)`, and `getReceiptWithSigner(wallet)`.

## Creating a Topic

```js
import { TopicCreateTransaction } from "@hiero-ledger/sdk";

const { topicId } = await (
    await new TopicCreateTransaction()
        .setTopicMemo("My event log")
        .setAdminKey(operatorKey)       // allows update/delete
        .setSubmitKey(operatorKey)      // restricts who can post
        .execute(client)
).getReceipt(client);

console.log(`Topic created: ${topicId.toString()}`);
```

**Key behaviors**:
- Without an `adminKey`, the topic cannot be updated or deleted (only expiration can be extended).
- Without a `submitKey`, anyone can submit messages.
- Default auto-renew period is 90 days.

### Topic with Custom Fees

Topics can charge per-message fees (Hbar or token-denominated):

```js
import { TopicCreateTransaction, CustomFixedFee, Hbar } from "@hiero-ledger/sdk";

const fee = new CustomFixedFee()
    .setAmount(new Hbar(1).toTinybars())
    .setFeeCollectorAccountId(collectorId);

const { topicId } = await (
    await new TopicCreateTransaction()
        .setAdminKey(operatorKey)
        .setSubmitKey(operatorKey)
        .setFeeScheduleKey(operatorKey)
        .setCustomFees([fee])
        .addFeeExemptKey(trustedKey)  // this key skips fees
        .execute(client)
).getReceipt(client);
```

When paying custom fees, submitters can set a maximum they're willing to pay:

```js
import { CustomFeeLimit, CustomFixedFee, Hbar, HbarUnit } from "@hiero-ledger/sdk";

const limit = new CustomFeeLimit()
    .setAccountId(payerId)
    .setFees([
        new CustomFixedFee().setAmount(Hbar.from(2, HbarUnit.Hbar).toTinybars())
    ]);

await new TopicMessageSubmitTransaction()
    .setTopicId(topicId)
    .setMessage("Hello")
    .setCustomFeeLimits([limit])
    .execute(client);
```

## Submitting Messages

```js
import { TopicMessageSubmitTransaction } from "@hiero-ledger/sdk";

const response = await new TopicMessageSubmitTransaction()
    .setTopicId(topicId)
    .setMessage("Hello, Hedera!")
    .execute(client);

const receipt = await response.getReceipt(client);
console.log(`Sequence: ${receipt.topicSequenceNumber}`);
```

Messages can be `string` or `Uint8Array`. The receipt contains `topicSequenceNumber` (incremented per message) and `topicRunningHash`.

### When a submit key exists

If the topic has a submit key, messages must be signed by it:

```js
await (
    await new TopicMessageSubmitTransaction()
        .setTopicId(topicId)
        .setMessage("Authorized message")
        .freezeWith(client)
        .sign(submitKey)
).execute(client);
```

## Subscribing to Messages

The `TopicMessageQuery` creates a real-time subscription via the mirror node. Messages arrive as they reach consensus.

```js
import { TopicMessageQuery } from "@hiero-ledger/sdk";

const handle = new TopicMessageQuery()
    .setTopicId(topicId)
    .setStartTime(0)  // from the beginning
    .subscribe(
        client,
        (message, error) => console.error("Error:", error),
        (message) => {
            console.log(
                `[${message.consensusTimestamp}] #${message.sequenceNumber}: ` +
                Buffer.from(message.contents).toString("utf8")
            );
        },
    );

// Later, to stop receiving:
handle.unsubscribe();
```

**Important**: After creating a topic, wait a few seconds before subscribing — the mirror node needs time to sync the new topic.

### Subscription Options

```js
new TopicMessageQuery()
    .setTopicId(topicId)
    .setStartTime(startTimestamp)        // receive from this time forward
    .setEndTime(endTimestamp)            // stop after this time
    .setLimit(100)                       // max messages to receive
    .setMaxAttempts(20)                  // retry attempts (default: 20)
    .setMaxBackoff(8000)                 // max retry delay ms (default: 8000)
    .setErrorHandler((msg, err) => {})   // error callback
    .setCompletionHandler(() => {})      // fires when limit/endTime reached
    .subscribe(client, errorHandler, messageHandler);
```

### TopicMessage Properties

Each received `TopicMessage` has:
- `consensusTimestamp` — when the message reached consensus
- `contents` — `Uint8Array` message body (automatically reassembled from chunks)
- `sequenceNumber` — position in the topic (starts at 1)
- `runningHash` — SHA-384 running hash of the topic at this message
- `chunks` — individual `TopicMessageChunk[]` if the message was chunked
- `initialTransactionId` — original transaction ID (for chunked messages)

## Chunked Messages

Messages larger than 1024 bytes are automatically split into chunks. Each chunk is a separate transaction on the network. The SDK handles splitting on submit and reassembly on subscribe.

```js
const largeMessage = "x".repeat(5000); // 5KB message

// Option 1: execute() returns first chunk's response
const response = await new TopicMessageSubmitTransaction()
    .setTopicId(topicId)
    .setMessage(largeMessage)
    .execute(client);

// Option 2: executeAll() returns all chunk responses
const responses = await new TopicMessageSubmitTransaction()
    .setTopicId(topicId)
    .setMessage(largeMessage)
    .setMaxChunks(30)       // default: 20 (max ~20KB at 1024/chunk)
    .setChunkSize(2048)     // override chunk size (default: 1024)
    .executeAll(client);

for (const resp of responses) {
    const receipt = await resp.getReceipt(client);
    console.log(`Chunk seq: ${receipt.topicSequenceNumber}`);
}
```

**Limits**:
- Default chunk size: 1024 bytes
- Default max chunks: 20 (so ~20KB max message by default)
- Configurable via `setChunkSize()` and `setMaxChunks()`
- Subscribers automatically reassemble chunks into a single `TopicMessage`

## Updating a Topic

```js
import { TopicUpdateTransaction } from "@hiero-ledger/sdk";

await new TopicUpdateTransaction()
    .setTopicId(topicId)
    .setTopicMemo("Updated memo")
    .setSubmitKey(newSubmitKey)
    .execute(client);
```

All update operations require the admin key. Key-specific updates:
- Changing the admin key requires both old and new admin keys to sign
- Setting a new auto-renew account requires that account to sign
- You can clear keys with `clearAdminKey()`, `clearSubmitKey()`, etc.

### Updating Topic Fees

```js
await new TopicUpdateTransaction()
    .setTopicId(topicId)
    .setCustomFees([newFee])
    .addFeeExemptKey(anotherKey)
    .execute(client);
```

## Deleting a Topic

```js
import { TopicDeleteTransaction } from "@hiero-ledger/sdk";

await new TopicDeleteTransaction()
    .setTopicId(topicId)
    .execute(client);
```

Requires the admin key. After deletion, no operations on the topic will succeed.

## Querying Topic Info

```js
import { TopicInfoQuery } from "@hiero-ledger/sdk";

const info = await new TopicInfoQuery()
    .setTopicId(topicId)
    .execute(client);

console.log(`Memo: ${info.topicMemo}`);
console.log(`Sequence: ${info.sequenceNumber}`);
console.log(`Admin key: ${info.adminKey}`);
console.log(`Submit key: ${info.submitKey}`);
```

See `references/api-reference.md` for the full `TopicInfo` property list.

## Key Roles

| Key | Purpose |
|-----|---------|
| `adminKey` | Update/delete the topic; rotate other keys |
| `submitKey` | Authorize message submission (if absent, open to all) |
| `feeScheduleKey` | Update custom fee schedule |

## Common Patterns

### Event Log / Audit Trail
Create a topic per entity or event type. Submit structured JSON messages. Subscribe from a service to build a read model.

```js
const event = JSON.stringify({
    type: "ORDER_PLACED",
    orderId: "12345",
    timestamp: Date.now(),
    data: { items: 3, total: 99.99 },
});

await new TopicMessageSubmitTransaction()
    .setTopicId(ordersTopic)
    .setMessage(event)
    .execute(client);
```

### Pub/Sub with Multiple Subscribers
Multiple services can subscribe to the same topic independently. Each maintains its own cursor via `setStartTime`.

```js
// Service A: process all messages from the beginning
new TopicMessageQuery()
    .setTopicId(topicId)
    .setStartTime(0)
    .subscribe(client, null, processMessage);

// Service B: only new messages from now
new TopicMessageQuery()
    .setTopicId(topicId)
    .subscribe(client, null, processMessage);
```

## Common Gotchas

1. **Mirror node sync delay**: After creating a topic, wait 3-5 seconds before subscribing. The mirror node needs time to index the new topic.

2. **Chunk reassembly is automatic**: When subscribing, you receive complete messages even if they were submitted as multiple chunks. The SDK handles reassembly.

3. **No `execute()` for subscriptions**: `TopicMessageQuery` uses `.subscribe()`, not `.execute()`. It returns a `SubscriptionHandle`, not a `TransactionResponse`.

4. **Messages are immutable**: Once submitted, messages cannot be edited or deleted. Design your message schema with this in mind.

5. **Sequence numbers start at 1**: The first message on a topic gets sequence number 1, not 0.

6. **Submit key means access control**: If you set a submit key, only holders of that key can post. Omit it for open topics.

7. **String vs Uint8Array**: `setMessage()` accepts both. Use `Buffer.from(message.contents).toString("utf8")` to decode on the subscriber side.

8. **Cleanup**: Always call `handle.unsubscribe()` when done, and `client.close()` when shutting down.

## Reference Files

- `references/api-reference.md` — Complete list of all HCS classes with their methods and properties
