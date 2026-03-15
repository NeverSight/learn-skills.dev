---
name: static-site-security
description: Security best practices specifically for static HTML/CSS websites on GitHub Pages
license: Apache-2.0
---

# Static Site Security Skill

## Purpose

Comprehensive security practices for static websites, leveraging their inherent security advantages while addressing remaining risks.

## Security Advantages of Static Sites

### Eliminated Attack Vectors
✅ **No SQL Injection**: No database to inject into
✅ **No Server-Side XSS**: No server-side rendering
✅ **No CSRF**: No state management or forms processing
✅ **No Session Hijacking**: No sessions to hijack
✅ **No Remote Code Execution**: No server-side code
✅ **No File Upload Vulnerabilities**: No upload functionality
✅ **No Authentication Bypass**: No authentication system

### Reduced Attack Surface
```
Traditional Web App Attack Surface:
- Web server vulnerabilities
- Application code vulnerabilities
- Database vulnerabilities
- Server OS vulnerabilities
- Third-party libraries
- Session management
- File system access
- Network services

Static Site Attack Surface:
- CDN security (GitHub Pages)
- DNS hijacking
- Content integrity
- Dependency vulnerabilities (minimal)
```

## Transport Layer Security

### HTTPS Configuration
```
✅ Required:
- HTTPS-only (TLS 1.3)
- Automatic HTTPS redirect
- Valid SSL/TLS certificate
- Perfect Forward Secrecy (PFS)

For GitHub Pages:
- Enforced HTTPS in repository settings
- Automatic Let's Encrypt certificates
- TLS 1.3 support by default
```

### Security Headers
```
Essential headers for static sites:

Content-Security-Policy:
  default-src 'self';
  script-src 'self';
  style-src 'self' 'unsafe-inline' fonts.googleapis.com;
  font-src 'self' fonts.gstatic.com;
  img-src 'self' data:;
  connect-src 'self';
  frame-ancestors 'none';

Strict-Transport-Security:
  max-age=31536000; includeSubDomains; preload

X-Content-Type-Options:
  nosniff

X-Frame-Options:
  DENY

Referrer-Policy:
  strict-origin-when-cross-origin

Permissions-Policy:
  geolocation=(), microphone=(), camera=()
```

## Content Security

### Subresource Integrity (SRI)
```html
<!-- ✅ Good: SRI for stable, versioned external resources -->
<script
  src="https://cdn.example.com/script.v1.2.3.js"
  integrity="sha384-..."
  crossorigin="anonymous"
></script>

<!-- ⚠️ Google Fonts: dynamic content, SRI not reliable unless you self-host -->
<!-- Either self-host the font CSS with SRI, or omit SRI for the dynamic URL: -->
<link
  rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Inter"
  crossorigin="anonymous"
>

<!-- ❌ Bad: No integrity check on a static, versioned asset -->
<script src="https://cdn.example.com/script.v1.2.3.js"></script>
```

### Dependency Management
```
✅ Best practices:
1. Minimize external dependencies
2. Use trusted CDNs only (Google Fonts, etc.)
3. Implement SRI for CDN resources
4. Regular dependency scanning
5. Prefer self-hosted over CDN when possible
6. Document all external dependencies
```

### HTML Injection Prevention
```html
<!-- Even static sites can have issues if using templates -->

<!-- ❌ Bad: Unsafe data in HTML -->
<div>{{ userData }}</div>

<!-- ✅ Good: Escaped/sanitized -->
<div>{{ userData | escape }}</div>

<!-- ✅ Best: Static content only -->
<div>Hardcoded safe content</div>
```

## Access Control Security

### GitHub Repository Security
```
✅ Required access controls:
- MFA enabled for all contributors
- SSH keys with passphrase
- GPG commit signing required
- Branch protection on main/master
- Required pull request reviews
- Status checks must pass
- Restrict who can push
- Restrict force pushes
```

### GitHub Pages Security
```
✅ Configuration:
- Enforce HTTPS enabled
- Source branch restricted (main only)
- Custom domain with DNSSEC (optional)
- Repository visibility: Public (for open source)
```

### Secrets Management
```
✅ Never commit:
- API keys
- Passwords
- Private keys
- OAuth tokens
- Any credentials

✅ Use instead:
- GitHub Secrets for CI/CD
- Environment variables
- Secure credential stores
- GitHub Apps (not PATs when possible)
```

## CDN and Hosting Security

### GitHub Pages Security Model
```
✅ GitHub provides:
- Global CDN with DDoS protection
- Automatic TLS certificates
- High availability (99.9% SLA)
- Infrastructure security
- Regular security updates

⚠️ User responsibilities:
- Content security
- Access control
- Dependency management
- Security monitoring
```

### DNS Security
```
✅ Best practices:
- Use DNSSEC if supported
- CAA records for certificate authority
- Monitor DNS for hijacking
- Use reputable DNS provider

Example CAA record:
example.com. CAA 0 issue "letsencrypt.org"
```

## Monitoring and Detection

### Security Monitoring
```
✅ Implement monitoring for:
- GitHub security alerts
- Dependabot vulnerability alerts
- Secret scanning alerts
- Code scanning (CodeQL) alerts
- Unusual access patterns
- Repository changes
- Workflow failures
```

### Audit Logging
```
✅ Enable and review:
- GitHub audit log (organization)
- GitHub Actions logs
- Commit history (immutable)
- Access logs (GitHub provides)
- Security event logs
```

### Alerting Strategy
```
Critical alerts (immediate response):
- Secret exposure detected
- Unauthorized access attempt
- Critical vulnerability found
- Security workflow failure

Warning alerts (24h response):
- Dependency with high severity CVE
- Failed security checks
- Unusual activity patterns

Info alerts (weekly review):
- New dependencies added
- Configuration changes
- Access changes
```

## Incident Response

### Detection
```
1. Automated alerts (Dependabot, CodeQL, secret scanning)
2. Manual monitoring (code reviews, security audits)
3. External reports (responsible disclosure)
4. GitHub security advisories
```

### Containment
```
Immediate actions:
1. Disable GitHub Pages if compromised
2. Revoke exposed credentials
3. Block malicious IP addresses (if applicable)
4. Revert to last known good state
```

### Recovery
```
Steps:
1. Identify root cause
2. Fix vulnerability
3. Test fix thoroughly
4. Deploy patched version
5. Verify security restored
6. Monitor for recurrence
```

### Post-Incident
```
Actions:
1. Document incident timeline
2. Update THREAT_MODEL.md
3. Update SECURITY_ARCHITECTURE.md
4. Improve detection capabilities
5. Share lessons learned
6. Update incident response procedures
```

## Deployment Security

### CI/CD Security
```yaml
# Security-hardened deployment workflow
name: Deploy

on:
  push:
    branches: [main]

permissions:
  contents: read  # Least privilege

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: step-security/harden-runner@SHA
        with:
          egress-policy: audit
          
      - uses: actions/checkout@SHA
      
      - name: Security Scan
        run: |
          # HTML validation
          htmlhint *.html
          
          # Link check
          linkinator . --recurse
          
          # Dependency check
          npm audit
          
      - name: Deploy
        if: success()
        run: echo "Deploy to GitHub Pages"
```

### Rollback Procedures
```
✅ Ensure capability to:
1. Revert to previous commit (git revert)
2. Redeploy last known good version
3. Disable site temporarily if needed
4. Restore from backup if necessary

RTO (Recovery Time Objective): < 15 minutes
RPO (Recovery Point Objective): Last commit
```

## Security Testing

### Pre-Deployment Tests
```
Automated tests:
- HTML validation (HTMLHint)
- Link checking (linkinator)
- Dependency scanning (Dependabot)
- Secret scanning (GitHub)
- Code scanning (CodeQL)

Manual tests:
- Security header verification
- HTTPS enforcement check
- Content review
- Access control verification
```

### Security Audit Checklist
```
Monthly audit:
- [ ] Review GitHub security alerts
- [ ] Check for exposed secrets
- [ ] Verify HTTPS enforcement
- [ ] Test security headers
- [ ] Review access controls
- [ ] Update dependencies
- [ ] Review commit history
- [ ] Test rollback procedures

Quarterly audit:
- [ ] Full threat model review
- [ ] Penetration testing (if applicable)
- [ ] Security architecture review
- [ ] Incident response drill
- [ ] Third-party security assessment
```

## Remember

- **Leverage Static Advantages**: No server-side code = no server-side vulnerabilities
- **Transport Security**: Always HTTPS with strong headers
- **Minimize Dependencies**: Each dependency is potential risk
- **Monitor Continuously**: Automated scanning catches issues early
- **Access Control**: Protect the source, protect the site
- **Plan for Incidents**: Detection, response, recovery procedures
- **Document Everything**: Security decisions and configurations

## References

- [OWASP Static Site Security](https://owasp.org/www-project-static-site-generator-security/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
