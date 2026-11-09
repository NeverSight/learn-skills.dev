---
name: payloads-scm-exposure
description: "Insecure Source Code Management (SCM) can lead to several critical vulnerabilities in web applications and services. Developers often rely on SCM systems like Git and Subversion (SVN) to manage their source code versions. However, poor security practices, such as leaving .git and .svn folders in production environments exposed to the internet, can pose significant risks. Exposing the version..."
---

# Source Code Management Exposure Payloads

> **Source:** [PayloadsAllTheThings/Insecure Source Code Management](https://github.com/swisskyrepo/payloadsallthethings/tree/master/Insecure%20Source%20Code%20Management)
> **Category:** `payloads-research` | **Skill ID:** `payloads-scm-exposure`

## Overview

SCM exposure payloads for .git, .svn, and .hg directory disclosure and source code extraction.

This skill integrates the full **PayloadsAllTheThings** (PATT) payload library for the **Source Code Management Exposure Payloads** domain into the REA_Skill framework. Use it during authorized penetration testing, bug bounty research, security audits, and CTF challenges.

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

# Insecure Source Code Management

> Insecure Source Code Management (SCM) can lead to several critical vulnerabilities in web applications and services. Developers often rely on SCM systems like Git and Subversion (SVN) to manage their source code versions. However, poor security practices, such as leaving .git and .svn folders in production environments exposed to the internet, can pose significant risks.

## Summary

* [Methodology](#methodology)
    * [Bazaar](./Bazaar.md)
    * [Git](./Git.md)
    * [Mercurial](./Mercurial.md)
    * [Subversion](./Subversion.md)
* [Labs](#labs)
* [References](#references)

## Methodology

Exposing the version control system folders on a web server can lead to severe security risks, including:

* **Source Code Leaks** : Attackers can download the entire source code repository, gaining access to the application's logic.
* **Sensitive Information Exposure** : Embedded secrets, configuration files, and credentials might be present within the codebase.
* **Commit History Exposure** : Attackers can view past changes, revealing sensitive information that might have been previously exposed and later mitigated.

The first step is to gather information about the target application. This can be done using various web reconnaissance tools and techniques.

* **Manual Inspection** : Check URLs manually by navigating to common SCM paths.
    * Git: `http://target.com/.git/`
    * SVN: `http://target.com/.svn/`

* **Automated Tools** : Refer to the page related to the specific technology.

Once a potential SCM folder is identified, check the HTTP response codes and contents. You might need to bypass `.htaccess` or Reverse Proxy rules.

The NGINX rule below returns a `403 (Forbidden)` response instead of `404 (Not Found)` when hitting the `/.git` endpoint.

```ps1
location /.git {
  deny all;
}
```

For example in Git, the exploitation technique doesn't require to list the content of the `.git` folder (`http://target.com/.git/`), the data extraction can still be conducted when files can be read.

## Labs

* [Root Me - Insecure Code Management](https://www.root-me.org/fr/Challenges/Web-Serveur/Insecure-Code-Management)

## References

* [Hidden directories and files as a source of sensitive information about web application - bl4de - April 30, 2017](https://github.com/bl4de/research/tree/master/hidden_directories_leaks)

---

## REA MCP Integration

```javascript
// REA MCP — Automated payload injection via REA tools
// Use analyze_function, procedure_pseudo_code, or observe_native_calls
// to identify injection sinks, then apply payloads from this skill.
```

## Legal Notice

> ⚠️ **Authorized Use Only.** All payloads in this skill are for security research, penetration testing with written permission, CTF competitions, and defensive study. Unauthorized use against systems you do not own or have explicit permission to test is illegal.
