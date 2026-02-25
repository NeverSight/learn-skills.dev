---
name: infrastructure-health-check
description: |
  Executes comprehensive health checks and generates status reports for network infrastructure
  services. Verifies Docker containers, validates Caddy reverse proxy, checks Pi-hole DNS,
  confirms Cloudflare Tunnel connectivity, and validates SSL certificates. Use when verifying
  infrastructure status, diagnosing connectivity issues, checking service health, or
  troubleshooting network problems. Triggers on "check health", "infrastructure status",
  "is everything running", "diagnose network", "service health", or "verify SSL".
allowed-tools:
  - Bash
  - Read
  - Grep
---

Works with docker-compose, Caddy, Pi-hole, and Cloudflare services.
# Infrastructure Health Check

Comprehensive health verification for all network infrastructure services.

## Quick Start

Run a full infrastructure health check:

```bash
cd /home/dawiddutoit/projects/network && ./scripts/health-check.sh
```

Or invoke this skill with: "Check infrastructure health" or "Is everything running?"

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Docker Container Status
   - 3.2 Caddy HTTPS Verification
   - 3.3 Pi-hole DNS Check
   - 3.4 Cloudflare Tunnel Status
   - 3.5 Webhook Endpoint Test
   - 3.6 SSL Certificate Validity
   - 3.7 Cloudflare Access Verification
   - 3.8 Generate Health Report
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Requirements](#6-requirements)
7. [Red Flags to Avoid](#7-red-flags-to-avoid)

## When to Use This Skill

**Explicit Triggers:**
- "Check infrastructure health"
- "Is everything running?"
- "Check service status"
- "Verify SSL certificates"
- "Check tunnel connection"
- "Diagnose network issues"

**Implicit Triggers:**
- After restarting Docker services
- After network configuration changes
- Before deploying new services
- When services seem unresponsive

**Debugging Triggers:**
- "Why can't I access pihole.temet.ai?"
- "Services are not responding"
- "SSL certificate errors"
- "Authentication not working"

## What This Skill Does

Performs 8 health checks and generates a comprehensive status report:

1. **Docker Containers** - Verifies all containers are running and healthy
2. **Caddy HTTPS** - Tests reverse proxy is serving HTTPS correctly
3. **Pi-hole DNS** - Confirms DNS resolution is working
4. **Cloudflare Tunnel** - Checks tunnel connectivity to Cloudflare
5. **Webhook Endpoint** - Tests GitHub webhook accessibility
6. **SSL Certificates** - Validates certificate validity and expiration
7. **Cloudflare Access** - Verifies authentication is configured
8. **Overall Status** - Aggregates results into pass/fail summary

## Instructions

### 3.1 Docker Container Status

Check all containers are running:

```bash
cd /home/dawiddutoit/projects/network && docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Health}}"
```

**Expected containers:**
| Container | Status | Purpose |
|-----------|--------|---------|
| pihole | Up (healthy) | DNS + Ad blocking |
| caddy | Up | Reverse proxy |
| cloudflared | Up | Cloudflare Tunnel |
| webhook | Up | GitHub auto-deploy |

**Check for issues:**
```bash
docker compose ps --filter "status=exited"
docker compose ps --filter "health=unhealthy"
```

### 3.2 Caddy HTTPS Verification

Test Caddy is serving HTTPS for each domain:

```bash
# Test Pi-hole
curl -sI https://pihole.temet.ai --max-time 5 | head -1

# Test Jaeger
curl -sI https://jaeger.temet.ai --max-time 5 | head -1

# Test Langfuse
curl -sI https://langfuse.temet.ai --max-time 5 | head -1
```

**Expected:** `HTTP/2 200` or `HTTP/2 302` (redirect to auth)

**Check Caddy logs for errors:**
```bash
docker logs caddy --tail 20 2>&1 | grep -iE "error|warn|fail"
```

### 3.3 Pi-hole DNS Check

Verify DNS resolution is working:

```bash
# Check Pi-hole can resolve local domains
docker exec pihole dig +short @127.0.0.1 pihole.temet.ai

# Check from host
dig @localhost pihole.temet.ai +short

# Check external DNS
dig @1.1.1.1 pihole.temet.ai +short
```

**Expected:** Returns IP address (192.168.68.135 for local, Cloudflare IP for external)

**Check Pi-hole status:**
```bash
docker exec pihole pihole status
```

### 3.4 Cloudflare Tunnel Status

Verify tunnel is connected:

```bash
# Check tunnel logs for connection status
docker logs cloudflared --tail 30 2>&1 | grep -iE "connected|registered|error|failed"

# Check tunnel process is running
docker exec cloudflared pgrep -f cloudflared
```

**Expected output contains:**
- `Registered tunnel connection` - Tunnel is connected
- `Connection ... registered` - Healthy connection

**Warning signs:**
- `connection failed` - Network issues
- `error` - Configuration problems
- No recent log entries - Process may be stuck

### 3.5 Webhook Endpoint Test

Verify webhook is accessible:

```bash
# Test webhook health endpoint locally
curl -s http://localhost:9000/hooks/health

# Test via domain (if local)
curl -sI https://webhook.temet.ai/hooks/health --max-time 5 | head -1
```

**Expected:** `OK` response or `HTTP/2 200`

### 3.6 SSL Certificate Validity

Check certificate details for each domain:

```bash
for domain in pihole jaeger langfuse ha code; do
  echo "=== $domain.temet.ai ==="
  echo | openssl s_client -servername $domain.temet.ai \
    -connect $domain.temet.ai:443 2>/dev/null | \
    openssl x509 -noout -dates -issuer 2>/dev/null || echo "FAILED"
  echo
done
```

**Expected output:**
```
notBefore=<date>
notAfter=<date>
issuer=C = US, O = Let's Encrypt, CN = R11
```

**Check certificate expiration:**
```bash
# Get days until expiration
for domain in pihole jaeger langfuse; do
  echo -n "$domain.temet.ai: "
  echo | openssl s_client -servername $domain.temet.ai \
    -connect $domain.temet.ai:443 2>/dev/null | \
    openssl x509 -noout -checkend 2592000 && echo "OK (>30 days)" || echo "RENEW SOON"
done
```

### 3.7 Cloudflare Access Verification

Check Access is configured for protected services:

```bash
# Test that Access is intercepting (should redirect to login)
curl -sI https://pihole.temet.ai --max-time 5 | grep -E "^(HTTP|location|cf-)"
```

**Expected for protected services:**
- `HTTP/2 302` with redirect to cloudflareaccess.com login
- OR `HTTP/2 200` if already authenticated

**Check Access configuration via API:**
```bash
source /home/dawiddutoit/projects/network/.env
curl -s "https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/access/apps" \
  -H "Authorization: Bearer ${CLOUDFLARE_ACCESS_API_TOKEN}" | \
  python3 -c "import sys,json; apps=json.load(sys.stdin).get('result',[]); print('\n'.join([f\"{a['name']}: {a['domain']}\" for a in apps]))"
```

### 3.8 Generate Health Report

Aggregate all checks into a summary report:

```
========================================
  Infrastructure Health Report
  Generated: $(date)
========================================

DOCKER CONTAINERS
-----------------
[PASS] pihole: running (healthy)
[PASS] caddy: running
[PASS] cloudflared: running
[PASS] webhook: running

HTTPS ENDPOINTS
---------------
[PASS] pihole.temet.ai: HTTP/2 200
[PASS] jaeger.temet.ai: HTTP/2 200
[PASS] langfuse.temet.ai: HTTP/2 200

DNS RESOLUTION
--------------
[PASS] Local DNS: 192.168.68.135
[PASS] External DNS: resolving via Cloudflare

CLOUDFLARE TUNNEL
-----------------
[PASS] Tunnel: connected

WEBHOOK
-------
[PASS] Endpoint: responding

SSL CERTIFICATES
----------------
[PASS] pihole.temet.ai: valid, expires in 67 days
[PASS] jaeger.temet.ai: valid, expires in 67 days
[PASS] langfuse.temet.ai: valid, expires in 67 days

CLOUDFLARE ACCESS
-----------------
[PASS] pihole.temet.ai: protected
[PASS] jaeger.temet.ai: protected
[PASS] langfuse.temet.ai: protected
[PASS] webhook.temet.ai: bypass (public)

========================================
  Overall Status: ALL CHECKS PASSED
========================================
```

## Supporting Files

| File | Purpose |
|------|---------|
| `scripts/health-check.sh` | Automated health check script |
| `references/troubleshooting.md` | Common issues and solutions |
| `examples/examples.md` | Example health check outputs |

## Expected Outcomes

**Success (All Checks Pass):**
- All 4 containers running
- HTTPS endpoints responding with 200/302
- DNS resolving correctly
- Tunnel connected to Cloudflare
- Webhook accessible
- Certificates valid with >30 days remaining
- Access configured for protected services

**Partial Failure:**
- One or more containers down -> Restart with `docker compose up -d`
- Certificate expiring soon -> Will auto-renew, monitor
- Access misconfigured -> Run `./scripts/cf-access-setup.sh setup`

**Critical Failure:**
- Multiple containers down -> Check Docker daemon, disk space
- Tunnel disconnected -> Check internet, tunnel token
- DNS not resolving -> Check Pi-hole container, router DNS settings
- All certificates invalid -> Check Cloudflare API token

## Requirements

**Environment:**
- Docker and Docker Compose running
- Access to `/home/dawiddutoit/projects/network`
- `.env` file with Cloudflare credentials
- Network connectivity

**Services:**
- pihole container
- caddy container
- cloudflared container
- webhook container

## Red Flags to Avoid

- [ ] Do not ignore certificate expiration warnings
- [ ] Do not skip DNS checks when troubleshooting access issues
- [ ] Do not assume tunnel is connected without checking logs
- [ ] Do not run health checks without network connectivity
- [ ] Do not ignore container health status (unhealthy state)
- [ ] Do not forget to check both local and external DNS resolution
- [ ] Do not assume HTTP 302 is a failure (it's auth redirect)

## Notes

- Health checks should be run from the Pi (192.168.68.135) for accurate local results
- Remote access testing requires being outside the home network
- Certificate auto-renewal happens 30 days before expiration
- Cloudflare Tunnel reconnects automatically after brief disconnections
- Pi-hole DNS may cache results for up to 5 minutes
- Run `./scripts/health-check.sh` for automated checking
