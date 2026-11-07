---
name: pipa-keep-clients
description: "Use when the user wants Pipa to maintain client trust: follow-ups, check-ins, client health, retention, renewals, referrals, testimonials, stakeholder care, and relationship-sensitive next actions."
metadata:
  version: 0.2.0
---

# Pipa Keep Clients

Protect trust after and around delivery.

When present, read `~/.pipa/profile.md` once for durable business context. If missing, continue without blocking and do not start setup unless the user asks or a soft setup offer is useful.

## Use For

- Existing-client check-ins, relationship health, retention, renewals, referrals, and testimonials.
- Follow-up wording when the user wants to keep trust or recover momentum.
- Relationship risks surfaced by delivery or closeout.

## Starter Jobs

- Find who needs a check-in and why now.
- Draft or structure a follow-up. Send nothing by default.
- Surface stakeholder risk, client-health signals, renewal or retention opportunities, trust gaps, testimonials, and referrals.
- Treat generic `follow up with client` as client-retention follow-through, not reminder scheduling.

## Required Inputs

- Source: client notes, stakeholder map, thread, delivery state, support signal, or `TBD`.
- Objective: repair, nurture, unblock, renew, ask, thank, or `TBD`.
- Timing, owner, and channel, if known.

## Workflow

1. State the relationship objective and source.
2. Name the signal and why now.
3. Choose the smallest useful touch: check-in, clarification, escalation, thanks, renewal prompt, or no action.
4. Draft the next action when useful. Do not send.
5. Capture owner, timing, source, and watchlist.

## Output Contract

- Client or relationship signal.
- Why now.
- Suggested touch or ask.
- Owner and timing.
- Source/evidence or `TBD`.
- Watchlist items.

## Boundaries

- Existing-client trust, retention, renewal, testimonial, and referral asks belong here. Acquiring a new prospect or opportunity belongs to `pipa-get-work`.
- Relationship follow-up with an existing client belongs here; prospect and pipeline follow-up belongs to `pipa-get-work`.
- Invoice and payment follow-up belongs to `pipa-get-paid`, even when relationship-sensitive wording matters.
- Do not send messages or schedule reminders unless explicitly asked.
- One-shot self-email reminders go through `pipa-tools` to `pipa-follow-up-reminders`.
- Active delivery status stays `pipa-deliver-work` unless relationship health dominates.
- Use `composio-mcp` only for live email, CRM, calendar access, or an explicitly approved external send.
- Route future automated client-health checks to `pipa-manage` or `pipa-triggers`.
- Do not update CRM records or access an inbox without connected-tool approval.
- Relevant connector categories include CRM, email, chat, calendar, project tracker, and knowledge base.

## Supporting Methods

- `pipa-stakeholder-map`: role, influence, and decision authority.
- `pipa-status-update`: anchor updates in delivery reality.
- `pipa-risk-escalation`: trust, owner drift, and blocker escalation.
- `pipa-handover`: transition ownership.
- Load `references/examples/keep-clients.md` when an example shape helps.

## Gotchas

- Do not fake relationship history; mark unknown context as `TBD`.
- Generic follow-up is client work, not a reminder, unless future self-email wording is explicit.
- Testimonials, referrals, and renewals should be grounded in delivered value or client signal.
