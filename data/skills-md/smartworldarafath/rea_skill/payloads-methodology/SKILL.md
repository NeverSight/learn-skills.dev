---
name: payloads-methodology
description: "Penetration testing methodology cheatsheets from PayloadsAllTheThings covering Active Directory, Cloud (AWS/Azure/GCP), network pivoting, reverse shells, C2 frameworks, and structured pentest engagement resources."
---

# Pentest Methodology & Resources

> **Source:** [PayloadsAllTheThings/Methodology and Resources](https://github.com/swisskyrepo/payloadsallthethings/tree/master/Methodology%20and%20Resources)
> **Category:** `payloads-resources` | **Skill ID:** `payloads-methodology`

## Overview

Structured penetration testing methodology and reference checklists from PayloadsAllTheThings, covering the full engagement lifecycle from reconnaissance to post-exploitation and reporting.

## Cheatsheet Library

This skill references the following methodology documents from PATT:

| Topic | PATT Reference |
|-------|---------------|
| Active Directory Attack | [Active Directory Attack.md](https://github.com/swisskyrepo/payloadsallthethings/blob/master/Methodology%20and%20Resources/Active%20Directory%20Attack.md) |
| Bind Shell Cheatsheet | [Bind Shell Cheatsheet.md](https://github.com/swisskyrepo/payloadsallthethings/blob/master/Methodology%20and%20Resources/Bind%20Shell%20Cheatsheet.md) |
| Cloud AWS Pentest | [Cloud - AWS Pentest.md](https://github.com/swisskyrepo/payloadsallthethings/blob/master/Methodology%20and%20Resources/Cloud%20-%20AWS%20Pentest.md) |
| Cloud Azure Pentest | [Cloud - Azure Pentest.md](https://github.com/swisskyrepo/payloadsallthethings/blob/master/Methodology%20and%20Resources/Cloud%20-%20Azure%20Pentest.md) |
| Cloud GCP Pentest | [Cloud - GCP Pentest.md](https://github.com/swisskyrepo/payloadsallthethings/blob/master/Methodology%20and%20Resources/Cloud%20-%20GCP%20Pentest.md) |
| Cobalt Strike Cheatsheet | [Cobalt Strike - Cheatsheet.md](https://github.com/swisskyrepo/payloadsallthethings/blob/master/Methodology%20and%20Resources/Cobalt%20Strike%20-%20Cheatsheet.md) |
| Docker | [Docker.md](https://github.com/swisskyrepo/payloadsallthethings/blob/master/Methodology%20and%20Resources/Docker.md) |
| Empire Cheatsheet | [Empire - Cheatsheet.md](https://github.com/swisskyrepo/payloadsallthethings/blob/master/Methodology%20and%20Resources/Empire%20-%20Cheatsheet.md) |
| Generic Methodologies | [Generic Methodologies & Resources.md](https://github.com/swisskyrepo/payloadsallthethings/blob/master/Methodology%20and%20Resources/Generic%20Methodologies%20%26%20Resources.md) |
| Kubernetes | [Kubernetes.md](https://github.com/swisskyrepo/payloadsallthethings/blob/master/Methodology%20and%20Resources/Kubernetes.md) |
| Linux Privesc | [Linux - Privilege Escalation.md](https://github.com/swisskyrepo/payloadsallthethings/blob/master/Methodology%20and%20Resources/Linux%20-%20Privilege%20Escalation.md) |
| Network Pivoting | [Network Pivoting Techniques.md](https://github.com/swisskyrepo/payloadsallthethings/blob/master/Methodology%20and%20Resources/Network%20Pivoting%20Techniques.md) |
| Reverse Shell | [Reverse Shell Cheatsheet.md](https://github.com/swisskyrepo/payloadsallthethings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md) |
| Subdomains Enumeration | [Subdomains Enumeration.md](https://github.com/swisskyrepo/payloadsallthethings/blob/master/Methodology%20and%20Resources/Subdomains%20Enumeration.md) |
| Windows Privesc | [Windows - Privilege Escalation.md](https://github.com/swisskyrepo/payloadsallthethings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md) |

## Workflow

### 1. Pre-Engagement
- Scope definition, rules of engagement, threat modeling
- Asset discovery and attack surface mapping
- OSINT and passive reconnaissance

### 2. Active Reconnaissance
- Subdomain enumeration (`amass`, `subfinder`, `dnsx`)
- Port scanning and service fingerprinting (`nmap`, `masscan`)
- Technology stack identification

### 3. Exploitation
- Prioritize vulnerabilities by impact and exploitability
- Use relevant PATT payload libraries for each vulnerability class
- Document every test case with HTTP logs and screenshots

### 4. Post-Exploitation
- Privilege escalation (Linux/Windows cheatsheets above)
- Lateral movement and network pivoting
- Data access and exfiltration assessment

### 5. Reporting
- Executive summary with business impact
- Technical findings with CVSS scores
- Remediation roadmap with code-level fixes

## REA MCP Integration

```javascript
// REA MCP — Combine with rea-universal-orchestrator for full pentest automation
// Use procedure_assembly, procedure_pseudo_code, and observe_native_calls
// to analyze binaries encountered during post-exploitation.
```

## Legal Notice

> ⚠️ **Authorized Use Only.** All methodology resources in this skill are for authorized penetration testing, security research, and defensive study only.
