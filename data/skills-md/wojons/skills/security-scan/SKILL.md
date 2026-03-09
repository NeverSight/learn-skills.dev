---
name: security-scan
description: Use when you need comprehensive security scanning across applications, infrastructure, and dependencies with LLM-based analysis
license: MIT
compatibility: opencode
metadata:
  audience: security-engineers, developers, devops
  category: security
---

# Security Scanning

Perform comprehensive security scanning across your entire stack including applications, infrastructure, containers, dependencies, and cloud environments. This skill integrates LLM-based security analysis with industry-standard tools to identify vulnerabilities, misconfigurations, and security weaknesses.

## When to use me

Use this skill when:
- You need a complete security assessment of your application and infrastructure
- You want to integrate multiple security scanning tools into a unified workflow
- You need LLM-powered analysis to identify complex security issues
- You're preparing for security audits or compliance certifications
- You want to establish baseline security scanning in CI/CD pipelines
- You need to scan across multiple environments (cloud, containers, infrastructure)

## What I do

- **LLM-based security analysis**: Use AI to identify complex security patterns, business logic flaws, and novel vulnerabilities
- **Integrated tool ecosystem**: Orchestrate OWASP ZAP, Snyk, Trivy, Nessus, and other security scanners
- **Multi-layer scanning**: Application (SAST/DAST), infrastructure (IaC scanning), containers, dependencies, cloud configurations
- **Vulnerability correlation**: Correlate findings across different scanning tools to prioritize critical issues
- **Compliance mapping**: Map vulnerabilities to compliance frameworks (SOC 2, ISO 27001, HIPAA, GDPR)
- **Remediation guidance**: Provide specific, actionable remediation steps for each finding
- **Risk scoring**: Calculate risk scores based on CVSS, exploit availability, and business impact

## Examples

```bash
# Run comprehensive security scan
./scripts/security-scan.sh --target https://app.example.com

# Scan Docker containers
./scripts/security-scan.sh --container myapp:latest

# Scan infrastructure as code
./scripts/security-scan.sh --iac terraform/

# Generate compliance report
./scripts/security-scan.sh --compliance soc2

# LLM-powered security analysis
./scripts/security-scan.sh --llm-analysis --context "Payment processing system"
```

## Output format

```
Security Scan Report
─────────────────────────────────────
Scan Date: 2025-01-15T10:30:00Z
Target: https://app.example.com
Scan Duration: 2m 45s

CRITICAL FINDINGS (3):
────────────────────────
❌ SQL Injection in /api/users endpoint
   Risk: Critical (CVSS 9.8)
   Detection: OWASP ZAP + LLM analysis
   Remediation: Use parameterized queries, implement input validation
   Compliance Impact: PCI DSS 6.5.1, OWASP A1

❌ Hard-coded AWS credentials in config file
   Risk: Critical (CVSS 8.9)
   Detection: TruffleHog + LLM pattern matching
   Remediation: Move to AWS Secrets Manager, rotate credentials
   Compliance Impact: SOC 2 CC6.1, ISO 27001 A.9.4.1

❌ Unpatched vulnerability in nginx:1.18 (CVE-2021-23017)
   Risk: Critical (CVSS 9.1)
   Detection: Trivy container scan
   Remediation: Upgrade to nginx 1.20+, apply security patches
   Compliance Impact: PCI DSS 6.2, ISO 27001 A.12.6.1

HIGH FINDINGS (8):
───────────────────
⚠️ Missing Content Security Policy header
⚠️ Excessive permissions in IAM role (AdminAccess)
⚠️ Outdated OpenSSL library (CVE-2022-2068)
⚠️ Docker container running as root
⚠️ API endpoint without rate limiting
⚠️ Sensitive data in application logs
⚠️ Missing MFA for administrative access
⚠️ Unencrypted S3 bucket

MEDIUM/LOW FINDINGS (14):
──────────────────────────
ℹ️ Security headers missing (X-Frame-Options, X-Content-Type-Options)
ℹ️ Verbose error messages revealing system information
ℹ️ Session timeout too long (24 hours)
ℹ️ Cross-site request forgery (CSRF) protection missing

LLM SECURITY ANALYSIS:
──────────────────────
🔍 Business Logic Vulnerabilities:
   • Payment amount manipulation possible in checkout flow
   • Privilege escalation via IDOR in admin panel
   • Race condition in inventory reservation system

🔍 Architectural Security Issues:
   • Monolithic architecture increases attack surface
   • Lack of network segmentation between tiers
   • Insufficient logging for security events

🔍 Compliance Gaps:
   • Missing data retention policy implementation
   • Inadequate incident response procedures
   • Insufficient employee security training documentation

SUMMARY:
────────
Total Findings: 25
Critical: 3 | High: 8 | Medium: 9 | Low: 5
Risk Score: 78/100 (High Risk)
Compliance Status: 65% compliant with SOC 2

RECOMMENDATIONS:
────────────────
1. IMMEDIATE ACTION: Fix 3 critical vulnerabilities within 24 hours
2. PRIORITY: Address 8 high-risk issues within 7 days
3. IMPROVEMENTS: Implement security controls for medium/low issues
4. ARCHITECTURAL: Consider microservices segmentation, zero-trust network
5. PROCESS: Establish security training program, incident response plan
```

## Notes

- Integrates with existing CI/CD pipelines and security tools
- LLM analysis requires careful validation to avoid false positives
- Different scanning tools may have different licensing requirements
- Some scanners require authentication tokens or API keys
- Always validate findings before taking remediation actions
- Consider running scans during off-peak hours to minimize performance impact
- Regular scanning (daily/weekly) recommended for production systems
- Keep scanning tools updated to detect latest vulnerabilities