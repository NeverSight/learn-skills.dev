---
name: orca-asset-profile
description: Full 360° security profile of any cloud asset — alerts, attack paths, compliance, permissions, exposure, sensitive data, and CDR activity in one view. Use when user asks about an asset's security posture or profile (e.g., "asset profile for web-bastion-host", "tell me about WEB-PRD", "security posture of", "show me everything about").
trigger: When user asks for a full asset review, asset profile, asset risk summary, "tell me about this asset", "what's the risk on this asset", asset details, or asset security posture (e.g., "profile web-bastion-host", "asset review i-1234567890abcdef0", "what do we know about CI-SERVER-01-PRD")
---

# Orca Asset Profile Skill

Answers the question: **"Tell me everything about this asset in one place."**

Given an asset name, ID, or ARN, provides a complete 360° security profile: all open alerts (grouped by category), attack paths, compliance violations, permissions, network exposure, sensitive data, CDR activity summary, crown jewel status, and linked entities.

## Usage

```
/orca-asset-profile web-bastion-host
/orca-asset-profile i-1234567890abcdef0
/orca-asset-profile arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0
```

Or natural language:
- "tell me about web-bastion-host"
- "profile CI-SERVER-01-PRD"
- "asset risk for vm-chain3-1"
- "what do we know about this instance?"

## Processing Logic

### Step 1: Find the Asset

Determine the input type and use the appropriate tool:

| Input Pattern | Tool | Parameter |
|--------------|------|-----------|
| `orca-XXXX` (alert ID) | `get_asset_by_alert_id` | `alert_id` |
| UUID format | `get_asset_by_id` | `asset_id` |
| `vm_XXXX`, `AwsXXX_XXXX` (asset_unique_id) | `get_asset_by_id` | `asset_id` + `model_type` |
| ARN format `arn:aws:...` | `get_asset_by_id` or `discovery_search` | varies |
| Name (anything else) | `get_asset_by_name` | `asset_name` |

If `get_asset_by_name` returns multiple results, show the list and ask the user to pick.

### Step 2: Gather All Data (run ALL in parallel)

Once the asset is identified, extract its UUID (`Inventory.id` or `id`), `asset_unique_id`, `group_unique_id`, and ARN, then run all queries simultaneously:

**Query 1: Full asset details**
```
get_asset_by_id:
  asset_id: <asset_unique_id or group_unique_id>
  model_type: <asset type e.g. "AwsEc2Instance">
```

**Query 2: All alerts on asset**
```
get_asset_related_alerts_summary:
  asset_id: <UUID>
```

**Query 3: Alert count by severity**
```
get_asset_alerts_count_grouped_by_risk_level:
  asset_id: <UUID>
```

**Query 4: Attack paths**
```
get_asset_related_attack_paths_summary:
  asset_id: <UUID>
```

**Query 5: Crown jewel status**
```
get_asset_crown_jewel_info:
  group_unique_id: <group_unique_id>
```

**Query 6: Compliance frameworks**
```
get_related_compliance_frameworks_for_asset:
  asset_id: <UUID or asset_unique_id>
```

**Query 7: Linked entities**
```
get_linked_entities_mapping:
  asset_id: <UUID or asset_unique_id>
```

**Query 8: CDR events (last 30 days)**
```
search_cdr_events:
  targets: [<asset ARN or identifier>]
  time_range: "last_30_days"
  limit: 50
```

**Query 9: CDR event summary**
```
get_cdr_events_grouped_by_event_name:
  targets: [<asset ARN or identifier>]
  time_range: "last_30_days"
```

**Query 10: Effective permissions (AWS IAM assets only)**
```
get_aws_effective_permissions_policy_on_asset:
  asset_arn: <ARN>
```
Only call this for IAM-related assets (AwsIamRole, AwsIamUser) or assets with IAM profiles.

### Step 3: Synthesize the Profile

From the gathered data, extract and organize:

**Asset Identity:**
- Name, type, account, region, state
- Public/private IPs, DNS names
- OS, kernel, AMI/image
- Tags (all tags)
- Creation date, age, uptime
- CodeOrigins (if present — IaC source)

**Risk Summary:**
- Orca Score, risk level
- Crown jewel status and reason
- Exposure (public_facing, internal)
- Observations (sensitive_data, brute-force_attempts, etc.)

**Alerts (from related_alerts_summary):**
Group by category:
- Vulnerabilities — CVEs with CVSS, exploit status
- Misconfigurations — CSPM findings
- Malware / Threats — detected malware, suspicious files
- Sensitive Data — exposed secrets, PII
- Anomalies — behavioral detections
- IAM — overprivileged, unused access

Sort each group by Orca Score descending.

**Attack Paths:**
- Count of active attack paths
- Top attack paths with stories
- Role of this asset in each path (entry point, pivot, target)

**Compliance:**
- Applicable frameworks and scores
- Number of failing controls per framework

**Permissions (IAM assets):**
- Effective permissions count
- Used vs unused (from CDR correlation)
- Overprivilege assessment

**CDR Activity:**
- Total events in 30 days
- Top actions by count
- Unique actors interacting with this asset
- Any suspicious patterns

**Linked Entities:**
- Connected assets (roles, instances, buckets, databases, load balancers)
- Network connections
- IAM relationships

## Proactive Remediation Behavior

**CRITICAL: Never leave the user with just data. After EVERY output layer, suggest the next action and offer to generate remediation code.**

After the dashboard and after every drill-down section:
1. **Suggest what to do next** — based on the highest-risk finding, recommend a specific action
2. **Offer remediation format selection** — always ask: "I can generate the fix. What format do you prefer?"
3. **Supported formats**: Terraform, CloudFormation, Ansible, CLI commands (aws/az/gcloud), step-by-step instructions, Pulumi, ARM/Bicep
4. **Auto-suggest the most impactful fix** — don't wait for the user to ask. Proactively say "The highest-impact fix is X. Want me to generate it?"

When the user selects a format:
- Generate the remediation code immediately
- Write it to a file: `remediate-<alert-id>.<ext>` (e.g., `.tf`, `.yml`, `.sh`)
- Include verification commands
- Suggest the next fix after the first one is done

**Format mapping:**
| User says | Extension | Template |
|-----------|-----------|----------|
| Terraform | `.tf` | HCL with provider + resource blocks |
| CloudFormation | `.cfn.yaml` | YAML template with Parameters/Resources |
| Ansible | `.yml` | Playbook with tasks |
| CLI | `.sh` | Shell script with cloud CLI commands |
| Instructions | inline | Numbered step-by-step console walkthrough |
| Pulumi | `.ts` | TypeScript Pulumi program |
| ARM/Bicep | `.bicep` | Bicep template |

## Output Format

### Layer 1: Dashboard (always shown)

```
═══════════════════════════════════════════════════════════════════
ASSET PROFILE — <asset name>
<asset type> | <account> | <region> | <state>
═══════════════════════════════════════════════════════════════════

RISK: <Orca Score X.X> (<risk level>) | Crown Jewel: YES/NO (<score>)

┌─────────────────────────────────────────────────────────────────┐
│  ALERTS        <N> total (<X> critical, <Y> high, <Z> medium)  │
│  ATTACK PATHS  <N> active kill chains                           │
│  COMPLIANCE    <N> frameworks, <X> failing controls             │
│  EXPOSURE      <public_facing / internal> | ports: <list>       │
│  SENSITIVE     <data types — PII, secrets, keys, or "none">     │
│  PERMISSIONS   <overprivileged / right-sized / N/A>             │
│  CDR ACTIVITY  <N> events in 30d (<assessment>)                 │
│  LINKED        <N> connected assets                             │
└─────────────────────────────────────────────────────────────────┘

ASSET DETAILS:
  ID:        <instance-id / ARN / unique-id>
  IP:        <public IP> (public) / <private IP>
  OS:        <distribution + version> | EOL: <date or "supported">
  AMI/Image: <image name>
  Tags:      <key=value, key=value, ...>
  Created:   <date> (<age>)
  IaC:       <Terraform / CloudFormation / None> (from CodeOrigins)

TOP ALERTS:
  [1] <alert-id> — <title> (score: <X.X>, <category>)
  [2] <alert-id> — <title> (score: <X.X>, <category>)
  [3] <alert-id> — <title> (score: <X.X>, <category>)

RECOMMENDED ACTION:
  The highest-impact fix is <top alert/issue>. I can generate
  remediation code right now.

  What format? terraform | cloudformation | ansible | cli |
  instructions | pulumi | arm/bicep

═══════════════════════════════════════════════════════════════════
Or drill down: alerts | attack paths | compliance | permissions |
exposure | activity | linked | code origin | full
═══════════════════════════════════════════════════════════════════
```

### Layer 2: Drill-Down Sections

#### "alerts" — All Alerts by Category

```
───────────────────────────────────────────────────────────────────
ALERTS — <asset name>
───────────────────────────────────────────────────────────────────

VULNERABILITIES (<N>):
  <alert-id>  <score>  <CVE> — <title>
              CVSS: <X.X> | Exploit: YES/NO | Fix: <version>

MISCONFIGURATIONS (<N>):
  <alert-id>  <score>  <title>
              Rule: <rule-id> | Compliance: <frameworks>

MALWARE / THREATS (<N>):
  <alert-id>  <score>  <malware name> — <classification>
              Path: <file path>

SENSITIVE DATA (<N>):
  <alert-id>  <score>  <title>
              Data type: <PII / API key / credential>

ANOMALIES (<N>):
  <alert-id>  <score>  <title>

───────────────────────────────────────────────────────────────────
NEXT STEPS:
  Triage any alert:  /orca-alert-triage <alert-id>
  Fix impact:        /orca-impact-analysis <alert-id>
  Generate fix:      Tell me which alert + format (terraform,
                     cloudformation, ansible, cli, instructions,
                     pulumi, arm/bicep)
───────────────────────────────────────────────────────────────────
```

#### "attack paths" — Kill Chains

```
───────────────────────────────────────────────────────────────────
ATTACK PATHS — <asset name>
───────────────────────────────────────────────────────────────────

  [1] Score: <X.X> — <attack path story>
      Role: <entry point / pivot / target>
      Steps: <N> | Crown jewel target: YES/NO

  [2] ...

BREAK THE CHAIN:
  The easiest path to break is [path #N] by fixing <alert>.
  Want me to generate the fix? Choose format: terraform |
  cloudformation | ansible | cli | instructions | pulumi | arm/bicep
───────────────────────────────────────────────────────────────────
```

#### "compliance" — Framework Violations

```
───────────────────────────────────────────────────────────────────
COMPLIANCE — <asset name>
───────────────────────────────────────────────────────────────────

  <Framework Name>: <X>% (<P> pass, <F> fail)
    Failing: <control 1>, <control 2>, ...

  <Framework Name>: <X>%
    Failing: ...

───────────────────────────────────────────────────────────────────
```

#### "permissions" — IAM Analysis

```
───────────────────────────────────────────────────────────────────
PERMISSIONS — <asset name>
───────────────────────────────────────────────────────────────────

  Effective permissions: <N> actions across <M> services
  Used (30d):           <N> actions
  Unused:               <N> actions (candidates for removal)

  DANGEROUS PERMISSIONS:
    <permission> — <why it's dangerous>
    ...

  Recommendation: /orca-identity-review <identity name>

FIX IT:
  I can generate a least-privilege policy to replace the current
  overprivileged one. Choose format: terraform | cloudformation |
  ansible | cli | instructions | pulumi | arm/bicep
───────────────────────────────────────────────────────────────────
```

#### "activity" — CDR Events

```
───────────────────────────────────────────────────────────────────
CDR ACTIVITY — <asset name> (last 30 days)
───────────────────────────────────────────────────────────────────

  Total events: <N> | Unique actions: <M> | Unique actors: <P>

  TOP ACTIONS:
    <action>  <count>  <actors>
    ...

  RECENT EVENTS:
    <date>  <action>  <actor>  <source IP>
    ...

───────────────────────────────────────────────────────────────────
```

#### "linked" — Connected Assets

```
───────────────────────────────────────────────────────────────────
LINKED ENTITIES — <asset name>
───────────────────────────────────────────────────────────────────

  <entity type>: <count>
    <name> (<type>) — <relationship>
    ...

───────────────────────────────────────────────────────────────────
```

#### "code origin" — IaC Source

```
───────────────────────────────────────────────────────────────────
CODE ORIGIN — <asset name>
───────────────────────────────────────────────────────────────────

  IaC:    <Terraform / CloudFormation / None>
  Repo:   <repository>
  File:   <file>:<lines>
  Author: <git blame author>
  Commit: <hash> "<message>"

  <code snippet>

  Full trace: /orca-config-origin <alert-id>

FIX AT SOURCE:
  I can generate the corrected IaC code. Choose format:
  terraform | cloudformation | ansible | pulumi | arm/bicep
───────────────────────────────────────────────────────────────────
```

#### "full" — Everything Expanded

Show all sections in order.

## Edge Cases

### Asset Not Found
```
⚠️ No asset found matching "<input>"

Try:
  • Check spelling
  • Use instance ID (i-XXXX) or ARN
  • Search: discovery_search for "<input>"
```

### Multiple Assets Match Name
Show a numbered list and ask the user to pick:
```
Multiple assets match "bastion":
  [1] web-bastion-host (AwsEc2Instance) in 123456789012
  [2] bastion-dev (AwsEc2Instance) in 506464807365
  [3] bastion-sg (AwsSecurityGroup) in 123456789012

Which one? (enter number or be more specific)
```

### No Alerts
```
ALERTS: ✅ Clean — no open alerts on this asset
```

### No CDR Events
Note CDR retention limits (30 days) and suggest checking cloud provider audit logs directly.

## MCP Tools Used

### Primary Tools (always called)

| Tool | Purpose | Parameter |
|------|---------|-----------|
| `get_asset_by_name` | Find asset by name | `asset_name` (substring), optional `model_type` |
| `get_asset_by_id` | Full asset details, tags, CodeOrigins | `asset_id`, optional `model_type` |
| `get_asset_by_alert_id` | Find asset from alert | `alert_id` |
| `get_asset_related_alerts_summary` | All alerts (top 50) | `asset_id` (UUID) |
| `get_asset_alerts_count_grouped_by_risk_level` | Alert counts by severity | `asset_id` (UUID) |
| `get_asset_related_attack_paths_summary` | Attack paths (top 50) | `asset_id` (UUID) |
| `get_asset_crown_jewel_info` | Crown jewel status | `group_unique_id` |
| `get_linked_entities_mapping` | Linked entity counts | `asset_id` |
| `search_cdr_events` | Audit log events | `targets` (array), `time_range`, `limit` |
| `get_cdr_events_grouped_by_event_name` | Event summary | `targets` (array), `time_range` |

### Secondary Tools (called when relevant)

| Tool | Purpose | When |
|------|---------|------|
| `get_related_compliance_frameworks_for_asset` | Compliance frameworks | Always attempted |
| `get_aws_effective_permissions_policy_on_asset` | IAM permissions | AWS IAM assets only |
| `get_linked_entities_data` | Detailed linked entities | "linked" drill-down |
| `get_compliance_framework_stats_for_asset` | Per-framework score | "compliance" drill-down |
| `discovery_search` | Fallback asset search | When name search fails |

### Parameter Notes

- `asset_id` for most tools = UUID from `Inventory.id` (e.g., `c46cb523-3db4-49b0-...`)
- `group_unique_id` for crown jewel = from alert/asset data (e.g., `vm_123456789012_i-0caf...`)
- CDR `targets` must be an array: `["arn:aws:..."]`
- CDR `time_range` is an enum: `"last_24_hours"`, `"last_3_days"`, `"last_7_days"`, `"last_30_days"`
- `get_aws_effective_permissions_policy_on_asset` takes `asset_arn` as a string (NOT array)

## Implementation Notes

1. **Parallelize aggressively** — all 10 queries in Step 2 should run simultaneously.
2. **Handle missing data gracefully** — not every asset has CDR events, compliance, or permissions data.
3. **Keep the dashboard under 30 lines** — details go in drill-downs.
4. **Link to other skills** — suggest `/orca-alert-triage`, `/orca-impact-analysis`, `/orca-config-origin` for individual alerts.
5. **CodeOrigins** is in the `get_asset_by_id` response — check `data.CodeOrigins` for IaC source mapping.
6. **Crown jewel score** is in `DetectedCrownJewelScore` / `DetectedCrownJewelReason` in asset data.
7. **Observations** array (e.g., `["public_facing", "sensitive_data", "brute-force_attempts"]`) is key for quick risk assessment.
