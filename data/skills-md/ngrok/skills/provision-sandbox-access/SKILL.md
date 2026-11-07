---
name: provision-sandbox-access
description: Give every sandbox, container, device, or tenant its own isolated ngrok endpoint, provisioned programmatically at runtime from a controlplane. Covers the per-workload resource set - service user, reserved address or domain, ACL-scoped authtoken, cloud endpoint forwarding to a private internal endpoint - plus the agent config that runs inside the workload, and teardown. Use when the user is building a platform that spins up isolated environments.
license: MIT
metadata:
  author: ngrok
  version: "1.0"
  category: connectivity
  surface: job
compatibility: Requires an ngrok API key for the controlplane, and the ngrok agent or an SDK inside the provisioned workload.
---

# Provision isolated access per sandbox

The job: a controlplane creates an environment - a sandbox, a container, a customer appliance - and each one needs its own reachable, isolated entry point. Not one shared endpoint with routing, but a separate set of ngrok resources per workload, created and destroyed with it.

This differs from `expose-localhost` in lifecycle and trust. There, a developer exposes their own machine and trusts themselves. Here, a platform exposes _someone else's_ workload, at machine speed, and must assume the code inside it is hostile.

## Before you start

You need an ngrok API key (not an agent authtoken) in the controlplane. See `ngrok-setup`. The provisioning calls are documented in `ngrok-surfaces` (`ngrok-surfaces/references/api.md` and `ngrok-surfaces/references/api-resources.md`); this skill is the recipe, those are the mechanics.

## The shape

```
public client
  -> cloud endpoint        (stable public URL/address, always on, runs the policy)
  -> forward-internal      (Traffic Policy)
  -> internal endpoint     (no public address; only reachable via forward-internal)
  -> ngrok agent inside the workload
  -> the local service (sshd, HTTP server, database)
```

The public side is provisioned by your controlplane before the workload boots. The internal side is created by the agent from inside the workload when it starts. They rendezvous on an agreed internal hostname, which is why that hostname has to be derived, not invented.

## 1. Derive a stable identifier

Pick the UUID your own object model already uses for whatever owns the environment - the sandbox record, the tenant, the session. Every ngrok resource you create is named and tagged from it.

Do not mint a new identifier for ngrok's benefit. The whole point is that ngrok's state can be reconciled against yours later, and that requires a shared key.

The internal hostname is derived from it too: `tcp://sandbox-<uuid>.internal:22`. Both sides of the rendezvous compute the same string from the same UUID, so neither has to discover the other.

## 2. Create the identity and address

In the controlplane, before the workload starts:

- **Service user** (`POST /service_users`) - owns the credential, so it is not attached to an employee account. Note this resource takes only `name`, no metadata; put the identifier in the name.
- **A public address**, which differs by protocol:
  - **Raw TCP** (SSH, RDP, a database) -> `POST /reserved_addrs`. ngrok assigns the
    `host:port` and returns it as `addr`. Takes a `region` (`us` unless the
    workload's users are elsewhere), fixed at creation.
  - **HTTP/TLS** -> `POST /reserved_domains`. You choose the hostname and it comes
    back as `domain`, not `addr`. No `region` - that field is deprecated for
    domains. A custom domain also needs its `cname_target` set in DNS before it
    resolves; an ngrok-owned subdomain needs no DNS step, which is usually what you
    want when provisioning per workload.

Fill `description` with something a human can identify in the dashboard and `metadata` with a JSON string carrying your UUID. See `ngrok-surfaces` for why both, and for the exact bodies.

## 3. Mint a credential that can do exactly one thing

This is the load-bearing security step.

```json
{
  "description": "Agent authtoken for sandbox <uuid>",
  "metadata": "{\"sandbox_id\":\"<uuid>\"}",
  "acl": ["bind:tcp://sandbox-<uuid>.internal:22"],
  "owner_id": "<service user id>"
}
```

The `bind:` ACL restricts the token to creating that one endpoint and nothing else. **Without an ACL the token can create any endpoint on your account** - and this token is about to be placed inside a workload running untrusted code. Assume it will leak. With the ACL, a leaked token buys an attacker the ability to bind an endpoint that is already theirs.

The `token` comes back once and only once. Write it straight into the sandbox provider's secret store in the same code path; never log it or pass it back through your own API.

## 4. Create the cloud endpoint

`POST /endpoints` with `type: "cloud"`, `bindings: ["public"]`, and `url: "tcp://{addr}"` from step 2. Its Traffic Policy forwards to the internal endpoint the workload will later create:

```yaml
on_tcp_connect:
  - actions:
      - type: forward-internal
        config:
          url: tcp://sandbox-<uuid>.internal:22
```

For HTTP workloads it is `on_http_request` and an `https://` internal URL. The policy is passed to the API as a serialized string - see `ngrok-surfaces`.

This endpoint exists immediately and is stable. It will refuse connections until the agent inside the workload comes up and binds the internal endpoint, which is the correct behavior: the address is allocated at provision time, reachable at boot time.

Because the policy lives at the edge and not in the workload, this is also where you add controls the sandbox cannot remove. On a TCP endpoint you can add `restrict-ips` or `deny` in `on_tcp_connect`. On an HTTP endpoint, those actions are available, as well as `oauth` and `rate-limit`. See `secure-endpoint` for more details.

## 5. Configure the agent inside the workload

The workload needs: the authtoken in its environment, the ngrok agent binary, and a config file naming the internal endpoint.

```yaml
version: 3
endpoints:
  - name: ssh
    # must match what the cloud endpoint forwards to, and what the ACL allows
    url: tcp://sandbox-<uuid>.internal:22
    upstream:
      url: 22
```

```bash
ngrok start --all --config /path/to/ngrok.yml
```

The authtoken comes from `NGROK_AUTHTOKEN` in the environment rather than the config file, so the token never lands on disk in the image. See `ngrok-surfaces` for the config surface generally, and `references/sandbox-ssh.md` for the full sandbox-container walkthrough including binary download and the embedded-SDK alternative.

Three strings must agree exactly: the internal URL in the agent config, the `forward-internal` target in the cloud endpoint's policy, and the `bind:` rule in the ACL. A mismatch fails as "the endpoint is up but nothing reaches it" or as an agent that cannot start at all. Generate all three from the same UUID in one function.

## Tear it down

When the environment is destroyed, delete in reverse order: endpoint, credential, the reserved TCP address or HTTP domain, service user. Store each `id` against your record at create time.

Then run reconciliation anyway. Provisioning is a multi-call sequence that will fail partway through; a job that lists ngrok resources, parses `metadata`, and deletes those whose parent is gone is not optional at scale. `ngrok-surfaces` covers the delete calls.

## Scenarios

**Ephemeral dev sandboxes.** The case above. SSH over a reserved TCP address, one per sandbox, torn down with the sandbox. Full walkthrough in `references/sandbox-ssh.md`.

**Customer-premises devices or networks.** Same resource set, longer-lived. One service user and ACL-scoped token per customer site so a compromise at one customer cannot touch another. Often several internal endpoints behind one agent (SSH, RDP, a database), each with its own cloud endpoint.

**Per-developer preview environments.** A wildcard reserved domain and one cloud endpoint can serve everyone, routing on hostname to `<alias>.internal`, with a per-developer token scoped `bind:<alias>.internal`. See `secure-endpoint` for the access-control side.

## Notes for agents

- Make the sequence idempotent and retry-safe, keyed on the caller's UUID. Partial provisioning is the normal failure mode.
- Never suggest reusing one authtoken across tenants, and never suggest an unscoped token for a workload running user code. If the user proposes it, say plainly what it costs them.
- Do not put the authtoken in a container image, a config file baked into the image, or logs. Environment variable from the provider's secret store.
- Prefer the agent binary for a first implementation. Embedding ngrok in an existing process via an SDK (`ngrok-surfaces`) removes a moving part and may be the right end state, but it is harder to debug when the endpoint URL is wrong.
- If the user is on Kubernetes, the operator may be a better fit than raw API calls; see `ngrok-surfaces`.
