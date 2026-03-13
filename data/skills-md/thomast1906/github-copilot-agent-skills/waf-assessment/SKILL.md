---
name: waf-assessment
description: Assess Azure architectures against Well-Architected Framework (WAF) five pillars - Reliability, Security, Cost Optimization, Operational Excellence, and Performance Efficiency. Provide scores and recommendations.
---

# Well-Architected Framework Assessment Skill

Evaluate Azure architectures against Microsoft's Well-Architected Framework (WAF) five pillars to identify strengths, risks, and improvement opportunities.

## When to Use

- Assess existing or proposed Azure architectures
- Validate designs meet WAF best practices
- Identify architectural risks and gaps
- Provide scored assessment with recommendations
- Review before production deployment

## Five Pillars Overview

### 1. Reliability
Ability of the system to recover from failures and continue functioning.
- **Focus**: Availability, resiliency, disaster recovery, health monitoring

### 2. Security
Protecting applications and data from threats.
- **Focus**: Identity, network security, encryption, secrets management

### 3. Cost Optimization
Managing costs to maximize value delivered.
- **Focus**: Right-sizing, reserved instances, monitoring, waste elimination

### 4. Operational Excellence
Operations processes that keep a system running in production.
- **Focus**: IaC, CI/CD, monitoring, incident response, automation

### 5. Performance Efficiency
Ability of a system to adapt to changes in load.
- **Focus**: Scaling, caching, CDN, resource selection, optimization

## Assessment Process

### Step 1: Analyze Architecture

Review the architecture for each pillar:

**Reliability Checklist:**
- [ ] Availability Zones configured?
- [ ] Multi-region deployment for critical workloads?
- [ ] Health checks and monitoring configured?
- [ ] Auto-healing and circuit breakers implemented?
- [ ] Backup strategy defined with RPO/RTO?
- [ ] Disaster recovery plan documented?

**Security Checklist:**
- [ ] Managed identities used (no credentials in code)?
- [ ] Private endpoints for PaaS services?
- [ ] HTTPS only with TLS 1.2+?
- [ ] Network security groups with least privilege?
- [ ] Key Vault for secrets management?
- [ ] Azure AD authentication and RBAC configured?
- [ ] Data encrypted at rest and in transit?

**Cost Optimization Checklist:**
- [ ] Resources right-sized for actual usage?
- [ ] Auto-scaling configured?
- [ ] Reserved instances considered for predictable workloads?
- [ ] Storage tiering implemented (Hot/Cool/Archive)?
- [ ] Unused resources identified?
- [ ] Cost monitoring and alerts configured?

**Operational Excellence Checklist:**
- [ ] Infrastructure as Code (Bicep/Terraform)?
- [ ] CI/CD pipelines implemented?
- [ ] Application Insights for telemetry?
- [ ] Centralized logging (Log Analytics)?
- [ ] Alerts configured for critical scenarios?
- [ ] Deployment automation and rollback?

**Performance Efficiency Checklist:**
- [ ] CDN for static content?
- [ ] Caching strategy (Redis, CDN)?
- [ ] Asynchronous processing for long operations?
- [ ] Appropriate compute SKUs selected?
- [ ] Auto-scaling rules defined?
- [ ] Performance testing completed?

### Step 2: Score Each Pillar

Use 0-100 scoring system:

**Scoring Criteria:**
- **80-100 (Excellent):** Meets all best practices, production-ready
- **60-79 (Good):** Meets most practices, minor gaps
- **40-59 (Fair):** Some practices missing, moderate risk
- **20-39 (Poor):** Many gaps, significant improvements needed
- **0-19 (Critical):** Major gaps, not production-ready

### Step 3: Provide Recommendations

For each identified gap:
- **Finding**: What's missing or problematic
- **Risk**: Impact if not addressed
- **Recommendation**: Specific action to take
- **Priority**: Critical / High / Medium / Low
- **Effort**: Hours or days to implement

## Assessment Output Format

```markdown
# Well-Architected Framework Assessment
**Architecture**: [Name]
**Assessment Date**: [Date]
**Overall Score**: [Average of 5 pillars]/100

## Executive Summary
[2-3 sentences on overall health, key strengths, top risks]

## Pillar Scores

| Pillar | Score | Status |
|--------|-------|--------|
| Reliability | 75/100 | 🟢 Good |
| Security | 65/100 | 🟡 Fair |
| Cost Optimization | 80/100 | 🟢 Good |
| Operational Excellence | 70/100 | 🟡 Fair |
| Performance Efficiency | 85/100 | 🟢 Excellent |
| **Overall** | **75/100** | **🟢 Good** |

---

## 1. Reliability (75/100) - 🟢 Good

### Strengths
Availability Zones configured for App Service and Azure SQL
Health checks implemented with automatic failover
Backup strategy defined (RPO: 1 hour, RTO: 4 hours)

### Gaps & Recommendations

#### Finding #1: No Multi-Region Deployment
**Risk**: Regional outage causes complete service unavailability
**Recommendation**: Implement active-passive multi-region with Azure Front Door
**Priority**: High
**Effort**: 3-5 days
**Implementation**: Deploy secondary region (West US), configure Azure Front Door with priority routing

#### Finding #2: Missing Circuit Breaker Pattern
**Risk**: Cascading failures when dependencies are degraded
**Recommendation**: Implement circuit breaker using Polly library
**Priority**: Medium
**Effort**: 1-2 days

---

## 2. Security (65/100) - 🟡 Fair

### Strengths
Azure AD authentication configured
HTTPS enforced with TLS 1.2
Key Vault used for connection strings

### Gaps & Recommendations

#### Finding #1: Service Principal Used Instead of Managed Identity
**Risk**: Credential rotation required, potential secret exposure
**Recommendation**: Replace service principal with system-assigned managed identity
**Priority**: Critical
**Effort**: 4 hours
**Implementation**: 
1. Enable managed identity on App Service
2. Grant RBAC permissions to SQL and Key Vault
3. Remove service principal credentials

#### Finding #2: No Private Endpoints
**Risk**: PaaS services exposed to public internet
**Recommendation**: Implement private endpoints for SQL, Storage, Key Vault
**Priority**: High
**Effort**: 1 day

---

## 3-5. [Remaining Pillars Follow Same Structure]

---

## Priority Roadmap

### Critical (Fix Immediately)
1. Replace service principal with managed identity
2. Implement private endpoints for PaaS services

### High (Next 30 Days)
3. Multi-region deployment (active-passive)
4. Infrastructure as Code implementation
5. Implement comprehensive alerting

### Medium (Next 90 Days)
6. Circuit breaker pattern
7. Reserved instances for predictable workloads
8. Performance testing automation

### Low (Future Enhancements)
9. Chaos engineering tests
10. Additional caching layers

---

## Cost Impact Summary
- **Savings Opportunities**: ~$480/month (right-sizing, reserved instances)
- **Security Enhancements**: +$200/month (private endpoints)
- **Multi-Region**: +$850/month (passive region infrastructure)
- **Net Impact**: +$570/month for significantly improved resilience and security

---

## Conclusion
[Summary of assessment with key takeaways and prioritized next steps]
```

## Tips for Effective Assessments

**Be Specific:** Reference exact resources and configurations
**Quantify Risk:** Use concrete examples of potential impact
**Actionable Recommendations:** Provide implementation steps, not just principles
**Prioritize Ruthlessly:** Help teams focus on what matters most
**Show Business Impact:** Connect technical gaps to business risks
**Include Quick Wins:** Balance strategic improvements with fast fixes
**Cost-Aware:** Show ROI for recommendations (cost vs benefit)

**Avoid:** Generic advice, overwhelming lists, missing priorities, theoretical recommendations
