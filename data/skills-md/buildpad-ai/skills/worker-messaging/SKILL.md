---
name: worker-messaging
description: Offload long-running work from a Next.js/Amplify app to a Buildpad runtime worker over RabbitMQ, and chain job → worker → worker. Covers the standard topic-exchange convention (a single `jobs` exchange, routing key = job type, a message envelope, dead-lettering), the producer side (publish a job, fire-and-forget) and the consumer side (a worker that consumes and may hand off to another worker), and how to fetch the live RabbitMQ connection from the Buildpad Platform MCP (`get_project_detail` → `messaging`). Use when a request is too slow for request/response, needs background processing, or when one worker must pass work to another. Because the producer (Next.js repo) and the consumer (Node.js worker repo) are SEPARATE repositories worked on by separate agents, this skill also generates a cross-repo handoff doc that carries the topic/routing key, the payload schema and how to read it, the user's intent, and everything the other repo's agent needs to implement the matching side.
argument-hint: "[job type, e.g. report.generate]"
---

# Worker Messaging (offload jobs to Buildpad workers)

<!-- backend-gate:begin v1 -->
**Establish the backend first.** A Buildpad project's backend is either the Buildpad Engine or
Supabase, and some parts of this file hold for one of them only. Before you act on anything in
this file, find the backend with these steps, in order, and stop at the first step that answers:

1. Read `.buildpad/project.json` at the project root. If it is JSON and its field `backend` is
   `"engine"` or `"supabase"`, that is the backend. If `.buildpad/backend-answer.json` names the
   other backend, tell the developer the two files disagree, and follow `.buildpad/project.json`.
2. Otherwise read `.buildpad/backend-answer.json` in the same way; if its `backend` is
   `"engine"` or `"supabase"`, that is the backend.
3. If a folder named `supabase` at the project root holds a file named `config.toml`, or holds a
   folder named `migrations` that holds a file whose name ends in `.sql`, the backend is Supabase.
4. Otherwise ask the developer once: "Is this project's backend the Buildpad Engine or
   Supabase?" Write the answer to `.buildpad/backend-answer.json` as
   `{"buildpadBackendAnswer": 1, "backend": "engine"}` or
   `{"buildpadBackendAnswer": 1, "backend": "supabase"}`, and ask the developer to commit that
   file. Do not add it to `.gitignore`. Never write `.buildpad/project.json`.

To find the backend, do not open an environment file (`.env`, `.env.*`) or an MCP configuration
file, and do not call a tool that returns project credentials.

Then follow only the parts for that backend. A part starts at a line that holds only a comment
whose text is `buildpad` + `-backend: engine` or `buildpad` + `-backend: supabase`, and ends at the
next line that holds only a comment whose text is `/buildpad` + `-backend`. A comment that merely
mentions a backend is not a part. A file whose first line, after any front matter, holds only a
comment whose text is `buildpad` + `-backend-file: engine` (or `supabase`) holds for that backend
only, and so does every file in a folder named `engine-only` or `supabase-only`. Skip the other
backend's parts and copy no code from them; everything else holds for both. On an Engine project, when this file says that
something is not available, tell the developer so and stop: do not build a substitute.
<!-- backend-gate:end -->

Use this when a Next.js/Amplify app needs to **offload a long-running task** to a
background **worker**, or when one worker needs to **hand work to another worker**.
Communication is over the project's **RabbitMQ** broker using a single, standard
convention so producers never need to know which worker handles a job.

> **Why "too slow for request/response" is a hard rule here, not just good practice.**
> Amplify runs every API route as a Lambda with a ~30s response ceiling and buffered
> (non-streaming) invocations — confirmed in practice: a slow call gets a clean 504
> around 28s, and a streamed response fails differently (a raw 500 at the 30s hard
> timeout) instead of succeeding, since nothing reaches the caller until the Lambda
> returns. It isn't configurable, and it only shows up after deploying — `next dev`
> has no Lambda in the path. If the task doesn't need retries, scheduling, or to
> outlive a single request beyond that ~30s window, a lighter option than standing up
> a worker is **client-driven chunking**: the client repeatedly calls your API route
> within a time budget per call, each round trip well under 30s, until the work
> reports done. Reach for a worker (this skill) when the task should keep running
> independent of the browser, retry on failure, or run on a schedule instead.

> **The producer never waits for a reply.** Offload is fire-and-forget. If a worker
> produces a follow-up message, it's for **another worker** to consume — never for
> the Next.js app to consume.

> **Two repos, one contract.** The producer (Next.js app on Amplify) and the
> consumer (Node.js worker) live in **separate repositories**, each with its own AI
> agent. They share **no code** — only this convention plus a per-job **contract**.
> So implementing one side is only half the work: whenever you add or change a job
> type, you MUST emit a **handoff doc** (Step 4) so the other repo's agent can build
> the matching side exactly. Do not assume the other agent can see your code — it
> can't.

## Step 1 — Get the connection from the Platform MCP (do NOT hardcode)

The RabbitMQ connection string is **not** committed anywhere. Fetch it live from
the **Buildpad Platform MCP**:

- Call **`get_project_detail`** → use the **`messaging`** block:
  - `messaging.enabled` — is the worker/RabbitMQ feature active for this project?
  - `messaging.rabbitmq.amqpUrl` — the full AMQP connection string (with credentials).
  - `messaging.rabbitmq.managementUrl` — the browser console.
  - `messaging.convention` — the exchange/DLX/routing-key rules below.
  - `workers[]` — the workers that exist (id, name, status).

This works the same whether you're in a **newly-downloaded** repo or an **older**
project starter — always read the connection from `get_project_detail`, then put it
in the app's environment (e.g. `RABBITMQ_URL`). If `messaging.enabled` is false, the
project owner must enable Workers on the Buildpad platform first.

## Step 2 — The convention

Each project has its own RabbitMQ. All job traffic flows through one durable
**topic exchange** named **`jobs`**; the **routing key is the job type**.

```
Next.js (Amplify)                RabbitMQ                          Workers
  producer ──publish("jobs","report.generate")──▶ [topic: jobs] ──▶ q.report.generate ─▶ Worker A
                                                        │
  Worker A ──publish("jobs","report.email")────────────┘        ──▶ q.report.email     ─▶ Worker B
                                    (failed msgs) ──▶ [jobs.dlx] ──▶ q.dead
```

- **Producers** publish to exchange `jobs` with `routingKey = <job.type>` (dotted,
  e.g. `report.generate`, `image.thumbnail`). Anyone can produce: the Next.js app, or
  a worker chaining onward.
- **Consumers** (workers) declare a durable queue `q.<job.type>` bound to `jobs` with
  that routing key, and consume it.
- **Worker → worker handoff** is just another publish to `jobs` with the *next* job
  type's routing key. No point-to-point wiring, no reply/RPC queues.

### Message envelope (JSON)

```json
{
  "id": "<uuid>",                          // idempotency key — handlers MUST dedupe
  "type": "report.generate",               // == routing key
  "source": "nextjs" | "worker:<WORKER_ID>",
  "occurredAt": "<ISO-8601>",
  "data": { /* job-specific payload */ }
}
```

### Reliability

- Durable exchange + durable queues + **persistent** messages.
- Manual `ack`; `prefetch(1)` to start. Ack on success.
- On failure: `nack(msg, false /*allUpTo*/, false /*requeue*/)` → the queue's
  dead-letter exchange **`jobs.dlx`** → **`q.dead`** for inspection/replay.
  Declare each work queue with `{ deadLetterExchange: 'jobs.dlx' }`.

## Step 3a — Producer (Next.js / Amplify app)

Publish a job and return immediately. Never open a consumer in the web app.

```ts
// lib/jobs.ts  (Next.js — server side only)
import amqp from 'amqplib';
import { randomUUID } from 'crypto';

const JOBS_EXCHANGE = 'jobs';

export async function offloadJob(type: string, data: unknown) {
  // RABBITMQ_URL comes from get_project_detail → messaging.rabbitmq.amqpUrl,
  // stored as an env var / Amplify env var (server-side, NEVER NEXT_PUBLIC_*).
  const conn = await amqp.connect(process.env.RABBITMQ_URL!);
  const ch = await conn.createChannel();
  await ch.assertExchange(JOBS_EXCHANGE, 'topic', { durable: true });

  const envelope = {
    id: randomUUID(),
    type,
    source: 'nextjs',
    occurredAt: new Date().toISOString(),
    data,
  };
  ch.publish(JOBS_EXCHANGE, type, Buffer.from(JSON.stringify(envelope)), { persistent: true });

  await ch.close();
  await conn.close();
}
// In an API route:  await offloadJob('report.generate', { orderId }); return { accepted: true };
```

> Keep the RabbitMQ URL **server-side only** (it contains credentials). Publish from
> an API route / server action, never from the browser.

## Step 3b — Consumer (worker)

A worker binds a queue per job type it handles, processes, and may publish a
follow-up job for another worker. See the `worker-starter` scaffold and
`WORKER-REPO-CONTRACT.md` for the worker repo's build/run rules.

```ts
import amqp from 'amqplib';
import { randomUUID } from 'crypto';

const JOBS_EXCHANGE = 'jobs';
const DLX = 'jobs.dlx';
const JOB_TYPES = (process.env.WORKER_JOB_TYPES || '').split(',').map((s) => s.trim()).filter(Boolean);

async function main() {
  const conn = await amqp.connect(process.env.RABBITMQ_URL!);
  const ch = await conn.createChannel();
  await ch.assertExchange(JOBS_EXCHANGE, 'topic', { durable: true });
  await ch.assertExchange(DLX, 'fanout', { durable: true });
  await ch.prefetch(1);

  for (const type of JOB_TYPES) {
    const q = `q.${type}`;
    await ch.assertQueue(q, { durable: true, deadLetterExchange: DLX });
    await ch.bindQueue(q, JOBS_EXCHANGE, type);
    await ch.consume(q, async (msg) => {
      if (!msg) return;
      try {
        const env = JSON.parse(msg.content.toString());
        // ...do the work (call DaaS, etc.)...
        // Chain to the next worker (optional):
        // publishJob(ch, 'report.email', { reportId: env.data.id });
        ch.ack(msg);
      } catch (err) {
        console.error('handler failed:', err);
        ch.nack(msg, false, false); // → jobs.dlx → q.dead
      }
    });
  }
}

function publishJob(ch: amqp.Channel, type: string, data: unknown, workerId = process.env.WORKER_ID) {
  const envelope = { id: randomUUID(), type, source: `worker:${workerId}`, occurredAt: new Date().toISOString(), data };
  ch.publish(JOBS_EXCHANGE, type, Buffer.from(JSON.stringify(envelope)), { persistent: true });
}

main().catch((e) => { console.error(e); process.exit(1); });
```

<!-- buildpad-backend: engine -->
### Reaching the data service from a worker

On an Engine project a worker reaches the data API at `DAAS_URL`, the Engine_URL, and presents its own worker token, read from `DAAS_TOKEN`, as `Authorization: Bearer`; never the project's MCP token. The worker may create, read, update and delete the items of every collection a member creates, and may change no collection, field, relation, role, policy, permission, account or setting. Until the Engine accepts the worker token on its data API, a worker cannot reach the data API of an Engine project: tell the developer so and stop.

<!-- /buildpad-backend -->
## Step 4 — Hand off the contract to the other repo (REQUIRED)

The producer and consumer are in **different repositories**, so the code you just
wrote is invisible to the agent on the other side. The only thing that crosses the
gap is a **handoff doc**. Whenever you add or change a job type:

- **Producing from Next.js** (you wrote an `offloadJob('<type>', …)` call) → write a
  handoff for the **worker** repo's agent that will consume `<type>`.
- **Chaining worker → worker** (you `publishJob('<next.type>', …)`) → write a handoff
  for the agent that owns the **downstream** worker.

Save it as a Markdown file in the repo you're in (e.g.
`docs/handoffs/<job-type>.handoff.md`) and tell the user, in your final message:

> "Messaging spans two repos. Give **`docs/handoffs/<job-type>.handoff.md`** to the
> AI agent working on the **`<worker>`** repo — it has everything they need to
> implement the consumer. Come back and tell me if they change the payload."

The receiving agent runs **this same skill** on its side: fetch the connection from
the Platform MCP (Step 1), declare `q.<type>` bound to `jobs` with routing key
`<type>` (Step 3b), and implement the handler against the schema in the handoff.

### Handoff template

Fill **every** field from the code you just wrote **and** the intent the user gave
you in their prompt — the downstream agent has neither your code nor that
conversation. (Outer fence is 4 backticks so the inner code blocks copy cleanly.)

````markdown
# Worker job handoff — `<job.type>`

## Context (why this job exists)
<1–3 sentences from the user's request: what the webapp is offloading and the
business goal, not just the mechanics. Include anything the user said about
timing, ordering, retries, volume, or SLAs.>

## Where this fits
- **Producer:** <this repo> — <the route/action that publishes it, e.g.
  `app/api/reports/route.ts` on POST>.
- **Consumer:** <worker repo/name> — you implement this.
- **Downstream:** after handling, publish `<next.type>` for `<worker>` — or
  "none, terminal job".

## Transport (fixed convention — see the `worker-messaging` skill)
- Exchange `jobs` (durable topic); dead-letter `jobs.dlx` → `q.dead`.
- **Routing key / job type:** `<job.type>`
- **Consume from:** queue `q.<job.type>` (durable, `deadLetterExchange: jobs.dlx`),
  bound to `jobs` with routing key `<job.type>`.
- Connection: fetch live from Platform MCP `get_project_detail` →
  `messaging.rabbitmq.amqpUrl`. Never hardcode. Set `WORKER_JOB_TYPES=<job.type>`
  (comma-append if the worker already handles other types).

## Message envelope
Standard envelope; your handler reads `envelope.data`:
```json
{
  "id": "<uuid>",          // idempotency key — DEDUPE on this
  "type": "<job.type>",
  "source": "nextjs",      // or "worker:<id>" when chained
  "occurredAt": "<ISO-8601>",
  "data": { /* payload — see schema below */ }
}
```

## Payload schema (`data`)
| Field | Type | Required | Description / how to read |
|---|---|---|---|
| `<field>` | `<type>` | yes/no | <meaning, units, enum values, format> |

Real example:
```json
{ <a fully filled-in example of data> }
```

## What the consumer must do
<Step-by-step of the handler's job, from the user's intent: which DaaS collections
to read/write, external calls, the idempotency rule, what "done" means. If it emits
a downstream job, give that job's type + data shape.>

## Failure / retry
- Unrecoverable error → `nack` (no requeue) → `jobs.dlx` → `q.dead`.
- Redelivery-safe: dedupe on `envelope.id` (<how — e.g. a processed-ids table>).
- <Any ordering / rate limits the user mentioned.>

## Done when
<Observable success criteria the user cares about.>
````

> Keep it in sync: if you later change the payload, routing key, or downstream on
> the producer side, **regenerate** the handoff and tell the user to re-send it to
> the worker repo's agent.

## Rules

1. **Fetch the connection from `get_project_detail` (Platform MCP).** Never hardcode
   the RabbitMQ URL; never expose it to the browser (`NEXT_PUBLIC_*`).
2. **One `jobs` topic exchange; routing key = job type.** Producers publish job
   *types*, not worker addresses.
3. **Fire-and-forget offload.** The web app publishes and returns; it does not consume.
   Worker follow-ups are for other workers, never the web app.
4. **Durable + persistent + manual ack**, with `jobs.dlx` → `q.dead` for failures.
   Make handlers **idempotent** (dedupe on `envelope.id`) — messages can redeliver.
5. **Worker repo constraints** (build/run/pm2) live in `WORKER-REPO-CONTRACT.md` — a
   worker must be a long-running process; read config from `process.env`.
6. **Cross-repo contract (Step 4).** Producer and consumer are separate repos with
   separate agents. After implementing a producer for a new or changed job type,
   ALWAYS write the handoff doc and tell the user which repo/agent to hand it to.
   Never assume the other side "just knows" the topic name or payload — it doesn't.
