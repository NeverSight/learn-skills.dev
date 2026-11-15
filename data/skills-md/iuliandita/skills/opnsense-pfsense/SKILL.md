---
name: opnsense-pfsense
description: >
  OPNsense and pfSense firewalls over SSH: pf rules, NAT, VLANs, Unbound, WireGuard, CARP failover, upgrades. Not plain Linux hosts.
license: MIT
compatibility: "Requires SSH access to OPNsense or pfSense appliance"
metadata:
  source: iuliandita/skills
  date_added: "2026-03-30"
  effort: high
  argument_hint: "[platform-or-task-or-host]"
---

# OPNsense and pfSense Management

Manage, troubleshoot, and harden OPNsense and pfSense firewalls via SSH. Both are FreeBSD-based,
pf-powered firewall distributions - most concepts, commands, and patterns apply to both.

**Target versions**: see `references/versions.md` (verified per the receipt date
in that file). Do not restate version numbers here.

## When to use

- Managing or troubleshooting OPNsense and pfSense firewalls over SSH
- Reviewing pf rules, NAT, CARP, Unbound, WireGuard, CrowdSec, or pfBlockerNG on these appliances
- Configuring VLANs, CARP HA failover, or interface assignments on firewall appliances
- Debugging connectivity between networks or VLANs routed through OPNsense/pfSense
- Hardening BSD firewall appliances and validating safe remote-change workflows

## When NOT to use

- Linux networking, reverse proxies, VPN setup, or nftables work outside firewall appliances - use **networking**
- Cloud firewall rules, WAF configuration, or AWS/GCP/Azure network ACLs - use **networking** or the relevant IaC skill (**terraform**, **ansible**)
- General shell scripting or local shell behavior outside the BSD firewall context - use **shell-scripting**
- Fleet-wide configuration management via playbooks - use **ansible**
- Offensive testing, exploitation, or post-exploitation - use **privilege-escalation** (opt-in; if installed)
- Application-level security review or dependency scanning - use **security-audit**

## AI Self-Check

Before returning any firewall commands, verify:

- [ ] Platform and version confirmed (OPNsense vs pfSense, appliance and plugin versions) -
  commands differ between them
- [ ] No commands that could lock out SSH or management access; rollback path stated
- [ ] Config backup taken (or reminded) before destructive changes
- [ ] `pfctl` rules tested with `-n` (dry run) before applying
- [ ] Service names correct for the target platform (`configctl` vs `service`)
- [ ] Plugin names use correct prefix (`os-*` for OPNsense, unprefixed for pfSense)
- [ ] CARP changes target the master node, not the backup
- [ ] Shell syntax is POSIX sh (heredoc), not bash/zsh (csh/tcsh is the default shell on both)
- [ ] No firmware or plugin updates without explicit user confirmation
- [ ] Blast radius stated for any change affecting network connectivity
- [ ] DNS impact considered - changes to Unbound, DHCP, or firewall rules on port 53 can
  break name resolution for all clients on affected VLANs
- [ ] CrowdSec/pfBlockerNG checked when diagnosing blocks - bans look identical to firewall
  drops from the client side
- [ ] VLAN interface assigned before adding rules - unassigned VLANs pass no traffic through
  the firewall even if the trunk is tagged correctly
- [ ] Cross-cutting agent hygiene applied - see `references/agent-hygiene.md`

---

## Performance

- Prefer rule ordering that rejects high-volume unwanted traffic early and keeps expensive inspection scoped.
- Use aliases/tables for large address sets instead of expanding repetitive rules.
- Check state table, DNSBL, IDS/IPS, and plugin load before blaming WAN latency.

---

## Best Practices

- Make HA changes one node at a time and verify CARP state before touching the peer.
- Keep emergency console or out-of-band access available for management-plane changes.

## Workflow

For any change (skip for read-only diagnostics), copy this checklist and track progress:

```markdown
- [ ] Step 1: Platform and target device confirmed
- [ ] Step 2: Config backup taken and copied off-box
- [ ] Step 3: Change dry-run (`pfctl -n`), blast radius stated, then applied
- [ ] Step 4: Verified (on failure: revert, confirm healthy, return to Step 3)
```

### Step 1: Detect platform

If the platform is not obvious from context, **ask the user** which one they're running before
issuing commands. Identify the target device explicitly - never assume which firewall you're
talking to. Key differences at a glance:

| | OPNsense | pfSense |
|---|---|---|
| Base OS | FreeBSD (migrated from HardenedBSD in 2021) | FreeBSD |
| Config path | `/conf/config.xml` | `/cf/conf/config.xml` |
| Service control | `configctl service restart <svc>` | `pfSsh.php playback svc restart <svc>` or `service <svc> restart` |
| Plugin prefix | `os-<name>` (e.g., `os-wireguard`) | No prefix (e.g., `pfSense-pkg-WireGuard`) |
| PHP shell | N/A | `pfSsh.php` (interactive PHP shell) |
| Quick rule add | N/A | `easyrule pass wan tcp <src> <dst> <port>` |
| IP blocking | CrowdSec (`os-crowdsec`) | pfBlockerNG |
| Root shell | `csh` | `tcsh` (same heredoc workaround applies) |
| IDS/IPS config | `/var/log/suricata/*.log`, eve.json | `/var/log/suricata/suricata_<iface><uuid>/eve.json` (per interface) |
| Firmware CLI | `configctl firmware check/status` | `pfSense-upgrade` (metadata refresh: `pkg-static update`) + GUI |
| Template engine | `configd` + `configctl template` | PHP-generated configs |
| REST API | Yes, built in (`/api/`, key/secret auth) | Unofficial `pfSense-pkg-RESTAPI` package (optional third-party install) |
| Licensing | Free, open source | CE: free but slower updates; Plus: $129/yr on non-Netgate HW |
| Release cadence | Two majors a year (January/July) plus fortnightly point releases | Irregular, Netgate hardware prioritized |

**2026 status**: OPNsense is the clear choice for new deployments. pfSense CE gets slower updates and zero priority; Plus costs $129/year on non-Netgate hardware. Migration from pfSense to OPNsense has no automated path - expect ~60% clean config transfer, manual rebuild for NAT rules, VPN, and DNS forwarder settings.

**When platform is unknown**, these commands work on both:
```
pfctl -sr                # firewall rules
pfctl -ss                # state table
ifconfig                 # interfaces
pkg info                 # installed packages
netstat -rn              # routing table
sockstat -4l             # listening sockets
```

### Step 2: Back up config

Before any change that modifies rules, services, plugins, or firmware:
- Default over SSH: copy the config file to a timestamped name, then pull that copy off-box
  with `scp`. OPNsense: `` cp /conf/config.xml /root/config-`date +%Y%m%d-%H%M%S`.xml ``. pfSense:
  same with `/cf/conf/config.xml`
- Alternatives: GUI export (OPNsense System > Configuration > Backups, pfSense Diagnostics >
  Backup & Restore) or the OPNsense `/api/core/backup/download/this` endpoint. There is no
  `configctl` action that exports the config
- For major upgrades on virtualized firewalls, pair config backup with a hypervisor snapshot

Skip this step only for read-only operations (diagnostics, log review, status checks).

### Step 3: Execute the task

Apply changes using the platform-appropriate commands. Refer to the domain sections below
and the reference files for specifics. For any change that affects connectivity:
- Test `pfctl` rules with `-n` (dry run) before applying
- State the blast radius ("this will drop all VPN tunnels for ~30s")
- On HA pairs, always change on the master node and let XMLRPC sync propagate

### Step 4: Verify

After every change, confirm the firewall is healthy:
- Connectivity: can you still reach the device? Can clients reach the internet?
- Logs: check `/var/log/filter.log`, service logs, and CrowdSec/Suricata if active
- Service status: `service -e` (works on both, FreeBSD base) plus `pluginctl -s <name> status` for OPNsense plugin services. `configctl` with no arguments lists the available configd actions; there is no `configctl service list`
- State table: `pfctl -si | grep entries` - watch for unexpected drops or state exhaustion

If any check fails, revert the change (or restore the Step 2 backup), confirm the device is
healthy again, then return to Step 3 with a corrected change.

---

## Quick Task Procedures

### Creating a firewall rule (VLAN to server)

1. Identify the interface the traffic originates from (e.g., `opt1` for VLAN 50)
2. **Confirm the VLAN interface is assigned**: `ifconfig` must show the VLAN interface UP. If the VLAN is not assigned to an OPNsense/pfSense interface yet (Interfaces > Assignments), it cannot have rules - assign it first.
3. **Check existing rules**: `pfctl -sr | grep <iface>` - new interfaces have no rules (implicit deny all). Confirm the baseline before adding anything so you know exactly what you're changing.
4. Create aliases for source subnet and destination server (keeps rules readable):
   - OPNsense API (the config file holds credentials; no secret appears in argv or shell history):
     ```bash
     : "${FW_API_CURL_CONFIG:?set to a mode-0600 curl config populated from an approved secret store or no-echo prompt}"
     curl --config "$FW_API_CURL_CONFIG" -H 'Content-Type: application/json' -X POST https://<fw>/api/firewall/alias/add_item \
       -d '{"alias":{"name":"SourceVLAN","type":"network","content":"10.0.50.0/24"}}'
     curl --config "$FW_API_CURL_CONFIG" -H 'Content-Type: application/json' -X POST https://<fw>/api/firewall/alias/add_item \
       -d '{"alias":{"name":"WebServer","type":"host","content":"10.0.1.100"}}'
     ```
   - OPNsense CLI: `configctl template reload OPNsense/Filter` (after editing alias via API or XML). To verify the alias was created: `configctl template list | grep Alias`, then confirm with `pfctl -t WebServer -T show`.
   - pfSense: `easyrule` doesn't support aliases - use GUI or edit `/cf/conf/config.xml` directly
   - Verify both aliases: `pfctl -t SourceVLAN -T show && pfctl -t WebServer -T show`.
5. Add a pass rule on the **VLAN interface** (not WAN - pf evaluates rules on the interface where traffic enters): source = SourceVLAN, destination = WebServer, port = 443
6. Place the allow rule above any block-all rule for that interface (OPNsense/pfSense interface rules use `quick` by default, so the FIRST matching rule wins - put the specific allow above the broad block)
7. Test: `pfctl -n -f /tmp/rules.debug` (OPNsense) to dry-run before applying
8. Apply: `configctl filter reload` (OPNsense) or `pfSsh.php playback svc restart filter` (pfSense)
9. Verify: `pfctl -sr | grep <alias>` to confirm the rule is active

### Creating a block rule (isolate IoT VLAN)

Block IoT devices from reaching internal networks while allowing internet access:

1. Identify the IoT VLAN interface (e.g., `opt3` for VLAN 30)
2. Create an alias for RFC1918 ranges: name `RFC1918`, type `Network`, content `10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16`
3. Allow only required infrastructure exceptions first: for example, TCP/UDP 53 to the exact intended resolver, including a resolver on the firewall's private address. Account for DHCP if used.
4. Below those exceptions, **block** IoT traffic to `RFC1918`, then **pass** only the intended internet services such as TCP 443. Leave other traffic denied.
5. With `quick` rules, the FIRST match wins: narrow infrastructure exceptions, private-network block, then internet allow. RFC1918 covers only IPv4; define corresponding IPv6 isolation or disable IPv6 on this VLAN deliberately.
6. Test and apply as above: `pfctl -n -f /tmp/rules.debug`, then `configctl filter reload`

### Troubleshooting connectivity after VLAN changes

Work through these steps in order. **Do not skip ahead or assume the root cause** - each step eliminates one layer. The most common failure is a missing outbound NAT rule, not a firewall rule. Also check CrowdSec (`cscli decisions list`) and Suricata early - their blocks look identical to firewall drops from the client side.

**Prerequisite**: the VLAN must be assigned to a firewall interface before it can have rules, DHCP, or NAT. In OPNsense: Interfaces > Assignments > add the VLAN, then enable it and set its IP. In pfSense: Interfaces > Interface Assignments. An unassigned VLAN passes no traffic through the firewall even if the parent trunk is tagged correctly.

1. **Interface assigned and UP?** `ifconfig` - is the VLAN interface listed and UP? If not: assign it (see prerequisite above). If listed but DOWN: enable it in the GUI or check the parent interface.
2. **Blocklist check**: `cscli decisions list` (OPNsense CrowdSec) or check pfBlockerNG deny logs (pfSense) - CrowdSec and pfBlockerNG bans look identical to firewall drops from the client side. Clear false positives before digging into rules.
3. **Services running?** `service -e` on either platform, plus `pluginctl -s <name> status` for OPNsense plugin services - confirm DHCP, DNS (Unbound), and the packet filter are running. A stopped DHCP server on the new VLAN means clients never get an IP.
4. **Rules present?** `pfctl -sr` - any pass rules on the new VLAN interface? New interfaces have no rules by default (deny all).
5. **NAT configured?** Check outbound NAT rules include the new VLAN subnet. On OPNsense: Firewall > NAT > Outbound. Missing outbound NAT is the #1 cause of "VLAN can't reach internet."
6. **DNS working?** `drill google.com @<firewall-ip>` from a VLAN client. If this fails while public-IP connectivity works, inspect the DNS path: resolver service, TCP/UDP 53 rules and the reply path. IP reachability alone does not rule out a DNS-specific firewall block.
7. **Packet capture**: `tcpdump -ni <vlan-iface> host <client-ip>` - are packets arriving at the firewall?
   - **Reading tcpdump output**: correlate ingress requests with egress traffic, translated addresses and return packets. Requests without replies on one interface do not identify the cause: inspect rule counters/states, routes, NAT, upstream reachability and the target's return path. Use `-v` for header details; capture payloads only when needed and authorized.
8. If no packets are captured, first confirm the client generated traffic and the interface/filter are correct, then inspect VLAN tagging, trunks and switch ports. If requests leave the WAN but replies do not return, investigate the upstream/target path before changing local rules.

---

## FreeBSD Mental Model

Read `references/platform-and-operations.md` for the detailed FreeBSD shell model, key commands,
config system, REST API, IPv6 gotchas, SOPs, and recovery procedures.

- Treat both platforms as FreeBSD appliances, not Linux hosts.
- For anything beyond trivial SSH one-liners, prefer piping a POSIX `sh` heredoc instead of fighting `csh` or `tcsh`.
- Guard non-zero informational commands with `; true` when running checks in parallel.

## Operations and Common Tasks

- Check plugin or package layers early because they often explain traffic behavior that looks like a firewall-rule problem.
- Use `references/plugins.md` for plugin specifics and `references/hardening.md` for hardening and CARP guidance.

---

## Reference Files

- `references/platform-and-operations.md` - FreeBSD shell model, key commands, config system,
  REST API, IPv6 gotchas, SOPs, and recovery procedures (both platforms)
- `references/plugins.md` - operational guidance for common OPNsense plugins (CrowdSec,
  WireGuard, Suricata, HAProxy, ACME, FRR, etc.). For pfSense package equivalents, map
  concepts using the platform comparison table above.
- `references/hardening.md` - comprehensive hardening checklist. OPNsense-focused but most
  items apply to pfSense with equivalent settings in its GUI/config.

## Output Contract

See `references/output-contract.md` for the full contract.

- **Skill name:** OPNSENSE-PFSENSE
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, apply the reporting size and evidence rules in `references/output-contract.md` and write the deliverable to `docs/local/audits/opnsense-pfsense/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **networking** - for Linux reverse proxies, VPNs, DNS, nftables, and cloud network ACLs (AWS/GCP/Azure security groups, WAF rules) outside BSD firewall appliances
- **terraform** - for provisioning and managing cloud firewall rules, WAF policies, and network ACLs as infrastructure-as-code
- **ansible** - for fleet-wide firewall automation or playbook-based configuration management
- **shell-scripting** - for general shell scripting and local shell behavior; this skill covers the FreeBSD firewall context
- **security-audit** - for defensive security review of application code and supply chain, rather than firewall administration
- **privilege-escalation** (opt-in; if installed) - for authorized offensive testing and post-exploitation, not defensive firewall operations

---

## Rules

These exist because bricking a firewall remotely means driving to wherever it is.

- **Never** modify rules that could lock out SSH access. If the change touches the SSH port or the
  management interface, triple-check the rule order and confirm with the user.
- **Never** disable the LAN interface or change its IP without explicit confirmation and a rollback
  plan.
- **Never** apply firmware or plugin updates without asking first - updates can reboot the device
  and may require physical console access if something goes wrong.
- **Always** confirm destructive changes: rule deletions, service disables, plugin removals,
  state table flushes (`pfctl -Fa`).
- **OPNsense CrowdSec**: don't delete decisions or bouncers without understanding why they exist.
  A ban that looks wrong might be catching a real attack.
- **pfSense pfBlockerNG**: don't disable feed lists without understanding what they block.
  Review the deny logs before removing feeds.
- **HA/CARP (both platforms)**: never make config changes directly on the backup node - XMLRPC
  sync from master will overwrite them. Always change on master and let sync propagate.
- **pfSense `easyrule`**: convenient but creates rules without descriptions. Document what you
  added and why. Consider using the GUI or config.xml for permanent rules instead.
