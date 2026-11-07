---
name: push-inventory-collector
description: >-
  Generate one customer-hosted collector script that lists agents, MCP servers,
  or REST APIs, uploads each asset ZIP with POST /push, then finishes with POST
  /commit. TRIGGER when: the user asks to push inventory, generate a push
  script, How to Push, self-managed scanner, or download the collector skill.
  Trigger phrases include "push inventory", "generate a push script", "How to
  Push", "self-managed scanner", "collector skill", "POST /push", "POST /commit".
  DO NOT TRIGGER when: creating a pull scanner (skill setup-service-scanner) or
  running a hosted scan (skill run-service-scan-and-view-results).
license: Apache-2.0
compatibility: Requires a coding agent that can write files, plus the language the customer names at runtime.
allowed-tools: Bash Read Write Edit AskUserQuestion
metadata:
  author: ms-phoenix
  version: "1.0.0"
---

# Push inventory collector

Generate one collector script for one self-managed scanner configuration. Do not assume a cloud vendor, a programming language, or a credential shape until the customer provides them. The script is the pull-scanner connection form on their machine, in the language they name. It reads their APIs, builds one payload per asset, uploads each payload, and then commits the scan. The scanner reconciles and publishes. The script does not publish by itself.

There is no universal provider credential set. There is no schedule on this scanner. Do not add a schedule, a last-run time, or a "run discovery" step.

## When to Use This Skill

**Use this skill when the user asks to:**

- Generate a collector script for a self-managed scanner
- How to Push, download the collector skill, or push inventory
- Write a script that calls POST /push then POST /commit

**Trigger keywords:** push inventory, push script, How to Push, self-managed scanner, collector skill, POST /push, POST /commit.

**Do NOT use this skill when:** creating a pull scanner that discovers from a connected cloud platform — use skill setup-service-scanner. Running a hosted scan and reviewing staging assets — use skill run-service-scan-and-view-results.

## Prerequisites

- Organization id and scanner configuration id copied from the self-managed scanner page
- A Connected App with client-credentials grant and `manage:exchange` on that organization
- The provider API specification they can paste or attach (OpenAPI, Postman, or a redacted request and response)
- Authentication documentation for those APIs, without secret values
- A language they can run on their machine

## Reference files

- **`references/scanner-contract.md`** — ZIP layout, POST /push multipart, POST /commit body. Read it before writing the upload and commit functions.
- **`references/generated-script-standard.md`** — runtime inputs, stderr stages, JSON stdout, mapping fingerprint. Read it when writing the script.
- **`references/provider-auth-resolution.md`** — one question per turn, managed-only auth, new-provider contract. Read it when choosing operations and credential fields.


## Workflow

### Rules that always apply

1. **Customer-facing words** — use the table below in every question, in `--help`, in the FAILED block, and in **Ways to run the script**. A wrong verb here is a generation failure.
2. **One question per response** — never combine asset type, inventory, auth, or language.
3. **Never ask for a provider name** — infer the provider from a usable spec. On an unreadable or incomplete spec, ask only the missing list, fetch, handshake, export, or auth piece.
4. **Never reorder** — skip a step only when this chat already answered it with usable data. Ask a step again when the previous answer was unreadable, the wrong kind of file, or missing a required piece.
5. **Do not create a scanner during generation** — do not log in, do not call Anypoint CLI, do not mint a token to discover an organization. Organization id and configuration id are values copied from the scanner page into the inputs file or the parameters.

Use these words. Do not hard-code a vendor, a non-production host, or a loopback address into a question or an example host. The example host is `https://anypoint.mulesoft.com`.

| Say | Do not say |
|---|---|
| script | adapter, collector, product command |
| input file, parameters, or prompts | three CLIs, CLI mode |
| self-managed scanner | self-serve, self-service, build your own |
| commit the scan | seal, seal the zip, complete and publish, publish to Exchange |

The upload call is `POST .../push`. The finish call is `POST .../commit`. The question is exactly: "Commit this scan? [y/N]". A generated script that calls `POST .../seal`, `POST .../complete`, or `POST .../push-assets` is a generation failure. The JSON body still has a boolean field named `complete`. That field is not the customer sentence.

Examples of an inventory (OpenAPI, a Postman collection, a redacted request and response) show the shape. They are not a menu and not a default. Language examples are not a fixed list. Do not default to one language.

A script that creates a configuration, calls `anypoint-cli`, or calls `GET /accounts/api/me` in order to invent an organization id is a generation failure. That auto-fill is later work. It is not this script.

The only customer questions in this chat are the quoted sentences in Steps 1–5, the missing-piece follow-ups, "Does this look fine?", and the generated script's "Commit this scan? [y/N]". Do not ask which provider.

### Step 1: Ask asset type

When the asset type is not already explicit, the whole message is:

"What asset type does this scanner configuration accept? Reply with one of: agent, mcp, or rest-api.

agent is one agent card. mcp is one MCP server card. rest-api is one API description. One script commits one of these, to one configuration."

Then stop.

Explicit means they wrote `agent`, `mcp`, or `rest-api`, or a harmless alias (`agents` → `agent`, `api` / `REST APIs` / `APIs` → `rest-api`, `MCP` / `MCP servers` → `mcp`). A provider name, a file name, or an operation name is not an asset type. Do not infer the asset type from a single-type contract. Inferring the type so generation can jump ahead is a generation failure.

### Step 2: Collect inventory

Once the type is known, the whole next message is:

"Please provide the API specification or documentation for the provider APIs that list and fetch these assets. OpenAPI or Swagger, a Postman or Insomnia collection, RAML, an API Blueprint, a GraphQL schema, an SDK reference, or a redacted request and response are examples, not required formats."

Then stop. Do not ask which provider. Infer the provider from a usable spec. Do not invent calls. Do not fetch a spec they did not provide. The catalog later in this file is a shape reminder for a matching paste, not a substitute.

Read what they attached. Then stop if it is not yet usable. Ask only the missing piece. One question per response.

- Unreadable, empty, unrelated, or not a spec or redacted request and response. Whole message: "This attachment is not a usable specification for listing and fetching these assets. Please attach or paste a valid API spec or a redacted request and response that includes those APIs."
- No list API for the type they named. Whole message: "This specification does not include an API that lists {agent|mcp|rest-api} assets. Please attach or paste that list API."
- Agent list with no fetch or card API. Whole message: "This specification lists assets but does not include the fetch or card API needed to build the agent zip. Please attach or paste that call."
- MCP list with no `initialize` / `tools/list` (or the equivalent handshake). Whole message: "This specification does not include initialize and tools/list (or the equivalent handshake) needed to build an MCP card. Please attach or paste those calls."
- REST list with no export or OpenAPI download. Whole message: "This specification does not include the export or OpenAPI download needed to build a REST zip. Please attach or paste that call."

A usable inventory has the list call plus the fetch, card, handshake, or export that type needs. Only then ask authentication. Vertex MCP, Gemini MCP, Gemini agents, Azure AI Foundry MCP, and Microsoft 365 Copilot with no customer list docs are enum-only: ask for a customer list call, or stop. If they ask which file to use, they only have this skill and the files they attach; do not name a path from this package.

### Step 3: Collect authentication

Once the inventory is usable, the whole next message is:

"Please provide the authentication documentation needed to call those APIs. Include the token or signing request, the response, which field is a secret, and how a call is proven to be the right account. Do not paste secret values."

Then stop. A long-lived secret, a session token, and a private key are never typed into this chat. They belong in the inputs file or in the environment when the script runs.

If that document is missing a piece, ask only that piece. Whole message, fill one gap: "The authentication documentation is missing {the token or signing request|the response|which field is a secret|how a call is proven to be the right account}. Please add that piece. Do not paste secret values." Do not proceed to language until those four are present.

Use the authentication document they pasted. Do not open a catalog file from this skill. When they describe Salesforce connected-org (C2C) login or a MuleSoft-managed authorization-code flow, that is not customer-executable: ask for a request and response they can run from their machine. Until they provide one, do not write files. A pasted SigV4 access-key flow still uses the request and response they pasted. Do not copy pull-scanner-only fields such as Hub Role ARN, Spoke Role Name, External ID, Account IDs, or Target Regions into the script.

### Step 4: Ask script language

Once auth is known, the whole next message is:

"Which script language should I use? Project conventions are optional. Any language you can run is acceptable. Named languages are examples, not a fixed list."

Then stop. Do not default to a language. Writing a file before they answer is a failure. If they name a language and omit conventions, write a plain script in that language.

Default script stderr the customer sees: the numbered step banner only when that step runs; after a successful list `listed N, matching M, skipped K`; then one line per **matching** asset (`type`, external id, display name); `No matching {ASSET_TYPE} assets found.` when M is 0; FAILED for real failures. Do not print skip ids, `skipping MCP`, or `not MCP` unless `--verbose`.

### Step 5: Show the mapping

**[GATE] WAIT for an explicit yes to "Does this look fine?" before writing files.**

When type, inventory, auth, and language are known, do not write files in that turn. Show the mapping in this order, then stop. Do not treat dumping the script as having shown the mapping.

1. What was collected, in plain English: the list and detail calls, the auth field names (not values), the language, and the one asset type.
2. One row per inventory call. Columns: Call, Request, Response field, Zip path.
3. One row per field the zip will contain. Columns: Source, Sent as, Required. Source is the operation and response path, or `constant`. If a required Source cannot be pointed at, leave the row blank and ask only for that API or field. Do not guess. If any required Source is blank, stop here. Do not show items 4–8 and do not ask "Does this look fine?" until every required Source is filled.
4. One Representative generated JSON object for a single asset, using values from their inventory when they gave an example, otherwise empty strings. For `agent`, every required A2A v0.3 field has a row (`name`, `description`, `protocolVersion`, `url`, `version`, `capabilities`, `defaultInputModes`, `defaultOutputModes`, `skills`). A v1 card uses `supportedInterfaces` or `supported_interfaces` and has no top-level `url`. The artifact is `a2a-card.json` or `a2a-v1-card.json`. For `mcp`, `specification/mcp-metadata.json` with `transport` required; if capabilities are included, include all four booleans `tools`, `resources`, `prompts`, and `logging`; do not add `serverInfo`. For `rest-api`, `specification/oas.json` with `info` and `paths`; `externalId` is the provider id, and one stage is one asset.
5. How the zip is uploaded after they run the script: `POST {ANYPOINT_BASE}/agent-scanner/api/v1/organizations/{org}/scanner-configurations/{config}/push` is the zip as multipart part `file`, filename `{externalId}.zip`. Not JSON. Finish is a separate `POST .../commit`. The customer question is "Commit this scan? [y/N]". Do not name `/push-assets`, `/complete`, or `/seal`.
6. Script architecture: the function names to write (provider login, list, shape zip, token, upload, optional commit, print status) and the numbered stderr steps below.
7. Flags, environment variables, prompts, and which of those are secret. Same names as **The script**. `--help` three columns: Prompt label, Parameter flag, Input file key.
8. Ask exactly: "Does this look fine?"

Do not show Prerequisites or Ways to run the script in this turn. Those come after the files exist. Showing them before they say yes is a generation failure.

If they say no, ask which row is wrong, fix the table, and ask again. Still do not write files. If they say yes, write the two files. After the files exist, show Prerequisites, then Ways to run the script in this order: interactive, parameters, input file, and the full `inputs.env` as a fenced block named `inputs.env` so they can download it. Do not ask "Does this look fine?" after writing.

That yes is the only approval. The script is not written until they say yes, so a run does not ask them to approve the mapping again and does not refuse live because a fingerprint is pending. Record the approved rows as `MAPPING_FINGERPRINT`: canonical JSON, UTF-8, keys sorted, `{"assetType":"...","rows":[{"source":"...","sentAs":"...","required":true}]}`, rows in the order shown, SHA-256 hex. That value is a record of the chat yes. It is not a second question.

Classify with the check described in their inventory. Do not classify by display name. A list that returns more than one kind of asset still yields only the type they named. The other kinds are skipped. A shared AgentCore `ListAgentRuntimes` is not permission to zip both agents and MCP. Agent script: skip `protocolConfiguration.serverProtocol=MCP`, then `GetAgentCard` or the documented synthesized card. MCP script: SigV4 JSON-RPC `initialize`, then `tools/list`; null `initialize` = skip. Name is never classification. REST script lists API Gateway (or their REST inventory), not AgentCore runtimes. A skip is a count, not a default log line: increment `skipped` and continue. Do not print `skipped {id}`, `skipping MCP`, or `not MCP` on stderr unless `--verbose` is set. `--verbose` may print `skipped {id} <reason>`. FAILED still prints (list/page errors, HTTP 401/403, missing required zip fields, upload refusals).

AgentCore MCP handshake URL is not the Exchange card field `transport.path` (`/mcp`). The invoke URL is `https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{urlencoded agentRuntimeArn}/invocations?qualifier={endpointName}`. `agentRuntimeArn` comes from `get-agent-runtime` / the list item. Encode it with `urllib.parse.quote(arn, safe="")` (every `:`, `/`, and extra character). `endpointName` is `list-agent-runtime-endpoints` `runtimeEndpoints[0].name`, usually `DEFAULT`. No endpoint name means skip that runtime. `Accept` is `application/json, text/event-stream`. Parse JSON or SSE `data:` lines. `initialize` params are `protocolVersion` `2025-03-26`, `capabilities` `{}`, `clientInfo`. HTTP 401/403 on initialize is FAILED. HTTP 400/404/405/415/422 or a missing `result` object is skip. A generated script that POSTs `/runtimes/{agentRuntimeId}/invocations/mcp`, uses the unencoded runtime id in the path, or omits `?qualifier=` is a generation failure. A default run that prints `skipped {id}` for every non-matching runtime is a generation failure.

### Step 6: Write the two files

Two files, in the language they named. No markdown guide. The chat already showed the mapping. Prerequisites and Ways to run come after these files exist.

1. The script. One run lists the assets, checks each matching object, uploads each matching one, and then either commits the scan or stops. Zero matching assets stop after list/shape: no MuleSoft login. The asset type is a source constant (`ASSET_TYPE`). The script does not accept `--asset-type`, `SCANNER_ASSET_TYPE`, or an environment variable that switches type.
2. An inputs file, `inputs.env`, written to disk beside the script and shown again as a fenced block named `inputs.env` so the customer can download it. The block contains the whole file. A chat that only prints the command `--input-file inputs.env` is a generation failure. Every secret value is empty. Non-secret placeholders are obvious fakes, never a real id from this chat. Mark each line `(required)` or `(optional)` in a comment.

Do not write a pipeline, a container, a schedule, or a second library.

`inputs.env` always contains these MuleSoft lines, then the provider keys from the auth they described:

```
# (required) Anypoint host. Example: https://anypoint.mulesoft.com
ANYPOINT_BASE=
# (required) Organization id, copied from the scanner page
ANYPOINT_ORG_ID=
# (required) Scanner configuration id, copied from the scanner page
SCANNER_CONFIGURATION_ID=
# (required) Connected App client id
ANYPOINT_CLIENT_ID=
# (required) Connected App client secret. Leave empty in chat. Fill this on the machine that runs the script.
ANYPOINT_CLIENT_SECRET=
# (optional) Commit the scan without a prompt. yes or no. Default no.
PUSH_COMMIT=
```

Append one line per provider credential the script will actually ask for, with `(required)` or `(optional)`. Do not copy a credential set from a different provider. A session token, a private key, or any other long secret is `(required)` only when their auth document says the call fails without it.

When that document offers more than one credential source, ask which one before the mapping. The script uses only that source. It does not fall back to another. An attached role or a named profile is allowed when they select it. Do not demand an access key for that choice. An unattended run names the source in the inputs file. It does not guess from leftover environment variables. For AWS that line is `AWS_AUTH_MODE` with one of `profile`, `default-chain`, or `access-keys`.

The rest of this file is the script contract. Read **The script**, **One input mode**, **ZIP and push**, and `references/scanner-contract.md` before writing. Read `references/generated-script-standard.md` for stderr, JSON stdout, and the mapping fingerprint. Read `references/provider-auth-resolution.md` for managed-only auth.

### Step 7: Verify generation and show how to run

After the two files exist, show Prerequisites, then **Ways to run the script** in this order: interactive, parameters, input file, and the full `inputs.env` as a fenced block named `inputs.env` so they can download it. Do not ask "Does this look fine?" after writing.

Run the language checker in **Same job, any language** on the generated file. Search for forbidden patterns (`json=` or `"Content-Type": "application/json"` on `/push`, `POST .../seal`, `POST .../complete`, `--client-secret`, `args.[a-z]+-`). If the checker cannot run here, search the file for those patterns. Do not declare completion until the file parses in the named language and those searches are clean.

## Connected App

The script logs in to Anypoint with one Connected App: client id and client secret, grant `client_credentials`. It never asks for an Anypoint username or password.

An Organization Administrator creates the app once, in Access Management, before they run the script. The script cannot create it.

1. Access Management → Connected Apps → Create App.
2. Type: App acts on its own behalf (client credentials).
3. Add scope `manage:exchange` and apply it to this organization. A token without that scope is rejected.
4. Save. Copy the client id. Store the client secret as `ANYPOINT_CLIENT_SECRET`. Do not paste it into this chat.

The self-managed types are offered only when `push-scanner-enabled` is on and the entitlement matches: `agent` for agents, `apiScanners` for MCP and REST. If upload returns that the type is absent, stop and say so. Do not invent an id.

Token request, in every language: `POST {ANYPOINT_BASE}/accounts/api/v2/oauth2/token` with `Content-Type: application/x-www-form-urlencoded` and body `grant_type=client_credentials&client_id=...&client_secret=...`. Never JSON.

## What the script does

Inside that one run the script prints a numbered step banner on stderr only when that step runs, then stops. Do not split them across programs. Do not print a later banner after the run has stopped.

```
── Step 1: provider login
── Step 2: list assets
── Step 3: shape zips
── Step 4: MuleSoft login
── Step 5: publish
── Step 6: commit
```

`--dry-run` stops after step 3. There is no MuleSoft login and no secret prompt. That skip is success.

After step 3, if zero assets matched `ASSET_TYPE`:
- Print `No matching {ASSET_TYPE} assets found.` on stderr (`agent`, `mcp`, or `rest-api`).
- Print the JSON object on stdout (`ok` true, that type's count `0`, `skipped` for classified-away and handshake skips, empty publish ids).
- Exit 0.
- Do not print Step 4, 5, or 6. Do not prompt for the Connected App secret. Do not call `/push` or `/commit`.
- `--dry-run` uses this same stop.
- Live exception only: `PUSH_ALLOW_EMPTY=yes` continues to `GET .../workspace` and the empty-commit path in step 5.

1. Read inputs. See **One input mode**.
2. Call their list and detail APIs with their auth. Follow pages until the list ends or a page cap is hit. If the list call itself fails, exit 2 and do not commit. After a successful list, print one summary line: `listed N, matching M, skipped K`. Do not print one line per skipped id unless `--verbose`.
3. For each matching asset, build the object from the mapping they accepted. If a required field is missing, print FAILED and do not upload that object. An invalid object is the script's fault. Print each matching asset on its own line: type, external id, display name. Print the zip path `{id}/specification/config.json` plus the artifact. A zip that uses `{id}/config.json` (no `specification/`) is a generation failure.
4. Upload each valid ZIP with `POST {ANYPOINT_BASE}/agent-scanner/api/v1/organizations/{org}/scanner-configurations/{config}/push`. The body is the zip bytes, not JSON. `Content-Type` is `multipart/form-data` with exactly one part named `file`, filename `{externalId}.zip`, part `Content-Type: application/zip`. HTTP 202 JSON is `{assetId, action, workspaceRunId}`. Keep that `workspaceRunId`. Every later upload in this run must return the same id. The server checks the zip again. A refusal is FAILED, with the response body. The same provider id replaces the staged object. It does not create a second row, and Exchange is not called. An id uploaded earlier and absent from this list stays staged until `DELETE .../push/{externalId}`. Omission is not deletion. HTTP 415 means this POST was not a zip part named `file` (JSON body, `application/x-www-form-urlencoded`, `Content-Type: multipart/form-data` with no boundary, or a boundary that starts with `=`). A generated script that posts JSON to `/push`, uses `json=`, sets `Content-Type: application/json` on `/push`, or names the part anything other than `file` is a generation failure.
5. Close the workspace and declare completeness separately. `workspaceRunId` comes only from a 202 `/push` (or `GET .../workspace` when `PUSH_ALLOW_EMPTY=yes` and nothing was uploaded). Inventing `run-…` or posting `/commit` without that id is a generation failure. Zero accepted uploads: do not call `/commit`.
   - The list stopped at a page cap, or any upload failed, and at least one upload was accepted: `POST .../commit` with `{"workspaceRunId":"<id from 202>","complete":false}`. Do not ask. `complete:false` is upsert only. It must not be `true`.
   - The list finished and every upload succeeded: ask on a TTY, "Commit this scan? [y/N]". The default is no. `--commit` or `PUSH_COMMIT=yes` is the yes when there is no TTY. Yes sends `POST .../commit` with `"complete":true`. No uploads and does not commit.
   - An empty successful list does not commit unless they also set `PUSH_ALLOW_EMPTY=yes`.
6. Print one JSON object on stdout: counts, `truncated`, `workspaceRunId`, `scanRunId`, and whether the scan was committed. Exit 0 when nothing failed. Exit 2 when a list, an upload, or a requested commit failed.

`complete: true` means this list is the full inventory, so the scanner may retire assets that were not in the list. `complete: false` means upsert only.

The upload is one ZIP per asset because that is the API. The customer confirms the mapping and the sample JSON. Do not spend the chat on archive layout. The script still produces a valid ZIP: one directory whose name is the provider's stable id, `specification/config.json` with `name` and `type`, and the artifact next to it (`a2a-card.json` or `a2a-v1-card.json`, `mcp-metadata.json`, or `oas.json`).

Live stderr after MuleSoft values resolve (non-secrets in full; secret presence only):

```
Anypoint host: https://anypoint.mulesoft.com
Anypoint Organization ID: …
Scanner Configuration ID: …
Connected App Client ID: …
Connected App Client Secret: set
```

Ask only the missing ones. `--dry-run` must not prompt for those Anypoint rows.

## One input mode

One run uses one value source. Control flags do not pick a source and do not block prompts. Control flags are `--help`, `--dry-run`, `--verbose`, and `--commit`. Provider fields come from the authentication document they pasted, minus pull-scanner-only hub/spoke fields. AWS, Azure, GCP, Databricks, Snowflake, Kong, and a provider that is not in the catalog use that same rule. Do not copy an AWS field onto another provider.

Inside the chosen source, every field uses this fill order. A variable already in the shell fills the value. It does not switch the source, and a blank prompt must not erase it.

1. Command flag already set → use it. Do not prompt.
2. Else the environment variable.
3. Else the `--input-file` / `PUSH_INPUT_FILE` key, when that source is the input file.
4. Else a TTY prompt in this same process. Hide a secret. An empty answer keeps step 2.
5. Else, not a TTY → `FAILED` naming the missing input.

Three ways to supply values. They are OR.

1. **Input file.** `--input-file` or `PUSH_INPUT_FILE` is set. Every required value, including secrets, is in that file. A missing required key is FAILED. `--dry-run` and `--commit` may be added. They do not switch the run to parameters mode.
2. **Parameters.** A value flag is on the command line, and no input file is set. Value flags are `--anypoint-base`, `--org`, `--config`, `--client-id`, then only that provider's flags. AWS adds `--profile` and `--region` / `--aws-region`. Azure and GCP do not get `--profile`. Secrets are environment variables, never flags. A missing required value is FAILED. No prompt.
3. **Prompts.** No input file and no value flag, and stdin is a TTY. `--dry-run` alone is this mode. Ask only for a label that is still empty after the environment. A secret already in the environment is not asked again.

`--dry-run` does not call the scanner. It does not require the Anypoint host, organization id, configuration id, client id, or client secret. It still needs the provider credentials that list the assets.

No file, no value flag, and no TTY → FAILED naming the missing input.

## Pull-form provider login

Step 1 looks like the Exchange connection form for **that** provider, not a cloud-CLI tutorial. Derive prompts from the authentication document they pasted. If a current pull form matches that provider, use that credential class's `@Field(label=...)` for the fields the script actually asks. Do not copy an AWS, Azure, or Kong field set onto a different provider. Do not send any of these values to MuleSoft. The push configuration is `authScheme=customer-upload` with no `authParameters`.

| Pull scanner form (UI label) | Script prompt | Secret? |
|---|---|---|
| AWS Access Key ID | `AWS Access Key ID` | no |
| AWS Secret Access Key | `AWS Secret Access Key` | yes |
| AWS Session Token | hidden, only when the access key is `ASIA` after stripping quotes and the token is not already in the environment or the input file | yes |
| AWS Region | `AWS Region` | no |
| Tenant ID / Client ID / Client Secret (Azure) | same labels | secret last |
| Subscription ID (Azure APIM) | same label | no |
| Personal Access Token (Kong) | same label | yes |
| GCP Project ID / Service Account Email / Private Key | same labels | private key yes |
| Workspace URL + client id/secret (Databricks) | same labels | secret yes |

Do not prompt Hub Role ARN, Spoke Role Name, External ID, Account IDs, or Target Regions. Those names exist on the pull scanner form. This script does not assume a role. A `--help` row labeled Hub Role ARN, Spoke Role Name, External ID, Account IDs, or Target Regions is a generation failure.

## Already logged in

The laptop CLI/SDK session is the default. Access keys, client secrets, and private keys are the other branch.

- **AWS.** `~/.aws/config` / `~/.aws/credentials` already work. `--help` must have the row `AWS Profile | --profile | AWS_PROFILE`. `--profile NAME` uses that profile and does not ask for Access Key, Secret, or Session Token. `--profile` / `AWS_PROFILE` wins over leftover `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` in the environment. Do not tell them to `export AWS_PROFILE`. On a TTY, **AWS Access Key ID** first. Blank, and `--profile` / `AWS_PROFILE` already set: do not ask Secret. Blank, and no profile yet: prompt **AWS Profile** (empty = default chain already on this machine), then **AWS Region** only. Non-TTY: `--profile`, `AWS_AUTH_MODE=default-chain`, or access keys. Blank Access Key with none of those is FAILED; do not silently call STS on leftover environment credentials or a default chain they did not choose. An AWS `--help` that lists Access Key and Region but never `--profile` / `AWS_PROFILE` is a generation failure.
- **Azure.** `az` is already logged in. Use that session (DefaultAzureCredential / `az account`). Do not add `--profile`. Do not prompt Tenant ID, Client ID, or Client Secret unless they pasted those as the auth document they will actually use.
- **GCP.** `gcloud` is already logged in (ADC). Use that session. Do not add `--profile`. Do not prompt Service Account Email or Private Key unless they pasted the service-account JSON as the auth they will actually use.
- **Kong, Databricks, Snowflake, Claude, LangSmith.** No analog of `aws/config`. Use that provider's token fields. Do not invent `--profile`.

`--profile` is AWS only. A `--help` row `--profile` on Azure, GCP, Kong, or Databricks is a generation failure.

## AWS login

AWS asks for one login, then the region. Nothing else. Order on a TTY: **AWS Access Key ID**, then either the already-logged-in profile path above, or **AWS Secret Access Key** (hidden) when the key is non-empty, then **AWS Session Token** (hidden) only when the unquoted key starts with `ASIA` and the token is not already set, then **AWS Region**. Skipping Access Key ID and jumping to Secret is a generation failure.

- Access keys: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` from the flag/env/file/prompt. Strip wrapping quotes, including `“”‘’`, **before** an `ASIA` check. A check on the raw prompt string is a generation failure. Pass the unquoted key, secret, and token into boto3 together. Do not leave a leftover `AWS_SESSION_TOKEN` in the process environment. If the key is `ASIA` and the token is still empty, `FAILED` names `AWS_SESSION_TOKEN` before any AWS call.
- Region: `--region` / `--aws-region` / `AWS_REGION`. One region. Do not ask for a second region list.

`--help` provider rows for AWS are only `--profile`, the access-key pair (secret has no flag), and `--region` / `--aws-region`.

Required unquote (or the same behavior in the language they named):

```python
def _unquote_aws(value):
    text = (value or "").strip()
    marks = "\"'" + "\u201c\u201d\u2018\u2019"
    while len(text) >= 2 and text[0] in marks and text[-1] in marks:
        text = text[1:-1].strip()
    return text
```

ASIA check is `_unquote_aws(ack).upper().startswith("ASIA")`. After writing, search the script for `startswith("ASIA")` applied to the raw prompt string. Any such match is a generation failure.

AWS inventory paths such as `/ListAgentRuntimes` are boto3 operation names. They are not URLs. Call `boto3.client("bedrock-agentcore-control").list_agent_runtimes` and `boto3.client("bedrock-agentcore").get_agent_card`. A handwritten SigV4 request, a POST to `https://bedrock-agentcore-control.../ListAgentRuntimes`, or `Content-Type: application/x-amz-json-1.1` without the AWS SDK is a generation failure. The 403 body `Unable to determine service/operation name to be authorized` means that mistake.

`--region us-east-1 --profile scanner` must reach STS as region `us-east-1` and profile `scanner`. Do not prompt AWS Secret Access Key when Access Key ID is blank and `--profile` is set. Nested Bash `${CLI_REGION:-${AWS_REGION:-x}}}}` is a generation failure (`us-east-1}`). Sequential assignments only. After writing a `.sh`, search for `}}}}` and `--region ${`.

## The script

Flags, same spelling in every language: `--dry-run`, `--input-file`, `--anypoint-base`, `--org`, `--config`, `--client-id`, `--commit`, `--verbose`, `--help`. There is no `--asset-type` and no `--client-secret`. `--profile` is AWS only. `--region` / `--aws-region` is only when that provider uses a region. Other provider flags come from their auth document.

`--help` exits 0 and shows three columns for every input, in this order of ways to supply it: Prompt label, Parameter flag, Input file key. Connected App fields first, then the already-logged-in row for that cloud if it has one (`AWS Profile` / `az` / `gcloud`), then the fields from their auth document. The client secret has no flag. Help explains `--dry-run` and `--commit`. A `--help` that lists `--client-id` but never mentions **Connected App Client Secret** or `ANYPOINT_CLIENT_SECRET` is a generation failure. Copy this into argparse `epilog` / usage:

```
Inputs and where to obtain them:
  --anypoint-base / ANYPOINT_BASE: Anypoint host. Scanner path is that host plus /agent-scanner.
    Example US production: https://anypoint.mulesoft.com
  --org / ANYPOINT_ORG_ID: organization id from the Exchange scanner page
  --config / SCANNER_CONFIGURATION_ID: configuration id from that same page
  --client-id / ANYPOINT_CLIENT_ID: Connected App Client ID
  Connected App Client Secret: ANYPOINT_CLIENT_SECRET, matching --input-file key, or hidden
    prompt labeled "Connected App Client Secret". Never a process argument. No --client-secret.
AWS scripts also:
  --profile / AWS_PROFILE: AWS Profile. Already logged in via ~/.aws/config. Wins over leftover
    AWS_ACCESS_KEY_ID. Not an Azure or GCP flag.
  AWS Access Key ID: AWS_ACCESS_KEY_ID or prompt. Blank uses --profile / the default chain.
  AWS Secret Access Key: AWS_SECRET_ACCESS_KEY or hidden prompt. No flag. Skip when Access Key
    is blank and --profile or the default chain is in use.
  --region / --aws-region / AWS_REGION: AWS Region
Azure scripts: az already logged in (DefaultAzureCredential). Do not add --profile.
GCP scripts: gcloud already logged in (ADC). Do not add --profile.
```

Python argparse dests use underscores (`args.anypoint_base`). `args.approve-mapping` is a generation failure. After writing, search the script for `args.[a-z]+-`. Any match is a failure.

`--dry-run` builds the objects on disk and does not call the scanner. It does not commit. It does not prove the server will accept the object. The server check happens on upload. Say that in the help text and in **Ways to run the script**.

A generated script that posts to `localhost`, `127.0.0.1`, a laptop port, or any URL other than `{ANYPOINT_BASE}/agent-scanner` is a generation failure. There is no `--scanner-base` and no `SCANNER_BASE`.

## Ways to run the script

After the two files exist, the chat shows this section in this order, then it stops: interactive, then parameters, then the input file. The command is whatever runs the file they asked for. Do not show a Python, Bash, Java, or Go command unless that is the language they named. The blocks below use `<run> <script>` as the shape. `--help` uses the same three columns: prompt label, parameter flag, input file key.

### Prerequisites

- The language runtime they named is installed, including any library their auth document requires.
- A Connected App client id and secret, as in **Connected App**.
- The organization id and the configuration id, copied from the self-managed scanner page. The script does not look these up and does not create them.
- The provider session: already logged in (`--profile` / `~/.aws/config` on AWS, `az` on Azure, `gcloud` on GCP) or the credentials from their auth document, stored as environment variables or in the inputs file. Not in the chat. Not on the command line.

### Prompts

```
<run> <script>
```

The script asks once for each required value that is still empty, then uploads. At the end it asks "Commit this scan? [y/N]". Pressing Enter means no.

### Parameters

```
export ANYPOINT_CLIENT_SECRET="..."
export PROVIDER_SECRET="..."
<run> <script> \
  --anypoint-base https://anypoint.mulesoft.com \
  --org YOUR_ORG_ID \
  --config YOUR_CONFIGURATION_ID \
  --client-id YOUR_CLIENT_ID \
  --commit
```

`--commit` answers yes. Without it, the script uploads and does not commit. Secret names match their auth document. `PROVIDER_SECRET` above is a placeholder for that name. For AWS already logged in on this machine, add `--profile NAME --region us-east-1` instead of access-key exports.

### Input file

The file `inputs.env` is a downloadable file, written beside the script, and its full text is in the chat as a block named `inputs.env`. They fill the empty secrets on the machine that runs the script, then:

```
<run> <script> --input-file inputs.env
```

`PUSH_COMMIT=yes` in that file commits the scan. Empty or `no` does not.

### Dry-run and help

```
<run> <script> --help
<run> <script> --dry-run
<run> <script> --input-file inputs.env --dry-run
```

`--help` lists the inputs. `--dry-run` writes the objects locally and does not contact the scanner.

## Failures

Every failure prints this on stderr and exits 2:

```
FAILED step=<name> http=<code>
where: <call>
request: <method and path, no secrets>
response fields: <names only>
why: <one sentence>
body: <response snippet with secrets removed>
next: <what to fix>
```

Do not print only `HTTP Error 503:` or a traceback.

| http | why | next |
|---|---|---|
| 0 / connection refused | Cannot reach that Anypoint host. | Confirm `--anypoint-base` / `ANYPOINT_BASE` is reachable. Token and push both use `{that host}/agent-scanner`. |
| 401 / 403 | Connected App rejected. Wrong secret, or missing `manage:exchange` on this organization. | Reset the secret on the same app as the client id. Scope it to this org. |
| 404 | Org id, configuration id, or `/agent-scanner` path is wrong on this Anypoint host. | Stay on `{ANYPOINT_BASE}/agent-scanner`. Copy both ids from the Exchange scanner page. |
| 400 / 422 | Zip refused. `type` must match this configuration. Path must be `{id}/specification/...`. Or `/commit` without a real `workspaceRunId`. | Unzip and check `specification/config.json`. Do not invent the workspace id. |
| 415 | `/push` did not receive a zip. The endpoint consumes `multipart/form-data` part `file`. | POST the zip bytes. Do not JSON. Boundary must not start with `=`. With `requests`, use `files=` and do not also set `Content-Type`. |
| 503 | Scanner or a proxy in front of it is down. | Retry when the operator says the scanner is healthy. |

JSON stdout must include `ok`, `truncated`, asset counts by type, `skipped`, `failures`, and `publish` with `uploaded`, `failed`, `completed`, `workspaceRunId`, `scanRunId`, `notes`.

Read configuration id from `--config`, `SCANNER_CONFIGURATION_ID`, then `SCANNER_CONFIG_ID`. One id. Zip `type` is the source constant `ASSET_TYPE`. A customer script that can emit more than one zip type is a generation failure.

## Provider-agnostic UX, asset-type-specific pull

The generated script is the laptop half of pull `execute`. Provider SDK calls and form fields change. Customer UX does not.

- **Provider-agnostic UX.** Same flags, same “prompt only what is missing”, same numbered stderr, same FAILED block, same JSON stdout — AWS, Azure, GCP, Databricks, Snowflake, Kong, or a new provider. Only the pull-form labels and that bundle’s inventory calls change.
- **Language-agnostic I/O.** Python, Bash, Node, Java, Go, PowerShell: same flag names, env names, step labels, JSON keys.
- **Asset-type-specific discovery.** One source constant, `ASSET_TYPE`. Classify with the probe in that bundle’s inventory, the way pull Java does. Never by name. Never “every READY row from a shared list”.

Zipping `harness_model_Bedrock` as `type: mcp`, or zipping `agent_scanner_mcp_fixture` as `type: agent`, is a generation failure even when both runtimes appeared in `ListAgentRuntimes`.

## Same job, any language

Whatever they named (Python, Bash, Node, Java, Go, PowerShell, or another runtime) the generated file must parse in that language and do the same job: pull-form provider login, list one zip type, MuleSoft token, `POST .../push`, optional commit, FAILED block, JSON stdout. Do not emit Python because Bash is hard.

Run these on the generated file before claiming it works. If the checker cannot run here, search the file for the forbidden patterns.

| They asked | Must pass |
|---|---|
| Python | `python3 -m py_compile FILE`. Search for `args.[a-z]+-`. Any match fails. |
| Node / `.mjs` | `node --check FILE`. |
| Bash | `bash -n FILE`, then search for `}}}}` and `--region ${`. Any match fails. |
| Java | project compile. |
| Go | `go build`. |
| Other | that project's syntax check. |

Do **not** nest `${CLI_REGION:-${AWS_REGION:-${AWS_DEFAULT_REGION:-x}}}}`. Sequential assignments only:

```bash
region=""
[ -n "${CLI_REGION:-}" ] && region="$CLI_REGION"
[ -z "$region" ] && region="${AWS_REGION:-}"
[ -z "$region" ] && region="${AWS_DEFAULT_REGION:-}"
region="$(unquote_aws "$region")"
```

Python: stdlib plus the cloud SDK already on the laptop; AWS uses `boto3`. Node: Node 18+ `fetch` unless their project already has an SDK. Bash: `curl`, `jq`, `zip`; token call is form-urlencoded, never JSON content-type. Same env names (`ANYPOINT_BASE`, `SCANNER_CONFIGURATION_ID`, `ANYPOINT_CLIENT_SECRET`, `PUSH_COMMIT`).

## Catalog of calls

Shape reminder only. The customer paste is their own OpenAPI, Postman collection, or redacted request and response. Do not embed a block from here because they named that provider. Use a block only when they pasted that same inventory. A provider that is not in this catalog is onboarded the same way: their inventory, their auth, their language, the same `POST .../push`, the same `POST .../commit`.

### AWS agents and MCP (AgentCore)

Already logged in on this machine, or access keys. Service `bedrock-agentcore-control`. Call boto3 `list_agent_runtimes` (CLI name `list-agent-runtimes`). Do not POST to the path `/ListAgentRuntimes`.

- List: `list-agent-runtimes`, `max-results` 100, token `next-token`. Response array `agentRuntimes`. Stop after 50 pages. A stopped list is partial.
- Keep runtimes whose `status` is `READY`.
- External id is the runtime id. Display name is the runtime name.
- **This script publishes one asset type.** Shared list is not shared publish.
- Agent (`ASSET_TYPE = "agent"`): `get-agent-runtime` before any A2A zip. Skip `serverProtocol=MCP` (count only unless `--verbose`). Then `bedrock-agentcore` `get-agent-card`. If that returns a validation error that the card is only for A2A agents, build a card from the runtime id. `url` is `https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{id}/invocations`. `protocolVersion` is `0.3.0`. `description` is required. `version` is `1.0.0`. `capabilities` is `{ "streaming": true }`. Both mode arrays are `["text"]`. `skills` is `[]`. If GetAgentCard returns v1 interfaces and no `url`, write `a2a-v1-card.json` and keep `supportedInterfaces`.
- MCP (`ASSET_TYPE = "mcp"`): same list, then `get-agent-runtime` for `agentRuntimeArn`, then `list-agent-runtime-endpoints` for `qualifier`. SigV4 JSON-RPC `initialize` then `tools/list` to `https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{urlencoded ARN}/invocations?qualifier={endpointName}`. Service is `bedrock-agentcore`. Null `initialize` result = not MCP; skip (count only; `--verbose` may print `skipped {id} not MCP`). Name is never classification. Do not POST `/runtimes/{id}/invocations/mcp`. Exchange `transport.path` `/mcp` is the zip field only.

### AWS REST (API Gateway v1)

- List: `aws apigateway get-rest-apis`, `limit` 500, token query `position`.
- Stages: `get-stages` for that `rest-api-id`. No stage means skip that API (count only unless `--verbose`).
- Export: `get-export` with `export-type` `oas30` and `accepts` `application/json`.
- One asset per stage. External id is `{apiId}__{stage}`.

### Azure AI Foundry agents

`az` already logged in. List URL they must confirm: `https://{resource}.services.ai.azure.com/api/projects/{project}/agents?api-version=v1`. Detail: `GET` that host `/agents/{id}?api-version=v1`. Stop after 100 pages or 50 agents.

### Azure API Management REST

`az` already logged in. List APIs with the API Management resource in the subscription, resource group, and service name they provide. Export each API as OpenAPI. Caps: 1000 instances, 10000 APIs.

### Azure API Management MCP

`GET https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.ApiManagement/service?api-version=2025-09-01-preview`, then `GET .../service/{name}/apis?api-version=2025-09-01-preview` with `$filter=properties/type eq 'mcp'`. One MCP card per API.

### Google Vertex agents

`gcloud` already logged in (ADC, scope `cloud-platform`). Same list API as pull `VertexAgentScannerService`. Prompt **GCP Project ID** and **Location**. Do not prompt Service Account Email or Private Key unless they pasted a service-account key as the auth they will actually use. Pull form is `ServiceAccountCredentials` from those fields; both mint a Bearer token for the same host.

`GET https://{location}-aiplatform.googleapis.com/v1/projects/{project}/locations/{location}/reasoningEngines?pageSize=100`. Follow `pageToken`. Cap 10000. Connection test `pageSize=1`.

Zip directory (push external id) is `projectId + location + engineId` with no separators (`getAgentIdFromName`, example `test-projectus-central1123456789`). A Vertex zip named only the last path segment of `name` is a generation failure.

Card: look at `spec.classMethods` for `name` `on_message_send` and `a2a_agent_card`. If that JSON is A2A v0.3 or v1, use it. Always set `url` to `https://{location}-aiplatform.googleapis.com/v1/{engine.name}:query`. If there is no card, write `a2a-card.json` with `name`/`description` from `displayName` and `description` (empty string if missing), `protocolVersion` `0.3.0`, `version` `1.0.0`, `capabilities` `{ "streaming": false }`, `defaultInputModes` `["text","json"]`, `defaultOutputModes` `["json"]`, `skills` `[]`.

### Google Apigee REST

`gcloud` already logged in (ADC). Prompt **GCP Project ID** (that value is the Apigee org in every path). Same calls as pull `ApigeeApiClient`. Do not prompt Service Account Email or Private Key unless they pasted a service-account key.

`GET https://apigee.googleapis.com/v1/organizations/{project}/apis`, array `proxies`, `pageToken`, stop after 1000 pages. Then `GET .../apis/{api}/deployments`. Skip when `deployments` is missing or empty. Each deployment needs `environment` and `revision`. Download `GET .../apis/{api}/revisions/{rev}?format=bundle`. Take the first valid `openapi.yaml` or `openapi.json` under `apiproxy/resources/oas/`. One zip per proxy. If no bundle has OAS, synthesize `openapi` `3.0.0`, `info.title` the proxy name, `info.version` `current`, `paths` `{}`, `servers` `[{ "url": "https://{project}-{firstEnvironment}.apigee.net" }]`. External id `apigee-{proxyName}`.

### Google Cloud Run MCP (customer-supplied)

Not `VERTEX_MCP`. That enum has no pull class. Do not list reasoning engines.

`gcloud` ADC. Prompt **GCP Project ID** and **Location**. List `GET https://run.googleapis.com/v2/projects/{project}/locations/{location}/services` with an **access** token. For each service `uri`, JSON-RPC `initialize` (`protocolVersion` `2025-03-26`) then `tools/list` to `POST {uri}/` with an **identity** token (`gcloud auth print-identity-token --audiences={uri}`). Null `initialize` result = skip (count only unless `--verbose`). HTTP 401/403 on initialize is FAILED. Do not POST `https://run.googleapis.com/mcp-handshake`.

Zip `mcp-metadata.json`: `transport.kind` `streamableHttp`, `transport.path` `/`. If `capabilities` is present, four booleans `tools`, `resources`, `prompts`, `logging`. Omit `serverInfo`. External id is the service id (last segment of `name`).

### Databricks agents

They give a workspace URL. List serving endpoints. Then `GET {workspace}/api/2.0/serving-endpoints/{name}/openapi`. Cap 10000. Reject a workspace URL that is not public https.

### Databricks MCP

Same workspace login. Try, in order, `/api/2.0/mcp/functions/system/ai`, `/api/2.0/mcp/sql`, `/api/2.0/mcp/genie`, `/api/2.1/unity-catalog/connections`, `/api/2.0/unity-catalog/connections`, `/api/2.0/preview/apps`, `/api/2.0/apps`, `GET /api/2.0/genie/spaces`. A 404 on the first page means that source is absent.

### Snowflake agents

They give an account URL. Header `Authorization: Bearer` and `X-Snowflake-Authorization-Token-Type: PROGRAMMATIC_ACCESS_TOKEN`. List databases, schemas, agents, then read `agent_spec`.

### Snowflake MCP

`POST {account}/api/v2/statements` with SQL `SHOW MCP SERVERS`. Then JSON-RPC `initialize`, then `tools/list`. A failed handshake is a skip (count only unless `--verbose`).

### Microsoft Copilot Studio agents

`GET https://api.powerplatform.com/environmentmanagement/environments?api-version=2024-10-01`. Then Dataverse `bots` with the published, non-msdyn filter. Dataverse host must look like `https://{name}.crm.dynamics.com`.

### Kong REST

Bearer token in the environment, not in the file. Control planes, then services, routes, plugins. OpenAPI body is `GET {host}/v3/apis/{id}/specifications/{specId}`. Do not invent an OpenAPI document from the route list.

### GoDaddy agents

`GET {baseUrl}/v1/agents?protocol=A2A&limit=20&offset={offset}`. Cap 1000. `baseUrl` must be public https.

### Claude agents

`GET https://api.anthropic.com/v1/agents?limit=100&page={next_page}`. Headers `X-Api-Key` from the environment, `anthropic-version: 2023-06-01`, `anthropic-beta: managed-agents-2026-04-01`. Card `url` is `https://api.anthropic.com/v1/agents/{id}/messages`.

### LangSmith agents

`GET {apiHost}/v2/deployments?status=READY&limit=100&offset=`. Then `POST {custom_url}/assistants/search` and `GET {custom_url}/.well-known/agent-card.json`.

### Salesforce Agentforce

`GET {instance}/services/data/v64.0/query`. SOQL `SELECT Id, DeveloperName, MasterLabel FROM BotDefinition WHERE IsDeleted = false`. Follow `nextRecordsUrl` for at most 50 pages. External id is `Id`.

### Bedrock agents (not AgentCore)

`aws bedrock list-agents`, then `get-agent`, versions, aliases. A missing permission omits that field and the script continues. Do not mix this inventory with AgentCore `list-agent-runtimes`.

### ServiceNow agents

Not a shipped pull scanner. Use it only if they confirm this list. Client credentials token, then `alm_ai_system_digital_asset`. Do not call `sn_aia_agent`. Ask them what to put in the card `url`.

### No calls exist

Do not write a script for Azure AI Foundry MCP, Microsoft 365 Copilot, Vertex MCP, Gemini agents, or Gemini MCP **from those enum names**. There is no pull-scanner call to copy. Ask them for the list call, or stop. A customer-supplied Cloud Run MCP inventory is a list-plus-handshake they paste; that is not the Vertex MCP enum.

## ZIP and push

One asset is one zip. The zip has one top-level directory. That directory name is the external id, at most 255 characters, the provider id, not the display name.

`specification/config.json`:

```json
{ "name": "<display name>", "type": "agent", "description": "<optional, max 500 chars>" }
```

`type` is the baked `ASSET_TYPE` and must match that configuration.

Artifact JSON must pass the Exchange agent-fabric schemas (tag `1.2609.1`: `agent_card`, `agent_card_v1`, `other_card`, `mcp_metadata`). Do not invent a second subset.

A2A v0.3 (`a2a-card.json`) required keys: `name`, `description`, `protocolVersion`, `url`, `version`, `capabilities`, `defaultInputModes` (at least one), `defaultOutputModes` (at least one), `skills`. Synthesized AgentCore fallbacks use `protocolVersion` `0.3.0`. Skill objects, when present, need `id`, `name`, `description`, and `tags`.

A2A v1 (`a2a-v1-card.json`): `supportedInterfaces` or `supported_interfaces` with a callable `url`; never a top-level `url`.

MCP (`mcp-metadata.json`): `transport` required; if emitting `capabilities`, emit all four booleans `tools`, `resources`, `prompts`, `logging`; omit `serverInfo`.

REST artifact is the exported OpenAPI document. It must contain `openapi` or `swagger`.

Push, to that one configuration id. `/push` is the zip.

```http
POST {ANYPOINT_BASE}/agent-scanner/api/v1/organizations/{ANYPOINT_ORG_ID}/scanner-configurations/{configId}/push
Authorization: Bearer <token>
Content-Type: multipart/form-data; boundary=----pushcollector7b1c

------pushcollector7b1c
Content-Disposition: form-data; name="file"; filename="{externalId}.zip"
Content-Type: application/zip

<zip bytes>
------pushcollector7b1c--
```

Required Python (or the same bytes in the language they named). Copy the boundary; do not start it with `=`.

```python
def _multipart_zip(filename, payload):
    boundary = "----pushcollector7b1c"
    head = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        "Content-Type: application/zip\r\n\r\n"
    ).encode()
    tail = f"\r\n--{boundary}--\r\n".encode()
    return head + payload + tail, f"multipart/form-data; boundary={boundary}"
```

`requests` equivalent: `files={"file": (f"{external_id}.zip", zip_bytes, "application/zip")}` and do not set `Content-Type` yourself (that drops the boundary → 415). `curl`: `-F "file=@{externalId}.zip;type=application/zip"`. After writing, search the script for `json=` or `"Content-Type": "application/json"` on the `/push` URL. Any match is a generation failure. Search for `boundary================` or a boundary that starts with `=`. Any match is a generation failure.

HTTP 202 body has `workspaceRunId`. Read it. A generated script that calls `POST .../push-assets` is a generation failure.

2. Finish with `POST .../commit` `Content-Type: application/json` `{"workspaceRunId":"<id from 202>","complete":true|false}`. The customer question is "Commit this scan? [y/N]". A generated script that calls `POST .../complete` or `POST .../seal` is a generation failure. A generated script that POSTs `/commit` when every `/push` failed, or with a homemade `run-` id, is a generation failure.

The zip **must** contain `{externalId}/specification/config.json` and `{externalId}/specification/<artifact>`. `{externalId}/config.json` at the top of the zip is invalid.

## Best Practices

- **One question per turn.** ✅ the quoted sentences in **Workflow**. ❌ combining asset type, inventory, auth, or language in one reply.
- **Infer the provider; never ask its name.** ✅ read the attached spec. ❌ "which provider?". On an invalid spec, ask for the missing list, fetch, handshake, export, or auth piece.
- **Mapping gate.** ✅ show the mapping, then wait for "Does this look fine?". ❌ writing files in the mapping turn. ❌ treating a script dump as the mapping.
- **Quiet skips.** ✅ `listed N, matching M, skipped K` plus matching asset lines. ❌ skip ids, `skipping MCP`, or `not MCP` unless `--verbose`.
- **Omission is not deletion.** ✅ `DELETE .../push/{externalId}` only when they ask to unstage. ❌ DELETE because a second run's list is shorter.
- **Baked asset type.** ✅ `ASSET_TYPE` constant. ❌ `--asset-type` or an environment variable that switches type.

## Troubleshooting

**HTTP 415 on POST /push:** the body was not a ZIP as multipart part `file`. JSON, `json=`, `Content-Type: application/json`, a missing boundary, or a boundary that starts with `=` all produce 415. Use the `_multipart_zip` helper (or `files={"file": (...)}` without setting Content-Type).

**No inventory file in this skill:** this package does not ship provider OpenAPI files. If they ask which file to open, ask them to paste or attach their own specification.

**Invalid or incomplete spec:** do not invent calls and do not ask which provider. Ask for the missing list, fetch, handshake, export, or auth piece using the questions in **Workflow**.

**Salesforce C2C or managed authorization-code login:** that pull form is not customer-executable. Ask for a request and response they can run from their machine before writing files.

**Zero matching assets:** print `No matching {ASSET_TYPE} assets found.`, print JSON, exit 0. Do not call /push or /commit.

**HTTP 401/403 on /push or /commit:** Connected App missing `manage:exchange`, wrong organization, or the configuration is not a self-managed scanner they can write.

## Related Skills

- **skill setup-service-scanner**: Create a pull scanner configuration that discovers assets from a connected cloud platform.
- **skill run-service-scan-and-view-results**: Run a hosted scan and review discovered staging assets.

