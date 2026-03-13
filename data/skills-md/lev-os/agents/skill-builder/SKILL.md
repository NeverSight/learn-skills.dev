---
name: skill-builder
description: "Router for skill creation: routes doc/repo-to-skill codification or routes to skill-creator for authoring. Use for doc-to-skill, new skills, or merging skills."
skill_type: workflow
category: process-skill-builder
---

# Lev Skill Builder

## Overview

Unified skill creation hub. Routes between documentation codification (Skill_Seekers v2.7.4) and new skill authoring (skill-creator standards). Supports website scraping, GitHub repository analysis (with AST parsing), PDF extraction, and unified multi-source with conflict detection.

## When to Use This Skill

Use skill-builder when you need to:

| Scenario                      | Example                              | Route                       |
| ----------------------------- | ------------------------------------ | --------------------------- |
| Convert docs website to skill | "Codify the FastAPI docs"            | Codifier pipeline (see below) |
| Convert GitHub repo to skill  | "Make a skill from facebook/react"   | Codifier pipeline (see below) |
| Extract PDF into skill        | "Turn this manual into a skill"      | Codifier pipeline (see below) |
| Combine multiple sources      | "Skill from React docs + repo + PDF" | Codifier pipeline (see below) |
| Author new skill from scratch | "Create a skill for my workflow"     | skill-creator               |
| Merge existing skills         | "Combine these 3 skills into one"    | Both routes                 |
| Export for non-Claude LLMs    | "Package for Gemini/ChatGPT"         | Codifier with `--target`    |

**Do NOT use** for: editing existing skills (use editor), searching skills (use `lev get`), or installing skills (use clawdhub).

## Quick Decision Tree

```
What does the user want?
│
├─→ Convert existing docs to skill?
│   ├─→ Website only? → Website Scraping
│   ├─→ GitHub repo only? → GitHub Analysis
│   ├─→ PDF only? → PDF Extraction
│   └─→ Multiple sources? → Unified Multi-Source
│
├─→ Create NEW skill from scratch?
│   └─→ Route to skill-creator
│       - SKILL.md format: YAML frontmatter + markdown body
│       - Progressive disclosure: metadata → body → references
│       - Body <500 lines, description is PRIMARY trigger
│       - See skill-creator skill for full standards
│
├─→ Combine/merge existing skills?
│   └─→ Route to BOTH:
│       1. Analyze existing skills (codifier patterns)
│       2. Author merged skill (skill-creator standards)
│       3. Ensure router pattern if subsumes others
│
├─→ Export for non-Claude platform?
│   └─→ Package with --target (gemini|openai|markdown)
│
└─→ First time? → references/setup.md
```

## Skill Installation from External Sources

When intake routes a skills.sh URL or skill:// to skill-builder:

### Step 1: Acquire → skills-db staging
```bash
# Extract GitHub repo URL from skills.sh page (WebFetch for the link ONLY)
git clone --depth 1 {repo} /tmp/skill-intake-{ts}/
# Find the skill: find /tmp/skill-intake-{ts}/ -name "SKILL.md" -path "*{name}*"
# Stage to skills-db (NOT directly to active):
cp -r /tmp/skill-intake-{ts}/skills/{name}/ ~/.agents/skills-db/_workshop/{source}/{name}/
rm -rf /tmp/skill-intake-{ts}/
```

### Step 2: Validate (HARD GATES — run on staged copy)
```bash
file=~/.agents/skills-db/_workshop/{source}/{name}/SKILL.md
head -1 "$file" | grep -q "^---$"           # Has YAML frontmatter
grep -q "^name:" "$file"                     # Has name field
grep -q "^description:" "$file"              # Has description field
awk '/^---$/{c++} c==2{exit}' "$file"        # Has closing ---
```
If any hard gate fails → REJECT. Move to `.archive/` or delete. Do NOT promote.

### Step 3: Prior Art Check
- Search ~/.agents/skills/ for name/trigger overlap
- Exact match → compare quality (line count, scoring), keep better version
- Partial overlap (>30% triggers) → recommend merge
- No overlap → proceed to scoring

### Step 4: Quality Score (run on staged copy, BEFORE promotion)
Score 1-10 on 5 dimensions (read the SKILL.md content):

| Dimension | What to evaluate |
|-----------|-----------------|
| Actionability | Concrete steps/code/templates vs vague advice |
| Depth | Expert-level detail vs surface overview |
| Structure | Decision trees/tables vs wall of text |
| Trigger quality | WHAT/HOW/WHEN/WHY + tags vs bare description |
| Uniqueness | Novel frameworks vs generic blog advice |

Grades: A (8+) promote, B (7-7.9) promote with note, C (5-6.9) hold in _todo, D (<5) reject

### Step 5: Catalog (move from staging to skills-db home)
```bash
# A/B grade → catalog in skills-db (DEFAULT destination):
mv ~/.agents/skills-db/_workshop/{source}/{name}/ ~/.agents/skills-db/{domain}/{name}/
# C grade → move to _todo for enhancement:
mv ~/.agents/skills-db/_workshop/{source}/{name}/ ~/.agents/skills-db/_todo/{name}/
# D grade → reject:
mv ~/.agents/skills-db/_workshop/{source}/{name}/ ~/.agents/skills-db/.archive/{name}/
```

### Step 5b: Activate (ONLY if user requests)
```bash
# Only when user explicitly wants the skill loaded into Claude Code:
cp -r ~/.agents/skills-db/{domain}/{name}/ ~/.agents/skills/{name}/
# Or symlink:
ln -s ~/.agents/skills-db/{domain}/{name}/ ~/.agents/skills/{name}
```
**NOTE**: Most skills stay in skills-db. Only day-to-day/global operational skills get activated.
The user decides when to activate — skill-builder should PROPOSE activation, not assume it.

### Step 6: Lifecycle Check
- Is this skill a candidate for merging into an existing hub/router?
- Does it overlap with 2+ existing skills in the same domain?
- If yes → recommend leaf→hub→router graduation

## Skill Lifecycle: Leaf → Hub → Router

Skills grow organically through 3 stages:

| Stage | Lines | Pattern | Example |
|-------|-------|---------|---------|
| LEAF | <300L | Standalone, no routing | writing-substack (147L) |
| HUB | 300-500L | Cross-references peers | content-strategy (356L) |
| ROUTER | 80-100L body | Dispatches to sub-skills | security-hub (80L → 4 sub-skills) |

### Growth triggers
- **Merge**: 2+ skills share >30% intent overlap → merge into hub
- **Router**: Merged hub exceeds ~400L → graduate to router (move content to sub-skills)
- **Split**: Single skill >500L without references/ → split into skill + references/

### Router graduation checklist
1. Create {domain}-hub/ directory
2. Write SKILL.md routing header (<100L): decision tree + sub-skill table
3. Add `skill_type: router` and `subsumes: [list]` to frontmatter
4. Keep sub-skills as independent SKILL.md files
5. Router description MUST include ALL sub-skill triggers (union of tags)

## Full Pipeline (The Correct Order)

Every codification job follows this pipeline. Do NOT skip steps.

```
1. PRIOR ART CHECK → Does this skill already exist?
   ├─ lev get "{name}" --scope=knowledge --pattern="SKILL.md"
   ├─ grep -rl "{name}" ~/.claude/skills/
   └─ If found:
      • Exact match → use as-is or enhance existing, skip to step 4
      • Partial overlap → recommend merge/consolidation with existing
      • Related but different → proceed, note in description for routing

2. ESTIMATE (websites only) → How big is this job?
   └─ skill-seekers estimate configs/{name}.json
      • < 5K pages: single skill, proceed normally
      • 5K-10K: consider category split
      • 10K+: must split with router strategy

3. EXTRACT → Get the raw content
   ├─ Website:  skill-seekers scrape --name {name} --url {url}
   ├─ GitHub:   skill-seekers github --repo {owner/repo}
   ├─ PDF:      skill-seekers pdf --pdf {file} --name {name}
   └─ Unified:  skill-seekers unified --config {config.json}

4. ENHANCE → Transform raw extraction into a real skill
   └─ skill-seekers enhance output/{name}/

   ⚠️ KNOWN BUG (skill-seekers ≤2.7.4): enhance passes file path
   as positional arg to claude CLI. SKILL.md never gets updated.
   USE WORKAROUND: scripts/enhance-workaround.sh output/{name}

5. REVIEW → Check the enhanced output
   • Compare frontmatter against standards (what/how/when/why + triggers)
   • Verify description is the PRIMARY trigger mechanism
   • Check progressive disclosure (SKILL.md <500 lines, rest in references/)
   • Validate: no stats-only wrappers, real actionable content

6. PACKAGE → Bundle for distribution
   └─ echo "y" | skill-seekers package output/{name}/ [--target claude|gemini|openai|markdown]

7. INSTALL → Put it where it belongs
   ├─ Global:  cp -r output/{name} ~/.claude/skills/{name}/
   ├─ Project: cp -r output/{name} .claude/skills/{name}/
   └─ Upload:  output/{name}.zip → https://claude.ai/skills
```

## Quick Reference: Essential Commands

### 1. Installation Check

```bash
command -v skill-seekers || python3 -m skill_seekers --version
```

If not installed, see `references/setup.md` for uv/venv/pip auto-detection.

### 2. Website Scraping (Preset)

```bash
skill-seekers scrape --config configs/react.json --enhance-local
skill-seekers package output/react/
```

### 3. Website Scraping (Custom)

```bash
skill-seekers scrape --name myframework --url https://docs.example.com/
skill-seekers package output/myframework/
```

### 4. GitHub Repository Analysis

```bash
skill-seekers github --repo facebook/react
skill-seekers package output/react/
```

Supports deep AST parsing for Python, JavaScript, TypeScript, Java, C++, Go. Extracts APIs, issues, PRs, changelogs, and detects doc-vs-code conflicts.

### 5. PDF Extraction

```bash
skill-seekers pdf --pdf docs/manual.pdf --name myskill
skill-seekers package output/myskill/
```

Supports OCR for scanned PDFs, table extraction, password-protected files, and parallel processing.

### 6. Unified Multi-Source (Docs + GitHub + PDF)

```bash
skill-seekers unified --config configs/react_unified.json
skill-seekers package output/react/
```

Combines all sources with automatic conflict detection and intelligent merging.

### 7. Multi-Platform Export

```bash
# Claude (default)
skill-seekers package output/react/

# Google Gemini
skill-seekers package output/react/ --target gemini

# OpenAI ChatGPT
skill-seekers package output/react/ --target openai

# Generic Markdown (any LLM)
skill-seekers package output/react/ --target markdown
```

For large docs (10K+ pages), async mode, three-stream GitHub analysis, splitting strategies, and troubleshooting, see `references/advanced-commands.md`.

## Frontmatter Design Philosophy

### The Description is Everything

The `description` field is the **PRIMARY trigger mechanism**. Agents read descriptions to route. Body loads AFTER triggering.

Every description needs What/How/When/Why + tag soup:

```yaml
description: |
  [WHAT] - What this skill does (1 sentence)
  [HOW] - How it works (mechanism, tools used)
  [WHEN] - When to use it (trigger conditions)
  [WHY] - Why it exists (problem it solves)

  Triggers: "tag1", "tag2", "tag3", ...
```

### Intentional Tag Overlap

Skills SHOULD have overlapping triggers for semantic routing:

| Domain            | Shared Triggers             | Skills                             |
| ----------------- | --------------------------- | ---------------------------------- |
| Context gathering | find, search, lookup, get   | lev get, lev-research, lev-memory |
| Modification      | update, patch, change, edit | lev-patch, bd, edit tools          |
| Execution         | run, execute, do, make      | ralph, bash, Task tool             |

**Anti-pattern:** Descriptions that only say WHAT without WHEN triggers:

```yaml
# BAD
description: Manages memory storage and retrieval.

# GOOD
description: |
  Store and recall information across sessions using AutoMem.
  Triggers: "remember", "recall", "forget", "save this", "memory"
```

### The 3-Tool Agent Model

Skills wrap 3 fundamental operations:

1. **GET** (context gathering) - lev get, lev-research, read
2. **EXECUTE** (run things) - ralph, bash, Task tool, skills
3. **PATCH** (modify the graph) - bd, edit, write, memory_store

Categorize your skill's operations to help semantic routing.

## Skill Creator Standards (Quick Reference)

When authoring a new skill from scratch:

**Structure:**

```
skill-name/
├── SKILL.md (required, <500 lines)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown body
└── references/ (optional, loaded on demand)
```

**Progressive Disclosure Tiers:**

1. Metadata (~100 words) - Always loaded
2. Body (<5k words) - On trigger
3. References (unlimited) - On demand

**Rules:**

- `description` is the PRIMARY trigger - include what + when
- Use imperative/infinitive form
- No separate README.md or CHANGELOG.md - the skill IS the docs

## Validation (Post-Extraction)

```
VALIDATION RULES:
1. SKILL.md > 150 lines? → Move detail to references/
2. No references/ + heavy SKILL.md? → Create references/, split
3. Any file > 500 lines? → Consider chunking
4. Total skill > 2000 lines? → Consider sub-skills with router

IDEAL STRUCTURE:
skill-name/
├── SKILL.md (~100-150 lines)
│   ├── Frontmatter + decision tree
│   └── "See references/X.md" pointers
├── references/
│   ├── api.md
│   └── patterns.md
└── scripts/ (optional)
```

## Install Location

Ask user where to install:

- `~/.claude/skills/X/` - User-level (global)
- `.claude/skills/X/` - Project-level (local)

## Output & Delivery

All workflows create `.zip` in `output/<name>.zip`. Users upload to Claude at https://claude.ai/skills. For other platforms, use `--target` flag.

## Working with This Skill

### Beginners

1. Run installation check (`command -v skill-seekers`)
2. If not installed, follow `references/setup.md` (auto-detects uv/venv/pip)
3. Start with a preset: `skill-seekers scrape --config configs/react.json --enhance-local`
4. Package: `skill-seekers package output/react/`

### Intermediate

- Use unified multi-source for comprehensive skills (docs + code + PDF)
- Enable async mode for docs over 500 pages
- Use `--enhance-local` (no API key) or `--enhance` (with `ANTHROPIC_API_KEY`) for AI improvement
- Export to multiple LLM platforms with `--target`

### Advanced

- Split 10K+ page docs with router strategy for parallel scraping
- Use three-stream GitHub analysis (code + docs + insights) via Python API
- Configure GitHub profiles for private repos: `skill-seekers config --github`
- Resume interrupted scrapes: `skill-seekers scrape --config config.json --resume`
- Custom endpoint support: set `ANTHROPIC_BASE_URL` for GLM-4.7 compatible APIs

For troubleshooting, see `references/advanced-commands.md` or `references/troubleshooting.md`.

## Reference Files

| File                                 | Content                                                     |
| ------------------------------------ | ----------------------------------------------------------- |
| `references/setup.md`                | Installation with uv/venv/pip auto-detection                |
| `references/advanced-commands.md`    | Large docs, async, three-stream, splitting, troubleshooting |
| `references/advanced-workflows.md`   | Unified multi-source config, enhancement options            |
| `references/troubleshooting.md`      | Installation issues, runtime errors, CSS selectors          |
| `references/skill-seekers-readme.md` | Full Skill_Seekers v2.7.4 feature matrix                    |
| `scripts/enhance-workaround.sh`      | Fix for broken `skill-seekers enhance` CLI invocation       |

## Routing Summary

| Intent                                 | Route To          | Action                                            |
| -------------------------------------- | ----------------- | ------------------------------------------------- |
| "codify docs", "convert docs to skill" | Codifier pipeline | Prior art → extract → enhance → package → install |
| "skill from GitHub repo"               | Codifier pipeline | Prior art → github → enhance → package → install  |
| "skill from PDF"                       | Codifier pipeline | Prior art → pdf → enhance → package → install     |
| "combine docs + code + PDF"            | Codifier pipeline | Prior art → unified → enhance → package → install |
| "make a skill", "new skill"            | skill-creator     | Author with standards                             |
| "combine skills", "merge skills"       | Both              | Analyze + author                                  |
| "export for Gemini/ChatGPT"            | Codifier pipeline | Package with `--target` flag                      |
| "enhance skill"                        | Enhance step      | Run enhance workaround (pipe to claude -p)        |
| "codify X" (ambiguous)                 | Ask clarification | Docs source or new authoring?                     |

For full skill authoring guidance, load the `skill-creator` skill.

## Technique Map

- **Identify scope** — Determine what the skill applies to before executing.
- **Follow workflow** — Use documented steps; avoid ad-hoc shortcuts.
- **Verify outputs** — Check results match expected contract.
- **Handle errors** — Graceful degradation when dependencies missing.
- **Reference docs** — Load references/ when detail needed.
- **Preserve state** — Don't overwrite user config or artifacts.

## Technique Notes

Skill-specific technique rationale. Apply patterns from the skill body. Progressive disclosure: metadata first, body on trigger, references on demand.

## Prompt Architect Overlay

**Role Definition:** Specialist for skill-builder domain. Executes workflows, produces artifacts, routes to related skills when needed.

**Input Contract:** Context, optional config, artifacts from prior steps. Depends on skill.

**Output Contract:** Artifacts, status, next-step recommendations. Format per skill.

**Edge Cases & Fallbacks:** Missing context—ask or infer from workspace. Dependency missing—degrade gracefully; note in output. Ambiguous request—clarify before proceeding.

## Agent Rules for Skill Operations

HARD LEARNED (2026-02-11):
1. NEVER use WebFetch to extract SKILL.md content — it summarizes
2. NEVER use haiku agents for skill installation — they hallucinate content
3. ALWAYS git clone source repo and cp files verbatim
4. ALWAYS verify: head -1 == "---", wc -l matches source
5. NEVER add custom frontmatter if source already has it
