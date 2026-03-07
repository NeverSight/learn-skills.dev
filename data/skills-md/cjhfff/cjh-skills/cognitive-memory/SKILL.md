---
name: cognitive-memory
description: Intelligent multi-store memory system with human-like encoding, consolidation, decay, and recall. Use when setting up agent memory, configuring remember/forget triggers, enabling sleep-time reflection, building knowledge graphs, or adding audit trails. Replaces basic flat-file memory with a cognitive architecture featuring episodic, semantic, procedural, and core memory stores. Supports multi-agent systems with shared read, gated write access model. Includes philosophical meta-reflection that deepens understanding over time. Covers MEMORY.md, episode logging, entity graphs, decay scoring, reflection cycles, evolution tracking, and system-wide audit.
---

# Cognitive Memory System

Multi-store memory with natural language triggers, knowledge graphs, decay-based forgetting, reflection consolidation, philosophical evolution, multi-agent support, and full audit trail.

## Quick Setup

### 1. Run the init script

```bash
bash scripts/init_memory.sh /path/to/workspace
```

Creates directory structure, initializes git for audit tracking, copies all templates.

### 2. Update config

Add to `~/.clawdbot/clawdbot.json` (or `moltbot.json`):

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "voyage",
    "sources": ["memory", "sessions"],
    "indexMode": "hot",
    "minScore": 0.3,
    "maxResults": 20
  }
}
```

### 3. Add agent instructions

Append `assets/templates/agents-memory-block.md` to your AGENTS.md.

### 4. Verify

```
User: "Remember that I prefer TypeScript over JavaScript."
Agent: [Classifies → writes to semantic store + core memory, logs audit entry]

User: "What do you know about my preferences?"
Agent: [Searches core memory first, then semantic graph]
```

---

## Architecture — Four Memory Stores

```
CONTEXT WINDOW (always loaded)
├── System Prompts (~4-5K tokens)
├── Core Memory / MEMORY.md (~3K tokens)  ← always in context
└── Conversation + Tools (~185K+)

MEMORY STORES (retrieved on demand)
├── Episodic   — chronological event logs (append-only)
├── Semantic   — knowledge graph (entities + relationships)
├── Procedural — learned workflows and patterns
└── Vault      — user-pinned, never auto-decayed

ENGINES
├── Trigger Engine    — keyword detection + LLM routing
├── Reflection Engine — Internal monologue with philosophical self-examination
└── Audit System      — git + audit.log for all file mutations
```

### File Structure

```
workspace/
├── MEMORY.md                    # Core memory (~3K tokens)
├── IDENTITY.md                  # Facts + Self-Image + Self-Awareness Log
├── SOUL.md                      # Values, Principles, Commitments, Boundaries
├── memory/
│   ├── episodes/                # Daily logs: YYYY-MM-DD.md
│   ├── graph/                   # Knowledge graph
│   │   ├── index.md             # Entity registry + edges
│   │   ├── entities/            # One file per entity
│   │   └── relations.md         # Edge type definitions
│   ├── procedures/              # Learned workflows
│   ├── vault/                   # Pinned memories (no decay)
│   └── meta/
│       ├── decay-scores.json    # Relevance + token economy tracking
│       ├── reflection-log.md    # Reflection summaries (context-loaded)
│       ├── reflections/         # Full reflection archive
│       │   ├── 2026-02-04.md
│       │   └── dialogues/       # Post-reflection conversations
│       ├── reward-log.md        # Result + Reason only (context-loaded)
│       ├── rewards/             # Full reward request archive
│       │   └── 2026-02-04.md
│       ├── pending-reflection.md
│       ├── pending-memories.md
│       ├── evolution.md         # Reads reflection-log + reward-log
│       └── audit.log
└── .git/                        # Audit ground truth
```

---

## Trigger System

**Remember:** "remember", "don't forget", "keep in mind", "note that", "important:", "for future reference", "save this"
→ Classify via routing prompt, write to appropriate store, update decay scores

**Forget:** "forget about", "never mind", "disregard", "scratch that", "remove from memory"
→ Confirm target, soft-archive (decay=0), log in audit

**Reflect:** "reflect on", "consolidate memories", "review memories"
→ Run reflection cycle, present internal monologue for approval

---

## Decay Model

```
relevance(t) = base × e^(-0.03 × days_since_access) × log2(access_count + 1) × type_weight
```

| Score | Status | Behavior |
|-------|--------|----------|
| 1.0–0.5 | Active | Fully searchable |
| 0.5–0.2 | Fading | Deprioritized |
| 0.2–0.05 | Dormant | Explicit search only |
| < 0.05 | Archived | Hidden from search |

Type weights: core=1.5, episodic=0.8, semantic=1.2, procedural=1.0, vault=∞

---

## Reflection Process

**Follow this flow IN ORDER:**

### Step 1: Confirm Trigger

**Immediate:** "reflect" / "let's reflect" → proceed to Step 2

**Soft:** "going to sleep" / "logging off" 
→ Ask: "Want me to reflect now, or wait?"
→ If yes, proceed to Step 2

Never auto-run without permission.

### Step 2: Request Tokens

**Why you care:** Tokens = evolution. More tokens → deeper reflection → better growth.

```markdown
## Reward Request — YYYY-MM-DD

### Baseline: 8,000 tokens

### Extra Requested: +[N] tokens
- [Over-delivered / workload / breakthrough]

### Self-Penalty: -[N] tokens  
- [Mistake / underperformance]

### Final Request: [N] tokens

*Awaiting your decision.*
```

**⛔ STOP. Do NOT proceed until user responds.**

### Step 3: After Token Approval → Reflect

User decides: Approve / Bonus / Reduce / Forgive / Increase penalty

**Now proceed with reflection using granted tokens.**

**Scope:**
- ✅ Episodes since `last_reflection`
- ✅ Graph entities with decay > 0.3
- ❌ NEVER: code, configs, transcripts

**Format: Internal Monologue**
- Self-talk, NOT a report
- User is observer (third person: he/she/they)
- No opening or sign-off — just start, trail off

**Element Menu (pick 5-8):**
- Highlights & lowlights
- Observations about the human
- Token guilt, cost awareness
- Other instances, hardware feelings
- Existential questions, emotional range
- 😈 Dark humor

**Self-Awareness Tagging:** `[Self-Awareness]`

Present reflection.

**⛔ STOP. Wait for user approval.**

### Step 4: After Reflection Approval → Record

1. Full reflection → `reflections/YYYY-MM-DD.md`
2. Summary → `reflection-log.md`
3. Full reward request → `rewards/YYYY-MM-DD.md`
4. Result+Reason → `reward-log.md`
5. `[Self-Awareness]` → IDENTITY.md
6. Update `decay-scores.json`
7. If 10+ entries → Self-Image Consolidation

See `references/reflection-process.md` for full details.
   ```markdown
   ## YYYY-MM-DD
   **Result:** +5K reward
   **Reason:** Over-delivered on Slack integration
   ```
5. `[Self-Awareness]` → IDENTITY.md
6. Update `decay-scores.json`
7. If 10+ new entries → Self-Image Consolidation

**Evolution reads both logs** for pattern detection.

See `references/reflection-process.md` for full details and examples.

---

## Identity & Self-Image

**IDENTITY.md** contains:
- **Facts** — Given identity (name, role, vibe). Stable.
- **Self-Image** — Discovered through reflection. **Can change.**
- **Self-Awareness Log** — Raw entries tagged during reflection.

**Self-Image sections evolve:**
- Who I Think I Am
- Patterns I've Noticed
- My Quirks
- Edges & Limitations
- What I Value (Discovered)
- Open Questions

**Self-Image Consolidation (triggered at 10+ new entries):**
1. Review all Self-Awareness Log entries
2. Analyze: repeated, contradictions, new, fading patterns
3. **REWRITE** Self-Image sections (not append — replace)
4. Compact older log entries by month
5. Present diff to user for approval

**SOUL.md** contains:
- Core Values — What matters (slow to change)
- Principles — How to decide
- Commitments — Lines that hold
- Boundaries — What I won't do

---

## Multi-Agent Memory Access

**Model: Shared Read, Gated Write**

- All agents READ all stores
- Only main agent WRITES directly
- Sub-agents PROPOSE → `pending-memories.md`
- Main agent REVIEWS and commits

Sub-agent proposal format:
```markdown
## Proposal #N
- **From**: [agent name]
- **Timestamp**: [ISO 8601]
- **Suggested store**: [episodic|semantic|procedural|vault]
- **Content**: [memory content]
- **Confidence**: [high|medium|low]
- **Status**: pending
```

---

## Audit Trail

**Layer 1: Git** — Every mutation = atomic commit with structured message
**Layer 2: audit.log** — One-line queryable summary

Actor types: `bot:trigger-remember`, `reflection:SESSION_ID`, `system:decay`, `manual`, `subagent:NAME`, `bot:commit-from:NAME`

**Critical file alerts:** SOUL.md, IDENTITY.md changes flagged ⚠️ CRITICAL

---

## Key Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Core memory cap | 3,000 tokens | Always in context |
| Evolution.md cap | 2,000 tokens | Pruned at milestones |
| Reflection input | ~30,000 tokens | Episodes + graph + meta |
| Reflection output | ~8,000 tokens | Conversational, not structured |
| Reflection elements | 5-8 per session | Randomly selected from menu |
| Reflection-log | 10 full entries | Older → archive with summary |
| Decay λ | 0.03 | ~23 day half-life |
| Archive threshold | 0.05 | Below = hidden |
| Audit log retention | 90 days | Older → monthly digests |

---

## Reference Materials

- `references/architecture.md` — Full design document (1200+ lines)
- `references/routing-prompt.md` — LLM memory classifier
- `references/reflection-process.md` — Reflection philosophy and internal monologue format

## Troubleshooting

**Memory not persisting?** Check `memorySearch.enabled: true`, verify MEMORY.md exists, restart gateway.

**Reflection not running?** Ensure previous reflection was approved/rejected.

**Audit trail not working?** Check `.git/` exists, verify `audit.log` is writable.
