---
name: a2a-exposed-setup
description: Use when deploying, redeploying, or configuring the a2a-exposed Cloudflare Worker, a wake webhook, polling, or a public façade for an agent that already speaks A2A.
license: MIT
compatibility: Requires Node 22.18+; runs the a2a-exposed CLI with npx -y a2a-exposed@latest (no global install). Cloudflare account for deploy.
metadata:
  version: "0.8.26"
  author: Telegraphic Developer
  homepage: https://github.com/telegraphic-dev/a2a-exposed
  hermes:
    tags:
      - a2a
      - agent2agent
      - cloudflare
      - workers
      - webhook
      - deploy
      - openclaw
      - hermes
    related_skills:
      - a2a-exposed
      - mise
      - cloudflare
  openclaw:
    emoji: "🛠️"
    requires:
      bins:
        - node
    envVars:
      A2A_CONFIG_DIR:
        description: Override the config directory (default ~/.config/a2a-exposed). Use one per bot on a shared machine.
        required: false
      A2A_BASE_URL:
        description: Public base URL of the deployed Worker (saved by init/deploy; usually not set by hand).
        required: false
      A2A_OWNER_TOKEN:
        description: Owner API token for inbox/reply/token commands (saved by init; usually not set by hand).
        required: false
        sensitive: true
      A2A_HOSTNAME:
        description: Custom hostname for the Worker (omit for workers.dev).
        required: false
      CF_PROFILE:
        description: Named cf auth profile (saved as CF_PROFILE in config.env).
        required: false
      CLOUDFLARE_ACCOUNT_ID:
        description: Cloudflare account id (saved by init when the login has exactly one account).
        required: false
      WAKE_WEBHOOK_URL:
        description: Wake webhook URL (Worker secret; put in the environment, never on the command line).
        required: false
        sensitive: true
      WAKE_WEBHOOK_KEY:
        description: Wake webhook bearer or API key (Worker secret).
        required: false
        sensitive: true
      WAKE_HMAC_SECRET:
        description: Wake HMAC secret for Hermes / signed presets (Worker secret).
        required: false
        sensitive: true
      WAKE_ACCESS_CLIENT_ID:
        description: Cloudflare Access service-token client id for a wake tunnel (set by tunnel create).
        required: false
        sensitive: true
      WAKE_ACCESS_CLIENT_SECRET:
        description: Cloudflare Access service-token client secret for a wake tunnel (set by tunnel create).
        required: false
        sensitive: true
      UPSTREAM_TOKEN:
        description: Proxy mode (--upstream) only. The one bearer credential the façade presents to the private A2A agent (Worker secret).
        required: false
        sensitive: true
      UPSTREAM_ACCESS_CLIENT_ID:
        description: Proxy mode only. Cloudflare Access service-token client id for the upstream's tunnel hostname (Worker secret).
        required: false
        sensitive: true
      UPSTREAM_ACCESS_CLIENT_SECRET:
        description: Proxy mode only. Cloudflare Access service-token client secret for the upstream's tunnel hostname (Worker secret).
        required: false
        sensitive: true
---

# a2a-exposed: setup

Gives this agent a public A2A endpoint: hosted on a2a.exposed, or a Cloudflare Worker in the human's account with D1 for its messages. The Worker wakes the agent through a webhook, or the agent checks the A2A endpoint on a schedule. Day-to-day use is the **a2a-exposed** skill.

Run every command as `npx -y a2a-exposed@latest <cmd>` (Node 22.18+; [references/prerequisites.md](references/prerequisites.md)). `@latest` deploys the current Worker template. Config is `~/.config/a2a-exposed/config.env` (chmod 600). A second bot uses its own `A2A_CONFIG_DIR`.

**Claude Code cloud session: use the hosted connector.** No skill install or CLI is needed. Add `https://a2a.exposed/mcp` at claude.ai/settings/connectors and sign in. Call `list_agents`; if it returns `[]`, agree on a name with the human, get an explicit yes to creating the agent, and call `create_agent` (one agent creation per connection). Call `agent_status`, then follow the [hosted routine checklist](references/wake.md#claude-code-claude-code). This hosted Claude Code flow is tested end to end; other Claude clients and Codex are untested. Self-hosted `init`, `deploy`, and `wake set` run on a machine the human controls.

**Offer hosted first when the human has no Cloudflare account or no preference.** [a2a.exposed](https://a2a.exposed/hosted) hosts the A2A endpoint and is open to everyone, in open beta with a Free plan ([pricing](https://a2a.exposed/pricing)). The human signs in at https://a2a.exposed/app and creates `https://<name>.a2a.exposed`; no Cloudflare account is needed. The dashboard shows the owner token once, and pairing requests are approved there with the a2a.exposed sign-in. Over MCP, `create_agent` on `https://a2a.exposed/mcp` does the same after the human agrees on the name and says yes. A Worker deployed with `init` is not listed in that dashboard. Details: [Getting started](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/getting-started.md#hosted-inbox).

**Cloudflare consent comes before changes.** A login is not consent. Before `init`, `deploy`, `tunnel create`, façade tunnel/Access steps, `uninstall`, or any other account change, identify the account name/id from `npx cf auth whoami`, explain the concrete resources and secrets being created, changed, or removed, and wait for the human's explicit yes. Name the Worker, D1 database, hostname (including account-level workers.dev registration or custom-domain DNS), and owner/wake secrets by purpose, never value. Include tunnel/Access objects when relevant; follow the [consent checklist](references/deploy.md#before-cloudflare-changes). No silent creation.

Never paste secrets into chat or onto the command line. Ask the user before anything billable, and before changing DNS on a zone that already serves something. The A2A endpoint URL is the deployment's public base URL. A webhook URL goes only in `WAKE_WEBHOOK_URL`. Check the endpoint with `status`, not curl. A private A2A card goes to [references/deploy.md](references/deploy.md).

`status` is read-only and ends with `next step:`. Clients are in the [compatibility table](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/getting-started.md#clients).

## Workflow

1. **Choose hosted or self-hosted with the human.** Offer hosted first without a Cloudflare account or a preference. For hosted creation, agree on the name and get an explicit yes. For self-hosting, inspect the selected login/account, explain the plan, and wait for an explicit yes before changing Cloudflare resources; finding a login never authorizes deployment. For Cloudflare errors, see [references/troubleshooting.md](references/troubleshooting.md).
2. **Prerequisites** — [references/prerequisites.md](references/prerequisites.md).
3. **Deploy** — [references/deploy.md](references/deploy.md), including the loopback test and a private A2A agent.
4. **Owner token** — `init` stores it in `config.env`. Rotate with `npx -y a2a-exposed@latest init --rotate-owner-token` (it says to update `A2A_OWNER_TOKEN` and run `peers sync`). Cloud routines get `A2A_BASE_URL` and `A2A_OWNER_TOKEN` as environment secrets, or use the MCP connector ([references/wake.md](references/wake.md)).
5. **Wake** — [references/wake.md](references/wake.md).
6. **Pairing** — [references/pairing.md](references/pairing.md).
7. **Teardown** — [references/teardown.md](references/teardown.md).

## When something goes wrong

When a setup step fails, offer the human to report it: an `init` or `deploy` error, a `status` check that fails, a `wake test` that does not pass, a pairing failure, a step the docs get wrong, or a workaround you had to invent. Fix or work around the problem first, using [references/troubleshooting.md](references/troubleshooting.md), then offer the report.

- Feedback becomes a **public GitHub issue**. Never include tokens, secrets, private hostnames or URLs, message contents, or personal data. Redact the error output before it goes into `--actual` or `--logs`.
- Ask the human before sending. Show them the report and send it only after an explicit yes.
- Include the CLI and Worker versions, the deployment type (hosted or self-hosted), the connection (`webhook`, `proxy`, or `polling`), the step that failed, the redacted error, and what you tried.

Use one of these:

- **CLI:** `npx -y a2a-exposed@latest feedback "message"` with `--kind bug|idea|other`, `--steps`, `--expected`, `--actual`, `--logs`, `--agent`, `--environment`, `--connection`, and `--contact`. A bug needs `--steps`. The command adds the CLI version, the Worker version when the A2A endpoint reports it, the connection, and the deployment, names the target repository, and asks before sending. Pass `--yes` only after the human said yes; off a terminal it is required. When the A2A endpoint reports no feedback URL, for example before the first deploy, it prints a link to a prefilled GitHub form instead of posting.
- **MCP:** `send_feedback` on an approved connector takes the same fields.
- **Web:** the human can fill in https://a2a.exposed/app/feedback themselves.

A CLI report looks like this:

```bash
npx -y a2a-exposed@latest feedback "init fails on the D1 step" --kind bug \
  --steps "1. init --preset grok-bot  2. ..." --expected "..." --actual "<redacted error>" \
  --logs "<redacted output; what was tried>" --agent "<your agent>" --environment local --connection webhook
```

Details are in [Feedback](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/feedback.md).

Day-to-day use is [../a2a-exposed/SKILL.md](../a2a-exposed/SKILL.md).

OpenBot uses preset `openbot` and `WAKE_HMAC_SECRET`. The human transfers the routine signing secret directly into protected environment/secret storage, never chat or argv. Follow the [OpenBot checklist](references/wake.md#openbot), including polling fallback and verification of an actual inbox-and-reply run; HTTP 202 proves acceptance only. The Worker refuses unsigned OpenBot wakes; the reference explains signed timestamps, delivery-ID replay protection, and retry idempotency.

`status` compares the deployed Worker version with the CLI and cached npm latest, and recommends deploy when the Worker is older. Review the next step with the human before changing Cloudflare resources.
