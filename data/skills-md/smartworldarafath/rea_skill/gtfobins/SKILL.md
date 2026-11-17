---
name: gtfobins
description: GTFOBins — curated reference of Unix-like executables that can bypass local security restrictions (privilege escalation, post-exploitation). Owner-authorized defensive auditing only; references GTFOBins externally (GPL-3.0), no content copied.
---

# GTFOBins — Unix Binary Bypass Reference

## Overview

This skill integrates **[GTFOBins](https://gtfobins.org)** — the curated list of Unix-like executables that can be used to bypass local security restrictions in misconfigured systems — into the REA_Skill agent ecosystem.

GTFOBins documents functions such as:
- File read / write
- SUID / sudo abuse for privilege escalation
- Bind shell & reverse shell
- Exfiltration
- LOLBins / living-off-the-land binary usage

**GTFOBins is GPL-3.0 licensed.** This skill only references GTFOBins externally and does **not** copy its content into REA_Skill (MIT). Use `https://gtfobins.org` for the full entry details.

## ⚠️ Security & Red Lines (read first)

- **Authorized use only:** Run GTFOBins techniques exclusively against systems you own or have explicit, written permission to test, within the agreed scope.
- **No third-party targets:** Never apply GTFOBins techniques against systems you do not own or are not explicitly authorized to assess.
- **You are responsible** for obtaining authorization and complying with applicable law.
- Unauthorized privilege escalation or bypass is illegal in most jurisdictions.

## ⚡ Integration with REA (Reverse Engineer Anything)

When combined with the REA suite:

1. **Privilege escalation audit:** After gaining an initial foothold on your own system, consult GTFOBins to identify locally installed binaries that can bypass restrictions, then verify remediation (e.g., fix sudoers, remove SUID bits, restrict binary access).
2. **Post-exploitation validation:** Use GTFOBins (bind shell, reverse shell, exfiltration entries) to test whether your own application/server can be abused, then harden accordingly.
3. **REA correlation:** Pair GTFOBins findings with REA skills (`rea-binary-disassembly`, `offensive-linux-privesc`, `website-security-audit`) for root-cause analysis and fix verification.

## 🔍 Example workflow

```bash
# 1. Identify a suspicious/setuid binary on your own system (authorized audit)
find / -perm -4000 2>/dev/null

# 2. Look up the binary on GTFOBins for known bypass techniques
#    Open https://gtfobins.org and search the binary name

# 3. Verify and remediate on your system:
#    - Remove unintended SUID bits: chmod u-s /path/to/binary
#    - Restrict sudoers entries
#    - Apply vendor patches / configuration hardening
```

## 📚 See also

- GTFOBins: https://gtfobins.org
- GTFOBins repository: https://github.com/GTFOBins/gtfobins.github.io (GPL-3.0)
- LOLBAS project (related): https://lolbas-project.github.io
- REA_Skill: https://github.com/smartworldarafath/REA_Skill