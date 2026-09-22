---
name: setup-pstack
description: "Install, update, remove, or inspect optional Codex agent profiles for pstack, including explicit model-role configuration. Use for setup-pstack or requests to configure pstack agents and models."
---

# Setup pstack for Codex

Install optional custom-agent profiles without making them part of the plugin manifest. Codex loads project profiles from `.codex/agents/*.toml` and user profiles from `~/.codex/agents/*.toml`. This skill's `agents/openai.yaml` is UI metadata only.

Read `references/model-profile.md` before changing configuration. The portable prompts in the owning skills remain authoritative and work without installed profiles.

## Safety contract

- Require explicit user intent for install, upgrade, or uninstall.
- Ask for `project` or `user` scope when it is not clear. Project scope is the safer default only when the user says to configure the current repository.
- Scan both project and user agent directories before a write. Stop on duplicate TOML `name` fields regardless of filename or layer.
- Never overwrite another owner. Update or remove only files whose current SHA-256 matches this setup's receipt.
- A modified, missing, or relocated receipted file requires review; leave profiles and receipt untouched.
- Configuration is not runtime proof. Never claim the served model, effort, effective permissions, connector set, or skill availability unless a supported live surface reports it.

## Model policy

Ask whether each role should inherit the parent or request an explicit `model` plus `reasoning_effort` pair.

If a supported Codex model-list surface is observable, convert it to JSON records shaped like:

```json
[{"slug":"gpt-5.6-sol","reasoning_efforts":["low","medium","high","xhigh","max","ultra"]}]
```

Validate both values before writing them. If no supported model list is observable, do not guess or accept pasted entitlement claims as proof: omit both TOML fields, inherit the parent, and record `unverified-inheritance` with the requested pair in the receipt. A missing model or unsupported effort is a hard stop; let the user choose another pair or inheritance.

Profiles are a JSON object keyed by namespaced agent name:

```json
{
  "pstack-poteto-agent": {"model":"gpt-5.6-sol","reasoning_effort":"high"},
  "pstack-comment-sicko": {"model":"gpt-5.6-terra","reasoning_effort":"medium"}
}
```

## Execute

The helper is `scripts/manage-agents.mjs` relative to this skill.

```text
node scripts/manage-agents.mjs scan --project-root <repo> --user-home <home>
node scripts/manage-agents.mjs install --scope project --project-root <repo> --user-home <home>
node scripts/manage-agents.mjs install --scope user --project-root <repo> --user-home <home>
node scripts/manage-agents.mjs uninstall --scope project --project-root <repo> --user-home <home>
```

Add `--profile <json-file>` for requested pairs and `--models <json-file>` only when the list came from an observable supported surface. Do not create temporary files containing secrets; these files contain model identifiers only.

On success, report the scope, written paths, receipt path, and each role's configuration status. Say that new profiles apply to newly spawned agents. When a panel inherits or loses distinct profiles, report reduced model diversity instead of claiming which model served it.

On `review-required` or any collision, stop. Show the exact paths and do not suggest force deletion.
