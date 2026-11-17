---
name: orca-exposure-map
description: External attack surface mapping — internet-facing assets ranked by risk, exposed ports/services, and attacker's-eye view of the environment. Use when user asks about attack surface, exposure, or external view (e.g., "exposure map", "attack surface", "what's exposed", "internet-facing", "external view").
trigger: When user asks about attack surface, exposure, internet-facing assets, external risk, "what's exposed", "show me public-facing assets", "attack surface map", or external exposure analysis (e.g., "what can an attacker see?", "exposed services", "public assets")
---

# Orca Exposure Map Skill

Answers the question: **"What can an attacker see from outside, and what's the easiest way in?"**

Maps all internet-facing assets, ranks them by exploitability, groups by attack vector (exposed services, public storage, vulnerable web apps, open management ports), and presents the environment from an attacker's perspective.

## Usage

```
/orca-exposure-map
/orca-exposure-map account 123456789012
/orca-exposure-map web services
```

Or natural language:
- "what's exposed to the internet?"
- "show me our attack surface"
- "what can an attacker see?"
- "public-facing assets with vulnerabilities"
- "exposed ports and services"

## Processing Logic

### Step 1: Determine Scope

Parse user input:
- **All accounts**: no argument → full environment
- **Specific account**: "account 123456789012" → filter
- **Specific vector**: "web services" → focus on that category

### Step 2: Gather Data (run ALL in parallel)

Run 6 discovery_search queries to cover different exposure types:

**Query 1: Internet-facing assets with critical vulns**
```
discovery_search:
  search_phrase: "internet facing assets with critical vulnerabilities"
  limit: 10
```

**Query 2: Publicly accessible storage**
```
discovery_search:
  search_phrase: "publicly accessible S3 buckets or storage with sensitive data"
  limit: 10
```

**Query 3: Exposed management interfaces**
```
discovery_search:
  search_phrase: "internet facing assets with exposed management ports SSH RDP"
  limit: 10
```

**Query 4: Exposed web applications**
```
discovery_search:
  search_phrase: "internet facing web applications with high vulnerabilities"
  limit: 10
```

**Query 5: Exposed databases**
```
discovery_search:
  search_phrase: "internet facing databases or database ports exposed"
  limit: 10
```

**Query 6: Assets with public IPs and critical alerts**
```
discovery_search:
  search_phrase: "public facing assets with critical open alerts"
  limit: 10
```

### Step 3: Enrich High-Risk Assets

For the top 5 most critical exposed assets, run in parallel:

**Per asset:**
```
get_asset_related_alerts_summary:
  asset_id: <UUID>
```
```
get_asset_related_attack_paths_summary:
  asset_id: <UUID>
```
```
get_asset_crown_jewel_info:
  group_unique_id: <group_unique_id>
```

### Step 4: Classify and Rank

#### Risk Classification

Rank each exposed asset by exploitability:

```
CRITICAL — Immediate exploitation likely:
  • Public-facing + known exploit available (EPSS > 0.5)
  • Exposed management port (SSH/RDP) + weak auth alert
  • Public storage with sensitive data
  • Exposed database with default credentials

HIGH — Exploitable with moderate effort:
  • Public-facing + critical CVE (no known exploit yet)
  • Exposed web app + SQL injection / RCE vulnerability
  • Public-facing + multiple high vulnerabilities stacked

MEDIUM — Requires specific conditions:
  • Public-facing + high CVE but behind WAF/CDN
  • Exposed service with informational vulns
  • Public IP but limited attack surface (few ports)

LOW — Minimal exposure:
  • Public-facing but no known vulnerabilities
  • Exposed but with strong auth/encryption
  • CDN/load balancer with no backend vulns
```

#### Attacker Perspective Grouping

Group by attack vector (how an attacker would approach):

1. **Easy Wins** — known exploits, default creds, public data
2. **Web Attack Surface** — web apps with injection/RCE vulns
3. **Management Access** — SSH, RDP, admin panels exposed
4. **Data Exposure** — public buckets, databases, file shares
5. **Lateral Movement Entry** — exposed assets that connect to internal crown jewels

### Step 5: Map Attack Paths from Outside In

For critical exposed assets, trace attack paths:
- Entry point: the exposed asset
- Pivot: what internal resources it connects to
- Target: crown jewels reachable from this entry point

This shows the "outside-in" kill chain — not just what's exposed, but what an attacker reaches AFTER getting in.

## Proactive Remediation Behavior

**CRITICAL: Never leave the user with just data. After EVERY output layer, suggest the next action and offer to generate remediation code.**

After the dashboard and after every drill-down section:
1. **Suggest what to do next** — based on the exposure findings, recommend the highest-impact fix
2. **Offer remediation format selection** — always ask: "I can generate the fix. What format do you prefer?"
3. **Supported formats**: Terraform, CloudFormation, Ansible, CLI commands (aws/az/gcloud), step-by-step instructions, Pulumi, ARM/Bicep
4. **Auto-suggest easy wins** — proactively say "The #1 target to lock down is X. Want me to generate security group rules / bucket policy / patching script?"

When the user selects a format:
- Generate the remediation code immediately (security group rules, bucket policies, network ACLs, WAF configs, patching scripts)
- Write it to a file: `lockdown-<asset-name>.<ext>` (e.g., `.tf`, `.yml`, `.sh`)
- Include verification commands
- Suggest the next exposure to close after the first one is done

**Format mapping:**
| User says | Extension | Template |
|-----------|-----------|----------|
| Terraform | `.tf` | HCL with security group / bucket policy / network resources |
| CloudFormation | `.cfn.yaml` | YAML template with security resources |
| Ansible | `.yml` | Playbook with security hardening tasks |
| CLI | `.sh` | Shell script with aws/az/gcloud CLI commands |
| Instructions | inline | Numbered step-by-step console walkthrough |
| Pulumi | `.ts` | TypeScript Pulumi program |
| ARM/Bicep | `.bicep` | Bicep template |

## Output Format

### Layer 1: Dashboard

```
═══════════════════════════════════════════════════════════════════
EXPOSURE MAP — External Attack Surface
<date> | <account scope>
═══════════════════════════════════════════════════════════════════

SURFACE: <assessment — 1 line>

┌─────────────────────────────────────────────────────────────────┐
│  EXPOSED ASSETS     <N> internet-facing                         │
│  CRITICAL RISK      <N> immediately exploitable                 │
│  HIGH RISK          <N> exploitable with effort                 │
│  PUBLIC STORAGE     <N> buckets/blobs publicly accessible       │
│  EXPOSED MGMT       <N> SSH/RDP/admin panels                    │
│  EXPOSED DATABASES  <N> databases reachable from internet       │
│  CROWN JEWELS       <N> exposed critical assets                 │
│  ATTACK PATHS       <N> outside-in kill chains                  │
└─────────────────────────────────────────────────────────────────┘

TOP TARGETS (attacker's priority list):
  [1] <asset> — <why it's #1 target> (score: <X.X>)
      <type> | <public IP> | <exposed services>
  [2] <asset> — <why> (score: <X.X>)
      <type> | <public IP> | <exposed services>
  [3] <asset> — <why> (score: <X.X>)
      <type> | <public IP> | <exposed services>
  [4] <asset> — <why> (score: <X.X>)
  [5] <asset> — <why> (score: <X.X>)

RECOMMENDED ACTION:
  Priority #1: Lock down <top target> — <reason>.
  I can generate the security fix right now.

  What format? terraform | cloudformation | ansible | cli |
  instructions | pulumi | arm/bicep

═══════════════════════════════════════════════════════════════════
Or drill down: easy wins | web apps | management | data |
attack paths | accounts | all assets | full
═══════════════════════════════════════════════════════════════════
```

### Layer 2: Drill-Down Sections

#### "easy wins" — Immediately Exploitable

```
───────────────────────────────────────────────────────────────────
EASY WINS — Fix These First
───────────────────────────────────────────────────────────────────

Assets an attacker can compromise with minimal effort:

  [!] <asset> (<type>) in <account>
      Public IP: <ip> | Ports: <list>
      Vulnerability: <CVE> (exploit available, CVSS <X.X>)
      Alerts: <N> critical
      Crown jewel: YES/NO
      Fix: <1-line action>

  [!] <asset> — <description>
      ...

TOTAL EASY WINS: <N>
Estimated fix time: <hours/days>

LET'S CLOSE THESE:
  I'll generate fixes for all easy wins. Choose format:
  terraform | cloudformation | ansible | cli | instructions |
  pulumi | arm/bicep

───────────────────────────────────────────────────────────────────
```

#### "web apps" — Exposed Web Applications

```
───────────────────────────────────────────────────────────────────
WEB ATTACK SURFACE
───────────────────────────────────────────────────────────────────

  <asset> (<type>) — <service name>
    URL: <public URL/IP:port>
    Vulnerabilities:
      <CVE> — <title> (CVSS <X.X>, exploit: YES/NO)
      <CVE> — <title>
    Alerts: <N> (list top 3)
    WAF: YES/NO | CDN: YES/NO

  <asset> — ...

───────────────────────────────────────────────────────────────────
```

#### "management" — Exposed Management Ports

```
───────────────────────────────────────────────────────────────────
EXPOSED MANAGEMENT INTERFACES
───────────────────────────────────────────────────────────────────

  ⚠ <asset> — SSH (22) open to 0.0.0.0/0
    IP: <public IP> | Account: <account>
    Auth alerts: <weak auth / default creds / brute force detected>
    Fix: Restrict to VPN/bastion CIDR

  ⚠ <asset> — RDP (3389) open to 0.0.0.0/0
    ...

  ⚠ <asset> — Admin panel (8080/443) exposed
    ...

TOTAL EXPOSED: <N> management interfaces
HIGHEST RISK: <asset> — <why>

LOCK THESE DOWN:
  I can generate security group restrictions, bastion configs,
  or network ACLs. Choose format: terraform | cloudformation |
  ansible | cli | instructions | pulumi | arm/bicep

───────────────────────────────────────────────────────────────────
```

#### "data" — Public Data Exposure

```
───────────────────────────────────────────────────────────────────
DATA EXPOSURE — Publicly Accessible Data Stores
───────────────────────────────────────────────────────────────────

  ⚠ <bucket/storage> in <account>
    Access: PUBLIC READ / PUBLIC WRITE / PUBLIC LIST
    Sensitive data: <types — PII, credentials, API keys, etc.>
    Size: <estimated>
    Fix: <specific action>

  ⚠ <database> in <account>
    Port: <port> open to internet
    Auth: <default creds / weak password / no auth>
    Data: <type if known>
    Fix: <action>

SECURE THIS DATA:
  I can generate bucket policies, encryption configs, or
  access controls. Choose format: terraform | cloudformation |
  ansible | cli | instructions | pulumi | arm/bicep

───────────────────────────────────────────────────────────────────
```

#### "attack paths" — Outside-In Kill Chains

```
───────────────────────────────────────────────────────────────────
OUTSIDE-IN ATTACK PATHS
───────────────────────────────────────────────────────────────────

How an attacker moves from internet to crown jewels:

  [1] Score: <X.X>
      Entry: <exposed asset> (public IP: <ip>)
        → Exploit: <CVE or misconfiguration>
        → Pivot: <internal asset reached>
        → Target: <crown jewel> (<why it matters>)
      Fix entry point: <action to break this chain>

  [2] Score: <X.X>
      Entry: <exposed asset>
        → ...

TOTAL PATHS: <N>
Crown jewels reachable: <N>

BREAK THESE CHAINS:
  Fix the entry point to break all paths at once. I'll generate
  the fix. Choose format: terraform | cloudformation | ansible |
  cli | instructions | pulumi | arm/bicep

───────────────────────────────────────────────────────────────────
```

#### "accounts" — Exposure by Account

```
───────────────────────────────────────────────────────────────────
EXPOSURE BY ACCOUNT
───────────────────────────────────────────────────────────────────

  Account              Exposed    Critical    Mgmt Ports    Public Data
  ─────────────────────────────────────────────────────────────────────
  <account-1>          <N>        <N>         <N>           <N>
  <account-2>          <N>        <N>         <N>           <N>
  ...

WORST ACCOUNT: <account> — <why>

───────────────────────────────────────────────────────────────────
```

#### "all assets" — Complete Asset List

Full list of all exposed assets with basic details, sorted by risk.

#### "full" — Everything Expanded

Show all sections in order.

## Edge Cases

### No Internet-Facing Assets
```
✅ No internet-facing assets with critical vulnerabilities detected.

Your external attack surface appears minimal. Consider:
  • Verify this matches your expected architecture
  • Check if assets are behind CDN/WAF (may not show as "internet-facing")
  • Review network security groups for unintended exposure
```

### Too Many Exposed Assets (> 50)
```
⚠ Large attack surface: <N> internet-facing assets detected.

Showing top 10 by risk. For the full inventory:
  • Use Orca UI → Inventory → Filter: Internet Facing
  • Group by account to assign ownership
  • Consider a network segmentation review
```

### Exposure Without Vulnerabilities
```
<asset> is internet-facing but has no known vulnerabilities.

Risk: LOW (currently)
Note: Attack surface exists — new CVEs could change this.
Recommendation: Monitor for new vulnerabilities, minimize exposure if not needed.
```

## MCP Tools Used

### Primary Tools

| Tool | Purpose | Parameter |
|------|---------|-----------|
| `discovery_search` | Find exposed assets by category | `search_phrase`, `limit` |
| `get_asset_related_alerts_summary` | Alerts on exposed assets | `asset_id` (UUID) |
| `get_asset_related_attack_paths_summary` | Kill chains from exposed assets | `asset_id` (UUID) |
| `get_asset_crown_jewel_info` | Crown jewel status of exposed assets | `group_unique_id` |

### Secondary Tools

| Tool | Purpose | When |
|------|---------|------|
| `get_asset_by_id` | Full asset details | Drill-down on specific asset |
| `get_linked_entities_mapping` | What the exposed asset connects to | "attack paths" drill-down |
| `search_cdr_events` | Who's accessing the exposed asset | Investigation |

### Parameter Notes

- `discovery_search` max 10 results per query — use multiple queries with different search phrases
- Attack path enrichment per asset adds latency — limit to top 5 most critical
- Crown jewel check requires `group_unique_id` from asset data

## Implementation Notes

1. **6 parallel discovery_search queries** cover different exposure categories — don't try to get everything in one query.
2. **Attacker's perspective** is the key differentiator — rank by "how would an attacker prioritize these targets?" not just severity scores.
3. **Outside-in attack paths** show the real risk — an exposed asset with no internal connections is lower risk than one that pivots to crown jewels.
4. **Easy wins** should be actionable — "restrict SSH to VPN CIDR" not "review security groups".
5. **Link to other skills** — suggest `/orca-alert-triage <alert-id>` for individual vulnerabilities, `/orca-impact-analysis` for fix prioritization, `/orca-asset-profile` for full asset context.
6. **discovery_search is the primary tool** — no dedicated "list exposed assets" API, so natural language queries are the approach.
