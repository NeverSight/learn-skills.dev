---
name: server-hardening
description: Methodology for safely hardening + monitoring a remote server — phased, each phase gated by a verification check. Stack- and distro-agnostic; the agent maps each objective to the target's actual tooling.
disable-model-invocation: true
---

# Server Hardening

A repeatable, **safety-first** method for hardening and instrumenting a remote server you
administer over SSH. This skill is the *method*, not a script. It states each phase's
objective, its safety concern, and its verification gate — you translate every step into
the commands the target actually uses.

## When to use

Use when you have SSH access **and authorization** to mutate a running host, and want to
lock it down without knocking yourself out or taking apps offline.

Do **not** use to attack, scan, or modify a host you don't administer.

## First: identify the stack, then adapt

The method is deliberately generic. Before touching anything, learn what you're on and map
each phase to it:

| Concept in this skill | Find the target's actual… |
| --- | --- |
| package updates | package manager + update mechanism |
| host firewall | firewall front-end (or raw packet filter) |
| SSH daemon config | the running SSH server + its config path |
| brute-force jail | intrusion-prevention tool available on the distro |
| process manager | whatever keeps the apps running + its boot integration |
| boot services | the init/service manager |
| web front end | reverse proxy / web server, if any |
| TLS certs | the cert tool + where live certs live |

If any mapping is unclear from recon (Phase 1), ask before proceeding — don't guess a
destructive command.

## Golden rules (hold across every phase)

1. **Keep your current SSH session open** through every SSH-daemon or firewall change. A
   bad edit can lock you out; the open session is your escape hatch. Before you *trust* any
   such change, prove a **second, fresh** login succeeds.
2. **Never enable the firewall** before you have (a) allowed the SSH port and (b) accounted
   for every listening port. Blocking a port you didn't know was in use breaks a service —
   or your own access.
3. **Re-verify the running apps after every change.** Cheap to check, expensive to discover
   later.
4. **Prefer offline / FOSS tooling.** Remove internet-exposed vendor agents — they add
   attack surface, lock-in, and their own CVEs.
5. **Every phase ends in a verification gate.** Do not advance until the gate passes.

## Phased procedure

Run top-to-bottom. Each phase: **objective → safety concern → gate.**

### 0. Parameters — pin these first
Decide up front, so later steps are unambiguous:
- the target host / SSH alias
- the primary network interface
- the app / process owner account
- the set of ports that must stay publicly reachable

### 1. Recon — read-only, change nothing
**Objective:** build a full picture before mutating. Inventory: OS + version, CPU/mem/disk,
**every listening socket** and the process behind it, current firewall state, SSH-daemon
config (root login, password auth, port), interactive users and who has admin/sudo, pending
updates, configured third-party package repos, and TLS cert expiry.
**Gate:** you can name the purpose of every listening port and every admin user.

### 1b. Map every exposed port — before any firewalling  ⛔
**Objective:** for each externally-bound port, prove *what it is*. A port is safe to block
only if it's reached exclusively as a local upstream (e.g. loopback) behind the proxy.
Anything genuinely external must be added to the keep-open set.
**Safety concern:** this is the step that prevents locking out a real service.
**Gate:** every external port classified (upstream-only vs must-stay-open); get explicit
sign-off on the keep-open set before Phase 2.

### 2. Network edge — firewall + shed exposed agents
**Objective:** allow the known-good ports (SSH **first**), default-deny the rest, then
enable the firewall. Remove any internet-exposed monitoring/vendor agent and any public
route pointing at it.
**Safety concern:** order matters — allow SSH and enable in the right sequence, never the
reverse.
**Gate:** from an *external* host, the closed ports refuse; the intended apps are still
reachable; all app processes still up.

### 3. SSH hardening + brute-force protection
**Objective:** disable password login and root password login (key-only), validate the
config, reload the SSH daemon, then add a brute-force jail.
**Safety concern:** validate config *before* reload; **prove a fresh login works** before
you trust it and close your safety session.
**Gate:** a new login succeeds; the brute-force jail is active.

### 4. Resilience — swap
**Objective:** add swap if the host lacks it and would benefit (small-RAM boxes).
**Gate:** swap present and active (skip cleanly if already fine).

### 5. Patching — audit repos first  ⚠️
**Objective:** bring the system fully up to date, keeping existing configs, catching held
kernels.
**Safety concern:** **one dead third-party repo (expired cert / 404) silently blocks the
entire upgrade.** Audit configured repos first; disable or purge broken ones (and their
orphaned agent) before upgrading.
**Gate:** zero pending updates / security advisories. Note whether a reboot is now required
(handled in Phase 7).

### 6. Monitoring — offline health + traffic
**Objective:** install offline/FOSS observability and wrap it in one convenience entry
point. Conceptually the wrapper offers: a live tiled dashboard; traffic history + per-
process bandwidth ("why the spike"); merged application + system logs; and a **one-shot
text health report** suitable for a cron job that appends to a rotating logfile.
**Reference implementation:** `templates/srvmon` (dispatcher over glances/btop/vnstat/
nethogs/journalctl) and `templates/srvmon-report` (the cron-safe text report). Install both
to `/usr/local/bin`, adapt `PUB_IF` to the primary interface, then wire the report into a
cron job + logrotate as documented in the report's header — e.g. an hourly
`/etc/cron.d/srvmon-health` appending to `/var/log/srvmon/health.log`, rotated by
`/etc/logrotate.d/srvmon`.
**Gate:** the text report runs clean (and, if logged, contains no terminal escape codes).

### 7. Reboot safety + schedule
**Objective:** make the apps survive a reboot **before** you ever trigger one — persist the
process manager's state and confirm its boot service is enabled, alongside the other
services. Optionally schedule a maintenance-reboot window.
**Safety concern:** scheduling (or triggering) a reboot before proving persistence loses
the apps.
**Final gate:** new kernel active · swap up · zero pending CVEs · reboot flag clear · all
apps online · all target services active · firewall active · root SSH key-only.

### 8. Record — leave docs on the host for the next session
**Objective:** so a future session (human or agent) skips re-recon, write two Markdown files
**to the admin user's home dir** (`~`) on the target:

- **`~/README.md` — the host reference.** A living snapshot of *what this server is*: identity
  (host, provider, public/private IPs, primary interface, OS/kernel, specs, admin user), its
  purpose, **every domain it serves** (and notable ones it does *not* — e.g. names that resolve
  elsewhere), TLS reality (which cert actually serves, expiry, any orphans), web-proxy routing,
  the app/process inventory + where their configs live, the firewall model (**both** host
  firewall *and* any container-layer rules), security posture, the monitoring entry point (and
  where its health log lands), and a **gotchas/lore** section. Rewrite in place each session so
  it stays current.
- **`~/LOGBOOK.md` — append-only change journal, newest entry on top.** One dated entry per
  session: the incident (if any), each change made, decisions the owner made, and findings left
  unchanged. Never edit or delete past entries — **merge** any pre-existing logbook's history in
  rather than overwriting it (back it up first). README says *what is true now*; LOGBOOK says
  *what changed and why*. Cross-link them.

**Gate:** both files exist in `~`, README reflects the post-hardening state, and the LOGBOOK's
newest entry summarizes this session (with prior history preserved).

## Failure lore (worth encoding)

- **A dead package repo blocks *all* updates.** One third-party source with an expired cert
  or 404 makes the whole update step fail. Always audit and disable broken repos before
  patching.
- **A reboot before persistence loses the apps.** If the process manager's state isn't
  saved and its boot service isn't enabled, a reboot brings the box up with the apps down.
  Prove persistence first, reboot second.
