---
name: remote-agent-setup
description: Walk a human through putting Pi sessions on an always-on host with Tailscale, Herdr, and Moshi. Use when they want a remote agent setup, a VPS for coding agents, or to install Herdr and Pi on a server.
---

# Remote agent setup

You are on the laptop. Conduct the setup. Fetch each product's current install from its docs and run that — do not use remembered commands. Do not paste a script and leave. Do not call a layer done until its check passed. If Tailscale, Herdr, or Pi is already present, skip that install and run the check only.

## Done

Pass/fail before you start. Fill this as you go; stop at the first fail.

| Layer | Check |
| --- | --- |
| Host | SSH to the always-on machine |
| Tailscale | Reach it from the laptop over Tailscale |
| Herdr | On the host; laptop attached; detach survives |
| Pi | On the host; authenticated session in a Herdr pane |
| Moshi | Hook paired; phone round-trip to the same Pi session |
| Recovery | Snapshot/backup named, or called out as missing |

## Fetch, then install

Before each install, open the live page and follow it. Confirm against the live docs page before running.

| Layer | Docs |
| --- | --- |
| Tailscale | https://tailscale.com/docs/install/linux |
| Herdr | https://herdr.dev/docs/install/ · https://herdr.dev/docs/connecting-machines/ · https://herdr.dev/docs/persistence-remote/ |
| Pi | https://pi.dev/docs/latest/quickstart |
| Moshi | https://getmoshi.app/docs/introduction · https://getmoshi.app/docs/install-moshi-hook · https://getmoshi.app/docs/hooks |

## Do not

Keep SSH, Herdr, and Pi off the public internet. After Tailscale works, reach the host by MagicDNS or Tailscale IP with normal SSH.

Never store auth keys, pairing tokens, API keys, or `.pem` files in the skill folder, a repo, or chat.

Humans only: buy/create the VPS, Tailscale login, Moshi on the phone. You stop and wait.

Don't stop a Herdr server unless they mean to kill remote panes.

## Phases

Stop at the first failed check. Say what is blocked and who acts.

**0. Interview** — New VPS or a machine they already have? SSH already working? Default: cheap VPS, 4–8 GB RAM, not a large box. VPS vs owned is their call: rent is low start / resize / provider outage; owned is hardware / home power / physical control.

**1. Host (human)** — They create the machine and give you SSH. Check: `ssh <host>` works. If not, stop.

**2. Tailscale** — If it already joins the tailnet, skip install and run the check. Otherwise install from the Tailscale Linux page on the VPS. They authenticate. They install Tailscale on the laptop and phone. Check: normal SSH via MagicDNS or Tailscale IP. Use that as `<host>` from here. Mention key expiry on a server if their docs do.

**3. Herdr and Pi on the VPS** — If `herdr` or `pi` already exists in a **fresh** SSH login, skip that install and run its check. Otherwise install from their current docs, then prove both exist in a fresh SSH login, not the shell you just configured. Attach the laptop Herdr client using the connecting-machines page, over the Tailscale path — that step is interactive; if you have no TTY, print the command and wait. Check: the laptop sees the remote machine; detach; work on the host keeps running.

**4. Auth and a workspace (human)** — Pi on the host needs its own login. Clone only the repos they name. Check: a Pi session in a Herdr pane on the VPS can talk to a model.

**5. Moshi** — They install the app and add a connection to the VPS over Tailscale. On the host, follow the current Moshi hook docs: install the hook, pair it with the token from the app (they paste it; do not store it), and run it so it survives logout. Installing the hook wires Pi; there is no separate Pi switch. Persistence in this stack is Herdr, not another multiplexer. Check: Pi waits for input; the phone inbox shows it; the answer returns to the same session.

**6. Recovery** — Always-on is not immortal. If they have no snapshot or backup, say so. Do not call the setup finished without naming that gap.
