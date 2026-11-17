---
name: edgegap-launch
description: 'Take an Edgegap-hosted game from "the test deployment works" to live players: the launch checklist (token hygiene, app version settings, restart policy, max duration, self-stop, image caching, log storage), version naming and blue/green rollouts with zero matchmaking downtime, cost and leak control, rate limits, free-tier limits to lift before launch, observability (logs, metrics, deployment IDs), capacity planning with Edgegap, Private Fleets and persistent servers, and incident basics. Use when preparing a launch, beta or playtest on Edgegap, reviewing production readiness, rolling out a new server build, deploying builds from CI or GitHub Actions (edgegap/deploy-action), or when someone mentions going live, launch day, rollout, scaling, hosting costs or operating game servers with real players.'
metadata:
  version: "0.3.1"
---

# Launching and operating on Edgegap

This assumes a test deployment already accepted a real client (`edgegap-local-testing`). This skill is the gap between "it works" and "it's operable". When you act on the account during a launch, follow the `edgegap` skill's [references/agent-rules.md](../edgegap/references/agent-rules.md): this is real players and real billing.

## Pre-launch checklist

**Account and tier**
- Free tier limits are not launch limits: one deployment at a time, 60-minute deployments, 2 apps, 2 versions, 10 GB registry, 1.5 vCPU / 3 GB, matchmaker stops after 3 hours. Upgrade to Pay as You Go before any public test. It also unlocks image caching and detailed metrics.
- Move the matchmaker off the free tier (it stops 3 hours after each start) to a private cluster tier sized for launch traffic (Hobbyist, Studio or Enterprise; they differ in rate limit and redundancy). Pricing: https://edgegap.com/resources/pricing#matchmaker.
- Tell Edgegap about the launch date and expected traffic in advance (support ticket, Discord, or info@edgegap.com). They plan regional capacity and can raise rate limits.

**Tokens**
- The Edgegap API token is organization-wide. Only the backend and CI hold it, from a secret store. None in clients, server images, deployment env vars or repos.
- Use a separate token per system (backend, CI, the agent) so one can be revoked without breaking the others. Delete unused tokens.
- The matchmaker Auth Token is client-safe; rotating it means shipping a client update, so plan that.

**App version settings** (per live version)
- Restart policy **Never** for match servers: process exit ends the deployment and its billing.
- Self-stop wired in the server (`ARBITRIUM_DELETE_URL`) at match end and when empty, tested.
- **Max duration** set to the longest real match plus margin (cloud hard cap: 24 h).
- **Termination grace period** long enough to flush results after SIGTERM.
- Ports, protocol and TLS Upgrade (WS) match the netcode. Port verification (`to_check`, on by default through the API) delays Ready until the port answers; turn it off only for ports that never answer a probe.
- vCPU and memory sized from a measured full match (`docker stats`), plus margin. Too low: lag or OOM restarts. Too high: money.
- **Active caching** enabled on the version players will hit, so deployments start in seconds worldwide. Cache takes time to reach "Good" and an image drops out of cache after 72 hours without deployments; enable it a day ahead and keep the version warm.
- **Endpoint Storage** (S3 bucket) configured, or container logs are lost every time a deployment stops.
- Secrets the server needs are hidden env vars.

**Releases**
- Server and client builds stay compatible per version; name versions on purpose: build tags for history, `dev`/`staging`/`prod` for environments, `blue`/`green` as aliases for rolling updates.
- Rollout with the matchmaker (blue/green): keep two matchmaker copies (`green` live, `blue` idle). Point `blue` at the new version, enable caching on that version and wait for it to reach green, ship the client that uses `blue`, let matches on `green` finish, then turn `green` off until the next release. Edgegap's rolling update guide: https://docs.edgegap.com/learn/matchmaking/matchmaker-in-depth#rolling-updates-and-ab-tests.
- Rollout with your own backend: flip the pinned version in config; rollback is flipping it back while the old version still exists and is cached.
- Never re-push a changed image under an existing tag: Edgegap caches by tag and you lose track of what ran.
- Disable (don't delete) old versions in the dashboard to stop accidental deploys.
- **Automate releases from GitHub Actions with Edgegap's [Deploy Action](https://github.com/edgegap/deploy-action)** (`edgegap/deploy-action@v0`) instead of writing API calls. After the workflow pushes the image, the action does three things:
  - creates a version named with the UTC time, copying an existing version's settings;
  - with `smoke-test: true`, deploys it, requires Ready with no restart for `smoke-duration`, and then stops it;
  - with `promote-version`, points an existing version such as `prod` at the new image once everything passed.

  Secrets are `EDGEGAP_API_TOKEN` (a CI-only token) and the registry login, which the action needs as inputs because the API never returns it. The docs page is https://docs.edgegap.com/docs/tools-and-integrations/github-actions.
  - Promoting changes only the image of `promote-version`, not its ports, resources or env vars.
  - That a running matchmaker picks the new image up without Stop → Start was not tested. Check it with a test match after the first promotion, or use the blue/green flow above with the version the action created.

**Cost and leak control**
- Self-stop + restart policy Never + max duration on every version.
- Reconciliation in your backend (or a daily check) that stops deployments your backend created (its own tag, older than a few minutes) that no live match owns (`edgegap-deployments-api`). Never reconcile across a whole application: matchmaker and test deployments live there too.
- Error deployments are not charged, but watch their rate: rising errors usually mean a broken build or missing registry credentials.
- Egress: estimate it from a measured match (bytes sent per player per second × players × match length). Edge Cloud egress is $0.10 per GB; Private Fleet hosts include 6 TB per host per month for free (about 18 Mbps sustained per host). Put steady or bandwidth-heavy traffic on a fleet and let cloud overflow absorb peaks: overflow deployments pay the cloud rate, and so does fleet traffic above 6 TB per host.

## Launch-day behavior

- **Rate limits** per organization: 40 deploys/s, 20 status+context requests/s, 10 list requests/s. Use webhooks instead of polling. A `429` is not fixed by retrying harder.
- **Capacity**: Edgegap scales each location with demand, but a sudden spike can still produce `422` (couldn't allocate). The matchmaker retries for you; a custom backend needs backoff and a player-facing "finding a server" state.
- **Watch the funnel, not only servers**: time from match found to connected, deployment errors per version, deployments per version (is the rollout complete?), players per server, matches that never filled.
- Keep a known-good version ready and rehearse the rollback.

## Observability

- **Dashboard**: deployment list with filters, per-deployment container logs and metrics (1-minute history on free, 1-second on paid), deployment map, and the balance-point heatmap per application. Hotspots in odd places (mid-ocean, Greenland) mean players far apart are being matched together.
- **Analytics dashboards** (paid): live servers per version, CPU, memory and networking insights.
- **Deployment IDs**: log them in the backend and show them in the client's match history. A support request with a deployment ID gets answered fast; "servers seem broken" does not.
- Service status: https://status.edgegap.com.

## Long-running and persistent servers

Cloud deployments stop after 24 hours. For MMO shards, survival worlds or baseline capacity, use **Private Fleets** (reserved hosts with 6 TB of free egress per host per month, with overflow to the public cloud) and persistence (max duration `-1`, restart policy On Crash, state in external storage). For player-chosen servers, the **Server Browser** lists running servers with seats. Guides: https://docs.edgegap.com/learn/orchestration/private-fleets, https://docs.edgegap.com/learn/orchestration/persistence, https://docs.edgegap.com/learn/server-browser.

## When something breaks

Order: your funnel metrics → deployment logs (before the deployment stops) → `edgegap-troubleshoot` → status page → Edgegap support with deployment IDs, times and the app version.

## After launch

Revisit regularly: vCPU and memory against real usage, max duration against real match lengths, placement quality (balance points, player latency reports), cache status on live versions, token inventory, and the free-tier assumptions left in configs.
