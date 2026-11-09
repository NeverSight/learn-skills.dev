---
name: payloads-deserial
description: "Serialization is the process of turning some object into a data format that can be restored later. People often serialize objects in order to save them to storage, or to send as part of communications. Deserialization is the reverse of that process -- taking data structured from some format, and rebuilding it into an object - OWASP Check the following sub-sections, located in other chapters :..."
---

# Insecure Deserialization Payloads

> **Source:** [PayloadsAllTheThings/Insecure Deserialization](https://github.com/swisskyrepo/payloadsallthethings/tree/master/Insecure%20Deserialization)
> **Category:** `payloads-web` | **Skill ID:** `payloads-deserial`

## Overview

Deserialization attack payloads for Java, PHP, Python, Ruby, and .NET gadget chains.

This skill integrates the full **PayloadsAllTheThings** (PATT) payload library for the **Insecure Deserialization Payloads** domain into the REA_Skill framework. Use it during authorized penetration testing, bug bounty research, security audits, and CTF challenges.

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

# Insecure Deserialization

> Serialization is the process of turning some object into a data format that can be restored later. People often serialize objects in order to save them to storage, or to send as part of communications. Deserialization is the reverse of that process -- taking data structured from some format, and rebuilding it into an object - OWASP

## Summary

* [Deserialization Identifier](#deserialization-identifier)
* [POP Gadgets](#pop-gadgets)
* [Labs](#labs)
* [References](#references)

## Deserialization Identifier

Check the following sub-sections, located in other chapters :

* [Java deserialization : ysoserial, ...](Java.md)
* [PHP (Object injection) : phpggc, ...](PHP.md)
* [Ruby : universal rce gadget, ...](Ruby.md)
* [Python : pickle, PyYAML, ...](Python.md)
* [.NET : ysoserial.net, ...](DotNET.md)

| Object Type     | Header (Hex)               | Header (Base64) | Indicators                                                   |
| --------------- | -------------------------- | --------------- | ------------------------------------------------------------ |
| .NET ViewState  | `FF 01`                    | `/w`            | Commonly found inside hidden inputs around HTML forms        |
| BinaryFormatter | `0001 0000 00FF FFFF FF01` | `AAEAAAD`       | Base64 decode and check for the long `FF FF FF FF` sequence. |
| Java Serialized | `AC ED`                    | `rO`            | Base64 decode and check first bytes.                         |
| PHP Serialized  | `4F 3A`                    | `Tz`            | Prefixes like `O:, a:, s:, i:, b:` and length indicators.    |
| Python Pickle   | `80 04 95`                 | `gASV`          | Text: opcodes like `(lp0, S'Test'`.                          |
| Ruby Marshal    | `04 08`                    | `BAgK`          | Base64 decode and look for `\x04\x08` at the start.          |

## POP Gadgets

> A POP (Property Oriented Programming) gadget is a piece of code implemented by an application's class, that can be called during the deserialization process.

POP gadgets characteristics:

* Can be serialized
* Has public/accessible properties
* Implements specific vulnerable methods
* Has access to other "callable" classes

## Labs

* [PortSwigger - Modifying serialized objects](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects)
* [PortSwigger - Modifying serialized data types](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-data-types)
* [PortSwigger - Using application functionality to exploit insecure deserialization](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-using-application-functionality-to-exploit-insecure-deserialization)
* [PortSwigger - Arbitrary object injection in PHP](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-arbitrary-object-injection-in-php)
* [PortSwigger - Exploiting Java deserialization with Apache Commons](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-java-deserialization-with-apache-commons)
* [PortSwigger - Exploiting PHP deserialization with a pre-built gadget chain](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-php-deserialization-with-a-pre-built-gadget-chain)
* [PortSwigger - Exploiting Ruby deserialization using a documented gadget chain](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-ruby-deserialization-using-a-documented-gadget-chain)
* [PortSwigger - Developing a custom gadget chain for Java deserialization](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-developing-a-custom-gadget-chain-for-java-deserialization)
* [PortSwigger - Developing a custom gadget chain for PHP deserialization](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-developing-a-custom-gadget-chain-for-php-deserialization)
* [PortSwigger - Using PHAR deserialization to deploy a custom gadget chain](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-using-phar-deserialization-to-deploy-a-custom-gadget-chain)
* [NickstaDB - DeserLab](https://github.com/NickstaDB/DeserLab)

## References

* [ExploitDB Introduction - Abdelazim Mohammed(@intx0x80) - May 27, 2018](https://web.archive.org/web/20180527082635/https://www.exploit-db.com/docs/english/44756-deserialization-vulnerability.pdf)
* [Exploiting insecure deserialization vulnerabilities - PortSwigger - July 25, 2020](https://web.archive.org/web/20200725143552/https://portswigger.net/web-security/deserialization/exploiting)
* [Instagram's Million Dollar Bug - Wesley Wineberg - December 17, 2015](https://web.archive.org/web/20151217194413/http://exfiltrated.com/research-Instagram-RCE.php)

---

## REA MCP Integration

```javascript
// REA MCP — Automated payload injection via REA tools
// Use analyze_function, procedure_pseudo_code, or observe_native_calls
// to identify injection sinks, then apply payloads from this skill.
```

## Legal Notice

> ⚠️ **Authorized Use Only.** All payloads in this skill are for security research, penetration testing with written permission, CTF competitions, and defensive study. Unauthorized use against systems you do not own or have explicit permission to test is illegal.
