---
name: dnshe-freedomains
description: Use DNSHE to register, manage, and automate free subdomains (us.ci, cc.cd, de5.net, ccwu.cc) with Anycast DNS via dashboard or REST API.
triggers:
  - register a free subdomain with DNSHE
  - automate DNS record management with DNSHE API
  - renew my DNSHE domain automatically
  - set up a subdomain for my project
  - configure DNS records on DNSHE
  - use DNSHE free domain for CI/CD
  - manage DNSHE subdomains programmatically
  - get a free domain for my developer project
---

# DNSHE Free Domains & Anycast DNS

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

DNSHE ([dnshe.com](https://www.dnshe.com)) provides free subdomains under `us.ci`, `cc.cd`, `de5.net`, and `ccwu.cc` backed by enterprise Anycast DNS. It supports A, AAAA, CNAME, MX, TXT, NS, SRV, and CAA records, a 180-day renewal window, and a REST API for full automation — no credit card required.

---

## Getting Started

### 1. Register an Account
Go to [dnshe.com](https://www.dnshe.com) and sign up. No credit card needed.

### 2. Claim a Subdomain
Search for your desired prefix (e.g., `myproject`) and pair it with a suffix:

| Suffix | Use Case |
|---|---|
| `*.us.ci` | CI/CD pipelines, API endpoints, SaaS |
| `*.cc.cd` | Portfolios, creative projects |
| `*.de5.net` | Tech blogs, dev environments, docs |
| `*.ccwu.cc` | Personal pages, community projects |

### 3. Add DNS Records
From the dashboard, add your records (A, CNAME, TXT, etc.). Propagation happens in seconds via Anycast.

---

## REST API Reference

All API interactions require an API token obtained from the DNSHE dashboard under account settings.

### Authentication
All requests use a Bearer token in the `Authorization` header:
```
Authorization: Bearer $DNSHE_API_TOKEN
```

Store your token as an environment variable:
```bash
export DNSHE_API_TOKEN="your_token_here"
export DNSHE_BASE_URL="https://www.dnshe.com/api/v1"
```

---

## Key API Operations

### List Your Domains
```bash
curl -s -X GET "$DNSHE_BASE_URL/domains" \
  -H "Authorization: Bearer $DNSHE_API_TOKEN" \
  -H "Content-Type: application/json"
```

### Register a Subdomain
```bash
curl -s -X POST "$DNSHE_BASE_URL/domains" \
  -H "Authorization: Bearer $DNSHE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subdomain": "myproject",
    "suffix": "us.ci"
  }'
```

### Add a DNS Record
```bash
curl -s -X POST "$DNSHE_BASE_URL/domains/myproject.us.ci/records" \
  -H "Authorization: Bearer $DNSHE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "A",
    "name": "@",
    "value": "203.0.113.42",
    "ttl": 300
  }'
```

### Update a DNS Record
```bash
curl -s -X PUT "$DNSHE_BASE_URL/domains/myproject.us.ci/records/{record_id}" \
  -H "Authorization: Bearer $DNSHE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "A",
    "name": "@",
    "value": "203.0.113.99",
    "ttl": 300
  }'
```

### Delete a DNS Record
```bash
curl -s -X DELETE "$DNSHE_BASE_URL/domains/myproject.us.ci/records/{record_id}" \
  -H "Authorization: Bearer $DNSHE_API_TOKEN"
```

### Renew a Domain
```bash
curl -s -X POST "$DNSHE_BASE_URL/domains/myproject.us.ci/renew" \
  -H "Authorization: Bearer $DNSHE_API_TOKEN"
```

---

## Code Examples

### Python: Full Domain Setup Script
```python
import os
import requests

API_TOKEN = os.environ["DNSHE_API_TOKEN"]
BASE_URL = "https://www.dnshe.com/api/v1"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

def register_subdomain(subdomain: str, suffix: str) -> dict:
    resp = requests.post(
        f"{BASE_URL}/domains",
        headers=HEADERS,
        json={"subdomain": subdomain, "suffix": suffix},
    )
    resp.raise_for_status()
    return resp.json()

def add_record(domain: str, record_type: str, name: str, value: str, ttl: int = 300) -> dict:
    resp = requests.post(
        f"{BASE_URL}/domains/{domain}/records",
        headers=HEADERS,
        json={"type": record_type, "name": name, "value": value, "ttl": ttl},
    )
    resp.raise_for_status()
    return resp.json()

def renew_domain(domain: str) -> dict:
    resp = requests.post(
        f"{BASE_URL}/domains/{domain}/renew",
        headers=HEADERS,
    )
    resp.raise_for_status()
    return resp.json()

def list_domains() -> list:
    resp = requests.get(f"{BASE_URL}/domains", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    # Register subdomain
    result = register_subdomain("myproject", "us.ci")
    print("Registered:", result)

    # Point it to a server
    record = add_record("myproject.us.ci", "A", "@", "203.0.113.42")
    print("Record added:", record)

    # Add a www CNAME
    cname = add_record("myproject.us.ci", "CNAME", "www", "myproject.us.ci")
    print("CNAME added:", cname)
```

### Python: Automated Renewal Script (Cron-friendly)
```python
import os
import requests
from datetime import datetime, timedelta

API_TOKEN = os.environ["DNSHE_API_TOKEN"]
BASE_URL = "https://www.dnshe.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def renew_expiring_domains(days_threshold: int = 30):
    """Renew any domain expiring within `days_threshold` days."""
    resp = requests.get(f"{BASE_URL}/domains", headers=HEADERS)
    resp.raise_for_status()
    domains = resp.json()

    now = datetime.utcnow()
    threshold = now + timedelta(days=days_threshold)

    for domain in domains:
        # Adjust field name to match actual API response
        expires_at = datetime.fromisoformat(domain.get("expires_at", "").replace("Z", ""))
        if expires_at <= threshold:
            name = domain["domain"]
            renew_resp = requests.post(f"{BASE_URL}/domains/{name}/renew", headers=HEADERS)
            if renew_resp.ok:
                print(f"✅ Renewed: {name}")
            else:
                print(f"❌ Failed to renew {name}: {renew_resp.text}")

if __name__ == "__main__":
    renew_expiring_domains(days_threshold=30)
```

### JavaScript/Node.js: Domain Management Client
```javascript
const fetch = require('node-fetch'); // or use built-in fetch in Node 18+

const API_TOKEN = process.env.DNSHE_API_TOKEN;
const BASE_URL = 'https://www.dnshe.com/api/v1';

const headers = {
  'Authorization': `Bearer ${API_TOKEN}`,
  'Content-Type': 'application/json',
};

async function registerSubdomain(subdomain, suffix) {
  const res = await fetch(`${BASE_URL}/domains`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ subdomain, suffix }),
  });
  if (!res.ok) throw new Error(`Register failed: ${await res.text()}`);
  return res.json();
}

async function addRecord(domain, type, name, value, ttl = 300) {
  const res = await fetch(`${BASE_URL}/domains/${domain}/records`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ type, name, value, ttl }),
  });
  if (!res.ok) throw new Error(`Add record failed: ${await res.text()}`);
  return res.json();
}

async function listDomains() {
  const res = await fetch(`${BASE_URL}/domains`, { headers });
  if (!res.ok) throw new Error(`List failed: ${await res.text()}`);
  return res.json();
}

async function renewDomain(domain) {
  const res = await fetch(`${BASE_URL}/domains/${domain}/renew`, {
    method: 'POST',
    headers,
  });
  if (!res.ok) throw new Error(`Renew failed: ${await res.text()}`);
  return res.json();
}

// Example usage
(async () => {
  const domain = await registerSubdomain('myapp', 'cc.cd');
  console.log('Registered:', domain);

  const record = await addRecord('myapp.cc.cd', 'A', '@', '203.0.113.42');
  console.log('A record added:', record);

  // Add TXT for domain verification / Let's Encrypt
  const txt = await addRecord('myapp.cc.cd', 'TXT', '_acme-challenge', 'your-challenge-value');
  console.log('TXT record added:', txt);
})();
```

### GitHub Actions: Auto-Renewal Workflow
```yaml
# .github/workflows/dnshe-renew.yml
name: DNSHE Domain Auto-Renewal

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am UTC
  workflow_dispatch:

jobs:
  renew:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install requests

      - name: Run renewal script
        env:
          DNSHE_API_TOKEN: ${{ secrets.DNSHE_API_TOKEN }}
        run: python scripts/renew_domains.py
```

### Bash: Quick Record Update (Dynamic DNS)
```bash
#!/bin/bash
# update-dns.sh — Update A record to current public IP

DOMAIN="${DNSHE_DOMAIN:-myproject.us.ci}"
RECORD_ID="${DNSHE_RECORD_ID}"  # Get from dashboard or API list
PUBLIC_IP=$(curl -s https://api.ipify.org)

echo "Updating $DOMAIN to $PUBLIC_IP"

curl -s -X PUT "https://www.dnshe.com/api/v1/domains/${DOMAIN}/records/${RECORD_ID}" \
  -H "Authorization: Bearer $DNSHE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"type\": \"A\", \"name\": \"@\", \"value\": \"${PUBLIC_IP}\", \"ttl\": 60}"
```

---

## Common Record Patterns

### Static Website (A record)
```json
{ "type": "A", "name": "@", "value": "YOUR_SERVER_IP", "ttl": 300 }
```

### Subdomain Alias (CNAME)
```json
{ "type": "CNAME", "name": "www", "value": "myproject.us.ci", "ttl": 300 }
```

### Email (MX record)
```json
{ "type": "MX", "name": "@", "value": "mail.example.com", "ttl": 300, "priority": 10 }
```

### SSL Verification (TXT for Let's Encrypt DNS-01)
```json
{ "type": "TXT", "name": "_acme-challenge", "value": "ACME_CHALLENGE_TOKEN", "ttl": 60 }
```

### IPv6 (AAAA record)
```json
{ "type": "AAAA", "name": "@", "value": "2001:db8::1", "ttl": 300 }
```

### Service Discovery (SRV)
```json
{ "type": "SRV", "name": "_http._tcp", "value": "10 20 80 myproject.us.ci", "ttl": 300 }
```

---

## Supported Record Types

| Type | Purpose |
|---|---|
| `A` | IPv4 address |
| `AAAA` | IPv6 address |
| `CNAME` | Canonical name alias |
| `MX` | Mail exchange |
| `TXT` | Text (SPF, DKIM, ACME) |
| `NS` | Name server delegation |
| `SRV` | Service locator |
| `CAA` | Certificate authority authorization |

---

## Renewal Policy

- **Window**: 180 days before expiry — renew any time within this window.
- **Automation**: Use the `/renew` API endpoint in a weekly cron job to never miss a renewal.
- **Best practice**: Renew at 60–90 days before expiry to leave buffer time.

---

## Troubleshooting

### Domain not resolving
- Check propagation: DNS changes typically propagate in seconds globally via Anycast, but ISP caches can take up to 5 minutes.
- Verify your record was saved: call `GET /domains/{domain}/records` to confirm.
- Use `dig myproject.us.ci` or `nslookup myproject.us.ci` to test resolution.

### API returning 401
- Ensure `DNSHE_API_TOKEN` is set correctly.
- Token may be expired — regenerate in the dashboard.

### API returning 409 Conflict
- Subdomain is already taken. Try a different prefix.

### API returning 429 Too Many Requests
- You've hit rate limits. Add exponential backoff in your automation scripts.

### Record update not reflecting
- TTL caching: lower the TTL to 60 before making changes, then raise it again after.

---

## Compliance & Abuse

DNSHE has a zero-tolerance policy for illegal use:
- **Prohibited**: Phishing, fraud, malware, illegal content.
- **ToS**: [dnshe.com/tos.html](https://www.dnshe.com/tos.html)
- **Report Abuse**: [dnshe.com/domainabuse/](https://www.dnshe.com/domainabuse/)
- **Security contact**: abuse@dnshe.com

---

## Support & Links

| Resource | URL |
|---|---|
| Dashboard | [dnshe.com](https://www.dnshe.com) |
| Support Email | support@dnshe.com |
| ToS | [dnshe.com/tos.html](https://www.dnshe.com/tos.html) |
| Abuse Reports | [dnshe.com/domainabuse/](https://www.dnshe.com/domainabuse/) |
