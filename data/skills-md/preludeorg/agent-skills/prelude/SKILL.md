---
name: prelude
description: Operate the Prelude Security platform CLI for continuous security testing (Detect) and endpoint posture monitoring (SCM). Manages endpoints, schedules tests, evaluates security control policies, integrates with EDR/XDR partners, and generates reports. Use when working with the `prelude` CLI or managing security infrastructure.
license: MIT
metadata:
  author: prelude
  version: "1.0.0"
---

# Prelude P2D Platform CLI Skill

You are an expert operator of the Prelude platform CLI (`prelude`), which provides access to two distinct applications:

1. **Detect** - Continuous security testing: manage endpoints/probes, schedule and run security tests, view activity and results, manage threats and threat hunts
2. **SCM (Security Control Monitor)** - Endpoint posture and policy evaluation: query endpoints/users/inboxes, evaluate security control policies, manage exceptions, generate reports, monitor partner integrations

You help the user authenticate, explore both systems, query data, and perform operations across Detect and SCM.

## Prerequisites

- **CLI**: `prelude` v2.6+ (requires Python 3.10+)
- **Config file**: `~/.prelude/keychain.ini`
- **Token store**: `~/.prelude/tokens.json` (created after login)

## Getting Started

When a user invokes this skill and has not set up the CLI yet, walk them through this flow interactively. Do NOT dump all the steps at once. Guide them one step at a time.

### Step 1: Check if the CLI is installed and working

Run `prelude --version`. If it fails or is not found:
- The CLI requires Python 3.10+. Check `python3.10 --version`.
- Install with: `python3.10 -m pip install prelude-cli`
- If `prelude` in PATH points to an older Python, uninstall the old one and ensure the 3.10 version is first in PATH.

### Step 2: Check if a profile exists

Read `~/.prelude/keychain.ini`. A valid profile needs these fields:
```ini
[default]
hq = <api_url>
account = <account_id>
handle = <email>
```

If the file is missing, empty, or lacks `handle`, the profile needs to be configured.

### Step 3: Configure the profile

Since `prelude configure` is interactive and cannot be run non-interactively, write the keychain file directly. Collect the following from the user:

1. **Account ID** - Ask: "What is your Prelude account ID?" (a 32-character hex string)
2. **Email** - Ask: "What is the email address you use to log into Prelude?"
3. **OIDC provider** - Ask: "How do you log in?" Options: `google` (Google SSO), `custom` (custom OIDC), or `none` (password)
4. If OIDC is `custom`, also ask for the **account slug**

**Default to production (US1)**: `https://api.us1.preludesecurity.com`

Do NOT ask the user which environment they want. Assume production. Only if the user explicitly mentions a specific environment (e.g., "us2", "eu1", "staging") should you use a different API URL.

**Environment URLs** (only use when explicitly requested):

| Environment | API URL |
|-------------|---------|
| US1 (production) | `https://api.us1.preludesecurity.com` |
| US2 | `https://api.us2.preludesecurity.com` |
| EU1 | `https://api.eu1.preludesecurity.com` |

Write the keychain file:

```ini
[default]
hq = https://api.us1.preludesecurity.com
account = <account_id>
handle = <email>
```

Add `oidc = <provider>` only if not `none`. Add `slug = <slug>` only if OIDC is `custom`.

### Step 4: Login

The user must run `prelude auth login` in their terminal because it requires interactive input (password prompt or browser-based SSO).

- **Password auth** (`oidc = none`): Tell them to run `prelude auth login` and enter their password when prompted. They can also pass it directly: `prelude auth login -p "password"`
- **SSO auth** (`oidc = google` or `custom`): Tell them to run `prelude auth login`. This opens a browser for authentication and gives them a code to paste back.
- **First login with temporary password**: `prelude auth login -p "new_password" -t "temp_password"`

After login, tokens are saved to `~/.prelude/tokens.json` automatically.

### Step 5: Verify the connection

Run `prelude iam account` to confirm everything works. This returns account details including users, controls, features, and mode.

### Multiple profiles

Users can maintain multiple profiles (e.g., different accounts or environments):

```ini
[default]
hq = https://api.us1.preludesecurity.com
account = <account_id_1>
handle = <email>

[staging]
hq = https://api.us2.preludesecurity.com
account = <account_id_2>
handle = <email>
```

Switch profiles with: `prelude --profile staging <command>`

## Global Options

```bash
prelude --version              # Show CLI version
prelude --profile <name>       # Use a specific keychain profile
prelude --resolve_enums        # Show enum names instead of integer codes
prelude --help                 # Show available commands
```

**Tip**: Always use `--resolve_enums` when you want human-readable output (control names instead of codes, status names instead of numbers).

## System Architecture

The P2D platform has 9 command domains:

| Domain | Purpose |
|--------|---------|
| `auth` | Login (password/SSO), token refresh |
| `configure` | Set up local keychain profiles |
| `iam` | Account management, users, permissions, OIDC, audit logs |
| `detect` | Endpoint management, test scheduling, activity queries, threat hunts |
| `build` | Create/update security tests, threats, detections, threat hunt queries |
| `partner` | Attach/manage EDR integrations (CrowdStrike, Defender, etc.), deploy probes |
| `scm` | Security Control Monitor - endpoints/users/inboxes posture, policy evaluation, exceptions, reports |
| `generate` | AI-powered test generation from threat intel PDFs and partner advisories |
| `jobs` | Monitor background jobs (SCM sync, probe deployment, exports) |

## Key Concepts

### Controls (Security Partners)
Integer-coded partner integrations. Important codes:

| Code | Name | Category |
|------|------|----------|
| 1 | CrowdStrike | XDR |
| 2 | Microsoft Defender | XDR |
| 3 | Splunk | SIEM |
| 4 | SentinelOne | XDR |
| 7 | Intune | Asset Manager |
| 8 | ServiceNow | Asset Manager |
| 9 | Okta | Identity |
| 10 | Microsoft 365 | Email |
| 11 | Entra | Identity |
| 12 | Jamf | Asset Manager |
| 13 | CrowdStrike Identity | Identity |
| 14 | Gmail | Email |
| 17 | Tenable | Vuln Manager |
| 23 | Qualys | Vuln Manager |
| 25 | Rapid7 | Vuln Manager |
| 29 | Cisco Meraki | Network/SASE |
| 33 | Netskope | SASE |

### Control Categories

| Code | Name |
|------|------|
| 1 | Cloud |
| 2 | Email |
| 3 | Identity |
| 4 | Network |
| 5 | XDR (EDR) |
| 6 | Asset Manager |
| 7 | Discovered Devices |
| 8 | Vuln Manager |
| 9 | SIEM |
| 10 | Private Repo |
| 11 | Hardware |
| 12 | SASE |

### Run Codes (Scheduling)

| Code | Name |
|------|------|
| 1 | DAILY |
| 2 | WEEKLY |
| 3 | MONTHLY |
| 4 | SMART |
| 5 | DEBUG |
| 6 | RUN_ONCE |
| 10-16 | MONDAY-SUNDAY |

### Exit Codes (Test Results)

| Code | Meaning | State |
|------|---------|-------|
| 100 | PROTECTED | Protected |
| 137 | BLOCKED | Protected |
| 126 | EXECUTION_PREVENTED | Protected |
| 101 | UNPROTECTED | Unprotected |
| 102 | TIMED_OUT | Error |
| 104 | TEST_NOT_RELEVANT | Not Relevant |
| -1 | MISSING | None |

### Account Modes

| Code | Name | Behavior |
|------|------|----------|
| 0 | MANUAL | Tests only run when explicitly scheduled |
| 1 | FROZEN | No tests run |
| 2 | AUTOPILOT | Tests run automatically |

### Permissions

| Code | Role |
|------|------|
| 0 | ADMIN |
| 1 | EXECUTIVE |
| 2 | BUILD |
| 3 | SERVICE |
| 5 | SUPPORT |
| 6 | SCHEDULER |

---

## Command Reference

### AUTH - Authentication

```bash
# Login with password
prelude auth login -p "password"

# Login with temporary password (first login), sets new password
prelude auth login -p "new_password" -t "temp_password"

# Login with SSO (opens browser for OIDC flow)
prelude auth login

# Refresh access tokens
prelude auth refresh
```

### CONFIGURE - Keychain Setup

```bash
prelude configure
# Interactive prompts for: profile, API URL, account ID, email, OIDC provider
```

### IAM - Account & User Management

```bash
# Get account details (shows users, controls, queue, features, mode)
prelude iam account

# Update account settings
prelude iam update-account --company "Acme Corp"
prelude iam update-account --mode AUTOPILOT    # MANUAL, FROZEN, AUTOPILOT
prelude iam update-account --slug "acme"
prelude iam update-account --inactivity_timeout 90

# Invite a user
prelude iam invite-user -e "user@example.com" --oidc google -p ADMIN
# Permissions: ADMIN, EXECUTIVE, BUILD, SCHEDULER

# Create service user (for API/automation)
prelude iam create-service-user -n "CI Bot"
# Returns: handle + token (save the token!)

# Delete service user
prelude iam delete-service-user -h "service_handle"

# Update user permissions
prelude iam update-account-user -e "user@example.com" -p BUILD --oidc google

# Remove user
prelude iam remove-user -e "user@example.com" --oidc google

# OIDC management
prelude iam attach-oidc --client_id "xxx" --client_secret "xxx" --issuer google --oidc_url "https://..."
prelude iam detach-oidc

# Audit logs
prelude iam logs                  # Last 7 days, 1000 limit
prelude iam logs -d 30 -l 500    # Last 30 days, 500 results

# Delete account (DESTRUCTIVE)
prelude iam purge-account

# User-level commands
prelude iam user accounts              # List all accounts you belong to
prelude iam user update-user -n "Name" # Update your display name
prelude iam user forgot-password       # Send password reset email
prelude iam user confirm-forgot-password -c "code" -p "newpass"
prelude iam user change-password       # Change password (prompts for current/new)
prelude iam user purge-user            # Delete your user everywhere (DESTRUCTIVE)
```

### DETECT - Endpoints, Tests, Scheduling & Activity

```bash
# --- Endpoints ---
prelude detect endpoints                 # List endpoints (default: active in last 90 days)
prelude detect endpoints -d 30           # Active in last 30 days
prelude detect create-endpoint -h "hostname" -s "serial123" -r "<account_id>/<service_token>"
prelude detect create-endpoint -h "hostname" -s "serial123" -r "<account_id>/<service_token>" -t "tag1,tag2"
prelude detect update-endpoint <endpoint_id> -t "new_tag1,new_tag2"
prelude detect delete-endpoint <endpoint_id>

# --- Tests ---
prelude detect tests                     # List all security tests
prelude detect tests --techniques "T1059,T1053"  # Filter by MITRE techniques
prelude detect test <test_id>            # Get test details + attachments
prelude detect download <test_id>        # Download test files locally
prelude detect clone                     # Download ALL tests locally

# --- Threats ---
prelude detect threats                   # List all threats
prelude detect threat <threat_id>        # Get threat details

# --- Techniques ---
prelude detect techniques                # List all MITRE ATT&CK techniques

# --- Detections ---
prelude detect detections                # List all detection rules
prelude detect detection <detection_id>  # Get detection details
prelude detect detection <detection_id> -o rule.yaml  # Export Sigma rule to file

# --- Threat Hunts ---
prelude detect threat-hunts              # List all threat hunts
prelude detect threat-hunts --tests "test1,test2"  # Filter by tests
prelude detect threat-hunt <hunt_id>     # Get hunt details
prelude detect do-threat-hunt <hunt_id>  # Execute a threat hunt query

# --- Scheduling ---
prelude detect queue                     # Show active test queue
prelude detect schedule <id> -t TEST                          # Schedule test (daily)
prelude detect schedule <id> -t TEST -r WEEKLY                # Schedule weekly
prelude detect schedule <id> -t TEST -r SMART --tags "prod"   # Smart schedule for tagged endpoints
prelude detect schedule <id> -t THREAT -r DAILY               # Schedule a threat
prelude detect unschedule <id> -t TEST                        # Remove from queue
prelude detect unschedule <id> -t THREAT --tags "prod"        # Remove for specific tags

# --- Activity & Reporting ---
prelude detect activity                  # Default: logs view, last 29 days

# Views: logs, tests, threats, endpoints, techniques, findings, metrics, protected
prelude detect activity --view tests
prelude detect activity --view endpoints
prelude detect activity --view protected
prelude detect activity --view findings
prelude detect activity --view metrics
prelude detect activity --view threats
prelude detect activity --view techniques

# Filters
prelude detect activity --view logs --start "2024-01-01" --finish "2024-01-31"
prelude detect activity --view tests --control CROWDSTRIKE
prelude detect activity --view logs --tests "test1,test2"
prelude detect activity --view logs --threats "threat1"
prelude detect activity --view logs --endpoints "ep1,ep2"
prelude detect activity --view logs --dos "windows-x86_64"
prelude detect activity --view logs --statuses "100,101"
prelude detect activity --view logs --os "Windows 11"
prelude detect activity --view logs --policy "Default"
prelude detect activity --view protected --social   # Social (cross-account) stats

# Threat hunt activity
prelude detect threat-hunt-activity <id> -t THREAT_HUNT
prelude detect threat-hunt-activity <id> -t TEST
prelude detect threat-hunt-activity <id> -t THREAT
```

### BUILD - Create & Manage Security Tests

```bash
# --- Tests ---
prelude build create-test -n "My Test" --unit "go" --technique "T1059.001"
prelude build create-test -n "My Test" --unit "go" --test_id <custom_uuid>
prelude build clone-test <source_test_id>
prelude build update-test <test_id> -n "New Name"
prelude build update-test <test_id> --technique "T1059.001"
prelude build update-test <test_id> --expected_crowdstrike PREVENT  # OBSERVE, DETECT, PREVENT
prelude build delete-test <test_id>          # Soft delete (tombstone)
prelude build delete-test <test_id> --purge  # Permanent delete
prelude build undelete-test <test_id>        # Restore tombstoned test

# Upload test attachment
prelude build upload <test_id> -p /path/to/file.go
prelude build upload <test_id> -p /path/to/file.go --compile  # Upload and compile
prelude build compile-code-file -p /path/to/file.go           # Test compilation only

# --- Threats ---
prelude build create-threat <directory>      # Create from directory containing test files
prelude build create-threat <directory> -n "Threat Name" --published "2024-01-01"
prelude build update-threat <threat_id> -n "Updated Name"
prelude build delete-threat <threat_id>
prelude build delete-threat <threat_id> --purge
prelude build undelete-threat <threat_id>

# --- Detection Rules (Sigma) ---
prelude build create-detection <test_id> -r /path/to/rule.yaml
prelude build update-detection <detection_id> -r /path/to/rule.yaml
prelude build delete-detection <detection_id>

# --- Threat Hunt Queries ---
prelude build create-threat-hunt <test_id> --name "Hunt Name" --query "query_string" --control CROWDSTRIKE
prelude build update-threat-hunt <hunt_id> --name "New Name" --query "new_query"
prelude build delete-threat-hunt <hunt_id>
```

### PARTNER - EDR & Security Partner Integration

```bash
# Attach a partner (connect your security tool)
prelude partner attach CROWDSTRIKE -u "client_id" --secret "client_secret" --api "https://api.crowdstrike.com"
prelude partner attach DEFENDER -u "client_id" --secret "client_secret" --api "https://graph.microsoft.com"
prelude partner attach OKTA -u "api_token" --api "https://your-org.okta.com"
prelude partner attach <PARTNER> -u "user" --secret "secret" --api "url" -i "instance_id" -n "Friendly Name"

# Detach partner
prelude partner detach <PARTNER> -i "instance_id"

# List endpoints from a partner
prelude partner endpoints <PARTNER> --platform windows         # windows, linux, darwin
prelude partner endpoints CROWDSTRIKE --platform windows --hostname "web*"
prelude partner endpoints DEFENDER --platform linux --offset 0 --count 100

# Deploy probes to partner hosts
prelude partner deploy CROWDSTRIKE --host_ids "id1,id2"

# Block a test (deploy detection rule to partner)
prelude partner block <test_id> -p CROWDSTRIKE

# Get partner reports
prelude partner reports CROWDSTRIKE -t <test_id>

# Get observed/detected statistics
prelude partner observed-detected
prelude partner observed-detected -t <test_id> --lookback 48

# List partner advisories
prelude partner advisories CROWDSTRIKE
prelude partner advisories CROWDSTRIKE --start "2024-01-01" --offset 0 --limit 50

# List partner groups
prelude partner groups <PARTNER> -i "instance_id"
```

### SCM - Security Control Monitor

```bash
# --- Query Resources (OData-powered) ---
prelude scm endpoints                                    # List all SCM endpoints
prelude scm endpoints --odata_filter "hostname eq 'web01'"
prelude scm endpoints --odata_filter "controls/any(c: c eq 1)"  # Has CrowdStrike
prelude scm endpoints --top 50 --skip 0 --order_by "hostname asc"
prelude scm users                                        # List all SCM users
prelude scm users --odata_filter "email eq 'user@example.com'"
prelude scm inboxes                                      # List all SCM inboxes
prelude scm network_devices                              # List network devices

# --- Policy Evaluation ---
prelude scm evaluation-summary                           # Summary across all partners
prelude scm evaluation CROWDSTRIKE -i "instance_id"      # Detailed evaluation for partner
prelude scm technique-summary --techniques "T1059,T1053" # Policy summary per technique
prelude scm sync CROWDSTRIKE -i "instance_id"            # Trigger policy sync

# --- Export ---
prelude scm export ENDPOINT                              # Export endpoints CSV
prelude scm export USER                                  # Export users CSV
prelude scm export INBOX                                 # Export inboxes CSV
prelude scm export ENDPOINT --odata_filter "hostname eq 'web01'"

# --- Exceptions ---
# Object exceptions (exclude resources from monitoring)
prelude scm exception object list
prelude scm exception object create <CATEGORY> -f "hostname eq 'test*'" -n "Test Exception" -c "Excluding test hosts"
prelude scm exception object update <exception_id> -f "new filter" -n "Updated Name"
prelude scm exception object delete <exception_id>

# Policy exceptions (exclude specific policy settings)
prelude scm exception policy list
prelude scm exception policy create <PARTNER> -i "instance_id" -p "policy_id" -s "setting1,setting2" -c "Exception reason"
prelude scm exception policy update <PARTNER> -i "instance_id" -p "policy_id" -s "setting1,setting2"
prelude scm exception policy delete <PARTNER> -i "instance_id" -p "policy_id"

# --- Threats ---
prelude scm threat list
prelude scm threat get <threat_id>
prelude scm threat create -n "Threat Name" --techniques "T1059,T1053"
prelude scm threat delete <threat_id>

# --- Groups ---
prelude scm group list <PARTNER> -i "instance_id"
prelude scm group sync <PARTNER> -i "instance_id" --group_ids "id1,id2"

# --- Notifications ---
prelude scm notification list
prelude scm notification delete <notification_id>
prelude scm notification upsert <CATEGORY> -v <EVENT> -r <RUN_CODE> -s <HOUR> -e "email1,email2"

# --- Reports ---
prelude scm report list
prelude scm report get <report_id>
prelude scm report put --report_file /path/to/report.json
prelude scm report put --report_data '{"name":"Report",...}'
prelude scm report put --report_id <id> --report_file /path/to/report.json  # Update
prelude scm report delete <report_id>
prelude scm report chart-data <SCM_CATEGORY> -b "group_field" -s count_desc -l 100

# --- History & Notations ---
prelude scm history
prelude scm history --start "2024-01-01" --end "2024-06-01"
prelude scm history --odata_filter "some filter"
prelude scm notations

# --- Threat Intel ---
prelude scm threat-intel -f /path/to/report.pdf          # Parse threat intel from PDF
prelude scm from-advisory <PARTNER> --advisory_id "id"    # Generate from partner advisory
```

### GENERATE - AI-Powered Test Generation

```bash
# Upload threat intel PDF for automated test generation
prelude generate threat-intel -f /path/to/report.pdf
prelude generate threat-intel -f /path/to/report.pdf --force_ai  # Force AI regeneration

# Generate from partner advisory
prelude generate from-advisory CROWDSTRIKE --advisory_id "CS-2024-001"
prelude generate from-advisory CROWDSTRIKE --advisory_id "CS-2024-001" --force_ai
```

### JOBS - Background Job Monitoring

```bash
# List all background jobs
prelude jobs background-jobs

# Get specific job status
prelude jobs background-job <job_id>
```

Job types: UPDATE_SCM, DEPLOY_PROBE, OBSERVED_DETECTED, PRELUDE_ENDPOINT_SYNC, EXPORT_SCM, PARTNER_GROUPS

---

## Common Workflows

### Quick Health Check
```bash
prelude iam account                      # Verify connection, see account features
prelude detect endpoints                 # See active endpoints
prelude detect queue                     # See scheduled tests
prelude detect activity --view protected # See protection status
```

### Investigate Endpoint Posture
```bash
prelude scm endpoints --odata_filter "hostname eq 'target-host'"
prelude scm evaluation-summary
prelude scm evaluation CROWDSTRIKE -i "instance_id"
```

### Review Test Results
```bash
prelude detect activity --view logs --start "2024-01-01" --finish "2024-01-31"
prelude detect activity --view tests --control CROWDSTRIKE
prelude detect activity --view findings
```

### Set Up Continuous Testing
```bash
prelude detect tests                                     # Browse available tests
prelude detect schedule <test_id> -t TEST -r DAILY       # Schedule daily
prelude detect queue                                     # Verify it's queued
prelude detect activity --view logs                      # Check results later
```

### Partner Integration
```bash
prelude partner attach CROWDSTRIKE -u "client_id" --secret "secret" --api "https://api.crowdstrike.com"
prelude partner endpoints CROWDSTRIKE --platform windows
prelude partner deploy CROWDSTRIKE --host_ids "host1,host2"
prelude partner observed-detected
```

---

## Naming Differences: CLI vs Platform UI

Some CLI terms differ from what appears in the web platform:

| CLI Term | Platform UI Term | Notes |
|----------|-----------------|-------|
| `endpoint` / `probe` | Endpoint | Interchangeable in CLI |
| `control` | Partner / Integration | Integer codes map to partner names |
| `dos` | Platform | e.g., `windows-x86_64`, `darwin-arm64` |
| `queue` | Schedule | Active test scheduling |
| `activity` | Results / Reports | Test execution results |
| `scm` | Monitor | Security Control Monitor |
| `technique` | MITRE Technique | ATT&CK framework reference |
| `threat` | Threat | Collection of related tests |
| `detection` | Detection Rule | Sigma YAML rules |
| `threat-hunt` | Threat Hunt | Partner-specific hunting queries |

## Error Handling

- **401 Unauthorized**: Run `prelude auth login` or `prelude auth refresh`
- **"Please make sure you are using an up-to-date profile"**: Run `prelude configure` and ensure `handle` field is set
- **Python version error** (`str | None` unsupported): CLI requires Python 3.10+. Use `/opt/homebrew/bin/prelude`
- **Connection errors**: Check `hq` URL in `~/.prelude/keychain.ini`

## Tips

- Use `--resolve_enums` to see human-readable names: `prelude --resolve_enums detect endpoints`
- Pipe JSON output to `jq` for filtering: `prelude detect tests 2>/dev/null | jq '.[] | .name'`
- The CLI outputs JSON by default - great for scripting and automation
- Service users (created via `iam create-service-user`) are ideal for CI/CD and automation
- OData filters in SCM commands support complex queries: `contains()`, `eq`, `ne`, `and`, `or`, `any()`, `all()`
