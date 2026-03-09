---
name: github-research
description: Explore and analyze GitHub repositories related to a research topic. Reads deep-research output, discovers repos from multiple sources, deeply analyzes code, and produces integration blueprints.
argument-hint: [deep-research-output-dir]
---

# GitHub Research Skill

## Trigger

Activate this skill when the user wants to:
- "Find repos for [topic]", "GitHub research on [topic]"
- "Analyze open-source code for [topic]"
- "Find implementations of [paper/technique]"
- "Which repos implement [algorithm]?"
- Uses `/github-research <deep-research-output-dir>` slash command

## Overview

This skill systematically discovers, evaluates, and deeply analyzes GitHub repositories related to a research topic. It reads **deep-research** output (paper database, phase reports, code references) and produces an actionable integration blueprint for reusing open-source code.

**Installation**: `~/.claude/skills/github-research/` — scripts, references, and this skill definition.
**Output**: `./github-research-output/{slug}/` relative to the current working directory.
**Input**: A deep-research output directory (containing `paper_db.jsonl`, phase reports, `code_repos.md`, etc.)

## 6-Phase Pipeline

```
Phase 1: Intake     → Extract refs, URLs, keywords from deep-research output
Phase 2: Discovery  → Multi-source broad GitHub search (50-200 repos)
Phase 3: Filtering  → Score & rank → select top 15-30 repos
Phase 4: Deep Dive  → Clone & deeply analyze top 8-15 repos (code reading)
Phase 5: Analysis   → Per-repo reports + cross-repo comparison
Phase 6: Blueprint  → Integration/reuse plan for research topic
```

## Output Directory Structure

```
github-research-output/{slug}/
├── repo_db.jsonl                     # Master repo database
├── phase1_intake/
│   ├── extracted_refs.jsonl          # URLs, keywords, paper-repo links
│   └── intake_summary.md
├── phase2_discovery/
│   ├── search_results/               # Raw JSONL from each search
│   └── discovery_log.md
├── phase3_filtering/
│   ├── ranked_repos.jsonl            # Scored & ranked subset
│   └── filtering_report.md
├── phase4_deep_dive/
│   ├── repos/                        # Cloned repos (shallow)
│   ├── analyses/                     # Per-repo analysis .md files
│   └── deep_dive_summary.md
├── phase5_analysis/
│   ├── comparison_matrix.md          # Cross-repo comparison
│   ├── technique_map.md              # Paper concept → code mapping
│   └── analysis_report.md
└── phase6_blueprint/
    ├── integration_plan.md           # How to combine repos
    ├── reuse_catalog.md              # Reusable components catalog
    ├── final_report.md               # Complete compiled report
    └── blueprint_summary.md
```

## Scripts Reference

All scripts are Python 3, stdlib-only, located in `~/.claude/skills/github-research/scripts/`.

| Script | Purpose | Key Flags |
|--------|---------|-----------|
| `extract_research_refs.py` | Parse deep-research output for GitHub URLs, paper refs, keywords | `--research-dir`, `--output` |
| `search_github.py` | Search GitHub repos via `gh api` | `--query`, `--language`, `--min-stars`, `--sort`, `--max-results`, `--topic`, `--output` |
| `search_github_code.py` | Search GitHub code for implementations | `--query`, `--language`, `--filename`, `--max-results`, `--output` |
| `search_paperswithcode.py` | Search Papers With Code for paper→repo mappings | `--paper-title`, `--arxiv-id`, `--query`, `--output` |
| `repo_db.py` | JSONL repo database management | subcommands: `merge`, `filter`, `score`, `search`, `tag`, `stats`, `export`, `rank` |
| `repo_metadata.py` | Fetch detailed metadata via `gh api` | `--repos`, `--input`, `--output`, `--delay` |
| `clone_repo.py` | Shallow-clone repos for analysis | `--repo`, `--output-dir`, `--depth`, `--branch` |
| `analyze_repo_structure.py` | Map file tree, key files, LOC stats | `--repo-dir`, `--output` |
| `extract_dependencies.py` | Extract and parse dependency files | `--repo-dir`, `--output` |
| `find_implementations.py` | Search cloned repo for specific code patterns | `--repo-dir`, `--patterns`, `--output` |
| `repo_readme_fetch.py` | Fetch README without cloning | `--repos`, `--input`, `--output`, `--max-chars` |
| `compare_repos.py` | Generate comparison matrix across repos | `--input`, `--output` |
| `compile_github_report.py` | Assemble final report from all phases | `--topic-dir` |

---

## Phase 1: Intake

**Goal**: Extract all relevant references, URLs, and keywords from the deep-research output.

### Steps

1. **Create output directory structure**:
   ```bash
   SLUG=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
   mkdir -p github-research-output/$SLUG/{phase1_intake,phase2_discovery/search_results,phase3_filtering,phase4_deep_dive/{repos,analyses},phase5_analysis,phase6_blueprint}
   ```

2. **Extract references from deep-research output**:
   ```bash
   python ~/.claude/skills/github-research/scripts/extract_research_refs.py \
     --research-dir <deep-research-output-dir> \
     --output github-research-output/$SLUG/phase1_intake/extracted_refs.jsonl
   ```

3. **Review extracted refs**: Read the generated JSONL. Note:
   - GitHub URLs found directly in reports
   - Paper titles and arxiv IDs (for Papers With Code lookup)
   - Research keywords and themes (for GitHub search queries)

4. **Write intake summary**: Create `phase1_intake/intake_summary.md` with:
   - Number of direct GitHub URLs found
   - Number of papers with potential code links
   - Key research themes extracted
   - Planned search queries for Phase 2

### Checkpoint
- `extracted_refs.jsonl` exists with entries
- `intake_summary.md` written
- Search strategy documented

---

## Phase 2: Discovery

**Goal**: Cast a wide net to find 50-200 candidate repos from multiple sources.

### Steps

1. **Search by direct URLs**: Any GitHub URLs from Phase 1 → fetch metadata:
   ```bash
   python ~/.claude/skills/github-research/scripts/repo_metadata.py \
     --repos owner1/name1 owner2/name2 ... \
     --output github-research-output/$SLUG/phase2_discovery/search_results/direct_urls.jsonl
   ```

2. **Search Papers With Code**: For each paper with an arxiv ID:
   ```bash
   python ~/.claude/skills/github-research/scripts/search_paperswithcode.py \
     --arxiv-id 2401.12345 \
     --output github-research-output/$SLUG/phase2_discovery/search_results/pwc_2401.12345.jsonl
   ```

3. **Search GitHub by keywords** (3-8 queries based on research themes):
   ```bash
   python ~/.claude/skills/github-research/scripts/search_github.py \
     --query "multi-agent LLM coordination" \
     --min-stars 10 --sort stars --max-results 50 \
     --output github-research-output/$SLUG/phase2_discovery/search_results/gh_query1.jsonl
   ```

4. **Search GitHub code** (for specific implementations):
   ```bash
   python ~/.claude/skills/github-research/scripts/search_github_code.py \
     --query "class MultiAgentOrchestrator" \
     --language python --max-results 30 \
     --output github-research-output/$SLUG/phase2_discovery/search_results/code_query1.jsonl
   ```

5. **Fetch READMEs** for repos that lack descriptions:
   ```bash
   python ~/.claude/skills/github-research/scripts/repo_readme_fetch.py \
     --input <repos.jsonl> \
     --output github-research-output/$SLUG/phase2_discovery/search_results/readmes.jsonl
   ```

6. **Merge all results** into master database:
   ```bash
   python ~/.claude/skills/github-research/scripts/repo_db.py merge \
     --inputs github-research-output/$SLUG/phase2_discovery/search_results/*.jsonl \
     --output github-research-output/$SLUG/repo_db.jsonl
   ```

7. **Write discovery log**: Create `phase2_discovery/discovery_log.md` with search queries used, results per source, total unique repos found.

### Rate Limits
- GitHub search API: 30 requests/minute (authenticated)
- Papers With Code API: No strict limit but be respectful (1 req/sec)
- Add `--delay 1.0` to batch operations when needed

### Checkpoint
- `repo_db.jsonl` populated with 50-200 repos
- `discovery_log.md` with search details

---

## Phase 3: Filtering

**Goal**: Score and rank repos, select top 15-30 for deeper analysis.

### Steps

1. **Enrich metadata** for all repos:
   ```bash
   python ~/.claude/skills/github-research/scripts/repo_metadata.py \
     --input github-research-output/$SLUG/repo_db.jsonl \
     --output github-research-output/$SLUG/repo_db.jsonl \
     --delay 0.5
   ```

2. **Score repos** (quality + activity scores):
   ```bash
   python ~/.claude/skills/github-research/scripts/repo_db.py score \
     --input github-research-output/$SLUG/repo_db.jsonl \
     --output github-research-output/$SLUG/repo_db.jsonl
   ```

3. **LLM relevance scoring**: Read through the top ~50 repos (by quality_score) and assign `relevance_score` (0.0-1.0) based on:
   - Direct relevance to research topic
   - Implementation completeness
   - Code quality signals (from README, description)
   - Update the relevance scores:
   ```bash
   python ~/.claude/skills/github-research/scripts/repo_db.py tag \
     --input github-research-output/$SLUG/repo_db.jsonl \
     --ids owner/name --tags "relevance:0.85"
   ```

4. **Compute composite scores and rank**:
   ```bash
   python ~/.claude/skills/github-research/scripts/repo_db.py score \
     --input github-research-output/$SLUG/repo_db.jsonl \
     --output github-research-output/$SLUG/repo_db.jsonl
   python ~/.claude/skills/github-research/scripts/repo_db.py rank \
     --input github-research-output/$SLUG/repo_db.jsonl \
     --output github-research-output/$SLUG/phase3_filtering/ranked_repos.jsonl \
     --by composite_score
   ```

5. **Select top repos**: Filter to top 15-30:
   ```bash
   python ~/.claude/skills/github-research/scripts/repo_db.py filter \
     --input github-research-output/$SLUG/phase3_filtering/ranked_repos.jsonl \
     --output github-research-output/$SLUG/phase3_filtering/ranked_repos.jsonl \
     --max-repos 30 --not-archived
   ```

6. **Write filtering report**: Create `phase3_filtering/filtering_report.md`:
   - Stats before/after filtering
   - Score distributions
   - Top 30 repos with scores and rationale

### Scoring Formula
```
activity_score = sigmoid((days_since_push < 90) * 0.4 + has_recent_commits * 0.3 + open_issues_ratio * 0.3)
quality_score  = normalize(log(stars+1) * 0.3 + log(forks+1) * 0.2 + has_license * 0.15 + has_readme * 0.15 + not_archived * 0.2)
composite_score = relevance * 0.4 + quality * 0.35 + activity * 0.25
```

### Checkpoint
- `ranked_repos.jsonl` with 15-30 repos
- `filtering_report.md` with scoring details

---

## Phase 4: Deep Dive

**Goal**: Clone and deeply analyze the top 8-15 repos.

### Steps

1. **Select repos for deep dive**: Take top 8-15 from ranked list.

2. **Clone each repo** (shallow):
   ```bash
   python ~/.claude/skills/github-research/scripts/clone_repo.py \
     --repo owner/name \
     --output-dir github-research-output/$SLUG/phase4_deep_dive/repos/
   ```

3. **Analyze structure** for each cloned repo:
   ```bash
   python ~/.claude/skills/github-research/scripts/analyze_repo_structure.py \
     --repo-dir github-research-output/$SLUG/phase4_deep_dive/repos/name/ \
     --output github-research-output/$SLUG/phase4_deep_dive/analyses/name_structure.json
   ```

4. **Extract dependencies**:
   ```bash
   python ~/.claude/skills/github-research/scripts/extract_dependencies.py \
     --repo-dir github-research-output/$SLUG/phase4_deep_dive/repos/name/ \
     --output github-research-output/$SLUG/phase4_deep_dive/analyses/name_deps.json
   ```

5. **Find implementations**: Search for key algorithms/concepts from research:
   ```bash
   python ~/.claude/skills/github-research/scripts/find_implementations.py \
     --repo-dir github-research-output/$SLUG/phase4_deep_dive/repos/name/ \
     --patterns "class Transformer" "def forward" "attention" \
     --output github-research-output/$SLUG/phase4_deep_dive/analyses/name_impls.jsonl
   ```

6. **Deep code reading**: For each repo, READ the key source files identified by structure analysis. Write a per-repo analysis in `phase4_deep_dive/analyses/{name}_analysis.md`:
   - Architecture overview
   - Key algorithms implemented
   - Code quality assessment
   - API / interface design
   - Dependencies and requirements
   - Strengths and limitations
   - Reusability assessment (how easy to extract components)

7. **Write deep dive summary**: `phase4_deep_dive/deep_dive_summary.md`

### IMPORTANT: Actually Read Code
Do NOT just summarize READMEs. You must:
- Read the main source files (entry points, core modules)
- Understand the actual implementation approach
- Identify specific functions/classes that implement research concepts
- Note code patterns, design decisions, and trade-offs

### Checkpoint
- Repos cloned in `repos/`
- Per-repo analysis files in `analyses/`
- `deep_dive_summary.md` written

---

## Phase 5: Analysis

**Goal**: Cross-repo comparison and technique-to-code mapping.

### Steps

1. **Generate comparison matrix**:
   ```bash
   python ~/.claude/skills/github-research/scripts/compare_repos.py \
     --input github-research-output/$SLUG/phase4_deep_dive/analyses/ \
     --output github-research-output/$SLUG/phase5_analysis/comparison.json
   ```

2. **Write comparison matrix**: Create `phase5_analysis/comparison_matrix.md`:
   - Table comparing repos across dimensions (language, LOC, stars, framework, license, tests)
   - Dependency overlap analysis
   - Strengths/weaknesses per repo

3. **Write technique map**: Create `phase5_analysis/technique_map.md`:
   - Map each paper concept / research technique → specific repo + file + function
   - Identify gaps (techniques with no implementation found)
   - Note alternative implementations of the same concept

4. **Write analysis report**: `phase5_analysis/analysis_report.md`:
   - Executive summary of findings
   - Key insights from code analysis
   - Recommendations for which repos to use for which purposes

### Checkpoint
- `comparison_matrix.md` with repo comparison table
- `technique_map.md` mapping concepts to code
- `analysis_report.md` with findings

---

## Phase 6: Blueprint

**Goal**: Produce an actionable integration and reuse plan.

### Steps

1. **Write integration plan**: `phase6_blueprint/integration_plan.md`:
   - Recommended architecture for combining repos
   - Step-by-step integration approach
   - Dependency resolution strategy
   - Potential conflicts and how to resolve them

2. **Write reuse catalog**: `phase6_blueprint/reuse_catalog.md`:
   - For each reusable component: source repo, file path, function/class, what it does, how to extract it
   - License compatibility matrix
   - Effort estimates (easy/medium/hard to integrate)

3. **Compile final report**:
   ```bash
   python ~/.claude/skills/github-research/scripts/compile_github_report.py \
     --topic-dir github-research-output/$SLUG/
   ```

4. **Write blueprint summary**: `phase6_blueprint/blueprint_summary.md`:
   - One-page executive summary
   - Top 5 repos and why
   - Recommended next steps

### Checkpoint
- `integration_plan.md` complete
- `reuse_catalog.md` with component catalog
- `final_report.md` compiled
- `blueprint_summary.md` as executive summary

---

## Quality Conventions

1. **Repos are ranked by composite score**: `relevance × 0.4 + quality × 0.35 + activity × 0.25`
2. **Deep dive requires reading actual code**, not just READMEs
3. **Integration blueprint must map paper concepts → specific code files/functions**
4. **Incremental saves**: Each phase writes to disk immediately
5. **Checkpoint recovery**: Can resume from any phase by checking what outputs exist
6. **All scripts are stdlib-only Python** — no pip installs needed
7. **`gh` CLI is required** for GitHub API access (must be authenticated)
8. **Deduplication** by `repo_id` (owner/name) across all searches
9. **Rate limit awareness**: Respect GitHub search API limits (30 req/min)

## Error Handling

- If `gh` is not installed: warn user and provide installation instructions
- If a repo is archived/deleted: skip gracefully, note in log
- If clone fails: skip, note in log, continue with remaining repos
- If Papers With Code API is down: skip, rely on GitHub search only
- Always write partial progress to disk so work is not lost

## References

- See `references/phase-guide.md` for detailed phase execution guidance
- Deep-research skill: `~/.claude/skills/deep-research/SKILL.md`
- Paper database pattern: `~/.claude/skills/deep-research/scripts/paper_db.py`
