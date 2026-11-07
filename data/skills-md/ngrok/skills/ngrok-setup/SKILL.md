---
name: ngrok-setup
description: Get authenticated and ready to use ngrok on whatever surface the task needs - agent CLI, an SDK, or infrastructure-as-code. Detects what is already installed, walks the one-time authtoken step, and routes to the right surface. Use before other ngrok tasks, or whenever an ngrok command fails with an authentication or configuration error. Use when the user says "set up ngrok", "install ngrok", "add my authtoken", "ngrok isn't authenticated", or "getting an auth error from ngrok".
license: MIT
metadata:
  author: ngrok
  version: "1.0"
  category: setup
  surface: job
compatibility: Requires the ngrok CLI, an ngrok SDK, or an ngrok API key, depending on the surface chosen.
---

# Set up ngrok

Get the user authenticated and pointed at the right surface. Every ngrok action requires an authtoken (agent/SDK) or an API key (IaC) - there is no unauthenticated mode; this is deliberate abuse prevention.

## 1. Figure out the surface

Pick from what the user is doing, then defer the how-to to that surface skill:
`ngrok-surfaces` carries the routing table and the per-surface mechanics - read it off the user's project rather than asking. In short: a terminal means the agent CLI, an ngrok dependency in a manifest means the SDK, `*.tf` or k8s manifests mean infrastructure-as-code, and a controlplane provisioning per-tenant resources means the REST API.

If it is not obvious, the terminal path is the safe default for one-off tasks.

## 2. Authenticate

**CLI / SDK (authtoken):**
1. Check for an existing token: `ngrok config check`, and check the `NGROK_AUTHTOKEN` env var.
2. If none is set, **have the user set it themselves - do not ask them to paste the token to you.** Give them the link and the exact command to run:

   > Grab your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken, then run:
   > `ngrok config add-authtoken <YOUR_TOKEN>`

   On a headless box, or where the token comes from a secret store, `export NGROK_AUTHTOKEN=<YOUR_TOKEN>` in their environment does the same job.
3. Tell them to say when it is done, then re-run `ngrok config check` to confirm and carry on with the original task. Run every *other* ngrok command yourself - the authtoken is the one step that stays with the user.

**IaC and the REST API (API key):** Terraform, the operator, and `api.ngrok.com` authenticate with an ngrok API key (the operator needs an API key *and* an authtoken), not the agent authtoken. Point the user to https://dashboard.ngrok.com/api-keys and have them set it as the provider/operator credential or `NGROK_API_KEY`. See `ngrok-surfaces`.

The two credentials are not interchangeable and have very different blast radii: an API key administers the account, an authtoken only starts agent sessions. If a call fails with an auth error, check which one is in play before rotating anything.

## 3. Make sure the tool is present

- CLI: if `ngrok` is not installed, install it (`brew install ngrok`, or the platform package). Confirm with `ngrok --help`.
- SDK: ensure the ngrok package for the language is a project dependency; see `ngrok-surfaces`.
- IaC: ensure the provider/operator is configured; see `ngrok-surfaces`.
- REST API: no tool to install - confirm the key works with a read call before writing provisioning code.

## 4. Hand back

Once authenticated and the surface is ready, return to whatever the user actually asked for (expose a service, receive webhooks, etc.).

## Notes for agents

- **Never ask the user to paste an authtoken, API key, or any other secret into the chat**, and never accept one offered that way - tell them to set it themselves and continue once they confirm. A secret in a transcript has left their control: it is logged, and it is in your context for the rest of the session.
- This is a single one-time action per machine. Frame it that way, not as a wall.
- If a secret does end up in the conversation, do not repeat, echo, or print it. Acknowledge that it is set and move on, and suggest rotating it. The same goes for any token minted by `POST /credentials`.
- If a later ngrok command fails with an auth error, come back here rather than retrying blindly.
