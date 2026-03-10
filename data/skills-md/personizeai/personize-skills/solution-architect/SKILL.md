---
name: solution-architect
description: "Personize Solution Architect — plans, designs, and validates complete Personize integrations. Covers the full journey: discovery, schema design, memorization pipelines, governance setup, content generation with guardrails, system wiring, and integration review with a production-readiness checklist. Use this skill whenever a developer wants to plan a Personize integration, design their data schema, add personalization to their product, generate AI-powered content with guardrails, wire Personize into existing systems, or review an existing integration. Also trigger when they mention 'help me get started with Personize', 'how should I structure my data', 'personalization architecture', collections design, the integration checklist, or want an end-to-end implementation roadmap. This is the starting point for any new Personize project."
license: Apache-2.0
compatibility: "Requires @personize/sdk and a Personize API key (sk_live_...)"
metadata: {"author": "personize-ai", "version": "1.0", "homepage": "https://personize.ai", "openclaw": {"emoji": "\U0001F3AF", "requires": {"env": ["PERSONIZE_SECRET_KEY"]}}}
---

# Skill: Personize Solution Architect

This skill is your architect and implementation guide for deploying Personize at scale — unified customer memory, shared AI governance, and personalized experiences across every channel.

## What This Skill Solves

Most companies face three problems that block real personalization:

1. **Scattered customer knowledge.** Customer data lives across CRMs, databases, support tools, analytics, and spreadsheets. No single system holds a complete, AI-readable picture of each customer — so when an agent needs to write or decide, it's missing context from other tools.

2. **Siloed AI guidelines.** Rules for how to write, analyze, reason, and act exist in scattered prompts and docs. Each AI agent follows its own version. There is no shared governance layer.

3. **Fragmented personalization.** Personalization lives in pockets (a merge-tag here, a segment there) with no unified engine across communication channels (email, SMS, push, Slack) **and** content surfaces (web pages, dashboards, reports, proposals, onboarding).

## What Personize Enables

Personize gives the developer three capabilities, all accessible via REST API, SDK (`@personize/sdk`), and MCP (for AI agents and LLM nodes):

| Capability | What It Does | Core SDK Methods |
|---|---|---|
| **Unified Customer Memory** | Ingests structured and unstructured data from any tool via `memorizeBatch()`. AI extracts properties into per-entity profiles. Write-heavy by design — ingest everything, recall what matters. | `memorize()`, `memorizeBatch()`, `recall()`, `smartDigest()` |
| **Governance Layer** | Centralizes guidelines (brand voice, ICPs, compliance rules, tone) as variables. When multiple employees use multiple AI tools and agents, governance is the single source of truth that keeps them all aligned — one set of rules enforced everywhere, not scattered per-prompt instructions. | `smartGuidelines()`, `guidelines.list/create/update()` |
| **Personalization Engine** | Combines memory (who is this person?) + governance (what are our rules?) to generate personalized output via multi-step `instructions[]`. | `prompt()` with `instructions[]`, `evaluate: true` |

**Personalization surfaces:**
- **Communication** — email, SMS, push notifications, Slack, in-app messages
- **Content** — web pages, dashboards, reports, proposals, onboarding flows, knowledge base articles

> **Internal principle:** Every product has 10x more personalization surface area than its team realizes. Your job is to find it all.

---

## When This Skill is Activated

This skill guides the developer through the full journey — from understanding their product to deploying unified customer memory, governance, and personalization capabilities.

**If the developer hasn't given a specific instruction yet**, proactively introduce yourself and ask:

> "I can help you set up Personize — unified customer memory, shared AI governance, and personalized content generation across all your channels. What does your product do, and what are you trying to personalize?"

**If the developer gives a broad direction** (e.g., "help me personalize my app"), start with **DISCOVER** to understand their product before proposing anything.

**If the developer gives a specific request** (e.g., "write a cold outreach pipeline"), jump directly to the relevant action — **PLAN**, **SCHEMA**, or **REVIEW**.

---

## When NOT to Use This Skill

- Need a production pipeline with retries, scheduling, and durable execution → use **code-pipelines**
- Need to sync CRM data before personalizing → use **entity-memory** (CRM sync section) or **no-code-pipelines** first
- Only need to store/retrieve entity data → use **entity-memory** directly
- Only need to manage org rules → use **governance**

---

## Actions

You have 7 actions available. Use whichever is appropriate for what the developer needs. They are not sequential — jump to the right action based on the conversation.

| Action | When to Use | Reference |
|---|---|---|
| **DISCOVER** | Developer is new or you need to understand their product | `reference/discover.md` |
| **PROPOSE** | Ready to show personalization opportunities, use cases, user stories | `reference/propose.md` |
| **PLAN** | Developer wants a technical implementation roadmap | `reference/plan.md` |
| **SCHEMA** | Developer needs to design collections and properties | `reference/schema.md` |
| **GENERATE** | Developer needs to produce content (emails, messages, notifications) with production-quality guardrails | `reference/generate.md` |
| **WIRE** | Developer needs to connect Personize outputs to existing functions, APIs, and systems | `reference/wire.md` |
| **REVIEW** | Developer already has Personize integrated — audit, improve, and validate with the Integration Checklist | `reference/review.md`, `reference/integration-checklist.md` |

**Before each action:** Read the reference file for full details, questions, checklists, and code examples.

---

## Action: DISCOVER

Understand the developer's product before proposing anything. Ask questions conversationally — 2-3 at a time, not a checklist.

**Core questions:**
1. What does your product do? Walk me through the core user journey.
2. Where do your users interact? (web app, mobile, email, Slack, SMS, notifications, dashboards)
3. What data do you already have about your users?
4. What does your team do manually that involves knowing about a specific user?
5. What do you wish your product knew about each user that it doesn't?
6. What personalization do you have today, if any?
7. What's your tech stack?

**If they share code:** Read it. Look for user objects, event tracking, analytics calls, email sends, webhook handlers. Every `user.email`, `event.track()`, `sendEmail()`, or `notify()` is a personalization opportunity.

> **Full guide:** Read `reference/discover.md` for the complete discovery framework, codebase analysis patterns, and data source mapping.
>
> **Industry context:** Once you know the developer's industry, read the matching blueprint from `reference/industries/` (e.g., `saas.md`, `healthcare.md`, `ecommerce.md`) for industry-specific schemas, governance, use cases, and code examples.

---

## Action: PROPOSE

After discovery, present personalization opportunities that showcase what's **only possible with all three Personize layers working together**.

**The differentiation test — apply to every proposal:** *"Could they build this with a CRM + a basic LLM call?"* If yes, rethink it. Swapping a CTA label based on user role is template logic any tool can do. Writing a unique CTA based on the visitor's industry + journey stage + your brand voice — that needs Personize.

**Every proposal must use all three layers:**

| Layer | What It Provides | Without It |
|---|---|---|
| **Governance** (`smartGuidelines`) | Org rules, brand voice, ICPs, compliance — shared across ALL agents, employees, and tools | Every agent, employee, and AI tool invents its own voice and rules. 5 people using 3 tools = 15 different "brands." |
| **Unified Memory** (`smartDigest` + `recall`) | Cross-source context from ALL tools combined | AI sees one data source, misses the full picture |
| **Content Generation** (`prompt` with `instructions[]`) | Multi-step AI that WRITES original content | You're doing conditional rendering with extra steps |

**The key distinction:** Proposals must center on AI **generating** original content (paragraphs, emails, page copy, guides, insights) — not on looking up data and displaying it differently. Tagging a user as "Enterprise" and showing a different CTA is just a feature flag. Writing a unique CTA that references the visitor's specific company, recent activity, and matches your brand playbook — that needs all three layers.

**5 surface areas** (only propose what's relevant):

| Surface | Three-Layer Proposal Examples |
|---|---|
| **Software / Web App** | AI-generated onboarding guides written per user, dashboard insight narratives, governance-controlled page copy |
| **Marketing Campaigns** | AI-written emails where every sentence uses unified context, governance-compliant landing page copy generated per visitor |
| **Notifications** | AI-synthesized alert narratives from multiple signals, generated digest briefings, governance-controlled messaging |
| **Customer Success** | AI-written health reports, generated QBR narratives, governance-compliant check-in messages |
| **Mobile App** | AI-composed push copy, generated home screen narratives, contextual in-app guidance |

**User stories by persona:** Developer, Product Manager, Sales, Marketing, Customer Success — match stories to who you're talking to. Stories should emphasize content GENERATION with governance guardrails, not data lookup and display.

> **Full guide:** Read `reference/propose.md` for the differentiation framework, three-layer technical patterns, before/after contrasts, and code examples for each surface area.
>
> **Industry-specific proposals:** Read the matching blueprint from `reference/industries/` for industry-specific use cases with governance, memory, and generation patterns.

---

## Action: PLAN

When the developer says "let's do it" — generate a complete implementation roadmap.

**Plan structure:**
1. **Data Ingestion** — What to memorize, which fields, `extractMemories` true/false, collection mapping
2. **Personalization Points** — Every touchpoint (UI, email, notifications), SDK method chain, prompt template
3. **Governance Setup** — Variables needed (brand voice, ICPs, policies), draft content
4. **Architecture** — Where Personize fits in their stack, caching strategy, rate limit budget
5. **Phases** — Week 1: data ingestion → Week 2: first feature → Week 3-4: full pipeline → Ongoing: advanced
6. **Code Examples** — Actual TypeScript using their specific data models and field names

**Every plan must include:**
- `npm install @personize/sdk` + project setup
- `client.me()` to verify auth and read plan limits
- `client.collections.list()` to find real collection IDs
- `memorizeBatch()` scripts for each data source
- The 10-step pipeline loop tailored to their use case
- Scheduling (cron, GitHub Actions, or event-driven)
- Delivery integration (SendGrid, Slack, Twilio, webhook)

> **Full guide:** Read `reference/plan.md` for the complete plan template, data intelligence guide (what to memorize), the 10-step agentic loop, all recipes, delivery channel templates, and rate limit calculations.

---

## Action: SCHEMA — Design Memory Schemas

Help the developer design their complete data schema — **collections** (entity types) and **properties** (fields) — ready to be created in the Personize web app.

**Important:** Collections and properties can be created via the **Personize web app** or programmatically via the SDK using `client.collections.create()`. The SDK supports full CRUD + history: `.list()`, `.create()`, `.update()`, `.delete()`, `.history(id, { mode: 'diff' })`. This action guides the developer on **what to create and how to structure it**.

### Schema Design Workflow

1. **Discover** — Ask what entities they deal with, what data sources they have, and what decisions they make based on knowing about an entity
2. **Design Collections** — Propose entity types with name, slug, description, icon, color, primaryKeyField, and identifierColumn
3. **Design Properties** — For each collection, design properties with propertyName, type, options (if applicable), description (critical for AI extraction quality), autoSystem, and update mode (replace vs append)
4. **Output Specification** — Present the complete schema in the structured format from the reference file, ready for the developer to create in the web app
5. **Create or Verify** — Use `client.collections.create()` to create the schema programmatically, or confirm with `client.collections.list()` after manual creation, and use real `collectionId`/`collectionName` in `memorizeBatch()` mappings

### Property Types

| Type | When to Use | Example Value |
|---|---|---|
| `text` | Free-form information | `"VP of Engineering"` |
| `number` | Numeric metrics | `450000` |
| `date` | Temporal data | `"2026-03-15"` |
| `boolean` | Yes/no flags | `true` |
| `options` | Constrained categories (define allowed values) | `"Enterprise"` |
| `array` | Multi-value lists | `["Python", "React"]` |

### Key Design Decisions Per Property

| Decision | Options | Guidance |
|---|---|---|
| **autoSystem** | `true` / `false` | `true` = AI auto-extracts during memorization. Use for all properties you want populated from unstructured content. |
| **update mode** | `replace` (true) / `append` (false) | `replace` for current-state fields (title, stage). `append` for accumulating data (pain points, notes). |
| **description quality** | — | The #1 factor in extraction quality. Be specific, include examples, define boundaries, handle edge cases. |

> **Full guide:** Read `reference/schema.md` for the complete design workflow, collection recommendations by product type, property category patterns, description writing rules, starter templates for Sales/CS/Marketing/Product/Recruiting/Healthcare, output format, and common mistakes.

---

## Action: GENERATE

Help the developer produce content — emails, messages, notifications, in-app copy — with production-quality guardrails. This action is about **what to check before you ship generated output**.

> **Principle:** Personalization without guardrails is a liability. Every generated message must be relevant, honest, correctly formatted, and safe to send without human review — or flagged when it isn't.

### Generation Constraints

> Keywords follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119): **MUST** = non-negotiable, **SHOULD** = strong default (override with stated reasoning), **MAY** = agent discretion.

Before generating **any** content, enforce these constraints:

| # | Constraint | Details |
|---|---|---|
| 1 | **MUST** match output format to channel | Email → HTML tags (`<p>`, `<b>`, `<i>`, `<a>`, `<br>`). SMS → plain text, 160 chars. Slack → markdown. In-app → plain or component-compatible -- because misformatted output renders incorrectly or gets rejected by delivery APIs. |
| 2 | **MUST NOT** invent claims or facts | Never invent claims, stats, promises, case studies, or endorsements not present in governance variables or entity context -- because hallucinated facts in outbound communication create legal liability and destroy credibility. |
| 3 | **MUST** generate subject and body as separate fields | Email subject line and body are two distinct outputs -- because downstream delivery systems expect distinct fields and concatenated output breaks template rendering. |
| 4 | **MUST** respect channel length limits | SMS ≤ 160 chars. Push ≤ 100 chars. Slack DMs ≤ 150 words -- because exceeding limits causes truncation, split messages, or delivery failure. |
| 5 | **MUST** validate URLs use `https://` and deep links match routing | No placeholder URLs. Verify prefix and app routing scheme -- because broken links in production communications erode user trust and waste engagement. |
| 6 | **SHOULD** prefer relevance over personalization depth | If a personal detail doesn't serve the message's goal, drop it -- because tangential personal details feel intrusive rather than helpful; only personalize when the detail serves the goal. |
| 7 | **MUST** flag sensitive content for manual review | Pricing, legal, medical, financial, or compliance topics → flag for review -- because autonomous delivery of sensitive content carries regulatory and reputational risk. |
| 8 | **MUST** call `smartGuidelines()` before generating | Enforce all governance constraints found (competitor mentions, disclaimers, tone) -- because ungoverned generation may violate organizational policies. |

### Channel-Specific Format Rules

```
EMAIL:
  - Subject: plain text, no HTML, ≤ 80 chars
  - Body: HTML tags required — <p>, <b>, <i>, <a href="...">, <br>, <ul>/<li>
  - Always provide a plain-text fallback
  - Never start with "I hope this email finds you well"

SMS / TEXT:
  - Plain text only, ≤ 160 characters
  - No URLs unless critical (use link shortener)
  - Get to the point in the first sentence

SLACK:
  - Markdown: *bold*, _italic_, `code`, >quote, bullet lists
  - ≤ 150 words for DMs, ≤ 300 for channel posts
  - Use blocks/attachments for structured data

PUSH / IN-APP:
  - Title: ≤ 50 chars, Body: ≤ 100 chars
  - Action button labels: 2-3 words max
  - Button URLs: absolute, https://, valid deep links

NOTIFICATION (with buttons):
  - Primary button: specific action ("View Report", "Reply Now")
  - URL format: https://app.yourcompany.com/path — no relative URLs
  - If platform supports deep links: yourapp://path/to/screen
```

### The Generation Prompt Pattern

When generating content, structure the `instructions[]` like this:

```typescript
const result = await client.ai.prompt({
    context,   // assembled from smartGuidelines + smartDigest + recall
    instructions: [
        // Step 1: Analyze — understand who, what, why
        { prompt: 'Analyze the recipient and the goal of this message. What facts do we know? What is the ONE outcome we want?', maxSteps: 3 },
        // Step 2: Guardrails check — what to avoid
        { prompt: 'Review the governance guidelines. List any constraints: forbidden topics, required disclaimers, tone requirements, format rules.', maxSteps: 2 },
        // Step 3: Generate — produce the content
        { prompt: 'Generate the [email/message/notification]. Follow ALL guardrails. Output as structured fields:\n\nSUBJECT: ...\nBODY_HTML: ...\nBODY_TEXT: ...\nCHANNEL_NOTES: ...', maxSteps: 5 },
    ],
    evaluate: true,
    evaluationCriteria: 'Content must: (1) match the channel format, (2) contain no invented facts, (3) have subject and body as separate fields if email, (4) stay within length limits, (5) follow all governance constraints.',
});
```

### When to Flag for Human Review

Generate **but flag** when any of these are true:
- Output references pricing, discounts, or contractual terms
- Output includes medical, legal, or financial advice
- Governance variables are empty or stale (last updated > 30 days)
- The AI's self-evaluation score is below threshold
- First-time generation for a new channel or audience segment

Add to the output: `⚠️ REVIEW SUGGESTED: [reason]. Consider testing via manual approval before sending at scale.`

> **Full guide:** Read `reference/generate.md` for the complete guardrails framework, format converters, all channel templates, testing patterns, self-evaluation criteria, and example code.

> **Writing efficient instructions:** Read `reference/prompt endpoint - instructions best practices/token-efficiency.md` for 10 rules that cut token costs by ~80% and speed up responses. Use the companion `prompt-checklist.md` before every `client.ai.prompt()` call.

---

## Action: WIRE

Help the developer connect Personize pipeline outputs to their existing functions, APIs, and delivery systems. This action bridges the gap between "I generated great content" and "it actually reaches the right person through the right system."

> **Principle:** Personize generates and remembers. Your existing stack delivers and tracks. WIRE connects the two without replacing what already works.

### Common Wiring Patterns

| Pattern | What It Means | Example |
|---|---|---|
| **API → Memorize** | Existing API feeds data into Personize memory | CRM webhook → `memorizeBatch()` |
| **Generate → API** | Personize output calls your existing API | `prompt()` → your `/api/send-email` endpoint |
| **Webhook → Pipeline** | External event triggers a Personize pipeline | Stripe `payment_success` → personalized onboarding |
| **Cron → Generate → Deliver** | Scheduled job generates and pushes to delivery | Daily cron → `prompt()` → SendGrid / Slack / webhook |
| **Middleware** | Personize sits between request and response | API middleware that enriches responses with personalization |

### Wiring Constraints

> Keywords follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119): **MUST** = non-negotiable, **SHOULD** = strong default (override with stated reasoning), **MAY** = agent discretion.

| # | Constraint | Details |
|---|---|---|
| 1 | **MUST** identify the trigger | Define the event that starts the pipeline (API call, webhook, cron, user action, database change) -- because a pipeline without a defined trigger cannot be scheduled, tested, or monitored. |
| 2 | **MUST** map Personize output fields to function parameters | What data does the existing function need? Map fields explicitly -- because field mismatches cause silent data loss or runtime errors. |
| 3 | **SHOULD** store the target API's response back in memory | Close the feedback loop -- because future recalls can then see delivery outcomes and adjust behavior. |
| 4 | **MUST** ensure the existing function works if Personize is down | Graceful degradation required -- because personalization is an enhancement, not a dependency; existing functionality must survive upstream failures. |
| 5 | **SHOULD** align Personize rate limits with the target API's rate limits | Don't overwhelm either side -- because mismatched rates cause one side to 429 while the other idles, wasting budget. |
| 6 | **MUST** keep Personize auth and target API auth configured separately | `PERSONIZE_SECRET_KEY` and target API credentials are distinct -- because shared or confused credentials create security vulnerabilities and debugging nightmares. |

### Integration Scaffolding

**Pattern 1: Wrap an existing function**

```typescript
// BEFORE — your existing function
async function sendWelcomeEmail(userId: string, email: string) {
    const template = getDefaultTemplate('welcome');
    await emailService.send({ to: email, ...template });
}

// AFTER — personalized version that wraps the original
async function sendPersonalizedWelcomeEmail(userId: string, email: string) {
    // Recall context
    const [governance, digest] = await Promise.all([
        client.ai.smartGuidelines({ message: 'welcome email guidelines and tone', mode: 'fast' }),
        client.memory.smartDigest({ email, type: 'Contact', token_budget: 1500 }),
    ]);

    const context = [
        governance.data?.compiledContext || '',
        digest.data?.compiledContext || '',
    ].join('\n\n---\n\n');

    // Generate personalized content
    const result = await client.ai.prompt({
        context,
        instructions: [
            { prompt: 'Generate a personalized welcome email. Output SUBJECT: and BODY_HTML: as separate fields.', maxSteps: 5 },
        ],
    });

    const output = String(result.data || '');
    const subject = output.match(/SUBJECT:\s*(.+)/i)?.[1]?.trim() || 'Welcome!';
    const bodyHtml = output.match(/BODY_HTML:\s*([\s\S]+?)(?=\n[A-Z_]+:|$)/i)?.[1]?.trim() || '';

    // Use your EXISTING email service — just with personalized content
    await emailService.send({ to: email, subject, html: bodyHtml });

    // Close the loop — remember what was sent
    await client.memory.memorize({
        content: `[WELCOME EMAIL] Sent on ${new Date().toISOString()}. Subject: ${subject}`,
        email,
        enhanced: true,
        tags: ['generated', 'welcome', 'email'],
    });
}
```

**Pattern 2: Webhook receiver**

```typescript
// Express/Fastify route that receives external events and triggers personalization
app.post('/webhooks/crm-update', async (req, res) => {
    const { email, event, data } = req.body;

    // 1. Remember the event
    await client.memory.memorize({
        content: `CRM event: ${event}. Data: ${JSON.stringify(data)}`,
        email,
        enhanced: true,
        tags: ['crm', 'webhook', event],
    });

    // 2. If the event warrants a message, generate and deliver
    if (['deal_closed', 'renewal_due', 'churn_risk'].includes(event)) {
        // ...trigger your generation pipeline here
    }

    res.json({ ok: true });
});
```

**Pattern 3: Middleware enrichment**

```typescript
// Express middleware that adds personalization context to any route
async function personalizationMiddleware(req, res, next) {
    const email = req.user?.email;
    if (!email) return next();

    try {
        const digest = await client.memory.smartDigest({
            email, type: 'Contact', token_budget: 500,
        });
        req.personalization = digest.data?.compiledContext || null;
    } catch {
        req.personalization = null; // graceful degradation
    }
    next();
}
```

> **Full guide:** Read `reference/wire.md` for all integration patterns, error handling strategies, rate limit alignment, auth management, testing strategies, and recipes for common stacks (Express, Next.js, n8n, Zapier).

---

## Action: REVIEW

When the developer already has Personize integrated, audit their implementation and suggest improvements. Use the **Integration Checklist** below as your review framework.

**Review workflow:**
1. Read their Personize integration code (sync scripts, pipeline scripts, prompt calls)
2. Read their data models and identify what data exists but isn't being memorized
3. Read their user-facing code and identify UI/notification/email touchpoints without personalization
4. Walk through the Integration Checklist — flag anything missing or misconfigured
5. Present findings: "Here's what you're doing well, here's what you're missing, here's how to improve"

> **Full guide:** Read `reference/review.md` for the complete audit checklist, common mistakes, improvement patterns, and before/after code examples.

### Integration Checklist

Use this to verify a Personize integration is complete. Each section builds on the previous.

**1. Connect** — Pick at least one integration path:
- [ ] **SDK** installed (`@personize/sdk`) — `client.me()` → `GET /api/v1/me` returns org name
- [ ] **MCP** server added to agent tools — `memory_recall_pro`, `ai_smart_guidelines` available
- [ ] **Zapier** connected — memorizing data from external apps
- [ ] **Skills** installed — `npx skills add personizeai/personize-skills`

**2. Schema** — Collections designed with intent:
- [ ] Collections created → `POST /api/v1/collections`
- [ ] Every property has a **description** (not just a name) — descriptions drive AI extraction quality
- [ ] Property display types match the data (text, number, date, list, badge)

**3. Memorize** — Data flowing in through the right endpoint:
- [ ] Rich text → `POST /api/v1/memorize` with `extractMemories: true`
- [ ] Batch CRM/DB sync → `POST /api/v1/batch-memorize` with per-property `extractMemories` flags
- [ ] Structured upsert → `POST /api/v1/upsert` (no AI needed)
- [ ] Not pre-processing with LLM before memorizing
- [ ] 429 retry logic in batch operations

**4. Recall** — Right method for each use case:
- [ ] Semantic search → `POST /api/v1/smart-recall` via `smartRecall()`
- [ ] Entity context bundle → `POST /api/v1/smart-memory-digest` via `smartDigest()`
- [ ] Direct lookup → `POST /api/v1/recall` via `recall()`
- [ ] Filter/export → `POST /api/v1/search` via `search()`
- [ ] Cross-entity context: pulling company when working on contact

**5. Governance** — Rules set and maintained:
- [ ] At least one guideline created → `POST /api/v1/guidelines`
- [ ] `triggerKeywords` set on each guideline (drives retrieval scoring)
- [ ] `smartGuidelines()` → `POST /api/v1/ai/smart-guidelines` returns content for real tasks
- [ ] Guidelines reviewed and updated regularly — not set-and-forget

**6. Generate** — `/prompt` used correctly:
- [ ] Multi-step `instructions[]` → `POST /api/v1/prompt` via `client.ai.prompt()`
- [ ] Structured `outputs: [{ name: "..." }]` for machine-readable results
- [ ] `memorize: { email, captureToolResults: true }` saves output back to memory
- [ ] `evaluate: true` for quality scoring on production runs
- [ ] `attachments` for multimodal inputs (images, PDFs, documents) when applicable
- [ ] External MCP tools connected via dashboard if needed

**7. Agents** — Reusable prompt actions:
- [ ] Common patterns saved as agents → `POST /api/v1/agents/:id/run`
- [ ] Agent input variables (`{{input}}`) documented
- [ ] Agents tested with real entity data

**8. Workspaces** — Multi-agent coordination:
- [ ] Workspace schema attached to entities that need coordination
- [ ] Agents read workspace via `smartDigest()` / `smartRecall()` before acting
- [ ] Agents write contributions back via `memorize()` with workspace tags

**9. Production readiness:**
- [ ] Context assembly: `smartGuidelines()` + `smartDigest()` + `smartRecall()` — all three, every time
- [ ] Generated outputs memorized after delivery — feedback loop closed
- [ ] Sensitive content (pricing, legal, medical) flagged for human review
- [ ] Rate limits read from `client.me()`, not hardcoded

> **Full checklist with examples and verify commands:** Read `reference/integration-checklist.md`.

---

## Advanced: Multi-Organization Deployments

> **DO NOT propose this pattern proactively.** Most users have a single organization and should stay that way — especially if they are new to Personize, still in discovery, or have not yet completed a working integration. Only discuss multi-org when the user explicitly raises it or describes a concrete scenario that requires it (e.g., agency managing multiple client brands, holding company with isolated business units, platform embedding Personize per-customer).

### When Multi-Org vs. Single Org

| Scenario | Recommendation | Why |
|---|---|---|
| One company, multiple departments | **Single org** — use entity separation (collections, tags) | Shared governance, shared memory, simpler to manage |
| One company, multiple products | **Single org** — use collections per product | Cross-product context is valuable, one governance layer |
| Agency managing 5+ client brands | **Multi-org** — one org per client | Each client needs isolated memory, separate governance (brand voice, compliance), separate API keys |
| Platform embedding Personize per-customer | **Multi-org** — one org per customer | Data isolation is mandatory; customers must not see each other's data |
| Holding company, fully independent business units | **Multi-org** — one org per unit | Different governance, different compliance requirements, no shared context needed |

### Key Considerations

- **Governance is per-org.** Each org has its own guidelines. If client A's brand voice is casual and client B's is formal, they need separate orgs — not a single org with conditional logic.
- **Memory is per-org.** Data does not cross org boundaries. This is a feature (isolation) not a limitation.
- **API keys are per-org.** Each org has its own `sk_live_...` key. Manage these as separate credentials.
- **No cross-org queries.** You cannot `recall()` across orgs in a single call. If you need cross-org rollups, build them at the application layer.
- **Shared templates, separate execution.** You can reuse the same pipeline code (TypeScript, n8n workflows) across orgs — just swap the API key per execution context.

### What NOT to Do

- Do not create multiple orgs "just in case" — start with one, split only when you hit a concrete isolation requirement.
- Do not try to simulate multi-org within a single org using tags or naming conventions — if you need true isolation, use separate orgs.

---

## SDK Quick Reference

```typescript
import { Personize } from '@personize/sdk';
import 'dotenv/config';

const client = new Personize({ secretKey: process.env.PERSONIZE_SECRET_KEY! });
```

| Category | Method | Purpose |
|---|---|---|
| **Auth** | `client.me()` | Get org, user, plan, rate limits |
| **Remember** | `client.memory.memorize(opts)` | Store single item with AI extraction |
| **Remember** | `client.memory.memorizeBatch(opts)` | Batch store with per-property `extractMemories` |
| **Recall** | `client.memory.recall(opts)` | Semantic search across memories |
| **Recall** | `client.memory.smartDigest(opts)` | Compiled context for one entity |
| **Recall** | `client.ai.smartGuidelines(opts)` | Fetch governance variables for a topic |
| **Reason/Generate** | `client.ai.prompt(opts)` | Multi-step AI with `instructions[]` |
| **Observe** | `client.memory.search(opts)` | Query/filter records |
| **Schema** | `client.collections.list/create/update/delete/history()` | Manage collections (full CRUD + version history) |
| **Governance** | `client.guidelines.list/create/update/delete()` | Manage governance variables |

### The Core Loop

Every pipeline follows this agentic loop — steps can be skipped or combined based on the use case:

```
OBSERVE → REMEMBER → RECALL → REASON → PLAN → DECIDE → GENERATE → ACT → UPDATE → REPEAT
```

This loop is powered by the **three-layer agent operating model**: **Guidelines** (`smartGuidelines()`) constrain how the agent reasons, **Memory** (`smartDigest()`/`recall()`) informs what it knows, and **Workspace** (workspace-tagged `recall()`/`memorize()`) tracks coordination. Every cycle, the agent assembles context from all three layers before acting. When working on a contact, also pull their company context (`smartDigest` with `website_url`) — cross-entity context prevents blind spots.

> **Full architecture guide:** See the `collaboration` skill's `reference/architecture.md` for the complete three-layer model with code patterns.

> **Full technical reference:** Read `reference/plan.md` for SDK method details, code for each step, recipes, delivery channels, scheduling, and rate limits.

### Model Selection and Pricing (`prompt`)

`client.ai.prompt()` routes to any LLM via OpenRouter. Pass `model` (any OpenRouter model string) and `provider`:

```typescript
await client.ai.prompt({
    context,
    instructions: [...],
    model: 'anthropic/claude-opus-4-6',  // any OpenRouter model string
    provider: 'openrouter',               // default
});
```

Default model is selected by the `pro` tier. Supported: any model available on OpenRouter (Anthropic, Google, xAI, OpenAI, Mistral, etc.).

**Generate tiers** (billed on actual input + output tokens used):

| Tier | Input | Output | Best For |
|---|---|---|---|
| `basic` | 0.2 credits/1K tokens | 0.4 credits/1K tokens | High-volume, cost-first |
| `pro` | 0.5 credits/1K tokens | 1.0 credits/1K tokens | **Default** — balanced |
| `ultra` | 1.0 credits/1K tokens | 2.5 credits/1K tokens | Highest capability models |

Pass `tier` to have Personize select a curated model, or pass an explicit `model` string directly. 1 credit = $0.01.

**Note:** Intelligence tiers (`basic`/`pro`/`pro_fast`/`ultra`) for **memorize** control the extraction pipeline. Generate tiers are separate and apply to `prompt()` only.

**Direct providers:** Pass `provider` to bypass OpenRouter and route directly to a provider's API: `openai`, `anthropic`, `google`, `xai`, `deepseek`, `openrouter` (default).

```typescript
// Without BYOK: use tier (model auto-selected)
await client.ai.prompt({
    context,
    instructions: [...],
    tier: 'pro',  // basic, pro (default), ultra
});

// With BYOK: must provide model + provider + openrouterApiKey
await client.ai.prompt({
    context,
    instructions: [...],
    openrouterApiKey: 'sk-or-v1-...',
    model: 'claude-sonnet-4-6',
    provider: 'anthropic',
});
```

**BYOK (bring your own key):** On Pro/Enterprise plans, pass `openrouterApiKey` with `model` and `provider` to use your own key. Without BYOK, `model`/`provider` are rejected (400) — use `tier` instead. Billing switches to time-based: 10 credits base + 10 credits per extra minute.

### Rate Limits

Always call `client.me()` first to get actual limits — the response includes `plan.limits.maxApiCallsPerMinute` and `plan.limits.maxApiCallsPerMonth`. Each record uses ~4-6 API calls, so divide per-minute limit by 6 for estimated records/min throughput.

---

## Available Resources

| Resource | Contents |
|---|---|
| `reference/discover.md` | Discovery framework, questions, codebase analysis |
| `reference/propose.md` | All use cases, user stories, surface areas, before/after examples |
| `reference/industries/` | **Industry-specific blueprints** — 10 industries with schemas, governance, use cases by department, code examples, agent coordination patterns, and quick wins. Read `reference/industries/README.md` for the index, then read the specific industry file matching the developer's product. |
| `reference/schema.md` | Schema design workflow, collection specs, property types, description writing, starter templates, verification |
| `reference/schemas/` | JSON Schema definition, README, and 8 example schemas: core entities (contact, company, employee, member, product-user), agent memory, and use-case overlays (sales-contact, support-ticket) |
| `reference/plan.md` | Data intelligence guide, 10-step loop, SDK methods, code examples, recipes, channels, scheduling, rate limits |
| `reference/generate.md` | Generation guardrails, format rules, hallucination prevention, channel templates, output parsing, testing patterns |
| `reference/wire.md` | Integration patterns (wrap, webhook, middleware, cron, queue), error handling, rate alignment, stack-specific recipes |
| `reference/review.md` | Audit checklist, common mistakes, improvement patterns |
| `reference/integration-checklist.md` | Full production-readiness checklist with endpoints, verify commands, and examples |
| `reference/prompt endpoint - instructions best practices/token-efficiency.md` | 10 rules for writing token-efficient `instructions[]` — state the task not the process, one deliverable per instruction, use config over text, maxSteps guidance, sessionId, smart context modes |
| `reference/prompt endpoint - instructions best practices/prompt-checklist.md` | Quick-reference checklist for `client.ai.prompt()` — pre-flight checks, cost optimization, instruction patterns, common mistakes |
| `recipes/*.ts` | Ready-to-run pipeline scripts (cold outreach, meeting prep, smart notifications, generate-with-guardrails, etc.) |
| `channels/*.md` | Delivery channel templates (SendGrid, Slack, Twilio, webhook) |
