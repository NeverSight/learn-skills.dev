---
name: cis-controls
description: CIS Controls v8.1 critical security controls for static HTML/CSS websites on GitHub Pages
license: Apache-2.0
---

# CIS Controls v8.1 Implementation Skill (Static Site)

## Purpose

Implement prioritized CIS Controls for Riksdagsmonitor's static HTML/CSS website, focusing on controls applicable to static site hosting on GitHub Pages.

## When to Use

- ✅ Security hardening activities
- ✅ Compliance assessments
- ✅ Security baseline establishment
- ✅ GitHub Pages security configuration

## Applicable CIS Controls for Static Sites

### Control 1: Inventory and Control of Enterprise Assets

**Static Site Context:**
- GitHub repository (version control)
- GitHub Pages hosting infrastructure
- DNS records (riksdagsmonitor.com)
- CDN endpoints

**Implementation:**
```yaml
# Document in ARCHITECTURE.md
Assets:
  - Repository: Hack23/riksdagsmonitor (GitHub)
  - Hosting: GitHub Pages CDN
  - Domain: riksdagsmonitor.com
  - DNS: GitHub Pages DNS
  - Languages: 14 HTML files (index.html, index_sv.html, etc.)
  - Styles: styles.css (107KB)
```

### Control 2: Inventory and Control of Software Assets

**Static Site Context:**
- HTML5, CSS3 (no backend dependencies)
- GitHub Actions workflows
- MCP servers (local Node.js packages)

**Implementation:**
```json
// package.json - Track all MCP dependencies
{
  "dependencies": {
    "riksdag-regering-mcp": "^1.0.0",
    "@modelcontextprotocol/server-filesystem": "latest",
    "@modelcontextprotocol/server-memory": "latest",
    "@playwright/mcp": "latest"
  }
}
```

### Control 3: Data Protection

**Static Site Context:**
- No server-side data storage
- No cookies or tracking
- External links to CIA platform (HTTPS)

**Implementation:**
```html
<!-- All links use HTTPS -->
<a href="https://www.hack23.com/cia/" rel="noopener noreferrer">CIA Platform</a>

<!-- No data collection -->
<!-- No cookies, no analytics, no user tracking -->

<!-- Security headers configured in GitHub Pages -->
```

### Control 4: Secure Configuration

**Static Site Context:**
- GitHub Pages configuration
- Security headers
- CSP (Content Security Policy)

**Implementation:**
```yaml
# .github/workflows/deploy.yml
name: Deploy

# Minimal permissions
permissions:
  contents: read
  pages: write
  id-token: write

# Security headers enforced via GitHub Pages
# Additional headers via _headers file (if supported)
```

**Security Headers:**
```text
# _headers (Netlify-style, adapt for GitHub Pages alternatives)
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  X-XSS-Protection: 1; mode=block
  Referrer-Policy: no-referrer
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; frame-ancestors 'none';
```

### Control 5: Account Management

**Static Site Context:**
- GitHub organization members
- Repository contributors
- No end-user accounts (static site)

**Implementation:**
```bash
# Review GitHub organization members
gh api orgs/Hack23/members --jq '.[] | {login, role}'

# Review repository collaborators
gh api repos/Hack23/riksdagsmonitor/collaborators --jq '.[] | {login, permissions}'

# Audit access logs
gh api orgs/Hack23/audit-log --jq '.[] | select(.action == "repo.access")'
```

### Control 6: Access Control Management

**Static Site Context:**
- GitHub branch protection
- Required reviews
- Signed commits

**Implementation:**
```yaml
# Branch protection rules for main branch
protections:
  - required_pull_request_reviews:
      required_approving_review_count: 1
  - required_signatures: true
  - enforce_admins: true
  - restrictions:
      users: []
      teams: ["security-team"]
```

### Control 8: Audit Log Management

**Static Site Context:**
- GitHub audit logs
- GitHub Actions logs
- Deployment logs

**Implementation:**
```bash
# Query GitHub audit logs
gh api /orgs/Hack23/audit-log \
  --jq '.[] | select(.repo == "Hack23/riksdagsmonitor") | {created_at, action, actor}'

# Review workflow runs
gh run list --repo Hack23/riksdagsmonitor --limit 100

# Download workflow logs
gh run view <run-id> --log --repo Hack23/riksdagsmonitor
```

### Control 10: Malware Defenses

**Static Site Context:**
- No server-side code execution
- GitHub's malware scanning
- Dependency scanning

**Implementation:**
```yaml
# .github/workflows/security-scanning.yml
name: Security Scanning

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4
      
      # Scan for malware in committed files
      - name: Malware Scanner
        uses: dell/common-github-actions/malware-scanner@main
      
      # CodeQL for any JavaScript
      - name: CodeQL Analysis
        uses: github/codeql-action/init@v3
        with:
          languages: javascript
      
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
```

### Control 11: Data Recovery

**Static Site Context:**
- Git version history
- GitHub repository backups
- No dynamic data to backup

**Implementation:**
```bash
# Backup repository (automated via git)
git clone --mirror https://github.com/Hack23/riksdagsmonitor.git
tar -czf riksdagsmonitor-backup-$(date +%Y%m%d).tar.gz riksdagsmonitor.git

# Restore from backup
git clone riksdagsmonitor.git riksdagsmonitor-restored
cd riksdagsmonitor-restored
git remote set-url origin https://github.com/Hack23/riksdagsmonitor.git
```

### Control 12: Network Infrastructure Management

**Static Site Context:**
- GitHub Pages CDN
- TLS 1.3 enforced
- HTTPS-only

**Implementation:**
- ✅ GitHub Pages CDN (global distribution)
- ✅ Automatic TLS 1.3 via GitHub
- ✅ HTTPS enforced (redirect HTTP → HTTPS)
- ✅ Custom domain: riksdagsmonitor.com
- ✅ DNSSEC enabled (if DNS provider supports)

### Control 13: Network Monitoring and Defense

**Static Site Context:**
- GitHub's DDoS protection
- Rate limiting via CDN
- No application-level monitoring needed

**Implementation:**
- ✅ GitHub Pages CDN with built-in DDoS protection
- ✅ Rate limiting handled by GitHub infrastructure
- ✅ Monitor via GitHub Status: https://www.githubstatus.com/

### Control 16: Application Software Security

**Static Site Context:**
- HTML5/CSS3 validation
- Link checking
- Dependency scanning

**Implementation:**
```yaml
# .github/workflows/quality-checks.yml
name: Quality Checks

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # HTML validation
      - name: Validate HTML
        run: |
          npm install -g htmlhint
          htmlhint *.html
      
      # CSS validation
      - name: Validate CSS
        run: |
          npm install -g csslint
          csslint styles.css
      
      # Link checking
      - name: Check Links
        run: |
          npm install -g linkinator
          python3 -m http.server 8080 &
          sleep 5
          linkinator http://localhost:8080/ --recurse
      
      # Dependency scanning
      - name: Dependency Check
        uses: dependency-check/Dependency-Check_Action@main
        with:
          project: 'riksdagsmonitor'
          path: '.'
          format: 'HTML'
```

### Control 17: Incident Response Management

**Static Site Context:**
- GitHub Security Advisories
- Incident response procedures
- Security contact

**Implementation:**
```markdown
# SECURITY.md
## Security Policy

### Reporting a Vulnerability

Contact: security@hack23.com

Response time: Within 48 hours

### Incident Response Process
1. Assessment (4 hours)
2. Containment (8 hours)
3. Eradication (24 hours)
4. Recovery (48 hours)
5. Post-incident review (7 days)
```

### Control 18: Penetration Testing

**Static Site Context:**
- OWASP ZAP baseline scan
- Security header testing
- SSL/TLS configuration testing

**Implementation:**
```bash
# SSL Labs scan
curl -X GET "https://api.ssllabs.com/api/v3/analyze?host=riksdagsmonitor.com"

# Security Headers scan
curl -I https://riksdagsmonitor.com | grep -E "X-Frame-Options|X-Content-Type-Options|Strict-Transport-Security"

# OWASP ZAP baseline scan
docker run -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py \
  -t https://riksdagsmonitor.com \
  -r zap-report.html
```

## Implementation Priority (Static Site Focus)

**IG1 (Implementation Group 1)** - Essential
- ✅ Control 1: Asset inventory (repository, domain)
- ✅ Control 2: Software inventory (HTML/CSS, workflows)
- ✅ Control 4: Secure configuration (GitHub Pages)
- ✅ Control 5: Account management (GitHub org)
- ✅ Control 6: Access control (branch protection)

**IG2** - Enhanced
- ✅ Control 8: Audit logging (GitHub audit logs)
- ✅ Control 11: Data recovery (Git history)
- ✅ Control 12: Network infrastructure (CDN, TLS)

**IG3** - Advanced
- ✅ Control 16: Application security (validation, scanning)
- ✅ Control 17: Incident response (procedures)
- ✅ Control 18: Penetration testing (security scans)

## ISMS Compliance

### ISO 27001:2022 Mapping
- **A.5.10**: Asset inventory and classification
- **A.8.3**: Access restrictions via GitHub permissions
- **A.8.8**: Vulnerability management via Dependabot

### NIST CSF 2.0 Mapping
- **ID.AM**: Asset management (repository inventory)
- **PR.AC**: Access control (GitHub permissions)
- **PR.DS**: Data security (HTTPS, no cookies)
- **DE.CM**: Continuous monitoring (GitHub audit logs)

## References

- **CIS Controls v8**: https://www.cisecurity.org/controls/v8
- **GitHub Pages Security**: https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https
- **ISMS**: https://github.com/Hack23/ISMS-PUBLIC
- **ARCHITECTURE.md**: System architecture and components
- **SECURITY_ARCHITECTURE.md**: Security controls documentation
