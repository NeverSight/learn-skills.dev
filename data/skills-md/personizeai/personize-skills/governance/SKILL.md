---
name: governance
description: "Manages organizational guidelines, policies, and best practices as governance variables accessible to all AI agents via SmartContext. Use this skill whenever the user wants to create, update, or manage guidelines, brand voice, compliance policies, playbooks, ICPs, sales playbooks, tone rules, or any organizational rules. Also trigger when the user mentions smartGuidelines, governance variables, GitOps sync of policies, team knowledge sharing, AI agent rules, or when they want all their AI tools to follow the same policies. Even if they just say 'set up rules' or 'add a policy', this is the right skill."
license: Apache-2.0
compatibility: "Requires @personize/sdk or Personize MCP server and a Personize API key (sk_live_...)"
metadata: {"author": "personize-ai", "version": "1.0", "homepage": "https://personize.ai", "openclaw": {"emoji": "\U0001F4CB", "requires": {"env": ["PERSONIZE_SECRET_KEY"]}}}
---

# Skill: Governance

These are the rules, policies, and best practices that every AI agent in your organization must follow. **Always check Guidelines before generating content, making decisions, or taking actions.** One update here → every AI tool in your org gets smarter.

Guidelines are stored as markdown documents and are automatically available to all agents via `smartGuidelines`. Use this skill to read, create, update, and manage them.

> This skill supports **two workflows**: conversational editing (chat, SDK scripts, automated pipelines) and **GitOps sync** (`.md` files in a Git repo synced to the API). Both produce the same output: well-structured guidelines available to all agents via `smartGuidelines`.

---

## When NOT to Use This Skill

- Need to store data about contacts/companies → use **entity-memory**
- Need multi-agent coordination state (tasks, updates, issues) → use **collaboration**
- Need to plan a full Personize integration → use **solution-architect**

---

## Actions

You have 6 actions available. Use whichever is appropriate for what the admin needs. They are not sequential — jump to the right action based on the conversation.

| Action | When to Use | Reference |
|---|---|---|
| **CREATE** | Admin shares content or wants a new guideline | `reference/operations.md` |
| **UPDATE** | Admin wants to modify an existing guideline (section, append, replace) | `reference/operations.md` |
| **IMPROVE** | Admin wants to clean up, restructure, or improve guideline quality | `reference/operations.md` |
| **AUDIT** | A factual change affects multiple guidelines (pricing, branding, policy) | `reference/operations.md` |
| **VERIFY** | Confirm agents can see the updated content via `smartGuidelines` | `reference/operations.md` |
| **ONBOARD** | First-time user with 0-2 guidelines — guide them through setup | `reference/onboarding.md` |

**Before each action:** Read the reference file for full workflows, conversation patterns, and code examples.

---

## Works With Both SDK and MCP — One Skill, Two Interfaces

This skill works identically whether the LLM accesses guidelines via the **SDK** (code, scripts, IDE agents) or via **MCP** (Claude Desktop, ChatGPT, Cursor MCP connection).

| Interface | How it works | Best for |
|---|---|---|
| **SDK** (`@personize/sdk`) | `client.guidelines.list()`, `client.guidelines.update()`, etc. | Scripts, CI/CD, IDE agents, recipes |
| **MCP** (Model Context Protocol) | `guideline_list`, `guideline_read`, `guideline_create`, `guideline_update`, `guideline_delete` tools | Claude Desktop, ChatGPT, Cursor, any MCP-compatible client |

**MCP tools map 1:1 to SDK methods:**

| SDK Method | MCP Tool | Purpose |
|---|---|---|
| `client.guidelines.list()` | `guideline_list` | List all guidelines (includes `governanceScope`) |
| `client.guidelines.getStructure(id)` | `guideline_read(guidelineId)` | Get section headings (TOC) + `governanceScope` |
| `client.guidelines.getSection(id, { header })` | `guideline_read(guidelineId, header)` | Get section content |
| `client.guidelines.create(payload)` | `guideline_create(name, value, tags, description)` | Create new guideline |
| `client.guidelines.update(id, payload)` | `guideline_update(guidelineId, value, updateMode, ...)` | Update guideline |
| `client.guidelines.delete(id)` | `guideline_delete(guidelineId)` | Delete guideline |
| `client.guidelines.history(id)` | `guideline_history(guidelineId)` | View change history |
| `client.ai.smartGuidelines({ message })` | `ai_smart_guidelines(message)` | Verify/fetch guidelines |

### `smartGuidelines` Mode and Model

`smartGuidelines` has two modes and an optional model override:

| Mode | How it works | Latency | Cost | When to use |
|---|---|---|---|---|
| `fast` | Embedding-based routing only — no LLM | ~200ms | 0.1 credits/call | Real-time agents, loops, context injection |
| `deep` | LLM selects and composes guidelines | ~3s | 0.5 credits/call | First call, complex queries, deep analysis |

> **Mode rename:** `'full'` was renamed to `'deep'` in the SDK types and API. If you see `mode: 'full'` in older code, update it to `mode: 'deep'`.

1 credit = $0.01. Use `fast` in production pipelines — it handles the majority of cases well at 5× lower cost.

```typescript
// Fast — embedding-only, no LLM overhead (default for real-time)
const guidelines = await client.ai.smartGuidelines({
    message: 'cold email tone and constraints',
    mode: 'fast',
});

// Deep — LLM-based routing, optional model override
const guidelines = await client.ai.smartGuidelines({
    message: 'cold email tone and constraints',
    mode: 'deep',
    model: 'anthropic/claude-sonnet-4-6',  // optional — override the LLM used for routing
});
```

No intelligence tiers — `smartGuidelines` does not use the `basic`/`pro`/`pro_fast`/`ultra` tier system (those are for `memorize`/`batch-memorize` only).

> **`governanceScope`** is a read-only field returned on `guideline_list` and `guideline_read` (structure mode). It contains `alwaysOn` (boolean) and `triggerKeywords` (string array) — auto-inferred at save time. See the "Governance Scope" section below for details.

> **Response shape note:** `client.guidelines.list()` returns `{ data: { actions: [...], count, nextToken? } }` — guidelines are in `data.actions`, not a top-level array. Iterate with `res.data?.actions || []`.

**When reading this skill document:**
- If you're connected via **MCP**, use the MCP tool names (`guideline_list`, `guideline_update`, etc.)
- If you're running via **SDK**, use the `client.guidelines.*` methods
- All workflows, rules, and best practices apply equally to both interfaces

---

## Prerequisites

### SDK Mode
- `@personize/sdk` installed
- `PERSONIZE_SECRET_KEY` env var set to an `sk_live_...` key

```typescript
import { Personize } from '@personize/sdk';
const client = new Personize({ secretKey: process.env.PERSONIZE_SECRET_KEY! });
```

### MCP Mode
- Personize MCP server connected (SSE endpoint: `https://agent.personize.ai/mcp/sse`)
- API key provided via `?api_key=sk_live_...` or OAuth configured
- Tools `guideline_list`, `guideline_read`, `guideline_create`, `guideline_update`, `guideline_delete`, `guideline_history`, and `ai_smart_guidelines` are automatically available

---

## What Guidelines Are

Guidelines are organization-wide documents — policies, best practices, playbooks, checklists, technical manuals, how-tos — stored as markdown. Once saved, they are automatically available to **all agents** in the organization via `client.ai.smartGuidelines()`. When any agent asks smartGuidelines a question like "how should I write a cold email?", it retrieves the relevant guidelines and includes them as context.

**Examples:** `sales-playbook`, `brand-voice-guidelines`, `icp-definitions`, `data-handling-policy`, `engineering-standards`, `incident-response-runbook`, `known-bugs-and-workarounds`, `pricing-rules`

---

## Action Summaries

### CREATE — Draft a New Guideline

1. Ask admin for topic, audience, and source material
2. Check for overlap with existing variables (`client.guidelines.list()`)
3. Draft with proper markdown structure (H1 title, H2 sections, actionable content)
4. Propose kebab-case name, tags, description
5. **Show draft and ask for approval** → create → verify with `smartGuidelines`

### UPDATE — Modify Existing Guidelines

Choose the right update mode:

| Scope | Mode | When |
|---|---|---|
| Single section | `section` | "Update the Cold Email section" |
| Add to a section | `appendToSection` | "Add a new rule to the Email Rules section" |
| Add new section | `append` | "Add a GDPR section to the data policy" |
| Full rewrite | `replace` | "Completely rewrite this variable" |

Workflow: find variable → read structure → read target section → draft update → **show before/after** → apply with `historyNote`

### IMPROVE — Enhance Writing Quality

Read content → analyze structure/clarity/formatting/completeness → draft improved version → **show summary of changes** → apply

### AUDIT — Cross-Guideline Accuracy Scan

Admin reports a factual change → list ALL guidelines → search for old fact → draft corrections → **present batch of proposed changes** → apply each with `historyNote`

### VERIFY — Confirm Agent Visibility

After any create/update: call `smartGuidelines` with relevant query → confirm the updated content appears.

> **Full workflows, conversation patterns, and code:** Read `reference/operations.md`

---

## Constraints

> Keywords follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119): **MUST** = non-negotiable, **SHOULD** = strong default (override with stated reasoning), **MAY** = agent discretion.

1. **MUST** show the admin the proposed change before calling any mutating API -- because silent modifications erode trust and prevent catching errors before they reach production.
2. **MUST** include a descriptive `historyNote` on every update -- because change tracking enables audit trails, team collaboration, and rollback decisions.
3. **MUST** call `list()` and check for name/topic overlap before creating a new guideline -- because duplicate guidelines cause conflicting governance and confuse downstream agents.
4. **SHOULD** use section-level updates (`section` or `appendToSection` mode) over full `replace` -- because scoped edits reduce blast radius and allow concurrent editing; override only when structural reorganization requires full rewrite.
5. **MUST** call `smartGuidelines()` after any create or update to verify the change is visible to agents -- because the API call succeeding does not guarantee semantic retrievability.
6. **SHOULD** preserve the existing heading structure when updating a section -- because reorganizing adjacent sections creates unintended diffs and may break other agents' section-targeted queries.
7. **SHOULD** reuse existing tags before inventing new ones -- because inconsistent tagging fragments filtering and makes audit harder.
8. **MUST** write guideline content for agent consumption: explicit instructions, unambiguous language, headers that match likely `smartGuidelines` search queries -- because agents cannot infer intent from vague prose the way humans do.
9. **SHOULD** limit each guideline to a single concept or policy domain -- because mono-topic guidelines produce higher-relevance `smartGuidelines` matches and are easier to maintain.
10. **MUST** preserve the admin's voice and intent when improving structure or formatting -- because the admin owns the content; the agent is a writing assistant, not an editor-in-chief.
11. **SHOULD** check `history()` before editing and mention recent changes by others -- because concurrent edits without awareness cause overwrites in team environments.

---

## Guideline Quality at Scale

`smartGuidelines` uses hybrid semantic scoring (embeddings + keyword matching + governance scope boosts) to select the most relevant guidelines for each task. Its quality is directly affected by how guidelines are structured.

### Fewer, Richer Guidelines > Many Small Ones

The retrieval pipeline has **dynamic caps** on how many guidelines it returns per query (~7-12 critical, ~5-8 supplementary, scaling with total count). This means:

| Guideline count | Retrieval quality | Notes |
|---|---|---|
| 1-20 | Excellent | LLM-based routing sees everything |
| 20-50 | Very good | Embedding-based fast mode works well |
| 50-80 | Good | Quality starts to depend on naming/tagging discipline |
| 80+ | Requires care | Must follow all rules below to maintain quality |

**MUST** prefer consolidating related content into fewer, well-structured guidelines over creating many small ones — because each guideline competes for limited retrieval slots, and a single rich document with clear H2 sections is retrieved more reliably than five fragments. The section-level extraction in full mode already supports delivering only the relevant sections from a large guideline.

**Examples of consolidation:**

| Instead of these 5 guidelines... | Create 1 guideline with sections |
|---|---|
| `api-auth-rules`, `api-error-format`, `api-pagination`, `api-naming`, `api-versioning` | `api-conventions` with H2 sections: Auth, Errors, Pagination, Naming, Versioning |
| `bug-fix-process`, `known-bugs-list`, `debugging-tips` | `debugging-playbook` with H2 sections: Process, Known Issues, Tips & Patterns |
| `react-style-guide`, `react-testing`, `react-performance` | `react-standards` with H2 sections: Style, Testing, Performance |

### Writing for Maximum Retrievability

1. **Name = search query.** Name guidelines as a developer would search for them: `api-conventions` not `doc-v2-final`. The name is the highest-weight signal in scoring.
2. **Description = summary sentence.** Write the description as if answering "what is this?": `"REST API design rules: authentication, error handling, pagination, and naming conventions"`. Descriptions feed directly into embedding and keyword scoring.
3. **Tags = routing filters.** Use consistent tags (`engineering`, `security`, `sales`, `onboarding`). Agents can filter by tags to narrow the pool before scoring.
4. **H2 headers = section search targets.** In full mode, the LLM can select individual sections by header. Write headers that match how people describe the topic: `## Error Response Format` not `## Section 3.2`.
5. **Front-load key terms.** Put the most important terms in the first 1000 characters of content — this preview is included in the embedding for semantic matching.

### When to Split vs. Merge

**Split** when topics serve different audiences or are queried in completely different contexts (e.g., `sales-playbook` and `engineering-standards` should stay separate even if both are long).

**Merge** when topics are often needed together for the same task (e.g., API auth rules and API error formats are almost always needed together when building endpoints).

### Governance Scope: alwaysOn and triggerKeywords

Every guideline is automatically analyzed at save time to determine:

- **alwaysOn** — whether this guideline applies to virtually all tasks (e.g., core company values, universal compliance). alwaysOn guidelines are always included regardless of similarity score.
- **triggerKeywords** — action and domain words that trigger inclusion (e.g., "email", "pricing", "customer", "deploy"). Each matching keyword boosts the guideline's retrieval score.

These are inferred by LLM and stored automatically. Keep alwaysOn guidelines to a maximum of 2-3 — each one consumes a retrieval slot on every query.

---

## How It Works (Architecture)

```
┌─────────────────────────────────────────────────────┐
│                   GUIDELINES                         │
│              (Personize Variables)                   │
│                                                     │
│  sales-playbook    brand-voice    data-policy        │
│  icp-definitions   engineering-standards   ...       │
└────────┬─────────────────┬─────────────────┬────────┘
         │ smartGuidelines     │ SDK API          │ Sync
         ▼                 ▼                  ▼
┌────────────┐   ┌──────────────┐   ┌──────────────────┐
│ AI Agents  │   │ IDE/Dev Tool │   │ CI/CD Pipelines  │
│ (chat,     │   │ Claude Code  │   │ GitHub Actions   │
│  workflows │   │ Codex/Cursor │   │ Cron jobs        │
│  pipelines)│   │ Gemini/Copilot│  │ n8n workflows    │
└────────────┘   └──────────────┘   └──────────────────┘
```

Guidelines are one layer of the **three-layer agent operating model** — together with **Memory** (`entity-memory` skill) and **Workspace** (`collaboration` skill). Every agent should call `smartGuidelines()` for rules, `smartDigest()`/`recall()` for entity knowledge, and `recall()` by workspace tags for coordination — all before acting. Guidelines provide the governance that makes the other two layers safe to use autonomously.

> **Full architecture guide:** See the `collaboration` skill's `reference/architecture.md` for the complete three-layer model, composition patterns, and adoption path.

---

## Team Collaboration

When multiple people manage guidelines, follow these practices:

- **Version history:** Every update is tracked. Use `client.guidelines.history(id)` or `guideline_history` to review changes. Always start with `limit: 1`.
- **Conflict avoidance:** Use section-level updates (`updateMode: 'section'`) — two people can safely update different sections concurrently. Read before writing.
- **Attribution:** Write attribution-rich `historyNote` values — include what changed, why, and who requested it.
- **Ownership by tag:** `sales-*` variables owned by sales team, `engineering-*` by engineering.

> **Full guide:** Read `reference/collaboration.md` for version history patterns, conflict avoidance workflows, team patterns, and weekly review scripts.

---

## Advanced: Multi-Organization Governance

> **DO NOT raise this topic proactively.** Most users have a single organization. Only discuss multi-org governance when the user explicitly describes managing multiple orgs (e.g., agency with client brands, platform with per-customer orgs) and already has a working Personize integration.

Guidelines are **per-organization** — each org has its own isolated set. In multi-org deployments:

- **Shared policies, separate execution.** If all orgs must follow the same compliance rules, maintain a canonical source (Git repo, template) and sync it to each org separately using `sync.ts` or the SDK. There is no cross-org guideline inheritance.
- **Per-org brand voice.** Each org's `brand-voice` guideline should reflect that org's identity — this is the primary reason to use multi-org instead of a single org with tags.
- **Audit independently.** Use `client.guidelines.history(id)` per org. Changes in one org do not affect others.
- **Same skill, different key.** All governance workflows in this skill work identically — just initialize the SDK with the target org's API key.

---

## Production Guardrails (Recommended, Opt-in)

For shared/production deployments, add guardrails to autonomous learning. These are **recommendations** and are **off by default** so existing accounts keep working.

- `--require-approval`: write proposals JSON, do not mutate guidelines
- `--proposals-file`: persist proposals to a reviewable path/artifact
- `--min-confidence 0.60-0.75`: skip weak AI extractions
- `--max-updates N`: cap per-run blast radius
- `--dry-run`: test extraction/routing with zero writes
- `--no-auto-apply`: require an explicit promote/apply step

Recommended two-stage CI pattern:

1. Learn stage (non-mutating): run `scan-git --require-approval --proposals-file ...`
2. Apply stage (approved): run `batch --file ...` or re-run `scan-git --autoApply` with stricter bounds

This skill keeps auto-apply available for teams that want speed, but production defaults SHOULD include a review path.

---

## Use Cases & Deployment Patterns

This skill supports three deployment patterns beyond conversational editing:

| Use Case | What It Does | Reference |
|---|---|---|
| **IDE-Integrated Guidelines** | Developers read/write guidelines from Claude Code, Codex, Cursor, Copilot | `reference/use-cases.md` |
| **Autonomous Learning** | LLMs auto-extract learnings from incidents, code reviews, conversations | `reference/use-cases.md` |
| **Document Ingestion** | Batch-import policies from folders of docs (wikis, Notion, Google Docs) | `reference/use-cases.md` |

> **Full guide:** Read `reference/use-cases.md` for code examples, recipes, context engineering best practices, and layered context architecture.

---

## Available Resources

| Resource | Contents |
|---|---|
| `reference/operations.md` | Full workflows for CREATE, UPDATE, IMPROVE, AUDIT, VERIFY + conversation patterns + SDK code |
| `reference/collaboration.md` | Version history, conflict avoidance, attribution, team patterns, weekly review |
| `reference/onboarding.md` | First-time setup, starter templates (brand voice, ICP), handling existing content |
| `reference/use-cases.md` | IDE integration, autonomous learning, document ingestion, context engineering |
| `reference/team-setup.md` | Team onboarding runbook for SDK + Skills + MCP + governance CI guardrails |
| `recipes/ide-governance-bridge.ts` | Fetch guidelines from IDE, push learnings back |
| `recipes/auto-learning-loop.ts` | Automatically extract and persist learnings |
| `recipes/document-ingestion.ts` | Batch-import policies from a folder of documents |
| `templates/project-governance-setup.md` | Step-by-step guide for governance-aware projects |
| `templates/context-engineering-guide.md` | Deep dive on context engineering principles |
| `sync.ts` | GitOps sync script — push local `.md` files to Personize variables API |
| `github-action.yml` | GitHub Actions workflow for auto-syncing on push |

---

## Variables as Code (GitOps Sync)

For teams that prefer managing guidelines in Git, the included `sync.ts` script syncs local `.md` files to Personize variables. Filename = variable name, file content = variable value.

**Quick start:**
```bash
npx ts-node sync.ts --pull          # Bootstrap: download remote → local
npx ts-node sync.ts --dry-run       # Preview changes
npx ts-node sync.ts                 # Sync (create + update, never delete)
npx ts-node sync.ts --delete        # Sync with deletion of remote-only
```

**CI integration:** Two GitHub Actions workflows auto-sync on push (`governance-sync.yml`) and auto-extract learnings from code commits (`governance-learn.yml`).

> **Full guide:** Read `reference/team-setup.md` for the complete GitOps workflow, folder conventions, YAML frontmatter format, sync algorithm, CI integration YAML, safety guarantees, pull mode, auto-learning from commits, IDE bridge setup, and the step-by-step team onboarding runbook.
