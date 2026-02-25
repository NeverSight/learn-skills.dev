---
name: eve-agent-native-design
description: Design agent-native applications on Eve Horizon. Apply parity, granularity, composability, and emergent capability principles to make apps that agents can build, operate, and extend naturally.
triggers:
  - agent native
  - agent native design
  - design for agents
  - agent first
  - agentic app
  - agent native app
---

# Agent-Native Design for Eve Horizon

Build applications where agents are first-class citizens — not afterthoughts.

## When to Use

Load this skill when:
- Designing a new application or API on Eve
- Evaluating whether an existing app is agent-friendly
- Adding features that agents should be able to use
- Deciding between putting logic in code vs. in prompts
- Choosing how to handle inter-agent communication

## The Four Principles

### 1. Parity — Agents Can Do Everything Users Can

Every user action must have an agent-equivalent path.

**On Eve**: The CLI IS the parity layer. If a user can do it through `eve ...`, an agent can too. When building your app, apply the same principle:

| Check | How |
|-------|-----|
| Can agents create/read/update/delete every entity? | Map UI actions to CLI/API equivalents |
| Are there UI-only workflows? | Expose them as API endpoints or CLI commands |
| Can agents discover what's available? | Provide `list` operations for every entity type |

**CRUD Completeness**: For every entity in your app, verify agents have Create, Read, Update, and Delete paths. Missing any one breaks parity.

### 2. Granularity — Atomic Primitives, Not Bundled Logic

Features emerge from agent loops, not monolithic tools.

**Wrong**: `deploy_and_monitor(app)` — bundles judgment into code
**Wrong**: `classify_and_organize_files(files)` — agent should decide classification
**Right**: `eve build create`, `eve build run`, `eve env deploy`, `eve job follow` — agent decides the sequence

**On Eve**: The manifest defines WHAT (services, pipelines), the agent decides HOW and WHEN to compose them.

**Design test**: To change behavior, do you edit prose (prompts/skills) or refactor code? If code — your tools aren't atomic enough.

### 3. Composability — New Features = New Prompts

When tools are atomic and parity exists, you add capabilities by writing prompts, not code.

**Eve example**: The `eve-pipelines-workflows` skill adds pipeline composition capability. No new CLI commands needed — the skill teaches agents to compose existing `eve pipeline` and `eve workflow` commands.

**Your app**: If adding a feature requires new API endpoints, you may be bundling logic. Consider whether existing primitives can be composed differently.

### 4. Emergent Capability — Agents Surprise You

Build atomic tools. Agents compose unexpected solutions. You observe patterns. Optimize common patterns. Repeat.

**Eve example**: Agents compose `eve job create --parent` + `eve job dep add` + depth propagation to build arbitrary work hierarchies. The platform didn't prescribe this — agents discovered it from atomic primitives.

## Platform Capabilities for Agentic Apps

Beyond the four principles, Eve provides (or is building) specific primitives that make agentic apps dramatically simpler:

### Job Attachments — Structured Context Passing

Pass plans, reports, and insights between agents without file gymnastics. Attach text documents (markdown, JSON, YAML) to jobs. Downstream agents read attachments from parent jobs. This solves 80% of the "agents passing structured context" problem.

### Service Account Auth — Backend-to-API Communication

Use `eve auth mint` (today) or service accounts (emerging) to authenticate app backends. Every app with a backend needs a non-user token for API calls. Scoped permissions enforce least privilege.

### Org Document Store — Persistent Agent Knowledge

Agents accumulate knowledge that outlives individual jobs: architecture reports, risk assessments, conventions. DB-backed with full-text search and agent-native search/replace editing via PATCH operations.

### Web Chat — Two Mechanisms

Choose based on your needs:
- **Gateway Provider** (Mechanism A): WebSocket to Eve gateway. Zero backend. Best for simple chat widgets and admin consoles.
- **Backend-Proxied** (Mechanism B): App backend calls `POST /internal/orgs/:id/chat/route`. Full control over enrichment, storage, routing. Best for production SaaS.

**Decision**: If your app intercepts, enriches, or stores conversations → use B. Otherwise → use A.

### Cross-Project Queries — Org-Level Intelligence

Portfolio views, dashboards, and any tool spanning multiple projects. Org-level endpoints eliminate N+1 API calls.

See `references/eve-horizon-primitives.md` for the full catalog with API schemas and priority ranking.

## Eve-Specific Design Patterns

### Files as Universal Interface
- Agents know `cat`, `grep`, `mv`, `mkdir`
- Use `.eve/manifest.yaml` as single source of truth — agents read and edit it
- Agent configs live in repo files (`agents.yaml`, `teams.yaml`) — not hidden in databases
- Directory structure = information architecture: `{entity_type}/{entity_id}/content`
- Name files by purpose: `{entity}.json`, `{type}.md`, `agent_log.md`

### Context Injection (Three Layers)
System prompts should include:

1. **Available resources** — what exists, with counts: "12 notes in /notes, 3 projects"
2. **Capabilities** — what agents can do: "Create, edit, tag, delete notes"
3. **Recent activity** — what happened: "User created 'Project kickoff' 2 hours ago"

Eve injects `EVE_API_URL`, `EVE_PROJECT_ID`, `EVE_ORG_ID`, `EVE_ENV_NAME` into every environment. Skills provide domain vocabulary.

### Explicit Completion Signals
- Jobs return `json-result` with `eve.status` ("success", "failed", "waiting")
- No heuristic completion detection — explicit signals always
- Track progress at task level with phase transitions
- Support `shouldContinue` for multi-step operations
- Checkpoint state for resume on interruption

### Dynamic Capability Discovery
- `eve job list` discovers available work
- `eve agents list` discovers available agents
- Skills system auto-discovers capabilities at install time
- Gateway routes messages to agents by slug — new agents are instantly addressable
- Prefer runtime discovery (`list_available_types()`) over static tool-per-endpoint mapping

### Agent-to-UI Communication
- Event types: `thinking`, `toolCall`, `toolResult`, `textResponse`, `statusChange`
- No silent actions — changes visible immediately
- Show progress during execution, not just results
- Consider `ephemeralToolCalls` for noisy internal operations

## The Success Checklist

**Architecture:**
- [ ] Every UI action has a CLI/API equivalent (parity)
- [ ] Every entity has full CRUD (completeness)
- [ ] Tools do one thing; agent decides composition (granularity)
- [ ] Adding capability = adding a skill/prompt, not code (composability)
- [ ] Agent can handle requests you didn't explicitly design for (emergent)

**Implementation:**
- [ ] Manifest and config files are the source of truth (files as interface)
- [ ] System prompt includes resources, capabilities, and recent activity (context injection)
- [ ] Completion is explicit, not heuristic (json-result with eve.status)
- [ ] Agent actions reflect immediately in UI (visibility)
- [ ] Dynamic discovery works for new capabilities (extensibility)

**If building an app with a backend:**
- [ ] Service account auth configured for API access
- [ ] Web chat mechanism chosen (gateway vs. proxied)
- [ ] Job attachments used for structured inter-agent context
- [ ] Org document store for persistent knowledge (when available)

## Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| Agent as router only | Let agents act, not just route |
| Workflow-shaped tools (`analyze_and_deploy`) | Break into atomic primitives |
| UI-only actions | Maintain parity — add CLI/API paths |
| Context starvation | Inject resources via skills and env vars |
| Gates without reason | Default to open; keep primitives available |
| Heuristic completion | Use explicit completion signals |
| Static API mapping | Use dynamic capability discovery |
| Stuffing context in job descriptions | Use job attachments for structured docs |
| Per-user tokens for backends | Use service accounts / eve auth mint |
| Polling for events | Use webhooks when available (emerging) |

## Reference

See `references/eve-horizon-primitives.md` for the full platform primitives catalog with API schemas, DB designs, and implementation priority ranking.

For the source philosophy: `../eve-horizon/docs/ideas/agent-native-design.md`
For platform primitives analysis: `../eve-horizon/docs/ideas/platform-primitives-for-agentic-apps.md`
