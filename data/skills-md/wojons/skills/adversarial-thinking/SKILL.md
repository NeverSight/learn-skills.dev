---
name: adversarial-thinking
description: Apply systematic adversarial thinking patterns including devil's advocate, assumption busting, red teaming, and white hat security approaches
license: MIT
compatibility: opencode
metadata:
  audience: developers, security professionals, decision-makers
  category: critical-thinking
---

# Adversarial Thinking

Apply systematic adversarial thinking patterns to challenge assumptions, identify weaknesses, and improve decision quality through multiple complementary adversarial perspectives.

## When to use me

Use this skill when:
- Making high-stakes decisions with significant consequences
- Designing systems that must withstand real-world challenges
- Preparing for security reviews, audits, or compliance checks
- Building resilience against failures, attacks, or market changes
- Preventing groupthink and confirmation bias in teams
- Stress-testing ideas, designs, or implementations
- Improving system security and robustness
- Developing critical thinking skills across the organization
- Preparing for competitive environments or adversarial conditions

## Adversarial Thinking Framework

Adversarial thinking applies multiple complementary perspectives to systematically challenge and improve ideas:

### 1. **Devil's Advocate** (@skills/devils-advocate)
- **Purpose**: Challenge ideas through logical counterarguments and alternative perspectives
- **Focus**: Logical reasoning, argument quality, alternative explanations
- **When to use**: Decision-making, proposal evaluation, preventing groupthink
- **Output**: Counterarguments, weaknesses, alternative approaches

### 2. **Assumption Buster** (@skills/assumption-buster)
- **Purpose**: Aggressively identify and disprove assumptions through counterexamples
- **Focus**: Finding where assumptions fail, edge cases, failure modes
- **When to use**: Critical systems, high-failure-cost scenarios, risk assessment
- **Output**: Busted assumptions, failure scenarios, risk areas

### 3. **Red Team** (@skills/redteam)
- **Purpose**: Think like an attacker to identify security vulnerabilities
- **Focus**: Security weaknesses, penetration vectors, attack paths
- **When to use**: Security assessments, penetration testing, defense preparation
- **Output**: Vulnerabilities, attack simulations, security recommendations

### 4. **White Hat** (@skills/white-hat)
- **Purpose**: Build defensive security capabilities and implement security by design
- **Focus**: Protective controls, security architecture, ethical testing
- **When to use**: Security implementation, compliance, defense building
- **Output**: Security controls, defense recommendations, security posture

### 5. **Trust But Verify** (@skills/trust-but-verify)
- **Purpose**: Independently verify claims rather than trusting assumptions
- **Focus**: Evidence validation, claim verification, reality checking
- **When to use**: Validating test results, progress claims, system capabilities
- **Output**: Verification results, discrepancies, confidence assessments

## Integrated Adversarial Thinking Workflow

### Phase 1: Challenge Foundation
1. **Devil's Advocate**: Challenge core ideas and reasoning
2. **Assumption Buster**: Identify and test foundational assumptions
3. **Trust But Verify**: Validate evidence and claims

### Phase 2: Stress Test Design
1. **Assumption Buster**: Find edge cases and failure modes
2. **Red Team**: Identify attack vectors and security weaknesses
3. **Devil's Advocate**: Challenge design decisions and alternatives

### Phase 3: Build Defenses
1. **White Hat**: Implement security controls and defenses
2. **Trust But Verify**: Validate defensive effectiveness
3. **Devil's Advocate**: Challenge defense completeness

### Phase 4: Continuous Improvement
1. **Trust But Verify**: Monitor and validate ongoing
2. **Red Team**: Regular security testing
3. **Assumption Buster**: Periodic assumption review

## When to Use Which Adversarial Perspective

### For Technical Decisions:
- **Architecture choices**: Devil's Advocate + Assumption Buster
- **Technology selection**: Devil's Advocate + Trust But Verify
- **Implementation details**: Assumption Buster + White Hat
- **Security design**: Red Team + White Hat

### For Product Decisions:
- **Feature prioritization**: Devil's Advocate + Assumption Buster
- **User experience**: Assumption Buster + Trust But Verify
- **Market strategy**: Devil's Advocate + Red Team (competitive analysis)
- **Business model**: Assumption Buster + Trust But Verify

### For Security Assessments:
- **Penetration testing**: Red Team primary, White Hat secondary
- **Security architecture**: White Hat primary, Red Team secondary
- **Incident response**: White Hat primary, Trust But Verify secondary
- **Compliance**: White Hat primary, Devil's Advocate secondary

### For Risk Management:
- **Risk identification**: Assumption Buster primary
- **Risk assessment**: Trust But Verify primary
- **Risk mitigation**: White Hat primary
- **Risk monitoring**: Trust But Verify primary

## Examples

```bash
# Full adversarial assessment of a new feature
npm run adversarial:full -- --feature "payment-processing" --phases all

# Security-focused adversarial review
npm run adversarial:security -- --component "authentication" --perspectives "redteam,white-hat"

# Decision-focused adversarial review
npm run adversarial:decision -- --decision "microservices-architecture" --perspectives "devils-advocate,assumption-buster"

# Continuous adversarial monitoring
npm run adversarial:monitor -- --system "production" --frequency daily --perspectives "trust-but-verify,redteam"
```

## Output format

```
Adversarial Thinking Assessment
──────────────────────────────
Subject: New User Authentication System
Assessment Date: 2026-02-26
Adversarial Perspectives Applied: All 5
Assessment Duration: 4 hours

Perspective Analysis:

1. Devil's Advocate Assessment:
   - Challenged: "Biometric authentication improves security"
   - Counterargument: "Biometrics can't be changed if compromised"
   - Alternative: "Hardware security keys + biometrics"
   - Weakness identified: "Fallback to password weakens security"
   - Quality score: 8.2/10 (thorough challenging)

2. Assumption Buster Assessment:
   - Assumption tested: "Users have compatible biometric hardware"
   - Busted: "30% of users lack compatible hardware"
   - Failure scenario: "Users downgrade to weak password auth"
   - Edge case: "Biometric sensors fail in cold temperatures"
   - Risk level: High (security regression likely)

3. Red Team Assessment:
   - Attack vector: "Biometric spoofing with high-res photos"
   - Vulnerability: "Liveness detection not implemented"
   - Exploit: "Replay attack on biometric data"
   - Impact: "Account takeover possible"
   - Security score: 5.8/10 (vulnerable)

4. White Hat Assessment:
   - Defense implemented: "Multi-factor authentication"
   - Security control: "Rate limiting on failed attempts"
   - Gap: "No step-up authentication for sensitive actions"
   - Recommendation: "Add hardware security key support"
   - Defense score: 7.1/10 (good but incomplete)

5. Trust But Verify Assessment:
   - Claim verified: "Biometric reduces authentication time"
   - Result: "Verified (35% faster than password)"
   - Claim verified: "Biometric reduces support tickets"
   - Result: "Partially verified (reduces password reset tickets)"
   - Confidence: Medium (limited production data)

Integrated Findings:

Critical Issues:
1. Security regression risk (biometric fallback to password)
2. Biometric spoofing vulnerability (no liveness detection)
3. Hardware compatibility exclusion (30% of users)

Strengths:
1. Multi-factor implementation solid
2. Performance improvement verified
3. User convenience likely improved

Recommendations by Priority:

HIGH PRIORITY:
1. Implement liveness detection for biometric authentication
2. Remove password fallback (use alternative methods)
3. Add hardware security key support for incompatible devices

MEDIUM PRIORITY:
4. Implement step-up authentication for sensitive actions
5. Add biometric failure rate monitoring
6. Conduct user education on biometric security

LOW PRIORITY:
7. Enhance audit logging for biometric attempts
8. Add geographic anomaly detection
9. Implement biometric template update mechanism

Adversarial Thinking Value:
- Blind spots revealed: 7 significant blind spots identified
- Risk reduction: Estimated 68% reduction in security incidents
- Decision quality: Improved from 6.5/10 to 8.8/10
- Cost savings: Estimated $420K (breach prevention + support reduction)
- Time investment vs return: 4 hours → High ROI

Next Steps:
1. Address high-priority recommendations before launch
2. Schedule follow-up adversarial assessment in 90 days
3. Establish continuous adversarial monitoring
4. Share findings with development and security teams
5. Update threat model based on adversarial findings

Adversarial Thinking Maturity:
- Current: Integrated but manual
- Target: Automated adversarial testing in CI/CD
- Gap: Missing adversarial metrics and tracking
- Roadmap: 6 months to mature adversarial program
```

## Notes

- Adversarial thinking is a system, not just occasional criticism
- Different adversarial perspectives complement each other
- Balance adversarial challenge with constructive improvement
- Document adversarial findings for organizational learning
- Use adversarial thinking to build resilience, not just find faults
- Regular adversarial practice prevents complacency
- The most valuable adversarial thinking challenges deeply held beliefs
- Measure adversarial thinking effectiveness over time
- Foster culture that welcomes adversarial perspectives
- Adversarial thinking should improve outcomes, not just criticize
- The best adversarial thinkers help build better solutions
- Integrate adversarial thinking into regular processes, not just special reviews