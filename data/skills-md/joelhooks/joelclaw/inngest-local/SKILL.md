---
name: inngest-local
displayName: Inngest Local
description: "Set up self-hosted Inngest on macOS as a durable background task manager for AI agents. Interactive Q&A to match intent — from Docker one-liner to full k8s deployment with persistent state. Use when: 'set up inngest', 'background tasks', 'durable workflows', 'self-host inngest', 'event-driven functions', 'cron jobs', or any request for a local workflow engine."
version: 1.0.0
author: Joel Hooks
tags: [joelclaw, inngest, workflows, events, local]
---

# Self-Hosted Inngest on macOS

This skill sets up Inngest as a self-hosted durable workflow engine on a Mac. Inngest gives you event-driven functions where each step retries independently — if step 3 of 5 fails, only step 3 retries.

## Before You Start

**Required:**
- macOS with Docker (Docker Desktop, OrbStack, or Colima)
- Bun or Node.js for the worker process

**Optional:**
- k8s cluster (k3d, Talos, etc.) for persistent deployment
- Redis (for state sharing between functions and gateway integration)

## Intent Alignment

Ask the user these questions to determine scope.

### Question 1: What are you building?

1. **Quick experiment** — I want to try Inngest, run a function, see the dashboard
2. **Persistent setup** — I want this running all the time, surviving reboots, with real workflows
3. **Full infrastructure** — I want k8s-deployed Inngest with persistent storage, integrated with an agent gateway

### Question 2: What runtime for the worker?

1. **Bun** — fast, good TypeScript support, what joelclaw uses
2. **Node.js** — standard, widest compatibility
3. **Existing framework** — I have a Next.js/Express/Hono app already

### Question 3: What kind of work?

1. **AI agent tasks** — coding loops, content processing, transcription pipelines
2. **General background jobs** — scheduled tasks, webhooks, data processing
3. **Both** — mixed workloads

## Setup Tiers

### Signing Keys (required)

As of Feb 2026, `inngest/inngest:latest` requires signing keys. Without them the container crash-loops with `Error: signing-key is required`.

```bash
# Generate once, reuse across tiers
INNGEST_SIGNING_KEY="signkey-dev-$(openssl rand -hex 16)"
INNGEST_EVENT_KEY="evtkey-dev-$(openssl rand -hex 16)"
echo "INNGEST_SIGNING_KEY=$INNGEST_SIGNING_KEY" >> .env.inngest
echo "INNGEST_EVENT_KEY=$INNGEST_EVENT_KEY" >> .env.inngest
```

### Tier 1: Docker One-Liner (experiment)

Get Inngest running in 30 seconds:

```bash
docker run -d --name inngest \
  -p 8288:8288 \
  -e INNGEST_SIGNING_KEY="$INNGEST_SIGNING_KEY" \
  -e INNGEST_EVENT_KEY="$INNGEST_EVENT_KEY" \
  inngest/inngest:latest \
  inngest start --host 0.0.0.0
```

Open http://localhost:8288 — you should see the Inngest dashboard.

**Limitation:** No persistent state. Container restart = lost history. Fine for experimenting.

### Tier 2: Persistent Docker (daily driver)

Add a volume for SQLite state:

```bash
docker run -d --name inngest \
  -p 8288:8288 \
  -v inngest-data:/var/lib/inngest \
  -e INNGEST_SIGNING_KEY="$INNGEST_SIGNING_KEY" \
  -e INNGEST_EVENT_KEY="$INNGEST_EVENT_KEY" \
  --restart unless-stopped \
  inngest/inngest:latest \
  inngest start --host 0.0.0.0
```

Now Inngest state survives container restarts. `--restart unless-stopped` brings it back after Docker restarts.

### Tier 3: Kubernetes (production-grade)

For full persistence with proper health checks. Requires a k8s cluster (k3d, Talos, etc.).

```yaml
# inngest.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: inngest
  namespace: default
spec:
  serviceName: inngest-svc  # NOT "inngest" — avoids env var collision
  replicas: 1
  selector:
    matchLabels:
      app: inngest
  template:
    metadata:
      labels:
        app: inngest
    spec:
      containers:
      - name: inngest
        image: inngest/inngest:latest
        command: ["inngest", "start", "--host", "0.0.0.0"]
        ports:
        - containerPort: 8288
        volumeMounts:
        - name: data
          mountPath: /var/lib/inngest
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 5Gi
---
apiVersion: v1
kind: Service
metadata:
  name: inngest-svc  # CRITICAL: not "inngest" — k8s creates INNGEST_PORT env var that conflicts
  namespace: default
spec:
  type: NodePort
  selector:
    app: inngest
  ports:
  - port: 8288
    targetPort: 8288
    nodePort: 8288
```

Apply:
```bash
kubectl apply -f inngest.yaml
```

**⚠️ GOTCHA:** Never name a k8s Service the same as the binary it runs. A Service named `inngest` creates `INNGEST_PORT=tcp://10.43.x.x:8288`. The Inngest binary expects `INNGEST_PORT` to be an integer. Name it `inngest-svc`.

## Build a Worker

### Step 1: Initialize

```bash
mkdir my-worker && cd my-worker
bun init -y
bun add inngest @inngest/ai hono
```

### Step 2: Create the Inngest client

```typescript
// src/inngest.ts
import { Inngest } from "inngest";

// Type your events for full type safety
type Events = {
  "task/process": { data: { url: string; outputPath: string } };
  "task/completed": { data: { url: string; result: string } };
};

export const inngest = new Inngest({
  id: "my-worker",
  schemas: new EventSchemas().fromRecord<Events>(),
});
```

### Step 3: Write your first function

```typescript
// src/functions/process-task.ts
import { inngest } from "../inngest";

export const processTask = inngest.createFunction(
  {
    id: "process-task",
    concurrency: { limit: 1 },  // one at a time
    retries: 3,
  },
  { event: "task/process" },
  async ({ event, step }) => {
    // Step 1: Download — retries independently on failure
    const localPath = await step.run("download", async () => {
      const response = await fetch(event.data.url);
      const buffer = await response.arrayBuffer();
      const path = `/tmp/downloads/${crypto.randomUUID()}.bin`;
      await Bun.write(path, buffer);
      return path;  // Only the path is stored in step state (claim-check pattern)
    });

    // Step 2: Process — if this fails, download doesn't re-run
    const result = await step.run("process", async () => {
      const data = await Bun.file(localPath).text();
      // ... your processing logic
      return { processed: true, size: data.length };
    });

    // Step 3: Emit completion event — chains to other functions
    await step.sendEvent("notify-complete", {
      name: "task/completed",
      data: { url: event.data.url, result: JSON.stringify(result) },
    });

    return { status: "done", result };
  }
);
```

### Step 4: Serve it

```typescript
// src/serve.ts
import { Hono } from "hono";
import { serve as inngestServe } from "inngest/hono";
import { inngest } from "./inngest";
import { processTask } from "./functions/process-task";

const app = new Hono();

// Health check
app.get("/", (c) => c.json({ status: "running", functions: 1 }));

// Inngest endpoint — registers functions with the server
app.on(
  ["GET", "POST", "PUT"],
  "/api/inngest",
  inngestServe({ client: inngest, functions: [processTask] })
);

export default {
  port: 3111,
  fetch: app.fetch,
};
```

### Step 5: Run it

```bash
INNGEST_DEV=1 bun run src/serve.ts
```

The worker starts, registers with Inngest at localhost:8288, and your function appears in the dashboard.

### Step 6: Test it

Send an event via the dashboard (Events → Send Event) or curl:

```bash
curl -X POST http://localhost:8288/e/key \
  -H "Content-Type: application/json" \
  -d '{"name": "task/process", "data": {"url": "https://example.com/file.txt", "outputPath": "/tmp/out"}}'
```

Watch it execute step-by-step in the dashboard.

## Patterns

### Event Chaining

Function A emits an event that triggers Function B:

```typescript
// In function A:
await step.sendEvent("chain", { name: "pipeline/step-two", data: { result } });

// Function B triggers on that event:
export const stepTwo = inngest.createFunction(
  { id: "step-two" },
  { event: "pipeline/step-two" },
  async ({ event, step }) => { /* ... */ }
);
```

### Concurrency Keys

Run one instance per project, but allow parallel across projects:

```typescript
concurrency: {
  key: "event.data.project",
  limit: 1,
}
```

### Cron Functions

```typescript
export const heartbeat = inngest.createFunction(
  { id: "heartbeat" },
  [{ cron: "*/15 * * * *" }],
  async ({ step }) => {
    await step.run("check-health", async () => {
      // ... system health checks
    });
  }
);
```

### Claim-Check Pattern

Large data between steps: write to file, pass path.

```typescript
// ❌ DON'T: return large data from a step
const transcript = await step.run("transcribe", async () => {
  return { text: hugeString }; // Step output has size limits!
});

// ✅ DO: write to file, return path
const transcriptPath = await step.run("transcribe", async () => {
  const result = await transcribe(audioPath);
  await Bun.write("/tmp/transcript.json", JSON.stringify(result));
  return "/tmp/transcript.json";
});
```

## Make It Survive Reboots

### Worker via launchd

```xml
<!-- ~/Library/LaunchAgents/com.you.inngest-worker.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.you.inngest-worker</string>
  <key>ProgramArguments</key>
  <array>
    <string>/Users/you/.bun/bin/bun</string>
    <string>run</string>
    <string>/path/to/your/worker/src/serve.ts</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>INNGEST_DEV</key><string>1</string>
    <key>HOME</key><string>/Users/you</string>
    <key>PATH</key><string>/usr/local/bin:/usr/bin:/bin:/Users/you/.bun/bin</string>
  </dict>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>/tmp/inngest-worker.log</string>
  <key>StandardErrorPath</key><string>/tmp/inngest-worker.log</string>
  <key>WorkingDirectory</key><string>/path/to/your/worker</string>
</dict>
</plist>
```

Load:
```bash
launchctl load ~/Library/LaunchAgents/com.you.inngest-worker.plist
```

### What happens on reboot

1. Docker starts → Inngest server comes up with persisted state (SQLite)
2. launchd starts → worker process registers functions
3. Any incomplete function runs resume from their last completed step

## Gotchas

1. **`@inngest/ai` is a required peer dep.** `bun add inngest` alone isn't enough — the SDK imports `@inngest/ai` at startup. Worker crashes with `Cannot find module '@inngest/ai'`. Always install both.

2. **Docker-to-host networking.** If Inngest runs in Docker and the worker on the host, the server can't reach `localhost:3111`. Pass `--sdk-url http://host.docker.internal:3111/api/inngest` on the docker run command. This is Docker Desktop/OrbStack-specific; Linux Docker needs `--add-host=host.docker.internal:host-gateway`.

3. **Service naming in k8s:** Never name a Service the same as the binary. `INNGEST_PORT` env var collision crashes the container.

4. **Step output size:** Keep step return values small. Use claim-check pattern for large data.

5. **Worker re-registration:** After Inngest server restart, the worker needs to re-register. Restart the worker or hit the registration endpoint.

6. **Trigger drift:** Functions register their triggers at startup. If you change a trigger in code but the server has stale state, the old trigger stays active. Build an auditor or restart both server and worker.

7. **`INNGEST_DEV=1`:** Required for local development. Without it, the worker tries to register with Inngest Cloud.

8. **Concurrency = 1 for GPU work:** Transcription, inference — anything that saturates a GPU needs `concurrency: { limit: 1 }`.

## Verification

- [ ] Inngest dashboard accessible at http://localhost:8288
- [ ] Worker shows as registered in dashboard (Functions tab)
- [ ] Send a test event — function executes in dashboard
- [ ] Kill the worker mid-function — restart worker, function resumes from last step
- [ ] (Tier 2+) Restart Docker — Inngest state is preserved
- [ ] (launchd) Reboot Mac — worker and Inngest both come back automatically

## Setup Script (curl-first)

For automated setup, the user can run:
```bash
curl -sL joelclaw.com/scripts/inngest-setup.sh | bash
```

Or with a specific tier:
```bash
curl -sL joelclaw.com/scripts/inngest-setup.sh | bash -s -- 2
```

The script is idempotent, detects existing state, and scaffolds a worker with typed events.

## Decision Chain (compressed ADRs)

This skill's architecture is backed by a chain of Architecture Decision Records. Unfurl as needed for tradeoff context.

**ADR-0010 → ADR-0029 → current state**

| Decision | Choice | Key Tradeoff | Link |
|----------|--------|-------------|------|
| Workflow engine | Inngest (self-hosted) | Step-level durability vs complexity. Cron+scripts has no per-step retry. | [ADR-0010](/adrs/0010-system-loop-gateway) |
| Container runtime | Colima (VZ framework) | Replaces Docker Desktop. Free, headless, less RAM. | [ADR-0029](/adrs/0029-colima-talos-migration) |
| k8s for 3 containers | Yes (k3d → Talos) | 380MB overhead for reconciliation loop + multi-node future. Docker Compose = no self-healing. | [joel-deploys-k8s](/joel-deploys-k8s) |
| Service naming | `inngest-svc` not `inngest` | k8s injects `INNGEST_PORT` env var. Binary expects integer, gets URL. | Hard-won debugging |
| Worker runtime | Bun + Hono | Faster cold start than Node. Hono = minimal HTTP. launchd KeepAlive for persistence. | Practical choice |
| Step data pattern | Claim-check (file path) | Step outputs have size limits. Write large data to disk, pass path between steps. | Inngest docs |
| Trigger auditing | Heartbeat cron auditor | Silent trigger drift broke promote function for days. Now audited every 15 min. | [ADR-0037](/adrs/0037-gateway-watchdog) |

## Credits

- [Inngest](https://www.inngest.com/) — the workflow engine
- [joelclaw.com/inngest-is-the-nervous-system](/inngest-is-the-nervous-system) — architecture narrative
- [joelclaw.com/self-hosting-inngest-background-tasks](/self-hosting-inngest-background-tasks) — human summary
