---
name: inbox-commander
description: Email triage and organization system for Gmail. Use when user asks to "triage my inbox", "check my email", "process emails", "what needs my attention", "inbox zero", or any request to organize, classify, or act on emails. Provides GTD-style processing with autonomous actions for clear-cut items and surfaced decisions for ambiguous ones. Creates newsletter digests, drafts replies, and suggests bulk unsubscribes.
---

# Inbox Commander

Email triage using GTD: Do it now, Decide, Defer, or Dump.

## Tool Selection

**Check for gscli first** (faster, includes calendar/drive context):
```bash
which gscli && gscli auth status
```

If available and authenticated, use gscli for READ operations:
- `gscli gmail list` - List messages
- `gscli gmail read <id>` - Read message
- `gscli calendar list` - Get upcoming meetings
- `gscli drive search` - Find related docs

**Use Gmail MCP for WRITE operations** (gscli is read-only):
- Archive, label, snooze, create drafts, create filters

**Fallback**: If gscli unavailable, use Gmail MCP for everything.

## Triage Scope

Process ALL unarchived mail (Inbox), regardless of read state:
- Unread + unarchived = definitely needs attention
- Read + unarchived = user saw it but didn't act (still needs triage)
- Archived = processed/done → ignore
- Snoozed (label: `snooze/YYYY-MM-DD`) → ignore until date passes

## Execution Flow

```
1. Check tool availability (gscli vs MCP-only)
2. Load references:
   - learned-rules.md (corrections take precedence)
   - known-senders-private.md (if exists) or known-senders.md
3. Check snoozed items → unsnooze if date passed
4. Fetch emails (Inbox, regardless of read state)
5. Fetch context: calendar, Linear (graceful fail)
6. For each email:
   a. Already labeled by Gmail filter? → Validate, compute urgency
   b. Unlabeled? → Classify, apply label, track pattern
   c. Invoice/Bill detected? → Validate, flag validity, surface for approval
7. Execute Tier 1 actions (no approval needed)
8. Aggregate Tier 2 → create newsletter digest
9. Process invoices → validate, present for approval, forward if approved
10. Present triage summary grouped by computed urgency
11. Await decisions → execute → log corrections
12. Suggest new Gmail filters if patterns emerged
```

## Label System

### Philosophy

**Labels = stable categorization** (stored on email)
**Urgency = dynamic computation** (calculated fresh each run)

Urgency changes constantly (Monday's "this week" becomes Friday's "today"). Don't label urgency — compute it based on context.

### Hybrid Approach

Gmail filters handle deterministic patterns instantly at delivery. AI handles unlabeled items and suggests new filters when patterns emerge.

**If email is already labeled** (by Gmail filter):
- Validate the label is correct
- Focus on computing urgency and action state
- Don't re-classify unless label seems wrong

**If email is unlabeled:**
- Classify and apply appropriate label
- Track the pattern (sender, subject)
- After 3+ similar classifications → suggest Gmail filter

### Label Structure

Create labels if missing. Use Gmail MCP `get_or_create_label`.

**Content Bundles** (for Simplify Gmail visual grouping):
- `Newsletters` - digested content, auto-archive after
- `Receipts` - payment confirmations, auto-archive
- `Bills` - invoices awaiting payment (never auto-archive)
- `Bills/Queued` - invoices forwarded to Brex for payment
- `Bills/Crypto-Pending` - crypto invoices awaiting manual payment
- `Bills/Paid` - paid invoices (audit trail)
- `Notifications` - tool notifications, auto-archive (unless error)
- `Transactional` - shipping, confirmations

**Entity Types** (for rules + search):
- `Team` - internal team domains
- `Investors` - known investor contacts
- `Legal` - law firms, legal matters
- `Vendors` - payroll, finance, contractors

**Action State** (workflow tracking):
- `ic/needs-response` - user owes a reply
- `ic/waiting-on` - ball in their court
- `ic/scheduled` - has follow-up date
- `ic/processed` - audit trail (apply before archiving)

**Snooze** (time-based deferral):
- `snooze/YYYY-MM-DD` - hide until this date

## Urgency Tiers (Computed, Not Labeled)

Compute urgency fresh each run based on context:

**🔴 TODAY** - Surface immediately
- Explicit deadline today or overdue
- Error/failure notifications
- Sender you're meeting today (check calendar)
- Follow-up on something already escalated
- Team + needs-response older than 24h

**🟡 THIS WEEK** - Surface prominently
- Deadline this week
- Investors + needs-response
- Legal + needs-response
- Important sender waiting 2+ days

**🟢 SOMETIME** - Surface in list
- No deadline, low stakes
- Vendors with non-urgent questions
- Requests that can wait

**⚪ FYI** - Mention briefly or skip
- Informational only, no action needed
- Already handled, just confirming

## Classification Tiers

### Tier 1: Auto-Action (No Approval)

| Pattern | Action |
|---------|--------|
| Payment confirmations | Label: Receipts → Archive |
| Calendar responses (Accepted/Declined/Tentative) | Archive |
| Tool notifications | Label: Notifications → Archive |
| Misrouted (wrong recipient, user not CC'd) | Archive + note |

**Escalate to Tier 3** if contains: "failed", "error", "action required", "urgent", "security alert"

### Tier 2: Newsletter Digest

Match: `*@substack.com`, `*@tldrnewsletter.com`, `*@beehiiv.com`, known senders (see `references/known-senders.md`)

Action: Label: Newsletters → Summarize → Archive originals

Output: Create digest with top stories, key insights. Digest is the deliverable; originals archived for reference.

### Tier 3: Surface for Decision

- Team emails (unless purely informational)
- Starred messages (user's hot list — never auto-modify)
- Investors, Legal, important Vendors
- Anything with `ic/needs-response` label
- Anything ambiguous

### Tier 4: Elimination Candidates

- Cold outreach (first contact + sales language patterns)
- Marketing drip campaigns from tools not in use
- Mailing lists with zero engagement
- Batch for bulk unsubscribe offer

## Output Format

Keep it scannable. Group by computed urgency:

```
🔴 TODAY (2)
├── **Alex** [Team] - Q1 budget review needs sign-off by EOD
│   Labels: Team, ic/needs-response
│   Context: You're meeting them at 2pm
│   → [Draft response] [Snooze 2h] [Mark waiting-on]
│
└── **Justworks** [Vendors] - Payroll processing failed
    Labels: Vendors, ic/needs-response
    Context: Payroll due today, $102K
    → [Draft response] [Call 888-534-1711]

🟡 THIS WEEK (3)
├── **Cooley** [Legal] - Stock option docs for review
│   Labels: Legal, ic/needs-response
│   → [Draft response] [Snooze to Monday]
...

🟢 SOMETIME (5)
├── **Random Vendor** - Quarterly review request
│   → [Draft polite decline] [Snooze 2 weeks]
...

✅ AUTO-PROCESSED
- Archived: 3 calendar responses, 2 receipts, 4 notifications
- Labels applied: 2 new Team, 1 new Vendors

📰 NEWSLETTER DIGEST
- 6 newsletters summarized → [View digest]
- Archived originals

🗑️ ELIMINATION CANDIDATES (4)
- sales@random-saas.com (3 emails, cold outreach)
- marketing@tool-you-dont-use.com (5 emails, drip)
→ [Unsubscribe all] [Select individually] [Skip]
```

## Snooze Handling

When user requests snooze:
1. Apply label: `snooze/YYYY-MM-DD`
2. Remove from inbox (archive)
3. Apply `ic/scheduled` label

On future triage runs, check snoozed items:
- If today >= snooze date → remove snooze label, move back to inbox
- Otherwise → ignore

## Draft Creation

When user approves a draft:
1. Create Gmail draft via MCP (appears in Gmail Drafts folder)
2. Show draft content in response
3. Provide: [Send now] [Edit first] [Discard]

**Never send without explicit "send" or "yes send it" confirmation.**

## Invoice/Bill Processing

When an email is detected as an invoice or bill that requires manual payment action.

### Scope: Manual-Pay Invoices Only

**SKIP this flow for auto-pay items:**
- Vendors on auto-pay/autopay (check `known-senders.md` for `autopay: true`)
- Subscriptions with card on file (AWS, GCP, SaaS tools)
- Recurring charges that auto-debit
- Payment confirmations (these are Receipts, not Bills)

**PROCESS through this flow:**
- Invoices requiring manual approval/payment
- New vendors not yet on auto-pay
- One-time or irregular invoices
- Invoices where payment method needs selection

### Detection

Trigger invoice flow when email contains:
- Subject: "invoice", "bill", "payment due", "amount due", "statement"
- From: invoices@*, billing@*, ar@*, or known billing platforms (QuickBooks, FreshBooks, Bill.com, Xero)
- Body: Invoice numbers, amounts due, due dates, payment terms

**AND** sender is NOT marked as `autopay: true` in known-senders.md.

### Validation

For each invoice, assess validity:

**✅ LOOKS VALID** - All conditions met:
- Sender domain matches known vendor in `known-senders.md`
- Amount consistent with prior invoices (±10%)
- Invoice format matches vendor's history
- No red flags present

**🚩 SUSPICIOUS** - One or more concerns:
- First invoice from this sender
- Amount differs significantly from history
- Bank details changed without prior notice
- Pressure tactics or unusual urgency
- Domain similar but not exact match (typosquatting)

**⛔ LIKELY FRAUD** - Reject signals present:
- Unexpected wire transfer demands from known ACH vendor
- Personal payment accounts (Venmo, personal PayPal) for business invoice
- "Bank details changed" claims without context
- Typosquatted domain pretending to be known vendor

### Payment Method Detection

Invoices may require different payment methods. **Validation applies to ALL payment types.**

**💳 STANDARD (Brex)** - Default for most vendors:
- ACH, wire, check, card payment
- If valid → forward to bills@brex.com

**🪙 CRYPTO/USDC** - Separate payment flow:
- Invoice explicitly requests USDC, USDT, ETH, or other crypto
- Vendor is known crypto-native service (check known-senders.md for `payment: crypto`)
- If valid → present "Pay via crypto wallet" (NOT forwarded to Brex)
- Still validate for fraud - crypto invoices can be fraudulent too

**⚠️ Note:** Crypto payment request from a vendor that normally takes USD is a RED FLAG. Crypto request from a known crypto-native vendor is expected.

### Output Format

```
💰 INVOICES REQUIRING APPROVAL (2)

📄 AWS - $2,847.23 [AUTO-PAY - No action needed]
   Just FYI: Card on file will be charged
   → [Note only]

📄 Legal Firm LLP - $12,500.00 💳
   Invoice #: INV-2025-0042
   Due: Jan 25, 2025
   Validation: ✅ LOOKS VALID
   Confidence: HIGH
   Reason: Known vendor, consistent with retainer amount
   Payment: ACH/Wire
   Prior invoices: 6 (avg: $12,500/mo)
   → [Approve & forward to Brex] [Review first] [Reject]

📄 Web3 Infra Co - $5,000.00 🪙
   Invoice #: 2025-01-001
   Due: Jan 20, 2025
   Validation: ✅ LOOKS VALID
   Confidence: HIGH
   Reason: Known crypto-native vendor, USDC payment expected
   Payment: USDC (expected for this vendor)
   Prior invoices: 3 (avg: $5,000/mo)
   → [Pay via USDC] [Review first] [Reject]

📄 Acme Consulting - $15,000.00 🚩
   Invoice #: 2025-001
   Due: Jan 20, 2025
   Validation: 🚩 SUSPICIOUS
   Confidence: LOW
   Reason: First invoice from this sender, no prior relationship found
   Payment: Wire requested
   Prior invoices: 0
   → [Review carefully] [Request verification] [Reject]
```

### Brex Forwarding (Standard Payment)

When user approves a valid invoice for standard payment:
1. Confirm approval explicitly: "Forward Legal Firm invoice ($12,500) to bills@brex.com for payment?"
2. On confirmation, forward the original email to `bills@brex.com`
3. Apply label: `Bills/Queued`
4. Log action: "Forwarded to Brex: [vendor] $[amount] Invoice #[number]"

**Forward email format:**
```
To: bills@brex.com
Subject: Fwd: [Original subject]
Body: [Original email content]
```

**Never auto-forward** - Always require explicit approval per invoice.

### Crypto Payment Handling

When user approves a crypto invoice:
1. Confirm: "Pay Web3 Infra Co $5,000 via USDC?"
2. Present wallet/payment details from invoice
3. Apply label: `Bills/Crypto-Pending`
4. User executes payment manually
5. After confirmation, apply label: `Bills/Paid`

### Invoice History Tracking

Track invoice history for validation:
- Store in `references/invoice-history.md` (create if missing)
- Log: date, vendor, amount, invoice number, validation result, payment method
- Use history to establish "normal" patterns per vendor

## Bulk Unsubscribe

For Tier 4 items:
1. Extract unsubscribe links (List-Unsubscribe header or body link)
2. Present as batch: "Found 5 unsubscribe links. Execute all?"
3. On approval, open each link or send unsubscribe request
4. Log results

## Rule Suggestions (AI Training the System)

Track patterns in unlabeled emails that AI classifies. When a pattern emerges, suggest Gmail filter creation.

**Suggest new Gmail filter when:**
- Same sender domain classified 3+ times with same label
- Same subject pattern classified 3+ times
- New vendor/service appears repeatedly

**Output format for suggestions:**
```
📋 SUGGESTED GMAIL FILTERS

Based on patterns I've seen:

1. from:*@cooley.com → Legal
   (classified 5 emails this way, 100% match)
   → [Create filter] [Ignore] [Add to known senders]

2. from:*@srsacquiom.com → Vendors
   (classified 3 emails, shareholder notices)
   → [Create filter] [Ignore]

3. subject:"Your order" from:*@amazon.com → Receipts
   (classified 8 emails)
   → [Create filter] [Ignore]
```

**Suggest unsubscribe/block rules when:**
- Sender classified as Tier 4 (cold outreach) 2+ times
- Newsletter with 0 opens for 30+ days
- Marketing drip from tool not in use

## Learning from Corrections

When user overrides AI classification:
- Log the correction to `references/learned-rules.md`
- Apply learned rules before default classification on future runs
- If pattern becomes clear, suggest filter

Example correction log:
```
You archived "SRS Acquiom" despite HIGH urgency classification.
→ Noted: Shareholder notices from SRS Acquiom = FYI only
→ Suggest filter: from:*@srsacquiom.com subject:shareholder → auto-archive?
```

## Context Integrations

### Calendar (gscli or MCP)
- Flag emails from people you're meeting today/tomorrow
- Detect deadline language ("by Friday", "EOD")

### Linear (MCP)
- Link emails mentioning project names
- Note if sender is assigned to active project

### Drive (gscli)
- If email references a doc, check if it exists in Drive

All optional. Graceful fail. Note status at end: "Calendar: connected | Linear: unavailable"

## Rules

- NEVER auto-send emails. Always save as draft.
- For drafts, show content and offer: [Send] [Edit] [Discard]
- Apply `ic/processed` label before archiving (audit trail)
- Log all actions for review
- Ask before any destructive action (delete, unsubscribe)
- When in doubt, surface it (Tier 3) rather than auto-process

### Invoice-Specific Rules

- NEVER auto-forward invoices to bills@brex.com - always require explicit approval
- NEVER auto-pay crypto invoices - always surface for manual payment
- Flag ALL invoices with validity assessment (valid/suspicious/fraud)
- Crypto invoices get same fraud validation as standard invoices
- Skip invoice flow for vendors marked `autopay: true` in known-senders
- Log all invoice actions to `references/invoice-history.md`

## References

- `references/classification-rules.md` - Detailed patterns for each tier
- `references/known-senders.md` - VIPs, team, newsletter sources (template)
- `references/known-senders-private.md` - Personal overrides (if exists, takes precedence)
- `references/learned-rules.md` - Corrections from past runs (auto-generated)
- `references/invoice-history.md` - Invoice history for validation (auto-generated)
