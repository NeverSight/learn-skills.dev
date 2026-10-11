---
name: retire-machine
description: Retire a machine the user no longer uses, such as an old VPS - take stock of what is still on it and what still points at it, save what the user wants to keep, disconnect it from the user's accounts and other machines, hand the user the provider's delete step, and record the retirement where the user keeps notes on the machine. Use when the user wants to shut down, delete, clean up or replace a server or another machine set up with /set-up-machine.
---

# Retire machine

Take a machine out of use without losing work and without leaving anything that still trusts it. The reverse of `/set-up-machine`: that skill gives a machine keys, sessions and settings, and this one takes them away again, in an order that keeps the machine reachable until the last step. The user deletes the machine at the provider; an agent never does, since deletion can't be undone.

## Parameters

- `<session-host>`: where agent sessions run, e.g. `herdr`. It is also how the agent reaches the machine.
- `<notification-method>`: how a notification reaches the user. Its configuration may list the machine as a sender.

## Steps

1. **Read the record.** Find what the user wrote about the machine: in their workstation repo, which the pointer `~/.config/agents/source.md` names, read every file that names it, any checklist for deleting it, and the issue that retires it. Note the machine that replaces it, if any.
   - **When the pointer records no workstation repo:** ask the user once where they keep notes on the machine, or go on from what the machine itself shows.
2. **Take stock, without changing anything.** Read the session host's state first: its workspaces, panes and agents. Read a pane's output; never send it keys or a prompt, and never start a stopped agent, since a resumed session reloads its whole context. Then open a new workspace on the machine for your own commands, so you don't type into a pane someone else uses. Collect:
   - **Work:** every git repository in the home folder, with its uncommitted files, unpushed commits, stashes and branches without an upstream. A repository without a remote counts as unpushed.
   - **Files outside repositories:** the visible entries in the home folder and application data under `~/.local/share`.
   - **Services:** containers and their volumes, listening ports, enabled system and user services, cron jobs and timers. A web service can run unnoticed for weeks: for port 80 or 443, read the proxy config for the name it serves.
   - **What points at the machine:** domain names, including names built from the IP such as `<ip>.sslip.io`; allow-lists; the tailnet device; SSH keys and deploy keys on GitHub; tokens created for it; and on the user's other machines, the session host's saved machine, the notification method's sender list, `~/.ssh/config` and `known_hosts`.
3. **Propose one plan** with a line per item found: keep it (and where it goes), move it to the replacement, or let it go. Ask the user once for the items you can't decide from the record. Ask also whether to keep a provider snapshot. A snapshot costs a little each month, but a closed plan line may not be orderable again.
4. **Save** what the plan keeps or moves, before anything is stopped, and check that each copy arrived.
5. **Disconnect** in this order. The session host's saved machine goes last, because it is how you reach the machine.
   1. Stop the services the plan lets go.
   2. Take the machine off the tailnet: `tailscale logout` on the machine, then check the device is gone in the admin console.
   3. Remove it from the notification method's sender list and from `~/.ssh/config` on the user's other machines. Remove its host keys with `ssh-keygen -R <host>`.
   4. Give the user the commands that revoke its access to their accounts: its SSH key and deploy keys on GitHub (`gh ssh-key list`, then `gh ssh-key delete <id>`), and each token created for it. The rule table refuses these commands to agents, since they change who can reach the account.
   5. Close your workspace on the machine, then remove the saved machine: for Herdr, `herdr machine remove <id>`, with the 32-character id `herdr machine list` prints, since the label is refused.
6. **Hand over the delete.** Give the user the provider's console link and say what to do: take the snapshot if the plan keeps one, then delete the server. A stopped server is still billed; only deletion ends the bill. The user confirms when it's done.
7. **Record** the retirement, as its own change, in each file step 1 found: say the machine is retired, with the date and where its work went, and drop or mark it where a file lists machines. Close the issue that retires it.
8. **Check** after the user deletes it: the host no longer answers SSH, and the provider's console lists no server. Report what was saved where, what was let go, and anything left for the user.
