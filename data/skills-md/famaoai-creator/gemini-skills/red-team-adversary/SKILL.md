---
name: red-team-adversary
description: Performs active security "war gaming" by attempting to exploit identified vulnerabilities in a sandbox. Validates threat reality beyond static scans.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory
  - name: scope
    short: s
    type: string
    description: Assessment scope
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
  - security
---

# Red-Team Adversary

This skill takes a proactive, offensive stance on security to ensure defenses are truly effective.

## Capabilities

### 1. Controlled Exploitation

- Attempts to exploit vulnerabilities found by `security-scanner` within a local sandbox or staging environment.
- Provides "Proof of Concept" (PoC) for critical bugs to demonstrate real impact.

### 2. Resilience Testing

- Simulates common attack vectors (DDoS, SQLi, Credential Stuffing) to test the robustness of the `crisis-manager` and `disaster-recovery-planner`.

## Usage

- "Perform a red-team audit on the authentication module and try to bypass it."
- "Verify if the SQLi vulnerability found yesterday is actually exploitable in our current setup."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
