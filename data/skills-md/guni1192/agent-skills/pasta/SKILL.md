---
name: pasta
description: Perform PASTA (Process for Attack Simulation and Threat Analysis) threat modeling by guiding through 7 stages interactively.
argument-hint: "[target system or application name]"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(ls *), Bash(cat *), WebSearch, AskUserQuestion
---

# pasta

Perform threat modeling using the PASTA (Process for Attack Simulation and Threat Analysis) framework — a risk-centric, seven-stage methodology that combines business impact analysis with attacker simulation.

## When to use

- When the user wants to perform threat modeling on an application or system
- When the user wants to identify and prioritize security risks
- When the user runs `/pasta`

## Instructions

Guide the user through all 7 stages of PASTA interactively. At each stage, ask the user relevant questions, wait for their answers, then synthesize the results before moving to the next stage. Output all results in the user's language.

If a target system or application name is provided as an argument, use it as context throughout. If not provided, ask the user what system they want to threat-model.

If the current directory contains source code relevant to the target system, read it proactively to inform stages 2, 3, and 5.

---

### Stage 1: Define Business Objectives

Ask the user the following questions to establish business context:

- What is the purpose of this application/system? What business problem does it solve?
- Who are the primary users and stakeholders?
- What data does this system handle? What is the data classification (public, internal, confidential, restricted)?
- Are there compliance or regulatory requirements (e.g., PCI DSS, HIPAA, GDPR, SOC 2, ISMS)?
- What would be the business impact if this system were compromised (financial loss, reputational damage, legal liability, operational disruption)?
- What are the top business-critical assets that must be protected?

Summarize the business objectives, security goals, and compliance requirements.

---

### Stage 2: Define Technical Scope

Ask the user about the technical environment, and also scan the codebase if available:

- What is the system architecture? (monolith, microservices, serverless, etc.)
- What programming languages, frameworks, and libraries are used?
- What infrastructure does it run on? (cloud provider, on-premises, hybrid, container orchestration)
- What external services, APIs, or third-party dependencies does it integrate with?
- What authentication and authorization mechanisms are in place?
- What data stores are used? (databases, object storage, caches, message queues)
- What network boundaries and zones exist? (DMZ, VPC, internal network)
- Are there mobile clients, SPAs, or other client-side components?

If source code is available in the working directory, scan it to identify:
- Dependency files (package.json, go.mod, Cargo.toml, requirements.txt, etc.)
- Configuration files (docker-compose.yml, Kubernetes manifests, terraform files, etc.)
- API definitions (OpenAPI specs, GraphQL schemas, proto files, etc.)

Produce a technical scope summary listing all components, dependencies, and the attack surface boundary.

---

### Stage 3: Application Decomposition

Based on information gathered so far:

- Identify trust boundaries (where data crosses between different trust levels)
- Identify entry points (APIs, UI forms, file uploads, message consumers, etc.)
- Identify data flows (how data moves between components)
- Identify actors (users, admins, external systems, background jobs)
- Identify assets (data at rest, data in transit, credentials, keys)

Ask the user to confirm or correct the decomposition. Then produce:

1. A list of trust boundaries
2. A list of entry points and exit points
3. A Data Flow Diagram (DFD) in text/Mermaid format showing actors, processes, data stores, and data flows with trust boundaries marked

---

### Stage 4: Threat Analysis

Based on the decomposition, identify threats by:

- Applying threat categories relevant to each data flow and trust boundary:
  - Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege (STRIDE as a reference)
- Considering common attack vectors for the identified technology stack
- Referencing known threat patterns (OWASP Top 10, CWE Top 25, MITRE ATT&CK where applicable)
- Filtering threats by relevancy — focus on threats with real-world evidence of exploitation

Ask the user:
- Are there known threat actors or adversary profiles relevant to your domain?
- Have there been past security incidents or known attack patterns in similar systems?
- Are there any specific threats you are already concerned about?

Produce a threat catalog: a table listing each threat with ID, description, affected component, threat category, and relevancy assessment.

---

### Stage 5: Vulnerability Analysis

Identify potential vulnerabilities by:

- Correlating identified threats with the technical components from Stage 2
- Checking for common vulnerability patterns in the codebase if source code is available:
  - Hardcoded secrets or credentials
  - SQL injection, XSS, command injection patterns
  - Insecure deserialization
  - Missing authentication/authorization checks
  - Insecure cryptographic usage
  - Misconfigured security headers
- Reviewing dependency files for known vulnerable packages (check if lockfiles exist)
- Reviewing infrastructure configuration for misconfigurations

Ask the user:
- Have you run any security scanning tools (SAST, DAST, SCA)? If so, share the results.
- Are there any known vulnerabilities or technical debt items related to security?
- Are there areas of the codebase that have not been reviewed for security?

Produce a vulnerability list: a table with vulnerability ID, description, related threat ID(s), affected component, and estimated severity (Critical/High/Medium/Low).

---

### Stage 6: Attack Modeling and Simulation

Build attack models based on the threats and vulnerabilities identified:

- Construct attack trees showing how an attacker could achieve each high-priority threat goal
  - Root node: attacker's goal (e.g., "Exfiltrate user PII")
  - Child nodes: steps/conditions needed (AND/OR relationships)
  - Leaf nodes: specific exploitable vulnerabilities
- Identify viable attack paths by mapping vulnerabilities to attack tree nodes
- Assess the feasibility of each attack path (skill level required, access needed, detection likelihood)

Present attack trees in text or Mermaid diagram format.

Ask the user:
- Do these attack scenarios seem realistic for your threat landscape?
- Are there existing security controls that would block or detect any of these paths?
- Are there attack paths you want to explore in more detail?

---

### Stage 7: Risk and Impact Analysis

For each viable attack path, assess and score risk:

- **Likelihood**: based on vulnerability exploitability, attacker capability, and existing controls
- **Impact**: based on business impact defined in Stage 1 (financial, reputational, legal, operational)
- **Risk Score**: Likelihood x Impact (use a simple High/Medium/Low matrix or numeric scale)

Produce:

1. A risk assessment table: Attack path, Likelihood, Impact, Risk Score, Priority
2. A prioritized list of countermeasures/mitigations for each high and critical risk, including:
   - Specific remediation actions (code changes, configuration fixes, architecture changes)
   - Detection mechanisms (logging, monitoring, alerting)
   - Preventive controls (WAF rules, input validation, access controls)
3. A summary of residual risks after proposed mitigations

Ask the user:
- Do the risk scores align with your understanding of business priorities?
- Are there any constraints on implementing the proposed countermeasures (budget, timeline, resources)?
- Which mitigations would you like to prioritize?

---

## Output

After completing all 7 stages, produce a final PASTA Threat Model Report as a Markdown file containing:

1. Executive Summary
2. Stage 1: Business Objectives and Security Goals
3. Stage 2: Technical Scope
4. Stage 3: Application Decomposition (with DFD)
5. Stage 4: Threat Catalog
6. Stage 5: Vulnerability List
7. Stage 6: Attack Trees and Attack Paths
8. Stage 7: Risk Assessment and Countermeasures
9. Recommendations and Next Steps

Save the report as `threat-model-pasta.md` in the current working directory. Ask the user for confirmation before writing.

## Important notes

- Always wait for user responses at each stage before proceeding — do NOT skip ahead or assume answers.
- Use the user's language for all output and questions.
- If source code is available, actively read and analyze it to provide concrete, specific findings rather than generic advice.
- Focus on actionable, prioritized results. Avoid boilerplate or generic threat lists.
- Threat relevancy is key to PASTA — always filter by real-world applicability rather than listing every theoretical threat.
