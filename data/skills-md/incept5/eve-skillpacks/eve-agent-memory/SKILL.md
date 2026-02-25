---
name: eve-agent-memory
description: Choose and combine Eve storage primitives to give agents persistent memory — short-term workspace, medium-term attachments and threads, long-term org docs and filesystem. Use when designing how agents remember, retrieve, and share knowledge.
---

# Eve Agent Memory

Agents on Eve Horizon have no built-in "memory" primitive, but the platform provides storage systems at every timescale. This skill teaches how to compose them into coherent memory for agents that learn, remember, and share.

## The Memory Problem

Every agent starts cold. Without deliberate memory design, agents:

- Re-discover the same facts on every job.
- Lose context when jobs end.
- Cannot share learned knowledge with sibling agents.
- Accumulate stale information with no expiry.

Solve this by mapping **what to remember** to **where to store it**, using the right primitive for each timescale.

## Storage Primitives by Timescale

### Short-Term (within a job)

**Workspace files** — the git repo checkout available during job execution.

```bash
# Workspace is at $EVE_REPO_PATH
# Write working state to .eve/ (gitignored by convention)
echo '{"findings": [...]}' > .eve/agent-scratch.json

# Workspace modes control sharing:
#   job       — fresh checkout per job (default)
#   session   — shared across jobs in a session
#   isolated  — no git state, pure scratch
eve job create --workspace-mode session --workspace-key "auth-sprint"
```

Use for: scratch notes, intermediate results, coordination inbox files. Ephemeral by design — workspace state does not survive the job unless committed to git or saved elsewhere.

**Coordination inbox** — `.eve/coordination-inbox.md` is auto-generated from coordination thread messages at job start. Read it for sibling status without API calls.

### Medium-Term (across jobs within a project)

**Job attachments** — named key-value pairs attached to any job. Survive after job completion.

```bash
# Store findings
eve job attach $EVE_JOB_ID --name findings.json --content '{"patterns": [...]}'
eve job attach $EVE_JOB_ID --name summary.md --file ./analysis-summary.md

# Retrieve from any job (including parent/child)
eve job attachment $PARENT_JOB_ID findings.json --out ./prior-findings.json
eve job attachments $JOB_ID  # list all
```

Use for: job outputs, decision records, analysis results. Attached to a specific job, so retrievable by job ID. Good for passing structured data between parent and child jobs.

**Threads** — message sequences with continuity across sessions.

```bash
# Project threads maintain chat context
eve thread messages $THREAD_ID --since 1h

# Coordination threads connect parent/child agents
eve thread post $COORD_THREAD_ID --body '{"kind":"update","body":"Found 3 auth issues"}'
eve thread follow $COORD_THREAD_ID  # poll for sibling updates
```

Use for: inter-agent communication, rolling context, coordination. Thread summaries provide compressed history. Coordination threads (`coord:job:{parent_job_id}`) are auto-created for team dispatches.

**Resource refs** — versioned pointers to org documents, mounted into job workspaces.

```bash
eve job create \
  --description "Review the approved plan" \
  --resource-refs='[{"uri":"org_docs:/pm/features/FEAT-123.md@v3","label":"Plan","mount_path":"pm/plan.md"}]'
```

Use for: pinning specific document versions as job inputs. The referenced document is hydrated into the workspace at the specified mount path. Events track hydration success/failure.

### Long-Term (across projects, persistent)

**Org Document Store** — versioned documents scoped to the organization.

```bash
# Store knowledge
eve docs create --org $ORG_ID --path /agents/learnings/auth-patterns.md --file ./auth-patterns.md
eve docs update --org $ORG_ID --path /agents/learnings/auth-patterns.md --file ./updated.md

# Retrieve
eve docs get --org $ORG_ID --path /agents/learnings/auth-patterns.md
eve docs list --org $ORG_ID --prefix /agents/learnings/

# Search
eve docs search --org $ORG_ID --query "authentication retry"
```

Use for: curated knowledge, decision logs, learned patterns. Versioned (every update creates a new version). Emits `system.doc.created/updated/deleted` events on the event spine. Best for knowledge that is reviewed, refined, and shared.

**Org Filesystem (sync)** — bidirectional file sync between local machines and org storage.

```bash
# Set up sync (developer/operator machine)
eve fs sync init --org $ORG_ID --local ~/Eve/acme --mode two-way

# Status and monitoring
eve fs sync status --org $ORG_ID
eve fs sync logs --org $ORG_ID --follow
```

Use for: large knowledge bases, design assets, documentation trees. Markdown-first defaults. Syncthing-based data plane with event-driven notifications (`file.created/updated/deleted`). Best for knowledge that lives as a file tree and benefits from local editing.

**Skills and Skillpacks** — distilled patterns packaged for reuse.

Use for: encoding recurring workflows and hard-won knowledge as reusable instructions. When an agent discovers a pattern worth preserving, distill it into a skill (see `eve-skill-distillation`). Skills are the highest-fidelity form of long-term memory — they don't just store information, they teach how to use it.

**Managed databases** — environment-scoped Postgres instances with agent-accessible SQL.

```bash
eve db sql --env $ENV --sql "SELECT key, value FROM agent_memory WHERE agent_id = 'reviewer' AND expires_at > NOW()"
eve db sql --env $ENV --sql "INSERT INTO agent_memory (agent_id, key, value) VALUES ('reviewer', 'last_review', '...')" --write
```

Use for: structured queries, relationship data, anything that benefits from SQL. Requires schema setup via migrations. Use `eve db rls init --with-groups` for access-controlled agent memory tables.

### Shared (coordination across agents)

**Org threads** — org-scoped message sequences for cross-project coordination.

```bash
eve thread list --org $ORG_ID
eve thread post $ORG_THREAD_ID --body '{"kind":"directive","body":"All agents: use new auth pattern"}'
```

**Event spine** — pub/sub event bus for reactive workflows.

```bash
eve event emit --type=agent.memory.updated --source=app --payload '{"agent":"reviewer","key":"patterns"}'
eve event list --type agent.memory.*
```

Use for: broadcasting knowledge updates, triggering reactive workflows when memory changes.

## Memory Patterns

### Pattern 1: Job-Scoped Scratch

The simplest pattern. Write working state to workspace files during execution. Nothing survives the job.

```
Job starts → read inputs → write .eve/scratch.json → process → complete
```

When to use: single-job tasks with no memory requirement.

### Pattern 2: Parent-Child Knowledge Passing

Pass knowledge between orchestrator and workers using attachments and threads.

```
Parent creates children with resource-refs →
Children execute, attach findings →
Parent resumes, reads child attachments →
Parent synthesizes into final output
```

```bash
# Child stores its findings
eve job attach $EVE_JOB_ID --name findings.json --content "$FINDINGS"

# Parent reads child findings on resume
for child_id in $CHILD_IDS; do
  eve job attachment $child_id findings.json --out ./child-${child_id}.json
done
```

When to use: orchestrated work where children discover information the parent needs.

### Pattern 3: Org Knowledge Base

Build persistent, searchable knowledge that survives across projects and time.

```
Agent discovers pattern →
Check if existing doc covers it (eve docs search) →
  If yes: update with new information (eve docs update)
  If no: create new document (eve docs create) →
Emit event for other agents (eve event emit)
```

Namespace convention for agent-maintained docs:

```
/agents/{agent-slug}/learnings/     — patterns and discoveries
/agents/{agent-slug}/decisions/     — decision records with rationale
/agents/{agent-slug}/runbooks/      — operational procedures
/agents/shared/                     — cross-agent shared knowledge
```

When to use: knowledge that accumulates over time and should be available to any agent in the org.

### Pattern 4: Memory-Augmented Job Start

Combine primitives to give an agent relevant context at the start of every job.

```
Job starts →
Read coordination inbox (.eve/coordination-inbox.md) →
Query org docs for relevant prior knowledge (eve docs search) →
Check parent/sibling attachments for recent findings →
Proceed with enriched context
```

```bash
# Startup sequence
cat .eve/coordination-inbox.md 2>/dev/null  # sibling context
eve docs search --org $ORG_ID --query "$JOB_DESCRIPTION_KEYWORDS"  # prior knowledge
eve job attachments $PARENT_JOB_ID  # parent context
```

When to use: any agent that benefits from remembering what happened before.

## Choosing the Right Primitive

| Question | Answer → Primitive |
|---|---|
| Need it only during this job? | Workspace files |
| Need to pass data to parent/children? | Job attachments |
| Need rolling conversation context? | Threads |
| Need versioned, searchable documents? | Org Document Store |
| Need file-tree sync with local editing? | Org Filesystem |
| Need structured queries (SQL)? | Managed database |
| Need to encode a reusable workflow? | Skills |
| Need reactive notifications? | Event spine |

## Access Control

Storage primitives respect Eve's access model:

- **Secrets**: scoped resolution (project → user → org → system). Never store memory in secrets.
- **Org docs**: org membership required. Use access groups for fine-grained control.
- **Database**: use RLS with group-aware policies for multi-agent isolation.
- **Threads**: project-scoped or org-scoped. Job tokens grant access to coordination threads.
- **Filesystem**: org-level permissions, with optional path ACLs via access groups.

```bash
# Check agent's effective access
eve access can --resource orgdocs:/agents/shared/ --action read
eve access memberships --org $ORG_ID
```

## Anti-Patterns

- **Storing everything in workspace files** — dies with the job. Use attachments or org docs for anything worth keeping.
- **Giant thread messages as memory** — threads are for communication, not storage. Post summaries, store details in docs.
- **No expiry strategy** — memory without lifecycle becomes noise. Date your documents, prune periodically.
- **Duplicating knowledge across primitives** — pick one source of truth per piece of knowledge. Reference it from other places, don't copy it.
- **Skipping search before writing** — always check if the knowledge already exists before creating a new document. Update beats create.

## Current Gaps and Workarounds

Some memory patterns require manual assembly today:

- **No dedicated KV store** — use managed DB with a simple `key/value/ttl` table, or org docs with path-based keys.
- **No vector search** — use keyword search via `eve docs search` for now. Structure documents with clear headings and terms to improve retrieval.
- **No automatic context carryover** — build startup sequences manually (see Pattern 4). Consider encoding these as job templates or skill instructions.
- **No document lifecycle automation** — set TTLs manually or build periodic cleanup jobs. Tag documents with creation dates and review dates.
