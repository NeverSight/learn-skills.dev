---
name: eve-agentic-app-design
description: Layer agentic capabilities onto a full-stack Eve app — agents, teams, multi-model inference, memory, events, chat, and coordination. Use when designing an app where agents are primary actors, not afterthoughts.
triggers:
  - agentic app design
  - agent architecture
  - design agents
  - agent layer
  - agentic design
  - multi agent
  - agent system design
---

# Agentic App Design on Eve Horizon

Transform a full-stack app into one where agents are primary actors — reasoning, coordinating, remembering, and communicating alongside humans.

## When to Use

Load this skill when:
- Designing an app where agents are primary users alongside (or instead of) humans
- Adding agent capabilities to an existing Eve app
- Choosing between human-first and agent-first architecture
- Deciding how agents should coordinate, remember, and communicate
- Planning multi-model inference strategy

## Prerequisite: Start with the Foundation

**Load `eve-fullstack-app-design` first.** The agentic layer builds on a solid PaaS foundation. Without a well-designed manifest, service topology, database, pipeline, and deployment strategy, agentic capabilities collapse into chaos.

The progression:
1. **`eve-agent-native-design`** — Principles (parity, granularity, composability, emergent capability)
2. **`eve-fullstack-app-design`** — PaaS foundation (manifest, services, DB, pipelines, deploys)
3. **This skill** — Agentic layer (agents, teams, inference, memory, events, chat, coordination)

Each layer assumes the previous. Skip none.

## Agent Architecture

### Defining Agents

Agents are defined in `agents.yaml` (path set via `x-eve.agents.config_path` in the manifest). Each agent is a persona with a skill, access scope, and policies.

```yaml
version: 1
agents:
  coder:
    slug: coder
    description: "Implements features and fixes bugs"
    skill: eve-orchestration
    harness_profile: primary-coder
    access:
      envs: [staging]
      services: [api, worker]
    policies:
      permission_policy: auto_edit
      git:
        commit: auto
        push: on_success
    gateway:
      policy: routable
```

**Design decisions for each agent:**

| Decision | Options | Guidance |
|----------|---------|----------|
| Slug | Lowercase, alphanumeric + dashes | Org-unique. Used for chat routing: `@eve coder fix the login bug` |
| Skill | Any installed skill name | The agent's core competency. One skill per agent. |
| Harness profile | Named profile from manifest | Decouples agent from specific models. Use profiles, never hardcode harnesses. |
| Gateway policy | `none`, `discoverable`, `routable` | Default to `none`. Make `routable` only for agents that should receive direct chat. |
| Permission policy | `default`, `auto_edit`, `never`, `yolo` | Start with `auto_edit` for worker agents. Use `default` for agents that need human approval. |
| Git policies | `commit`, `push` | `auto` commit + `on_success` push for coding agents. `never` for read-only agents. |

### Designing Teams

Teams are defined in `teams.yaml`. A team groups agents under a lead with a dispatch strategy.

```yaml
version: 1
teams:
  review-council:
    lead: mission-control
    members: [code-reviewer, security-auditor]
    dispatch:
      mode: council
      merge_strategy: majority
  deploy-ops:
    lead: ops-lead
    members: [deploy-agent, monitor-agent]
    dispatch:
      mode: relay
```

**Choose the right dispatch mode:**

| Mode | When to Use | How It Works |
|------|-------------|--------------|
| `fanout` | Independent parallel work | Root job + parallel child per member. Best for decomposable tasks. |
| `council` | Collective judgment | All agents respond, results merged by strategy (majority, unanimous, lead-decides). Best for reviews, audits. |
| `relay` | Sequential handoff | Lead delegates to first member, output passes to next. Best for staged workflows. |

**Design principle**: Most work is `fanout`. Use `council` only when multiple perspectives genuinely improve the outcome. Use `relay` only when each stage's output is the next stage's input.

## Multi-Model Inference

### Harness Profiles

Define named profiles in the manifest. Agents reference profiles, never specific harnesses.

```yaml
x-eve:
  agents:
    profiles:
      primary-coder:
        - harness: claude
          model: opus-4.5
          reasoning_effort: high
        - harness: codex
          model: gpt-5.2-codex
          reasoning_effort: high
      fast-reviewer:
        - harness: mclaude
          model: sonnet-4.5
          reasoning_effort: medium
```

Profile entries are a fallback chain: if the first harness is unavailable, the next is tried. Design profiles around capability needs, not provider loyalty.

### Model Selection Guidance

| Task Type | Profile Strategy |
|-----------|-----------------|
| Complex coding, architecture | High-reasoning model (opus, gpt-5.2-codex) |
| Code review, documentation | Medium-reasoning model (sonnet, gemini) |
| Triage, routing, classification | Fast model (haiku-equivalent, low reasoning) |
| Specialized domains | Choose the model with strongest domain performance |

### Managed Models

Use managed models (`managed/<name>`) for org-wide or project-wide model policies. The registry merges across scopes: platform <- org <- project.

### Local Inference

For development and cost-sensitive tasks, configure local inference via Ollama targets. Use route policies to direct specific agent types to local models.

## Memory Design

Load `eve-agent-memory` for the full storage primitive catalog. This section focuses on *architectural decisions*.

### What Goes Where

| Information Type | Storage Primitive | Why |
|-----------------|-------------------|-----|
| Scratch notes during a job | Workspace files (`.eve/`) | Ephemeral, dies with the job |
| Job outputs passed to parent | Job attachments | Survives job completion, addressable by job ID |
| Rolling conversation context | Threads | Continuity across sessions, summarizable |
| Curated knowledge | Org Document Store | Versioned, searchable, shared across projects |
| File trees and assets | Org Filesystem (sync) | Bidirectional sync, local editing |
| Structured queries | Managed database | SQL, relationships, RLS |
| Reusable workflows | Skills | Highest-fidelity long-term memory |

### Namespace Conventions

Organize org docs by agent and purpose:

```
/agents/{agent-slug}/learnings/      — discoveries and patterns
/agents/{agent-slug}/decisions/      — decision records
/agents/{agent-slug}/runbooks/       — operational procedures
/agents/shared/                      — cross-agent shared knowledge
/projects/{project-slug}/            — project-scoped knowledge
```

### Lifecycle Strategy

Memory without expiry becomes noise. For every storage location, decide:
1. **Who writes?** Which agents create and update this knowledge.
2. **Who reads?** Which agents query it and when (job start? on demand?).
3. **When does it expire?** Tag with creation dates. Build periodic cleanup jobs.
4. **How does it stay current?** Search before writing. Update beats create.

## Event-Driven Coordination

### The Event Spine

Events are the nervous system of an agentic app. Use them for reactive automation — things that should happen *in response to* other things.

### Trigger Patterns

| Trigger | Event | Response |
|---------|-------|----------|
| Code pushed to main | `github.push` | Run CI pipeline |
| PR opened | `github.pull_request` | Run review council |
| Deploy pipeline failed | `system.pipeline.failed` | Run self-healing workflow |
| Job failed | `system.job.failed` | Run diagnostic agent |
| Org doc created | `system.doc.created` | Notify subscribers, update indexes |
| Scheduled maintenance | `cron.tick` | Run audit, cleanup, reporting |
| Custom app event | `app.*` | Application-specific automation |

### Self-Healing Pattern

Wire system failure events to recovery pipelines:

```yaml
pipelines:
  self-heal:
    trigger:
      system:
        event: job.failed
        pipeline: deploy
    steps:
      - name: diagnose
        agent:
          prompt: "Diagnose the failed deploy and suggest a fix"
```

### Custom App Events

Emit application-specific events from your services:

```bash
eve event emit --type app.invoice.created --source app --payload '{"invoice_id":"inv_123"}'
```

Wire these to workflows or pipelines in the manifest. Design your app's event vocabulary intentionally — events are the API between your app logic and your agent automation.

## Chat and Human-Agent Interface

### Gateway Architecture

Eve supports multiple chat providers through a unified gateway:

| Provider | Transport | Best For |
|----------|-----------|----------|
| Slack | Webhook | Team collaboration, existing Slack workspaces |
| Nostr | Subscription | Decentralized, privacy-focused, censorship-resistant |
| WebChat | WebSocket | Browser-native, embedded in your app |

### Routing Design

Define routes in `chat.yaml` to map inbound messages to agents or teams:

```yaml
version: 1
default_route: route_default
routes:
  - id: deploy-route
    match: "deploy|release|ship"
    target: agent:deploy-agent
  - id: review-route
    match: "review|PR|pull request"
    target: team:review-council
  - id: route_default
    match: ".*"
    target: agent:mission-control
```

Route targets can be `agent:<key>`, `team:<key>`, `workflow:<name>`, or `pipeline:<name>`.

### Gateway vs Backend-Proxied Chat

| Approach | When to Use |
|----------|-------------|
| **Gateway provider** (WebSocket to Eve) | Simple chat widgets, admin consoles, no backend needed |
| **Backend-proxied** (`POST /internal/orgs/:id/chat/route`) | Production SaaS, when you need to intercept, enrich, or store conversations |

If your app needs to add context, filter messages, or maintain its own chat history — proxy through your backend.

### Thread Continuity

Chat threads maintain context across messages. Thread keys are scoped to the integration account. Design your chat UX to preserve thread context — agents are dramatically more effective when they can reference conversation history.

## Jobs as Coordination Primitive

### Parent-Child Orchestration

Jobs are the fundamental unit of agent work. Design complex workflows as job trees:

```
Parent (orchestrator)
├── Child A (research)
├── Child B (implementation)
└── Child C (testing)
```

The parent dispatches, waits, resumes, synthesizes. Children execute independently. Use `waits_for` relations to express dependencies. See `eve-orchestration` for full patterns.

### Structured Context via Attachments

Pass structured data between agents using job attachments, not giant description strings:

```bash
# Child stores findings
eve job attach $EVE_JOB_ID --name findings.json --content '{"patterns": [...]}'

# Parent reads on resume
eve job attachment $CHILD_JOB_ID findings.json --out ./child-findings.json
```

### Resource Refs for Document Mounting

Pin specific org document versions as job inputs:

```bash
eve job create \
  --description "Review the approved plan" \
  --resource-refs='[{"uri":"org_docs:/pm/features/FEAT-123.md@v3","label":"Plan","mount_path":"pm/plan.md"}]'
```

The document is hydrated into the workspace at the mount path. Events track hydration success or failure.

### Coordination Threads

When teams dispatch work, a coordination thread (`coord:job:{parent_job_id}`) links parent and children. Children read `.eve/coordination-inbox.md` for sibling context. Post updates via `eve thread post`. The lead agent can `eve supervise` to monitor the job tree.

## Access and Security

### Service Accounts

Backend services need non-user tokens for API calls. Use `eve auth mint` to create scoped tokens:

```bash
eve auth mint --email app-bot@example.com --project proj_xxx --role admin
```

Design each service account with minimal necessary scope.

### Access Groups

Segment data-plane access using groups. Groups control who can read/write org docs, org filesystem paths, and database schemas:

```yaml
# .eve/access.yaml
version: 2
access:
  groups:
    eng-team:
      name: Engineering
      members:
        - type: user
          id: user_abc
  bindings:
    - subject: { type: group, id: eng-team }
      roles: [data-reader]
      scope:
        orgdocs: { allow_prefixes: ["/agents/shared/"] }
        envdb: { schemas: ["public"] }
```

Sync with `eve access sync --file .eve/access.yaml --org org_xxx`.

### Agent Permission Policies

| Policy | Use Case |
|--------|----------|
| `default` | Interactive agents that need human approval for risky actions |
| `auto_edit` | Worker agents that edit code and files autonomously |
| `never` | Read-only agents (auditors, reviewers) |
| `yolo` | Fully autonomous agents in controlled environments (use carefully) |

### Policy-as-Code

Declare all access in `.eve/access.yaml` and sync declaratively. This ensures access is version-controlled, reviewable, and reproducible. See `eve-auth-and-secrets` for the full v2 policy schema.

## The Agentic Checklist

**Agent Architecture:**
- [ ] Agents defined in `agents.yaml` with clear slug, skill, and profile
- [ ] Teams defined in `teams.yaml` with appropriate dispatch modes
- [ ] Gateway policies set intentionally (not everything routable)
- [ ] Chat routes defined for inbound message handling

**Inference:**
- [ ] Harness profiles defined in manifest (agents reference profiles, not harnesses)
- [ ] Fallback chains in profiles for resilience
- [ ] Model choice matches task complexity

**Memory:**
- [ ] Storage primitive chosen for each information type (see table above)
- [ ] Namespace conventions established for org docs
- [ ] Lifecycle and expiry strategy defined
- [ ] Agents search before writing (update beats create)

**Events:**
- [ ] Trigger patterns wired for key events (push, PR, failures)
- [ ] Self-healing pipeline exists for deploy and job failures
- [ ] Custom app events defined for domain-specific automation

**Chat:**
- [ ] Gateway provider chosen (Slack, Nostr, WebChat, or multiple)
- [ ] Chat routing configured (`chat.yaml`)
- [ ] Gateway vs backend-proxied decision made
- [ ] Thread continuity preserved in UX

**Coordination:**
- [ ] Complex work decomposed as job trees (parent-child)
- [ ] Attachments used for structured context passing
- [ ] Coordination threads used for team communication
- [ ] Resource refs used for document mounting

**Security:**
- [ ] Service accounts created for backend services
- [ ] Access groups defined for data-plane segmentation
- [ ] Agent permission policies appropriate to each agent's role
- [ ] Access policy declared as code (`.eve/access.yaml`)

**The Real Test — Is This App Truly Agent-Native?**
- [ ] Agents can do everything users can (parity)
- [ ] Adding capability means writing prompts, not code (composability)
- [ ] Agents coordinate through platform primitives, not custom glue (granularity)
- [ ] Agents have surprised you with unexpected solutions (emergent capability)

## Cross-References

- **Principles**: `eve-agent-native-design` — parity, granularity, composability, emergent capability
- **PaaS foundation**: `eve-fullstack-app-design` — manifest, services, DB, pipelines, deploys
- **Storage primitives**: `eve-agent-memory` — detailed guidance on each memory primitive
- **Job orchestration**: `eve-orchestration` — depth propagation, parallel decomposition, control signals
- **Agents and teams reference**: `eve-read-eve-docs` → `references/agents-teams.md`
- **Harness execution**: `eve-read-eve-docs` → `references/harnesses.md`
- **Chat gateway**: `eve-read-eve-docs` → `references/gateways.md`
- **Events and triggers**: `eve-read-eve-docs` → `references/events.md`
