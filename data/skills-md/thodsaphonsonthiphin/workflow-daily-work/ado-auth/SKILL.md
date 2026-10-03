---
name: ado-auth
description: >-
  Authenticate to Azure DevOps and fix auth problems — the shared primitive every
  other ado-* skill relies on. Use this BEFORE any create/query when ADO auth setup
  is uncertain, and whenever an ADO call misbehaves: a REST call returns 401 or 403,
  "az not logged in" / token expired, results come back from the wrong org or empty,
  or you hit "A potentially dangerous Request.Path value was detected (:)". Covers the
  two supported methods (Entra token via `az`, or AZDO_PAT), a one-line PowerShell
  verify snippet against the projects API, and a 401/403/wrong-org troubleshooting
  table. Invoke when someone says "I'm getting a 401 from Azure DevOps", "create-backlog
  says it can't get a token", "ado auth failing", or "check my ADO login before we run".
effort: max
---

# ado-auth

Authenticate to Azure DevOps (ADO) and diagnose auth failures. This is a **verify and
troubleshoot** skill — the bundled `create-backlog.cs` already implements both auth
methods, so you are not writing new auth code here. You are confirming a token works
and the org/project point where the user expects, then unblocking the create/query
skills ([[ado-create-work-items]], the orchestrator [[findings-to-ado-backlog]]).

ADO accepts two credential styles. Pick A unless the user has a reason to use a PAT.

## Method A — Entra token via Azure CLI (recommended)

Why preferred: no long-lived secret to store, and it rides the user's existing `az`
session. The resource id below is the **global Azure DevOps application id** (same for
every tenant) — it tells Entra "mint a token for Azure DevOps".

```powershell
az login
$token = az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv
```

Use it as a bearer header: `Authorization: Bearer <token>`.

## Method B — Personal Access Token (PAT)

Use when `az login` isn't available (e.g. a service context) or the user already has a
PAT. Scope must include **Work Items (Read & Write)**. ADO PATs go in a *Basic* header
where the username is empty and the password is the PAT:

```powershell
$env:AZDO_PAT = "<your-pat>"
$basic = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$env:AZDO_PAT"))
# header -> Authorization: Basic <basic>
```

`create-backlog.cs` reads `AZDO_PAT` automatically: if it's set it uses Basic auth,
otherwise it shells out to `az` for an Entra token. So setting (or unsetting)
`AZDO_PAT` is how you switch methods for that script — you don't pass a flag.

## Verify the credential works

Run this before kicking off a real create. A `200` against the project endpoint proves
the token is valid **and** that the user can see the target org/project — the two things
most auth failures actually break. Set `AZDO_ORG` to the org **name only** (not a URL):

```powershell
$env:AZDO_ORG     = "Cartagena365"   # the NAME, not https://dev.azure.com/...
$env:AZDO_PROJECT = "GlassHull"
$token = az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv
$uri = "https://dev.azure.com/$($env:AZDO_ORG)/_apis/projects/$($env:AZDO_PROJECT)?api-version=7.1"
Invoke-RestMethod -Uri $uri -Headers @{ Authorization = "Bearer $token" }
```

PAT variant — swap the header for:
`@{ Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$env:AZDO_PAT")))" }`

A `200` returns the project's JSON (id, name, state). Anything else, see below.

For a broader prereq sweep (az, .NET 10, python/openpyxl, env vars) run the bundled
checker instead — it's read-only and changes nothing:

```powershell
powershell -ExecutionPolicy Bypass -File "${CLAUDE_SKILL_DIR}/scripts/setup_check.ps1"
```

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| **HTTP 401** Unauthorized | No token, or it expired | `az login`, then re-fetch the token (Entra tokens are short-lived — re-run the `get-access-token` line). For PAT: check it hasn't expired/been revoked. |
| **HTTP 403** Forbidden | Token is valid but lacks rights | PAT scope missing **Work Items (Read & Write)** — reissue with that scope. For Entra: the account lacks board/project permission — get added to the project / area path. |
| **"A potentially dangerous Request.Path value was detected (:)"** | `AZDO_ORG` was set to a full URL (e.g. `https://dev.azure.com/Cartagena365`) instead of the bare org name. The `:` from `https:` lands inside the request path. | Set `AZDO_ORG` to the **org name only**: `$env:AZDO_ORG = "Cartagena365"`. |
| **200 but wrong / empty results** | Token is fine; you're pointed at the wrong place | Check `AZDO_ORG` / `AZDO_PROJECT` — confirm the project name's exact casing, and that this org actually contains it (the verify call's JSON is the source of truth). |
| **"could not start az" / "failed to get Entra token"** | Azure CLI not installed or no active login | Install Azure CLI (https://aka.ms/installazurecli), run `az login`, retry. Or fall back to Method B (`AZDO_PAT`). |

## Hand-off

Once the verify call returns `200`, auth is good — continue with
[[ado-create-work-items]] (which drives `create-backlog.cs`) or
[[ado-writeback-tracking]]. The same `AZDO_ORG` / `AZDO_PROJECT` env vars carry
straight into those steps, so leave them set in this shell. Field shapes and the
`org`/`project` precedence rules live in `references/data-contracts.md`.
