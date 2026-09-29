---
name: browser-extension-connector
description: >
  Build a Chrome MV3 extension that acts on an external web service with no
  (or a limited) public API from inside the user's own signed-in browser
  session, observing the site's JSON traffic, replaying its auth headers for
  pulls and writes, buffering offline, and syncing with a host app through one
  polled endpoint that carries records up and commands down. Use when: (1) a
  product needs data out of, or actions into, a third-party site that offers
  no API, no OAuth and no export, and server-side scraping with the user's
  password is off the table, (2) an existing connector extension needs
  hardening: a service worker that dies, an alarm that never fires, a content
  script that shipped dead, records that go missing, commands marked failed
  without having run, (3) the user mentions: browser extension
  connector, chrome extension integration, no API, scrape from the logged-in
  session, MV3 service worker, content script MAIN world, tap fetch/XHR,
  replay auth headers, offline buffer, pairing PIN, "sync bookings from
  <site>", "publish to <site> without an API". Ships a compiled, tested
  runtime (tap, relay, worker, queue, pairing, diagnostics) and a vendor-neutral
  adapter seam; the host app's endpoints are a documented contract. Chrome MV3;
  host-agnostic. Not a per-service adapter; those are separate skills on top.
---

# Browser-Extension Connector

A site with no API still has a signed-in user and a browser that sees every
response the site serves. This skill turns that into a connector: a Chrome
extension that observes in the page's own context, issues requests with the
page's own credentials, buffers what it learns, and exchanges it with a host
app through one polled request. The hard part is not the plumbing but the
runtime it lives in: a service worker Chrome evicts every thirty seconds,
content scripts that die silently, a buffer with a ceiling, and a credential
that must never leave the tab.

## When to use

Building or hardening an extension that connects a third-party site to your
own app, where the site offers no partner API and handing over the user's
password is not acceptable. The service is the seam; this skill is the
infrastructure under any service adapter.

## When NOT to use

- **The site has an API or OAuth.** Use it; this is a workaround with real costs.
- **Server-side scraping with stored credentials.** Different threat model; not covered.
- **A one-off data export**: a script in DevTools is cheaper than an extension.
- **Writing a specific service's adapter**: a separate skill built on this one
  ([adapter-seam.md](references/adapter-seam.md) says what it must provide).
- **The host app's routes and schema**: described as a contract here, built in
  the host's own idiom ([server-contract.md](references/server-contract.md)).
- **Recording how employees work, with their consent**: the
  [`ecommerce-process-mining`](https://github.com/timerise-ai/ecommerce-process-mining)
  skill. This one moves a service's data, not a record of the work.

## Architecture

```
 HOST APP                      USER'S BROWSER (MV3 extension)                        SERVICE
 pair: PIN, then token --->  options page ---> storage
 sync: records up      <---  service worker <--- relay (ISOLATED) <--- tap (MAIN world) <--- page's fetch/XHR
       commands down   --->  buffer, loop,      port + 20 s ping,      captures JSON +
                             adapter.pull/      replays the page's     allowlisted auth
                             adapter.execute -> own auth headers -------------------------> service API
```

One request sustains the runtime: telemetry and records up, commands and
pacing down. No inbound connection to the user's machine is needed.

## Critical facts

1. **Only MAIN-world code sees the page's responses.** An isolated content
   script has its own `fetch`. The tap runs in MAIN, has no `chrome.*`, imports
   nothing, and must be built as a classic script. One top-level `export` and
   it ships dead, silently.
2. **The worker is evicted after ~30 s idle; `alarms` floor at one minute.** An
   open port does not count as activity; **traffic** on it does. The relay pings
   every 20 s while a service tab is open. Closed browser, no sync: say so.
3. **The credential never leaves the tab.** Captured from the page's own
   requests, replayed only to the same origin, never stored, never posted.
4. **The host may hand out commands on any response.** Every response is
   handled the same way; a discarded response burns a lease and an attempt.
5. **The buffer is bounded and loud.** It drops oldest, counts the drop, and
   the count reaches the host. Silence would look like health.
6. **The host stays service-agnostic.** The adapter normalises; a service
   changing its shape is an extension release, not a host deploy.

## Hard rules

> **Never create the alarm unconditionally at startup.** `alarms.create`
> replaces and restarts a same-named alarm; a worker revived often never
> reaches it. Check `alarms.get` first, and poll immediately on bootstrap.

> **Never fall back to a worker-side fetch when no service tab is open.** The
> worker has no session; a login page parses as "zero rows" and looks like a
> finished pull. Refuse loudly.

> **Never keep one "current port".** Keep every live port; two tabs are two
> ports, and closing one must not orphan the other.

> **Never acknowledge a command on the same post that ran it.** Acks ride the
> next post, so a browser closing between lets the lease expire and the
> command comes back instead of being lost.

> **Never validate a batch as a whole on the host.** One bad record must cost
> one record, named in `rejected`; a batch-level 400 wedges the channel forever.

> **Never write into the service until the write path is verified live**, and
> never delete by anything but the id the service returned.

## Quick start

0. Fill the seam contract and agree record, pull and command kinds with the
   host: [adaptation.md](references/adaptation.md).
1. Read the shape and the credential rules: [architecture.md](references/architecture.md).
2. Copy `assets/extension/` **verbatim**, set hosts and rationale:
   [manifest-and-permissions.md](references/manifest-and-permissions.md). Edit only
   the adapter, `tap-config.ts`, `ADAPTERS`, `PROVIDER`, the manifest hosts,
   `PERMISSIONS.md` and `strings.ts`; for cookie auth, the relay's `credentials`
   line with an empty allowlist, never both ([relay.md](references/relay.md)). A
   defect you find goes in the handover, not in a patch.
3. Implement the host's two endpoints to the contract:
   [server-contract.md](references/server-contract.md). PIN and pepper come from
   the environment, with no default in any tracked file.
4. Write the adapter (its own skill) against the seam:
   [adapter-seam.md](references/adapter-seam.md), then point the tap config at it:
   [main-world-tap.md](references/main-world-tap.md).
5. `npm i -D esbuild typescript vitest @types/node` (the registry is not an
   external service), then build, run the suites unmodified with vitest, load
   unpacked, pair over loopback: [build-and-package.md](references/build-and-package.md),
   [tests.md](references/tests.md), [pairing-ui.md](references/pairing-ui.md).
6. Put the operator surface in the host before going live:
   [operations.md](references/operations.md).
7. Say in your final message, not only in a README: nothing syncs while the
   browser is closed, pulls and commands need a signed-in service tab, and the
   hosts and parser stay unverified until checked against live traffic.

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| The shape, contexts, credential rules, cadence | architecture, MAIN world, isolated, threat model, poll | [architecture.md](references/architecture.md) |
| Manifest, permissions, review | manifest, host_permissions, optional_host_permissions, Web Store, single purpose | [manifest-and-permissions.md](references/manifest-and-permissions.md) |
| Capturing the page's traffic | tap, fetch patch, XHR, clone, auth headers, document_start, iife | [main-world-tap.md](references/main-world-tap.md) |
| Bridging page and worker | relay, port, keepalive, ping, context invalidated, orphaned, replay | [relay.md](references/relay.md) |
| Worker plumbing | service worker, alarm, setInterval, bootstrap, ports, onMessage | [service-worker-loop.md](references/service-worker-loop.md) |
| The loop's logic | tick, syncOne, commands, ack, lease, pull step, backoff | [sync-engine.md](references/sync-engine.md) |
| Test connection | diagnose, diagnostics ladder, why nothing syncs, paired but nothing happens | [diagnostics.md](references/diagnostics.md) |
| Buffering and routing | offline, chrome.storage.local, quota, dropped, Serial, two accounts | [offline-queue.md](references/offline-queue.md) |
| Talking to the host | SyncClient, 401, captive portal, timeout, pairings, LastPost | [host-client.md](references/host-client.md) |
| Plugging in a service | adapter, parse, pull, execute, cursor, writeVerified, externalRef | [adapter-seam.md](references/adapter-seam.md) |
| What the host must implement | pair endpoint, sync endpoint, token, PIN, staging, content hash, rejected | [server-contract.md](references/server-contract.md) |
| Pairing screen | options page, PIN, permissions.request, test connection, unpair | [pairing-ui.md](references/pairing-ui.md) |
| Popup, strings | popup, health, stale, i18n, strings.ts | [popup-and-strings.md](references/popup-and-strings.md) |
| Building and shipping | esbuild, iife, esm, define, zip, chrome.d.ts, version | [build-and-package.md](references/build-and-package.md) |
| Proof | vitest, regression, fixtures | [tests.md](references/tests.md) |
| Running it | runbook, silence, diagnostics, paused, revoked, reload | [operations.md](references/operations.md) |
| Fitting it to a host | seam, rename, host probe, order of work | [adaptation.md](references/adaptation.md) |
| Why the templates read as they do | provenance, defect, kept deliberately, added | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
