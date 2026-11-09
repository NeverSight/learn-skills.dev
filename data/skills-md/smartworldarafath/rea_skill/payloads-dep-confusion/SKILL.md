---
name: payloads-dep-confusion
description: "A dependency confusion attack or supply chain substitution attack occurs when a software installer script is tricked into pulling a malicious code file from a public repository instead of the intended file of the same name from an internal repository. Tool to check for dependency confusion vulnerabilities in multiple package management systems Tool used to find dependency confusion or project..."
---

# Dependency Confusion Payloads

> **Source:** [PayloadsAllTheThings/Dependency Confusion](https://github.com/swisskyrepo/payloadsallthethings/tree/master/Dependency%20Confusion)
> **Category:** `payloads-web` | **Skill ID:** `payloads-dep-confusion`

## Overview

Dependency confusion attack techniques for supply-chain package hijacking.

This skill integrates the full **PayloadsAllTheThings** (PATT) payload library for the **Dependency Confusion Payloads** domain into the REA_Skill framework. Use it during authorized penetration testing, bug bounty research, security audits, and CTF challenges.

## Workflow

### 1. Recon & Identification
- Identify the target technology stack and injection points
- Enumerate endpoints, parameters, and input vectors
- Determine applicable payload categories from the reference below

### 2. Payload Selection
- Browse the PATT payload library for the attack class
- Select encoding-appropriate payloads for the target environment
- Consider WAF bypass variants and obfuscation techniques

### 3. Exploitation (Authorized Only)
- Test payloads in order: passive → active → escalation
- Document every payload tested and its response
- Capture PoC evidence (screenshots, HTTP logs, curl output)

### 4. Verification & Reporting
- Confirm the vulnerability with a clean minimal PoC
- Map findings to CVE/CWE where applicable
- Report with remediation recommendations and code fixes

---

## Full PATT Reference

# Dependency Confusion

> A dependency confusion attack or supply chain substitution attack occurs when a software installer script is tricked into pulling a malicious code file from a public repository instead of the intended file of the same name from an internal repository.

## Summary

* [Tools](#tools)
* [Methodology](#methodology)
    * [NPM Example](#npm-example)
* [References](#references)

## Tools

* [visma-prodsec/confused](https://github.com/visma-prodsec/confused) - Tool to check for dependency confusion vulnerabilities in multiple package management systems
* [synacktiv/DepFuzzer](https://github.com/synacktiv/DepFuzzer) - Tool used to find dependency confusion or project where owner's email can be takeover.

## Methodology

Look for `npm`, `pip`, `gem` packages, the methodology is the same : you register a public package with the same name of private one used by the company and then you wait for it to be used.

* **DockerHub**: Dockerfile image
* **JavaScript** (npm): package.json
* **MVN** (maven): pom.xml
* **PHP** (composer): composer.json
* **Python** (pypi): requirements.txt

### NPM Example

* List all the packages (ie: package.json, composer.json, ...)
* Find the package missing from [www.npmjs.com](https://www.npmjs.com/)
* Register and create a **public** package with the same name
    * Package example : [0xsapra/dependency-confusion-expoit](https://github.com/0xsapra/dependency-confusion-expoit)

## References

* [Exploiting Dependency Confusion - Aman Sapra (0xsapra) - July 2, 2021](https://web.archive.org/web/20251107024922/https://0xsapra.github.io/website/Exploiting-Dependency-Confusion)
* [Dependency Confusion: How I Hacked Into Apple, Microsoft and Dozens of Other Companies - Alex Birsan - February 9, 2021](https://web.archive.org/web/20210209181139/https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610)
* [3 Ways to Mitigate Risk When Using Private Package Feeds - Microsoft - March 29, 2021](https://web.archive.org/web/20210210121930/https://azure.microsoft.com/en-gb/resources/3-ways-to-mitigate-risk-using-private-package-feeds/)
* [$130,000+ Learn New Hacking Technique in 2021 - Dependency Confusion - Bug Bounty Reports Explained - February 22, 2021](https://web.archive.org/web/20210223060107/https://www.youtube.com/watch?v=zFHJwehpBrU)

---

## REA MCP Integration

```javascript
// REA MCP — Automated payload injection via REA tools
// Use analyze_function, procedure_pseudo_code, or observe_native_calls
// to identify injection sinks, then apply payloads from this skill.
```

## Legal Notice

> ⚠️ **Authorized Use Only.** All payloads in this skill are for security research, penetration testing with written permission, CTF competitions, and defensive study. Unauthorized use against systems you do not own or have explicit permission to test is illegal.
