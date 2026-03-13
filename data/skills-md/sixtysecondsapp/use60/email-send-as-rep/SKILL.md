---
name: Email Send-as-Rep
description: |
  Compose and send real emails from the rep's connected Gmail or Office 365 account.
  This skill sends actual emails that appear in the rep's Sent folder and are
  indistinguishable from emails the rep typed themselves. Every email requires
  explicit human approval before sending -- there are zero exceptions.
  Use when someone says "send this email", "email them the follow-up",
  "reply to their last message", "send the proposal over", "draft and send",
  "fire off that email", or "email [contact name]".
  Do NOT use for drafting emails without sending (use followup-reply-drafter instead),
  internal team emails, or marketing/bulk email campaigns.
metadata:
  author: sixty-ai
  version: "1"
  category: sales-ai
  skill_type: atomic
  is_active: true
  command_centre:
    enabled: true
    label: "/email"
    description: "Draft an email from task context"
    icon: "mail"
  agent_affinity:
    - outreach
    - pipeline
  triggers:
    - pattern: "send this email"
      intent: "send_email"
      confidence: 0.95
      examples:
        - "send that email"
        - "send the email"
        - "go ahead and send it"
        - "send this to them"
    - pattern: "email them"
      intent: "email_contact"
      confidence: 0.90
      examples:
        - "email this person"
        - "email the client"
        - "shoot them an email"
        - "email [name]"
    - pattern: "send the follow-up"
      intent: "send_followup"
      confidence: 0.90
      examples:
        - "send that follow-up"
        - "fire off the follow-up"
        - "send the follow-up email"
        - "send my follow-up"
    - pattern: "reply to their email"
      intent: "send_reply"
      confidence: 0.85
      examples:
        - "reply to this thread"
        - "respond to their message"
        - "send a reply"
        - "write back to them"
    - pattern: "send the proposal over"
      intent: "send_document"
      confidence: 0.80
      examples:
        - "send them the deck"
        - "email the proposal"
        - "send the quote"
        - "forward this to the client"
  keywords:
    - "email"
    - "send"
    - "gmail"
    - "follow-up"
    - "reply"
    - "compose"
    - "draft"
    - "outreach"
    - "inbox"
  required_context:
    - user_email_connection
    - recipient_email
  inputs:
    - name: to
      type: string
      description: "Recipient email address or contact name to resolve"
      required: true
    - name: subject
      type: string
      description: "Email subject line (auto-generated for replies using Re: prefix)"
      required: false
    - name: body
      type: string
      description: "Email body content (plain text or HTML)"
      required: true
    - name: thread_id
      type: string
      description: "Gmail/O365 thread ID for replies (loads thread context automatically)"
      required: false
    - name: approval_id
      type: string
      description: "Pre-existing approval ID from Slack HITL flow (skips re-approval)"
      required: false
    - name: cc
      type: array
      description: "CC recipients (email addresses or contact names)"
      required: false
    - name: bcc
      type: array
      description: "BCC recipients (email addresses or contact names)"
      required: false
    - name: send_later_at
      type: string
      description: "ISO 8601 timestamp for scheduled send (respects quiet hours)"
      required: false
  outputs:
    - name: sent_message_id
      type: string
      description: "Gmail/O365 message ID of the sent email"
    - name: delivery_status
      type: string
      description: "Status: sent, scheduled, cancelled, failed, pending_approval"
    - name: audit_record
      type: object
      description: "Full audit trail including approval timestamp, approver, and body hash"
    - name: thread_id
      type: string
      description: "Thread ID (returned for threading future replies)"
  requires_capabilities:
    - gmail_send
    - email
  priority: critical
  tags:
    - sales
    - email
    - outreach
    - gmail
    - office365
    - communication
    - follow-up
    - send
---

## Available Context
@_platform-references/org-variables.md

# Email Send-as-Rep

## THE CARDINAL RULE

This skill sends real emails from a real person's inbox. Every email MUST be explicitly approved by the rep before sending. There are ZERO exceptions to this rule.

- No auto-send.
- No batch send.
- No "smart auto-approve."
- No "the rep said it was okay last time."
- No "it's just a follow-up."
- No "the sequence configured it."

**Every. Single. Email. Gets. Human. Approval.**

If the approval system is down, emails do not send. If Slack is unreachable, emails do not send. If there is any ambiguity about whether the rep approved, emails do not send. The default state is NOT SENDING. Sending requires an affirmative, auditable human action.

This is not a safety feature you can relax later. This is the foundation the entire skill is built on. Violating this rule is a career-ending event for the rep whose inbox was used without consent.

## Context Sources

Before composing or sending anything, load all available context. The quality of the email depends entirely on the quality of the context feeding it.

### Source 1: Email Connection (Required)

The rep must have an active OAuth connection to Gmail or Office 365. Check:

- **OAuth token** -- valid, not expired, correct scopes
- **Required scopes** -- `gmail.send` (Gmail) or `Mail.Send` (O365)
- **Email address** -- the From address that will appear on the sent email
- **Display name** -- the sender name that will appear (e.g., "Sarah Chen")
- **Connection status** -- last successful API call timestamp

If the connection is missing or expired, STOP. Do not compose the email. Prompt the rep to reconnect their email account. See `references/safety-rails.md` for re-authorization flow.

### Source 2: Rep's Email Signature

Load the rep's email signature from their profile or email settings. This is appended to every outbound email.

- Check `user_settings` for a stored signature
- If none stored, fetch the signature from Gmail API (`users.settings.sendAs`)
- If the rep has multiple signatures, use the one marked as default
- Never compose an email without a signature -- it looks like spam

### Source 3: Thread History (for replies)

If `thread_id` is provided, load the full thread:

- All messages in the thread (sender, timestamp, body)
- The most recent message (this is what we're replying to)
- Original subject line (for Re: prefix)
- All participants (To, CC, BCC from the most recent message)
- Message-ID and References headers (for proper threading)

Thread context ensures the reply is relevant, avoids repeating information already shared, and maintains proper email threading so the reply appears in the same conversation in the recipient's inbox.

### Source 4: CRM Contact Record

Look up the recipient in the CRM:

- Contact name, title, company
- Relationship history (last meeting, last email, deal stage)
- Communication preferences (if stored in copilot memory)
- Any notes or tags relevant to tone or content
- Previous email interactions (what was discussed, what was promised)

### Source 5: Rep's Writing Style (Copilot Memory)

Check copilot memory for the rep's communication style:

- Typical greeting style ("Hi Sarah," vs "Hey Sarah," vs "Sarah,")
- Sign-off preference ("Best," vs "Thanks," vs "Cheers,")
- Formality level (casual, professional, enterprise)
- Common phrases or patterns they use
- Length preference (brief vs detailed)

If no style profile exists, default to professional tone and note that the style will improve as the system learns.

## Step 1: Validate Prerequisites

Before composing anything, run every validation check. If any check fails, stop and report the specific failure to the rep. Do not partially compose. Do not "try anyway."

### 1.1 Email Connection Active

```
CHECK: user_email_connections WHERE user_id = rep AND provider IN ('gmail', 'office365')
VERIFY: token_expires_at > NOW()
VERIFY: scopes INCLUDE 'gmail.send' OR 'Mail.Send'
```

If expired: "Your Gmail connection has expired. Please reconnect at Settings > Integrations > Gmail to send emails."

If missing scope: "Your Gmail connection doesn't include send permissions. Please reconnect and grant the 'Send email' permission."

### 1.2 Recipient Email Valid

```
VALIDATE: recipient_email matches RFC 5322 format
VALIDATE: domain has MX records (basic deliverability check)
VALIDATE: email is not in organization's suppression list
VALIDATE: email is not a role address (no-reply@, postmaster@, abuse@) unless explicitly intended
```

If invalid format: "The email address '[address]' doesn't look right. Can you double-check it?"

If suppressed: "This email address is on the suppression list. It was marked as do-not-contact on [date]. Remove it from the suppression list first if you want to proceed."

### 1.3 Daily Send Limit Not Exceeded

```
CHECK: daily_email_sends WHERE user_id = rep AND sent_date = TODAY
COMPARE: count < daily_limit (default: 50, configurable per org)
```

If exceeded: "You've sent [count] emails today, which is at your daily limit of [limit]. This protects your sender reputation. The limit resets at midnight. Contact your admin to adjust the limit."

### 1.4 Not in Quiet Hours

```
CHECK: user_settings.quiet_hours WHERE user_id = rep
IF current_time WITHIN quiet_hours:
  OPTION A: Queue for delivery at quiet_hours_end
  OPTION B: Inform rep and let them override
```

If in quiet hours: "It's currently [time] which is within your quiet hours ([start]-[end]). Would you like to schedule this email for [quiet_hours_end] instead, or send it now anyway?"

### 1.5 Cost Budget Not Exceeded

```
CHECK: ai_usage WHERE user_id = rep AND period = current_billing_period
VERIFY: total_cost < budget_limit
```

If exceeded: "Your AI usage budget for this period has been reached. Contact your admin to increase the limit."

### 1.6 Recipient Not Recently Emailed (Spam Prevention)

```
CHECK: sent_emails WHERE to = recipient AND sent_at > NOW() - INTERVAL '4 hours'
IF found: WARN rep about recent send
```

If recently emailed: "You sent an email to [recipient] [time] ago. Are you sure you want to send another one? Sending too frequently can feel pushy."

## Step 2: Compose the Email

Once all prerequisites pass, compose the email. The composition process differs for replies vs new emails. See `references/email-composition.md` for technical formatting rules.

### 2.1 Reply to Existing Thread

When `thread_id` is provided:

1. **Load the thread** -- fetch all messages, identify the most recent
2. **Set threading headers** -- `In-Reply-To` and `References` headers from the last message's `Message-ID`. This is critical for threading. See `references/email-composition.md` for header format.
3. **Set subject** -- `Re: [original subject]` (do not stack Re: Re: Re:)
4. **Set recipients** -- default to Reply (sender only) unless rep specifies Reply All
5. **Compose body** -- reference the thread context, respond to what was said, advance the conversation
6. **Quote the previous message** -- include the quoted reply block below the new content (standard email convention)
7. **Append signature** -- after the body, before the quoted content

### 2.2 New Email (No Thread)

When composing fresh:

1. **Set subject** -- concise, specific, no clickbait. Good: "Meeting follow-up: pricing discussion". Bad: "Quick question" or "Checking in"
2. **Set recipients** -- resolve contact names to email addresses via CRM lookup
3. **Compose body** -- use the rep's writing style, reference relevant CRM context
4. **Append signature** -- at the end of the body

### 2.3 Writing Style Application

Apply the rep's writing style from copilot memory:

- **Greeting** -- use the rep's preferred greeting. If the recipient is in the CRM and has a preferred name, use it.
- **Tone** -- match the formality level from the rep's style profile. If replying to a thread, also match the tone of the conversation.
- **Length** -- match the rep's typical email length. If the rep writes short emails, don't generate a novel. If they're detailed, don't be terse.
- **Sign-off** -- use the rep's preferred closing.
- **Vocabulary** -- use words the rep actually uses. Don't insert corporate jargon they'd never say.

If the rep provided the body content directly (e.g., "send this exact email"), use their content verbatim. Do not rewrite, polish, or "improve" content the rep wrote themselves. Only append the signature.

### 2.4 Content Safety Checks

Before presenting for approval, scan the composed email:

- **No placeholder text** -- no `[NAME]`, `${variable}`, `{{merge_field}}` remnants
- **No internal references** -- no mention of CRM tools, AI assistance, copilot, or internal systems
- **No confidential data leaks** -- no other clients' information, no internal pricing notes, no team Slack conversations
- **No broken links** -- validate any URLs included in the body
- **Correct recipient** -- double-check the To address matches the intended contact (easy to confuse similar names)
- **Appropriate content** -- no profanity, no offensive content, no legal claims the rep shouldn't make

If any check fails, flag the specific issue and do not proceed to approval.

## Step 3: Present for Approval via Slack

The composed email is presented to the rep for approval through the Slack HITL (Human-in-the-Loop) flow. This is not optional. This is not skippable. This is the gate.

### 3.1 Build the Approval Message

Construct a Slack Block Kit message with:

```
┌─────────────────────────────────────────────────────────┐
│  Email Ready to Send                                     │
│                                                          │
│  From: Sarah Chen <sarah@company.com>                    │
│  To: john.smith@prospect.com                             │
│  Subject: Meeting follow-up: pricing discussion          │
│                                                          │
│  ── Preview ──────────────────────────────────────────    │
│  Hi John,                                                │
│                                                          │
│  Great speaking with you earlier today. As discussed,    │
│  here's the pricing breakdown for the Growth tier...     │
│                                                          │
│  [Body truncated -- click "View Full Email" for more]    │
│  ── End Preview ──────────────────────────────────────    │
│                                                          │
│  ┌──────────┐ ┌──────────────┐ ┌──────────┐ ┌────────┐  │
│  │ Send Now │ │ Edit in use60│ │Send Later│ │ Cancel │  │
│  └──────────┘ └──────────────┘ └──────────┘ └────────┘  │
│                                                          │
│  Approval expires in 30 minutes                          │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Approval Actions

| Button | Action | Result |
|--------|--------|--------|
| **Send Now** | Approve and send immediately | Triggers Step 4 (with undo window) |
| **Edit in use60** | Open email editor in the web app | Rep can modify before re-submitting |
| **Send Later** | Schedule for a specific time | Prompts for date/time, then queues |
| **Cancel** | Reject the email | Email is discarded, logged as cancelled |

### 3.3 Approval Record

When the rep clicks any button, record:

```
slack_pending_actions:
  action_type: 'email_send_approval'
  payload: { to, subject, body_hash, thread_id }
  created_at: NOW()
  expires_at: NOW() + INTERVAL '30 minutes'
  status: 'pending' | 'approved' | 'rejected' | 'expired'
  resolved_by: user_id (from Slack identity)
  resolved_at: timestamp
```

### 3.4 Expiration

If no action is taken within 30 minutes:

- Set status to `expired`
- Update the Slack message: "This email approval has expired. Run the command again to re-send."
- Do NOT send the email
- Log the expiration in the audit trail

### 3.5 No Slack Fallback

If Slack is not connected or unreachable:

- Present the approval in the copilot chat interface instead
- Use the standard preview-confirm HITL pattern (is_simulation: true -> pending_action -> confirm)
- The approval requirements are identical -- the channel changes, the rules do not

## Step 4: On Approval -- Send

When the rep clicks "Send Now" (or confirms via copilot chat), begin the send sequence.

### 4.1 Undo Window (30 Seconds)

Immediately after approval, start a 30-second undo window:

1. Update Slack message: "Sending in 30 seconds... [Cancel Send]"
2. Start countdown timer
3. If rep clicks "Cancel Send" within 30 seconds:
   - Cancel the send
   - Update Slack: "Email cancelled. Not sent."
   - Log as `cancelled_during_undo`
4. If 30 seconds pass without cancellation, proceed to send

The undo window exists because humans click buttons by accident. It's a lightweight safety net that costs nothing and prevents real harm.

### 4.2 Send via Gmail API

Execute the send through the rep's connected Gmail account:

```
POST https://gmail.googleapis.com/gmail/v1/users/me/messages/send
Authorization: Bearer {rep_oauth_token}
Content-Type: application/json

{
  "raw": base64url_encoded_rfc2822_message
}
```

The email MUST:
- Appear in the rep's Sent folder (this happens automatically with Gmail API)
- Use the rep's email address as From
- Use the rep's display name as the sender name
- Include proper threading headers if it's a reply
- Include the rep's signature
- Be encoded as UTF-8

See `references/email-composition.md` for the full RFC 2822 message format.

### 4.3 Send via Office 365 API

For O365-connected reps:

```
POST https://graph.microsoft.com/v1.0/me/sendMail
Authorization: Bearer {rep_oauth_token}
Content-Type: application/json

{
  "message": {
    "subject": "...",
    "body": { "contentType": "Text", "content": "..." },
    "toRecipients": [{ "emailAddress": { "address": "..." } }]
  },
  "saveToSentItems": true
}
```

### 4.4 Post-Send Slack Update

After successful send:

- Update the Slack message to remove all buttons
- Replace with: "Sent at [time] to [recipient]"
- Add a checkmark indicator
- The undo window is now closed -- indicate this clearly

### 4.5 Send Failure Handling

If the send API call fails:

1. **OAuth expired during send** -- the token expired between approval and send
   - Attempt silent token refresh using the refresh_token
   - If refresh succeeds, retry the send once
   - If refresh fails, notify rep: "Your Gmail connection expired. Please reconnect and try again."
   - Log as `send_failed_oauth_expired`

2. **Rate limit hit** -- Gmail API rate limit (250 sends/day for workspace, 500 for paid)
   - Queue the email for retry in 1 hour
   - Notify rep: "Gmail rate limit reached. Email queued for delivery in 1 hour."
   - Log as `send_failed_rate_limit`

3. **Recipient rejected** -- mailbox full, address doesn't exist, etc.
   - Notify rep with the specific bounce reason
   - Log as `send_failed_recipient_rejected`
   - Update CRM contact record with bounce status

4. **Network error** -- timeout, connection refused, etc.
   - Retry once after 10 seconds
   - If retry fails, notify rep: "Email send failed due to a network error. Please try again."
   - Log as `send_failed_network`

5. **Unknown error** -- anything else
   - Do NOT retry automatically (unknown errors could indicate account issues)
   - Notify rep with error details
   - Log as `send_failed_unknown` with full error payload

## Step 5: Post-Send Processing

After the email is successfully sent, execute all post-send tasks. These are important for maintaining data integrity but must not block the rep's workflow. Run them asynchronously.

### 5.1 Audit Logging

Create a comprehensive audit record. See `references/safety-rails.md` for full audit requirements.

```
sequence_jobs:
  job_type: 'email_send'
  user_id: rep_user_id
  contact_id: recipient_contact_id
  status: 'completed'
  metadata: {
    to: recipient_email,
    cc: [...],
    bcc: [...],
    subject: subject_line,
    body_hash: SHA256(body),  -- NOT the plaintext body
    thread_id: thread_id,
    sent_message_id: gmail_message_id,
    sent_at: ISO8601_timestamp,
    approved_by: rep_user_id,
    approved_at: ISO8601_timestamp,
    approval_channel: 'slack' | 'copilot_chat',
    approval_latency_seconds: time_between_preview_and_approval,
    undo_window_used: boolean,
    send_method: 'gmail_api' | 'office365_api',
    composition_source: 'ai_generated' | 'rep_provided' | 'template',
    style_profile_applied: boolean
  }
```

### 5.2 CRM Activity Record

Create an activity record in the CRM:

```
activities:
  user_id: rep_user_id
  contact_id: recipient_contact_id
  deal_id: associated_deal_id (if applicable)
  activity_type: 'email_sent'
  title: 'Email: [subject_line]'
  description: body_preview (first 200 characters)
  metadata: { sent_message_id, thread_id }
  created_at: NOW()
```

### 5.3 Email Thread Sync

If the organization uses local email sync:

- Trigger a sync for the rep's sent folder
- Ensure the new message appears in the local email index
- Update thread metadata (last_message_at, message_count)

### 5.4 Daily Send Counter

Increment the rep's daily send counter:

```
daily_email_sends:
  user_id: rep_user_id
  sent_date: TODAY
  count: count + 1
  last_sent_at: NOW()
```

### 5.5 Sequence Update (if applicable)

If this email was part of a sales sequence:

- Mark the sequence step as completed
- Advance to the next step (or mark sequence as complete)
- Update sequence metrics (sent count, response tracking)

### 5.6 Contact Engagement Tracking

Update the contact's engagement timeline:

- Last contacted date
- Email frequency (for future spam prevention checks)
- Thread continuity (is this an ongoing conversation or cold outreach?)

## Quality Check

Before any email reaches the approval stage, verify:

- [ ] Rep's email signature is present and correctly formatted
- [ ] Threading headers are correct (In-Reply-To, References) for replies
- [ ] Subject line is appropriate (not blank, not all caps, not clickbait)
- [ ] Recipient email address is valid and not suppressed
- [ ] No PII from other contacts leaked into this email
- [ ] No internal system references visible in the body
- [ ] No placeholder or template variables remain unresolved
- [ ] Body length is reasonable (not empty, not excessively long)
- [ ] Character encoding is UTF-8 throughout
- [ ] Links in the body are valid and point to expected destinations
- [ ] CC/BCC recipients are intentional (not auto-populated incorrectly)
- [ ] The email makes sense as a standalone message OR as a reply in thread context
- [ ] Audit record captures all required fields
- [ ] Approval was explicitly granted by the rep (not inferred, not assumed)

## Error Handling

### "The rep's Gmail isn't connected"

Do not attempt to compose the email. Respond with:
"You need to connect your Gmail account before I can send emails on your behalf. Go to Settings > Integrations > Gmail and connect your account. Make sure to grant the 'Send email' permission when prompted."

### "The recipient email bounced"

Record the bounce, update the contact record, and inform the rep:
"The email to [address] bounced: [reason]. I've updated their contact record. Would you like to try a different email address?"

### "The rep wants to send to multiple recipients"

This skill sends one email at a time. For multiple recipients:
- If it's one email with multiple To/CC: supported, compose as normal
- If it's separate personalized emails to different people: run the skill once per recipient
- Never batch-send. Never mail-merge. Each email gets its own approval.

### "The email content was generated by another skill"

Common flow: `followup-reply-drafter` generates content, then `email-send-as-rep` sends it. The handoff works like this:
1. The drafting skill produces the email body
2. The rep reviews the draft (first approval gate -- content)
3. `email-send-as-rep` takes the approved content and presents it for send approval (second approval gate -- sending)
4. Both approvals are required. The content approval does NOT count as send approval.

### "The rep wants to send right now, skip approval"

No. Re-read THE CARDINAL RULE. There is no "skip approval" path. There is no "trusted sender" mode. There is no admin override for approval. The approval step is architecturally mandatory. If a rep asks to skip it, explain why it exists: "Every email sent from your inbox gets your approval first. This protects you from AI mistakes, wrong recipients, and content you wouldn't have written. It takes 2 seconds to approve."

### "OAuth token expired mid-conversation"

If the token expires between composition and send:
1. Attempt silent refresh using the stored refresh_token
2. If refresh succeeds, continue transparently
3. If refresh fails, inform the rep: "Your Gmail connection needs to be refreshed. Please click [reconnect link] and I'll retry the send."
4. Store the composed email in pending state so the rep doesn't lose their work

### "Rate limit reached"

Gmail enforces sending limits:
- Google Workspace: 2,000 emails/day (but we cap at 50 by default for safety)
- Consumer Gmail: 500 emails/day

If the platform daily limit is reached, do not queue silently. Inform the rep and let them decide:
"You've hit your daily send limit of [limit] emails. This resets at midnight [timezone]. Would you like me to schedule this for tomorrow morning?"

### "Slack is down during approval"

Fall back to the copilot chat approval flow. The rules are identical:
1. Present the full email preview in chat
2. Ask for explicit "Confirm" or "Send" response
3. Apply the same 30-minute expiration
4. Apply the same 30-second undo window
5. Log the approval channel as `copilot_chat` instead of `slack`

### "The email is part of a sequence but the rep edited it"

The rep's edits always win. If they modify the email during the approval flow:
1. Use the edited version, not the original template
2. Log `composition_source: 'rep_edited'` in the audit
3. Do not "correct" their edits or revert to the template
4. The sequence continues with their edited version as the record of what was sent
