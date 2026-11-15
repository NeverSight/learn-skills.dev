---
name: tailscale-superpowers
description: Tailscale workflows for personal Macs/devices with safety tiers. Use when routing traffic through home, sending files, fixing or setting up a Mac remotely, sharing localhost, replacing localhost links with tailnet links (tailnet-url, localhost hook), checking slow/offline machines, coordinating agents, reaching printers/NAS, granting scoped contractor access, getting files someone else shares, checking who can reach your devices, using one-word shortcuts, clipboard handoff, or optional tailscale-pp-cli admin actions.
license: MIT
---

# Tailscale Superpowers

Pro Tailscale workflows for every device you own.

A community skill for Tailscale. It isn't made by, affiliated with, or endorsed by Tailscale Inc.

These recipes cover everyday jobs for people who run AI agents on a few Macs. A few of them need an admin step, like approving a route or adding a Taildrive rule. If the user has set up `tailscale-pp-cli` (see "Optional: the admin CLI" below), the agent can do those steps, with a plan first. Otherwise the user does them in the admin console. For other admin work, such as users or auth keys, point the user to Tailscale's official skill: https://github.com/tailscale/tailscale-skill

Talk to the user in plain English. Define tailnet, exit node, SSH, and relay the first time you use them. Use example names like home-mac, laptop, and phone, never real device names in anything you write down.

## Safety tiers

Every command in the recipes is labeled with one of these. Follow the tier even when the user sounds sure.

**Run freely.** Read-only: `tailscale status` (including `--json`), `ping`, `netcheck`, `ip`, `whois`, `whoami`, `version` (including `--upstream`), `get`, `dns status`, `exit-node list`, `exit-node suggest`, `serve status`, `funnel status`, `switch --list`, `file cp --targets`, `file get` into a folder the user named, `scripts/check-all-macs.py`, and `scripts/screen-sharing-list.py` without `--yes`. Also the look-only helpers the recipes use: `nc -z` port checks, `ssh -G`, `ippfind`, `lpstat`, `who`, `tmux ls`, and `defaults read`. From `tailscale-pp-cli`: `doctor`, `devices expiry`, `devices inspect`, `routes overview`, `shares audit`, `access check`, `policy restore --list`, `tailnet users list`, `tailnet acl get`, `tailnet logging list-configuration-audit-logs`, the plan-first write commands below when run without `--yes`, which only print a plan, and any `tailscale-pp-cli` command run with `--dry-run`.

**Ask first.** Show the exact command and wait for a yes: set or clear an exit node, send a file, `serve`, SSH into the user's own machine, offer or stop offering a home network range (`--advertise-routes`), add or remove a printer, add an SSH key, edit `~/.ssh/config` or `~/.zshrc`, run `scripts/screen-sharing-list.py --yes`, save a link in Screens 5, switch Taildrive's hidden setting on or off, and the three Services commands in `tailscale-pp-cli` (`tailnet services update`, `update-device-approval` and `delete`), each previewed with `--dry-run` first.

**Ask first and name the risk.** Show the command, say the risk in one sentence, then wait for a yes: `funnel` (public internet), `down` or `logout`, `switch` to another account (it takes the device off your tailnet), turning on Remote Login or Screen Sharing, giving anyone else a way into the user's Mac, anything on another person's device, and anything that could cut the connection you're using. If you reach this machine over SSH or Tailscale, changing its exit node or running `down` can lock you out. From `tailscale-pp-cli`, any of these with `--yes`: `routes approve`, `routes unapprove`, `shares revoke`, `policy add-entry`, and `policy restore`. Run the command without `--yes` first, show the user the plan, say the risk, then run it again with `--yes`.

**Never.** Create or delete auth keys, edit the policy file by hand, add or remove users, touch the admin console, or turn off key expiry. Don't use `tailscale-pp-cli`'s raw admin API commands either, such as `tailnet acl set`, `tailnet keys create`, `users delete`, or `device delete`. Use only the plan-first commands listed in the tiers above. When a recipe needs something from this list, such as sharing a machine or turning off key expiry, tell the user what to click and let them do it.

Show the undo next to every change, before you run it.

## Step one: find the CLI

`tailscale` in the recipes means the command-line tool. Find it before anything else. Check PATH, then the Mac app, then Homebrew:

```sh
command -v tailscale \
  || ls /Applications/Tailscale.app/Contents/MacOS/Tailscale \
  || ls /opt/homebrew/bin/tailscale /usr/local/bin/tailscale
```

Then confirm it runs (run freely): `<path> version`.

What to tell the user, depending on what you found:

- **On PATH.** Nothing to fix.
- **Inside the app.** The Mac app keeps the tool inside itself and doesn't add it to PATH, so typing `tailscale` in Terminal says "command not found". Run it by full path: `/Applications/Tailscale.app/Contents/MacOS/Tailscale status`. Use that path wherever a recipe says `tailscale`. If a script opens the app window instead of printing output, Tailscale's docs say to set `TAILSCALE_BE_CLI=1`.
- **Want plain `tailscale` in their own Terminal?** Ask first, since it edits their shell settings. Add `alias tailscale="/Applications/Tailscale.app/Contents/MacOS/Tailscale"` to `~/.zshrc`. Undo: delete that line. Agent shells often skip aliases, so keep using the full path yourself.
- **Standalone app** (downloaded from tailscale.com, or `brew install --cask tailscale-app`): the user can open the app's Settings, find the CLI integration section, choose Show me how, then Install Now. That puts `tailscale` at `/usr/local/bin/tailscale` and asks for their Mac password, so they do it.
- **Homebrew formula** (`brew install tailscale`): the open-source version, at `/opt/homebrew/bin/tailscale` on Apple silicon or `/usr/local/bin/tailscale` on Intel.
- **Linux:** usually already on PATH after install. **Windows:** `C:\Program Files\Tailscale\tailscale.exe`.
- **Nowhere.** Tailscale isn't installed. See [new-mac-setup.md](references/new-mac-setup.md).

Which Mac app it is matters. If `/Applications/Tailscale.app/Contents/_MASReceipt` exists, it's the Mac App Store version. That version can't run `tailscale ssh`, and Apple's sandbox limits which files it can send.

## Optional: the admin CLI

`tailscale-pp-cli` is a separate, open-source command-line tool for Tailscale's admin API, published in the [Printing Press library](https://github.com/mvanhorn/printing-press-library/tree/main/library/cloud/tailscale). It isn't made by Tailscale either. With it, the agent can approve a route or exit node, add a Taildrive rule, check sign-in expiry for every device, revoke a pending share, and give an always-on app a stable name (Tailscale Services, see [links-not-localhost.md](references/links-not-localhost.md)), with a plan before anything changes. Install it when a recipe needs an admin step and the user would rather the agent did it.

Check whether it's installed (run freely): `command -v tailscale-pp-cli`.

To install it, ask first:

```sh
npx -y @mvanhorn/printing-press-library install tailscale
```

That installs the CLI and its own agent skill. Without Node, `go install github.com/mvanhorn/printing-press-library/library/cloud/tailscale/cmd/tailscale-pp-cli@latest` works too.

It needs an API access token. The user creates one in the admin console under **Settings**, **Keys**, **Generate access token**, and puts it in their environment as `TAILSCALE_API_KEY`. The agent never creates the token. A short expiry is fine, and a day covers a one-off job. Check it works (run freely): `tailscale-pp-cli doctor`.

How it stays safe:

- Its plan-first commands (routes, policy, shares) print a plan and change nothing until you add `--yes`. The Services commands run straight away, so preview each one with `--dry-run`.
- Approving or removing a route keeps every other route the device already has.
- A policy change is checked by Tailscale first, saved as a local backup, shown as a diff, and refused if someone else changed the policy in between.

`self` means this machine. No CLI, or no token? Use the admin console steps in each recipe.

## Links to things on this computer

Never give the user a `localhost` link; it only opens on this machine. Run `scripts/tailnet-url <port> [path]` and give them the link it prints. Where the `localhost-guard` hook is installed, it does this itself: any localhost link left in a reply gets a working tailnet link shown under it, with no agent step. Setup and stable names: [links-not-localhost.md](references/links-not-localhost.md).

## Recipes

- [travel-wifi.md](references/travel-wifi.md): hotel or plane wifi you don't trust. Send your traffic through your home Mac.
- [send-a-file.md](references/send-a-file.md): send a file to your phone or another Mac with Taildrop.
- [help-family-mac.md](references/help-family-mac.md): help fix a family member's Mac over SSH, with their consent.
- [new-mac-setup.md](references/new-mac-setup.md): install Tailscale on a new Mac, then let an agent finish the setup.
- [open-site-on-phone.md](references/open-site-on-phone.md): open a site running on your laptop from your phone.
- [links-not-localhost.md](references/links-not-localhost.md): make agents give tailnet links instead of localhost, with a script, a hook, and optional stable names.
- [public-demo.md](references/public-demo.md): share a local site publicly for a demo, then turn it off.
- [is-it-online.md](references/is-it-online.md): is my other Mac online, and why is it slow?
- [agents-talk.md](references/agents-talk.md): let agents on different machines ask each other for help.
- [check-all-macs.md](references/check-all-macs.md): check every device at once, with how it's connected and when its sign-in expires.
- [see-the-screen.md](references/see-the-screen.md): see and control your home Mac's screen with Screen Sharing, and list every tailnet Mac in Screen Sharing or Screens 5.
- [agents-from-phone.md](references/agents-from-phone.md): check on an agent running on your home Mac from your phone.
- [shared-folders.md](references/shared-folders.md): share a folder between your Macs with Taildrive, and when Dropbox is the better fit.
- [home-network.md](references/home-network.md): reach your home printer, network drive, or router page from anywhere.
- [files-from-someone-else.md](references/files-from-someone-else.md): someone says they'll share files with you over Tailscale. Work out which case you're in and open them.
- [contractor-access.md](references/contractor-access.md): give a contractor access to one Mac, then take it away.
- [who-can-reach-my-macs.md](references/who-can-reach-my-macs.md): check whether another person can reach any of your Macs, and close the gaps.
- [one-word-shortcuts.md](references/one-word-shortcuts.md): type one word to get into another Mac.
- [paste-to-another-mac.md](references/paste-to-another-mac.md): put text on another Mac's clipboard over SSH.
