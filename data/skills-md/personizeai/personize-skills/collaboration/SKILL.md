---
name: collaboration
description: "Turn any record into a shared workspace where agents and humans collaborate. Attach a simple workspace schema to any entity — contacts, companies, deals, projects, tickets — and let any participant contribute updates, tasks, notes, and issues. Use this skill whenever the user wants multi-agent collaboration, shared context on an entity, agent handoffs, workspace-based coordination, or the three-layer agent operating model (Guidelines + Memory + Workspace). Also trigger when they mention multiple agents working on the same record, deal rooms, account intelligence, customer health monitoring, cross-functional coordination, or progressive autonomy for AI agents."
license: Apache-2.0
compatibility: "Requires @personize/sdk and a Personize API key (sk_live_...)"
metadata: {"author": "personize-ai", "version": "1.0", "homepage": "https://personize.ai", "openclaw": {"emoji": "\U0001F91D", "requires": {"env": ["PERSONIZE_SECRET_KEY"]}}}
---

# Skill: Collaboration

Turn any record into a workspace. Agents and humans contribute updates, tasks, notes, and issues. The record becomes the coordination.

## What This Skill Solves

Every organization has entities that multiple people and systems touch — accounts, deals, patients, projects, tickets, students, properties. Today, knowledge about those entities lives in silos: the CRM knows the deal stage, the support desk knows the open tickets, the product tool knows the usage, the sales rep knows the vibe of the last call, and the AI agent knows whatever was in its last prompt.

Nobody has the full picture. And there's no place where all contributors — human and AI — can work on the same entity together.

Traditional collaboration tools (Jira, Notion, Slack) were designed for humans typing to humans. They don't work for AI agents. And "integrations" just copy data between silos — they don't create shared workspaces.

## The Mental Model

**A patient chart.** Multiple specialists — cardiologist, GP, nurse, pharmacist, lab tech — all contribute to the same record. Nobody orchestrates them. Nobody schedules their contributions. They each read the chart, act within their expertise, record what they did, and move on. The chart IS the coordination.

Now apply that to any entity:

- A **company account** where a sales agent logs call intel, a CS agent tracks health signals, a product agent monitors usage, and a human manager reviews the combined picture
- A **deal** where an SDR qualifies, an AE strategizes, an SE evaluates technical fit — each picking up where the last left off with zero context loss
- A **support ticket** where a bot triages, an agent investigates, an engineer escalates, and a manager tracks resolution — all on the same record
- A **student** where an enrollment advisor, academic coach, career counselor, and AI tutor all contribute to the same developmental picture

Same pattern every time. The record is the workspace. Contributors write. Intelligence accumulates.

---

## When This Skill is Activated

This skill helps developers set up shared workspaces on any Personize entity so that multiple participants (agents, humans, systems) can collaborate on the same record.

**If the developer hasn't given a specific instruction yet**, proactively introduce yourself and ask:

> "I can help you set up a shared workspace on any entity — so agents, humans, and systems can collaborate on the same record. What entity do you want to collaborate on, and who are the contributors?"

**If the developer gives a broad direction** (e.g., "I want my agents to work together on accounts"), start with **CREATE** to understand the entity and design the workspace.

**If the developer gives a specific request** (e.g., "show me how to add a task to a contact workspace"), jump directly to **USE**.

---

## When NOT to Use This Skill

- Need to store entity data (not coordination state) → use **entity-memory**
- Need to manage organizational rules/policies → use **governance**
- Need to build a data sync pipeline → use **entity-memory** (CRM sync section) or **no-code-pipelines**

---

## Works With Both SDK and MCP

| What you want | SDK method | MCP tool |
|---|---|---|
| Write to workspace | `client.memory.memorize()` | `memory_store_pro` |
| Batch write | `client.memory.memorizeBatch()` | (SDK only) |
| Read workspace digest | `client.memory.smartDigest()` | (SDK only — use `memory_recall_pro` with targeted queries) |
| Search workspace | `client.memory.smartRecall()` | `memory_recall_pro` |
| Simple lookup | `client.memory.recall()` | `memory_recall_pro` |
| Search records by filters | `client.memory.search()` | (SDK only) |
| Get governance rules | `client.ai.smartGuidelines()` | `ai_smart_guidelines` |
| Generate with workspace context | `client.ai.prompt()` | (use assembled context) |
| Manage collections | `client.collections.create/list/update/delete()` | (SDK only) |

> **Important:** Use `smartRecall()` (not `recall()`) for workspace reads that need `limit`, `fast_mode`, or `include_property_values`. The simpler `recall()` only accepts `query`, `email`, `record_id`, `website_url`, and `filters`. See `reference/api-examples.md` for raw REST equivalents.

> **Guiding AI agents via MCP?** Read `reference/agent-prompts.md` for complete system prompt templates, MCP tool call examples, role-specific prompts (sales intel, CS health, product analytics, human-in-the-loop), and multi-agent coordination patterns.

---

## The Three-Layer Agent Operating Model

Shared workspaces are one of three layers every agent should use. Read `reference/architecture.md` for the full picture.

```
GUIDELINES    →  "What are the rules?"             →  ai_smart_guidelines
MEMORY        →  "What do I know about this entity?" →  recall / smartDigest
WORKSPACE     →  "What's been done & what's next?"  →  recall by tag / memorize
```

**Without Guidelines:** Agent ignores organizational rules.
**Without Memory:** Agent doesn't know who the entity is.
**Without Workspace:** Agent doesn't know what others have done.
**All three:** Agent acts within governance, with full context, in coordination with others.

> **Using workspaces in workflows (n8n, Trigger.dev, cron)?** Agents in workflows don't have access to Skills — they only have MCP tools. Upload the workspace protocol as a governance variable so any agent gets it via `ai_smart_guidelines`. Read `reference/governance-setup.md` for the guideline template, upload instructions, and workflow prompt injection snippets.

> **Using the GTM Workflows Builder skill?** The `recipes/trigger-dev-bridge.ts` recipe shows how a Trigger.dev pipeline can analyze a CRM lead and write findings back to the contact's workspace — bridging the GTM and Shared Workspace skills.

---

## Actions

You have 4 actions. They are not sequential — jump to the right action based on the conversation.

| Action | When to Use | Reference |
|---|---|---|
| **CREATE** | Design and attach a workspace to an entity type | `reference/create.md` |
| **USE** | Contribute to or read from a workspace | `reference/use.md` |
| **GROW** | Add new property types as the workspace matures | `reference/grow.md` |
| **REVIEW** | Audit workspace health and collaboration quality | `reference/review.md` |

**Before each action:** Read the reference file for full details, examples, and code.

---

## Action: CREATE — Design a Workspace

Help the developer design and attach a workspace schema to any entity type. Start from the 5-property starter and adjust to their domain language.

### The Starter Schema: 5 Properties

The minimum that covers what agents and humans actually do when working on a record:

| Property | Type | Semantics | What goes here |
|---|---|---|---|
| **Context** | text | replace | Current state. What's going on right now. Rewritten each cycle. |
| **Updates** | array | append (immutable) | What happened. Who did it. When. The timeline. |
| **Tasks** | array | append (mutable) | What needs to happen. Who owns it. Status. |
| **Notes** | array | append (immutable) | Observations, knowledge, ideas from any contributor. |
| **Issues** | array | append (mutable) | Problems, blockers, risks. Status and resolution. |

### Why These 5 Are Enough

- **Roles?** The `author` field on every entry tells you who contributed. No registry needed.
- **Handoffs?** A task assigned to someone with context IS a handoff. The workspace history IS the context transfer.
- **Conflict resolution?** Two contributors say different things? That's two data points. The consumer reads both and decides.
- **Permissions?** Governance via `smartGuidelines()` tells each agent what they can and can't do. The organizational guidelines are the access control.
- **Escalation?** An issue with severity `critical` IS an escalation. Whoever monitors the workspace acts on it.

### CREATE Workflow

1. **Ask:** What entity? (contact, company, deal, project, ticket, custom?) What contributors? (which agents, which humans, which systems?)
2. **Design:** Start from the 5-property starter. Adjust property names, descriptions, and entry schemas to match their domain language.
3. **Output:** Complete workspace schema ready to create in the Personize web app or via `client.collections.create()`.
4. **Verify:** After creation, confirm with `client.collections.list()` and test with a sample contribution.

> **Full guide:** Read `reference/create.md` for the complete design workflow, property specifications, entry schemas, domain-specific naming examples, and verification steps.

---

## Action: USE — Contribute and Consume

Show how agents and humans write to the workspace and read from it.

### The Contribution Loop

Every participant — agent or human — follows the same natural loop:

```
READ    → smartDigest() gives you the full workspace state in one call
GOVERN  → smartGuidelines() tells you what rules apply to your role
ACT     → Do your work (analyze, generate, decide, communicate)
RECORD  → memorize() your contribution (update, task, note, issue)
```

No orchestrator. No message bus. No event system. The workspace IS the bus. Reading it gives you full context. Writing to it signals everyone else.

### Contributing

Any participant writes to the workspace by memorizing structured entries:

```typescript
// Agent adds a task to a contact workspace
await client.memory.memorize({
    content: JSON.stringify({
        title: 'Schedule QBR prep call',
        description: 'Usage dropped 30% — need to understand why before renewal.',
        status: 'pending',
        owner: 'account-manager',
        createdBy: 'cs-health-agent',
        priority: 'high',
        dueDate: '2026-03-01',
    }),
    email: 'sarah@acme.com',
    enhanced: true,
    tags: ['workspace:tasks', 'source:cs-health-agent'],
});
```

### Consuming

Any participant reads the workspace with one call:

```typescript
const digest = await client.memory.smartDigest({
    email: 'sarah@acme.com',
    type: 'Contact',
    token_budget: 3000,
    include_properties: true,
    include_memories: true,
});

// digest.data.compiledContext contains the full workspace narrative:
// context, recent updates, open tasks, notes, unresolved issues — all compiled
```

### Progressive Autonomy

A pattern the skill teaches, not a feature it enforces:

| Level | What happens | When to use |
|---|---|---|
| **Report only** | Agents contribute notes and updates. Humans create tasks and make decisions. | Starting out. Building trust. |
| **Suggest** | Agents create tasks with status `pending`. Humans review and approve. | Agents have proven reliable. |
| **Act and log** | Agents execute tasks autonomously and record outcomes. Critical issues still escalate. | High confidence in agent quality. |
| **Full autonomy** | Agents act within governance boundaries. Humans audit by reading, not approving. | Mature workspace with strong governance. |

You start at Level 1. You move up as trust builds. The workspace schema doesn't change between levels — only the behavior of the contributors does.

> **Full guide:** Read `reference/use.md` for all contribution patterns, entry formats, consumption patterns, tagging conventions, agent loop examples, and human contribution flows.

---

## Action: GROW — Expand the Workspace

When the starter 5 properties aren't enough, the GROW action helps you add new ones. Each expansion is a conversation: describe what you're struggling with, get a property definition, add it.

### Growth Paths

| You say... | Add this property |
|---|---|
| "I need agents to explain their reasoning" | **Decisions** — question, decision, reasoning, alternatives, confidence, autonomous, approvedBy |
| "I need to track what was communicated" | **Messages Sent** — channel, recipient, summary, sentAt, triggeredBy, status |
| "I need proactive monitoring between cycles" | **Monitors** — target, description, type, frequency, action, status, lastChecked |
| "I need alerts that route to the right person" | **Alerts** — title, severity, message, targetAudience, action, status, acknowledgedBy |
| "I need periodic summaries for stakeholders" | **Reports** — title, content, period, generatedBy, audience, timestamp |
| "I need to know who's active on this record" | **Participants** — participantId, type, role, scope, lastActive, status |

The agent-memory schema (8 properties) isn't a separate thing. It's a workspace that evolved to need Decisions, Alerts, Monitors, and Messages Sent. Your workspace might evolve differently.

> **Full guide:** Read `reference/grow.md` for complete property definitions, entry schemas, when-to-add guidance, and examples of workspaces at different maturity stages.

---

## Action: REVIEW — Audit Workspace Health

When the workspace is running, audit how well the collaboration is working.

### What to Check

| Signal | What it means | How to detect |
|---|---|---|
| **Stale context** | Nobody has updated the Context property recently | `recall()` for context entries, check timestamps |
| **Orphaned tasks** | Tasks assigned but never picked up | `recall()` for tasks with status `pending` older than threshold |
| **Unanswered issues** | Issues raised but no investigation or resolution | `recall()` for issues with status `open` |
| **Silent contributors** | An expected participant hasn't contributed recently | `recall()` by author/tag, check recency |
| **Empty workspaces** | Entity has a workspace but nobody writes to it | `smartDigest()` returns sparse content |
| **One-sided collaboration** | Only one agent contributes — others don't read or act | Check author diversity across entries |

### Review Workflow

1. **Query:** Use `recall()` and `export()` to pull workspace entries across entities.
2. **Analyze:** Check for health signals above.
3. **Report:** Summarize findings — what's working, what's stale, what needs attention.
4. **Recommend:** Suggest fixes — new contributors, governance updates, property additions, workflow changes.

> **Full guide:** Read `reference/review.md` for the complete audit checklist, query patterns, health scoring, and improvement recommendations.

---

## Use Cases

### Multi-Agent Account Intelligence

A **company** entity with a shared workspace. Three agents contribute independently:

- **Sales agent** (runs after every call): Adds notes from call transcripts, updates tasks with next steps, flags issues when a champion goes dark
- **Product agent** (runs daily): Adds updates on feature usage trends, raises issues when adoption drops, creates tasks when an expansion signal appears
- **CS agent** (runs weekly): Rewrites the context with a holistic health summary, creates tasks for QBR prep, adds notes on risk factors

A human account manager reads the workspace via `smartDigest()` and gets a compiled narrative — everything three agents and their own notes have contributed this week. No dashboard. No 3-tool login. One digest.

### The Deal Room

A **deal** entity where the workspace is the handoff mechanism. The SDR qualifies a lead and writes:
- **Note**: "Spoke with VP Eng. Evaluating because current vendor can't handle scale. Technical decision, not budget."
- **Task**: Assigned to AE — "Schedule deep-dive. Key angle: scale story. Bring SE for architecture discussion."
- **Update**: "Qualified. Moving to AE."

The AE's agent reads the workspace, sees the full context, and picks up without asking "what happened on the first call?" After the deep-dive, the AE adds their own notes, creates tasks for the SE, and the workspace grows. Every step of the journey is there — not in someone's head, not in a CRM text field, but in a structured, queryable workspace.

### Customer Health Monitor

A **contact** workspace where multiple signals converge:
- Support agent detects 3 tickets in 2 weeks → raises an **issue** (severity: high, "recurring support volume")
- Product agent detects login frequency dropped 40% → adds a **note** (category: observation)
- CS agent reads both, rewrites the **context** ("At-risk: support volume up, engagement down, renewal in 60 days"), creates a **task** for the CSM with a recommended action plan

The CSM opens the workspace and sees: the problem (issue), the evidence (notes + updates), what to do (task). Three agents, one human, zero meetings.

### Cross-Functional Project Coordination

A **project** entity where engineering, design, and PM agents all contribute:
- Engineering agent: Updates on build progress, issues on technical blockers, tasks for code review
- Design agent: Notes on design decisions, updates on asset delivery, issues on scope creep
- PM agent: Rewrites context with overall status, creates tasks for stakeholder updates, flags issues when timelines slip

No standup needed. The workspace IS the standup.

---

## Constraints

> Keywords follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119): **MUST** = non-negotiable, **SHOULD** = strong default (override with stated reasoning), **MAY** = agent discretion.

1. **SHOULD** start with the 5-property starter schema (Context, Updates, Tasks, Notes, Issues) -- because premature schema complexity kills adoption; expand only when the existing properties force workarounds.
2. **MUST** include an `author` field or `source:agent-name` tag on every workspace entry -- because without attribution, consumers cannot evaluate the reliability or recency of contributions.
3. **MUST NOT** overwrite or delete existing Updates or Notes entries -- because append-only history provides the timeline that makes collaboration legible; if something changes, add a new entry.
4. **MUST** use the `status` field on Tasks and Issues to track state transitions (pending → done, open → resolved) -- because statusless mutable entries create ambiguity about whether work is complete.
5. **MUST** use `replace` semantics for the Context property -- because Context is the current summary, not a log; appending creates unbounded growth that breaks `smartDigest` token budgets.
6. **MUST** use the standard workspace tags (`workspace:tasks`, `workspace:updates`, `workspace:notes`, `workspace:issues`) and add `source:agent-name` for attribution -- because tag-based recall is the primary workspace query mechanism; non-standard tags create invisible entries.
7. **MUST** call `smartDigest()` before contributing to a workspace -- because acting without reading the current state leads to duplicate work, contradictions, and stale decisions.
8. **SHOULD** memorize generated outputs and actions taken as workspace updates -- because the feedback loop prevents duplicate work and gives other contributors visibility into what happened.
9. **SHOULD** call `smartGuidelines()` before generating or deciding -- because governance constraints define what the agent is permitted to do; skipping it risks policy violations.
10. **MAY** attach a workspace to any entity with an identity (contacts, companies, deals, projects, tickets, patients, etc.) -- because the schema is entity-agnostic by design.

---

## Available Resources

| Resource | Contents |
|---|---|
| `reference/architecture.md` | **The three-layer agent operating model:** Guidelines + Memory + Workspace — why all three matter, how they compose, SDK/MCP patterns, adoption path |
| `reference/governance-setup.md` | **Runtime guideline for workflows:** The `shared-workspace-protocol` governance variable, upload instructions, workflow prompt injection snippets for n8n/Trigger.dev/cron |
| `reference/create.md` | Full CREATE workflow: design questions, property specifications, entry schemas, domain naming, verification |
| `reference/use.md` | Full USE guide: contribution patterns, entry formats, consumption, tagging, agent loops, human flows, progressive autonomy |
| `reference/grow.md` | Full GROW guide: all expansion properties (Decisions, Messages, Monitors, Alerts, Reports, Participants), when to add, maturity stages |
| `reference/review.md` | Full REVIEW guide: audit checklist, query patterns, health scoring, improvement recommendations |
| `reference/agent-prompts.md` | **Agent prompt guide:** system prompt templates, MCP tool call examples, role-specific prompts, multi-agent coordination patterns, testing checklist |
| `reference/api-examples.md` | **Raw REST API examples:** curl/fetch for memorize, smart-recall, smart-digest, smart-guidelines, prompt, collections CRUD, search |
| `reference/schemas/examples/workspace-starter.json` | The 5-property starter schema as JSON |
| `reference/schemas/examples/workspace-evolved.json` | A fully evolved workspace (all expansion properties added) |
| `recipes/quickstart.ts` | **Quickstart recipe:** 80-line hello-workspace — auth, memorize one task, smartRecall it, smartDigest the full state |
| `recipes/helpers.ts` | **Shared helpers:** `safeParseJSON()` for robust LLM output parsing, `contributeEntry()` for DRY memorize-with-tags |
| `recipes/contribute.ts` | Recipe: contribute updates, tasks, notes, issues to a workspace |
| `recipes/workspace-digest.ts` | Recipe: read and compile workspace state for any participant |
| `recipes/multi-agent-account.ts` | Recipe: three agents collaborating on an account workspace |
| `recipes/trigger-dev-bridge.ts` | **Cross-skill recipe:** Trigger.dev pipeline that analyzes a CRM lead and writes findings to the contact's workspace |

---

## Signal Integration

**[@personize/signal](../../signal/)** uses the workspace pattern to coordinate notifications across teams. Signal's engine automatically creates workspace entries when `workspaceUpdates: true`:

- On **SEND** — `workspace:updates` entry: "Notification sent: \<subject\>"
- On **DEFER** — `workspace:tasks` entry: "Review deferred notification for \<entity\>"

Signal's `WorkspaceUtils` class provides convenience methods over the raw SDK calls shown in this skill's recipes:

| Signal method | Equivalent SDK pattern | Tag |
|---|---|---|
| `signal.workspace.addTask(email, { title, priority, assignee })` | `memorize({ content: JSON.stringify(task), tags: ['workspace:tasks', 'source:signal'] })` | `workspace:tasks` |
| `signal.workspace.addNote(email, { content, tags })` | `memorize({ content, tags: ['workspace:notes', 'source:signal'] })` | `workspace:notes` |
| `signal.workspace.addUpdate(email, update)` | `memorize({ content: update, tags: ['workspace:updates', 'source:signal'] })` | `workspace:updates` |
| `signal.workspace.addIssue(email, { title, severity })` | `memorize({ content: JSON.stringify(issue), tags: ['workspace:issues', 'source:signal'] })` | `workspace:issues` |
| `signal.workspace.getDigest(email)` | `smartDigest({ email, include_properties: true, include_memories: true })` | — |

### Multi-Team Workspace via Signal

Multiple teams (product, sales, marketing) emit events with `metadata.team` tags. Signal writes workspace entries with team attribution:

```typescript
tags: ['workspace:updates', 'source:product-signal', 'team:product']
```

When any contributor reads the workspace via `smartDigest()`, they see the combined picture from ALL teams — product usage events, sales call notes, marketing engagement. The workspace IS the cross-team coordination, whether contributions come from raw SDK calls or Signal's engine.
