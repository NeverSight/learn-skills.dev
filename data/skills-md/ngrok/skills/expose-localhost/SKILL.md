---
name: expose-localhost
description: Expose a local service to the public internet using ngrok. Starts a tunnel, optionally adds OAuth or WAF via Traffic Policy. Handles HTTP services and raw TCP (SSH, RDP, databases). Use when asked to expose, tunnel, share, or make a local service publicly accessible, or to reach a machine that has no public IP. Also covers sharing work-in-progress with a specific person and the dev-server quirks that break a shared preview.
license: MIT
metadata:
  author: ngrok
  version: "2.1"
compatibility: Requires ngrok CLI installed and authenticated.
---

# Expose Localhost

Expose a local service to the public internet using ngrok. Optionally add OAuth, OWASP protection, or rate limiting via Traffic Policy.

## Prerequisites

- ngrok CLI installed (`ngrok` command available)
- Auth token configured (`ngrok config add-authtoken <TOKEN>`)

## Workflow

### Step 1: Pre-flight & Configuration

Silently verify ngrok is ready:

```bash
ngrok config check
```

If auth token missing, tell user to run: `ngrok config add-authtoken <TOKEN>` (get token at https://dashboard.ngrok.com/get-started/your-authtoken)

Then **ask all questions upfront** before doing anything:

```
Before I expose your service, I need a few details:

1. **Port**: I see your app runs on port 3000. Is that correct?
2. **Domain**: Use your dev domain, or do you have a custom domain?
3. **Access control**: Open access, or require login (Google/GitHub/etc.)?
4. **Save config?**: One-time setup, or save for reuse?
```

Do NOT mention cloud endpoints, reserved domains, or internal endpoints — those are advanced concepts the user shouldn't need to think about.

**Detecting the port**: Check `package.json` scripts for `--port`, `.env` for `PORT=`, `docker-compose.yml` for port mappings.

**Is it even HTTP?** If the user says SSH, RDP, a database, or names a port like 22, 3389, 5432, or 3306, this is a raw TCP service — skip to [Non-HTTP Services (TCP)](#non-http-services-tcp). The domain and access-control questions above do not apply there.

**Domains**: Most ngrok accounts have a free static dev domain (e.g., `something.ngrok-free.dev`). Running `ngrok http PORT` uses it automatically. Users can also provide a custom domain configured in the ngrok dashboard. Some accounts (especially new ones) may not have a dev domain yet — if ngrok fails with `ERR_NGROK_15013`, tell the user: "You don't have a dev domain yet. Claim your free one at https://dashboard.ngrok.com/domains — then we can try again."

**If user requests OAuth**, also ask: "Should only specific people be able to access it? I can restrict by email address or email domain."

After gathering answers, confirm and get a Y/n before proceeding.

### Step 2: Start the Tunnel

#### No security (simplest)

```bash
ngrok http {PORT} &
sleep 3
curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | head -1
```

With a specific domain, add `--url https://{DOMAIN}`.

#### With security (Traffic Policy)

Create the traffic policy file first, then start ngrok with it.

**OAuth-only** (default when user requests auth):

```yaml
on_http_request:
  - actions:
      - type: oauth
        config:
          provider: google
```

Replace `google` with the chosen provider (google, github, microsoft, gitlab, linkedin, twitch).

If the user requests OAuth, default to OAuth-only. Do NOT add OWASP or rate limiting unless explicitly asked — OAuth already blocks unauthenticated access.

**OAuth with email restriction** — use a separate rule with a CEL expression to deny non-matching emails. Do NOT add an `allow` field to the OAuth action.

Single email:

```yaml
on_http_request:
  - actions:
      - type: oauth
        config:
          provider: google
  - expressions:
      - "actions.ngrok.oauth.identity.email != 'user@example.com'"
    actions:
      - type: deny
        config:
          status_code: 403
```

Email domain:

```yaml
on_http_request:
  - actions:
      - type: oauth
        config:
          provider: google
  - expressions:
      - "!actions.ngrok.oauth.identity.email.endsWith('@your-company.com')"
    actions:
      - type: deny
        config:
          status_code: 403
```

Multiple emails — name the identity explicitly on the left of `in`:

```yaml
  - expressions:
      - "!(actions.ngrok.oauth.identity.email in ['a@x.com', 'b@x.com'])"
    actions:
      - type: deny
        config:
          status_code: 403
```

**Shared secret** (when the person won't log in with an IdP — an external client, a
reviewer without a company account):

```yaml
on_http_request:
  - actions:
      - type: basic-auth
        config:
          credentials:
            - "reviewer:{PASSWORD}"
```

Hand them the URL and the password over a channel you already trust. If they have a
stable IP, `restrict-ips` is an alternative with nothing to share.

**Open-access hardening** (no auth, but wants protection):

```yaml
on_http_request:
  - actions:
      - type: rate-limit
        config:
          name: default-rate-limit
          algorithm: sliding_window
          capacity: 200
          rate: "60s"
          bucket_key:
            - conn.client_ip
      - type: owasp-crs-request
        config:
          on_error: halt

on_http_response:
  - actions:
      - type: owasp-crs-response
        config:
          on_error: halt
```

After writing the policy file, start ngrok:

```bash
ngrok http {PORT} --traffic-policy-file .ngrok/traffic-policy.yml &
sleep 3
curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | head -1
```

Add `--url https://{DOMAIN}` if using a specific domain.

**Sharing a dev server?** Vite, Next, and webpack reject requests whose Host header
isn't localhost, and their hot-reload websockets need the ngrok domain allowed. Set
this up before handing over the URL — see `references/TROUBLESHOOTING.md`.

### Step 3: Handle Errors

If a traffic policy action fails due to plan limitations:

1. Tell the user which specific action requires an upgrade
2. Offer to remove that action from the policy and retry
3. Do NOT suggest switching to cloud endpoints as a workaround

### Step 4: Persistent Configuration (If Requested)

Save these files to the project:

- **`.ngrok/traffic-policy.yml`** — the policy (if security was configured)
- **`.ngrok/expose.sh`**:

```bash
#!/bin/bash
set -e
echo "Your service will be at: https://{DOMAIN}"
ngrok http {PORT} --url https://{DOMAIN} --traffic-policy-file .ngrok/traffic-policy.yml
```

Omit `--traffic-policy-file` if no policy. Omit `--url` if no specific domain.

Optionally add to `package.json`:

```json
{ "scripts": { "tunnel": "bash .ngrok/expose.sh" } }
```

## Teardown

```bash
pkill ngrok
```

## Non-HTTP Services (TCP)

For SSH, RDP, or a database, use `ngrok tcp` instead of `ngrok http`.

```bash
ngrok tcp {PORT} &
sleep 3
curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | head -1
```

ngrok returns an address like `tcp://1.tcp.ngrok.io:12345`. The host and port are
used separately by the client:

```bash
# local sshd on port 22, reached through the address above
ssh -p 12345 {USER}@1.tcp.ngrok.io
```

Common ports: SSH `22`, RDP `3389`, PostgreSQL `5432`, MySQL `3306`.

**The address changes on every restart.** For one that persists, reserve it first.
ngrok assigns the hostname and port — unlike domains, you cannot choose them:

```bash
ngrok api reserved-addrs create --description "SSH for {NAME}" --region us
ngrok tcp {PORT} --url tcp://{ADDR}
```

Reserved TCP addresses need a paid plan and keep billing until deleted.

**Access control is different here.** OAuth and OWASP are HTTP-only and will not
work. TCP policies run in the `on_tcp_connect` phase, where `restrict-ips` is the
usual control:

```yaml
on_tcp_connect:
  - actions:
      - type: restrict-ips
        config:
          enforce: true
          allow:
            - 203.0.113.0/24
```

Attach it the same way: `ngrok tcp {PORT} --traffic-policy-file .ngrok/traffic-policy.yml`

## Cloud Endpoints (Advanced)

Only use if the user explicitly needs a URL that persists after the agent stops (e.g., webhooks, long-lived integrations).

Requires an API key: `ngrok config add-api-key <KEY>` (get at https://dashboard.ngrok.com/api-keys)

1. Reserve domain: `ngrok api reserved-domains create --domain "{DOMAIN}"`
2. Create cloud endpoint with a traffic policy that includes `forward-internal` as the **last** action:

```bash
ngrok api endpoints create --url "https://{DOMAIN}" --bindings public --traffic-policy "$(cat .ngrok/traffic-policy.yml)"
```

The traffic policy must end with:

```yaml
- type: forward-internal
  config:
    url: https://{NAME}.internal
```

3. Start the internal agent: `ngrok http {PORT} --url https://{NAME}.internal`
4. Teardown: `ngrok api endpoints delete {ENDPOINT_ID}`

## Related Skills

This skill covers giving a service a public URL. Neighbouring jobs have their own
skills — hand off rather than reimplementing them here:

- **Auth, rate limits, IP rules, or a maintenance page in general** —
  `secure-endpoint`. (Sharing a preview with one named person is handled here, in
  Step 2.)
- **It should receive webhooks** — `receive-webhooks` verifies provider signatures
  at the edge and can keep the receiver off the public internet.
- **It is an MCP server** — `run-mcp-gateway` handles per-provider credentials.
- **One endpoint per sandbox, tenant, or device, created by a controlplane** —
  `provision-sandbox-access`.
- **Something is broken** (`ERR_NGROK_*`, a 400 through the URL but not on
  localhost) — `troubleshoot-ngrok`.
- **Setup or auth problems** — `ngrok-setup`.

For the underlying model — endpoint types, HTTP vs TCP, and the full Traffic Policy
action set — see `ngrok-engine`. For applying config on a surface other than the
CLI (SDKs, REST API, Terraform, Kubernetes), see `ngrok-surfaces`.
