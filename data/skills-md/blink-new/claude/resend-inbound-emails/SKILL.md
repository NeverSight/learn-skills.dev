---
name: resend-inbound-emails
description: Set up two-way email communication with send and receive capabilities using Resend API. Includes custom domain management, AI-powered personalization, email threading, and a rich inbox UI
---

## When to Use This Skill

Use when:
- Setting up two-way email communication (send and receive)
- Implementing custom sending domain management
- Building an inbox system with threading
- Adding AI-powered email personalization
- Processing inbound emails via webhooks

## Features Overview

### Core Features (Required)
| Feature | Description |
|---------|-------------|
| **Custom Domains** | Add, verify, and manage sending domains via Resend API |
| **Inbound Webhooks** | Receive and process incoming emails with threading |
| **Single Send** | Send emails individually with RFC 5322 threading |
| **User Settings** | Notification preferences, sending domain selection |
| **Real-time Updates** | Polling for instant inbox updates with toast notifications |
| **Notifications** | Email notifications to team members on replies |

### Optional Features
| Feature | Description |
|---------|-------------|
| **AI Personalization** | AI-powered `{{ tag }}` replacement using Vercel AI SDK |
| **Preview/Review** | Review and edit personalized emails before sending |
| **Bulk Send** | Send emails in batches via pg-boss queue |
| **Rich Text Editor** | TipTap-based editor with attachments and formatting |

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         OUTBOUND FLOW                               │
├─────────────────────────────────────────────────────────────────────┤
│  Composer → Detect {{tags}} → Generate Previews → Review Modal      │
│                                      ↓                              │
│  Send via Resend → Store InboxMessage → Update Thread               │
├─────────────────────────────────────────────────────────────────────┤
│                         INBOUND FLOW                                │
├─────────────────────────────────────────────────────────────────────┤
│  Resend Webhook → Verify Signature → Parse Headers                  │
│         ↓                                                           │
│  Match Thread (RFC 5322) → Resolve Creator → Store Message          │
│         ↓                                                           │
│  Notify Team → Publish Event → Update UI via Polling/SSE            │
└─────────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- Resend account with API key
- PostgreSQL database
- pg-boss for bulk email queue
- Vercel AI SDK for personalization

## Environment Variables

```bash
# Resend
RESEND_API_KEY="re_your_api_key"
RESEND_WEBHOOK_SECRET="whsec_your_webhook_secret"
EMAIL_FROM="onboarding@resend.dev"

# Your default inbound domain (set up in Resend dashboard)
# Format: emails to *@yourdomain.com will be forwarded to your webhook
DEFAULT_EMAIL_DOMAIN="inbox.yourdomain.com"

# App URL for notification links
NEXT_PUBLIC_APP_URL="https://yourdomain.com"
```

## Database Schema

Add these models to your Prisma schema:

### Team Domain Management

```prisma
model TeamDomain {
  id     String @id @default(cuid())
  teamId String
  team   Team   @relation(fields: [teamId], references: [id], onDelete: Cascade)

  resendDomainId String  @unique // Resend's domain ID
  domain         String // e.g., "acme.com"
  status         String  @default("not_started") // "not_started" | "pending" | "verified" | "invalid"
  isActive       Boolean @default(false) // Only one domain can be active per team

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@unique([teamId, domain])
  @@index([teamId])
}
```

### Inbox Threading

```prisma
model InboxThread {
  id            String   @id @default(cuid())
  teamId        String
  creatorId     String?  // Link to your entity (creator, contact, etc.)
  creatorEmail  String   // Primary email for this thread
  primaryEmail  String?  // Original email the thread was created with
  isRead        Boolean  @default(false)
  isArchived    Boolean  @default(false)
  lastMessageAt DateTime
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt

  // Track all emails that have participated
  participantEmails String[] @default([])

  team     Team           @relation(fields: [teamId], references: [id], onDelete: Cascade)
  messages InboxMessage[]

  @@index([teamId, lastMessageAt])
  @@index([teamId, creatorId])
}

model InboxMessage {
  id             String              @id @default(cuid())
  threadId       String
  direction      InboxDirection      // INBOUND or OUTBOUND
  from           String
  to             String
  subject        String?
  textBody       String?
  htmlBody       String?
  resendEmailId  String?
  messageId      String?             // RFC 5322 Message-ID
  inReplyTo      String?             // RFC 5322 In-Reply-To
  references     String[]            // RFC 5322 References chain
  sentAt         DateTime?
  receivedAt     DateTime?
  deliveryStatus InboxDeliveryStatus @default(PENDING)
  createdAt      DateTime            @default(now())
  updatedAt      DateTime            @updatedAt

  thread      InboxThread       @relation(fields: [threadId], references: [id], onDelete: Cascade)
  attachments InboxAttachment[]

  @@index([resendEmailId])
  @@index([messageId])
}

model InboxAttachment {
  id        String @id @default(cuid())
  messageId String
  filename  String
  url       String
  size      Int?
  contentType String?

  message InboxMessage @relation(fields: [messageId], references: [id], onDelete: Cascade)
}

enum InboxDirection {
  INBOUND
  OUTBOUND
}

enum InboxDeliveryStatus {
  PENDING
  SENT
  DELIVERED
  BOUNCED
  FAILED
}
```

### Personalization Review

```prisma
model PersonalizedEmailPreview {
  id              String             @id @default(cuid())
  teamId          String
  creatorId       String?
  createdById     String

  originalSubject String
  originalBody    String             @db.Text
  personalizedSubject String
  personalizedBody    String         @db.Text
  explanation         String?        @db.Text

  recipientEmail  String
  recipientName   String?
  status          EmailReviewStatus  @default(PENDING)

  editedSubject   String?
  editedBody      String?            @db.Text
  wasEdited       Boolean            @default(false)
  sentMessageId   String?            @unique

  createdAt       DateTime           @default(now())
  updatedAt       DateTime           @updatedAt
  expiresAt       DateTime           // 7 days from creation

  @@index([teamId, status])
}

enum EmailReviewStatus {
  PENDING
  SENT
  EXPIRED
}
```

## Core Patterns

### 1. Custom Domain Management

Users can add custom sending domains through Resend API:

```typescript
// Add domain
const { data } = await resend.domains.create({ name: "acme.com" });

// Verify DNS records
await resend.domains.verify(domainId);

// Get DNS records for user to configure
const { data: details } = await resend.domains.get(domainId);
// details.records contains MX, TXT, DKIM records
```

### 2. Building From/Reply-To Addresses

```typescript
// Always use your inbound domain for reply-to to ensure tracking
const fromAddress = buildFromAddress(userEmail, userName, sendingDomain);
// Result: "Kai <kai@acme.com>"

const replyTo = buildReplyToAddress(userEmail);
// Result: "kai@inbox.yourdomain.com" (your inbound domain)
```

### 3. RFC 5322 Email Threading

Thread continuity is maintained using standard email headers:

```typescript
// On send: build headers from previous messages
const lastMessage = await getLastThreadMessage(threadId);
const headers = {
  "Message-ID": `<${uuid()}@${EMAIL_DOMAIN}>`,
  "In-Reply-To": formatMessageIdHeader(lastMessage?.messageId),
  "References": buildReferencesHeader(
    mergeReferences(lastMessage?.references ?? [], lastMessage?.messageId)
  ),
};

// On receive: match thread by headers
const match = await findThreadByHeaders({
  teamId,
  messageId: parseMessageIdHeader(headers["message-id"]),
  inReplyTo: parseMessageIdHeader(headers["in-reply-to"]),
  references: parseReferencesHeader(headers["references"]),
});
```

### 4. Resend Webhook Processing

```typescript
// Verify webhook signature using Svix headers
const payload = await req.text(); // Must read as text, not json
const event = resend.webhooks.verify({
  payload,
  headers: {
    id: req.headers.get("svix-id") ?? "",
    timestamp: req.headers.get("svix-timestamp") ?? "",
    signature: req.headers.get("svix-signature") ?? "",
  },
  webhookSecret: process.env.RESEND_WEBHOOK_SECRET ?? "",
});

// Handle event types
switch (event.type) {
  case "email.received":
    // Fetch full email content
    const { data: email } = await resend.emails.receiving.get(event.data.email_id);
    // email.html, email.text, email.headers, email.attachments
    break;
  case "email.delivered":
  case "email.bounced":
    // Update delivery status
    break;
}
```

**Important:** 
- Read payload as `req.text()`, not `req.json()` before verification
- Svix headers use lowercase with hyphens: `svix-id`, `svix-timestamp`, `svix-signature`
- Always deduplicate using `resendEmailId` before processing

### 5. AI Personalization with {{ Tags }} (OPTIONAL)

> **Note:** This feature is optional. Skip if you don't need AI-powered email personalization.

```typescript
// Detect if personalization is needed
if (hasLiquidTags(subject) || hasLiquidTags(body)) {
  const result = await generatePersonalizedEmail({
    subject,
    body,
    context: buildPersonalizationContext({ creator, team, sender }),
  });
  
  // Verify all tags were replaced
  if (hasLiquidTags(result.subject) || hasLiquidTags(result.message)) {
    throw new Error("Personalization failed");
  }
}
```

Available tags:
- `{{ name }}` - Creator's name
- `{{ time_based_greeting }}` - Day-appropriate greeting
- `{{ compliment }}` - AI-generated compliment
- `{{ content_fit_pitch }}` - Why collaboration makes sense
- `{{ reply_cta }}` - Call to action
- `{{ user_name }}` - Sender's name

**Required for personalization:**
- Vercel AI SDK (`@ai-sdk/gateway`)
- Team personalization settings UI
- `PersonalizedEmailPreview` model (for review workflow)

### 6. Bulk Email with pg-boss (OPTIONAL)

> **Note:** This feature is optional. Skip if you only need single email sending.

```typescript
// Queue bulk send job
await boss.send(QUEUES.BULK_SEND_EMAIL, {
  teamId,
  recipients: [{ creatorId, email, name }],
  subject,
  body,
  fromEmail: session.user.email,
}, DEFAULT_JOB_OPTIONS);

// Worker processes in batches of 100 via Resend batch API
const { data } = await resend.batch.send(emailObjects);
```

**Required for bulk send:**
- pg-boss setup (see team-saas skill)
- Bulk send API route
- Worker handler for `BULK_SEND_EMAIL` jobs

## File Structure

```
src/
├── app/api/
│   ├── teams/[teamId]/
│   │   ├── domains/
│   │   │   ├── route.ts              # List/add domains
│   │   │   └── [domainId]/
│   │   │       ├── route.ts          # Get/delete domain
│   │   │       ├── verify/route.ts   # Verify DNS
│   │   │       └── activate/route.ts # Activate domain
│   │   ├── inbox/
│   │   │   ├── send/route.ts         # Single email send
│   │   │   ├── bulk-send/route.ts    # Bulk send (queued)
│   │   │   ├── threads/route.ts      # List threads
│   │   │   ├── personalization/
│   │   │   │   └── preview/route.ts  # Generate previews
│   │   │   └── reviews/              # Review management
│   │   └── ...
│   └── webhooks/
│       └── resend/route.ts           # Webhook handler
├── lib/
│   ├── resend.ts                     # Client + address builders
│   ├── inbox/
│   │   ├── threading.ts              # Thread matching
│   │   ├── email-headers.ts          # RFC 5322 utilities
│   │   ├── reply-parser.ts           # Strip quoted content
│   │   ├── resend-webhook.ts         # Webhook helpers
│   │   └── inbound-notification.ts   # Team notifications
│   ├── personalization/
│   │   ├── types.ts                  # Context types
│   │   ├── build-context.ts          # Build AI context
│   │   ├── generate-personalized-email.ts
│   │   └── process-liquid-tags.ts    # Tag detection
│   └── jobs/handlers/
│       └── bulk-email-handler.ts     # Bulk send worker
├── hooks/
│   ├── use-inbox.ts                  # Thread/message hooks
│   ├── use-inbox-polling.ts          # Real-time updates
│   ├── use-team-domains.ts           # Domain management
│   └── use-email-reviews.ts          # Review hooks
└── components/
    ├── inbox/
    │   ├── inbox-editor.tsx          # TipTap rich editor
    │   ├── inbox-compose-dialog.tsx  # Compose modal
    │   ├── inbox-message-bubble.tsx  # Message display
    │   ├── personalization-button.tsx# Tag insertion
    │   └── personalization-preview-modal.tsx
    └── settings/
        ├── team-domains-section.tsx  # Domain UI
        └── domain-dns-records.tsx    # DNS records table
```

## Asset Files Included

| Asset | Description |
|-------|-------------|
| `assets/lib/resend.ts` | Resend client + address builders |
| `assets/lib/inbox/threading.ts` | Thread matching logic |
| `assets/lib/inbox/email-headers.ts` | RFC 5322 utilities |
| `assets/lib/inbox/reply-parser.ts` | Strip quoted content |
| `assets/lib/inbox/inbound-notification.ts` | Notification emails |
| `assets/lib/personalization/types.ts` | Context types (OPTIONAL) |
| `assets/lib/personalization/process-liquid-tags.ts` | Tag detection (OPTIONAL) |
| `assets/api/domains-route.ts` | Domain management API |
| `assets/api/inbox-send-route.ts` | Single send API |
| `assets/api/webhook-resend-route.ts` | Webhook handler |
| `assets/hooks/use-team-domains.ts` | Domain hooks |
| `assets/hooks/use-inbox.ts` | Inbox hooks |
| `assets/prisma/schema-additions.prisma` | Schema models |
| `assets/api/users-me-route.ts` | User profile GET/PATCH |
| `assets/api/available-domains-route.ts` | Get user's available domains |
| `assets/api/inbox-updates-route.ts` | Polling endpoint for new messages |
| `assets/hooks/use-user.ts` | User profile hooks |
| `assets/hooks/use-available-domains.ts` | Available domains hook |
| `assets/hooks/use-inbox-polling.ts` | Inbox polling with toasts |
| `assets/components/notifications-section.tsx` | Notification toggle UI |
| `assets/components/email-settings-section.tsx` | Domain selector UI |
| `assets/components/team-personalization-section.tsx` | AI personalization settings (OPTIONAL) |
| `assets/components/inbox-notification-provider.tsx` | Polling provider wrapper |
| `assets/lib/redis.ts` | Redis pub/sub client (OPTIONAL) |
| `assets/api/inbox-events-sse-route.ts` | SSE endpoint (OPTIONAL) |
| `assets/hooks/use-inbox-realtime.ts` | SSE hook (OPTIONAL) |

## Setup Instructions

### 1. Configure Resend

1. Create account at resend.com
2. Get API key from dashboard
3. Set up inbound domain:
   - Go to Resend Dashboard → Domains
   - Add your inbound domain (e.g., `inbox.yourdomain.com`)
   - Configure DNS MX record to point to Resend
   - Set up webhook endpoint

### 2. Configure Webhook

In Resend Dashboard → Webhooks:
- URL: `https://yourdomain.com/api/webhooks/resend`
- Events: `email.received`, `email.delivered`, `email.bounced`, `email.sent`
- Copy the webhook secret to `RESEND_WEBHOOK_SECRET`

### 3. Install Dependencies

```bash
bun add resend
bun add @tiptap/react @tiptap/starter-kit @tiptap/extension-link @tiptap/extension-placeholder
```

### 4. Add Database Models

Copy schema additions from `assets/prisma/schema-additions.prisma` to your schema.

### 5. Copy Asset Files

Copy template files from `assets/` to your project structure.

## Inbound Email Matching Priority

When an email is received:

1. **Deduplication** - Check if `resendEmailId` already exists (skip if duplicate)
2. **OUTBOUND Detection** - Check if sender is team member sending externally
3. **RFC 5322 Headers** - Match via Message-ID, In-Reply-To, or References
4. **Creator Email** - Match sender against primary creator email
5. **Creator Contacts** - Match sender against associated contact emails
6. **Domain Match** - Match sender domain against creator email domain
7. **Auto-create** - Create new creator if no match found

**OUTBOUND Detection:** If a team member sends an email from their personal email client (Gmail, Outlook) to an external address, the webhook will receive it as `email.received`. The handler detects this by checking if the sender is a team member and creates an OUTBOUND message record.

## User Domain Selection Flow

1. Admin adds domain via Team Settings → Domains
2. User configures DNS records (MX, SPF, DKIM)
3. Admin verifies domain via "Verify DNS" button
4. Admin activates domain (one active per team)
5. User selects preferred domain in Personal Settings → Email
6. Emails sent use user's selected domain for From address
7. Reply-To always uses inbound domain for tracking

## User Settings

### Notification Preferences

Users can toggle email notifications for inbound replies:

```typescript
// PATCH /api/users/me
{ notifyInboundEmail: true }

// Only members with notifyInboundEmail: true receive notifications
// If creator has an assignee, only the assignee is notified
```

### Sending Domain Selection

Users can select their preferred sending domain from verified team domains:

```typescript
// GET /api/users/me/available-domains
// Returns all verified domains from user's teams

// PATCH /api/users/me
{ sendFromDomain: "acme.com" }  // or null for default

// Validated: domain must be verified and belong to user's team
```

## Team Settings

### AI Personalization Configuration (OPTIONAL)

> **Note:** Skip this section if you don't need AI personalization.

Teams can configure AI personalization settings:

| Field | Description |
|-------|-------------|
| `personalizationAboutUs` | Team description for AI context (max 2000 chars) |
| `personalizationModelId` | AI model: `google/gemini-3-flash`, `anthropic/claude-sonnet-4.5`, etc. |
| `personalizationInstructions` | Custom AI instructions (max 2000 chars) |
| `personalizationPreviewEnabled` | Show preview modal before sending personalized emails |

```typescript
// PATCH /api/teams/[teamId]
{
  personalizationAboutUs: "We are a marketing agency...",
  personalizationModelId: "google/gemini-3-flash",
  personalizationInstructions: "Keep tone professional but friendly",
  personalizationPreviewEnabled: true
}
```

## Real-time Updates

Two approaches are available. **Polling is recommended** for simplicity and serverless compatibility.

### Option 1: Polling (Recommended)

The system uses polling (10s interval) for reliability with serverless:

```typescript
// Wrap dashboard with InboxNotificationProvider
<InboxNotificationProvider>
  <DashboardShell>{children}</DashboardShell>
</InboxNotificationProvider>

// Hook configuration
useInboxPolling(teamId, {
  interval: 10000,  // 10 seconds
  enabled: true,
});
```

Features:
- Toast notifications for new messages (max 3, then summary)
- Auto-refetch inbox queries on new messages
- Memory cleanup (keeps last 100 message IDs)
- Click "View" to navigate to message
- **No Redis required**

### Option 2: SSE with Redis (OPTIONAL)

For true real-time updates, use Server-Sent Events with Redis pub/sub:

```typescript
// Hook usage
useInboxRealtime(teamId, {
  enabled: true,
  onNewMessage: (data) => console.log("New message:", data),
});
```

**Requirements:**
- Redis instance (e.g., Railway Redis)
- `REDIS_URL` environment variable
- `ioredis` package

**Flow:**
1. Webhook receives email → calls `publishInboxEvent(teamId, event)`
2. Redis publishes to channel `inbox:events:{teamId}`
3. SSE connections subscribed to channel receive event instantly
4. Frontend updates via `useInboxRealtime` hook

**Event types:**
- `new_message` - New inbound email received
- `inbox_update` - Thread/message updated
- `message_status` - Delivery status changed (sent, delivered, bounced)

**Advantages:** True real-time, more efficient
**Disadvantages:** Requires Redis, connection limits with serverless

## Checklist

### Core Setup (Required)
- [ ] Resend API key configured
- [ ] Inbound domain set up in Resend
- [ ] Webhook endpoint deployed and verified
- [ ] Database schema updated (TeamDomain, InboxThread, InboxMessage)
- [ ] Resend client utilities added
- [ ] Threading utilities added
- [ ] Webhook handler implemented
- [ ] Domain management API routes
- [ ] Single email send API route
- [ ] User settings (notification toggle, domain selector)
- [ ] Inbox polling with toast notifications

### Optional Features
- [ ] AI Personalization system (lib/personalization/*, team settings UI)
- [ ] PersonalizedEmailPreview model + review API routes
- [ ] pg-boss worker for bulk send
- [ ] TipTap rich text editor
- [ ] SSE with Redis for true real-time (lib/redis.ts, inbox/events route)
