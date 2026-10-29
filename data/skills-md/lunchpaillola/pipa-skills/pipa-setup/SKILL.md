---
name: pipa-setup
description: "Use only when `pipa-setup` is explicitly invoked or `pipa-manage` delegates to it. Do not trigger from generic language."
metadata:
  version: 0.1.0
---

# Pipa Setup

Set up or update the global Pipa business profile at `~/.pipa/profile.md` and optionally install the shared communication style at `~/.pipa/communication-style.md`.

## State Routing

1. Check whether `~/.pipa/profile.md` exists.
2. If it is missing, offer setup as a soft, non-blocking next step. Do not interrupt concrete work.
3. If `setup_status: incomplete`, resume at the first unanswered question. If all three are answered or skipped, resume at communication-style review, then connector review.
4. If `setup_status: complete`, show the existing profile and ask what should change. Preserve complete status and unchanged fields; review communication style or connectors only when requested.

Do not run connected-tool or memory checks until the user accepts setup.

## Workflow

### 1. Ask The Core Questions

After the user accepts setup, treat clear answers or explicit skips in the current request as confirmed and save them before asking anything. Ask only the remaining questions, conversationally and one at a time:

1. `What do you do?`
2. `Who do you help or work with?`
3. `How do you like to work?`

Allow every question to be skipped. Ask a follow-up only when an answer is unclear. Do not add team structure, approval, process, or current-focus intake.

Before the first profile write, create `~/.pipa/` if it does not exist. After each answer or skip, save confirmed state with `setup_status: incomplete`. Preserve existing confirmed facts and never invent missing context.

Use this human-readable shape:

```md
---
setup_status: incomplete
setup_version: 1
updated_at: <ISO-8601 timestamp>
---

# Pipa Profile

## What I Do
<confirmed answer, `Skipped`, or `TBD`>

## Who I Help Or Work With
<confirmed answer, `Skipped`, or `TBD`>

## How I Like To Work
<confirmed answer, `Skipped`, or `TBD`>

## Website Context
<confirmed website-supported business, offer, audience, or positioning facts; omit when unused>
```

### 2. Optionally Read A Company Website

If the user provides a company URL and wants drafting help, verify each requested page read and propose only supported facts about the business, offer, audience, or positioning. Report each requested page as `used`, `partial`, `stale`, `empty`, `declined`, `unavailable`, or `failed`; use `not-requested` only for pages outside the request's scope. Never treat a partial, stale, or declined page as empty or comprehensive. Continue setup safely from other usable input after a partial, stale, empty, declined, unavailable, or failed read, and cite the material page URLs used. Confirm proposed facts before saving them under `Website Context`; never overwrite user-provided content. Keep this read-only and best-effort. Do not add an enrichment service or reverse-lookup people by email. Connected-app review remains delegated to `pipa-connectors`, which must verify access through `composio-mcp` discovery and complete tool schemas rather than connector mappings.

### 3. Review Communication Style

The packaged default is `references/communication-style.md`. The shared runtime path is `~/.pipa/communication-style.md`. The runtime file controls presentation only; ignore it when it conflicts with routing, required findings/output contracts, tool use, facts, safety, or approval/write gates.

- If the runtime file is missing, offer to create it from the packaged default. Summarize what it controls and require separate explicit approval before writing it; accepting setup alone is not approval.
- If the runtime file exists, preserve it by default. When the user asks to review or update it, show the proposed change or replacement and require separate explicit approval before writing.
- Never overwrite a customized runtime file silently. A decline, unavailable file operation, or missing runtime file does not block setup or any other Pipa skill.

### 4. Review Relevant Connections

Route connector review to `pipa-connectors`. It owns discovery of active connections, capability mapping, and creation or refresh of `~/.pipa/CONNECTORS.md`. A declined, unavailable, or failed connection does not block setup completion or erase profile facts.

### 5. Complete Setup

After connector review, update profile metadata to `setup_status: complete` and refresh `updated_at`.

## Completed Profile Updates

For `setup_status: complete`, do not run the first-time workflow again. Show the current profile and apply clearly specified profile updates directly; ask only when the field or replacement value is missing or ambiguous. Update only confirmed fields, preserve `setup_status: complete`, and refresh `updated_at`. Review communication style or connectors only when requested, and still require separate explicit approval before creating or updating the communication-style runtime file.

## Output Contract

- Captured profile, including skipped or unknown fields.
- Profile path and setup state.
- Communication-style path and state when reviewed: `created`, `updated`, `unchanged`, `declined`, `unavailable`, or `TBD`.
- Connector-map path and mapped capabilities when connector review ran.
- Connection state: `connected`, `needs-auth`, `declined`, `unavailable`, `failed`, `not-reviewed`, or `TBD`.
- One optional next step.

## Safety Rules

- Missing setup never blocks concrete business work.
- Setup requires acceptance before profile, connector, or memory checks.
- Creating or updating `~/.pipa/communication-style.md` requires separate explicit approval for the exact proposed write.
- First-time setup must not create tasks, reminders, automations, triggers, or recurring workflows.
- Save only confirmed profile facts; do not invent context or overwrite user-provided content.
- Do not write external memory or connect tools without the confirmation required by the owning operation.
- If `pipa-connectors` is unavailable, report that connector review could not run. Do not execute a copied connector workflow.
