---
name: sailpoint-stuck-requests
description: Diagnose and resolve stuck, waiting, or hung SailPoint access requests using the sail CLI. Use this skill whenever the user mentions a stuck access request, a pending request that won't complete, a hung provisioning phase, wants to cancel or force-close an access request, or asks about access requests in a waiting/executing state in SailPoint Identity Security Cloud. Also trigger when the user says things like "my request is stuck", "access request won't go through", "pending for days", or "can't see my request".
---

# SailPoint Stuck Access Requests

Diagnose and resolve access requests that are stuck in EXECUTING, PENDING, or otherwise non-completing states in SailPoint Identity Security Cloud.

## Prerequisites

- The `sail` CLI must be installed and configured
- The user needs appropriate admin permissions to view and manage access requests

## Workflow

### Step 1: Environment Selection

Before doing anything, show the user which environments are available and ask them to pick one. This matters because the wrong environment means operating on the wrong tenant.

```bash
sail environment list
sail environment show  # show current
```

Present the list and ask: "Which environment should I operate in?" Then switch:

```bash
sail environment use {name}
```

### Step 2: Discover Stuck Requests

Fetch all access request statuses and filter for stuck ones:

```bash
sail api get "/v2025/access-request-status"
```

The response is a JSON array. The CLI prefixes a log line (`INFO Making GET request...`) and suffixes a status line — strip both before parsing.

Filter for requests where:
- `state` is `EXECUTING` or `PENDING`
- Or any phase in `accessRequestPhases` has `state: "EXECUTING"` with `finished: null`

Present results as a summary table with: Name, Type, State, Requested For, Created date, Days waiting (calculated from `created` to today).

If no stuck requests are found, tell the user and stop.

### Step 3: Diagnose

For each stuck request (or the one the user picks), examine:

- **Error messages**: The `errorMessages` field — may contain provisioning errors, rule exceptions, or connector failures
- **Phases**: Check `accessRequestPhases` — which phase is stuck (APPROVAL vs PROVISIONING)
- **Cancelable flag**: The `cancelable` field determines which resolution path is available
- **Account info**: `requestedAccounts` shows the target source and account
- **Related requests**: Look for ERROR-state requests with the same `requestedFor` identity and access profile — these are often failed retries that confirm the original is stuck

Present the diagnosis clearly: what's stuck, where, why (if error messages exist), and how long.

### Step 4: Resolve

Always ask for user confirmation before taking action.

**Path A — Standard Cancel** (when `cancelable: true`):

```bash
sail api post "/v2025/access-requests/cancel" \
  --body '{"accountActivityId":"<accountActivityItemId>","comment":"<reason>"}'
```

**Path B — Force Close** (when `cancelable: false`):

The standard cancel endpoint will reject with "Invalid request in current state". Use the beta close endpoint instead:

```bash
sail api post "/beta/access-requests/close" \
  --body '{"accessRequestIds":["<accessRequestId>"],"message":"<reason>"}'
```

Note the field differences between the two endpoints — see `references/api-endpoints.md` for details.

**After resolution**: Report the result (job ID, status, any errors). Suggest the user refresh the admin UI to confirm, and remind them they can re-submit the access request if needed.

## Common Root Causes

When diagnosing, these are the patterns you'll see most often:

- **Hung provisioning with no error**: The connector timed out or lost connection — force-close is the only option
- **"IdentityRequest already exists"**: A retry was attempted while the original was still stuck — close the original first
- **Null identity / missing attributes**: The before-operation rule failed because identity data was incomplete
- **SQL syntax errors in GLPi**: Special characters in names broke the ticket creation query
- **"No configuration found for 'Remove Entitlement'"**: The connector doesn't have a remove operation configured
