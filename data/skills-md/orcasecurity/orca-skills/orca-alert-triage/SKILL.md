---
name: orca-alert-triage
description: Analyzes Orca Security alerts with timeline visualization, risk assessment, and progressive disclosure. Use when user asks to triage, analyze, explain, summarize, investigate, or check an Orca alert by ID (e.g., "triage orca-3636513", "what is alert orca-3548863", "check orca-3636513").
---

# Orca Alert Triage Skill

Formats Orca Security alerts into analyst-friendly summaries with behavioral timelines, risk analysis, and progressive disclosure of investigation steps.

## Usage

```
/orca-alert-triage <alert-id>
/orca-alert-triage orca-3636513
/orca-alert-triage orca-3548863
```

Or natural language:
- "triage alert orca-3636513"
- "explain orca-3548863"
- "analyze alert orca-3636513"

## What This Skill Does

1. **Fetches alert data** from Orca Security via MCP
2. **Analyzes timeline** to identify behavioral patterns and remediation blockers
3. **Calculates blast radius** by checking related assets and correlation
4. **Formats output** with progressive disclosure (summary first, details on request)
5. **Provides contextual recommendations** based on alert type and severity

## Output Format

### Initial Summary (Always Shown)

```
═══════════════════════════════════════════════════════════════════
ALERT TITLE
═══════════════════════════════════════════════════════════════════

VERDICT: <assessment> | CONFIDENCE: <percent> | ACTION: <what to do> | TIMELINE: <when>

───────────────────────────────────────────────────────────────────
ALERT TIMELINE
───────────────────────────────────────────────────────────────────

BEHAVIORAL PATTERN / VULNERABILITY LIFECYCLE:
  [Visual timeline with key events]

RECURRENCE: <pattern analysis>
ESCALATION: <status change summary>
RED FLAGS: <critical indicators if present>

───────────────────────────────────────────────────────────────────
WHAT HAPPENED
───────────────────────────────────────────────────────────────────
[2-3 sentence summary of the alert]

───────────────────────────────────────────────────────────────────
WHY IT MATTERS
───────────────────────────────────────────────────────────────────
Risk Level: <severity> (Orca Score: X.X)

BEHAVIORAL ASSESSMENT / SEVERITY FACTORS:
  [Risk indicators with ✓/✗ symbols]

BLAST RADIUS:
  • Affected Assets: X
  • Alert History: [correlation]
  • Environment: [prod/dev/test]
  • Impact: [description]

BUSINESS IMPACT: [concise statement]

═══════════════════════════════════════════════════════════════════
```

**Follow-up options:**
- Reply with "**investigate**" for investigation checklist
- Reply with "**evidence**" for detailed references
- Reply with "**remediate**" for remediation steps
- Reply with "**correlate**" for related alerts

### Progressive Disclosure Sections (On Request)

**Investigation Checklist** (`investigate`):
- Pre-investigation verification steps
- CloudTrail/audit log queries with actual commands
- Correlation checks
- Clear escalation criteria with team/channel info

**Evidence & References** (`evidence`):
- Alert metadata (IDs, rules, timestamps)
- Anomaly context details
- Direct links (Orca, AWS Console, etc.)
- MITRE ATT&CK mappings

**Remediation Steps** (`remediate`):
- Immediate actions
- Patching/fix instructions
- Verification commands
- Rollback procedures if needed

**Correlation Analysis** (`correlate`):
- Related alerts on same asset
- Similar alerts across environment
- Attack campaign indicators
- Historical pattern analysis

## Alert Processing Logic

### 1. Fetch Alert Data
```
Tools: get_alert, get_alert_timeline, get_asset_alerts_count_grouped_by_risk_level
```

### 2. Determine Alert Category
- **Anomaly Detection**: Behavioral analysis focus
- **Vulnerability (CVE)**: Exploitability and patch status focus
- **Misconfiguration**: Compliance and fix complexity focus
- **Malware/Threat**: Incident response focus

### 3. Timeline Analysis

Analyze event_log for:
- **Duration open**: First detection → current time
- **Recurrence pattern**: Single event vs repeated
- **Status changes**: Count and pattern (closed→reopened = friction)
- **Manual interventions**: User actions indicate organizational issues
- **Integration health**: Which notifications succeeded/failed

Key patterns to identify:
```
Pattern                          Interpretation
────────────────────────────────────────────────────────────────
Single event, no recurrence      Likely benign/false positive
Open > 7 days, no action        Ownership/priority issue
Closed → Reopened same day      Premature closure, issue persists
Multiple dismiss/reopen          Remediation blockers/disagreement
Failed notifications             Integration health problem
```

### 4. Risk Assessment

Calculate confidence level based on:
- **Anomaly alerts:**
  - Same tool family = High confidence benign
  - Minor version change = High confidence benign
  - Completely new tool = Low confidence, investigate
  - Multiple anomalies same timeframe = Medium confidence threat

- **Vulnerability alerts:**
  - CVSS + Orca Score + EPSS + Exposure + Data sensitivity
  - Exploit in wild = Critical regardless of CVSS
  - Public facing + High CVSS = Critical
  - Internal + No exploit = Medium/Low priority

- **Misconfiguration alerts:**
  - Compliance framework impact
  - Data exposure risk
  - Privilege escalation potential

### 5. Blast Radius Calculation

Query for:
```
1. Asset alert count (get_asset_alerts_count_grouped_by_risk_level)
2. Similar alerts (discovery_search with same alert type + timeframe)
3. Asset context (permissions, exposure, sensitive data)
4. Related assets (same vulnerability/misconfiguration pattern)
```

Format as:
```
BLAST RADIUS:
  • Affected Assets: X [type]
  • Alert History: Clean | N alerts | Targeted
  • Correlation: Isolated | Part of pattern (N similar alerts)
  • Environment: Production | Dev | Test
```

### 6. Verdict Generation

**Verdict Formula:**
```
IF severity = critical AND (exploit_available OR exposure = public) THEN
  "Active Threat"
ELSE IF anomaly AND single_occurrence AND same_tool_family THEN
  "Likely Benign"
ELSE IF vulnerability AND fix_available AND NOT exploited THEN
  "Patchable Risk"
ELSE IF status_changes > 3 AND duration > 7d THEN
  "Remediation Blocked"
ELSE
  "Requires Investigation"
```

**Confidence Calculation:**
```
Start: 50%
+ Same tool family (anomaly): +30%
+ Minor version bump: +20%
+ Clean baseline 30+ days: +15%
+ No correlation with suspicious activity: +15%
+ Single occurrence: +10%

OR

+ Known CVE with CVSS: +40%
+ Public exploit available: +30%
+ Verified by multiple sources: +20%

Cap at: 100%
Floor at: 30%
```

**Timeline Guidance:**
```
Severity    Public Facing    Exploited    Timeline
──────────────────────────────────────────────────
Critical    Yes             Yes          NOW (immediate)
Critical    Yes             No           4 hours
Critical    No              Yes          24 hours
High        Yes             -            48 hours
Medium      -               -            1 week
Low         -               -            2 weeks
Info        -               -            Review on close
```

## Follow-up Command Handlers

When user replies with keywords, provide the appropriate section:

### "investigate" / "investigation" / "how to investigate"

**Two-phase approach — gather data from Orca first, then suggest external actions only for gaps.**

**Phase 1: Automated investigation using Orca data (do this BEFORE showing anything to the user)**

Query Orca MCP tools to gather as much context as possible:

1. **Asset deep-dive** — use `get_asset_by_id` to get full asset details (permissions, exposure, tags, configuration)
2. **Alert correlation** — use `get_asset_alerts_count_grouped_by_risk_level` to see what else is firing on this asset
3. **Related alerts** — use `discovery_search` to find:
   - Other alerts on the same asset (e.g., same IAM user, same VM, same domain)
   - Similar alert types across the environment (e.g., all "MFA disabled" alerts, all "exposed tool" alerts)
   - Alerts in the same account/subscription in the same timeframe
4. **Cloud logs & runtime events** — if available via Orca, check:
   - CloudTrail events / Azure Activity Log / GCP Audit Log tied to the asset
   - Runtime events (process execution, network connections, file changes)
   - Login/authentication events for the identity
5. **Asset relationships** — check what the asset has access to, what connects to it, lateral movement paths

Synthesize all findings into a structured investigation report:

```
═══════════════════════════════════════════════════════════════════
INVESTIGATION REPORT — <alert-id>
<alert title>
═══════════════════════════════════════════════════════════════════

───────────────────────────────────────────────────────────────────
FINDINGS FROM ORCA DATA
───────────────────────────────────────────────────────────────────

ASSET CONTEXT:
  [Full asset details — permissions, exposure, config, relationships]

ALERT CORRELATION:
  [Other alerts on this asset — grouped by risk level]
  [Pattern: isolated finding vs. part of a cluster]

RELATED ACTIVITY:
  [Cloud logs, runtime events, login history from Orca]
  [Suspicious vs. expected activity]

VERDICT UPDATE:
  [Did investigation change the initial verdict? Why?]

───────────────────────────────────────────────────────────────────
GAPS — What Orca data could NOT answer
───────────────────────────────────────────────────────────────────

[Only if there are real gaps after Phase 1]

[ ] <specific action> — why it's needed, what to look for
    <runnable command or console URL>

ESCALATION CRITERIA:
  [When to escalate based on what was found AND what gaps remain]
═══════════════════════════════════════════════════════════════════
```

**Phase 2: External investigation steps (only for gaps)**

Only suggest manual commands or external tool queries when Orca data is insufficient. Examples of valid gaps:
- Orca doesn't have CloudTrail/audit logs for the specific timeframe
- Need to verify current state (is the issue still present right now?)
- Need data from systems Orca doesn't cover (email, Slack, ticketing details)
- Need to check external breach databases

When suggesting external steps, always:
- Explain WHY Orca data was insufficient for this specific check
- Provide runnable commands with actual values pre-filled from the alert
- Include what to look for in the output (not just "review the logs")

### "evidence" / "references" / "details"
Show EVIDENCE & REFERENCES:
- Alert metadata
- Anomaly context (baseline vs new values)
- Event IDs and evidence room links
- All relevant URLs (Orca, AWS Console, etc.)
- MITRE ATT&CK mapping if applicable

### "remediate" / "fix" / "patch"

**Two-step flow — always ask for format first, then generate output.**

**Step 1: Ask the user how they want the remediation delivered.**
Use AskUserQuestion to present format options. The available options depend on the alert's cloud provider and asset type:

| Option | When to offer | Description |
|--------|--------------|-------------|
| **Step-by-step instructions** | Always | Console walkthrough with manual steps |
| **Terraform** | Always (cloud resources) | HCL code to fix the misconfiguration or harden the resource |
| **CloudFormation** | AWS alerts only | CFN template (YAML) to remediate |
| **Azure Resource Manager (ARM)** | Azure alerts only | ARM/Bicep template to remediate |
| **Pulumi** | Always (cloud resources) | Pulumi code (TypeScript) to remediate |
| **CLI commands** | Always | Cloud CLI commands (aws/az/gcloud/cf) to run directly |

Only show options relevant to the alert's cloud provider. For example:
- Azure alert → offer: Instructions, Terraform, ARM/Bicep, CLI commands (az)
- AWS alert → offer: Instructions, Terraform, CloudFormation, CLI commands (aws)
- GCP alert → offer: Instructions, Terraform, CLI commands (gcloud)
- Cloudflare alert → offer: Instructions, Terraform, CLI commands (cf/curl)
- Multi-cloud / other → offer: Instructions, Terraform, CLI commands

**Step 2: Generate remediation in the selected format and write to file.**

After the user selects a format, generate the remediation and **always write code/template/script output to a file** using the Write tool. Use a sensible filename based on the alert ID and format:
- Terraform → `remediate-<alert-id>.tf`
- CloudFormation → `remediate-<alert-id>.cfn.yaml`
- ARM/Bicep → `remediate-<alert-id>.bicep`
- Pulumi → `remediate-<alert-id>.ts`
- CLI commands → `remediate-<alert-id>.sh`
- Step-by-step instructions → display inline (no file needed)

Write the file to the current working directory. After writing, show a summary of the remediation with the file path, and display the key sections (immediate actions, verification, prevent recurrence) inline. The user can then review and apply the file.

Structure the inline summary as:

```
═══════════════════════════════════════════════════════════════════
REMEDIATION — <alert-id> (<selected format>)
<alert title>
═══════════════════════════════════════════════════════════════════

IMMEDIATE ACTIONS:
  [blocking/isolation steps if critical]

FIX:
  [full remediation in the selected format — code block for IaC/CLI]

VERIFICATION:
  [commands to confirm the fix worked]

PREVENT RECURRENCE:
  [guardrails to avoid regression]
═══════════════════════════════════════════════════════════════════
```

For each format, the content should be:

**Step-by-step instructions**: Console walkthrough matching Orca's RemediationConsole field, enriched with context from the alert.

**Terraform**: Complete `.tf` snippet that remediates the finding. Include provider block, resource/data blocks, and comments explaining each setting. Use the alert's asset details (IDs, names, regions) to pre-fill values where possible.

**CloudFormation / ARM / Bicep**: Complete template with parameters, resources, and outputs. Pre-fill known values from the alert.

**Pulumi**: TypeScript Pulumi program with imports, resource definitions, and exports.

**CLI commands**: Runnable shell commands with actual values from the alert (asset names, IDs, regions). Include verification commands at the end.

Always include at the end:
```
VERIFICATION:
[ ] Run verification command(s) provided above
[ ] Wait for next Orca scan or trigger manual rescan
[ ] Confirm alert status changes to closed
```

### "correlate" / "related" / "similar"
Query and show:
```
discovery_search: <alert-type> in last 7 days
- Similar alerts: X found
- Pattern: Isolated | Widespread | Targeted
- Affected accounts: [list]
- Recommendation: [based on pattern]
```

## Error Handling

If MCP query fails:
```
⚠️  Unable to fetch alert data for <alert-id>

Possible reasons:
• Alert ID not found (check spelling: orca-XXXXXXX)
• MCP authentication expired
• Network connectivity issue

Try:
1. Verify alert ID in Orca UI
2. Check MCP status:
   - Claude Code: `claude mcp list`
   - Codex: `codex mcp list`
3. Re-authenticate if needed
```

## Best Practices

### DO:
✅ Start with verdict (decision first, details second)
✅ Use visual timeline with symbols (●, ├─, └─, ⚠️)
✅ Show clear next actions with timelines
✅ Provide runnable commands, not generic advice
✅ Highlight red flags prominently
✅ Progressive disclosure (offer investigation steps, don't force them)
✅ Calculate confidence level transparently

### DON'T:
❌ Dump all data at once
❌ Use excessive emojis (limit to critical indicators only)
❌ Include irrelevant details (asset creation date unless relevant)
❌ Provide generic recommendations ("review the logs")
❌ Skip the timeline (it shows critical behavioral patterns)
❌ Overuse technical jargon without context

## Example Outputs

### Low-Severity Anomaly (orca-3636513)

**Initial output**: 15-20 lines with verdict, timeline, what happened, why it matters
**User types**: "investigate"
**Follow-up**: Investigation checklist with CloudTrail queries
**Result**: Analyst closes alert in ~2 minutes

### Critical Vulnerability (orca-3548863)

**Initial output**: 25-30 lines with RED FLAGS section
**Automatic**: Show remediation urgency ("NOW")
**Timeline shows**: 39 days open, multiple status changes (friction indicator)
**User types**: "remediate"
**Follow-up**: Specific patching steps for Log4j
**Result**: Analyst escalates with full context

## Required MCP Tools

This skill requires the Orca Security MCP server. Below is the tested tool reference with correct parameter names and known issues.

### Verified Working Tools

| Tool | Parameters | Notes |
|------|-----------|-------|
| `get_alert` | `alert_id` (string, e.g. "orca-1234") | Primary alert data. Returns full alert with RiskFindings, ScoreVector, Inventory, AssetData. |
| `get_alert_timeline` | `alert_id` (string) | Returns `event_log` array with status changes, notifications, score overrides. |
| `get_asset_by_alert_id` | `alert_id` (string) | Get the asset tied to an alert. |
| `get_asset_by_id` | `asset_id` (UUID or asset_unique_id), optional `model_type` | Full asset details. Use the Inventory `id` field (UUID), NOT `asset_unique_id`. |
| `get_asset_by_name` | `asset_name` (substring), optional `model_type`, `name_match_limit` | Search by name substring. May return multiple results. |
| `get_asset_related_alerts_summary` | `asset_id` (UUID) | Top 50 alerts on this asset. **Key for investigation** — returns related alerts with RiskFindings including CloudTrail events. |
| `get_asset_related_attack_paths_summary` | `asset_id` (UUID) | Attack paths connected to the asset. |
| `get_asset_crown_jewel_info` | `group_unique_id` (string) | Check if asset is a crown jewel. Use the `GroupUniqueId` or `cluster_unique_id` from alert data. |
| `discovery_search` | `search_phrase` (natural language), optional `limit` (1-10) | Natural language search across Orca data. Use for finding similar alerts, related assets, etc. |

### Known Issues & Gotchas

1. **`get_asset_alerts_count_grouped_by_risk_level`**: Requires `asset_id` as a UUID. Using `asset_unique_id` format (e.g., "AwsUser_506464807365_...") causes a 400 error. Use the Inventory `id` field instead.
2. **`discovery_search`**: Parameter is `search_phrase`, NOT `query`. Uses natural language, not a query DSL.
3. **`get_asset_related_alerts_summary`**: This is the most valuable investigation tool — related alerts often contain CloudTrail events, runtime detections, and other context not in the primary alert.
4. **MCP connection**: If Orca MCP servers from `.mcp.json` are not loading, fall back to direct HTTP calls to `https://api.orcasecurity.io/mcp` using SSE protocol (`Accept: application/json, text/event-stream`). Parse the `data:` line from the SSE response.
5. **Asset ID types**: Alerts contain multiple ID formats. For MCP tool calls:
   - UUID (e.g., `c46cb523-3c5d-5bae-...`) → use with `get_asset_by_id`, `get_asset_related_alerts_summary`, `get_asset_related_attack_paths_summary`
   - `asset_unique_id` (e.g., `AwsUser_506464807365_...`) → do NOT use with asset tools expecting UUID
   - `GroupUniqueId` / `cluster_unique_id` → use with `get_asset_crown_jewel_info`

## Implementation Notes

1. **Cache timeline analysis** - Don't re-fetch on follow-up questions
2. **Format consistently** - Use the same symbols and structure across all alerts
3. **Validate alert ID format** - Must be "orca-XXXXXXX"
4. **Handle missing data gracefully** - Not all alerts have all fields
5. **Respect progressive disclosure** - Initial output max 30 lines
6. **Use current date** - Calculate age dynamically from today's date

## Success Metrics

A successful triage should enable the analyst to:
- ✅ Make close/investigate decision in < 60 seconds
- ✅ Understand behavioral context without deep diving
- ✅ Know exact next steps (not just "investigate")
- ✅ Identify remediation blockers from timeline
- ✅ Escalate with full context if needed
