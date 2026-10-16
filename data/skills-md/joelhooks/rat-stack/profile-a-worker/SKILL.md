---
name: profile-a-worker
description: Capture a CPU or heap profile of a deployed Cloudflare Worker or Durable Object and read it with pprof. Use when a Worker is slow, burns CPU, nears its memory limit, throws Exceeded Memory, or you need to know which function costs the most in production.
plain: "Send real traffic, capture a short profile of the live isolate, read the widest frames, and change one thing at a time."
diagram: |-
  traffic to the version
    │ during the capture
    ▼
  POST …/versions/<v>/profile
    │ cpu or heap, 1–50 s
    ▼
  pprof file
    │ go tool pprof -top
    ▼
  widest frames → one change
    │
  capture again, compare
---

# Profile a Worker

Cloudflare can sample a deployed Worker or Durable Object while it serves traffic. The result is a pprof file. Each frame is a function. Wider frames cost more CPU time or allocate more memory.

Source: [Profiling in production](https://developers.cloudflare.com/workers/observability/profiling-in-production/).

## Terms used here

- **Isolate:** one running copy of a Worker. A profile samples one isolate that is already loaded.
- **CPU profile:** where CPU time goes. It samples about every millisecond.
- **Heap profile:** where code allocates memory. It records a stack every 512 kB allocated. It does not show retained memory, so it cannot prove a leak by itself.
- **Flat:** cost in the function itself. **Cum:** cost in the function and everything it calls.

## 1. Pick the target

1. Find the deployed script name. Alchemy names it from the app, resource, stage, and a suffix. Read it from the Alchemy state or the dashboard; do not guess it.
2. Pick the version. `latest` is the newest uploaded version, which may not be deployed. After an upload without a deploy, use the deployed version's id.
3. For a Durable Object, use the Worker that owns the namespace, the namespace id, and the 64-character instance id.

## 2. Get read access

Use one of these:

- The `cf` CLI with its own login.
- An API token with **Workers Scripts Read**, taken from your secret store for this one run.

Profiling is read-only. Do not add the token to the repo, `.env.schema`, or CI. Deploy credentials stay in Alchemy profiles.

## 3. Send traffic during the capture

A capture does not invoke your code. It records only what runs during the window.

- Start a load loop against the routes you suspect, then start the capture.
- Keep the loop running for the whole duration.
- `No recent executions` or `no loaded isolate` means the version had no traffic. Send traffic, then retry.

## 4. Capture

API, 10 seconds of CPU:

```sh
curl --fail --silent --show-error --request POST \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/workers/workers/$SCRIPT/versions/latest/profile" \
  --header "Authorization: Bearer $TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"duration_ms": 10000, "profile_type": "cpu"}' \
  --output worker-cpu.pprof
```

- `duration_ms` is 1000 to 50000. `profile_type` is `cpu` (default) or `heap`.
- For a Durable Object, add `namespace_id` and `actor_id` to the body.
- CLI: `cf workers versions profile latest --worker-id "$SCRIPT" --duration-ms 10000 --profile-type cpu > worker-cpu.pprof`.
- The dashboard has the same capture under the Worker's **Observability** tab, view **Flamegraph**.
- Captures are rate limited. On HTTP 429, wait for `Retry-After`.

Check the response before reading it. A failure returns JSON. A success returns protobuf.

```sh
file worker-cpu.pprof
```

The docs say the API returns gzip. In a capture taken on 2026-10-09, it returned raw protobuf (`application/vnd.google.protobuf`). pprof reads both.

## 5. Read it

```sh
go tool pprof -top -nodecount=25 worker-cpu.pprof
go tool pprof -top -lines -nodecount=15 worker-cpu.pprof
go tool pprof -peek 'functionName' worker-cpu.pprof
go tool pprof -http=:0 worker-cpu.pprof
```

- Start with `-top`. Ignore `(idle)` and `(program)`. Note `(garbage collector)`: a high share points to allocation, so take a heap profile next.
- Use `-peek` on a wide frame to see its callers and callees.
- Function names come from the bundle. If the bundler keeps names, they are readable. Locations point at bundle files and lines, such as `file:/bundle/worker.js:3348`, even when source maps upload. Search the bundle or the source for the function name.
- In an Effect program, the fiber runtime (`runLoop`, `makePrimitiveProto`, `succeedWith`) is the floor every request pays. Look below it for your own functions.

## 6. Act on one finding

1. Name the widest function you own and the route that reaches it.
2. Make one change. Common wins: compute a value once instead of per call, [cache a completed value](/lore/cache-completed-values), stop building objects you throw away, remove code that a flag only half disables.
3. Deploy, send the same traffic, capture again for the same duration, and compare the same frame.
4. Record the before and after numbers in the commit message.

One capture samples one isolate for seconds. Take two or three before calling a pattern. Say "this capture shows", not "the Worker always".

## Finish

- The profile file and the command that took it.
- The top frames you own, with flat and cum.
- One change and its measured effect, or the reason no change is worth it.
