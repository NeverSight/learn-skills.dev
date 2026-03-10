---
name: code-pipelines
description: "Builds, deploys, and iterates production-ready AI agent pipelines using Trigger.dev and the Personize SDK. Handles the full lifecycle: interview the user about what they want, design the schema and governance, write the pipeline code, deploy it, monitor results, and iterate based on feedback. Generates TypeScript tasks for outbound sequences, inbound lead processing, conversational reply handlers, enrichment pipelines, and account signal monitoring — all backed by Personize memory, AI context, and governance. Use this skill whenever someone wants to build an AI agent, automated workflow, email sequence, drip campaign, cold outreach, lead enrichment, reply handler, account monitor, CRM automation, daily digest, or any durable pipeline — whether they provide technical specs or just describe what they want in plain language. Also trigger for Trigger.dev, background tasks, self-scheduling follow-ups, GTM automation, 'build me an agent that...', or 'I want to automate...'."
license: Apache-2.0
compatibility: "Requires Node.js 20+, a Trigger.dev account (cloud or self-hosted), and a Personize API key (sk_live_...)"
metadata: {"author": "personize-ai", "version": "1.0", "homepage": "https://personize.ai", "openclaw": {"emoji": "\u26A1", "requires": {"env": ["PERSONIZE_SECRET_KEY", "TRIGGER_SECRET_KEY"]}}}
---

# Skill: Code Pipelines

Build production-ready Go-To-Market automation pipelines using **Trigger.dev** for durable task execution and the **Personize SDK** for AI-powered memory, context, and personalization.

Every pipeline is TypeScript. Every pipeline is testable. Every pipeline uses the Personize SDK as the core intelligence layer.

---

## When to Use This Skill

- Someone describes an agent or automation they want built — "I want an agent that monitors leads and sends follow-ups"
- Developer wants to build GTM automation (outbound, inbound, enrichment, reply handling)
- Developer asks for "durable workflows", "background tasks", or "scheduled pipelines"
- User wants AI-powered email sequences that learn from every interaction
- User wants to combine CRM data + web research + Personize memory for personalization
- User needs self-scheduling follow-ups that survive server restarts
- User says "build me an agent that..." or "I want to automate..."

**You handle two types of users:**
- **Developers** who know TypeScript → give them scaffold + pipeline templates, they customize
- **Non-developers** who describe what they want → interview them, design everything, write the code, deploy it, iterate based on their feedback

## When NOT to Use This Skill

- User wants no-code/visual workflows → use the **no-code-pipelines** skill instead
- User only needs a one-time data import → use the **entity-memory** skill with `batch-memorize`
- User wants to plan/design before building → use the **solution-architect** skill first, then come here to build

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│  Trigger.dev — Durable Task Execution                    │
│  • Tasks, retries, schedules, durable wait/sleep         │
│  • Checkpoints survive restarts, deploys, crashes        │
│  • TypeScript — testable, versionable, deployable        │
├──────────────────────────────────────────────────────────┤
│  Personize SDK — AI Intelligence Layer                   │
│  • memory.memorize() — store + AI extract                │
│  • memory.recall() — semantic search across all memory   │
│  • memory.smartDigest() — compiled context per entity    │
│  • ai.smartGuidelines() — retrieve org guidelines           │
│  • ai.prompt() — generate with MCP tools + auto-memorize │
│  • agents.run() — execute multi-step agents with tools   │
├──────────────────────────────────────────────────────────┤
│  App SDKs — Native Libraries (No Wrappers)               │
│  • googleapis (Gmail, Sheets, Calendar)                  │
│  • @hubspot/api-client (HubSpot CRM)                    │
│  • jsforce (Salesforce)                                  │
│  • @slack/web-api (Slack)                                │
│  • twilio (SMS, WhatsApp)                                │
│  • Apollo.io (enrichment), Tavily + Exa (research)       │
└──────────────────────────────────────────────────────────┘
```

---

## The Core Pattern: AI Agent as Pipeline

Personize SDK is the **memory + governance layer**. You can use it with:
- **Personize AI** (`ai.prompt()`, `agents.run()`) — built-in, simplest
- **Any LLM** (OpenAI, Anthropic Claude, Gemini, local models) — bring your own

### Option A: Personize AI with Built-in Tools
```typescript
// Built-in tools (recall, memorize, smart_guidelines, guidelines, etc.)
// are available by default.
const result = await personize.ai.prompt({
  prompt: `Research ${email} and write a personalized cold email.`,
  outputs: [{ name: "email_subject" }, { name: "email_body" }],
  memorize: { email, captureToolResults: true },
  // tier: 'basic' | 'pro' (default) | 'ultra' — selects curated model + credit rate
  // openrouterApiKey: '...' — BYOK (Pro/Enterprise): 10 cr base + 10 cr/extra min
  // model + provider: requires BYOK (openrouterApiKey). Without BYOK, use tier.
});

// result.data.text — cleaned response (output markers stripped)
// result.data.outputs.email_subject — extracted structured output
// result.data.outputs.email_body — extracted structured output
// result.data.metadata.toolResults — tool return values (always present)
```

> **`outputs`**: The server instructs the LLM to wrap each named deliverable in `<output name="...">` XML markers, then extracts and JSON-parses them server-side. The `text` field contains the cleaned response; structured data goes in `outputs`.

> **`captureToolResults: true`**: Memorizes tool return values (e.g. web search results, enrichment data) alongside extracted outputs. Does NOT change the response body — only affects what gets memorized. Meta tools (`smart_guidelines`, `recall_pro`, etc.) are excluded from capture.

> **MCP Tools:** External MCP servers (Tavily, HubSpot, Zapier, etc.) connected via the [Personize dashboard](https://app.personize.ai) are automatically available to the AI during prompt execution.

> **Attachments:** Send images, PDFs, or documents for multimodal analysis. Provide base64 `data` or a `url`:
> ```typescript
> const result = await personize.ai.prompt({
>   prompt: "Extract key data from this invoice and create a contact record.",
>   attachments: [
>     { name: "invoice.pdf", mimeType: "application/pdf", url: "https://..." },
>   ],
>   outputs: [{ name: "invoice_data" }, { name: "contact_info" }],
>   memorize: { email: extractedEmail, captureToolResults: true },
> });
> ```
> Supported: `image/png`, `image/jpeg`, `image/gif`, `image/webp`, `application/pdf`, `text/plain`, `text/csv`, `text/html`, `text/markdown`, `application/json`. Max 10 attachments, 20 MB each, 50 MB total. In multi-step `instructions[]`, attachments are sent with the first step only.

### Option B: YOUR LLM + Personize Memory (Bring Your Own LLM)
```typescript
import OpenAI from "openai";
import { personize } from "./lib/personize";

// 1. Recall from Personize memory
const digest = await personize.memory.smartDigest({ email, include_properties: true, include_memories: true });

// 2. Get org guidelines from Personize
const guidelines = await personize.ai.smartGuidelines({ message: "outbound email guidelines" });

// 3. YOUR LLM generates content
const completion = await new OpenAI().chat.completions.create({
  model: "gpt-4o",
  messages: [
    { role: "system", content: `Guidelines:\n${guidelines.data.compiledContext}` },
    { role: "user", content: `Write email to ${email}.\n\nContext:\n${digest.data.compiledContext}` },
  ],
});

// 4. Memorize the result back into Personize
await personize.memory.memorize({ email, content: `[SENT] ${completion.choices[0].message.content}`, speaker: "outbound" });
```

### Option C: YOUR LLM with Personize as Function Tools
```typescript
import { OPENAI_TOOLS, executePersonizeTool } from "./lib/personize-tools";

// Give your LLM Personize tools — it decides when to recall, memorize, check guidelines
const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Write a follow-up for john@acme.com" }],
  tools: OPENAI_TOOLS,  // personize_recall, personize_memorize, personize_smart_guidelines, personize_smart_digest
});

// Execute tool calls via Personize SDK
for (const tc of response.choices[0].message.tool_calls || []) {
  await executePersonizeTool(tc.function.name, JSON.parse(tc.function.arguments));
}
```

See `reference/personize-sdk-reference.md` for full BYOLLM documentation and `pipelines/outbound/cold-outreach-byollm.ts` for all three patterns in action.

---

## Action: BUILD — Full Lifecycle Agent Creation

When the user describes what they want (instead of asking for a specific pipeline template), guide them through the full lifecycle. This is the primary action for non-developer users and for developers who want a faster path.

### Phase 1: Interview (2-5 questions)

Understand the agent's purpose. Ask conversationally, not as a checklist:

1. **"What should this agent do?"** — the core automation (monitor leads, send outreach, handle replies, generate reports)
2. **"What data does it work with?"** — CRM, email, product usage, web research, manual input
3. **"Where should results go?"** — Email, Slack, CRM update, webhook, dashboard
4. **"What rules should it follow?"** — Brand voice, compliance, competitor policy, approval workflows
5. **"How often should it run?"** — Real-time (webhook trigger), scheduled (daily/hourly cron), or event-driven (on new lead, on reply)

If the user gives a broad description like "I want an agent that handles my leads," ask follow-up questions. If they give a detailed spec, skip to Phase 2.

### Phase 2: Design

Based on the interview, design four things before writing any code:

**1. Schema** — What collections and properties does this agent need?
```typescript
// Example: Lead monitoring agent
await client.collections.create({
    collectionName: 'Lead',
    properties: [
        { propertyName: 'engagement_score', type: 'number', description: 'AI-assessed engagement level 0-100' },
        { propertyName: 'lifecycle_stage', type: 'options', options: ['new', 'enriched', 'contacted', 'engaged', 'qualified'] },
        { propertyName: 'last_outreach_date', type: 'date', description: 'Date of most recent outbound communication' },
        { propertyName: 'enrichment_status', type: 'options', options: ['pending', 'enriched', 'failed'] },
    ],
});
```

**2. Governance** — What rules constrain the agent?
```typescript
await client.guidelines.create({
    name: 'Outbound Email Rules',
    content: 'Professional but approachable. Max 150 words. Reference a specific fact about the recipient. Never mention competitors by name. Include clear CTA. No emails on weekends.',
    triggerKeywords: ['email', 'outreach', 'outbound', 'cold', 'follow-up'],
    tags: ['outbound', 'email', 'brand-voice'],
});
```

**3. Pipeline architecture** — Which pipeline template(s) to combine, what trigger, what schedule.

**4. Integration map** — Which external services and credentials are needed (CRM, email, enrichment).

Present this design to the user for confirmation before writing code.

### Phase 3: Implement

Write the complete pipeline code:

1. **Copy the scaffold** as the project base
2. **Create the schema** — `collections.create()` calls for all entities
3. **Create governance variables** — `guidelines.create()` calls for all rules
4. **Write the pipeline** — combine patterns from existing templates, customized to their data model and business logic
5. **Set up integrations** — configure env vars and auth for external services
6. **Add monitoring** — include a daily digest pipeline that reports results to Slack or email

Every pipeline MUST follow: **Recall → Contextualize → Act → Memorize → Schedule**

### Phase 4: Deploy

Walk the user through deployment. Read `reference/deploy.md` for the full deployment guide.

```bash
# 1. Install dependencies
npm install

# 2. Configure environment
cp .env.example .env
# Fill in API keys

# 3. Test locally
npx trigger.dev@latest dev

# 4. Test with a single record
# Trigger the task manually via Trigger.dev dashboard or CLI

# 5. Deploy to production
npx trigger.dev@latest deploy
```

### Phase 5: Monitor & Iterate

After deployment, help the user evaluate results and improve:

1. **Check initial results** — "How do the first few outputs look? Any issues?"
2. **Adjust governance** — If tone is wrong, update the governance variable. No code change needed.
3. **Adjust prompts** — If the AI misunderstands the task, refine `instructions[]` or `prompt` text
4. **Adjust pipeline logic** — If the workflow order is wrong, restructure the pipeline
5. **Redeploy** — `npx trigger.dev@latest deploy`
6. **Repeat** until the user is satisfied

**Common iteration patterns:**

| User Feedback | What to Change |
|---|---|
| "Emails are too formal" | Update governance variable (brand voice) |
| "It's emailing people we already talked to" | Add recall check before outreach (dedup) |
| "I want Slack alerts for high-priority leads" | Add Signal/notification step after scoring |
| "It's too slow" | Use `fast_mode: true` on smartRecall, reduce `token_budget` |
| "Some outputs feel hallucinated" | Add `evaluate: true` with `evaluationCriteria`, tighten governance |
| "I want it to also update HubSpot" | Add HubSpot API call after generation step |

---

## Available Pipelines

### Outbound
| Pipeline | File | Description |
|---|---|---|
| Cold Outreach | `pipelines/outbound/cold-outreach.ts` | Enrich (Apollo) → Research (Tavily/Exa) → Memorize → AI Generate → Send |
| Cold Outreach (BYOLLM) | `pipelines/outbound/cold-outreach-byollm.ts` | Same flow with YOUR LLM (OpenAI/Claude) + Personize as memory layer |
| Multi-Touch Sequence | `pipelines/outbound/multi-touch-sequence.ts` | Self-scheduling 3-step sequence with durable waits + reply detection |

### CRM Lead Management
| Pipeline | File | Description |
|---|---|---|
| HubSpot Lead Review | `pipelines/crm/hubspot-lead-review.ts` | Daily: pull leads → enrich → review engagement → plan follow-ups |
| Salesforce Lead Review | `pipelines/crm/salesforce-lead-review.ts` | Daily: pull leads → enrich → review engagement → plan follow-ups |

### Conversational
| Pipeline | File | Description |
|---|---|---|
| Email Reply Handler | `pipelines/conversational/email-reply-handler.ts` | Gmail inbound → classify intent → AI reply → self-schedule follow-up |
| Slack Bot | `pipelines/conversational/slack-bot.ts` | Team queries → AI answers using Personize memory + meeting prep |

### Signals
| Pipeline | File | Description |
|---|---|---|
| Account Monitor | `pipelines/signals/account-monitor.ts` | Daily: scan accounts via Tavily/Exa for buying signals |
| Daily Digest | `pipelines/signals/daily-digest.ts` | End-of-day engagement summary + pipeline health → Slack |

---

## Quick Start

### 1. Clone the scaffold

```bash
cp -r Skills/code-pipelines/scaffold/ my-gtm-pipelines/
cd my-gtm-pipelines
npm install
```

### 2. Configure environment

```bash
cp .env.example .env
# Fill in: PERSONIZE_SECRET_KEY, TRIGGER_SECRET_KEY, and any app credentials
```

### 3. Copy the pipelines you need

```bash
cp ../pipelines/outbound/cold-outreach.ts src/trigger/
cp ../pipelines/conversational/email-reply-handler.ts src/trigger/
```

### 4. Dev mode

```bash
npx trigger.dev@latest dev
```

### 5. Deploy

```bash
npx trigger.dev@latest deploy
```

---

## Pipeline Customization Guide

When generating or customizing a pipeline, follow these steps:

### Step 1: Identify the GTM motion
- **Outbound** — we initiate contact (cold email, sequence, signal-triggered outreach)
- **Inbound** — they initiate contact (form, demo request, reply)
- **Enrichment** — data flows in from external sources into Personize memory
- **Signals** — monitoring for triggers/events

### Step 2: Choose the trigger
- `task()` — triggered programmatically or via webhook
- `schedules.task()` — cron-based (daily sync, hourly monitor)
- Webhook endpoint → triggers a task via `myTask.trigger(payload)`

### Step 3: Wire the Personize SDK
Every pipeline should:
1. **Recall** — check what we already know (`memory.recall()` or via MCP tools)
2. **Contextualize** — get org guidelines (`ai.smartGuidelines()` or via MCP tools)
3. **Act** — generate content, score leads, draft replies (`ai.prompt()` or `agents.run()`)
4. **Memorize** — store the interaction (`memory.memorize()` or `memorize:` param)
5. **Schedule** — self-schedule follow-ups if needed (`wait.for()` or `.trigger({ delay })`)

### Step 4: Add app integrations
Use native SDKs. See `reference/channel-setup.md` for setup patterns for each app.

### Step 5: Deploy and test
```bash
npx trigger.dev@latest dev    # local testing
npx trigger.dev@latest deploy # production
```

---

## Reference Documentation

| Doc | File | Content |
|---|---|---|
| Trigger.dev Patterns | `reference/trigger-dev-patterns.md` | Tasks, waits, schedules, retries, batch operations |
| Personize SDK Reference | `reference/personize-sdk-reference.md` | All SDK methods, MCP tools, auto-memorize patterns |
| Enrichment APIs | `reference/enrichment-apis.md` | Apollo.io + Tavily API patterns, rate limits, costs |
| Channel Setup | `reference/channel-setup.md` | Gmail, HubSpot, Salesforce, Slack, Twilio setup |
| Deploy & Iterate | `reference/deploy.md` | Deployment, env vars, monitoring, iteration patterns, scaling, troubleshooting |

---

## Shared Libraries

The `scaffold/lib/` directory contains reusable helpers:

| File | Purpose |
|---|---|
| `lib/personize.ts` | Personize client singleton + `generateWithTools()` + `runAgent()` helpers |
| `lib/personize-tools.ts` | Personize SDK methods as LLM function tools (OpenAI + Anthropic formats) |
| `lib/llm.ts` | BYOLLM helpers: context injection, OpenAI/Claude with Personize tools, recall-generate-memorize loop |
| `lib/gmail.ts` | Gmail read/send/reply helpers using googleapis |
| `lib/hubspot.ts` | HubSpot contact search/update helpers |
| `lib/enrichment.ts` | Apollo + Tavily + Exa wrappers with waterfall pattern |
| `lib/notifications.ts` | Slack + SendGrid notification helpers |

---

## Constraints

> Keywords follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119): **MUST** = non-negotiable, **SHOULD** = strong default (override with stated reasoning), **MAY** = agent discretion.

1. **MUST** use the Personize SDK as the memory and governance layer in every pipeline -- because pipelines without memory lose context between runs and ignore organizational rules.
2. **MUST** follow the Recall → Contextualize → Act → Memorize → Schedule pattern in every pipeline -- because skipping steps produces ungoverned, context-blind, or non-learning automation.
3. **SHOULD** use native app SDKs (googleapis, @hubspot/api-client, jsforce, @slack/web-api) over generic HTTP wrappers -- because native SDKs handle auth refresh, pagination, and error codes automatically.
4. **SHOULD** use `ai.prompt()` with `memorize: { captureToolResults: true }` for generation tasks -- because it closes the feedback loop automatically without extra memorize calls.
5. **MAY** use any LLM provider (OpenAI, Anthropic, Google, local models) alongside Personize memory -- because the SDK is LLM-agnostic; the memory and governance layer works with any generation backend.

---

## Cost Estimates

### Per-pipeline execution costs (approximate)

| Pipeline | Trigger.dev | Personize | Apollo | Tavily | Total |
|---|---|---|---|---|---|
| Cold outreach (1 lead) | ~$0.001 | ~$0.01 | 1-8 credits | 1 search | ~$0.02-0.05 |
| Multi-touch (3 steps) | ~$0.003 | ~$0.03 | 0 (already enriched) | 0 | ~$0.03 |
| Batch enrich (100 leads) | ~$0.05 | ~$0.50 | 100-800 credits | 100 searches | ~$2-5 |
| Daily signal monitor (50 accounts) | ~$0.02 | ~$0.10 | 0 | 50 searches | ~$0.60 |
| Email reply handler (1 reply) | ~$0.001 | ~$0.01 | 0 | 0 | ~$0.01 |

Trigger.dev: $0.0000169/sec (Micro machine). Personize: per plan. Apollo: $0.20/credit overage. Tavily: $0.01/search.

### Generate Tiers & Direct Providers

`ai.prompt()` supports tiered model selection and direct provider routing:

| Tier | Input | Output |
|---|---|---|
| `basic` | 0.2 cr/1K | 0.4 cr/1K |
| `pro` | 0.5 cr/1K | 1.0 cr/1K |
| `ultra` | 1.0 cr/1K | 2.5 cr/1K |

1 credit = $0.01. Pass `tier` for curated model selection. Custom `model` + `provider` require BYOK (`openrouterApiKey`) — without it, the API returns 400. BYOK billing: 10 credits base + 10/extra minute (Pro/Enterprise plans).
