---
name: instant-web-publishing-with-pigeonscale
description: Publish a local directory to Pigeonscale Sites and get a live hosted URL, including first publish, approval-gated bootstrap, signed-in redeploys, site-local pigeonscale.jsonc config, and domain management. Use when an agent needs to put files on the internet with Pigeonscale, redeploy an existing site, sync site config, or manage Pigeonscale site domains.
license: MIT
metadata:
  author: Pigeonscale
  version: "0.1.2"
  homepage: https://pigeonscale.com/
---

# Pigeonscale Sites

Pigeonscale Sites publishes a local directory to the web and returns a live hosted URL. Use it for static sites, demos, landing pages, and other agent-built outputs that need to be reachable on the internet.

Run the CLI as `pigeonscale ...`. If it is not installed globally, use `npx -y pigeonscale ...`.

## When to use it

- Publish a new site from a local folder.
- Redeploy an existing site.
- Sync local site config with a known site id.
- Add, list, or verify custom domains after the site exists.

## Get started

First publish while signed out:

```bash
pigeonscale sites publish ./dist \
  --human owner@example.com \
  --name "Marketing demo"
```

First publish while already signed in:

```bash
pigeonscale sites publish ./dist --name "Marketing demo"
```

The CLI uploads the directory and returns a live site URL. After the first successful publish, `pigeonscale.jsonc` pins the site locally so later deploys can reuse it.

## What happens on first publish

- New human: publish can complete in one run.
- Existing human: publish can require approval before the flow continues.
- Some approval-required flows still upload and finalize in the same run under a temporary publish token, then exit with `status: "pending_approval"`. In that case the deployment is already staged and human approval activates it server-side.
- If the command prints `Approval required` and did not already finish with `pending_approval`, rerun the same `sites publish` command after approval.

For existing sites, prefer `--site-id` or the local `pigeonscale.jsonc` file instead of guessing site identity.

## Repeat deploys

After the first successful publish:

```bash
pigeonscale sites publish ./dist
pigeonscale sites publish ./dist --site-id ps_site_123
```

If local `pigeonscale.jsonc` is stale, sync it:

```bash
pigeonscale sites config sync ./dist --site-id ps_site_123
```

Use `--sync-config` only when the mismatch is purely stale local config. Do not bulldoze real remote settings with conflicting flags or env vars.

## Domains

Use the domains subcommands after the site exists:

```bash
pigeonscale sites domains list --site-id ps_site_123
pigeonscale sites domains add --site-id ps_site_123 example.com
pigeonscale sites domains verify example.com
```

## Local state

Pigeonscale keeps local state under `~/.config/pigeonscale/`:

- Session state lives in `~/.config/pigeonscale/session.json`.
- Pending approvals live in `~/.config/pigeonscale/pending-approvals.json`.
- Inspect pending approvals with `pigeonscale approvals status`.

Token storage uses `cross-keychain`:

- When a native credential backend exists, `session.json` stores metadata only and the actual access and refresh tokens live in the OS keychain under service `pigeonscale.session`.
- When no native backend exists, the CLI stores both tokens in `session.json` with `0600` permissions.

## Safety defaults

Default publish filtering skips `.env*`, `*.vars`, `.gitignore`, and `.pigeonscaleignore` matches, and runs a local secret scan. Keep those defaults.

Use `--skip-filter` only when the user explicitly asks to bypass filtering and understands the risk.

Hostname changes during publish require `--yes`.

## Approval edge cases

- If output says `Approval still pending`, wait and rerun only if the current command did not already finish with `status: "pending_approval"`.
- If output says `Approval denied`, stop and request a new approval instead of retrying blindly.
- If output says `Approval token invalid/expired`, rerun the publish command to mint a fresh approval.
- Signed-in site updates that need `site:manage` can also trigger `PUBLISH_SITE` approval for hostname or metadata changes.

## Constraints

- Use the cloud provider for sites.
- Do not use `--provider resend`; sites require cloud.
- Do not pass `--human` if already signed in under a different human.
- When `--slug` is set, also pass `--tld`.
- Hostname changes during publish require `--yes`.
- Prefer rerunning the same publish command after approval instead of changing flags mid-flow.
