---
name: ngrok-engine
description: Reference for ngrok's traffic model - what an endpoint is and what happens to traffic at the edge. Covers endpoint types (agent, cloud, internal), bindings and protocols (HTTP, TLS, TCP), and Traffic Policy - the YAML rule language of phases, CEL expressions, and actions, with a generated catalog of all 26 actions. Other ngrok skills point here to decide what to build, then to ngrok-surfaces to apply it. Not a standalone task - load when another skill references it.
license: MIT
metadata:
  author: ngrok
  version: "1.0"
  category: reference
  surface: engine-reference
compatibility: Reference skill. Loaded by other ngrok skills; not invoked directly.
---

# The ngrok engine: endpoints and Traffic Policy

Two decisions sit behind almost every ngrok task:

1. **What kind of endpoint?** Agent, cloud, or internal - and on what protocol.
2. **What should happen to the traffic?** The Traffic Policy that runs at the edge.

This skill answers both at the level a job skill needs, and holds the detail in `references/`. Where to *apply* the result is a separate question - see `ngrok-surfaces`.

Make these decisions from the user's intent. Do not ask them to choose an endpoint type; they should not have to know the taxonomy.

## 1. Endpoint type

- **Agent endpoint** - created by a running agent or SDK process, lives only as long as that process. Ephemeral, local, demos, tests.
- **Cloud endpoint** - created via API, dashboard, or IaC, independent of any agent. Always-on, stable URL. Production front doors, and anything a third party connects to on its own schedule.
- **Internal endpoint** - no public URL. Reachable only through a `forward-internal` action. This is how a receiver stays off the public internet.

The composed shape most jobs land on:

**cloud endpoint (public, runs the policy) -> forward-internal -> internal endpoint -> local service**

Protocol is a separate axis from type. HTTP is the default; TCP (SSH, RDP, databases) changes several things - a public TCP endpoint needs a reserved address, internal TCP URLs need an explicit port, the policy phase becomes `on_tcp_connect`, and the Kubernetes operator does not support TCP at all.

Full decision logic, bindings, and the TCP rules: `references/endpoints.md`.

## 2. Traffic Policy

Rules grouped by phase. Each rule has optional CEL `expressions` and a list of `actions`.

```yaml
on_http_request:
  - expressions:
      - "req.url.path.startsWith('/admin')"
    actions:
      - type: deny
```

- **Phases:** `on_http_request`, `on_http_response`, `on_tcp_connect`, `on_event_stream_message`.
- **Rules run in order**, and a terminating action ends the chain. Every Cloud Endpoint policy must end with a terminating action; agent endpoints need not.
- **The policy body is identical on every surface.** Only attachment differs.

Grammar, CEL variables, Secrets and Vaults, the seven most-used actions, and how actions chain: `references/traffic-policy.md`.

## The action vocabulary

All 26 actions, so you know what exists without fetching anything:

<!-- BEGIN generated: action-names -->
- **connection modification**: `deny`, `forward-internal`, `http-request`, `log`, `restrict-ips`, `set-vars`, `terminate-tls`
- **request modification**: `add-headers`, `circuit-breaker`, `log`, `owasp-crs-request`, `rate-limit`, `redirect`, `remove-headers`, `request-body-find-replace`, `set-vars`, `url-rewrite`
- **response modification**: `add-headers`, `compress-response`, `custom-response`, `log`, `owasp-crs-response`, `remove-headers`, `response-body-find-replace`, `set-vars`, `sse-find-replace`
- **security**: `basic-auth`, `jwt-validation`, `oauth`, `openid-connect`, `owasp-crs-request`, `owasp-crs-response`, `restrict-ips`, `terminate-tls`, `verify-webhook`
- **traffic control**: `circuit-breaker`, `close-connection`, `deny`, `forward-internal`, `http-request`, `owasp-crs-request`, `owasp-crs-response`, `rate-limit`
<!-- END generated: action-names -->

**Never guess an action's config.** Look it up in two steps:

1. `references/action-catalog.md` - the index. One row per action: phases, whether it ends the chain, what it does.
2. `references/actions/<action>.md` - that action's config fields, result variables, and an example.

Read only the action file you need; the whole directory is ~12k tokens and one action is a few hundred.

## Notes for agents

- The seven actions written out in `references/traffic-policy.md` are the ones existing job skills happen to use. They are not the interesting half - reach for the catalog whenever the task needs anything else.
- Many actions enforce on their own (`rate-limit` returns its own 429, `verify-webhook` fails closed). Check the action's entry before adding a `deny` that duplicates it.
- Keep the policy in its own `policy.yaml` so it survives the user adding a second surface later.
