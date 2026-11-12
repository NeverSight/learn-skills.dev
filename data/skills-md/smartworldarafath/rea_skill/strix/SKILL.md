---
name: strix
description: Autonomous AI penetration testing skill that finds and fixes vulnerabilities in your own applications and web services using the Strix AI pentest agent (usestrix/strix). Owner-authorized, defensive security auditing only.
---

# Strix AI Penetration Testing

## Overview

This skill integrates **[Strix](https://github.com/usestrix/strix)** — the open-source AI penetration testing tool — into the REA_Skill agent ecosystem. Strix deploys autonomous AI hackers to find and fix your app's vulnerabilities, with seamless GitHub Actions / CI/CD integration to scan on every pull request and block insecure code before it reaches production.

Strix is **strictly for targets you own or have explicit, written authorization to test**. Unauthorized testing is illegal in most jurisdictions.

## What Strix Does

- **Autonomous AI hacking:** AI agents that actively test your targets and propose fixes.
- **CI/CD ready:** Integrates with GitHub Actions to scan every pull request.
- **Cloud scans:** `strix cloud scans start --engagement-type live_test --domain-ids <uuid> --wait`
- **Vulnerability listing:** `strix cloud vulns list --severity critical` (JSON output supported)
- **MCP servers:** Connect your own Model Context Protocol servers via `~/.strix/mcp-servers.json` and expose their tools to the agent during a run.
- **REST API:** Every cloud operation has a matching `strix cloud <resource> <verb>` command.

## ⚡ Integration with REA (Reverse Engineer Anything)

When combined with the REA suite:

1. **Pre-publish vulnerability hunt:** Before shipping your app/website, run Strix to find weaknesses, then use REA skills to reverse-engineer and remediate the affected components.
2. **Web audit pivot:** Use the Website Security Audit (`website-security-audit`) skill for the 10-layer defensive scan, then Strix for active AI-driven penetration testing.
3. **Binary ↔ App correlation:** Recover source/assets with REA core skills, then point Strix at the running application to validate exploitability end-to-end.

```bash
# Example: start a live test scan and wait for results
strix cloud scans start --engagement-type live_test --domain-ids <uuid> --wait

# Example: list critical vulnerabilities as JSON
strix cloud vulns list --severity critical --json
```

## 🚀 Setup & Installation

Strix is a Python/uv project. Install from the upstream repository:

```bash
# Clone Strix (upstream: https://github.com/usestrix/strix)
git clone https://github.com/usestrix/strix.git
cd strix

# Install dependencies
uv sync

# Run Strix
uv run strix --help
```

Configure MCP servers (optional) in `~/.strix/mcp-servers.json`:

```json
[
  {
    "name": "github",
    "transport": "http",
    "url": "https://api.githubcopilot.com/mcp/",
    "auth": { "kind": "bearer", "token": "your-token" },
    "allowed_tools": ["list_issues"]
  }
]
```

## 📊 Result Handling

- Strix cloud JSON output is machine-readable; use `--json` when stdout is not a terminal.
- Binary downloads redirect raw bytes or use `--output FILE --json` for download metadata.

## 🛡️ Security & Red Lines

- **Authorized use only:** Run Strix exclusively against systems you own or have explicit, written permission to test, within the agreed scope.
- **You are responsible** for obtaining authorization and complying with applicable law.
- **No third-party targets:** Never point Strix at applications, websites, or APIs you do not own or are not explicitly authorized to assess.
- Provided "as is" with no warranty; misuse is your own responsibility.

## See Also

- Strix repository: https://github.com/usestrix/strix
- Strix documentation: https://docs.strix.ai
- REA_Skill: https://github.com/smartworldarafath/REA_Skill