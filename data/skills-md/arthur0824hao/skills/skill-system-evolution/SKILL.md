---
name: skill-system-evolution
description: "Version-controlled evolution engine that uses accumulated insight results to evolve soul profiles and workflow recipes with auditability, safety constraints, and rollbacks."
license: MIT
compatibility: opencode
metadata:
  os: windows, linux, macos
  storage: postgres.agent_memories
---

# Skill System Evolution

Version-controlled evolution engine that uses insight results to evolve soul profiles and workflow recipes.

This skill is the ACT half of the system: it reads accumulated observation data, decides changes that are justified by evidence, applies them conservatively, and records a versioned snapshot for every change.

## Key Concepts

1) Insight = OBSERVE
   - Extract facets from sessions and accumulate buffers.
   - This is handled by `skill-system-insight`.

2) Evolution = ACT
   - Read accumulated data and decide changes.
   - Apply changes with strong evidence only.
   - Always version and store an audit snapshot.

3) Every evolution creates a versioned snapshot
   - No mutation without a recorded snapshot.
   - Snapshots are stored in Postgres (`agent_memories`) and can be listed/rolled back.

4) Users can list, compare, rollback, and pin versions
   - `list-versions` provides the history.
   - `rollback` restores a prior snapshot (and records the rollback as its own snapshot).
   - Pinning is represented as an additional tag on the snapshot (e.g., `pin:true`) or as a separate memory record (implementation choice for the operator).

## Architecture

### Reads

- Insight facets:
  - `agent_memories.category = 'insight-facet'`
  - Tags include `user:<user>`
- Soul state (dual matrix):
  - `agent_memories.category = 'soul-state'`
  - Tags include `user:<user>` and `matrix`

### Writes

- Evolution snapshots:
  - `agent_memories.category = 'evolution-snapshot'`
  - Each snapshot stores the full artifact YAML/markdown in `snapshot_data`
- Soul profiles (filesystem):
  - `../skill-system-soul/profiles/<user>.md`
- Workflow recipes (filesystem):
  - `../skill-system-workflow/recipes/*.yaml` (or `.yml`)

### Version tags

Version tag format:

`v{N}_{target}_{timestamp}`

Example: `v3_soul_20260211`

Recommended versioning algorithm per user+target:

- Let `N = 1 + max(existing N)` for snapshots with tags `user:<user>` and `target:<target>`.
- If none exist, start at `N = 1`.
- Timestamp uses local date (YYYYMMDD) unless you need time disambiguation; if you do, append `_HHMM`.

## Operational Constraints

- Max 1 evolution pass per day per user.
  - Applies across targets (soul/recipe/both). Use the most recent `evolution-snapshot` date as the limiter.
- Transparency: always explain what changed and why.
  - Every proposed change must include evidence strings from facets or state context.
- Safety: cannot remove core safety constraints from soul profiles.
  - The evolved profile must retain baseline safety expectations: honest uncertainty, no hallucinated authority, and refusal of harmful/illegal instructions.
- User approval: major changes require confirmation.
  - If any proposed personality dimension change has `abs(proposed_value - current_value) > 0.5`, do not apply automatically.
  - Instead, produce an evolution plan and ask for explicit approval.

## Relationship to `skill-system-insight`

For new installations, `skill-system-evolution` supersedes the insight skill's synthesis operation:

- `skill-system-insight` remains the source of facets and matrix updates.
- Layer 3 profile generation (synthesis) is performed and versioned here, so changes are auditable and reversible.

## Storage Pattern (agent_memories)

Evolution snapshots are stored as episodic memories:

- `memory_type = 'episodic'`
- `category = 'evolution-snapshot'`
- `tags` include:
  - `user:<user>`
  - `target:<target>` where target is `soul`, `recipe`, or `both`
  - `version:<version_tag>`

Example SQL templates (copy/paste and substitute values):

```sql
-- Rate limit check (max 1/day): any snapshot in last 24h?
SELECT id, created_at, title
FROM agent_memories
WHERE category = 'evolution-snapshot'
  AND 'user:<user>' = ANY(tags)
  AND created_at >= (NOW() - INTERVAL '24 hours')
ORDER BY created_at DESC
LIMIT 1;

-- Store an evolution snapshot
SELECT store_memory(
  'episodic',
  'evolution-snapshot',
  ARRAY['user:<user>', 'target:<target>', 'version:<version_tag>'],
  'Evolution Snapshot: <version_tag>',
  '<full evolution-snapshot YAML as text>',
  '{"version_tag": "<version_tag>", "target": "<target>", "timestamp": "<iso>"}',
  'evolution-agent',
  NULL,
  8.0
);

-- List recent snapshots for a user (most recent first)
SELECT id, created_at, title
FROM agent_memories
WHERE category = 'evolution-snapshot'
  AND 'user:<user>' = ANY(tags)
ORDER BY created_at DESC
LIMIT 50;
```

## Operations

- `evolve-soul`
  - Check if matrix has enough data (buffer threshold) and/or synthesis is pending.
  - Apply pending matrix updates.
  - Synthesize new Layer 3 profile using evidence (last 50 facets), then version it.

- `evolve-recipes`
  - Analyze workflow facets to detect friction/outcomes.
  - Propose conservative recipe modifications and version them.

- `list-versions`
  - List evolution history for a user, optionally filtered by target.

- `rollback`
  - Restore a previous version of soul or recipes.
  - Records the rollback as a new snapshot.

```skill-manifest
{
  "schema_version": "2.0",
  "id": "skill-system-evolution",
  "version": "1.0.0",
  "capabilities": ["evolution-soul", "evolution-recipes", "evolution-list", "evolution-rollback"],
  "effects": ["db.read", "db.write", "fs.read", "fs.write"],
  "operations": {
    "evolve-soul": {
      "description": "Evolve soul profile from accumulated insight data. Creates versioned snapshot.",
      "input": {
        "user": {"type": "string", "required": true, "description": "User handle"}
      },
      "output": {
        "description": "Evolution result with version tag",
        "fields": {"version_tag": "string", "changes": "array", "profile_path": "string"}
      },
      "entrypoints": {
        "agent": "Follow scripts/evolve-soul.md procedure"
      }
    },
    "evolve-recipes": {
      "description": "Evolve workflow recipes based on effectiveness data from insight facets.",
      "input": {
        "user": {"type": "string", "required": true, "description": "User handle"}
      },
      "output": {
        "description": "Recipe evolution result with version tag",
        "fields": {"version_tag": "string", "recipes_changed": "array"}
      },
      "entrypoints": {
        "agent": "Follow scripts/evolve-recipes.md procedure"
      }
    },
    "list-versions": {
      "description": "List all evolution snapshots for a user.",
      "input": {
        "user": {"type": "string", "required": true},
        "target": {"type": "string", "required": false, "description": "Filter: soul | recipe | all"}
      },
      "output": {
        "description": "Array of version snapshots",
        "fields": {"versions": "array of {tag, target, timestamp, summary}"}
      },
      "entrypoints": {
        "agent": "Follow scripts/list-versions.md procedure"
      }
    },
    "rollback": {
      "description": "Restore a previous evolution version.",
      "input": {
        "user": {"type": "string", "required": true},
        "version_tag": {"type": "string", "required": true, "description": "Version tag to restore"}
      },
      "output": {
        "description": "Rollback result",
        "fields": {"status": "ok | error", "restored_from": "string"}
      },
      "entrypoints": {
        "agent": "Follow scripts/rollback.md procedure"
      }
    }
  },
  "stdout_contract": {
    "last_line_json": false,
    "note": "Agent-executed procedures; versioned snapshots stored in agent_memories."
  }
}
```
