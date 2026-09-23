---
name: crowdsec
description: >-
  Deploy, configure, and operate CrowdSec Security Engine, cscli, remediation
  components, acquisition pipelines, and AppSec WAF. Use for Linux or Docker
  installation, detection-to-blocking design, incident review, and safe changes.
  Do not use for generic firewall, Kubernetes, or reverse-proxy design; route
  those to the named platform skill and use this skill for CrowdSec integration.
license: MIT
compatibility: Requires CrowdSec/cscli for live operations; Docker is optional for container deployment.
metadata:
  source: https://docs.crowdsec.net
  version: 0.0.3
---

# CrowdSec

CrowdSec detects hostile behavior from logs and HTTP requests, then exposes
alerts and decisions through LAPI. The engine alone does not block traffic:
install and verify at least one remediation component (bouncer) before claiming
protection.

## Safety Gate

Before any mutation, confirm the target host/container, scope, backup or rollback,
and maintenance window. Prefer read-only inspection and simulation first. Never
manually delete decisions, collections, or data without recording the reason and
an undo path. Save bouncer keys when created; they are shown once. Use
`simulation: true` while tuning scenarios so detections are observed without
enforcement, then verify allowlists before live blocking.

## Choose a Deployment

For Debian/Ubuntu, add the CrowdSec repository, install `crowdsec`, then install
a remediation package such as `crowdsec-firewall-bouncer-iptables` or
`-nftables`. For Docker Compose, expose LAPI (`127.0.0.1:8080`), metrics
(`127.0.0.1:6060`), and AppSec (`127.0.0.1:7422`) only to required networks,
mount `/etc/crowdsec`, `/var/lib/crowdsec/data`, and logs read-only, and pin a
reviewed image version. Persist the data directory, mandatory for v1.7.0+.
Load [the Docker deployment guide](references/docker-deployment.md) for a full
compose example and remote-agent caveats.

After installation, verify `systemctl status crowdsec` (or container health),
then `cscli version`, `cscli collections list`, acquisition metrics, and
bouncer connectivity. Do not expose LAPI or AppSec publicly without an explicit
network and authentication design.

## The Detection-to-Blocking Workflow

1. Select collections for the actual log format, for example
   `crowdsecurity/linux`, `sshd`, `nginx`, `traefik`, or `base-http-scenarios`.
2. Configure acquisition in `/etc/crowdsec/acquis.yaml` or `acquis.d/`; every
   source needs `labels.type` so the correct parser runs. Use
   `poll_without_inotify: true` for unreliable NFS/SMB or bind mounts and
   `use_time_machine: true` for buffered logs.
3. Check parser/scenario hits and unparsed lines with `cscli metrics -o json`.
4. Use profiles to map alerts to decisions. Keep `profiles.yaml.local` and
   remember YAML sequences replace rather than merge.
5. Add a bouncer with `cscli bouncers add NAME`, store its one-time key securely,
   and verify `cscli bouncers list` plus a harmless test decision.
6. Confirm the reverse proxy/firewall is actually enforcing decisions; an alert
   or LAPI decision alone is not proof of a blocked request.

For complete configuration directives, database choices, and hardening, read
[config-reference](references/config-reference.md),
[database-config](references/database-config.md), and
[production-hardening](references/production-hardening.md).

## cscli Essentials

Use `cscli -o json` for automation and capture command output, version, host,
and time as evidence. Read-only triage commonly uses:

```bash
cscli version
cscli hub list
cscli collections list
cscli alerts list --contain "scenario:ssh-bf"
cscli decisions list -o json
cscli metrics -o json
cscli explain --file /path/to/sample.log
```

`cscli hub update` refreshes the local hub index and can change local state. It
is optional, not part of the read-only triage path, and requires the safety gate
above before running it. Manage hub items with
`collections|parsers|scenarios install/list/upgrade/inspect`; those install,
upgrade, and delete operations also require the safety gate. Manage alerts and
decisions with `alerts list/inspect` and `decisions add/list/delete`; mutation
commands require the safety gate above.
Manage bouncers and machines with `bouncers add/list/delete` and
`machines add/list/delete`. Use `console status`, `console enroll`, and
`lapi register` only after confirming the destination and credentials. Load the
[full cscli reference](references/cscli-command-reference.md) for flags,
output modes, and less common commands.

## Acquisition and AppSec WAF

A minimal file acquisition entry is:

```yaml
filenames: [/var/log/nginx/*.log]
labels: {type: nginx}
```

For AppSec, install the relevant virtual-patching/CRS collections and add an
`appsec` acquisition source listening on `7422` with
`appsec_config: crowdsecurity/appsec-default` and `labels.type: appsec`. Route
requests from the proxy to AppSec and decide failure behavior deliberately:
fail-open preserves availability but can bypass protection; fail-closed protects
more strongly but can cause an outage. Test with benign fixtures and inspect
AppSec metrics before enabling blocking. In-band rules block or captcha the
current request; out-of-band rules emit events for later scenarios. Load
[the AppSec deep dive](references/appsec-deep-dive.md) and the relevant
[bouncer guide](references/traefik-bouncer.md) or
[nginx-bouncer](references/nginx-bouncer.md).

## Operations and Troubleshooting

Check service logs, `cscli metrics`, parser/unparsed counts, scenario hits,
active decisions, and bouncer last-pull time in that order. Distinguish “no
logs acquired”, “logs acquired but unparsed”, “parsed but no scenario hit”,
“decision exists but bouncer is stale”, and “bouncer enforced but proxy routing
is wrong”. Do not interpret an empty alert query as proof of safety. Use
[the troubleshooting guide](references/troubleshooting.md) and the
[operations checklist](references/operations-checklist.md) for a bounded
verification packet.

Use profiles and notifications deliberately. Test notification plugins with
`cscli notifications test NAME`; never place webhook secrets or CTI keys in
examples. Enable TLS/mTLS for LAPI across trust boundaries and review
community/blocklist pulls before relying on them.

## References

- [Docker deployment](references/docker-deployment.md)
- [Configuration](references/config-reference.md)
- [cscli commands](references/cscli-command-reference.md)
- [AppSec WAF](references/appsec-deep-dive.md)
- [Operations checklist](references/operations-checklist.md)
- [Troubleshooting](references/troubleshooting.md)
- [Production hardening](references/production-hardening.md)
- [Database configuration](references/database-config.md)
- [Hub collections](references/hub-collections.md)
- [Traefik bouncer](references/traefik-bouncer.md)
- [Nginx bouncer](references/nginx-bouncer.md)
