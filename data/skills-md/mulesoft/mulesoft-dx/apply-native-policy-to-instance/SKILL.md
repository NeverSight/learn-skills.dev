---
name: apply-native-policy-to-instance
description: |
  Apply, list, or edit provider-native policies on API instances (Kong plugin,
  Apigee template, Azure policy, or MuleSoft/Anypoint) via the MuleSoft
  Platform MCP Server. TRIGGER when: the user asks what protection they have
  on a provider's APIs ("what protection do I have for my Apigee APIs"), wants
  to change an already-applied native policy ("improve the IP filtering to
  include 1.1.1.1"), or apply one native plugin to an already-chosen instance
  ("add ip-restriction on this Kong service"). DO NOT TRIGGER when: they want
  one Universal/canonical policy across many instances or providers — use
  skill apply-universal-policy. DO NOT TRIGGER to remove, detach, enable, or
  disable a policy, or when they are driving Anypoint REST (skill
  apply-policy-to-api-instance).
license: Apache-2.0
compatibility: Requires the MuleSoft Platform MCP Server (urn:mcp:mulesoft-platform) with find_assets, view_api_instance_policies, prepare_policy_creation, get_policy_template_form, apply_policy_to_instance, edit_applied_policy, list_instance_policy_operations. If those tools are missing, stop.
metadata:
  author: mulesoft-omni
  version: "1.1.0"
---

# Apply Native Policy to an Instance

List what is already applied, change it, or apply one native plugin to one
instance — then wait until the write has actually finished.

## When to Use This Skill

**Use this skill when the user asks to:**

- "What protection do I have for my Apigee APIs?"
- "Improve the IP filtering to include 1.1.1.1"
- "Add ip-restriction to this Kong instance"
- "Apply quota to that Apigee proxy"
- List, edit, or apply a **native** plugin/template (not a Universal/canonical
  template)

**Trigger keywords:** what protection · what's applied · change this policy ·
IP filtering · this instance · Kong plugin · Apigee · Azure · native policy.

**Do NOT use this skill when:**

- They want the **same canonical policy on many instances / providers**
  → **skill apply-universal-policy** (`apply_universal_policy`)
- They are driving **Anypoint REST** (OpenAPI `urn:api:*`), not MCP →
  **skill apply-policy-to-api-instance**
- They need to **create** the instance first → **skill secure-api**
- They want to **remove / disable** a policy — say so and stop

## Prerequisites

Connected to `urn:mcp:mulesoft-platform`. Probe with
`view_api_instance_policies` or `prepare_policy_creation`. If the tools are
missing, stop. On 403 / gate-closed (`enabled: false`), say they are not
entitled and stop — never silently switch provider.

## Reference files

- **`references/native-apply.md`** — provider routing, `find_assets` join,
  edit merge, Apigee rename rule, and how to wait for completion. Read it
  before the first write.

## Workflow

### Pick the path first

Read the latest user turn and choose **one** path. Do not run Apply steps for
an Audit or Edit request.

| Path | When | Go to |
| --- | --- | --- |
| **Audit** | "What protection / what's applied" with no change yet | Step A |
| **Edit** | Change an already-applied native policy ("add 1.1.1.1") | Step E |
| **Apply** | Add a native plugin that is **not** already on this instance | Steps 1–5 |

### Rules that always apply

1. **Native catalog, not Universal.** Never send a Kong plugin name (or an
   Apigee template id) to `apply_universal_policy`.
2. **Confirm before acting.** Show the mapping (native policy name → API
   instances), then wait for an explicit yes before apply or edit.
3. **Do not guess property names.** Build `configuration_data` from
   `get_policy_template_form` (`template.configuration`). Apigee uses nested
   objects and `@`-prefixed attributes — copy those names.
4. **One-shot config.** Show the schema table (required-only when it is
   longer than about 12 flattened rows, disclosing hidden optionals and
   offering to expand). Collect the visible fields in one reply. Do not
   invent optionals. On **edit**, prompt only for fields the merge left
   empty — do not re-ask the whole schema when the delta is complete.
5. **Wait for completion.** External writes often return `status: "success"`
   with `httpStatus` 202 / `operationStatus=accepted`. That is **acceptance**,
   not done. Poll `list_instance_policy_operations`. MuleSoft writes are
   typically synchronous (2xx without `operationStatus`).

### Step A: Audit — what is already applied

Skip Apply. Do **not** pass `policy_name_filter`. Do **not** offer to apply
a Universal policy unless they ask.

This is the "what protection do I have for my Apigee APIs?" path: they may
name a **provider slice** (several APIs), not a single instance.

1. Call `find_assets` with `include_applied_policies=true`, `asset_type=api`,
   `user_query` verbatim. Put a named provider in `query`, then filter
   client-side (`references/native-apply.md`).
2. Present the **applied-policy list** grouped by API, then instance — policy
   **names** with each API instance. When they named a provider, show only
   that provider's instances.
3. Ask whether they want to change any. If they do, go to Step E.

Example shape:

```
Payments API
  prod (Production · apigee)
    - Access control (inbound, enabled)
  sandbox (Sandbox · apigee)
    - (none)
```

### Step E: Edit an already-applied native policy

Skip Apply unless you still need the instance list from Step A.

There is no bulk-edit tool: loop **once per instance**. Several Apigee APIs
with the same native policy is still one `edit_applied_policy` each.

1. Identify `api_instance_id` + `policy_id` + Exchange
   `asset.{group_id,asset_id,asset_version}` + `provider` (and
   `environment_id` on MuleSoft) from `view_api_instance_policies`
   (do not guess). Skip `readOnly: true` — say so and stop for those.
2. Load the schema with `get_policy_template_form` using those coordinates.
3. Read current `configurationData`. Merge the requested **delta** into that
   full object (`configuration_data` replaces wholesale — omitted keys are
   dropped). Prompt only for required fields the merge left empty.
4. **Apigee: never change `@name` / display name** on an existing policy.
   Edit configuration values only. A rename makes the async `UPDATE` fail
   (`BAD_REQUEST`) even though the tool reported `success` on the 202.
5. Show the **native-policy → API + instance mapping** of every instance you
   will loop. **[GATE] Wait for okay.**
6. Call `edit_applied_policy` per instance. Then wait
   (`references/native-apply.md`). Confirm per API instance.

### Step 1: Identify the instance (Apply)

If the user already named an instance, use that `api_instance_id` (and
`environment_id` for MuleSoft). Otherwise `find_assets` (`asset_type=api`,
`user_query` verbatim) and pick **one**. If several remain, list them
(API name · instance · environment · provider) and wait.

Resolve `provider`: `kong` / `apigee` / `azure` for external; omit (or
`mulesoft`) for Anypoint. Do not guess.

Do not silently apply a **new** native plugin to a set — that fan-out is
skill apply-universal-policy (canonical) or a confirmed Edit loop (already
applied).

### Step 2: List native policies that are not yet applied

Call `prepare_policy_creation` with `organization_id`, `api_instance_id`,
`provider` (external), and `policy_name_hint` when they named a policy.
MuleSoft also needs `environment_id`.

Each entry carries Exchange coordinates (`groupId` / `assetId` /
`assetVersion`) plus `capabilities.injectionPoints` and `applicationLimit`
(`MULTIPLE` = the same template may be applied more than once). Applied
policies are filtered out (`alreadyApplied` is always false here).

If more than one template matches the hint, list `name`s and ask. If none
match, say so and stop.

### Step 3: Load the schema and collect configuration

Call `get_policy_template_form` with the selected template's Exchange
coordinates (`group_id`, `asset_id`, `asset_version` — required on the
external path) plus `provider` / `environment_id` as in Step 2.

Present the schema table. **[GATE] Wait for the whole config in one
reply, then for okay to apply.**

### Step 4: Apply once

Call `apply_policy_to_instance` **once** with:

- `api_instance_id`
- `configuration_data` — the collected object (schema property names, not
  guessed ones)
- `asset.{group_id,asset_id,asset_version}` from Step 2 (required external)
- `provider` for Kong / Apigee / Azure
- `environment_id` for MuleSoft
- `injection_point` only if the template requires it and the user set it;
  otherwise omit and let APIM default it

Do not loop this tool. Do not call `apply_universal_policy`.

### Step 5: Wait until it is actually done

See `references/native-apply.md`. Report the native policy name → API
instances (environment / provider). On `FAILED`, say whether
`error.retryable` is present. Optionally re-read
`view_api_instance_policies` so the user sees the live `policyId` and
config.

## Best Practices

- **Route first.** ✅ Audit stays on Step A; Edit on Step E; a new plugin
  on one instance is Steps 1–5. ❌ running `prepare_policy_creation` /
  apply because the file is numbered 1–5. ❌ sending a Kong plugin to
  `apply_universal_policy`.
- **Confirm the mapping, then wait.** ✅ native policy name → API
  instances, then an explicit yes. ❌ writing on the schema reply. ❌
  treating `status: "success"` + HTTP 202 as done — poll
  `list_instance_policy_operations`.
- **Don't guess coordinates or property names.** ✅ `policy_id` / `asset`
  from `view_api_instance_policies`; config keys from
  `get_policy_template_form`. ❌ inventing Apigee `@`-prefixed fields or
  changing `@name` on edit.

## Troubleshooting

**Tools missing:** the Platform MCP catalog on this host is stale. Stop.
Do not fall back to Anypoint REST unless the user is on
skill apply-policy-to-api-instance.

**Gate closed / 403:** say they are not entitled for that provider. Stop.

**Apply of a new plugin to more than one instance:** ask which one, or
switch to skill apply-universal-policy if they meant a canonical template.

**`httpStatus` 422 on apply/edit:** `configuration_data` does not match the
provider schema. Re-read `get_policy_template_form` and use its exact
property names.

**Apigee edit failed after a 202 `success`:** you likely changed
`AccessControl.@name` (or the equivalent display name). Keep `@name`
identical to the applied value; delete-and-recreate is not on this surface.

**User named a Universal/canonical template for many APIs:** switch to
skill apply-universal-policy.

## Related Skills

- **skill apply-universal-policy**: one canonical policy across many
  instances or providers (`apply_universal_policy`).
- **skill apply-policy-to-api-instance**: same job over Anypoint REST
  (`urn:api:*`), not MCP.
- **skill secure-api**: create/deploy the instance first.
