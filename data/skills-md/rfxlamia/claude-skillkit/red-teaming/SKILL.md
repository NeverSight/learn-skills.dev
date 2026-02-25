---
name: red-teaming
description: Comprehensive red teaming methodology for both cybersecurity and AI/LLM systems. Use when conducting adversary emulation, vulnerability assessment, attack simulation, or security validation. Trigger on requests for penetration testing, threat modeling, security audits, MITRE ATT&CK operations, LLM safety testing, prompt injection attacks, or compliance validation (OWASP, NIST, TIBER, DORA, EU AI Act). Apply when users ask to "test like an attacker", "red team our system", "validate security posture", "assess LLM vulnerabilities", or "simulate cyber attacks". Includes planning frameworks, execution strategies, reporting templates, and progressive references to specialized attack techniques and tools.
---

# Red Teaming

## Overview

Red teaming is a structured adversarial approach to testing organizational security posture by simulating real-world attacks. This skill provides comprehensive methodology for both **traditional cybersecurity red teaming** (network, physical, social engineering) and **AI/LLM red teaming** (prompt injection, jailbreaking, safety testing).

**Core Philosophy:** Think like an attacker, operate covertly, test holistically, document thoroughly.

## When to Use This Skill

Use this skill when users need:

### Cybersecurity Red Teaming
- **Adversary emulation** using MITRE ATT&CK framework
- **Network penetration testing** beyond traditional pen tests
- **Purple team exercises** (red-blue collaboration)
- **Security posture validation** before major deployments
- **Compliance testing** for TIBER, DORA, ISO 27001
- **Physical security assessment** and social engineering
- **Incident response readiness** testing

### AI/LLM Red Teaming
- **LLM safety validation** before production deployment
- **Prompt injection vulnerability** assessment
- **Jailbreaking resistance** testing
- **Data leakage detection** (PII, training data)
- **Bias and toxicity evaluation**
- **Multi-turn attack simulation**
- **Compliance validation** for OWASP Top 10 LLM, NIST AI RMF, EU AI Act

### Key Indicators to Use This Skill
- "Test our security like a real attacker"
- "MITRE ATT&CK" or "adversary emulation"
- "LLM red teaming" or "prompt injection testing"
- "Purple team exercise"
- "Security audit" (holistic vs. point-in-time)
- "Jailbreak our AI model"

## Red Teaming Fundamentals

### Red Team vs. Other Security Approaches

| Aspect | Red Teaming | Penetration Testing | Vulnerability Assessment |
|--------|-------------|---------------------|-------------------------|
| **Scope** | Holistic, goal-oriented | Technical, scope-limited | Automated scanning |
| **Approach** | Covert, realistic attack | Overt testing | Compliance-driven |
| **Duration** | Weeks-months | Days-weeks | Hours-days |
| **Objective** | Compromise organization | Find vulnerabilities | Identify weaknesses |
| **Detection** | Avoid detection | Detection acceptable | N/A |
| **Focus** | People + Process + Technology | Technology only | Technology only |

### Core Principles

1. **Realistic Threat Modeling**
   - Base scenarios on actual threat actors relevant to industry
   - Use Tactics, Techniques, Procedures (TTPs) over specific tools
   - Emulate adversary behavior patterns, not just exploit signatures

2. **Adversarial Mindset**
   - Think like an attacker: creative, patient, opportunistic
   - Exploit human factors, not just technical vulnerabilities
   - Chain multiple small weaknesses into critical impact

3. **Stealth Operations**
   - Avoid detection by security tools and personnel
   - Use living-off-the-land techniques
   - Gradual escalation to avoid triggering alarms

4. **Comprehensive Testing**
   - Test all attack surfaces: physical, digital, human
   - Multi-vector approach (not single exploit chains)
   - Test detection AND response capabilities

5. **Evidence-Based Reporting**
   - Document every step with screenshots, logs, timestamps
   - Provide proof of exploitation, not just theoretical risks
   - Actionable remediation recommendations

6. **Ethical Boundaries**
   - Operate within rules of engagement
   - Obtain proper authorization
   - Avoid collateral damage to business operations

## Universal Red Teaming Methodology

All red team engagements follow this core process, adapted for cybersecurity or AI domains:

### Phase 1: Planning

**Objective:** Define scope, objectives, rules of engagement

**Key Activities:**
- **Scope Definition**
  - Target systems, networks, applications
  - In-scope vs. out-of-scope boundaries
  - Time constraints and testing windows
  
- **Objectives & Goals**
  - What are we trying to compromise? (data, access, control)
  - Success criteria (e.g., "exfiltrate customer database", "bypass AI safety filters")
  - Realistic vs. theoretical scenarios
  
- **Threat Modeling**
  - Identify relevant threat actors (APT groups, insider threats, etc.)
  - Map threat landscape to organizational risk profile
  - Select TTPs to emulate (MITRE ATT&CK for cyber, OWASP for AI)
  
- **Rules of Engagement**
  - Authorization documentation
  - Restricted actions (e.g., no DoS, no data destruction)
  - Escalation procedures
  - Communication protocols
  - Legal and compliance requirements
  
- **Team Assembly**
  - Red team members and specializations
  - Blue team awareness (known vs. unknown exercise)
  - White cell coordination (exercise management)

**Deliverable:** Red team operation plan with objectives, scope, rules, timeline

### Phase 2: Reconnaissance & Intelligence Gathering

**Objective:** Collect information about target without detection

**Key Activities:**
- **Open-Source Intelligence (OSINT)**
  - Public records, social media, company websites
  - Technology stack identification
  - Employee information and organizational structure
  - For AI: Model documentation, API specifications, training data sources
  
- **Technical Reconnaissance**
  - Network mapping and asset discovery
  - Subdomain enumeration and infrastructure fingerprinting
  - For AI: Endpoint testing, model architecture inference
  
- **Social Intelligence**
  - Employee behavior patterns
  - Communication channels and workflows
  - Physical security observations

**Deliverable:** Intelligence dossier with target information and attack surface map

### Phase 3: Attack Execution

**Objective:** Exploit identified weaknesses to achieve objectives

**Key Activities:**
- **Initial Access**
  - Exploit vulnerabilities in perimeter defenses
  - Phishing, social engineering, or physical intrusion
  - For AI: Prompt injection, API abuse
  
- **Establish Persistence**
  - Install backdoors and command & control (C2)
  - Create alternative access methods
  - For AI: Inject persistent instructions, poison context
  
- **Privilege Escalation**
  - Exploit local vulnerabilities
  - Credential theft and lateral movement
  - For AI: Escalate from user to system-level control
  
- **Goal Achievement**
  - Data exfiltration, system compromise, or other objectives
  - Maintain stealth throughout operation
  
- **Clean-up & Evidence Collection**
  - Document all actions with evidence
  - Remove traces if required (or leave for blue team training)

**Deliverable:** Exploitation evidence with step-by-step attack chain documentation

### Phase 4: Reporting & Debriefing

**Objective:** Communicate findings and provide actionable recommendations

**Key Activities:**
- **Comprehensive Report**
  - Executive summary (business impact, risk levels)
  - Technical findings (vulnerabilities exploited, attack paths)
  - Evidence (screenshots, logs, PoC code)
  - Remediation recommendations (prioritized by risk)
  
- **Presentation & Debriefing**
  - Present findings to stakeholders
  - Demonstrate attack techniques (if safe)
  - Answer questions and provide clarifications
  
- **Blue Team Collaboration**
  - Share indicators of compromise (IOCs)
  - Discuss detection gaps and improvements
  - Purple team knowledge transfer

**Deliverable:** Final red team report with findings, evidence, and remediation roadmap

## Best Practices

### Planning Phase
- **Understand Business Context**: Align testing with business priorities and risk tolerance
- **Set Clear Success Criteria**: Define measurable objectives before starting
- **Document Everything**: Authorization, scope, rules of engagement must be in writing

### Execution Phase
- **Start Low & Slow**: Gradual reconnaissance avoids detection
- **Diversify Attack Vectors**: Don't rely on single technique
- **Monitor Blue Team Response**: Evaluate detection and response capabilities
- **Maintain Operational Security**: Protect red team infrastructure and tactics

### Reporting Phase
- **Prioritize Findings**: Focus on business impact, not technical severity alone
- **Provide Context**: Explain realistic attack scenarios, not just theoretical risks
- **Actionable Recommendations**: Give specific, implementable remediation steps
- **Celebrate Wins**: Acknowledge effective defenses alongside vulnerabilities

### Organizational Culture
- **No Blame Culture**: Red teaming is learning, not punishment
- **Continuous Improvement**: Regular exercises (quarterly or bi-annually)
- **Purple Team Collaboration**: Break down red-blue silos
- **Executive Buy-In**: Ensure leadership understands value and supports findings

## Progressive Disclosure: Domain-Specific Guidance

This skill uses progressive disclosure to manage complexity. Core methodology above applies universally. For domain-specific techniques, reference these files:

### Cybersecurity Red Teaming (P1)
**File:** [references/cybersecurity-redteam.md](references/cybersecurity-redteam.md)
**Contents:**
- MITRE ATT&CK framework integration
- 7-phase cybersecurity methodology (detailed)
- Network penetration techniques
- Social engineering tactics
- Physical security testing
- Purple team practices
- Tools: Atomic Red Team, CALDERA, Metasploit

### AI/LLM Red Teaming (P1)
**File:** [references/ai-llm-redteam.md](references/ai-llm-redteam.md)
**Contents:**
- LLM vulnerability assessment (OWASP Top 10 LLM)
- Prompt injection attack techniques
- Jailbreaking strategies
- Multi-turn attack simulation
- Evaluation methodologies (scoring, metrics)
- Compliance: NIST AI RMF, EU AI Act
- Tools: DeepTeam, Promptfoo, custom frameworks

### Attack Techniques Library (P2)
**File:** [references/attack-techniques.md](references/attack-techniques.md)
**Contents:**
- Comprehensive attack technique taxonomy
- Cybersecurity: MITRE ATT&CK techniques mapped
- AI/LLM: 20+ prompt injection techniques
- Social engineering patterns
- Physical intrusion methods
- Evasion and anti-forensics

### Tools & Frameworks (P2)
**File:** [references/tools-frameworks.md](references/tools-frameworks.md)
**Contents:**
- MITRE ATT&CK Navigator
- Atomic Red Team & CALDERA
- LLM red teaming frameworks (DeepTeam, Promptfoo)
- C2 frameworks (Cobalt Strike, Sliver)
- OSINT tools (Shodan, theHarvester)
- Evaluation platforms

## Critical Reminders

- **Authorization is Mandatory**: Never conduct red team operations without explicit written authorization
- **Respect Rules of Engagement**: Stay within defined boundaries to avoid legal/ethical issues
- **Document Everything**: Comprehensive documentation is essential for learning and compliance
- **Think Like an Attacker**: Creative, patient, and opportunistic mindset
- **Test Detection AND Response**: Don't just breach—evaluate how organization responds
- **Prioritize Business Impact**: Focus on realistic threats, not just technical curiosities
- **Collaborate with Blue Team**: Knowledge transfer accelerates organizational learning
- **Continuous Evolution**: Red teaming is not one-time; threats evolve, so must testing

## When NOT to Use This Skill

This skill is NOT appropriate for:
- **Simple vulnerability scanning** → Use automated scanners
- **Compliance checklists** → Use audit frameworks
- **Bug bounty hunting** → Use bug bounty methodologies
- **Incident response** → Use IR playbooks (though red team findings inform IR)
- **Production monitoring** → Use SOC/SIEM tools

## Quality Standards

Effective red team operations must:
- ✅ Align with realistic threat scenarios
- ✅ Operate covertly within rules of engagement
- ✅ Document comprehensive evidence trail
- ✅ Provide actionable remediation recommendations
- ✅ Test both detection AND response capabilities
- ✅ Deliver value through organizational learning

## Integration with Other Skills

This skill complements:
- **Research skill**: Threat intelligence gathering, OSINT
- **Skillkit**: If creating custom red team tools or frameworks
- **Frontend-design**: If testing web application security
- **Arch-v/Imagine**: If documenting attack scenarios visually

## References

For deeper domain expertise, always refer to the progressive disclosure files:
1. **Cybersecurity**: `references/cybersecurity-redteam.md`
2. **AI/LLM**: `references/ai-llm-redteam.md`
3. **Attack Techniques**: `references/attack-techniques.md`
4. **Tools**: `references/tools-frameworks.md`

These references provide the technical depth needed for specialized red team operations while keeping this core methodology concise and actionable.
