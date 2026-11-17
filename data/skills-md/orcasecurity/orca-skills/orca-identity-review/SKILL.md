---
name: orca-identity-review
description: Analyzes any cloud identity for overprivileged access, actual usage patterns, lateral movement risk, and least-privilege recommendations. Use when user asks about identity permissions, overprivileged access, or IAM review (e.g., "identity review for anika", "is this role overprivileged", "review permissions", "IAM analysis").
trigger: When user asks to review an identity, check permissions, analyze a role, review IAM access, "is this role overprivileged", "what can this identity do", permission analysis, or identity risk (e.g., "review role admin-role", "is arn:aws:iam::123:role/dev-role overprivileged?", "identity review for terraform-deploy")
---

# Orca Identity Review Skill

Answers the question: **"Is this identity overprivileged, and what's the blast radius if it's compromised?"**

Given an IAM role, user, or service account, analyzes effective permissions vs actual usage from CloudTrail, identifies overprivileged access, maps lateral movement potential, and generates a least-privilege recommendation.

## Usage

```
/orca-identity-review admin-role
/orca-identity-review arn:aws:iam::123456789012:role/bastion-admin-role
```

Or natural language:
- "review the permissions on admin-role"
- "is terraform-deploy overprivileged?"
- "identity risk for orca-scanner-role"
- "what can this role access?"

## Processing Logic

### Step 1: Find the Identity

| Input Pattern | Tool | Parameter |
|--------------|------|-----------|
| ARN format `arn:aws:iam::...` | `get_asset_by_id` | `asset_id` with appropriate `model_type` |
| Role/user name | `get_asset_by_name` | `asset_name`, `model_type: "AwsIamRole"` or `"AwsIamUser"` |
| Name (ambiguous) | Try `get_asset_by_name` with each IAM type, or `discovery_search` |

If multiple results, show list and ask user to pick.

Extract: ARN, identity type (Role/User/ServiceAccount), account, creation date, tags, attached policies.

### Step 2: Gather Data (run ALL in parallel)

**Query 1: Effective permissions**
```
get_aws_effective_permissions_policy_on_asset:
  asset_arn: "<identity ARN>"
```
Returns the current effective permissions AND a recommended least-privilege policy.

**Query 2: Alerts on this identity**
```
get_asset_related_alerts_summary:
  asset_id: <UUID>
```

**Query 3: Alert severity breakdown**
```
get_asset_alerts_count_grouped_by_risk_level:
  asset_id: <UUID>
```

**Query 4: What this identity has DONE (CloudTrail)**
```
search_cdr_events:
  actors: ["<identity ARN>"]
  time_range: "last_30_days"
  limit: 100
```

**Query 5: Action summary**
```
get_cdr_events_grouped_by_event_name:
  actors: ["<identity ARN>"]
  time_range: "last_30_days"
```

**Query 6: Attack paths**
```
get_asset_related_attack_paths_summary:
  asset_id: <UUID>
```

**Query 7: Linked entities**
```
get_linked_entities_mapping:
  asset_id: <UUID or asset_unique_id>
```

**Query 8: Crown jewel status**
```
get_asset_crown_jewel_info:
  group_unique_id: <group_unique_id>
```

### Step 3: Analyze Overprivilege

Compare effective permissions vs CDR actual usage:

**Used permissions** — actions seen in CloudTrail in last 30 days:
- Extract unique action names from CDR events
- These are CONFIRMED in-use permissions

**Unused permissions** — granted but never used:
- All effective permissions MINUS used permissions
- The larger this set, the more overprivileged

**Dangerous permissions** — high-risk regardless of usage:
```
Permission Pattern               Risk
────────────────────────────────────────────────────────
iam:*                            CRITICAL — full IAM control
sts:AssumeRole (broad)           HIGH — lateral movement
s3:* or s3:GetObject on *        HIGH — data exfiltration
ec2:RunInstances                 HIGH — resource hijacking
lambda:InvokeFunction            HIGH — code execution
kms:Decrypt on *                 HIGH — secret access
organizations:*                  CRITICAL — org-level control
iam:CreateUser                   HIGH — persistence
iam:AttachUserPolicy             HIGH — privilege escalation
iam:PassRole                     HIGH — privilege escalation
```

**Overprivilege classification:**
```
IF dangerous_unused_permissions > 5 OR has_admin_star THEN
  "SEVERE" — identity has admin-level access it doesn't use
ELSE IF unused_permissions > 50% of total THEN
  "HIGH" — more than half of permissions are unused
ELSE IF unused_permissions > 20% of total THEN
  "MODERATE" — some excess permissions
ELSE
  "MINIMAL" — well-scoped identity
```

### Step 4: Assess Lateral Movement

Analyze what this identity can REACH:

1. **Role assumption** — can it `sts:AssumeRole`? Which roles?
   - Check effective permissions for AssumeRole
   - Check CDR for actual AssumeRole events (what roles were assumed)
   - Cross-account assumptions = HIGH risk

2. **Resource access** — what services/resources can it touch?
   - Group effective permissions by AWS service
   - Flag services with data access (S3, RDS, DynamoDB, Secrets Manager)

3. **Attack path analysis** — is this identity in any kill chains?
   - From attack paths: role in the chain (entry point, pivot, escalation step)
   - How many attack paths go through this identity?

4. **CDR patterns** — what has it actually done?
   - Source IPs (internal, external, VPN, CI/CD)
   - User-agents (console, CLI, SDK, Terraform)
   - Time patterns (business hours, 24/7, irregular)

### Step 5: Generate Recommendations

Build a specific least-privilege recommendation:

1. **Permissions to REMOVE** — unused AND not in the recommended policy
2. **Permissions to KEEP** — used in CloudTrail in last 30 days
3. **Permissions to REVIEW** — used but potentially overly broad (e.g., `s3:*` when only `s3:GetObject` is used)
4. **Policy suggestion** — the recommended policy from `get_aws_effective_permissions_policy_on_asset`

## Proactive Remediation Behavior

**CRITICAL: Never leave the user with just data. After EVERY output layer, suggest the next action and offer to generate remediation code.**

After the dashboard and after every drill-down section:
1. **Suggest what to do next** — based on the overprivilege verdict, recommend a specific action
2. **Offer remediation format selection** — always ask: "I can generate the fix. What format do you prefer?"
3. **Supported formats**: Terraform, CloudFormation, Ansible, CLI commands (aws/az/gcloud), step-by-step instructions, Pulumi, ARM/Bicep
4. **Auto-suggest the most impactful fix** — proactively say "The biggest risk reduction is removing X. Want me to generate the updated policy?"

When the user selects a format:
- Generate the least-privilege IAM policy or remediation code immediately
- Write it to a file: `remediate-<identity-name>.<ext>` (e.g., `.tf`, `.yml`, `.sh`)
- Include verification commands and rollback instructions
- Suggest the next fix after the first one is done

**Format mapping:**
| User says | Extension | Template |
|-----------|-----------|----------|
| Terraform | `.tf` | HCL with aws_iam_policy resource |
| CloudFormation | `.cfn.yaml` | YAML template with IAM resources |
| Ansible | `.yml` | Playbook with iam tasks |
| CLI | `.sh` | AWS CLI commands for policy updates |
| Instructions | inline | Step-by-step console walkthrough |
| Pulumi | `.ts` | TypeScript Pulumi IAM program |
| ARM/Bicep | `.bicep` | Bicep template for Azure IAM |

## Output Format

### Layer 1: Dashboard

```
═══════════════════════════════════════════════════════════════════
IDENTITY REVIEW — <identity name>
<identity type> | <account> | <ARN>
═══════════════════════════════════════════════════════════════════

VERDICT: <OVERPRIVILEGED / RIGHT-SIZED / MINIMAL>

┌─────────────────────────────────────────────────────────────────┐
│  PERMISSIONS     <N> effective actions across <M> services      │
│  OVERPRIVILEGE   <SEVERE / HIGH / MODERATE / MINIMAL>           │
│  USED (30d)      <N> actions actually used                      │
│  UNUSED          <N> actions never used — removal candidates    │
│  DANGEROUS       <N> high-risk permissions                      │
│  BLAST RADIUS    <M> services, <P> resources reachable          │
│  LATERAL MOVE    <N> roles assumable, <M> accounts reachable    │
│  ATTACK PATHS    <N> kill chains through this identity          │
│  ALERTS          <N> open (<X> critical, <Y> high)              │
│  CDR ACTIVITY    <N> events in 30d, <M> unique actions          │
│  CROWN JEWEL     YES/NO (score: <N>)                            │
└─────────────────────────────────────────────────────────────────┘

PERMISSION SUMMARY:
  Total:        <N> effective actions across <M> services
  Used (30d):   <N> actions — KEEP these
  Unused:       <N> actions — candidates for removal
  Dangerous:    <list of high-risk permissions>

TOP RISK:
  <1-2 sentence summary of the biggest risk with this identity>

RECOMMENDED ACTION:
  <Based on verdict — e.g., "Remove N unused dangerous permissions
  to reduce blast radius by X%. I can generate the updated policy.">

  What format? terraform | cloudformation | ansible | cli |
  instructions | pulumi | arm/bicep

═══════════════════════════════════════════════════════════════════
Or drill down: permissions | usage | lateral | attack paths |
alerts | activity | recommend | full
═══════════════════════════════════════════════════════════════════
```

### Layer 2: Drill-Down Sections

#### "permissions" — Full Permission List

```
───────────────────────────────────────────────────────────────────
PERMISSIONS — <identity name>
───────────────────────────────────────────────────────────────────

BY SERVICE:
  <service> (<N> actions, <M> used):
    ✓ <used-action>           (last used: <date>)
    ✗ <unused-action>         REMOVE — never used in 30d
    ⚠ <dangerous-action>      REVIEW — high risk

  <service> (<N> actions, <M> used):
    ...

SUMMARY:
  Used:      <N> (keep)
  Unused:    <N> (remove)
  Dangerous: <N> (review urgently)

READY TO FIX:
  I can generate an updated policy removing all <N> unused
  permissions. Choose format: terraform | cloudformation |
  ansible | cli | instructions | pulumi | arm/bicep

───────────────────────────────────────────────────────────────────
```

#### "usage" — CDR Activity Details

```
───────────────────────────────────────────────────────────────────
USAGE — <identity name> (last 30 days)
───────────────────────────────────────────────────────────────────

  Total events: <N> | Unique actions: <M>
  Source IPs: <list with classification>
  User-agents: <list with classification>

  TOP ACTIONS BY FREQUENCY:
    <action>  <count>  <service>  <pattern>
    ...

  TIME PATTERN:
    <business hours / 24x7 / irregular>
    Peak activity: <time range>

───────────────────────────────────────────────────────────────────
```

#### "lateral" — Lateral Movement Analysis

```
───────────────────────────────────────────────────────────────────
LATERAL MOVEMENT — <identity name>
───────────────────────────────────────────────────────────────────

  ROLE ASSUMPTIONS:
    Can assume: <N> roles (from permissions)
    Has assumed: <N> roles (from CDR)
    Cross-account: <N> accounts reachable

    <role ARN> — <last assumed date> — <account>
    ...

  SERVICE REACH:
    <N> AWS services accessible
    Data services: <S3, RDS, DynamoDB, SecretsManager, ...>

  ATTACK PATHS:
    <N> kill chains pass through this identity
    [1] <story> — role: <entry/pivot/target>
    ...

REDUCE LATERAL MOVEMENT:
  The fastest way to limit blast radius is to restrict
  AssumeRole permissions. Want me to generate the fix?
  Choose format: terraform | cloudformation | ansible | cli |
  instructions | pulumi | arm/bicep

───────────────────────────────────────────────────────────────────
```

#### "recommend" — Least-Privilege Policy

```
───────────────────────────────────────────────────────────────────
RECOMMENDATION — <identity name>
───────────────────────────────────────────────────────────────────

  PERMISSIONS TO REMOVE (<N>):
    <action> — unused, not in recommended policy
    ...

  PERMISSIONS TO KEEP (<N>):
    <action> — used <X> times in last 30 days
    ...

  PERMISSIONS TO SCOPE DOWN:
    <action> on * → scope to specific resources
    ...

  RECOMMENDED POLICY:
    (from get_aws_effective_permissions_policy_on_asset)
    <JSON policy or summary>

  ESTIMATED RISK REDUCTION:
    Current: <N> permissions → Recommended: <M> permissions
    Reduction: <X>% fewer permissions
    Dangerous removed: <N>

  SAFE DEPLOYMENT:
    [ ] Apply in audit mode first (CloudTrail monitoring)
    [ ] Test with specific workloads before enforcing
    [ ] Monitor for AccessDenied errors after applying
    [ ] Roll back if critical service fails

GENERATE THE FIX:
  I'll create the implementation code for you right now.
  Choose format: terraform | cloudformation | ansible | cli |
  instructions | pulumi | arm/bicep

  After applying, I'll help you verify and move to the next
  identity that needs attention.

───────────────────────────────────────────────────────────────────
```

#### "full" — Everything Expanded

Show all sections in order.

## Edge Cases

### Identity Not Found
```
⚠️ No IAM identity found matching "<input>"

Try:
  • Use full ARN: arn:aws:iam::<account>:role/<name>
  • Check spelling
  • Specify type: "review IAM user admin" or "review role deploy-role"
```

### Non-AWS Identity
```
⚠️ Permission analysis is currently optimized for AWS IAM.

For GCP/Azure identities:
  • CDR activity analysis is available
  • Alert and attack path analysis is available
  • Effective permissions comparison is NOT available
    (get_aws_effective_permissions_policy_on_asset is AWS-only)
```

### No CDR Events
```
CDR: No CloudTrail events for this identity in 30 days.

This means either:
  • Identity is genuinely unused (consider deleting)
  • CloudTrail logging is not enabled for this account
  • CDR retention has expired
```

### Service Role (not human)
Flag in the output:
```
NOTE: This is a SERVICE ROLE (automation), not a human user.
  Assumed by: <what assumes it — EC2, Lambda, ECS, etc.>
  Review with service workload requirements in mind.
```

## MCP Tools Used

### Primary Tools

| Tool | Purpose | Parameter |
|------|---------|-----------|
| `get_asset_by_name` | Find identity by name | `asset_name`, `model_type` |
| `get_asset_by_id` | Full identity details | `asset_id`, `model_type` |
| `get_aws_effective_permissions_policy_on_asset` | Current vs recommended permissions | `asset_arn` (string, NOT array) |
| `get_asset_related_alerts_summary` | All alerts | `asset_id` (UUID) |
| `get_asset_alerts_count_grouped_by_risk_level` | Alert counts | `asset_id` (UUID) |
| `search_cdr_events` | What identity has done | `actors` (array), `time_range`, `limit` |
| `get_cdr_events_grouped_by_event_name` | Action summary | `actors` (array), `time_range` |
| `get_asset_related_attack_paths_summary` | Attack paths | `asset_id` (UUID) |
| `get_linked_entities_mapping` | Connected resources | `asset_id` |
| `get_asset_crown_jewel_info` | Crown jewel status | `group_unique_id` |

### Parameter Notes

- `get_aws_effective_permissions_policy_on_asset` takes `asset_arn` as a **string** (NOT array)
- CDR `actors` must be an **array**: `["arn:aws:iam::123:role/name"]`
- CDR `time_range` is an enum: `"last_24_hours"`, `"last_3_days"`, `"last_7_days"`, `"last_30_days"`
- For `get_asset_by_name`, try `model_type: "AwsIamRole"` first, then `"AwsIamUser"` if no results

## Implementation Notes

1. **Parallelize all queries** in Step 2 — the permission analysis and CDR queries are independent.
2. **The key insight** is comparing effective permissions (what the identity CAN do) vs CDR events (what it actually DID). The gap = overprivilege.
3. **Dangerous permissions** should be flagged regardless of usage — some permissions are high-risk even if actively used (e.g., `iam:*`).
4. **Service roles vs human users** behave differently — flag the identity type and adjust recommendations accordingly.
5. **Cross-account AssumeRole** is the highest lateral movement risk — always call it out.
6. **Link to other skills** — suggest `/orca-asset-profile` for full asset context, `/orca-investigate` for deep CDR analysis.
