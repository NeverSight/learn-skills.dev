---
name: quien-whois-lookup
description: Use quien for interactive TUI and CLI/JSON domain, IP, DNS, mail, SSL/TLS, and tech stack lookups
triggers:
  - "look up a domain with quien"
  - "whois lookup for a domain"
  - "check DNS records for a domain"
  - "inspect mail configuration SPF DMARC DKIM"
  - "get IP address info with quien"
  - "check tech stack of a website"
  - "run quien for TLS or HTTP headers"
  - "use quien instead of whois"
---

# quien — Better WHOIS Lookup Tool

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`quien` is a Go-based CLI/TUI tool that replaces `whois` with tabbed interactive views and JSON-scriptable subcommands for domain WHOIS/RDAP, DNS records, mail configuration (SPF, DMARC, DKIM, BIMI), SSL/TLS, HTTP headers, tech stack detection, and IP/ASN/BGP lookups.

---

## Installation

**Homebrew (macOS/Linux)**
```sh
brew tap retlehs/tap
brew install retlehs/tap/quien
```

**Ubuntu / Debian**
```sh
curl -fsSL https://apt.quien.dev/install.sh | sudo sh
```

**Go**
```sh
go install github.com/retlehs/quien@latest
```

**Verify installation**
```sh
quien --version
```

**Optional — replace system whois:**
```sh
# Add to ~/.bashrc or ~/.zshrc
alias whois=quien
```

---

## Core CLI Commands

### Interactive TUI (default)
```sh
# Launch interactive prompt
quien

# Open TUI directly for a domain
quien example.com

# Open TUI for an IP address
quien 8.8.8.8
```

### JSON output (scriptable)
```sh
# Full JSON output for all tabs
quien --json example.com

# Individual subcommands (always output JSON)
quien dns example.com
quien mail example.com
quien tls example.com
quien http example.com
quien stack example.com
quien all example.com        # all data in one JSON object
```

---

## TUI Tab Overview

| Tab | Data shown |
|---|---|
| **WHOIS** | RDAP-first registration data, registrar, dates, nameservers |
| **DNS** | A, AAAA, MX, TXT, NS, CNAME, SOA records |
| **Mail** | MX, SPF, DMARC, DKIM, BIMI + VMC chain validation |
| **TLS** | Certificate chain, validity, SANs, cipher info |
| **HTTP** | Response headers, redirects, status codes |
| **Stack** | WordPress plugins, JS/CSS frameworks, external services |
| **IP** | Reverse DNS, network info, abuse contacts, ASN via RDAP/BGP |

---

## JSON Subcommand Examples

### DNS records
```sh
quien dns github.com
# Output:
# {
#   "domain": "github.com",
#   "a": ["140.82.121.4"],
#   "aaaa": [],
#   "mx": [{"host": "aspmx.l.google.com", "priority": 1}],
#   "ns": ["dns1.p08.nsone.net", "dns2.p08.nsone.net"],
#   "txt": ["v=spf1 ip4:... ~all"],
#   ...
# }
```

### Mail configuration audit
```sh
quien mail example.com
# Returns SPF record, DMARC policy, DKIM selectors found,
# BIMI record, VMC certificate chain validation
```

### TLS/SSL inspection
```sh
quien tls example.com
# Returns certificate subject, issuer, validity dates,
# SANs, chain depth, protocol version, cipher suite
```

### HTTP headers
```sh
quien http example.com
# Returns status code, redirect chain, all response headers
# (Content-Security-Policy, HSTS, X-Frame-Options, etc.)
```

### Tech stack detection
```sh
quien stack example.com
# Parses HTML for:
# - WordPress version + active plugins
# - JavaScript frameworks (React, Vue, Angular, Next.js, etc.)
# - CSS frameworks (Tailwind, Bootstrap, etc.)
# - External services (analytics, CDNs, payment providers)
```

### IP address lookup
```sh
quien 8.8.8.8
quien --json 8.8.8.8

# Returns:
# - Reverse DNS (PTR record)
# - RDAP network block info
# - Abuse contact
# - Origin ASN + prefix (RDAP with BGP fallback)
# - PeeringDB enrichment: org, peering policy, IX/facility counts,
#   traffic profile, peering locations
```

### All data at once
```sh
quien all example.com | jq '.dns.a'
quien all example.com | jq '.mail.spf'
quien all example.com | jq '.tls.valid_until'
```

---

## Scripting Patterns

### Pipe JSON into jq
```sh
# Get all A records
quien dns example.com | jq '.a[]'

# Check if DMARC policy is reject
quien mail example.com | jq '.dmarc.policy == "reject"'

# Get certificate expiry
quien tls example.com | jq '.certificates[0].not_after'

# List detected JS frameworks
quien stack example.com | jq '.javascript_frameworks[]'

# Get ASN number for an IP
quien --json 1.1.1.1 | jq '.asn.number'
```

### Shell script: bulk domain audit
```sh
#!/bin/bash
domains=("example.com" "github.com" "golang.org")

for domain in "${domains[@]}"; do
  echo "=== $domain ==="
  
  spf=$(quien mail "$domain" | jq -r '.spf.record // "MISSING"')
  dmarc=$(quien mail "$domain" | jq -r '.dmarc.policy // "MISSING"')
  tls_expiry=$(quien tls "$domain" | jq -r '.certificates[0].not_after // "N/A"')
  
  echo "SPF:   $spf"
  echo "DMARC: $dmarc"
  echo "TLS expires: $tls_expiry"
  echo
done
```

### Shell script: check domain expiry
```sh
#!/bin/bash
DOMAIN="${1:?Usage: $0 <domain>}"

expiry=$(quien --json "$DOMAIN" | jq -r '.whois.expires // .rdap.expires // empty')

if [ -z "$expiry" ]; then
  echo "Could not determine expiry for $DOMAIN"
  exit 1
fi

echo "$DOMAIN expires: $expiry"
```

### Go integration — run quien as subprocess
```go
package main

import (
    "encoding/json"
    "fmt"
    "os/exec"
)

type DNSResult struct {
    Domain string   `json:"domain"`
    A      []string `json:"a"`
    MX     []struct {
        Host     string `json:"host"`
        Priority int    `json:"priority"`
    } `json:"mx"`
    TXT []string `json:"txt"`
}

func lookupDNS(domain string) (*DNSResult, error) {
    out, err := exec.Command("quien", "dns", domain).Output()
    if err != nil {
        return nil, fmt.Errorf("quien dns failed: %w", err)
    }
    var result DNSResult
    if err := json.Unmarshal(out, &result); err != nil {
        return nil, fmt.Errorf("parse error: %w", err)
    }
    return &result, nil
}

func main() {
    dns, err := lookupDNS("example.com")
    if err != nil {
        panic(err)
    }
    fmt.Printf("A records for %s: %v\n", dns.Domain, dns.A)
    for _, mx := range dns.MX {
        fmt.Printf("MX %d: %s\n", mx.Priority, mx.Host)
    }
}
```

### Go integration — full audit struct
```go
package main

import (
    "encoding/json"
    "os/exec"
)

type FullAudit struct {
    WHOIS struct {
        Registrar string `json:"registrar"`
        Created   string `json:"created"`
        Expires   string `json:"expires"`
        Updated   string `json:"updated"`
    } `json:"whois"`
    DNS struct {
        A   []string `json:"a"`
        NS  []string `json:"ns"`
        TXT []string `json:"txt"`
    } `json:"dns"`
    Mail struct {
        SPF struct {
            Record string `json:"record"`
            Valid  bool   `json:"valid"`
        } `json:"spf"`
        DMARC struct {
            Record string `json:"record"`
            Policy string `json:"policy"`
        } `json:"dmarc"`
    } `json:"mail"`
    TLS struct {
        Certificates []struct {
            Subject  string `json:"subject"`
            NotAfter string `json:"not_after"`
        } `json:"certificates"`
    } `json:"tls"`
    Stack struct {
        JavascriptFrameworks []string `json:"javascript_frameworks"`
        CSSFrameworks        []string `json:"css_frameworks"`
        ExternalServices     []string `json:"external_services"`
    } `json:"stack"`
}

func auditDomain(domain string) (*FullAudit, error) {
    out, err := exec.Command("quien", "all", domain).Output()
    if err != nil {
        return nil, err
    }
    var audit FullAudit
    return &audit, json.Unmarshal(out, &audit)
}
```

---

## Agent Skill Integration

Install quien as an agent skill so AI coding agents automatically use it for domain/IP lookups:

```sh
npx skills add retlehs/quien
```

---

## Key Behaviors to Know

- **RDAP-first**: Uses RDAP protocol before falling back to raw WHOIS. Broader TLD coverage via IANA referral.
- **Automatic retry**: All network lookups use exponential backoff — transient failures are retried automatically.
- **BGP fallback**: If RDAP does not return ASN data for an IP, quien queries BGP routing tables for origin ASN/prefix.
- **PeeringDB enrichment**: ASN lookups are enriched with PeeringDB data (peering policy, IX presence, traffic profile).
- **VMC validation**: BIMI lookups validate the full VMC certificate chain, not just the record presence.
- **Tech stack from HTML**: Stack detection fetches and parses the actual HTML of the target, not just HTTP headers.

---

## Troubleshooting

**`quien: command not found`**
```sh
# If installed via go install, ensure GOPATH/bin is in PATH
export PATH="$PATH:$(go env GOPATH)/bin"
```

**TUI doesn't render correctly**
```sh
# Ensure your terminal supports true color and UTF-8
echo $TERM          # should be xterm-256color or similar
echo $LANG          # should include UTF-8
```

**Rate limiting / lookup failures**
- RDAP and WHOIS servers may rate-limit. quien retries with backoff automatically.
- For bulk scripting, add `sleep 1` between calls to avoid hitting rate limits.

**No DKIM results**
- DKIM requires knowing the selector. quien probes common selectors (google, default, mail, etc.) but custom selectors won't be discovered automatically.

**IP lookup shows no ASN**
- Some IP blocks are not in RDAP. quien falls back to BGP; if both fail, the block may be unrouted or private.

**JSON output is empty / malformed**
```sh
# Confirm the subcommand syntax — subcommands always output JSON
quien dns example.com        # correct
quien --json dns example.com # incorrect - --json is for top-level only
```
