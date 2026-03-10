---
name: signal
description: "Set up @personize/signal — a smart notification engine that decides IF, WHAT, WHEN, and HOW to notify each person using Personize memory and governance. Guides you through connecting event sources, configuring delivery channels, setting up governance rules, and testing the decision engine. Use this skill whenever the user wants to build smart notifications, AI-powered alerts, notification fatigue prevention, daily/weekly digests, personalized messaging, or intelligent notification routing. Also trigger when they mention @personize/signal, notification scoring, quiet hours, deduplication, channel routing (email vs Slack vs in-app vs SMS), or want notifications that know when to stay silent."
license: Apache-2.0
compatibility: "Requires @personize/sdk >=0.4.0 and a Personize API key (sk_live_...)"
metadata: {"author": "personize-ai", "version": "1.0", "homepage": "https://personize.ai", "openclaw": {"emoji": "\U0001F4E1", "requires": {"env": ["PERSONIZE_SECRET_KEY"]}}}
---

# Skill: Signal — Smart Notification Engine

Set up AI-powered notifications that decide IF, WHAT, WHEN, and HOW to notify each person. Signal uses Personize memory and governance to send the right message, to the right person, at the right time — or stay quiet when silence is better.

## What This Skill Solves

Most notification systems are dumb rules: "if event X, send template Y." They don't know who the person is, what they care about, what was already sent, or whether this notification will help or annoy.

Signal replaces rules with intelligence:
- **IF** — Should this person be notified at all? (AI scores 0-100 based on full entity context)
- **WHAT** — What should the message say? (Uniquely personalized using everything known about the person)
- **WHEN** — Now, or later in a digest? (AI decides priority: immediate / standard / digest)
- **HOW** — Which channel? (Email, Slack, in-app, SMS — chosen based on context)

The intelligence comes from Personize SDK — memory, governance, and AI. Signal packages the orchestration into a reusable engine.

---

## When This Skill is Activated

**If the developer mentions notifications, alerts, or messaging**, start with **ASSESS**.

**If the developer has a specific question** (e.g., "how do I add a Slack channel to Signal"), jump to the relevant action.

**If the developer wants to understand the architecture**, walk them through the engine flow.

---

## When NOT to Use This Skill

- Need raw memory operations → use **entity-memory**
- Need shared workspaces without notifications → use **collaboration**
- Need governance rules without notifications → use **governance**
- Need CRM data sync → use **entity-memory** (CRM sync section)

---

## Actions

| Action | When to Use |
|---|---|
| **ASSESS** | Understand their stack, events, channels, and recipients |
| **CONFIGURE** | Generate Signal initialization code |
| **CONNECT** | Scaffold event hooks for their framework |
| **GOVERN** | Set up governance rules for notification guidelines |
| **TEST** | Run a dry-run evaluation and verify the decision |

---

## Action: ASSESS

Understand what the developer needs before writing code.

### Questions to Ask

1. **What events matter?** — What happens in your product that should potentially trigger a notification?
   - User lifecycle: signup, login, trial expiry, churn risk
   - Usage: milestones, drops, feature adoption
   - CRM: deal changes, meeting outcomes, support tickets
   - System: sync complete, errors, billing events

2. **Who are the recipients?** — Who gets notified?
   - End users (in-app, email)
   - Internal team (Slack, email)
   - Both (different channels)

3. **What channels?** — How should messages be delivered?
   - Email (SES, SendGrid)
   - Slack (webhook)
   - In-app (bridge to existing UI)
   - SMS (Twilio — community channel)

4. **What governance rules exist?** — What constraints apply?
   - Max notifications per day per user
   - Quiet hours / time zones
   - Content policies (tone, compliance)
   - Opt-out preferences

5. **What framework?** — Where do events originate?
   - Express.js / Fastify / Next.js / NestJS
   - Trigger.dev / n8n / cron jobs
   - Webhook-based (external system pushes events)

### Output

After assessment, summarize:
- Events to handle (with types like `user.signup`, `usage.drop`)
- Channels needed
- Governance constraints
- Framework/integration approach

---

## Action: CONFIGURE

Generate the Signal initialization code based on the assessment.

### Minimal Setup

```typescript
import { Personize } from '@personize/sdk';
import { Signal, ConsoleChannel, ManualSource } from '@personize/signal';

const client = new Personize({ secretKey: process.env.PERSONIZE_SECRET_KEY! });
const manual = new ManualSource();

const signal = new Signal({
    client,
    channels: [new ConsoleChannel()],
    sources: [manual],
});

await signal.start();
```

### Production Setup

```typescript
import { Personize } from '@personize/sdk';
import {
    Signal,
    ManualSource,
    SesChannel,       // or SendGridChannel
    SlackChannel,
    InAppChannel,
} from '@personize/signal';

const client = new Personize({ secretKey: process.env.PERSONIZE_SECRET_KEY! });
const manual = new ManualSource();

const signal = new Signal({
    client,
    channels: [
        new SesChannel({ sourceEmail: 'notifications@yourapp.com' }),
        new SlackChannel({ webhookUrl: process.env.SLACK_WEBHOOK! }),
        new InAppChannel(async (recipient, payload) => {
            // Bridge to your existing notification UI
            await yourNotificationService.create({
                userId: recipient.userId,
                title: payload.subject,
                body: payload.body,
            });
            return { success: true, channel: 'in-app', timestamp: new Date().toISOString() };
        }),
    ],
    sources: [manual],
    engine: {
        dailyCap: 5,                              // max per user per day
        deduplicationWindowMs: 6 * 60 * 60 * 1000, // 6 hours
        memorize: true,                            // feedback loop
        workspaceUpdates: true,                    // track in workspace
    },
});

await signal.start();

// Schedule daily digests (weekdays 9 AM)
signal.schedule('daily-digest', '0 9 * * 1-5', async () => {
    const users = await getActiveUsers();
    await signal.digest.runBatch(users);
});
```

### Configuration Reference

| Option | Default | Description |
|---|---|---|
| `engine.dailyCap` | 5 | Max notifications per email per day |
| `engine.deduplicationWindowMs` | 6h | Skip same event type within window |
| `engine.memorize` | true | Record sent notifications in memory |
| `engine.workspaceUpdates` | false | Create workspace entries on SEND/DEFER |
| `engine.concurrency` | 5 | Max parallel evaluations |
| `engine.maxEvaluationsPerMinute` | 20 | Rate limit for batch processing |

---

## Action: CONNECT

Scaffold event hooks that push product events into Signal.

### Express.js Pattern

```typescript
// event-hooks.ts — fire-and-forget, never throws, never blocks
import { ManualSource } from '@personize/signal';

const manual = new ManualSource(); // same instance used in Signal config

export const EventHooks = {
    async onUserSignup(email: string, data?: Record<string, unknown>) {
        manual.emit({
            id: `evt_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`,
            type: 'user.signup',
            email,
            data: data || {},
            timestamp: new Date().toISOString(),
            metadata: { team: 'product' },
        });
    },

    async onUsageDrop(email: string, data: { metric: string; dropPercent: number }) {
        manual.emit({
            id: `evt_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`,
            type: 'usage.drop',
            email,
            data,
            timestamp: new Date().toISOString(),
            metadata: { team: 'product' },
        });
    },
};
```

### Using in Controllers

```typescript
// In your signup controller
router.post('/signup', async (req, res) => {
    const user = await createUser(req.body);
    EventHooks.onUserSignup(user.email, { plan: user.plan }).catch(() => {});
    res.json(user);
});
```

### Webhook Source (external events)

```typescript
import { WebhookSource } from '@personize/signal';

const webhookSource = new WebhookSource({
    path: '/webhooks/signal',
    secret: process.env.WEBHOOK_SECRET,
    parser: (body) => ({
        id: body.id || `wh_${Date.now()}`,
        type: body.event || 'webhook.received',
        email: body.email || body.user_email,
        data: body.data || body,
        timestamp: body.timestamp || new Date().toISOString(),
    }),
});

// Mount on Express
app.use(webhookSource.middleware());
```

---

## Action: GOVERN

Set up governance rules that guide Signal's AI decisions.

### Governance Variables to Create

Use the Personize web app or SDK to create these governance variables:

**1. Notification Guidelines** (tag: `notifications`)
```
Notification Policy:
- Never notify about events the user has already seen in the product
- Prioritize actionable insights over informational updates
- Match tone to the urgency: critical = direct, informational = friendly
- Always include a specific next step, not generic "check it out"
- Maximum 3 notifications per user per day (engine enforces 5 as hard cap)
```

**2. Channel Routing** (tag: `notifications`)
```
Channel Selection:
- Slack: For internal team alerts (sales, support, ops)
- Email: For user-facing notifications that need persistence
- In-app: For real-time product notifications when user is active
- Digest: For low-priority updates that can wait for weekly summary
```

**3. Frequency Policy** (tag: `communications`)
```
Communication Frequency:
- New users (< 30 days): Max 1 notification per day. Focus on onboarding milestones.
- Active users: Max 3 per week. Only high-signal events.
- At-risk users: Increase frequency for re-engagement. Max 1 per day.
- Churned users: Do not notify. Only send win-back campaigns via marketing.
```

### How Governance Flows into Signal

Signal's engine calls `smartGuidelines()` and `smartDigest()` in step 3 (context assembly). The AI sees these governance rules alongside the entity's full context and makes decisions accordingly. No code changes needed — update governance variables and Signal adapts.

---

## Action: TEST

Verify Signal is working with a dry-run evaluation.

### Quick Test

```typescript
const result = await signal.trigger({
    id: 'test_001',
    type: 'user.signup',
    email: 'test@example.com',
    data: { plan: 'trial', source: 'website' },
    timestamp: new Date().toISOString(),
});

console.log('Action:', result.action);    // SEND | DEFER | SKIP
console.log('Score:', result.score);      // 0-100
console.log('Reasoning:', result.reasoning);
console.log('SDK calls:', result.sdkCallsUsed);
console.log('Duration:', result.durationMs, 'ms');
```

### What to Verify

1. **Pre-check works** — Trigger the same event twice within 6 hours. Second should SKIP instantly (0 SDK calls).
2. **Daily cap works** — Trigger 6 events for the same email. The 6th should SKIP.
3. **AI decision varies** — Trigger different event types. Scores should vary based on context relevance.
4. **Feedback loop** — After a SEND, check that the notification was memorized: `client.memory.recall({ query: 'signal:sent', email: '...' })`.
5. **Dedup via memory** — After step 4, trigger a similar event. The AI should reference the recently sent notification in its reasoning.

### Console Channel for Testing

Use `ConsoleChannel` during development — it logs decisions without delivering:

```typescript
const signal = new Signal({
    client,
    channels: [new ConsoleChannel()],  // logs to stdout
    sources: [manual],
});
```

---

## Available Resources

| Resource | Contents |
|---|---|
| `../../signal/README.md` | Full Signal documentation — architecture, channels, sources, workspace, digest, cost controls |
| `../../signal/CLAUDE.md` | AI tool instructions for Signal package |
| `../../signal/examples/quickstart/` | Minimal setup example |
| `../../signal/examples/saas-onboarding/` | Signup → nurture → convert sequence |
| `../../signal/examples/sales-alerts/` | Usage drop alerts to sales team |
| `../../signal/examples/weekly-digest/` | Deferred items → compiled digest |
| `../../signal/examples/multi-team/` | Product + Sales + Marketing on same records |
| `../../signal/templates/CHANNEL_TEMPLATE.md` | How to build a new channel |
| `../../signal/templates/SOURCE_TEMPLATE.md` | How to build a new source |
| `recipes/quickstart.ts` | Minimal Signal setup recipe |
| `recipes/multi-team.ts` | Multi-team configuration recipe |
