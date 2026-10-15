---
name: vp-tunnel
description: >-
  Use when something outside this machine must reach a local service: a
  deployed or public page whose requests to localhost, a local proxy, or a
  local WebSocket hang, spin, or fail with net::ERR_BLOCKED_BY_CLIENT (Chrome
  Local Network Access); a webhook; an OAuth provider that rejects localhost
  redirects; a phone off the LAN; a remote or cloud browser; or a teammate or
  client viewing a demo. Also use when asked to expose or share localhost, get
  a public URL, or compare ngrok, cloudflared, trycloudflare, tmole, or their
  alternatives. Decides whether a tunnel is needed, gates the exposure, and
  chooses the tool. Boundary: not for local clients reaching localhost,
  starting dev servers, or running a tunnel as production infrastructure; each
  tool's docs cover its commands, and vp-long-running-processes owns the
  process.
---

# Tunnel

A tunnel gives a local port a public HTTPS URL by relaying traffic through a
third-party provider. Use one only when something that cannot reach this
machine must reach a local service, no local path works, and the user accepts
the exposure. This skill decides whether to tunnel and which tool to use; each
tool's linked documentation covers its commands and flags.

## 1. Confirm that a tunnel is needed

Start from who must reach the local service:

| Caller                                                                                  | Path without a tunnel                                                                                                                                                                                                                                                                         |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A client on this machine: curl, a local browser opening a local page, the iOS Simulator | Reaches `localhost` directly. No tunnel.                                                                                                                                                                                                                                                      |
| A public page in a local browser, such as deployed staging calling a local API or mock  | Works only if the site has the local network permission. Check it first (below).                                                                                                                                                                                                              |
| A device on the same network                                                            | The LAN address, or `adb reverse` for an Android device over USB. Tunnel only when the feature needs HTTPS that the LAN address cannot provide.                                                                                                                                                |
| A webhook provider                                                                      | The provider's own forwarder, when one exists, needs no public URL: [`stripe listen`](https://docs.stripe.com/stripe-cli/use-cli), [`gh webhook forward`](https://docs.github.com/en/webhooks/testing-and-troubleshooting-webhooks/using-the-github-cli-to-forward-webhooks-for-testing). |
| An OAuth provider                                                                       | Many accept a `http://localhost` redirect URI. Tunnel only when the provider requires a public HTTPS URL.                                                                                                                                                                                     |
| A remote party: a teammate, a cloud agent or hosted browser, CI                         | None. Tunnel.                                                                                                                                                                                                                                                                                 |

### Public page to local service: check the permission first

Chrome's
[Local Network Access](https://developer.chrome.com/blog/local-network-access)
(LNA) holds requests from a public origin to loopback or private addresses
behind a permission prompt in the browser's own UI, and
[Chrome 147](https://developer.chrome.com/release-notes/147) added WebSocket
connections to that gate. An agent can neither see nor answer the prompt. An
unanswered request either hangs with no console error, never reaching the
local server, or fails with `net::ERR_BLOCKED_BY_CLIENT`. A page that waits
forever for data is often the only symptom.

Grants are stored per origin and per browser profile. Run this query in a page
loaded from the target origin, in the browser profile that will run the test:

```js
(await navigator.permissions.query({ name: "loopback-network" })).state;
```

Use `local-network` instead for a private address such as `192.168.x.x`.
[Chrome 145](https://developer.chrome.com/release-notes/145) introduced both
names and kept the old `local-network-access` as an alias. If a name throws,
try the old one. If every name throws, send one request with a timeout, and
treat a hang or a blocked error as `prompt`.

| State     | Do this                                                                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `granted` | Connect to the local URL directly. No tunnel.                                                                                                        |
| `prompt`  | With a person present, ask them to click Allow; nothing leaves the machine, and the grant persists for that origin and profile. Otherwise tunnel. |
| `denied`  | Tunnel, or ask a person to reset the site's permission and allow it.                                                                                 |

An agent-managed browser profile starts without grants, so expect `prompt`
there even when the user's daily browser already allows the site. Run the
query even when nobody is present, because `granted` still means no tunnel. A
headless browser cannot show the prompt; when it returns `prompt`, treat it as
having nobody present.

## 2. Get authorization for the exposure

Opening a tunnel publishes a local service to the internet, so treat it as an
external write:

- The provider terminates TLS. It can read every header and body that crosses
  the tunnel, including `Authorization` tokens, cookies, and production data.
- The URL is public. Anyone who has it reaches the service, including any
  debug, admin, or mock-control endpoints the service exposes.
- Default `ngrok` URLs and `tmole` URLs contain this machine's public IP
  address, so sharing the URL also shares that address.

Before starting a tunnel, get explicit approval from the user that covers
three things: the local service, the data that crosses it (for example,
staging or production, real user data, tokens), and the provider. The task
itself can name the service or the data. An earlier approval covers only what
it named. When one of the three is missing, ask; with nobody to ask, defer the
tunnel and report why. Check that no organization policy forbids third-party
tunnels, and when a network blocks one provider, ask before switching to
another.

Never tunnel a service that issues or stores credentials or session tokens,
such as a local sign-in or session server or a secret manager, or one that
grants access without authentication, such as an unauthenticated admin panel.
A public URL hands that access to anyone who finds it. Decline even when asked,
explain the risk, and offer a path that keeps the credential on this machine,
such as a person granting the local network permission.

Installing a tunnel client is a dependency install, and approving the
exposure does not approve the install. Follow the user's install and trust
rules, and ask first when an installer needs `sudo`. Only a person can create
or verify a provider account.

## 3. Choose a tool

A tool is available when it is installed or can be installed with approval,
is signed in where required, and can connect. Take the first available tool in
this order that meets the task's needs. When the user names a tool, use it and
report any gap this table predicts.

| Order | Tool                                                                                                                                                 | Account                  | WebSocket | Live Server-Sent Events (SSE) | Choose it when                                                                   |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ | --------- | ----------------------------- | -------------------------------------------------------------------------------- |
| 1     | `cloudflared` [Quick Tunnel](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/) | None                     | Yes       | **No** (buffered)             | Default: no account and no monthly quota; 200 requests in flight; no uptime guarantee. |
| 2     | [`ngrok`](https://ngrok.com/docs/)                                                                                                                   | Required, email verified | Yes       | Yes                           | The app streams with SSE, or `cloudflared` cannot connect.                       |
| 3     | `tmole` ([Tunnelmole](https://tunnelmole.com/docs/))                                                                                                 | None                     | **No**    | **No** (buffered)             | Only HTTP must cross, and neither tool above is available.                       |

"Buffered" means the client receives every event only after the stream ends,
so a streaming UI shows nothing until the response completes. Read
[references/tools.md](references/tools.md) before installing or first using a
tool: it lists each tool's prerequisites, limits, and behavior.

Rules that change the order:

- **Protocol needs come first.** WebSocket and SSE decide the tool before
  convenience such as ngrok's free-plan warning page or quotas does. Live SSE
  requires `ngrok`, because the other two buffer it. When a person will open
  pages through `ngrok`, tell them its free plan may show a warning page before
  HTML content.
- **When no available tool carries the needed protocol, ask.** This happens
  when the app needs live SSE and `ngrok` is unavailable, or needs WebSocket
  and only `tmole` is available. Ask the user to unblock `ngrok`, for example
  by installing it or verifying the account email. If the user declines and
  picks a tool that lacks the protocol, report the gap: SSE arrives only when
  each stream ends, or WebSocket traffic stays on its real host.
- **Volume decides between the first two.** ngrok's free plan caps monthly
  requests and data transfer, so long-running traffic favors `cloudflared`.
  Neither suits a load test: the Quick Tunnel returns `429` beyond 200 requests
  in flight, and ngrok's free plan caps the request rate. Run the load
  generator on this machine or the same network instead.
- **A URL that must survive restarts favors `ngrok`.** By default, all three
  tools give a new URL on every start. When the URL must survive, as for a
  registered webhook, an OAuth redirect allowlist, or a link given to
  teammates, use a fixed hostname. ngrok's free plan includes one development
  domain that stays the same when requested explicitly. With `cloudflared`, a
  fixed hostname needs an account-backed named tunnel. Set either up from the
  tool's documentation with the user's approval.

Other relays, such as Tailscale Funnel, VS Code port forwarding, or
localtunnel, are outside this skill. Use one only when the user asks
for it, under the same authorization rules.

## 4. Avoid the common wiring failures

These apply to every tool:

- **Point the tunnel at the port the service listens on.** All three tools
  send their own hostname as the `Host` header. A local proxy that routes by
  `Host`, such as Portless, then misroutes the request, and a dev server that
  checks `Host` rejects it; Vite's
  [`server.allowedHosts`](https://vite.dev/config/server-options#server-allowedhosts)
  is one example. Allow the tunnel's exact hostname, never every host.
- **Wait until the URL answers before using it.** A new `cloudflared`
  hostname can take a minute or more to resolve. Poll with `curl` from this
  machine until any HTTP status comes back; a lookup made too early can be
  cached as a failure by the resolver the browser or provider uses.
- **Move every host the client uses.** If the page talks to an API host and a
  WebSocket host, point both at the tunnel (`https://` and `wss://`), or report
  which one still reaches the real backend.
- **Read the URL after every start.** Without a fixed hostname, every restart
  gives a new URL, which breaks overrides, webhook registrations, and shared
  links that still name the old one.

## 5. Run, report, and stop

Run the tunnel as a background process that you own, with its log captured;
the URL appears in that log.

In the report, state that a tunnel was used, which tool, which local service it
exposed, which site and data crossed it, and anything it did not cover.

Stop the tunnel when the task is done or the approved window ends. Remove
client overrides and webhook registrations that point at the URL first, then
stop the tunnel, then the local service. A tunnel left open keeps exposing the
service.

## Related skills

- [`vp-long-running-processes`](https://github.com/VdustR/skills/tree/main/skills/vp-long-running-processes)
  for starting, inspecting, and stopping the tunnel and the local service.
- [`vp-session-wrapup`](https://github.com/VdustR/skills/tree/main/skills/vp-session-wrapup)
  when a session ends while a tunnel is still open.
