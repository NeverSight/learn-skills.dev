---
name: netcup-vps-provider
description: |
  Netcup VPS and DNS API management. Use when:
  (1) Managing DNS records via Netcup DNS API
  (2) Configuring VPS via Server Control Panel (SCP)
  (3) Setting up firewall rules and reverse DNS (PTR)
  (4) Obtaining and managing Netcup API credentials
  (5) Troubleshooting DNS propagation issues
  (6) Managing domains registered at Netcup
  (7) Configuring external domains to use Netcup DNS
---

# Netcup VPS Provider

Netcup is a German hosting provider offering VPS and DNS services. This skill covers DNS API automation and VPS management for ARM G11 servers.

## Quick Reference

| Resource | URL/Value |
|----------|-----------|
| DNS API endpoint | `https://ccp.netcup.net/run/webservice/servers/endpoint.php?JSON` |
| Customer Control Panel | https://customercontrolpanel.de |
| Server Control Panel | https://servercontrolpanel.de |
| Nameservers | `root-dns.netcup.net`, `second-dns.netcup.net`, `third-dns.netcup.net` |

## DNS API Workflow

```
1. Login       → Get session ID
2. Query       → infoDnsZone, infoDnsRecords
3. Update      → updateDnsRecords (replaces ALL records)
4. Logout      → End session
```

### Authentication

```typescript
const response = await fetch(NETCUP_API, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    action: 'login',
    param: {
      customernumber: '12345',
      apikey: 'abc123...',
      apipassword: 'xyz789...'
    }
  })
});
// Returns: { responsedata: { apisessionid: 'session-id' } }
```

### Get Records

```typescript
{
  action: 'infoDnsRecords',
  param: {
    customernumber: '12345',
    apikey: 'abc123...',
    apisessionid: 'session-id',
    domainname: 'example.com'
  }
}
```

### Update Records

**IMPORTANT**: This replaces ALL records in the zone. Always send the complete record set.

```typescript
{
  action: 'updateDnsRecords',
  param: {
    customernumber: '12345',
    apikey: 'abc123...',
    apisessionid: 'session-id',
    domainname: 'example.com',
    dnsrecordset: {
      dnsrecords: [
        { hostname: '@', type: 'A', destination: '203.0.113.50' },
        { hostname: 'mail', type: 'A', destination: '203.0.113.50' },
        { hostname: '@', type: 'MX', priority: '10', destination: 'mail.example.com' },
        { hostname: '@', type: 'TXT', destination: 'v=spf1 mx ~all' }
      ]
    }
  }
}
```

## API Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| No per-record TTL | All records share zone TTL | Accept limitation |
| Slow propagation | ~15 min typical | Add wait/retry logic |
| Full zone updates | Must send ALL records | Cache and merge |
| Session timeout | 15 min sessions | Login per batch |

## Email DNS Records

Standard records for Mox email server:

| Type | Hostname | Value |
|------|----------|-------|
| A | mail | VPS_IP |
| A | mta-sts | VPS_IP |
| A | autoconfig | VPS_IP |
| MX | @ | mail.domain.com (priority 10) |
| TXT | @ | v=spf1 mx ~all |
| TXT | _dmarc | v=DMARC1; p=quarantine; rua=mailto:... |
| TXT | `<selector>`._domainkey | v=DKIM1; k=rsa; p=... |
| TXT | _mta-sts | v=STSv1; id=1 |
| TXT | _smtp._tls | v=TLSRPTv1; rua=mailto:... |

## External Domains

For domains registered elsewhere (Netim, Gandi, etc.):

1. **Add zone in Netcup CCP**: Products → Domain → DNS → Add DNS Zone
2. **At registrar**: Change nameservers to:
   - `root-dns.netcup.net`
   - `second-dns.netcup.net`
   - `third-dns.netcup.net`
3. **Wait**: 24-48 hours for NS propagation
4. **Manage via API**: Works like Netcup-registered domains

## VPS Management

### Reverse DNS (PTR)

Set in Server Control Panel → Network → IPv4/IPv6 address → Edit PTR

**Critical for email**: PTR must match mail server hostname (e.g., `mail.example.com`)

### Firewall (Port 25)

New VPS may have port 25 blocked:
1. SCP → Firewall
2. Remove "netcup Mail block" policy
3. Save changes

## Reference Files

| File | When to Read |
|------|--------------|
| [dns-api.md](references/dns-api.md) | API endpoints, authentication, record types |
| [vps-management.md](references/vps-management.md) | SCP operations, firewall, rDNS, SSH |
| [account-setup.md](references/account-setup.md) | Getting API credentials, adding zones |
| [troubleshooting.md](references/troubleshooting.md) | DNS propagation, API errors, email issues |

## Common Issues

| Problem | Solution |
|---------|----------|
| "Domain not found" | Add zone in CCP first (API can't create zones) |
| Slow propagation | Wait 15+ min; verify with `dig @8.8.8.8` |
| Auth failure | Regenerate API key in CCP → Stammdaten → API |
| Records disappear | API replaces ALL records; always send complete set |
| Port 25 blocked | Remove "netcup Mail block" in SCP firewall |

## Verification Commands

```bash
# Check A record
dig A mail.example.com @8.8.8.8 +short

# Check MX
dig MX example.com @8.8.8.8 +short

# Check SPF
dig TXT example.com @8.8.8.8 +short | grep spf

# Check DKIM
dig TXT selector._domainkey.example.com @8.8.8.8 +short

# Check DMARC
dig TXT _dmarc.example.com @8.8.8.8 +short

# Check PTR (reverse DNS)
dig -x YOUR_IP +short

# Check from multiple locations
# Use: https://dnschecker.org/
```

## Official Documentation

- [Netcup Help Center](https://helpcenter.netcup.com/en/)
- [DNS API Wiki](https://helpcenter.netcup.com/en/wiki/domain/our-api)
- [Firewall Documentation](https://helpcenter.netcup.com/en/wiki/server/firewall)
