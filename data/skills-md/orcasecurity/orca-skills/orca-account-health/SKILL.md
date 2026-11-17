---
name: orca-account-health
description: Cloud account coverage and sync-health audit — lists every connected cloud account, sync status, scanner deployment, integration health, and flags blind spots before any audit, investigation, or security review. Use when user asks about coverage, account health, sync status, scanner deployment, "are we monitoring X", or "do we have full coverage" (e.g., "account health", "are all accounts connected", "is everything synced", "coverage audit").
trigger: When user asks about Orca tenant coverage, account connectivity, integration status, scanner deployment, sync freshness, or wants confidence the data behind an investigation/audit is complete and recent. Also pre-audit ("prove we have full coverage") and pre-investigation ("is the data fresh?").
---

# Orca Account Health Skill

Answers the question: **"Is every account connected, recently synced, and fully scanned — so we can trust the data we're about to act on?"**

Blind spots in account coverage produce blind spots in every other skill: if `prod-eu-west` last synced 48 hours ago, the alerts you triage are stale. This skill audits the foundation.

## Usage

```
/orca-account-health
/orca-account-health aws
/orca-account-health degraded
```

Or natural language:
- "are all accounts connected?"
- "is everything synced?"
- "coverage audit before the audit"
- "any blind spots?"
- "show me account health"

## Processing Logic

### Step 1: Determine Scope

Parse the input:
- **No arg**: full inventory across all clouds.
- **Provider arg** (`aws`, `gcp`, `azure`, `kubernetes`, `oci`): filter to one cloud.
- **Status arg** (`degraded`, `offline`, `healthy`): filter by health.

### Step 2: Pull integration configs (single call)

```
get_integration_configs_data:
```

This returns every configured integration / source: cloud accounts, log sources (CloudTrail, Azure Monitor, etc.), Kubernetes clusters, and their extraction settings. Parse out:
- Source type and provider
- Connection state
- Last successful run / sync timestamp
- Any error messages or degraded indicators

### Step 3: Cross-check coverage with discovery (parallel)

In parallel with Step 2, run two `discovery_search` queries to spot-check that data is *actually* flowing — not just that the connection exists:

**Query A: Asset freshness per account**
```
discovery_search:
  search_phrase: "assets grouped by cloud account"
  limit: 50
```

**Query B: Recent CDR event flow** (confirms log ingestion, not just inventory)
```
discovery_search:
  search_phrase: "cloud audit events in the last 24 hours grouped by account"
  limit: 50
```

If an account appears in `get_integration_configs_data` but returns **zero assets** or **zero recent CDR events**, that's a covert blind spot even though the integration reports "connected."

### Step 4: Compute per-account health

For each account, derive a health verdict:

| State | Definition |
|---|---|
| **Healthy** | Connected, synced in last 24h, scanner deployed, ≥1 recent CDR event |
| **Sync Lag** | Connected, last sync 24–72h ago, scanner deployed |
| **Stale** | Connected, last sync > 72h ago |
| **Degraded** | Connection error reported, OR scanner missing, OR no CDR events in 72h |
| **Offline** | Never synced, OR connection broken |
| **Recently Added** | Onboarded in the last 7 days (verify onboarding finished) |

### Step 5: Detect specific blind-spot patterns

Flag these patterns explicitly — they're the ones that bite during audits or investigations:

1. **Account is connected but produces no assets** → onboarding likely incomplete.
2. **Account is connected, has assets, but no CDR events in 24h** → audit log integration broken (CloudTrail / Azure Monitor / GCP Audit Logs misrouted).
3. **Scanner deployed but stuck on a stale scan** → SideScanning or workload scanner needs restart.
4. **New account added < 7 days ago, no successful sync yet** → onboarding incomplete or failed silently.
5. **Provider drift** — account listed in one cloud's console but missing from Orca.

## Proactive Behavior

**This skill is diagnostic, not remediation-heavy** — but it should still surface the next step:

1. **Identify the worst blind spot** and recommend a specific fix:
   - "Reconnect `prod-eu-west` — last sync 48h ago, no CDR events. Open Orca Console → Cloud Accounts → Reconnect."
2. **For onboarding failures**, link to the docs:
   - `/orca-account-health` should reference `documentation_search` for "onboarding troubleshooting" if user asks "how do I fix it".
3. **Pre-audit framing**: if the user said "before the audit", explicitly say whether they can proceed or need to wait for re-sync.

## Output Format

### Layer 1: Coverage Dashboard

```
═══════════════════════════════════════════════════════════════════
ACCOUNT HEALTH — Cloud Coverage Audit
<date> | <scope>
═══════════════════════════════════════════════════════════════════

VERDICT: <one-liner — "Full coverage, all green" / "1 offline, 2 sync lag, action needed">

┌─────────────────────────────────────────────────────────────────┐
│  TOTAL ACCOUNTS    <N>                                          │
│  HEALTHY           <N>                                          │
│  SYNC LAG          <N> (24-72h since last sync)                 │
│  STALE             <N> (> 72h since last sync)                  │
│  DEGRADED          <N> (errors / scanner gap / no CDR)          │
│  OFFLINE           <N> (broken / never synced)                  │
│  RECENTLY ADDED    <N> (onboarded < 7d, verify completion)      │
│  BLIND SPOTS       <N> (connected but no data flowing)          │
└─────────────────────────────────────────────────────────────────┘

ACCOUNT STATUS:
  Account              Provider   Last Sync     Scanner   CDR    Status
  ────────────────────────────────────────────────────────────────────────
  <account-1>          AWS        2 min ago     YES       OK     Healthy
  <account-2>          AWS        26 hours ago  YES       OK     Sync Lag
  <account-3>          Azure      Never         NO        —      Offline
  <account-4>          GCP        2h ago        YES       NO     Degraded
  ...

BLIND SPOTS (immediate attention):
  [!] <account> — <specific issue>
      Impact: <what's invisible because of this gap>
      Fix: <specific action>

  [!] <account> — ...

RECOMMENDED ACTION:
  Reconnect <account> first — <reason>.
  After reconnect, re-run any pending investigation or audit.

═══════════════════════════════════════════════════════════════════
Or drill down: degraded | offline | sync-lag | recently-added |
by-provider | full
═══════════════════════════════════════════════════════════════════
```

### Layer 2: Drill-Downs

#### "degraded" — Accounts with active problems

```
───────────────────────────────────────────────────────────────────
DEGRADED ACCOUNTS — Active Issues
───────────────────────────────────────────────────────────────────

  [!] <account> (<provider>)
      Connection: <state>
      Last sync: <time>
      Scanner: <deployed / missing / stuck>
      CDR ingestion: <events in 24h or "none">
      Error: <reported error message>
      Impact: <what's invisible — e.g. "any investigation in this
              account is missing the last 6h of CDR data">
      Fix: <specific action — link to documentation_search if needed>

  [!] <account> — ...

───────────────────────────────────────────────────────────────────
```

#### "offline" — Broken or never-synced accounts

```
───────────────────────────────────────────────────────────────────
OFFLINE ACCOUNTS
───────────────────────────────────────────────────────────────────

These accounts are configured but Orca has no data:

  [X] <account> (<provider>)
      Last successful sync: <date or NEVER>
      Connection error: <message>
      Likely cause: <inferred — e.g. revoked role, deleted trust policy>
      Fix path: <action>

───────────────────────────────────────────────────────────────────
```

#### "sync-lag" — Accounts behind on sync

```
───────────────────────────────────────────────────────────────────
SYNC LAG — 24-72h Behind
───────────────────────────────────────────────────────────────────

  <account> (<provider>) — last sync <time> ago
    Why it matters: <e.g. "alerts triaged here may be missing the
                    last day of activity">

  ...

If urgency is high (audit, investigation), force a re-sync:
  Orca Console → Cloud Accounts → <account> → Sync Now
───────────────────────────────────────────────────────────────────
```

#### "recently-added" — New accounts (verify onboarding)

```
───────────────────────────────────────────────────────────────────
RECENTLY ADDED ACCOUNTS — Verify Onboarding
───────────────────────────────────────────────────────────────────

  <account> (<provider>) — added <N> days ago
    First sync: <success / pending / failed>
    Assets discovered: <N>
    Scanner deployed: <Y/N>
    CDR ingestion: <active / pending>
    Onboarding status: <complete / pending / failed>

───────────────────────────────────────────────────────────────────
```

#### "by-provider" — Coverage split by cloud

```
───────────────────────────────────────────────────────────────────
COVERAGE BY PROVIDER
───────────────────────────────────────────────────────────────────

  Provider     Connected   Healthy   Issues
  ───────────────────────────────────────────
  AWS          <N>         <N>       <N>
  Azure        <N>         <N>       <N>
  GCP          <N>         <N>       <N>
  Kubernetes   <N>         <N>       <N>
  OCI          <N>         <N>       <N>

───────────────────────────────────────────────────────────────────
```

#### "full"
Show all sections in order.

## Edge Cases

### No Accounts Configured
```
⚠ No cloud accounts configured in Orca.

To get started:
  Orca Console → Cloud Accounts → Add Account
  Choose: AWS / Azure / GCP / Kubernetes / OCI

After onboarding, re-run /orca-account-health to verify coverage.
```

### All Accounts Healthy
```
✅ All <N> accounts healthy.

  • All connections active
  • All accounts synced within the last hour
  • All scanners deployed
  • CDR ingestion active across all accounts

You're clear to proceed with audit / investigation / review.
```

### Coverage Mismatch (account in cloud console but not in Orca)
```
⚠ Provider-side accounts NOT in Orca:

This skill can only see what's configured in Orca. If your AWS Org has
30 accounts but Orca has 25, the other 5 are invisible here.

To verify completeness:
  • Compare Orca account list against AWS Organizations / Azure Tenants /
    GCP Organization root.
  • Use /orca-account-health to confirm Orca's view; cross-check
    externally for accounts that never made it to Orca.
```

### "Connected but Empty"
```
⚠ <account> reports "connected" but Orca has zero assets and zero events.

This is the worst kind of blind spot — the integration looks healthy in
the dashboard but no data is actually flowing.

Likely causes:
  • IAM role attached but policy missing read permissions
  • Cross-account trust set up but external ID mismatch
  • Newly added account, scan not yet started
  • Region scope of the integration excludes the account's resources

Fix path:
  Orca Console → Cloud Accounts → <account> → Verify Permissions
```

## MCP Tools Used

### Primary Tools

| Tool | Purpose | Parameter |
|------|---------|-----------|
| `get_integration_configs_data` | All connected sources, state, last sync | (none) |
| `discovery_search` | Cross-check assets and CDR flow per account | `search_phrase` (NL), `limit` |

### Secondary Tools

| Tool | Purpose | When |
|------|---------|------|
| `get_cdr_events_grouped_by_event_name` | Deeper CDR ingestion check | When `discovery_search` says "no CDR events" — confirm |
| `documentation_search` | Onboarding/troubleshooting docs | When user asks "how do I fix it" |
| `get_business_units_data` | Map accounts to ownership for assignment | When user wants to route fixes to a team |

### Parameter Notes

- `get_integration_configs_data` takes **no parameters** — it's a full dump of configured sources. Filter client-side.
- `discovery_search` for `"cloud audit events in the last 24 hours grouped by account"` is the best signal that audit log ingestion is actually working — connection state alone is insufficient.
- `discovery_search` is capped at 50 results; for tenants with many accounts, narrow with `"... in account <id>"`.

## Implementation Notes

1. **Two-source verification is the differentiator.** `get_integration_configs_data` alone says "connected"; the discovery cross-check says "data is actually flowing." A "connected but empty" account is the worst blind spot and only the cross-check catches it.
2. **Categorize the freshness, don't dump timestamps.** Users need "Healthy / Sync Lag / Stale / Degraded / Offline" buckets, not raw "last_sync_at" values.
3. **Always state the impact of each gap.** Don't say "prod-eu-west has sync lag" — say "any alert triage in prod-eu-west is missing the last day's data". Connect the gap to the next action.
4. **Pre-audit / pre-investigation framing matters.** If the user invoked this before another skill ("before /orca-investigate"), end with an explicit "you can proceed" or "wait for re-sync" verdict.
5. **External coverage drift** (accounts in AWS Org but not in Orca) is out of scope for this skill — flag it in the edge case and recommend manual cross-check rather than pretend the MCP can detect it.
6. **Link to other skills**: this skill is a prerequisite for trusting the output of `/orca-morning-briefing`, `/orca-investigate`, `/orca-compliance-gap`, and `/orca-cve-blast-radius`. Mention this when appropriate.
