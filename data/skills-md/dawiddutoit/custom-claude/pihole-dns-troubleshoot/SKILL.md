---
name: pihole-dns-troubleshoot
description: |
  Diagnoses and fixes DNS resolution issues in the network infrastructure including
  Pi-hole not resolving locally, router DNS configuration, and DNS record verification.
  Use when services can't be accessed via domain names, "can't access pihole.temet.ai",
  DNS not resolving, or need to verify Pi-hole DNS records. Triggers on "DNS not working",
  "can't resolve domain", "domain not found", "Pi-hole DNS issue", "fix DNS", or
  "troubleshoot DNS resolution". Works with Pi-hole DNS, docker-compose.yml FTLCONF
  variables, and local network DNS resolution.
allowed-tools:
  - Read
  - Bash
  - Grep
---

# Troubleshoot DNS Resolution Skill

Systematic diagnosis and resolution of DNS resolution issues in the Pi-hole DNS infrastructure.

## Quick Start

Run quick diagnostic to identify DNS issues:

```bash
# Check DNS resolution
dig @192.168.68.136 pihole.temet.ai

# Check Pi-hole is running
docker ps | grep pihole

# Check DNS records configured
docker exec pihole nslookup pihole.temet.ai 127.0.0.1
```

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Verify Pi-hole is Running
   - 3.2 Check Pi-hole DNS Configuration
   - 3.3 Test DNS Resolution from Pi-hole
   - 3.4 Verify Router DNS Settings
   - 3.5 Test DNS Resolution from Client
   - 3.6 Check FTLCONF DNS Records
   - 3.7 Apply Fix
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Requirements](#6-requirements)
7. [Red Flags to Avoid](#7-red-flags-to-avoid)

## When to Use This Skill

**Explicit Triggers:**
- "DNS not working"
- "Can't access pihole.temet.ai"
- "Domain not resolving"
- "Fix DNS resolution"
- "Pi-hole DNS not working"

**Implicit Triggers:**
- Services work via IP but not domain name
- Browser shows "DNS_PROBE_FINISHED_NXDOMAIN"
- Can access services remotely but not locally
- Ping fails for local domains

**Debugging Triggers:**
- "Why isn't my domain resolving?"
- "Why can't I access local services?"
- "Is Pi-hole working?"

## What This Skill Does

1. **Verifies Pi-hole** - Checks Pi-hole container is running
2. **Checks DNS Config** - Verifies FTLCONF DNS records in docker-compose.yml
3. **Tests Pi-hole DNS** - Queries Pi-hole directly for DNS records
4. **Checks Router** - Verifies router is configured to use Pi-hole
5. **Tests Client DNS** - Verifies client devices can resolve domains
6. **Identifies Issue** - Determines root cause of DNS failure
7. **Provides Fix** - Gives specific commands to resolve the issue

## Instructions

### 3.1 Verify Pi-hole is Running

```bash
docker ps | grep pihole
```

Expected: Container status "Up" (not "Restarting" or "Exited")

**If not running:**
```bash
cd /home/dawiddutoit/projects/network && \
docker compose up -d pihole && \
docker logs pihole --tail 50
```

### 3.2 Check Pi-hole DNS Configuration

Verify FTLCONF_dns_hosts environment variable is set:

```bash
docker exec pihole env | grep FTLCONF_dns_hosts
```

Expected output should include:
```
FTLCONF_dns_hosts=192.168.68.136 pihole.temet.ai
192.168.68.136 ha.temet.ai
192.168.68.136 jaeger.temet.ai
...
```

**If missing or incorrect:**
Edit docker-compose.yml to add/update FTLCONF_dns_hosts environment variable.

### 3.3 Test DNS Resolution from Pi-hole

Test that Pi-hole itself can resolve the domain:

```bash
# Test single domain
docker exec pihole nslookup pihole.temet.ai 127.0.0.1

# Test all configured domains
for domain in pihole ha jaeger langfuse sprinkler code webhook; do
  echo "=== Testing $domain.temet.ai ==="
  docker exec pihole nslookup $domain.temet.ai 127.0.0.1
  echo
done
```

Expected: Shows "Address: 192.168.68.136" for each domain

**If "NXDOMAIN" or "can't find":**
- DNS records not configured in FTLCONF_dns_hosts
- Pi-hole FTL hasn't loaded the configuration

Fix:
```bash
# Reload Pi-hole DNS
docker exec pihole pihole reloaddns

# Or restart Pi-hole
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml restart pihole
```

### 3.4 Verify Router DNS Settings

Check router is configured to use Pi-hole as DNS server:

**Router should point to:** 192.168.68.136 (Pi-hole IP)

**How to verify:**
1. Log into router admin interface
2. Check DHCP settings
3. Verify DNS server is set to 192.168.68.136

**Common router interfaces:**
- Eero: App → Settings → Network Settings → DNS
- Unifi: Network → Settings → Networks → LAN → DHCP Name Server
- Generic: Usually under LAN/DHCP settings

### 3.5 Test DNS Resolution from Client

From your computer or device:

```bash
# Check what DNS server you're using
scutil --dns | grep "nameserver\[0\]"

# Test resolution using system DNS
dig pihole.temet.ai

# Test resolution using Pi-hole directly
dig @192.168.68.136 pihole.temet.ai
```

**Expected:**
- System DNS should show 192.168.68.136
- Both dig commands should return 192.168.68.136 as answer

**If using wrong DNS server:**
- Client may have cached old DNS settings
- Router may not have updated DHCP lease
- Client may have manual DNS override

Fix:
```bash
# Flush DNS cache (macOS)
sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder

# Renew DHCP lease (macOS)
sudo ipconfig set en0 DHCP

# Linux
sudo systemd-resolve --flush-caches
```

### 3.6 Check FTLCONF DNS Records

Verify DNS records are configured in docker-compose.yml:

```bash
grep -A20 "FTLCONF_dns_hosts" /home/dawiddutoit/projects/network/docker-compose.yml
```

Expected format:
```yaml
FTLCONF_dns_hosts: |
  192.168.68.136 pihole.temet.ai
  192.168.68.136 ha.temet.ai
  192.168.68.136 jaeger.temet.ai
  192.168.68.136 langfuse.temet.ai
  192.168.68.136 sprinkler.temet.ai
  192.168.68.136 code.temet.ai
  192.168.68.136 webhook.temet.ai
```

**If missing domains:** Add them to FTLCONF_dns_hosts and restart Pi-hole.

### 3.7 Apply Fix

**Fix A: Pi-hole Not Running**

```bash
cd /home/dawiddutoit/projects/network && \
docker compose up -d pihole && \
docker logs pihole --tail 50
```

**Fix B: DNS Records Not Configured**

1. Edit docker-compose.yml:
```bash
nano /home/dawiddutoit/projects/network/docker-compose.yml
```

2. Add missing domains to FTLCONF_dns_hosts:
```yaml
FTLCONF_dns_hosts: |
  192.168.68.136 newservice.temet.ai
```

3. Restart Pi-hole:
```bash
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml up -d pihole
```

**Fix C: Client Using Wrong DNS**

1. Check router DHCP settings point to 192.168.68.136
2. Renew client DHCP lease
3. Flush client DNS cache

**Fix D: Pi-hole DNS Not Reloaded**

```bash
# Reload DNS without restart
docker exec pihole pihole reloaddns

# Or full restart
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml restart pihole
```

## Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | Complete DNS configuration reference, Pi-hole v6 FTL details |
| `examples/examples.md` | Example DNS configurations, common scenarios |

## Expected Outcomes

**Success:**
- Pi-hole container running and healthy
- DNS queries to Pi-hole return correct IP addresses
- Client devices resolve domains correctly
- All configured domains accessible via domain name

**Partial Success:**
- Pi-hole resolves correctly but clients still using old DNS
- Records configured but not yet propagated to clients

**Failure Indicators:**
- Pi-hole container not running
- FTLCONF_dns_hosts missing or incorrect
- Router not configured to use Pi-hole
- DNS resolution returns NXDOMAIN

## Requirements

- Docker running with Pi-hole container
- Pi-hole v6+ using FTL DNS server
- Network access to Pi-hole (192.168.68.136)
- Router admin access to configure DHCP/DNS

## Red Flags to Avoid

- [ ] Do not use dnsmasq configuration files (Pi-hole v6 uses FTL with FTLCONF variables)
- [ ] Do not add DNS records via Pi-hole web UI (use FTLCONF_dns_hosts instead)
- [ ] Do not forget to restart Pi-hole after changing FTLCONF_dns_hosts
- [ ] Do not configure DNS manually on clients (use router DHCP instead)
- [ ] Do not skip flushing DNS cache on clients after DNS changes
- [ ] Do not use -uall flag with Pi-hole DNS queries (causes memory issues)

## Notes

- Pi-hole v6 uses FTL DNS server, not dnsmasq directly
- FTLCONF environment variables configure FTL's pihole.toml
- DNS records added via web UI are not persistent (use FTLCONF_dns_hosts)
- Router must push Pi-hole DNS to clients via DHCP
- Client DNS cache can persist for hours (flush after changes)
- Use domains.toml + manage-domains.sh for automated DNS record management
