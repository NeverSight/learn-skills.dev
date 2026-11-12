---
name: payloads-gwt
description: "Google Web Toolkit (GWT), also known as GWT Web Toolkit, is an open-source set of tools that allows web developers to create and maintain JavaScript front-end applications using Java. It was originally developed by Google and had its initial release on May 16, 2006. GWTMap is a tool to help map the attack surface of Google Web Toolkit (GWT) based applications. A set of tools made to assist in..."
---

# Google Web Toolkit Payloads

> **Source:** [PayloadsAllTheThings/Google Web Toolkit](https://github.com/swisskyrepo/payloadsallthethings/tree/master/Google%20Web%20Toolkit)
> **Category:** `payloads-research` | **Skill ID:** `payloads-gwt`

## Overview

GWT application attack payloads for RPC serialization abuse and endpoint discovery.

This skill integrates the full **PayloadsAllTheThings** (PATT) payload library for the **Google Web Toolkit Payloads** domain into the REA_Skill framework. Use it during authorized penetration testing, bug bounty research, security audits, and CTF challenges.

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

# Google Web Toolkit

> Google Web Toolkit (GWT), also known as GWT Web Toolkit, is an open-source set of tools that allows web developers to create and maintain JavaScript front-end applications using Java. It was originally developed by Google and had its initial release on May 16, 2006.

## Summary

* [Tools](#tools)
* [Methodology](#methodology)
* [References](#references)

## Tools

* [FSecureLABS/GWTMap](https://github.com/FSecureLABS/GWTMap) - GWTMap is a tool to help map the attack surface of Google Web Toolkit (GWT) based applications.
* [GDSSecurity/GWT-Penetration-Testing-Toolset](https://github.com/GDSSecurity/GWT-Penetration-Testing-Toolset) - A set of tools made to assist in penetration testing GWT applications.

## Methodology

* Enumerate the methods of a remote application via it's bootstrap file and create a local backup of the code (selects permutation at random):

    ```ps1
    ./gwtmap.py -u http://10.10.10.10/olympian/olympian.nocache.js --backup
    ```

* Enumerate the methods of a remote application via a specific code permutation

    ```ps1
    ./gwtmap.py -u http://10.10.10.10/olympian/C39AB19B83398A76A21E0CD04EC9B14C.cache.js
    ```

* Enumerate the methods whilst routing traffic through an HTTP proxy:

    ```ps1
    ./gwtmap.py -u http://10.10.10.10/olympian/olympian.nocache.js --backup -p http://127.0.0.1:8080
    ```

* Enumerate the methods of a local copy (a file) of any given permutation:

    ```ps1
    ./gwtmap.py -F test_data/olympian/C39AB19B83398A76A21E0CD04EC9B14C.cache.js
    ```

* Filter output to a specific service or method:

    ```ps1
    ./gwtmap.py -u http://10.10.10.10/olympian/olympian.nocache.js --filter AuthenticationService.login
    ```

* Generate RPC payloads for all methods of the filtered service, with coloured output

    ```ps1
    ./gwtmap.py -u http://10.10.10.10/olympian/olympian.nocache.js --filter AuthenticationService --rpc --color
    ```

* Automatically test (probe) the generate RPC request for the filtered service method

    ```ps1
    ./gwtmap.py -u http://10.10.10.10/olympian/olympian.nocache.js --filter AuthenticationService.login --rpc --probe
    ./gwtmap.py -u http://10.10.10.10/olympian/olympian.nocache.js --filter TestService.testDetails --rpc --probe
    ```

## References

* [From Serialized to Shell :: Exploiting Google Web Toolkit with EL Injection - Stevent Seeley - May 22, 2017](https://web.archive.org/web/20260220100658/https://srcincite.io/blog/2017/05/22/from-serialized-to-shell-auditing-google-web-toolkit-with-el-injection.html)
* [Hacking a Google Web Toolkit application - thehackerish - April 22, 2021](https://web.archive.org/web/20210227222455/https://thehackerish.com/hacking-a-google-web-toolkit-application/)

---

## REA MCP Integration

```javascript
// REA MCP — Automated payload injection via REA tools
// Use analyze_function, procedure_pseudo_code, or observe_native_calls
// to identify injection sinks, then apply payloads from this skill.
```

## Legal Notice

> ⚠️ **Authorized Use Only.** All payloads in this skill are for security research, penetration testing with written permission, CTF competitions, and defensive study. Unauthorized use against systems you do not own or have explicit permission to test is illegal.
