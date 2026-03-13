---
name: mox-email-server
description: |
  Mox email server installation, configuration, and administration. Use when:
  (1) Setting up Mox mail server on a VPS
  (2) Configuring DNS records for email (MX, SPF, DKIM, DMARC, MTA-STS)
  (3) Integrating Mox with Caddy reverse proxy and Docker
  (4) Managing email accounts, domains, and aliases
  (5) Troubleshooting email delivery, TLS, or connectivity issues
  (6) Syncing TLS certificates from Caddy to Mox
---

# Mox Email Server

Mox is a modern, self-hosted email server written in Go. This skill covers installation, Caddy integration, and administration.

## Quick Reference

| Task | Command/Location |
|------|------------------|
| Start/stop service | `systemctl start/stop/restart mox` |
| View logs | `journalctl -u mox -f` |
| Test config | `sudo -u mox /home/mox/mox config test` |
| List accounts | `sudo -u mox /home/mox/mox config account list` |
| Add account | `sudo -u mox /home/mox/mox config account add user@domain.com` |
| Set password | `sudo -u mox /home/mox/mox setaccountpassword user@domain.com` |
| Admin UI | `https://mail.domain.com/admin/` |
| Webmail | `https://mail.domain.com/webmail/` |

## Installation Workflow

1. **DNS Setup** - Configure A, MX, SPF, DMARC records
   - See [dns-records.md](references/dns-records.md)

2. **Install Mox** - Download binary, run quickstart
   - See [administration.md](references/administration.md)

3. **Configure for Docker** - Add Docker bridge IPs, set up listeners
   - See [mox-config.md](references/mox-config.md)

4. **Caddy Integration** - Reverse proxy, certificate sync
   - See [caddy-integration.md](references/caddy-integration.md)

5. **Create Accounts** - Admin UI or CLI
   - See [administration.md](references/administration.md)

## Architecture: Caddy + Mox

```
Internet → Caddy (Docker, ports 80/443) → Mox (Host, port 8080) [Web UI]
Internet → Mox (Host, ports 25/465/587/993) [SMTP/IMAP]
```

Caddy handles:
- TLS certificates via ACME
- Reverse proxy for web interfaces (admin, webmail, autoconfig, MTA-STS)

Mox handles:
- SMTP (25), SMTPS (465), Submission (587), IMAPS (993)
- Web interfaces on port 8080

Certificate sync: Caddy obtains certs → systemd timer copies to Mox → Mox uses for SMTP/IMAP TLS.

## Critical Configuration Points

### Docker Bridge IPs in mox.conf

Mox internal listener must include Docker bridge IPs for Caddy to reach it:

```sconf
internal:
    IPs:
        - 127.0.0.1
        - ::1
        - 172.17.0.1
        - 172.18.0.1
        - 172.19.0.1
        - 172.20.0.1
        - 172.21.0.1
        - 172.22.0.1
    Hostname: localhost
```

### Caddyfile Admin Path

Admin interface requires Host header rewrite:

```caddyfile
handle /admin/* {
    reverse_proxy host.docker.internal:8080 {
        header_up Host localhost
    }
}
```

### UFW Firewall Rule

Allow Docker-to-host communication:

```bash
sudo ufw allow from 172.16.0.0/12 to any port 8080 comment 'Docker to mox'
```

## Reference Files

| File | When to Read |
|------|--------------|
| [dns-records.md](references/dns-records.md) | Setting up DNS for new domain |
| [mox-config.md](references/mox-config.md) | Editing mox.conf, understanding sconf format |
| [caddy-integration.md](references/caddy-integration.md) | Setting up reverse proxy, certificate sync |
| [administration.md](references/administration.md) | Managing accounts, domains, backups |
| [troubleshooting.md](references/troubleshooting.md) | Diagnosing issues with connectivity, TLS, delivery |

## Health Check

Run the included health check script:

```bash
sudo scripts/mox-health-check.sh [PUBLIC_IP]
```

Checks: service status, port connectivity, certificate validity, configuration, recent errors.
