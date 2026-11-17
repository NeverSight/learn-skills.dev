---
name: orca-config-origin
description: Traces any Orca alert back to who deployed it, what tool was used, what introduced the issue, and a full timeline of events. Use when user asks about origin, deployment, or ownership of an alert (e.g., "who created this", "where did this come from", "trace back orca-3380725", "who deployed", "what tool was used").
trigger: When user asks who created or changed a resource, where a config came from, who owns an alert, trace back an alert, find the origin of an alert, or "who did this" (e.g., "trace orca-3380725", "who deployed this?", "where did this config come from?", "find the owner of orca-3511464")
---

# Orca Config Origin Skill

Answers the question: **"Who did this, how was it deployed, and what introduced the issue?"**

Given any Orca alert (misconfiguration, vulnerability, sensitive data, or anomaly), traces back through cloud audit logs, Orca CodeOrigins, and asset metadata to find:
1. **Who** created or modified the resource (identity, role, account)
2. **How** it was deployed (Terraform, CloudFormation, Pulumi, CDK, Console, CLI, SDK)
3. **What** introduced the specific issue (the IaC code, AMI, container image, user action, or automation that caused the alert)
4. **When** — a full timeline from resource creation → issue introduction → alert detection
5. **Where** — source code file, CI/CD pipeline, or manual action that should be fixed

## Usage

```
/orca-config-origin <alert-id>
/orca-config-origin orca-3380725
```

Or natural language:
- "who created this misconfiguration? orca-3380725"
- "trace back orca-3511464"
- "where did this config come from? orca-3364845"
- "find the owner of orca-3213766"

## Processing Logic

### Step 1: Understand the Alert and Resource

Fetch the alert with `get_alert` and extract:
- **Asset type** (e.g., AwsUser, GcpUser, AwsS3Bucket, AzureVm)
- **Asset identifiers**: ARN, name, unique ID, account/project
- **Cloud provider**: AWS, Azure, GCP (determines which audit log to query)
- **Misconfiguration details**: What setting is wrong (e.g., MFA disabled, public access, overprivileged role)
- **Alert creation date**: When Orca first detected this

Also fetch the asset with `get_asset_by_id` (using the asset_unique_id or group_unique_id, with `model_type` matching the asset type) for additional context:
- Tags (often contain `owner`, `team`, `environment`, `terraform`, `stack-name`)
- Creation timestamp
- Configuration details
- **CodeOrigins** — if present, this contains the exact IaC source code (repo, file, line numbers, git blame). This is the strongest possible origin signal.

#### Alert Category → Origin Strategy

The origin of the issue depends on the alert type. Classify first, then trace differently:

```
Alert Category       What to Trace                   Key Distinction
─────────────────────────────────────────────────────────────────────────
Misconfiguration     Who configured the resource      The IaC/console action that SET
                     incorrectly?                     the wrong setting IS the cause.
                     e.g., public S3 ACL, no MFA      Fix: change the config.

Vulnerability (CVE)  Who deployed the vulnerable      The IaC/image/AMI that DEPLOYED
                     package/image?                   the resource is the vehicle, but
                     e.g., Log4j, OpenSSL CVE         the PACKAGE is the cause.
                                                      Fix: patch the package or update
                                                      the image — not the IaC itself.

Sensitive Data       Who put the secret/data on       The container image build, user
                     the resource?                    script, or deployment pipeline
                     e.g., API keys in files          that PLACED the file is the cause.
                                                      Fix: remove secret from image/code,
                                                      use secrets manager.

Anomaly / Threat     Who performed the suspicious     The actor IS the finding.
                     action?                          Fix: investigate the actor.
```

**Critical: For vulnerability alerts**, clearly distinguish:
- **"Who created the resource?"** → the infra deployer (Terraform, CFN, etc.) — they are the OWNER but not the CAUSE
- **"What introduced the vulnerability?"** → the AMI, container image, package manager, or user_data script that installed the vulnerable package — this is the ROOT CAUSE

For example: Terraform deploys an EC2 instance (owner: Alex Chen). The AMI bakes in Log4j 2.3 (root cause: the AMI or provisioner). The fix is to update the AMI or patch the package, NOT to change the Terraform module structure.

### Step 1.5: Extract CodeOrigins (if available)

After fetching the asset via `get_asset_by_id`, check for the `CodeOrigins` field. This is Orca's Shift Left data that maps cloud resources back to their IaC source code.

If `CodeOrigins` exists, it contains:
- **type**: `TerraformModuleCall`, `CloudFormationResource`, etc.
- **ReferenceUrl**: Direct link to the source file on GitHub/GitLab with line numbers
- **StartLine / EndLine**: Exact lines in the IaC file
- **CodeSnippet**: The actual code with git blame per line (author, commit hash, date, message)
- **IsDeleted**: Whether the code still exists

**CodeOrigins is the strongest origin signal** — it gives you the exact file, line, author, and commit. When present, it should be the primary source for:
- Deployment method (Terraform, CloudFormation, etc.)
- Owner (git blame author)
- Source code location (repo, file, lines)

Even with CodeOrigins, still query CDR for:
- Runtime modifications (IaC drift)
- When the resource was actually created (CodeOrigins shows the code, not the deploy time)
- Who/what else has touched the resource since deployment

### Step 2: Identify Target Resource for CDR Query

Map the alert's asset to the correct CDR search parameters:

```
Asset Type              CDR Filter Strategy
────────────────────────────────────────────────────────────────
AWS IAM User/Role       targets: [asset ARN]
                        actions: ["CreateUser", "AttachUserPolicy", "PutUserPolicy",
                                  "CreateRole", "AttachRolePolicy", "UpdateAssumeRolePolicy"]

AWS S3 Bucket           targets: [bucket ARN]
                        actions: ["CreateBucket", "PutBucketPolicy", "PutBucketAcl",
                                  "PutBucketPublicAccessBlock", "PutBucketEncryption"]

AWS Security Group      targets: [SG ARN]
                        actions: ["CreateSecurityGroup", "AuthorizeSecurityGroupIngress",
                                  "AuthorizeSecurityGroupEgress", "ModifySecurityGroupRules"]

AWS EC2 Instance        targets: [instance ARN]
                        actions: ["RunInstances", "ModifyInstanceAttribute"]

AWS RDS                 targets: [RDS ARN]
                        actions: ["CreateDBInstance", "ModifyDBInstance"]

AWS Lambda              targets: [function ARN]
                        actions: ["CreateFunction20150331", "UpdateFunctionConfiguration20150331v2",
                                  "AddPermission20150331v2"]

GCP IAM                 targets: [resource name]
                        actions: ["SetIamPolicy", "CreateServiceAccount", "CreateRole"]

GCP Compute             targets: [resource name]
                        actions: ["compute.firewalls.insert", "compute.firewalls.update",
                                  "compute.instances.insert", "compute.instances.setMetadata"]

GCP Storage             targets: [bucket name]
                        actions: ["storage.buckets.create", "storage.buckets.update",
                                  "storage.setIamPermissions"]

Azure VM                targets: [resource ID]
                        actions: ["Microsoft.Compute/virtualMachines/write"]

Azure Storage           targets: [resource ID]
                        actions: ["Microsoft.Storage/storageAccounts/write"]

Azure NSG               targets: [resource ID]
                        actions: ["Microsoft.Network/networkSecurityGroups/write",
                                  "Microsoft.Network/networkSecurityGroups/securityRules/write"]
```

If you cannot determine the specific actions for the asset type, use a broad search:
- Filter by `targets` only (the resource ARN/name)
- Use `time_range: "last_30_days"` to capture recent changes
- Sort results to find the earliest (creation) and latest (last modification) events

### Step 3: Search Audit Logs

Execute CDR queries in this order:

**Query 1: Find modification events for the resource**
```
search_cdr_events:
  targets: [<resource ARN or identifier>]
  time_range: "last_30_days"
  limit: 100
```

**Query 2: If Query 1 returns results, group by event name to see patterns**
```
get_cdr_events_grouped_by_event_name:
  targets: [<resource ARN or identifier>]
  time_range: "last_30_days"
```

**Query 3: If Query 1 returns 0 results, try broader search**
- Try with `accounts` filter (account ID) + `actions` filter (resource-specific actions)
- Try with `services` filter (e.g., `["iam.amazonaws.com"]`)
- Extend to `time_range: "last_30_days"` if using a shorter range

**Query 4: Check related alerts for embedded CloudTrail data**
```
get_asset_related_alerts_summary:
  asset_id: <UUID from Inventory.id>
```
Related alerts often contain CloudTrail events in their RiskFindings that reveal who accessed or modified the resource.

### Step 4: Classify the Deployer

Analyze the CDR events to identify HOW the resource was deployed/modified.

#### User-Agent Classification

The `user_agent` field in CloudTrail/audit events reveals the deployment tool:

```
User-Agent Pattern                   Deployer Classification
────────────────────────────────────────────────────────────────────
"APN/1.0 HashiCorp/1.0              TERRAFORM
 Terraform/X.Y.Z"
"terraform-provider-aws/X.Y.Z"      TERRAFORM (AWS provider)
"terraform-provider-google/X.Y.Z"   TERRAFORM (GCP provider)
"terraform-provider-azurerm/X.Y.Z"  TERRAFORM (Azure provider)

"aws-sdk-go/X.Y.Z"                  TERRAFORM or GO SDK
 + actor is assumed-role             (check role name for clues)

"CloudFormation"                     CLOUDFORMATION
"cloudformation.amazonaws.com"       CLOUDFORMATION
"AWS CloudFormation"                 CLOUDFORMATION

"pulumi-resource-aws/vX.Y.Z"        PULUMI
"pulumi/vX.Y.Z"                     PULUMI

"aws-cdk"                            AWS CDK (generates CFN)
"cdk-deploy"                         AWS CDK

"console.amazonaws.com"              AWS CONSOLE (manual)
"console.cloud.google.com"           GCP CONSOLE (manual)
"Mozilla/5.0" or "Chrome/X"         BROWSER / CONSOLE (manual)

"aws-cli/X.Y.Z"                     AWS CLI
"gcloud/X.Y.Z"                      GCLOUD CLI
"azcli/X.Y.Z"                       AZURE CLI

"boto3/X.Y.Z"                       PYTHON SDK (automation)
"Boto3/X.Y.Z botocore/X.Y.Z"       PYTHON SDK (automation)

"aws-sdk-java/X.Y.Z"                JAVA SDK (automation)
"aws-sdk-nodejs/X.Y.Z"              NODE SDK (Lambda or automation)

"github-actions"                     GITHUB ACTIONS CI/CD
"jenkins"                            JENKINS CI/CD
"atlantis"                           ATLANTIS (Terraform CI/CD)

"orca-security"                      ORCA SECURITY (scanner)
"dassana"                            DASSANA (security platform)
```

#### Actor Classification

The actor identity reveals WHO made the change:

```
Actor Pattern                        Classification
────────────────────────────────────────────────────────────────────
arn:aws:iam::XXXX:user/<name>        HUMAN USER — direct IAM user
arn:aws:sts::XXXX:assumed-role/      ASSUMED ROLE — could be human via SSO
  <role-name>/<session-name>          or automation. Check session name:
                                       - email/username → SSO human
                                       - "i-XXXXX" → EC2 instance
                                       - "botocore-session-XXXX" → SDK
                                       - "terraform-XXXX" → Terraform run
                                       - "AWSCloudFormation" → CFN stack

arn:aws:iam::XXXX:role/<role-name>   SERVICE ROLE — automation/service
  role name contains:
    - "terraform" → Terraform pipeline
    - "cloudformation" → CFN stack
    - "codepipeline" → CI/CD
    - "github-actions" → GitHub Actions
    - "jenkins" → Jenkins
    - "atlantis" → Atlantis

serviceAccount:<name>@<project>.     GCP SERVICE ACCOUNT — automation
  iam.gserviceaccount.com

user:<email>                          GCP/AZURE HUMAN USER

<guid>                                AZURE SERVICE PRINCIPAL
```

#### Source IP Classification

```
Source IP Pattern                     Classification
────────────────────────────────────────────────────────────────────
10.X.X.X / 172.16-31.X.X /          INTERNAL — VPC, on-prem, VPN
  192.168.X.X
Known corporate CIDR ranges           CORPORATE — office/VPN
AWS IP ranges (check ip-ranges.json)  AWS SERVICE — Lambda, CodeBuild, etc.
GitHub Actions IP ranges              GITHUB ACTIONS CI/CD
Unknown public IPs                    INVESTIGATE — could be external
"cloudformation.amazonaws.com"        CLOUDFORMATION SERVICE
```

### Step 5: Build the Origin Chain

Combine all findings into an ownership chain:

```
ORIGIN CHAIN:
  Resource → Event → Actor → Tool → Source

Example:
  S3 bucket "prod-data" →
    PutBucketPolicy (2026-03-15) →
      assumed-role/terraform-deploy/terraform-session →
        Terraform v1.8.2 (user-agent) →
          IP 10.0.1.50 (internal VPC, likely CI/CD runner)
```

### Step 6: Extract IaC Indicators

From the CDR events, extract any IaC-specific metadata:

**CloudFormation:**
- Stack name from the `requestParameters.stackName` or actor session
- Stack ID from event metadata
- Template URL if available

**Terraform:**
- Workspace/state indicators from role session name
- Provider version from user-agent
- State backend clues from source IP (S3 backend, Terraform Cloud IP ranges)

**Tags on the resource** (from `get_asset_by_id`):
- `aws:cloudformation:stack-name` → CloudFormation stack
- `aws:cloudformation:stack-id` → CloudFormation stack ID
- `aws:cloudformation:logical-id` → Logical resource name in template
- `terraform` or `tf_` prefixed tags → Terraform managed
- `pulumi:project` / `pulumi:stack` → Pulumi managed
- `Owner` / `Team` / `CreatedBy` → Organizational ownership
- `Environment` → prod/staging/dev

### Step 7: Determine Ownership

Build the ownership attribution:

```
IF resource has "Owner" or "Team" tag THEN
  Owner = tag value (strongest signal)
ELSE IF CDR shows a specific human user created/modified it THEN
  Owner = that user (direct attribution)
ELSE IF CDR shows an assumed role with SSO session THEN
  Owner = SSO user who assumed the role
ELSE IF CDR shows a CI/CD service role THEN
  Owner = the team that owns the CI/CD pipeline
  (derive from role name, account, or known pipeline mappings)
ELSE IF CDR shows CloudFormation THEN
  Owner = whoever manages the CFN stack
ELSE IF no CDR data available THEN
  Owner = UNKNOWN — suggest manual investigation
```

## Output Format

```
═══════════════════════════════════════════════════════════════════
CONFIG ORIGIN — <alert-id>
<Alert Title>
═══════════════════════════════════════════════════════════════════

ASSET: <asset name> (<asset type>) in <account/project>
ISSUE: <what's wrong — 1 sentence>

┌─────────────────────────────────────────────────────────────────┐
│  DEPLOYED BY: <tool>                                            │
│  OWNER:       <identity or team>                                │
│  ROOT CAUSE:  <what introduced the issue — distinct from owner> │
│  LAST CHANGE: <date> (<how long ago>)                           │
│  METHOD:      <Terraform / CloudFormation / Console / CLI / …>  │
└─────────────────────────────────────────────────────────────────┘

───────────────────────────────────────────────────────────────────
TIMELINE
───────────────────────────────────────────────────────────────────

  Build a visual timeline showing every significant event from
  resource creation to the current alert. Include:

  <date>  ● <event>                           <actor / tool>
  ├───────────────────────────────────────────────────────────
  <date>  ● IaC code committed                <author via git blame>
          │ repo: <repo>, file: <file>:<lines>
          │ commit: <hash> "<message>"
  │
  <date>  ● Resource created                  <actor via CDR/metadata>
          │ tool: <Terraform/CFN/Console/...>
          │ from: <source IP / pipeline>
  │
  <date>  ● <modification event>              <actor via CDR>
          │ action: <API call>
          │ tool: <detected from user-agent>
  │
  <date>  ● Issue introduced                  <what caused it>
          │ (For misconfig: the API call that set the wrong value)
          │ (For vuln: the AMI/image/package that includes the vuln)
          │ (For sensitive data: the file/image that contains the secret)
  │
  <date>  ● Alert first detected by Orca      (alert CreatedAt)
          │ score: <X.X>, risk: <level>
  │
  <today> ● Current state                     <open / investigating>
          │ age: <X days since detection>
          │ exposure window: <X days since issue introduced>

  KEY INSIGHT:
    <1-2 sentences explaining the timeline significance>
    e.g., "The vulnerability was baked into the AMI 137 days ago.
    The resource has been exposed since creation — no one modified
    the security posture after deployment."

  EXPOSURE WINDOW:
    Issue introduced → Today = <X days>
    Alert detected → Today = <X days unactioned>

The timeline should show the FULL story — not just "who deployed it"
but the chain of events that led to the alert being raised.
Always calculate the exposure window (time between issue introduction
and today) and the response gap (time between alert detection and today).

For vulnerability alerts, the timeline often looks like:
  Code committed → Resource deployed → (months pass) →
  CVE published → Orca detects vuln → (days/weeks pass) → Today

For misconfiguration alerts:
  Resource created (correctly) → Config changed (introduced issue) →
  Orca detects → Today
  OR:
  Resource created WITH misconfiguration → Orca detects → Today

For sensitive data alerts:
  Container image built (secret baked in) → Deployed to cluster →
  Orca scans and finds secret → Today

───────────────────────────────────────────────────────────────────
ORIGIN CHAIN
───────────────────────────────────────────────────────────────────

  WHO CREATED THE RESOURCE (owner):
    When:   <timestamp>
    Who:    <actor ARN/identity>
    How:    <user-agent → tool classification>
    From:   <source IP → classification>

  WHAT INTRODUCED THE ISSUE (root cause):
    <For misconfiguration>:
      The same actor/event that created or modified the resource
      IS the root cause. Show the specific API call.

    <For vulnerability>:
      The resource owner deployed it correctly. The issue is:
      • Package: <package name> version <X> (vulnerable)
      • Installed via: <AMI / container image / user_data / package manager>
      • Fix: patch to <version Y> — this is NOT an IaC change
      • If AMI: the AMI builder/owner is responsible for patching
      • If container: the Dockerfile/image owner is responsible

    <For sensitive data>:
      The secret was placed by:
      • Container image build (if file creation time ≈ image build time)
      • User script / provisioner (if file is in user_data path)
      • Manual action (if CDR shows a specific actor writing the file)
      • The fix is in the image build pipeline, not the infra code

  LAST MODIFICATION (if different from creation):
    When:   <timestamp>
    Who:    <actor ARN/identity>
    Action: <event name — what was changed>

  MODIFICATION HISTORY (last 30 days):
    <date>  <action>  <actor>  <tool>
    <date>  <action>  <actor>  <tool>
    ...

───────────────────────────────────────────────────────────────────
DEPLOYMENT METHOD
───────────────────────────────────────────────────────────────────

  Tool:     <TERRAFORM / CLOUDFORMATION / PULUMI / CDK / CONSOLE / CLI / SDK>
  Evidence: <user-agent string, role name, tags, CodeOrigins>

  IaC SOURCE CODE (from CodeOrigins, if available):
    Repo:   <repository URL>
    File:   <file path>
    Lines:  <start>-<end>
    Author: <git blame author>
    Commit: <hash> "<message>" (<date>)

    <code snippet with line numbers>

  IaC INDICATORS (from tags/CDR, if no CodeOrigins):
    • CloudFormation Stack: <stack-name> (<stack-id>)
    • Terraform Provider: <provider/version from user-agent>
    • Terraform Role: <role name suggesting TF pipeline>
    • Resource Tags: <IaC-related tags>
    • CI/CD Pipeline: <pipeline indicators from role/IP/session>

  (If no IaC detected):
    This resource appears to have been created/modified via
    <Console / CLI / direct SDK call>. No IaC management detected.

───────────────────────────────────────────────────────────────────
OWNERSHIP
───────────────────────────────────────────────────────────────────

  Resource owner:  <person, team, or service — who deployed the resource>
  Issue owner:     <who is responsible for fixing THIS specific issue>
                   (may differ from resource owner for vuln/secret alerts)
  Attribution:     <how we determined ownership — CodeOrigins, tag, CDR actor, role>
  Confidence:      <HIGH / MEDIUM / LOW>

  RESOURCE TAGS:
    <key>: <value>
    <key>: <value>
    ...

  (If no owner found):
    ⚠️  No clear owner identified. Suggest:
    [ ] Check CloudFormation/Terraform state for managing stack
    [ ] Query IAM access advisor for who uses this resource
    [ ] Check organizational CMDB or asset inventory

───────────────────────────────────────────────────────────────────
REMEDIATION ROUTING
───────────────────────────────────────────────────────────────────

  FIX SHOULD BE APPLIED IN:
    <WHERE to make the change based on alert type AND deployment method>

  FOR MISCONFIGURATION ALERTS:
    The fix IS in the deployment code/config.

    IF TERRAFORM:
      Fix in the Terraform code, not in the console.
      Changing the resource directly will cause state drift.
      Look for the resource definition in the Terraform repo
      managed by <owner/pipeline>.

    IF CLOUDFORMATION:
      Update the CloudFormation template for stack <stack-name>.
      Direct changes will be overwritten on next stack update.

    IF PULUMI:
      Update the Pulumi program for stack <stack/project>.

    IF CONSOLE / CLI / NO IaC:
      Can be fixed directly via console or CLI.
      Consider importing into IaC to prevent recurrence.

  FOR VULNERABILITY ALERTS:
    The fix is NOT in the IaC code (usually). The IaC deployed
    the resource correctly — the issue is the package/image.

    IF AMI-BASED (EC2):
      1. Update the AMI to include patched packages
      2. Or: add a patch step to user_data / provisioner
      3. Then re-deploy via the existing IaC pipeline
      The Terraform/CFN code structure stays the same —
      only the AMI ID or package version changes.

    IF CONTAINER-BASED (EKS/ECS/K8s):
      1. Update the base image in the Dockerfile
      2. Or: add a package update step in the build
      3. Rebuild and push the image
      4. Redeploy (rolling update via K8s/ECS)
      The IaC that deploys the cluster is NOT the fix target.

    IF OS PACKAGE:
      1. SSH/SSM into the instance and patch directly
      2. Or: update the AMI and re-deploy
      3. For IaC-managed instances, prefer AMI update to avoid drift

  FOR SENSITIVE DATA ALERTS:
    The fix is in whatever placed the secret on the resource.

    IF CONTAINER IMAGE:
      Remove the secret from the Dockerfile/build pipeline.
      Use K8s Secrets or Secrets Manager instead.

    IF USER_DATA / PROVISIONER:
      Remove hardcoded secrets from the script.
      Reference Secrets Manager/Parameter Store at runtime.

    IF MANUAL:
      Delete the file and rotate the exposed credential.

═══════════════════════════════════════════════════════════════════
```

## Edge Cases

### No CDR Events Found

If CDR returns 0 events for the resource:

```
⚠️  No audit log events found for this resource in the last 30 days.

Possible reasons:
  • Resource was created more than 30 days ago (CDR retention limit)
  • Audit logging is not enabled for this service/region
  • GCP Audit Logs or Azure Activity Logs not ingested into Orca CDR

Fallback investigation:
  • Check resource tags for ownership clues
  • Check resource creation date from asset metadata
  • Suggest manual audit log query with extended timeframe
```

Fall back to:
1. Resource tags (from `get_asset_by_id`)
2. Asset creation date from Orca metadata
3. Related alerts that may contain embedded CloudTrail data
4. Suggest direct cloud console audit log query

### Resource Predates CDR Retention

If the resource was created before the CDR retention window:
- Note the creation date from asset metadata
- Show any modification events within the CDR window
- Suggest querying cloud provider's long-term audit log storage (S3/CloudWatch for AWS, Cloud Logging for GCP, Log Analytics for Azure)

### Multiple Modifiers

If multiple actors have modified the resource:
- Show all unique actors with their most recent action
- Highlight the original creator vs. subsequent modifiers
- Flag if different tools were used (e.g., created via Terraform, modified via Console — potential drift)

### IaC Drift Detection

If evidence shows the resource was created by IaC but later modified by Console/CLI:

```
⚠️  POTENTIAL IaC DRIFT DETECTED

  Created by:  Terraform (assumed-role/terraform-deploy)
  Modified by: Console (user:admin@company.com) on 2026-04-10

  The console change may be overwritten on next Terraform apply.
  If the console change was intentional, update the Terraform code
  to match, or the misconfiguration may recur.
```

## MCP Tools Used

### Primary Tools (always called)

| Tool | Purpose | Parameter |
|------|---------|-----------|
| `get_alert` | Understand the alert and resource | `alert_id` |
| `get_asset_by_id` | Full asset details: tags, CodeOrigins, creation time | `asset_id` (asset_unique_id or group_unique_id), optional `model_type` |
| `get_alert_timeline` | Alert lifecycle events (status changes, detections) | `alert_id` |
| `search_cdr_events` | Find creation/modification events in audit logs | `targets`, `time_range`, `limit` |
| `get_cdr_events_grouped_by_event_name` | Aggregate modification patterns | `targets`, `time_range` |

### Secondary Tools (called when needed)

| Tool | Purpose | Parameter |
|------|---------|-----------|
| `get_asset_related_alerts_summary` | Embedded CloudTrail in related alerts | `asset_id` (UUID) |
| `get_linked_entities_data` | Connected resources and relationships | `asset_id`, `linked_entity` |
| `discovery_search` | Search for related assets or configs | `search_phrase` |

### CDR Tool Parameter Reference

Both `search_cdr_events` and `get_cdr_events_grouped_by_event_name` share these parameters:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `time_range` | enum string | Yes | `"last_1_hour"`, `"last_24_hours"`, `"last_3_days"`, `"last_7_days"`, `"last_30_days"` |
| `actors` | string array | No | Filter by actor ARNs/identities |
| `targets` | string array | No | Filter by target resource ARNs/names |
| `services` | string array | No | Filter by service (e.g., `["iam.amazonaws.com"]`) |
| `accounts` | string array | No | Filter by cloud account IDs |
| `actions` | string array | No | Filter by event name (e.g., `["CreateBucket"]`) |
| `source_ip_addresses` | string array | No | Filter by source IPs |
| `log_types` | string array | No | `["CloudTrail", "AzureActivityLog", "GCPAuditLog"]` |
| `cloud_providers` | string array | No | `["aws", "azure", "gcp"]` |
| `limit` | integer (1-100) | No | Max events (`search_cdr_events` only, default: 20) |

**All array parameters must be arrays**, even for single values: `["value"]` not `"value"`.

**`time_range` must be an enum value**, not freeform: use `"last_30_days"` not `"30d"`.

## Implementation Notes

1. **Always start with the broadest CDR query** (`targets` + `time_range: "last_30_days"`) — narrow down later if too many results.
2. **Parse user-agent carefully** — it's the strongest signal for IaC detection. Many user-agents contain multiple tool identifiers (e.g., `"aws-sdk-go/1.44.298 Terraform/1.5.7"`).
3. **Tags are gold** — `aws:cloudformation:stack-name` and similar tags are definitive proof of IaC management.
4. **Handle GCP and Azure** — their audit log formats differ from CloudTrail. Actor format and event names are provider-specific.
5. **Creation vs. modification** — the misconfiguration may have been present since creation, or introduced by a later change. Show both when available.
6. **Respect CDR retention** — if the resource is older than 30 days and no events found, say so clearly rather than claiming "no one modified it."
