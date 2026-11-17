---
name: orca-investigate
description: CDR-powered incident investigation — traces actor activity, builds session timelines, maps MITRE ATT&CK techniques, and assesses blast radius from cloud audit logs. Use when user asks to investigate activity, trace an actor, or analyze an incident (e.g., "investigate bastion-admin", "trace activity", "what did anika do", "incident investigation").
---

# Orca Investigate Skill

Answers the question: **"What happened, who did it, and how far did they get?"**

Given an actor (IAM identity), source IP, target resource, or suspicious event, traces activity through Orca CDR (CloudTrail/audit logs), builds a session timeline, maps actions to MITRE ATT&CK techniques, clusters related sessions, and assesses the blast radius.

## Usage

```
/orca-investigate arn:aws:iam::123456789012:role/bastion-admin-role
/orca-investigate 10.0.1.50
/orca-investigate account 123456789012
```

Or natural language:
- "investigate what this role did in the last 24 hours"
- "trace activity from IP 10.0.1.50"
- "what happened in this account today?"
- "investigate suspicious AssumeRole events"
- "who accessed the prod database?"
- "incident investigation for orca-3636513"

## Processing Logic

### Step 1: Determine Investigation Scope

Parse user input to determine the investigation axis:

| Input Pattern | Primary Filter | CDR Parameter |
|--------------|---------------|---------------|
| ARN (actor) | Identity-based | `actors: ["<ARN>"]` |
| IP address | Source-based | `source_ip_addresses: ["<IP>"]` |
| Resource ARN/name | Target-based | `targets: ["<resource>"]` |
| Account ID | Account-wide | `accounts: ["<account>"]` |
| Event/action name | Action-based | `actions: ["<action>"]` |
| Alert ID (orca-XXXX) | Alert-initiated | Fetch alert, extract actor/target, then CDR |
| Service name | Service-based | `services: ["<service>"]` |

Determine time range:
- Default: `"last_24_hours"` for active incidents
- "last 3 days" / "last week" → `"last_3_days"` / `"last_7_days"`
- User-specified → map to nearest CDR enum

### Step 2: Gather Data (run ALL in parallel)

**Query 1: Events by the actor/from the source/on the target**
```
search_cdr_events:
  <primary filter>: [<value>]
  time_range: "<selected range>"
  limit: 100
```

**Query 2: Event summary grouped by action**
```
get_cdr_events_grouped_by_event_name:
  <primary filter>: [<value>]
  time_range: "<selected range>"
  page_size: 100
```

**Query 3: If actor-based, also search as target**
```
search_cdr_events:
  targets: ["<actor ARN>"]
  time_range: "<selected range>"
  limit: 50
```
(To find events done TO this identity — policy changes, permission grants, etc.)

**Query 4: If alert-initiated, fetch the alert**
```
get_alert:
  alert_id: "<alert-id>"
```

**Query 5: Related alerts on the asset**
```
get_asset_related_alerts_summary:
  asset_id: <UUID>
```

**Query 6: Related attack paths**
```
get_asset_related_attack_paths_summary:
  asset_id: <UUID>
```

### Step 3: Build Session Timeline

From CDR events, construct a chronological timeline:

1. **Sort all events by timestamp**
2. **Cluster into sessions** based on:
   - Same actor + same source IP + events within 30-minute gaps = one session
   - Actor change or long gap = new session
3. **For each session:**
   - Start time, end time, duration
   - Source IP(s) and user-agent(s)
   - Actions performed (in order)
   - Resources touched
   - Success/failure status of each action

### Step 4: MITRE ATT&CK Mapping

Map observed actions to MITRE ATT&CK for Cloud:

```
CDR Action                          MITRE Technique                    Tactic
──────────────────────────────────────────────────────────────────────────────────
ConsoleLogin                        T1078 — Valid Accounts             Initial Access
AssumeRole (cross-account)          T1550.001 — Web Session Cookie     Lateral Movement
AssumeRole (same account)           T1078.004 — Cloud Accounts         Privilege Escalation
CreateUser / CreateAccessKey        T1136.003 — Cloud Account          Persistence
AttachUserPolicy / PutRolePolicy    T1098.003 — Additional Cloud Roles Persistence
PutBucketPolicy (public)            T1537 — Transfer to Cloud Account  Exfiltration
GetObject (bulk S3)                 T1530 — Data from Cloud Storage    Collection
DescribeInstances / ListBuckets     T1580 — Cloud Infrastructure       Discovery
RunInstances                        T1578.002 — Create Cloud Instance  Resource Hijacking
StopLogging / DeleteTrail           T1562.008 — Disable Cloud Logs     Defense Evasion
ModifyInstanceAttribute             T1578 — Modify Cloud Compute       Execution
AuthorizeSecurityGroupIngress       T1562.007 — Disable Cloud Firewall Defense Evasion
DeleteSnapshot / DeleteBucket       T1485 — Data Destruction           Impact
GetSecretValue / GetParameter       T1552.004 — Cloud Secrets          Credential Access
Invoke / InvokeFunction             T1648 — Serverless Execution       Execution
PutObject (to external account)     T1537 — Transfer to Cloud Account  Exfiltration
CreateSnapshot (shared externally)  T1537 — Transfer to Cloud Account  Exfiltration
```

For each mapped technique, assess:
- **Confidence**: HIGH (action directly matches) / MEDIUM (action could be benign) / LOW (speculative)
- **Context**: Was it expected for this identity's role?

### Step 5: Assess Blast Radius

Determine the scope of impact:

1. **Resources touched** — how many distinct resources were accessed/modified?
2. **Services involved** — how many AWS/Azure/GCP services?
3. **Accounts reached** — any cross-account activity?
4. **Data access** — any data stores accessed (S3, RDS, Secrets Manager)?
5. **Persistence indicators** — any new users, keys, roles, or policies created?
6. **Defense evasion** — any logging/monitoring changes?
7. **Lateral movement** — any role assumptions or cross-account jumps?

Classify blast radius:
```
CONTAINED     — activity limited to 1-2 resources in 1 service
MODERATE      — multiple resources or services, same account
BROAD         — multiple accounts or significant data access
SEVERE        — persistence established + data accessed + evasion attempted
```

### Step 6: Generate Verdict

```
IF defense_evasion AND persistence AND data_access THEN
  "ACTIVE COMPROMISE — containment needed NOW"
ELSE IF persistence OR cross_account_lateral_movement THEN
  "PROBABLE COMPROMISE — investigate and contain"
ELSE IF unusual_actions AND (off_hours OR new_source_ip) THEN
  "SUSPICIOUS — requires investigation"
ELSE IF actions_match_role AND normal_hours AND known_ips THEN
  "LIKELY BENIGN — routine activity"
ELSE
  "INCONCLUSIVE — need more data"
```

## Proactive Remediation Behavior

**CRITICAL: Never leave the user with just data. After EVERY output layer, suggest the next action and offer to generate containment/remediation code.**

After the dashboard and after every drill-down section:
1. **Suggest what to do next** — based on the verdict, recommend containment or remediation
2. **Offer remediation format selection** — always ask: "I can generate containment scripts. What format do you prefer?"
3. **Supported formats**: Terraform, CloudFormation, Ansible, CLI commands (aws/az/gcloud), step-by-step instructions, Pulumi, ARM/Bicep
4. **Urgency-based suggestions**:
   - ACTIVE COMPROMISE → "I can generate containment scripts NOW — revoke access, isolate resources"
   - PROBABLE COMPROMISE → "I can generate investigation runbooks and containment scripts"
   - SUSPICIOUS → "I can generate detection rules and monitoring configs"
   - LIKELY BENIGN → "I can generate an allowlist rule or close the alert"

When the user selects a format:
- Generate the containment/remediation code immediately (IAM policy revocation, security group isolation, credential rotation, detection rules)
- Write it to a file: `contain-<actor-or-resource>.<ext>` (e.g., `.tf`, `.yml`, `.sh`)
- Include verification commands and rollback instructions
- Suggest the next investigation step after containment

**Format mapping:**
| User says | Extension | Template |
|-----------|-----------|----------|
| Terraform | `.tf` | HCL with IAM deny policy / SG isolation resources |
| CloudFormation | `.cfn.yaml` | YAML template with containment resources |
| Ansible | `.yml` | Playbook with containment tasks |
| CLI | `.sh` | Shell script with immediate containment commands |
| Instructions | inline | Step-by-step containment runbook |
| Pulumi | `.ts` | TypeScript Pulumi containment program |
| ARM/Bicep | `.bicep` | Bicep template for Azure containment |

## Output Format

### Layer 1: Dashboard

```
═══════════════════════════════════════════════════════════════════
INVESTIGATION — <scope description>
<actor/IP/resource> | <time range>
═══════════════════════════════════════════════════════════════════

VERDICT: <assessment> | CONFIDENCE: <X%>

┌─────────────────────────────────────────────────────────────────┐
│  EVENTS          <N> total, <M> unique actions                  │
│  SESSIONS        <N> distinct sessions                          │
│  TIME SPAN       <first event> → <last event> (<duration>)     │
│  SERVICES        <N> AWS/Azure/GCP services touched             │
│  RESOURCES       <N> distinct resources accessed                │
│  SOURCE IPs      <N> unique IPs (<classification>)              │
│  USER AGENTS     <N> unique (<classification>)                  │
│  BLAST RADIUS    <CONTAINED / MODERATE / BROAD / SEVERE>        │
│  MITRE ATT&CK   <N> techniques mapped across <M> tactics       │
│  ALERTS          <N> related alerts on involved assets          │
│  ATTACK PATHS    <N> kill chains involving this actor           │
└─────────────────────────────────────────────────────────────────┘

EXECUTIVE SUMMARY:
  <2-3 sentences: what happened, what's the risk, what to do next>

MITRE ATT&CK COVERAGE:
  ■ Initial Access    ■ Execution    □ Persistence    □ Priv Esc
  □ Defense Evasion   ■ Discovery    □ Lateral Move   ■ Collection
  □ Exfiltration      □ Impact
  (■ = observed, □ = not observed)

RECOMMENDED ACTION:
  <Based on verdict — e.g., "Containment needed: revoke access
  for <actor> and rotate credentials. I can generate the scripts.">

  What format? terraform | cloudformation | ansible | cli |
  instructions | pulumi | arm/bicep

═══════════════════════════════════════════════════════════════════
Or drill down: timeline | sessions | mitre | blast radius |
actions | resources | alerts | iocs | contain | full
═══════════════════════════════════════════════════════════════════
```

### Layer 2: Drill-Down Sections

#### "timeline" — Chronological Event Timeline

```
───────────────────────────────────────────────────────────────────
TIMELINE — <scope>
───────────────────────────────────────────────────────────────────

<date/time>  <action>
             Actor: <identity>
             Target: <resource>
             Source: <IP> (<classification>)
             Agent: <user-agent> (<classification>)
             Status: <success/failure>
             MITRE: <technique if mapped>

<date/time>  <action>
             ...

[... continues chronologically ...]

KEY MOMENTS:
  <time> — <significant event description>
  <time> — <significant event description>

───────────────────────────────────────────────────────────────────
```

#### "sessions" — Clustered Sessions

```
───────────────────────────────────────────────────────────────────
SESSIONS — <scope>
───────────────────────────────────────────────────────────────────

SESSION 1: <start> → <end> (<duration>)
  Actor: <identity>
  Source: <IP> (<classification>)
  Agent: <user-agent>
  Actions: <N> total
    <action> × <count>
    <action> × <count>
    ...
  Resources: <list>
  Assessment: <normal / suspicious / malicious>

SESSION 2: <start> → <end>
  ...

SESSION COMPARISON:
  <note any unusual sessions — off-hours, new IPs, different behavior>

───────────────────────────────────────────────────────────────────
```

#### "mitre" — MITRE ATT&CK Mapping

```
───────────────────────────────────────────────────────────────────
MITRE ATT&CK MAPPING — <scope>
───────────────────────────────────────────────────────────────────

TACTIC              TECHNIQUE                  ACTION              CONFIDENCE
──────────────────────────────────────────────────────────────────────────────
Initial Access      T1078 Valid Accounts       ConsoleLogin        HIGH
Discovery           T1580 Cloud Infra Disc     DescribeInstances   MEDIUM
Collection          T1530 Cloud Storage Data   GetObject           HIGH
...

KILL CHAIN ASSESSMENT:
  Tactics covered: <N> of 10
  Chain completeness: <PARTIAL / NEAR-COMPLETE / COMPLETE>
  Missing for full chain: <tactics not observed>

  Assessment: <interpretation of the ATT&CK coverage>

───────────────────────────────────────────────────────────────────
```

#### "blast radius" — Impact Assessment

```
───────────────────────────────────────────────────────────────────
BLAST RADIUS — <scope>
───────────────────────────────────────────────────────────────────

SCOPE: <CONTAINED / MODERATE / BROAD / SEVERE>

RESOURCES ACCESSED:
  <service>: <N> resources
    <resource ARN> — <action performed>
    ...

DATA STORES TOUCHED:
  <S3 bucket / RDS / DynamoDB / etc.> — <action> (<N> events)
  Crown jewel: YES/NO

ACCOUNTS INVOLVED:
  <account-1> — <N> events
  <account-2> — <N> events (CROSS-ACCOUNT!)

PERSISTENCE INDICATORS:
  [!] New user created: <user ARN>
  [!] New access key: <key ID>
  [!] Policy attached: <policy> to <identity>
  (or: None detected)

DEFENSE EVASION:
  [!] Trail stopped/deleted
  [!] Security group modified
  (or: None detected)

CONTAIN NOW:
  I can generate scripts to revoke access, isolate resources,
  and rotate credentials. Choose format: terraform |
  cloudformation | ansible | cli | instructions | pulumi |
  arm/bicep

───────────────────────────────────────────────────────────────────
```

#### "actions" — All Actions Summary

```
───────────────────────────────────────────────────────────────────
ACTIONS — <scope>
───────────────────────────────────────────────────────────────────

  Action                          Count   Service          Risk
  ──────────────────────────────────────────────────────────────
  <action>                        <N>     <service>        <assessment>
  <action>                        <N>     <service>        <assessment>
  ...

BY SERVICE:
  <service>: <N> events (<M> unique actions)
  ...

BY RISK:
  HIGH RISK: <list of dangerous actions>
  NORMAL:    <list of routine actions>

───────────────────────────────────────────────────────────────────
```

#### "resources" — Resources Touched

```
───────────────────────────────────────────────────────────────────
RESOURCES — <scope>
───────────────────────────────────────────────────────────────────

  <resource ARN/name>
    Type: <resource type>
    Actions: <list of actions performed on it>
    Crown jewel: YES/NO
    Alerts: <N> open alerts

  <resource ARN/name>
    ...

───────────────────────────────────────────────────────────────────
```

#### "iocs" — Indicators of Compromise

```
───────────────────────────────────────────────────────────────────
INDICATORS OF COMPROMISE — <scope>
───────────────────────────────────────────────────────────────────

IP ADDRESSES:
  <IP> — <classification> | <N> events | <services>

USER AGENTS:
  <agent> — <classification> | <N> events

IDENTITIES:
  <ARN> — <role in the investigation>

RESOURCES CREATED (potential persistence):
  <ARN> — created at <time>

ACCESS KEYS:
  <key ID> — created for <user> at <time>

SHARE THESE WITH YOUR SOC:
  [Copy-paste block of IOCs for threat intel tools]

AUTOMATE DETECTION:
  I can generate detection rules or monitoring configs for
  these IOCs. Choose format: terraform (CloudWatch/GuardDuty) |
  ansible | cli | instructions

───────────────────────────────────────────────────────────────────
```

#### "contain" — Containment Recommendations

```
───────────────────────────────────────────────────────────────────
CONTAINMENT — Recommended Actions
───────────────────────────────────────────────────────────────────

IMMEDIATE (within 1 hour):
  [ ] <action 1> — <why and how>
  [ ] <action 2> — <why and how>

SHORT-TERM (within 24 hours):
  [ ] <action> — <context>
  [ ] <action> — <context>

INVESTIGATION NEXT STEPS:
  [ ] <what to check next>
  [ ] <what to check next>

EVIDENCE PRESERVATION:
  [ ] Snapshot affected instances before changes
  [ ] Export CloudTrail logs for the period
  [ ] Document current state of modified resources

GENERATE CONTAINMENT CODE:
  I'll create implementation scripts for the actions above.
  Choose format: terraform | cloudformation | ansible | cli |
  step-by-step runbook | pulumi | arm/bicep

  After containment, I can help with:
  • /orca-identity-review <actor> — review and right-size permissions
  • /orca-asset-profile <resource> — full profile of affected assets
  • Detection rule generation — prevent recurrence

───────────────────────────────────────────────────────────────────
```

#### "full" — Everything Expanded

Show all sections in order.

## Edge Cases

### No CDR Events Found
```
⚠ No CDR events found for <input> in <time range>.

Possible reasons:
  • Identity/resource hasn't been active in this period
  • CloudTrail/audit log ingestion not configured for this account
  • CDR retention has expired for older events
  • The actor ARN may be different (check aliases/assumed roles)

Try:
  • Extend time range: /orca-investigate <input> last 30 days
  • Search by account: /orca-investigate account <account-id>
  • Check CDR configuration in Orca Console
```

### Too Many Events (> 1000)
```
Note: High event volume (<N> events). Showing top 100 by relevance.

For high-volume actors (automation/services), consider:
  • Filtering by specific action: /orca-investigate <actor> action CreateUser
  • Filtering by time: /orca-investigate <actor> last 1 hour
  • Using Orca CDR UI for full event exploration
```

### Alert-Initiated Investigation
When starting from an alert:
1. Fetch the alert to get actor/target context
2. Use the alert's actor ARN as the primary CDR filter
3. Include the alert's timeline in the investigation timeline
4. Cross-reference with related alerts on the same asset

### Cross-Account Activity
Flag prominently:
```
⚠ CROSS-ACCOUNT ACTIVITY DETECTED

This actor accessed resources in multiple accounts:
  <account-1> — <N> events
  <account-2> — <N> events

Cross-account activity significantly increases blast radius.
Review each account separately for full impact.
```

## MCP Tools Used

### Primary Tools

| Tool | Purpose | Parameter |
|------|---------|-----------|
| `search_cdr_events` | Detailed event data | `actors`/`targets`/`source_ip_addresses`/`actions`/`services`/`accounts`, `time_range`, `limit` |
| `get_cdr_events_grouped_by_event_name` | Action summary | Same filters as above, `page_size` |
| `get_alert` | Alert context (if alert-initiated) | `alert_id` |
| `get_asset_related_alerts_summary` | Related alerts | `asset_id` (UUID) |
| `get_asset_related_attack_paths_summary` | Attack paths | `asset_id` (UUID) |

### Secondary Tools

| Tool | Purpose | When |
|------|---------|------|
| `get_asset_by_id` | Full asset details | Drill-down on touched resources |
| `get_asset_crown_jewel_info` | Crown jewel status | Blast radius assessment |
| `get_linked_entities_mapping` | Connected resources | Lateral movement analysis |
| `discovery_search` | Find related assets/alerts | Broader investigation |

### CDR Parameter Reference

All array parameters MUST be arrays even for single values:

| Parameter | Type | Description |
|-----------|------|-------------|
| `actors` | array of strings | Actor ARNs |
| `targets` | array of strings | Target resource ARNs |
| `source_ip_addresses` | array of strings | Source IPs |
| `actions` | array of strings | Event/action names |
| `services` | array of strings | Service names (e.g., "iam.amazonaws.com") |
| `accounts` | array of strings | Account IDs |
| `time_range` | enum string | `"last_1_hour"`, `"last_24_hours"`, `"last_3_days"`, `"last_7_days"`, `"last_30_days"` |
| `limit` | integer (1-100) | Max events for search_cdr_events |
| `page_size` | integer (1-100) | Results per page for grouped events |

## Implementation Notes

1. **Parallelize CDR queries** — event search and grouped summary are independent.
2. **Session clustering** is key — raw events are overwhelming; sessions tell a story.
3. **MITRE ATT&CK mapping** adds analyst value — don't just list events, classify them.
4. **Blast radius** drives urgency — "3 resources in 1 service" vs "50 resources across 5 accounts" changes the response.
5. **IOCs section** should be copy-paste ready for SOC tools.
6. **Link to other skills** — suggest `/orca-alert-triage` for related alerts, `/orca-identity-review` for the actor's permissions, `/orca-asset-profile` for touched assets.
7. **Cross-account activity** is always HIGH priority — flag it prominently.
8. **CDR retention** is limited — note if events may be missing due to time range limits.
