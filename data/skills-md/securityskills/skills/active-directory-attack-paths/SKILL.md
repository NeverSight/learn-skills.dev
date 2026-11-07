---
name: active-directory-attack-paths
description: Enumerate and exploit common Active Directory misconfigurations such as Kerberoasting, AS-REP roasting, delegation abuse, and ACL attacks. Use during authorized internal network assessments.
---

# Active Directory Attack Paths

Identify and demonstrate Active Directory misconfigurations during authorized internal assessments.

## When to Use

- You have a foothold (or credentials) inside an authorized internal network
- You need to map privilege-escalation paths to Domain Admin or Enterprise Admin

## Methodology

### 1. Initial Enumeration

- `whoami /all`, domain trusts, nested groups
- BloodHound / SharpHound collection (small collection first: `--collectionmethod All --exclude-dc` if stealth matters)
- Look for: Kerberoastable SPNs, AS-REP roastable accounts (no preauth), unconstrained delegation, DCSync rights, GPO abuse

### 2. Credential Attacks

- **Kerberoasting**: request TGS for SPN accounts, crack offline (`hashcat -m 13100`)
- **AS-REP Roasting**: accounts with `DONT_REQ_PREAUTH`, crack offline (`hashcat -m 18200`)
- Password spraying only within RoE — respect lockout policies

### 3. Delegation Abuse

- Unconstrained delegation: capture TGTs via printer bug (SpoolSample) with Rubeus
- Constrained delegation: S4U2Proxy abuse to impersonate users
- Resource-based constrained delegation (RBCD): requires write rights over `msDS-AllowedToActOnBehalfOfOtherIdentity`

### 4. ACL Attacks

- GenericAll / GenericWrite / WriteDacl / WriteOwner on users, groups, or GPOs
- Force a password reset or ACL change, then re-run collection to confirm the new path

### 5. Domain Dominance

- DCSync (`mimikatz lsadump::dcsync` or secretsdump.py) — only with explicit authorization
- AD CS abuse: ESC1–ESC8 templates (Certipy), Golden/Silver certificates

## Evidence to Capture

For each step: the command run, the output showing the escalation, and the accounts affected.

## Cleanup

Remove created accounts, changed ACLs, and dropped tools; note every modification in the cleanup log.
