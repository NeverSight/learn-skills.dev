---
name: skill-auditor
description: >
  Analyzes Claude Code session transcripts to evaluate skill portfolio health —
  routing errors, attention competition between descriptions, and coverage gaps.
  Generates an interactive HTML report with per-skill health cards, competition
  matrix, attention budget analysis, and actionable patches. Unlike skill-creator
  which optimizes individual skills in isolation, skill-auditor optimizes the
  portfolio as a system, detecting cross-skill attention theft and cascade risks.
  Use when user says "audit my skills", "skill audit", "run skill-auditor",
  "analyze skill routing", "check skill competition", "portfolio health",
  "スキル監査", "スキルの精度を分析", "スキルルーティング分析".
disable-model-invocation: true
---

# Skill Auditor

Portfolio-level skill routing analysis and optimization. Analyzes real session
transcripts to find routing errors, attention competition, and coverage gaps,
then generates an interactive HTML report.

## Prerequisites

- `pip install tiktoken` (optional — falls back to character-based estimation)
- No external API keys required. Analysis uses Claude sub-agents.

## Workflow

Run all steps sequentially. The coordinator (you) manages data flow between
scripts and sub-agents.

### Step 0: Initial Questions

Before starting, ask the user two questions using AskUserQuestion:

1. **Report language**: "レポートの言語は？ (e.g. 日本語, English, 中文, ...)"
   — Free text input. Default to the user's conversation language if not specified.
2. **Scope**: "分析範囲はどうしますか？" — Cross-project (all projects) / Current project only

Store these choices. Pass the language choice to all sub-agents as an
instruction prefix: "Write all output text (health_assessment, detail, reason,
suggested_fix, etc.) in [chosen language]."

For cross-project mode, use `"all"` as the project_path argument in Step 3.
For current-project mode, use `--cwd "$(pwd)"`.

### Step 1: Detect Project

If cross-project mode was selected:
```bash
python3 scripts/collect_transcripts.py all --days 14 \
  --output <workspace>/transcripts.json --verbose
```

If current-project mode:
```bash
python3 scripts/collect_transcripts.py --cwd "$(pwd)" --days 14 \
  --output <workspace>/transcripts.json --verbose
```

If auto-detection fails, show the list and ask the user which project to audit.

For cross-project mode, base dir: `~/.claude/skill-report/`.
For current-project mode, base dir: `<project>/.claude/skill-report/`.

### Step 2: Set Up Workspace

Each run gets a timestamped subdirectory so multiple runs never collide:

```bash
RUN_ID=$(date +%Y-%m-%dT%H-%M-%S)
WORKSPACE=<base_dir>/${RUN_ID}
mkdir -p ${WORKSPACE}
```

Use `${WORKSPACE}` as `<workspace>` in all subsequent steps.
`health-history.json` stays at `<base_dir>/health-history.json` (shared
across runs — see Step 8).

### Step 3: Collect Data

Run both scripts. They produce the input files for analysis.

```bash
# Transcripts already collected in Step 1

python3 scripts/collect_skills.py \
  --output <workspace>/skill-manifest.json --verbose
```

Report the collection summary to the user:
"N sessions, M user turns, K skills found. Attention budget: T tokens total."

### Step 4: Routing Audit (Sub-agents)

Spawn one or more routing-analyst sub-agents. Each sub-agent:
1. Reads `agents/routing-analyst.md` for its analysis rubric
2. Reads a **filtered** skill manifest (only skills visible to that batch)
3. Reads a batch of transcripts
4. Writes analysis to a batch JSON file

**IMPORTANT — Project-aware batching**: Projects with local skills must be
batched separately. Projects with only global skills can be pooled together
(they see the same skill set). When many projects have unique local skills,
batches are capped at `MAX_BATCHES` (default 12). Excess groups are merged
by greedy similarity — the group with the fewest extra skills is merged into
the most similar existing batch. This adds a few extra skills to
`visible_skill_names` but keeps sub-agent count bounded.

```python
import json, math
from collections import defaultdict

data = json.load(open("<workspace>/transcripts.json"))
manifest = json.load(open("<workspace>/skill-manifest.json"))
sessions = data["sessions"]

# Identify global skills and project-local skills
global_skills = [s for s in manifest["skills"] if s["scope"] == "global"]
global_names = [s["name"] for s in global_skills]
project_local = defaultdict(list)  # project_path -> [skill dicts]
for s in manifest["skills"]:
    if s["scope"] == "project-local" and s.get("project_path"):
        project_local[s["project_path"]].append(s)

# Helper: does this encoded project_dir match a project_path with locals?
def find_local_skills(project_dir):
    for pp, skills in project_local.items():
        encoded = pp.replace("/", "-").replace(".", "-")
        if encoded.lstrip("-") in project_dir.lstrip("-"):
            return skills
    return []

# Separate sessions: projects with local skills vs global-only
global_only_indices = []            # can be pooled
local_project_groups = defaultdict(list)  # project_dir -> indices

for i, s in enumerate(sessions):
    pdir = s.get("project_dir", "unknown")
    locals = find_local_skills(pdir)
    if locals:
        local_project_groups[pdir].append(i)
    else:
        global_only_indices.append(i)

# Build batches
batch_size = 60
MAX_BATCHES = 12  # Cap total sub-agents to keep cost/time bounded
batches = []

# 1) Pool all global-only sessions together
for chunk_start in range(0, len(global_only_indices), batch_size):
    chunk = global_only_indices[chunk_start:chunk_start + batch_size]
    batches.append({
        "session_indices": chunk,
        "label": "global-only (mixed projects)",
        "visible_skill_names": global_names,
    })

# 2) Group projects with same local skill set, then batch together
by_skill_set = defaultdict(list)  # tuple of local names -> indices
for pdir, indices in local_project_groups.items():
    local_names = tuple(sorted(s["name"] for s in find_local_skills(pdir)))
    by_skill_set[local_names].extend(indices)

local_batches = []
for local_names, indices in by_skill_set.items():
    visible = global_names + list(local_names)
    for chunk_start in range(0, len(indices), batch_size):
        chunk = indices[chunk_start:chunk_start + batch_size]
        local_batches.append({
            "session_indices": chunk,
            "label": f"local skills: {', '.join(local_names[:3])}{'...' if len(local_names) > 3 else ''}",
            "visible_skill_names": visible,
            "_local_set": set(local_names),
        })

# 3) Merge if too many batches — greedily merge smallest into most similar
remaining_budget = MAX_BATCHES - len(batches)
while len(local_batches) > remaining_budget and len(local_batches) > 1:
    # Find the smallest batch
    smallest_idx = min(range(len(local_batches)), key=lambda i: len(local_batches[i]["session_indices"]))
    smallest = local_batches.pop(smallest_idx)
    # Find the most similar batch (fewest extra skills added)
    best_idx, best_extra = 0, float("inf")
    for j, b in enumerate(local_batches):
        extra = len(smallest["_local_set"] - b["_local_set"]) + len(b["_local_set"] - smallest["_local_set"])
        if extra < best_extra:
            best_idx, best_extra = j, extra
    # Merge into best match
    target = local_batches[best_idx]
    target["session_indices"].extend(smallest["session_indices"])
    target["_local_set"] = target["_local_set"] | smallest["_local_set"]
    merged_local = sorted(target["_local_set"])
    target["visible_skill_names"] = global_names + merged_local
    target["label"] = f"merged local skills: {', '.join(merged_local[:3])}{'...' if len(merged_local) > 3 else ''}"

# Clean up internal field and add to batches
for b in local_batches:
    b.pop("_local_set", None)
    batches.append(b)

for i, b in enumerate(batches):
    print(f"Batch {i}: {len(b['session_indices'])} sessions, "
          f"{len(b['visible_skill_names'])} skills — {b['label']}")
```

Before spawning, build a DMI list per batch from the manifest:

```python
dmi_skills = {s["name"] for s in manifest["skills"] if s.get("disable_model_invocation")}
for b in batches:
    b["dmi_skill_names"] = sorted(set(b["visible_skill_names"]) & dmi_skills)
```

Spawn sub-agents in parallel — one per batch:

```
For each batch i:
  Agent tool (general-purpose):
    "Read agents/routing-analyst.md from the skill-auditor skill directory for
     your analysis instructions.
     Read <workspace>/skill-manifest.json for skill definitions.
     Read <workspace>/transcripts.json for session data.
     Only analyze sessions with these indices: [list from batch].
     Only evaluate against these skills: [visible_skill_names from batch].
     Ignore skills not in this list — they are not available in this
     project context.
     These skills have disable-model-invocation: true and NEVER auto-fire:
     [dmi_skill_names from batch]. Do NOT flag them as false_negative.
     Write your analysis as JSON to <workspace>/batch-audit-<i>.json
     following the exact schema in schemas/schemas.md (audit-report.json section)."
```

After all sub-agents complete, merge batch results:
- Union all `skill_reports` (combine incidents, recalculate stats per skill)
- Union all `competition_pairs` and `coverage_gaps`
- Recalculate `meta` totals (sum sessions_analyzed, turns_analyzed, etc.)

Write merged result to `<workspace>/audit-report.json`.

### Step 5: Portfolio Analysis (Sub-agent)

Spawn a portfolio-analyst sub-agent:

```
Agent tool (general-purpose):
  "Read agents/portfolio-analyst.md from the skill-auditor skill directory.
   Read <workspace>/skill-manifest.json for skill definitions and attention budget.
   Read <workspace>/audit-report.json for the routing audit results.
   Write your portfolio analysis as JSON to <workspace>/portfolio-analysis.json."
```

### Step 6: Improvement Plan (Sub-agent)

Spawn an improvement-planner sub-agent:

```
Agent tool (general-purpose):
  "Read agents/improvement-planner.md from the skill-auditor skill directory.
   Read <workspace>/audit-report.json for routing audit results.
   Read <workspace>/portfolio-analysis.json for portfolio analysis.
   Read <workspace>/skill-manifest.json for current skill definitions.
   IMPORTANT: Write ALL output text in [chosen language] — this includes
   fixes_issues, changes_made, cascade_risk, expected_impact, rationale,
   suggested_description, and every other human-readable string field.
   Write your improvement proposals as JSON to <workspace>/improvement-proposals.json.
   Also write individual patch files to <workspace>/patches/ directory."
```

### Step 7: Generate HTML Report

```bash
python3 scripts/generate_report.py \
  --workspace <workspace>
```

Output: `<workspace>/skill-audit-report.html`.
Open the report in the browser:

```bash
open <workspace>/skill-audit-report.html
```

### Step 8: Update Health History

Read `<base_dir>/health-history.json` (create if doesn't exist — start with
empty array `[]`). Append a new entry with the current run's summary:

```json
{
  "timestamp": "<ISO 8601>",
  "sessions_analyzed": <N>,
  "turns_analyzed": <N>,
  "portfolio_health": "<score>",
  "routing_accuracy_avg": <0.0-1.0>,
  "total_description_tokens": <N>,
  "competition_conflicts": <N>,
  "coverage_gaps": <N>,
  "skills_audited": <N>,
  "patches_proposed": <N>
}
```

If there's a previous entry, show the delta: "Accuracy changed from X to Y."

### Step 9: Apply Patches (User Approval)

Show the user a summary from the HTML report. For each patch, show the
before/after diff and cascade risk. Let the user approve or reject each.

For approved patches:

```bash
python3 scripts/apply_patches.py \
  --patches <workspace>/patches/ --confirm \
  --output <workspace>/changelog.md
```

### Step 10: Summary

Report what was done:
- How many sessions analyzed
- How many routing issues found
- Portfolio health score
- Patches proposed / approved / applied
- New skills suggested
- Link to the HTML report

## Analysis Capabilities

### Routing Accuracy
Per-skill fire count, accuracy, false positives/negatives, specific incidents
with root cause analysis. See `agents/routing-analyst.md` for the rubric.

### Attention Budget
Total description tokens across all skills. Per-skill token cost and efficiency
rating. Identifies bloated descriptions that waste attention budget.
See `agents/portfolio-analyst.md`.

### Competition Matrix
Classifies skill-pair relationships: orthogonal / adjacent / overlapping / nested.
Based on real transcript evidence, not just keyword overlap.

### Portfolio-Aware Optimization
Patches consider the full skill set. Cascade checking is mandatory — each patch
states what it fixes, what it might break, and the token budget impact.
See `agents/improvement-planner.md`.

## Error Taxonomy

| Verdict | Description |
|---------|-------------|
| correct | Right skill loaded for the intent |
| false_negative | Skill should have loaded but didn't. High bar: task must be meaningfully worse without it |
| false_positive | Skill loaded but was irrelevant |
| confused | Wrong skill loaded instead of the correct one |
| no_skill_needed | No skill was needed for this turn (most common) |
| explicit_invocation | User explicitly called `/skill-name` — not a routing event, skip from accuracy calc |
| coverage_gap | User intent not covered by any existing skill |

**Note on `disable-model-invocation: true`**: Skills with this flag never
auto-fire by design. They are excluded from false_negative analysis and
listed separately in the report as "explicit-only" skills.

## Workspace Structure

```
<base_dir>/                          # e.g. ~/.claude/skill-report/
├── health-history.json              # shared across runs (append-only)
├── 2026-03-04T18-45-23/             # run 1
│   ├── transcripts.json
│   ├── skill-manifest.json
│   ├── batch-audit-*.json
│   ├── audit-report.json
│   ├── portfolio-analysis.json
│   ├── improvement-proposals.json
│   ├── patches/*.patch.json
│   ├── skill-audit-report.html
│   └── changelog.md
└── 2026-03-04T20-12-07/             # run 2
    └── ...
```

## Troubleshooting

- **"No project found"**: Run with `--cwd` pointing to the project root, or
  use `--list` to see available projects.
- **tiktoken not installed**: Token counts will use character-based approximation.
  Install with `pip install tiktoken` for accuracy.
- **Large project (100+ sessions)**: Sessions are batched automatically. Multiple
  sub-agents run in parallel.
- **Sub-agent produces invalid JSON**: Re-run the specific sub-agent step. The
  rubric in agents/ includes exact schema specifications.
