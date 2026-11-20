---
name: public-url-hosting
description: Host a service on a stable public HTTPS URL straight from a cloud VM — start your app, run one command, get https://<box>-<port>.on.ascii.dev with managed TLS and token-gating. Raw TCP/UDP ports open on the VM's own IP address. Use to host a web app, API, demo, or webhook endpoint without DNS or certificate setup.
---

# Public URL hosting (Box)

Use this to **put a running service on the public internet** from inside a Box: a web app, an API, a demo, or a long-lived endpoint. Box handles TLS, routing, and auth — no DNS, no certificates, no separate platform.

## Recipe

```bash
box_id="$(box new --no-auto-stop --json | jq -r 'select(.event == "ready") | .id')"
box ssh "$box_id" -- bash -s < ./deploy.sh                 # build + start app on 0.0.0.0:8080
box ssh "$box_id" -- "host 8080 --public --title 'my app'"
box ssh "$box_id" -- "host url 8080"                        # https://<box>-8080.on.ascii.dev
```

`host` URLs are token-gated by default; `--public` makes them open. For a non-HTTP service, open a raw TCP/UDP port on the VM's IP address (IPv6 only on boxes without their own IPv4; the IP changes at each resume). Custom domains are not supported: put your own reverse proxy or CDN in front of the HTTPS URL.

## Why Box

- **Zero infra** — TLS + subdomain + auth managed for you.
- **Stays up** — `--no-auto-stop` (paid plan) keeps the host alive 24-7; the URL persists across resume.
- **Flat per-hour price** — $0.036/h for 4 vCPU / 8 GB, about $26/mo always on, billed per second, from a $20/mo plan (https://docs.boat.dev/pricing).

## Prereqs

`curl -fsSL https://box.ascii.dev/install | sh`, then `box login "$BOX_API_KEY" --json`.

## Limits

Runs in Germany, Finland and France (no region choice); $20 plan: 100 boxes at once. For multi-region CDN-grade hosting, use a dedicated host; Box fits single-VM services, previews, and demos.
