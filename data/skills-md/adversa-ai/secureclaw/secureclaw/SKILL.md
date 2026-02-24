---
name: secureclaw
description: Security hardening toolkit for OpenClaw. Run audits, apply fixes, scan skills, monitor costs and memory integrity.
metadata:
  clawdbot:
    config:
      stateDirs: [".secureclaw"]
---

# SecureClaw — Security Hardening

## Tools

### security_audit
Run a comprehensive security audit of this OpenClaw instance.
Returns findings with severity, description, and remediation steps.
Use when the user asks about security status or hardening.

### security_status
Get current security posture: score, active monitors, recent alerts.

### skill_scan
Scan a ClawHub skill for malicious patterns before installation.
Required parameter: skill name or URL.

### cost_report
Show API cost tracking data: current spend, projections, and alerts.
