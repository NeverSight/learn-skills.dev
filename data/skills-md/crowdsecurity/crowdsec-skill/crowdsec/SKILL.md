---
name: crowdsec
description: Use when the user is installing, configuring, operating, or debugging CrowdSec — including cscli, LAPI/CAPI, hub collections, parsers/scenarios/whitelists deployment, bouncers (firewall, nginx, traefik, caddy), WAF (AppSec component) deployment, bot detection / AppSec challenge mode (blocking headless browsers and scrapers, allowing verified crawlers), profiles, notifications, upgrades, and fail2ban migration. Covers bare-metal/systemd, Docker, Kubernetes/Helm, and CrowdSec Console enrollment. This is an operational skill — it does not author WAF rules, scenarios, or parsers.
---

# CrowdSec — operations, deployment, configuration, and debugging

**Glossary:** *AppSec* is the engine component name (in configs, hub paths,
`cscli appsec-*`, Helm workload); *WAF* is the user-facing term for the same
thing. This skill uses both interchangeably.

## Boundary — what this skill does and does not do

| You want to… | Use |
|---|---|
| Install / upgrade / uninstall CrowdSec | this skill |
| Configure acquisition, hub, profiles, notifications | this skill |
| Install and wire a bouncer (firewall, nginx, traefik, caddy) | this skill |
| Deploy the WAF (AppSec component) | this skill |
| Deploy and tune bot detection (AppSec challenge mode) | this skill |
| Debug "logs not parsing" / "no alerts" / "bouncer not blocking" | this skill |
| Migrate from fail2ban | this skill |
| **Write** a parser, scenario, or WAF (AppSec) rule | the `crowdsec-local-mcp` mcp |
| Drive the **cloud Service API** (manage blocklists / allowlists / firewall integrations / metrics / decisions programmatically) | the `crowdsec-service-api` skill |


## Step 1 — Detect the environment

Run probes in this order. Stop at the first match.

```bash
# systemd / bare-metal
systemctl list-unit-files crowdsec.service >/dev/null 2>&1 && systemctl is-enabled crowdsec >/dev/null 2>&1
# docker
docker ps --format '{{.Names}} {{.Image}}' 2>/dev/null | grep -E '(^|/)(crowdsec)([: ]|$)'
# kubernetes
kubectl get pods -A 2>/dev/null | grep -i crowdsec
```

If nothing matches and the user reports CrowdSec is installed, ask where: a vendor appliance, a custom image, a binary in `/opt/`, or a remote host. Otherwise pivot to install: see [references/install/](./references/install/).

**pfSense detection:**
```sh
uname -i   # → pfSense  (pfSense CE or Plus)
```
If confirmed pfSense, go directly to [references/install/pfsense.md](./references/install/pfsense.md) — paths, service names, and activation flow are entirely different from Linux/systemd.

## Privileges — bare-metal / systemd prerequisite

On bare-metal/systemd, `cscli` and `crowdsec` need **root** (they read
`/etc/crowdsec/`, the DB under `/var/lib/crowdsec/`, and control the systemd
unit). Before running anything that touches config or state, confirm the user
is **root or has sudo**:

```bash
id -u   # 0 = root; otherwise the user needs sudo
```

If they are neither root nor a sudoer, **stop and ask them to grant it** — don't
guess. Once confirmed, run bare-metal commands as root or prefixed with `sudo`.
Docker/k8s commands run inside the container/pod and do not need this.

## Step 1.5 — Version & install-source sanity check (Linux)

Do this **first** on any install task and on any "weird behavior" report (missing
`cscli` commands/flags, hub items that won't install, behavior ≠ docs). An engine
installed from the wrong source can be **years behind** — a Linux-distro-only trap.

Compare the running engine to the latest published release:

```bash
curl -s https://version.crowdsec.net/latest    # → {"tag_name":"v1.7.8",...}; parse tag_name
cscli version                                  # bare-metal: prefix sudo
```

Then check **where the package came from**:

```bash
# Debian/Ubuntu
apt-cache policy crowdsec                       # read the *** installed line's origin
ls /etc/apt/sources.list.d/ | grep -i crowdsec
# RHEL-family
dnf info crowdsec ; dnf repolist | grep -i crowdsec
```

The official source is the packagecloud repo (`packagecloud.io/crowdsec/crowdsec`, repo id
`crowdsec_crowdsec`). A distro origin (`archive.ubuntu.com`, `deb.debian.org`,
`ports.ubuntu.com`) — or **no crowdsec repo file at all** — means it was installed from the
distro's own ancient package.

**Rule:** if the source isn't the official repo **or** the version is well behind
`tag_name`, treat it as a likely-outdated install — **stop debugging config** and migrate
onto the official repo first: [references/operate/upgrades.md](./references/operate/upgrades.md)
§ Detect & fix an outdated / distro-packaged install.

**Docker/Kubernetes:** no repo-source trap — the version is the image tag pulled from Docker
Hub. If it's far behind `version.crowdsec.net/latest`, pull a newer tag
([references/operate/upgrades.md](./references/operate/upgrades.md) happy path).

## Step 1.6 — Feature compatibility

Some features only exist past a given engine version, and a few also need a capable bouncer.
Check here before debugging "the config is right but nothing happens" — on an older engine the
answer is an upgrade, not a config change.

| Feature | Min engine | Also needs | Docs |
|---|---|---|---|
| Bot detection (AppSec challenge mode) — *alpha* | **1.8.0** | A bot-detection-capable bouncer (nginx, OpenResty, HAProxy SPOA, Traefik, Envoy) and a host that can run WASM in compiler mode | [references/appsec/bot-detection/](./references/appsec/bot-detection/) |
| Glob patterns in `appsec_configs` | **1.8.0** | — | [references/appsec/bot-detection/deploy.md](./references/appsec/bot-detection/deploy.md) § 2 |

Version-gated behaviour is recorded here rather than repeated in each reference doc — when a
feature is added, give it a row instead of sprinkling "x.y+" through the prose.

## Step 2 — Detect the intent

| Cue from user | Go to |
|---|---|
| "install", "set up", "fresh box", "how do I start" | [references/install/](./references/install/) (pick file by env) |
| "pfsense", "pfSense", "netgate" | [references/install/pfsense.md](./references/install/pfsense.md) |
| "configure logs / acquisition", "read journald / syslog / docker logs" | [references/configure/acquisition.md](./references/configure/acquisition.md) |
| "install a collection / parser / scenario", "hub", "tainted" | [references/configure/hub.md](./references/configure/hub.md) |
| "ban duration", "captcha", "decisions", "simulation", "alerts but no bans" | [references/configure/profiles.md](./references/configure/profiles.md) |
| "allowlist my office / CDN / monitoring IP", "I'm getting blocked by CAPI", "exclude IP from any ban" | [references/configure/allowlists.md](./references/configure/allowlists.md) |
| "whitelist vs allowlist vs postoverflow", "which suppression layer should I use" | [references/configure/allowlists.md](./references/configure/allowlists.md) § Suppression mechanisms |
| "test my whitelist works", "is my postoverflow / dynamic-IP whitelist actually firing" | [references/configure/allowlists.md](./references/configure/allowlists.md) § Verification — does a whitelist actually work? |
| "notifications", "alert me on slack/email/webhook", "notification not firing" | [references/configure/notifications.md](./references/configure/notifications.md) |
| "block at the firewall", "iptables", "nftables", "ipset" | [references/configure/bouncers/firewall.md](./references/configure/bouncers/firewall.md) |
| "nginx bouncer", "lua / openresty module" | [references/configure/bouncers/web-servers.md](./references/configure/bouncers/web-servers.md) § nginx |
| "haproxy bouncer", "SPOA / SPOE" | [references/configure/bouncers/web-servers.md](./references/configure/bouncers/web-servers.md) § haproxy |
| "apache bouncer", "mod_crowdsec" | [references/configure/bouncers/web-servers.md](./references/configure/bouncers/web-servers.md) § apache |
| "traefik bouncer", "traefik plugin / middleware" | [references/configure/bouncers/web-servers.md](./references/configure/bouncers/web-servers.md) § Traefik |
| "caddy bouncer", "caddy module / xcaddy" | [references/configure/bouncers/web-servers.md](./references/configure/bouncers/web-servers.md) § Caddy |
| "wrong source IP", "real client IP", "behind Cloudflare / reverse proxy / NPM", "X-Forwarded-For", "everyone shows as the proxy IP" | [references/configure/bouncers/web-servers.md](./references/configure/bouncers/web-servers.md) — per-bouncer real-IP/trusted-proxy sections |
| "AppSec", "WAF", "virtual patching", "block by request shape" | [references/appsec/](./references/appsec/) — overview, deploy, configure, troubleshoot |
| "bot detection", "challenge mode", "JS challenge", "proof of work", "block headless browsers / puppeteer / selenium / scrapers", "let Googlebot through" | [references/appsec/bot-detection/](./references/appsec/bot-detection/) — overview, deploy, configure, customize, troubleshoot |
| "Console", "enroll", "share signals" | [references/install/console.md](./references/install/console.md) |
| "upgrade", "back up", "roll back", "new version", "tainted items after upgrade" | [references/operate/upgrades.md](./references/operate/upgrades.md) |
| "old/outdated version", "`cscli` command or flag missing", "hub item won't install", "behavior doesn't match the docs", "installed from the distro package" | [references/operate/upgrades.md](./references/operate/upgrades.md) § Detect & fix an outdated / distro-packaged install (see **Step 1.5** above) |
| "multiple agents", "remote LAPI", "mTLS", "postgres backend" | [references/operate/multi-server.md](./references/operate/multi-server.md) *(partial — machine cleanup done, rest stub)* |
| "stale machines / log processors in `cscli machines list`", "prune dead agents", "ephemeral k8s pods piling up" | [references/operate/multi-server.md](./references/operate/multi-server.md) § Decommissioning stale machines |
| "is it working?", "smoke test", "validate install", "verify setup", "did detection / WAF / blocking actually wire up?" | [references/operate/health-check.md](./references/operate/health-check.md) |
| **Debug — common** · "it's broken" / "not working" / general diagnosis | [references/debug/common/triage.md](./references/debug/common/triage.md) → run `bash ${CLAUDE_SKILL_DIR}/scripts/diagnose.sh` |
| **Debug — common** · specific error string | [references/debug/common/errors.md](./references/debug/common/errors.md) |
| **Debug — common** · "container can't see logs", "mount", "SELinux/AppArmor denied", "k8s RBAC / DaemonSet" | [references/debug/common/platform-gotchas.md](./references/debug/common/platform-gotchas.md) |
| **Debug — by symptom** · "logs not parsed", "0 parsed" | [references/debug/symptoms/parsing.md](./references/debug/symptoms/parsing.md) |
| **Debug — by symptom** · "no alerts firing" | [references/debug/symptoms/no-alerts.md](./references/debug/symptoms/no-alerts.md) |
| **Debug — by symptom** · "decision exists but not blocked" | [references/debug/symptoms/not-blocked.md](./references/debug/symptoms/not-blocked.md) |
| **Debug — by symptom** · "bouncer blocks everything", "locked out of all services", "every request 403 after adding the bouncer" | [references/debug/symptoms/not-blocked.md](./references/debug/symptoms/not-blocked.md) § 7 — Inverse symptom |
| **Debug — by feature** · AppSec/WAF not blocking, false positives, captcha | [references/appsec/troubleshoot.md](./references/appsec/troubleshoot.md) |
| **Debug — by feature** · challenge never served, endless challenge loop, real crawlers being challenged, everything blocked after enabling bot detection | [references/appsec/bot-detection/troubleshoot.md](./references/appsec/bot-detection/troubleshoot.md) |
| "switch from fail2ban" | [references/migrate/from-fail2ban.md](./references/migrate/from-fail2ban.md) *(TODO — stub)* |

For anything debug-shaped, the first move is almost always:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/diagnose.sh
```

(or `--env docker --container <name>` / `--env k8s --namespace ... --pod ...`).

## Step 3 — Universal `cscli` cheat sheet

These work in every environment. On bare-metal/systemd, prefix with `sudo` (unless you are root) — see **Privileges** above. In docker/k8s prefix with `docker exec <name>` / `kubectl exec -n <ns> <pod> --` (which run as root inside the container/pod).

| Purpose | Command |
|---|---|
| Engine version | `cscli version` |
| Effective config (paths, LAPI URL, DB type) | `cscli config show` |
| One-shot triage table | `cscli metrics` |
| Recent alerts | `cscli alerts list -l 50` |
| Active bans | `cscli decisions list` |
| Delete one ban | `cscli decisions delete -i <ip>` |
| Hub state (installed + tainted/missing flags) | `cscli hub list` |
| Refresh hub index, then upgrade items | `cscli hub update && cscli hub upgrade` |
| Allowlists — list / check one IP / add | `cscli allowlists list`, `cscli allowlists check <ip>`, `cscli allowlists add <name> <ip>` |
| List bouncers and their last pull time | `cscli bouncers list` |
| List agents registered to this LAPI | `cscli machines list` |
| LAPI reachable (agent→LAPI) | `cscli lapi status` |
| CAPI/Console connectivity (enrolled, pulling/sharing) | `cscli capi status` |
| Console feature toggles (custom/manual/tainted/context/console_management) | `cscli console status` |
| Enroll this engine in the Console | `cscli console enroll <key>` then reload (see [references/install/console.md](./references/install/console.md)) |
| Replay a log file through parsers (read-only) | `cscli explain --file <path> --type <syslog\|nginx\|...>` |
| Replay a single log line | `cscli explain --log '<line>' --type <type>` |
| Validate config after editing any yaml (acquisition/profiles/config) | `crowdsec -t` (bare-metal; also auto-runs on `systemctl reload`) — then confirm the source reads with `cscli metrics show acquisition` |
| See simulation state (alerts but no decisions) | `cscli simulation status` |
| Inspect decision profiles (filters / ban duration) | `cat /etc/crowdsec/profiles.yaml` — there is **no** `cscli profiles` command (through v1.7.8); see [references/configure/profiles.md](./references/configure/profiles.md) |

Where things live on a default bare-metal install:

- Binaries: `/usr/bin/crowdsec`, `/usr/bin/cscli`
- Config root: `/etc/crowdsec/`
- Acquisition: `/etc/crowdsec/acquis.yaml` and/or `/etc/crowdsec/acquis.d/*.yaml`
- Hub items: `/etc/crowdsec/hub/`, enabled symlinks under `/etc/crowdsec/{parsers,scenarios,collections,postoverflows,contexts}/`
- Local overrides: `*/parsers/*/_custom/`, `*/scenarios/*/_custom/`, etc.
- Data (sqlite DB, geoip): `/var/lib/crowdsec/data/`
- Logs: `/var/log/crowdsec.log` (agent) and `/var/log/crowdsec_api.log` (LAPI)
- LAPI default listen: `127.0.0.1:8080`
- Systemd unit: `crowdsec.service`

## Step 4 — Hard don'ts

Confirm with the user before any of these:

- `cscli decisions delete --all` — wipes every active ban including CAPI-pulled blocklists. Use targeted `delete -i`, `delete -r`, `delete --id`, `delete --origin lists --scenario <name>`.
- Editing hub-managed files under `/etc/crowdsec/{parsers,scenarios,collections,postoverflows,contexts}/` instead of the sibling `_custom/` directory — see [references/debug/common/triage.md](./references/debug/common/triage.md) § Hard don'ts.
- Disabling a signature collection wholesale to silence a false positive — pick the right suppression layer (allowlist / whitelist parser / postoverflow) per [references/configure/allowlists.md](./references/configure/allowlists.md) § Suppression mechanisms.
- Mutating host firewall state (firewall bouncer install, `ipset` flush, iptables↔nftables switch) without confirming — the firewall bouncer can wipe rule chains other tools depend on.
- Skipping `--reset-then-reuse-values` on `helm upgrade crowdsec` — silently drops values.

## Docs

Canonical reference: <https://docs.crowdsec.net/>. Each file in `references/` cites the specific page it relies on — follow the link rather than paraphrasing from memory.
