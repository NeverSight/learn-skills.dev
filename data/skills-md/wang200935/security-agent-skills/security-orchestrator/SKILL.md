---
name: security-orchestrator
description: Router for cross-domain security operations. Use when a task spans multiple
  security domains (e.g. full pentest workflow, multi-domain attack chain, CTF orchestration,
  parallel reconnaissance). For single-domain tasks, let native skill discovery handle
  routing instead.
version: 3.0.0
category: orchestrator
metadata:
  role: orchestrator
  hermes_origin: import
license: MIT
tags:
- security
- orchestrator
related_skills:
- ctf-orchestrator
- advanced-pentest
- osint-framework
---

# Security Orchestrator — Cross-Domain Router

## When to Load

Load this skill ONLY when a security task spans multiple domains and needs
coordination. For single-domain tasks (e.g. "scan this web app", "reverse this
binary"), let the agent's native skill discovery handle routing — it is faster
and avoids loading unnecessary context.

**Use this orchestrator for:**
- Full pentest workflow (recon → web → network → post-exploitation → report)
- Multi-domain attack chains
- CTF orchestration across categories
- Parallel reconnaissance operations
- When you need to understand which skills to combine

## Skill Inventory

Skill counts are machine-generated from `catalog.yaml`. Do not edit manually.

| Domain | Count | Skills |
|:-------|------:|:-------|
| Recon & OSINT | 12 | osint-framework, username-scanner, email-osint-investigation, spiderfoot-automation, parallel-intel-gathering, osint-recon-model, reconnaissance-ops, darkweb-research, vulnerability-discovery, chatgpt-web-relay, local-network-recon, network-device-recon |
| Web Pentest | 13 | web-app-pentest, api-security-testing, client-auth-bypass, web-app-assessment, web-security-advanced, waf-bypass-techniques, ctf-web-attacks, ctf-web-pwn-methodology, framework-vulnerability-research, sql-server-exploitation, client-reverse-engineering, android-pentest, browser-automation-security |
| Network Pentest | 6 | network-pentest, advanced-pentest, pentest-tool-setup, pentest-workflow, pentest-tool-reference, pentest-quick-checklist |
| Exploit Dev | 10 | exploit-development, zero-day-hunting, kernel-exploitation, exploit-poc-builder, crypto-toolkit, crypto-ctf-attacks, cryptography-fundamentals, crypto-attack-patterns, encoding-realignment, binary-exploitation |
| Reverse Engineering | 3 | reverse-engineering, ctf-reverse-engineering, digital-forensics |
| CTF | 10 | ctf-playbook, ctf-orchestrator, ctf-misc-toolkit, ctf-technique-atlas, ctf-training-loop, ctf-web-exploitation, ctf-writeup-discipline, ctf-writeup-screenshots, ctf-kernel-exploitation, ctf-jail-escape |
| Post-Exploitation | 6 | post-exploitation-ops, intranet-pentest-advanced, advanced-attack-chains, professional-pentest-guide, autonomous-pentest-scanner, pentest-report-generator |
| Cloud Security | 6 | ai-ml-security-assessment, ai-mcp-security, modern-attack-surfaces, security-and-hardening, security-audit, offensive-toolkit |
| Hardware & IoT | 12 | hardware-iot-hacking, bluetooth-jammer-sweep, wifi-deauth-jammer, nrf24-bitbang-spi, rf-multi-protocol-jammer, wifi-dualband-jammer, esp32-serial-diag, flipper-zero-backup, flipper-zero-firmware, rf-jammer-firmware-port, smart-card-driver-debug, smart-card-usb-direct |

**Total: 79 skills across 9 domains + this orchestrator**

## Routing Logic

```
User intent → route to skill:

"scan this target" / "find vulnerabilities" → recon + web-app-pentest
"exploit this bug" / "write PoC" → exploit-development
"reverse this binary" / "decompile" → reverse-engineering
"CTF challenge" / "capture the flag" → ctf-orchestrator
"enumerate network" / "port scan" → network-pentest
"OSINT on person/domain" → osint-framework
"bypass WAF" → waf-bypass-techniques
"privilege escalation" / "lateral movement" → post-exploitation-ops
"audit this code" / "security review" → security-audit
"hack IoT device" / "firmware reverse" → hardware-iot-hacking
"AI security" / "MCP vulnerability" → ai-mcp-security
"fuzz this target" / "find crashes" → zero-day-hunting
"crack this hash" / "break encryption" → cryptography-fundamentals
"pentest report" → pentest-report-generator
"jailbreak" / "escape sandbox" → ctf-misc-toolkit
```

## Parallel Execution

For multi-domain tasks, load skills in parallel:
- **Full pentest**: recon + web-app-pentest + network-pentest + post-exploitation
- **Bug bounty**: recon + web-app-pentest + exploit-dev + waf-bypass-techniques
- **CTF solve**: ctf-orchestrator routes to ctf-web-exploitation / crypto-ctf-attacks / ctf-misc-toolkit / ctf-reverse-engineering
- **Internal pentest**: network-pentest + post-exploitation + intranet-pentest-advanced
- **Hardware assessment**: hardware-iot-hacking + reverse-engineering

## Installation

```bash
git clone https://github.com/Wang200935/security-agent-skills.git
cd security-agent-skills
./install.sh --agent claude-code  # or codex, cursor, gemini-cli, hermes-agent, openclaw, github-copilot, windsurf
./install.sh --all                # install for all agents
./install.sh --list               # list available skills
./install.sh --dry-run --all      # preview without changes
```

## Companion Rules

Shared rules live in `rules/security-rules.md`. This file contains
authorization boundaries and ethical use guidelines that apply across all
skills.

## Catalog

The machine-readable skill index is in `catalog.yaml`. Regenerate with:
```bash
python scripts/generate_catalog.py
```
Validate with:
```bash
python scripts/validate.py
```
