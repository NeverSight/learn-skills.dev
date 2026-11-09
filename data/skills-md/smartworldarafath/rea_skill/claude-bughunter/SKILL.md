---
name: claude-bughunter
description: Claude-BugHunter — a Claude Code skill bundle for bug hunting and external red-team work (82 skills, 15 slash commands, 681 disclosed-report patterns across 24 vulnerability classes). MIT + CC-BY-4.0; referenced externally only, no content copied.
---

# Claude-BugHunter — Bug Hunting & Red Team Skill Bundle

## Overview

This skill integrates **[Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)** — a Claude Code skill bundle for bug hunting and external red-team work — into the REA_Skill agent ecosystem.

Includes:
- 82 Claude skills across 24 core vulnerability classes
- 15 slash commands
- 681 disclosed-report patterns
- Enterprise identity + infrastructure attack matrices (Citrix NetScaler, F5 BIG-IP, AD CS, enterprise VPN)
- Recon skills (offensive-osint, osint-methodology) paired with Claude-OSINT

**Licenses:** Code (Python helpers, shell scripts) — MIT; Content (skill methodology, wordlists, regex catalogs, severity rubrics, docs) — CC-BY-4.0. This skill references Claude-BugHunter externally and does **not** copy its content into REA_Skill. Credit Sachin Sharma / Claude-BugHunter when reusing content.

## ⚠️ Security & Red Lines (read first)

- **Authorized use only:** Run bug-hunting and red-team techniques exclusively against targets within a valid bug bounty program scope, or systems you own/have explicit written permission to test.
- **No out-of-scope targets:** Never test systems outside authorized scope.
- **You are responsible** for program rules, authorization, and applicable law.

## ⚡ Integration with REA

Combine Claude-BugHunter patterns with REA skills:
- `website-security-audit` — web app auditing
- `offensive-api-security` — API testing
- `offensive-bug-identification` — static/dynamic bug discovery
- `offensive-osint`, `offensive-osint-methodology` — recon
- `rea-binary-disassembly` — binary analysis for vulnerability confirmation