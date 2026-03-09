---
name: redteam
description: Think and act like an attacker to identify security vulnerabilities, weaknesses, and penetration vectors through adversarial security testing
license: MIT
compatibility: opencode
metadata:
  audience: security professionals, developers, operations teams
  category: security
---

# Red Team

Adopt attacker mindset to identify security vulnerabilities, penetration vectors, and systemic weaknesses through adversarial thinking, simulated attacks, and offensive security testing.

## When to use me

Use this skill when:
- Conducting security assessments or penetration tests
- Designing security-sensitive systems or features
- Preparing for security audits or compliance reviews
- Responding to security incidents or breaches
- Training defensive teams (blue team) through exercises
- Evaluating security controls and detection capabilities
- Testing incident response procedures
- Validating security architecture decisions
- Assessing third-party systems or integrations
- Building security awareness and attacker empathy

## What I do

### 1. Attacker Mindset Adoption
- **Think like different attacker types**:
  - Script kiddies (automated tools, low sophistication)
  - Organized crime (financial motivation, moderate sophistication)
  - Nation states (unlimited resources, high sophistication)
  - Insider threats (knowledge, access, motivation)
  - Hacktivists (ideological motivation, publicity seeking)
  
- **Adopt attack methodologies**:
  - Reconnaissance (information gathering, footprinting)
  - Scanning (vulnerability discovery, enumeration)
  - Exploitation (vulnerability weaponization)
  - Privilege escalation (expanding access)
  - Persistence (maintaining access)
  - Exfiltration (data theft, extraction)

### 2. Vulnerability Discovery
- **Identify attack surfaces** and entry points
- **Map trust boundaries** and privilege transitions
- **Discover security misconfigurations**
- **Find logic flaws** and business logic vulnerabilities
- **Identify weak authentication and authorization**
- **Spot insecure data handling** and storage
- **Find missing security controls**

### 3. Exploitation Simulation
- **Chain vulnerabilities** for maximum impact
- **Bypass security controls** through creative methods
- **Exploit trust relationships** between components
- **Use social engineering** techniques (where appropriate)
- **Test physical security** (for comprehensive assessments)
- **Simulate advanced persistent threats** (APT tactics)

### 4. Impact Assessment
- **Evaluate exploit consequences** (data loss, system compromise)
- **Assess business impact** (financial, reputational, operational)
- **Measure detection capabilities** (how long would attack go unnoticed?)
- **Test response effectiveness** (incident response, recovery)
- **Quantify risk levels** based on likelihood and impact

## Red Team Techniques

### Reconnaissance & Information Gathering:
- **Open source intelligence (OSINT)** collection
- **Network scanning** and service enumeration
- **Application fingerprinting** and technology detection
- **Social media profiling** (for social engineering)
- **DNS reconnaissance** and subdomain discovery

### Vulnerability Identification:
- **Automated scanning** with tools (Nessus, OpenVAS, etc.)
- **Manual testing** for logic flaws and business logic vulnerabilities
- **Code review** for security weaknesses
- **Configuration review** for security misconfigurations
- **Architecture analysis** for design flaws

### Exploitation Methods:
- **Web application attacks** (SQLi, XSS, CSRF, SSRF, etc.)
- **Network attacks** (man-in-the-middle, replay, spoofing)
- **Authentication bypass** (password cracking, session hijacking)
- **Privilege escalation** (horizontal and vertical)
- **Persistence mechanisms** (backdoors, scheduled tasks, etc.)

### Social Engineering:
- **Phishing simulation** (email, phone, in-person)
- **Pretext development** (convincing stories and personas)
- **Baiting** (malicious USB drops, etc.)
- **Quid pro quo** (something for something)
- **Tailgating** (physical access following)

## Examples

```bash
# Conduct reconnaissance on target system
npm run redteam:recon -- --target example.com --scope external

# Perform vulnerability assessment
npm run redteam:vulnerability-scan -- --target 192.168.1.0/24 --intensity aggressive

# Simulate web application attacks
npm run redteam:web-attack -- --url https://app.example.com --techniques "sql-injection,xss,csrf"

# Test social engineering resilience
npm run redteam:phishing-test -- --targets employees.csv --template "password-reset"

# Full red team engagement
npm run redteam:full-engagement -- --target organization --duration 2weeks --rules-of-engagement approved
```

## Output format

```
Red Team Engagement Report
──────────────────────────────
Target: E-commerce Platform (shop.example.com)
Engagement Duration: 72 hours
Rules of Engagement: Approved scope, no production impact
Red Team Lead: Synthetic Attacker #7

Executive Summary:
- Critical Vulnerabilities: 3
- High Severity Vulnerabilities: 7
- Medium Severity Vulnerabilities: 12
- Detection Rate: 42% (58% went undetected)
- Mean Time to Detection: 8.5 hours
- Business Impact Score: 8.2/10 (Severe)

Critical Findings:

1. Vulnerability: SQL Injection in Product Search
   CVE Equivalent: CWE-89
   Severity: Critical
   
   Attack Path:
   - Reconnaissance identified search functionality
   - Fuzzing revealed parameter vulnerable to SQL injection
   - Exploitation allowed database schema extraction
   - Privilege escalation to database administrator
   - Data exfiltration possible: 2.3M customer records
   
   Proof of Concept:
   ```
   GET /search?q=' UNION SELECT username,password FROM users--
   Response: admin | 5f4dcc3b5aa765d61d8327deb882cf99
   ```
   
   Impact:
   - Complete database compromise
   - Customer PII exposure (names, emails, addresses)
   - Payment information potentially accessible
   - Regulatory violations (GDPR, CCPA, PCI-DSS)
   
   Business Consequences:
   - Estimated fine: $4.2M (GDPR violation)
   - Customer notification costs: $850K
   - Reputational damage: 35% customer churn likely
   - Legal liability: Class action lawsuits probable
   
   Recommendation:
   - Immediate: WAF rule blocking injection patterns
   - Short-term: Parameterized queries implementation
   - Long-term: Secure coding training, code review process

2. Vulnerability: Authentication Bypass via JWT Tampering
   CVE Equivalent: CWE-287
   Severity: High
   
   Attack Path:
   - Captured JWT token from legitimate user
   - Analyzed token structure (header.payload.signature)
   - Modified "role" claim from "user" to "admin"
   - None signature verification detected
   - Full administrative access achieved
   
   Technical Details:
   - JWT uses "none" algorithm vulnerability
   - No signature validation on server side
   - Role-based access control depends solely on token claims
   
   Impact:
   - Complete administrative control
   - Order manipulation, pricing changes, user data access
   - Financial fraud capability
   - Platform compromise
   
   Detection Metrics:
   - Attack duration before detection: 14 hours
   - Detection method: Manual log review (not automated)
   - Alert quality: Low (generic "unusual activity")
   
   Recommendation:
   - Immediate: Reject "none" algorithm JWTs
   - Short-term: Implement proper JWT validation
   - Long-term: Add anomaly detection for admin actions

3. Vulnerability: Server-Side Request Forgery (SSRF)
   CVE Equivalent: CWE-918
   Severity: High
   
   Attack Path:
   - Image upload functionality accepts URLs
   - SSRF to internal metadata service (169.254.169.254)
   - AWS credentials retrieval
   - Cloud environment compromise
   
   Impact:
   - Complete AWS account compromise
   - Data exfiltration from S3 buckets
   - Resource hijacking (crypto mining, botnet)
   - Infrastructure destruction capability
   
   Business Consequences:
   - Cloud resource costs: $50K+/month potential
   - Data breach: All cloud-stored data
   - Service disruption: Complete outage possible
   - Recovery time: Weeks to rebuild infrastructure
   
   Recommendation:
   - Immediate: Block metadata service access
   - Short-term: Implement URL validation and allowlisting
   - Long-term: Network segmentation, outbound proxy

Detection & Response Assessment:
- Security Monitoring Coverage: 65%
- Alert Quality Score: 4.2/10 (High false positives, low true positives)
- Mean Time to Respond: 3.5 hours (excluding undetected incidents)
- Incident Response Effectiveness: 6.1/10
- Forensic Capability: Basic (log review only)

Attack Simulation Metrics:
- Initial Compromise Time: 2.3 hours
- Privilege Escalation Time: 1.1 hours
- Lateral Movement Effectiveness: 8.7/10
- Persistence Established: 5 locations
- Data Exfiltration Simulation: 2.1GB in 4.5 hours

Red Team Observations:
1. Defense-in-depth lacking (single points of failure)
2. Detection focused on perimeter, blind to internal movement
3. Incident response reactive, not proactive
4. Security controls inconsistent across services
5. Developers lack security training (vulnerability density high)

Strategic Recommendations:
1. IMMEDIATE (Next 24 hours):
   - Apply WAF rules for SQL injection protection
   - Disable "none" algorithm for JWT
   - Block metadata service access from applications

2. SHORT-TERM (Next 2 weeks):
   - Implement parameterized queries globally
   - Add JWT signature validation
   - Deploy SSRF protection middleware
   - Enhance monitoring for authentication anomalies

3. MEDIUM-TERM (Next 2 months):
   - Conduct secure coding training for developers
   - Implement automated security testing in CI/CD
   - Enhance incident response playbooks
   - Deploy endpoint detection and response (EDR)

4. LONG-TERM (Next 6 months):
   - Establish security champion program
   - Implement threat modeling process
   - Deploy deception technology (honeypots, canaries)
   - Conduct regular red team exercises (quarterly)

Lessons Learned:
- The most critical vulnerabilities were in business logic, not typical OWASP Top 10
- Detection failed for sophisticated attacks (58% undetected)
- Response was slow even for detected incidents
- Security debt accumulated from rapid feature development
- Attacker mindset revealed blind spots in defensive thinking

Engagement Value:
- Prevented potential breach: High confidence (>90%)
- Cost savings: Estimated $8.4M (fines + breach costs)
- Risk reduction: Significant (addressed critical vulnerabilities)
- Organizational learning: High (attacker perspective gained)
- Security maturity improvement: Foundation for growth
```

## Notes

- Red teaming requires proper authorization and rules of engagement
- Focus on improving security, not blaming individuals or teams
- Balance thorough testing with business operational needs
- Document findings clearly with actionable recommendations
- Share lessons learned across the organization
- Use red team findings to improve blue team capabilities
- Regular red teaming prevents security stagnation
- The best red teams think creatively, not just run tools
- Measure improvement over time, not just vulnerability counts
- Red teaming builds security culture through shared understanding