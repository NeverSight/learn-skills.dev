---
name: synthesize-learnings
description: >
  Convert raw plugin analysis results into actionable improvement recommendations for agent-scaffolders
  and agent-skill-open-specifications. Trigger with "synthesize learnings", "generate improvement
  recommendations", "what should we improve in our scaffolders", "update our meta-skills based on
  these findings", or after completing a plugin analysis.
allowed-tools: Bash, Read, Write
---
# Synthesize Learnings

Take raw analysis output from `analyze-plugin` and transform it into concrete, actionable improvements for our meta-skills ecosystem. This is the "close the loop" skill that turns observations into evolution.

## Improvement Targets

Learnings are mapped to three improvement targets:

### Target 1: `agent-scaffolders`
Improvements to the plugin/skill/hook/sub-agent scaffolding tools.

**What to look for:**
- New component types or patterns that `scaffold.py` should support
- Better default templates based on exemplary plugins
- New scaffolder skills needed (e.g., creating connectors, reference files)
- Improved acceptance criteria templates based on real-world examples

### Target 2: `agent-skill-open-specifications`
Improvements to ecosystem standards and authoritative source documentation.

**What to look for:**
- New best practices discovered from high-quality plugins
- Anti-patterns that should be documented as warnings
- Spec gaps where plugins do things the standards don't address
- New pattern categories to add to ecosystem knowledge

### Target 3: `agent-plugin-analyzer` (Self-Improvement)
Improvements to this analyzer plugin itself.

**What to look for:**
- New patterns discovered that should be added to `pattern-catalog.md`
- Analysis blind spots — things that should have been caught
- Framework gaps — phases that need refinement
- New anti-patterns to add to the detection checklist

### Target 4: Domain Plugins (e.g., `legacy system`)
Improvements to the primary domain plugins in this repository — especially the legacy Oracle Forms/DB analysis plugins.

**What to look for:**
- **Severity/classification frameworks** that could improve how legacy code issues are categorized (e.g., GREEN/YELLOW/RED deviation severity from legal contract-review)
- **Playbook-based review methodology** adaptable to legacy code review playbooks (standard migration positions, acceptable risk levels)
- **Confidence scoring** applicable to legacy code analysis certainty levels
- **Connector abstractions** (`~~category` patterns) for tool-agnostic Oracle analysis workflows
- **Progressive disclosure structures** for organizing deep Oracle Forms/DB reference knowledge
- **Decision tables** for legacy migration pathways (like chart selection guides but for migration strategies)
- **Checklist patterns** for legacy system audit completeness
- **Tiered execution strategies** for handling different legacy code complexity levels
- **Bootstrap/iteration modes** for incremental legacy system analysis
- **Output templates** (HTML artifacts, structured reports) for presenting legacy analysis results

## Synthesis Process

### Step 1: Gather Analysis Results
Collect all analysis reports from the current session or from referenced analysis artifacts.

### Step 2: Categorize Observations

Sort every observation into one of these categories:

| Category | Description | Maps To |
|----------|-------------|---------|
| **Structural Innovation** | Novel directory layouts, component organization | Scaffolders |
| **Content Pattern** | Reusable content structures (tables, frameworks, checklists) | Specs + Catalog + Domain |
| **Execution Pattern** | Workflow designs, phase structures, decision trees | Scaffolders + Specs + Domain |
| **Integration Pattern** | MCP tool usage, connector abstractions, cross-tool design | Specs + Domain |
| **Quality Pattern** | Testing, validation, compliance approaches | Scaffolders + Specs |
| **Meta Pattern** | Self-referential or recursive designs (skills that build skills) | Analyzer + Scaffolders |
| **Anti-Pattern** | Things to avoid, documented pitfalls | Specs |
| **Domain Applicability** | Patterns transferable to legacy code analysis workflows | Domain |
| **Novel Discovery** | Something entirely new not in existing catalogs | All targets |

### Step 3: Generate Recommendations

For EACH observation, produce a structured recommendation:

```markdown
### [Recommendation Title]

**Source**: [Plugin/skill where observed]
**Category**: [from table above]
**Target**: [which meta-skill to improve]
**Priority**: [high / medium / low]

**Observation**: [What was found]

**Current State**: [How our meta-skills handle this today, or "not addressed"]

**Proposed Improvement**: [Specific change to make]

**Example**: [Before/after or concrete illustration]
```

### Step 4: Prioritize

Rank recommendations by impact:

| Priority | Criteria |
|----------|----------|
| **High** | Universal pattern found across many plugins; would improve ALL generated plugins; addresses a gap in current standards |
| **Medium** | Common pattern found in several plugins; would improve most generated plugins; refines existing standards |
| **Low** | Niche pattern from specific domain; would improve specialized plugins; nice-to-have enhancement |

### Step 5: Update the Pattern Catalog

Append any newly discovered patterns to `references/pattern-catalog.md` in the `analyze-plugin` skill. This is the self-improvement loop — every analysis makes future analyses better.

Format new catalog entries as:
```markdown
### [Pattern Name]
- **Category**: [Structural / Content / Execution / Integration / Quality / Meta]
- **First Seen In**: [plugin name]
- **Description**: [2-3 sentences]
- **When to Use**: [trigger conditions]
- **Example**: [brief illustration]
```

### Step 6: Generate Summary Report

Produce a final synthesis report with:

1. **Executive Summary** — 3-5 bullet points of the highest-impact learnings
2. **Recommendations by Target** — Grouped by scaffolders / specs / analyzer
3. **Updated Pattern Count** — How many new patterns were added to the catalog
4. **Virtuous Cycle Status** — What percentage of the analysis framework was exercised and how it can be tightened

## Output

The synthesis report should be a standalone markdown document suitable for:
- Filing as a reference artifact
- Using as a briefing for planning sessions
- Driving specific PRs against the scaffolders and specs

**Iteration Directory Isolation**: Do NOT overwrite existing synthesis reports. Always output to a newly isolated directory (e.g. `synthesis-reports/run-1/`) so historical recommendations are preserved.
**Asynchronous Benchmark Metric Capture**: Log the `total_tokens` and `duration_ms` consumed during the synthesis back to `timing.json` to track the ROI cost of this meta-analysis.

Always close with a **Next Steps** section listing the 3 most impactful changes to make first.
