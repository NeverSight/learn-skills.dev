---
name: qwencloud-operate
version: "1.0"
description: >-
  Diagnose why an application deployed by qwencloud-deploy to Alibaba Cloud International
  (alibabacloud.com) is unavailable or slow, and — only after explicit user confirmation —
  perform a safe recovery and verify the result. Reads the local .qwencloud-deploy state file
  to identify ECS (and optional RDS MySQL) resources, runs minimal read-only diagnostics, then
  proposes one recovery action at a time (start ECS, restart the app service, reload Nginx),
  each gated by a confirmation that states impact.
  Use when: the user says the app is down / returns 502 / cannot connect to the database, or
  asks to restart and verify the app.
  Do not use when: no .qwencloud-deploy state file exists, the target is Aliyun China
  (use qianwenai-operate), or the user only wants a status/cost overview (use qwencloud-observe).
prerequisites:
  - aliyun CLI 3.x configured with international-site credentials
  - a .qwencloud-deploy state file in the project directory
input: >-
  A project directory containing .qwencloud-deploy. A described symptom (down / 502 / slow /
  cannot reach DB).
output: >-
  A diagnosis (fault layer, likely cause, evidence, recommended action, impact); after
  confirmation, one recovery action, then verification returning recovered / partially recovered /
  not recovered, plus an audit record (time, target, action, confirmation, CLI RequestId, result).
---

# Qwen Cloud Operate

Fault diagnosis and confirmed recovery for an application deployed by `qwencloud-deploy` on
Alibaba Cloud International. Diagnosis is read-only and needs no confirmation; any action that
changes cloud or app state requires explicit confirmation.

## Interaction Flow

```text
Identify app & resources
→ Minimal diagnosis (read-only)
→ Give cause, evidence, recommended action
→ Show impact and request confirmation
→ Execute one recovery action
→ Verify application, ECS, RDS
→ Return result + audit info
→ Offer to re-score via qwencloud-observe (before → after)
```

## Interaction form

- **Read-only information** (diagnosis, cause, evidence, verification): plain text, with one evidence
  line after each judgment (metric, status, RequestId).
- **State-changing actions** (start/stop ECS, restart app, reload Nginx — any write call): first an
  AskUserQuestion whose prompt answers **what it does** · **impact** (downtime/irreversible) · **how to
  verify**; do nothing before confirmation, and propose one recovery action at a time.
- **Proactive discipline**: after recovery, close quietly when the result is healthy; speak up with a
  next step only when a risk remains or recovery failed, and let the user choose.

## Scope

| In Scope | Out of Scope |
|----------|--------------|
| Apps deployed by `qwencloud-deploy` (state file present) | Apps without a `.qwencloud-deploy` state file |
| Single ECS, or ECS + RDS MySQL 8.0 | Other topologies / self-managed servers |
| Diagnose + confirmed recovery (start ECS, restart app, reload Nginx) | Data-destructive ops, scaling, config redesign |
| Pinpoint an app-layer error (which layer broke, what error) | Source-code review, finding bugs/vulns, judging which line is wrong, editing code |
| Alibaba Cloud International | Aliyun China → use `qianwenai-operate` |

## Code issues are out of scope

This skill handles infrastructure and runtime faults; it does not review source code, locate
defects, or edit code. Diagnosis can pinpoint an app-layer error and what was thrown to narrow
things down, but it does not judge which line is wrong and does not change code.

When code is involved, tell the user plainly: editing code is outside this skill's scope, the user
must decide and make the change themselves, and any consequences are the user's own. Never slip a
code change into a recovery action.

## Prerequisites

> **Aliyun CLI**: `aliyun version` (need 3.x). All commands use the PascalCase native form
> straight to OpenAPI — no plugin dependency. Credentials: `aliyun configure list` only.
> **Never** read, echo, print, or ask for AK/SK/tokens. No valid
> profile → stop and ask the user to configure credentials outside this session. See
> `references/cli_installation_guide.md`.

## How to work

1. **Identify the app** from `.qwencloud-deploy`. See [workflow](references/workflow.md).
2. **Diagnose** (read-only, no confirmation needed). Find where it's broken, the likely cause, the
   evidence, and what to do about it. See [diagnose](references/diagnose.md).
3. **Recover one thing, with confirmation.** Pick the action that matches the diagnosis, show the
   user its impact and get their go-ahead, then do exactly that one thing:
   - Start a stopped server → [recover-ecs](references/recover_ecs.md)
   - Reboot a hung server → [recover-reboot](references/recover_reboot.md)
   - Restart the app service → [recover-app](references/recover_app.md)
   - Reload Nginx after `nginx -t` passes → [recover-nginx](references/recover_nginx.md)
   - Re-bind the EIP after it is unbound → [recover-eip](references/recover_eip.md)
   - Allow security-group 80 / 443 ingress → [recover-securitygroup](references/recover_securitygroup.md)
   - Database-related trouble → [recover-rds](references/recover_rds.md)
   - Certificate expired / HTTPS handshake fails → [recover-cert](references/recover_cert.md)
   - Root disk near full / still short after cleanup (resize) → [recover-disk](references/recover_disk.md)
4. **Verify** whether the app is back, then **record** what you did. See
   [workflow](references/workflow.md).

## Rules that keep recovery safe

- Diagnosis is read-only; recovery uses a small fixed set of known-safe commands.
- Every action that changes anything is confirmed with the user first, and cancelling changes
  nothing.
- Do one action, verify, then decide the next — never batch recovery steps.
- Recovery actions are safe to repeat.
- Stop before any further change on a timeout, a permission error, or an unexpected state change.
- Never put passwords, tokens, or full connection strings into the audit record or the chat.

Before any change, the confirmation tells the user: what resource, what action, whether it briefly
interrupts the app, whether the version changes, whether it costs anything new, and how you'll
verify it (and what happens if it fails).

## Required Permissions

See `references/ram_policies.md`. Read: `ecs:DescribeInstances`, `ecs:DescribeInvocations`,
`ecs:DescribeSecurityGroupAttribute`, `ecs:DescribeDisks`, `vpc:DescribeEipAddresses`,
RDS describe/performance/slow-log. Write (recovery): `ecs:StartInstance`, `ecs:RebootInstance`,
`ecs:AuthorizeSecurityGroup`, `ecs:ResizeDisk`, `vpc:AssociateEipAddress`, `ecs:RunCommand`
(whitelisted recovery commands only). Certificate re-issue also needs `alidns` record
read/write (DNS-01 challenge).

## More detail

The step-by-step guides are linked from "How to work" above. Two setup references:

- [CLI setup](references/cli_installation_guide.md) — install and credential check.
- [CLI gotchas](references/api_gotchas.md) — parameter shapes, time formats, response parsing.
- [RAM policies](references/ram_policies.md) — the permissions this skill needs.
