---
name: hyperstack-consume
description: Consume Hyperstack streams using TypeScript, React, or Rust SDKs. Covers connecting to stacks, subscribing to views, handling real-time updates, and using typed entity data. Use when the user wants to read or stream Solana data from deployed Hyperstack stacks.
allowed-tools: Bash(hs:*) Bash(npx:hyperstack-cli*)
metadata:
  version: "0.5"
---

# Consuming Hyperstack Streams

The workflow is: **discover the schema, understand what the user needs, plan the integration, write the code, verify it works.**

## 1. Prerequisites

Required: Hyperstack CLI (`hs`) for schema discovery. Run once:

```bash
OS="$(uname -s 2>/dev/null || echo Windows)"

if command -v hs &>/dev/null; then
  HS_CLI="hs"
elif command -v hyperstack-cli &>/dev/null; then
  HS_CLI="hyperstack-cli"
else
  if ! command -v cargo &>/dev/null; then
    if [ "$OS" = "Darwin" ] || [ "$OS" = "Linux" ]; then
      curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path
      source "$HOME/.cargo/env"
    else
      curl -sSLo /tmp/rustup-init.exe https://win.rustup.rs/x86_64
      /tmp/rustup-init.exe -y
      export PATH="$USERPROFILE/.cargo/bin:$PATH"
    fi
  fi
  cargo install hyperstack-cli
  HS_CLI="hs"
fi
```

> All examples use `hs`. If installed via cargo (`cargo install hyperstack-cli`) or npm (`npm install -g hyperstack-cli`).

## 2. Discover the Stack Schema

Do this before writing any code. Never guess entity names, field paths, or types.

```bash
# List all available stacks
hs explore --json

# Get entities and views for a specific stack
hs explore <stack-name> --json

# Get detailed fields for a specific entity
hs explore <stack-name> <EntityName> --json
```

> **Custom stacks must be pushed first.** `hs explore` only works for stacks that have been pushed to Hyperstack. If the user is working with their own custom stack, they must run `hs stack push` before `hs explore` will return results. Public/global stacks (like `ore`) work immediately.

Review the output to build a mental model of:
- Which **entities** exist (e.g., `OreRound`, `OreMiner`, `OreTreasury`)
- What **sections** each entity has (e.g., `id`, `state`, `metrics`)
- What **fields** are in each section with their types
- What **views** are available (e.g., `latest`, `list`, `state`, custom views)

## 3. Understand What the User Needs

Adapt depth to how specific the user's request is:

### Clear requirements

The user names specific data points — "show miner rewards and round info."

Map each requirement to a concrete entity field from the schema you discovered in step 2:

| User wants | Required data | Available in stack? |
|------------|---------------|---------------------|
| "Show mining rewards" | reward amount, miner address | ✅ `OreMiner.state.reward`, `OreMiner.id.miner_pubkey` |
| "Current round info" | round ID, total miners | ✅ `OreRound.id.round_id`, `OreRound.state.total_miners` |
| "Transaction history" | past transactions | ❌ Not in stack |

Confirm every requested data point maps to a real field. If anything is missing, stop and tell the user immediately — don't proceed with implementation if critical data isn't available:

```
❌ "The ore stack doesn't expose transaction history. It tracks live state,
   not historical transactions. You'd need to query Solana directly via RPC."

⚠️ "The ore stack has current round data but doesn't store historical rounds.
   You'll get live updates but can't query past rounds."

✅ "The ore stack has everything you need — miner rewards are in
   OreMiner.state.reward and round info is in OreRound."
```

### App idea but unclear data needs

The user describes what they want to build — "a mining dashboard" — but hasn't specified which data points.

Present what the stack offers organized by entity, explain what each entity represents, and propose which ones are relevant to their idea. Get confirmation before proceeding.

### Exploratory

The user wants to know what's possible — "what can I build with this stack?"

Surface all entities with a one-liner on what each tracks. Let the user narrow scope before planning anything.

## 4. Plan the Integration

Before writing code, make four decisions:

### SDK choice

Match to the user's project and use case:
- **TypeScript** — scripts, backends, CLIs, any Node.js context
- **React** — UI components, dashboards, anything with a render loop
- **Rust** — high-performance consumers, infra, bots

If the user already has a project, match the existing stack. If greenfield, ask.

### Streaming mode

| User needs | Method | Why |
|------------|--------|-----|
| Live-updating data, simplest API | `.use()` | Emits merged entity after each change |
| Know what changed (create/update/delete) | `.watch()` | Emits operation type with data |
| Before/after diffs | `.watchRich()` | Emits before and after state for comparison |
| Current snapshot, no live updates | `.get()` | One-shot read, returns once |

Default to `.use()` unless the user explicitly needs operation types or diffs.

### Single vs multi-entity

If the user's requirements span multiple entities, plan the correlation strategy:
- Which entities to stream in parallel
- What shared keys link them (e.g., `round_id` across `OreRound` and `OreMiner`)
- Whether to use `Promise.all` (TS) or parallel hooks (React)

### Schema validation

Decide upfront whether to use schema filtering:
- **Partial data is fine** — fields are optional, use optional chaining (`round.state?.motherlode`)
- **Must have all fields present** — use the generated `CompletedSchema` variant to guarantee non-null fields
- **Only need specific fields** — define a custom Zod schema to validate just what the code requires

## 5. Install & Connect

### TypeScript

```bash
npm install hyperstack-typescript
# For prepackaged stacks:
npm install hyperstack-stacks
```

```typescript
import { HyperStack } from 'hyperstack-typescript';
import { ORE_STREAM_STACK } from 'hyperstack-stacks/ore';

const hs = await HyperStack.connect(ORE_STREAM_STACK);
```

For custom stacks (after `hs sdk create typescript <stack-name>`):
```typescript
import { HyperStack } from 'hyperstack-typescript';
import MY_STACK from './generated/my-stack';

const hs = await HyperStack.connect(MY_STACK);
```

> Full connection options, error handling, and state management: see `references/typescript-api.md`

### React

```bash
npm install hyperstack-react hyperstack-stacks
```

```tsx
import { HyperstackProvider } from 'hyperstack-react';

function App() {
  return (
    <HyperstackProvider>
      <MyComponent />
    </HyperstackProvider>
  );
}
```

```tsx
import { useHyperstack } from 'hyperstack-react';
import { ORE_STREAM_STACK } from 'hyperstack-stacks/ore';

function MyComponent() {
  const { views, isConnected } = useHyperstack(ORE_STREAM_STACK);
  // views is now typed and ready to use
}
```

> `hyperstack-react` re-exports everything from `hyperstack-typescript`. You don't need both packages.
>
> Full provider props, hook signatures, filtering operators, and conditional subscriptions: see `references/react-api.md`

### Rust

```toml
[dependencies]
hyperstack-sdk = "0.5"
tokio = { version = "1", features = ["full"] }
```

```rust
use hyperstack_sdk::prelude::*;
use hyperstack_stacks::ore::{OreStack, OreRound};

let hs = HyperStack::<OreStack>::connect().await?;
```

> Full Rust SDK API: see `references/rust-api.md`

## 6. Implement the Data Layer

Use the decisions from step 4 to write the minimal code. Examples below cover the most common patterns.

**For the full API surface** (all methods, options, types, and edge cases), read the reference for the SDK you chose in step 4:
- **TypeScript**: `references/typescript-api.md` — connection options, `.use()`/`.watch()`/`.watchRich()` signatures, one-shot reads, update types, error handling
- **React**: `references/react-api.md` — provider props, hook return types, `where` filtering operators, `useOne()`, conditional subscriptions, connection state
- **Rust**: `references/rust-api.md` — `HyperStack::<T>::connect()`, `.listen()`, tokio integration

### Streaming with `.use()` (TypeScript)

```typescript
for await (const round of hs.views.OreRound.latest.use()) {
  console.log("Round:", round.id.round_id);
  console.log("Motherlode:", round.state.motherlode);
}
```

### Streaming with hooks (React)

```tsx
function MiningDashboard() {
  const { views } = useHyperstack(ORE_STREAM_STACK);
  const { data: rounds, isLoading } = views.OreRound.latest.use();

  if (isLoading) return <p>Connecting...</p>;

  return (
    <ul>
      {rounds?.map((round) => (
        <li key={round.id?.round_id}>
          Round #{round.id?.round_id} — Motherlode: {round.state?.motherlode}
        </li>
      ))}
    </ul>
  );
}
```

### One-shot read (TypeScript)

```typescript
const rounds = await hs.views.OreRound.list.get();
const round = await hs.views.OreRound.state.get(roundAddress);
```

### Multi-entity correlation

```typescript
const [rounds, miners] = await Promise.all([
  hs.views.OreRound.latest.get(),
  hs.views.OreMiner.list.get(),
]);

const currentRoundId = rounds.values().next().value?.id?.round_id;
const minersInRound = [...miners.values()].filter(
  m => m.state?.current_round_id === currentRoundId
);
```

### Schema validation

```typescript
import { OreRoundCompletedSchema } from 'hyperstack-stacks/ore';

// Only receive fully-hydrated entities — all fields guaranteed non-null
for await (const round of hs.views.OreRound.latest.use({
  schema: OreRoundCompletedSchema,
})) {
  console.log(round.id.round_id, round.state.motherlode);
}
```

Custom schemas work too — validate only what your code needs:

```typescript
import { z } from 'zod';

const TradableTokenSchema = z.object({
  id: z.object({ mint: z.string() }),
  reserves: z.object({ current_price_sol: z.number() }),
});

for await (const token of hs.views.PumpfunToken.list.use({
  schema: TradableTokenSchema,
})) {
  console.log(token.id.mint, token.reserves.current_price_sol);
}
```

### Stream control

Break to stop streaming:
```typescript
for await (const round of hs.views.OreRound.latest.use()) {
  if ((round.state.motherlode ?? 0) > 1_000_000_000) break;
}
```

Cancel from outside the loop:
```typescript
const controller = new AbortController();
setTimeout(() => controller.abort(), 30_000);

try {
  for await (const round of hs.views.OreRound.latest.use()) {
    if (controller.signal.aborted) break;
    console.log("Round:", round.id.round_id);
  }
} catch (e) {
  if (!controller.signal.aborted) throw e;
}
```

### Generating SDK types for custom stacks

```bash
hs sdk create typescript <stack-name>
# If the stack was shared via URL:
hs sdk create typescript <stack-name> --url wss://their-stack.stack.usehyperstack.com
```

## 7. Verify

After implementation, confirm everything works:

1. **Connection** — check that the WebSocket connects successfully (connection state reaches `connected`)
2. **Data flowing** — log or render the first entity received to confirm the stream is live
3. **Field paths** — verify fields aren't `undefined` where you expect data (a sign of wrong field paths or entity names)
4. **Schema filtering** — if using schemas, confirm entities are passing validation (not silently filtered to empty)

## Common Mistakes

- **Guessing entity names or field paths.** Always run `hs explore <stack> --json` first. Training data may be outdated.
- **Confusing `.use()` with `.watch()`.** `.use()` emits the merged entity (`T`). `.watch()` emits the operation type (`upsert`/`patch`/`delete`).
- **Forgetting React hooks return `{ data, isLoading, error }`.** Always destructure — don't treat the hook result as raw data.
- **Misusing `skip` as field names.** `WatchOptions.skip` is a number for pagination (`{ skip: 20, take: 10 }`), not field exclusion.
- **Not pushing custom stacks.** `hs explore` only works after `hs stack push`. Custom stacks won't appear until pushed.
- **Not reading the API reference for your SDK.** The examples in step 6 are starting points. For complete method signatures, option types, filtering operators, error handling, and edge cases, read the relevant reference: `references/typescript-api.md`, `references/react-api.md`, or `references/rust-api.md`.
