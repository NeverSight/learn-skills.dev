---
name: caddy-certificate-maintenance
description: |
  Manages SSL certificate operations including checking expiry, monitoring renewal,
  forcing manual renewal, and backing up certificates. Use when checking certificate
  validity, monitoring auto-renewal, certificates expiring soon, or need to backup
  certificate data. Triggers on "check certificate expiry", "certificate renewal",
  "SSL certificate status", "backup certificates", or "force certificate renewal".
  Works with Let's Encrypt certificates, Caddy auto-renewal, and caddy_data Docker
  volume.
allowed-tools:
  - Read
  - Bash
  - Grep
---

# Certificate Maintenance Skill

Operations for monitoring, maintaining, and managing SSL/TLS certificates in the Caddy reverse proxy with Let's Encrypt.

## Quick Start

Quick certificate status check:

```bash
# Check expiry for single domain
echo | openssl s_client -servername pihole.temet.ai -connect pihole.temet.ai:443 2>/dev/null | \
  openssl x509 -noout -dates -issuer

# Check all domains
for domain in pihole jaeger langfuse sprinkler ha code webhook; do
  echo "=== $domain.temet.ai ==="
  echo | openssl s_client -servername $domain.temet.ai -connect $domain.temet.ai:443 2>/dev/null | \
    openssl x509 -noout -dates
  echo
done

# Check Caddy renewal logs
docker logs caddy 2>&1 | grep -E "renewal|renew|certificate obtained"
```

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Check Certificate Expiry
   - 3.2 Monitor Auto-Renewal Status
   - 3.3 Check Certificate Details
   - 3.4 Force Manual Renewal
   - 3.5 Backup Certificates
   - 3.6 Restore Certificates
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Requirements](#6-requirements)
7. [Red Flags to Avoid](#7-red-flags-to-avoid)

## When to Use This Skill

**Explicit Triggers:**
- "Check certificate expiry"
- "Certificate renewal status"
- "SSL certificate expiring"
- "Backup certificates"
- "Force certificate renewal"

**Implicit Triggers:**
- Certificate expiring in < 30 days
- Need to verify auto-renewal working
- Planning infrastructure maintenance
- Preparing for disaster recovery

**Debugging Triggers:**
- "When does my certificate expire?"
- "Is auto-renewal working?"
- "How to backup certificates?"

## What This Skill Does

1. **Checks Expiry** - Verifies certificate validity dates for all domains
2. **Monitors Renewal** - Reviews Caddy logs for renewal activity
3. **Shows Details** - Displays certificate issuer, validity, protocols
4. **Forces Renewal** - Triggers manual certificate renewal if needed
5. **Backs Up** - Creates backup of caddy_data volume
6. **Restores** - Restores certificates from backup

## Instructions

### 3.1 Check Certificate Expiry

**Check single domain:**

```bash
echo | openssl s_client -servername pihole.temet.ai -connect pihole.temet.ai:443 2>/dev/null | \
  openssl x509 -noout -dates -issuer
```

Expected output:
```
notBefore=Jan 10 12:00:00 2026 GMT
notAfter=Apr 10 12:00:00 2026 GMT
issuer=C = US, O = Let's Encrypt, CN = R3
```

**Check all domains with expiry countdown:**

```bash
for domain in pihole jaeger langfuse sprinkler ha code webhook; do
  echo "=== $domain.temet.ai ==="

  cert_info=$(echo | openssl s_client -servername $domain.temet.ai -connect $domain.temet.ai:443 2>/dev/null | \
    openssl x509 -noout -dates -issuer 2>&1)

  if echo "$cert_info" | grep -q "notAfter"; then
    echo "$cert_info"

    # Calculate days until expiry
    expiry_date=$(echo "$cert_info" | grep notAfter | cut -d= -f2)
    expiry_epoch=$(date -j -f "%b %d %T %Y %Z" "$expiry_date" +%s 2>/dev/null || \
                   date -d "$expiry_date" +%s 2>/dev/null)
    now_epoch=$(date +%s)
    days_left=$(( ($expiry_epoch - $now_epoch) / 86400 ))

    if [ $days_left -lt 30 ]; then
      echo "⚠️  WARNING: Expires in $days_left days (renewal due)"
    else
      echo "✅ Expires in $days_left days"
    fi
  else
    echo "❌ FAILED to get certificate"
  fi

  echo
done
```

**Alert thresholds:**
- < 30 days: Renewal due (Caddy triggers at 30 days)
- < 14 days: Check renewal logs for issues
- < 7 days: Manual intervention may be needed

### 3.2 Monitor Auto-Renewal Status

**Check recent renewal activity:**

```bash
docker logs caddy 2>&1 | grep -E "renewal|renew|certificate obtained" | tail -20
```

Expected indicators:
- `certificate obtained successfully` - New certificate issued
- `certificate renewed` - Auto-renewal succeeded
- `checking certificate renewal` - Caddy checking expiry

**Check renewal schedule:**

Caddy checks renewals every 12 hours and renews 30 days before expiry.

**Verify renewal configuration:**

```bash
# Check Caddy is running
docker ps | grep caddy

# Check Cloudflare DNS plugin loaded
docker exec caddy caddy list-modules | grep cloudflare

# Verify API token set
docker exec caddy env | grep CLOUDFLARE_API_KEY
```

**If no renewal activity and expiry < 30 days:**
- Check Caddy logs for errors (use troubleshoot-https skill)
- Verify Cloudflare API token valid
- Consider manual renewal (step 3.4)

### 3.3 Check Certificate Details

**View complete certificate details:**

```bash
domain="pihole.temet.ai"

echo | openssl s_client -servername $domain -connect $domain:443 2>/dev/null | \
  openssl x509 -noout -text | grep -A5 "Subject:\|Issuer:\|Validity"
```

Shows:
- Subject (domain name)
- Issuer (Let's Encrypt)
- Validity period (not before/after dates)

**Check certificate chain:**

```bash
echo | openssl s_client -servername pihole.temet.ai -connect pihole.temet.ai:443 -showcerts 2>/dev/null
```

**Check supported protocols:**

```bash
docker logs caddy | grep -i "protocol\|http/2\|http/3"
```

Expected: HTTP/2 and HTTP/3 (QUIC) enabled

### 3.4 Force Manual Renewal

**When to force renewal:**
- Certificate expiring in < 7 days with no auto-renewal
- Testing renewal process
- After fixing Cloudflare API token

**Option A: Reload Caddy (triggers renewal check)**

```bash
docker exec caddy caddy reload --config /etc/caddy/Caddyfile
```

Caddy will check expiry and renew if < 30 days remaining.

**Option B: Restart Caddy (full renewal check)**

```bash
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml restart caddy
```

**Option C: Delete and recreate certificates (last resort)**

⚠️ **WARNING:** Only use if renewal failing and expiry imminent.

```bash
# Stop Caddy
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml down caddy

# Delete certificate volume
docker volume rm network_caddy_data

# Recreate volume
docker volume create network_caddy_data

# Start Caddy (obtains fresh certificates)
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml up -d caddy

# Monitor certificate issuance
docker logs caddy -f
```

Watch for: `certificate obtained successfully {"identifier": "domain.temet.ai"}`

**Rate limit warning:**
- Let's Encrypt limit: 50 certificates per domain per week
- Check usage: https://crt.sh/?q=temet.ai

### 3.5 Backup Certificates

**Why backup:**
- Disaster recovery
- Infrastructure migration
- Before risky changes

**Note:** Certificates can be re-obtained automatically via DNS-01 challenge. Backup not strictly necessary if you have valid Cloudflare API token.

**Backup caddy_data volume:**

```bash
# Create backup directory
mkdir -p /home/dawiddutoit/projects/network/backups

# Backup with date stamp
backup_file="/home/dawiddutoit/projects/network/backups/caddy-backup-$(date +%Y%m%d-%H%M%S).tar.gz"

tar -czf "$backup_file" \
  -C /var/lib/docker/volumes/network_caddy_data/_data .

echo "Backup created: $backup_file"

# Check backup size
ls -lh "$backup_file"
```

**Backup retention:**
- Keep last 3 backups (certificates change every 60 days)
- Delete backups older than 6 months

**Alternative: Backup entire configuration:**

```bash
backup_dir="/home/dawiddutoit/projects/network/backups/full-backup-$(date +%Y%m%d)"
mkdir -p "$backup_dir"

# Backup configuration files
cp -r /home/dawiddutoit/projects/network/docker-compose.yml "$backup_dir/"
cp -r /home/dawiddutoit/projects/network/caddy "$backup_dir/"
cp -r /home/dawiddutoit/projects/network/config "$backup_dir/"

# Backup .env (SENSITIVE - secure this file)
cp /home/dawiddutoit/projects/network/.env "$backup_dir/.env"

# Backup Docker volumes
tar -czf "$backup_dir/caddy_data.tar.gz" \
  -C /var/lib/docker/volumes/network_caddy_data/_data .

echo "Full backup created: $backup_dir"
```

### 3.6 Restore Certificates

**Restore from backup:**

```bash
backup_file="/home/dawiddutoit/projects/network/backups/caddy-backup-20260110.tar.gz"

# Stop Caddy
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml down caddy

# Delete existing volume
docker volume rm network_caddy_data

# Recreate volume
docker volume create network_caddy_data

# Restore from backup
tar -xzf "$backup_file" \
  -C /var/lib/docker/volumes/network_caddy_data/_data

# Start Caddy
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml up -d caddy

# Verify certificates loaded
docker logs caddy --tail 50
```

**Disaster recovery scenario:**

If complete infrastructure loss:

1. Restore .env file (contains API tokens)
2. Restore docker-compose.yml
3. Restore Caddyfile
4. Start Caddy (automatically obtains certificates)

No certificate backup needed if Cloudflare API token valid.

## Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | Let's Encrypt details, DNS-01 challenge, renewal schedules |
| `scripts/check-expiry.sh` | Automated certificate expiry checker |
| `examples/examples.md` | Example certificate checks, backup procedures |

## Expected Outcomes

**Success:**
- All certificates valid and not expiring soon (> 30 days)
- Recent renewal activity in logs
- Backup created successfully
- Certificates restored and working

**Warnings:**
- Certificate expiring in < 30 days (renewal due)
- No renewal activity in logs (check troubleshoot-https skill)

**Failure Indicators:**
- Certificate expired
- Renewal failing repeatedly
- No certificate obtained after manual renewal attempt

## Requirements

- Docker running with Caddy container
- Valid Cloudflare API token for DNS-01 challenge
- Network connectivity for ACME protocol
- Sufficient disk space for backups

## Red Flags to Avoid

- [ ] Do not delete caddy_data volume without backup (unless can re-obtain quickly)
- [ ] Do not exceed Let's Encrypt rate limits (50 certs/domain/week)
- [ ] Do not force renewal repeatedly (causes rate limiting)
- [ ] Do not restore old certificates if near expiry (let Caddy renew fresh)
- [ ] Do not skip checking Cloudflare API token before manual renewal
- [ ] Do not commit certificate backups to git (includes private keys)
- [ ] Do not backup .env file to insecure location (contains secrets)

## Notes

- Let's Encrypt certificates valid for 90 days
- Caddy renews automatically 30 days before expiry
- Renewal checks occur every 12 hours
- DNS-01 challenge allows internal-only services to get certificates
- Certificates stored in `/var/lib/docker/volumes/network_caddy_data/_data`
- No downtime during renewal (Caddy handles gracefully)
- OCSP stapling enabled by default (better performance)
- HTTP/2 and HTTP/3 (QUIC) supported automatically
- Certificate transparency logs: https://crt.sh/?q=temet.ai
