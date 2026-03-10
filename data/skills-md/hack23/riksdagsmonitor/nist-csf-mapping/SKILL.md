---
name: nist-csf-mapping
description: NIST Cybersecurity Framework 2.0 mapping for static HTML/CSS websites
license: Apache-2.0
---

# NIST CSF 2.0 Mapping (Static Site)

## Purpose

Map Riksdagsmonitor security controls to NIST Cybersecurity Framework 2.0 functions.

## Core Functions

### IDENTIFY (ID)

**ID.AM - Asset Management**
- Repository: Hack23/riksdagsmonitor
- Domain: riksdagsmonitor.com
- Hosting: GitHub Pages CDN
- Content: 14 HTML files, CSS, images

**ID.RA - Risk Assessment**
- Annual threat modeling (STRIDE)
- Dependency vulnerability scanning
- Security header audits

**ID.GV - Governance**
- ISMS policies (Hack23 ISMS-PUBLIC)
- Secure Development Policy
- Access control procedures

### PROTECT (PR)

**PR.AC - Access Control**
- GitHub MFA required
- Branch protection enabled
- Required PR reviews

**PR.DS - Data Security**
- HTTPS-only (TLS 1.3)
- No cookies/tracking
- Public data classification

**PR.IP - Protective Technology**
- Security headers (CSP, HSTS, X-Frame-Options)
- Dependabot scanning
- Secret scanning enabled

### DETECT (DE)

**DE.CM - Monitoring**
- GitHub audit logs
- Dependabot alerts
- CodeQL scanning

**DE.AE - Adverse Events**
- Security advisory monitoring
- Failed workflow notifications
- Deployment monitoring

### RESPOND (RS)

**RS.AN - Analysis**
- Incident classification (CRITICAL/HIGH/MEDIUM/LOW)
- Root cause analysis
- Security advisory review

**RS.MI - Mitigation**
- Rollback via git revert
- PR closure for vulnerabilities
- Emergency deployment procedures

### RECOVER (RC)

**RC.RP - Recovery Planning**
- Git version history (complete backup)
- Repository mirroring
- Deployment rollback

**RC.CO - Communications**
- Security contact: security@hack23.com
- Status updates via GitHub
- Post-incident reports

## Implementation Checklist

- ✅ Asset inventory (ID.AM)
- ✅ Access controls (PR.AC)
- ✅ Monitoring enabled (DE.CM)
- ✅ Incident procedures (RS)
- ✅ Recovery plan (RC)

## References

- **NIST CSF 2.0**: https://www.nist.gov/cyberframework
- **SECURITY_ARCHITECTURE.md**: Security controls
