---
name: analyze-plugin
description: >
  Systematically analyze agent plugins and skills to extract design patterns, architectural decisions,
  and reusable techniques. Trigger with "analyze this plugin", "mine patterns from", "review plugin
  structure", "extract learnings from", "what patterns does this plugin use", or when examining any
  plugin or skill collection to understand its design.
allowed-tools: Bash, Read, Write
---
# Plugin & Skill Analyzer

Perform deep structural and content analysis on agent plugins and skills. Extract reusable patterns that feed the virtuous cycle of continuous improvement.

## Two Analysis Modes

### Single Plugin Mode
Deep-dive into one plugin. Use when you want to fully understand a plugin's architecture.

### Comparative Mode
Analyze multiple plugins side-by-side. Use when looking for common patterns across a collection.

## Analysis Framework

Execute these six phases sequentially. Do not skip phases.

### Phase 1: Inventory

Run the deterministic inventory script first:
```bash
python3 "./scripts/inventory_plugin.py" --path <plugin-dir> --format json
```

If the script is unavailable, manually enumerate:
1. Walk the directory tree
2. Classify every file by type:
   - `SKILL.md` → Skill definition
   - `commands/*.md` → Command definition
   - `references/*.md` → Reference material (progressive disclosure)
   - `scripts/*.py` → Executable scripts
   - `README.md` → Plugin documentation
   - `CONNECTORS.md` → Connector abstractions
   - `plugin.json` → Plugin manifest
   - `*.json` → Configuration (MCP, hooks, etc.)
   - `*.yaml` / `*.yml` → Pipeline/config data
   - `*.html` → Artifact templates
   - `*.mmd` → Architecture diagrams
   - Other → Assets/misc

3. Record for each file: path, type, line count, byte size
4. Output a structured inventory as a markdown checklist with one checkbox per file

### Phase 2: Structure Analysis

Evaluate the plugin's architectural decisions:

| Dimension | What to Look For |
|-----------|-----------------|
| **Layout** | How are skills/commands/references organized? Flat vs nested? |
| **Progressive Disclosure** | Is SKILL.md lean (<500 lines) with depth in `references/`? |
| **Component Ratios** | Skills vs commands vs scripts — what's the balance? |
| **Naming Patterns** | Are names descriptive? Follow kebab-case? Use gerund form? |
| **README Quality** | Does it have a file tree? Usage examples? Architecture diagram? |
| **CONNECTORS.md** | Does it use `~~category` connector abstraction for tool-agnosticism? |
| **Standalone vs Supercharged** | Can it work without MCP tools? What's enhanced with them? |

### Phase 3: Content Analysis

For each file, load the appropriate question set from `references/analysis-questions-by-type.md` and work through every checkbox. See the process diagram in `analyze-plugin-flow.mmd` for the full pipeline visualization.

For each SKILL.md, evaluate:

**Frontmatter Quality:**
- Is the `description` written in third person?
- Does it include specific trigger phrases?
- Is it under 1024 characters?
- Does it clearly state WHEN to trigger?

**Body Structure:**
- Does it have a clear execution flow (numbered phases/steps)?
- Are there decision trees or branching logic?
- Does it use tables for structured information?
- Are there output templates or format specifications?
- Does it link to `references/` for deep content?

**Interaction Design:**
- Does it use guided discovery interviews before execution?
- What question types are used? (open-ended, numbered options, yes/no, table-based comparisons)
- Does it present smart defaults with override options?
- Are there confirmation gates before expensive/irreversible operations?
- Does it use recap-before-execute to verify understanding?
- Does it offer numbered next-action menus after completion?
- Does it negotiate output format with the user?
- Are there inline progress indicators during multi-step workflows?

**For Commands**, evaluate:
- Are they written as instructions FOR the agent (not documentation for users)?
- Do they specify required arguments?
- Do they reference MCP tools with full namespaces?

**For Reference Files**, evaluate:
- Do they contain domain-specific deep knowledge?
- Are they organized by topic/domain?
- Do files >100 lines have a table of contents?

**For Scripts**, evaluate:
- Are they Python-only (no .sh/.ps1)?
- Do they have `--help` documentation?
- Do they handle errors gracefully?
- Are they cross-platform compatible?

### Phase 4: Pattern Extraction

Identify instances of known patterns from `references/pattern-catalog.md`. Also watch for novel patterns not yet cataloged.

**For each pattern found, document:**
```
Pattern: [name]
Plugin: [where found]
File: [specific file]
Description: [how it's used here]
Quality: [exemplary / good / basic]
Reusability: [high / medium / low]
Confidence: [high (≥3 plugins) / medium (2) / low (1)]
Lifecycle: [proposed / validated / canonical / deprecated]
```

**Before adding a new pattern**, check the catalog's deduplication rules. If an existing pattern covers ≥80% of the behavior, update its frequency instead.

**Key pattern categories to search for:**
1. **Architectural Patterns** — Standalone/supercharged, connector abstraction, meta-skills
2. **Execution Patterns** — Phase-based workflows, decision trees, bootstrap/iteration modes
3. **Content Patterns** — Severity frameworks, confidence scoring, priority tiers, checklists
4. **Output Patterns** — HTML artifacts, structured tables, ASCII diagrams, template systems
5. **Knowledge Patterns** — Progressive disclosure, dialect tables, domain references, tribal knowledge extraction
6. **Interaction Design Patterns** — Discovery interviews, option menus, confirmation gates, smart defaults, recap-before-execute, output format negotiation, progress indicators

### Phase 5: Anti-Pattern & Security Detection

Load the full check tables from `references/security-checks.md`.

**Execution order:**
1. Run security checks FIRST (P0 — Critical severity items)
2. Then run structural anti-pattern checks
3. Apply contextual severity based on plugin type/complexity
4. Flag any LLM-native attack vectors (skill impersonation, context poisoning, injection via references)

If `inventory_plugin.py` was run with `--security`, use its deterministic findings as ground truth.

### Phase 6: Synthesis & Scoring

Load the maturity model and scoring rubric from `references/maturity-model.md`.

**Steps:**
1. Assign maturity level (L1-L5)
2. Score each of the 6 dimensions (1-5) using the weighted rubric
3. Calculate overall score (weighted average, Scoring v2.0)
4. Generate the summary report using the template
5. For comparative mode, generate the Ecosystem Scorecard

## Output

Generate a structured markdown report. For single plugins, output inline. For collections, create an artifact file with the full analysis.

**Iteration Directory Isolation**: All analysis reports must be saved into explicitly versioned and isolated outputs (e.g. `analysis-reports/target-run-1/`) to prevent destructive overrides on re-runs.
**Asynchronous Benchmark Metric Capture**: Once the audit run completes, immediately log the resulting `total_tokens` and `duration_ms` to a `timing.json` file to calculate the cost of the deep-dive analysis.

Always end with **Virtuous Cycle Recommendations**: specific, actionable improvements for `agent-plugin-analyzer` (this plugin), `agent-scaffolders`, and `agent-skill-open-specifications` based on patterns discovered.
