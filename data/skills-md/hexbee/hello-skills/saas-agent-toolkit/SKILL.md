---
name: saas-agent-toolkit
description: Design agent-usable SaaS tool systems using six reusable tool shapes (Search, Summarize, Draft, Update, Notify, Approve) plus connectors and policy guardrails. Use when turning SaaS features into reliable agent actions with clear contracts, permissions, audit trails, and approval gates.
---

# SaaS Agent Toolkit

## Overview

Use this skill when a user asks how to make a SaaS product "agent-usable" rather than only human-usable.

This skill reframes product capabilities into a stable execution model:

1. Connectors layer: auth and event plumbing
2. Tools layer: six reusable tool shapes
3. Policy layer: permissions, approvals, and reliability guardrails

## Workflow

1. Scope target SaaS domain and entities.
2. Define the 3-layer architecture.
3. Map capabilities into the six tool shapes.
4. Add guardrails (auth, allowlists, idempotency, audit).
5. Produce a concrete rollout plan and KPI set.

## Step 1: Scope Domain

Capture:

- Product/system (for example Zendesk, Salesforce, Jira, Notion)
- Core entities (ticket, contact, issue, page, deal, order)
- High-risk actions (payment, delete, external publish, permission change)
- Success outcome (speed, quality, cost, reliability)

## Step 2: Build 3-Layer Architecture

Design these layers explicitly:

1. `Connectors`: OAuth/API key, webhook ingestion, identity mapping, optional SCIM.
2. `Tools`: Search, Summarize, Draft, Update, Notify, Approve.
3. `Policy & Guardrails`: RBAC, budgets, rate limits, PII controls, logging, retries.

Design principle:
Prefer predictable, auditable, rollback-safe operations over "smart but opaque" behavior.

## Step 3: Define Tool Contracts

Use six stable tool contracts:

1. `Search`: locate entities and relationships.
2. `Summarize`: produce structured, citation-backed takeaways.
3. `Draft`: generate submit-ready drafts without auto-sending.
4. `Update`: write bounded, idempotent changes back to systems.
5. `Notify`: close loops with owners/watchers/approvers.
6. `Approve`: enforce human gating for high-risk operations.

Read `references/tool-contracts.md` for function templates and I/O expectations.

## Step 4: Add Mandatory Guardrails

Apply all of the following:

- Explicit error taxonomy (`401`, `403`, `404`, `empty`, `conflict`, `timeout`)
- Idempotency key for mutating actions
- Field allowlist for `Update` (no unrestricted patch)
- Citation requirement for `Summarize`
- Dry-run and draft-only defaults for user-facing output
- Approval gates for high-risk categories
- Full audit trail: who requested, who approved, what changed, when, result

Read `references/approval-and-audit.md` for standard approval and audit schema.

## Step 5: Produce Deliverables

Return output in this structure:

1. Domain scope and entities
2. 3-layer architecture
3. Tool contract table (six tools)
4. Guardrail design
5. Example end-to-end workflow
6. Rollout plan (`0-30`, `31-90`, `90+` days)
7. KPI table
8. Top unresolved risk

KPI minimums:

- task completion rate
- first-call success
- API success rate
- p95 latency
- integration lead time
- unit outcome cost

## Example Workflow Patterns

Use `references/workflow-patterns.md` for ready-to-adapt flows:

- customer support triage and response
- sales follow-up automation
- incident assistant with approval-gated external updates
